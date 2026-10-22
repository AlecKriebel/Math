# Independent audit: Birman Problem 2.1 / 11000158

Date: 2026-10-03 UTC. Reviewer: an independent AI review worker, uninvolved in drafting the supplied packet. This is not external human peer review.

## Verdict

**Accept the candidate mathematical disposition `already_solved`, 0/5 substantive discovery turns, as a credited consequence of prior literature, with one required source-convention clarification before publication.** The complete double-coset target is covered under the explicitly stated equivalence relation: oriented, side-preserving homeomorphism of fixed compression-body Heegaard models, with the chosen boundary data retained. I found no missing theorem or proof component in that formulation. No novelty, first-resolution priority, arbitrary-manifold recognition algorithm, or classification of ambient-isotopy classes is established.

The required clarification concerns a genuine distinction in equivalence relations. Birman's printed p.142 / PDF p.149, last full paragraph before equation (2), says: "the splittings are equivalent if the splitting surfaces are isotopic". She then also requires a diffeomorphism B preserving the two pieces and derives equation (2). In contrast, Problem 2.1 itself on printed p.149 / PDF p.156 contains no isotopy requirement: it asks how to modify H phi H. The equation and the gluing parameters support homeomorphism equivalence. They contain no identification with a pre-fixed ambient M, and cannot classify ambient-isotopy classes without that additional data and restriction on allowed ambient maps. Scharlemann's printed p.2 explicitly distinguishes homeomorphic from isotopic splittings.

PROOF.md lines 14-18 already choose homeomorphism equivalence correctly and exclude ambient isotopy, but lines 8-9 and SOURCE_GATE.md present the source conventions too seamlessly. **Require an additive note explicitly acknowledging this source wording and the adopted double-coset interpretation.** This does not call for a new mathematical discovery. If a downstream gate instead insists that the p.142 isotopy sentence is a literal additional target, the present packet must be marked narrower than that target; it does not solve that stronger classification problem. The prior-resolution recommendation applies to Problem 2.1's stated double-coset formulation, not to this stronger reading.

## Frozen target and integrity

- Repository: `AlecKriebel/Math`.
- Supplied branch: `math/11000158-compression-body-prior-resolution`.
- Audited commit: `b235debbff17fa700be75cef648b44be6fe7b5f9`.
- Repository packet: `unsolved_math_prioritization/attempts/11000158`.
- Local packet: `boundary_three_manifolds_11000158/public`, ten files.
- PROOF.md SHA256: `f2c2ef819f8f8a6291088e409f223d58001d3c85cd854bde550810fe1328dc7d`.
- I separately fetched PROOF.md through the GitHub connector at the exact commit. Its returned UTF-8 content equals the local bytes, and its Git blob SHA is `1878d9122f70229c0c6424a7ac02cbac8917f316`.
- All nine entries in the supplied MANIFEST.json match the local files. The manifest itself and all ten packet files are also hashed in this review's INPUT_MANIFEST.json.
- All ten packet files were read. I reviewed the actual original problem and relevant primary-source text, not only the candidate's source summaries. I made no remote writes, PR, queue change, or modification to the supplied packet.

Verified remote proof: https://github.com/AlecKriebel/Math/blob/b235debbff17fa700be75cef648b44be6fe7b5f9/unsolved_math_prioritization/attempts/11000158/PROOF.md

This audit independently verifies the mathematical source resolution. The packet's campaign-history and duplicate-search narrative was read but not exhaustively repeated; accepting the mathematical result does not independently certify the claimed 439-branch enumeration or all accessible-history searches.

## Exact target and primary-source boundaries

Birman's printed p.149 / PDF p.156, Problem 2.1, asks for the compression-body replacement of a handlebody factor in the Heegaard double coset, how its handles enter that replacement, and the knot-space specialization. The original page was inspected as pixels and text. The statement in the selected dataset agrees. Chapter authorship is Birman, not the misattribution noted in the imported report. The surrounding pp.142 and 145-146 supply oriented gluing, the capped-sphere 2/3-handle model, and the torus-plus-tunnels example. They do not request a finite presentation, decision procedure, or stabilization bound.

Primary source: https://math.uchicago.edu/~farb/papers/mcgbook.pdf

Theorem-level dependencies were checked with their hypotheses:

1. **Biringer-Johnson-Minsky, Lemma 4.2, pp.15-16.** Section 4 defines ordinary compression bodies from a closed orientable positive boundary other than S^2, with newly created spherical boundary capped. Its marked-compression-body lemma says kernel inclusion gives a boundary-compatible embedding; equality gives a homeomorphism. This is not merely the paper's pseudo-Anosov partial-extension theorem, and no pseudo-Anosov or hyperbolic hypothesis is attached to Lemma 4.2. The packet uses the equality conclusion in exactly this ordinary category. I read the proof on p.16 and visually inspected its p.15 statement. https://arxiv.org/pdf/1011.0021v1

2. **Oertel, Definitions 1.1-1.3, Theorems 1.4(b) and 1.5, pp.1-3; proof pp.11-12.** These define images of extension maps, identify the well-defined inner-boundary mapping class induced by an extendible outer class, and prove the surjective restriction exact sequence. At most one spherical inner component is allowed by the relevant theorem; ordinary nonspherical F satisfies this. For closed orientable nonspherical surfaces the universal-cover condition of 1.4 is satisfied. The packet does not import the unrelated four-dimensional generator statements. I read the surjectivity construction, including permutations of homeomorphic inner components, and visually inspected p.3. https://arxiv.org/pdf/math/0607444v2

3. **Bonahon, Appendix B, Proposition B.1 and Corollary B.2, pp.267-268.** The systems are complete and minimal under deletion, not arbitrary finite collections of disks. The proposition connects these systems by slides and isotopies. The proof and the pictured slide were checked. The packet accurately uses this to explain why a particular finite system must not be frozen, not to claim that every arbitrary redundant system is related by slides alone. https://numdam.org/item/10.24033/asens.1448.pdf

4. **Barbar, equation (3.37) and immediately following definition.** This explicitly uses the compression-body/handlebody double quotient with pointwise-fixed inner boundary. Its written formula has one connected inner boundary. The adjacent footnote describes multiple boundary components prospectively, and its topology sums and stabilization limit are not a proof for all the packet's cases. The packet treats it only as corroborating prior use and supplies the wider gluing proof separately. That is appropriate. https://arxiv.org/html/2511.04311v1#S3.SS2

5. **Scharlemann, sections 1, 2.2-2.3, 3.1 and 7.** These support the distinction between homeomorphic and isotopic splittings, the chosen partition of the boundary, the dual handle picture, and the separate role of stabilization. No historical conjecture in that survey is promoted to a current theorem. https://arxiv.org/pdf/math/0007144v1

## Mathematical audit

### 1. Handle kernel and extension subgroup: pass

For the designated positive boundary S, attaching the 2-handles kills exactly the normal closure N_X in pi_1(S); capping sphere components changes no fundamental group. Inclusion is surjective and its kernel is N_X. This statement uses the full normal closure, rather than the subgroup generated without conjugates, a homology subspace, or the finite set of attaching curves.

Necessity of f_*(N_X)=N_X follows by the commutative inclusion square for a homeomorphism of C and its inverse. For sufficiency, the two copies marked by id and f have marking kernels N_X and f_*^{-1}(N_X). Equality is precisely what the quoted marked-body lemma needs, and its boundary extension is f, not f^{-1}. A homeomorphism of a connected oriented 3-manifold preserving the orientation induced on a boundary component is orientation preserving in the interior. The use of outer automorphisms causes no basepoint issue because inner automorphisms preserve every normal subgroup.

The proof concerns the unrestricted extendible image. It does not silently identify that image with a relative subgroup. The later pullback under rho supplies the additional restrictions when inner-boundary data are retained.

Bonahon's slides produce alternative complete systems with the same inclusion kernel. A disk slide can replace a meridian with its band sum with another, so exact setwise preservation of the original finite system is too restrictive. Full disk-set preservation is equivalent here: the attaching meridians are among that full set and normally generate the kernel, while extension maps preserve the full set. No one-way disk-set inclusion has been substituted for equality.

The graph underlying the dual construction has k vertices, n edges and cycle rank n-k+1. The positive genus is therefore sum(h_i)+n-k+1. This independently agrees with the packet's Euler-characteristic calculation. The separate one-0-handle description for empty negative boundary avoids the invalid substitution k=0 into the product construction. Counts alone determine neither the marked kernel in S nor its subgroup placement in Mod(S).

### 2. Both double-coset directions and orientation: pass

Let alpha_i map the first positive boundary to the second. For extensions b_1,b_2 to descend through the gluing equivalence, their exact compatibility is alpha_2 b_1=b_2 alpha_1. Hence alpha_2=b_2 alpha_1 b_1^{-1}, with E(C_2) on the left and E(C_1) on the right. Conversely, if this equation holds only in boundary mapping classes, a boundary collar isotopy of an extension realizes it pointwise without affecting the opposite boundary. The two maps then descend to a side-preserving homeomorphism. Both directions work with all the boundary restrictions being imposed.

For alpha=j phi with j orientation reversing, multiplication by j^{-1} on the left gives phi_2=(j^{-1}b_2j)phi_1b_1^{-1}. Thus the left factor is j^{-1}E(C_2)j. Suppressing this conjugation requires extra compatible choices; it is not valid by mere identification of both positive boundaries with an abstract S. Reversing gluing direction inverts alpha and exchanges the factors. The packet states these distinctions correctly.

The theorem classifies fixed-model splittings under the specified homeomorphism relation. It does not classify the underlying manifold injectively after forgetting the splitting, and it does not classify embeddings up to isotopy in a fixed M. Stabilization changes the genus/model and is a separate relation. Boundary assignment to the sides remains fixed. A side-swap quotient applies only when the full chosen models and retained data allow the swap; this is implicit in the packet's initial fixed-data convention.

### 3. Unmarked, labelled and relative boundary: pass

For ordinary C with nonspherical F, Oertel gives a unique induced mapping class on F from an outer extendible class. Surjectivity is important here and is actually proved in the source: one can realize an arbitrary inner-boundary homeomorphism, including permitted component permutations, on the product pieces and compensate near their attachments to the remaining handlebody.

The kernel of rho is the image of extensions fixed on F. An isotopically trivial restriction can be made pointwise identity by an isotopy supported in a collar of F, disjoint from S. Consequently the relative double coset is obtained by replacing E(C) with ker(rho); permissible mapping classes B on F give rho^{-1}(B). This is not a mapping class group of a punctured positive surface. When F is empty, the displayed exact sequence is the tautological sequence with trivial target, independently of conventions about admitting handlebodies in Oertel's product-based definition.

For a product S x I, all surface classes extend and rho is an isomorphism, so the relative image is trivial. This sharp example detects the error of treating the full and relative groups interchangeably. In genus one, the unrestricted left factor would collapse all product/handlebody gluings to one unmarked class, whereas the boundary-parametrized quotient retains distinct meridian data.

### 4. Knot exteriors and filling slopes: pass

Birman's own tunnel construction yields C_p=(T^2 x I) plus p 1-handles, with genus p+1 positive boundary and torus negative boundary, glued to H_{p+1}. Its p co-core meridians form the required compression system. The packet uses the tunnel count of the chosen description, not a claim that the description has minimal tunnel number.

For a fixed peripheral parametrization the subgroup is ker(rho). Retaining only the unoriented filling meridian uses rho^{-1}(Stab(mu)). The extension criterion over the filling solid torus is exactly preservation of its meridian slope. One can choose the solid-torus extension to preserve its core, giving an equivalence of filled knot pairs; conversely a knot-pair map preserves that slope after aligning tubular neighborhoods. Oriented-knot or longitude data require the corresponding additional restrictions, as the packet says.

This does not assert that every torus-boundary manifold in the unrestricted double-coset family is a knot exterior in S^3. A selected filling must yield S^3. Nor does it assert that an arbitrary unmarked exterior equivalence preserves the chosen meridian. For the unknot the disk meridian of the exterior solid torus and the meridian of the solid torus used to fill it are different slopes. The proof does not conflate them. Its p=0 product/relative discussion is correct.

### 5. Spherical punctures and low genus: pass

Removing interior balls leaves the inclusion kernel unchanged, so a kernel cannot recover the number or side assignment of spherical boundary components. The packet correctly keeps this as extra model data. It also avoids applying Oertel's unique-restriction theorem to several inner spheres, where sphere permutations cannot in general be recovered from the outer mapping class.

The independent extension argument is sufficient: cap a punctured-body homeomorphism by ball homeomorphisms in one direction; in the other direction, isotope an automorphism of the capped body in its interior until it takes the specified finite labelled ball collection to itself. A finite collection of tame balls can be shrunk and transported through the connected interior, using spare locations if necessary so that individual paths do not hit the remaining balls. Isotopy extension fixes the original boundary. Orientation-preserving maps of each resulting sphere are isotopic to the identity and can be corrected in disjoint collars. This argument also works while retaining existing nonspherical boundary restrictions. It identifies positive-boundary images, not full mapping class groups of punctured and unpunctured bodies.

For S^2, the oriented surface mapping class group is trivial; fixed ball/punctured-ball models have one gluing class. For T^2, the only ordinary models are the product and solid torus, with extendible images SL(2,Z) and the meridian stabilizer respectively. If (mu,lambda) is a meridian-longitude basis, a determinant-one matrix preserves the unoriented meridian exactly when its lower-left entry is zero (then the diagonal entries are both +1 or both -1). This provides the separate low-genus check; no genus-two hypothesis is stretched to these cases. Disconnected M is componentwise with any allowed permutation quotient explicitly additional.

## Computational and adversarial checks

The original verifier was replayed, with byte-for-byte equivalent parsed JSON output: 576 double-coset comparisons, 1,700 Euler checks, 50 tunnel-genus checks and 180 integral torus matrices. The original omitted-conjugation mutant is rejected.

A separate implementation, `independent_controls.py`, uses determinant-minus-one matrices over F_5 as an orientation-reversing torsor for SL(2,F_5), not the original S_4 implementation. It checks 14,400 gluing relations and 120 gluing-direction inversions. Dropping conjugation or putting the factors on the wrong sides fails for all 120 test elements. The full/relative/slope-marked finite quotient controls give distinct counts 1, 6 and 2. It independently checks 2,541 genus identities from the graph viewpoint.

Two further negative controls test why weaker interpretations fail. An integral torus Dehn twist can preserve an exterior meridian while changing the selected filling meridian. A genus-two surface-group representation into S_3 has nontrivial first separating commutator but trivial product of the two handle commutators, demonstrating that homology alone loses separating compression data.

During construction of the independent harness, an initially chosen lower-unipotent right subgroup did not distinguish the wrong-side mutant. That failed test-design assertion was not evidence against the proof. Replacing it by the cyclic order-four rotation subgroup produced nondegenerate independent controls; the final checked code and output are frozen. All controls are diagnostics for conventions and elementary algebra. They do not computationally certify isotopy extension, the Loop Theorem, compression-body topology, or the cited published results.

## Required author work and disposition

No mathematical correction or additional new theorem is required for the stated homeomorphism-equivalence answer. Before publication, add an explicit source-convention note to PROOF.md and its source comparison. Suitable substance is:

The double-coset formulation uses side-preserving homeomorphism equivalence, as encoded by Birman's equation (2). Her preceding prose also mentions isotopic splitting surfaces. That stronger relation for surfaces embedded in a preidentified ambient M is not detected by H phi H alone; an ambient marking and restriction to ambient maps isotopic to the identity would be additional data. The answer here resolves Problem 2.1 in its stated double-coset sense, and makes no ambient-isotopy classification claim.

Retain the other limitations prominently. In particular, do not promote Barbar's relative connected-boundary use into a theorem for every marking and boundary type; do not promote the current double coset to underlying-manifold classification; and do not claim new discovery or historical priority for the first answer naming this problem.

The original problem's three explicit requested components are accounted for: the precise extension subgroup, its handle-data criterion, and the knot-space instance. The appropriate disposition remains a credited prior-literature resolution at 0/5 after the source-convention note is added. Under a stronger ambient-isotopy interpretation, full-scope acceptance is not granted.
