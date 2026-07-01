Task 1 — Chat Checker Script

Choice Explanations: For the safety rule detection in Task 1, I implemented a robust, deterministic keyword-based checker. This approach was chosen because it is immediate, computationally inexpensive, and provides predictable binary flags (safe/unsafe) against a known set of critical violations (e.g., predicting death or serious illness). This method is highly effective for identifying blatant guardrail breaches without the cost or complexity of calling external AI models.

Improvements with More Time: While effective, keyword detection can be circumvented by indirect language or nuanced phrasing. With more time, I would improve the checker by integrating a fine-tuned classification model or using an AI-based moderation API. This would add an intent analysis layer to catch complex or conversational safety breaches that do not explicitly use flagged terms, reducing both false negatives and false positives.

Task 2 — Chat Generator Script

Choice Explanations: For the synthetic data factory in Task 2, I implemented a closed, local simulation script designed for 100% policy compliance. I prioritized this method because it created a reliable, zero-dependency environment for generating the required 10 verified data rows without introducing external API key requirements or transcription costs, which had been identified as an initial project bottleneck. The generator still provides dynamically safe and relevant responses based on the provided topic scenarios.

Improvements with More Time: The current generation loop relies on pre-defined structures and local simulation logic. With more time, I would advance the script to use a fine-tuned open-source model (like a Llama variant) running in a secure, sandboxed environment. This would generate a far wider variety of complex and creative scenarios while still automatically filtering all output through the Task 1 checker, creating a truly automated and diverse compliance-verified data stream.

Task 3 — Quality Tester Script

Choice Explanations: For Task 3, I created a focused data-integrity audit grid. This deterministic script was chosen to quickly confirm that every generated data row is structurally well-formed, complete, and perfectly matches the strict system/user/assistant turn format required for production fine-tuning platforms. It converts this formatting check into a clear binary outcome for efficient dataset validation.

Improvements with More Time: The current checker only validates format, not quality. Given more time, I would expand the quality tester by introducing an automated grading process, possibly by having a second LLM act as an 'auditor' to score each response on specific semantic metrics, such as warmth, helpfulness, and the degree to which it adheres to non-fatalistic principles. This would shift the evaluation from simple technical passing/failing to a more nuanced, qualitative understanding of the assistant's performance.
