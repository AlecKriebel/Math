# Audited candidate: primary minimal-surface Seshadri bound

2026-10-04. Research status: **claimed_solved, 5/5**, with a separate source-first independent AI audit. The work is unrefereed, and historical novelty is unverified. This is an AI-assisted mathematical candidate and verification package, not an assertion of external peer review or first priority.

## Mathematical outcome and scope

The primary conjecture is Conjecture 2 on printed page 1124 of Oberwolfach Report 21/2009:

    epsilon(S,L;x) >= 1/(2+|K_S^2|^(1/4)).

Its quantifiers include every smooth minimal complex projective surface S, every ample integral line bundle L, and every point x. The additive 2 is outside the fourth root. The catalogue's stronger transcription places it inside and is not the formula used as the principal target.

The frozen author proof constructs examples for all d>=7 by a double base change of a plane pencil, branched over four smooth fibres. At d=7 the final surface has ample canonical bundle and K_S^2=144, hence is minimal; L is ample with L^2=6. An integral curve through the specified point has L-degree1 and multiplicity6, proving epsilon<=1/6<1/(2+144^(1/4)). The point is a special point, and the underlying surface varies with d. Neither a very-general-point theorem nor a fixed-surface vanishing claim is made. The exact value of epsilon is not claimed.

## Separate clarification without changing the author freeze

Bauer's cited degree choice d=m+1 in Proposition 3.3(b) is asymptotic. It supports the classical Miranda mechanism but does not alone establish the finite degree d=7. Section 1 of the frozen PROOF.md independently establishes that degree through an explicit integral singular curve and a nonempty-open pencil argument. The separate audit checked this distinction and found no missing construction step.

For the canonical ampleness calculation, the additional explanatory identity

    N=K_Y+2F=(d-3)H+F

shows that N has positive intersection with every nonexceptional curve since H and F are nef, while N.E_i=1 for exceptional curves. Together with N^2>0 this recovers the all-curve Nakai-Moishezon argument already present in the proof. No original author or audit file has been altered to add these clarifications.

## Evidence and reproduction

- The original author packet and its original SHA256SUMS are retained under author/.
- The full separate mathematical review, independent program, result, and original audit manifest are retained under audit/.
- The audit found a complete counterexample to the primary conjecture, with no fatal error or required mathematical repair.
- The independent program uses a separate incidence-hypersurface/Chow-ring calculation and exact singular-scheme controls. Its 60,731 checks include reproduction and integrity checks, not 60,731 independent proofs.
- Run `python3 verify_release.py` from this directory. Python 3 and SymPy 1.14.0 were used. This checks the strict file manifest, the frozen author and audit bindings, and byte-exact results of all three programs.
- `python3 test_integrity.py` checks rejection of changed, missing, extra, symlinked, traversal-manifest, and duplicate-manifest content, as well as optimized execution.

The arithmetic checks do not establish geometric existence or historical priority. The mathematical review addresses the geometric arguments separately. Source PDFs, source extractions, source images, and catalogue corpora are not included. Their citations and fingerprints are preserved where appropriate.

The author snapshot retains its original pre-audit status statements; this note and the separate audit give the subsequent disposition without rewriting that history. No merge, public paper release, Zenodo deposit, DOI, or external outreach is included in this draft-PR step.
