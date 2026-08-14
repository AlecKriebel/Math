# The two-root Lorentz cone and the unmarked path-affinity obstruction

Date: 2026-08-13 (America/Los_Angeles)

No graph search, kernel search, literature search, or external communication
was used.

## 1. Status

**PROVED STRUCTURAL LEMMA AND EXACT PROOF-ROUTE OBSTRUCTION.**  The exact
two-root minimal-product criterion admits a useful Lorentz form.  Its
same-root slack becomes two nonnegative rapidities, while the swapped-root
assignment square becomes a third, orientation-sensitive coordinate.  A
new hyperbolic comparison proves that the Euclidean cone

\[
 \boxed{\quad
 \epsilon_{ij}^2\leq
   (\alpha_i+\alpha_j)^2+\delta_{ij}^2
 \quad}                                                \tag{1}
\]

is sufficient for the exact pair inequality.  This retains orientation;
setting `delta=0` would return to the stronger root-Hellinger route.

The natural attempt to prove (1) using the path-space Hellinger affinity of
the full Bd and dB duals is structurally vacuous.  Its geometric-mean
subgenerator `H` has the genuine radial supersolution

\[
                         H(|A|-1)\leq0,                \tag{2}
\]

but it has no positive transition from a singleton into rank at least two.
Therefore its killed Green excursion reward above the singleton boundary is
identically zero.  This remains true after every positive diagonal
conjugation, including degree conjugation.

The obstruction is one of support, not a failed coefficient estimate.  Bd
branching retains its occupied target, while a loopless dB burst deletes
that target and cannot resample it.  Their unmarked one-step path supports
therefore disagree exactly at the first rank-increasing step.  A successful
path-affinity proof would have to enlarge the state by a phase, operation,
or source-history mark before taking geometric means.  No such marked
construction is pursued here.

The universal minimal product and the Lorentz cone (1) remain **OPEN** for
physical modules.  This note proves the scalar bridge and closes only the
unmarked full-chain Hellinger route.

## 2. Kac return-cycle coordinates

Let `lambda_U` be the stationary law of the singleton-root Schur trace for
`U in {B,D}`, and let

\[
 \overline\phi_U=\lambda_U\phi_U>0                    \tag{3}
\]

be its signed excess-rank reward on the active branch.  For singleton root
`i`, write `q_{U,i}` for the trace return intensity and `C_{U,i}` for one
return cycle rooted at `i`, with the killed-complement occupation reward
included.  The continuous-time Kac identity gives the rate-normalized cycle
reward

\[
 \boxed{
 \mathscr R_U(i)
 :=q_{U,i}E_i\!\int_{C_{U,i}}
       \left({|A_t|\over s}-p\right)dt
 ={\overline\phi_U\over\lambda_{U,i}}
 ={\rho_U-p\over u_{U,i}}.}                           \tag{4}
\]

The factor `q_{U,i}` is essential for a continuous-time chain whose root
exit rates are not one.  Formula (4), rather than the unnormalized cycle
lifetime, is invariant under rootwise clock changes.

Put

\[
 h_i=\lambda_{B,i}\lambda_{D,i},\qquad
 Q=r^3\overline\phi_B\overline\phi_D.                 \tag{5}
\]

Then the one-root part of minimal product is exactly

\[
 \boxed{
 h_i\ge Q
 \quad\Longleftrightarrow\quad
 \mathscr R_B(i)\mathscr R_D(i)\le r^{-3}.}          \tag{6}
\]

Thus the diagonal obligation is already a paired full-return theorem.  It
cannot be proved by a bounded-rank prefix, and it is the first quantity a
path-space comparison must control.

## 3. Exact pair criterion in rapidities

Let `e_i=1/d_i` be inverse weighted degree.  On a pair `i!=j`, define the
degree and root-assignment orientations

\[
 \epsilon_{ij}={1\over2}\log{e_i\over e_j},           \tag{7}
\]

\[
 \delta_{ij}={1\over2}\log
 {\lambda_{B,i}e_j\lambda_{D,j}
  \over
  \lambda_{B,j}e_i\lambda_{D,i}}.                    \tag{8}
\]

Assume the two diagonal conditions (6), and put

\[
 \alpha_i=\operatorname{arcosh}\sqrt{h_i/Q}\ge0.     \tag{9}
\]

The exact orientation-preserving copositivity criterion is

\[
 \boxed{
 \cosh\alpha_i\cosh\alpha_j\cosh\delta_{ij}
 +\sinh\alpha_i\sinh\alpha_j
 \ge\cosh\epsilon_{ij}.}                             \tag{10}
\]

Indeed, multiply (10) by `Q` and use

\[
 Q\cosh\alpha_i\cosh\alpha_j=\sqrt{h_ih_j},
 \qquad
 Q\sinh\alpha_i\sinh\alpha_j
 =\sqrt{(h_i-Q)(h_j-Q)}.                              \tag{11}
\]

This recovers exactly the established two-root criterion, with no Cauchy
loss.

Equations (4)--(5) put every rapidity into full return-cycle coordinates:

\[
 \boxed{
 \alpha_i=\operatorname{arcosh}
 {1\over r^{3/2}
  \sqrt{\mathscr R_B(i)\mathscr R_D(i)}}.}            \tag{12}
\]

The orientation also has a swapped-cycle form,

\[
 \boxed{
 \delta_{ij}={1\over2}\log\left{
 {e_j\over e_i}
 {\mathscr R_B(j)\mathscr R_D(i)
  \over
  \mathscr R_B(i)\mathscr R_D(j)}\right}.}          \tag{13}
\]

Thus (10) compares the two same-root return products with both swapped
root assignments.  The degree mismatch on its right is not asked to be
paid by either rule separately.

## 4. A hyperbolic Euclidean comparison

The scalar result behind (1) is the following.

**Lorentz comparison.**  For every `A,B,D>=0`,

\[
 \boxed{
 \cosh A\cosh B\cosh D+\sinh A\sinh B
 \ge\cosh\sqrt{(A+B)^2+D^2}.}                        \tag{14}
\]

### Proof

Put `t=A+B`.  Product-to-sum and `tanh(t/2)<=t/2` give

\[
 \cosh A\cosh B
 ={\cosh t+\cosh(A-B)\over2}
 \ge {\cosh t+1\over2}
 \ge {\sinh t\over t}.                              \tag{15}
\]

Since

\[
 \cosh A\cosh B+\sinh A\sinh B=\cosh t,
\]

the left side of (14) is at least

\[
 \cosh t+{\sinh t\over t}(\cosh D-1).               \tag{16}
\]

It remains to compare (16) with the right side of (14).  Define

\[
 \Phi(x)=\log{\sinh\sqrt x\over\sqrt x},\qquad
 \Phi(0)=0.                                          \tag{17}
\]

For `q=sqrt(x)>0`, direct differentiation gives

\[
 \Phi''(x)=-{q\coth q+q^2\operatorname{csch}^2q-2
                 \over4q^4}\le0.                    \tag{18}
\]

To prove the sign, multiply the numerator in (18) by `sinh^2(q)` and put

\[
 M(q)=q\sinh q\cosh q+q^2-2\sinh^2q.                \tag{19}
\]

The first four initial jets are zero and

\[
                         M^{(4)}(q)=16q\sinh q\cosh q\ge0. \tag{20}
\]

Hence `M>=0`, proving concavity.  Concavity and `Phi(0)=0` imply
subadditivity on the nonnegative half-line:

\[
                         \Phi(x)+\Phi(y)\ge\Phi(x+y). \tag{21}
\]

With `u=sqrt(t^2+D^2)`, exponentiating (21) gives

\[
 {\sinh t\over t}{\sinh D\over D}\ge{\sinh u\over u}. \tag{22}
\]

Finally, the difference between (16) and `cosh u` vanishes at `D=0`, and
its derivative in `D` is

\[
 {\sinh t\over t}\sinh D-{D\over u}\sinh u\ge0     \tag{23}
\]

by (22).  This proves (14), including boundary cases by continuity.

Apply (14) with `(A,B,D)=(alpha_i,alpha_j,|delta_ij|)`.  Condition (1) says
explicitly that

\[
 |\epsilon_{ij}|\le
 \sqrt{(\alpha_i+\alpha_j)^2+\delta_{ij}^2}.
\]

Since `cosh` is even and increasing on the nonnegative half-line, (1)
implies (10).  Therefore (1) is a rigorous orientation-preserving
sufficient target for every physical root pair.

## 5. The unmarked geometric-mean subgenerator

Let `Q_B,Q_D` be the exact full Bd and dB dual generators on nonempty mutant
sets.  States not in the recurrent dB class may be retained for this local
operator statement.  For `A!=B`, write their jump rates as

\[
 b_{AB}=Q_B(A,B),\qquad d_{AB}=Q_D(A,B).              \tag{24}
\]

Define the path-affinity operator

\[
 H(A,B)=\sqrt{b_{AB}d_{AB}}\quad(A\ne B),\qquad
 H(A,A)={Q_B(A,A)+Q_D(A,A)\over2}.                   \tag{25}
\]

It is a killed Metzler generator.  Conservativity of the two original
generators gives the exact row killing

\[
 \boxed{
 (H\mathbf1)(A)
 =-{1\over2}\sum_{B\ne A}
   (\sqrt{b_{AB}}-\sqrt{d_{AB}})^2\le0.}             \tag{26}
\]

For every column `f`, there are two useful exact drift identities:

\[
 \boxed{
 (Hf)(A)
 ={(Q_Bf)(A)+(Q_Df)(A)\over2}
 -{1\over2}\sum_{B\ne A}
  (\sqrt{b_{AB}}-\sqrt{d_{AB}})^2f(B),}              \tag{27}
\]

and

\[
 \boxed{
 (Hf)(A)=
 \sum_{B\ne A}\sqrt{b_{AB}d_{AB}}{f(B)-f(A)\}
 +f(A)(H\mathbf1)(A).}                               \tag{28}
\]

Formula (27) displays the exact orientation square spent by path-space
Hellinger.  Formula (28) is the direct route to radial superharmonicity.

## 6. Exact support theorem and radial supersolution

Let `A` be nonempty and let an occupied target `v in A` update.

- A Bd neutral arrow lands at `(A minus {v}) union {u}`, whose rank is at
  most `|A|`.
- A rank-increasing Bd selective arrow lands at `A union {u}` and retains
  `v`.
- A dB burst lands at `(A minus {v}) union S`, where `S` is a nonempty
  union of row-`v` samples.  Looplessness gives `v notin S`, so this state
  does not contain `v`.

Consequently a rank-increasing Bd selective endpoint cannot be a dB
endpoint from the same state, even when the two generator entries arise
from different update targets.  Indeed, every rank-increasing Bd endpoint
contains all of `A`, whereas every dB endpoint omits whichever occupied
target generated that burst.  Every common off-diagonal edge of `Q_B` and
`Q_D`, and hence every positive off-diagonal edge of `H`, is therefore
rank-nonincreasing:

\[
 H(A,B)>0\quad\Longrightarrow\quad |B|\le|A|.        \tag{29}
\]

Take

\[
                             f(A)=|A|-1\ge0.           \tag{30}
\]

Every difference in (28) is nonpositive by (29), and the killing term is
nonpositive by (26).  This proves the promised full-rank theorem

\[
                              \boxed{Hf\le0.}          \tag{31}
\]

This proof is rowwise and uses all set ranks at once.  It is not a
rank-by-rank induction or a finite-prefix closure.

## 7. Why the Green implication is zero

At a singleton `A={i}`, every common edge in (29) must end at another
singleton.  Equivalently, with `S` the singleton sector and `R` every state
of rank at least two,

\[
                              \boxed{H_{SR}=0.}         \tag{32}
\]

Therefore for every reward `g_R` and every killed higher-rank Green kernel,

\[
                       H_{SR}(-H_{RR})^{-1}g_R=0.      \tag{33}
\]

An `H`-path started at a singleton may swap among singletons or be killed,
but it never enters a positive-rank excursion.  Thus (31) cannot bound the
positive Kac rewards in (4): it proves a contraction only after deleting
the very branching histories that generate those rewards.

This is not a boundary case where the physical target vanishes.  On the
unweighted three-path at `r=3/2`, the exact singleton-root data are

\[
 \lambda_B={1\over39}(16,7,16),\qquad
 \lambda_D={1\over13}(3,7,3),                         \tag{34}
\]

\[
 \overline\phi_B={200\over819},\qquad
 \overline\phi_D={2\over39}.                         \tag{35}
\]

Hence the rate-normalized Kac rewards are strictly positive:

\[
 \mathscr R_B(L)=\mathscr R_B(R)={25\over42},\qquad
 \mathscr R_B(C)={200\over147},                      \tag{36}
\]

\[
 \mathscr R_D(L)=\mathscr R_D(R)={2\over9},\qquad
 \mathscr R_D(C)={2\over21}.                        \tag{37}
\]

The unmarked affinity excursion reward is nevertheless zero by (32)--(33).
Positive diagonal similarities preserve the support zero in (32), so a
degree conjugation cannot repair it.

## 8. Stopping conclusion

The Lorentz comparison (14) remains useful: it converts the exact pair
criterion into the concrete full-return cone (1), with all variables given
by (7), (12), and (13).  What fails is the proposed operator mechanism for
proving that cone.  Entrywise geometric means must synchronize a Bd
branching step with a dB deleting burst, and no such unmarked state edge
exists.

A future path-space route would need an enlarged state which records the
operation phase, retained/deleted target, or complete source history before
taking the geometric mean.  That enlargement may preserve a common
rank-increasing edge, but it also reintroduces the target-locking and
collision information already known to be essential.  No search over such
marked constructions is made here.

## 9. Exact replay

From the repository root run

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B \
  universal_simultaneous_amplification/phase5_exact_threshold/\
rhyb_lorentz_affinity_obstruction/verify_lorentz_affinity.py
```
