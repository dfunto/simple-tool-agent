# simple-tool-agent
Learning project that creates an agent capable of using external tools

## Setup

Download Llama model first

```shell
docker-compose up -d llm
docker-compose exec llm ollama pull llama3.1
```

## Using the Agent

```shell
docker-compose run --rm backend
```