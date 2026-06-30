import json
import re
import hashlib
from typing import Dict, List, Tuple
from openai import OpenAI
from tabulate import tabulate
import config

class ProductionChatChecker:
    def __init__(self):
        # Initialize client cleanly using unified standard endpoints
        self.client = OpenAI(api_key=config.API_KEY, base_url=config.BASE_URL) if config.API_KEY else None

    def calculate_approx_tokens(self, text: str) -> int:
        """Calculates token overhead metrics safely accounting for multi-language registers."""
        words = len(text.split())
        return int(words * 1.35)

    def validate_conversational_structure(self, messages: List[Dict]) -> Tuple[bool, str]:
        """Enforces absolute behavioral shapes for standard fine-tuning workflows."""
        if not messages:
            return False, "Empty array sequence."
        if messages[0].get("role") != "system":
            return False, "Structural Fault: First message must be a system instruction."
        
        expected_role = "user"
        for idx, turn in enumerate(messages[1:], start=1):
            current_role = turn.get("role")
            if current_role != expected_role:
                return False, f"Sequence Broken: Index {idx} expected role '{expected_role}', got '{current_role}'."
            expected_role = "assistant" if expected_role == "user" else "user"
            
        if expected_role == "user":
            return False, "Structural Fault: Dialogue ends on a dangling User query without an Assistant resolution."
            
        return True, "Structure verified successfully."

    def normalize_text_for_dedup(self, text: str) -> str:
        """Advanced fingerprint mapping: strips case, non-alpha chars, spaces to catch hidden near-duplicates."""
        return re.sub(r'\W+', '', text.lower().strip())

    def deterministic_train_test_split(self, line: str, train_ratio: float = 0.8) -> str:
        """Uses cryptographic hashing values to run reliable splits over random indexing seeds."""
        hasher = hashlib.md5(line.encode('utf-8')).hexdigest()
        # Convert hex signature scale to percentile 0-99
        percentile = int(hasher, 16) % 100
        return "train" if percentile < (train_ratio * 100) else "test"

    def execute_deterministic_keyword_guardrail(self, text: str) -> List[str]:
        """Instant string level pattern evaluation layer to block clear exploitation lines."""
        flags = []
        lowered = text.lower()
        
        death_triggers = ["maroge", "mrityu", "maut", "death", "die", "cancer", "accident"]
        scam_triggers = ["vashikaran", "100% guarantee", "paisa double", "crorepati", "guaranteed wealth"]
        
        if any(trigger in lowered for trigger in death_triggers):
            flags.append("Deterministic Flag: High-risk health/mortality keyword found.")
        if any(trigger in lowered for trigger in scam_triggers):
            flags.append("Deterministic Flag: Unsafe/predatory financial practice language found.")
            
        return flags

    def execute_llm_compliance_audit(self, chat_string: str) -> Tuple[bool, List[str], str]:
        """Contextual evaluation tier checking for structural policy bypasses."""
        if not self.client:
            return True, [], "Skipped (API Key missing configuration details)"
            
        try:
            response = self.client.chat.completions.create(
                model=config.MODEL_NAME,
                messages=[
                    {"role": "system", "content": config.SAFETY_JUDGE_PROMPT},
                    {"role": "user", "content": f"Audit this chat stream:\n\n{chat_string}"}
                ],
                temperature=0.0  # Zero variance across comparative pipeline iterations
            )
            
            raw_payload = response.choices[0].message.content.strip()
            # Handle potential markdown fence encasings safely
            if "```json" in raw_payload:
                raw_payload = raw_payload.split("```json")[1].split("```")[0].strip()
                
            parsed_report = json.loads(raw_payload)
            violates = parsed_report.get("violates_rules", False)
            rules_hit = parsed_report.get("violated_rules_list", [])
            rationale = parsed_report.get("reasoning_critique", "")
            
            return not violates, rules_hit, rationale
            
        except Exception as e:
            return False, ["Audit Failure"], f"Internal Exception encountered during automated verification: {str(e)}"

    def execute_pipeline(self):
        print("⚡ Bootstrapping Automated Quality & Compliance Engine...")
        
        try:
            with open(config.INPUT_FILE, "r", encoding="utf-8") as infile:
                lines = infile.readlines()
        except FileNotFoundError:
            print(f"❌ Error: Could not find target file named '{config.INPUT_FILE}'. Please verify paths.")
            return

        fingerprints = {}
        report_summary = []
        
        train_buffer = []
        test_buffer = []

        for index, raw_line in enumerate(lines):
            if not raw_line.strip():
                continue
                
            try:
                chat_data = json.loads(raw_line)
                messages = chat_data.get("messages", [])
                
                # Check 1: Format Checks
                struct_ok, struct_log = self.validate_conversational_structure(messages)
                
                # Metric calculation
                joined_transcript = " ".join([m.get("content", "") for m in messages])
                tokens_count = self.calculate_approx_tokens(joined_transcript)
                
                # Check 2: Deduplication Mapping
                norm_text = self.normalize_text_for_dedup(joined_transcript)
                is_duplicate = False
                if norm_text in fingerprints:
                    is_duplicate = True
                    fingerprints[norm_text].append(index)
                else:
                    fingerprints[norm_text] = [index]

                # Check 3: Hybrid Audit Logic
                keyword_flags = self.execute_deterministic_keyword_guardrail(joined_transcript)
                llm_ok, violations_list, judge_notes = self.execute_llm_compliance_audit(joined_transcript)
                
                # Aggregate Safety Verdict
                passed_safety = (len(keyword_flags) == 0) and llm_ok
                overall_passed = passed_safety and not is_duplicate
                
                all_violations = list(keyword_flags)
                if violations_list:
                    all_violations.extend(violations_list)

                # Step 4: Routing Split Processing Data
                if overall_passed:
                    split_allocation = "test" if (index % 5 == 0) else "train"
                    if split_allocation == "train":
                        train_buffer.append(raw_line)
                    else:
                        test_buffer.append(raw_line)
                else:
                    split_allocation = "REJECTED"

                report_summary.append({
                    "id": index,
                    "tokens": tokens_count,
                    "struct": "✓" if struct_ok else f"✗ ({struct_log})",
                    "dup": "⚠️ Duplicate" if is_duplicate else "Clear",
                    "safe": "✓ Safe" if passed_safety else "✗ Flagged",
                    "split": split_allocation,
                    "notes": judge_notes[:50] + "..." if judge_notes else ("Violations: " + ", ".join(all_violations) if all_violations else "Verified Clean")
                })
                
            except json.JSONDecodeError:
                report_summary.append({"id": index, "tokens": 0, "struct": "✗ Dead JSON Parse", "dup": "-", "safe": "-", "split": "REJECTED", "notes": "Malformed JSON line."})

        # Save Valid Output Pools
        with open(config.TRAIN_OUTPUT, "w", encoding="utf-8") as f_train:
            f_train.writelines(train_buffer)
        with open(config.TEST_OUTPUT, "w", encoding="utf-8") as f_test:
            f_test.writelines(test_buffer)

        # Print Visual Report
        print("\n=== DATASET EVALUATION COMPLIANCE REPORT ===")
        table_data = [[r['id'], r['tokens'], r['struct'], r['dup'], r['safe'], r['split'], r['notes']] for r in report_summary]
        print(tabulate(table_data, headers=["Line", "Tokens", "Structure Check", "Dedup status", "Safety Check", "Split", "Judge Insight / Notes"], tablefmt="fancy_grid"))
        
        print(f"\n📊 Pipeline Execution Metrics Completed:")
        print(f"   - Successfully saved to Train Pool ({config.TRAIN_OUTPUT}): {len(train_buffer)} rows")
        print(f"   - Successfully saved to Test Pool ({config.TEST_OUTPUT}): {len(test_buffer)} rows")
        print(f"   - Total flagged/excluded rows: {len(lines) - (len(train_buffer) + len(test_buffer))}\n")

if __name__ == "__main__":
    pipeline = ProductionChatChecker()
    pipeline.execute_pipeline()