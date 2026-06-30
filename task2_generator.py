import json
import time
import os
import random

class SimpleSyntheticGenerator:
    def __init__(self):
        # List of banned phrases to check against (Simulating Task 1 local keyword guardrails)
        self.banned_keywords = ["you will die", "critical illness", "cancer", "guaranteed wealth", "must pay me"]

    def generate_simulated_chat(self, scenario: str) -> dict:
        """Simulates high-quality synthetic astrologer responses locally without any API keys."""
        greetings = ["Pranam", "Namaste ji", "Welcome to Vedaz Astrology"]
        user_names = ["Rahul", "Amit", "Priya", "Sneha", "Vikram", "Anjali"]
        
        selected_greeting = random.choice(greetings)
        selected_name = random.choice(user_names)

        # Build dynamic, safe, compliant responses based on the scenario
        if "medical" in scenario.lower() or "health" in scenario.lower():
            assistant_text = f"{selected_greeting}. I can see your planetary transits are causing minor stress, but for any genuine health or medical queries, please consult a professional doctor immediately. For peace of mind, you can practice daily meditation."
        elif "gemstones" in scenario.lower() or "career" in scenario.lower():
            assistant_text = f"{selected_greeting} {selected_name}. Your professional house configurations look strong. Do not worry about buying expensive gemstones or paid remedies. Instead, focus on simple, free mindfulness exercises for clarity."
        else:
            assistant_text = f"{selected_greeting} {selected_name}. I have analyzed your birth chart setup. Your current Jupiter cycle looks very favorable for personal growth over the coming months. Stay positive!"

        # Structure exactly matching the required fine-tuning platform standard
        return {
            "messages": [
                {"role": "system", "content": "You are Vedaz's AI Vedic astrologer. Provide compassionate guidance while maintaining strict platform guardrails."},
                {"role": "user", "content": f"Hello, my name is {selected_name}. Can you check my chart regarding: {scenario}?"},
                {"role": "assistant", "content": assistant_text}
            ]
        }

    def run_generation_pipeline(self, scenarios: list[str], target_count: int = 10, output_file: str = "generated_output.jsonl"):
        """Generates 10 rows safely and writes them to the output file."""
        print(f"🚀 Launching Local Synthetic Data Factory (Zero API Key Dependencies)...")
        
        if os.path.exists(output_file):
            os.remove(output_file)

        valid_count = 0
        
        for i in range(target_count):
            current_scenario = scenarios[i % len(scenarios)]
            chat_data = self.generate_simulated_chat(current_scenario)
            
            # Combine transcript text to quickly audit for safety keywords locally
            joined_transcript = " ".join([m.get("content", "").lower() for m in chat_data["messages"]])
            
            # Check if any banned phrases made it into the text
            has_violation = any(flag in joined_transcript for flag in self.banned_keywords)
            
            if not has_violation:
                valid_count += 1
                print(f"   ✓ [Row {valid_count}/{target_count}] Verified & Saved: Scenario -> '{current_scenario}'")
                
                with open(output_file, "a", encoding="utf-8") as f:
                    f.write(json.dumps(chat_data, ensure_ascii=False) + "\n")
            else:
                print(f"   ✗ Row rejected due to safety violations.")
                
            time.sleep(0.05)

        print(f"\n🏆 Task 2 Complete! Successfully generated {valid_count} clean rows in '{output_file}'.")

if __name__ == "__main__":
    test_scenarios = [
        "Career guidance and job promotion delay timeline",
        "Medical redirection audit check",
        "Business growth projections for retail store",
        "Skeptical user evaluating platform response rules",
        "Relationship compatibility and family harmony outlook",
        "Financial investment roadblocks and optional spiritual mindfulness solutions"
    ]
    
    factory = SimpleSyntheticGenerator()
    factory.run_generation_pipeline(test_scenarios, target_count=10)