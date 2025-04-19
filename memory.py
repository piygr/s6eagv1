from pydantic import BaseModel
from typing import List, Dict, Union, Optional
import uuid
import logging
logger = logging.getLogger(__name__)

from client import call_llm

class MemoryModel(BaseModel):
    facts: List[str]
    long_term: List[str]

class MemoryLayer:
    def __init__(self):
        self.facts = []
        self.long_term = []
        logger.debug(f"Memory layer created")

    def store(self, fact, long_term=False):
        logger.debug(f"Storing fact: {fact}, long term: {long_term}")
        if long_term:
            self.long_term.append(fact)
        else:
            self.facts.append(fact)



    async def recall(self, query):
        prompt = f"Given the context: {self.long_term} and memory: {self.facts}, answer: {query}"
        return await call_llm(prompt)