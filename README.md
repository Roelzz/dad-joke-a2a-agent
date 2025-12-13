# Dad Joke Agent - Microsoft 365 Agents SDK

A demonstration agent built with the Microsoft 365 Agents SDK that delivers dad jokes on demand. Fully compliant with the Activity Protocol and Agent-to-Agent (A2A) communication for Copilot Studio integration.

## ✨ Features

- **Random Dad Jokes**: Delivers jokes from a curated collection of 15 classic dad jokes
- **AI-Powered Custom Jokes**: Generate topic-specific jokes using OpenAI GPT-3.5-turbo (optional)
- **Full Protocol Support**:
  - Bot Framework Activity Protocol
  - JSON-RPC 2.0 messaging
  - Agent-to-Agent (A2A) handoff
- **Multiple Activity Types**: Message, conversation update, event, handoff, and invoke
- **Discovery Endpoints**: Agent card, manifest, and declarative agent definitions
- **Development Ready**: Works with VS Code dev tunnels and local testing

## 📋 Quick Start

### Prerequisites

- Python 3.9 or newer
- [uv](https://github.com/astral-sh/uv) package manager (recommended) or pip

### Installation

1. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Navigate to the project directory**:
   ```bash
   cd "Dad joke Agent example"
   ```

3. **Install dependencies**:
   ```bash
   uv sync
   ```

4. **Configure environment variables**:

   Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and configure:
   ```env
   # Optional: Add OpenAI API key for custom jokes
   OPENAI_API_KEY=your_openai_api_key_here

   # Server port
   PORT=2009

   # Base URL (update for production or tunnels)
   BASE_URL=http://localhost:2009
   ```

### Running the Agent

Start the agent server:

```bash
uv run python main.py
```

The agent will start on `http://localhost:2009/api/messages`

You should see:
```
🤣 Dad Joke Agent Starting...
📡 Listening on http://localhost:2009/api/messages
🔑 OpenAI Integration: Enabled
```

### Testing

**Check agent health**:
```bash
curl http://localhost:2009/health
```

**Send a message** (using Teams App Test Tool):
```bash
npm install -g @microsoft/teams-app-test-tool
teamsapptester
```

Then open `http://localhost:56150` and connect to `http://localhost:2009/api/messages`

## 🌐 Using with VS Code Dev Tunnels

To expose your local agent for external testing:

1. **Forward port 2009** in VS Code
2. **Make it public**
3. **Copy the tunnel URL** (e.g., `https://abc123-2009.uks1.devtunnels.ms`)
4. **Update `.env`**:
   ```env
   BASE_URL=https://abc123-2009.uks1.devtunnels.ms
   ```
5. **Restart the agent**

See [A2A_SETUP.md](./A2A_SETUP.md) and [TUNNEL_SETUP.md](./TUNNEL_SETUP.md) for detailed instructions.

## 🔌 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/messages` | POST | Main Bot Framework activity endpoint |
| `/api/messages` | GET | Health check for messages endpoint |
| `/health` | GET | General health check |
| `/api/card` | GET | Agent's Adaptive Card |
| `/api/manifest` | GET | Teams app manifest |
| `/api/declarative-agent` | GET | Copilot Studio declarative agent definition |
| `/api/discovery` | GET | Comprehensive A2A metadata |
| `/.well-known/agent-card.json` | GET | Standard agent card endpoint |
| `/.well-known/agent-discovery.json` | GET | Standard discovery endpoint |

See [ENDPOINTS.md](./ENDPOINTS.md) for complete API documentation.

## 💬 Usage Examples

### Basic Requests
- "Tell me a dad joke"
- "Give me a joke"
- "Make me laugh"

### Topic-Specific Requests (requires OpenAI)
- "Tell me a joke about cats"
- "Give me a food joke"
- "Joke about programming"

### Commands
- `/help` - Display help information

## 🔗 Copilot Studio Integration

This agent supports Agent-to-Agent (A2A) handoff from Copilot Studio. See [A2A_SETUP.md](./A2A_SETUP.md) for:
- Configuration steps in Copilot Studio
- Handoff examples
- Troubleshooting common issues (405 errors, etc.)

## 📁 Project Structure

```
Dad joke Agent example/
├── main.py                    # Main agent implementation
├── config.py                  # Configuration helper for BASE_URL
├── pyproject.toml             # Python dependencies
├── .env.example               # Environment variable template
├── .gitignore                 # Git ignore rules (protects .env)
├── README.md                  # This file
├── agent-card.json           # Adaptive card definition
├── agent-discovery.json      # A2A discovery metadata
├── agent-manifest.json       # Teams app manifest
├── declarative-agent.json    # Copilot Studio definition
├── A2A_SETUP.md              # Copilot Studio integration guide
├── ENDPOINTS.md              # API endpoint reference
├── PROTOCOL.md               # Protocol compliance details
├── TUNNEL_SETUP.md           # VS Code tunnel configuration
└── ICONS.md                  # Icon creation guide
```

## 🔐 Security Note

**Never commit your `.env` file!** It contains sensitive API keys. The `.gitignore` file is configured to prevent this, but always verify before pushing code.

## 📚 Documentation

- **[A2A_SETUP.md](./A2A_SETUP.md)** - Copilot Studio integration guide
- **[ENDPOINTS.md](./ENDPOINTS.md)** - Complete API reference
- **[PROTOCOL.md](./PROTOCOL.md)** - Protocol compliance documentation
- **[TUNNEL_SETUP.md](./TUNNEL_SETUP.md)** - VS Code dev tunnel setup
- **[ICONS.md](./ICONS.md)** - Icon creation guide

## 🤝 Contributing

This is a sample project for demonstration purposes. Feel free to:
- Fork and customize for your own agents
- Report issues or suggestions
- Share your implementations

## 📄 License

This is a sample project provided as-is for educational purposes.

## 🆘 Troubleshooting

### OpenAI Integration Issues
- Verify your API key is correct in `.env`
- Agent falls back to random jokes if OpenAI fails

### Port Already in Use
- Change `PORT` in `.env` to an available port
- Or kill the process: `lsof -ti:2009 | xargs kill -9`

### Tunnel Connection Issues
- Ensure `BASE_URL` in `.env` matches your tunnel URL
- Restart the agent after changing `.env`
- Check that the port is publicly accessible

### JSON Files Not Loading
- Verify all JSON files are in the same directory as `main.py`
- Check that `BASE_URL` in `.env` is set correctly

For more help, see [TUNNEL_SETUP.md](./TUNNEL_SETUP.md) for tunnel-specific issues and [A2A_SETUP.md](./A2A_SETUP.md) for Copilot Studio configuration.
