# Proof 05  Arithmetic progression triples and a failed multiradius extension

This is a reading edition of an accepted authored proof. Its mathematical scope is unchanged. Source and reading-edition hashes are recorded in the [inventory](../CONTENT_AND_DEPENDENCIES.md). No novelty claim is made.

Public analytic inputs and exact attribution are listed in [References](../REFERENCES.md).

## 1. The precise inequality

For every p >= 2 and a,b,c >= 0, with normalized angular measure,

E_t |a exp(it) + c + b exp(-it)|^p
>= E_t |a exp(it) + c - b exp(-it)|^p.                 (1)

For p > 2 the inequality is strict if a,b,c > 0. If p=2, or if any of a,b,c is zero, equality holds.

Set A=a+b and B=|a-b|, so A>=B>=0. Reversing the angular parameter if necessary, the left side is the p-th radial moment of the ellipse

c + A cos(theta) + i B sin(theta).

The right side is the p-th radial moment of the same centered ellipse with the shift along its minor axis:

A cos(theta) + i(B sin(theta)+c).

These statements follow by direct expansion, multiplication by a unit complex scalar, and a change of angular parameter. Thus (1) is exactly the claim that translating a parametrically uniform ellipse by c along its major axis gives at least as large a p-th radial moment as translating it by c along its minor axis.

## 2. Scalar supermodularity lemma

Define

H_p(u,v) = E_theta |sqrt(u)+sqrt(v) cos(theta)|^p,

for u,v>=0. For p>2, H_p is C^2 on the open positive quadrant. Indeed, the scalar function |r|^p is C^2, including at r=0; composing with square roots is C^2 when u,v>0, and on compact subsets the differentiated integrands are bounded uniformly in theta. Hence differentiation under the integral is valid even when the scalar argument vanishes for some theta.

Direct differentiation yields

(H_p)_{uv}(u,v)
= p(p-1)/(4 sqrt(uv)) E_theta [cos(theta) |sqrt(u)+sqrt(v) cos(theta)|^(p-2)].       (2)

The law of T=cos(theta) is symmetric. Therefore the expectation in (2) is

(1/2) E [ |T| ( |sqrt(u)+sqrt(v)|T||^(p-2)
                      - |sqrt(u)-sqrt(v)|T||^(p-2) ) ].

It is nonnegative, because sqrt(u)+sqrt(v)|T| >= |sqrt(u)-sqrt(v)|T||. It is strictly positive when p>2 and u,v>0, since the inequality of bases is strict whenever |T|>0. Thus H_p is supermodular, strictly so on every nondegenerate rectangle in the positive quadrant. Integrating (2) over rectangles proves the ordinary four-point supermodularity inequality. Rectangles touching an axis follow by continuity.

For p=2, H_2(u,v)=u+v/2, so the supermodularity difference vanishes.

## 3. Angular projection identity and rectangle pairing

Let

k_p = E_phi |cos(phi)|^p
    = Gamma((p+1)/2)/(sqrt(pi) Gamma((p+2)/2)) > 0.

Every z in the complex plane satisfies

E_phi |Re(exp(-i phi) z)|^p = k_p |z|^p.

Projecting the major-axis-shifted ellipse onto direction phi and then integrating theta gives

I_major = k_p^(-1) E_phi H_p(c^2 cos^2(phi),
                            A^2 cos^2(phi)+B^2 sin^2(phi)).

The same projection for the minor-axis shift gives

I_minor = k_p^(-1) E_phi H_p(c^2 sin^2(phi),
                            A^2 cos^2(phi)+B^2 sin^2(phi)).

The scalar sinusoid A cos(theta) cos(phi)+B sin(theta) sin(phi) has amplitude sqrt(A^2 cos^2(phi)+B^2 sin^2(phi)); this justifies the inner integration exactly. The sign of the constant projection is irrelevant by symmetry of cos(theta).

Put X=cos^2(phi), D=A^2-B^2=4ab, and v(x)=B^2+D x. The variables X and 1-X have the same distribution. Therefore

2 k_p (I_major-I_minor)
= E_X [ H_p(c^2 X,v(X)) + H_p(c^2(1-X),v(1-X))
        - H_p(c^2(1-X),v(X)) - H_p(c^2 X,v(1-X)) ].

For each X>=1/2, the bracket is the supermodularity difference on the rectangle with u-coordinates c^2(1-X),c^2X and v-coordinates v(1-X),v(X). For X<=1/2 both orderings reverse, leaving the same conclusion. Every bracket is nonnegative, proving (1).

If p>2 and a,b,c>0, then D>0 and for almost every X in (0,1) other than 1/2 both rectangle side lengths are positive and the rectangle interior lies in the positive quadrant. Equation (2) makes its supermodularity difference strictly positive. Thus I_major>I_minor. The listed equality cases follow directly.

## 4. Consequence for real majorants on an AP triple

Translation and nonzero dilation of frequencies do not affect normalized norm comparisons. Every sign pattern on a three-term arithmetic progression reduces, by an overall sign, t -> t+pi, and t -> -t, to one of the two cases in (1). Consequently every sign vertex of a real coefficient box has its p-th norm bounded by the all-positive vertex. For p>=1 the p-th norm functional is convex in the real coefficients, so its value throughout the coefficient box is bounded by that maximum over vertices.

It follows that every three-term arithmetic progression, and every subset thereof, has the full real coefficient majorant property for every p>=2.

## 5. Audit of the attempted multicosine extension

Do not infer full multivariable supermodularity from section 2. Consider

G_p(u,v,w)=E_{theta,psi}|sqrt(u)+sqrt(v)cos(theta)+sqrt(w)cos(psi)|^p.

Fix u=c^2>0 and take v,w sufficiently small that the scalar argument stays positive. The Taylor series at v=w=0 gives

(G_p)_{vw}(c^2,0,0) = [p(p-1)(p-2)(p-3)/16] c^(p-4).

Indeed the mixed term is g''''(c) E[(sqrt(v)cos(theta))^2] E[(sqrt(w)cos(psi))^2]/4 = g''''(c) v w/16. For 2<p<3 this derivative is negative. By continuity the mixed derivative is also negative at sufficiently small positive v,w. Hence the scalar kernel is not lattice-supermodular in all its coordinates in that exponent interval. This disproves only that direct extension strategy; it does not disprove a centered-cross-polytope majorant inequality, whose outer angular averaging could restore positivity.
