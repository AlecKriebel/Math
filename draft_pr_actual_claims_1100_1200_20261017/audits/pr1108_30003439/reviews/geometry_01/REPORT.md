# Independent adversarial geometry, barrier and algebraicity audit

Audit completed: 2026-10-17, with exact validation timestamps in results.json and results_optimized.json.
Reviewer family: geometry/normality/algebraic-boundary adversary.
Frozen candidate: PR 1108; problem 30003439 / OWR-15219-008; commit 148130ab93ab46a3459d7bc98a11a1ca79052d65.
Audit scope is only this candidate. No novelty/priority investigation was conducted.

## Verdict and exact accepted claim

**Accept the mathematics at its stated, existential scope. No substantive flaw or necessary mathematical correction was found.**

Let p(x,y,z)=xy²-z³ and
K={(x,y,z): x≥0,y≥0,z≥0,p≥0}.
On int K define f=-log p-log z and F=25f, extending F by +∞ elsewhere. The verified claim is that K is a regular cone defined by homogeneous polynomial inequalities; F is a 100-normal barrier; D³F(q)[h,u,u]≤0 for all q∈int K, h∈K, u∈R³; and K is not the hyperbolicity cone of any homogeneous polynomial in the original R³.

This supplies the requested witness for Tunçel's original existential problem. It says nothing universal about all cones, and does not assert that the cone, barrier, or certificate is novel.

Frozen PROOF.md: 13,923 bytes; SHA-256 9577476ee2c0fd2e3d12ab1265201d8b99f6ef50a9060e245c46f872dd673302. Retrieved independently with GitHub's raw contents API at the named commit. The old MATHEMATICAL_AUDIT.md was first read only after independently inspecting the proof, definitions, geometry, self-concordance, and exact matrix identities. Its historical claims of computation are not evidence for this audit's new computations.

## Target and source definitions

The author-hosted 2017 contribution was read first. The full official MFO report was then retrieved into memory and its physical page 29 parsed independently: its printed header is 799 and it contains the existential algebraic-cone problem. This removes ambiguity from the broader later question. The official PDF has 92 pages, 924,239 bytes, SHA-256 a3d9a9bf745a07427869a2f6559011c055d6eaaf385c54c3aee604c67811f31d. A web screenshot request timed out; no claim of new visual inspection is made.

Nesterov–Tunçel 1412.1857, pp.3–4, defines regularity and normality using scalar self-concordance and logarithmic homogeneity; §6 uses the cone-direction third-derivative matrix condition. These are exactly the conventions checked below.

Dahl–Tunçel–Vandenberghe 2509.10263v2 §2.2 instead displays a matrix self-concordance inequality. Its Definition 3.1 uses concavity of directional gradients, equivalent here to the same third-derivative condition. Its §6 asks the broader universal existence question. Both arXiv HTML and the author-hosted PDF were inspected; the latter bears an internal June 16, 2026 revision date, while arXiv v2 was submitted June 12.

Hildebrand 1305.4814 Theorem 3.2 family 5 already contains this cone: use exponent parameters p=3, q=3/2 and coordinates (x₁,x₂,x₃)=(x,z,y). Its affine-sphere terminology creates no polynomial-hyperbolicity exception.

The sources and inspected locations are recorded in SOURCES.json, with direct primary-source URLs. No source document copies are distributed in this audit.

## Geometry, interior and all finite boundary strata

The four inequalities are homogeneous polynomials. Their common feasible set is closed and positively conic. Orthant containment implies K∩(-K)={0}; (2,1,1) is strictly feasible, so K has nonempty three-dimensional interior.

The interior is precisely x,y,z>0 and p>0. Vanishing coordinates lie in supporting orthant planes. At a positive-coordinate point with p=0, decreasing x leaves K and increasing x enters its interior.

Write m=x^(1/3)y^(2/3). For x,y>0,

D²m=-(2/9)x^(-5/3)y^(-4/3) (y,-x)ᵀ(y,-x).

Thus m is concave; continuity extends concavity to the nonnegative orthant. K is the hypograph z≤m intersected with z≥0. This proves convexity directly, without assuming a representation or importing a nonpolynomial defining condition.

At every finite boundary point, z=0 or p=0, including edges and the origin: if x=0 or y=0, the cone constraints force z=0. Any interior sequence tending to such a point has zp→0⁺ and F=-25log(zp)→+∞. Outside K, a neighborhood misses the effective domain. Consequently the extended function is lower semicontinuous everywhere. Its interior formula is C∞ and finite; the Hessian calculation below makes it convex on a convex domain. Hence it is proper and closed. There is no requirement to control sequences whose base points escape to infinity.

## Scalar and mixed self-concordance: independent derivation

At a fixed interior point set g=z³/y², δ=x-g>0. For any direction u put b=u_y/y, c=u_z/z,
w=(u_x-g(3c-2b))/δ, k=6g/δ, v²=k(c-b)² and Q=2b²+c².

Expansion of g(q+τu)=g(1+τc)³/(1+τb)² gives, without any omitted chain-rule term,

g'=g(3c-2b),  g''=6g(c-b)²,
g'''=6g(c-b)²(c-4b).

Applying these to f=-logδ-2log y-log z yields

S=D²f[u,u]=w²+v²+Q,
D³f[u,u,u]=-2w³-3wv²+(c-4b)v²-4b³-2c³.

If S=0 then b=c=w=0 and u=0, proving a positive definite Hessian. Also
9Q-(c-4b)²=2(b+2c)²≥0 and
2|b|³+|c|³≤Q^(3/2).
Bounding the four displayed cubic groups gives |D³f[u³]|≤10S^(3/2). Therefore

|D³F[u³]|≤250S^(3/2)=2(25S)^(3/2)=2(D²F[u²])^(3/2).

For the matrix convention, choose the signed linear functional v_u=√k(c_u-b_u) and ℓ_u=c_u-4b_u. The symmetric polarization is exactly

D³f[h,u,u]
=-2w_h w_u²-w_h v_u²-2w_u v_h v_u
 +(ℓ_h v_u²+2ℓ_u v_h v_u)/3
 -4b_h b_u²-2c_h c_u².

In order, the four groups are bounded by 2,3,3,2 times ||h||_f ||u||_f². For the last group one may use
|4b_h b_u²+2c_h c_u²|
≤2√(2b_h²+c_h²)√(2b_u⁴+c_u⁴)
≤2||h||_f ||u||_f².
No independence among these linear functionals is assumed or needed. Multiplication by 25 converts the resulting bound 10 to 2 in the F norm. This directly proves both sides of the matrix self-concordance condition for every real h,u, without relying on an unstated diagonal-to-mixed equivalence.

Because zp has degree four, F(ta)=F(a)-100log t. Euler differentiation gives H_F(a)a=-∇F(a) and aᵀH_F(a)a=100. Since H_F is invertible,

∇F(a)ᵀ H_F(a)^(-1) ∇F(a)=100.

Thus the barrier parameter is 100, not the unscaled value four. All normality requirements are met.

## Negative curvature: exhaustive directions and exact algebra

This was independently checked although geometry/normality/nonhyperbolicity were the main assigned focus.

For positive diagonal D=diag(a,b,c) with ab²=c³, K is invariant and f(Dq)=f(q)-4log c. At any interior base (x,y,z), D=diag(y²/z³,1/y,1/z) sends it to (r,1,1), r=xy²/z³>1. Third derivatives transform with all direction arguments, giving the required congruence. The invariant r is retained; transitivity of the automorphism group is not assumed.

For any h∈K with h_y>0, t=h_z/h_y≥0 and

h=h_y(t³,1,t)+(h_x-h_z³/h_y²)e_x.

Both coefficients are nonnegative. When h_y=0, h_z=0 and h is a nonnegative multiple of e_x. Thus t=0, the facet, e_x, h=0, and all curved boundary/interior directions are covered.

Put s=r-1>0. Independently differentiating -log p-log z uses

dp=(1,2r,-3),
D²p=[[0,2,0],[2,2r,0],[0,0,-6]],
D³p[h(t)]=[[0,2,0],[2,2t³,0],[0,0,-6t]].

In particular the exact numerator formula is

-s³D³f[h]
=s²D³p[h]-s((D²p h)dpᵀ+dp(D²p h)ᵀ+(dp·h)D²p)
 +2(dp·h)dp dpᵀ+2s³ h_z E_zz.

Expanding over Q[s,t] reproduces all nine NC1 entries. The exact checker also independently reproduces NC2, NC3, NC4, NC5, the t=1 block, and the e_x sum of Gram matrices.

The positivity reasoning is universal. For 0≤t<1, the terms of P and R in the manuscript are nonnegative and their constant terms are positive. At t=1 both equal 6s². For t>1, both square certificates have positive remainder: the possibly obscure NC4 polynomial becomes 8u³+45u²+72u+24 at t=1+u. Thus the first three leading minors are positive when t≠1, proving positive definiteness by Sylvester's criterion.

At t=1, the leading minors vanish, so that criterion alone would be insufficient. The actual matrix is

2s² [[0,0,0],[0,2r+1,-3],[0,-3,r+2]],

whose lower block has determinant (r-1)(2r+7)>0. It is positive semidefinite of rank two. At e_x the exact matrix is

2(1,2,-3)ᵀ(1,2,-3)+6s(0,1,-1)ᵀ(0,1,-1),

with rank two and kernel R(1,1,1). This is a direct certificate; the alternative limit h(t)/t³→e_x is also valid. Linearity in h and positive rescaling then prove D³F[h]≤0 in the required matrix order. No bound at s=0 is needed, since it is a base boundary outside the barrier domain.

## Arbitrary-degree nonhyperbolicity: no polynomial loophole

The proof excludes every homogeneous H in R³, not merely the displayed cubic p.

1. As an element of R[y,z][x], p=y²x-z³ is primitive: gcd(y²,z³)=1. It is linear and irreducible over R(y,z). Gauss's lemma makes it irreducible, hence prime, in R[x,y,z].

2. The set B={(z³/y²,y,z):y,z>0} is a genuine topological boundary patch, as verified above. If a homogeneous polynomial H had hyperbolicity cone K, H must vanish at every boundary point. One direct justification is to use the source's eigenvalue roots of H(q-λe): their leading coefficient is fixed and nonzero. At a boundary point of the closed nonnegative-root cone, some root must be zero, since otherwise positivity persists in a neighborhood. Thus H(q)=0 there. A positive constant H gives all R³ and cannot be an exception.

3. Let d=deg_x H. Multiplying H(z³/y²,y,z) by y^(2d) yields a polynomial in y,z that vanishes on the positive open orthant, hence identically. Division in the fraction field gives p|H there. More concretely, clearing denominators gives p|y^N H for some N; because p is prime and does not divide y, p|H already in R[x,y,z]. This establishes the necessary density/divisibility step independently of the extra flat facet.

4. Every possible hyperbolicity direction e lies in int K, so a=(e_x e_y²)^(1/3)>b=e_z>0. For v=(0,0,1),

p(v+te)=a³t³-(1+bt)³
=((a-b)t-1)((a²+ab+b²)t²+(a+2b)t+1).

The quadratic discriminant is -3a²<0. This holds for every interior direction e; no direction has been selected by convenience. If H=pQ and H(e)>0, then Q(e)≠0, so the restriction is a genuine nonzero product. Polynomial multiplication cannot cancel nonreal roots. The choice v-te simply negates the roots. This contradicts hyperbolicity in e.

An invertible linear identification with another three-dimensional hyperbolicity cone would pull its polynomial back to R³, and is excluded by the same argument. Nothing here asserts the absence of a projection or higher-dimensional lift; those are different notions and provide no exception to the original-space claim.

## One-sided scope and falsification controls

The usual signed cone allows -m(x,y)≤z≤m(x,y). It is not this K: K has a z=0 facet, whereas that plane cuts through the signed cone. F contains -log z and cannot serve as a barrier on the whole signed cone. The proof never silently transfers between them.

The extra term is substantive. Independent exact differentiation at base (5,1,1), cone direction (8,1,2), for f₀=-log p produces det(-(5-1)³D³f₀[h])=-24576, excluding positive semidefiniteness. Also f₀ stays finite approaching the point (1,1,0), so would fail the facet barrier condition.

The checker rejects claims of strict definiteness at t=1 and e_x, a changed matrix coefficient, a changed square remainder, a false positive discriminant, assigning parameter four to F, and pretending the loose coefficient-10 certificate establishes self-concordance with scale one. The last control concerns this certificate only; it is not a claim that every smaller scaling fails actual self-concordance.

## Reproducibility and remaining gap

Run, from any directory:

python3 -B /absolute/path/to/check_geometry.py
python3 -B -O /absolute/path/to/check_geometry.py

Only Python's standard library is needed. No candidate code is imported and no network or file writes occur in the checker. Polynomial equalities are expanded exactly over fractions. Explicit exceptions enforce checks even under optimization.

Both saved runs pass **791 checks, including 8 adverse controls**. The complementary rational tests verify scalar and mixed identities against the separately constructed full polynomial-log tensor at six nonnormalized rational bases and seven arbitrary real directions, including zero and mixed signs. They are not substitutes for the universal analytic proofs.

Strongest verified result: the complete original-space existential theorem for exactly (K,F) above.
Exact remaining mathematical gap at that scope: none found.
Unresolved work outside this audit: worldwide priority/novelty determination; universal existence for all regular cones; signed-cone or other-exponent generalizations.
Completion estimate: **100% of this bounded mathematical audit**. This is a work-completion estimate, not a probability of correctness or a publication/priority assessment.

No communications with external individuals, external mutations, commits, pushes, PR actions, or subagent spawning occurred. Disk was initially full; no deletion or out-of-scope workaround was attempted. After the parent reported disk recovery, only this geometry_01 folder was written.
