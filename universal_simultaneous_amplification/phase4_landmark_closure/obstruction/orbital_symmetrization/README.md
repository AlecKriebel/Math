# Orbital symmetrization for regular dB at fitness two

## Target

Let `P` be a symmetric stochastic zero-diagonal kernel, let `sigma` be a
transposition, and put

\[
 P^\sigma=\Sigma P\Sigma^{-1},\qquad
 M={P+P^\sigma\over2}.
\]

Determine from first principles whether

\[
 \rho_{\rm dB}(M,2)\ge \rho_{\rm dB}(P,2)                 \tag{S}
\]

always holds.  This folder is an independent attack on (S).  No theorem is
claimed until an exact proof or rational counterexample is recorded below.

## Status

- **OPEN:** inequality (S).
- **PROVED:** at `r=2` each configuration-coordinate update is a heat-bath
  update.  If `x=P_{vS}`, its mutant resampling probability is
  `h(x)=2x/(1+x)`, and the two opposing changing rates sum to one.
- **PROVED:** kernel midpoint symmetrization improves every mutant-resampling
  probability relative to the arithmetic mean of the two conjugate endpoint
  generators, by concavity of `h`.  The remaining issue is to compare the
  arithmetic-mean generator with either fixed conjugate environment.
- **EXACTLY FALSIFIED BEYOND THE REGULAR CLASS:** (S) fails for general
  row-stochastic directed kernels already on three vertices.  Consequently
  the regular conjecture cannot be extended through arbitrary directed
  permutation-averaging intermediates.
- **EXACTLY FALSIFIED FOR NONREGULAR CONDUCTANCE AVERAGING:** directly
  averaging an undirected weight matrix with a transposition conjugate can
  strictly lower dB fixation.  Thus the regular statement supplies no
  immediate regularization reduction for the unrestricted class.

## Exact heat-bath reduction

Write a configuration as `S`, remove the status of `v`, and put

\[
 x=P_{v,S\setminus\{v\}},\qquad h(x)={2x\over1+x}.
\]

At the rate-one clock of `v`, its new status is a Bernoulli variable of
parameter `h(x)`, independently of its old status.  Thus, on the hypercube
edge with lower endpoint `T` and upper endpoint `T+v`, the two changing
rates are

\[
 h(x)={2x\over1+x},\qquad 1-h(x)={1-x\over1+x},
\]

and their sum is one.

If the two conjugate endpoint masses on a paired context are `x+z` and
`x-z`, put

\[
 \bar h={h(x+z)+h(x-z)\over2},\qquad
 s={h(x+z)-h(x-z)\over2}.
\]

The exact concavity bonus of the kernel midpoint is

\[
 \delta=h(x)-\bar h
 ={2z^2\over(1+x)((1+x)^2-z^2)},\qquad
 s={2z\over(1+x)^2-z^2},                              \tag{1}
\]

so `delta=s z/(1+x)` and `delta>=s^2/2` on the admissible interval
`0<=x+-z<=1`.  This is the precise quadratic term that must dominate the
odd-mode feedback; discarding it loses the conjectured inequality.

For the transient forward generator, let `U` act by the transposition on
configuration space and write

\[
 L_{\rm av}={L_P+UL_PU\over2},\qquad
 B={L_P-UL_PU\over2}.
\]

In the `U`-even/odd decomposition, `L_av` is block diagonal and `B` is block
off-diagonal.  If `f_P=g+d` is decomposed into its even and odd parts, its
harmonic equations are

\[
 L_+g+B_{+-}d=0,\qquad L_-d+B_{-+}g=0.                \tag{2}
\]

The midpoint residual of the averaged endpoint committor is consequently

\[
 L_Mg=(L_M-L_+)g-B_{+-}d.                             \tag{3}
\]

This gives an exact scalar closure criterion.  Put

\[
 C=L_M-L_+,qquad G_-=(-L_-)^{-1},qquad
 \mu=(-L_M)^{-T}\alpha,
\]

on the transient states, where `alpha` is uniform on the singleton states;
all generators act on functions with fixation boundary values `0,1`.  The
odd equation in (2) gives `d=G_-B_{-+}g`, while the midpoint Poisson equation
gives

\[
 \boxed{
 \rho(M,2)-\rho(P,2)
 =\left\langle\mu,
   \{C-B_{+-}G_-B_{-+}\}g\right\rangle.}               \tag{4}
\]

Thus orbital symmetrization is exactly an occupation-weighted sector
inequality.  The first operator is the local concavity bonus; the second is
the gain from an excursion through the odd mode.

The first term in (3) is the positive local bonus (1); the second is the
nonlocal Schur-complement feedback through `(-L_-)^{-1}`.  Direct statewise
subharmonicity of `g` is false, so (3) has to be controlled only after the
uniform-singleton occupation functional is applied.

The endpoint committor nevertheless has additional exact order structure.
If `pi_P` is the limiting dB-dual law started from the full set, Boolean
duality gives, for every initial mutant set `S`,

\[
 f_P(S)=\Pr_{A\sim\pi_P}(A\cap S\ne\varnothing).        \tag{5}
\]

Therefore `f_P`, and hence its orbital average `g`, is a coverage function:
it is monotone and submodular.  This is stronger than ordinary monotonicity
but it is not by itself enough for the sector estimate.  On the exact
order-four kernel used below, the `U`-even extreme coverage ray

\[
 g(S)=\boldsymbol1\{S\cap\{1,2\}\ne\varnothing\}
\]

has the exact sector value

\[
 \left\langle\mu,(C-B_{+-}G_-B_{-+})g\right\rangle
 =-{268925\over327199119}<0.                          \tag{6}
\]

Thus any proof of (4) must use that `g` is the averaged *harmonic committor*,
or equivalently use extra stationarity structure of its representing dual
law.  Coverage, monotonicity, and submodularity alone are rigorously
insufficient.

There is a useful transposition-specific bound on the odd block.  Label the
swapped vertices `1,2`, write their midpoint mutual weight as `c`, and their
common weights to the other vertices as `m_j`.  An odd function is supported
on configurations containing exactly one of `1,2`.  On such a configuration
with outside mutant set `T`, updates of `1,2` kill the odd mode at rate

\[
 \kappa(T)=1-\bar h(m_T)+\bar h(c+m_T)\ge1,            \tag{7}
\]

where each bar is the average over the two endpoint masses.  The remaining
outside-coordinate part is a Markov generator.  Hence the killed odd Green
operator is positivity preserving and has sup-norm at most one.  Equations
(1), (4), and (7) isolate a possible sharp sector inequality.  A proof that
the sector feedback in (3) is bounded by the bonus remains open.

## Closed proof routes

Two tempting intermediate comparisons are false.

1. The absorption probability of the arithmetic-mean generator
   `(L_P+UL_PU)/2` need not exceed that of `L_P`.  Ordinary regular kernels
   already give exact strict deficits; therefore pointwise heat-bath
   concavity and generator averaging cannot be separated into two monotone
   steps.  For the regular order-four kernel `(a,b,c)=(7/10,1/5,1/10)` and
   the transposition swapping the first two vertices,

   \[
   \rho(P)={8941\over21293},\qquad
   \rho\left({L_P+UL_PU\over2}\right)={387817\over926066},
   \]

   and the latter minus the former is
   `-22168725/19718723338`.  In contrast, the actual kernel midpoint has
   fixation `863/2054` and improves the endpoint by
   `11045/43735822`.
2. Averaging the generator over the full permutation group gives an exact
   mutant-count birth--death chain.  If

   \[
   a_k={1\over n{n-1\choose k}}
       \sum_v\sum_{|T|=k}h(P_{vT}),
   \]

   its rates are `b_k=(n-k)a_k` and `d_k=k(1-a_{k-1})`.  Although concavity
   makes the complete graph dominate this annealed count chain, the
   annealed fixation can be strictly below the fixed-environment fixation.
   For the same rational order-four kernel its value is
   `959027/2557096`, below the endpoint by
   `2442433425/54448245128`.  Thus full-group annealing is not a valid lower
   intermediary either.  `verify_failed_annealing_routes.py` reconstructs
   all labelled rates and certifies these rational comparisons.

The exact dB dual gives one further structural fact.  For the hit indicator
`F_C(A)=1{A intersects C}`, its generator is

\[
 L_P^*F_C(A)=
 \begin{cases}
  \sum_{v\in A}h(P_{vC}),&A\cap C=\varnothing,\\
  h(P_{vC})-1,&A\cap C=\{v\},\\
 0,&|A\cap C|\ge2.
 \end{cases}                                           \tag{8}
\]

This proves directly that future expected cardinality is a coverage
function of the starting dual set.  However, the natural one-step orbital
inequality on the whole coverage cone is false.  On the rational kernel
above, with `A={1,2}` and `C={1,3}`, its exact paired generator residual is
`-10/69`.  Numerical exact-state evolution also shows that finite-time dual
mean domination from the full set can fail before the stationary ordering
reappears.  A stationary argument is therefore essential.

### Directed extension is false

The heat-bath identities, even/odd decomposition, and odd killing argument
make sense for a general row-stochastic zero-diagonal kernel.  The orbital
inequality itself does not.  Let

\[
 P=\begin{pmatrix}
 0&999/1000&1/1000\\
 24/25&0&1/25\\
 2/5&3/5&0
 \end{pmatrix},
\]

and swap the first two vertices.  Exact labelled solution gives

\[
 \rho(P,2)={150104029643\over432850757676},\qquad
 \rho\left({P+P^\sigma\over2},2\right)
 ={52230380\over150626871},
\]

with midpoint minus endpoint

\[
 -{580250970313391\over21732985079571703932}<0.         \tag{9}
\]

Thus symmetry of `P` (equivalently regularity for the undirected weighted
graph after scaling) is doing essential work.  For a nonregular undirected
graph its row kernel is reversible but not symmetric, and its kernel
midpoint need not correspond to an undirected graph.  No exact
fixation-preserving reduction from the nonregular class to the regular class
is supplied here; ordinary vertex cloning introduces partially mutant clone
modules and does not preserve the original chain.

Even staying inside undirected weighted graphs does not repair the extension.
On vertices `0,1,2,3,4`, take the connected conductance graph whose only
positive edges are

\[
 w_{02}=5,\qquad w_{04}=1,\qquad
 w_{13}=20,\qquad w_{14}=1/10.                         \tag{10}
\]

For the same transposition `sigma=(0 1)`, exact solution gives

\[
 \rho(W,2)={39794039823911\over114450553349505},
\]

while

\[
 \rho\left({W+W^\sigma\over2},2\right)
 ={65633240271786525885720837847
   \over203520905146834717343643922215}.
\]

The latter minus the former is

\[
 -{39143889145638008146691134610289543891142
 \over1552872014149823570194880387852400261916905}<0. \tag{11}
\]

The support in (10) is a connected tree.  Hence admissible undirected
conductance symmetrization itself fails, not merely the directed kernel
intermediate.

## Mesoscopic specialization stress test

`screen_two_group_specialization.py` tests a regular family designed to make
the odd feedback coherent across many vertices.  Besides the swapped
vertices `0,1`, take equal classes `A,B` of size `m`.  Vertex `0` has weights
`a,b` to each vertex of `A,B`, while vertex `1` has weights `b,a`; the two
outside classes have common within-class and cross-class weights.  With

\[
 a+b={1-c\over m},\qquad
 m v=\gamma(1-a-b),\qquad
 (m-1)u=(1-\gamma)(1-a-b),
\]

all rows sum to one.  The transposition midpoint replaces `a,b` by their
average.  Both endpoint and midpoint are exactly lumpable by

\[
 (x_0,x_1,i,j)\in\{0,1\}^2\times\{0,\ldots,m\}^2,
\]

because every target in a class sees mutant weight determined only by these
four counts.  The script builds the resulting `4(m+1)^2-2` transient
equations directly.  Targeted maximal-specialization and near-boundary
screens through `m=80` retained positive orbital slack, sometimes only of
order `m^-2`.  This is a stress test, not a proof or an asymptotic claim.

## Reproduction

From the repository root:

```text
./.venv/bin/python \
  universal_simultaneous_amplification/phase4_landmark_closure/obstruction/\
orbital_symmetrization/verify_failed_annealing_routes.py

OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 ./.venv/bin/python \
  universal_simultaneous_amplification/phase4_landmark_closure/obstruction/\
orbital_symmetrization/screen_two_group_specialization.py --max-m 80
```
