import asyncio
import platform
import datetime
from typing import Any
import json
import fire
import yaml
from metagpt.actions import Action, UserRequirement
from metagpt.logs import logger
from metagpt.roles import Role
from metagpt.schema import Message
from metagpt.team import Team

def load_prompt_template(file_path):
    """Loads a prompt template from a YAML file.

    Args:
        file_path (str): The path to the YAML file containing the prompt template.

    Returns:
        str: The loaded prompt template.
    """
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data['PROMPT_TEMPLATE']

class ConveyThoughts(Action):
    PROMPT_TEMPLATE: str = load_prompt_template('prompt_template.yaml')
    name: str = "ConveyThoughts"

    async def run(self, context: str, name: str, opponent_name: str):
        """Generates a thoughtful response in a debate context.

        Args:
            context (str): The current debate history.
            name (str): The name of the participant generating the response.
            opponent_name (str): The name of the debate opponent.

        Returns:
            str: The generated response.
        """
        prompt = self.PROMPT_TEMPLATE.format(context=context, name=name, opponent_name=opponent_name)
        rsp = await self._aask(prompt)
        return rsp


class Participants(Role):
    name: str = ""
    profile: str = ""
    opponent_name: str = ""

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.set_actions([ConveyThoughts])
        self._watch([UserRequirement, ConveyThoughts])

    async def _observe(self) -> int:
        """Filters incoming messages and updates the newsfeed.

        Returns:
            int: The number of new messages received.
        """
        await super()._observe()
        # accept messages sent (from opponent) to self, disregard own messages from the last round
        self.rc.news = [msg for msg in self.rc.news if msg.send_to == {self.name}]
        return len(self.rc.news)

    async def _act(self) -> Message:
        """Generates a debate response, logs timestamps, and calculates speaking time.

        Returns:
            Message: The generated message object.
        """
        logger.info(f"{self._setting}: Now Speaking... {self.rc.todo}({self.rc.todo.name})")
        todo = self.rc.todo  # An instance of ConveyThoughts

        memories = self.get_memories()
        context = "\n".join(f"{msg.sent_from}: {msg.content}" for msg in memories)

        start_time = datetime.datetime.now()
        rsp = await todo.run(context=context, name=self.name, opponent_name=self.opponent_name)
        end_time = datetime.datetime.now()

        # Calculate speaking time
        speaking_time = end_time - start_time
        speaking_time_seconds = speaking_time.total_seconds()  # Get duration in seconds

        # Generate the timestamp
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        msg = Message(
            content=f"[{current_time}] {rsp}",
            role=self.profile,
            cause_by=type(todo),
            sent_from=self.name,
            send_to=self.opponent_name,
        )
        self.rc.memory.add(msg)

        print("-------------------")
        print(f"{self.name} spoke for {speaking_time_seconds:.2f} seconds")  # Display speaking time

        return msg


async def debate(idea: str, investment: float = 3.0, n_round: int = 5):
    """Orchestrates a multi-round debate between two participants.

    Args:
        idea (str): The topic of the debate.
        investment (float, optional): The amount of investment (likely computational resources). Defaults to 3.0.
        n_round (int, optional): The number of debate rounds. Defaults to 5.
    """
    with open('participants.json', 'r') as file:
        participants = json.load(file)

    debator1 = Participants(**participants['debator1'])
    debator2 = Participants(**participants['debator2'])

    team = Team()
    team.hire([debator1, debator2])
    team.invest(investment)
    team.run_project(idea, send_to=debator1.name)
    await team.run(n_round=n_round)

def main(idea: str, investment: float = 3.0, n_round: int = 10):

    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(debate(idea, investment, n_round))


if __name__ == "__main__":
    fire.Fire(main)