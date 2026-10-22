# Coarse endpoint concentration at every diverging scale

Alec Kriebel — ORCID https://orcid.org/0009-0001-9320-500X. Version 1.0, 18 October 2026.

The self-contained 11-page note proves the affirmative one-dimensional assertion contrary to Conjecture 1 in Noam Berger's contribution to Oberwolfach Report 38/2009, printed pages 2151–2152, DOI https://doi.org/10.4171/OWR/2009/38. Repository problem30001321 / OWR-4081-005; source PR https://github.com/AlecKriebel/Math/pull/239.

For any fixed iid nearest-neighbor space-time environment with 0<p<1 almost surely, the quenched and averaged endpoint laws become close in full coarse L1 distance on deterministic intervals of any lengths M_N tending to infinity, with environmental fixed-epsilon tails O(N^-K) for every fixed K. Biased laws, parity, real half-open intervals and arbitrary deterministic alignments are included. Constants depend on the fixed law; the eventual threshold may depend on the scale sequence. No uniform ellipticity, inverse-moment assumption or lower growth rate for M_N is needed. The theorem makes no law-uniform assertion near arrow environments or claim about static/correlated environments or environment-adapted partitions.

## Priority and review status

Originality and historical priority remain unresolved. The bounded primary-source audit found no verified full anticipation, but the complete original texts of BMP1999, BP2001, BMP2004 and Berard2004 could not be obtained; their internal estimates have not been eliminated as antecedents. The manuscript and detailed ledger identify them precisely. Replica, martingale, ordered coalescence, bounded differences and final-layer/local-corrector mechanisms are established methods; Dunlap–Gu2022 and Barraquand–Rychnovsky2023 receive explicit credit. We claim no firstness, independent discovery, new method or present-day open status.

AI tools were used extensively in solving, drafting and verification. The work is unrefereed and has not undergone conventional human peer review. Finite assertion counts represent parameter instances, not independent theorems. The asymptotic claim rests on the written analytic proof.

## Files and reproducibility

The published paper is coarse_endpoint_concentration.pdf. Its complete LaTeX source main.tex is included in coarse_endpoint_verification.zip alongside the verification subtree. The source compiles using standard LaTeX packages; it was checked with the built-in desktop compiler and Tectonic0.16.9 using cached resources.

Read verification/README.md before executing verification/verify.py from an extracted archive. The portable verifier authenticates its finite file manifest and the32 historical native Git blobs, then runs each selected checker in its own temporary directory. It never executes the archived environment-specific historical replay driver. The default suite uses only Python's standard library; the optional original turn1 checker additionally requires the pinned SymPy version. Consult the verifier's actual output for counts. Its checks supplement general proofs and do not certify novelty.

Historical pending-review statuses and self-reported turn/reviewer claims are retained as dated evidence. Manifests authenticate bytes and internal references, not physical creation times, distinct reviewer identity, absence of pre-freeze influence or historical PDF access. Fresh mathematical derivations and the current dated priority ledger accompany them. Third-party full texts, personal credentials, raw API journals, provider responses and spreadsheet contents are excluded.

The Zenodo manifest zenodo-deposit.json records the exact intended metadata and the two publication files. Publishing and spreadsheet updates are separate actions performed only after the package review workflow. No GitHub release should be created for this deposit, because this repository's release integration could create a second DOI.
