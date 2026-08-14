# Soft coverage transfer: exact data-processing and mark-erasure obstruction

Date: 2026-08-13 (America/Los_Angeles)

No graph search, literature search, or external communication was used.

## 1. Result and scope

The perfect-classification premise in the locked-history note was stronger
than necessary.  A positive soft tester really can improve the projective
clean/adverse ratio on one output, even though its two classification errors
cannot both vanish.  The exact improvement, however, has an unavoidable
absolute-throughput cost.

Write `a=r-1`.  For a uniform fan-out of size `m`, let a random ancestral
tester `Z` be the union of `ell` iid uniform singleton tests.  Put

\[
 c=\Pr\{Z\hbox{ misses a fixed label}\}
   =\left(1-{1\over m}\right)^\ell .                    \tag{1}
\]

Conditional on a clean locked history, the source union is a uniform
singleton.  Conditional on an adverse history, it is the union of at least
two geometrically many iid uniform labels.  The exact conditional
clean/adverse transfer to the no-hit and hit outputs is

\[
 K_{m,\ell}=\begin{pmatrix}c&d\\1-c&1-d\end{pmatrix},
 \qquad
 d=E\,{X^2\over r-aX},\qquad X=1-{|Z|\over m}.           \tag{2}
\]

Including the prior locked-history masses `1/r` and `a/r` gives

\[
 \boxed{
 M_{m,\ell}={1\over r}
 \begin{pmatrix}c&ad\\1-c&a(1-d)\end{pmatrix}.}         \tag{3}
\]

The no-hit branch is clean-enriching, with adverse/clean ratio `ad/c`; the
hit branch is adverse-enriching, with ratio `a(1-d)/(1-c)`.  Convexity gives
the sharp distribution-free inequalities

\[
 \boxed{
 {d\over c}\ge {c\over r-ac}\ge c^r,}                  \tag{4}
\]

and the geometric-union collision law gives the independent floor

\[
 \boxed{{ad\over c}\ge {a\over rm-a}.}                  \tag{5}
\]

Thus, in the optimistic relaxation where one persistent hidden label is
retained through a cascade of no-hit observations, if

\[
 C=\prod_i c_i
 \quad\hbox{and}\quad
 \Delta=\prod_i{d_i\over c_i},                           \tag{6}
\]

are respectively the absolute clean throughput relative to the labelled
clean history and the additional projective retention, then

\[
                         \boxed{\Delta\ge C^r.}           \tag{7}
\]

This inequality is asymptotically sharp.  Exponentially strong *additional*
projective discrimination forces exponentially small absolute throughput.
Positive parallel multiplicity cannot repair that ratio: restoring the clean
signal by a factor `1/C` costs at least the same common coefficient.  Section
6 proves that an ordinary one-output reset does not even retain the hidden
label assumed in this optimistic calculation.

There is a second, physical sign obstruction.  The only clean-enriching
output is the no-hit function

\[
 g(B)=\Pr(Z\cap B=\varnothing)=1-h(B),                   \tag{8}
\]

where `h` is a normalized coverage harmonic.  Hence `g(\varnothing)=1`: it is
the affine complement (resident output), not a positive mutant hitting or
fixation harmonic.  A coefficient `w` carries unmatched baseline `w`.  A
depth-`n` clean one-sample process has no-hit signal `wC`; the formal all-F
cylinder inside the full geometric process has mass `w r^{-n}C`.  Thus

\[
 \boxed{
 {\text{baseline}\over\text{clean-process signal}}={1\over C},
 \qquad
 {\text{baseline}\over\text{all-F cylinder}}={r^n\over C}.} \tag{9}
\]

Replication and uniform dilution multiply numerator and denominator by the
same factor.  This closes the clean-enriching **complement** route unless a
signed common control cancels its baseline.

The decisive composable quantities are not the posterior ratios `ad/c` and
`a(1-d)/(1-c)`.  The clean event and adverse event are resampled latent
subevents inside each full geometric batch.  If a retained output has clean
and adverse conditional probabilities `u,v`, then the clean one-sample law
succeeds with probability `u`, while the full batch succeeds with

\[
                         s={u+av\over r}.                 \tag{10a}
\]

Their physical full/clean ratio is therefore

\[
                         \chi={s\over u}
                         ={1+av/u\over r}.               \tag{10b}
\]

For hit, `u=1-c` and `v=1-d>=u`, so

\[
                         \boxed{\chi_+\ge1}.              \tag{10c}
\]

The baseline-free positive output has exactly the wrong direction.  For
no-hit, `u=c,v=d<=c`, and Jensen strengthens the physical tradeoff to

\[
 \boxed{
 \chi_-={c+ad\over rc}
 \ge {1\over r-ac}
 \ge c^a.}                                             \tag{10d}
\]

Consequently a physical no-hit cascade with clean throughput
`C=product_i c_i` has full/clean ratio at least `C^(r-1)`.  Exponential
suppression again forces exponential throughput loss, and this is the
affine-complement output carrying the baseline (9).

A genuine two-output conditional classifier has matrix (2); matrix (3)
also includes the fixed locked-history prior weights.  Its cross-channel
errors are `1-c` and `d`, and (4) implies the scale-independent bound

\[
 \boxed{(1-c)+d\ge1-{r\over(1+\sqrt r)^2}>0.}            \tag{10e}
\]

It cannot approach the channel-preserving diagonal transfer.  The exact
conclusion is that perfect classification was stronger than needed for one
posterior comparison, but not for isolating the all-clean/all-adverse
cylinders.  Under physical reset, the full batch contains every mixed word;
under persistent two-state testing, the mark contracts.  Together with
(4)--(10e), this closes the memoryless positive soft coverage/complement
workaround.  Signed common control or an additional physical memory state
remains outside the theorem.

## 2. Exact geometric-union transfer

Let

\[
 \Pr(K=k)={1\over r}\left({a\over r}\right)^{k-1},
\qquad k\ge1,                                           \tag{12}
\]

and let `U_1,...,U_K` be iid uniform on `[m]`.  The locked output is

\[
 B=\{U_1,\ldots,U_K\}.                                   \tag{13}
\]

The clean event is `F={K=1}` and the adverse event is `A={K>=2}`, with
probabilities `1/r` and `a/r`.  Independently sample a random tester set
`Z`.  Conditional on `Z`, put `X=1-|Z|/m`.  Then

\[
 \Pr(Z\cap B=\varnothing\mid K,Z)=X^K.                  \tag{14}
\]

The clean no-hit probability is `E X=c`.  Conditional on `A`,

\[
 \begin{aligned}
 \Pr(Z\cap B=\varnothing\mid A)
 &=\sum_{k\ge2}{a^{k-2}\over r^{k-1}}E X^k\\
 &=E\,{X^2\over r-aX}=d.                                \tag{15}
 \end{aligned}
\]

This proves (2)--(3).  Notice that the derivation only uses independence
and a uniform source row.  Formula (15), and hence (4), holds for any random
ancestral coverage tester, including an exact OR-chain analogue; iid
singleton tests are needed only for the explicit finite formula below.

For `ell` iid singleton tests, if `D=|Z|`, then

\[
 \Pr(D=j)={(m)_j\,\left\{\begin{smallmatrix}\ell\\j\end{smallmatrix}\right\}
                 \over m^\ell},                         \tag{16}
\]

where the braces denote a Stirling number of the second kind.  Therefore

\[
 \boxed{
 d={1\over m^\ell}
 \sum_{j=1}^{\min(\ell,m)}
 (m)_j\left\{\begin{smallmatrix}\ell\\j\end{smallmatrix}\right\}
 { (m-j)^2\over m(m+aj)}.}                              \tag{17}
\]

Equations (1), (3), and (17) are the requested exact finite `2 by 2`
transfer, with all tester collisions retained.

## 3. Projective discrimination and data processing

For `0<=X<=1`, set

\[
                         f(X)={X^2\over r-aX}.             \tag{18}
\]

The two elementary identities

\[
 f(X)\le X,
 \qquad
 f''(X)={2r^2\over(r-aX)^3}>0                            \tag{19}
\]

give `d<=c` and, by Jensen,

\[
                         d\ge {c^2\over r-ac}.             \tag{20}
\]

Thus no-hit is clean-enriching and hit is adverse-enriching:

\[
 {ad\over c}\le a,
 \qquad
 {a(1-d)\over1-c}\ge a.                                \tag{21}
\]

The second inequality in (4) is just the tangent inequality for the convex
function `c^(-a)`:

\[
 c^{-a}\ge1+a(1-c)=r-ac.                                \tag{22}
\]

This proves (4) and its product form (7).  Equality in the Jensen step holds
when `|Z|` is deterministic.  In particular, the bound is attained exactly
for one singleton tester, and asymptotically whenever tester occupancy
concentrates.

The same calculation quantifies why full two-output classification remains
impossible.  The total-variation separation between the conditional output
laws is

\[
                         c-d.                             \tag{23}
\]

By (20),

\[
 c-d\le {r c(1-c)\over r-ac}
       \le\boxed{{r\over(1+\sqrt r)^2}}<1,               \tag{24}
\]

where the maximum occurs at `c=sqrt(r)/(1+sqrt(r))`.  Soft testing therefore
does not approach a perfect router.  What it can do is make the likelihood
ratio on a rare no-hit output small; (4) states the exact price of doing so.

## 4. Exact source-collision floor

Conditional on `A`, the probability that all geometrically many source
samples collide on one label is

\[
 \begin{aligned}
 \Pr(|B|=1\mid A)
 &=\sum_{k\ge2}{a^{k-2}\over r^{k-1}}m^{1-k}\\
 &=\boxed{{1\over rm-a}}.                                \tag{25}
 \end{aligned}
\]

On this event `B` is again a uniform singleton, so its no-hit probability is
exactly `c`, indistinguishable from `F`.  Consequently

\[
                         d\ge {c\over rm-a},               \tag{26}
\]

which proves (5).  For fixed `m`, as `ell` tends to infinity all source sets
of rank at least two are rejected faster than singletons, and

\[
 \lim_{\ell\to\infty}{d\over c}={1\over rm-a},
 \qquad
 \lim_{\ell\to\infty}{ad\over c}={a\over rm-a}.          \tag{27}
\]

For the physical full-batch versus clean-process no-hit comparison, the same
collision atom gives

\[
 \chi_-={c+ad\over rc}\ge {m\over rm-a},                \tag{27a}
\]

with equality in the fixed-`m`, infinite-tester limit.

Thus increasing tester depth eventually stops buying projective
discrimination: it only attenuates the absolute signal.

## 5. The `ell/m` regimes

Let `m` tend to infinity and write `lambda=ell/m`.

If `lambda` tends to a finite value, occupancy concentration gives

\[
 X\longrightarrow x=e^{-\lambda},
 \qquad
 c\longrightarrow x,
 \qquad
 d\longrightarrow{x^2\over r-ax}.                       \tag{28}
\]

Hence

\[
 M_{m,\ell}\longrightarrow {1\over r}
 \begin{pmatrix}
 x&\displaystyle {a x^2\over r-ax}\\[4pt]
 1-x&\displaystyle a\left(1-{x^2\over r-ax}\right)
 \end{pmatrix},                                         \tag{29}
\]

and the no-hit adverse/clean ratio is

\[
                         \boxed{{a x\over r-ax}}.          \tag{30}
\]

There are three useful consequences.

1. If `ell/m -> 0`, then

   \[
   c=1-{\ell\over m}+o(\ell/m),
   \qquad
   {d\over c}=1-r{\ell\over m}+o(\ell/m).               \tag{31}
   \]

   Weak tests preserve a one-stage posterior ratio and its absolute
   throughput.  Section 6 shows why that posterior cannot be powered after
   a one-state reset.

2. If `ell/m -> lambda in (0,infinity)`, one observation obtains a strict
   constant posterior improvement, but also loses the constant clean factor
   `e^(-lambda)`.  In the persistent-label relaxation, infinitesimal stages
   make (7) asymptotically an equality: total projective retention is
   `C^r(1+o(1))`.

3. If `ell/m -> infinity`, the two rigorous lower bounds (4) and (5) are of
   orders `a exp(-ell/m)/r` and `a/(rm)`.  They cross when `ell/m` is of
   order `log m`.  For every fixed `m`, (27) shows that further testing
   eventually decreases absolute no-hit signal without overcoming source
   collisions.

These are statements about the ideal tester granted for free.  Any physical
module multiplicity or interface cost can only add to the losses.

## 6. The exact Markov-sufficiency obstruction

The scalar likelihood ratios above do not by themselves define a composable
transfer.  This is the decisive point missed by a naive strong-hit argument.

Let `w=(w_F,w_A)^T` be the decomposition into the two latent subevents of a
geometric batch before a tester.  For a retained output with conditional
probabilities `u` and `v`, the tester maps them to the one scalar

\[
                         s=(u,v)w.                        \tag{32}
\]

For hit, `(u,v)=(1-c,1-d)`; for no-hit, `(u,v)=(c,d)`.
Suppose a successful test hands off to one common downstream portal.  A
fresh locked stage splits `s` into `(s/r,as/r)^T`.  Its complete transfer is

\[
 R_{u,v}={1\over r}\binom1a(u,v).                        \tag{33}
\]

This matrix has rank one, and exactly

\[
 R_{u,v}^n=\left({u+av\over r}\right)^{n-1}R_{u,v}.      \tag{34}
\]

In this latent bookkeeping, every nonzero output after the first reset has
channel ratio `a`, not `(av/u)^n`.  There need not be an absolute-signal loss
hiding this failure.  For deterministic `X=x`, the hit-reset Perron
multiplier is

\[
 {u+av\over r}={r(1-x)\over r-ax}\longrightarrow1
 \quad(x\downarrow0).                                   \tag{35}
\]

The scalar `av/u` is a one-observation posterior odds ratio between the two
subevents.  Powering it assumes the diagonal persistent-label operator

\[
                         {1\over r}
                         \begin{pmatrix}u&0\\0&av\end{pmatrix}, \tag{36}
\]

which is a different physical kernel: it must send successful clean and
adverse histories to two distinguishable downstream states.  If F and A
were two fixed global models, their likelihood ratio could of course be
powered without storing the parameter in the state.  Here they are not:
they are newly resampled subevents inside each full geometric batch.

The mixed-history loss is explicit.  For the hit reset, put

\[
 \alpha={1-c\over r},
 \qquad
 \beta={a(1-d)\over r},
 \qquad s=\alpha+\beta.                                 \tag{37}
\]

The full geometric depth-`n` success mass is

\[
 s^n=\sum_{j=0}^n {n\choose j}\alpha^{n-j}\beta^j.      \tag{38}
\]

The two desired latent cylinders are only the extreme terms `alpha^n` and
`beta^n`; a reset merges every mixed cylinder with them.  The separate clean
one-sample process succeeds with probability `u=1-c` per level, so its
ratio against the full reset is `s/u`, not `beta/alpha`.  In the
deterministic-hole case,

\[
 s={r(1-x)\over r-ax},
 \qquad
 q_+={\beta\over\alpha}=a{r+x\over r-ax},
 \qquad
 \chi_+={s\over1-x}={1+q_+\over r}
 ={r\over r-ax}\ge1.                                  \tag{39}
\]

Thus `s` may tend to one while almost all surviving mass is mixed.  Good
absolute survival does not preserve the history ratio, and the actual
full/clean hit comparison is never favorable.

Keeping both binary test outputs gives the conditional kernel (2), with (3)
after the locked prior weights are included, not the persistent-label
operator (36).  A channel-preserving approximation would require both
off-diagonal conditional errors

\[
                         \epsilon_F=1-c,
 \qquad \epsilon_A=d                                    \tag{40}
\]

to vanish.  But (24) gives

\[
 \epsilon_F+\epsilon_A
 =1-(c-d)
 \ge\boxed{1-{r\over(1+\sqrt r)^2}>0.}                  \tag{41}
\]

Swapping the two output labels is worse: its error sum is
`c+(1-d)=1+(c-d)`.  This remains true for growing fan-out and arbitrary
tester depth.

There is also an exact all-depth data-processing identity for memoryless
binary-state Markov composition.  Write the conditional classifier as

\[
 K_i=\begin{pmatrix}c_i&d_i\\1-c_i&1-d_i\end{pmatrix}.
\]

On the binary zero-mass direction,

\[
 K_n\cdots K_1\binom1{-1}
 =\left\{\prod_{i=1}^n(c_i-d_i)\right\}\binom1{-1}.     \tag{42}
\]

By (24), its retained distinguishability is at most

\[
 \left\{{r\over(1+\sqrt r)^2}\right\}^{n}.             \tag{43}
\]

Thus even an inhomogeneous sequence of memoryless binary soft classifiers
erases the mark exponentially; it cannot approach the required diagonal
channel-preserving kernel.  Retaining the entire observation record can
increase posterior separation, but that record is precisely an additional
physical memory state and is not this two-state composition.

There are only two possibilities:

1. **Reset.** Project the successful test to one canonical portal.  This is
   a valid Markov sufficient statistic for future dynamics, but its rank-one
   transfer (33) erases the accumulated history mark and regenerates only one
   factor `a`.
2. **Persistence.** Keep enough of the old set or a separate memory state to
   retain the latent channel.  Repeated likelihood factors may then be
   meaningful, but an ordinary binary soft tester does not produce the
   diagonal kernel (36); the exact error floor (41) applies to its two-output
   version.

If the old source set remains dynamically active after a hit, it is the
second case, not a canonical reset.  The next-stage probability then depends
on that set, and the correct object is a set-valued Feynman--Kac kernel; the
scalar factors `u,v` cannot be multiplied.  Thus destructive reset does not
supply the diagonal transfer, while nondestructive testing requires a new
set-valued memory theorem not contained in the scalar calculation.

## 7. Absolute response and the complement obstruction

For comparison, if one formally retains a persistent hidden label through
`n` no-hit observations, the clean and adverse cylinder masses would be

\[
 S_F=r^{-n}\prod_{i=1}^n c_i=r^{-n}C,                    \tag{44}
\]

\[
 S_A=(a/r)^n\prod_{i=1}^n d_i,
 \qquad
 {S_A\over S_F}=a^n\Delta.                              \tag{45}
\]

Equation (7) is the exact throughput price even in this optimistic
persistent-label relaxation.  A physical one-output reset does not realize
(44)--(45), by Section 6.

The actual clean-process versus full-geometric no-hit comparison does
compose after common reset.  At level `i` its ratio is

\[
 \chi_{-,i}={c_i+a d_i\over r c_i}.
\]

By (20) and (22),

\[
 \prod_{i=1}^n\chi_{-,i}
 \ge\prod_{i=1}^n{1\over r-a c_i}
 \ge\left(\prod_{i=1}^n c_i\right)^a
 =C^{r-1}.                                              \tag{46}
\]

Thus physical exponential suppression forces `C` to vanish
exponentially.  The hit comparison cannot help because `chi_(+,i)>=1`.

There is also an independent sign/baseline obstruction.  Every normalized
positive mutant hitting/fixation harmonic is a coverage function `h` with
`h(\varnothing)=0`.  The clean-enriching output is `1-h`, whose empty-set
value is one.  At coefficient `w`, the physical clean-process signal is
`wC`, while the formal all-F cylinder in (44) has mass `w r^{-n}C`; the
unmatched affine baseline is exactly `w`.  The two ratios are (9).

Putting `N` positive copies in parallel, or enlarging a neutral bulk,
multiplies the baseline and useful signals by the same coefficient or
dilution factor.  Neither operation changes `1/C` (nor the stronger
`r^n/C` against the latent all-F cylinder).
If a construction cancels the unit baseline against a common control, it is
a signed response construction and must satisfy the separate obligations in
the signed-coverage note.

This theorem is deliberately scoped.  It closes memoryless iid-union soft
coverage and complement gates as a substitute for the channel-preserving
locked-history transfer.  It does not rule out a genuine extra memory state,
a signed common-control identity, or a direct graph response which never
factors through the proposed hidden two-channel history.

## 8. Exact replay

Run

```text
PYTHONDONTWRITEBYTECODE=1 ../../../.venv/bin/python -B verify_soft_coverage_transfer.py
```

The replay checks the exact occupancy transfer, its direct finite
enumeration, the convexity and sharp total-variation bounds, the collision
floor, the rank-one reset and mixed-history identities, and all-depth binary
mark erasure.
