# Agent-to-Agent (A2A) Setup for Copilot Studio

## Configuration in Copilot Studio

When setting up the Dad Joke Agent for A2A handoff in Copilot Studio, use the following configuration:

### Step 1: Agent Card URL

When Copilot Studio asks:
> "If your agent card is hosted at a well-known location, enter its full URL..."

**Enter this URL:**
```
https://nkcx4fnm-2009.uks1.devtunnels.ms/.well-known/agent-card.json
```

This provides the visual display information for your agent.

### Step 2: Messaging Endpoint

**IMPORTANT**: Copilot Studio may ask for a separate messaging endpoint or base URL.

**The messaging endpoint should be:**
```
https://nkcx4fnm-2009.uks1.devtunnels.ms/api/messages
```

**OR if it asks for base URL:**
```
https://nkcx4fnm-2009.uks1.devtunnels.ms
```

## Common Issues

### Error 405: Method Not Allowed

If you see error code 405, it means:
- Copilot Studio is sending POST requests to the agent card URL
- The agent card endpoint only accepts GET requests
- You need to configure Copilot Studio to POST to `/api/messages` instead

**Solution**: Make sure you're providing the correct messaging endpoint URL, not the agent card URL.

### How Copilot Studio Calls Your Agent

For A2A handoff, Copilot Studio should:

1. **Discovery** (GET): Fetch agent metadata from the card URL
   - URL: `https://nkcx4fnm-2009.uks1.devtunnels.ms/.well-known/agent-card.json`
   - Method: GET

2. **Messaging** (POST): Send activities to the messaging endpoint
   - URL: `https://nkcx4fnm-2009.uks1.devtunnels.ms/api/messages`
   - Method: POST
   - Content-Type: application/json
   - Body: Bot Framework Activity

## Testing the Endpoints

### Test Agent Card (GET)
```bash
curl https://nkcx4fnm-2009.uks1.devtunnels.ms/.well-known/agent-card.json
```

Should return the Adaptive Card JSON.

### Test Messaging Endpoint (POST)
```bash
curl -X POST https://nkcx4fnm-2009.uks1.devtunnels.ms/api/messages \
  -H "Content-Type: application/json" \
  -d '{
    "type": "message",
    "text": "Tell me a joke about Philips",
    "from": {"id": "user123", "name": "Test User"},
    "recipient": {"id": "bot", "name": "Dad Joke Agent"},
    "conversation": {"id": "test-conv"},
    "channelId": "copilot-studio"
  }'
```

Should return 200 OK and the agent should respond with a dad joke.

## Alternative Discovery Endpoints

If Copilot Studio needs more metadata, you can also provide:

### Declarative Agent Definition
```
https://nkcx4fnm-2009.uks1.devtunnels.ms/api/declarative-agent
```

This includes full capability definitions and A2A protocol information.

### Agent Discovery Document
```
https://nkcx4fnm-2009.uks1.devtunnels.ms/.well-known/agent-discovery.json
```

This provides comprehensive A2A metadata including all endpoints.

## Expected Handoff Flow

1. **User asks Copilot Studio agent for a dad joke**
2. **Copilot Studio initiates handoff**:
   - Sends POST to `https://nkcx4fnm-2009.uks1.devtunnels.ms/api/messages`
   - Activity type: `message`, `handoff`, `event`, or `invoke`
   - Contains handoff context with user request

3. **Dad Joke Agent receives and processes**:
   - Parses the activity
   - Extracts joke request from context
   - Generates or selects appropriate dad joke
   - Returns response

4. **User receives dad joke** from the Dad Joke Agent

## Debugging

Enable the agent with logging:
```bash
cd A365SDK-Dad
env PYTHONUNBUFFERED=1 uv run python main.py
```

Watch the logs for:
- `🌐 POST /api/messages` - Correct messaging calls
- `🌐 POST /.well-known/agent-card.json` - **WRONG** (indicates misconfiguration)
- `📨 INCOMING REQUEST` - Full request details
- `✅ Request processed successfully` - Successful processing
- `❌ ERROR PROCESSING MESSAGE` - Errors with stack traces

## Recommended Configuration

In Copilot Studio's A2A agent configuration:

| Field | Value |
|-------|-------|
| **Agent Card URL** | `https://nkcx4fnm-2009.uks1.devtunnels.ms/.well-known/agent-card.json` |
| **Base URL** or **Messaging Endpoint** | `https://nkcx4fnm-2009.uks1.devtunnels.ms/api/messages` |
| **Agent ID** | `dad-joke-agent-365` |
| **Display Name** | `Dad Joke Agent` |
