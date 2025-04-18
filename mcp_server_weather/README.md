# Weather MCP Server

A Model Context Protocol server that provides weather forecasts and current weather conditions. This server enables LLMs to access real-time weather data and forecasts using the Open-Meteo API.

### Available Tools

- `get_current_weather` - Get current weather conditions for a specific location.
  - Required arguments:
    - `latitude` (number): Latitude of the location
    - `longitude` (number): Longitude of the location

- `get_forecast` - Get weather forecast for a specific location.
  - Required arguments:
    - `latitude` (number): Latitude of the location
    - `longitude` (number): Longitude of the location


## Build and Run

### Build the Docker image

```bash
# Build the Docker image
docker build -t mcp_server_weather .
```

### Run with Docker

You can run the MCP server directly with:

```bash
# Run in foreground (will stop when you press Ctrl+C)
docker run -i --rm mcp_weather_server

# Or run detached (keeps running in background)
docker run -i -d mcp_weather_server
```

To stop a detached container:

```bash
docker stop mcp_weather_server
```

To interact with a running container:

```bash
docker attach mcp_weather_server
```

## Installation

### Using docker

```json
"mcpServers": {
  "weather": {
    "command": "docker",
    "args": [
        "run",
        "-i",
        "--rm",
        "mcp_server_weather"
    ]
  }
}
```
</details>

