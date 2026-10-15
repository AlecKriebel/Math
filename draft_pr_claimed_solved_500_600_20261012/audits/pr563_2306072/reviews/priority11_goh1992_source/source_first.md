# Goh 1992: independent source-first reading

Recorded 2026-10-15 03:07 UTC, before candidate proof, original target, or earlier reviews were consulted. Review effort completion estimate: 35%. Source: Say Song Goh, *On the Two-Functional Conjecture for Univalent Functions*, Complex Variables 20 (1992), 197-206, DOI 10.1080/17476939208814600. The source PDF has an extra publisher wrapper (PDF page 1); PDF pages 2-11 are article pages 197-206. See source_custody.json for exact custody. All ten article pages, including every proof, remark, example, acknowledgment, and reference, were read. Critical displayed mathematics was checked in rendered page images, rather than trusting defective OCR.

## Exact objects and success criteria in this source

S consists of f(z)=z+a2 z^2+... analytic and univalent in D. A support point maximizes Re L over the full S for a continuous complex-linear L, nonconstant on S. The standing two-functional hypothesis is simultaneous maximization of Re L and Re M, with L not a positive real multiple of M. Coefficient degrees are genuine: L=sum(j=2..n) lambda_j a_j with lambda_n nonzero, and M=sum(j=2..m) mu_j a_j with mu_m nonzero. A missing top coefficient changes the degree. The conclusion sought in this paper is that f is a rotated Koebe map. The introduction recalls that any support point omits one analytic arc extending with increasing modulus from a finite tip to infinity. Increasing modulus is the sole explicit general slit geometry asserted; it does not assert monotone argument, curvature, or radial-tangent angle.

## Source mechanism, pages 198-200

Boundary variation yields (z w'/w)^2 P_L(1/w)=R_L(z), w=f(z), where

P_L(zeta)=sum(lambda_j P_j(zeta));
P_j(zeta)=sum(k=1..j-1) A_j(f^(k+1)) zeta^k
          =zeta^(j-1)+(j-1)a2 zeta^(j-2)+...,
R_L(z)=sum_j lambda_j sum(k=1..j-1) k a_k z^(k-j)
       +sum_j (j-1)lambda_j a_j
       +sum_j conjugate(lambda_j) sum(k=1..j-1) k conjugate(a_k) z^(j-k).

A_j extracts the coefficient of z^j and a1=1. A second independent Schiffer equation permits division and algebraic continuation F, with F(0)=0 on every sheet. Each local branch is F(z)=b1 z+b2 z^2+..., b1 nonzero. This algebraicity and the implication that all b1=1 force a rational support point, hence rotated Koebe, are cited to Schaeffer-Spencer/Duren; they are not proved from scratch in this paper.

Coefficient comparison gives b1^(n-1)=b1^(m-1)=1 and, writing r=lambda_(n-1)/lambda_n,
2 b2+(n-1)(a2 b1^2-b2)+r b1^2=2 a2 b1+r b1.
The analogous identity with m and s=mu_(m-1)/mu_m yields
(n-m)(a2 b1^2-b2)=(r-s)(b1-b1^2).
For n not m, elimination gives alpha(1-b1)=2 a2(1-b1),
alpha=((m-3)r-(n-3)s)/(n-m).
Theorem 1: the two-functional conclusion holds if |alpha|<=2 sqrt(2) OR |alpha|>=4. This is 2 sqrt(2), not the OCR-corrupted square roots. It uses the strict support bound |a2|>sqrt(2), Bieberbach |a2|<=2, and equality forcing Koebe. Remark (i) allows one global support equation and a second critical equation: critical means satisfying the *full generalized Schiffer equation*, not merely an arbitrary local slit trajectory. Remark (iii) says some additional computations at order z^(3-n) work in the remaining annulus when one degree is even, but omits those computations.

## Degree-three mechanism and example, pages 200-201

Theorem 2: n=3,m>=4. If b1 not 1, the elimination says lambda2+2 lambda3 a2=0, whereas this equals L(f^2), nonzero for a support point. Both orientations of support/critical are justified by the later same-degree reduction. Brown's cited theorem states that for L=lambda2 a2+a3 no Koebe rotation maximizes Re L when both Re lambda2 and Im lambda2 are nonzero, or Re lambda2=0 and 0<|lambda2|<6. Combined with the two-functional theorem this excludes simultaneous maximizers with an essentially different M. The printed corollary omits repeating the essential-difference standing assumption: taken literally with M=L it is false, because S is compact and a maximizer exists. The only sound use is under the paper's standing two-functional hypothesis. Brown's theorem is a cited result, not reproved here. This constructs/examples the absence of a common maximizer, not a nonmonotone-argument slit.

## Same-degree mechanism, pages 201-205

Lemma 1 proves lambda_n/mu_n real for simultaneous maximizers. Using algebraic F at infinity, finite nonzero or infinite F limits cannot match the R pole. F=b z^(-gamma)+... must have gamma=1 and b^(n-1)=lambda_n/conjugate(lambda_n)=mu_n/conjugate(mu_n). Thus their ratio is real. Lemma 2 uses omitted-arc quadratic-differential positivity: if f supports both L and cL, dividing the positive differentials forces c>0. This geometric positivity is stronger than a formal complex equation and is not implied by it alone.

For independent equal-degree L,M with real top-coefficient ratio, let ell=max{j:2<=j<=n-1, lambda_j/lambda_n not mu_j/mu_n}. Theorem 3: gcd(n-1,ell-1)=1 forces Koebe. Subtracting the two normalized equations cancels top terms and creates a degree-ell Schiffer equation; b1^(ell-1)=1 together with b1^(n-1)=1 then forces b1=1. The top coefficient ratio being real is essential to cancel both conjugate-positive and negative Laurent terms. In particular, differing penultimate normalized coefficients suffice (ell=n-1).

Theorem 4 handles ell=3 without the coprimality condition. Put d3=lambda3/lambda_n-mu3/mu_n, d2=lambda2/lambda_n-mu2/mu_n and beta=d2+2a2 d3. If beta nonzero, the previous elimination forces b1=1. If beta=0, the equation reduces to
(c2/w^2)(z w'/w)^2=(z^4+c1 z^2+c2)/z^2,
c2=d3/conjugate(d3).
The numerator is (z-a)(z+a)(z-b)(z+b). At the actual finite slit tip, f(z)-w0 has a double zero, so f' has a simple zero; hence the quartic must have a double zero at z0. Its evenness forces a^2=b^2=z0^2, and the equation integrates as
-sqrt(c2)/w=+/- (z+z0^2/z+c3).
Thus f is rational, and the cited rational-support classification gives Koebe. This is the only explicit finite-tip geometric construction in the proof, and its outcome is rational Koebe, not a general nonradial slit. Corollary: n=m=5 since ell in {2,3,4}; Theorems 3/4 also cover *all* n=m=3 and 4 under the standing independence assumptions (for n=4, ell=2 or 3).

The final remarks allow one support point plus the other critical equation, and derive the degree-three result in the opposite orientation by replacing the pair with M and L+M (then ell=3).

## Final section and complete-source coverage

Page 206 proves a reduction: if the two-functional conjecture is true in the equal-degree case, it follows for unequal degrees, because a common maximizer for L,M also maximizes L+M, and L+M has the higher degree while remaining essentially different from L. The converse under the stronger support/critical theorem hypothesis follows from equation subtraction. The final section does not assert monotonic argument or angle and contains no new slit family, extrema construction, or hidden geometric counterexample. It explicitly lists n=4,m=7 as still open. References [1]-[7] were read: Babenko 1972/75, Bakhtin 1981 and 1986 preprint, Brown 1981, Duren 1983, Kirwan-Pell 1978, Schaeffer-Spencer 1950.

## Independently derived low-order identities to be checked exactly later

P2=zeta; P3=zeta^2+2a2 zeta;
P4=zeta^3+3a2 zeta^2+(2a3+a2^2)zeta.
For degree 4, P_L=lambda4 zeta^3+(lambda3+3a2 lambda4)zeta^2
 +(lambda2+2a2 lambda3+(2a3+a2^2)lambda4)zeta.
Thus a single coefficient-support slit equation has a cubic P_L. The two-functional conclusions cannot be inferred from this one equation without a second actual support or critical equation. A potential later priority collision must be tested on actual slit geometry, rather than dismissed by different functional names.

## Verification scope and unresolved source dependencies

The displayed coefficient elimination, normalized equation subtraction, degree/coprimality cases, and beta=0 quartic integration have been followed algebraically. An exact checker remains to be authored. The global Schiffer variation theorem, algebraic continuation for two equations, support a2 lower bound, Brown classification, rational-support classification, and analytic slit-tip extension are used as cited source dependencies, not independently reproved. The reading is not a complete independent proof of those external results. No theorem in this paper has been falsified by this review.
