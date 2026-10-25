# Subagent model preference

The human explicitly instructed: stop using GPT-6 Astra Ultra for subagents and use GPT-6.1 Sol Ultra instead.

For all new subagents in this project, use `model="gpt-6.1-sol"`, `reasoning_effort="ultra"`, and `fork_turns="none"` with a self-contained handoff. Do not resume earlier agents on an inherited or unspecified model. Any descendant agents must use the same explicit model and effort.

Preserve existing scientific reports and seals. This is a prospective orchestration change; it does not authorize rewriting prior evidence, restarting a live process unnecessarily, or reducing the full research inventory.
