# Frobenius–Schur indicators in real nilpotent blocks

**Problem:** 30005507 / OWR-13750328-012  
**Research date:** 3 October 2026  
**Outcome:** Unsolved after five substantive approaches. No complete proof or counterexample is claimed.

## Exact question

Let B be a real, nilpotent, nonprincipal 2-block with defect pair (D,E). Does there exist a height-preserving bijection Gamma:Irr(D)->Irr(B) satisfying

    epsilon(Gamma(lambda)) = |D|^(-1) sum_{e in E outside D} lambda(e^2)

for every lambda in Irr(D)? This is Sambale's Conjecture B, also Conjecture 2 on p.1055 of the original Oberwolfach report.

## Findings

1. The abelian and dihedral defect cases, and solvable and quasisimple ambient cases, are existing results. No inspected primary source provides the general theorem.
2. An explicit induction calculation proves the formula in the existing universal model C3 semidirect E for every pair (D,E). Transferring it to an arbitrary block remains the hard part.
3. The local indicator is the trace of a square-corrected flip on a zero- or one-dimensional invariant-tensor space. A Morita approach must preserve its sign, including the biduality coherence determined by t^2. Matching the duality permutation alone does not suffice.
4. An exact Q8 times Q8 example gives two distinct height-sign distributions with the same real-character counts, positive height-zero signs and scalar projective indicator. The incorrect distribution is only a numerical assignment; no block realizing it is claimed. This blocks a shortcut, not the conjecture.
5. Full local subsection square-count identities would determine all indicators by a short positivity and character-orthogonality argument. These identities follow from suitable local and central-quotient projective formulas, as proved in the literature, but those formulas are not established here in general.

## Verification

The standard-library verifier checks all 32 compatible marked index-two extension presentations of Q8, including 160 model-character indicators and 800 exact inner products. All assertions passed. These model groups are solvable, so the checks are not new evidence from the unresolved ambient cases.

Run:

    python3 check_indicators.py

The script writes [exact_results.json](exact_results.json). It uses integer arithmetic in Z[zeta_3], not floating-point character values. Repeated isomorphic presentations are deliberately retained and are not counted as distinct groups.

## Contents

- [Source and scope check](SOURCE_GATE.md)
- [Research log](RESEARCH_LOG.md)
- [Attempt 1: universal model and induction](turn_01.md)
- [Attempt 2: corrected flip and Morita coherence](turn_02.md)
- [Attempt 3: numerical underdetermination](turn_03.md)
- [Attempt 4: conditional local reconstruction](turn_04.md)
- [Attempt 5: exact extension search](turn_05.md)
- [Reproducible exact verifier](check_indicators.py)

These are AI-assisted research notes with explicit proof boundaries, not a refereed publication or a claim of novel resolution. The stronger local problem 30005508 is related and remains a separate target.
