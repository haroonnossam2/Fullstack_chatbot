from typing import TypedDict, List, Any



class SupportState(TypedDict):
    
    messages: List[Any]

    next_agent: str

    final_response: str

    last_agent: str

    activity: List[str]