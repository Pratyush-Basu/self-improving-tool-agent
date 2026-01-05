from typing import TypedDict, List, Optional, Dict, Any

class AgentState(TypedDict):
    query: str
    city: str
    trace: List[str]
    mistakes: List[str]
    route: str
    weather_data: Optional[Dict]
    research_data: Optional[str]
    final_answer: str
    reminders: List[str]