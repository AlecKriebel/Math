# Correct scalarization and physical-time Foster lemmas

These lemmas are independent of the unresolved T3-2 network classification.
They record exactly what the proposed final-repair strategy may use.

## 1. Finite lexicographic scalarization

Let (h^{(1)},\ldots,h^{(r)}\in\mathbb Q^d), and let
Δ be a finite set of comparison vectors. For every (z\in\Delta), assume
that the tuple

\[
  (h^{(1)}\!\cdot z,\ldots,h^{(r)}\!\cdot z)
\]

is not identically zero. There are positive rational coefficients
α₁,…,αᵣ, with each later coefficient sufficiently smaller than the
preceding ones, such that

\[
 \operatorname{sgn}\!\left(\sum_j\alpha_jh^{(j)}\!\cdot z\right)
\]

equals the sign of the first nonzero entry of the tuple for every
(z\in\Delta).

This follows by a finite perturbation argument: after fixing
α₁,…,αⱼ, choose αⱼ₊₁ small enough that its maximum possible
contribution over the finite comparison set is smaller than half the minimum
already-fixed nonzero gap; proceed recursively. Clearing denominators gives
an integer scalarization.

This is only a finite comparison theorem. It does not create stochastic
service margins or a recurrence proof.

### Positivity condition

The statement “every coordinate is positive in at least one component” is
not enough to make the separated scalarization positive. A sufficient and
essential lexicographic condition is that, for every coordinate (i), the
first nonzero number in

\[
 (h^{(1)}_i,\ldots,h^{(r)}_i)
\]

is positive. Equivalently, include the coordinate vectors (e_i) among the
finite comparisons and require their lexicographic signs to be positive.
Then the scalarized coefficient of every species is positive, so its integer
workload has finite shells.

If an earlier component has a negative coefficient, no sufficiently
separated scalarization can both preserve that primary sign and make the
coefficient positive. This is relevant to the exceptional certificate
(W=B-C).

### Joint shells

For a workload tuple with matrix (H), all componentwise sublevel sets are
finite exactly when its recession cone is trivial:

\[
 \{v\in\mathbb R^d_{\ge0}:Hv\le0\}=\{0\}.
\]

Nonnegative rows that collectively give every coordinate a positive
coefficient are a simple sufficient condition. Merely placing a positive
coefficient somewhere in each column is not sufficient when other entries
can be negative.

## 2. Scalar shell-adapted physical-time Foster theorem

Let (X) be an irreducible, nonexplosive CTMC on a countable state space.
Let (H:E\to\mathbb N_0) be proper and let (K=\{H\le n_0\}). Suppose that,
for every (x\notin K), there is a strong-Markov-compatible stopping time
τₓ such that

\[
 H(X_{\tau_x})\le H(x)-1\quad\text{a.s.},
 \qquad \mathbb E_x\tau_x<\infty.
\]

For (n>n_0), set

\[
 c(n)=1+\max_{H(x)=n}\mathbb E_x\tau_x
\]

and replace (c) by its nondecreasing envelope. Properness makes each
maximum finite. Define

\[
 U(x)=\sum_{j=0}^{H(x)}c(j).
\]

Then

\[
 \mathbb E_x[U(X_{\tau_x})-U(x)]\le-c(H(x)),
 \qquad \mathbb E_x\tau_x\le c(H(x)).
\]

Iterating the endpoint trace and summing only to bounded trace indices gives

\[
 \mathbb E_x T_K\le U(x)<\infty.
\]

A finite-set trace argument then gives finite mean positive return to one
state of (K), hence positive recurrence. No expected ordinary-jump count is
used.

The load-bearing hypothesis is the almost-sure proper-workload descent with
finite mean duration. Pointwise service inequalities at the starting shell
do not establish it.

## 3. General drift-cost version

A more flexible sufficient condition uses one global proper potential
(V\ge0). If a finite family of adapted physical-time episode rules has a
measurable statewise selector satisfying, outside a finite set,

\[
 \mathbb E_x\!\left[
   V(X_\tau)-V(x)+\tau
 \right]\le-1,
\]

with the endpoint term integrable, bounded-index telescoping gives both a
finite expected episode count and finite expected physical time to the finite
set. This is the natural target for the global residual-factorial potential.

For T3-2, neither the inherited finite atlas nor the scalar debt inequality
currently constructs such an episode selector.

