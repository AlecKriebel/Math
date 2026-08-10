# Nested entries refute the uniform mixed old-debt kernel

## 1. Exact network and status

Take \(C\) as the active species and use

\[
 L_0=\{0,AC\},\qquad
 L_1=\{2A,2B,AB,BC\}.                                  \tag{1.1}
\]

Orient the linkages as

\[
 0\rightleftarrows AC,\qquad
 BC\longrightarrow AB\longrightarrow2B
 \longrightarrow2A\longrightarrow BC,                 \tag{1.2}
\]

with arbitrary positive rates
\(\alpha,\beta,\kappa_1,\kappa_2,\kappa_3,\kappa_4\) in
the displayed order. This support pair belongs to the exact 1,227-pair
candidate branch. In particular it has an affine-feasible failed descriptor
with weight \((0,0,1)\) and inactive caps \(A=B=0\).

> **Certified conclusion.** The uniform-\(p\), bounded-duration old-debt
> assertion in Lemma 4.1 and Theorem 6.1 of
> *one_active_killed_carrier_service.md* is false.

This is not a counterexample to recurrence. Section 4 records the candidate
higher-power repair, whose full trace theorem remains analytic and is not
certified by the regression.

## 2. A consistent debt state in the singular zero-reward base

Start from \((A,B,C)=(0,0,N)\) with zero reflected \(C\)-debt. The physical
reaction path

\[
\begin{split}
 &0\to AC,\quad0\to AC,\quad0\to AC,\quad
 2A\to BC,\\
 &AB\to2B,\quad2B\to2A,\quad
 AC\to0,\quad AC\to0
\end{split}                                             \tag{2.1}
\]

is enabled in the displayed order and has positive probability. It ends at

\[
 (A,B,C)=(0,0,N+2),\qquad D_C=2.                        \tag{2.2}
\]

At \(A=B=0\), the only enabled source is \(0\). After \(0\to AC\),
the fast exit \(AC\to0\) has rate \(\beta C\), while another entry has
rate \(\alpha\). If the fast exit wins, the contracted macrostep has active
reward zero and returns to the same base. No source of \(L_1\) is enabled
until at least two \(A\)-molecules overlap.

Consequently, from \((1,0,C)\),

\[
 {\mathbb P}\{0\to AC\hbox{ before }AC\to0\}
 ={ \alpha\over \alpha+\beta C}
 =O(C^{-1}).                                           \tag{2.3}
\]

Every old-debt service path from the base must first win this race. On a
fixed physical interval, primary entries have rate \(\alpha\), so the
probability of service is \(O(C^{-1})\), not bounded below. More generally,
if a proposed family of stopping times had both a uniform positive service
probability and uniformly bounded mean duration, truncate at a sufficiently
large fixed time. Markov's inequality and (2.3) give a contradiction.

The reverse-history path used in the earlier proof has negative total
reward, but it necessarily prescribes a slow nested entry while a fast exit
is enabled. Its probability vanishes with \(C\). Net reward and physical
source-rate probability cannot be conflated.

## 3. Leading activation scale

Use falling-factorial propensities. Condition on the primary entry
\(0\to AC\). From \(A=1\), a second entry beats the exit with probability

\[
 {\alpha\over\beta N}+O(N^{-2}).                       \tag{3.1}
\]

From \(A=2\), the channel \(2A\to BC\) has rate
\(2\kappa_4\), whereas the aggregate \(AC\to0\) rate is
\(2\beta N+O(1)\). Therefore

\[
 {\mathbb P}\{\hbox{reach }B=1\mid\hbox{primary entry}\}
 ={ \gamma\over N^2}+O(N^{-3}),\qquad
 \gamma={\alpha\kappa_4\over\beta^2}>0.                \tag{3.2}
\]

Thus the debt-producing/service-enabling mechanism is two rare
slow-before-fast contests deep.

## 4. Why the obstruction still looks stabilizing

Once \(B=1\), the fast reactions are

\[
 BC\to AB,\qquad AC\to0.
\]

For fixed \(B=b\) and large \(C\), \(A\) is an
immigration--death phase with limiting Poisson mean

\[
 r b,\qquad r={\kappa_1\over\beta}.                    \tag{4.1}
\]

The averaged \(B\)-chain has leading transitions

\[
\begin{array}{rcl}
 b&\longrightarrow&b+1
 \quad\hbox{at rate }
 \lambda b^2,\qquad
 \lambda=\kappa_2r+\kappa_4r^2,\\
 b&\longrightarrow&b-2
 \quad\hbox{at rate }\kappa_3 b(b-1).
\end{array}                                            \tag{4.2}
\]

While this phase remains on the \(C\)-scale,

\[
 {d\over dt}\log C(t)=-2\kappa_1B(t).                  \tag{4.3}
\]

For a fixed post-activation horizon \(T>0\), stopped additionally when
\(B\) reaches a fixed finite boundary or the total population loses a
fixed fraction, the averaged loss fraction is

\[
 Y_T=1-\exp\left\{-2\kappa_1\int_0^T B(s)\,ds\right\}.
                                                               \tag{4.4}
\]

Starting from \(B(0)=1\), \(Y_T>0\) with positive probability for every
positive rate vector. Proposition 1.1 of
*nested_entry_bounded_core_trace.md* proves the stopped averaging,
duration, and uniform integrability needed to combine (3.2) and (4.4):

\[
\begin{aligned}
 {\mathbb E}\Delta C
   &=-{\gamma\,{\mathbb E}Y_T\over N}+o(N^{-1}),\\
 {\mathbb E}(\Delta C)^2
   &=\gamma\,{\mathbb E}Y_T^2+o(1),\\
 {\mathbb E}\{C_{\rm end}^2-N^2\}
   &=\gamma\,{\mathbb E}(-2Y_T+Y_T^2)+o(1)<0.
\end{aligned}                                          \tag{4.5}
\]

The resulting Lamperti combination is

\[
 2N\,{\mathbb E}\Delta C+{\mathbb E}(\Delta C)^2
 =\gamma\,{\mathbb E}(-2Y_T+Y_T^2)+o(1)<0,             \tag{4.6}
\]

because \(0\le Y_T\le1\) and \({\mathbb P}(Y_T>0)>0\).
Hence no positive rational rate choice makes the leading quadratic
coefficient nonnegative.

Equations (4.5)--(4.6) are now an independently audited theorem at this
exact stopped-network scope. Accordingly the stopped-network trace flag is
true. This does not compose the episode with every promoted endpoint and
does not prove an invariant probability for the full chain; the global
recurrence flag remains false.

## 5. Regression command

    PYTHONPATH=src python3 -B -m unittest \
      tests/test_one_active_nested_entry_obstruction.py -v
