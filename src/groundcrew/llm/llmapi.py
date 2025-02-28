import importlib
#import os

# Determine which API implementation to use
#USE_OLLAMA = os.getenv("USE_OLLAMA", "false").lower() == "true"

#if USE_OLLAMA:
#    from .ollamaapi import *  # Import everything from ollamaapi
#else:
#    from .openaiapi import *  # Import everything from openaiapi


llm_module = importlib.import_module(f"groundcrew.llm.openaiapi")
#llm_module = importlib.import_module(f"groundcrew.llm.ollamaapi")



# Expose common classes and functions to be used elsewhere in the code
SystemMessage       = llm_module.SystemMessage
UserMessage         = llm_module.UserMessage
AssistantMessage    = llm_module.AssistantMessage
Message             = llm_module.Message
get_llm_client      = llm_module.get_llm_client
start_chat          = llm_module.start_chat

