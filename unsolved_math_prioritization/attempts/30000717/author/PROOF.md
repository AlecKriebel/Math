# Exact sum-of-squares certificates fail for the Robinson sextic

Problem 30000717 / OWR-1465-011. Author candidate, 7 October 2026.

## 1. Statement and scope

Write S = R[x,y,z] and let ΣS² be the cone of finite sums of squares of polynomials with real coefficients. For f in S define two different ideals:

- J_f = (y f_x − x f_y, z f_x − x f_z, z f_y − y f_z), the tangency-minor ideal in the catalogue statement.
- K_f = (y f_x, x f_y, z f_x, x f_z, z f_y, y f_z), the literal separate-cross-product interpretation of the printed formula in the publisher's Oberwolfach report.

The source formula and its catalogue normalization are not identical. Section 8 explains why this distinction does not affect the main negative answer.

**Theorem.** The classical Robinson form

R = x⁶ + y⁶ + z⁶ − x⁴y² − x²y⁴ − x⁴z² − x²z⁴ − y⁴z² − y²z⁴ + 3x²y²z²

is nonnegative on R³, but, for every real ε≥0,

R+ε ∉ ΣS² + √J_R, and R+ε ∉ ΣS² + √K_R.

In fact, neither certificate exists if the ordinary radical is replaced by the entire ideal of polynomials vanishing on the corresponding real variety.

Thus the proposed four-way equivalence is false: its global nonnegativity condition (i) implies neither its exact certificate condition (iii) nor its epsilon certificate condition (iv). This resolves the catalogue question negatively and also refutes the literal-cross-product interpretation of the source's four-way equivalence. The epsilon obstruction is stronger than needed for (iv), since membership fails for every ε≥0 even with the radical in place of the original ideal.

The example has infimum zero, attained at the origin and elsewhere. Removing an attainment assumption asks for a statement valid for all polynomials, including those whose infimum is attained; it does not impose nonattainment. No claim about the smaller class consisting only of nonattaining polynomials is needed for this counterexample.

## 2. Nonnegativity, with no theorem input

Put a=x², b=y², c=z². The symmetric cubic

F(a,b,c) = a³+b³+c³ − a²b−ab²−a²c−ac²−b²c−bc² + 3abc

satisfies

F = (a−b)²(a+b−c) + c(a−c)(b−c).

By symmetry we may order a≥b≥c≥0. Both terms on the right are then nonnegative. Therefore R=F(x²,y²,z²)≥0 on R³. Also R(0,0,0)=0, so inf R=0.

## 3. Ten zero directions determine every cubic

Let Z consist of the following ten vectors, with each indicated sign chosen independently:

- (1,s,t), s,t∈{−1,1}, four vectors;
- (1,s,0), s∈{−1,1}, two vectors;
- (1,0,t), t∈{−1,1}, two vectors;
- (0,1,t), t∈{−1,1}, two vectors.

Direct substitution gives R(v)=0 for every v∈Z. Since R is homogeneous of degree six, R(tv)=0 for every real t.

**Lemma.** A homogeneous cubic p vanishing on Z is identically zero.

**Proof.** The six vectors with one zero coordinate force p to have the form

p = A x(x²−y²−z²) + B y(y²−x²−z²) + C z(z²−x²−y²) + D xyz.

Indeed, substitution at (1,±1,0) equates the x³ and xy² coefficients with opposite signs, and the y³ and x²y coefficients with opposite signs. The other two pairs give the remaining analogous equations. At (1,s,t) the displayed cubic has value

−A − Bs − Ct + Dst.

Summing these four equations against the four sign characters 1,s,t,st gives A=B=C=D=0. ∎

Consequently, a homogeneous polynomial p_d of any degree 0≤d≤3 that vanishes on Z is zero: the cubic x^(3−d)p_d vanishes on Z and hence is the zero polynomial, so p_d=0 in the integral domain S.

For a reproducible independent arithmetic check of the lemma, order Z as (1,1,1), (1,1,−1), (1,−1,1), (1,−1,−1), (1,1,0), (1,−1,0), (1,0,1), (1,0,−1), (0,1,1), (0,1,−1). Order cubic monomials as z³, yz², y²z, y³, xz², xyz, xy², x²z, x²y, x³. The 10×10 evaluation determinant is −128.

## 4. The relevant varieties contain the zero lines and an axis

Every point tv, v∈Z, is a global minimizer of the differentiable polynomial R. Hence its gradient is zero. It follows that every generator of J_R and K_R vanishes there.

This can also be checked from the explicit derivative

R_x = 2x(3x⁴−2x²y²−y⁴−2x²z²−z⁴+3y²z²)

and its coordinate permutations.

On the first coordinate axis (t,0,0), the gradient is (6t⁵,0,0). Every cross-product appearing in K_R vanishes, as do all differences defining J_R. Thus this entire axis is contained in both real varieties, and

R(t,0,0)=t⁶.

## 5. The exact certificate contradiction

Let L be either J_R or K_R, and fix any real ε≥0. Suppose for contradiction that

R+ε = q_1² + ⋯ + q_m² + h, with h∈√L.

At each real point w of V(L), h(w)=0: some positive power h^N belongs to L, so h(w)^N=0. The following argument actually requires only that h vanish on V(L)∩R³.

For v∈Z and every real t, Section 4 and the certificate give

ε = Σ q_j(tv)².

Each univariate real polynomial q_j(tv) is bounded in absolute value by √ε on the whole real line, so it is constant. Equivalently, the nonzero leading coefficients of real squares cannot cancel. Write q_j=Σ_d q_{j,d} as a finite sum of homogeneous parts. Since Σ_d t^d q_{j,d}(v) is constant, its positive-degree coefficients satisfy

q_{j,d}(v)=0 for every d≥1 and every v∈Z.

Section 3 implies q_{j,1}=q_{j,2}=q_{j,3}=0. Constants are allowed when ε>0; they are not discarded.

Now restrict the certificate to the first coordinate axis, where h vanishes. It gives

t⁶+ε = Σ q_j(t,0,0)².

Every polynomial q_j(t,0,0) has degree at most three: otherwise, if D>3 were the largest degree of these finitely many restrictions, the coefficient of t^(2D) in the right-hand side would be a nonempty sum of squares of nonzero real leading coefficients, hence strictly positive. This contradicts the degree-six left-hand side.

But the degree-one, degree-two, and degree-three homogeneous parts of every q_j have already been shown to vanish identically. Its restriction to this axis, of degree at most three, must therefore be constant. The right-hand side is consequently constant, contradicting t⁶+ε. This proves the theorem for every ε≥0. ∎

For ε=0 alone there is also a shorter order argument: all q_j vanish on each zero line, so the cubic lemma eliminates their homogeneous parts through degree three, including constants. On the axis the right-hand side is then divisible by t⁸ and cannot equal t⁶. The argument above handles positive ε without making that invalid constant-term inference.

There is no restriction on the degrees or number of SOS summands. No assumption that either ideal is radical, real radical, zero-dimensional, or generically reduced is used. In particular, the argument does not rely on a classification of complex eigenpoints or on a numerical SDP failure.

## 6. The real-variety condition for the tangency ideal remains valid

For every polynomial f in n variables, global nonnegativity is equivalent to nonnegativity on the real zero set of the tangency minors x_j f_i−x_i f_j.

Only the reverse direction needs proof. If f(x₀)<0 and x₀=0, the origin itself belongs to the tangency variety. Otherwise minimize f on the compact sphere of radius ||x₀||. A minimizing point u has f(u)≤f(x₀)<0. By the Lagrange multiplier condition, ∇f(u)=λu, so every tangency minor vanishes at u. Thus nonnegativity on that variety precludes any negative value. This proof does not require boundedness below or attainment of the global infimum.

The Robinson example therefore has both (i) and (ii) true and both (iii) and (iv) false. It does not contradict the familiar gradient-ideal theorem: for the actual gradient ideal, Euler's identity gives 6R=xR_x+yR_y+zR_z, so R already belongs to that ideal.

## 7. Additional diagnostic for the literal product interpretation

This section is distinct from the main exact-certificate obstruction. For

Q(x,y)=(1−xy)²+y²−1/2,

the literal product ideal is K_Q=(yQ_x,xQ_y), where

yQ_x=2y²(xy−1),  xQ_y=2x(x(xy−1)+y).

If both vanish at a real point, the first equation implies y=0 or xy=1. In the first case the second becomes −2x²=0, so x=0. In the second case the second equals 2xy=2, a contradiction. Therefore V(K_Q)∩R²={(0,0)}. Yet Q(0,0)=1/2, while Q(2,1/2)=−1/4.

Moreover Q>−1/2 everywhere: equality would require y=0 and xy=1 simultaneously. On (x,y)=(1/t,t), t≠0, Q=t²−1/2, so inf Q=−1/2 is not attained. Hence the literal-product version even fails (ii)⇒(i) within a genuinely nonattaining example.

This assertion is not made for the catalogue tangency-minor ideal; Section 6 proves its (i)⇔(ii).

## 8. Source fidelity and attribution

The primary report's Theorem 1, printed p.810, contains the exact radical certificate as item (iii). Conjecture 2 on p.811 proposes replacing its gradient ideal; the rendered display visibly lists the separate products with an ellipsis, not a minus sign. The catalogue instead explicitly uses pairwise differences. Both are treated above, without silently repairing the publisher's notation. An intended correction by the original author has not been verified.

The polynomial R is Robinson's classical nonnegative non-SOS sextic, not a newly discovered polynomial. Its formula is already recorded in Bruce Reznick's contribution to the same report, printed p.798, equation (2). The ten-zero cubic obstruction is classical in the study of this form. The use here is the explicit zero-line/axis contradiction for the proposed exact certificates. No exhaustive historical-priority or novelty claim is made.

This is an AI-assisted, unrefereed mathematical candidate prepared for independent audit, not a claim of formal proof certification or conventional human peer review. The self-contained argument above proves the result; the exact controls check its algebra and are not a substitute for the argument.

Primary public source: Reelle Algebraische Geometrie, Oberwolfach Reports 14/2007, https://doi.org/10.4171/owr/2007/14 ; publisher PDF https://ems.press/content/serial-article-files/46100 . See SOURCE_ASSESSMENT.md for the formulation and literature boundaries.
