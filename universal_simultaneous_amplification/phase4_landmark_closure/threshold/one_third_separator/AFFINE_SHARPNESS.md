# Sharpness of the Bd coefficient `1/3`

Date: 2026-08-08 (America/Los_Angeles)

No literature search or external communication was used.

## Status

This note proves the exact rare-state algebra for a sharpness theorem and
combines it with the independently hostile-audited mesoscopic-core
establishment lemma in the sibling clique--pendant manuscript
`threshold/clique_pendant_asymptotic/CLIQUE_PENDANT_ASYMPTOTICS.md`, Lemma 1.
That lemma, including its arbitrary fixed positive core-to-leaf ratio, is
proved in commit `1af17787`.  The coefficient-optimality theorem below is
therefore **PROVED**.  This note does **not** prove that the sharp candidate
is universal.

At fitness `r=3/2`, write

\[
 x(G)={\rho_{Bd}(G)\over\rho_{Bd}(K_n)},\qquad
 y(G)={\rho_{dB}(G)\over\rho_{dB}(K_n)}.
\]

If an inequality

\[
             \theta x(G)+(1-\theta)y(G)\leq1             \tag{1}
\]

holds for every finite connected undirected weighted graph, then necessarily

\[
                         \boxed{\theta\leq {1\over3}}.    \tag{2}
\]

The coefficient `1/3` is approached from above by explicit unweighted
clique--pendant families.  On every fixed ray, the candidate at
`theta=1/3` still has a strict limiting slack.  Thus (2) is an optimality
theorem for the coefficient, not the desired universal separator.

## 1. The explicit family

Fix a positive rational `alpha in (0,1)`.  Choose integers `c_m,m` with

\[
 {m\over c_m+m}\longrightarrow\alpha,
 \qquad c_m,m\longrightarrow\infty.                    \tag{3}
\]

Let `G_m` consist of the unit-weight clique on a hub `H` and `c_m`
ordinary vertices, together with `m` degree-one leaves adjacent to `H`.
The graph is connected, unweighted, and independent of fitness.

The exact quotient state is `(h,i,j)`, where `h` is the hub type and `i,j`
are the mutant counts among ordinary vertices and leaves.  Strong lumping
and the six transition formulas are proved directly in the sibling
clique--pendant audit.  The establishment lemma there is proved for arbitrary
fixed positive rational `a`, with `c_m=am` along an integer subsequence.
This suffices here because `alpha` is rational.  For completeness, the new
rare-state calculation is given next.

## 2. General leaf branching calculation

Put

\[
             a={1-\alpha\over\alpha},\qquad
             p=1-{1\over r}.
\]

Use the exact Bd statewise time change which removes the total-fitness
denominator, start from one mutant leaf, and observe time on the scale
`tau=t/m`.  While the leaf count is fixed and the ordinary-mutant family is
small, hub activations occur at rate `r` per mutant leaf.  An activated hub
returns to resident at rate `m+O(1)`.  During one such excursion, the total
rates of producing a new mutant leaf and an ordinary mutant are respectively

\[
              {r\over a+1}+o(1),\qquad
              {ra\over a+1}+o(1).                       \tag{4}
\]

When the hub is resident, one mutant leaf dies at rate
`1/((a+1)m)+o(m^-1)`.  Therefore each mutant leaf in the limiting killed
branching process has rates

\[
 \lambda={r^2\over a+1}=r^2\alpha,
 \quad
 \mu={1\over a+1}=\alpha,
 \quad
 \kappa={a r^2p\over a+1}=(1-\alpha)r(r-1),             \tag{5}
\]

for leaf birth, leaf death, and a successful ordinary-core mark.  The mark
rate includes the exact ordinary-family establishment probability `p`.

By the mesoscopic-core lemma, convergence follows by the same
stopped-path argument as on the ray
`a=8`: a hub excursion has probability `O(1/m)` of one productive event and
`O(1/m^2)` of two; failed ordinary families have an exponentially decaying
duration tail after conditioning on extinction.  Stop first at a fixed leaf
level or at a mesoscopic ordinary seed, let `m` tend to infinity, and then
let the leaf cutoff tend to infinity.  The mesoscopic-seed lemma under audit
turns a mark into fixation with probability `1-o(1)`.

If `q` is extinction before marking from one leaf, branching independence
and the first-event equation give

\[
       \lambda q^2-(\lambda+\mu+\kappa)q+\mu=0,          \tag{6}
\]

with the unique root `q in (0,1)`.  At `r=3/2`,

\[
 q(\alpha)=
 {3+10\alpha-\sqrt{9+60\alpha-44\alpha^2}
  \over18\alpha},
 \qquad
 \ell(\alpha):=1-q(\alpha)
 ={8\alpha-3+\sqrt{9+60\alpha-44\alpha^2}
  \over18\alpha}.                                     \tag{7}
\]

Here `ell(alpha)` is the limiting Bd fixation probability from one mutant
leaf.  Since the polynomial in (6) is positive at zero and negative at one,
`0<q<1`, hence `0<ell<1`.  Rationalizing (7) or expanding (6) at zero gives

\[
              q(\alpha)={4\over3}\alpha+O(\alpha^2),
              \qquad \ell(\alpha)\longrightarrow1.       \tag{8}
\]

For dB, a mutant leaf dies at rate one, whereas it activates the hub at rate
`O(1/m)`; even granting certain fixation after activation, its fixation
probability tends to zero.

## 3. Exact limiting ratios

By the same establishment lemma, an ordinary singleton fixes
with probability `p+o(1)` under both rules, and the hub has vanishing
initialization mass.  Uniform singleton initialization therefore gives

\[
 \rho_{Bd}(G_m,3/2)\longrightarrow
 {1-\alpha\over3}+\alpha\ell(\alpha),
 \qquad
 \rho_{dB}(G_m,3/2)\longrightarrow {1-\alpha\over3}.     \tag{9}
\]

Both complete baselines tend to `1/3`, so

\[
 \boxed{
 x_\infty(\alpha)=1-\alpha+3\alpha\ell(\alpha),
 \qquad
 y_\infty(\alpha)=1-\alpha.}                            \tag{10}
\]

The unique affine crossing on this ray is

\[
 \theta_0(\alpha)
 ={1-y_\infty\over x_\infty-y_\infty}
 ={1\over3\ell(\alpha)}>{1\over3},
 \qquad
 \theta_0(\alpha)\downarrow {1\over3}
 \quad(\alpha\downarrow0).                              \tag{11}
\]

Thus every `theta>1/3` is refuted by first choosing a sufficiently small
positive rational `alpha` and then taking `m` large.  This proves (2).

At the sharp candidate itself,

\[
 1-\left\{{x_\infty\over3}+{2y_\infty\over3}\right\}
 =\alpha\{1-\ell(\alpha)\}>0.                           \tag{12}
\]

Finally, (8) explains the coefficient directly:

\[
 x_\infty-1=2\alpha+O(\alpha^2),\qquad
 1-y_\infty=\alpha.
\]

The asymptotically largest Bd gain is twice the dB loss in this sharp
boundary regime.  Hence the normalized linear combination must weight Bd
and dB in the ratio `1:2`.  This is the structural origin of the proposed
one-third separator.
