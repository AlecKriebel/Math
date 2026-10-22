# Exact dimension-two dilation thresholds

This packet gives an elementary sharp threshold calculation for problem 30001058, restricted to ambient degree two. The controlling target is Theorem 2 and Corollary 3 of Beck's contribution, joint with Stapledon, in Oberwolfach Report 44/2008, printed pages 2498–2500.

For positive integers $N,m$, the full original theorem, including conditional strict alternation, and the lattice-polygon package have exactly the feasible pairs

\[
N\ge4,\qquad m>\frac{N+4}{N-2}.
\]

The imported unconditional coefficient/root package has exactly the feasible pairs

\[
N\ge3,\qquad m>\frac{N+4}{N-2}.
\]

In either expression, the integer condition is $m\ge\lfloor(N+4)/(N-2)\rfloor+1$. The strict inequality is essential because the ratio extremum is attained by constant inputs and by the unimodular triangle.

For the full theorem and polygons, the least dilation threshold is $N=4$, requiring $m\ge5$. The smallest possible multiplier is $m=2$, first valid at $N=9$. The coordinatewise nondominated pairs are $(4,5),(5,4),(6,3),(9,2)$. The unconditional package additionally admits the nondominated pair $(3,8)$. There is no pair that simultaneously minimizes both coordinates.

## Reading the packet

- [PROOF.md](PROOF.md) gives the complete operator derivation, coefficient positivity, distinct negative roots, strict log-concavity, ordered root limits, attained ratio extremum, strict-boundary obstructions, conditional alternation, actual-polygon witnesses, and integer optimization.
- [AUDIT.md](AUDIT.md) records the mathematical acceptance checks and source qualifications.
- [ACCEPTANCE.json](ACCEPTANCE.json) records the exact accepted scope and feasible sets.
- [SOURCE_PINS.json](SOURCE_PINS.json) gives the public bibliography, PDF hashes and byte counts, and limited retrieval and inspection history.
- [VERIFICATION.json](VERIFICATION.json) records aggregate verification results.
- [MANIFEST.json](MANIFEST.json) lists the exact public file set and hashes every other public file. Its own digest is recorded separately at preparation.

The Oberwolfach report controls the conditional hypothesis $a+b>c$ for general input with $a\ge1$. The related Beck–Stapledon PDF uses $h_0=1$ and a differently worded conditional hypothesis. Later real-rootedness results provide context; they do not replace the full-degree, strict-alternation, or ratio arguments in this proof.

The proof establishes universal statements by algebra. Exact finite tests are supporting checks, not substitutes for those arguments. No result in other dimensions, current general-problem status, or novelty is claimed.
