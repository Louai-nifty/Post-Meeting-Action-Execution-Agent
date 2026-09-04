from openai import AsyncOpenAI, APIError
from typing import TypeVar, Type
from pydantic import BaseModel, ValidationError
import asyncio
from llm_config import llm_config
from config import base_url, llm_api_key

T = TypeVar("T", bound=BaseModel)

class LLMClient:
    def __init__(self):
        self.client = AsyncOpenAI(
            base_url=base_url,
            api_key=llm_api_key, # Ensure valid API key here
            timeout=llm_config.timeout_seconds
        )
        self.config = llm_config
    
    async def structured_call(
        self,
        system_prompt: str,
        user_prompt: str,
        output_schema: Type[T],
        model: str | None = None,
        temperature: float | None = None,
        max_retries: int = 3
    ) -> T:
        """
        Executes a structured LLM call guaranteed to match `output_schema` Pydantic model.
        Includes automatic retry logic for transient API network failures.
        """
        selected_model = model or self.config.model
        selected_temp = temperature if temperature is not None else self.config.temperature

        for attempt in range(1, max_retries + 1):
            try:
                response = await self.client.beta.chat.completions.parse(
                    model=selected_model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    response_format=output_schema, 
                    temperature=selected_temp,
                    max_tokens=self.config.max_tokens
                )
                
                parsed_object: T = response.choices[0].message.parsed
                
                if parsed_object is None:
                    refusal = response.choices[0].message.refusal
                    raise ValueError(f"LLM Refused request: {refusal}")

                if self.config.track_cost and response.usage:
                    await self._log_cost(response.usage, selected_model)
                
                return parsed_object

            except (APIError, ValidationError, ValueError) as e:
                if attempt == max_retries:
                    await self._log_failure(system_prompt, user_prompt, e)
                    raise e
                await asyncio.sleep(2 ** (attempt - 1))

    async def _log_cost(self, usage, model: str):
        pass

    async def _log_failure(self, system: str, user: str, error: Exception):
        pass

llm_client = LLMClient()
