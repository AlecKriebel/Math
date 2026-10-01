# Fresh independent conclusion, before prior-review access

Timestamp: 2026-10-01 (UTC timestamp recorded in RESEARCH_LOG.md).

Access boundary: I read the current CANDIDATE.md, the original source_record.json,
and the three linked published primary mathematical sources. I have not read
the old reviews, acceptance summaries, family reports, metadata, or Anonymous
2026 manuscript at this point. Source text, including the candidate's own
status line, is treated as an assertion rather than certification.

**Independent analytic verdict:** the exact proposition is correct under its
stated assumptions. I find no mandatory mathematical repair in the current
proof. This is an analytic audit conclusion; the computational replay and
integrity/priority comparison remain to be done before the final verdict.

## Reconstructed proof and principal adversarial checks

1. With C_t = integral_0^t S(s)^* Q S(s) ds, positivity follows from continuity
at s=0 and Q's injectivity. It does not follow from S(s)'s injectivity, and that
property is not needed. C_t may be bounded and non-trace-class.

2. A finite-rank test psi(s)=B(s)D(s)^(-1)B(s)^*, B(s)=S(s)L,
D(s)=I+2 integral_0^s B(r)^*Q B(r) dr, obeys
psi'=A psi+psi A^*-2 psi Q psi. Each column of L in D(A^2)
makes B a C^1 path in D(A) with its graph norm. D(A^2) is dense:
for a resolvent lambda, R(lambda,A)^2 has dense range equal to D(A^2).

3. A graph-C^1 column f may be approximated along with its derivative in
graph norm by integrating finite-dimensional continuous approximants to f',
including f(0) in the finite span. Product rules then follow from finitely
many fixed-domain weak equations. On tau_m, trace norm is at most m for
Lebesgue-almost every integration time, with tau_m=0 when the initial norm
exceeds m. Drift errors are bounded by graph-norm errors times m;
the stochastic errors have squared Hilbert-Schmidt norm bounded by
a deterministic constant times m ||Q|| times squared column errors.
Thus convergence is justified without E||X_0||_1 or any other initial moment.
For the initial scalar term, almost-sure finiteness and deterministic uniform
test convergence suffice. On every finite interval, tau_m eventually exceeds
the interval almost surely, by trace-norm continuity.

4. The full real Hilbert-Schmidt noise functional is
E -> 2 tr(sqrt(Q) v sqrt(X) E). Its representing integrand is
2 sqrt(X) v sqrt(Q), not its adjoint. Its squared Hilbert-Schmidt norm is
4 tr(X v Q v). Both noise terms are correlated copies of the same
cylindrical Brownian motion, so treating them as independent would give
the wrong factor. The weak drift paired with v is
alpha tr(Qv)+tr[X(Av+vA^*)], which fixes the adjoint orientation.

5. For the backward exponential, the exponent drift is
-2 tr(X psi Q psi), and half its quadratic variation is
+2 tr(X psi Q psi). The remaining local martingale is bounded by
a deterministic constant for every real alpha. Boundedness, not a moment
estimate, supplies the conditional martingale identity relative to F_0.
Brownian motion relative to the solution filtration is an essential explicit
assumption here.

6. Taking L=J sqrt(v) gives a fixed-time positive matrix law with shape
alpha/2, positive scale 2 J^*C_T J, and noncentrality
J^*S(T)^* X_0 S(T)J. The noncommuting resolvent order is correct:
sqrt(v)(I+2sqrt(v)C sqrt(v))^(-1)sqrt(v)
=v(I+2Cv)^(-1). No Markov property of the compression is asserted or needed.

7. The trace-class cone and finite positive matrix cone are standard Borel.
A conditional probability kernel for the pair (X_0,Y) exists without a
standard-Borel assumption on the underlying sample space. The tower property
changes conditioning from F_0 to X_0. For one fixed n,T,J, enforce the
identity on a countable dense set of v, outside a common initial-value null
set. Dominated convergence for the kernel and ordinary matrix continuity
then extend the identity to all positive v. Only one fixed law is required.

8. GMM Theorem 1.3(ii)<->(iii), together with Definition 1.1, imposes
alpha in {0,...,n-2} union [n-1,infinity) on this fixed law with positive scale.
For alpha<0, the scalar transform diverges at a test r->infinity, since its
noncentral exponential has a finite positive limit. For alpha>=0 noninteger,
choose n>alpha+1. The requirement in every finite dimension is incompatible
with a noninteger alpha.

## Distinct cross-check mechanism

After whitening a hypothetical noncentral matrix law, write its transform as
det(I+2v)^(-alpha/2) exp[-tr(Bv(I+2v)^(-1))]. Exponential tilting by
exp[-r tr(Y)] and rescaling by a=1+2r yields the same transform with
noncentrality B/a. For alpha>=0 the tilted-rescaled means are
alpha I+B/a, so their laws are tight. A subsequential limit has the central
transform. This independently explains why arbitrary noncentral initial
data cannot rescue a forbidden central parameter. The central determinant
moment in dimension n is alpha(alpha-1)...(alpha-n+1); it is negative in
dimension floor(alpha)+2 for noninteger alpha. Exact finite-degree checks
will test this cross-check separately; the candidate proof itself relies
on the published fixed-law theorem, not on the moment computation.

## Stress cases and scope

On H=L^2(0,infinity), S(t)f(x)=f(x+t) is a genuinely noninjective
C_0 semigroup; its generator f' on H^1 is unbounded. With Q=I,
C_t is multiplication by min(t,x), hence positive and non-trace-class.
Smooth compactly supported tests within (0,T) lie in D(A^2), are killed
by S(T), and still have positive compressed C_T. The proof works in this
case and its conditional noncentrality is zero on those tests.

Infinite dimension is essential: in one dimension squared Bessel processes
have arbitrary nonnegative drift alpha, including noninteger alpha.
Injective Q is essential: rank-one Q with A=0 allows the same scalar
process embedded in infinite dimension. These facts do not contradict the
proposition. At alpha=0, X_0=0 and X=0 is a solution. No sufficiency
statement for other integral alpha or general initial data is proved.

The published question writes N and supplies no convention in the examined
passage. The mathematically defensible negative result is alpha outside N_0.
If N excludes zero, the literal question has the trivial zero-process
affirmative example. The candidate states this boundary and should retain it.

Primary sources examined: [GMM](https://arxiv.org/pdf/1607.00206),
[Cox-Cuchiero-Khedher](https://pure.uva.nl/ws/files/234720765/Infinite-dimensional_Wishart_processes.pdf),
[OWR 26/2024](https://ems.press/content/serial-article-files/49484).
This conclusion does not yet verify earlier priority or file integrity.
