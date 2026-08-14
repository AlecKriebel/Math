# Positive set memory cannot power the locked-history factor

Date: 2026-08-13 (America/Los_Angeles)

No graph search, literature search, or external communication was used.

## 1. Result

Retaining the set-valued output of a locked batch does not repair the soft
reset route if every downstream state and the final readout are positive
OR/coverage events.

Write

\[
                         a=r-1,\qquad 1<r<2.
\tag{1}
\]

Couple the clean and adverse locked batches by

\[
 B_F=\{U_1\},\qquad
 B_A=\{U_1,\ldots,U_K\},\quad K\geq2,
\tag{2}
\]

where, conditional on the adverse event,

\[
 \Pr(K=k\mid A)={a^{k-2}\over r^{k-1}},\qquad k\geq2.
\tag{3}
\]

Then `B_F subseteq B_A` pointwise.  Consequently, for every positive
downstream OR statistic `g`,

\[
 u:=E g(B_F),\qquad v:=E g(B_A)
\quad\Longrightarrow\quad
                         \boxed{u\leq v\leq(r+1)u.}
\tag{4}
\]

The lower inequality uses monotonicity.  The upper inequality uses
submodularity and the exact identity `E(K | A)=r+1`.

For two positive retained states `g_0,g_1`, put

\[
 u_j=E g_j(B_F),\qquad v_j=E g_j(B_A).
\tag{5}
\]

Including the locked-history prior masses `1/r` and `a/r`, their handoff
matrix is

\[
 H={1\over r}
 \begin{pmatrix}
 u_0&a v_0\\
 u_1&a v_1
 \end{pmatrix}.
\tag{6}
\]

Equation (4) gives the componentwise order

\[
                         \boxed{H e_A\geq a H e_F.}
\tag{7}
\]

Every common positive continuation preserves this order.  For every
nonnegative matrix `N` of any dimension and every nonnegative terminal
readout `z`,

\[
 z^T N H e_A\geq a\,z^T N H e_F.
\tag{8}
\]

This is the decisive all-depth obstruction.  It applies equally to a
finite handoff, a growing handoff, a full retained-set Markov kernel, or an
inhomogeneous cascade: once the two coupled input laws enter a common
positive OR continuation, their adverse/favorable ratio can never fall
below `a`.  The desired labelled cylinders instead have ratio `a^L`.
For `L>=2`,

\[
 {\hbox{positive retained adverse mass}\over
   \hbox{positive retained clean mass}}
 \geq a
 \quad\hbox{whereas}\quad
 {\hbox{all-adverse cylinder}\over\hbox{all-clean cylinder}}
 =a^L.
\tag{9}
\]

Thus positive set memory preserves only one factor `r-1`; it does not
multiply it.  Parallel replication, fan-out, and common dilution multiply
both sides of (8) and cannot change the conclusion.

The theorem is deliberately narrow.  A nonmonotone set statistic, an
affine complement, a signed common control, or channel/rule-dependent
continuations are not covered.

## 2. Coupling and the sharp submodular interval

A positive OR/hitting statistic has the coverage form

\[
                  g(B)=\int \mathbf1_{\{Z\cap B\ne\varnothing\}}\,d\mu(Z),
\tag{10}
\]

where `mu` is a finite positive measure on nonempty ancestral tester sets.
It is normalized at the empty set, monotone, and submodular.  In particular,

\[
                  g(C_1\cup\cdots\cup C_k)
                  \leq\sum_{i=1}^k g(C_i).
\tag{11}
\]

The coupling (2) immediately gives `g(B_A)>=g(B_F)`.  It also gives

\[
 g(B_A)\leq\sum_{i=1}^K g(\{U_i\}).
\tag{12}
\]

The geometric law has

\[
 E(K\mid A)
 ={E K-\Pr(K=1)\over\Pr(A)}
 ={r-r^{-1}\over a/r}=r+1.
\tag{13}
\]

Taking expectations in (12) proves the upper half of (4).  Both bounds are
sharp in the natural limiting senses: a constant nonempty-set hit has
`v/u=1`, while a diffuse singleton tester has `v/u` tending to `r+1`.

The first inequality alone proves (7)--(9).  Therefore no occupancy limit,
collision estimate, or exploration over set sizes is required.

## 3. Relation to the exact soft matrix

For the soft tester in the preceding note, let

\[
 c=\Pr(\hbox{no hit}\mid F),\qquad
 d=\Pr(\hbox{no hit}\mid A).
\tag{14}
\]

Its exact conditional classifier is

\[
 K=\begin{pmatrix}c&d\\1-c&1-d\end{pmatrix},
\qquad d\leq c.
\tag{15}
\]

The positive hit row obeys

\[
                         1-d\geq1-c,
\tag{16}
\]

exactly as (4) requires.  The only clean-enriching row is no-hit,

\[
                         c>d,
\tag{17}
\]

but this row is the affine complement `1-h(B)` of a positive coverage
function and has value one at the empty set.  Replacing it by any second
positive hit statistic restores (4), so both rows satisfy adverse
dominance and (7) follows.

The eigenvalue `c-d` of the column-stochastic matrix (15) therefore does
not contradict the theorem.  That mark direction uses the difference of
the two output coordinates; equivalently, it uses the affine-complement
row in (15).  A positive readout cannot isolate it.

## 4. Complete routing is rank one

Suppose two positive coverage routes are physical exclusive destinations,
so

\[
                         g_0(B)+g_1(B)\leq1
\tag{18}
\]

for every nonempty `B`.  If routing is complete, equality holds throughout.
For `B subseteq C`, monotonicity makes both increments
`g_j(C)-g_j(B)` nonnegative, while their sum is zero.  Hence each `g_j` is
constant on the nonempty Boolean lattice:

\[
                         g_j(B)=\alpha_j\quad(B\ne\varnothing).
\tag{19}
\]

It follows that `u_j=v_j=alpha_j` and

\[
 H={1\over r}\binom{\alpha_0}{\alpha_1}(1,a),
\tag{20}
\]

which has rank one.  Thus a complete two-destination positive OR router
erases the mark exactly.

If (18) is strict, the missing route is

\[
                         \ell(B)=1-g_0(B)-g_1(B),
\tag{21}
\]

with `ell(emptyset)=1`.  It is an affine NOT/loss coordinate.  One may
discard that coordinate as death, but the two retained positive routes
still obey (7), so discarding it cannot produce the powered ratio.

## 5. Exact two-state spectral corollary

There is a stronger statement if one nevertheless tries to use a
sub-Perron eigenmode of (6).  Every nonzero coverage row has `u_j>0`; put

\[
                         \theta_j={v_j\over u_j}.
\tag{22}
\]

By (4), `1<=theta_j<=r+1`.  If `det H<=0`, there is no positive second
eigenvalue.  If `det H>0`, then `theta_1>theta_0` in the displayed state
ordering.  Let `lambda_+>=lambda_->0` be the two eigenvalues and set
`q=lambda_-/lambda_+`.  Since

\[
 {q\over(1+q)^2}
 ={\det H\over(\mathop{tr}H)^2}
 ={a u_0u_1(\theta_1-\theta_0)
   \over(u_0+a\theta_1u_1)^2},
\tag{23}
\]

AM--GM and (4) give

\[
 {q\over(1+q)^2}
 \leq{\theta_1-\theta_0\over4\theta_1}
 \leq{r\over4(r+1)}.
\tag{24}
\]

The left side is increasing for `0<=q<=1`, so

\[
 \boxed{
 q\leq q_*(r):={\sqrt{r+1}-1\over\sqrt{r+1}+1}.}
\tag{25}
\]

This bound is sharp as an abstract coverage-statistic supremum: take one
row constant on nonempty sets and the other to be an increasingly diffuse
singleton hit, then balance the two row coefficients in the AM--GM step.
At `r=R_hyb`,

\[
 q_*(R_{\rm hyb})=0.2254192633\ldots,
 \qquad R_{\rm hyb}-1=0.5028569127\ldots.
\tag{26}
\]

Indeed the exact interval `3/2<r<151/100` gives

\[
                         q_*(r)<1/4<1/2<a.
\tag{27}
\]

Therefore the labelled transfer's exact spectral ratio `a` is not even a
two-state positive-coverage eigenratio at the candidate endpoint.  Smaller
sub-Perron ratios can occur algebraically, but their eigenvectors/readouts
are sign-changing by Perron--Frobenius.  Equation (8) shows directly that
no nonnegative initialization and readout can use such a mode to beat the
one-factor floor `a`.

## 6. Consequence for the lower program

The smallest genuine positive memory extension is closed:

* a complete two-state router is rank one;
* an incomplete positive router may be full rank, but every retained state
  is at least as likely under the adverse union as under the clean
  singleton;
* common positive continuation preserves that stochastic order at every
  depth;
* an algebraic attenuating eigenmode is necessarily a signed mode.

Thus the labelled factor cannot be powered through positive set-valued OR
memory.  A surviving construction must use a signed common control,
nonmonotone information about `B`, channel/rule-dependent dynamics, or a
direct response mechanism that does not factor through this coupled
clean/adverse handoff.

## 7. Exact replay

Run

```text
PYTHONDONTWRITEBYTECODE=1 ../../../.venv/bin/python -B verify_positive_set_memory.py
```

The replay checks the geometric conditional mean, the exact soft-row
inequalities, positive-kernel order preservation, the rank-one complete
router, and the spectral inversion (25).
