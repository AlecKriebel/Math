# Five-ground Picone reduction of the endpoint-versus-first-orbit lemma

Date: 2026-08-13 (America/Los_Angeles)

## Status

This note gives an exact finite reduction of the still-open inequality

\[
 \boxed{\ E_p\mathcal F(q)\geq E_p s\ },\qquad
 \mathcal F(y)={2Ry\over1+2Ry}.                              \tag{1}
\]

Together with the proved first-orbit inequality
`E_p F(q) <= E_p q`, (1) would prove the factor-one boundary
`beta+sigma <= 1`.  The reduction below is not a proof of (1).  It adds the
previously unused positive ground `w=aq` and identifies the exact theorem of
alternatives for every certificate obtained by summing pairwise Picone
inequalities among all five grounds.

## 1. Endpoint grounds and the target density

Let `P` be finite, row stochastic, and self-adjoint in `L^2(pi)`.  Let
`a>0` be normalized by `E_pi a=1`, and set

\[
 p=\pi a,\qquad R=D_a^{-1}PD_a,\qquad t={Pa\over a},          \tag{2}
\]

and suppose the positive endpoint solutions obey

\[
 tb=2qPb,\qquad s=2hRs,qquad q=1-b,\quad h=1-s.             \tag{3}
\]

Put

\[
 h_1={1\over1+2Rq},\qquad w=aq,\qquad v=as.                 \tag{4}
\]

Then the endpoint-versus-first-orbit gap is

\[
 E_p\mathcal F(q)-E_ps
   =\sum_i\pi_i e_i,qquad e_i=a_i(h_i-h_{1,i}).             \tag{5}
\]

The five positive grounds and their exact node potentials are

\[
\begin{array}{c|ccccc}
 f&1&a&b&v=as&w=aq\\ \hline
 V_f=(Pf)/f&1&t&t/(2q)&1/(2h)&Rq/q.
\end{array}                                                  \tag{6}
\]

The last entry is an identity, because `Pw=P(aq)=aRq`.  Therefore the new
ground is available without an additional endpoint equation.  It also
encodes the first iterate itself:

\[
 V_w={1-h_1\over2qh_1},\qquad
 e=a\left({1\over2V_v}-{1\over1+2(w/a)V_w}\right).           \tag{7}
\]

Thus (1) is entirely a five-ground potential inequality.

The fixed-point equation also gives the direct resolvent form

\[
 e=2ahh_1R(q-s)=2ahh_1(qV_w-sV_v).                          \tag{7c}
\]

There is also a useful exact separation of the raw ground difference from
the `(w,v)` potential difference:

\[
 \mathcal F(q)-s
 ={h\over h+q}(q-s)
  +{2qhh_1\over h+q}(V_w-V_v).                              \tag{7a}
\]

Equivalently, with `c^{wv}=wv(V_v-V_w)`,

\[
 e={ah\over h+q}(q-s)
   -{2hh_1\over as(h+q)}c^{wv}.                              \tag{7b}
\]

The coefficient in (7b) depends on more than the single ratio
`v/w=s/q`, which is the precise obstruction to closing (1) with only the
one `(w,v)` Picone order.

## 2. The temperature-adjoint involution

There is a useful exact second orientation of (5).  Define

\[
 p'=pt,\qquad P'=D_t^{-1}R.                                  \tag{8}
\]

Then the `p'`-adjoint of `P'` is `R'=D_t^{-1}P`, its temperature is
`t'=1/t`, and the endpoint roles swap:

\[
 b'=s,\qquad s'=b.                                           \tag{9}
\]

Indeed, (3) gives

\[
 t's=2hP's,qquad b=2qR'b.                                  \tag{10}
\]

Let

\[
 q_1={t\over t+2Ph},\qquad d=q-s.                            \tag{11}
\]

The original and involuted endpoint-versus-first residuals satisfy the
pointwise resolvent identities

\[
 \boxed{
 h-h_1=2hh_1Rd,qquad
 q-q_1={2qq_1\over t}Pd.}                                   \tag{12}
\]

Consequently they share the exact cross-energy

\[
 \boxed{
 \langle d,Pd\rangle_p
 =\left\langle {d(h-h_1)\over2hh_1}\right\rangle_p
 =\left\langle {td(q-q_1)\over2qq_1}\right\rangle_p.}      \tag{13}
\]

This explains why applying the proved first-orbit theorem in both
orientations does not immediately finish (1): the common quantity in (13)
is `⟨d,Pd⟩_p`, not a nonnegative Dirichlet form
`⟨d,(I-P)d⟩`.  No sign for (13) follows merely from self-adjointness of the
underlying kernel.

## 3. Complete five-ground pairwise certificate

For two positive grounds `f,g`, write

\[
 r_i^{fg}={g_i\over f_i},\qquad
 c_i^{fg}=f_ig_i(V_{g,i}-V_{f,i}).                           \tag{14}
\]

For every increasing function `psi_fg` on the finite ratio set, the
cut-Picone identity gives

\[
 \sum_i\pi_i c_i^{fg}\psi_{fg}(r_i^{fg})\leq0.              \tag{15}
\]

Take one orientation of each of the ten unordered pairs in

\[
                         \mathcal G=\{1,a,b,v,w\}.           \tag{16}
\]

The following is therefore immediate.

**Five-ground certificate theorem.**  If there are increasing functions
`psi_fg`, one for every pair `fg`, such that

\[
 e_i+\sum_{\{f,g\}\subset\mathcal G}
       c_i^{fg}\psi_{fg}(r_i^{fg})\geq0
 \qquad\hbox{for every }i,                                  \tag{17}
\]

then (1) holds.

This is the complete certificate obtained by taking arbitrary nonnegative
sums of the ten pairwise Picone inequalities for the five known grounds.
Its correction cone contains the earlier six-pair four-ground correction
cone, although (17) has the sharper endpoint-orbit target `e`.  The ratios
are highly linked; for example

\[
 {w\over a}=q,\quad {v\over a}=s,\quad {v\over w}={s\over q},
 \quad {w\over b}={aq\over b},\quad {v\over b}={as\over b},  \tag{18}
\]

and every other pair ratio is a quotient or product of these.  Likewise,
for any three grounds `f,g,k`,

\[
 r^{fk}=r^{fg}r^{gk},\qquad
 c^{fk}={k\over g}c^{fg}+{f\over g}c^{gk}.                  \tag{19}
\]

Any proof of (17) must retain these coupled identities; the coefficient of
the single `(w,v)` Picone term obtained by directly expanding (5) is not a
function of `v/w=s/q` alone.

## 4. Exact Farkas alternative

For `lambda_i>=0` and a pair `fg`, define the lower-prefix sums

\[
 S_{fg}(z)=\sum_{i:r_i^{fg}\leq z}\lambda_i c_i^{fg}.         \tag{20}
\]

Exactly one of the following alternatives holds:

1. the increasing label potentials in (17) exist;
2. there is a nonzero `lambda>=0` such that, for every one of the ten
   pairs,

   \[
   \sum_i\lambda_i c_i^{fg}=0,qquad
   S_{fg}(z)\geq0\quad\hbox{at every proper ratio cut},       \tag{21}
   \]

   but

   \[
                           \sum_i\lambda_i e_i<0.             \tag{22}
   \]

The proof is finite-dimensional Farkas elimination.  Assign one variable
to each distinct level of every ratio, impose consecutive monotonicity
inequalities, and dualize (17).  Eliminating the nonnegative dual flows on
the consecutive order edges gives precisely the prefix conditions (21).
Conversely, those prefix sums reconstruct the order-edge flows, proving
the reverse implication.

For the physical measure `lambda=pi`, (21) follows from the exact Picone
cut formula.  Hence the sharp remaining ordered statement for this route
is:

> Every nonnegative measure obeying all ten simultaneous linked ground
> cut orders (21) has nonnegative `e`-average.

A proof of this statement proves endpoint-versus-first and therefore
factor one.  A finite exact violation only refutes the complete pairwise
five-ground Picone route; it need not refute the physical inequality,
because a dual `lambda` in (21) need not itself be the reversible measure
of a kernel realizing the five grounds.

The multiplicative identities (18)-(19) do not by themselves force
`lambda=0`: the physical measure `lambda=pi` is nonzero and satisfies all
ten equalities and lower-prefix inequalities in (21) for every nonconstant
kernel.  What remains is therefore a target-sign consequence of the linked
orders, not a contradiction from the existence of a positive simultaneous
cut measure alone.

Even after normalizing away scalar multiples, the ten orders need not
determine the physical measure by linear algebra.  To see the exact
limitation, form the `10 by n` matrix whose rows are the ten vectors
`c^{fg}`.  If `n>=12`, its nullspace has dimension at least two and contains
`pi`.  Hence it contains a vector `u` not proportional to `pi`.  Whenever
all physical proper cut sums are strict, every sufficiently small signed
perturbation

\[
                         \lambda=\pi+\epsilon u              \tag{22a}
\]

remains positive and retains all ten cut inequalities, while the ten total
equalities remain exact.  Thus no cyclic-order proof can finish merely by
showing that the simultaneous cut measure is unique.  It must use the
specific target (7), or additional structure beyond pairwise Picone data.
This dimension observation does not produce (22): crossing the target
hyperplane before a cut becomes tight is a separate and unresolved issue.

## 5. Boundary interpretation

On a deterministic two-cycle with type-mass ratio `a`, (5) factors as

\[
 {3a(a-1)^2\over
  2(a+2)(2a+1)(a^2+4a+1)}\geq0.                              \tag{23}
\]

The gap vanishes only at the balanced orbit and in singular mass limits.
The singular three-type leak face likewise approaches equality only when
an active mass or transfer disappears.  These modes identify where a
future sharp construction can hide a nonuniform boundary layer: they do
not supply a negative endpoint witness.
