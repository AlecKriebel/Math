# Turn2: complete parameter selection for an exponential resolvent kernel

AI-assisted proof candidate; independent review pending. Original unresolved2/5. **This turn changes the kernel to J(x)=exp(−|x|)/2.** It is a normalized even decreasing kernel, but is not C3 at zero and is not compactly supported. Therefore this theorem does not resolve the source's smooth finite-range model. It is an exactly solvable nonlocal comparison model, with full details to support later local perturbation analysis. Classical phase-plane and Green-kernel methods are credited; no novelty certification.

## 1. Statement and reduction

For every beta>1 and u in(m*,m_beta), there exists exactly one h in(0,H(−m*)) and one m in(−m_beta,−m*) for which an even positive bump above m, with q(0)=u and q decreasing on the positive half-line, solves

q=tanh(beta(J*q+h)), lim_{|x|->infinity}q(x)=m.

The centered profile is unique as well. The selected field h(u) is smooth and strictly decreasing, and0<h(u)<H(−u)=u−atanh(u)/beta.

Set A(t)=atanh(t)/beta,H(t)=A(t)−t, as in Turn1. The kernel J is the bounded inverse Green kernel of1−d²/dx² on the full line. If v=J*q and w=v+h, the equation becomes

w''=w−h−tanh(beta w)=W_h'(w),
W_h(w)=w²/2−hw−log(cosh(beta w))/beta.

Its first integral is (w')²/2−W_h(w)=constant. The negative equilibrium is w_-(h)=m(h)+h=A(m(h)), with h=H(m), on the strictly increasing negative metastable branch. Write h_sp=H(−m*)>0.

## 2. A strictly monotone scalar equation selects h

Let a=A(u)>0, fixed. Define

D_u(h)=W_h(a)−W_h(w_-(h)), 0<=h<=h_sp,

using the continuous negative branch at the endpoints. A homoclinic even peak with q(0)=u requires D_u(h)=0, because w'(0)=0 and w' tends to0 at infinity. For0<h<h_sp,

D_u'(h)=−(a−w_-(h))<0.

Indeed the derivative of W_h at its equilibrium is zero, leaving only the explicit field derivatives. This does not assume a profile exists.

At h=0, W_0 has equal strict minima at±m_beta and a lies strictly between0 and m_beta. Hence D_u(0)>0. At h=h_sp the two negative equilibria merge. The derivative W_h'(w) is strictly negative between that double negative root and the positive stable root, except at the double root itself. The latter positive root exceeds m_beta, whereas a<m_beta. Thus D_u(h_sp)<0. Continuity and strict monotonicity give a unique selected h, and hence a unique m.

The bound h<H(−u) follows without using Turn1's compact-kernel hypothesis. At h0=H(−u), the negative root is m=−u and w_-=-a. Symmetry of the field-free part of W gives D_u(h0)=W_h0(a)−W_h0(−a)=−2h0*a<0. Since D_u(0)>0 and D_u is strictly decreasing, its zero precedes h0.

## 3. Existence and uniqueness of the homoclinic profile

For the selected h, W_h has a negative metastable minimum w_-, an intermediate negative maximum, and a positive stable minimum. The point a>0 lies between the latter two critical points, and W_h(a)=W_h(w_-). Therefore W_h(w)>W_h(w_-) for all w in(w_-,a), with W_h'(a)=A(u)−h−u=H(u)−h<0 and W_h''(w_-)=1−beta(1−m²)>0.

Define the decreasing half-profile by the quadrature

x=integral_{w(x)}^a [2(W_h(s)−W_h(w_-))]^(-1/2) ds, x>=0.

The integral is finite at its upper turning endpoint because W_h'(a)<0, and diverges logarithmically as w approaches w_- because that is a nondegenerate minimum. It defines a smooth solution on[0,infinity), with w(0)=a,w'(0)=0 and w tending to w_-. Even reflection gives the full homoclinic solution. Set q=tanh(beta w); then q(0)=u and its limit is m, with strict decrease for x>0.

The bounded function v=w−h satisfies v−v''=q. Since the only bounded full-line solution of z−z''=0 is zero, v equals J*q. Thus the ODE solution genuinely solves the original exponential-kernel integral equation. The first integral forces any centered even unimodal solution with this limit and peak onto the same orbit; uniqueness of the scalar field selection and the quadrature gives uniqueness of the profile. No local differential equation is asserted for a general finite-range kernel.

## 4. Monotonicity and the small-field endpoint

The implicit function theorem applies because partial_h D=−(A(u)−A(m)) is nonzero. Moreover

h'(u)=[H(u)−h] A'(u)/(A(u)−A(m))<0.

Let r=m_beta and a_beta=A'(r)>1. As u increases to r, the unique h tends to0 by the strict bound above. Taylor expansion of the scalar equation at(h,u)=(0,r), where partial_h D=−2r, gives

h(u)=[a_beta(a_beta−1)/(4r)](r−u)²+o((r−u)²).

The coefficient is positive. Also m(u)+r=h(u)/(a_beta−1)+o(h(u)). These are consequences of the explicit scalar selection equation; a profile approximation alone would not justify differentiating an asymptotic relation.

## 5. Verification and scope

The symbolic checker verifies the endpoint energy-difference derivatives, the bound at m=−u, the derivative formula, and the positive small-field coefficient. The proof of existence and global parameter uniqueness is the scalar sign/monotonicity and quadrature argument, not a numerical continuation scan. This solvable kernel lies outside the source's C3 compact class. Its relevance is as a controlled model and possible local perturbation anchor, not an unqualified answer to the OWR conjecture.
