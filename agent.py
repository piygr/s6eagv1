from client import start_agent
from perception import PerceptionLayer
from memory import MemoryLayer
from decision import DecisionLayer
import inspect
from pydantic import BaseModel
from typing import List, Dict, Callable, Any
from action import ActionLayer
import logging
import sys
logger = logging.getLogger(__name__)

async def app(session):
    # Get available tools
    logger.info("#####################\nAGENT ACTIVATED\n#####################\n")
    logger.info("Requesting tool list...")
    tools_result = await session.list_tools()
    tools = tools_result.tools
    logger.info(f"Successfully retrieved {len(tools)} tools")

    # Create system prompt with available tools
    logger.info("Creating system prompt...")
    tools_description = []
    for i, tool in enumerate(tools):
        try:
            params = tool.inputSchema
            desc = getattr(tool, 'description', 'No description available')
            name = getattr(tool, 'name', f'tool_{i}')

            param_details = []

            if "$defs" in params:
                defs = params.get("$defs")
                for _, param_type_info in defs.items():
                    if "properties" in param_type_info:
                        param_type_detail = param_type_info.get('properties')
                        #param_type = param_type_detail.get('title')
                        param_details.append(f"input: {param_type_detail}")
                        params_str = ', '.join(param_details)
                    else:
                        params_str = 'no parameters'

            else:
                params_str = ''
            tool_desc = f"{i+1}. {name}({params_str}) - {desc}"
            tools_description.append(tool_desc)
            logger.info(f"Added description for tool: {tool_desc}")


        except Exception as e:
            logging.error(f"Error processing tool {i}: {e}")
            tools_description.append(f"{i+1}. Error processing tool")

    tools_description = "\n".join(tools_description)
    logger.info("Successfully created tools description")
    #print(tools)
    query = "Calculate the devision of sum of cubes of ASCII values of word POKER with sum of squares of ASCII value of PORK. Do not show any reasoning."
    pl = PerceptionLayer(query, tools_description)
    perception = await pl.extract_structured_facts()
    print(perception)

    mem = MemoryLayer()
    mem.store(f"Available tools to use -\n{tools_description}", long_term=True)
    count = 1
    completed = False
    action = ActionLayer(tools)
    while count <= 20 and not completed:
        dec = DecisionLayer(perception, mem)
        next_step = await dec.next_action()
        logger.info(f"[Step {count}]: ", next_step)
        mem.store(f"Decision layer decided to take this action - {next_step}")
        count += 1
        act, completed = await action.call(session, next_step)
        mem.store(f"{act}")