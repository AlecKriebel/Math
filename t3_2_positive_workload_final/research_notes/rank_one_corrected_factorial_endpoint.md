# Corrected-factorial endpoints for the exact-flat rank-one carrier

## 1. Scope and conclusion

This note supplies the endpoint estimate which is deliberately absent from
*rank_one_multichannel_carrier.md*. A negative increment of the descriptor
workload \(H_w\) is not, by itself, a negative increment of factorial
entropy when adjacent D-tiers have a subpower gap. The repair is to keep
the actual maximal-to-lower reaction and to use one rate-corrected
factorial potential for the whole top linkage.

The conclusion is local to an exact-flat two-active sequence. It covers
the 895 seeded/top-activation carrier incidences and the 25 cap-zero
activation incidences. It does not compose different active dimensions
and does not assert recurrence of a support pair.

> **Theorem 1.1 (corrected-factorial carrier).** Fix arbitrary
> strongly connected orientations and positive rates on a rank-one whole
> top linkage \(L_*\), and let \(x_n\) realize one of the 920 nonfinite
> exact-flat incidences treated in Theorems 6.1--6.2 of
> *rank_one_multichannel_carrier.md*. There is a factorial-linear
> potential \({\cal F}_*\), depending only on \(L_*\) and its rates, and a
> physical stopping time \(\tau_n\) from the existing finite carrier such
> that
>
> \[
>  {\mathbb E}_{x_n}\bigl[{\cal F}_*(X_{\tau_n})
>                    -{\cal F}_*(x_n)\bigr]\longrightarrow-\infty.
> \tag{1.1}
> \]
>
> Its physical duration and scaled population endpoints have the moments
> stated in Theorems 6.1--6.2. For the 895 direct incidences the negative
> term is the actual D-tier gap. For the 25 cap-zero incidences it is a
> fixed negative multiple of \(\log N_n\).

The proof below reduces (1.1) to two estimates. First, every fast top
window or independent zero-source wait has uniformly bounded expected
**net** \({\cal F}_*\)-cost. Second, the prescribed maximal-to-lower edge
has its exact negative logarithmic reward, while every submaximal positive
edge contributes \(o(1)\) after propensity weighting.

An independent six-point proof replay has now checked this theorem at its
stated local scope. Section 8 records the audit boundary. No pair-level or
global recurrence flag follows from this result alone.

## 2. The common factorial-linear potential

For \(\ell\in{\mathbb R}^3\), put

\[
 {\cal F}_\ell(x)=\sum_{i=1}^3\log(x_i!)+\ell\mathbin{\cdot}x.
\tag{2.1}
\]

If \(e:y\to z\) is enabled at \(x\), with \(\nu=z-y\), then the following
identity is exact:

\[
 \Delta_e{\cal F}_\ell(x)
 =\log{(x+\nu)_{\underline z}\over x_{\underline y}}
   +\ell\mathbin{\cdot}\nu .
\tag{2.2}
\]

Indeed, both sides exponentiate to
\((x-y+z)!/x!\) times the linear-correction factor. This identity is the
reason to retain the actual physical target rather than a nominal complex.

There are three top templates, up to relabelling.

1. If \(L_*=\{y,z\}\) is reversible, choose \(\ell\) so that

   \[
    \ell\mathbin{\cdot}(z-y)=\log{\kappa_{zy}\over\kappa_{yz}}.
   \tag{2.3}
   \]

   Equivalently, choose \(\theta>0\) with
   \(\kappa_{yz}\theta^y=\kappa_{zy}\theta^z\) and take
   \(\ell=-\log\theta\).

2. If \(L_*=\{2A,A+B,2B\}\), choose
   \(\ell=(d,0,0)\), where

   \[
    d=-\log{r_*\over1-r_*}
   \tag{2.4}
   \]

   and \(r_*\) is the unique zero of the directed fluid polynomial from
   Lemma 4.1 of *certified_exact_shielded_seam.md*. Coordinate
   permutations give the other two versions.

3. The exceptional reversible template \(\{2A,R+I\}\), where \(I\) is
   the inactive cofactor and \(R\) is the other active species, again uses
   (2.3).

Inactive coordinates not displayed in a template are constant under
\(L_*\), so their terms in (2.1) cancel at every top endpoint.

For the 298 support pairs which have both an all-active failed phase and a
two-active rank-one phase, the finite compatibility certificate proves
that the whole-top mask is identical in the two phases. Thus (2.3) or
(2.4) selects literally the same correction in both dimensions. This is
a compatibility fact, not yet a Foster composition theorem.

## 3. Uniform top endpoint cost

Write \(a_n\) for the maximal lower source scale in (2.2) of
*rank_one_multichannel_carrier.md*. In every rank-one incidence
\(a_n\to\infty\), and the fast carrier windows have length at most
\(T/a_n\).

### Lemma 3.1 (fast-window endpoint bound)

Start at any state in one of the descriptor-compact sets used by the
finite carrier, allowing a fixed number of preceding bounded lower jumps.
Let \(\sigma_n\le T/a_n\) be either the end of a top-only window or the
first lower-reaction clock attached to that top path. Immediately before
the lower jump, if one occurs,

\[
 {\mathbb E}\bigl[{\cal F}_*(X_{\sigma_n-})
                  -{\cal F}_*(X_0)\bigr]\le C_T .
\tag{3.1}
\]

The constant is uniform along the exact-tier subsequence and over the
finite collection of carrier vertices.

#### Homogeneous quadratic shells

Suppose \(L_*\subseteq\{2A,A+B,2B\}\). Put \(N=A+B\), after relabelling.
Exact-flat realization gives \(a_n\asymp N\). For a reversible pair,
Lemma 3.2 of *certified_exact_shielded_seam.md* gives

\[
 {\cal L}_*{\cal F}_*\le K(1+N).
\tag{3.2}
\]

For the arbitrary directed triple the same statement is Lemma 4.1 there.
Attach the lower clocks by the conditional random-time-change
construction. Until the first lower clock the population path has the
top-only law, multiplied by a survival indicator bounded by one. Dynkin's
formula stopped at \(\sigma_n\), (3.2), and
\(\sigma_n\le T/a_n\le C T/N\) give (3.1).

#### The nonhomogeneous pair \(\{B,2A\}\)

Let the rates of \(B\to2A\) and \(2A\to B\) be \(\alpha,\beta>0\). Put
\(A=a,B=b\), and choose the correction in (2.3). The exact generator is

\[
\begin{split}
 {\cal L}_*{\cal F}_*(a,b)
 &=\alpha b\log{\beta(a+1)(a+2)\over\alpha b}\\
 &\quad+\beta(a)_2\log{\alpha(b+1)\over\beta(a)_2}.
\end{split}
\tag{3.3}
\]

Using \(\log u\le u-1\) in each term separately gives the pointwise bound

\[
 {\cal L}_*{\cal F}_*(a,b)
 \le\beta\{(a+1)(a+2)-a(a-1)\}+\alpha
 \le K(1+a).
\tag{3.4}
\]

Here \(q=A+2B\) is invariant, \(N_n\asymp\sqrt q\asymp A_0\), and
\(a_n\asymp N_n\). The Poisson domination (3.7) of
*rank_one_multichannel_carrier.md* gives

\[
 \sup_{t\le T/N_n}{\mathbb E}A_t\le C_TN_n.
\tag{3.5}
\]

Stopped Dynkin applied to (3.4), with the lower-clock survival indicator
deleted in the upper bound, proves (3.1).

#### The high-curvature pair \(\{2A,R+I\}\)

Let \(I\) denote the inactive cofactor. Along a top shell write

\[
 J=A+2I,\qquad K=R-I,\qquad I=i,\quad
 A=J-2i,\quad R=K+i.
\tag{3.6}
\]

For two states \(i_0,i\) on the shell, (2.1) gives exactly

\[
\begin{split}
 {\cal F}_*(i)-{\cal F}_*(i_0)
 &=\log{(J-2i)!\over(J-2i_0)!}
   +\log{(K+i)!\over(K+i_0)!}\\
 &\quad+\log{i!\over i_0!}
   +c_*(i-i_0),
\end{split}
\tag{3.7}
\]

where \(c_*=\ell_R+\ell_I-2\ell_A\) is fixed. Descriptor compactness and
bounded preceding lower jumps give

\[
 cN_n\le J\le CN_n,\qquad
 cN_n^2\le K\le CN_n^2
\tag{3.8}
\]

after a harmless finite enlargement; changing \(J,K\) by \(O(1)\) does not
alter these inequalities.

If \(i,i_0\le J/4\), summing the logarithms in the three factorial ratios
gives

\[
\begin{split}
 {\cal F}_*(i)-{\cal F}_*(i_0)
 &=(i-i_0)\{\log(K/J^2)+c_*\}\\
 &\quad+\log{i!\over i_0!}
   +O\!\left({(1+i+i_0)^2\over J}\right).
\end{split}
\tag{3.9}
\]

The error is uniform: every one of the \(2|i-i_0|\) \(A\)-factors lies
between \(J/2\) and \(J\), and every \(R\)-factor lies between \(K\) and
\(K+J/2\); applying
\(|\log(1+u)|\le2|u|\) and summing proves (3.9). Since \(K/J^2\) stays in
a compact subset of \((0,\infty)\),

\[
 \bigl({\cal F}_*(i)-{\cal F}_*(i_0)\bigr)^+
 \le C\{1+i\log(i+1)+i_0\log(i_0+1)\}
\tag{3.10}
\]

on this event.

The top-only cofactor estimate (3.10)--(3.11) of
*rank_one_multichannel_carrier.md* supplies \(\theta>0\) with

\[
 \sup_n\sup_{t\ge0}{\mathbb E}e^{\theta I_t}<\infty.
\tag{3.11}
\]

This remains true at a killed endpoint. Indeed, for any first lower edge
\(e\), conditional clock calculus gives, for \(\theta'<\theta\),

\[
\begin{split}
 {\mathbb E}\!\left[e^{\theta'I_{\sigma_n-}};\,\sigma_n<T/a_n\right]
 &\le {\mathbb E}\int_0^{T/a_n}
       e^{\theta'I_t}\Lambda_-(X_t)\,dt\le C_T .
\end{split}
\tag{3.12}
\]

The final inequality uses the exact rank-one source list: every lower
source has active weight at most one, so on this shell

\[
 \Lambda_-(X_t)\le C\{N_n(1+I_t)^2+(1+I_t)^2\},
\tag{3.13}
\]

and \(T/a_n=O(N_n^{-1})\). A smaller exponential absorbs the polynomial
factor. The window-end term is bounded directly by (3.11). A lower jump
changes \(I\) by at most two, so the estimate iterates through the fixed
carrier length.

On the complement of \(i,i_0\le J/4\), the factorial oscillation on the
shell is at most \(CN_n\log(N_n+2)\), whereas (3.11)--(3.12) make the
exceptional probability at most \(Ce^{-cN_n}\). Combining this with
(3.10) proves the stronger form

\[
 {\mathbb E}\bigl[
   ({\cal F}_*(X_{\sigma_n-})-{\cal F}_*(X_0))^+\bigr]\le C_T,
\tag{3.14}
\]

and hence (3.1). This is the step which prevents the pointwise
\(O(N_n^2)\) stochastic curvature of this template from being integrated
over an \(O(N_n^{-1})\) carrier window.

### Lemma 3.2 (independent zero-clock endpoint)

Consider one of the five top supports in (6.2) of
*rank_one_multichannel_carrier.md*. Start in an exact-flat compact
interior set, after a fixed number of bounded lower perturbations, and let
\(S\) be an independent exponential time whose rate lies in a fixed finite
positive set. Then

\[
 {\mathbb E}\bigl[{\cal F}_*(X_S)-{\cal F}_*(X_0)\bigr]\le C.
\tag{3.15}
\]

The same bound holds successively for any fixed deterministic number of
such waits.

#### Proof

First stop on leaving the larger compact interior set in the exponential
barrier estimate (6.5) of *rank_one_multichannel_carrier.md*. Let \(N\)
be the homogeneous active total, or \(N\asymp\sqrt q\) for
\(\{B,2A\}\), and set

\[
 W_N={\cal F}_*-\min_{\text{top shell}}{\cal F}_*.
\tag{3.16}
\]

On the stopped compact tube there are constants \(c,K>0\) such that

\[
 {\cal L}_*W_N\le N\{K-cW_N\}.
\tag{3.17}
\]

For a homogeneous support, write \(r=A/N\). The exact expansion is

\[
 {\cal L}_*{\cal F}_*
 =N^2p(r)\Phi(r)+O(N),
\tag{3.18}
\]

where \(p\) has one interior zero \(r_*\), points toward it, and
\(p(r)\Phi(r)\le-c(r-r_*)^2\) on the compact tube. Discrete convexity of
\(\log(A!)+\log(B!)+dA\) gives

\[
 W_N\le C\{1+N(r-r_*)^2\}.
\tag{3.19}
\]

Equations (3.18)--(3.19) prove (3.17). The same calculation covers each
two-node homogeneous support in (6.2) directly. No bounded-catalyst time
change is asserted or needed in Lemma 3.2.

For \(\{B,2A\}\), put \(u=\alpha B\) and \(v=\beta(A)_2\). Rewriting
(3.3) gives

\[
 {\cal L}_*{\cal F}_*=-(u-v)\log(u/v)+O(N)
\tag{3.20}
\]

uniformly when \(A/N\) stays in a compact subset of \((0,\infty)\); the
two shifted-factor logarithms make up the \(O(N)\) term. The unique root
of \(u=v\) is \(A/N=r_*+O(N^{-1})\), and on the tube

\[
 (u-v)\log(u/v)\ge cN^2(A/N-r_*)^2,\qquad
 W_N\le C\{1+N(A/N-r_*)^2\}.
\tag{3.21}
\]

This again proves (3.17).

Let \(\sigma\) be the tube exit. For the killed expectation
\(u_N(t)={\mathbb E}[W_N(X_t);\,t<\sigma]\), the boundary killing term is
nonpositive, and (3.17) gives

\[
 u_N(t)\le e^{-cNt}W_N(X_0)+K/c.
\tag{3.22}
\]

The barrier estimate (6.5) says, for every fixed \(L,m\),

\[
 {\mathbb P}\{\sigma\le L\log N\}\le C_{L,m}N^{-m}.
\tag{3.23}
\]

The full shell oscillation of \(W_N\) is \(O(N)\) in a homogeneous shell
and \(O(N^2\log(N+2))\) in a \(\{B,2A\}\) shell. Choose \(m\) and then
\(L\) so that both (3.23) and
\({\mathbb P}\{S>L\log N\}\) times this oscillation tend to zero. If the
rate of \(S\) is \(\rho\), integrating (3.22) gives

\[
\begin{split}
 {\mathbb E}W_N(X_S)
 &\le {\rho\over\rho+cN}W_N(X_0)+K/c+o(1),\\
 {\mathbb E}\{{\cal F}_*(X_S)-{\cal F}_*(X_0)\}
 &\le-{cN\over\rho+cN}W_N(X_0)+K/c+o(1)\le C.
\end{split}
\tag{3.24}
\]

A bounded lower perturbation cannot cross the fixed-width interior gap and
only changes the constants in (3.18)--(3.21). The strong Markov property
therefore iterates (3.24) through any fixed number of waits. \(\square\)

The stronger-looking global inequality (3.17) is not asserted. For
example, a homogeneous pair sharing a catalyst can leave an accessible
boundary only at rate \(O(N)\), while \(NW_N\) is \(O(N^2)\) there. The
stopped compact tube and exponentially small boundary probability are
essential.

## 4. Propensity-weighted logarithmic rewards

Return to the exact lower-tier notation

\[
 a_n=\max_{y\in L_-}(x_n\vee1)^y,\qquad
 {\cal M}=\{y:(x_n\vee1)^y/a_n\to c_y\in(0,\infty)\}.
\tag{4.1}
\]

At every compact carrier vertex, normalized active coordinates remain in
a compact subset of \((0,\infty)\); in the exceptional cofactor template
the inactive coordinate has the exponential bounds (3.11)--(3.12).
Consequently (2.2) has the following three uniform forms.

### Lemma 4.1 (edge rewards)

After restricting to a carrier compact event whose probability can be made
arbitrarily close to one:

1. if \(y,z\in{\cal M}\), then
   \((\Delta_{y\to z}{\cal F}_*)^+=O_{L^p}(1)\) for every fixed \(p\);
2. if \(y\in{\cal M}\) and \(z\notin{\cal M}\), then

   \[
    \Delta_{y\to z}{\cal F}_*=-g_{z,n}+O_{L^p}(1),\qquad
    g_{z,n}:=\log{a_n\over(x_n\vee1)^z}\longrightarrow\infty;
   \tag{4.2}
   \]

3. the expected positive contribution of every reaction sourced at
   \(y\notin{\cal M}\), over one \(T/a_n\) window, is \(o(1)\).

#### Proof

The first two statements follow immediately from (2.2), exact D-tier
equivalence, and the endpoint bounds just listed. Bounded population
jumps change the logarithm of every divergent coordinate by \(o(1)\), and
coordinates with finite caps contribute only an \(O_{L^p}(1)\) term.

For the third statement put

\[
 d_{y,n}=(x_n\vee1)^y,\qquad r_{y,n}=d_{y,n}/a_n\to0.
\tag{4.3}
\]

At time \(t\), write the source and target surrogate monomials as
\(d_{y,n}U_t\) and \(a_nV_t\). The moment estimate (3.6) of
*rank_one_multichannel_carrier.md* makes \(U_t,V_t\) uniformly integrable
on the window. By (2.2), fixed linear corrections, and falling-factorial
comparison, the normalized positive compensator is bounded by a constant
times

\[
 r_{y,n}U_t\left\{\log(1/r_{y,n})
                    +\log^+(V_t/U_t)+1\right\}.
\tag{4.4}
\]

The first term tends to zero because \(r\log(1/r)\to0\). For the second
use the elementary inequality

\[
 u\log^+(v/u)\le v/e,\qquad u,v\ge0,
\tag{4.5}
\]

with the value zero at \(u=0\). It is therefore at most
\(r_{y,n}{\mathbb E}V_t/e=o(1)\). Integration over a window of length
\(T/a_n\), followed by the finite sum over lower edges, proves the claim.
\(\square\)

This is the required subpower estimate. It controls propensity times the
actual logarithmic cost; an \(o(1)\) firing probability alone would not be
sufficient.

## 5. The 895 direct carriers

Use exactly the finite actual-target path (5.1) and macro-attempt of
*rank_one_multichannel_carrier.md*. Intersect its successful event with
one fixed compact endpoint event at each of its at most four vertices.
The transient moment estimates allow the compact to be chosen so that the
success probability remains a constant \(\pi>0\).

On that event the final edge has a maximal source and a target outside
\({\cal M}\). Lemma 4.1 gives

\[
 \Delta_{\rm final}{\cal F}_*\le-g_n+C,\qquad g_n\to\infty.
\tag{5.1}
\]

Every preceding maximal-to-maximal edge has expected positive cost \(O(1)\).
Lemma 3.1 bounds every intervening top segment by \(O(1)\), including the
two incidences in which the top linkage first creates the inactive
cofactor. Lemma 4.1 makes the total positive contribution of submaximal
interference \(o(1)\). Since the carrier length is bounded,

\[
 {\mathbb E}\bigl[{\cal F}_*(X_{\tau_n})-{\cal F}_*(x_n)\bigr]
 \le-\pi g_n+C+o(1)\longrightarrow-\infty.
\tag{5.2}
\]

Thus the 895 scalar \(H_w\)-carrier episodes are genuine corrected-factorial
episodes. No uniform lower bound on the D-tier gap is used; \(g_n\) may
diverge arbitrarily slowly.

## 6. The 25 cap-zero activation blocks

Use the deterministic attempt caps \(K_e,K_a,K_s\), the interior event
(6.5), and the debt arithmetic (6.6)--(6.10) of
*rank_one_multichannel_carrier.md*. On that interior event the active
logarithms satisfy, uniformly through every bounded lower perturbation,

\[
 \log(X_i\vee1)=w_i\log N_n+O(1)
\tag{6.1}
\]

for the two active species. This is immediate for a homogeneous shell.
For \(\{B,2A\}\), it is
\(\log A=\log N_n+O(1)\) and
\(\log B=2\log N_n+O(1)\). Hence every lower edge in the finite block has

\[
 \Delta_e{\cal F}_*
 =\Delta_eH_w\,\log N_n+O(1).
\tag{6.2}
\]

Lemma 3.2 bounds each independent zero-source wait by \(O(1)\) in expected
net top cost, and Lemma 3.1 does the same for each fast carrier window.
The number of both is deterministically bounded. Lemma 4.1 makes all
submaximal positive contributions \(o(1)\).

Let \(s_a,s_s,\eta\) have the meanings in (6.8). A completed activation
trial has zero \(H_w\)-reward: a possible \(0\to{\cal M}\) entry is paired
with its first \({\cal M}\)-exit. An unresolved trial has positive reward
at most one, and the additional unpaired service has reward at most
\(-1\). Equations (6.1)--(6.2) therefore lift the exact workload estimate
to

\[
\begin{split}
 {\mathbb E}\Delta{\cal F}_*
 &\le\{-(s_a-\eta)s_s+\eta\}\log N_n+O(1)+o(\log N_n)\\
 &\le-\tfrac12s_as_s\log N_n+O(1)\longrightarrow-\infty,
\end{split}
\tag{6.3}
\]

after enlarging \(K_e\) as in (6.8).

The exceptional interior-exit and long-wait probabilities are
super-polynomial by (6.5). The factorial oscillation on every relevant
shell is polynomial times \(\log N_n\), so their expected endpoint cost is
\(o(1)\). The per-window submaximal estimate is already an expected
logarithmic-cost estimate, not merely an event-probability estimate, and a
fixed number of attempts preserves \(o(1)\). Thus (6.3) also holds without
conditioning on the interior event.

## 7. What this does and does not close

Theorem 1.1 closes the common corrected-factorial endpoint obligation for
all 930 rank-one flat
incidences: 895 direct, 25 lower-activation, and ten finite-class boundary
incidences. The ten finite incidences need no stochastic episode.

It does not yet imply that all 310 carried support pairs are recurrent.
One must still check, pair by pair, that the same \({\cal F}_*\) handles
every other feasible descriptor and then apply the common-potential
physical-time gluing theorem. The finite compatibility calculation for
the 298 all-active/two-active overlaps removes one possible correction
conflict, but it does not perform that composition. In particular the
twelve all-active linear-workload seams require separate treatment.

## 8. Independent audit

An independent replay checked, in order:

1. the exact \(\{B,2A\}\) identity (3.3) and bound (3.4);
2. the uniform factorial-ratio expansion (3.9) and killed exponential
   moment (3.12) for \(\{2A,R+I\}\);
3. the stopped-tube coercivity (3.17), including catalyst-sharing
   homogeneous pairs;
4. the propensity-times-log estimate (4.4)--(4.5) under arbitrarily slow
   subpower separation;
5. retention of a positive-probability actual maximal-to-lower edge in
   (5.1); and
6. the conversion of the 25-case workload debt coefficient into the
   factorial coefficient in (6.3).

All six checks passed. In particular, the replay independently derived the
exact \(\beta(4A+2)+\alpha\) bound in (3.4), verified the
\(-2\log J+\log K+\log(i!)\) cancellation in (3.9), checked compensation
at the killed cofactor endpoint in (3.12), and confirmed that (4.5) is
strong enough for arbitrary subpower gaps. It also checked the actual-target
compact success event and the 25-case coefficient in (6.3).

The audit qualification is exactly the one now stated after (3.19): a
bounded shared catalyst could alter the physical scaling, but no such
time-change occurs among the five zero-clock top supports. The audit
certifies the local corrected-factorial episode only. Pair-level recurrence
still requires the selector and common-potential composition described in
Section 7.
