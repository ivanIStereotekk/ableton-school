
from typing import Any
from starlette.responses import JSONResponse
from starlette.background import BackgroundTask
from starlette import status
import orjson
from fastapi import Response

# Status Responses

# COLLECTION FOR ROUTER  - responses=ROUTER_API_RESPONSES_OPEN_API
ROUTER_API_RESPONSES_OPEN_API = {
        status.HTTP_200_OK: {
            "description": "OK",
        },
        status.HTTP_201_CREATED: { 
            "description": "CREATED",
        },
        status.HTTP_202_ACCEPTED: {  
            "description": "ACCEPTED",
        },
        status.HTTP_204_NO_CONTENT: {  
            "description": "NO_CONTENT",
        },
        status.HTTP_401_UNAUTHORIZED: {  
            "description": "UNAUTHORIZED",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "UNPROCESSABLE ENTITY"
        }
    }

    
class CustomizedORJSONResponse(Response):
    media_type: str = "application/json"
    status_code: int
    content: Any
    background: BackgroundTask 
    def render(self, content: Any) -> bytes:
        assert orjson is not None, "orjson must be installed"
        return orjson.dumps(content, option=orjson.OPT_INDENT_2)