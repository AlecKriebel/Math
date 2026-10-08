# Closed 3-manifold endpoints and smooth pseudo-isotopy

Problem 2945 / KP-4.69. Research date: 2026-10-08.

**Status: partial results; the existence question remains unresolved.**

This report contains five distinct mathematical attempts. Their output is a collection of obstruction-vanishing results and exact reductions, not a solution. In particular, no smooth pseudo-isotopy of a Friedman–Witt twist is constructed, and no obstruction to every such pseudo-isotopy is proved. No novelty claim is made for the elementary deductions below.

## 1. The exact target and conventions

The target is an endpoint diffeomorphism `f: M -> M` of a closed smooth 3-manifold for which a topological cylinder equivalence exists but a smooth one does not. Put `X=M×[0,1]`. The two conditions mean, respectively, the existence of a homeomorphism or a diffeomorphism `F: X -> X` with

- `F(x,0)=(x,0)`;
- `F(x,1)=(f(x),1)`.

There is no requirement that F preserve the interval coordinate. Requiring that would change pseudo-isotopy to isotopy. Because M is closed, there is no lateral boundary condition. Collar straightening permits the product forms near the two ends when needed for gluing. The topological map is a homeomorphism, not a possibly non-injective limit of homeomorphisms. Its endpoint is still the specified diffeomorphism f.

The actual 2026 K3 author manuscript, printed pages 247–248, was inspected in text and as rendered pages. The statement itself does not impose orientability or connectedness. Our attempts concern connected oriented examples and do not exclude nonorientable examples. Any pseudo-isotopy fixes the components: projection of F gives a homotopy from the identity to f. On an oriented connected component, f consequently preserves orientation. A disconnected example would contain a connected example, since cylinder components cannot be permuted by a map that is the identity on the bottom.

K3 also gives the equivalent question of whether the two *parametrized* embeddings `x -> (x,1/2)` and `x -> (f(x),1/2)` can be joined by an isotopy of embeddings. The ambient isotopy in this reformulation fixes both boundary components of X. Their unparametrized images are identical; invariants of the image alone discard the required information. This is source normalization, not one of the five attempts.

Sources: [K3], [G-thesis].

### 1.1. Known input and the test family

Let `M=Y1#Y2`, where each Yi is a metacyclic prism manifold, and let S be the separating connected-sum sphere. In this report that term means a spherical oriented 3-manifold whose finite nonabelian fundamental group has cyclic Sylow 2-subgroup. Let N be a neck `S²×[0,1]`. Choose a smooth loop `R_t` of rotations of R³ that makes one full turn and is the identity near t=0 and t=1. Define

`tau(x,t)=(R_t x,t)` on N, and extend by the identity.

Known results give that tau is homotopic and topologically pseudo-isotopic to the identity, but is not topologically isotopic to it. We use this as an external input, denoted **FW–KS**. K3 names precisely this family as a test case. Galvin's thesis, Theorem 9.2.6 and Question 9.2.8, states the result and the unresolved smooth question. The original Friedman–Witt article was inspected; the Kwasik–Schultz original was not obtained in full. Its topological pseudo-isotopy theorem is therefore used via the explicitly identified K3/thesis statements, not represented as independently proof-audited.

For a concrete algebraic model one can use `Y1=Y2=S³/Dic_3`, with the free left action on the unit quaternions and

`Dic_3=<a,x | a^6=1, x^2=a^3, x a x^{-1}=a^{-1}>`.

Here `a=exp(pi i/3)` and `x=j`. This group has order 12, cyclic Sylow 2-subgroup of order 4, and abelianization Z/4. The precise identification of the whole modern test family uses the later formulation [G-thesis], rather than attributing all its cases to the original 1986 theorem alone.

## 2. Attempt 1: derivative and framing obstructions

**Attack.** A smooth cylinder map must interpolate the stabilized derivatives of its two endpoint maps. Try to obstruct such an interpolation for tau.

Fix an oriented trivialization of TM, which exists for a closed oriented 3-manifold. For an orientation-preserving diffeomorphism f define `d_f: M -> GL^+(3,R)` by expressing Df in that trivialization at its source and target. The chain rule is

`d_(g f)(z)=d_g(f(z)) d_f(z)`.

### Proposition 2.1 (necessary derivative condition)

If f is smoothly pseudo-isotopic to the identity, then `diag(d_f,1): M -> GL^+(4,R)` is null-homotopic.

**Proof.** Use the product trivialization of TX and express DF on M×I as a matrix-valued map. At either boundary the tangential subspace is preserved. Its matrix has the form `[[D(endpoint),v],[0,c]]`, with c positive because the map preserves the inward side. The off-diagonal column and the positive scalar can be deformed to zero and one. Restricting DF along the interval, with these two boundary homotopies appended, gives a homotopy from the identity matrix to `diag(d_f,1)`. No assumption that F is level preserving is used. ∎

### Proposition 2.2 (the separating-twist derivative vanishes)

For any separating sphere twist tau in a closed oriented 3-manifold, `d_tau` is itself null-homotopic, already in GL^+(3,R).

**Proof.** The matrix map is the identity off N and near its boundary, so it factors through `N/∂N` after the entire complement of the interior of N is collapsed to a point. Here the two boundary components of N are collapsed to the same point. The resulting quotient has the homotopy type `S³∨S¹`. The degree-one mod-2 class of this quotient pulls back to the mod-2 Poincaré dual of S: a transverse closed curve counts its passages across the neck. Since S separates, this pullback vanishes. Thus `d_tau` induces the zero homomorphism on π1 and lifts, after the deformation retraction to SO(3), to its universal cover S³.

For any closed connected oriented 3-manifold M, obstruction theory identifies `[M,S³]` with `H³(M;Z)=Z`, by degree. Changing the lift by the nontrivial deck transformation does not change that degree, because the antipodal map of S³ has degree +1. The map `[M,S³] -> [M,SO(3)]` is injective on these classes: a homotopy in SO(3) lifts, and the possible change at its endpoint is this degree-preserving deck map.

The loop of rotations defining tau has order two in π1(SO(3)). Contracting its square through based loops, chosen constant near their endpoints, gives an isotopy of tau² to the identity supported in N. The chain rule therefore makes `d_tau∘tau · d_tau` null-homotopic. Its lifted degree is twice the degree of the lift of `d_tau`: tau is orientation preserving, and multiplication of maps into S³ adds their degree in dimension three. The group Z has no 2-torsion, so this degree is zero. The lift, and then d_tau, is null-homotopic. ∎

This argument is compatible with the derivative crossed homomorphism in [BBP, §§4–6]; their Lemma 5.1 identifies its mod-2 part with the dual of S. We have included the full degree argument to specify exactly why the remaining integer obstruction also vanishes in this case.

**Outcome and obstruction.** The framing and stabilized derivative tests cannot distinguish these endpoints. A null-homotopy of matrices is formal tangential data; it does not integrate to a diffeomorphism of the 4-dimensional cylinder. That integration problem is the unresolved step in this approach.

## 3. Attempt 2: obstruct smooth extension over a filling

**Attack.** A smooth pseudo-isotopy would extend f over every chosen smooth filling of M. Search for a filling over which the separating twist cannot extend, for example by comparing smooth invariants after gluing a cap.

### Proposition 3.1 (extension test)

If f is smoothly pseudo-isotopic to the identity and W is any compact smooth 4-manifold with a fixed identification of its boundary with M, f extends to a diffeomorphism of W.

**Proof.** Take a boundary collar in W, identify it with M×I with the inner edge t=0, and apply a collared pseudo-isotopy there. It is the identity near the inner edge and equals f at the outer edge. Extend it by the identity on the remainder of W. Its inverse is obtained in the same way, so the resulting smooth map is a diffeomorphism. ∎

### Proposition 3.2 (all split fillings fail this test)

Suppose `W=W1 natural W2` is a boundary connected sum, with `∂Wi=Yi` and with the specified neck on `∂W=Y1#Y2`. Then tau extends smoothly over W, whether or not it is pseudo-isotopic to the identity.

**Proof.** Write the joining 1-handle as `D³×[0,1]`, attached along its two end 3-balls. Define `E(v,t)=(R_t v,t)` on the handle and the identity on W1 and W2. Since R_t is identically the identity near the ends, these maps fit smoothly. The inverse is `(v,t)->(R_t^{-1}v,t)`. Its lateral boundary restriction is exactly the sphere twist on `S²×[0,1]`. Equivariant rounding of the handle corners preserves these statements. ∎

**Consequence for a gluing attack.** If V is another 4-manifold with compatible boundary, the closed manifolds obtained by gluing W to V using the identity or tau are diffeomorphic: apply E (or its inverse, according to the gluing convention) on W and the identity on V. Consequently no smooth invariant of those two closed manifolds can detect a difference.

**Outcome and obstruction.** Every boundary-connected-sum filling is unusable for this extension obstruction. An effective filling would have to exploit structure not admitting this matching split. The construction above is an extension over a filling, not an extension over M×I with the other end fixed; replacing one with the other would be an invalid inference.

## 4. Attempt 3: lift to a finite cover and detect the lifted twist

**Attack.** A pseudo-isotopy lifts to a suitable covering cylinder. Try to obstruct it upstairs, where the prime summands of M become simpler.

Let Yi be spherical with groups `Gi=π1(Yi)` of orders `g_i>1`. The homomorphism

`G1*G2 -> G1×G2`

that includes the two factors has kernel K. It determines a regular connected cover `p: Mtilde -> M` of degree `d=g1 g2`.

### Proposition 4.1 (explicit cover)

`Mtilde` is diffeomorphic to a connected sum of `r=(g1-1)(g2-1)` copies of S²×S¹. Its graph of punctured-sphere pieces is the complete bipartite graph `K_(g2,g1)`; its d edges correspond to the lifts of S.

**Proof.** Put `Pi=Yi minus int(D³)`. The universal cover of Pi is S³ with gi open 3-balls removed. In the specified cover there are `d/gi` copies of this punctured S³. A lift of P1 is indexed by the G2 coordinate, and a lift of P2 by the G1 coordinate. Each ordered pair of coordinates gives exactly one neck between the corresponding vertices, hence the complete bipartite graph.

Gluing all necks along a spanning tree combines the pieces into a punctured S³. Each remaining edge joins two of its boundary spheres and adds one S²×S¹ summand. There are `d-(g1+g2)+1=(g1-1)(g2-1)` such edges. This also shows directly that K is free of rank r; no general 3-manifold group classification is needed for the cover construction. ∎

### Proposition 4.2 (the natural lifted twist is smoothly isotopic to identity)

The lift of tau obtained by twisting once on every lifted neck and taking the identity on the complementary pieces is smoothly isotopic to the identity on Mtilde.

**Proof.** Its mapping class is the product of the sphere twists along all edge spheres. In a connected sum of S²×S¹, [BBP, Lemma 5.1 and Corollary 5.2] identify the twist subgroup with `H¹(Mtilde;Z/2)`, sending the twist along a sphere to that sphere's Poincaré dual. The union of all edge spheres is the boundary, mod 2, of the union of all pieces on one side of the bipartition. Thus the sum of their homology classes is zero, and injectivity of the cited identification proves that the product twist is isotopic to the identity. ∎

For the Dic_3 pair the degree is 144 and the cover is `#121(S²×S¹)`. The independent exact graph check confirms that the all-edge cochain is a cut (a coboundary); a single-edge negative control is not a cut.

**Outcome and obstruction.** This cover cannot furnish a non-equivariant isotopy obstruction to a smooth pseudo-isotopy downstairs. Any successful use of the cover must retain the deck action. A deck-equivariant smooth pseudo-isotopy with the required endpoints descends; an arbitrary smooth isotopy upstairs need not. We do not assert an equivariant isotopy or pseudo-isotopy. Indeed an equivariant ordinary isotopy of this lifted twist would descend to an ordinary isotopy of the Friedman–Witt twist, contradicting the known input.

## 5. Attempt 4: a marked mapping-torus obstruction

**Attack.** Convert the cylinder-extension problem into a smooth comparison of closed 4-manifolds, then try characteristic numbers or smooth invariants.

Use the explicit convention

`T(f)=(M×[0,1])/((x,0)~(f(x),1))`.

Write `j_f(x)=[(x,0)]` for its distinguished parametrized fiber and give that fiber the normal coorientation in the direction of increasing interval coordinate. Let `T(id)=M×S¹` have its corresponding marking.

### Proposition 5.1 (exact marked reformulation)

A smooth pseudo-isotopy from id to f exists if and only if there is a diffeomorphism `D:T(id)->T(f)` such that `D∘j_id=j_f` and D preserves the indicated coorientation. The same equivalence holds in the topological category, with locally flat marked fibers.

**Proof.** After straightening its boundary collars, a pseudo-isotopy F descends to D: F sends `(x,0)` to `(x,0)` and `(x,1)` to `(f(x),1)`, which are identified in T(f). It preserves the marking and its normal direction.

Conversely, cut source and target along the marked fibers. Preservation of the coorientation identifies the two boundary sides consistently, giving a cylinder equivalence F. On the bottom, the marking says `F(x,0)=(x,0)`. On the top, `[(y,1)]=j_f(x)` means exactly `y=f(x)`, so `F(x,1)=(f(x),1)`. The cut map is smooth (respectively topological), with the stated endpoints. ∎

### Proposition 5.2 (the classical closed-manifold invariants do not help here)

For the FW–KS family, T(tau) is homeomorphic to M×S¹. Both Yi are rational homology 3-spheres, so

`(b0,b1,b2,b3,b4)=(1,1,0,1,1)` over Q, and `chi=signature=0`.

For the Dic_3 pair, the integral groups are

- `H0=H4=Z`;
- `H1=Z plus (Z/4)^2`;
- `H2=(Z/4)^2`;
- `H3=Z`.

**Proof.** The topological version of Proposition 5.1 applied to the known topological pseudo-isotopy gives the homeomorphism. A spherical 3-manifold has finite π1 and hence zero rational H1 and H2. Connected sum preserves this property. The displayed groups then follow from the connected-sum homology calculation and the integral Künneth formula with S¹. The abelianization calculation for Dic_3 is checked exactly in the supplied script. The rational intersection space is zero-dimensional, so its signature is zero. ∎

**Outcome and obstruction.** Homology, the ordinary rational intersection form, signature and Euler characteristic provide no distinction. This does not rule out finer smooth invariants. More importantly, an abstract diffeomorphism of the two mapping tori would still be insufficient: the theorem requires a specified parametrized, cooriented fiber. The missing result is precisely a marked smooth comparison, or an obstruction to it.

## 6. Attempt 5: cancel the Casson–Sullivan obstruction without changing the endpoint

**Attack.** A topological pseudo-isotopy is a homeomorphism of the smooth 4-manifold X=M×I. Its Casson–Sullivan class might obstruct replacing it by a smooth map with the same boundary values. A single nonsmoothable choice of F is insufficient: the question asks whether *some* smooth F exists. We therefore compute the freedom to change this class while keeping both ends fixed.

We use the following external results from Galvin's final author version, arXiv:2405.07928v2, dated 9 July 2026 [G-CS]:

1. The Casson–Sullivan class of a boundary-smooth homeomorphism of an oriented smooth 4-manifold lies in `H³(X,∂X;Z/2)`, vanishes for diffeomorphisms, and obeys `cs(g h)=cs(h)+h*cs(g)` (Propositions 2.22–2.23).
2. If a compact oriented smooth 4-manifold has finite fundamental group with cyclic Sylow 2-subgroup, every relative class is realized by a boundary-fixed self-homeomorphism (Theorem 1.7 and Proposition 4.13, using the relative construction of Proposition 4.10).
3. Vanishing of the class implies pseudo-smoothability after finitely many interior S²×S² stabilizations (Proposition 2.27, explaining the Freedman–Quinn result).

The composition formula also applies when the boundary restrictions are specified diffeomorphisms rather than the identity: the same difference-of-stable-reductions proof fixes the smooth boundary reductions throughout. It is applied below only with the second map equal to the identity near the boundary.

**Boundary check for input 2.** Proposition 4.10 obtains its product identification relative to both the incoming end and the lateral boundary of the 5-dimensional relative surgery problem. Using the original boundary marking on its other end, the induced self-homeomorphism is the identity on the 4-manifold's boundary. Collar straightening makes it the identity on a neighborhood of that boundary. We need this relative conclusion, not merely an arbitrary diffeomorphism on the boundary. The subsequent applications below involve only finite-group pieces. They do not assume that the free product `G1*G2` is a good group.

### Lemma 6.1 (the fixed-end obstruction is a coset)

Let M be connected and oriented, X=M×I, and let `Q=Homeo(X rel a neighborhood of ∂X)`. Its action on `H³(X,∂X;Z/2)` is trivial. Thus `A=cs(Q)` is an additive subgroup. For a boundary-collared topological pseudo-isotopy F with endpoint f, all classes attainable while keeping its boundary values are exactly `cs(F)+A`.

**Proof.** Every h in Q fixes the bottom, whose inclusion into X is a homotopy equivalence. Hence h induces the identity on `H1(X;Z/2)`. Naturality of Poincaré–Lefschetz duality gives the identity on `H³(X,∂X;Z/2)`. The crossed-homomorphism formula is therefore an ordinary homomorphism on Q. Any second cylinder map F' with the same collars is uniquely `F h` with h in Q. Applying the formula gives `cs(F')=cs(h)+h*cs(F)=cs(h)+cs(F)`. ∎

### Lemma 6.2 (local realization fills the entire group)

Suppose `M=Y1#Y2`, where each Gi is finite and has cyclic Sylow 2-subgroup. Then

`cs(Q)=H³(M×I,∂(M×I);Z/2)`.

**Proof.** Choose disjoint punctured factors `Pi=Yi minus int(D³)` in M and choose `0<epsilon<1/2`. Round the corners of the disjoint codimension-zero submanifolds

`Zi=Pi×[epsilon,1-epsilon]` in the interior of X.

Each Zi has fundamental group Gi. By the relative realization theorem stated above, every class in `H³(Zi,∂Zi;Z/2)` is realized by a homeomorphism hi equal to the identity near ∂Zi. Extend hi by the identity to X, obtaining an element of Q.

The Casson–Sullivan difference obstruction is local: for a map equal to the identity off Zi, its relative class is extension by zero of the class on Zi. This follows from the definition as the difference of the two stable smooth tangent reductions, with their common reduction fixed on the complement; equivalently it follows from excision for the relative obstruction cocycle. Under Poincaré–Lefschetz duality, extension by zero corresponds to the inclusion

`H1(Zi;Z/2) -> H1(X;Z/2)`.

The two inclusions together are an isomorphism onto H1(X;Z/2), since `H1(Y1#Y2;Z/2)=H1(Y1;Z/2) plus H1(Y2;Z/2)`. Thus the attainable extended classes span all of `H³(X,∂X;Z/2)`. Composing the two disjointly supported maps adds their classes, by Lemma 6.1. ∎

### Theorem 6.3 (vanishing representative and stabilized boundary extension)

For the FW–KS twist tau there is a topological pseudo-isotopy F0 from id to tau with `cs(F0)=0`. Consequently for some finite k there is a diffeomorphism

`G:(M×I)#k(S²×S²) -> (M×I)#k(S²×S²)`

restricting to id on the bottom and tau on the top.

**Proof.** Start with a topological pseudo-isotopy F supplied by FW–KS and straighten its end collars. By Lemma 6.2 choose h in Q with `cs(h)=cs(F)`. Then Lemma 6.1 gives `cs(F h)=0`; set F0=Fh. It still has exactly the same boundary values. Apply [G-CS, Proposition 2.27] to F0. Its stabilized topological pseudo-isotopy to a diffeomorphism is relative to the prescribed boundary map, so the resulting diffeomorphism G has the required restrictions. ∎

**Outcome and obstruction.** The endpoint cannot be distinguished by the Casson–Sullivan class of a chosen cylinder map: there is always a zero-class choice in this family. The proved stabilized boundary extension is not a smooth pseudo-isotopy on M. Its domain is a different 4-manifold when k>0. Removing those interior S²×S² summands while preserving both boundary parametrizations is precisely the step not justified here. Neither k=0 nor a uniform bound on k is claimed. This is a deduction from existing realization and stable smoothing theorems, and is not presented as a new resolution of KP-4.69.

## 7. Exact unresolved question

For a fixed FW–KS pair `(M,tau)`, let `E_smooth(M)` be the endpoint image of the diffeomorphisms of M×I that fix a neighborhood of M×{0}; define `E_top(M)` with homeomorphisms. The missing assertion is whether

`tau belongs to E_smooth(M)`.

We know `tau belongs to E_top(M)` from FW–KS. Nontriviality of tau in the ordinary mapping class group only says it is not an isotopy endpoint. The five calculations above do not answer membership in E_smooth. They show, respectively, that one cannot settle it using only the endpoint derivative, split-filling nonextension, an ordinary isotopy obstruction in the explicit torsion-free cover, classical invariants of the unmarked mapping torus, or the Casson–Sullivan class modulo allowed fixed-boundary changes.

No claim is made that these exhaust all approaches, that the test family is the only possible family, or that no later or unindexed solution exists. The global existence question, and the named test case, remain unresolved by this report.

## 8. Source and reproducibility notes

Literature/source checks, category checks and exact computations were assigned zero mathematical-attempt credit. The five counted approaches are Sections 2–6, each of which applies a different mathematical mechanism to the endpoint problem and supplies the stated proof or construction.

The exact script verifies the Dic_3 multiplication, all associativity triples, its derived subgroup and cyclic abelianization, the finite cover graph dimensions and cut cancellation, the mapping-torus Betti arithmetic, and the small mod-2 cancellation model. It cannot verify pseudo-isotopy, the realization theorem, or smooth 4-manifold existence. `python verify_exact_checks.py` reproduces `EXACT_CHECKS.json`; running with `python -O` gives the same result because checks do not depend on Python assertions.

The source manifest distinguishes retrieved full papers, inspected passages, current manuscript versions, and the unavailable original KS96 paper. Source files and corpus contents are not included in this authored candidate.

### References

- [K3] R. İ. Baykur, R. C. Kirby and D. Ruberman, *K3: A New Problem List in Low-Dimensional Topology*, AMS Mathematical Surveys and Monographs 295 (2026), Problem 4.69, pp. 247–248. [Author manuscript](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf).
- [FW86] J. L. Friedman and D. M. Witt, *Homotopy is not isotopy for homeomorphisms of 3-manifolds*, Topology 25 (1986), 35–44. [DOI](https://doi.org/10.1016/0040-9383(86)90003-0). [University-hosted copy](https://www.maths.gla.ac.uk/~mpowell/Friedman-Witt-Homotopy-is-not-isotopy-homeos-3-mflds.pdf).
- [KS96] S. Kwasik and R. Schultz, *Pseudo-isotopies of 3-manifolds*, Topology 35 (1996), 363–376. [DOI](https://doi.org/10.1016/0040-9383(95)00017-8). Original full text unavailable during this pass.
- [G-thesis] D. A. P. Galvin, *Non-smoothable homeomorphisms of 4-manifolds*, PhD thesis, University of Glasgow, July 2024, Chapter 9, especially Theorem 9.2.6 and Question 9.2.8. [Institutional copy](https://theses.gla.ac.uk/84595/1/2024GalvinPhD.pdf).
- [BBP] T. Brendle, N. Broaddus and A. Putman, *The mapping class group of connect sums of S²×S¹*, Transactions of the American Mathematical Society 376 (2023), 2557–2572, especially §§4–6, Lemma 5.1 and Corollary 5.2. [Author copy](https://www.maths.gla.ac.uk/~tbrendle/papers/SplitLaudenbach.pdf).
- [G-CS] D. A. P. Galvin, *The Casson–Sullivan invariant for homeomorphisms of 4-manifolds*, final author version, arXiv:2405.07928v2, 9 July 2026, to appear in Compositio Mathematica; Theorem 1.7 and Propositions 2.22, 2.23, 2.27, 4.10 and 4.13. [Versioned manuscript](https://arxiv.org/abs/2405.07928v2).

Additional sources were screened only for scope/current status; their results are not counted as approaches:

- J. Lin, Y. Xie and B. Zhang, *Pseudo-isotopies of 3-manifolds with infinite fundamental groups*, arXiv:2602.09454v1. Its principal mapping classes act on I×Y and are fixed near its entire boundary; its rank results do not determine our 3-dimensional endpoint image. [Manuscript](https://arxiv.org/abs/2602.09454).
- Y. Ohta and T. Watanabe, *Unstable pseudo-isotopies of spherical 3-manifolds*, 18 October 2023 manuscript. Its boundary-fixed cylinder classes similarly do not give the required endpoint separation. [Author copy](https://www.math.kyoto-u.ac.jp/~tadayuki.watanabe/PI-cylinder.pdf).
- P. Orson, M. Powell and O. Randal-Williams, *Smoothing topological pseudo-isotopies of 4-manifolds*, arXiv:2507.16984v1. The endpoints there are maps of closed 4-manifolds. [Manuscript](https://arxiv.org/abs/2507.16984).
- P. Bader et al., *A survey on mapping class groups of 3-manifolds*, arXiv:2609.00233v1, 31 August 2026. This supplies a recent ordinary mapping-class comparison, not a claimed solution of the pseudo-isotopy endpoint question. [Manuscript](https://arxiv.org/abs/2609.00233).
