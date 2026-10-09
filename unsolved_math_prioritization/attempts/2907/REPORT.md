# KP 4.31 / 2907: reconstructed turn-3 partial report

**Status: VERIFIED PARTIAL LOCAL RESULT; original problem UNSOLVED, 3/5.** This proof-only editorial edition derives from a newly reconstructed report accepted by a fresh independent audit subject to the clarification visibly applied in Section 7, item 3. It is not an exact-byte recovery, does not inherit a missing historical file's hash or acceptance, and adds no turn or approach. The common-collar strengthening from the audit is included in Section 5. AUDIT.md identifies the precise reconstructed input it reviewed; PROVENANCE.md records the editorial changes. No solution of KP 4.31 is claimed.

## 1. Outcome and limits

For the specific two-annulus ball in Cindy Zhang's construction, the recovered argument gives an obstruction to extending any nonzero power of the surface-cork boundary twist over the **complement of the annuli**, even continuously. Consequently, its images under ambient smooth extensions are pairwise inequivalent by a homeomorphism fixed on the entire boundary 3-sphere.

All these complements nevertheless have abstract fundamental group the free group of rank two, with first homology Z². The distinguishing object is the kernel of the boundary-complement inclusion, with the boundary marked pointwise. Varying first homology is not a valid argument here.

An arbitrary prescribed smooth knot can be reached by adding a fixed oriented cobordism shell. This produces connected smooth oriented surfaces of equal genus and with exactly that boundary knot. It does **not** establish that these grafted surfaces are topologically equivalent relative to the outer sphere, or that smooth inequivalence survives grafting. These are the unresolved requirements; the local result cannot be substituted for them.

## 2. Sources and the geometric input

1. Cindy (Suixin) Zhang, *Exotic Surfaces in 4-manifolds and Surface Corks*, arXiv:2604.27545v2, dated May 25, 2026. [Version record](https://arxiv.org/abs/2604.27545v2), [PDF](https://arxiv.org/pdf/2604.27545v2), [HTML](https://arxiv.org/html/2604.27545v2).
2. Allen Hatcher, *Algebraic Topology*, printed pp. 23–24 (PDF pages 32–33), [author-hosted PDF](https://pi.math.cornell.edu/~hatcher/AT/AT.pdf).

The following geometric identifications were checked in Zhang §§4.4–6, especially Proposition 4.2, Theorem 5.1, Corollary 5.2, and Figures 8–10. The ball is C=(I×P)∪h₀, where P is the exterior of the unknotted third Borromean component B₃. Its intersection with the surface is two punctured cocores. The surgery-product identification makes them I×B₁ and I×B₂. Figure 10 identifies their dual-core link with the other Borromean components. The h₀ handle is disjoint from these annuli and attaches along a pushed-in meridian μ₃ in the upper face. The boundary twist is supported on I×∂P in direction λ₃, the preferred longitude of B₃, and is the identity off this support. It fixes a neighborhood of the four-component boundary link L. The ball is standard, and the boundary twist extends smoothly over the underlying ball. Hatcher pp. 23–24 identify the third Borromean component in the complement of the other two as a nontrivial commutator.

Here B₁ and B₂ denote the surviving dual-core circles after cancellation, not the deleted framed surgery components before cancellation. Their labels are chosen to agree with the positions in Figure 10.

### Why the product is a product of pairs

The required assertion is stronger than knowing that the underlying manifold C has a product-plus-handle decomposition. It follows by retaining the punctured cocores in the handle-trading construction. Write a two-handle as D²_core×D²_cocore and remove a neighborhood of the extended core. In each new three-dimensional slice the circle at the center of the surgery solid torus is the circle at fixed radial parameter in {0}×(D²_cocore\ν(0)). Varying that parameter gives the punctured cocore itself. Thus the cocore annulus is precisely the trace of the surgery-dual core in the product. This applies simultaneously to the two disjoint attaching curves; attaching one handle at the opposite end reverses its interval parameter, without changing the product subset. Zhang's §6 explicitly tracks those opposite end assignments. The cancellation is then a single three-dimensional diffeomorphism of P, applied in every slice, carrying the tracked pair to the two circles in Figure 10.

The meridional identification of h₀ must also be retained after deleting the annuli. In the pre-cancellation model its attaching circle is {p}×S¹, with p off the two curves on the punctured torus. A path from p to the boundary avoiding their spine produces the required annulus to the boundary S¹-direction. The path may be chosen in the component meeting the boundary (as in the construction); it avoids both surgery curves and their surgery-dual cores. Consequently the attaching loop remains the peripheral μ₃ in the complement of the dual-core circles, not merely a generator of π₁(P). This is the class actually killed below.

## 3. Complement group and its marking

Let I=[−1,1], let A=(I×B₁)⊔(I×B₂) inside C, and set

M=P\int ν(B₁⊔B₂)=S³\int ν(B₁⊔B₂⊔B₃).

Choose disjoint small product neighborhoods of A and a sufficiently small attaching tube for h₀ disjoint from them. After rounding corners, a compact exterior is

E=C\int ν(A)=(I×M)∪h₀.

The open complement U=C\A is homotopy equivalent to this exterior. Base it at b₋=(−1,b), with b on T₃=∂ν(B₃). The inclusion of the lower copy M₋ induces the quotient

π₁(M,b) → π₁(E,b₋)=π₁(M,b)/⟨⟨μ₃⟩⟩.

This is van Kampen for a two-handle. Its framing does not change this fundamental-group quotient. Meridional filling of the third component replaces ν(B₃), leaving the exterior of B₁⊔B₂ in S³. Those two components form the two-component unlink. Therefore

π₁(E) ≅ π₁(U) ≅ F(x,y),

where x and y can be chosen as meridians of the two surviving components. In particular, the lower-face inclusion is surjective.

Let d be the image of λ₃ under this quotient. After meridional filling, λ₃ is homotopic to the core B₃ of the restored solid torus. The Borromean calculation identifies its conjugacy class with a commutator of a meridional free basis, up to inversion and choices of orientations. In particular:

- d is nontrivial and has infinite order;
- d belongs to [F(x,y),F(x,y)];
- for every nonzero integer k, dᵏ is nontrivial with zero abelianization.

These properties are independent of the chosen basing paths. Exact signs and the conjugating word are immaterial to the obstruction.

## 4. The boundary-kernel obstruction

Let Y=∂C\L and let j:Y→U be inclusion. The complement Y contains the lower copy of M and the vertical torus cylinder I×T₃. At the upper end it contains M with the attaching solid torus for h₀ removed, together with the replacement boundary piece of h₀. **It does not contain an unchanged entire upper M.** This distinction is important but causes no difficulty for the following loop.

Choose a based loop a in M representing a preimage of x under the quotient π₁(M)→F(x,y). Arrange it disjoint from the h₀ attaching circle by general position in the three-manifold, and choose the attaching tube small enough that it also misses a. Its lower and upper copies a₋,a₊ then both lie in Y. They are based at b₋=(−1,b), b₊=(1,b), respectively. Let

v(t)=(t,b),  −1≤t≤1,

be the path in I×T₃ from b₋ to b₊. Concatenations below are traversed from left to right. Define the based boundary loop

q = v a₊ v⁻¹ a₋⁻¹.

The product homotopy I×a lies in I×M⊂U, so

j₍*₎(q)=1.

Use torus coordinates (s,u)∈(R/Z)² in the (λ₃,μ₃) directions. A representative of the twist has the form

f(t,s,u)=(t,s+ρ(t),u),

where ρ is smooth, 0 near −1, and 1 near +1. It is the identity near both end faces and extends by the identity over the rest of ∂C. A reversed convention replaces f by f⁻¹ and has no effect on the conclusion. The representative is the annular Dehn twist crossed with the second circle in the source construction. The support is disjoint from a collar of L.

The twist fixes b₋, b₊, a₋, and a₊. The loop fᵏ(v)v⁻¹ travels k times in the λ₃ direction after projecting I×T₃ to T₃. Hence

j₍*₎([fᵏ(v)v⁻¹])=dᵏ.

Using the product identification of the two copies of a gives

j₍*₎(fᵏ₍*₎(q)) = dᵏ x d⁻ᵏ x⁻¹ = [dᵏ,x].

This element is nontrivial for k≠0. Indeed, the centralizer of the free generator x in F(x,y) is ⟨x⟩. One elementary proof uses reduced words: after factoring off initial and terminal powers of x, any remaining word that begins and ends with a y-letter produces uncancelled y-letters in w x w⁻¹, so that conjugate cannot equal x. If dᵏ commuted with x, it would equal xᵐ. Abelianization forces m=0, contradicting the nontriviality of dᵏ.

Now suppose there were a continuous map G:U→U with G|Y=fᵏ|Y. Since the basepoint lies in Y and is fixed by fᵏ,

j₍*₎ fᵏ₍*₎ = G₍*₎ j₍*₎.

The right side kills q, whereas the left side does not. This contradiction proves:

**Local nonextension theorem.** For each k≠0, the boundary map fᵏ|Y has no continuous extension U→U. In particular, fᵏ does not extend to a homeomorphism of the pair (C,A).

Working with U, rather than requiring a self-map of the chosen compact exterior E, avoids an unjustified assumption that a pair homeomorphism preserves a particular tubular neighborhood. A pair homeomorphism automatically restricts to the open complement.

## 5. The annular family in the fixed standard ball

Choose one smooth extension Ψ:C→C of f using the trace of a boundary isotopy stationary near both endpoints, as allowed by the standard-ball identification and Zhang's Corollary 5.2. On a fixed outer collar the extension is f times the normal-coordinate identity. Because f is the identity on a neighborhood of L, Ψ is the identity near that collared link. For every integer k, set Ψₖ=Ψᵏ and Aₖ=Ψₖ(A). These extensions have one common fixed boundary collar. Thus every Aₖ is a smooth properly embedded union of two annuli with exactly the same four-component boundary link L. This is the common-collar strengthening in PRECISION_OVERLAY.md; the local distinction argument below works for arbitrary smooth extensions of the prescribed boundary powers as well. Two extensions of the same fᵏ give boundary-relative diffeomorphic annular pairs, by composing one with the inverse of the other.

If H:(C,Aⱼ)→(C,Aₖ) were a homeomorphism fixed pointwise on the entire ∂C, then

G=Ψₖ⁻¹ H Ψⱼ

would be a homeomorphism of (C,A) restricting on ∂C to f⁻ᵏ fʲ=fʲ⁻ᵏ. For j≠k this contradicts the local nonextension theorem. Therefore the Aₖ are pairwise inequivalent relative to the entire outer boundary. In particular there is no such relative ambient isotopy or relative diffeomorphism.

On the other hand, Ψₖ itself identifies C\A with C\Aₖ abstractly. Hence all abstract complement groups are F₂ and all their first integral homology groups are Z². If jₖ:Y→C\Aₖ denotes inclusion, the induced isomorphism from Ψₖ carries j₀ along the boundary automorphism fᵏ. It is the change of this marking, equivalently of the appropriate inclusion kernel in π₁(Y), that the witness detects.

There is no contradiction with Zhang's topological equivalence of the closed pairs: a homeomorphism of those closed pairs is not asserted to be the identity outside C, to preserve the separating sphere ∂C, or to restrict to a pair map on this particular ball.

## 6. The exact-knot shell and genus accounting

Fix an exact smooth oriented knot K⊂S³. Orient L as ∂A. There is a smooth connected oriented cobordism S⊂S³×[0,1] whose inner boundary is −L and outer boundary is K. For completeness, merge the four components of L by three oriented bands, obtaining a knot J. Choose a finite sequence of crossing changes and an isotopy taking J to the given embedded K. A crossing change has an oriented genus-one embedded cobordism, obtainable by two local oriented saddles. Concatenating these pieces gives such an S of some finite genus h. Make the final isotopy end at the specified embedding K and use product collars at both ends.

Attach this fixed shell to the standard ball C using its fixed boundary identification and set

Fₖ=Aₖ∪L S.

Appending a collar to a standard ball yields a standard ball. Each Fₖ is a connected properly embedded smooth oriented surface with **exact boundary K**. The common collar near L allows the seams to be smoothed compatibly. The shell has five boundary components, so

χ(S)=2−2h−5=−3−2h.

Both annuli have Euler characteristic zero, and gluing along circles does not change Euler characteristic. Thus χ(Fₖ)=−3−2h. Since Fₖ is connected with one boundary component,

1−2g(Fₖ)=−3−2h,  hence  g(Fₖ)=h+2.

This genus calculation and the exact-boundary construction are valid for every integer k. They are existence and bookkeeping statements, not distinction or equivalence theorems for the grafts.

## 7. What remains open, and what must not be inferred

1. No homeomorphism (B⁴,Fⱼ)→(B⁴,Fₖ) relative to the **outer** S³ has been constructed. Zhang's closed-pair homeomorphism supplies no such map automatically.
2. No invariant has been proved to retain smooth inequivalence after adding this arbitrary fixed shell. A theorem about the particular closed embedding does not imply this for arbitrary grafts.
3. **Required scope correction, applied:** the local obstruction rules out an ambient comparison that restricts to a pair homeomorphism of the original ball fixing its **entire boundary sphere pointwise**. For example, it rules out a comparison that is the identity on the ambient product shell S³×[0,1]. Being the identity only on the two-dimensional surface cobordism S does not imply that condition. A homeomorphism relative only to the outer boundary sphere may move the internal sphere or act nontrivially on it, and is not ruled out by this local argument. The original problem supplies no internal seam marking. See PRECISION_OVERLAY.md.
4. Conversely, there is no local boundary-relative topological isotopy available to paste into the shell. That proposed route is positively obstructed, rather than merely missing a reference.
5. Therefore this report neither solves KP 4.31 nor establishes that all the exact-knot grafts are topologically distinct. The correct status is a partial local obstruction and an unresolved global extension/distinction problem.

## 8. Recovery and verification record

- The missing historical report bytes were unavailable. The reconstructed input and this later editorial edition each have their own newly computed digest; no historical byte identity is claimed.
- Zhang's version record and v2 PDF were independently retrieved; PDF metadata identifies the author and title and reports 24 pages.
- The text of §§4–6 was examined. Rendered PDF pages 11–17 were visually inspected, including Figures 6–14; the decisive product/link checks use Figures 8–10.
- Hatcher printed pp. 23–24, PDF pages 32–33, were both textually and visually inspected.
- Source PDFs, extracted source text, and page images are retained only as local inspection material. They are not a publication payload.
- The reconstruction made two explicit precision repairs: the upper face is punctured by the h₀ attaching tube, and pair invariance is formulated using the open complement. The fresh audit additionally required the full-inner-sphere clarification now applied in Section 7, item 3; its common-collar strengthening is incorporated in Section 5.
- No repository publication, queue edit, or additional research turn is part of this recovery.

See SOURCE_MANIFEST.json and SOURCE_INSPECTION.json for the source identities and actual inspection history. The fresh independent audit accepted the local nonextension theorem and exact-knot genus calculation with the full-inner-sphere clarification. ACCEPTANCE.md and PROVENANCE.md identify the reconstructed input and distinguish it from this editorial edition; MANIFEST.json identifies the present files.
