# Involution product-order reconstruction: partial results

**Problem:** Kourovka Notebook 21.52, I. B. Gorshkov; catalogue ID2561, queue rank464.

**Outcome:** Unsolved after five substantive attempts. No counterexample to the full question, new-discovery claim, paper, or DOI. The partial proofs and exact checks below await independent adversarial audit.

For a finite nonabelian simple group L and one conjugacy class D of involutions, color each pair of distinct members by the order of its product. Must every permutation preserving those colors come from an automorphism of L stabilizing D?

## What this package establishes

1. An exact extension criterion: a color permutation extends precisely when it preserves the ternary conjugation operation (a,x) -> axa.
2. An elementary reconstruction for A5.
3. A self-contained affine-hyperplane argument for every characteristic-two symplectic transvection class. In particular, all even-q PSL2 involution classes are covered.
4. A computer-assisted proof for double transpositions in every A_n, n>=5. A proved support reduction reduces all n>=12 to one modest degree12 local-signature certificate; n5..11 are separately covered.
5. Exact full colored-graph certificates for A6/A7 double transpositions, A8 fixed-point-free involutions, PSL2(7), PSL2(11), and PSL2(8).
6. A general sufficient local two-point reconstruction criterion and a padding-probe restriction for larger alternating involution classes.

A separate credited consequence of Bryden-Rowley, arXiv2509.25901v2, Theorem1(ii), covers odd-q PSL2 for q>=7: preserving every color preserves the commuting graph, and its automorphism group is already Aut(PSL2(q)). The cited theorem itself is not independently reproved here. Together with A5 and the even-q argument, this covers the PSL2 family. The primary result predates these attempts.

No historical novelty is claimed for any family result or method. The package is a research record rather than a universal solution.

## Remaining problem

The proof does not cover arbitrary higher-rank involution classes, arbitrary larger matching types in A_n, or all exceptional/sporadic simple groups. A failed sufficient local criterion is not a counterexample to the graph-automorphism claim. In particular, four-transposition classes at n9 and n10 have local size4 signature fibers, but no nonextendible global color permutation was produced.

Problem21.53 has a confirmed negative solution in the October Notebook, but that example changes colors and therefore does not settle21.52.

## Contents and replay

- attempts/turn_01.md through turn_05.md: substantive arguments, exact gaps and scope
- checks/: standard-library Python checkers, expected-result checks and complete run outputs
- SOURCES.md: source versions and priority qualifications
- AUDIT_SCOPE.md: obligations for independent review
- status.json: conservative machine-readable outcome
- MANIFEST.json: SHA256 hashes of this frozen package

Run from this directory with Python3:

    python checks/run_all.py

No third-party package is needed. Do not use Python's -O flag: assertions are proof checks, and the aggregate runner rejects optimized mode. The complete run took about55 seconds on the authoring environment; timings vary. The largest graph-automorphism enumeration has105 vertices and709 search nodes. The degree12 alternating calculation checks local signatures of1485 involutions against269 commuting involutions; it does not enumerate1485! permutations.

The runner verifies the expected numerical outputs and checks a negative control: collapsing A5's noncommuting colors creates a symmetry that fails conjugation preservation, and the checker must reject it. A successful replay supports the finite certificates; it does not replace review of the mathematical reductions or certify the unrestricted problem. This is not a Lean/Rocq proof-assistant certificate.

Current verification: all positive checks passed; the negative control was rejected; independent adversarial review is pending.
