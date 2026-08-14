# One-root Kac event formulas and the scalar likelihood obstruction

Date: 2026-08-13 (America/Los_Angeles)

No graph enumeration, kernel optimization, literature search, or external
communication was used.

## 1. Status and scope

**EXACT CYCLE FORMULAS AND AN ACTIVE PHYSICAL PROOF-ROUTE OBSTRUCTION.**
For a singleton root `i`, the diagonal part of the minimal-product target is

\[
 r^3\psi_{B,i}\psi_{D,i}\leq 1,                    \tag{D-KAC}
\]

on the active branch, where

\[
 \psi_{U,i}=q_{U,i}\,\mathbb E_i\int_0^{\tau_i^+}
 \left\{\frac{|A_t|}{s}-\frac{r-1}{r}\right\}dt.  \tag{1}
\]

This note does **not** prove or refute `(D-KAC)`.  It does two narrower
things.

1. It derives exact event-epoch and first-departure formulas for both Kac
   rewards.  These formulas retain the signed low-rank/high-rank
   cancellation.
2. It closes the canonical scalar likelihood-ratio optional-stopping route.
   The unmarked cycle laws are singular.  On the natural target-locked
   source-history expansion, the likelihood ratio is not square integrable
   on an exact weighted three-path for which both stationary excesses are
   strictly positive throughout

   \[
                    \frac32\leq r\leq\frac{151}{100}. \tag{2}
   \]

   Scalar Hellinger retains a finite half-moment, but its exact remainder is
   indefinite for the signed cycle reward and, for a nonnegative reward,
   points in the lower-bound direction rather than the upper-bound direction
   required by `(D-KAC)`.

The obstruction is deliberately scoped.  It rules out a positive scalar
Radon--Nikodym/Hölder/Hellinger proof based on the unmarked cycle, an
endpoint or rank coboundary, or the canonical target-locked expansion.  It
does not rule out a signed full product-chain Poisson certificate, a marked
matrix-valued transport, or a global forest identity.

The algebraic endpoint `R_hyb` lies strictly inside (2), so the obstruction
is active at the fitness of interest.

## 2. The two exact event-epoch formulas

Let `H=(V,w)` be a finite connected loopless undirected weighted graph of
order `s`.  Put

\[
 d_v=\sum_uw_{vu},\qquad P_{vu}=\frac{w_{vu}}{d_v},
 \qquad t_v=\sum_uP_{uv},                            \tag{3}
\]

and, for a nonempty set `A`, put

\[
 T(A)=\sum_{v\in A}t_v,\qquad
 g(A)=\frac{|A|}{s}-p,\qquad p=\frac{r-1}{r}.       \tag{4}
\]

### 2.1 Bd graphical attempts

For every occupied target `v in A` and source `u`, a neutral graphical
arrow of rate `P_uv` sends

\[
 A\longmapsto(A\setminus\{v\})\cup\{u\},           \tag{5}
\]

and a selective arrow of rate `(r-1)P_uv` sends

\[
 A\longmapsto A\cup\{u\}.                           \tag{6}
\]

Include null selective attempts in the event chain.  Its attempt rate at
`A` is exactly `rT(A)`.  Start at `{i}` and let

\[
 X_0=\{i\},X_1,\ldots,X_{N_i}=\{i\}                \tag{7}
\]

be the marked-attempt states through the first return after the initial
departure.  Looplessness makes every first attempt at `{i}` a genuine
departure, and

\[
                         q_{B,i}=rt_i.               \tag{8}
\]

Conditional on `X_n=A`, the holding time before the next attempt has mean
`1/[rT(A)]`.  Tonelli applied separately to the positive and negative
parts, both integrable on a finite recurrent chain, gives the exact signed
identity

\[
 \boxed{
 \psi_{B,i}
 =t_i\,\mathbb E_i\sum_{n=0}^{N_i-1}\frac{g(X_n)}{T(X_n)}
 =\frac{t_i}{s}\,\mathbb E_i\sum_{n=0}^{N_i-1}
   \frac{|X_n|-sp}{T(X_n)}.}                         \tag{9}
\]

Null attempts do not alter the continuous-time cycle; they only express
its holding time by an exact geometric subdivision.

### 2.2 dB burst events

For dB, every occupied target rings at rate one.  It is removed and
replaced by the union of

\[
 K\sim\operatorname{Geom}(1/r),\qquad
 \Pr(K=n)=\frac1r\left(\frac{r-1}{r}\right)^{n-1}, \tag{10}
\]

iid samples from row `P_v`.  A loopless target cannot be resampled, so
every event changes the set.  The exit rate at `A` is `|A|`; in particular,

\[
                         q_{D,i}=1.                  \tag{11}
\]

For the event states

\[
 Y_0=\{i\},Y_1,\ldots,Y_{M_i}=\{i\},               \tag{12}
\]

the same holding-time conditioning gives

\[
 \boxed{
 \psi_{D,i}
 =\mathbb E_i\sum_{n=0}^{M_i-1}\frac{g(Y_n)}{|Y_n|}
 =\frac1s\,\mathbb E_i\sum_{n=0}^{M_i-1}
   \frac{|Y_n|-sp}{|Y_n|}.}                         \tag{13}
\]

Equations (9) and (13) show the exact clock mismatch that a paired
event-epoch proof must retain: Bd is normalized by the reversed-column
activity `T(A)`, whereas dB is normalized by the rank `|A|`.

### 2.3 First-departure form

Let

\[
 \mathcal H_U^i(A)=\mathbb E_A\int_0^{\tau_i}g(A_t)dt \tag{14}
\]

be the killed reward until first hitting `{i}`.  At the Bd root, the first
neutral and selective destinations have rates `P_ui` and `(r-1)P_ui`.
At the dB root, let `Gamma_i(B)` be the probability that the geometric
row-`P_i` sample union is exactly the nonempty set
`B subseteq V\setminus{i}`.  Then

\[
 \boxed{
 \psi_{B,i}=g(\{i\})+\sum_uP_{ui}
 \left\{\mathcal H_B^i(\{u\})
 +(r-1)\mathcal H_B^i(\{i,u\})\right\},}            \tag{15}
\]

\[
 \boxed{
 \psi_{D,i}=g(\{i\})+
 \sum_{\varnothing\ne B\subseteq V\setminus\{i\}}
       \Gamma_i(B)\mathcal H_D^i(B).}               \tag{16}
\]

These are the singleton Schur formulas written as honest first-departure
renewals.  No positive part has been taken.

## 3. An active weighted-three-path witness

Consider the weighted path

\[
                  u\mathbin{-}^{1}v\mathbin{-}^{17}w \tag{17}
\]

and root cycles at the centre `v`.  Scaling all weights is immaterial.
Exact solution of the two six-state fixation chains, followed by reciprocal
fitness/type complementation, gives the two stationary density excesses

\[
 \beta_B=\rho_{Bd}-p=\frac{N_B(r)}
 {3r(r+2)(18r^2+17r+306)(306r^2+17r+18)},           \tag{18}
\]

\[
 \begin{split}
 N_B(r)={}&-155450r^4-77725r^3+532446r^2\\
          &\quad+16524r+33048,
 \end{split}                                        \tag{19}
\]

and

\[
 \beta_D=\rho_{dB}-p=\frac{N_D(r)}
 {9r(r+17)(17r+1)},                                  \tag{20}
\]

\[
 N_D(r)=-68r^3-1587r^2+2474r+153.                  \tag{21}
\]

Both are strictly positive throughout (2).  A short exact sign proof is as
follows.  After `r=3/2+x`, every coefficient of `N_B'(r)` and `N_D'(r)` is
strictly negative for `x>=0`; hence both numerators decrease on (2).  At
the upper endpoint,

\[
 N_B(151/100)=\frac{392527662741}{2000000}>0,
 \qquad
 N_D(151/100)=\frac{4512579}{125000}>0.              \tag{22}
\]

For orientation, at the lower endpoint the actual excesses are

\[
 \beta_B(3/2)=\frac{1275}{26474},\qquad
 \beta_D(3/2)=\frac{170}{17649}.                    \tag{23}
\]

The recurrent singleton atoms are positive, so the Kac identities
`beta_U=pi_U({i})psi_U,i` imply

\[
                  \psi_{B,v}>0,\qquad\psi_{D,v}>0  \tag{24}
\]

throughout (2).  The likelihood obstruction below therefore occurs on the
active physical branch; it is not produced by a zero positive-part target.

## 4. The unmarked macro-cycle laws are singular

Write

\[
                   g_r(z)=\frac{z}{r-(r-1)z}.       \tag{25}
\]

At its first dB event, `{v}` is replaced by both leaves with probability

\[
 \chi_r(1/18)=1-g_r(1/18)-g_r(17/18)>0.             \tag{26}
\]

A single Bd arrow from `{v}` can land only at a leaf singleton or at a
doubleton containing `v`; it cannot land at `{u,w}`.  Hence a positive
dB-cycle cylinder has zero Bd macro-cycle mass.  There is no scalar
Radon--Nikodym derivative between the unmarked return-cycle laws.

This is a support obstruction, not a poor likelihood estimate.

## 5. The canonical marked likelihood is not in `L^2`

The standard repair expands a burst into a target-locked source history.
For a retained target `v`, the outgoing dB source law `C_v` and the
Bd-oriented reversed-column source law `L_v` are

\[
 C_v(x)=\frac{w_{xv}}{d_v},\qquad
 L_v(x)=\frac{w_{xv}/d_x}{t_v}.                     \tag{27}
\]

Put `c_v=d_v/t_v`.  For a history of `n` sources
`x_1,...,x_n`, the common geometric factor cancels and the exact likelihood
ratio is

\[
 \boxed{
 \Lambda(x_1,\ldots,x_n)
 =\prod_{k=1}^n\frac{L_v(x_k)}{C_v(x_k)}
 =\frac{c_v^n}{\prod_{k=1}^nd_{x_k}}.}              \tag{28}
\]

This also gives a general moment test.  If one fixed source has

\[
                        z=C_v(x),\qquad \ell=L_v(x), \tag{29}
\]

then the histories with `K=n` and every source equal to `x` contribute

\[
 \boxed{
 \sum_{n\ge1}\Pr_C(K=n,x_1=\cdots=x_n=x)\Lambda^q
 =\frac{\ell^qz^{1-q}}{r}
  \sum_{n\ge1}
  \left\{\frac{r-1}{r}\ell^qz^{1-q}\right\}^{n-1}.} \tag{30}
\]

Thus the `q`-moment diverges whenever the displayed geometric ratio is at
least one.

On (17), at the centre target,

\[
 C_v=(1/18,17/18),\qquad L_v=(1/2,1/2).             \tag{31}
\]

For the weak source, `z=1/18`, `ell=1/2`, and

\[
 \begin{split}
 \mathbb E_C\Lambda^2
 &\geq\sum_{n\ge1}\frac1r
   \left(\frac{r-1}{r}\right)^{n-1}
   \left(\frac1{18}\right)^n9^{2n}\\
 &=\frac9{2r}\sum_{n\ge1}
   \left\{\frac{9(r-1)}{2r}\right\}^{n-1}
 =+\infty                                             \tag{32}
 \end{split}
\]

throughout (2), because the ratio is already `3/2` at `r=3/2` and increases
with `r`.

Append the deterministic-source leaf-to-centre return event.  Its source
likelihood is one, so (32) persists on closed expanded root histories.  All
histories in (32) have the same projected macrocycle

\[
                         \{v\}\to\{u\}\to\{v\},    \tag{33}
\]

and the hidden draws are instantaneous.  Their physical holding-time
reward does not record `n`, while their likelihood is `9^n`.  Therefore the
defect cannot be represented by a root endpoint, projected-set, rank, or
physical-reward coboundary.  In particular, the direct reference-space
`L^2`/Cauchy or chi-square likelihood estimate is genuinely infinite on an
active module.

## 6. Signed Hellinger has an indefinite exact remainder

Let `C` and `L` now be any two common-support probability laws, let
`Lambda=dL/dC`, and let `Z` be an integrable signed reward for which the
displayed quantities are finite.  Two independent `C`-histories give the
identity

\[
 \boxed{
 \begin{split}
 &(\mathbb E_C[\Lambda Z])(\mathbb E_C Z)
       -(\mathbb E_C[\sqrt\Lambda Z])^2\\
 &\quad=\frac12\mathbb E_{C\otimes C}
 \left[Z(\omega)Z(\eta)
   \{\sqrt{\Lambda(\omega)}-\sqrt{\Lambda(\eta)}\}^2\right].
 \end{split}}                                        \tag{34}
\]

For `Z>=0`, (34) says that scalar Hellinger is a **lower** bound on the
product of the two reward means.  That is the opposite direction from a
direct proof of `(D-KAC)`.  For signed `Z`, the right side has no sign, even
when both means on the first line are positive.

The physical Kac reward is genuinely signed on (17) at every
`3/2<r<=151/100`.  On an order-three module,

\[
 g(\text{singleton})=\frac{3-2r}{3r}<0,
 \qquad
 g(\text{doubleton})=\frac{3-r}{3r}>0.              \tag{35}
\]

Both duals have a positive-probability singleton-only return cycle, hence a
negative reward.  Bd has a positive-probability selective jump to a
doubleton, and dB has the positive burst event (26); restricting singleton
holds to be short and the doubleton hold to be long gives a positive reward
with positive probability for each rule.  Equation (24) says that the two
signed means are nevertheless positive.

Thus neither active-branch positivity nor the finite Hellinger half-moment
turns the cycle reward into a positive measure.  Taking its positive part or
total variation deletes the cancellation in (9), (13), (15), and (16).

## 7. The signed product-chain route remains open

It is useful to state exactly what the obstruction does not close.  Let
`Q_B,Q_D` be the two recurrent dual generators, with stationary laws
`pi_B,pi_D`, singleton atoms `u_i,v_i`, and means
`beta_B=pi_B g`, `beta_D=pi_D g`.  On the product state space put

\[
 \mathcal L=Q_B\otimes I+I\otimes Q_D             \tag{36}
\]

and

\[
 h_i(A,D)=r^{-3}\mathbf1_{\{A=\{i\},D=\{i\}\}}
              -g(A)g(D).                            \tag{37}
\]

Then

\[
 (\pi_B\otimes\pi_D)h_i
 =r^{-3}u_iv_i-\beta_B\beta_D.                      \tag{38}
\]

On the active branch, `(D-KAC)` is exactly nonnegativity of (38).  A
pointwise signed Poisson certificate

\[
                         h_i+\mathcal L\Phi_i\geq0  \tag{39}
\]

would prove it.  Conversely, for a fixed physical module, if (38) is
nonnegative then the finite irreducible Poisson equation can choose
`Phi_i` so that the left side of (39) is the constant (38).  Thus allowing
an arbitrary full product-state signed potential makes (39) equivalent to
the target, rather than obstructed by this note.

The remaining proof-first obligation is therefore a **universal explicit**
signed product-chain, marked-matrix, or forest certificate.  A scalar
positive likelihood comparison cannot supply it through the canonical
cycle representations above.

## 8. Exact replay

From the repository root run

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B \
  universal_simultaneous_amplification/phase5_exact_threshold/\
rhyb_one_root_kac_likelihood_obstruction/\
verify_one_root_kac_likelihood.py
```

The replay derives the weighted-three-path fixation data from the two exact
six-state absorbing chains, checks (18)--(23), proves the interval signs in
exact rational arithmetic, verifies the geometric-union singular mass, the
general likelihood-moment ratio and active `L^2` divergence, and the signed
Hellinger identity with both signs.  It performs no graph enumeration or
kernel search.
