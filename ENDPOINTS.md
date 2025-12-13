# Dad Joke Agent - API Endpoints

Quick reference guide for all available endpoints.

## Base URL

```
http://localhost:2009
```

## Endpoints

### 1. Bot Framework Message Endpoint

```
POST /api/messages
Content-Type: application/json
Authorization: Bearer <token> (optional for local dev)
```

**Purpose**: Receive and process Bot Framework activities

**Example Activity**:
```json
{
  "type": "message",
  "text": "Tell me a dad joke",
  "from": {
    "id": "user123",
    "name": "Test User"
  },
  "recipient": {
    "id": "bot",
    "name": "Dad Joke Agent"
  },
  "conversation": {
    "id": "test-conversation"
  },
  "channelId": "test"
}
```

**Response**: 200 OK (activity processed asynchronously)

---

### 2. Health Check

```
GET /health
```

**Purpose**: Monitor agent health status

**Example**:
```bash
curl http://localhost:2009/health
```

**Response**:
```json
{
  "status": "healthy",
  "agent": "Dad Joke Agent"
}
```

---

### 3. Agent Card

```
GET /api/card
```

**Purpose**: Retrieve the agent's Adaptive Card for display

**Example**:
```bash
curl http://localhost:2009/api/card
```

**Response**: Adaptive Card JSON (v1.5)

**Use Cases**:
- Display agent information in chat clients
- Show agent capabilities to users
- Provide interactive buttons for common actions

---

### 4. Agent Manifest

```
GET /api/manifest
```

**Purpose**: Retrieve the Teams app manifest

**Example**:
```bash
curl http://localhost:2009/api/manifest
```

**Response**: Teams manifest JSON (v1.16)

**Use Cases**:
- Teams app registration
- Bot configuration discovery
- Command and capability listing

---

### 5. Declarative Agent Definition

```
GET /api/declarative-agent
```

**Purpose**: Retrieve the Copilot Studio declarative agent definition

**Example**:
```bash
curl http://localhost:2009/api/declarative-agent
```

**Response**: Declarative agent JSON (v1.0)

**Use Cases**:
- Copilot Studio agent registration
- Agent-to-agent handoff configuration
- Capability and action discovery

---

## Testing Examples

### Send a Message Activity

```bash
curl -X POST http://localhost:2009/api/messages \
  -H "Content-Type: application/json" \
  -d '{
    "type": "message",
    "text": "Tell me a joke about cats",
    "from": {"id": "user123", "name": "Test User"},
    "recipient": {"id": "bot", "name": "Dad Joke Agent"},
    "conversation": {"id": "test-conv"},
    "channelId": "test"
  }'
```

### Send a Handoff Activity

```bash
curl -X POST http://localhost:2009/api/messages \
  -H "Content-Type: application/json" \
  -d '{
    "type": "handoff",
    "value": {
      "request": "Tell me a programming joke",
      "metadata": {
        "sourceAgent": "copilot-agent-id"
      }
    },
    "from": {"id": "user123", "name": "Test User"},
    "recipient": {"id": "bot", "name": "Dad Joke Agent"},
    "conversation": {"id": "test-conv"},
    "channelId": "copilot"
  }'
```

### Get All Metadata

```bash
# Health check
curl http://localhost:2009/health

# Agent card
curl http://localhost:2009/api/card | jq '.'

# Manifest
curl http://localhost:2009/api/manifest | jq '.'

# Declarative agent
curl http://localhost:2009/api/declarative-agent | jq '.'
```

---

## Integration with Copilot Studio

When integrating with Copilot Studio:

1. **Register the agent** using the declarative agent endpoint:
   ```
   GET http://localhost:2009/api/declarative-agent
   ```

2. **Configure handoff** to point to:
   ```
   POST http://localhost:2009/api/messages
   ```

3. **Test handoff** by sending a handoff activity with the expected context structure

4. **Monitor health** using:
   ```
   GET http://localhost:2009/health
   ```

---

## Error Responses

All endpoints return appropriate HTTP status codes:

- **200 OK**: Request successful
- **404 Not Found**: Endpoint or resource not found
- **500 Internal Server Error**: Server error (check logs)

Example error response:
```json
{
  "error": "Agent card not found",
  "message": "[Errno 2] No such file or directory: 'agent-card.json'"
}
```

---

## Security Notes

- For local development, JWT authorization is optional
- For production, configure proper Azure Bot Service credentials
- All endpoints except `/api/messages` POST are read-only (GET requests)
- The `/api/messages` endpoint should be protected in production with proper authentication

---

## Port Configuration

Default port: **2009**

To change the port, update the `PORT` value in the `.env` file:

```bash
PORT=3978  # Or any available port
```

Then restart the agent.
