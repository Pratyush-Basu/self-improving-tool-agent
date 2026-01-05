import json
from pathlib import Path

MISTAKES_FILE = Path("mistakes_log.json")

class LearningMemory:
    def __init__(self):
        self.data = self._load()
    
    def _load(self):
        if MISTAKES_FILE.exists():
            return json.loads(MISTAKES_FILE.read_text())
        return {"mistakes": {}, "total_runs": 0, "successful_runs": 0}
    
    def save(self):
        MISTAKES_FILE.write_text(json.dumps(self.data, indent=2))
    
    def log_mistake(self, mistake):
        self.data["mistakes"][mistake] = self.data["mistakes"].get(mistake, 0) + 1
    
    def log_success(self):
        self.data["successful_runs"] += 1
    
    def increment_runs(self):
        self.data["total_runs"] += 1
    
    def get_reminders(self):
        reminders = []
        for mistake, count in self.data["mistakes"].items():
        # TRIGGER SOONER: after just 1 occurrence for critical mistakes
            if count >= 1:
                if "research" in mistake:
                    reminders.append("ALWAYS use research tool for queries with 'research', 'news', or 'AI'")
                if "weather" in mistake:
                    reminders.append("ALWAYS use weather tool for queries with 'weather' or 'temperature'")
                if "multi" in mistake:
                    reminders.append("Queries with 'and' need BOTH weather AND research tools")

                if count >= 3:
                    reminders.append("STRICT RULE: Research MUST run before Weather when both appear")
    
    # Remove duplicates
        return list(dict.fromkeys(reminders))

memory = LearningMemory()