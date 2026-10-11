# Mathematical audit of dimension-two dilation thresholds

## Decision

**Accept the dimension-two statements in PROOF.md.** The unconditional result must not be described as giving $N=3$ for the full original theorem.

The accepted exact positive-integer feasible sets are:

- Imported unconditional coefficient/root package: $N\ge3$ and $m\ge\lfloor(N+4)/(N-2)\rfloor+1$.
- Original OWR Theorem 2 including its conditional strict alternation, and the lattice-polygon package: $N\ge4$ and the same strict integer bound on $m$.

Thus the full-source smallest-threshold pair is $(N,m)=(4,5)$; the smallest possible coefficient multiplier is $m=2$, first compatible at $N=9$. These are different optimization objectives.

## What was independently checked

1. The accepted calculation and its original-theorem-scope clarification were verified against their recorded byte counts and SHA-256 digests. Both were unchanged during verification.
2. The complete relevant OWR report contribution, printed pp. 2498–2500, was text-inspected and visually inspected from the PDF. Both thresholds are expressly positive integers. The polynomial input has degree at most $d$, so $h=1$ is permitted when $d=2$.
3. The operator was rederived from its generating-series definition, including vanishing of all coefficients above degree two. No finite-sample interpolation is substituted for this derivation.
4. The discriminant identities, positivity, exact degree, distinctness and negativity of both roots, strict log-concavity, and the ordered root limits were checked separately.
5. The coefficient-ratio maximum is attained, not only approached: $B_n/C_n=(n+4)/(n-2)$ exactly for constant inputs. The strict bound therefore requires $m>R(N)$, including at integral boundary values.
6. The original conditional hypothesis specializes to $a+b>c$; the source addendum correctly restores it. The witness $h=1$ fails $a<C_3$, so $N=3$ is impossible for the full source package.
7. The same extremizer is realized by the unimodular lattice triangle. Hence the polygon sharpness arguments use actual polygons.
8. The exact integer feasible sets and coordinatewise nondominated pairs were checked, including $m=1$, $N=2,3,4,5,8,9$, and equality at the strict ratio boundary.

## Source qualifications

- The original report, rather than a cleaned database statement or a related article abstract, controls the conditional clause.
- The inspected Beck–Stapledon PDF is arXiv:0804.3639v3, titled *On the Log-Concavity of Hilbert Series of Veronese Subrings and Ehrhart Series*. Its theorem uses $h_0=1$; this is not identical to the OWR version with $h_0\ge1$. The bibliographic title is taken from the inspected PDF; the OWR contribution retains its distinct title.
- Jochemko's real-rootedness theorem is relevant context, but lower actual polynomial degree remains possible for small dilations. It cannot be used to bypass the full-degree and strict-alternation obstructions above.

## Reproducibility and limits

Verification checked input and source byte counts and digests, symbolic identities, exact finite regression tests, and mathematical boundary controls. The verification used explicit exceptions rather than removable Python assertions. Fresh normal, `-O`, and `-OO` executions gave identical successful results, summarized in VERIFICATION.json. Symbolic and exhaustive finite checks support the written proof; the proof, not a finite grid, establishes the universal quantifiers.

No source-author code was executed. Relevant passages were inspected; the entire OWR volume and both entire papers were not read. Acceptance is limited to the dimension-two assertions proved here. No all-dimensional result, present general-problem status, or novelty assertion is made.
