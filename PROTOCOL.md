# Protocol Compliance Documentation

## Microsoft 365 Agents SDK Activity Protocol

This document details how the Dad Joke Agent implements the Microsoft 365 Agents SDK Activity Protocol and Agent-to-Agent (A2A) Protocol for Copilot Studio integration.

## Activity Protocol Support

### Supported Activity Types

#### 1. Message Activity (`ActivityTypes.message`)
- **Purpose**: Handle incoming user messages and respond with dad jokes
- **Implementation**: `main.py:77-98`
- **Features**:
  - Text message processing
  - Command detection (`/help`)
  - Random joke delivery
  - Topic-based joke generation (with OpenAI)

**Example Activity**:
```json
{
  "type": "message",
  "text": "Tell me a dad joke",
  "from": {
    "id": "user-id",
    "name": "User Name"
  },
  "recipient": {
    "id": "bot-id",
    "name": "Dad Joke Agent"
  }
}
```

#### 2. Conversation Update Activity (`ActivityTypes.conversation_update`)
- **Purpose**: Handle user join/leave events
- **Implementation**: `main.py:100-110`
- **Features**:
  - Welcome messages for new users
  - Bot identity detection (avoids self-greeting)

**Example Activity**:
```json
{
  "type": "conversationUpdate",
  "membersAdded": [
    {
      "id": "user-id",
      "name": "User Name"
    }
  ]
}
```

#### 3. Event Activity (`ActivityTypes.event`)
- **Purpose**: Handle system events including handoffs
- **Implementation**: `main.py:112-127`
- **Features**:
  - Event name routing
  - Handoff event detection (`name: "handoff"`)
  - Generic event echo for debugging

**Example Activity**:
```json
{
  "type": "event",
  "name": "handoff",
  "value": {
    "request": "Tell me a joke about cats",
    "metadata": {}
  }
}
```

#### 4. Handoff Activity (`type: "handoff"`)
- **Purpose**: Receive agent-to-agent handoff from Copilot Studio
- **Implementation**: `main.py:129-166`
- **Features**:
  - Context extraction
  - Multiple field name support
  - Error handling
  - Acknowledgment messages
  - Request processing

**Example Activity**:
```json
{
  "type": "handoff",
  "value": {
    "request": "joke about programming",
    "message": "User wants a programming joke",
    "metadata": {
      "sourceAgent": "copilot-agent-id"
    }
  }
}
```

#### 5. Invoke Activity (`ActivityTypes.invoke`)
- **Purpose**: Handle skill invocation from Copilot Studio
- **Implementation**: `main.py:168-204`
- **Features**:
  - Standard A2A handoff invoke support
  - Invoke response generation
  - Error response handling

**Example Activity**:
```json
{
  "type": "invoke",
  "name": "application/vnd.microsoft.activity.handoff",
  "value": {
    "request": "Tell me a dad joke"
  }
}
```

**Example Response**:
```json
{
  "type": "invokeResponse",
  "value": {
    "status": 200,
    "body": {
      "message": "Invoke received by Dad Joke Agent",
      "invokeName": "application/vnd.microsoft.activity.handoff"
    }
  }
}
```

## Agent-to-Agent (A2A) Protocol

### Handoff Context Schema

The agent supports multiple handoff context field names for maximum compatibility:

```typescript
interface HandoffContext {
  // Primary field (recommended)
  request?: string;

  // Alternative fields (for compatibility)
  message?: string;
  userMessage?: string;
  text?: string;

  // Optional metadata
  metadata?: {
    sourceAgent?: string;
    conversationId?: string;
    timestamp?: string;
    [key: string]: any;
  };
}
```

### Handoff Flow

1. **Receive Handoff**: Agent receives either:
   - `type: "handoff"` activity
   - `type: "event"` with `name: "handoff"`
   - `type: "invoke"` with `name: "application/vnd.microsoft.activity.handoff"`

2. **Extract Context**: Parse handoff context from `activity.value`

3. **Acknowledge**: Send welcome message to user

4. **Process Request**: If context contains a request, generate and deliver joke

5. **Error Handling**: Catch errors and provide fallback response

### A2A Compliance Checklist

- ✅ Accepts handoff activities
- ✅ Extracts handoff context
- ✅ Supports multiple context field names
- ✅ Sends acknowledgment messages
- ✅ Processes embedded requests
- ✅ Handles invoke activities
- ✅ Returns invoke responses
- ✅ Error handling with graceful degradation
- ✅ Logging for debugging
- ✅ Multiple handoff activity type support

## Adapter Configuration

### CloudAdapter Setup
- **Implementation**: `main.py:238-248`
- **Features**:
  - SimpleCredentialProvider for local testing
  - CloudAdapterConfig with connector options
  - Activity processing pipeline
  - Authorization header validation

### API Endpoints

The agent exposes the following endpoints:

#### 1. Message Endpoint
- **URL**: `POST /api/messages`
- **Purpose**: Main endpoint for Bot Framework activity processing
- **Features**:
  - Activity deserialization
  - Auth header extraction via JWT middleware
  - Adapter processing with `start_agent_process`
  - Error response handling

#### 2. Health Check
- **URL**: `GET /health`
- **Purpose**: Health monitoring endpoint
- **Response**: `{"status": "healthy", "agent": "Dad Joke Agent"}`

#### 3. Agent Card
- **URL**: `GET /api/card`
- **Purpose**: Serves the Adaptive Card for agent discovery
- **Response**: Complete Adaptive Card JSON schema
- **Use Case**: Display agent information in Copilot Studio, Teams, or other clients

#### 4. Agent Manifest
- **URL**: `GET /api/manifest`
- **Purpose**: Serves the Teams app manifest
- **Response**: Complete Teams manifest (v1.16) with bot configuration
- **Use Case**: Teams app registration and configuration

#### 5. Declarative Agent
- **URL**: `GET /api/declarative-agent`
- **Purpose**: Serves the Copilot Studio declarative agent definition
- **Response**: Complete declarative agent schema with capabilities and handoff configuration
- **Use Case**: Copilot Studio agent registration and discovery

## Testing Compliance

### Activity Protocol Testing

1. **Message Activity**:
```bash
curl -X POST http://localhost:2009/api/messages \
  -H "Content-Type: application/json" \
  -d '{
    "type": "message",
    "text": "Tell me a dad joke"
  }'
```

2. **Handoff Activity**:
```bash
curl -X POST http://localhost:2009/api/messages \
  -H "Content-Type: application/json" \
  -d '{
    "type": "handoff",
    "value": {
      "request": "joke about cats"
    }
  }'
```

3. **Invoke Activity**:
```bash
curl -X POST http://localhost:2009/api/messages \
  -H "Content-Type: application/json" \
  -d '{
    "type": "invoke",
    "name": "application/vnd.microsoft.activity.handoff",
    "value": {
      "request": "Tell me a joke"
    }
  }'
```

## Manifest Files

### Required Files
1. **agent-manifest.json**: Teams app manifest with bot configuration
2. **declarative-agent.json**: Copilot Studio declarative agent definition
3. **agent-card.json**: Adaptive card for agent display

### Manifest Compliance
- ✅ Activity types declared
- ✅ Handoff capability specified
- ✅ Commands documented
- ✅ Scopes defined (personal, team, groupchat)
- ✅ Bot ID configured
- ✅ Endpoints specified

## Security Considerations

### Authentication
- Uses SimpleCredentialProvider for local development
- Production should use proper app ID and password
- Authorization header validation in adapter

### Input Validation
- Text message sanitization
- Context field validation
- Error handling for malformed activities
- Safe JSON parsing

## Production Deployment Checklist

- [ ] Replace SimpleCredentialProvider with production credentials
- [ ] Configure proper app ID and password in Azure Bot Service
- [ ] Update manifest with production bot ID
- [ ] Set up proper SSL/TLS certificates
- [ ] Configure logging and monitoring
- [ ] Test handoff with actual Copilot Studio agents
- [ ] Validate invoke response handling
- [ ] Test error scenarios
- [ ] Update endpoints in manifest files
- [ ] Configure rate limiting

## References

- Microsoft Bot Framework Activity Schema
- Microsoft 365 Agents SDK Documentation
- Copilot Studio Agent-to-Agent Protocol
- Adaptive Cards Schema v1.5
- Teams App Manifest v1.16
