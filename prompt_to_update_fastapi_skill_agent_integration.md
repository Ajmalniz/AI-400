# Prompt to Update FastAPI Skill with Agent Integration Content

**Update my FastAPI skill at `.claude/skills/fastapi/` to include comprehensive Agent Integration content based on the Agent Factory documentation.**

## Requirements:

### 1. Create or Enhance references/agent-integration.md

Add comprehensive content including:

- **The Pattern: APIs → Functions → Tools** - How API endpoints become agent-callable functions, table mapping endpoints to operations
- **Creating Tool Functions** - Wrap API endpoints as callable functions, clear docstrings (become tool descriptions), type hints for parameters, return JSON-serializable dicts, manage own sessions
- **Creating the Agent** - Install `openai-agents`, use `@function_tool` decorator, create Agent with name, instructions, tools list
- **Non-Streaming Agent Endpoint** - POST `/agent/chat` endpoint, use `Runner.run()`, return complete response
- **Streaming Agent Endpoint** - POST `/agent/chat/stream`, use `Runner.run_streamed()`, stream events with SSE, extract text from raw_response_event
- **Complete Agent Integration** - Full example with tools.py, agent.py, main.py routes, both streaming and non-streaming endpoints
- **Hands-On Exercise** - Step-by-step: create tools.py, create agent.py, add endpoints, test with natural language requests
- **Common Mistakes** - Forgetting docstrings on tools, returning complex objects instead of dicts, not handling missing resources
- **What You've Achieved** - The complete loop: REST API + agent integration, machine-callable and natural language accessible

### 2. Enhance SKILL.md

Add agent integration section:

```markdown
## Agent Integration

Turn your API endpoints into tools that AI agents can use. This is where FastAPI meets AI agents.

**The pattern:**
1. Your API endpoints define capabilities
2. Wrap them as functions agents can call
3. Create an agent that orchestrates the tools
4. Expose the agent via SSE endpoint

**Basic pattern:**

```python
from agents import Agent, Runner, function_tool

# Wrap API function as tool
@function_tool
def tool_create_task(title: str, description: str | None = None) -> str:
    """Create a new task with the given title."""
    result = create_task(title, description)
    return f"Created task {result['id']}: {result['title']}"

# Create agent with tools
task_agent = Agent(
    name="Task Manager",
    instructions="You help manage tasks.",
    tools=[tool_create_task, tool_list_tasks, ...],
)

# Non-streaming endpoint
@app.post("/agent/chat")
async def chat_with_agent(request: ChatRequest):
    result = await Runner.run(task_agent, request.message)
    return {"response": result.final_output}

# Streaming endpoint
@app.post("/agent/chat/stream")
async def chat_with_agent_stream(request: ChatRequest):
    return EventSourceResponse(agent_stream_generator(request.message))
```

**Key concepts:**
- Tool functions need clear docstrings (become tool descriptions)
- Return JSON-serializable data (dicts, not complex objects)
- Use `@function_tool` decorator to wrap functions
- `Runner.run()` for non-streaming, `Runner.run_streamed()` for streaming
- Connect to SSE streaming from previous lesson

**See [references/agent-integration.md](references/agent-integration.md) for:**
- Complete agent integration guide
- API-to-function-to-tool conversion
- Agent creation with OpenAI Agents SDK
- Streaming and non-streaming endpoints
- Complete working examples
- Common mistakes and best practices
```

### 3. Update references/streaming-sse.md (if exists)

Add connection to agent streaming:

```markdown
## Agent Streaming

SSE streaming is used for agent responses:

**See [references/agent-integration.md](references/agent-integration.md) for:**
- Streaming agent responses with Runner.run_streamed()
- Extracting tokens from raw_response_event
- Complete agent streaming implementation
```

## Style Guidelines:

1. Use `uv add openai-agents` (not pip)
2. Emphasize the pattern: APIs → Functions → Tools → Agent
3. Show complete working examples
4. Include hands-on exercises
5. Common mistakes section
6. Connect to previous lessons (CRUD, streaming)
7. Emphasize docstrings (critical for tool descriptions)
8. All examples must be runnable

## File Locations:

- Main skill: `.claude/skills/fastapi/SKILL.md`
- New/enhanced reference: `.claude/skills/fastapi/references/agent-integration.md`
- Streaming reference: `.claude/skills/fastapi/references/streaming-sse.md` (if exists)

## Important Notes:

- Show the complete pattern: API endpoints → tool functions → agent tools
- Emphasize docstrings on tool functions (agents use these)
- Tool functions should return JSON-serializable data (dicts)
- Show both streaming and non-streaming agent endpoints
- Connect to SSE streaming patterns from previous lesson
- Complete example should show tools.py, agent.py, and main.py
- Mention this completes the loop: REST API + natural language access

---

**After updating, verify:**
1. The APIs → Functions → Tools pattern is clearly explained
2. Tool function creation with docstrings is demonstrated
3. Agent creation with function_tool decorator is shown
4. Non-streaming endpoint with Runner.run() is complete
5. Streaming endpoint with Runner.run_streamed() is complete
6. Complete example with all files is provided
7. Hands-on exercise is actionable
8. Common mistakes are practical
9. Connection to previous lessons (CRUD, streaming) is made
10. Code examples are complete and runnable
