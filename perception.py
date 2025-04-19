import json

import re
from pydantic import BaseModel
from typing import List, Dict, Union, Optional
import uuid
from client import _session_refs, call_llm, start_agent
import logging
logger = logging.getLogger(__name__)


class ToolStep(BaseModel):
    tool: str
    args: Dict[str, Union[int, str]]

class PerceptionModel(BaseModel):
    intent: str
    task_description: str
    entities: Dict[str, Union[int, str, List[int]]]
    needs_visual_output: Optional[bool] = False
    #available_tools: List[ToolStep]


class PerceptionLayer:
    def __init__(self, query, tools):
        self.query = query
        self.schema = PerceptionModel.schema_json(indent=2)

    async def extract_structured_facts(self) -> PerceptionModel:
        prompt = f"""
        You are a browser cum math agent solving problems in iterations and finally display the result 
        inside a rectangle in the browser-based paint app. You have access to various tools. 
        You must use EXACTLY these tools to calculate the answer and display it using the paint app.
        Respond ONLY with a valid JSON object that matches this schema:
            
        {self.schema}
            
        User query: {self.query}. \nYou MUST display the calculated result inside a rectangle in the browser based paint app.
        """
        logger.info(f"Extracting structured facts from User Query")
        response = await call_llm(prompt)
        text = response.text.strip()
        #cleaned = text.replace("json\n", "").replace("```", "")
        cleaned = re.sub(r"```json|```", "", text).strip()

        logger.info(f"Structured facts\n{text}")

        data = json.loads(cleaned)

        perception = PerceptionModel(**data)
        return perception
