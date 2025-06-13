# Compose agents demo

## Prerequisites

+ Install Docker Desktop `4.41` or a recent `4.42 nightly`

## Demos

Each of these demos is self-contained and can be run either locally or using a cloud context. They are all configured using two steps.

1. change directory to the root of the demo project
1. create a `.mcp.env` file from the `mcp.env.example` file and supply the required MCP tokens
2. run `docker compose up --build`

| Demo | Models | MCPs | project | compose |
| ---- | ---- | ---- | ---- | ---- |
| [Agno](https://github.com/agno-agi/agno) agent that summarizes GitHub issues | deepseek(local), qwen3(local), o3(openai) | github-official, notion, fetch | [project](./demos/agno) | [compose.yaml](./demos/agno/compose.yaml) |
| [Vercel AI-SDK](https://github.com/vercel/ai) Chat-UI for mixing MCPs and Model | llama3.2(local), qwen3(local) | wikipedia-mcp, brave, resend(email) | [project](https://github.com/slimslenderslacks/scira-mcp-chat) | [compose.yaml](https://github.com/slimslenderslacks/scira-mcp-chat/blob/main/compose.yaml) |
| [CrewAI](https://github.com/crewAIInc/crewAI) Marketing Strategy Agent | qwen3(local) | duckduckgo | unmerged | [compose.yaml](https://github.com/docker/compose-agents-demo/blob/alberto/crew-ai/demos/crew-ai/docker-compose.yaml) |
| [ADK](https://github.com/google/adk-python) academic_research agent | TODO | TODO | TODO | TODO | 
| [LangGraph](https://github.com/langchain-ai/langgraph) SQL Agent | TODO | TODO | TODO | TODO | 
| [Embabel](https://github.com/embabel/embabel-agent) Travel Agent | TODO | TODO | TODO | TODO | 

