# Complete Setup Guide

This guide covers everything you need to get the Dad Joke Agent running locally and integrated with Copilot Studio.

## Table of Contents

1. [Local Development Setup](#local-development-setup)
2. [Environment Configuration](#environment-configuration)
3. [Running the Agent](#running-the-agent)
4. [Testing Locally](#testing-locally)
5. [VS Code Dev Tunnel Setup](#vs-code-dev-tunnel-setup)
6. [Copilot Studio Integration](#copilot-studio-integration)
7. [Production Deployment](#production-deployment)

---

## Local Development Setup

### Prerequisites

- **Python 3.9+** - Check your version:
  ```bash
  python --version
  ```

- **uv package manager** - Install if needed:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

- **(Optional) OpenAI API Key** - Get one from [platform.openai.com](https://platform.openai.com/api-keys)

### Installation Steps

1. **Navigate to the project**:
   ```bash
   cd "Dad joke Agent example"
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

   This creates a virtual environment and installs all required packages.

3. **Verify installation**:
   ```bash
   uv run python -c "import microsoft_agents; print('✅ SDK installed')"
   ```

---

## Environment Configuration

### Create Your .env File

1. **Copy the example**:
   ```bash
   cp .env.example .env
   ```

2. **Edit .env** with your preferred editor:
   ```bash
   # For nano
   nano .env

   # For VS Code
   code .env
   ```

3. **Configure the variables**:

   ```env
   # Optional: OpenAI API key for custom topic jokes
   # Without this, the agent uses random jokes from the built-in collection
   OPENAI_API_KEY=sk-your-actual-key-here

   # Server port (default: 2009)
   PORT=2009

   # Base URL - UPDATE THIS based on your environment:

   # For local development:
   BASE_URL=http://localhost:2009

   # For VS Code dev tunnel (update with your tunnel URL):
   # BASE_URL=https://abc123-2009.uks1.devtunnels.ms

   # For production (update with your domain):
   # BASE_URL=https://your-agent.yourdomain.com
   ```

### Important Notes

- **Never commit .env** - It's already in `.gitignore`
- **BASE_URL is critical** - All JSON manifests use this to generate URLs
- **Port must match** - If you change PORT, update BASE_URL accordingly

---

## Running the Agent

### Start the Server

```bash
uv run python main.py
```

**Expected output**:
```
🤣 Dad Joke Agent Starting...
📡 Listening on http://localhost:2009/api/messages
🔑 OpenAI Integration: Enabled (or Disabled)

Press Ctrl+C to stop the agent
```

### Verify It's Running

Open a new terminal and test the health endpoint:

```bash
curl http://localhost:2009/health
```

**Expected response**:
```json
{"status": "healthy", "agent": "Dad Joke Agent"}
```

---

## Testing Locally

### Option 1: Teams App Test Tool (Recommended)

1. **Install the test tool**:
   ```bash
   npm install -g @microsoft/teams-app-test-tool
   ```

2. **Start the test tool**:
   ```bash
   teamsapptester
   ```

3. **Open the web interface**:
   - Browser opens automatically at `http://localhost:56150`
   - Or navigate there manually

4. **Configure the connection**:
   - Endpoint URL: `http://localhost:2009/api/messages`
   - Click "Connect"

5. **Test the agent**:
   - Type: "Tell me a dad joke"
   - Try: "/help"
   - Test topic jokes: "Joke about cats" (requires OpenAI)

### Option 2: Direct API Testing with curl

**Send a message activity**:
```bash
curl -X POST http://localhost:2009/api/messages \
  -H "Content-Type: application/json" \
  -d '{
    "type": "message",
    "text": "Tell me a dad joke",
    "from": {"id": "user123", "name": "Test User"},
    "recipient": {"id": "bot", "name": "Dad Joke Agent"},
    "conversation": {"id": "test-conv"},
    "channelId": "test"
  }'
```

**Test handoff activity**:
```bash
curl -X POST http://localhost:2009/api/messages \
  -H "Content-Type: application/json" \
  -d '{
    "type": "handoff",
    "value": {
      "request": "Tell me a programming joke"
    },
    "from": {"id": "user123"},
    "recipient": {"id": "bot"},
    "conversation": {"id": "test-conv"},
    "channelId": "copilot"
  }'
```

---

## VS Code Dev Tunnel Setup

Dev tunnels expose your local agent to the internet for external testing and Copilot Studio integration.

### Enable Port Forwarding

1. **In VS Code**, open the "Ports" panel (View → Ports)

2. **Forward port 2009**:
   - Click "Forward a Port"
   - Enter: `2009`
   - Press Enter

3. **Make it public**:
   - Right-click the port
   - Select "Port Visibility" → "Public"

4. **Copy the tunnel URL**:
   - Look for something like: `https://abc123-2009.uks1.devtunnels.ms`
   - Copy this URL

### Update Your Configuration

1. **Edit .env**:
   ```env
   BASE_URL=https://abc123-2009.uks1.devtunnels.ms
   ```

2. **Restart the agent**:
   ```bash
   # Stop with Ctrl+C
   uv run python main.py
   ```

### Test the Tunnel

```bash
curl https://abc123-2009.uks1.devtunnels.ms/health
```

Should return the same health check response.

### Troubleshooting Tunnels

**Problem**: Tunnel returns empty response
- **Solution**: Ensure agent is binding to `0.0.0.0` (already configured in `main.py`)

**Problem**: Tunnel returns 502 Bad Gateway
- **Solution**: Agent isn't running - start it with `uv run python main.py`

**Problem**: URLs in JSON files still show localhost
- **Solution**: Restart the agent after updating `.env` - URLs are generated at startup

---

## Copilot Studio Integration

See [A2A_SETUP.md](./A2A_SETUP.md) for complete Copilot Studio configuration.

### Quick Start

1. **Ensure tunnel is running** (see previous section)

2. **In Copilot Studio**:
   - Create a new agent or edit existing
   - Add "Agent-to-Agent" capability
   - When prompted for agent card URL, enter:
     ```
     https://your-tunnel-url/.well-known/agent-card.json
     ```

3. **Configure messaging endpoint**:
   - If asked separately, provide:
     ```
     https://your-tunnel-url/api/messages
     ```

4. **Test the handoff**:
   - In Copilot Studio, configure a topic to hand off to your agent
   - Test in the chat interface

### Common Issues

**Error 405: Method Not Allowed**
- You're using the card URL for messaging
- Use `/api/messages` for POST requests, not the card URL

**Error 404: Not Found**
- Check that your tunnel URL is correct
- Verify the agent is running
- Test the health endpoint first

---

## Production Deployment

### Azure Bot Service Setup

1. **Register your bot** in Azure Bot Service
2. **Get credentials**: App ID and App Password
3. **Update code** to use proper authentication (currently using SimpleCredentialProvider)

### Environment Configuration

```env
# Production settings
OPENAI_API_KEY=your-production-key
PORT=443  # or 80
BASE_URL=https://your-domain.com

# Azure Bot Service (when ready)
MICROSOFT_APP_ID=your-app-id
MICROSOFT_APP_PASSWORD=your-app-password
```

### Deployment Checklist

- [ ] Remove SimpleCredentialProvider, use proper Azure credentials
- [ ] Configure HTTPS with valid SSL certificate
- [ ] Set up proper logging and monitoring
- [ ] Configure rate limiting
- [ ] Test all endpoints with production URLs
- [ ] Update all manifest files with production BASE_URL
- [ ] Set up CI/CD pipeline
- [ ] Configure backup and disaster recovery
- [ ] Document production architecture
- [ ] Set up alerts for errors and downtime

### Hosting Options

1. **Azure App Service** - Recommended for Microsoft ecosystem
2. **Azure Container Instances** - For Docker deployments
3. **Azure Kubernetes Service** - For scalable production
4. **Any Python hosting** - Works anywhere Python AIOHTTP runs

---

## Next Steps

- **[A2A_SETUP.md](./A2A_SETUP.md)** - Configure Copilot Studio integration
- **[ENDPOINTS.md](./ENDPOINTS.md)** - Explore all available endpoints
- **[PROTOCOL.md](./PROTOCOL.md)** - Understand protocol compliance
- **[ICONS.md](./ICONS.md)** - Create custom icons for your agent

## Getting Help

- Check logs in the terminal where agent is running
- Look for `🌐`, `📨`, `✅`, or `❌` emoji indicators
- Review the error messages for specific issues
- Consult individual documentation files for detailed topics
