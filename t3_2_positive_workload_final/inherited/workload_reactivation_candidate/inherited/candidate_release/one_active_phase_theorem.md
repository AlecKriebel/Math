# One-active-coordinate finite-phase theorem

Assume that only species `A` is active in a terminal chart.  The populations
of `B` and `C`, target marks, capped availability, and lattice data lie in a
finite phase set.  Kill on bounded-coordinate promotion, source/support-rank
exit, lower-shell descent, or entry into the finite set.

Every channel has rate

\[
 k_e(\phi)(A)_{d_e},\qquad d_e\in\{0,1,2\},
\]

where the coefficient is positive exactly when the bounded source part is
enabled.

## 1. Quadratic source

The only degree-two source is `2A`.  Every genuine target has at most one
`A`, so every channel from `2A` lowers `A`.  If `2A` is present, then outside
a finite set

\[
 \mathcal L A\le -\kappa_{2A}A(A-1)+C_1A+C_0<0.
\]

Thus this branch has direct strict descent.

## 2. Linear fast phase

Suppose `2A` is absent.  A degree-one source cannot increase `A`, because
the only target with two `A` particles would be `2A`.  Freeze the large
factor `A` and form the finite generator `Q_1` from all enabled degree-one
channels.  Edge rewards are in `{0,-1}`.

In a recurrent class of `Q_1`:

* if a negative edge is present, its stationary mean reward is strictly
  negative for every positive rate vector; the finite Poisson equation gives
  a bounded phase corrector and generator drift `-cA+O(1)`;
* if no negative edge is present, every recurrent edge preserves `A`.

Transient degree-one motion is eliminated exactly by the finite Green
matrix.  Since all transient rewards are nonpositive, elimination cannot
create a positive effective reward.

## 3. Constant-rate births and source ownership

A degree-zero channel can increase `A` by only one.  Its target contains one
`A`.  In the creator linkage, take a directed return path from that target to
a zero-`A` complex.  The first crossing from one `A` to zero `A` is a
negative degree-one channel; every preceding source on the path contains one
`A`.

At a source `A+D`, another linkage cannot consume the bounded cofactor `D`
at the same linear-in-`A` order without using the same source complex, which
belongs to the creator linkage.  A competing source that consumes the active
`A` is already a negative service event.  A competing source that preserves
`A` and omits `D` leaves `A+D` enabled.  Sources using only bounded particles
have bounded rate and are lower-order interruptions.

Consequently, after a degree-zero birth, the finite degree-one carrier phase
reaches negative service in physical time `O(1/A)` unless a bounded-source
interruption occurs.  The interruption probability along one finite carrier
path is `O(1/A)`.  Every interrupted cofactor and outstanding failed service
is part of the bounded physical phase; an unbounded accumulation is bounded-
coordinate promotion and therefore a chart exit.  Exact finite Green
elimination includes all interruptions and gives complete birth--relaxation
reward at most zero.

If a recurrent effective degree-zero class has zero mean reward, all its
positive-probability complete rewards are zero.  Finite graph cohomology
then gives a bounded phase function `psi` such that

\[
 A+\psi(\phi)
\]

is invariant on that class.  Since `psi` is bounded, this class cannot carry
an escaping occupation in the `A` direction.  Otherwise the first nonzero
class has strict negative drift.

Every argument occurs in a finite killed shell, so all activation and
absorption times have finite physical mean.  There is no critical
zero-mean/nonzero-variance branch: zero mean is edgewise zero after the
nonpositive complete-reward elimination.
