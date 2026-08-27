# Full four-port replay: proof boundary

This package is an active replay of the complete bounded four-port universe.
It is not a recheck of the previously frozen fourteen-orbit answer.

## Producing boundary

`generate_full_four_port_replay.py` begins with the literal primitive
cycle/four-theta grammar in the bundled K3P atlas compiler.  It constructs six
sources, 831 incoming-selected targets, 1,983 incoming-marginalized targets,
and all 24 labelled port permutations.  Thus it visits

\[
6(831+1983)24=405216
\]

directed presentations.  It does not read the historical raw ledger, the
frozen fourteen-orbit lock, or the former cloud descriptor corpus.

The producing compiler is an input, not an independent witness.  Its output
is accepted only after the separate verifier reconstructs the graph grammar,
maps, ranks, polynomial pullbacks, graph relations, and quotient without
importing either the producer or the atlas compiler.

## Rank-upper mechanism

For a target map \(f\) with parameter vector \(x\) and inheritance coordinates
\(\lambda\), the replay solves coefficientwise for polynomial vector fields

\[
V(x_i)=x_iA_i(\lambda),\qquad
V(\lambda_j)=\lambda_j(1-\lambda_j)C_j(\lambda_{\ne j})
\]

such that \(J_fV=0\) as a polynomial identity.  Let \(A\) be the exact integer
coefficient matrix of these identities and let \(E\) be evaluation of the
vector-field coefficients at the recorded strict rational point.  Exact
linear algebra gives

\[
\dim E(\ker A)=\operatorname{rank}\!\begin{bmatrix}A\\E\end{bmatrix}
-\operatorname{rank}(A).
\]

A nonzero evaluation minor remains nonzero on a Zariski-open set.  Therefore
the corresponding exact syzygy fields are generically independent and give
the stated a priori generic target-rank upper.  A sampled Jacobian rank is
used only for a nonzero lower-rank minor; it is never treated as an upper
bound.

When this syzygy ansatz does not by itself give a strict enough upper bound,
the replay retains the presentation until an exact polynomial obstruction is
found.  In particular, 88 such presentations are separated by a literal
transport of the normalized three-leaf \(H_{14}\) quartic: the target
pullback is zero coefficientwise, while the source pullback is nonzero and
has a nonzero value at a strict rational physical point.

## Restoration boundary

The dummy-completion test alone is not accepted as a proof.  After all exact
topology, rank, quadratic, \(H_{14}\), and graph-relation filters, the replay
derives exactly 2,540 restoration presentations in 997 K3P-local map classes.
The independent verifier matches the independently derived
`(source, target, permutation)` triples bijectively to the 2,540 active forest
roots, then checks all 36,568 active first-layer K3P children and their proof
registry bindings.  It also checks the four-port anchor crosswalk into the
active probe package.  Historical companion class ordinals are deliberately
not inferred from K3P-local class ordinals.

## Acceptance boundary

The replay is accepted only if the independent verifier derives all of the
following simultaneously:

- 405,216 primitive presentations;
- 27,834 post-topology presentations;
- 13,686 compatible target/permutation keys and 4,379 literal map
  descriptors including sources;
- 2,540 restoration obligations in 997 classes, with complete active routing;
- 40 final complete presentations, decomposed as 38 members of fourteen
  canonical orbits plus two separately classified sink swaps; and
- exact rejection of coherent omission and reclassification mutations and of
  optimized Python execution.
