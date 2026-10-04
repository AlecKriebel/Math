# Kirby Problem 4.11: five unsuccessful routes and proved reductions

Numeric target **2887 / KP-4.11**, queue rank 595. Research date: 2026-10-04 UTC.

**Outcome: UNSOLVED. Neither part has been resolved.** This is a complete account of the deductions obtained, not a complete proof of the requested existence assertions. The principal deductions below are elementary consequences of established theorems or rederivations of known facts; no novelty is claimed.

## 0. Exact target and conventions

For a smooth embedding f:S²→M with trivial normal bundle, write M_f for the Gluck twist. The target asks:

- (a) Is there an **orientable** M and f for which M_f is homeomorphic, but not diffeomorphic, to M?
- (b) Is there an **orientable** M and **homotopic smooth embeddings** f,g with trivial normal bundles for which M_f and M_g are homeomorphic, but not diffeomorphic?

Source: Baykur–Kirby–Ruberman (eds.), *K3: A New Problem List in Low-Dimensional Topology*, author preliminary version, Problem 4.11, printed/PDF page 199 [K3]. This numbering is that of the 2026 K3 list, not an unidentified older Kirby-list edition. The problem does not explicitly restrict M to be closed or compact. No blanket compactness convention was found in the book's general introduction, Chapter 4 introduction, or Section 4.1 conventions. We retain the full stated target and do not discard noncompact ambient manifolds. The Akbulut–Yasui invocation and Proposition 3.1 below, and the stated KPR conclusions, are restricted to compact connected M. Their proofs here establish no extension to noncompact M. Other results retain their separately stated hypotheses; none excludes examples outside those hypotheses.

Put N=S²×D² and E=M\int(N). In product coordinates on B=∂N, the twisting map is

τ(x,e^{it})=(R_t x,e^{it}),

where R_t rotates S² about a fixed axis through angle t. The loop R represents the nonzero class of π₁(SO(3))=Z/2. The original attaching identification is suppressed; M=E∪N and M_f=E∪_τN. We use the canonical identification of E in the two manifolds.

A positive answer to (a) using a null-homotopic f also gives (b): choose a small unknotted sphere g. In general (a) and (b) must be kept separate. In particular, non-diffeomorphic M_f,M_g need not both be homeomorphic to M. We do not infer either unrestricted part from the other.

## 1. Route 1: topology of the gluing, and the essential-fibre trap

**Attempt.** Obtain a homeomorphic candidate from the topology of the cut-and-paste, then detect a difference in the intersection form. The topology is sufficiently rigid in a null-homologous simply connected setting, but intersection-form changes in an essential-fibre example destroy the homeomorphism requirement.

### Proposition 1.1. Fundamental group and coarse invariants

For a connected smooth M and f as above,

π₁(M_f)≅π₁(M).

If M is compact, χ(M_f)=χ(M). If M is compact and oriented, its signature is unchanged.

**Proof.** The generator of π₁(B)=Z is a meridian μ. Take its basepoint at a pole of the rotation, so τ fixes the representing loop pointwise. Since N is simply connected, van Kampen gives both groups as π₁(E)/⟪μ⟫. The Euler characteristic follows by additivity for the identical pieces E,N,B. For the signature use Novikov additivity across the closed 3-manifold B; N has zero signature. These conclusions do not assert that the full intersection forms are isomorphic. ∎

### Proposition 1.2. The topological part for a null-homologous sphere

Suppose M is **closed, simply connected, smooth and oriented**, and [f(S²)]=0 in H₂(M;Z). Then M_f is orientation-preservingly homeomorphic to M.

**Proof.** Write S=f(S²). Excision and the Thom isomorphism for its trivial oriented normal bundle identify H_i(M,E;Z) with H_{i−2}(S²;Z). In particular H₃(M,E)=0 and H₂(M,E)=Z. The map H₂(M)→H₂(M,E) is algebraic intersection with [S], hence zero. The pair sequence consequently gives

H₂(E)≅H₂(M),  and  H₁(E)≅Z,

where the second assertion uses H₁(M)=0 and the meridian as generator. The boundary S²×{pt} represents zero in H₂(E), because its image in H₂(M) is [S]=0 and H₂(E)→H₂(M) is injective.

The map τ acts trivially on the integral homology of B: it preserves the circle projection, has degree one on each sphere fibre, and preserves the orientation of B. In the Mayer–Vietoris sequence for M_f, the map

H₂(B)=Z → H₂(E)⊕H₂(N)=H₂(E)⊕Z

is therefore (0,±1), while H₁(B)→H₁(E) is an isomorphism. Thus inclusion induces H₂(E)≅H₂(M_f). The two identifications with H₂(E) preserve the intersection pairings, since cycles can be put in transverse position in the common interior of E. By Proposition 1.1, M_f is simply connected. Both Kirby–Siebenmann invariants vanish because both manifolds are smooth. The classification of closed simply connected topological 4-manifolds then identifies them by an orientation-preserving homeomorphism. This last classification theorem is an external input [Freedman], not proved here. ∎

This proof also shows why the sphere's vanishing homology class matters. One cannot use the same argument for an arbitrary sphere merely because τ acts trivially on boundary homology.

### Proposition 1.3. The standard fibre is a negative control

Gluck twisting a fibre S²×{pt} in S²×S² gives the nontrivial oriented S²-bundle over S². These two total spaces are not homeomorphic.

**Proof.** Split the base S² into two discs. The product bundle glues two S²×D² pieces by a constant clutching loop. Gluck twisting one fibre changes that loop by the nonzero element of π₁(SO(3)). This is precisely the nontrivial oriented sphere bundle. In the trivial bundle, a fibre F and a section D have pairing matrix

Q₀ = [[0,1],[1,0]].

In the twisted bundle choose the section at a pole fixed by the rotations. Its vertical normal plane is clutched by one full rotation, so its Euler number is odd; choosing the sign and then adding multiples of F gives the matrix

Q₁ = [[0,1],[1,1]].

Q₀ is even because (xF+yD)²=2xy. Q₁ is odd because D²=1. Parity is invariant under integral change of basis and orientation reversal. Hence the forms cannot be isomorphic, even up to overall sign, and the manifolds cannot be homeomorphic. Both have π₁=1, χ=4 and signature 0. ∎

More generally Q_k=[[0,1],[1,k]] changes to Q_{k+2r} under D↦D+rF. Its parity is k modulo 2. This exact calculation rules out a false positive in the simplest bundle family, rather than providing an exotic pair.

**Exact gap after route 1.** Proposition 1.2 supplies homeomorphism in a useful class, but no smooth distinction. Proposition 1.3 supplies a smooth distinction that is already topological and therefore fails the target.

## 2. Route 2: local knots and homotopy 4-spheres

**Attempt.** Place a complicated 2-knot inside a ball, hoping its Gluck twist supplies the smooth distinction missing above.

### Proposition 2.1. Local twists reduce to connected sum with a Gluck sphere

Let K be a smooth 2-knot inside a standard ball B⁴⊂M, and let Σ_K be its Gluck twist in S⁴. Then, with compatible oriented gluing conventions,

M_K≅M#Σ_K.

Moreover Σ_K is a smooth homotopy 4-sphere and hence is homeomorphic to S⁴.

**Proof.** Let W be the ball B⁴ after twisting K in its interior. Its outer S³ boundary and a collar are unchanged. Capping W with a standard ball gives Σ_K. On the other hand M_K=(M\int B⁴)∪_{S³}W, exactly the connected-sum construction using the capping ball in Σ_K. Compatible boundary identifications suffice; the usual independence of the oriented connected sum uses extension of orientation-preserving S³ diffeomorphisms over B⁴.

For completeness, Σ_K is simply connected by Proposition 1.1. The exterior of K in S⁴ has H₁=Z generated by a meridian and H₂=H₃=0, by Alexander duality. In Mayer–Vietoris for the twist, H₂(B)→H₂(S²×D²) and H₁(B)→H₁(E) are both isomorphisms. It follows that Σ_K has the integral homology of S⁴. A simply connected homology 4-sphere is a homotopy 4-sphere by Hurewicz and Whitehead, and Freedman's topological 4-dimensional Poincaré theorem identifies its homeomorphism type. ∎

For the unknot U, the twist is diffeomorphic to S⁴: the boundary rotation extends over its exterior S¹×D³ by (e^{it},v)↦(e^{it},R_t v). In a ball this gives the usual trivial local Gluck twist, and M_U≅M [KPR, Proposition 1.5].

Thus a nonstandard Σ_K would answer both parts positively with M=S⁴: every map S²→S⁴ is null-homotopic, so K and U are homotopic. Conversely, proving Σ_K≅S⁴ for one K only disposes of that K; it says nothing about all local knots or about essential spheres in general M.

**Exact gap after route 2.** No explicit K with a provably nonstandard Σ_K was found. This route reaches K3 Problem 4.9, the unresolved subproblem about Gluck twists in S⁴, rather than bypassing it. We do not identify it with the full smooth Poincaré conjecture: not every hypothetical exotic 4-sphere is known to arise this way.

## 3. Route 3: odd classes, stabilization and cork-transfer attempts

**Attempt.** Start with an ambient manifold with tractable odd intersection form, or stabilize a candidate to create a calculable handle description. This makes broad families of twists trivial.

For compact connected smooth M, we use the following published input from Akbulut–Yasui [AY, Theorem 1.1]: if sphere surgery

M°_f = E∪(D³×S¹)

contains an integral spherical 2-homology class of odd square, then M_f≅M. This is stronger than merely requiring such a class in E, but it does **not** say that oddness of the intersection form of M alone is sufficient.

### Proposition 3.1. A disjoint odd sphere excludes an exotic twist

Assume M is compact and connected. If E contains a smoothly embedded sphere A with odd normal Euler number, then M_f≅M.

**Proof.** The same A, with the same tubular neighbourhood, lies in M°_f. Its homology class is spherical and its self-intersection remains odd. Apply [AY]. ∎

### Corollary 3.2. One projective-plane stabilization erases the distinction

For any compact connected oriented smooth M and any f as in the problem,

M_f#CP²≅M#CP².

The same statement holds with the oppositely oriented projective plane.

**Proof.** Form the connected sum in a ball disjoint from f. The projective-line sphere in the added punctured projective plane has square +1 (or −1) and is disjoint from f. Proposition 3.1 makes the twist trivial in the stabilized manifold. Since the surgery support is disjoint from the connected-sum ball, twisting commutes with this connected sum, giving the stated diffeomorphism. ∎

This is a consequence of an existing theorem, not a new stabilization theorem. There is no valid cancellation step from the stabilized diffeomorphism to M_f≅M. Indeed such cancellation is exactly the kind of unsupported smooth classification argument the problem warns against. Likewise, an arbitrary cork twist cannot be replaced by a Gluck twist merely because both are cut-and-paste operations: a cork has a contractible filling and different boundary, whereas the present filling is S²×D².

The matrix identity H⊕[1]≅diag(1,1,−1), where H=Q₀, is checked by the columns (1,0,1), (0,1,−1), (1,−1,1). It illustrates loss of parity information after odd stabilization. It is not a substitute for [AY]'s smooth theorem.

**Exact gap after route 3.** Need a sphere for which the relevant odd spherical class does not exist, together with a genuine unstabilized smooth obstruction. Stabilization simplifies the candidate by removing the very difference to be detected.

## 4. Route 4: homotopic spheres, concordance and geometric duals

**Attempt.** Exploit the extra flexibility of (b), arranging homotopic or concordant spheres so that homeomorphism is supplied by surgery theory, then distinguish the twists geometrically.

For compact connected M and embedded spheres with trivial normal bundles, [KPR, Theorems 1.1–1.2] gives simple-homotopy-equivalent twists for homotopic spheres, and an s-cobordism for concordant spheres. The concordance and resulting s-cobordism are in the chosen smooth or locally flat topological category; a good fundamental group then gives a homeomorphism. For closed orientable M with cyclic π₁, homotopic spheres already yield homeomorphic twists (Corollary 1.3(i)). These statements do not give a diffeomorphism, do not say that homotopy alone always gives homeomorphism for arbitrary π₁, and are not asserted here for noncompact M.

### Proposition 4.1. Ambient isotopy cannot produce an exotic pair

If f and g are smoothly ambiently isotopic, M_f and M_g are diffeomorphic.

**Proof.** Take the endpoint h of an ambient isotopy carrying f(S²) to g(S²). Transport a tubular parametrization for f by h. In these parametrizations h intertwines the two boundary twisting maps exactly. Its restriction to the exterior, together with the induced map on the reattached S²×D², therefore descends to a diffeomorphism M_f→M_g. Changing the oriented normal trivialization does not affect the conclusion: its difference is a map S²→SO(2), which is null-homotopic. ∎

Gabai's published light-bulb theorem [Gabai, Theorem 1.2] says that homotopic smooth spheres in an orientable 4-manifold with no order-two element in π₁ are ambiently isotopic if they have a **common embedded transverse sphere with trivial normal bundle**. Consequently such pairs cannot answer (b). Merely having an algebraic dual, having separate duals, or allowing a transverse sphere of unspecified normal Euler number does not establish these hypotheses.

For example, consider a sphere R in S²×S² homologous to a standard factor and sharing the other factor as a transverse sphere with the standard representative. Simple connectivity converts homology equality to homotopy equality. Gabai gives an isotopy, and Proposition 4.1 gives identical twisted diffeomorphism types. The homeomorphism gate is satisfied for that pair, but the required smooth distinction is absent.

**Exact gap after route 4.** Need homotopic spheres escaping the common-dual/no-two-torsion isotopy criterion, then an invariant of the resulting manifolds. Nonisotopy of embeddings is insufficient: Proposition 4.1 gives one implication only. A diffeomorphism of the twisted manifolds need not remember their distinguished cores or restrict to a diffeomorphism of the original pairs.

## 5. Route 5: Seiberg–Witten discrimination and its null-homologous obstruction

**Attempt.** Use a gauge invariant to distinguish M and M_f, especially in the simply connected null-homologous class where Proposition 1.2 already gives a homeomorphism.

### Proposition 5.1. Ordinary Seiberg–Witten invariants cannot distinguish this class

Assume M is closed, oriented, simply connected, b₂⁺(M)>1, and [S]=0, where S is a smooth embedded sphere of square zero. Under the cohomology identification induced by the common exterior, M and M_S have the same ordinary Seiberg–Witten invariants.

**Justification with explicit external inputs.** Use the local Kirby-calculus identity that Gluck twisting S is equivalent to blowing up a point of S and then blowing down its proper transform S′ of square −1. This identity, and the resulting gauge-invariant equality, are recorded with a diagram and proof in [AKMR, Lemma 2.3, pp.4–5]. Put Y=M#overline(CP²), with exceptional class e. Since [S]=0, [S′]=±e. The orthogonal complement e⊥ in H²(Y) is therefore the same for the two blowdown descriptions Y→M and Y→M_S. Identify their cohomology using this complement and compatible homology orientations. The Seiberg–Witten blowup formula evaluates the invariant of either blowdown at K by evaluating SW_Y at a lift K+e, choosing the sign to match S′. The ±e lifts have equal blowup coefficients. The two evaluations agree for every spin^c structure under this identification. Simple connectivity removes torsion ambiguity in identifying spin^c structures by their characteristic first Chern classes. The b₂⁺>1 restriction avoids chamber choices. No claim for unrestricted boundary invariants, relative invariants, or chamber-free b₂⁺=1 invariants is being made. ∎

This is a reconstruction of a known obstruction with declared blowup-formula and Kirby-calculus inputs, not an independently developed gauge theory proof. The cited manuscript is an author-hosted unpublished 2018 manuscript, not a verified peer-reviewed publication. Its precise identity is preserved in the source manifest; the filename is misleadingly similar to a different later paper called *Exotic families of embeddings*.

If S and T are both null-homologous in the same M under these hypotheses, the same argument gives SW(M_S)=SW(M)=SW(M_T), with compatible identifications. Thus this route cannot settle either part in that subclass using the ordinary invariant. Equality of the invariants does not prove diffeomorphism. For non-null spheres we make no universal gauge-theoretic classification claim.

**Exact gap after route 5.** Need a smooth distinction that survives these identities, or a rigorously analysed candidate outside their hypotheses. No such invariant evaluation or candidate has been produced. Changing the target to sphere nonisotopy, using a relative invariant without a gluing theorem, or dropping orientability would not complete KP-4.11.

## 6. Literature false positives and final gap

[KPR, Proposition 1.6] constructs homotopic smooth spheres whose twisted manifolds are an exotic pair, but its ambient manifold is RP⁴#(S²~×S²), which is nonorientable. The separate orientable example in Proposition 1.4 involves locally flat spheres and produces manifolds that are **not homeomorphic**. Neither is a solution here. These are hypothesis checks, not additional proof-attempt turns.

Torres's 2025 preprint, published in 2026 [Torres], extends exotic nonorientable Gluck-twist examples to many groups. Theorem A explicitly makes their orientation double covers diffeomorphic. Passing to those covers therefore does not supply an orientable exotic pair. No assertion is made that every possible covering construction must fail.

The searches through 2026-10-04 found no verified solution of the exact orientable questions. This is a bounded literature result, not a proof of the absence of later, unindexed, or differently phrased work.

**Remaining target in full:** construct an orientable smooth M with a sphere f such that M_f is homeomorphic and demonstrably not diffeomorphic to M, and resolve the corresponding existence question for homotopic f,g and the pair M_f,M_g; alternatively prove the requested examples impossible in their full intended domain. Neither a construction nor a universal obstruction is present. Five substantive routes are exhausted. Status remains **unsolved, 5/5**, with no complete candidate and no novelty claim.

## References

- [K3] Baykur, Kirby and Ruberman (eds.), *K3: A New Problem List in Low-Dimensional Topology*, 2026 author preliminary version, Problem 4.11, p.199. https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf
- [KPR] Kasprowski, Powell and Ray, *Gluck twists on concordant or homotopic spheres*, Mathematical Research Letters 30(6) (2023), 1787–1811; published online 2024. https://doi.org/10.4310/MRL.2023.v30.n6.a6 ; author manuscript https://www.maths.gla.ac.uk/~mpowell/gluck-paper.pdf
- [AY] Akbulut and Yasui, *Gluck twisting 4-manifolds with odd intersection form*, Mathematical Research Letters 20(2) (2013), 385–389. https://doi.org/10.4310/MRL.2013.v20.n2.a13 ; https://arxiv.org/abs/1205.6038
- [Gabai] *The 4-dimensional light bulb theorem*, Journal of the AMS 33(3) (2020), 609–652, Theorem 1.2. https://doi.org/10.1090/jams/920 ; author offprint https://web.math.princeton.edu/facultypapers/Gabai/Light.Bulb.pdf
- [AKMR] Auckly, Kim, Melvin and Ruberman, *Infinite families of homologous 2-spheres in 4-manifolds*, unpublished author manuscript (2018), Lemma 2.3, pp.4–5. https://pmelvin.blogs.brynmawr.edu/files/2022/05/2018June14ExoticEmbeddings.pdf
- [Torres] *Exotic non-orientable four-manifolds with prescribed fundamental group*, Mathematical Proceedings of the Cambridge Philosophical Society 181(1) (2026), 773–780. https://doi.org/10.1017/S0305004126101935 ; https://arxiv.org/abs/2508.19142
- [Freedman] *The topology of four-dimensional manifolds*, Journal of Differential Geometry 17(3) (1982), 357–453. Bibliographic and applicable classification statements cross-checked through [KPR]; original complete proof not independently audited in this attempt.
