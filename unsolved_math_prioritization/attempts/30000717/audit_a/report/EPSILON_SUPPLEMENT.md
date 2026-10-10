# Constant perturbations do not repair the Robinson certificate

Problem 30000717 / OWR-1465-011. Authored extension identified during independent review on 7 October 2026.

## Statement

Let S=R[x,y,z], let R be the Robinson sextic

R=x^6+y^6+z^6−x^4y^2−x^2y^4−x^4z^2−x^2z^4−y^4z^2−y^2z^4+3x^2y^2z^2,

and let

J=(yR_x−xR_y,zR_x−xR_z,zR_y−yR_z),

K=(yR_x,xR_y,zR_x,xR_z,zR_y,yR_z).

For L=J or L=K, let I(V_R(L)) denote the ideal of all real polynomials vanishing at every real common zero of L. For every real constant c,

R+c ∉ ΣS²+I(V_R(L)).

In particular this holds for L, its ordinary radical, and its real radical. Consequently the Robinson example also refutes the proposed implication from global nonnegativity to condition (iv), which requires R+ε∈ΣS²+L for every ε>0. This is a separate strengthening of the exact-certificate obstruction; it does not follow merely by substituting ε=0 in a positive-ε condition.

## Ingredients

Use the ten directions

Z={(1,s,t):s,t∈{−1,1}} ∪ {(1,s,0):s∈{−1,1}} ∪ {(1,0,t):t∈{−1,1}} ∪ {(0,1,t):t∈{−1,1}}.

The following facts have elementary proofs and exact independent arithmetic checks:

1. R is nonnegative on R³. For a=x²,b=y²,c=z² and after ordering a≥b≥c≥0, its symmetric cubic expression equals (a−b)²(a+b−c)+c(a−c)(b−c), a sum of nonnegative terms.
2. Every line Rv, v∈Z, lies in V_R(J)∩V_R(K), and R vanishes there. Indeed its gradient is zero at every real zero of this nonnegative differentiable polynomial.
3. The first coordinate axis also lies in both varieties, because ∇R(t,0,0)=(6t^5,0,0). On this axis R=t^6.
4. A homogeneous cubic vanishing on Z is zero. The six directions having a zero coordinate reduce such a cubic to

   A x(x²−y²−z²)+B y(y²−x²−z²)+C z(z²−x²−y²)+D xyz.

   Its remaining four values are −A−Bs−Ct+Dst. Summing against the four sign characters gives A=B=C=D=0. Multiplying a degree-d homogeneous polynomial by x^(3−d) then proves the same injectivity for every d≤3.

## The finite univariate sum of squares degree lemma

If p_1,...,p_m are real polynomials and Σp_i(t)² has degree at most 2d, then every p_i has degree at most d. If some p_i has degree D>d, choose D to be the largest such degree. The coefficient of t^(2D) in the sum is the sum of the squares of the leading coefficients of all degree-D summands. It is strictly positive, a contradiction. The zero-polynomial case is included by direct pointwise nonnegativity.

In particular a finite sum of real polynomial squares that is constant has only constant summands. Finiteness and real coefficients are essential and hold in the source's SOS cone.

## Proof

Suppose R+c=Σ_{j=1}^m q_j²+h, where h∈I(V_R(L)). If c<0, evaluating on any zero line immediately gives a negative sum of real squares. Hence only c≥0 needs consideration.

Fix v∈Z. Restriction to the entire real line tv gives

Σ_j q_j(tv)²=c.

By the degree lemma each q_j(tv) is constant as a polynomial in t. Write q_j=Σ_d q_{j,d}, its finite homogeneous decomposition. For every positive d, the coefficient of t^d gives q_{j,d}(v)=0. This holds for every v∈Z. In particular q_{j,1}, q_{j,2}, and q_{j,3} are zero polynomials by ingredient 4. No assertion about q_{j,0} is needed.

Restriction to the first coordinate axis gives

Σ_j q_j(t,0,0)²=t^6+c.

The degree lemma forces every q_j(t,0,0) to have degree at most 3. Its coefficients of t, t², and t³ are all zero by the preceding paragraph. Therefore every axis restriction is constant. Their sum of squares is constant, contradicting the coefficient 1 of t^6 on the right. This proves the assertion for every c≥0 and completes the proof.

## Scope and limitations

The argument allows any finite number of summands and arbitrary ambient polynomial degrees. It imposes no unproved global degree bound: the degree bounds follow separately from exact identities on real lines. It requires only vanishing of h on eleven explicit lines, so no radical computation, real Nullstellensatz, complete tangency-variety classification, or SDP calculation is needed.

The conclusion does not concern rational-function sums of squares, localizations, semialgebraic certificates with inequality multipliers, or truncated tangency varieties. Those are different representations. It does not dispute the gradient-ideal theorem: Euler's identity puts R itself in its ordinary gradient ideal. It also makes no claim that the original author's intended interpretation of the comma/ellipsis display is uniquely determined.

The form is classical and the source conjecture is documented in Markus Schweighofer's “Gradient tentacles and sums of squares,” Oberwolfach Report 14/2007, pp. 810–813, Theorem 1 and Conjecture 2. Public source: https://ems.press/content/serial-article-files/46100 and https://doi.org/10.4171/owr/2007/14 . No historical priority or novelty claim is made.
