# Hostile audit B: exact-pair cloud averaging

**Strict verdict on the 2026-08-11 22:48 PDT draft:** **FAIL as a proved
theorem, but no counterexample to the proposed averaged trace was found.**

The exact carrier product, effective un-killed hazard, cofactor-envelope
coboundary, seventeen-support equality-set classification, and the
large-\(U\) maximal-source mechanism pass.  The present text does not yet
prove four uniform statements on which the stopped theorem relies.  The
repairs below are analytic and require no orientation or path enumeration.

## 1. Exact product: PASS

For a lower source \(y=cU+bI\), the un-killed hazard per unit base local
time is exactly

\[
 A_y(u,v)
 ={\kappa_y\rho^b(u)_{\underline{ab+c}}
      \over(v+1)^{\overline b}}
 Z_a(u-ab-c,v+b),                                                \tag{1.1}
\]

where

\[
 Z_a(s,N)=\sum_{j\ge0}{\rho^j(s)_{\underline{aj}}
                 \over j!(N+1)^{\overline j}}.                   \tag{1.2}
\]

This is precisely (1.9).  Since

\[
       1\le Z_a(s,N)\le\exp\{C(1+s)^a/N\},                       \tag{1.3}
\]

the uniform asymptotic (1.11) is correct below the stated cutoff.  The
formula is an occupation ratio relative to level-zero local time, not a
normalized stationary probability; the note uses the correct object.

## 2. Relative first-kill error: FAIL of proof

The implication

\[
        \sup_i\mathbb E_iJ\le\varepsilon_n
 \quad\Longrightarrow\quad
        \widehat A_e=A_e(1+O(\varepsilon_n))                     \tag{2.1}
\]

does not follow merely by “reversing the past part.”  For a rare edge, an
absolute Feynman--Kac error is insufficient.  What is needed
source-by-source is

\[
 \mathbb E\!left[J_eJ\right]
       \le C\delta_n(u)\,\mathbb E J_e,
 \qquad
 \delta_n(u)={C(1+u)^3\over n},                                  \tag{2.2}
\]

where \(J_e=\int\lambda_e(I_s)ds\).  The current time-reversal sentence
does not establish (2.2), and the later pointwise version (2.5) is only an
assertion.

### Required repair

Write the two time orderings in \(\mathbb E[J_eJ]\) using the killed-at-zero
proper Green kernel.  Detailed balance (1.5) reverses the ordering.  In
each ordering sum the additional lower insertion with (1.1).  Relative to
the distinguished edge insertion, an additional binary lower hazard costs
at most

\[
 C\left\{{(1+u)^2\over n}
          +{(1+u)^{a+1}\over n}
          +{(1+u)^{2a}\over n^2}\right\}
 \le {C(1+u)^3\over n}.                                         \tag{2.3}
\]

The three terms are respectively an \(I\)-free hazard during an open
level, a one-\(I\) source, and a two-\(I\) source.  The factorial product
in (1.2) sums all carrier levels, so (2.3) is uniform in the distinguished
source, including \(b=2\).  Then

\[
 0\le A_e-\widehat A_e
 \le\mathbb E[J_e(1-e^{-J})]
 \le\mathbb E[J_eJ]
 \le C\delta_n(u)A_e,                                           \tag{2.4}
\]

which proves the claimed relative estimate.  The same two-insertion
calculation after the first lower reaction proves the cleanup-dirty bound,
with \(u\) replaced by \(u+C\).  A cutoff-only estimate
\(CL_n^3/n\) cannot by itself yield the later
\(n^{-1+o(1)}\) claim; the pointwise bound (2.3) is essential.

## 3. Equality structure and Green kernel

### Structural part: PASS

All displayed \({\cal M}_{a,r}\) sets are correct and proper.  The strong
path argument is valid as a compact nontrapping argument, provided it is
understood as a chosen positive-probability subpath.  The preceding target
is not automatically the next lower source; the draft correctly does not
make that assumption globally.

Outside a compact set, \(m_a=0\).  If \(dU\) is the maximal \(I\)-free
lower complex, every \(dU\)-sourced equality edge descends, and every other
positive equality edge has source degree at most \(d-1\).  Therefore

\[
 {Q_nF_\theta(u)\over F_\theta(u)}
 \le Cu^{-\theta}+Cu^{-1+2\theta},\qquad \theta<1/2,             \tag{3.1}
\]

uniformly below the cutoff after the relative hazard repair in Section 2.

### Proposition 6.1: FAIL of current proof statement

The kernel \(Q_n\) is not defined precisely enough to make (6.2) a theorem.
It must be the substochastic kernel obtained by:

1. contracting completed proper excursions in base local time;
2. selecting the first lower edge with probability
   \(\widehat A_e/\sum_f\widehat A_f\);
3. retaining only leading sources and clean cleanup; and
4. killing strict drops, subleading edges, dirty cleanup, and included
   physical boundary.

For uniformity on the compact set, one must also record the following
minorization.  At each compact base, the rescaled leading edge weights
converge by (1.1) to strictly positive finite weights.  The proper
\({\cal M}_{a,r}\) path has length at most \(|L_0|\), and clean probability
tends to one.  Since there are finitely many compact bases and path edges,
there are \(M<\infty\) and \(\eta>0\), independent of large \(n\), such
that

\[
   \mathbb P_u\{S_n\hbox{ is hit in at most }M\hbox{ leading macros}\}
       \ge\eta.                                                   \tag{3.2}
\]

Equations (3.1)--(3.2), plus a finite-state corrector, do prove the desired
same-weight Green bound.  Without the kernel definition and (3.2), the
current proposition is incomplete rather than false.

## 4. Physical duration: FAIL of proof

The claim that an order-\(b\) macro has a geometric trial count of order
\(n^b\) is correct on the finite singular set, but it is not by itself an
additive-functional proof of (7.4).

### Required repair

Use level-zero local time.  Marked proper openings form a thinned Poisson
process in that clock, so the local time to the first lower event is
exponential with rate \(\sum_e\widehat A_e\).  From (1.1), at every
nonstatic base this gives

\[
        \mathbb E_u T_{m macro}^p
          \le C_p n^{2p}(1+u)^{c_p}.                              \tag{4.1}
\]

The real-time overhead is a compound sum of proper excursion times.  Each
open excursion has fixed moments \(O(n^{-p})\), and its intensity per unit
base local time is at most \(C(1+u)^a\); hence it changes only the
polynomial factor in (4.1).  For a sum over the equality trace, use

\[
 \left(\sum_{j<N}T_j\right)^p
    \le N^{p-1}\sum_{j<N}T_j^p                                  \tag{4.2}
\]

and the macro-count/polynomial Green bounds following from (3.1)--(3.2).
Iterating at most three strict-drop episodes proves
\(\mathbb ET^p\le C_pn^{2p}(1+u_0)^{c_p}\).

## 5. Bases with no feasible lower source

At such a base \(m_a(u)\) is undefined, so Sections 3--7 cannot quantify
over it silently.  In the actual supports the only cases are disabled
zero faces with no proper opening.  Every reaction source then contains
\(U\) or \(I\), the state is static, and that face is isolated.  A marked
state reachable from a class reference on this face has \(D_V=0\), so it is
outside the historically reachable positive-debt local theorem.  The
unified trace theorem must explicitly assume either a feasible lower source
or the historical positive-debt scope and discharge this static
alternative first.

## 6. Final verdict

The averaged-trace strategy survives hostile audit, and no exact network or
rate counterexample was found.  The current draft is nevertheless a strict
**FAIL** until (2.2)--(2.4), the precise \(Q_n\) definition and compact
minorization (3.2), the duration recursion (4.1)--(4.2), and the static-face
scope are inserted.  These are proof repairs, not finite search tasks.
