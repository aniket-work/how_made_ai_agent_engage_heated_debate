# how_made_ai_agent_engage_heated_debate
how_made_ai_agent_engage_heated_debate

## Setting Up how_made_ai_agent_engage_heated_debate Environment

To set up the `how_made_ai_agent_engage_heated_debate` environment, follow these steps:

Note : Make sure Neo4J DB is running locally. 

1. Create a virtual environment using Python's built-in `venv` module:

    ```bash
    python -m venv how_made_ai_agent_engage_heated_debate
    ```

2. Activate the virtual environment:

    - On Windows:

        ```bash
        how_made_ai_agent_engage_heated_debate\Scripts\activate
        ```

    - On Unix or MacOS:

        ```bash
        source how_made_ai_agent_engage_heated_debate/bin/activate
        ```

3. Install npm & check after install by - "npm --version"
4. Install mermaid 
   ```bash
   npm install -g @mermaid-js/mermaid-cli
   ```
5. install ollama 
6. install mistral in ollama
   ```bash
   ollama run mistral
   ```
7. Configure model
   ```bash
   (how_made_ai_agent_engage_heated_debate) ~\PycharmProjects\how_made_ai_agent_engage_heated_debate>metagpt --init-config
   ```
8. Add model  at ~\.metagpt\config2.yaml
9. Let's start the debate

   ```bash
   python start_debate.py --idea="Talk about how world should develop Artificial intelligence"
   ```
