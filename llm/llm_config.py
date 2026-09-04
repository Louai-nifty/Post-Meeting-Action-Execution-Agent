from pydantic_settings import BaseSettings

class LLMConfig(BaseSettings):
    model: str = "glm-5.3-flash-thinking:free"
    temperature: float = 0.0
    max_tokens: int = 100000
    timeout_seconds: int = 180
    
    # Cost tracking
    track_cost: bool = True
    
    class Config:
        env_prefix = "LLM_"

llm_config = LLMConfig()