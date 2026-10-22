# Hermite tetranomial strip problem

**2304006 / AMR-022-4006 · Hayman–Lingham Problem4.6 · Unsolved, 5/5 attempts**

The full question remains unresolved: is there an absolute C such that
1+H1+aHn+bHm always has a zero with |Im z|<=C, for arbitrary complex a,b and
2<=n<m?

Verified partials:

- Every real-coefficient instance has a real zero.
- For the full complex cubic subfamily n=2,m=3, the sharp half-width is
  C3=0.903669747226..., with an exact algebraic formula and attaining triple zero.
- Any affirmative answer to the full question must use C>=C3.
- Every fixed pair of degrees admits a coefficient-independent bound. The
  unbounded-degree limit is the unresolved part.
- Explicit Rouché sufficient regions and an exact differential-elimination
  identity are available, with their missing uniform implications stated.

Read `SOURCE_GATE.md`, then `PROOF.md` and `CUBIC_SUBCASE.md`. The five
approach records and `RESEARCH_LOG.md` explain why the general problem is not
claimed solved. No novelty or priority claim is made for the partial results.

## Reproduce finite checks

Run `python verify.py` from this directory using Python3 and SymPy. The authored
run used Python's installed SymPy1.14.0. Compare stdout with `verification.json`.
The exact finite checks cover identities and rational constant brackets;
compactness, Rouché, positivity and half-plane arguments are proved in the text.
No finite computation certifies the degree-uniform conjecture.

`numerical_exploration.py` is an optional deterministic-seed exploratory search,
requiring NumPy and SciPy. Its finite parameter box and local optimization
outputs are evidence only. They are not used as proof certificates, sharpness
certificates, or evidence of a global search over all coefficients.
