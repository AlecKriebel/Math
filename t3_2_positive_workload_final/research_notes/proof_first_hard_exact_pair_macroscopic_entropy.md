# Macroscopic entropy trace for the hard exact carrier pairs

**Proof-first scoped theorem, 2026-08-12 PDT.  Audit status: pending.**
This note treats the exact carrier pairs in the physical two-active hard
phase.  It is deliberately separate from the generalized one-active cloud
theorem: here both \(U\) and \(V\) are macroscopic.

Fix an arbitrary strong orientation and arbitrary positive rate constants.
Constants below may depend on those fixed data.  No orientation enumeration
or finite state box is a proof input.

## 1. Exact asymptotic regime

Let

\[
 U=s^{p+o(1)},\qquad V=s^{q+o(1)},\qquad I=0,
 \qquad 0<p<q,                                                   \tag{1.1}
\]

and suppose the proper linkage is

\[
                         L_+=\{aU,V+I\},\qquad a\in\{0,1,2\}.  \tag{1.2}
\]

The actual hard exact-pair rows have either \(a=0\), or
\((p,q)=(1,3)\).  Hence

\[
                         q-pa\ge1.                              \tag{1.3}
\]

For the lower complex \(y=c_yU+b_yI\), put

\[
 w_a(y)=c_y+ab_y,
 \qquad
 \phi_{p,q,a}(y)=p\,w_a(y)-q b_y.                              \tag{1.4}
\]

The physical hard menu contains nineteen distinct normalized ratio/support
rows of the form (1.2): seventeen at ratio \((1,3)\), one at \((1,2)\),
and one at \((4,5)\).  The finite exact-support table is used only for the following four
structural facts:

1. every lower source is one of \(0,U,2U,I,2I,U+I\);
2. the largest \(U\)-degree occurring in a lower support obeys
   \(q-pc_{\max}\ge1\); and
3. the maximizer set
   \(Y_*:=\{y\in L_0:\phi(y)=\max_{z\in L_0}\phi(z)\}\)
   is a nonempty proper subset of the strong lower linkage; and
4. \(Y_*\) is a singleton except for
   \((p,q,a)=(1,3,2)\),
   \(L_0=\{0,I,2I,U+I\}\), where \(Y_*=\{0,U+I\}\).
5. \(\max_{y\in L_0}\phi(y)\ge0\).

These facts are support identities, independent of orientation and rates.

## 2. Exact carrier averaging

At a no-fast base \((u,v,0)\), the proper carrier level \(i=I\) has

\[
 (U,V,I)=(u-ai,v+i,i),
 \qquad
 {\pi_i\over\pi_0}
 =\rho^i{(u)_{\underline{ai}}
          \over i!(v+1)^{\overline i}}.                         \tag{2.1}
\]

For a lower edge \(e:y\to z\), its exact un-killed hazard per unit
level-zero local time is

\[
 A_e(u,v)=
 {\kappa_e\rho^{b_y}(u)_{\underline{w_a(y)}}
  \over(v+1)^{\overline{b_y}}}
 \sum_{j\ge0}{\rho^j
 (u-w_a(y))_{\underline{aj}}
 \over j!(v+b_y+1)^{\overline j}}.                             \tag{2.2}
\]

By (1.1)--(1.3), the sum in (2.2) is \(1+o(1)\), uniformly after any
bounded number of macros.  Therefore

\[
                         A_e(u,v)=s^{\phi(y)+o(1)}.              \tag{2.3}
\]

Let \(c_*\) be the largest actual lower \(U\)-degree.  Repeating the
reversible ordered-Green proof sourcewise, rather than using a crude
quadratic clock bound, gives

\[
 0\le A_e-\widehat A_e
 \le C s^{-\gamma+o(1)}A_e,
 \qquad \gamma=\min\{q-pa,q-pc_*\}\ge1,                       \tag{2.4}
\]

where \(\widehat A_e\) is the exact first-lower killed hazard.  Indeed, the
carrier birth/death ratio is \(O(s^{pa-q+o(1)}/i)\), and the future lower
hazard after a distinguished insertion is bounded using only the monomials
actually present, by \(Cs^{pc_*-q+o(1)}\), with every carrier-level size
bias.  Reversibility identifies the past- and future-ordered integrals.
After the first firing, the shifted carrier has \(u+O(1),v+O(1)\) and an
edge-size-biased factorial initial level, so the same downward potential
gives, for every fixed \(r\),

\[
 \mathbb E[(1+I_E+|U_E-U|+|V_E-V|)^r;
       \hbox{second lower firing}\mid e]
 \le C_r s^{-\gamma+o(1)}.                                   \tag{2.5}
\]

Thus the first source belongs to \(Y_*\) with probability
\(1-O(s^{-1+o(1)})\), and a selected macro is clean with the same
probability.  The statement is valid also for the \((p,q)=(4,5)\) row,
where its actual lower degree is one; no false \(u^2/v\) estimate is used.

## 3. Rate exponent equals entropy gradient

If the clean first lower edge is \(y\to z\), exact carrier cancellation
gives the no-fast endpoint

\[
 u'=u-w_a(y)+w_a(z),
 \qquad
 v'=v+b_y-b_z.                                                  \tag{3.1}
\]

Let

\[
 G_\ell(x)=K_\ell+\sum_j\log(x_j!)+\ell\mathbin\cdot x\ge1,
 \qquad W_\ell=G_\ell^4,                                      \tag{3.2}
\]

for an arbitrary fixed common correction vector \(\ell\).  Stirling's
bounded-jump formula and (1.1) give

\[
\begin{aligned}
 G_\ell(u',v',0)-G_\ell(u,v,0)
 &=\{p[-w_a(y)+w_a(z)]+q[b_y-b_z]\}\log s+o(\log s)\\
 &=\{\phi(z)-\phi(y)\}\log s+o(\log s).                       \tag{3.3}
\end{aligned}
\]

This identity is the central point: the exponent which selects the next
physical lower source is exactly the negative gradient of the physical
factorial entropy along its clean macro.

For \(y\in Y_*\), (3.3) is nonpositive to leading order.  It is strictly
negative when \(z\notin Y_*\).  If \(Y_*\) is a singleton, a lower edge
cannot remain inside it, so the first leading clean macro is already strict.

It remains to handle the unique two-source equality shell in structural
fact 4.  Write \(k\) for the net number of clean (0\to U+I) macros.  On
that shell

\[
 U_k=u+3k,\qquad V_k=v-k,                                      \tag{3.4}
\]

and, after the exact carrier average, the two equality-source scales are

\[
 \lambda_k=\alpha_0[1+o(1)],
 \qquad
 \mu_k=\alpha_1{(u+3k)_{\underline3}\over v-k}[1+o(1)].       \tag{3.5}
\]

The equality transition itself may be absent in one direction, which only
adds killing.  If it is present, the bounded-jump factorial identity gives

\[
 G_\ell(k+1)-G_\ell(k)
 =\log{(u+1+3k)(u+2+3k)(u+3+3k)\over v-k}+O(1).                \tag{3.6}
\]

Thus, after absorbing the fixed rate and \(\ell\)-constants into the
center, a birth has negative entropy drift when \(\lambda_k\) dominates,
and a death has negative entropy drift when \(\mu_k\) dominates.  Strong
connectivity supplies a strict edge from the proper subset
\(\{0,U+I\}\).  If that edge is sourced at the currently dominant equality
source, its killing rate is comparable to the dominant equality rate; if
it is sourced at the other source, the dominant equality move points toward
the kinetic center and decreases \(G_\ell\).

Use this dichotomy only for a logarithmic killed Green block; no global
shell mixing assertion is needed.  Let \(H(k)=G_\ell(U_k,V_k,0)\), and
write \(b_k,d_k,r_k\) for the clean equality-birth, equality-death, and
strict-exit rates.  Uniformly for \(|k|\le C\log s\),

\[
 \begin{aligned}
 b_k&=B[1+O(s^{-1+o(1)})],\\
 d_k&=D{(U_k)_{\underline3}\over V_k+1}
          [1+O(s^{-1+o(1)})],\\
 r_k&=\left(R_0+R_1{(U_k)_{\underline3}\over V_k+1}\right)
          [1+O(s^{-1+o(1)})],
 \end{aligned}                                                \tag{3.7}
\]

where missing equality directions mean \(B=0\) or \(D=0\), while strong
connectivity and properness of \(Y_*\) give \(R_0+R_1>0\).  When both
directions occur, the adjacent detailed-balance ratio is

\[
 {d_{k+1}\over b_k}
 =C_*\exp\{H(k+1)-H(k)\}[1+O(s^{-1+o(1)})].                  \tag{3.8}
\]

Stop at a strict exit, at \(H(k)-H(0)\le-2\log s\), or after
\(N=C_M\log s\) equality moves.  Inside a fixed kinetic tube, the source
carrying a strict cut has a uniform positive selection probability.
Outside it, (3.8) says that an uphill entropy move of height \(h\) has
weight at most \(Ce^{-h}\) relative to a downhill move or killing.
Applying the embedded killed kernel to
\(\exp\{\theta[H-H(0)]_+\}\), \(0<\theta<1\), gives a strict Foster
inequality.  Optional stopping and layer-cake integration yield, after
choosing \(C_M\),

\[
 \begin{aligned}
 \mathbb P\{\tau=N\}&\le s^{-M},\\
 \mathbb P\{\max_{j\le\tau}[H(k_j)-H(0)]\ge h\}
   &\le Ce^{-\theta h}+s^{-M},\\
 \mathbb E([H(k_{\tau-})-H(0)]_+^r;\tau<N)&\le C_r .
 \end{aligned}                                                \tag{3.9}
\]

During only \(O(\log s)\) moves, a nonmaximal source or second lower
insertion has total endpoint-weighted probability \(s^{-1+o(1)}\).  Thus
one may retain it as the defect event rather than prove a global equality
Green theorem.  Every strict exit has integer \(\phi\)-gap at least one,
so its terminal increment is at most \(-\log s+o(\log s)\).
Combining this terminal decrement with (3.9), rather than asserting a
false pathwise sign, gives

\[
 \mathbb E[\Delta G_\ell;\hbox{clean shell}]
       \le-(1-o(1))\log s,
 \qquad
 \mathbb E[|\Delta G_\ell|^r;\hbox{clean shell}]
       =O(\log^r s).                                           \tag{3.10}
\]

## 4. Defects, time, and fourth power

Stop at the strict clean exit in (3.10), or at the first subleading source,
second lower firing, logarithmic move cap, or included carrier boundary
\(I\ge K_M\log s\).  Include the boundary-causing physical reaction.
Equations (2.1)--(2.5) and the move-marked version of (3.9)
and the logarithmic equality-block bound give, for every fixed \(r\),

\[
 \mathbb P(E)=O(s^{-1+o(1)}),
 \qquad
 \mathbb E[|\Delta G_\ell|^r;E]=O(s^{-1+o(1)}\log^r s),        \tag{4.1}
\]

while the carrier and move-cap boundaries have superpolynomially small
endpoint-weighted mass.  The leading effective hazard has exponent
\(\max_y\phi(y)\ge0\) in every actual exact support, so one macro has all
fixed physical-time moments \(s^{o(1)}\).  A time-marked finite Green
recursion therefore gives

\[
                         \mathbb E\sigma^r=s^{o(1)}.             \tag{4.2}
\]

Combining (3.10), (4.1), and the clean endpoint moment bounds yields

\[
 \mathbb E\Delta G_\ell\le-c\log s,
 \qquad
 \mathbb E|\Delta G_\ell|^r=O(\log^r s).                       \tag{4.3}
\]

At the starting state, \(G_\ell=s^{q+o(1)}\log s\).  The exact fourth-power
expansion and (4.2)--(4.3) give

\[
 \mathbb E[W_\ell(X_\sigma)-W_\ell(X_0)+\sigma]
 \le-cG_\ell(X_0)^3\log s.                                    \tag{4.4}
\]

### Scoped theorem

For every macroscopic hard row whose proper linkage is the exact carrier
pair (1.2), every strong orientation, every fixed positive rate vector, and
every fixed common correction \(\ell\), the raw physical stopped episode
above has the common-fourth-power drift (4.4), arbitrary fixed endpoint
moments, and finite physical-time moments.  The proof is analytic; the
finite table is used only for the three support identities in Section 1.

This theorem does not cover the larger proper supports, does not cover the
generalized one-active subpower regime, and makes no pair/global claim until
independently audited and composed.
