# 2142 / EP-488: accepted prior finite refutation

Publication edition prepared 10 October 2026.

The complete elementary proof of a finite counterexample to the multiples-density inequality is accepted after AI-assisted mathematical audit. The construction, proof and Lean formalization are credited to **Declan Gessel, with disclosed GPT-6 Astra assistance in Codex, September 2026**. This is an audit of identified prior work, with no novelty or priority claim.

For a nonempty finite set A of positive integers, let M_A(x) count positive integers at most x divisible by at least one member of A. The accepted result gives integers m>n>=max(A) with

    2 m M_A(n) < n M_A(m).

All constructed generators exceed 1. The proof establishes a finite existential parameter 0<=k<4096; neither k nor the corresponding generators/endpoints have been enumerated in this audit.

## Contents and mathematical scope

- `AUDIT.md`: complete accepted analytic proof, original-statement interpretation, source inspection, adapter analysis and formal-evidence limits.
- `ACCEPTANCE.md` and `ACCEPTANCE.json`: acceptance report and unchanged structured verdict.
- `CITATIONS.json`: public titles/URLs, source byte/hash pins, historical retrieval and inspection records, and the author's stated review status.
- `SOURCE_BINDING.json`: unchanged source-identity and literal retained-statement match metadata, with external-run limits.
- `VERIFICATION.json`: selected historical check metadata, excluding raw computational certificate contents.
- `MANIFEST.json`: exact eight-file publication inventory and byte/hash identities of the other seven members; its own digest is independently pinned in the proposed PR body.

The full proof retains the exponent-vector bound, finite-growth contradiction, all generator and endpoint obligations, exact near-count identity, exponent-residue injection, coprime far-count injection, strict comparison, and the exact statement adapter's positivity/maximum/count/division bridge. No mathematical correction was required.

## Original statement and formal boundary

The controlling primary source is Erdős's 1966 section II.6, printed page 150, which explicitly counts multiples. The 1961 I.27 sentence, printed page 236, literally says nonmultiples; that wording is preserved and no conclusion about that separate interpretation is claimed.

The retained server-source GitHub run reports success at commit `ccf4a26cb8a8c49f476d44304070a2b677da4d7e`. This audit performed no local Lean build, kernel replay or transitive axiom audit. That external success is not a replay of the later gist adapter. The complete ordinary mathematical argument and adapter content were accepted on their own merits.

## Editorial and reproducibility boundary

This is an authored-prose and public-verification-metadata edition, not an executable reproduction package. Source PDFs/text/code, checker code, raw products/gaps/prime lists/certificates, private sources and private coordination are excluded. The audit's optional explicit numerical-gap and raw-certificate discussion is replaced with a historical-check summary; all analytic constants and exact inequalities remain. The three selected metadata reports are unchanged.

Statements about reading sources or checking arithmetic describe the completed accepted audit. Publication preparation verifies bytes, the bounded editorial transformation and native additions-only structure; it makes no fresh source-inspection or proof-assistant claim. The original sealed audit remains unchanged.

This AI-assisted audit is unrefereed. It does not claim completed human specialist review, mathematical-community consensus, current external-catalogue status or exhaustive historical priority research. Public source links are supplied in `AUDIT.md` and `CITATIONS.json`.
