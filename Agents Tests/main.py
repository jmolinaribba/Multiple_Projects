from smolagents import CodeAgent, LiteLLMModel

# 1. Initialize the model
model = LiteLLMModel(
    model_id="ollama_chat/qwen2:7b",
    api_base="http://127.0.0.1:11434",
    num_ctx=8192,
)

# 2. Initialize a simple agent with the model
agent = CodeAgent(tools=[], model=model)

# 3. Ask the agent a question
agent.run("Say hello and tell me a quick joke!")