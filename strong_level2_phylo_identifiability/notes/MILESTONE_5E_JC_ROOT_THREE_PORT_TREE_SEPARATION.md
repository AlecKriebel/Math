# Milestone 5E: exact tree/reticulation separation at three root ports

## Result

Let

\[
F=r_{12}r_{13}r_{23}-u_{123}^2
\]

on the four nontrivial three-port JC Fourier orbits.

**PROVED.** Every open ordinary-tree parameter point satisfies `F=0`, while
every open parameter point of every reticulate three-port root cycle or theta
satisfies

\[
\boxed{F>0.}
\]

Consequently, the complete open stochastic interiors of the tree class and
the `R3` reticulate class are disjoint.  In particular, neither one-sided
generic containment occurs.

Combined with Milestone 5D, this completes both `bowtie_JC` and one-sided
containment classification for all three-port root factors.

## Tree identity

An ordinary three-port tree has effective arm multipliers `a,b,c`, giving

\[
(r_{12},r_{13},r_{23},u_{123})=(ab,ac,bc,abc).
\]

**PROVED.** Direct substitution gives `F=0` identically.  Its model has
dimension three.

## Exhaustive reticulate certificate

Milestone 5D exhaustively enumerates two unlabelled root cycles and five
unlabelled root theta blobs.  For each topology, substitute its complete
displayed-tree Fourier parameterization into `F`.

Every pendant multiplier occurs as a common positive square factor.  Divide
those three factors out.  Next divide every exact factor of the form `x_e` or
`1-x_e`; all are strictly positive on the open stochastic cube.  Call the
remaining polynomial `P`.

Write `P` in its natural tensor-product Bernstein basis on `[0,1]^d`:

\[
P(x)=\sum_{0\le k_i\le d_i}
b_k\prod_i {d_i\choose k_i}x_i^{k_i}(1-x_i)^{d_i-k_i}.
\]

If `P=sum_j a_j x^j` in the power basis, the verifier computes every
coefficient exactly from

\[
b_k=\sum_{j\le k}a_j
\prod_i\frac{{k_i\choose j_i}}{{d_i\choose j_i}}.
\]

**EXACTLY COMPUTED.** The exact coefficient counts are:

| topology | negative | zero | positive |
|---|---:|---:|---:|
| balanced root cycle | 0 | 3 | 6 |
| unbalanced root cycle | 0 | 0 | 1 |
| theta `TR-nested` | 0 | 10,824 | 1,464 |
| theta `TR-separated`, placement 1 | 0 | 633 | 1,671 |
| theta `TR-separated`, placement 2 | 0 | 21,560 | 3,016 |
| theta `TT-nested`, placement 1 | 0 | 7,510 | 266 |
| theta `TT-nested`, placement 2 | 0 | 4,916 | 268 |

Every coefficient lies in `[0,1]`, and every row has at least one positive
coefficient.

**PROVED.** Every tensor-product Bernstein basis function is strictly
positive when all variables lie in `(0,1)`.  Thus each residual `P` is
strictly positive there.  Restoring the removed pendant and boundary factors
proves `F>0` on the complete open parameter cube for all seven reticulate
topologies.

This is a complete symbolic sign certificate, not sampled evidence.

## Exact local classification

**PROVED.** The three-port root atlas has exactly two stochastic classes:

1. ordinary trees: dimension three, `F=0`;
2. all reticulate cycles and thetas: dimension four, `F>0`, with the common
   regular overlap from `R3`.

The classes have disjoint open images, so the ordered-pair categories are
complete:

- within the tree class: equality of the complete open image by reversible
  root placement;
- within the reticulate class: full-dimensional regular overlap;
- between the two classes in either direction: disjoint open stochastic
  interiors, hence no one-sided containment.

**UNRESOLVED.** Equality of the complete open images of distinct `R3`
reticulate topologies is not claimed.  The proved relation is the required
full-dimensional regular overlap.

## Machine replay

- `src/verify_jc_root_three_port_tree_separation.py` regenerates all eight
  unlabelled models, exact pullbacks, boundary-factor divisions, and every
  Bernstein coefficient.
- `certificates/jc_root_three_port_tree_separation.json` records the factors,
  multidegrees, coefficient counts, extrema, and coefficient hashes.

No numerical evidence or literature search is used.
