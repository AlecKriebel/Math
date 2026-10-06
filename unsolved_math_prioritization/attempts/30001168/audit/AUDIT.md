# Independent adversarial audit: weighted Yamabe heat-trace comparison

Problem 30001168 / OWR-3389-021, ranked record 821  
Audit date: 6 October 2026  
Disposition: **ACCEPT the stated dimension-three counterexample.**

No mathematical correction to the frozen proof was required. This is an
independent AI analytic and computational review, not a claim of independent
human peer review, formal proof-assistant verification, publication, or
historical priority.

## 1. Exact claim accepted and exclusions

The accepted result is the existence of one smooth, strictly positive weight
W on the standard round S³ satisfying

    integral W^(3/2) dv_round = 2 pi²

for which the normalized weighted Yamabe heat trace at one specified
positive time exceeds 13/20, whereas the round comparison trace is less
than 129/200 at every positive time. The exact rational gap between those
thresholds is 1/200. Thus the assertion quantified over every n>=3 is false.

This is a full negative answer to that universal assertion. It is not a
classification by dimension. The n>=4 restriction of the comparison and
problem 30001169, the separate monotonicity assertion, are not resolved by
this audit or counted as solved here.

The frozen author ZIP has 14,945 bytes and SHA-256
6c9ac2c22c5cb50da08c55e12a97a309e5f0b1108dbcb2ac32fa284f93da0987.
Its eight regular-file members are preserved byte-for-byte in author/.
Its manifest SHA-256 is
d7f0d673dce90072e3e5b4fec31a5b002cbbeb9ba885468878ca9d27abe6b33a.
The author files' pending-audit status remains a historical statement in
that immutable snapshot. This document supplies the subsequent verdict.

## 2. Source and scope gate

The primary question was independently checked in section 9, item (16),
printed pages 421–422 of *Low Eigenvalues of Laplace and Schrödinger
Operators*, Oberwolfach Reports 6 (2009), 355–428:
[DOI](https://doi.org/10.4171/OWR/2009/06),
[official EMS PDF](https://ems.press/content/serial-article-files/46205).
The operator, positive smooth weight, round-volume normalization and n>=3
quantifier agree with the authored theorem. No Yamabe-minimizer,
constant-scalar-curvature, curvature-sign or weight-amplitude restriction
appears there. The conformal-metric realization is expressly identified
by the source. Conjecture 2 has the different n>=4 scope.

The official EMS target pages were read as text and visually inspected.
Independent rerendering from the hash-verified PDF reproduced the inspected
page images byte-for-byte. The alternate official MFO PDF was independently
text-extracted and checked at the same printed pages. The public AIM
version of the problem list also agrees at item (16):
[AIM problem list](https://aimath.org/WWN/loweigenvalues/loweigenvalues.pdf).

All three full supplied corpora were independently hashed and parsed.
The complete target record plus its absent research-report value `{}` was
reconstructed from the full corpora; its canonical digest agrees with the
ranked catalog. The complete adjacent record was separately reviewed to
prevent scope leakage. Counts, byte sizes and digests are recorded in
SOURCE_VERIFICATION.json without republishing dataset contents.

The older record's reference to the solved half-line Hardy inequality
concerns another problem. Its primary abstract was checked:
[Ekholm–Frank, arXiv:math/0611247](https://arxiv.org/abs/math/0611247).
It is not evidence resolving this weighted-sphere comparison. Targeted
current searches found no published exact resolution; those searches are
not exhaustive and establish no priority claim. Historical repository
search metadata in the author snapshot is not claimed as a fresh repository
audit. No remote repository action or external outreach was performed.

## 3. Construction: smooth, positive and on the required sphere

Let C=R x S² with product metric g_c and stereographic radial coordinate
r=e^s. Direct substitution gives

    g_round = sech²(s) g_c.

The author's cutoff chi is smooth, takes values in [0,1], and is constant
outside [0,1]. Flatness at its endpoints follows from the usual function
exp(-1/x), extended by zero for x<=0. With L=10000 and q=|s|-L/2,

    u = exp(-chi(q) log(cosh(q))),
    g_L = u² g_c,

u equals one on the entire middle cylinder. The nonsmooth point of |s| is
harmless because the resulting function is locally constant there. At
q=0, flatness of chi makes the transition match the constant jet. At q=1,
flatness of 1-chi makes it match the full jet of sech(q). Thus no
piecewise-smooth metric or distributional curvature is introduced.

Outside each transition, u=sech(|s|-L/2). Relative to g_round the weight is
W_L=u² cosh²(s). At either missing pole, using the appropriate small
stereographic radius rho, elementary algebra gives

    W_L = e^L (1+rho²)² / (1+e^L rho²)².

This is a smooth function of the Cartesian squared radius and has the
strictly positive finite value e^L at the pole. The large constant is
mathematically finite; floating-point representability is not a
hypothesis. The middle and pole formulas therefore define a smooth,
strictly positive global weight on the original S³, with no change of
smooth structure or topology. Multiplication by the subsequent positive
normalizing constant preserves these properties.

## 4. Operator and quadratic-form audit

In dimension three the geometric conformal Laplacian is

    Y_g = Delta_g + R_g/8,

with positive Laplace convention. Hence the round potential is 6/8=3/4.
For h=W g_round, covariance gives

    Y_h = W^(-5/4) Y_round W^(1/4).

The volume form is W^(3/2) dv_round, so U f=W^(3/4)f is unitary from
L²(dv_h) to L²(dv_round). Multiplying the three weight exponents on each
side yields exactly

    U Y_h U^(-1) = W^(-1/2) Y_round W^(-1/2).

In particular, this is the requested weighted operator, not merely an
analogous Laplacian on a conformal metric. The equality holds first on
smooth functions and then for the self-adjoint realizations by their
closed forms. Smooth positive weights on a compact manifold give bounded,
invertible multiplication maps on the required Sobolev spaces.

For completeness the positivity is strict: for nonzero f, the weighted
form is the round form applied to W^(-1/2)f. The round form is bounded
below by (3/4)||W^(-1/2)f||², hence by
(3/(4 max W))||f||². Smooth ellipticity on compact S³ gives compact
resolvent and trace-class heat operators for positive time. No positivity
of the cap scalar curvature is assumed or needed.

On the exact product cylinder, scalar curvature is 2, so the potential is
1/4 and

    Y = -d²/ds² + Delta_S² + 1/4.

The S²-constant Dirichlet modes have eigenvalues
mu_k=1/4+(pi k/L)². Their zero extensions to S³ are H¹ functions because
their boundary traces vanish. Distributional first derivatives have no
interface delta: the function values agree at zero. Normal-derivative
jumps concern second derivatives and do not add a term to the quadratic
form. Equivalently, approximate the Dirichlet functions in H¹ by interior
smooth functions and extend those by zero.

The resulting modes are orthogonal both for the L² inner product and
for the form. On the span of the first k, the largest Rayleigh quotient
is exactly mu_k. Closed-manifold min–max with all multiplicities then
gives lambda_k<=mu_k. No boundary condition has been imposed on the actual
closed operator. The k-dimensional trial space suffices regardless of
other transverse modes or cap-localized modes. Summing the individual
inequalities e^(-4 lambda_k)>=e^(-4 mu_k) proves the stated trace lower
bound. This is a finite-L variational comparison, not an assertion of
spectral convergence or cap decoupling.

## 5. Volume, Gaussian sum and time normalization

The cylinder volume is 4 pi L. Each cap contributes at most 4 pi times

    1 + integral from 1 to infinity of 8 exp(-3q) dq
      = 1 + 8/(3e³) < 2.

Thus V_L<=4 pi (L+4). The inequality uses only 0<u<=1 in the unit
transition and sech(q)<=2 exp(-q) beyond it. There is no omitted
transition-length or spherical-area factor.

The positive decreasing function G(x)=exp(-4 pi²x²/L²) obeys

    sum from k=1 to infinity G(k)
      >= integral from 1 to infinity G(x) dx
      >= L/(4 sqrt(pi)) - 1.

The latter bound is positive at the specified finite L; this matters when
replacing the volume by its upper bound.

Now a=(2 pi²/V_L)^(2/3), h=a g_L and W=a W_L. The normalized volume
is a^(3/2)V_L=2 pi², exactly the weight constraint with the round measure.
Because Y_h=a^(-1)Y_gL, the time is t_*=4a. Both the operator exponent
and prefactor give

    t_*^(3/2) Tr exp(-t_*Y_W)
      = (16 pi²/V_L) Tr exp(-4Y_gL)
      >= (sqrt(pi)/e) (L-4 sqrt(pi))/(L+4).

The powers 2/3 and 3/2, the factor 16 pi², and the rescaled time have all
been independently recomputed. Applying the enclosures
1.772<sqrt(pi)<1.773 and e<2.719 in the indicated positive factors gives

    (1772/2719) * (10000000-7092)/10004000
      = 1106714561/1700054750
      > 13/20.

This lower bound is strictly above 0.650987599664069. The use of L=10000
is explicit and fixed; no unquantified sufficiently-large-L step remains.

## 6. Round comparison: every time, every multiplicity

Degree j-1 round S³ harmonics have multiplicity j² and Laplace eigenvalue
j²-1. Including the potential produces lambda=j²-1/4. Thus the series in
the author's Lemma 1 is exactly the full heat trace.

For 0<t<=1, differentiating the Gaussian Poisson identity yields the
stated theta correction with coefficient 1-2 pi²m²/t. Every correction
is negative, and e^(1/4)<4/3. Consequently the bound 1773/3000<129/200
is valid uniformly down to arbitrarily small positive t. The power of t,
factor sqrt(pi)/4 and sign of the differentiated correction all check.

For 1<=t<=2, the author's intervals cover the entire closed range with
no endpoint gap. For j>=4 the ratio of consecutive spherical summands
is at most (25/16)e^(-9)<1/2. Twice the j=4 summand is therefore a valid
upper tail. On [a,b], replacing t^(3/2) by b sqrt(b) and every decaying
exponential by its value at a has the right inequality direction.
The upper square-root bracket and reciprocal positive Taylor polynomial
are strict upper bounds. Replaying all 100 exact comparisons gives the
recorded maximum below 0.643380136594, strictly below 129/200.

For t>=2, each summand t^(3/2)e^(-lambda t) is nonincreasing because
lambda>=3/4. Comparing summands at two times and summing is sufficient;
no questionable derivative/sum exchange is needed. The endpoint t=2
was already included in the finite certificate. All positive times are
therefore covered.

### Independent numerical certificate

The audit supplies a second implementation without importing the author's
certificate or reusing its exponential or square-root routines:

- 200 intervals of width 1/200 rather than 100 of width 1/100.
- Four explicit spherical modes; the tail beginning at j=5 is bounded
  by 50 exp(-99a/4), using ratio (36/25)e^(-11)<1/2.
- To bound exp(-x), reduce x by 512, bracket the alternating Taylor
  series between degrees 15 and 16, then square nine times. Rational
  outward rounding at every stage preserves the interval.
- Square roots use integer bisection and exact rational squaring.
- Pi is bracketed using pi=4 atan(1/2)+4 atan(1/3), independently of the
  author's Machin implementation; e uses a degree-20 positive series
  with a proved geometric upper tail.

It proves the same strict separation with a stronger middle-range
upper bound below 0.640842149351329. This is a certified upper bound,
not an estimate of the exact maximum. All acceptance tests use integers
and fractions; decimal strings are only outward-rounded presentation.

## 7. Literal maxima and admissibility conclusion

At zero time the common volume-normalized leading heat coefficient is
sqrt(pi)/4. At infinity each scaled trace tends to zero by strict
positivity and compact elliptic heat-trace estimates. Continuity holds
at positive time. The constructed value exceeds the zero-time limit.
The round first mode at t=2 alone exceeds 0.631107397280160, also above
the zero-time limit. Both suprema are therefore attained inside a compact
positive-time interval. The source's word max causes no defect.

Every required hypothesis is met: fixed n=3; original round sphere;
smooth strictly positive normalized weight; correct two exterior weight
powers; correct Hilbert space; and a strictly larger global comparison
quantity. The smaller-time failure of n=3 monotonicity mentioned in the
source is not being mistaken for the present maximum comparison.

## 8. Computational adversarial checks and release boundary

Both author replays passed in isolated Python under normal and optimized
execution. The independent audit verifier also passes in both modes.
All eight author members were checked against the frozen ZIP.

The supplied independent control runner performs 34 expected-outcome
checks, including both optimization modes and relocated paths containing
spaces with a foreign working directory. All 34 passed:
4 relocated baselines were accepted and 30 corrupt/false variants rejected.
Controls cover missing and extra files, bytecode-cache directories,
symlinks, FIFOs, same-size corruption, wrong reproduced output after
rehashing, changed frozen-author identity, falsely tight round thresholds,
and too-short cylinders after rehashing. The mathematical negative
controls reach actual failed inequalities rather than merely failing a
stale file hash. No assert statement is relied upon for acceptance.

The package verifier enforces the exact regular-file inventory before
reading payloads and rejects nonregular entries and unexpected folders.
A manifest authenticates all payload bytes relative to the external
receipt; it is not a proof of the analytic mathematics. Neither are the
613 author checks or 200 independent intervals substitutes for Sections
3–7 of this audit.

Only authored proof, audit, code, results and public provenance metadata
are packaged. Source PDFs, extracted text, dataset contents and private
coordination files are excluded. Original author files and source corpora
were not modified. No correction patch is necessary. Publication remains
a separate action; no publication or outreach occurred in this audit.
