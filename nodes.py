from tools import get_weather, search_web
from memory import memory

def agent_node(state):
    query = state["query"].lower()
    reminders = memory.get_reminders()  # Get current reminders
    
    print(f"DEBUG: Current reminders: {reminders}")  # Debug line

# Strict learning rule — force Research before Weather
    if any("STRICT RULE" in r for r in reminders):
        if "weather" in query and "research" in query:
            state["route"] = "both"
            state["tool_priority"] = ["research", "weather"]
            state["trace"].append("rule:strict_research_first")
            return state
    
    # Check reminders first - they override everything
    for reminder in reminders:
        if "research" in reminder.lower() and ("research" in query or "news" in query):
            # Force research tool for research queries
            if "weather" in query or "temperature" in query:
                state["route"] = "both"  # Use both tools
            else:
                state["route"] = "research"
            state["trace"].append(f"route:{state['route']}(reminder)")
            return state
    
    # Original logic for early runs (make mistakes)
    if memory.data["total_runs"] < 3:
        # Early runs: Make natural mistakes
        if "temperature" in query and "weather" not in query:
            state["route"] = "direct"  # Common mistake
        elif "explain" in query:
            state["route"] = "direct"  # Another common mistake
        elif "weather" in query and "news" in query:
            state["route"] = "both"  # Multi-tool query
        elif "weather" in query:
            state["route"] = "weather"
        elif "research" in query or "explain" in query:
            state["route"] = "research"
        else:
            state["route"] = "direct"
    else:
        # Later runs: Apply learning (with reminder check above)
        if "weather" in query or "temperature" in query:
            state["route"] = "weather" if "research" not in query else "both"
        elif "research" in query or "news" in query or "explain" in query or "ai" in query:
            state["route"] = "research" if "weather" not in query else "both"
        else:
            state["route"] = "direct"
    
    state["reminders"] = reminders
    state["trace"].append(f"route:{state['route']}")
    return state


def tool_node(state):
    if state["route"] in ["weather", "both"]:
        state["weather_data"] = get_weather(state["city"])
        state["trace"].append("used:weather")
    
    if state["route"] in ["research", "both"]:
        state["research_data"] = search_web(state["query"])
        state["trace"].append("used:research")
    
    return state

def summary_node(state):
    answer = []
    if state.get("weather_data"):
        w = state["weather_data"]
        answer.append(f"Weather: {w['temp']}°C, {w['condition']}")
    
    if state.get("research_data"):
        answer.append(f"Research: {state['research_data']}")
    
    if not answer:
        answer.append("No data collected.")
    
    state["final_answer"] = "\n".join(answer)
    state["trace"].append("summary")
    return state

def evaluate_node(state):
    query = state["query"].lower()
    mistakes = []
    
    # ---- mistake detection ----
    if ("weather" in query or "temperature" in query) and "used:weather" not in state["trace"]:
        mistakes.append("missed_weather")
    
    if ("research" in query or "explain" in query or "news" in query or "ai" in query) \
        and "used:research" not in state["trace"]:
        mistakes.append("missed_research")

    if "and" in query:
        if "used:weather" not in state["trace"] or "used:research" not in state["trace"]:
            mistakes.append("incomplete_multi_query")

    if state["route"] == "direct" and ("weather" in query or "research" in query):
        mistakes.append("wrong_route")
    
    state["mistakes"] = mistakes

    # ---- learning / memory update ----
    for mistake in mistakes:
        memory.log_mistake(mistake)

    if not mistakes:
        memory.log_success()

    memory.increment_runs()

    # ----  feedback explanation  ----
    if mistakes:
        state["trace"].append(f"feedback: learned_from -> {mistakes}")
    else:
        state["trace"].append("feedback: no mistakes — behavior improved")

    return state


def learn_node(state):
    memory.save()
    return state