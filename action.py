# Agentic AI Loop: Perception → Decision → Action → Memory (Dynamic Tool Plan)

from pydantic import BaseModel
from typing import List, Dict, Union, Optional
import uuid
from client import function_call
import logging
logger = logging.getLogger(__name__)


class ActionLayer():
    def __init__(self, tools):
        self.tools = tools

    async def call(self, session, decision):
        if decision:
            if decision.get("type") in ["TaskFunctionCallModel", "FUNCTION_CALL"]:
                logger.info(f"Calling function:\n{decision}")
                response = await function_call(session, decision.get("content"), self.tools)
                return response.strip(), False  #decision, completed
            elif decision.get("type") in ["TaskCompletedModel", "COMPLETED"]:
                logger.info(f"Task COMPLETED:\n{decision}")
                return decision, True
            elif decision.get("type") in ["CALCULATED_ANSWER"]:
                logger.info(f"Calculated answer:\n{decision}")
                return decision, False