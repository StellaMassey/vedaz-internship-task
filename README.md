# Vedaz AI Astrology Alignment & Compliance Pipeline

This project contains a complete evaluation and synthetic data generation pipeline designed for **Vedaz**. It ensures that automated Vedic astrology transcripts completely adhere to core safety policies (no fear-mongering, medical/legal redirections, and optional spiritual remedies).

## 📁 Project Structure
* `config.py` - Centralized configuration and environment settings.
* `task1_checker.py` - Processes data, applies keyword guardrails, and splits datasets into Train/Test subsets.
* `task2_generator.py` - An automated local synthetic chat data factory creating policy-compliant rows.
* `task3_tester.py` - Quality control script verifying the format and structure of the generated data grid.
* `generated_output.jsonl` - The finalized dataset containing 10 verified sample conversations.

## 🚀 How to Run Locally
1. Clone the repository.
2. Run the synthetic data factory:
   ```bash
   python task2_generator.py
