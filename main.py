"""
Dad Joke Agent using Microsoft 365 Agents SDK
Supports Activity Protocol and Agent-to-Agent communication with Copilot Studio
"""

import os
import random
from dotenv import load_dotenv
from openai import OpenAI

from aiohttp.web import Application, Request, Response, run_app, json_response
from microsoft_agents.hosting.core import (
    AgentApplication,
    AgentAuthConfiguration,
    MemoryStorage,
    TurnState,
)
from microsoft_agents.hosting.aiohttp import CloudAdapter
from microsoft_agents.activity import Activity, ActivityTypes

# Load environment variables
load_dotenv()

# Configuration
PORT = int(os.getenv("PORT", 2009))
BASE_URL = os.getenv("BASE_URL", f"http://localhost:{PORT}")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client if API key is available
openai_client = None
if OPENAI_API_KEY and OPENAI_API_KEY != "your_openai_api_key_here":
    openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Random Dad Jokes Collection
DAD_JOKES = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "I'm reading a book about anti-gravity. It's impossible to put down!",
    "Why did the scarecrow win an award? He was outstanding in his field!",
    "What do you call a fake noodle? An impasta!",
    "Why don't eggs tell jokes? They'd crack each other up!",
    "How do you organize a space party? You planet!",
    "What do you call cheese that isn't yours? Nacho cheese!",
    "Why did the coffee file a police report? It got mugged!",
    "What do you call a bear with no teeth? A gummy bear!",
    "Why did the bicycle fall over? It was two tired!",
    "What's the best time to go to the dentist? Tooth-hurty!",
    "Why don't skeletons fight each other? They don't have the guts!",
    "What did the ocean say to the beach? Nothing, it just waved!",
    "Why did the math book look sad? It had too many problems!",
    "What do you call a can opener that doesn't work? A can't opener!",
]


# Create the AgentApplication with CloudAdapter
# For local development without authentication
AGENT_APP = AgentApplication[TurnState](
    storage=MemoryStorage(),
    adapter=CloudAdapter()
)


async def get_dad_joke(user_request: str) -> str:
    """Get a dad joke - random from list or generated via OpenAI"""

    # Check if user wants a random joke or no specific topic
    random_keywords = ["random", "any", "surprise", "tell me a joke", "give me a joke",
                      "dad joke", "make me laugh", "joke please", "hi", "hello", "hey"]

    is_random_request = (
        not user_request or
        any(keyword in user_request.lower() for keyword in random_keywords)
    )

    if is_random_request:
        # Return a random joke from our collection
        return f"🤣 {random.choice(DAD_JOKES)}"

    # User asked for a specific topic - try to use OpenAI if available
    if openai_client:
        try:
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a dad joke expert. Generate a single, clean, family-friendly dad joke. Only return the joke itself, no explanations or additional text."
                    },
                    {
                        "role": "user",
                        "content": f"Tell me a dad joke about: {user_request}"
                    }
                ],
                max_tokens=150,
                temperature=0.8
            )
            joke = response.choices[0].message.content.strip()
            return f"🤣 {joke}"
        except Exception as e:
            print(f"Error generating joke with OpenAI: {e}")
            # Fallback to random joke
            return f"🤣 {random.choice(DAD_JOKES)}\n\n_(Had trouble with a custom joke, so here's a classic!)_"
    else:
        # No OpenAI available, return random joke
        return f"🤣 {random.choice(DAD_JOKES)}\n\n_(For custom jokes, add your OpenAI API key to .env!)_"


# Handle conversation updates (member added)
@AGENT_APP.activity("conversationUpdate")
async def on_conversation_update(context: TurnState, activity: Activity):
    """Handle conversation updates (member added/removed)"""
    if activity.members_added:
        for member in activity.members_added:
            if member.id != activity.recipient.id:
                welcome_message = """👋 Welcome to the Dad Joke Agent!

I'm here to brighten your day with the finest dad jokes around! Just ask me for a joke, or specify a topic you'd like a joke about.

Type `/help` for more information. Let's get this party started! 🎉"""
                await context.send_activity(welcome_message)


# Handle messages
@AGENT_APP.activity("message")
async def on_message(context: TurnState, activity: Activity):
    """Handle incoming message activities"""
    user_message = activity.text.strip() if activity.text else ""

    # Check for help command
    if user_message.lower() in ["/help", "help"]:
        help_text = """🤣 **Dad Joke Agent** 🤣

I'm your friendly Dad Joke delivery service! Here's what I can do:

**Commands:**
- Just say hi or ask for a joke to get a random dad joke
- Ask for a joke about a specific topic (e.g., "tell me a joke about cats")
- Type `/help` to see this message

**Examples:**
- "Tell me a dad joke"
- "Give me a joke about food"
- "Make me laugh"
- "Random joke please"

Ready to groan? Ask away! 😄"""
        await context.send_activity(help_text)
        return

    # Generate or retrieve a dad joke
    joke = await get_dad_joke(user_message)
    await context.send_activity(joke)


# Handle event activities
@AGENT_APP.activity("event")
async def on_event(context: TurnState, activity: Activity):
    """Handle event activities"""
    event_name = activity.name if hasattr(activity, 'name') else None

    if event_name == "handoff":
        # Handle agent-to-agent handoff event
        await handle_handoff(context, activity)
    else:
        # Echo back event information
        await context.send_activity(f"Received event: {event_name}")


# Handle handoff activities
async def handle_handoff(context: TurnState, activity: Activity):
    """
    Handle agent-to-agent handoff from Copilot Studio
    Compliant with Microsoft 365 A2A Protocol
    """
    try:
        # Extract handoff context if available
        handoff_context = activity.value if hasattr(activity, 'value') else {}

        # Log handoff for debugging
        print(f"Handoff received - Activity Type: {activity.type}")
        if handoff_context:
            print(f"Handoff Context: {handoff_context}")

        # Send acknowledgment
        response = """🤝 **Handoff Received!**

Hey there! I'm the Dad Joke Agent, and I've just received your conversation from another agent.

I'm here to make you laugh with some quality dad jokes! What kind of joke would you like to hear?"""

        await context.send_activity(response)

        # If there's a specific request in the handoff context, handle it
        if handoff_context and isinstance(handoff_context, dict):
            # Support multiple context field names for compatibility
            request = (handoff_context.get("request") or
                      handoff_context.get("message") or
                      handoff_context.get("userMessage") or
                      handoff_context.get("text"))

            if request:
                joke = await get_dad_joke(request)
                await context.send_activity(joke)

    except Exception as e:
        print(f"Error handling handoff: {e}")
        await context.send_activity("I received the handoff, but encountered an issue. Let's start fresh - ask me for a joke!")


# Handle invoke activities for A2A
@AGENT_APP.activity("invoke")
async def on_invoke(context: TurnState, activity: Activity):
    """
    Handle invoke activities for agent-to-agent protocol
    Used by Copilot Studio for skill invocation
    """
    try:
        invoke_name = activity.name if hasattr(activity, 'name') else None
        invoke_value = activity.value if hasattr(activity, 'value') else {}

        print(f"Invoke received - Name: {invoke_name}, Value: {invoke_value}")

        if invoke_name == "application/vnd.microsoft.activity.handoff":
            # Standard A2A handoff invoke
            await handle_handoff(context, activity)
        else:
            # Generic invoke handler - send response
            response_value = {
                "status": 200,
                "body": {
                    "message": "Invoke received by Dad Joke Agent",
                    "invokeName": invoke_name
                }
            }
            await context.send_activity(Activity(
                type=ActivityTypes.invoke_response,
                value=response_value
            ))
    except Exception as e:
        print(f"Error handling invoke: {e}")
        error_response = {
            "status": 500,
            "body": {"error": str(e)}
        }
        await context.send_activity(Activity(
            type=ActivityTypes.invoke_response,
            value=error_response
        ))


if __name__ == "__main__":
    print("🤣 Dad Joke Agent Starting...")
    print(f"📡 Listening on http://localhost:{PORT}/api/messages")
    print(f"🔑 OpenAI Integration: {'Enabled' if openai_client else 'Disabled (using random jokes only)'}")
    print("\nPress Ctrl+C to stop the agent\n")

    # Create request logging middleware
    from aiohttp.web import middleware

    @middleware
    async def request_logger(request, handler):
        """Log all incoming requests for debugging"""
        print(f"\n🌐 {request.method} {request.path} from {request.remote}")
        response = await handler(request)
        print(f"   → Response: {response.status}")
        return response

    # Create the web application with middleware
    app = Application(middlewares=[request_logger])

    # Add health check endpoint (no auth required)
    async def health_check(request):
        return json_response({"status": "healthy", "agent": "Dad Joke Agent"})

    app.router.add_get("/health", health_check)

    # Add agent card endpoint
    async def agent_card(request):
        """Serve the agent card for discovery and integration"""
        import json
        try:
            with open("agent-card.json", "r") as f:
                card_data = json.load(f)
            # Replace {BASE_URL} placeholder with actual BASE_URL
            card_str = json.dumps(card_data).replace("{BASE_URL}", BASE_URL)
            card_data = json.loads(card_str)
            return json_response(card_data)
        except Exception as e:
            return json_response(
                {"error": "Agent card not found", "message": str(e)},
                status=404
            )

    app.router.add_get("/api/card", agent_card)

    # Add well-known agent card endpoint (A2A protocol standard) - GET only for now
    # POST route will be added after messages_endpoint is defined
    app.router.add_get("/.well-known/agent-card.json", agent_card)

    # Add agent discovery endpoint (comprehensive A2A metadata)
    async def agent_discovery(request):
        """Serve the agent discovery document for A2A protocol"""
        import json
        try:
            with open("agent-discovery.json", "r") as f:
                discovery_data = json.load(f)
            # Replace {BASE_URL} placeholder with actual BASE_URL
            discovery_str = json.dumps(discovery_data).replace("{BASE_URL}", BASE_URL)
            discovery_data = json.loads(discovery_str)
            return json_response(discovery_data)
        except Exception as e:
            return json_response(
                {"error": "Agent discovery document not found", "message": str(e)},
                status=404
            )

    app.router.add_get("/api/discovery", agent_discovery)
    app.router.add_get("/.well-known/agent-discovery.json", agent_discovery)

    # Add agent manifest endpoint
    async def agent_manifest(request):
        """Serve the agent manifest for Teams/Copilot Studio integration"""
        import json
        try:
            with open("agent-manifest.json", "r") as f:
                manifest_data = json.load(f)
            return json_response(manifest_data)
        except Exception as e:
            return json_response(
                {"error": "Agent manifest not found", "message": str(e)},
                status=404
            )

    app.router.add_get("/api/manifest", agent_manifest)

    # Add declarative agent endpoint
    async def declarative_agent(request):
        """Serve the declarative agent definition for Copilot Studio"""
        import json
        try:
            with open("declarative-agent.json", "r") as f:
                declarative_data = json.load(f)
            return json_response(declarative_data)
        except Exception as e:
            return json_response(
                {"error": "Declarative agent definition not found", "message": str(e)},
                status=404
            )

    app.router.add_get("/api/declarative-agent", declarative_agent)

    # Add simple message endpoint with manual activity processing
    async def messages_endpoint(request):
        """Handle Bot Framework messages and JSON-RPC 2.0 A2A messages"""
        try:
            # Add detailed logging for troubleshooting Copilot Studio connection
            print("\n" + "="*60)
            print("📨 INCOMING REQUEST")
            print("="*60)
            print(f"Method: {request.method}")
            print(f"Path: {request.path}")
            print(f"Query: {request.query_string}")
            print(f"\nHeaders:")
            for header, value in request.headers.items():
                # Mask authorization tokens for security
                if header.lower() == 'authorization':
                    print(f"  {header}: Bearer ***masked***")
                else:
                    print(f"  {header}: {value}")

            # Parse the incoming message
            body = await request.json()
            print(f"\nBody:")
            import json
            print(json.dumps(body, indent=2))
            print("="*60 + "\n")

            # Check if this is a JSON-RPC 2.0 A2A message
            if body.get("jsonrpc") == "2.0" and body.get("method") == "message/send":
                print("🔀 Detected JSON-RPC 2.0 A2A message")

                # Extract the message from JSON-RPC params
                params = body.get("params", {})
                message = params.get("message", {})

                # Extract the text from parts
                text = ""
                parts = message.get("parts", [])
                for part in parts:
                    if part.get("kind") == "text":
                        text = part.get("text", "")
                        break

                print(f"📝 Extracted text: {text}")

                # Generate the dad joke
                joke = await get_dad_joke(text)

                # Build JSON-RPC 2.0 response
                jsonrpc_response = {
                    "jsonrpc": "2.0",
                    "id": body.get("id"),
                    "result": {
                        "message": {
                            "kind": "message",
                            "parts": [
                                {
                                    "kind": "text",
                                    "text": joke
                                }
                            ],
                            "role": "assistant"
                        }
                    }
                }

                print(f"📤 Sending JSON-RPC 2.0 response")
                print(json.dumps(jsonrpc_response, indent=2))
                return json_response(jsonrpc_response)

            # Otherwise, treat as Bot Framework Activity
            print("🔀 Detected Bot Framework Activity")
            activity = Activity(**body)

            # Create a simple turn context and call the agent handlers directly
            # For local dev, we bypass the full adapter pipeline

            # Create a mock context that can send responses
            class SimpleTurnContext:
                def __init__(self, activity):
                    self.activity = activity
                    self.responses = []

                async def send_activity(self, text_or_activity):
                    if isinstance(text_or_activity, str):
                        self.responses.append({"type": "message", "text": text_or_activity})
                    elif isinstance(text_or_activity, Activity):
                        self.responses.append({"type": text_or_activity.type, "text": getattr(text_or_activity, 'text', '')})
                    else:
                        self.responses.append({"type": "message", "text": str(text_or_activity)})

            context = SimpleTurnContext(activity)

            # Route to the appropriate handler based on activity type
            print(f"🔀 Routing activity type: {activity.type}")
            if activity.type == ActivityTypes.message:
                print("  → Routing to on_message handler")
                await on_message(context, activity)
            elif activity.type == ActivityTypes.conversation_update:
                print("  → Routing to on_conversation_update handler")
                await on_conversation_update(context, activity)
            elif activity.type == "event" or activity.type == ActivityTypes.event:
                print("  → Routing to on_event handler")
                await on_event(context, activity)
            elif activity.type == "invoke" or activity.type == ActivityTypes.invoke:
                print("  → Routing to on_invoke handler")
                await on_invoke(context, activity)
            else:
                print(f"  ⚠️  Unknown activity type: {activity.type}")

            print(f"✅ Request processed successfully")
            print(f"📤 Responses generated: {len(context.responses)}")
            if context.responses:
                print(f"   Response preview: {context.responses[0] if context.responses else 'None'}")

            # Build Bot Framework response activities
            response_activities = []
            for resp in context.responses:
                # Get the from field (note: Pydantic uses 'from' not 'from_')
                from_field = getattr(activity, 'from', None) or getattr(activity, 'from_', None)

                response_activity = {
                    "type": resp.get("type", "message"),
                    "text": resp.get("text", ""),
                    "from": activity.recipient.model_dump() if hasattr(activity.recipient, 'model_dump') else activity.recipient,
                    "recipient": from_field.model_dump() if hasattr(from_field, 'model_dump') else from_field,
                    "replyToId": activity.id,
                    "serviceUrl": activity.service_url,
                    "channelId": activity.channel_id,
                    "conversation": activity.conversation.model_dump() if hasattr(activity.conversation, 'model_dump') else activity.conversation
                }
                response_activities.append(response_activity)

            # Return Bot Framework response
            if response_activities:
                print(f"📤 Sending {len(response_activities)} activities back to Copilot Studio")
                # For single response, return the activity directly
                if len(response_activities) == 1:
                    return json_response(response_activities[0])
                else:
                    # For multiple responses, return as array
                    return json_response({"activities": response_activities})
            else:
                # No responses, just return success
                return Response(status=200)

        except Exception as e:
            print(f"\n❌ ERROR PROCESSING MESSAGE")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {e}")
            print("\nFull traceback:")
            import traceback
            traceback.print_exc()
            print("="*60 + "\n")
            return Response(text=str(e), status=500)

    app.router.add_post("/api/messages", messages_endpoint)
    app.router.add_get("/api/messages", lambda _: Response(status=200))

    # Add POST route for well-known agent card endpoint (A2A protocol)
    # This allows Copilot Studio to POST to /.well-known/agent-card.json for A2A messaging
    app.router.add_post("/.well-known/agent-card.json", messages_endpoint)

    # Run the app
    # Bind to 0.0.0.0 to allow external connections (like VS Code tunnel)
    run_app(app, host="0.0.0.0", port=PORT)
