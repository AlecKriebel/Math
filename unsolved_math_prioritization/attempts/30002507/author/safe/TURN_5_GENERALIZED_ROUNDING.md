# Approach 5: round the frequencies of a known general-series example

The valid Broucke–Vindas result, arXiv:2102.08478v2, Proposition 1.4 and Theorem 3.1, supplies a general Dirichlet series with one simple zero at 1 in H_{1/2}. Its frequencies are generalized integers, not necessarily rational integers. The authors explicitly distinguish the ordinary question from their result. Their generalized Möbius coefficients are in {-1,0,1}, and the counting function of generalized integers is O(x). We use these stated published inputs as dependencies, not as a new solution of the ordinary problem.

The elementary lemma below proves exactly what integer rounding preserves. It also makes a compact-set approximation route substantive without promoting its finite-domain control to an all-height result.

## Theorem 5.1: bounded frequency rounding

Let 1<=x_0<=x_1<=... tend to infinity, with multiplicity allowed, and suppose

A(X)=sum_{x_k<=X}|a_k|=O(X).

Suppose D(s)=sum a_k x_k^{-s}, in this displayed order, converges in H_beta for some beta>=0. For each positive integer q set m_{k,q}=ceil(q x_k), and group the consecutive equal values to define ordinary coefficients

b_{m,q}=sum_{k:m_{k,q}=m} a_k,
B_q(s)=sum_{m>=1}b_{m,q}m^{-s}.

Then B_q converges in H_beta. There is a holomorphic E_q on H_0 such that

q^s B_q(s)=D(s)+E_q(s)  on H_beta,

and E_q -> 0 locally uniformly in H_0. More explicitly, for every compact K in H_0 with epsilon=min_K Re(s)>0 and L=max_K|s|,

sup_K |E_q| <= (L/q) sum_k |a_k| x_k^{-epsilon-1}.

### Proof

The weighted counting bound implies sum |a_k|x_k^{-1-epsilon}<infinity for every epsilon>0, by partial summation or a dyadic decomposition. Since y_{k,q}=m_{k,q}/q lies in [x_k,x_k+1/q), integration of the derivative of u^{-s} gives, for Re(s)>=epsilon>0,

|y_{k,q}^{-s}-x_k^{-s}| <= |s| integral_{x_k}^{y_{k,q}} u^{-Re(s)-1}du <= (|s|/q)x_k^{-epsilon-1}.

Thus E_q(s)=sum a_k(y_{k,q}^{-s}-x_k^{-s}) converges absolutely and locally uniformly in H_0, has the stated bound, and is holomorphic there. For fixed s in H_beta, the generalized series with bases y_{k,q} is the sum of the convergent series D and this absolutely convergent difference. Grouping equal y values groups finite consecutive blocks, so its grouped partial sums have the same limit. The grouped series is q^s B_q. This proves ordinary convergence and the identity. QED.

## Corollary 5.2: exact local zero control, conditional only on the credited general-series input

Assume in addition D is holomorphic on H_beta, rho belongs to H_beta, Re(rho)>0, and rho is a simple zero of D. Define an ordinary series

C_q(s)=B_q(s)-q^{-s}E_q(rho).

This only changes the coefficient at the positive integer q. It converges in H_beta, and

q^s C_q(s)=D(s)+E_q(s)-E_q(rho),

so C_q(rho)=0 exactly. Fix a closed disk centered at rho contained in H_beta and H_0 on which rho is D's only zero, and whose boundary contains no zero. For every sufficiently large q, C_q has exactly one zero in that disk, counted with multiplicity; it is therefore precisely rho and is simple. Also, on any fixed compact zero-free subset K of H_beta intersect H_0, C_q has no zeros for all sufficiently large q.

### Proof

On the boundary of the disk, the positive minimum of |D| exceeds |E_q(s)-E_q(rho)| for sufficiently large q, by Theorem 5.1. Rouché gives one zero counted with multiplicity for q^s C_q. The factor q^s is entire and nowhere zero, and the forced zero is rho. On K the same minimum-modulus comparison proves nonvanishing. QED.

For the Broucke–Vindas example, beta=1/2 and rho=1. Its simple zero follows from the reciprocal of the simple pole of its generalized zeta function in their Section 3. Thus the corollary constructs ordinary convergent series with a simple zero at 1 and controlled nonvanishing on any preassigned compact zero-free region. This is an approximation consequence of their credited theorem, not a global solution or novelty claim.

## The exact all-height gap

The quantifier is: for each fixed compact K there is a sufficiently large q=q(K). It is not: there is one q that works on the whole unbounded half-plane. A sequence of compacts exhausting H_{1/2} may require q tending to infinity. Their resulting series are different, and their normalized local limit is the original general series D; this does not produce one ordinary Dirichlet series with the required global divisor.

A general analytic negative control makes this quantifier failure explicit: h_N(s)=(s-1)(1-s/(2+iN)) tends locally uniformly to s-1, yet every h_N has the additional zero 2+iN. For |s|<=R, |h_N(s)-(s-1)|<=R(R+1)/sqrt(4+N^2), which proves the local convergence while the second zero escapes to unbounded height inside H_{1/2}. These polynomials are a counterexample to the general compact-convergence inference; they are not asserted to be Dirichlet-series examples or counterexamples to the source target.

There is a direct obstruction to inferring uniform-in-height control from a small frequency displacement. If x,y>0 are distinct, choose t=(2j+1)pi/log(y/x). Then |x^{-it}-y^{-it}|=2. Therefore arbitrarily close but different frequencies need not have close phases uniformly in t. The |s| factor in the rounding estimate reflects a real issue, not merely a dispensable numerical inconvenience.

Even preserving the known zero is not automatic before the correction above. The finite general sum D(s)=1-(3/2)(3/2)^{-s} vanishes at s=1. Rounding 3/2 up to 2 gives 1-(3/2)2^{-s}, whose value at 1 is 1/4. After subtracting 1/4 the corrected ordinary polynomial 3/4-(3/2)2^{-s} vanishes at 1 but has all the zeros 1+2pi i j/log 2. This is an exact negative control for the inference from one corrected local zero to uniqueness in a half-plane.

## Final attempt disposition

Five materially distinct approaches have been completed. The exact ordinary-series target remains unresolved in this attempt. The last approach preserves convergence and achieves rigorous fixed-compact control, but leaves global exclusion of additional zeros at unbounded imaginary heights. No numerical zero count or compact convergence statement closes that gap. Estimated full-resolution progress: 0%; scoped proofs and this five-approach investigation are complete, subject to a fresh independent audit.
