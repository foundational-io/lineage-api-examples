# Lineage API Examples

This repository contains example code for using the Foundational Lineage API. You can run the examples either directly on your local machine or within a Docker container.

## Getting Started

### Clone the Repository
To get started, clone this repository to your local machine:
```sh
git clone https://github.com/foundational-io/lineage-api-examples.git
cd lineage-api-examples
```

### Create an API Token
Before running the examples, you need an API token. Follow the instructions here to generate your API key:
[Creating an API Token](https://docs.foundational.io/en/articles/9920307-creating-api-token)

### Configure Your API Credentials
Update the following variables in the `main.py` file under `hello_lineage_graph` folder:
```python
ENTITY_NAME = "table_name_to_search_for"
API_KEY_ID = "your_api_key_id"
API_KEY_SECRET = "your_api_key_secret"
```

## Running the Example Code
You can run the example in two ways: directly on your machine or within Docker.

### Option 1: Run Without Docker
1. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Run the example script:
   ```sh
   python hello_lineage_graph/main.py
   ```

### Option 2: Run Within Docker
1. Build the Docker image:
   ```sh
   docker build -t lineage-api-example .
   ```
2. Run the container:
   ```sh
   docker run --rm lineage-api-example
   ```

### Option 3: Use MCP Server
This repository includes an MCP server implementation that provides convenient access to the Foundational API. To use it:

1. Install the MCP package:
   ```sh
   pip install mcp
   ```

2. Test that the server is running correctly by executing:
   ```sh
   mcp run /path/to/lineage-api-examples/mcp/foundational_mcp_server.py
   ```

3. Configure the MCP server in your AI assistant settings (e.g., Claude). Add the following configuration, replacing the paths and API credentials with your own:
   ```json
   {
     "mcpServers": {
       "FoundationalRamp": {
         "command": "/path/to/your/python/mcp",
         "args": [
           "run",
           "/path/to/lineage-api-examples/mcp/foundational_mcp_server.py"
         ],
         "env": {
           "FOUNDATIONAL_API_KEY": "your-api-key",
           "FOUNDATIONAL_API_SECRET": "your-api-secret"
         }
       }
     },
     "globalShortcut": ""
   }
   ```

The MCP server provides tools for searching entities, getting entity details, and exploring upstream/downstream dependencies through your AI assistant.

## Additional Resources
- Learn more about the API: [Getting Started with the Lineage API](https://docs.foundational.io/en/articles/10067204-getting-started-with-the-lineage-api)
- Explore the OpenAPI documentation: [API Reference](https://api.foundational.io/api/v1/docs)

## Support
If you have any questions, please contact [support@foundational.io](mailto:support@foundational.io).

