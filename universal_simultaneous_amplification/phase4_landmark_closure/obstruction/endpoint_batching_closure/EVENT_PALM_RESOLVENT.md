# Event--Palm closure of the endpoint batching comparison

Date: 2026-08-08 (America/Los_Angeles)

No literature search or external communication was used.

## 1. Status

At fitness $r=3/2$, let $C$ be the unbatched reversed-arrow dual and
$D$ the locked-target geometric-burst dB dual.  Write

\[
 m_U=\mathbb E_{\pi_U}|A|,
 \qquad
 R_n={n-1\over n}{1-(2/3)^n\over1-(2/3)^{n-1}}.
\]

The desired independent batching comparison is

\[
 {m_D\over m_C}\le R_n.                                      \tag{1}
\]

This note proves an exact marked event--Palm/resolvent identity reducing
(1) to one global sign, while retaining every multi-rank jump in the
geometric burst.  It also gives exact rational graphs proving that the two
natural terms in that identity are separately indefinite.  Thus the
remaining sign must use their cancellation.

The status is:

- **PROVED:** the event kernels, Palm laws, marked resolvent factorization,
  Poisson identity, directed-arborescence formulation, and complete-graph
  equality;
- **EXACTLY FALSIFIED:** a nonnegative locked-target persistence term;
- **EXACTLY FALSIFIED:** a nonnegative neutral/selective timing term;
- **NUMERICALLY OBSERVED:** no violation of (1) in the new structured and
  hostile screens described in Section 7;
- **OPEN:** the single combined sign in (16), equivalently (1).

## 2. Four event operators

Let $\Omega$ be the nonempty subsets of $V$, and let

\[
 \widetilde\Omega=\{(A,v):A\in\Omega, v\in A\}
\]

be the target-marked state space.  Matrices below act on row distributions
from the left.  Define:

- $J:\Omega\to\widetilde\Omega$: choose $v$ uniformly from $A$;
- $H:\widetilde\Omega\to\Omega$: forget $v$;
- $S:\widetilde\Omega\to\widetilde\Omega$: sample $u\sim P_{v*}$
  and send $(A,v)$ to $(A\cup\{u\},v)$;
- $N:\widetilde\Omega\to\Omega$: sample $u\sim P_{v*}$ and send
  $(A,v)$ to $(A\setminus\{v\})\cup\{u\}$.

Thus $JH=I_\Omega$, while

\[
 \mathsf R:=HJ                                                   \tag{2}
\]

refreshes the target uniformly within the current occupied set.  Put

\[
 p={2\over3},\qquad q={1\over3}.                                 \tag{3}
\]

The number of selective arrows before the next neutral arrow has law
$p q^j$, $j\ge0$.

For $C$, the unmarked selective and neutral kernels are

\[
 S_C=JSH,\qquad N_C=JN,                                          \tag{4}
\]

and the full selective resolvent is

\[
 R_C=p(I-qS_C)^{-1}=p\sum_{j\ge0}q^jS_C^j.                       \tag{5}
\]

Observe $C$ immediately before neutral arrows.  One first applies the
neutral arrow and then sees a geometric number of selective arrows before
the next neutral arrow.  Its exact event kernel is therefore

\[
 \boxed{K_C=N_CR_C.}                                             \tag{6}
\]

The corresponding post-neutral kernel is

\[
 \boxed{K_R=R_CN_C.}                                             \tag{7}
\]

For $D$, one target is chosen at the beginning of the event, every
selective arrow remains locked to it, and the final neutral arrow uses the
same target.  Hence

\[
 \boxed{K_D=pJ(I-qS)^{-1}N.}                                    \tag{8}
\]

Equations (5)--(8) include the entire geometric series.  No truncation to
adjacent ranks or to one selective arrow is being made.

## 3. Exact Palm laws

Neutral events of $C$, and burst events of $D$, occur at total rate
$|A|$.  Their pre-event Palm laws are therefore

\[
 \alpha_U(A)={|A|\pi_U(A)\over m_U},
 \qquad
 m_U={1\over\alpha_U f},
 \qquad f(A)={1\over|A|}.                                      \tag{9}
\]

The laws satisfy

\[
 \alpha_CK_C=\alpha_C,
 \qquad
 \alpha_DK_D=\alpha_D.                                         \tag{10}
\]

Define the post-neutral $C$ law

\[
 \beta_C:=\alpha_CN_C.                                         \tag{11}
\]

Stationarity in (10) gives, exactly,

\[
 \beta_CK_R=\beta_C,
 \qquad
 \alpha_C=\beta_CR_C.                                          \tag{12}
\]

The distinction between $\alpha_C$ and $\beta_C$ matters.  Treating the
post-neutral law as the size-biased stationary law would reverse the order
of $N_C$ and $R_C$ and lose the complete-graph correction.

## 4. Locked versus refreshed targets

The push-through identity

\[
 (I-AB)^{-1}A=A(I-BA)^{-1}
\]

and (2) give

\[
 K_R=pJ(I-qS\mathsf R)^{-1}N.                                  \tag{13}
\]

Subtracting (13) from (8) and using the resolvent identity gives the exact
marked factorization

\[
\boxed{
 K_D-K_R
 =pqJ(I-qS)^{-1}S(I-\mathsf R)(I-qS\mathsf R)^{-1}N.}           \tag{14}
\]

This is the promised all-burst persistence operator.  The sole local
factor $I-\mathsf R$ is target dispersion.  Every operator around it is a
positive full geometric resolvent.

## 5. The single remaining sign

Let $g$ be the uniquely normalized $K_R$-Poisson potential

\[
 (I-K_R)g=f-(\beta_Cf)\mathbf1,
 \qquad \beta_Cg=0.                                             \tag{15}
\]

Since $\alpha_D$ is stationary for $K_D$, equations (12) and (15) give

\[
\begin{aligned}
 \mathcal G(G)
 &:={\alpha_Df}-{1\over R_n}\alpha_Cf\\
 &=\underbrace{\alpha_D(K_D-K_R)g}_{\mathcal P(G)}
   +\underbrace{\beta_C\left(f-{1\over R_n}R_Cf\right)}
                _{\mathcal T(G)}.                              \tag{16}
\end{aligned}
\]

By (9),

\[
 {m_D\over m_C}={\alpha_Cf\over\alpha_Df},
\]

so (1) is exactly equivalent to the one graph-independent sign

\[
 \boxed{\mathcal P(G)+\mathcal T(G)\ge0.}                       \tag{17}
\]

Formula (14) makes the first term in (16) explicit:

\[
 \mathcal P(G)=pq\,\alpha_DJ(I-qS)^{-1}S(I-\mathsf R)
                  (I-qS\mathsf R)^{-1}Ng.                       \tag{18}
\]

If

\[
 \ell=\alpha_DJ(I-qS)^{-1}S,
 \qquad
 \Phi=(I-qS\mathsf R)^{-1}Ng,
\]

then (18) is $pq\ell(I-\mathsf R)\Phi$.  Conditional on an unmarked set
$A$, $\mathsf R\Phi$ is the uniform average of $\Phi(A,v)$ over
$v\in A$.  Thus $\mathcal P$ is a global occupation-weighted covariance
between the locked-target Palm bias and the future Poisson value.  The term
$\mathcal T$ is the exact pre-/post-neutral timing correction.  Neither
may be discarded.

### 5.1 A classical directed-arborescence--coverage inequality

There is a positive, current-free form of the combined sign.  Let

\[
 \Omega^\circ=\Omega\setminus\{V\}.
\]

Both $K_R$ and $K_D$ restrict to irreducible stochastic kernels on
$\Omega^\circ$.  For $U\in\{R,D\}$, put $L_U=I-K_U$ on this recurrent
space and define the principal cofactor

\[
 \tau_U(A)=\det L_U^{\widehat A,\widehat A},
 \qquad
 \mathcal Z_U=\sum_{A\in\Omega^\circ}\tau_U(A).                 \tag{18a}
\]

Expanding the determinant by permutations, and cancelling permutations
that contain a directed cycle, gives the directed matrix-tree formula.
Every $\tau_U(A)$ is the positive total weight of in-arborescences rooted
at $A$, and

\[
 \beta_C(A)={\tau_R(A)\over\mathcal Z_R},
 \qquad
 \alpha_D(A)={\tau_D(A)\over\mathcal Z_D}.                       \tag{18b}
\]

Define the root likelihood and the resampled geometric-coverage cost

\[
 \zeta(A)={\mathcal Z_R\tau_D(A)
                 \over\mathcal Z_D\tau_R(A)},
 \qquad
 c(A)=(R_Cf)(A).                                                 \tag{18c}
\]

Then $\mathbb E_{\beta_C}\zeta=1$, and (17) is exactly the classical
root-likelihood covariance inequality

\[
\boxed{
 \operatorname{Cov}_{\beta_C}(\zeta,f)
 \ge {1\over R_n}\mathbb E_{\beta_C}c
       -\mathbb E_{\beta_C}f.}                                  \tag{18d}
\]

Equivalently, it is the following comparison of positive partition sums:

\[
\boxed{
 R_n\mathcal Z_R\sum_A\tau_D(A)f(A)
 \ge
 \mathcal Z_D\sum_A\tau_R(A)c(A).}                              \tag{18e}
\]

This is the precise irreducible classical inequality left by the bounded
closure cycle.  The left root law is a directed-arborescence measure, while
$c(A)$ is the expected reciprocal size after a full resampled geometric
coverage burst.  There are no signed currents in (18e), and every
multi-rank burst is retained in $K_D$ and $R_C$.

The comparison is nevertheless not rootwise.  Already on $K_4$, where
$\zeta\equiv1$, the integrand

\[
 \zeta(A)f(A)-R_4^{-1}c(A)                                     \tag{18f}
\]

equals $47/1092>0$ on a singleton and $-58/1365<0$ on a
three-set.  Its arborescence-root average is exactly zero.  Hence even at
the equality graph, (18e) cannot follow from a root-preserving termwise
injection.  A successful tree proof must transport mass between roots, or
prove (18d) as a genuine covariance inequality.

## 6. Why the two terms cannot be separated

### 6.1 Negative persistence term

On the connected weighted four-vertex graph

\[
 W_P=
 \begin{pmatrix}
 0&2&0&3\\
 2&0&1&30\\
 0&1&0&1\\
 3&30&1&0
 \end{pmatrix},                                                  \tag{19}
\]

the exact marked-chain calculation gives

\[
 \mathcal P(W_P)=
 -{1258360419250557731020595790088878547460822775
 \over
 50519340759882110603804078136843075407789088648182}<0.          \tag{20}
\]

Nevertheless

\[
 \mathcal G(W_P)
 ={33764935823332732303680844225141604836701378512191
 \over
 1970254289635402313548359047336879940903774457279098}>0.        \tag{21}
\]

Thus a universal sign for the locked-versus-refreshed term is false.

### 6.2 Negative timing term

On the connected weighted five-vertex graph

\[
 W_T=
 \begin{pmatrix}
 0&0&5&5&11\\
 0&0&7&13&1\\
 5&7&0&1&7\\
 5&13&1&0&2\\
 11&1&7&2&0
 \end{pmatrix},                                                  \tag{22}
\]

the timing term is exactly

\[
 \mathcal T(W_T)=
 -{18330460111543524961293002426757304977699514669055785529098495
 \over
 1430836065643243043514486290271161366196834807117417091134086123514}
 <0.                                                             \tag{23}
\]

Here $\mathcal P(W_T)>0$ and
$\mathcal G(W_T)>0.0057172769382$.  Hence a universal sign for the timing
term is also false.  The exact rational hash of the full positive gap is

```text
a91e439aab3ce89423793a8bf73b9497b590ae606ebe916ff616842e9ed2b8c2
```

Equations (20) and (23) show that (17), if true, is an intrinsically paired
stationary-resolvent inequality.  A proof cannot establish (1) by proving
the two most natural event contributions nonnegative one at a time.

## 7. Complete equality and hostile search

For $K_n$, put $a=1/2$.  The $C$ stationary law is proportional to
$a^{|A|}$, so its pre-neutral Palm law is proportional to
$|A|a^{|A|}$.  Applying one complete-graph neutral arrow shows directly
that

\[
 \beta_C(A)\ \propto\ |A|(n-|A|)a^{|A|}.                       \tag{24}
\]

Indeed, for a fixed $k$-set, the incoming same-rank swaps contribute a
factor $k(n-k)a^k/(n-1)$, and incoming $(k+1)$-sets contribute
$k(n-k)a^{k+1}/(n-1)$.  Their sum is (24), up to the common factor
$1+a$.

The complete $D$ stationary law is proportional to
$(n-|A|)a^{|A|}$.  Therefore

\[
 \boxed{\beta_C=\alpha_D\quad\hbox{on }K_n.}                    \tag{25}
\]

Moreover

\[
 {\alpha_Cf\over\beta_Cf}
 ={n-1\over n}{1-(2/3)^n\over1-(2/3)^{n-1}}=R_n,                \tag{26}
\]

so both sides of (17) vanish on the complete graph.

Before freezing (16), the true ratio was screened numerically on:

- the exact endpoint hostile corpus, including the seven-vertex
  dB-amplifying three-blade windmill;
- unweighted clique--pendant graphs $K_{c+1}$ with grouped pendants and
  rays reaching $1+100+1000$ vertices;
- dense three-class reversible blow-ups with class sizes through
  $(1,10,30)$, weights spanning up to forty logarithmic units;
- multi-scale weighted stars with three and four growing leaf groups.

No positive normalized excess was observed.  These are discovery screens,
not a proof of (17).  The exact sign failures (20) and (23), by contrast,
are proofs over $\mathbb Q$.

## 8. Verification

Run

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  universal_simultaneous_amplification/phase4_landmark_closure/obstruction/endpoint_batching_closure/verify_event_palm_resolvent.py
```

The verifier independently:

1. builds $J,H,S,N$ from the weighted graph;
2. checks every row sum and the identities (6)--(8);
3. solves all three invariant laws exactly over $\mathbb Q$;
4. checks (12), the Poisson equation (15), and the marked factorization
   (14);
5. computes every principal cofactor in (18a), reconstructs both tree-root
   laws, and checks both exact signs in (18f);
6. certifies the strict signs (20) and (23);
7. reconstructs the forward C and dB fixation chains directly and
   checks $\rho_U=1/(n\alpha_Uf)=m_U/n$.

No floating-point value is used for an assertion.
