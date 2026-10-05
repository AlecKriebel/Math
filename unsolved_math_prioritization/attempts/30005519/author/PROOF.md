# A credited verification of Conflitti's real-subspace bound

## 1. Scope and attribution

Write

    e_j(x_1,...,x_n) = sum_{|I|=j} product_{i in I} x_i,
    e_0 = 1, and e_j = 0 for j > n.

All dimensions in the principal result are **real vector-space dimensions**. For every n >= 1 and positive even r, a real linear subspace L on which e_r vanishes identically has dimension at most min(n,r-1). Coordinate subspaces attain this dimension.

This is the exact conjecture of Conflitti (2006), p. 224, Conjecture 8, recalled in OWR 21/2023, p. 1131. The supplied record's date 2023 is the workshop-record date, not the original conjecture's date. Its quantifier is all subspaces, without symmetry, coordinate-support or genericity assumptions. Degrees r > n are harmless: e_r is zero and n < r. Degree zero is excluded.

The result, the sparse-intersection mechanism, and the maximal-subspace classification below are credited to Ferudun (2026), Theorems 1.3 and 1.5 and Corollary 1.4. This is a verification/reconstruction of that prior, explicitly unrefereed result. The preprint proves the coefficient obstruction by Descartes' rule; below we also supply a real-rooted differentiation proof. No novelty is asserted for either formulation. The separate star-transform construction in that paper is not needed and has not been audited here.

## 2. Coefficient obstruction, with an elementary proof

**Lemma.** For a real vector x and an integer 2 <= r <= n, if e_{r-1}(x)=e_r(x)=0, then x has at most r-2 nonzero coordinates.

First recall an elementary fact about a nonconstant real-rooted polynomial P: if P' has a root a of multiplicity at least two, then P has a root a, and its multiplicity is one greater than that in P'. To justify the only nontrivial assertion, suppose P(a) != 0 and list its real roots rho_i with multiplicities. Near a,

    (P'/P)'(a) = -sum_i 1/(a-rho_i)^2 < 0.

If P'(a)=0, this says P''(a)/P(a)<0, so P''(a) != 0. Hence a zero of P' away from the roots of P is simple. If P(a)=0, factoring P(t)=(t-a)^m Q(t), Q(a)!=0, shows that its derivative has multiplicity exactly m-1 there. This proves the fact. Derivatives remain real-rooted by Rolle's theorem, with multiplicities included.

Now use the degree-n real-rooted polynomial

    P(t) = product_i(t+x_i) = sum_{j=0}^n e_j(x)t^{n-j}.

For Q=P^{(n-r)}, its constant and linear coefficients are respectively

    (n-r)! e_r(x),     (n-r+1)! e_{r-1}(x).

Thus zero is a root of Q of multiplicity at least two. Applying the preceding fact backwards through the n-r differentiations shows that P has zero as a root of multiplicity at least n-r+2. At least that many x_i are zero. This is the desired support bound. If n=r, there are no backwards steps and the same multiplicity conclusion is immediate. If r>n, the corresponding support implication is automatic for n<=r-2; for n=r-1 it follows from e_{r-1}=product_i x_i=0.

For comparison, the deposited paper's Descartes proof was checked separately: in E(t)=product_i(1+x_i t), the number of positive plus negative roots equals its degree s, the support size. For each successive pair of nonzero coefficients whose degrees differ by d, their total contribution to the sign variations of E(t) and E(-t) is 1 for odd d and 0 or 2 for even d. This is at most d, strictly less when d>=3. Two consecutive missing interior coefficients would create such a gap, contradicting Descartes' bound s <= V(E)+V(E(-t)). The constant and leading coefficients are nonzero, so these degree gaps sum to s. Edge cases where r or r-1 equals s are ruled out by the nonzero leading coefficient. This verifies the preprint's Lemma 3.1 without importing any computational result.

## 3. Oddness forces a sparse hyperplane

For J contained in {1,...,n}, let E_J be the real coordinate subspace supported on J. Suppose L is a d-dimensional real subspace, d>=2, and e_r|L=0 with r even. We claim some J of size at most r-2 satisfies

    dim(L intersect E_J) >= d-1.                         (1)

Assume otherwise. The finite collection K_J=L intersect E_J then consists of subspaces of dimension at most d-2. Choose y in L outside their union. Next choose z in L outside the union of K_J+span(y). These are all proper subspaces, since their dimensions are at most d-1. A finite family of proper subspaces cannot cover a real vector space: each lies in a hyperplane, and the product of defining nonzero linear forms is a nonzero polynomial, which cannot vanish on all of R^d.

The plane U=span(y,z) meets every K_J only at zero. Indeed, if ay+bz lies in K_J, a nonzero b contradicts the choice of z, and b=0 with a!=0 contradicts the choice of y. In particular y and z are independent.

The continuous function

    h(theta)=e_{r-1}(y cos(theta)+z sin(theta)),  0<=theta<=pi,

has opposite nonzero endpoint values. They are nonzero by the coefficient lemma and the choice of y; they are opposite because r-1 is odd. Consequently h vanishes at some theta. Its argument is nonzero because y,z are independent. At this point e_r also vanishes, as U lies in L, so the coefficient lemma puts the argument in one of the K_J. This contradicts U intersect K_J={0}, proving (1).

This argument makes no inference from a Hessian signature or a hyperbolicity cone. Real-rootedness is used only in the proved coefficient obstruction; oddness and a finite arrangement of genuine linear spaces finish the proof.

## 4. Complete dimension bound and equality

If n<r, the bound is immediate. Otherwise, if a vanishing subspace had dimension at least r, restrict it to an r-dimensional subspace. Formula (1) would give a J with

    r-1 <= dim(L intersect E_J) <= |J| <= r-2,

which is impossible. Thus dim L<=r-1. Conversely, on any coordinate (r-1)-space every degree-r squarefree monomial vanishes. For n<r, all of R^n is a vanishing space. The exact maximum is therefore min(n,r-1).

No residual n, degree or genericity case remains for the stated conjecture. The proof is valid for all positive even r, including r=2; computation does not establish its universal quantifiers.

## 5. Classification at maximum dimension

The preprint also gives a stronger conclusion, which we verify. Let r>=4 be even, n>=r-1, and dim L=r-1 with e_r|L=0. The sparse-intersection statement produces J with |J|=r-2 and E_J contained in L. Write L=E_J+span(w), where w!=0 and w has zero coordinates on J, by subtracting its J-component.

The supports of x in E_J and w are disjoint. Multiplying their elementary generating polynomials gives

    0=e_r(x+t w)=sum_{i=0}^{r-2} e_i(x)t^{r-i}e_{r-i}(w).

Each e_i on E_J in that range is a nonzero polynomial. Distinct powers of t cannot cancel, so e_2(w), e_3(w), ..., e_r(w) all vanish. Apply the coefficient lemma to e_2(w)=e_3(w)=0 with index 3 (the lemma itself has no parity restriction). The support of w has size at most one. Since w!=0, L is exactly a coordinate (r-1)-space.

For r=2 the classification is false: the line generated by (1,1,-1/2) is a non-coordinate e_2-zero line. Its dimension still equals r-1.

## 6. Boundaries and negative controls

**Affine spaces.** If e_r vanishes on a real affine space a+W, then for every w in W the polynomial e_r(a+t w) in t vanishes identically. Its leading coefficient is e_r(w), so e_r|W=0. Thus the identical dimension bound holds for affine spaces. The vector-space theorem is the original target; this immediate corollary does not require claiming that every zero affine space contains the origin.

**Odd degree.** For any odd r and n=2r, the r-dimensional subspace

    (t_1,-t_1,...,t_r,-t_r)

annihilates every odd elementary polynomial, since its generating polynomial is product_j(1-t_j^2 z^2). Therefore the even-degree restriction cannot be deleted.

**Complex field.** Let omega be a nontrivial cube root of unity. In C^4 the two-dimensional complex subspace (s,t,omega t,omega^2 t) satisfies e_2=0: both the st coefficient 1+omega+omega^2 and the t^2 coefficient omega+omega^2+omega^3 vanish. The real theorem does not extend with complex dimensions.

**Stronger support heuristic.** Conflitti's text following Conjecture 8 suggests a stronger assertion that any vanishing subspace containing a vector with at least r nonzero coordinates must be a line. It is not the conjecture proved above, and it is false. For r=4,

    (s,-s,t,t,-t/2)

is a two-dimensional real subspace in the e_4-zero set; at s=t=1 it has all five coordinates nonzero. Its generating polynomial is

    (1-s^2 z^2)(1+(3/2)t z-(1/2)t^3 z^3),

whose z^4 coefficient is zero. Ferudun's Remark 3.4 already gives this example, attributing the general block construction to Chirvasitu's 2025 Theorem 0.2. This is a credited control, not a new counterexample.

## 7. Sources and verification status

1. Alessandro Conflitti, *Zeros of Real Symmetric Polynomials*, Applied Mathematics E-Notes 6 (2006), 219-224, especially p. 224, Conjecture 8 and adjacent discussion. https://www.math.nthu.edu.tw/~amen/2006/051014-3.pdf
2. Gaik Ambartsoumian, joint work with M. J. Latifi, *Injectivity and stability of the inversion of the star transform*, OWR 21/2023, pp. 1128-1131; exact conjecture and special-case Theorem 7 on p. 1131. https://doi.org/10.4171/OWR/2023/21
3. Alper Ferudun, *Star Transforms Without Type 2 Singular Directions and Conflitti's Conjecture on Elementary Symmetric Polynomials*, version 1.0 (30 September 2026), unrefereed preprint, Theorem 1.3, Corollary 1.4, Theorem 1.5, Section 3. https://doi.org/10.5281/zenodo.23062557
4. Alexandru Chirvasitu, *Fano schemes of sub-maximal elementary symmetric functions*, arXiv:2507.19163v2 (4 August 2025), Theorem 0.2. https://arxiv.org/abs/2507.19163v2

The relevant Ferudun proof was checked mathematically and reconstructed here. Its self-reported verification materials were read as author claims, not as an independent audit of this packet. A separate fresh review of this frozen packet is still appropriate. No peer-review or editor-maintained solved-status claim is made.
