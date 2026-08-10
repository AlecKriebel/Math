# One-active finite-priority theorem

Assume `A` is the only active coordinate.  The exact values of `B,C`, capped
availability, the current actual target, linkage label, lattice data and the
finite source-rate cell form a finite phase `phi`.  Kill on exit from the
inactive box, promotion of `B` or `C`, lower-shell descent, or another declared
structural exit.

Every nonexit channel has

\[
 (n,\phi)\longrightarrow(n+k,\phi'),\qquad |k|\le2,
\]

and exact rate

\[
 c_2(\phi,e)n(n-1)+c_1(\phi,e)n+c_0(\phi,e),
 \qquad c_j\ge0.                               \tag{1.1}
\]

The coefficients are explicit positive combinations of the fixed reaction
rates and inactive falling factorials.

## 1. Degree two

If `2A` is a source complex, every genuine reaction from it has target
molecularity at most two and target `A`-count at most one.  Hence its level
increment is negative.  On every phase where it is enabled,

\[
 \mathcal L A\le-c_2A(A-1)+c_1A+c_0,
 \qquad c_2>0.                                  \tag{1.2}
\]

A phase in which the source is disabled is an inactive-coordinate/support
exit.  Thus the degree-two branch has strict descent outside a finite level
set.

## 2. Degree one

Suppose `2A` is absent.  Every degree-one source is one of

\[
 A,\quad A+B,\quad A+C,
\]

and no bimolecular target can contain two `A` particles.  Every degree-one
level increment is therefore `0` or `-1`.

Divide the phase generator by `A` and take the compact tied-rate limit.  In a
recurrent degree-one class:

* a negative edge has strictly positive stationary flux and gives a uniform
  negative mean;
* otherwise every recurrent degree-one edge preserves `A`.

The exact finite Poisson equation makes the first case statewise strict.
Transient degree-one states are eliminated by a nonnegative Green matrix.

## 3. Degree-zero births

A degree-zero source can create at most one `A`.  After an actual birth its
target contains one `A` and is physically enabled.  In the creator linkage,
choose a return path to a zero-`A` complex and truncate it at the first
negative one-`A` source.  All prefix sources have degree one and are faster
than every degree-zero event.

Apply the finite-priority actual-target trace theorem with workload `h=A`.
The finite carrier phase is exactly

\[
 (B,C,\text{actual target},\text{path/zero-class phase},\text{lattice data}).
\]

It contains no obligation count.  A different linkage can destroy the last
bounded cofactor only through a source containing that cofactor; its actual
target is another finite carrier phase.  A bounded-only interruption belongs
to the degree-zero trace and is retained at its natural probability.

Consequently every effective degree-zero birth has one of:

1. complete birth--service reward at most zero;
2. inactive-coordinate promotion or another structural exit;
3. entry into a closed zero carrier class.

## 4. Zero carrier classes

If a closed zero carrier class occurs, every positive-probability effective
edge has corrected `A`-reward zero.  Finite graph cohomology gives a rational
phase function `psi` such that

\[
 A+\psi(\phi)                                   \tag{4.1}
\]

is invariant on that class.  Alternatively, when one service token is
carried by an inactive species set `K`, the edge-by-edge invariant is

\[
 A-\sum_{D\in K}D.                              \tag{4.2}
\]

Since the inactive box and phase are finite, both (4.1) and (4.2) have finite
level sets in the terminal chart.  They cannot support an escaping
occupation.

The zero conclusion is edgewise zero after complete degree-one relaxation.
Its corrected increment has zero variance.  Thus no Lamperti-critical
zero-mean/nonzero-variance branch is omitted.

## 5. Conclusion

A one-active terminal chart has exactly one of:

* strict negative corrected level flux;
* positive structural-exit flux;
* an affine invariant with positive `A` coefficient.

Each contradicts terminal Green escape.  This proves the one-active branch
without an unbounded service-obligation phase and without conditioning on a
future degree-zero birth.
