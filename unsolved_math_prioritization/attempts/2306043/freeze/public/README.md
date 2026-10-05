# Function Theory 6.43: five-approach partial investigation

**Problem:** 2306043 / AMR-022-6043, ranked queue position 683.
**Disposition:** unresolved; five substantive approaches used; no full-class proof or counterexample. Recommended queue outcome: `exhausted`, `5/5`. Discovery count: zero. This is an authored partial investigation, not a claimed solution.

Let S be the holomorphic injective maps of the unit disk with f(0)=0 and f'(0)=1. Use the analytic logarithm normalized at zero:

    log(f(z)/z) = 2 sum_{n>=1} gamma_n z^n.

The question is whether every fixed f in S satisfies

    A_f(r) = sum_{n>=1} n |gamma_n| r^n = O_f((1-r)^(-1)),  r -> 1-.

The source does not explicitly require a constant uniform over S; this package does not silently strengthen that quantifier. A counterexample would have to be one fixed univalent function with unbounded (1-r)A_f(r).

## Results retained

1. A_f(r) has the classical weaker bound sqrt(r log(1/(1-r)))/(1-r), from the published de Branges–Milin inequalities. The square-root logarithm remains.
2. A_f(r)=O_f((1-r)^(-1)) is equivalent to sum_{n<=N} n|gamma_n|=O_f(N). A uniform bound on each dyadic weighted-square energy would suffice, but Hayman's example recorded in the primary problem update rules out that stronger intermediate claim in general.
3. Starlike functions of order sigma, 0<=sigma<1, satisfy A_f(r)<=(1-sigma)r/(1-r), sharply. Phase-aligned logarithmic coefficients also remove cancellation directly. These are proper subclasses.
4. The published Bazilevich inequality implies, whenever the Hayman index is positive,

       (1-r)A_f(r) -> 1,
       N^(-1) sum_{n<=N} n|gamma_n| -> 1.

   This is a deduction from an established theorem, with no novelty claimed. The full-class gap remains among zero-index functions outside the covered subclasses.
5. An explicit Rudin–Shapiro block construction satisfies both the signed analytic growth bound and stronger-than-needed Milin partial-energy bounds, while its absolute majorant violates the target order. Its associated normalized, bounded, zero-free-quotient holomorphic map has a proved critical point and is **not univalent**. It is a counterexample only to a relaxation of the problem. This prevents promoting generic coefficient estimates into a purported solution.

Read `EXACT_TARGET_AND_SOURCE_SCOPE.md` for definitions, source limitations and duplicate checks. The five `TURN_*.md` files contain the complete arguments and exact gaps. `verify_controls.py` is standard-library-only; run `python3 verify_controls.py`. Its finite controls check identities and boundary safeguards, not the infinite assertions or univalence.

All files in this directory are authored mathematics/code or public verification metadata. Source PDFs, extracted text, raw catalog entries, and private coordination are outside the publication set. No remote writes were made by this investigation. A fresh independent audit is required before publication.
