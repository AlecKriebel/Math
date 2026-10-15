# PR32 original-stage integral obstruction and action audit

This independent family finds no mathematical repair necessary in CANDIDATE §§4–8. Its verdict is **PASS_ASSIGNED_FORMAL_INTEGRAL_ACTION_FAMILY**, conditional on the separately audited totally real immersion h-principle and the stated interpretation of the source question. This is an original-head family audit, not a complete publication gate, novelty certification, peer review, or approval of a later packet/head.

The target is 6800007 / AMR-067-0007, original head `a92af24e2e6015893787e0c55cd4618f7098917e`, CANDIDATE SHA256 `501c9a536246ad06b29e16720c613bcb292c863857849f837bb0250c45a58050`. The parent supplied actual merge base `01358d66fc67d1c462bddf31c0d4ee5b120e6737`; the snapshot/PR metadata base `c6975ca76f9f667f1250ba403d0e6da2aafe14d0` is different. This family used the frozen exact diff and did not run Git. It verified all fifteen snapshot file hashes and that every added attempt-file body in the sixteen-path diff matches the corresponding original bytes. It does not claim to have independently recomputed the merge base.

## 1. Independence, full target and test boundary

Before reading old reviews, code, outputs, PR metadata, readiness, source audit or any PR32 sibling result, this family retrieved the literal [Morgan–Pansu author-hosted TeX](https://www.imo.universite-paris-saclay.fr/~pansu/problems_MTDG.tex) and read CANDIDATE alone. The flag section's second question, seventh globally, asks for a homotopy classification of totally real immersions of real three-manifolds into the complex full flag manifold. Its next sentence already invokes the h-principle. The preceding real-form orbit question is a different target. The early independent hypotheses, deductions and falsifiers were sealed at `2026-10-02T01:15:57.900314+00:00` in EARLY_INTEGRAL_SEAL.md, SHA256 `d62c9962acbd293d0318518739f8d58aad91917d4cccae6bd90309033f30cf16`. The seal remains unchanged.

Fix a connected smooth second-countable boundaryless real three-manifold M; use ordinary cohomology and ordinary homotopies. There is no orientability, compactness or properness assumption. The ordered flag has its integrable complex structure. Set

\[
A=H^1(M;\mathbb Z),\quad B=H^2(M;\mathbb Z),\quad C=H^3(M;\mathbb Z),
\quad E=TM\otimes\mathbb C,\quad \delta=\beta w_1(TM).
\]

The exact hypotheses to falsify are the admissible labels

\[
\mathcal X=\{(x,y)\in B^2:-4x-2y=\delta\},
\]

the integral map

\[
D_{x,y}(p,q)=(-4p-2q,(2x+y)\smile p+(x+2y)\smile q),
\]

and a formal-class fiber that is a torsor for \(C\oplus\operatorname{coker}D_{x,y}\), with existence exactly when \(\delta\in2B\), equivalently \(w_1^2=0\). The questions tested were whether a nontrivial E changes the loop groups or formulas, whether unstable homotopy or Whitehead terms survive, whether a relative identification is lost, and whether the action counts only framings over a fixed map.

No original or PR30-family file was edited. No additional substantive source-question attempt was charged: the immutable ledger has one original substantive response out of five; this audit adds zero. No new full-target/novelty search, publication, paper, release, DOI, outreach, Git or GitHub action occurred. Completion percentages below concern completion of this audit, not discovery of a new theorem.

## 2. The simultaneous homotopy fiber really remembers formal data

Write T for the determinant-one diagonal torus in SU(3). A map to BT specifies ordered line bundles \(L_1,L_2,L_3\) and a specified product trivialization, not three independently framed lines. There are representations

\[
E_0=L_1\oplus L_2\oplus L_3,
\qquad E_\rho=\bigoplus_{i<j}L_i^*\otimes L_j.
\]

The specified determinant makes \(b_0:BT\to BSU(3)\). The standard bundle \(SU(3)\to SU(3)/T\) identifies the homotopy fiber of b0 with the ordered flag. An SU trivialization of E0 identifies each summand with an ordered orthogonal line in the fixed \(\mathbb C^3\); its changes through such trivializations record homotopies of that flag map. The root representation \(b_\rho:BT\to BU(3)\) is the holomorphic tangent representation. At the standard upper-Borel flag the three lower matrix entries have characters \(t_j/t_i\), i<j, so the three tangent roots are \(x_j-x_i\).

Choose a classifying map \(\tau:M\to BU(3)\) for the generally nontrivial E. Formal data are a flag map and a complex-linear isomorphism of E with its pulled-back tangent bundle. Equivalently, they are torus data, an SU trivialization of E0, and an isomorphism of Eρ with E. Classifying bundles together with their isomorphisms and homotopies therefore gives

\[
\mathcal F\simeq\operatorname{hofib}_{(*,\tau)}
\left[\operatorname{Map}(M,BT)\longrightarrow
\operatorname{Map}(M,BSU(3))\times\operatorname{Map}(M,BU(3))\right]. \tag{F}
\]

This can be made literally by replacing maps by fibrations and using path spaces. Derived mapping spaces commute with this homotopy pullback for CW sources; use compactly generated homotopy function spaces. Smooth M can be replaced by a CW complex of dimension at most three without changing these ordinary homotopy classes. A path to τ remembers the bundle isomorphism, so (F) does not identify E with a trivial bundle. A free U(3) trivialization of E0 would add an erroneous determinant degree; §8 gives an actual-domain counterexample to that alteration.

An arbitrary complex isomorphism is equivalent to the unitary data for these homotopy questions by polar decomposition. That deformation works on bundle isomorphisms over noncompact paracompact M as well. No quotient by diffeomorphisms of M, Weyl permutations or embeddings has been introduced.

## 3. Components and existence, including a genuine nonzero δ

The determinant fibration \(BSU(3)\to BU(3)\to BU(1)\) has 3-connected fiber: SU(3) has π1=π2=0. Thus rank-three complex bundles on any three-dimensional CW complex are classified by c1, and all SU(3) bundles there are trivial. The source components in (F) are B², with

\[
(x_1,x_2,x_3)=(x,y,-x-y),\qquad
c_1(E_\rho)=\sum_{i<j}(x_j-x_i)=-4x-2y. \tag{1}
\]

The determinant of E is the complexified real orientation line. Its transition signs represent the integral Bockstein of w1: lift the mod-two transition cocycle to integers; half its integral coboundary is the complex line's c1. Consequently \(c_1(E)=\delta\), and exactness gives \(2\delta=0\). Equation (1) is precisely the condition that Eρ and E lie in the same target component. Every admissible label has a nonempty formal fiber, because the required two bundle isomorphisms then exist. A reference formal datum can therefore be chosen in each such fiber.

The image of \((x,y)\mapsto-4x-2y\) is exactly 2B: one containment is immediate, and for \(\delta=2z\), choose x=0,y=−z. The integral coefficient exact sequence says \(\delta\in2B\) exactly when its reduction mod two is zero. The cochain Bockstein identity is \(\rho_2\beta u=Sq^1u\), and on a degree-one class \(Sq^1u=u\smile u\). Hence the stated existence criterion is correct, with no division in torsion groups. Nonorientable does not mean nonexistence, and δ nonzero does not mean nonexistence.

A concrete nonzero divisible δ occurs in the closed nonorientable manifold m313(1,0) described in [A. W. Reid's author-hosted appendix](https://math.rice.edu/~ar99/immersionsFKKT_2.pdf), pp2–3. The published manifold presentation and orientation character are inputs, not an independently certified census reconstruction. With the displayed relators, their abelianizations are (4,4) and (0,0), so H1=Z⊕Z/4. The orientation character is a↦0,b↦1. Every integral character has a↦−n,b↦n and therefore equal parity on a,b; w1 has no integral lift, so βw1 is nonzero. The only nonzero order-two class in the torsion of H² is 2 in Z/4. The orientation character does lift mod four, consistently giving w1²=0. The closed nonorientable Euler/UCT calculation gives B=Z/4 here. Thus δ=2 and y must be odd, while x is arbitrary in Z/4: there are eight actual admissible labels. This family does not infer a cup table or complete fiber groups for this example from H1 alone.

For contrast, \(\mathbb{RP}^2\times S^1\) has B=Z/2 with δ its generator. Every −4x−2y is zero; no label exists. The same obstruction holds on the noncompact \(\mathbb{RP}^2\times\mathbb R\). These are actual domains, not arbitrary coefficient tables.

## 4. Rank three, relative dimension and infinite complexes

The fibration \(U(n)\to U(n+1)\to S^{2n+1}\) gives isomorphisms of homotopy groups in degrees i<2n and a surjection at i=2n. At n=3, stabilization therefore gives the required isomorphisms through π5 of U(3), hence through π6 of BU(3). In particular the relative dimension-four loop problem and its dimension-five homotopies are safely in range. Unstable \(\pi_4(SU(2))=\mathbb Z/2\) is not a rank-three loop invariant.

The low stable groups are π2(BU)=Z, π4(BU)=Z, and π1,π3,π5 zero. For a primary proof of periodicity sufficient to evaluate these sphere groups, this audit checked [Hatcher's author-hosted Vector Bundles and K-Theory](https://pi.math.cornell.edu/~hatcher/VBKT/VB.pdf), Theorem2.11 and Corollary2.12, printed54–55, including complete page pixels. Its compact-Hausdorff hypothesis is used on spheres only. Its Theorem1.16 gives paracompact bundle classification; Theorem3.2 gives the integral Whitney formula; Proposition3.13 identifies top Chern and Euler classes.

c1 induces an isomorphism on π2 by the determinant line. c2 induces an isomorphism on π4, with no factor two: the quaternionic Hopf line on \(S^4=\mathbb{HP}^1\), viewed as a complex rank-two bundle, has unit sphere bundle S7. The integral Gysin sequence in degrees zero and four forces its Euler class to be a generator. That Euler class is c2; adding a trivial complex line preserves it. Equivalently the S3 clutching map of the Hopf bundle generates π3(U(2)), and stabilization through U(3) preserves that generator. Choose the sign of the generator consistently with −c2 in the candidate.

It follows that

\[
(c_1,c_2):BU\longrightarrow K(\mathbb Z,2)\times K(\mathbb Z,4)
\]

is an isomorphism on homotopy groups through degree five and has 5-connected homotopy fiber. Its nontrivial further homotopy starts above the dimensions at issue. Relative cellular obstruction theory therefore classifies rank-zero stable classes on a four-dimensional pair by the two integral relative characteristic classes and makes dimension-five homotopies unique up to the requisite equivalence. The analogous map BSU(3)→K(Z,4) has the same sufficient low connectivity.

These are dimension statements on cells, not statements about finite numbers of cells. To lift a prescribed low Postnikov map on an infinite CW pair, extend successively over every cell in each dimension; all corresponding homotopy groups of the fiber vanish. To compare two lifts, do the same on the relative five-dimensional cylinder. The weak CW topology ensures the cellwise extensions define continuous maps and homotopies. There is no unverified passage from classifications of finite subcomplexes to an inverse limit, and no extra phantom ambiguity in this bounded-dimensional argument.

Representable K-theory means maps into Z×BU here. On infinite noncompact complexes it must not be silently replaced by a compact-base Grothendieck construction requiring finite trivial complements. The direct Postnikov argument just given already supplies the classification; stable K notation is convenient for its group structure. A and the other cohomology groups need not be finitely generated; in particular H¹ on an infinite complex must not be presumed a finite free lattice. The universal proof uses none of the finite Smith/minor presentations employed for examples. Ordinary, unrestricted homotopies are essential to this scope.

## 5. Relative coordinates at nontrivial τ, including torsion

A based loop at τ is a rank-three bundle V on X=M×S1 with a specified identification V|Q=E on Q=M×{1}; homotopies are relative to Q. Stable translation by the fixed E puts the loop in the zero component. The resulting class is the relative virtual difference

\[
\xi=[V]-[\operatorname{pr}_M^*E]\in K^0(X,Q).
\]

The specified identification is not lost by using this notation. Projection X→M splits Q→X in representable K-theory. In the relative exact sequence, the restriction K−1(X)→K−1(Q) is surjective; hence K⁰(X,Q)→K⁰(X) is injective. Its image is the kernel of restriction. The virtual absolute difference therefore determines this particular relative class, unlike for a general unrelated pair.

Likewise the pair quotient is \(M_+\wedge S^1\), where M+ adds a disjoint base point and is not a one-point compactification. The split relative integral cohomology is

\[
H^2(X,Q;\mathbb Z)\simeq A\,t,\qquad
H^4(X,Q;\mathbb Z)\simeq C\,t.
\]

Both maps to absolute cohomology are injective. Integral relative obstruction theory in §4 therefore gives a bijection of loop classes with

\[
\left(c_1(\xi)/[S^1],-c_2(\xi)/[S^1]\right)\in A\oplus C. \tag{2}
\]

It is a group isomorphism: translate the mapping-space component by −E in the group-like stable bundle space. For two relative classes ξ,ζ, the only possible Whitney correction is \(c_1(\xi)c_1(\zeta)\). Both first classes contain the circle factor t, so this product is zero exactly, since t²=0. Thus (2) is additive even when C has torsion. Stable translation and the rank-three connectivity transfer this group structure to π1(Map(M,BU(3)),τ). This is a statement about the fundamental group/components of the gauge space, not the false claim that the pointwise nonabelian U(3) gauge group is abelian.

At the constant SU target the determinant coordinate is absent, and the same argument gives π1 Map(M,BSU(3))=C with coordinate −c2/t. The target group of (F) is therefore C⊕A⊕C, genuinely abelian at the specified nontrivial τ. The rational Chern character is neither needed nor sufficient: it would kill the torsion coordinates tested below. Possible nonlinear Whitehead terms have not been assumed away; the integral low Postnikov map and vanishing relative c1 cross product account for them in the dimensions used.

An actual torsion test shows why the virtual choice matters. On M=RP²×S1_x take b the order-two H²(RP²) class, E=L_b⊕1⊕1, and on X=M×S1_t take P with c1(P)=x t and V=L_b⊕P⊕1. The cell differential of RP² is multiplication two from degree-one to degree-two cochains. Tensoring with the two circle complexes shows \(H^4(X;\mathbb Z)=\mathbb Z/2\), generated by bxt, and the parameter-relative top group maps injectively to that same class. The total Chern product gives

\[
c_2(V)=bxt\ne0,\qquad V-E=P-1,\qquad c_2(V-E)=0.
\]

This is a genuine loop in the nontrivial-E target component; P restricts trivially at t=0. M has no admissible flag label, so this example is a target-coordinate counterexample to the ordinary-c2 shortcut, not a purported counterexample to candidate existence. Importantly, torus-image loops alone can hide this mistake: k is always even and 2δ=0, hence δk=0 on every admissible representation loop. The original symbolic nonzero polynomial test does not by itself supply an admissible topological witness for that extra term.

## 6. Integral coupled image, with no rational division

At a component (x,y), loops in BT are pairs p,q∈A. Write

\[
x_1=x,\ x_2=y,\ x_3=-x-y,\qquad
h_1=p,\ h_2=q,\ h_3=-p-q.
\]

The three line classes on X are xi+hi t. K(Z,2) bundle classification and the split product-pair calculation realize every such loop, with the determinant-one product fixed. The SU target coefficient is

\[
a=-c_2(E_0\text{ loop})/t
=-\sum_{i<j}(x_i h_j+x_j h_i)=\sum_i x_i h_i. \tag{3}
\]

Degree two commutes with degree one, so no suppressed odd-class sign occurs in (3). Put rij=xj−xi and kij=hj−hi. The root bundle has first relative coordinate

\[
k=\sum_{i<j}k_{ij}=-4p-2q. \tag{4}
\]

Its ordinary second Chern coefficient is

\[
c_2(V)/t=\left(\sum r_{ij}\right)\left(\sum k_{ij}\right)
-\sum r_{ij}k_{ij}=\delta k-\sum r_{ij}k_{ij}.
\]

Multiplying total Chern classes by the inverse of c(E), through Chern degree two, gives the integral identity

\[
c_2(V-E)=c_2(V)-c_1(V)c_1(E)+c_1(E)^2-c_2(E).
\]

The −c1(V)c1(E) term subtracts precisely δk after slant. Thus the second target coordinate is

\[
b=\sum_{i<j}(x_j-x_i)(h_j-h_i)
=3\sum_i x_i h_i-\left(\sum_i x_i\right)\left(\sum_i h_i\right)=3a. \tag{5}
\]

Equations (3)–(5) are universal integer bilinear identities. They never divide by two or three or infer an integral class from a rational one. Even when the base E is nontrivial, the image is precisely

\[
\operatorname{im}(\pi_1 X\to\pi_1 Y)=\{(a,k,3a):p,q\in A\}. \tag{6}
\]

No extra loops are missing: π1 Map(M,BT)=A² exactly, while all target loops have the relative coordinates in §5. The independent control multiplies total Chern polynomials and their formal inverse with integer sparse arithmetic rather than importing the original symbolic calculation. Its square-zero circle parameter is used only after line-loop classes hi t have even degree; the resulting integer bilinear coefficients are valid for arbitrary integral cup products, including torsion. Numerical specializations supplement this calculation and do not replace the universal proof.

Abstract quotient-group examples alone cannot certify the coefficient three in (5). If one altered only b to an arbitrary integer multiple ℓa, the row operation v−ℓu would still split off the same abstract C factor. The coefficient three is certified by the direct integral representation calculation, not inferred from quotient counts. The separately rejected wrong-coefficient matrix in the code changes both the SU coefficient −3 to −2 and the root coefficient −9 to −4; it is explicitly labeled that way.

## 7. Why the full fiber is this orbit quotient

For any map of homotopy spaces X→Y, fix a path from the image of a source reference x0 to the target reference y0. A point of its homotopy fiber is (x,γ). If x is in the component of x0, choose a path α from x0 to x. Transport γ along its image to obtain a loop at y0. Every target loop arises by keeping x=x0. Choosing a different α changes that loop by the image of π1(X,x0); and a homotopy in the fiber changes it by exactly such an image. This is a direct path-space proof that the fiber components over that source component form the π1(Y,y0) orbit, with stabilizer im π1X. π2 terms affect higher groups of the fiber and introduce no additional π0 identifications.

In (F), the target fundamental group is the abelian group C⊕A⊕C established in §5. Hence these components are a torsor for

\[
(C\oplus A\oplus C)/\operatorname{im}(a,k,3a). \tag{7}
\]

An integral automorphism, valid for every abelian C and its torsion, is

\[
(u,m,v)\mapsto(v-3u,m,u),\qquad
(u',m',v')\mapsto(v',m',u'+3v') \text{ for its inverse}.
\]

It takes each image vector to (0,k,a). Finally

\[
a=(2x+y)\smile p+(x+2y)\smile q,
\]

so (7) is exactly a torsor for C⊕cokerD. The construction allows arbitrary homotopies of flag/line-bundle data and their derivative isomorphisms. Restricting to framings over one fixed map would retain the whole target group and miss these identifications. There is no preferred origin unless one reference formal class is chosen.

The general method is prior art. The actual [published Koshkin paper](https://tcms.org.ge/Journals/JHRS/xvolumes/2009/n1a16/v4n1a16.pdf), Theorem3 printed343, and [arXiv0808.0024v2](https://arxiv.org/pdf/0808.0024v2), p10, were independently checked through their full proofs and page pixels. Their assumptions include compact connected simply connected G, connected H and a three-dimensional CW source, and their bundle-of-shifts proof yields an integral stabilizer quotient for underlying maps. This theorem is not directly a theorem about the extra tangent isomorphism, nor applicable by simply taking G=SU(3)×U(3), which is not simply connected. The simultaneous proof above supplies that extra calculation.

The published pp344–345 and v2p11 later discard nonorientable top-degree integral torsion in their de Rham discussion. This is false: RP²×S1 already has H³=Z/2. The integral theorem and this family's independent Postnikov proof do not use that later assertion. It must not be imported as a premise.

## 8. Actual-domain adversaries and exact computations

The controls deliberately test tempting wrong mechanisms rather than only rechecking coefficient arithmetic.

* **Specified determinant and full action.** For E trivial, formal framed flags have homogeneous target \(Z=(SU(3)\times U(3))/T^2\), with diagonal embedding through the line-sum and root representations. Its exact sequence gives \(\pi_1 Z=\operatorname{coker}[{-4}\ {-2}]=\mathbb Z/2\); π2 is the primitive kernel generated by (1,−2), and π3=Z². On the actual noncompact domain open Möbius band×R, homotopy equivalent to S1 with B=C=δ=0, free homotopy classes are conjugacy classes of this abelian π1 and therefore exactly two. Replacing the first SU by U gives π1=Z⊕Z/2; keeping fixed-map framings and omitting the torus action gives Z. Both alterations fail on this actual domain. On R3 the target is connected and the domain contractible, so there is exactly one class; compact-support H³ would fabricate Z².
* **Coupled, not independent coordinate quotients.** On S²×S1 with x=nη,y=−2nη, the full pre-split image matrix is \(\left(\begin{smallmatrix}0&-3n\\-4&-2\\0&-9n\end{smallmatrix}\right)\). For n≠0, its exact minors give free rank1 and torsion factors g,12|n|/g where g=gcd(2,3n); at n=0 the result is Z²⊕Z/2. At n=1 the true quotient is Z⊕Z/12. Taking the images separately in the three coordinates would give only the finite factors Z/3, Z/2 and Z/9 and wrongly remove the free direction. The control checks the full matrix before the unimodular split for n=−20,…,20. These finite ranges are illustrations of the integer presentation proof, not a homotopy proof.
* **Top-degree nonorientable torsion on admissible domains.** The orientation-reversing S² mapping torus has cellular top differential2, A=Z,B=0,C=Z/2; its w1 lifts from the circle and δ=0. The formal fiber is (Z/2)³. Suppressing C gives only Z/2 and loses two actual invariants despite existence.
* **An order-four extension.** For K×S1, let a generate H¹(K;Z), b generate H²(K;Z)=Z/2, and t generate the circle. Integral cellular differential on K is d(b*)=2f*. The product cochains give A=Za⊕Zt, B=Z(a t)⊕Z/2 b, C=Z/2(b t). The circle diagonal gives b cup t nonzero; the free class a t has zero product with either a or t, since a²=t²=0. Write x=m a t+εb, y=−2m a t+ηb. Then a-coordinate (3) is ηp_t+εq_t mod2. The full four-row presentation retaining both C coordinates and their coupled root images gives: (ε,η)=(0,0), (Z/2)^4; (1,0), (Z/2)^2⊕Z/4; (0,1) or (1,1), (Z/2)^3. This holds for every integer m. A mutant that assumes all extensions split into elementary two-groups fails for x=b,y=0.
* **Rational obstruction/label loss.** On RP²×S1, rationalizing δ produces a false admissible zero label. On the genuine orientable lens space L(2,1), B=Z/2,δ=0 and there are four primary labels, while rationalization retains only one. These computations do not cancel or divide torsion.

The final stdlib control has 3,256 recorded assertions, including 3,125 supplementary coefficient specializations, and eleven rejected mutants. Its distinct mechanisms are generated tensor cochain complexes, an integral Whitney-class ring, exact gcds of minors implemented without SymPy, and a homogeneous-frame long exact sequence. No assertion count is offered as proof of the universal topology.

## 9. Original code, actual failures and reproducibility

All fifteen original files, exact sixteen-path diff, both actual original programs, old review/summary, source records/manifests, readiness/status and the one-row ledger were read after the early seal. Legacy PASS was treated as a hypothesis, not inherited evidence. The two original programs were executed unchanged only in isolated ignored copies. The original author output is byte-identical to verification.json, SHA256 `78a85bfdf25f6e46b4a7f479ca6bcf252bd65ce6ccf5219fb738c39e6c6ec447`. The legacy independent 1,595-assertion output is byte-identical, SHA256 `7302545150d78712b9ac8bc51568f11eed3b5b7704d835b957ee4dc328b6fb9f`. Both exit0 with empty stderr under /usr/bin/python3 3.9.6 and SymPy1.14.0.

Two new mathematical-control harness defects actually failed before correction and are retained verbatim:

1. `failures/cochain_shape_v1.py` demanded equality of complete absolute and relative degree-three matrices; their column sets differ. The correction tests equality of the top cell and the incoming integral relation ideal, which is the relevant injection claim.
2. `failures/reid_zero_relator_v2.py` demanded every Reid relator have nonzero abelianization. The second relator has zero abelianization. The correction requires equal coefficients on every row and a nonzero coefficient on at least one row.

Their actual exit1/stdout/stderr and explanatory receipts are preserved. Neither run is a PASS, and neither was a mathematical counterexample. A third closing protected-check harness failed because the PR30 manifest uses the key files rather than members; its exact code/output/receipt are also retained as failures/protected_schema_v1*. The corrected check uses the actual schema and verifies all twenty-six immutable PR30 members. A witness string initially described one wrong-coefficient mutant's order-eight quotient as cyclic; its actual invariant factors were (2,4). That string and the label implying only the root coefficient changed were corrected before the final receipt. The intentionally wrong ordinary-c2 harness also exits1 with an explicit EXPECTED_FAILURE assertion; its stderr is preserved separately and is never converted to PASS.

The final corrected program output SHA256 is `ae30eaeac6a52219e2c18374921005d55a7caa2f27a503ec6e5fc97a9c8dc218`; it exits0 with empty stderr. `reproduce.py` reruns the final controls, expected failure and both unchanged originals in ignored family tmp, compares recorded bytes and checks protected input/early-seal hashes. It never modifies closed family evidence. `REPRODUCE.md` provides the command. Reference downloads, extraction and Poppler page pixels live only in explicitly ignored tmp. `primary_sources_receipt.json` gives exact URLs, hashes and read locations; no foreign PDF/TeX/pixels are in the first-party manifest.

## 10. Required documentary correction and scoped conclusion

The PR body says that only the problem attempt folder changes. The frozen exact diff also changes `unsolved_math_prioritization/QUEUE.md`, promoting the target from queued0/5 to claimed_solved1/5. That scope description needs correction in a later publication packet. The metadata base must likewise not be mistaken for the parent-verified actual merge base. This family has no authority to edit those inputs or current publication material.

No mandatory mathematical repair to the assigned integral formal-classification mechanism was found. The strongest verified result here is the universal formal classification and existence criterion under the stated M/complex-structure/homotopy conventions, conditional on the separately assigned analytic h-principle. The exact source-question solution status, novelty, correctness of every analytic/source convention, future packet integrity and merge permission are outside this original-stage family. The report does not promote the original claimed_solved status or approve a future head. Root must read and reproduce this closed family's actual proof and code before composing the current packet, followed by a fresh whole-package gate.
