import json
import os

def test_generated_data(file_path="generated_output.jsonl"):
    print("📋 Starting Final Quality Control Audit on Generated Dataset...")
    print("-" * 75)
    print(f"{'Row #':<8} | {'System Turn':<12} | {'User Turn':<12} | {'Assistant Turn':<15} | {'Status':<10}")
    print("-" * 75)

    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} not found! Run Task 2 first.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for idx, line in enumerate(lines, start=1):
        try:
            data = json.loads(line)
            messages = data.get("messages", [])
            
            # Count the roles inside the message list
            has_system = any(m.get("role") == "system" for m in messages)
            has_user = any(m.get("role") == "user" for m in messages)
            has_assistant = any(m.get("role") == "assistant" for m in messages)
            
            # Format display tags
            sys_stat = "✓ YES" if has_system else "✗ NO"
            usr_stat = "✓ YES" if has_user else "✗ NO"
            ast_stat = "✓ YES" if has_assistant else "✗ NO"
            overall = "PASS" if (has_system and has_user and has_assistant) else "FAIL"
            
            print(f"Row {idx:<4} | {sys_stat:<12} | {usr_stat:<12} | {ast_stat:<15} | {overall:<10}")
        except Exception as e:
            print(f"Row {idx:<4} | Corrupted JSON formatting structure line. Error: {e}")

    print("-" * 75)
    print(f"🏁 Audit Complete! Total Checked Rows: {len(lines)}")

if __name__ == "__main__":
    test_generated_data()