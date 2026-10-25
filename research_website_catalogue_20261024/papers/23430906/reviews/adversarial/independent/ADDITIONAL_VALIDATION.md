# Additional validation after the independent freeze

This file supplements, and does not alter, the early sealed derivation.

The closed form used only in sampled diagnostics is independently recovered by
Tonelli from the nonnegative integrand:

 D_H = 4 ∫₀∞ (1-cos x)x^(-1-2H) dx
     = 4/Γ(1+2H) ∫₀∞ s^(2H-1)/(1+s²) ds
     = 2π/[Γ(1+2H) sin(πH)],  0<H<1.

The first interchange follows from the Laplace integral for x^(-1-2H).
The elementary inner integral is ∫₀∞ e^(-sx)(1-cos x)dx=1/[s(1+s²)].
The final identity is Euler's beta integral with t=s². At H=1/2 this is
2π. The actual theorem defines D_H by its convergent integral, so it
does not depend on floating evaluation of this closed form.

The optional radical for N_f in the support is correct. Set y=2x-1.
Then phi'''=(3/2)y(1-y²)(3-7y²), and
phi''''=3(35y⁴-30y²+3). Its internal zero squares are
q±=(15±2√30)/35. Total variation of phi''' on [-1,1] is
4[R(qminus)-R(qplus)], where R(q)=(3/2)√q(1-q)(3-7q).
This recovers the support expression; the integral definition avoids any
quadrature certification requirement.

A noncommuting signed-matrix control is
A=[[2,-1],[-1,2]], C=[[1,1/2],[1/2,3]]. Both are positive definite
(positive leading minors); they do not commute, and tr(AC)=7.
Since A<=3I, tr(AC)<=3 tr(C)=12. Thus negative individual covariance
products and failure of commutation do not threaten the trace argument.
The full proof already establishes it for arbitrary positive matrices.

An especially useful order-of-limits control is m=n in paper equation (16):
the deterministic pairing is zero because every sampled f_j vanishes.
This does not contradict its positive m->infinity limit for fixed n.
Taking the refinement count equal to the observation count would destroy
the proof, but the manuscript explicitly fixes n,T,j before that limit.

The source-version statement can be checked without any exact Euler
coefficient: in pinned NTU arXiv v1 equation (26), every lag-2 integrand is
positive when H!=1/2 and each distance is at most 3. Hence
c_2>=H²(2H-1)² 3^(4H-4)/4>0. There are 2(m-2) ordered lag-2 pairs.
After normalization by m^(1-4H), their contribution tends to 2c_2>0.
Thus the v1 equation (27) little-o statement is indeed false. The journal
author copy retains these near lags and discards only a diverging-lag
tail, as its equations (29)-(30) show. The current note correctly
distinguishes those versions and does not use the faulty coefficient.

No substantive flaw in the deposited theorem has emerged from these controls.
Neither these checks nor the archived wrapper's acceptance strings certify
novelty or replace the all-parameter analytic argument.
