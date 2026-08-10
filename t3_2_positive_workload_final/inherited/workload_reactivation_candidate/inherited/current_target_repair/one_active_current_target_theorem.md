# Exact one-active current-target theorem

Assume that only species \(A\) is active in a terminal chart and that the
other two populations lie in a fixed finite box.  The finite phase records
the exact bounded populations, the actual current target, linkage, capped
availability, source-rate cell and lattice data.  The unbounded level is the
physical population \(n=A\); no service-obligation count is introduced.

## 1. Exact polynomial generator

For a channel with source \(y=(d,b,c)\), the transition rate at phase
\((B,C)=(\beta,\gamma)\) is

\[
 \kappa_e(\beta)_b(\gamma)_c(n)_d.
\]

Thus every transition has the exact form

\[
 (n,\phi)\longrightarrow(n+k,\phi'),
 \qquad
 n(n-1)q_2+nq_1+q_0,                           \tag{1.1}
\]

with \(k\in\{-2,-1,0,1,2\}\) and nonnegative phase-dependent rational
coefficients.  `src/one_active_generator.py` reconstructs (1.1).

## 2. The quadratic branch

If \(2A\) is a source, every genuine outgoing reaction has target containing
at most one \(A\).  Consequently

\[
 \mathcal L A\le-c_2A(A-1)+c_1A+c_0,
 \qquad c_2>0,                                 \tag{2.1}
\]

before a box or chart exit.  The constants are the finite sums of channel
rates times bounded-coordinate factorials.  This is strictly negative
outside an explicit finite level.

## 3. The linear phase

Suppose \(2A\) is absent.  Every one-\(A\) source transition has level reward
\(0\) or \(-1\).  Let \(Q_1\) be the exact finite phase generator obtained
from their coefficients.

If a recurrent class of \(Q_1\) contains a death edge, its stationary vector
is strictly positive and its stationary mean level reward is strictly
negative.  The exact Poisson equation gives a bounded phase corrector
\(h(\phi)\) for which

\[
 \mathcal L(A+h(\phi))=-\gamma A+O(1),
 \qquad \gamma>0.                              \tag{3.1}
\]

Transient linear phases are eliminated by their exact finite Green matrix;
nonpositive rewards remain nonpositive.

## 4. Creator-service paths

A degree-zero birth has reward at most \(+1\) and produces an actual target
with one \(A\).  In its own strongly connected linkage, a path back to the
zero-\(A\) source has a first one-\(A\)-to-zero-\(A\) edge.  The prefix is
made entirely of one-\(A\) sources and ends with one death.  This path is
constructed exactly by `src/one_active_current_target.py`.

While a current target \(A+D\) is present, its source rate is at least
\(\kappa_*A\).  A competing linear source can remove the last bounded
cofactor \(D\) only if it also contains \(D\).  With one active particle and
molecularity at most two, that source is another \(A+D\) complex; exact
complex ownership keeps it in one linkage and its actual target transfers
the current-target service phase.  A source with no \(A\) has bounded total
rate in the box.

The finite carrier-clock argument therefore yields constants \(K,C\) such
that

\[
 \mathbb P\{\hbox{bounded-source interruption before creator service}\}
 \le K/A,                                      \tag{4.1}
\]

and the mean physical service-attempt duration is at most \(C/A\), unless a
box/support exit occurs.

Repeated bounded-source births are not stored as a phase.  Put
\(Q=(A-A_0)_+\).  Service lowers \(Q\) by one and an interruption raises it
by at most one.  For large \(A\), (4.1) gives

\[
 \mathbb E\Delta Q\le-1/2.                    \tag{4.2}
\]

Hence the complete creator-service trace returns in finite mean to
\(A\le A_0\), or exits the chart.

## 5. Exact zero alternative

Let \(K\) be the set of bounded species occurring in binary one-\(A\)
complexes \(A+D\).

If no unary complex \(A\) occurs and no zero-\(A\) complex contains a species
of \(K\), then every one-\(A\) complex contains exactly one \(K\)-particle
and every zero-\(A\) complex contains none.  Thus, for every physical
reaction in both linkages,

\[
 A-\sum_{D\in K}D                               \tag{5.1}
\]

is an exact affine stoichiometric invariant.  With the bounded coordinates
confined to the chart box, (5.1) bounds \(A\).

Otherwise there is a unary carrier or an unpaired service species in a
zero-\(A\) complex.  Strong connectivity and the carrier-clock estimate give
a service transition that is not charged to a preceding birth.  The
creator-service macrochain then has pathwise nonpositive rewards and at least
one strict negative transition in every recurrent class.

A zero stationary macroreward therefore forces every positive-probability
macroedge to have reward zero.  The corrected variance is exactly zero, and
the finite coboundary is (5.1) or a bounded phase version of it.  An abstract
zero-mean walk with nonzero variance is not silently declared invariant; it
fails the pathwise nonpositive-edge test.

## 6. Conclusion

Every one-active terminal chart has one of:

1. quadratic descent;
2. Poisson-corrected linear descent;
3. finite-mean creator-service descent;
4. positive bounded-box/support promotion flux;
5. an affine invariant bounding \(A\).

Thus no one-active terminal chart supports an escaping embedded reaction-count
occupation.
