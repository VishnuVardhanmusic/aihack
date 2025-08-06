import warnings
warnings.filterwarnings(
    "ignore",
    message="Pydantic serializer warnings",
    category=UserWarning    
)
import os
MODEL_NAME = "gpt-4o-mini"  
BASE_URL = os.getenv("LITELLM_URL","https://api.litellm.ai")  
API_KEY = os.getenv("LITELLM_API_KEY","your_api_key_here")        