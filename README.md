# Compose agents demo

## Prerequisites

+ Install Docker Desktop `4.41` or a recent `4.42 nightly`

## Demos

Each of these demos is self-contained and can be run either locally or using a cloud context. They are all configured using two steps.

1. change directory to the root of the demo project
1. create a `.mcp.env` file from the `mcp.env.example` file (if it exists, otherwise the demo doesn't need any secrets) and supply the required MCP tokens
2. run `docker compose up --build`

| Demo | Models | MCPs | project | compose |
| ---- | ---- | ---- | ---- | ---- |
| [Agno](https://github.com/agno-agi/agno) agent that summarizes GitHub issues | deepseek(local), qwen3(local), o3(openai) | github-official, notion, fetch | [./demos/agno](./demos/agno) | [compose.yaml](./demos/agno/compose.yaml) |
| [Vercel AI-SDK](https://github.com/vercel/ai) Chat-UI for mixing MCPs and Model | llama3.2(local), qwen3(local) | wikipedia-mcp, brave, resend(email) | [Repository](https://github.com/slimslenderslacks/scira-mcp-chat) | [compose.yaml](https://github.com/slimslenderslacks/scira-mcp-chat/blob/main/compose.yaml) |
| [CrewAI](https://github.com/crewAIInc/crewAI) Marketing Strategy Agent | qwen3(local) | duckduckgo | [./demos/crew-ai](./demos/crew-ai) | [compose.yaml](https://github.com/docker/compose-agents-demo/blob/main/demos/crew-ai/compose.yaml) |
| [ADK](https://github.com/google/adk-python) academic_research agent | gemma3-qat(local) | duckduckgo | [./demos/adk](./demos/adk) | [compose.yaml](./demos/adk/compose.yaml) | 
| [LangGraph](https://github.com/langchain-ai/langgraph) SQL Agent | qwen3(local) | postgres | [./demos/langgraph](./demos/langgraph) | [compose.yaml](./demos/langgraph/compose.yaml) |
| [Embabel](https://github.com/embabel/embabel-agent) Travel Agent | qwen3, Claude3.7, llama3.2 | brave, github-official, wikipedia-mcp, weather, google-maps | [Repository](https://github.com/embabel/travel-planner-agent) | [compose.yaml](https://github.com/slimslenderslacks/travel-planner-agent/blob/slim/compose/compose.yaml) and [compose.dmr.yaml](https://github.com/slimslenderslacks/travel-planner-agent/blob/slim/compose/compose.dmr.yaml) |

* the embabel demo merges two compose files at runtime. This is because it also supports an Ollama configuration so there is a compose.ollama.yaml file and a compose.dmr.yaml file.
