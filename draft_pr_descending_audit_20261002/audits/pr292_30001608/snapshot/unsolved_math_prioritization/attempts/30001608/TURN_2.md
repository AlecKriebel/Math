# Turn 2: a nonlinear Foster function extends stability to lambda<2

**Scoped partial; the original all-load conjecture remains unresolved.** This is the second substantive author turn, continuing the exact2011 six-rate generator. The source gate and the first-turn files remain unchanged as historical checkpoints. This turn proves a genuinely larger stability range, including every1<=lambda<2, using a quadratic function rather than repeating the affine argument.

## 1. Exact nonlinear identity

Let s=(a,b,x,y), D=x+y+1, n=x+y, S=a+b+x+y, and

Z=a+x-b-y,       W=2a+2b+x+y.

For0<lambda<2 choose

c=2/lambda>1,       K=3+c,
V=Z²+c(a²+b²)+K W.

This function is nonnegative and coercive on Z_+^4 because K W>=K S. Its increments are evaluated under exactly the source generator, retaining the seed terms. Direct expansion gives

D LV = P3+P2+P1+P0,

P3 = -2c(a²x+b²y),

P2 = -2c(a²+b²)-2(x²+y²)+4(ay+bx)-3(ax+by)-2cxy,

P1 = -(a+b)+(7lambda+4-c)(x+y),

P0 = 7lambda+6.                                           (1)

Here Pj is homogeneous of degree j in the state. In particular, the cubic part is nonpositive, and all mixed terms except ay and bx have a favorable sign. This calculation uses the first-turn exact identities for LZ² and LW and

D L(a²+b²)
 = lambda(a+b+1)D
   +(-2a+1)a(x+1)+(-2b+1)b(y+1).

The independently written direct finite-difference checker verifies the full polynomial identity, including all coordinate boundaries.

## 2. Uniform negative drift outside a finite set

Put delta=2(c-1)/(c+1)>0. Young's inequality gives

4ay <= (c+1)a²+4y²/(c+1),

so

2c a²+2y²-4ay >= (c-1)a²+delta y² >= delta(a²+y²).

Apply the same inequality to b,x. Dropping the other nonpositive terms in P2 gives

P2 <= -delta(a²+b²+x²+y²) <= -(delta/4) S².

Let B=max(7lambda+4-c,0), C=7lambda+6. Equation(1) implies

D LV <= -(delta/4)S²+B S+C.                              (2)

Choose any integer R>=1 with R>4(B+C+2)/delta. If S>=R, then

(delta/4)S² >= (B+C+2)S >= (B+1)S+(C+1),

and (2) gives D LV<=-(S+1). Since D<=S+1, this proves

LV<=-1 outside the finite set {S<R}.                    (3)

The chain is nonexplosive and irreducible by the first-turn pathwise proof. Apply stopped Dynkin to the nonnegative coercive V, with finite-level localization, and then remove the cutoff. It follows that the expected entrance time into {S<R} is at most V(s) from every state outside that set. The standard finite-set hitting-time criterion therefore yields positive recurrence and a unique stationary probability law at every fixed0<lambda<2.

This theorem includes the previously unproved interval1<=lambda<2. It does not establish the target for lambda>=2. The growth of the displayed constants as lambda approaches2 is genuine for this certificate and must not be suppressed in the conclusion.

## 3. How the new certificate uses majority imbalance

The cohort imbalance Z counts all peers committed to the two possible first-chunk orders, including waiting-room peers. Its exact drift is only the seed-scale term (y-x)/D, whereas its squared drift includes the restoring product -2Z(x-y)/D. The waiting-room square terms control the mismatch between cohort imbalance and current chunk imbalance. The workload term controls the balanced chunk-rich direction where Z and the waiting-room squares alone would not be coercive. All three terms are needed for the displayed global estimate.

This is an exact statewise argument, not an inference from a large-system trajectory, a diffusion approximation, or an unproved majority-switching average.

## 4. Exact high-load obstruction within this quadratic family

The argument does not merely fail because K was chosen crudely. Consider the broader family

V_(c,K)=Z²+c(a²+b²)+K W,       c>0, K>0.

For lambda>=2 no member has LV<0 outside a finite set. This claim is restricted to this family, not to all quadratic functions.

On states (a,b,x,y)=(t m,0,0,m), the leading degree-two part of D LV is

m² F(t),    F(t)=-2c t²+(lambda c+2)t-2.               (4)

The maximum over t>=0 is attained at t=(lambda c+2)/(4c) and equals

(lambda c+2)²/(8c)-2 >= lambda-2,

where the inequality follows from (lambda c-2)²>=0. The workload contributes only terms of degree one on this face. Thus for lambda>2, F is positive at some positive rational t, and an integer sequence on that ray has positive drift eventually, independently of K. At lambda=2 the maximum is positive unless c=1. If c=1, use the exact integer states (m,0,0,m). Direct evaluation gives

LV = [(8+2K)m+4+4K]/(m+1)>0.

Consequently this family cannot settle the remaining critical or high-load range. This is only a certificate obstruction; it does not prove instability. It suggests that a different nonlinear dependence, a boundary-layer correction or a time-averaged return argument is needed.

## 5. Scope and continuity

The original conjecture remains positive recurrence for every fixed lambda>0 under the invisible-waiting-room denominator X+Y+1. We have now proved it for0<lambda<2. The remaining range is lambda>=2. The superseded2009 conjecture and the different majority/common-chunk algorithms are not used as evidence for either answer. The two author turns use one continuing Foster/imbalance approach family, with the second delivering a nonlinear range extension and an exact limitation of that certificate family. Classical Foster reasoning and elementary inequalities are credited; no historical novelty is certified.
