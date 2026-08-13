# Hostile audit of the hard exact-pair macroscopic entropy trace

**Audit date:** 2026-08-12 PDT  
**Audited file:** `research_notes/proof_first_hard_exact_pair_macroscopic_entropy.md`  
**Audited SHA-256:**
`751f524d6eb90018b7c53bcf396099cce7c138db7f05f7426aeaf74a067969b2`  
**Verdict:** **FAIL as written; analytically repairable.**

This is a proof audit, not an orientation search.  The nineteen-row finite
certificate was used only as a frozen premise sheet.  In particular, none of
the conclusions below is inferred from testing reaction orientations or from
a finite state box.

## 1. Executive finding

The exact carrier product (2.1), the effective lower hazard (2.2), its
exponent (2.3), the clean endpoint formula (3.1), and the exponent/entropy
identity (3.3) are correct.  The unique nonsingleton maximizing shell is also
identified correctly.

The proof nevertheless fails at (3.8).  The exponential stopping discussion
can control the *probability* and moments of a positive equality-shell
overshoot, but it cannot turn that overshoot into a pathwise negative bound.
There are clean, maximal-source paths of positive probability which leave the
shell strictly before the move cap and have positive total entropy increment.
Such paths are not any of the draft's defect events.  Section 4 consequently
uses a false pathwise premise.

This does not give a recurrence or T3-2 counterexample.  It invalidates the
stated local proof.  The desired expected drift follows after replacing
(3.8) by a killed exponential-Green estimate for the positive shell
overshoot.  Exact replacement statements are recorded in Sections 6--9.

There is also a smaller scope defect: Section 4 uses
\(\max_{y\in L_0}\phi(y)\ge0\), but Section 1's declared finite-premise list
does not include that fact.  It is true in all nineteen frozen rows and should
be made an explicit fifth premise and test.

## 2. Carrier formula: PASS

During a proper-only excursion from the no-fast base \((u,v,0)\), level
\(i=I\) has

\[
 (U,V,I)=(u-ai,v+i,i),\qquad
 \lambda_i=\alpha(u-ai)_{\underline a},\quad
 \mu_i=\beta(v+i)i .
\]

Detailed balance gives

\[
 {\pi_i\over\pi_0}
 =\rho^i{(u)_{\underline{ai}}\over i!(v+1)^{\overline i}}.
\]

For a lower source \(y=cU+bI\), multiplication by
\((u-ai)_{\underline c}(i)_{\underline b}\), followed by \(i=b+j\), gives

\[
 A_e(u,v)=
 {\kappa_e\rho^b(u)_{\underline{c+ab}}
  \over(v+1)^{\overline b}}
 \sum_{j\ge0}{\rho^j
 (u-c-ab)_{\underline{aj}}
 \over j!(v+b+1)^{\overline j}}.
\]

Thus (2.2) is exact.  The ratio of consecutive summands is at most
\(C u^a/[v(j+1)]\).  Since every audited row has \(q-pa\ge1\), the series is
\(1+O(s^{pa-q+o(1)})=1+O(s^{-1+o(1)})\), uniformly after
\(O(\log s)\) bounded macros.  Hence

\[
 A_e(u,v)=s^{p(c+ab)-qb+o(1)}=s^{\phi(y)+o(1)}.
\]

Direct level-zero lower clocks are included by the \(i=0\) term; no base-time
versus excursion-time mismatch occurs in this formula.

## 3. First-kill and dirty-cleanup estimates: correct conclusion, missing macroscopic lemma

The conclusion (2.4) is valid for the nineteen premises, but it does not
follow literally by citing the subpower ordered-Green lemma.  The required
macroscopic version must retain the largest actual lower \(U\)-degree
\(c_*\), rather than use the crude universal quadratic bound.  This matters
for the \((p,q)=(4,5)\), \(a=0\) row: \(u^2/v\) is large there, whereas the
actual support has \(c_*=1\) and \(u/v=s^{-1+o(1)}\).

Let

\[
 \gamma=\min\{q-pa,\ q-pc_*\}.
\]

The frozen premises give \(\gamma\ge1\).  Repeating the reversible ordered
two-insertion proof sourcewise, with
\(K(i)\le C\sum_{cU+bI\in L_0}u^c(1+i)^b\), yields

\[
 0\le A_e-\widehat A_e
 \le C s^{-\gamma+o(1)}A_e.                         \tag{A1}
\]

After the first firing, the shifted carrier has \(u+O(1),v+O(1)\).  Its
edge-size-biased initial level is \(b+J\), where all fixed moments of \(J\)
are \(O(s^{pa-q+o(1)})\).  The same downward potential then gives

\[
 \mathbb E[(1+I_E+|U_E-U|+|V_E-V|)^r;
       \hbox{second lower firing}\mid e]
 \le C_r s^{-\gamma+o(1)}.                         \tag{A2}
\]

The endpoint in (A2) includes the second firing.  Equations (A1)--(A2), not
the subpower estimate with \((1+u)^2/v\), are the publication-grade bridge
needed for (2.4) in every one of the nineteen regimes.

The finite \(\phi\)-gap from a maximizer to a nonmaximizer is at least one,
so (A1) also gives, uniformly over \(O(\log s)\) shell macros,

\[
 \mathbb P\{\hbox{nonmaximal source or dirty cleanup at a given macro}\}
 =O(s^{-1+o(1)}).                                    \tag{A3}
\]

## 4. Entropy-gradient identity: PASS

For a clean macro \(y\to z\), carrier cancellation gives

\[
 \Delta U=-w_a(y)+w_a(z),\qquad
 \Delta V=b_y-b_z,qquad \Delta I=0.
\]

Since \(U=s^{p+o(1)}\), \(V=s^{q+o(1)}\), and the jumps are bounded,

\[
 \begin{aligned}
 \Delta G_\ell
 &=\{p[-w_a(y)+w_a(z)]+q[b_y-b_z]\}\log s+o(\log s)\\
 &=\{\phi(z)-\phi(y)\}\log s+o(\log s).
 \end{aligned}
\]

The fixed linear correction contributes only \(O(1)\).  Thus (3.3) has the
correct sign and is uniform over a logarithmic block.  If the maximizer is a
singleton, every nontrivial outgoing lower edge leaves it, and the first
maximal-source clean macro has a strict negative increment of at least
\(-\log s+o(\log s)\).

## 5. Exact analytic counterexample to the pathwise claim (3.8)

Use the unique exceptional premise

\[
 (p,q,a)=(1,3,2),\qquad
 L_+=\{2U,V+I\},\qquad
 L_0=\{0,I,2I,U+I\}.
\]

Choose the strong lower orientation

\[
             0\longrightarrow U+I\longrightarrow I
              \longrightarrow2I\longrightarrow0.             \tag{C1}
\]

Take \(\ell=0\), \(U_0=s\), and
\(V_0=\lfloor s^3/e\rfloor\).  Choose fixed positive edge rates so that,
among the two maximal-source clocks, the clean edge \(0\to U+I\) is selected
with limiting probability \(9/10\) and the strict edge \(U+I\to I\) with
limiting probability \(1/10\).  This is permitted because those two
effective hazards are both order one and their constants are arbitrary and
fixed.  Proper rates may, for example, be fixed with \(\rho=1\).

Each clean equality macro \(0\to U+I\) sends

\[
 (U_k,V_k)=(s+3k,V_0-k)\longmapsto(U_{k+1},V_{k+1})
\]

and has the exact factorial increment

\[
 \log{(U_k+1)(U_k+2)(U_k+3)\over V_k}=1+o(1)                 \tag{C2}
\]

uniformly for \(k=O(\log s)\).  The strict macro
\(U+I\to I\) has \(\Delta U=-1,\Delta V=0\), hence increment

\[
                         -\log U+o(1)=-\log s+o(\log s).       \tag{C3}
\]

Let \(m=\lceil2\log s\rceil\).  The event consisting of \(m\) successive
clean \(0\to U+I\) macros followed by one clean \(U+I\to I\) macro has
strictly positive probability for every \(s\).  Along this event:

* every selected source is in \(Y_*=\{0,U+I\}\);
* there is no second lower firing and no carrier boundary;
* the accumulated equality entropy never reaches \(-2\log s\); and
* the total entropy increment is
  \((2+o(1))\log s-(1+o(1))\log s=(1+o(1))\log s>0\).

Moreover, a move cap satisfying (3.7) for \(M=1\) in this example must have
\(C_M\ge1/[-\log(9/10)]>9\), because the probability of surviving
\(C_M\log s\) equality births is at least
\((9/10)^{C_M\log s+o(\log s)}\).  Therefore the path above, with only
\((2+o(1))\log s\) moves, occurs strictly before that cap.  It is a regular
path under the draft's stopping rule and contradicts (3.8).

The same example explains the repair: the bad path has polynomially small
probability.  What is true is an exponential *tail* for positive shell
overshoot and a negative *expectation* after the strict exit, not a pathwise
negative inequality.

## 6. Replacement equality-shell lemma

The following lemma is sufficient and is the form that should replace the
paragraph beginning with the kinetic tube through (3.8).

### Lemma (killed exponential Green bound on the exceptional shell)

Let

\[
 U_k=u+3k,\qquad V_k=v-k,\qquad
 H(k)=G_\ell(U_k,V_k,0),
\]

where \(u=s^{1+o(1)}\), \(v=s^{3+o(1)}\).  Contract proper excursions and
discard the defect events in (A3).  Write \(b_k,d_k,r_k\) for the clean
equality-birth, equality-death, and strict-exit rates from shell state \(k\).
For \(|k|\le C\log s\), there are fixed nonnegative constants
\(B,D,R_0,R_1\), with \(R_0+R_1>0\), such that

\[
 \begin{aligned}
 b_k&=B[1+O(s^{-1+o(1)})],\\
 d_k&=D{(U_k)_{\underline3}\over V_k+1}
          [1+O(s^{-1+o(1)})],\\
 r_k&=\left(R_0+R_1{(U_k)_{\underline3}\over V_k+1}\right)
          [1+O(s^{-1+o(1)})].                         \tag{E1}
 \end{aligned}
\]

Here a missing equality direction means \(B=0\) or \(D=0\).  Strong
connectivity and the properness of \(Y_*\) give \(R_0+R_1>0\).  When both
equality directions are present, the adjacent rate ratio satisfies

\[
 {d_{k+1}\over b_k}
 =C_*\exp\{H(k+1)-H(k)\}
   [1+O(s^{-1+o(1)})]                                  \tag{E2}
\]

after absorbing the fixed rate, proper-carrier, and \(\ell\)-constants into
\(C_*>0\).

Stop the clean shell at the first of:

1. a strict exit;
2. \(H(k)-H(0)\le-2\log s\); or
3. \(N=C_M\log s\) equality moves.

For every fixed \(M,r\), \(C_M\) can be chosen, depending only on the fixed
rates and orientation, so that

\[
 \begin{aligned}
 \mathbb P\{\tau=N\}&\le s^{-M},\\
 \mathbb P\!\left\{\max_{j\le\tau}[H(k_j)-H(0)]\ge h\right\}
   &\le C e^{-\theta h}+s^{-M},\qquad 0\le h\le C'\log s,\\
 \mathbb E\left([H(k_{\tau-})-H(0)]_+^r;	au<N\right)&\le C_r.
                                                               \tag{E3}
 \end{aligned}
\]

The proof splits at a fixed kinetic tube.  Inside the tube, the source of a
strict cut has a uniform positive chance to be selected at every step.
Outside it, (E2) says that an uphill move of entropy height \(h\) has weight
at most \(Ce^{-h}\) relative to a downhill move or killing.  Applying the
embedded kernel to \(\exp\{\theta[H-H(0)]_+\}\), with
\(0<\theta<1\), gives a strict killed Foster inequality.  Optional stopping
gives the second line of (E3), and the layer-cake formula gives the third.
The same Foster inequality with a move mark gives the first line.  If one
equality direction is missing, the corresponding one-sided argument is
strictly simpler.

Every strict exit from \(Y_*\) has integer \(\phi\)-gap at least one, so
uniformly before the logarithmic cap,

\[
 H(k_{\tau})-H(k_{\tau-})\le-\log s+o(\log s).                 \tag{E4}
\]

Combining (E3)--(E4), rather than claiming a pathwise sign, yields

\[
 \mathbb E[\Delta G_\ell;\hbox{clean shell}]
       \le-(1-o(1))\log s,qquad
 \mathbb E[|\Delta G_\ell|^r;\hbox{clean shell}]
       =O(\log^r s).                                           \tag{E5}
\]

Indeed, the entropy-threshold branch pays \(-2\log s+o(\log s)\), the
strict branch pays (E4) after an integrable positive overshoot, and the cap
has arbitrarily small endpoint-weighted mass.

## 7. Defect and carrier-boundary replacement

Let \(\delta_s=s^{-1+o(1)}\).  Equations (A1)--(A3) give a conditional
defect probability at most \(C\delta_s\) at every occupied clean shell
state, with all fixed moments of the carrier-level and bounded reaction
increments.  The move-marked version of (E3) gives

\[
 \mathbb E\sum_{j<\tau}
  \{1+|H(k_j)-H(0)|^r\}=O(\log^{r+1}s).
\]

Consequently, if the defect-causing reaction is included in the endpoint,

\[
 \mathbb P(E_{\rm defect})=O(s^{-1+o(1)}),\qquad
 \mathbb E[|\Delta G_\ell|^r;E_{\rm defect}]
       =O(s^{-1+o(1)}\log^r s).                               \tag{D1}

\]

The harmless extra logarithm from the occupation sum is absorbed by
\(s^{o(1)}\).  A carrier level \(K_M\log s\) requires a product of
birth/death ratios bounded by \(s^{-1+o(1)}/i\).  Even after the polynomial
number of proper openings occurring during \(O(\log s)\) macros, its
endpoint-weighted probability is \(O(s^{-M})\) after increasing \(K_M\).
The move-cap endpoint has the same property after choosing the exponent in
(E3) larger than the requested endpoint moment.  These are separate from
the ordinary defect in (D1) and should be labelled separately in the
stopping rule.

## 8. Duration: PASS after one explicit compound-excursion lemma

The finite premise sheet should explicitly add

\[
                    \max_{y\in L_0}\phi(y)\ge0.                \tag{T1}

\]

It holds in all nineteen frozen rows.  Thus the total effective lower hazard
at every shell base is \(s^{o(1)}\) or larger, and level-zero waiting time for
one macro has all fixed moments \(s^{o(1)}\).

Conditioned on a level-zero time interval \(T\), proper openings form a
Poisson process of rate at most \(Cs^{pa+o(1)}\).  Each completed excursion
has fixed time moments bounded by \(C_r s^{-qr+o(1)}\), because its downward
clock at level \(i\) is at least \(cVi\) and its upward/downward ratio is
\(O(s^{pa-q+o(1)})\).  The compound-Poisson moment recursion therefore gives

\[
 \mathbb E[\eta^r]\le s^{o(1)}                                \tag{T2}
\]

for one contracted physical macro.  Singleton-maximizer rows use one macro;
the exceptional row uses at most \(C_M\log s\).  Minkowski's inequality (or
the time-marked finite Green recursion) and (T2) yield

\[
                         \mathbb E\sigma^r=s^{o(1)}.            \tag{T3}

\]

No global shell mixing estimate is needed.

## 9. Fourth-power lift: PASS conditional on the repaired mean and moments

At the starting state,

\[
 G_\ell(X_0)=s^{q+o(1)}\log s.

\]

Using (E5), (D1), the superpolynomial boundary estimates, and the singleton
argument gives

\[
 \mathbb E\Delta G_\ell\le-c\log s,qquad
 \mathbb E|\Delta G_\ell|^r=O(\log^r s).                       \tag{F1}

\]

The exact identity

\[
 (G+\Delta G)^4-G^4
 =4G^3\Delta G+6G^2(\Delta G)^2
   +4G(\Delta G)^3+(\Delta G)^4
\]

then shows that the negative first term dominates all remaining terms.
Equation (T3) is negligible on the same scale.  Hence

\[
 \mathbb E[W_\ell(X_\sigma)-W_\ell(X_0)+\sigma]
 \le-c'G_\ell(X_0)^3\log s.                                  \tag{F2}

\]

Thus the scoped theorem is plausibly true, but (F2) is not proved by the
audited SHA until (3.8) is replaced by (E1)--(E5), the macroscopic
sourcewise lemma (A1)--(A2) is supplied, and (T1) is added to the frozen
finite premises.

## 10. Strict disposition

* Exact carrier hazard: **PASS**.
* Source exponent and clean endpoint identity: **PASS**.
* Entropy-gradient identity: **PASS**.
* Singleton-maximizer rows: **PASS**, subject to the macroscopic
  sourcewise perturbation lemma (A1)--(A2).
* Exceptional two-source pathwise block (3.8): **FAIL**, by (C1)--(C3).
* Endpoint-weighted defect conclusion: **repairable**, but must be derived
  from the killed Green estimate (E3), not from false (3.8).
* Duration: **PASS after explicitly adding (T1) and (T2)**.
* Fourth-power algebra: **PASS conditional on repaired (F1)**.
* Scoped theorem at audited SHA: **FAIL**.
