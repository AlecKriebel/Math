# Macroscopic fast-Schur descent for the 145 mixed hard templates

**Proof-first scoped theorem, 2026-08-12 PDT. Audit status: pending.**
This note treats the non-exact mixed part of the physical two-active hard
phase. Both active coordinates are macroscopic. It is not an extension by
enumeration of the generalized one-active proof: the finite support table
is used only for the four premises in Section 1, and every stochastic
estimate below is analytic.

Fix an arbitrary strong orientation of each linkage and arbitrary positive
rate constants. Constants may depend on those fixed data. Put

\[
 U=s^{p+o(1)},\qquad V=s^{q+o(1)},\qquad I=0,
 \qquad (p,q)\in\{(1,2),(1,3),(4,5)\}.                       \tag{1.1}
\]

Write \({\cal B}=\{0,U,2U\}\),
\({\cal C}=\{I,2I,U+I\}\), and \(C=V+I\).

## 1. Finite structural premises

The 145 normalized ratio/support rows in this scope satisfy:

1. one linkage contains (C), no other complex contains (V), and all
   complexes lie in \({\cal B}\cup{\cal C}\cup\{C\}\);
2. after deleting (C), at least one linkage contains both a base and a
   cofactor complex;
3. the (C)-linkage is not an exact pair \(\{aU,C\}\);
4. if
   \[
       d=\max\{c:cU\hbox{ occurs in either support}\},          \tag{1.2}
   \]
   then (d\in\{1,2\}) and
   \[
                         q-pd\ge1.                              \tag{1.3}
   \]

There are 119 rows of ratio (1:3), thirteen of ratio (1:2), and
thirteen of ratio (4:5). The support count and (1.3) are bookkeeping;
they do not assert a probabilistic conclusion.

Fix the common corrected factorial potential

\[
 G_\ell(x)=K_\ell+\sum_i\log(x_i!)+\ell\cdot x\ge1,
 \qquad W_\ell=G_\ell^4.                                      \tag{1.4}
\]

## 2. Exact clean Schur macro

At a no-fast state, precisely the base sources are enabled. An initiating
edge (e:y=c_yU\to z\) has rate

\[
                         \kappa_e(U)_{\underline{c_y}}.         \tag{2.1}
\]

Suppress every non-(C)-sourced firing after this initiation. If
(z\in{\cal B}), retain the direct base move. If
(z\in{\cal C}), the next (C)-sourced firing crosses (V<n), and its
actual endpoint is retained. If (z=C), the first (C)-sourced target
has the fixed law

\[
 p_t={\kappa_{C,t}\over\sum_{C\to r}\kappa_{C,r}}.             \tag{2.2}
\]

A base target gives a no-fast continuation. A cofactor target leaves
(I>0,V=n), so one further (C)-sourced firing crosses (V<n). Thus a
clean macro contains at most two fast firings before continuation or
service. Every clean endpoint differs from the start by a bounded vector.

An opening (dU\to C\to dU) can be an exact physical self return. Delete
it but retain its physical time. Since the (C)-linkage is not the exact
pair \(\{dU,C\}\), strong connectivity gives an edge leaving this
two-node set. Its source is (dU), in which case it competes with the
opening with the identical falling-factorial factor, or it is (C), in
which case (2.2) assigns it fixed positive conditional probability.
Therefore the number of exact self attempts before a nonself clean outcome
has a geometric tail with a parameter independent of (s).

## 3. Dominant source implies factorial descent

Call a macro **dominant** when its initiating source is (dU). After the
exact-return contraction, every dominant nonself clean macro has one of the
following forms.

* A base continuation lands at (cU) with (c<d). Hence
  \[
    \Delta G_\ell=-p(d-c)\log s+o(\log s).                    \tag{3.1}
  \]
* A service macro may collect at most two base target contributions, each
  of degree at most (d). Its net spectator increase is at most (d),
  while (V\) decreases by one. Thus
  \[
    \Delta G_\ell\le(pd-q)\log s+o(\log s)
                  \le-\log s+o(\log s).                       \tag{3.2}
  \]

The cofactor factorial and the fixed linear correction cost only (O(1))
at a clean endpoint. Since a distinct base complex cannot have the same
degree (d), (3.1)--(3.2) exhaust every nonself dominant outcome. Hence,
for some (c>0),

\[
                 \Delta G_\ell\le-c\log s                     \tag{3.3}
\]

on every dominant nonself clean macro for all large (s). This is a
pathwise statement here; unlike the exceptional exact carrier shell, no
equality source remains after the self return is deleted.

## 4. Subdominant and dirty events

At a no-fast base, the total rate of sources of degree at most (d-1) is
(O(s^{p(d-1)+o(1)})), whereas the contracted nonself degree-(d) rate is
at least (cs^{pd+o(1)}). Therefore

\[
 \mathbb P\{\hbox{subdominant initiator before the dominant macro}\}
       =O(s^{-p+o(1)})=O(s^{-1+o(1)}).                         \tag{4.1}
\]

During a clean fast window, (1\le I\le2), (V\ge s^{q+o(1)}), and every
nonfast source has propensity at most (Cs^{pd+o(1)}(1+I)^2). The fast
clock is at least (cs^{q+o(1)}I). By (1.3), the probability of a first
nonfast insertion before the next fast firing is (O(s^{-1+o(1)})).
There are at most two windows and a geometrically bounded number of exact
self attempts. Including the defect-causing reaction, for every fixed
(r),

\[
 \mathbb E[(1+|\Delta U|+I+|\Delta V|)^r;E]
       =O(s^{-1+o(1)}).                                        \tag{4.2}
\]

The same first-clock calculation with an exponential carrier-level mark
shows that (I\ge K_M\log s) has endpoint-weighted probability (O(s^{-M}))
for every prescribed (M), after increasing (K_M). No long spectator
excursion is possible before the first nonself macro: exact retries restore
the physical population, and every other initiation is terminal under the
stopping rule.

Stop at the first dominant nonself clean macro, at the first subdominant or
dirty event (E), or at the included carrier boundary. Equations
(3.3)--(4.2) give

\[
 \mathbb E\Delta G_\ell\le-c\log s,
 \qquad
 \mathbb E|\Delta G_\ell|^r=O(\log^r s).                      \tag{4.3}
\]

## 5. Physical time and the fourth power

The degree-(d) base clock has rate at least (cs^{pd+o(1)}); the exact
self-attempt count is geometrically bounded; and every fast holding time
has rate at least (cs^{q+o(1)}). Consequently, for each fixed (r),

\[
                            \mathbb E\sigma^r=O(1).             \tag{5.1}
\]

At the starting state (G_\ell=s^{q+o(1)}\log s). Applying the exact
fourth-power expansion to (4.3), while using (5.1), yields

\[
 \mathbb E[W_\ell(X_\sigma)-W_\ell(X_0)+\sigma]
       \le-cG_\ell(X_0)^3\log s.                              \tag{5.2}
\]

### Scoped theorem

For every one of the 145 physical mixed non-exact normalized
ratio/support rows, every strong orientation, every fixed positive rate
vector, and every fixed common correction \(\ell\), the physical stopping
rule above gives the common-fourth-power descent (5.2), arbitrary fixed
endpoint moments, and physical-time moments. It need not service old-active
debt on every regular path: a dominant base decrease already pays the same
common potential. Endpoint reclassification under this identical (W_\ell)
is the intended composition interface.

This theorem does not cover the nineteen exact carrier rows, the eight
separated rows, or the sixteen no-history rows, and it changes no pair or
global certification flag before independent audit and marked composition.
