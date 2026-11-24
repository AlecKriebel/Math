# Audit of the independently authored EP1038 interval kernels

Public edition dated 2026-10-12. This retains the complete substantive mathematical report, with transparent editorial changes to private references and review-status wording. Independently authored executable checkers, raw interval certificates, full numerical records, detailed diagnostic outputs, and source copies are not included. Hashes identify omitted evidence but do not provide executable public reproducibility. The work is AI-assisted and unrefereed, with no external human peer review or formal proof-assistant certification.

## Disposition and scope

The frozen kernels listed below have a sound real-enclosure interpretation on
their documented, actually used input domains. Their directed arithmetic,
logarithm and exponential remainders, square root and trigonometric routines
where present, derivative propagation, and parameter-uniform root-bracketing
and Newton-contraction logic are accepted within that scope. No unresolved
mathematical enclosure error was found in these versions.

This is **not acceptance of Certificate 6.1, Certificate 7.1, or the proposed
resolution of EP1038**. In particular it does not establish exhaustive slab
coverage, the correctness of every scalar reduction or reference-family
formula, the original analytic reduction to those inequalities, the final
lower bound for arbitrary polynomials, or nonattainment. Those require the
separate certificate and implication audits. Sound interval operations do
not prove that the right mathematical quantity was submitted to them.

No source-author verifier, source-author executable code, Lean development,
or third-party numerical package was executed. Only newly authored kernels
were imported, after verifying their exact byte hashes. The independent
tests use Python's standard library and exact rational arithmetic.

## Frozen targets

Frozen implementation identities (source programs are omitted):

1. One-cut minimum arithmetic at scale 2^240: SHA-256 `604c89d60cb6640f3c965b6037249e379e56e013e1d37bf7ff17368061bfc992`. Its interval classes, log/exp, first- and second-order jets, soft positive series, bulk/soft/tail root routines, and relevant guards were statically read in full.
2. Finite-reference arithmetic at scale 2^160: SHA-256 `48b28eb878de3d868d25ab4b23fdf34752fa0eb7b621df41e62b49f43c82e43d`. All interval primitives, log/exp, integer square root, Machin pi construction, trigonometric enclosure, root routine, and domain-guard call sites were statically read in full.
3. Terminal-reference arithmetic: SHA-256 `2020a31e3db7e7c2c4c0275660d68448d4f6a70f6916a380c2f668c2b6e9921c`. It uses implementation 2. Its elementary operations and root-validation call sites were reviewed. It was not executed in this kernel audit. Its terminal scalar formulas, parameter coverage and complete run are not accepted by this kernel report alone.

Two additional frozen inputs were read for the root-selection interface: the one-cut proof note, SHA-256 `81e95dd1f0376ca72e83c3299a139fd7fca9ee304d351b736cc34b5a39db3916`, and the raw one-cut integer certificate, SHA-256 `01a37c997aa6c705b7dc48995f7d731848eccabe802136097a07c31762818e9a`. A public edition of the former is `CERTIFICATE_6_1_PROOF.md`; the latter is omitted.

Reading their root/endpoint argument and metadata did not confer whole-certificate acceptance. The aggregate verification metadata identifies the separate final tests and end-to-end acceptance. All limitations of this kernel-only review remain explicit below.

## 1. Directed arithmetic

At scale S, integer endpoints a<=b denote the closed interval [a/S,b/S].
Every lower division is floor division. Every upper division uses
the integer identity −floor(−a/b)=ceil(a/b), including negative numerators or
denominators. The elementary identity floor(-t)=-ceil(t) proves the upper
rule; there is no truncation-toward-zero assumption.

Addition and subtraction are exact on the lattice. Multiplication uses all
four corners, whose minimum and maximum are the extrema of the bilinear
product over a real rectangle, then rounds outward. Reciprocal rejects any
interval containing zero, including a zero endpoint. On either component
of the nonzero real axis, reciprocal is decreasing, so its exact extrema
are S/b and S/a; storing these at scale S requires S^2/b and S^2/a. Both
kernels use exactly this rule. Negative denominator cases are therefore
covered, not assumed positive.

Both intersection methods fail on a reversed result. An intersection can
be used only when both operands contain the same sought quantity; this is
proved for Newton below. Squaring includes zero when the input does. General
integer powers are repeated sound products. They can overestimate, especially
in Certificate 7.1 where ordinary multiplication implements exponentiation,
but do not exclude the true values.

Certificate 6.1 converts ordinary values through Fraction. A supplied binary
float consequently denotes its exact binary rational, not an asserted exact
decimal. That is sound for untrusted proposals. Its replay only constructs
proof boxes from integers. Certificate 7.1 decimal strings are parsed by
integer numerator and a power-of-ten denominator, and its rational helper
uses directed division. The final raw constructors reject non-integer
endpoints.

The Certificate 7.1 constructor has a limited API: decimal-string and
interval-copy calls must have no second endpoint. Those branches ignore a
supplied second endpoint; interval formation from string endpoints must use
the explicit endpoint-box constructor. Every reviewed certificate call follows this convention. This
report does not claim the class implements an arbitrary two-string
constructor. Exponents must be integers. Interval endpoint members must not
be modified to non-integer or reversed values after construction.

## 2. Square root and transcendental enclosures

### Square root

Certificate 7.1 rejects a negative lower input endpoint and uses the integer floors of sqrt(aS) and sqrt(bS). The lower integer l satisfies
l^2<=a*S<(l+1)^2. The upper endpoint is h if h^2=b*S and h+1 otherwise.
This includes zero and exact squares. No floating square root enters this
primitive.

### Logarithm

Both public log functions require a strictly positive argument. An exact
endpoint is scaled by a power of two, with its exponent selected from integer
bit length. The reduced input lies in [1,2], with directed conversion where
needed. No floating exponent selection is trusted.

For t=(y-1)/(y+1), the positive expansion is

    log(y) = 2 sum(j=0..N-1) t^(2j+1)/(2j+1) + R,
    0 <= R <= 2 t^(2N+1) / ((2N+1)(1-t^2)).

This follows by replacing every omitted positive denominator by 2N+1 and
summing the geometric series. Certificate 6.1 uses N=96; Certificate 7.1
uses N=56. The latter accepts t<=1/2, accommodating outward rounding near
1/3. Its remainder is valid on that whole admitted domain. The former's
new explicit reduced-chart guard requires 1<=y<=2. Outward interval
operations absorb all term-rounding error; even a sub-lattice-unit remainder
is rounded upward rather than dropped.

The same construction encloses log(2). Adding k*log(2) handles negative k
by ordinary signed interval multiplication. Monotonicity justifies endpoint
evaluation for a whole log interval. Reusing a cached endpoint result has no
effect on the mathematics because the scale and functions are fixed.

### Exponential

Certificate 6.1 reduces a nonnegative argument to v<=1/8, sums through
v^60/60!, and bounds the remainder by

    (v^61/61!) / (1-v/62).

The successive omitted term ratios are at most v/62. Certificate 7.1
reduces to v<=1, sums through degree 60, and uses the simpler upper bound
2/61!: the omitted terms are at most (1/61!)/(1-1/62)<2/61!.

Both then square the full interval once per halving, with outward rounding
at each step. Negative arguments use reciprocal of the positive-argument
result. Arbitrary intervals use monotonicity. Very small positive outputs
may round to an interval starting at zero; that is a valid enclosure, though
it cannot subsequently be inverted. No epsilon padding is used to certify
these functions.

### Pi and trigonometric functions

Certificate 7.1 encloses pi by the Machin identity

    pi = 16 atan(1/5) - 4 atan(1/239).

Each arctangent has 120 alternating terms and a symmetric next-term error
bound. For its actual positive inputs below one, the terms decrease to zero,
so this remainder is rigorous. The small-argument arctangent helper has that mathematical
precondition rather than a full general-purpose input guard; no other input
is accepted here.

The integer period proposal m uses floating arithmetic, but the reduced
interval x-2m*PI uses the entire certified pi interval, and the code checks
it lies in [-4,4]. Thus a wrong proposal either still yields a valid
reduction or fails. The cosine polynomial ends at degree 72 and the sine
polynomial at degree 73. Treating each as also including its next zero
coefficient, Taylor's theorem bounds the errors by 4^74/74! and 4^75/75!,
respectively: all real derivatives of sine and cosine have absolute value
at most one. Each polynomial is interval-evaluated over the reduced box.

For a nonpoint input, endpoint values alone would be insufficient. The
implementation also enumerates every critical point n*pi for cosine and
pi/2+n*pi for sine. Floating arithmetic proposes the search window; exact
interval inequalities verify that the outer critical points lie strictly
beyond the input at both ends. Since pi>0, every possible intervening
critical point is then enumerated. Whenever its interval overlaps the input,
the exact extremal value +1 or -1 is included. Extra points only enlarge the
answer. Negative periods and intervals straddling extrema are covered.

## 3. Jets, soft-series derivatives and domain preservation

Certificate 6.1's second-order jet stores actual derivatives, not
factorial-normalized Taylor coefficients. Its product has the required
2*f'*g' term, and its reciprocal second derivative is
2*(f')^2/f^3-f''/f^2. The first-order three-coordinate jet uses the ordinary
componentwise chain and product rules. Its negative/noninteger exponent
cases now fail explicitly instead of silently returning the empty product.

The bulk derivatives were independently differentiated. In particular
q'=q/r^2, q''=q(1-2r)/r^4, and for
W=log(z-q^2)-log|1-z|,

    W_z  = 1/(z-q^2)+1/(1-z),
    W_zz = -1/(z-q^2)^2+1/(1-z)^2,
    W_r  = -2*q*q'/(z-q^2),
    W_rz = 2*q*q'/(z-q^2)^2,
    W_rr = -2*((q')^2+q*q'')/(z-q^2)
           -(2*q*q')^2/(z-q^2)^2.

The code agrees, including on the z>1 branch. Its implicit second derivative
uses -(G_rr+2*G_rz*z'+G_zz*(z')^2)/G_z, with the denominator required nonzero
by the bracket/slope tests. All inputs are simultaneous enclosures on the
same parameter slab; forgetting their dependence enlarges the result and
does not invalidate inclusion.

The soft chart uses C(y)=sum y^m/(2m)!, S(y)=sum y^m/(2m+1)! and
T(w)=sum w^m/(2m+1), summing m=0 through 32. Put K=33. For C/S with shift
sigma=0/1 and upper argument Y, the omitted value and derivative are bounded
by

    Y^K / ((2K+sigma)!*(1-r)),
    K*Y^(K-1) / ((2K+sigma)!*(1-(K+1)*r/K)),
    r = Y / ((2K+sigma+2)*(2K+sigma+1)).

The successive term ratios decrease with the index. Derivative ratios add
the factor (m+1)/m, bounded by (K+1)/K. For T, the displayed bounds replace the factorial by 2K+1 and r by Y.
Its value-term ratios are bounded above by Y and derivative-term ratios
by (K+1)Y/K for indices at least K. The value-term ratios increase toward Y,
but the stated geometric upper bounds remain valid. The input is
nonnegative; positive remainder denominators are enforced by division and
nonnegative-result guards. These are separate derivative error estimates,
not differentiation of an unqualified error bound.

Multiplying the nonnegative derivative-remainder interval by each actual
input-gradient interval is correct even for negative or sign-changing
gradients. The independent tests include negative, positive and zero
gradients. The accepted series kinds are exactly C, S and T; an arbitrary
unrecognized kind is not an accepted API input.

## 4. Uniform roots and branch identity

For a fixed closed parameter box P and root interval X=[a,b], the routines
evaluate F(P,a), F(P,b), and F_x(P,X). Strict opposite endpoint signs hold
for every parameter, while the slope interval excludes zero throughout the
whole box. Continuity and the intermediate value theorem give a root for
each parameter; strict slope sign gives its uniqueness within X.

For an exact midpoint m in X, every such root x satisfies

    x = m - F(p,m)/F_x(p,xi)

for some xi between m and x. Consequently the interval Newton intersection
with m-F(P,m)/F_x(P,X) preserves every already-established root
simultaneously. These implementations do not infer existence from mere
contraction. Their endpoint and slope tests precede all Newton rounds.

Certificate 6.1 also checks q<z_plus<1 and z_minus>1. The supplied analytic
classification was independently checked: for the plus equation in u,
the derivative numerator is q*u^2-B*u+q with
B=1+q^2-A*(1-q^2)>2q before the soft endpoint. Its reciprocal critical
points give exactly one ascending nontrivial root in (1,1/q). The minus
equation is strictly decreasing for u>1/q and has opposite infinite
endpoint limits. This identifies the locally bracketed roots without
assuming numerical continuation from overlapping projections.

Certificate 7.1 finite v2 explicitly checks the physical exterior domain
x<a and x!=0 before evaluating its displayed derivative. This matters:
K=sqrt((a-x)(2-x)) has the needed derivative formula on x<a, whereas an
unqualified use on x>2 would not. The negative and positive root sides are
also checked. Given the separate analytic premise that the reference
density is nonnegative of mass one and k>0, the negative-side potential is
strictly decreasing, while the positive-side potential is strictly concave.
Thus a certified positive-slope zero is the unique ascending main crossing.
This argument identifies the physical root; the kernel by itself only
establishes the zeros of the function supplied to it.

The terminal routine uses the same G equation as Certificate 6.1 and checks
q<z_plus<1<z_minus in its terminal-value validation. Its log and inverse domains enforce
continuity on the initial bracket used by its sign tests. Intersections
retain the root, and the final physical ordering identifies the branch.

### Singular and soft endpoints

The Certificate 6.1 tail uses q(r)=exp(-1/r), extended by q(0)=0. On
0<=r<=1/50, q and q'=q/r^2 increase, so the uniform bounds
q<=exp(-50) and q'<=2500*exp(-50) are valid. Placeholder second derivatives
in this first-order calculation are not consumed by the accepted sign test.
At r=0, the regularized root equation has roots 1/2 and 3/2 with nonzero
z derivative; its implicit continuation is legitimate.

In the last soft slab the code intentionally omits a strict lower D sign
and numerically encloses q slightly beyond the unknown q_s. This is not a
uniform root existence claim for the entire oversized numerical box. Its
application is restricted to admissible q<=q_s, where

    D(q,0)=A*(1+q)/(1-q)-1=(A-s)/s<=0.

The certified positive upper D sign and D_y>0 then give the required root,
including y=0 at q_s. The guards 1-q*C(y)>0 and
w=(q*sinh(sqrt(y))/(1-q*cosh(sqrt(y))))^2<0.03 imply
q*exp(sqrt(y))<1, so the deflation is on the correct real branch.
The positive square-root branch x=log(u)>=0 is essential to the inverse
coordinate y=x^2. The root selection and endpoint qualification are sound
with these analytic premises and must accompany any later certificate use.

## 5. Independent corroboration and negative controls

The independent test harness checks each target's exact hash before
compiling precisely those bytes. Its independent Fraction oracles evaluate
longer rational series directly, without floating transcendental functions.
It tests signed rounding; exact decimal and rational conversion; arithmetic
over positive, negative, sign-crossing and tiny intervals; zero-denominator
rejection; disjoint intersection rejection; exact integer sqrt; log/exp
points and nonpoint intervals; tiny endpoints and conservative underflow;
Machin pi; direct unreduced Taylor sine/cosine values; interior samples and
all tested critical endpoints; raw and dual jets; and soft-series values and
first derivatives.

The final run contains 2,454 exact checks, including 29 explicit rejection
controls. The check receipts give the exact test source pin. The same
tests were run under CPython 3.12.14 in normal, -O and -OO modes, and their
JSON receipts are byte-identical. Explicit exceptions implement every test
gate. Finite tests corroborate, rather than replace, the mathematical
arguments above; they do not cover a continuum by sampling.

During the audit, initial API gaps were corrected in separately frozen
versions: raw non-integer endpoints, missing physical-chart checks for the
finite potential, unsupported negative first-order dual powers, and an
unguarded reduced log helper. The final Certificate 6.1 replay also compares
recomputed decimal displays against stored metadata. No actual initial
certificate arithmetic counterexample was found; the changes prevent
misuse or misleading metadata from being accepted by the exposed interfaces.

A hash gate rejected a test run when a target had been replaced by its new
version before that version's pin was supplied. That run did not execute the
changed target. The harness was then deliberately updated to the verified
new pin and all final tests were rerun.

## 6. Exclusions and remaining acceptance gates

- This report does not execute a complete certificate run or verify every
  generated slab record. Reports of full runs from their authors are not
  substituted for an independent whole-certificate acceptance here.
- The exact finite/terminal coverage, mapping from q to k, Fourier lower
  bound formula, scalar rectangle reductions and downstream target-value
  linkage require their own acceptance. Only the elementary Fourier tail
  estimate sum(n>N) n^-3 <= 1/(2N^2) is immediate from the integral test.
- The underlying analytic reduction for arbitrary finite root
  configurations, endpoint adjoints, circle rearrangement and nonattainment
  are outside this kernel audit.
- Certificate 7.1's float proposals are validated by exact tests but its
  full generator is not a float-free replay. Its finite trigonometric
  reduction also uses validated floating integer proposals. This is not a
  dependency on floating accuracy for acceptance, though it can affect
  termination or which valid subdivisions are found.
- These are domain-specific mathematical checkers, not hardened libraries
  for arbitrary hostile Python objects, resource exhaustion, monkey-patched
  standard libraries or mutation of interval attributes after construction.
  The usual trust in the pinned Python integer/rational implementation and
  hardware remains. No formal verification claim is made.
- No source-author program, Lean code, package installer, publication,
  repository change or queue modification was performed by this audit.

This report records the complete substantive mathematical obligations for the frozen implementations and the precise assumptions that must survive their use in larger proofs. Whole-certificate and analytic acceptance is supplied separately by the end-to-end report, not by this kernel report alone.
