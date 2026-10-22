# Direct geometric checks of the universal reduction

The first-attack derivations are preserved separately. This note was developed after reading the manuscript; it is a review derivation, not a historical independence claim.

Put A=a², B=b², D=diag(A,B), n=D⁻¹P, and κ=√(λ/(AB)). The following arguments use real geometry and linear algebra.

1. **Actual foot and reflection.** The tangent is n·X=1, so Q=n/(n·n). At a boundary point and for a unit direction v, direct expansion gives

   A v_y²+B v_x²−det(P,v)²=AB(n·v)².

   For a unit normal u perpendicular to a chord, tangency to C says (u·P)²=uᵀ(D−λI)u. This is equivalent to (n·v)²=κ². Specular reflection with inward outgoing direction therefore gives v_in−v_out=2κQ. The denominator n·n is bounded below by 1/A, so no real foot singularity occurs.

2. **Outer intersection and polarity.** For distinct chord endpoints P,P′, let its line be u·X=h. The point R=Du/h satisfies PᵀD⁻¹R=P′ᵀD⁻¹R=1, precisely the two boundary tangents. Thus the manuscript uses the correct pole of the chord with respect to E. A pole with respect to C would give its contact point instead. Since h²≥B−λ>0 for unit u, the pole is finite. Coincident or antipodal endpoints are unavailable to a nondegenerate chord tangent to a strictly inner ellipse.

3. **Canonical parametrization covers all real physical branches.** This can be reconstructed without an additional completeness assumption. Set α=√(A−λ), β=√(B−λ), k²=(A−B)/(A−λ), and choose the unique v∈(0,K) with cn(v)=β/b. Then sn²(v)=λ/B, and algebra gives dn(v)=aβ/(bα). Hence a=αdn(v)/cn(v), b=β/cn(v). Jacobi addition shows the chord from P(z−v) to P(z+v), with P(z)=(−a sn(z),b cn(z)), is tangent to C. The real parametrization P runs once around E on [0,4K). There are exactly two real tangents from any P∈E to the strictly interior C, and these are the shifts ±2v. Consistent orientation selects one; reversal selects the other. Thus periodic closure forces 2Nv=4τK. Least period gives gcd(τ,N)=1 and v<K gives 0<τ<N/2. This does not discard admissible winding stars.

4. **Signed edge area.** For any closed indexed list P_j, determinant bilinearity gives

   A((P_{j+1}−P_j)_j)=2A(P)−(1/2)∑det(P_j,P_{j+2}).

   This uses no simplicity assumption. Reindexing the sum over j by two never requires stepping by two to make a single cycle. Applying the manuscript's checked two-point determinant identity therefore gives the coefficient ab(2f(v)−f(2v)) without a missing factor of two.

5. **Foot as edge image.** Put w=K−v. The real quarter-period relations give dn(w)=b/a and k²sn²(w)=(A−B)/A. Consequently the addition denominator is [A−(A−B)sn²z]/A, bounded below by B/A>0. The sum P(z+w)+P(z−w), multiplied by diag(b/a,1)/(2cn(w)), is exactly n(z)/(n(z)·n(z)). Because P(z−w+2K)=−P(z−w), this sum equals P(z+K−v)−P(z+K+v). The fixed linear area scale is b/[4a cn²(w)], yielding the manuscript's pedal coefficient b²/[4cn²(w)]. The minus sign on all edge vectors has determinant +1 in dimension two.

6. **Remaining global input.** These real identities reduce the product exactly to the displayed constant coefficient times T(u+v)T(u+v+K), since T has period 2v. The shifts modulo the real dn period 2K have order q=N/gcd(N,2); q is odd precisely for the admitted period classes. I checked the manuscript's meromorphic argument and its classical product-to-sum reproof as written: odd q excludes the real shift K from the subgroup, all poles are at most simple, opposing shifted zeros cancel them, or equivalently V−C_qU_q has no poles and is antiperiodic. This is a supplied proof of the needed trace fact rather than an unsupported replacement invariant. The separate analytic reviewer is responsible for the distinct special-function/source attack family; this review supplies the real geometric checks.

The proof divides by no polygon area, so it does not add a hidden nonzero-area hypothesis. Reversal changes each shoelace sign, and a displayed d-fold repetition duplicates each sum d times. The product therefore scales by d². A displayed length not divisible by four cannot have a primitive divisor divisible by four. N=1 and N=2 are unavailable under the strict caustic assumptions; no assertion here extends to focal, hyperbolic, or collapsed caustics.

For a planar rescaling by c, κ scales as 1/c while Q and R scale by c. The product scales as c⁴, matching the manuscript constant.
