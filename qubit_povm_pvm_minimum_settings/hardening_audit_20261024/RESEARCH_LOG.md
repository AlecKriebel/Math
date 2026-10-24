# Main two-input equality hardening audit

## 2026-10-24 — start (completion estimate: 20%)

User requested a fresh assessment of what would make the main two-input-per-party equality stronger. Inspect actual models and unconditional proof, commission independent mathematical and verifier reviews, and implement bounded validation improvements. Preserve the frozen September source/package/certificates and unrelated work. No external outreach or immutable release.

The actual repository-root workflow currently runs exact numerical artifacts and PDFs only. The nested bell_lean/.github/workflows/lean.yml is a standalone-project template, not an active monorepo workflow. Add an active root Lean job using the pinned existing verifier, full contracts and public dependency audit; retain receipts even on failure. Whether Lean --trust=0 really rechecks imported terms is under source inspection, not assumed from help text.
