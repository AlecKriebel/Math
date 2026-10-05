# Stringy Euler smoothness criterion: bounded research packet

Target identifier: 30002003 / OWR-11580-009, rank 712.

**Split result:** the literal dataset statement is false because it omits a necessary hypothesis. A complete counterexample is the factorial quadric cone `{x1*x2+x3*x4+x5^2=0}` times C*: it is singular and spherical, but both Euler numbers are zero. This does NOT resolve the full Batyrev–Moreau Conjecture 6.7, whose projective-closed-orbit hypothesis excludes this example. No novelty is claimed for the product mechanism or retained partial results.

The mathematical formulation was checked in the primary Oberwolfach report, pp. 766–767, and in Batyrev–Moreau, Conjecture 6.7. The latter concerns normal, locally factorial complex spherical embeddings, under a connected reductive group, whose closed orbits are projective. It asserts e_st(X) >= e(X), with equality exactly for smooth X. The closed-orbit condition is essential; it is weaker than requiring X itself to be complete or projective. The literal imported statement recovered from the public dataset omits that condition.

The exact UnsolvedMath webpage was requested but could not be retrieved (web errors and HTTP 403). A later public Hugging Face filter returned the complete unique ID 30002003 record, untruncated, at row 10787. Its ID, problem number, title, primary-source URL, and full statement were checked. Old raw AI-report corpora remain unavailable, so complete prior-attempt absence is not established. See SOURCE_VERIFICATION.json and HISTORY_AND_LIMITATIONS.md.

The January 2026 preprint by Gagliardi–Hofscheier–Pearson proves a different numerical smoothness criterion and explicitly describes the stringy extension as conjectural. The 2016/2017 Batyrev–Gagliardi Mori-program result does not establish this conjecture.

Files:
- STATEMENT_AUDIT.md: literal dataset counterexample versus the correctly qualified conjecture
- PROOFS.md: five approach families, retained proofs, exact obstructions; Approach 4 contains the complete counterexample
- RESEARCH_LOG.md: scoped attempt accounting and non-probabilistic progress estimates
- SOURCE_VERIFICATION.json: public bibliographic, retrieval, hash, and inspection metadata only
- HISTORY_AND_LIMITATIONS.md: history and source limits
- verify.py and CHECK_RESULTS.json: exact finite checks and false-shortcut controls
- AUTHOR_MANIFEST.json: frozen authored-file hashes

Run `python3 verify.py` in this directory. The checks corroborate exact calculations; they do not certify the general conjecture or substitute for the written geometric proofs. This packet has not yet received the required independent adversarial audit. No remote write or publication was performed by this investigation.
