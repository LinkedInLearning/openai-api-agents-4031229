# COURSENAME

This is the repository for the LinkedIn Learning course `OpenAI Agents SDK`. The full course is available from [LinkedIn Learning][lil-course-url].

![lil-thumbnail-url]

## Course Description

AI agents generate plans and perform complex multi-step tasks based on the user input. The OpenAI API provides comprehensive support for building AI agents that use models, tools, knowledge and memory, audio and speech, guardrails, orchestration, and MCP that can be customized to fit specific needs and scenarios. This course explores how to develop advanced agents with the OpenAI API and the Agents Python SDK. Through videos, articles, and hands-on practice in GitHub Codespaces you’ll define custom agents, set up agent runners, configure handoffs so agents can work together, add guardrails for content moderation, and extend the agents with off-the-shelf OpenAI features, custom functions, and MCP (Model Context Protocol) servers.

_See the readme file in the main branch for updated instructions and information._

## Instructions

This repository has three main folders:

- `./adventurebot/`: The folder you'll work with
- `./mcp_server_weather/`: An MCP Server you'll incorporate into the project
- `./adventurebot-advanced/`: An alternate version of the Adventurebot agent, for reference

To start developing, install all dependencies:

```bash
pip install -r requirements.txt
```

### Authentication

You need an OpenAI API key to run the Agents SDK. Get your key at [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)

To use the API key, either install the key into your environment:

```bash
export OPENAI_API_KEY=<your-key-here>
```

or create a `.env` file in the root with the value:

```json
OPENAI_API_KEY=<your-key-here>
```

## Instructor

Morten Rand-Hendriksen

Principal Staff Instructor, Speaker, Web Designer, and Software Developer

Check out my other courses on [LinkedIn Learning](https://www.linkedin.com/learning/instructors/morten-rand-hendriksen?u=104).

[0]: # "Replace these placeholder URLs with actual course URLs"
[lil-course-url]: https://www.linkedin.com/learning/openai-api-agents
[lil-thumbnail-url]: https://media.licdn.com/dms/image/v2/D4D0DAQEU-kFfzkcqxQ/learning-public-crop_675_1200/B4DZZfMIffH4Ac-/0/1745353738505?e=2147483647&v=beta&t=c9Qm7OEErMfUXJci9vKF1IjJxW2DYlAO6JWg2JFDv30
