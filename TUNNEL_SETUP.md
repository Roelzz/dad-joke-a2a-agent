# VS Code Dev Tunnel Setup

This document explains how the Dad Joke Agent is configured to work with VS Code dev tunnels.

## Problem

Initially, the VS Code dev tunnel at `https://nkcx4fnm-2009.uks1.devtunnels.ms` couldn't reach the agent, even though `http://localhost:2009` worked fine.

## Root Causes

1. **JWT Middleware Blocking**: The original code used `jwt_authorization_middleware` globally, which blocked all requests including `/health` and other public endpoints.

2. **Host Binding**: The agent was binding to `localhost` which only accepts connections from the same machine, not from external tunnels.

3. **CloudAdapter Configuration**: The `CloudAdapter` needed proper initialization without connection managers for local development.

## Solutions Applied

### 1. Removed Global JWT Middleware

**Before**:
```python
app = Application(middlewares=[jwt_authorization_middleware])
```

**After**:
```python
app = Application()  # No global middleware
```

Public endpoints (`/health`, `/api/card`, `/api/manifest`, `/api/declarative-agent`) now work without authentication.

### 2. Changed Host Binding

**Before**:
```python
run_app(app, host="localhost", port=PORT)
```

**After**:
```python
run_app(app, host="0.0.0.0", port=PORT)
```

This allows external connections (like VS Code tunnels) to reach the server.

### 3. Simplified Message Endpoint

**Before** (using `start_agent_process` with connection manager):
```python
return await start_agent_process(req, agent_app, adapter)
```

**After** (direct adapter call):
```python
return await AGENT_APP.adapter.process(request, AGENT_APP)
```

This avoids the connection manager requirement for local development.

## Current Configuration

### Agent Initialization
```python
AGENT_APP = AgentApplication[TurnState](
    storage=MemoryStorage(),
    adapter=CloudAdapter()  # No connection manager needed for local dev
)
```

### Endpoint Structure
- **Public Endpoints** (no auth):
  - `GET /health` - Health check
  - `GET /api/card` - Adaptive card
  - `GET /api/manifest` - Teams manifest
  - `GET /api/declarative-agent` - Declarative agent definition

- **Bot Framework Endpoint**:
  - `POST /api/messages` - Bot Framework activities
  - `GET /api/messages` - Health check for messages endpoint

## Testing the Tunnel

### Local Testing
```bash
curl http://localhost:2009/health
```

### Tunnel Testing
```bash
curl https://nkcx4fnm-2009.uks1.devtunnels.ms/health
```

Both should return:
```json
{"status": "healthy", "agent": "Dad Joke Agent"}
```

## VS Code Tunnel Setup

1. **In VS Code**: Forward port 2009
2. **Access Type**: Public (for external access) or Private (for authenticated access)
3. **Tunnel URL**: Will be something like `https://[random]-2009.uks1.devtunnels.ms`

## For Production Deployment

When deploying to production:

1. **Add Authentication**: Implement proper JWT authentication for `/api/messages`
2. **Change Host Binding**: Can keep `0.0.0.0` or use specific IP
3. **Connection Manager**: Configure proper `Connections` object with Azure Bot Service credentials
4. **HTTPS**: Use proper SSL certificates (Azure handles this automatically)

## Environment Variables

```.env
PORT=2009
OPENAI_API_KEY=your-key-here
```

## Troubleshooting

### Tunnel Returns Empty Response
- Check if agent is running: `lsof -i:2009`
- Check host binding is `0.0.0.0`
- Restart VS Code tunnel

### Tunnel Returns 500 Error
- Check agent logs for errors
- Verify CloudAdapter is initialized correctly
- Check that all JSON files exist (agent-card.json, etc.)

### Port Already in Use
```bash
# Kill process on port
lsof -ti:2009 | xargs kill -9

# Then restart agent
uv run python main.py
```

## Security Notes

- Current setup is for **local development only**
- Public endpoints have no authentication
- For production, add proper authentication middleware
- VS Code tunnels provide some built-in authentication, but add your own for sensitive endpoints

## Related Files

- `main.py` - Main agent implementation
- `.env` - Environment configuration
- `agent-card.json` - Adaptive card definition
- `agent-manifest.json` - Teams manifest
- `declarative-agent.json` - Copilot Studio definition
