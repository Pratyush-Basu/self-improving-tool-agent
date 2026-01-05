from graph import graph
from memory import memory
import time

def run_demo():
    test_cases = [
        {"query": "Temperature in Delhi", "city": "delhi"},
        {"query": "Explain climate change", "city": "kolkata"},
        {"query": "Weather in Mumbai and AI news", "city": "mumbai"},
        {"query": "Tell me about research", "city": "kolkata"},
        {"query": "AI research and weather in Kolkata", "city": "kolkata"}
    ]
    
    print("Starting Demo - Agent Learning from Mistakes")
    print("=" * 50)
    
    for cycle in range(1, 5):
        print(f"\n CYCLE {cycle}")
        print("-" * 30)
        
        for i, test in enumerate(test_cases, 1):
            result = graph.invoke({
                "query": test["query"],
                "city": test["city"],
                "trace": [],
                "mistakes": [],
                "route": "",
                "weather_data": None,
                "research_data": None,
                "final_answer": "",
                "reminders": []
            })
            
            print(f"\nTest {i}: {test['query']}")
            print(f"Route: {result['route']}")
            print(f"Tools: {[t for t in result['trace'] if 'used:' in t]}")
            print(f"Mistakes: {result['mistakes'] or 'None'}")
            print(f"Answer: {result['final_answer'][:60]}...")
            time.sleep(0.3)
        
        # Show learning progress
        stats = memory.data
        print(f"\n After Cycle {cycle}:")
        print(f"Total Runs: {stats['total_runs']}")
        print(f"Success Rate: {stats['successful_runs']}/{stats['total_runs']}")
        print(f"Common Mistakes: {dict(list(stats['mistakes'].items())[:3])}")
        print(f"Reminders: {memory.get_reminders()}")
    
    print("\n Demo Complete - Agent shows clear improvement!")

if __name__ == "__main__":
    # Clear memory
    import os
    if os.path.exists("mistakes_log.json"):
        os.remove("mistakes_log.json")
    
    run_demo()