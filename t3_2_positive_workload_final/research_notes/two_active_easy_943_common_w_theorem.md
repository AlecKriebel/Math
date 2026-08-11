# The easy 943 promotion incidences and the certified 416-pair theorem

## 1. Scope and certification boundary

This note separates a local analytic theorem from a larger pair-level
candidate theorem.  The finite selectors are frozen in
`src/two_active_easy_common_w.py`.

The post-exact-26 remainder has 769 support pairs.  Its two-active promotion
table has 1,350 incidences on 749 pairs and splits as follows.

| physical mechanism | incidences | pair union |
|---|---:|---:|
| enabled top seed | 929 | 550 |
| dormant rank-two access word (the nominal Poisson rows) | 8 | 8 |
| dormant finite rank-one shell | 6 | 6 |
| dormant, no whole-top linkage | 407 | 333 |

The first three rows are the **easy 943**.  Their pair union has 555 pairs
(527 positive and 28 signed).  The exact pair fingerprints are

```text
easy-943 union: 19420077a2e54b88498f8f791fbe05a967c26bef882a06c5e76a48973df676d5
hard-407 union: d3c9dad6e8510a81efee6c56873de0f1f2cf6f24d3f50b46d4cf22abb2ad9484
```

Exactly 416 pairs have **every** promotion incidence in the easy family.
They consist of 414 positive pairs and two signed pairs and have fingerprint

```text
8c3325983568c53772f024080c0b95d37873cfe0a149386ec9829d1d9323e186
```

This note proves the easy-943 stopped estimate and composes every remaining
interface on those 416 pairs.  Independent audit replayed the stochastic
endpoint estimates, all arbitrary-orientation cuts, the common correction,
and the marked fixed-class argument.  The exact 416-pair recurrence flag is
therefore certified.  Global T3-2 remains false.

There is one important qualification.  The 937 bounded access-word rows
work for any fixed linear correction \(\ell\).  The six finite rank-one
shell rows do **not**.  They require the usual rate-adjusted correction on
their fixed whole shell.  Section 5 gives an exact counterexample to the
stronger arbitrary-\(\ell\) assertion.

## 2. The common fourth-power potential

For a fixed network and a fixed closed population class, put

\[
 F_\ell(x)=K+\sum_{i=1}^3\log(x_i!)+\ell\mathbin\cdot x,
 \qquad G=1+F_\ell,
 \qquad W=G^4,                                      \tag{2.1}
\]

where \(K\) is chosen so that \(F_\ell\ge1\).  A fixed linear correction
does not destroy properness: the factorial term dominates every linear
term at infinity.

The correction menu on the 416-pair selector is exact and disjoint.

| common correction | pairs | fingerprint |
|---|---:|---|
| arbitrary fixed \(\ell\), chosen as \(0\) if desired | 371 | `77b42a7079d38c1b83b322b1e46fa4ea61dc4a7203a33760dd856b0a883ebca4` |
| reversible-shell rate adjustment | 29 | `d5026791e3166315e347a6d4b938f1d9f8315a898f785d1ace92026286437392` |
| directed-triple rate adjustment | 16 | `3d1a90f712f00ed4d343a97dcfc10b218a779a26640789dec232799d727f2712` |

For a reversible top \(y\rightleftarrows z\), the constraint is

\[
 \ell\mathbin\cdot(z-y)
   =\log\frac{\kappa_{zy}}{\kappa_{yz}}.             \tag{2.2}
\]

For \(\{2X,X+Y,2Y\}\), the correction is the rate-dependent one from the
directed fluid polynomial in the certified rank-one triple theorem.  The 23
reversible and 16 directed-triple all-active pairs use exactly the same top
mask in all their two-active closed-rank-one failures.  The six finite
promotion-shell pairs are disjoint from those 39 pairs.  Thus (2.2), or its
directed-triple analogue, imposes at most one correction on each pair.

### 2.1 A powered shell-overshoot lemma

The fourth power needs more than the first-moment endpoint estimate quoted
in the earlier corrected-factorial theorem.  The following strengthening is
the precise input used below.

> **Lemma 2.1 (positive shell overshoot).**  On any rank-one top shell used
> in Sections 5 and 7, let
> \[
> Z_N=F_\ell-\min_{\mathrm{shell}}F_\ell .           \tag{2.3}
> \]
> Start in an exact-tier compact interior, allowing a fixed number of
> bounded lower perturbations.  If \(S\) is an independent exponential
> time, or if \(\sigma\) is one of the killed top-window endpoints in the
> carrier construction, then, for every fixed \(r<\infty\),
> \[
> \sup_N\mathbb E
> \left[\left\{(F_\ell(X_S)-F_\ell(X_0))^+\right\}^r\right]<\infty,
> \tag{2.4}
> \]
> and the same bound holds with \(S\) replaced by \(\sigma\).

Use the one-dimensional shell coordinate from the audited rank-one
endpoint theorem.  Put \(s_N=1\) for \(A\rightleftarrows B\), and
\(s_N=N\) for \(B\rightleftarrows2A\) and for a homogeneous quadratic
shell.  The exact paired finite differences, strict inward shell drift,
and discrete convexity give, on the compact interior,

\[
\begin{split}
 \mathcal L_*Z_N&\le s_N(C-cZ_N),\\
 \sum_e\lambda_e(\Delta_eZ_N)^2
       e^{\theta|\Delta_eZ_N|}&\le Cs_N(1+Z_N)
\end{split}                                          \tag{2.5}
\]

for every sufficiently small fixed \(\theta>0\).  For
\(A\rightleftarrows B\), insert
\(\Delta_-Z_N=\log\{\kappa_{BA}(B+1)/(\kappa_{AB}A)\}\) and its reverse.
For \(B\rightleftarrows2A\), the two logarithms in the exact generator
formula give dissipation \(N^2(r-r_*)^2\), while
\(1+Z_N\asymp1+N(r-r_*)^2\).  For an arbitrary directed homogeneous triple,
the audited \(p(r)\Phi(r)\) calculation gives the first line of (2.5), and
bounded top jumps give the second.  Taylor's formula, after reducing
\(\theta\) once, therefore yields

\[
 \mathcal L_*e^{\theta Z_N}
 \le-cs_Ne^{\theta Z_N}+Cs_N .                       \tag{2.6}
\]

Consequently the stopped semigroup satisfies

\[
 \mathbb E_xe^{\theta Z_N(X_t)}
 \le e^{-cs_Nt}e^{\theta Z_N(x)}+C.                  \tag{2.7}
\]

The compensation formula gives the same estimate at a killed endpoint:
on the descriptor compact set its normalized killing density is a fixed
degree polynomial, which is absorbed after decreasing \(\theta\).  Hence

\[
 \mathbb P_x\{Z_N(X_\rho)-Z_N(x)>u\}\le Ce^{-cu}     \tag{2.8}
\]

for every endpoint \(\rho\) above, up to exit from the enlarged compact
tube.  The existing exponential-barrier estimate makes that exit
super-polynomially unlikely on the required horizons.  The full shell
factorial oscillation is polynomial in \(N\), so choosing the barrier power
after \(r\) removes the stop.  Integrating (2.8) proves (2.4); a fixed
number of bounded perturbations changes only the constant.

## 3. A bounded top-access word

The reusable local statement is the following.

> **Lemma 3.1 (all-reaction bounded access word).**  Let \(x_n\) realize an
> exact descriptor, fix \(\ell\), and let \(A_n\to\infty\) be the common
> source scale of its global top D-tier.  Suppose a directed physical word
> \(y_0\to y_1\to\cdots\to y_m\) has bounded length and satisfies:
>
> 1. \(y_0\) is enabled at \(x_n\);
> 2. every prescribed source along the actual-target word has propensity
>    between \(cA_n\) and \(CA_n\);
> 3. every preterminal target stays in the exact top D-tier; and
> 4. the terminal edge has factorial gap \(g_n\to\infty\) from its top source
>    to its lower target.
>
> Stop at word completion or at the first reaction not prescribed by the
> word.  Then all reactions are retained, the word succeeds with probability
> at least \(p>0\), and for every fixed \(q>0\)
>
> \[
> \begin{aligned}
>  \mathbb E\tau_n^q&=O(A_n^{-q}),\\
>  \sup_n\mathbb E[(\Delta F_\ell)^+]^q&<\infty,\\
>  \mathbb E\Delta W&\le-cG_n^3g_n
> \end{aligned}                                      \tag{3.1}
> \]
>
> for all sufficiently large \(n\).  The population displacement at the
> endpoint is bounded by a word-dependent constant.

### Proof

At each word state, the desired edge has rate at least \(cA_n\).  Because
the displayed tier is the **global** top D-tier, every physical source has
propensity at most \(CA_n\).  There are finitely many channels, so the total
all-reaction competitor rate is at most \(CA_n\).  A lower competitor with
source rate \(b_n\le CA_n\) can have positive factorial cost only of order

\[
 1+\log^+(A_n/b_n).                                   \tag{3.2}
\]

Successive exponential races therefore give a fixed success probability.
They also give the endpoint-weighted bound

\[
 \frac{b_n}{A_n}
 \left\{1+\log\frac{A_n}{b_n}\right\}^{q}\le C_q,
 \qquad 0<b_n\le A_n,                                \tag{3.3}
\]

with a harmless constant change when \(b_n/A_n\) stays in a compact range.
There are finitely many competitors and finitely many word positions, so
(3.3) proves every fixed positive endpoint moment.  The total hazard before
each stop is at least \(cA_n\), which proves the duration estimate.  Notice
that a competitor is not deleted: its physical firing is precisely an
endpoint of the stop.

On word success the exact factorial-ratio identity gives

\[
 \Delta F_\ell=-g_n+O(1).                             \tag{3.4}
\]

The fixed correction changes each bounded jump by only \(O(1)\).  Also
\(g_n\le C\log(2+\lVert x_n\rVert_1)=o(G_n)\).  On the compact part of the
success event,

\[
 (G_n-g_n+O(1))^4-G_n^4\le-cG_n^3g_n.                \tag{3.5}
\]

The complement and every failed race cost only \(O(G_n^3)\) in expectation
by (3.3), with the quadratic, cubic, and quartic terms smaller still.  Since
\(g_n\to\infty\), (3.5) dominates.  This proves (3.1).  In particular, the
statement supplies the endpoint orders \(q>8\) used by the global gluing
interface.  \(\square\)

## 4. Applying the word lemma to 937 rows

### 4.1 The 929 enabled rows

In every enabled row, a vertex of the proper top subset is physically
enabled.  Starting there, strong connectivity of that linkage supplies a
simple directed path to its complement.  Stop the path at its first target
outside the global top D-tier.  Every intermediate source is an actual
previous target; hence it is enabled, including when it needs the newly
created inactive species.  Exact D-tier equivalence makes all prescribed
source rates comparable to \(A_n\).  Lemma 3.1 applies for arbitrary strong
orientations, arbitrary positive rates, and any fixed \(\ell\).

This argument includes the four enabled rows that also display a whole-top
finite shell.  The access word takes \(O(A_n^{-1})\) physical time, so the
whole linkage is simply one of the retained top competitors; it does not
need to be averaged or deleted.

### 4.2 The eight nominal Poisson rows

These rows do not need a Poisson corrector.  Their supports, after the
displayed labelling, are

\[
 \{A,B,AC\}\quad\hbox{paired with one of}\quad
 \begin{cases}
 \{0,2C,BC\},\\
 \{0,C,2C,BC\},\\
 \{0,C,BC\},\\
 \{C,2C,BC\},
 \end{cases}                                         \tag{4.1}
\]

or the four copies obtained by exchanging \(A\) and \(B\), hence exchanging
\(AC\) and \(BC\).  The proper top intersection is the singleton \(BC\) in
the first four rows and \(AC\) in the other four.

At \(C=0\), the whole linkage has an enabled vertex \(A\) or \(B\).  Strong
connectivity gives a simple whole-linkage path to \(AC\), respectively
\(BC\), and that actual target creates \(C\).  The proper top singleton is
then enabled, and strong connectivity of the other linkage gives a path
from it to a lower target.  Concatenating the two simple paths gives the
word in Lemma 3.1.  Every source lies in the same global top D-tier.  Thus
all eight rows again work for arbitrary orientations, rates, and fixed
\(\ell\), with all reactions retained.

## 5. The six finite shells and why \(\ell\) is load-bearing

The six rank-one dormant supports are exactly

\[
 \begin{array}{c|l}
 \text{whole shell}&\text{proper linkage}\\ \hline
 \{A,B\}&\{0,C,AC,BC\}\\
 \{B,2A\}&\{0,A,C,BC\}\\
 \{B,2A\}&\{0,A,AC,BC\}\\
 \{B,2A\}&\{0,C,AC,BC\}\\
 \{B,2A\}&\{A,C,AC,BC\}\\
 \{B,2A\}&\{0,A,C,AC,BC\}.
 \end{array}                                         \tag{5.1}
\]

Use the rate-adjusted \(F_\ell\) from (2.2).  The earlier dormant-priority
theorem was stated for supports containing \(2C\), whereas none of the six
supports in (5.1) contains that vertex.  The following explicit cut lemma
is the needed extension.

On the \(\{A,B\}\) shell, reflected debt is at most one.  Before service,
the dominant reset graph is contained in \(\{0,AC,BC\}\); the remaining
proper vertex \(C\) is a service vertex.  A closed service-free reset class
would therefore be a proper closed subset of
\(\{0,C,AC,BC\}\), contradicting strong connectivity.

On the \(\{B,2A\}\) shell, reflected debt is at most two.  Whenever
\(C>0\), the unique \(BC\) top source has priority.  Every neutral dominant
reset component is contained in \(\{0,A,BC\}\), while each of the five
displayed proper supports contains \(C\) or \(AC\) outside that set.  If a
dominant reset component had no service exit, it would again project to a
proper closed subset of the strongly connected proper linkage.  Thus a cut
edge leaves it.  All choices from its source have the same source scale, so
the exit has a fixed positive conditional probability.  Lower-priority
clocks are retained as stopping interruptions.  Internal equal-scale
\(AC\leftrightarrow BC\) moves, when present, have a geometric count because
the aggregate exit rate is comparable to their total rate.

This proves, for arbitrary strong orientations and positive rates, that
after a fixed number \(K\) of retained physical macrotransitions,

\[
 \mathbb E\Delta H_w\le-\delta,
 \qquad |\Delta H_w|\le C_K.                          \tag{5.2}
\]

Lemma 2.1 gives uniformly bounded positive \(F_\ell\)-endpoint moments of
every fixed order at the independent zero-source waits and the killed
priority windows.  Let \(Y_n\ge0\) be the
sum of those positive shell costs.  For every fixed \(q\),

\[
 \sup_n\mathbb E Y_n^q<\infty,
 \qquad
 \Delta F_\ell\le \Delta H_w\log N_n+C+Y_n.           \tag{5.3}
\]

The right side of (5.3), call it \(Z_n\), is an upper endpoint surrogate,
has \(\mathbb EZ_n\le-\delta\log N_n+O(1)\), and has
\(q\)-moments \(O(\log^qN_n)\).  Monotonicity of \(u\mapsto u^4\) and the
exact binomial identity give

\[
\begin{split}
 \mathbb E\Delta W
 &\le4G_n^3\mathbb EZ_n
   +6G_n^2\mathbb EZ_n^2
   +4G_n\mathbb E|Z_n|^3+\mathbb EZ_n^4\\
 &\le-cG_n^3\log N_n,                                \tag{5.4}
\end{split}

because \(\log N_n=o(G_n)\).  The physical duration has every fixed
moment; the inactive endpoint is bounded by \(K\), and the scaled active
endpoint has every fixed moment.  Thus (5.4) has the required \(q>8\)
endpoint version and retains the whole-shell motion throughout.

### 5.1 Exact counterexample to arbitrary \(\ell\)

Consider the first row of (5.1).  Orient the whole shell reversibly with

\[
 A\mathop{\longrightarrow}^{2}B,
 \qquad B\mathop{\longrightarrow}^{1}A,              \tag{5.5}
\]

and orient the proper linkage as the unit-rate directed cycle

\[
 0\longrightarrow AC\longrightarrow C
  \longrightarrow BC\longrightarrow0.               \tag{5.6}
\]

Start from \((A,B,C)=(N,N,0)\), and take the uncorrected choice \(\ell=0\).
Let \(T\sim\operatorname{Exp}(1)\) be the first \(0\to AC\) clock.  It is
independent of the whole-shell chain.  Since total mass \(A+B=2N\),

\[
 \mathbb E B_t=\frac{4N}{3}-\frac{N}{3}e^{-3t},
 \qquad
 \mathbb E B_T=\frac{5N}{4}.                         \tag{5.7}
\]

On \(1\le T\le2\), particle independence and a Chernoff bound imply
\(B_T\ge1.25N\) with probability \(1-e^{-cN}\).  Convexity and Stirling's
formula then give

\[
 \log(A_T!)+\log(B_T!)-2\log(N!)
 \ge c_0N-O(\log N),                                 \tag{5.8}
\]

where one may take any

\[
 c_0<0.75\log0.75+1.25\log1.25.
\]

After activation, two consecutive \(AC\to C\) firings have probability
bounded below independently of \(N\); the second is surplus service.  They
take \(O(N^{-1})\) time and change the factorial potential by only
\(O(\log N)\).  Hence the positive \(\Theta(N)\) shell cost in (5.8)
overwhelms the \(-\Theta(\log N)\) service reward, and its fourth-power cost
is larger by the same leading \(G^3\) factor.

The required correction here is

\[
 \ell_B-\ell_A=-\log2,                               \tag{5.9}
\]

which centers the factorial-linear potential at the actual shell balance.
Thus “arbitrary common \(\ell\)” is false for the finite-six block.  This is
an exact rate/orientation obstruction, not a numerical simulation and not a
counterexample to recurrence with the rate-adjusted potential.

## 6. The one-active structural extension on all 416 pairs

The 416 pairs have 1,455 one-active failed incidences.  Their exact
classification under the existing graph-theorem predicates is

| structural family | incidences | pair union |
|---|---:|---:|
| direct physical \(C\)-source | 1,356 | 415 |
| Family I | 65 | 13 |
| exact Family II | 0 | 0 |
| Family III | 10 | 10 |
| open whole-top phase | 24 | 8 |
| generalized Family II | 0 | 0 |

The pair-union fingerprints, in table order after the direct row, are

```text
direct:       f0ca0f316e4796aef91c46c68bc24e780c808890ac8eb631c023739e4b8d5943
Family I:     e9cd9bdfdc6032dca816b851a83c9dcb46dc31365e2b229b5c6ba0efa5f0564d
Family III:   12cd9a7ca2abcc3508e691b7730d22ff2993e6516061ca588b0a74d39b131ecc
open whole:   a1c3277feba8d795479840d300772a9031d2ae5e616d4c19369bb25073807ae0
empty set:    4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
```

More finely, all 65 Family I rows are `family_i_origin_down_0`; the Family
III split is six `origin_down_0` plus four `origin_down_1`; and all 24 open
rows are `open_wholly_top_down_1`.  Every existing predicate ran without an
assertion failure.  There are 736 distinct normalized support/cap/phase
profiles.

This is not exact-signature reuse: none of the 1,455 normalized
support/cap signatures is literally one of the previously frozen 1,227-pair
selector signatures.  The extension is structural.  The proof of the
one-active fourth-power theorem uses only the following predicate-level
facts:

1. a direct mixed \(C\)-source has resistance-zero physical access;
2. Family I has one lower-only and one two-cofactor mixed phase, with the
   certified origin-service cut;
3. Family III has two singleton mixed phases and down resistance at most two
   strictly below same-base up resistance; and
4. the open whole-top row is the same immigration-death phase with its
   factorial maximum tail.

The finite classification checks exactly those facts here.  Extra lower
vertices are retained as interruptions; the compensation estimate uses
\(r\{1+\log(1/r)\}^q\), so it is insensitive to adding finitely many such
channels.  The moving-cutoff endpoint estimate and the ordered
three-interruption bound therefore give every moment \(q>8\), for the same
fixed \(\ell\) selected in Section 2.  No generalized Family II spectator
axis occurs.  Consequently all 416 pairs—not merely a proper subset—are the
immediate structural composition target.

Independent replay checked that this predicate-level extension uses no
selector-specific finite-box hypothesis.

## 7. Powering the other two-active rank-one episodes

Of the 416 pairs, 377 have failures in active dimensions \(\{1,2\}\) only.
The other 39 have profiles \(\{1,2,3\}\).  On those 39 pairs there are 117
additional two-active closed-rank-one rows: 115 have an enabled maximal
lower source and two use lower-layer activation.  Every pair contributes
three rows.

The already audited corrected-factorial endpoint theorem gives, for a
direct row,

\[
 \Delta F_\ell\le-I_ng_n+Y_n,
 \qquad \mathbb P(I_n=1)\ge p>0,
 \qquad g_n\to\infty,                                \tag{7.1}
\]

where \(Y_n^+\) has uniformly bounded moments of every fixed order.  This
is now an explicit consequence of Lemma 2.1 on the homogeneous and
\(\{B,2A\}\) shells, the exponential cofactor bound in the exceptional
template, and

\[
 r\{1+\log(1/r)\}^q\longrightarrow0                 \tag{7.2}
\]

for every submaximal interruption.  Thus (7.1) is stronger than a bare
first-moment statement.  Since \(g_n=O(\log R_n)=o(G_n)\), the same binomial
calculation as Lemma 3.1 gives

\[
 \mathbb E\Delta W\le-cG_n^3g_n.                     \tag{7.3}
\]

The two lower-activation rows have top
\(\{2A,A+B,2B\}\).  Their existing reflected-debt endpoint has
\(\mathbb E\Delta H_w\le-\delta\), bounded debt, and every fixed positive
shell-endpoint moment by Lemma 2.1.  Equations (5.3)--(5.4) apply verbatim and give
\(-cG^3\log N\).  Therefore all 117 closed-rank-one rows have the powered
physical-time endpoint estimate with the same correction used in the
all-active phase.

The load-bearing point in this section is the positive \(q\)-moment
strengthening, not merely \(\mathbb E\Delta F_\ell\to-\infty\); Lemma 2.1
and the independent replay certify that strengthening.

## 8. The 117 all-active rows

Exactly the same 39 pairs have all-active failures, again three per pair.
The exact split is

| fixed whole-top shape | incidences | pairs |
|---|---:|---:|
| curvature-safe reversible two-node rank one | 69 | 23 |
| arbitrary directed triple \(\{2X,X+Y,2Y\}\) | 48 | 16 |

Every two-node row satisfies the discrete curvature-cofactor premise.  The
audited reversible decomposition and fourth-power proof from the exact-26
theorem therefore applies without change: its proof is premise-based, not
selector-specific.

It remains to record the directed-triple power estimate.  Write
\(N=X+Y\) on the flat top and let \(\beta_n\) be the maximal propensity in
the other linkage.  The audited directed-triple theorem gives a fixed
rate-dependent correction such that

\[
 \mathcal L_TF_\ell\le KN,
 \qquad
 \mathcal L_RF_\ell\le-\beta_na_n,
 \qquad
 \beta_n\ge cN,
 \qquad a_n\to\infty.                                \tag{8.1}
\]

Flatness gives \(X\asymp Y\), so every top jump has
\(|\Delta_TF_\ell|=O(1)\), even though the total top rate is \(O(N^2)\).
Every other reaction has \(|\Delta_RF_\ell|\le C\log R_n\).  Hence, for
\(k=2,3,4\),

\[
 M_{k,n}:=\sum_r\lambda_r|\Delta_rF_\ell|^k
 \le C\{N^2+\beta_n(1+\log^kR_n)\}.                  \tag{8.2}
\]

After absorbing \(KN\) into \(-\beta_na_n\), substitute (8.1)--(8.2) into

\[
 \mathcal LW
 =4G^3\mathcal LF_\ell+6G^2M_2
   +4G\sum_r\lambda_r(\Delta_rF_\ell)^3+M_4.         \tag{8.3}
\]

The lower-linkage remainder divided by the leading negative term is at
most \(C(1+\log^2R_n)/(G_na_n)\to0\).  The largest top remainder has ratio

\[
 \frac{N^2}{G_n\beta_na_n}
 \le\frac{C}{a_n\log(N+1)}\longrightarrow0,          \tag{8.4}
\]

because \(G_n\ge cN\log(N+1)\).  The cubic and quartic ratios are smaller.
Thus

\[
 \mathcal LW(x_n)\le-cG_n^3\beta_na_n\to-\infty.    \tag{8.5}
\]

This closes the directed-triple carré seam; the independent audit replayed
the ratio in (8.4).

## 9. The 416-pair composition theorem

> **Theorem 9.1.**  Choose any one of
> the 416 support pairs, give both linkages arbitrary strongly connected
> orientations and arbitrary positive rates, and choose \(\ell\) from the
> exact menu in Section 2.  Then the common potential \(W=(1+F_\ell)^4\)
> supplies a physical-time Foster episode outside a finite set in every
> closed irreducible class.  Consequently every such class is positive
> recurrent.

The proof is the following finite composition:

1. all 1,455 one-active failures use Section 6;
2. the 762 promotion failures on the selector use Sections 3--5;
3. the additional 117 closed-rank-one two-active failures use Section 7;
4. the 117 all-active failures use Section 8; and
5. every passing descriptor uses the standard powered descending-source
   generator estimate with the same fixed \(W\).

All stopped episodes retain every reaction and include physical duration.
Their endpoints have moments above order eight.  Here is the fixed-class
gluing argument, including the moving-boundary case rather than importing
it from the earlier 1,227-pair selector.

Fix a closed irreducible class \(\Gamma\), a reference population
\(x^\circ\in\Gamma\), and mark all three species with reflected debts
\[
 D_i^+=(D_i+\Delta_i)^+ .                            \tag{9.1}
\]
Then \(X_i-D_i\) is pathwise nonincreasing and is at most
\(x_i^\circ\).  In a fixed-width one-active tube, a state with selected
debt \(D_X=0\) therefore has \(X\le x_X^\circ\); the two inactive
coordinates and all their marks are tube-bounded.  These states form a
finite class-dependent exception.  Every divergent reachable one-active
tube sequence consequently has \(D_X>0\) and uses the Section 6 episode.

That episode already includes in its expected \(W\)-increment the jump
which reaches its moving boundary.  If the endpoint is an at-least-two-active
**passing** state, the usual generator-good rule applies next.  If it is a
two-active **failed** state, no uncharged continuation is inferred: at the
next macrostep it uses one of the 762 promotion episodes or one of the 117
closed-rank-one episodes.  An all-active failed endpoint uses Section 8.
Thus the union of the one- and two-active bad
sets is closed under the stopping rule without deleting a reaction or
discarding an endpoint cost.

For completeness, suppose the required generator/episode alternatives did
not hold outside a finite subset of the reachable marked class.  Choose a
divergent countersequence and extract a fixed exact-tier descriptor, fixed
tube widths, and fixed invariant caps.  An affine-infeasible descriptor
cannot occur.  A descriptor which passes for the actual orientation is
generator-good for the common \(W\).  A remaining one-active failure is
covered by Section 6; a remaining two-active failure is in Sections 3--5
or 7; and an all-active failure is in Section 8.  The corresponding local
estimate has constants depending only on the fixed class, rates,
orientation, and template, and contradicts the selected countersequence.
This is the standard bad-sequence finite-exception lemma, now applied to
the complete mixed-profile list rather than to the old one-active list.

The all-species marked common-potential theorem therefore gives finite mean
hitting of a finite marked target.  One ordinary physical jump from that
finite target, followed by the same estimate from its finitely many
successors, gives finite mean positive return.  Projecting the target and
using irreducibility yields positive recurrence of \(\Gamma\).

Binary mass action is nonexplosive because every
population-increasing reaction has source molecularity at most one; its
positive total-population drift is bounded by \(C(1+|x|)\).  Finite mean
return and local finiteness then imply positive recurrence.

The independent audit replayed:

1. the all-competitor race moment in Lemma 3.1 for all 937 access rows;
2. the exponential shell-overshoot calculation in Lemma 2.1;
3. the six-support priority cut in Section 5;
4. the predicate-only one-active extension in Section 6;
5. the powered closed-rank-one endpoint in Section 7;
6. the directed-triple top-carré ratio (8.4); and
7. the marked fixed-class gluing argument in Section 9.

All seven obligations passed.  The 416 pairs contain 414 positive-invariant
and two signed members and have zero overlap with the previously certified
set.  Thus the ordered certified remainder changes by

\[
 (733,36)\longmapsto(319,34).                        \tag{9.2}
\]

The resulting 353-pair fingerprint is

```text
9868f965cc8af951fd7545f8832ed0275a8d60bab70b2593b7424654cba7d8ec
```

## 10. The separated hard 407

Nothing in this note treats the 407 dormant promotion rows with no whole
top linkage.  They lie on 333 pairs and have row/pair split disjoint from
the easy mechanism.  Every such row has one proper linkage whose global-top
intersection is exactly one complex of the form inactive-plus-active,
while the other linkage is disjoint from the global top.  Their normalized
workload profiles are

\[
 (1,3)\ (333\text{ rows}),\qquad
 (1,2)\ (37\text{ rows}),\qquad
 (4,5)\ (37\text{ rows}).                            \tag{10.1}
\]

The bounded priority-word regression passes all 407 rows, but that finite
search is not an arbitrary-rate/orientation analytic proof.  These rows
remain the separate dormant-resolvent problem and are not silently included
in Candidate Theorem 9.1.

## 11. Reproduction and frozen hashes

Run

```text
PYTHONPATH=src python3 -B src/two_active_easy_common_w.py
PYTHONPATH=src python3 -B -m unittest tests/test_two_active_easy_common_w.py -v
```

The canonical incidence hashes are

```text
all promotion rows:       e03857257080c80b0426c400f45781f6e291634ee32ab2757f46564bfab41e86
easy 943:                 d7cace7ff05356f6fd899ee622b6718413643d00b4da87ec61cf29941224a20a
hard 407:                 ddd4c217b0236d7a44aa684873e6f6a9d5356c6741dea0d8575703e6263b7567
promotion rows on 416:    318a861e2fae514680a1e42cfc74e5e2cdfa3d2f6cc8b5d3b117b51352f09333
one-active classified:    d835320fd024e14d2e3a3198b4546d7bd83889fa23ffb7d1238ca91ffd7534f9
one-active profiles:      3652ab6d5d7e660fffbfbee85ac48d440411f604bc39b534e6ed0c7f3c0ea55c
closed rank-one rows:     515ed4fbf3603d2c3489b73c7d9f26dd23ad160d5ec6bc48589f697c24a76124
all-active rows:          658010646b5ac720a9acc1fbf14fd08691620df7698042d9e0c9af7370a9c2a7
certificate payload:      40547e6856855ce5b128cf944a4e81aa44e1db77a35e29ea1d099e8b26ca3097
```

The certificate ends with the scoped certification boundary

```text
independent_audit_passed = true
analytic_easy_943_common_w_certified = true
analytic_one_active_structural_extension_certified = true
analytic_closed_rank_one_power_lift_certified = true
analytic_directed_triple_power_lift_certified = true
exact_416_pair_recurrence_certified = true
global_t3_2_certified = false
```
