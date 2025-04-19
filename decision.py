import json
import re
from pydantic import BaseModel
from typing import List, Dict, Union, Optional
import uuid
from client import call_llm

from perception import PerceptionModel
from memory import MemoryLayer
import logging
logger = logging.getLogger(__name__)


class ContentCompletedModel(BaseModel):
    completed: bool

class ContentFunctionCallModel(BaseModel):
    name: str
    args: Dict

class TaskCompletedModel(BaseModel):
    type: str
    content: ContentCompletedModel

class TaskFunctionCallModel(BaseModel):
    type: str
    content: ContentFunctionCallModel

class TaskCalculatedAnswerModel(BaseModel):
    type: str
    content: List

class DecisionLayer:
    def __init__(self, perception: PerceptionModel, memory: MemoryLayer):
        self.perception = perception
        self.memory = memory

    async def next_action(self):
        prompt = f"""
Given \n{self.memory.long_term} \nand structured query:\n {self.perception.json()}.
We have completed these steps -
{self.memory.facts}.\n What should be the next step? no reasoning needed.
The next step should follow either of these three formats-
        
==========================
🔧 RESPONSE FORMAT (STRICT)
==========================

Respond with EXACTLY ONE line in ONE of the following formats (no extra text):

1. For function calls:
   {{
  "type": "FUNCTION_CALL",
  "content": {{
    "name": "name of the function",
    "args": {{
      "arg1": "value1" ...
    }}
  }}

2. ONLY when the final answer is calculated:
   {{
  "type": "CALCULATED_ANSWER",
  "content": {{
    [output]
  }}

3. When all steps are completed:
   {{
  "type": "COMPLETED",
  "content": {{
    "completed": true
  }}
   
=========================
🧠 REASONING & CONSTRAINTS
==========================

- Always reason step-by-step, using function calls logically in the correct order.
- After each FUNCTION_CALL result, verify the function call output for sanity by evaluating the mathematical expression.
- If a function returns multiple values, you MUST process all of them.
- NEVER repeat the same function call with identical parameters.
- Only give CALCULATED_ANSWER after all calculations are done.
- After CALCULATED_ANSWER, you MUST issue relevant FUNCTION_CALL using available tools to display the result in Paint app. 
- YOU MUST NOT respond with CALCULATED_ANSWER twice.
- After all actions are done, return with type 'COMPLETED' as described
- Internally tag the reasoning type at each step (e.g., arithmetic, string parsing).

"""


        prompt += f"""
        """
        logger.info(f"Exploring next action...")
        next_step = await call_llm(prompt)
        text = next_step.text.strip()
        cleaned = re.sub(r"```json|```", "", text).strip()
        logger.debug(f"Next action: \n{cleaned}")
        data = json.loads(cleaned)
        return data
