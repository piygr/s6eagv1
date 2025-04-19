import json
import os
from typing import Dict, Any

from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
import asyncio
from google import genai
from concurrent.futures import TimeoutError
from functools import partial
import anyio
import logging

logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Access your API key and initialize Gemini client correctly
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Store state globally or pass it around
_session_refs = {}

async def generate_with_timeout(client, prompt, timeout=30):
    """Generate content with a timeout"""
    print("Starting LLM generation...")
    try:
        loop = asyncio.get_event_loop()
        response = await asyncio.wait_for(
            loop.run_in_executor(
                None,
                lambda: client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                ),
            ),
            timeout=timeout
        )
        print("LLM generation completed")
        return response
    except TimeoutError:
        print("LLM generation timed out!")
        raise
    except Exception as e:
        print(f"Error in LLM generation: {e}")
        raise

async def call_llm(prompt):
    return await generate_with_timeout(client, prompt)


def wrap_args_using_schema(schema: Dict[str, Any], args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Wraps the flat `args` dict inside the expected nesting structure defined by a Pydantic schema.
    Useful for MCP tools where input schemas use `$ref`.
    """
    # Check if 'properties' defines 'input' using $ref
    props = schema.get('properties', {})
    if 'input' in props and '$ref' in props['input']:
        return {'input': args}

    # Fallback to flat (no nesting)
    return args


async def function_call(session, js, tools):
    #js = json.loads(js)
    func_name = js.get('name')
    params = js.get("args")
    tool = next((t for t in tools if t.name == func_name), None)
    if not tool:
        logging.debug(f"DEBUG: Available tools: {[t.name for t in tools]}")
        raise ValueError(f"Unknown tool: {func_name}")
    logging.debug(f"DEBUG: Found tool: {tool.name}")
    logging.debug(f"DEBUG: Tool schema: {tool.inputSchema}")
    arguments = {}
    schema_properties = tool.inputSchema.get('properties', {})
    logging.debug(f"DEBUG: Schema properties: {schema_properties}")

    arguments = wrap_args_using_schema(tool.inputSchema, params)
    if arguments is None:
        result = await session.call_tool(func_name)
    else:
        result = await session.call_tool(func_name, arguments=arguments)

    logging.debug(f"DEBUG: Raw result: {result}")
    if hasattr(result, 'content'):
        logging.debug(f"DEBUG: Result has content attribute")
        if isinstance(result.content, list):
            iteration_result = [
                item.text if hasattr(item, 'text') else str(item)
                for item in result.content
            ]
        else:
            iteration_result = str(result.content)
    else:
        logging.debug(f"DEBUG: Result has no content attribute")
        iteration_result = str(result)

    if arguments:
        out = f"{func_name} was called with {arguments} and it resulted in {iteration_result}"
    else:
        out = f"{func_name} was called and it resulted in {iteration_result}"

    logging.info(out)

    return out



async def session_main(server_params, app_logic):
    print("Establishing connection to MCP server...")
    async with stdio_client(server_params) as (read, write):
        print("Connection established, creating session...")
        async with ClientSession(read, write) as session:
            print("Session created, initializing...")
            await session.initialize()

            # Store in global ref if needed
            _session_refs["session"] = session

            # Your app runs here (e.g. perception loop, LLM tasks, etc.)
            await app_logic(session)

def cleanup_session():
    async def _cleanup():
        session = _session_refs.get("session")
        client = _session_refs.get("client")
        if session:
            await session.__aexit__(None, None, None)
        if client:
            await client.__aexit__(None, None, None)

    asyncio.run(_cleanup())


def start_agent(app_logic):
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"]
    )
    anyio.run(session_main, server_params, app_logic)

