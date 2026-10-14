# Full defect functor application for a spherical fusion subcategory

**PASS1 lane:** independent application of the published Carqueville–Müller theorem.  
**Date:** 14 October 2026 UTC.  
**Verdict:** the proposed interface is supplied by an existing full oriented defect-TQFT theorem for every full spherical fusion-subcategory inclusion over the complex numbers. The bulk identifications are monoidal natural isomorphisms, with a real boundary-normalization issue that is explicitly handled by the cited construction. This lane does not certify that every historical input has been translated into this model; that is a separate coverage obligation. No new general defect theorem, novelty claim, or original-problem resolution is claimed here.

## 1. Declared mathematical input

Let C be a spherical fusion category over an algebraically closed field k of characteristic zero, and let i: D → C be a full fusion-subcategory inclusion with the inherited duality and spherical structure. In the adopted contract k = ℂ. The inclusion includes its strong monoidal structure; it is not merely an embedding of Grothendieck rings.

Write d_a for the spherical categorical dimension of a simple object, and

Dim(C) = sum over a in Irr(C) of d_a²,  
Dim(D) = sum over a in Irr(D) of d_a².

A retained simple object has the same dimension in D and C. Both global dimensions are nonzero under the characteristic-zero hypotheses. No braiding, positivity, unitarity, pseudo-unitarity, modularity, or nondegenerate S-matrix is required by this application.

The distinguished bimodule is M_i = _D C_C, with

x ▷ m ◁ y = (i(x) ⊗ m) ⊗ y,

and associativity, units, and the commuting-action constraint inherited from the tensor product and associator of C. Its trace is t_m(f) = tr_C(f). The action is the supplied inclusion, not an arbitrarily chosen common property of two categories. Indeed, right-C-linear endofunctors of the regular right module C are determined by their value at 1, and under this identification the left D action is precisely x ↦ i(x) ⊗ –.

The trace must meet two separate requirements: a nondegenerate cyclic Calabi–Yau trace on the finite semisimple underlying category, and compatibility with the left and right partial traces. For this particular bimodule both partial-trace equations are restrictions of the spherical trace identities in C. The inherited pivotal structure is essential for the left equation. This is not an invocation of an unrestricted trace-existence theorem for arbitrary module categories. The separate interface lane gives the detailed trace proof; the requirements above were checked directly against CM Definition 5.16 and its diagrammatic Equation (5.13).

In CM's displayed convention on published p. 52, a C–C′ bimodule labels a 1-morphism C → C′. Thus M_i is a wall from D to C in that convention. Reversal uses the specified adjoint/opposite wall with the sides exchanged, not the original oriented label with its arguments left unchanged.

## 2. What the published theorems say and why they apply

The complete published CM PDF is retained and was independently inspected at the level of definitions, the relevant theorem proofs, and the construction. The relevant chain is as follows.

1. **CM Example 5.5, published p. 48:** a spherical fusion category has the pivotal Calabi–Yau trace. Its tensor product is compatible with this structure.
2. **CM §5.1.3, published p. 51:** a spherical fusion category A gives an orbifold datum in the Euler-completed theory, using an Euler parameter φ_A with φ_A² = Dim(A)^−1. There is a separate choice for each bulk category.
3. **CM Definition 5.16 and Proposition 5.17, published pp. 52–54:** a traced bimodule satisfying both partial-trace compatibilities gives a 1-morphism between these orbifold data. Proposition 5.17 checks the necessary compatibility between the two descriptions of adjoints, separately for the two actions.
4. **CM Theorem 5.18, published p. 54:** spherical fusion categories, traced bimodule categories, bimodule functors, and bimodule natural transformations form the subcategory sFus of the orbifold completion of the Euler-completed Calabi–Yau/Frobenius-algebra model.
5. **CM Theorem 6.4, published p. 63:** applying the orbifold construction to a defect TQFT gives a symmetric monoidal defect bordism functor. This is supported by the actual surface-space and bordism-map construction on pp. 62–63.
6. **CM Example 6.5, published p. 63:** applying this to the Euler-completed trivial theory gives the defect state-sum TQFT with the sFus labels. The restriction to one bulk category is TVBW. The cited justification is CRS3, specifically its Theorem 4.5, which is a monoidal natural isomorphism of full ordinary TQFTs, not merely an equality of closed-manifold values.

There is therefore an oriented defect theory Z_ss in which the bulk labels include D and C and the surface labels include the particular M_i. One can use the full permitted sFus label system, or the restriction generated by these labels together with the identity/adjoint/composite labels and compatible junction data needed in a chosen calculation. Merely specifying an arbitrary pair of surface and point labels without checking adjacency is not allowed.

This result does not depend on an assertion that every arbitrary spherical module category has a trace. It uses the concrete verified trace on the restricted regular bimodule. It also does not require converting C and D to centers and hoping that the two separate TV = RT(center) identifications provide an inclusion map.

## 3. The actual domain and state spaces

CM §6.1, published pp. 57–59, uses a category of oriented, compatibly labelled, conically stratified bordisms. In dimension three:

- An object is a closed oriented stratified surface. Its two-dimensional regions carry bulk labels; its one-dimensional strata carry surface-defect labels; its zero-dimensional strata carry the corresponding line/junction labels.
- A morphism is a compact oriented stratified 3-bordism with a compatible parametrization of its incoming and outgoing boundaries. Three-, two-, one-, and zero-dimensional interior strata receive bulk, surface, line, and point labels with the prescribed adjacency data.
- Bordisms are taken up to label-preserving oriented stratified diffeomorphism relative to their parametrized boundary. Composition is gluing and the tensor product is disjoint union.

The strata are finite and satisfy the source's conical local-model conditions. This is not a claim about unrestricted pathological stratified spaces. CM permits junctions with more than two incident surface strata, beyond the restricted configuration mentioned in its comparison with Meusburger.

For a stratified surface Σ, choose a compatible triangulation τ. The orbifold data refine it to a surface carrying labels of the original Euler-completed trivial defect theory Z_0. The pre-space is V_τ(Σ) = Z_0(Σ^τ). Different triangulations can have different pre-space dimensions. Cylinder evaluation gives transition maps C_{τ,τ′}; in particular P_τ = C_{τ,τ} is idempotent. CM defines

H_ss(Σ) = colim_τ V_τ(Σ) ≅ im(P_τ).

For any labelled 3-bordism Y: Σ_in → Σ_out and a triangulation extending τ_in and τ_out, the refined bordism Y^t gives a map Z_0(Y^t) between the pre-spaces. The map descends to

Z_ss(Y): H_ss(Σ_in) → H_ss(Σ_out),

independent of the choices. In a fixed image-of-projector realization, it is the restriction of P_out Z_0(Y^t) P_in to im(P_in) with values in im(P_out). This is the content of CM Equations (6.8)–(6.9), together with the preceding cylinder construction. No inclusion of raw coloring spaces is being mistaken for an inclusion of physical TQFT state spaces.

## 4. Exact sewing and the inclusion-specific relation

For every composable pair of decorated bordisms Y_1: Σ_0 → Σ_1 and Y_2: Σ_1 → Σ_2,

Z_ss(Y_2 glued to Y_1) = Z_ss(Y_2) ◦ Z_ss(Y_1).

The identity cylinder is the identity on H_ss(Σ), even though its action on a triangulation-level pre-space is a projector. Disjoint union gives H_ss(Σ ⊔ Σ′) ≅ H_ss(Σ) ⊗ H_ss(Σ′), and the same tensor-product rule holds for bordism maps. The empty surface receives k. Reparametrizations of decorated surfaces act through mapping cylinders and all these assignments are invariant under the source category's labelled oriented diffeomorphisms.

Let j_A be the functor that labels an otherwise undecorated ordinary oriented bordism entirely by A, for A = D or C. There are monoidal natural isomorphisms

J_A: Z_ss ◦ j_A ≅ TVBW_A.

The relation produced by i is the common decorated-bordism extension Z_ss together with these two identified bulk restrictions and the distinguished wall M_i. It evaluates mixed D/C bordisms and their state spaces with a wall whose action and coherence contain i. That is a genuine inclusion-specific interface relation.

A useful family of comparison maps is obtained from a wall cylinder W_i(Σ). Its underlying 3-manifold is Σ × [0,1]; the incoming region is D, the outgoing region is C, and the middle copy of Σ is the oriented M_i wall. Define

T_i(Σ) = J_C(Σ) ◦ Z_ss(W_i(Σ)) ◦ J_D(Σ)^−1:
TVBW_D(Σ) → TVBW_C(Σ).

These maps exist on every closed oriented surface. They commute with oriented diffeomorphisms and respect disjoint unions because the corresponding decorated bordisms are isomorphic or disjoint unions. They also participate in the full sewing law above, including sewing along surfaces intersected by defects.

For a general ordinary bordism Y: Σ → Σ′, however, the two composites involving T_i and the D- or C-bulk evaluation are bordisms with walls next to different ends. Their wall topologies are Σ and Σ′. The defect-TQFT theorem does not identify them. Thus it does not assert

TVBW_C(Y) T_i(Σ) = T_i(Σ′) TVBW_D(Y)

for every undecorated Y. A topological wall can be moved by an allowed isotopy without being erased or forced through a topology-changing bordism. Sewing with the reversed wall gives the double-wall bordism; it does not automatically give the identity cylinder. The corresponding categorical composition is governed by the relative tensor product and appropriate junction data, not by an unproved cancellation rule.

## 5. Bulk normalization and the boundary conjugation

The Euler parameter is chosen separately:

φ_D² = Dim(D)^−1,    φ_C² = Dim(C)^−1.

For closed triangulated bulk manifolds this yields the usual vertex normalization Dim(A)^−v for A's state sum, together with A's own edge dimensions and tetrahedral/associator weights. The subtheory must not inherit Dim(C) as its vertex factor. A fusion-ring inclusion has no implication that these global dimensions agree.

There is a second, subtler issue for nonempty boundary. CRS3 §4.3, inspected in the complete arXiv v2 source on pp. 40–41, explains that its orbifold construction distributes boundary normalization symmetrically between incoming and outgoing sides, while the cited Turaev–Virelizier construction distributes the corresponding weights on the incoming side. Thus equality of the raw linear maps is not the correct statement.

For a boundary surface with embedded dual graph Γ and coloring c, define the nonzero factor

f_A(Σ,Γ;c) = Dim(A)^{|Σ minus Γ|/2} product over e in Γ_1 of d_{c(e)}^−1/2.

Here |Σ minus Γ| is the number of complementary regions. The square roots are chosen consistently with the orbifold datum. This is a diagonal rescaling on the direct sum of colored pre-spaces, not a single scalar independent of c. CRS3 Equation (4.70) gives, with the corresponding choices,

Z_orb(Y^t) = f_A(Σ_out,Γ_out)^−1 ◦ p_TV(Y) ◦ f_A(Σ_in,Γ_in).

Equivalently, each matrix block between specified incoming and outgoing colorings has the scalar ratio f_A,in/f_A,out appearing in CRS3 Equation (4.70).

Equivalently J_A,out Z_orb(Y) = TVBW_A(Y) J_A,in, where J_A is induced by the diagonal f_A. The relation intertwines cylinder projectors and hence descends to the actual state spaces. Multiplicativity of f_A under disjoint union makes J_A monoidal. CRS3 Theorem 4.5 states precisely the resulting monoidal natural isomorphism.

CRS3 Equation (4.39) notes equivalence for choices of the auxiliary simple-dimension square roots ψ_i. This audit fixes consistent available root choices and does not assert an unproved canonical, choice-free identification of the entire defect theory or the numerical wall amplitudes. The verified ordinary bulk identification is sufficient for the proposed relation.

## 6. Boundaries on the conclusion

The established output is a (3,2)-dimensional oriented defect functor: all closed decorated surfaces and all compact decorated 3-bordisms between them. It includes bordisms with nonempty incoming/outgoing boundary. This does not by itself assert a fully extended oriented TFT down to points, or an open-boundary theory on surfaces with boundary and freely chosen physical boundary conditions. CM Remark 5.19 separately discusses the still-expected canonical SO(3) homotopy-fixed-point structure; it must not be silently claimed as an accomplished part of Theorem 6.4.

Neither a monoidal natural transformation between the two different undecorated bulk theories, nor equality/equivalence of those theories, nor invertibility of M_i, nor injectivity/surjectivity of T_i(Σ) follows from the theorem.

There cannot be a universal monoidal natural transformation of these normalized bulk theories for all inclusions. For the standard inclusion Vec ⊂ Vec_(Z/2), the pointed state sum on a connected triangulated S³ has 2^(v−1) flat labelings and vertex factor 2^−v, giving TVBW_(Vec_(Z/2))(S³) = 1/2, whereas TVBW_Vec(S³) = 1. Flat labelings are assignments of group elements to vertices modulo a common group element because S³ is simply connected. A monoidal natural transformation has an invertible component at the empty surface; naturality for S³: empty → empty would force these scalars to agree. This simple obstruction concerns the stronger ordinary-TQFT-map formulation; it does not obstruct the defect extension just constructed.

CM Example 6.5 explicitly leaves detailed agreement with Meusburger's particular defect state sum for future work. This audit invokes CM directly and does not identify the two defect constructions, even on the overlap, merely because their labels have the same names.

The theorem also does not by itself reconstruct a spherical fusion category from every historically described fusion-rule/6j data set. To apply it to the original qualitative problem, the separate source-translation lane must match the actual finite, semisimple, duality, pivotal/spherical, subsystem-closure and normalization data. Likewise, an α-induction example enters once it gives the required actual full spherical inclusion. The absence of a modularity requirement here is meaningful, but it is not a proof that arbitrary ribbon input plus an unspecified algebraic object always provides that inclusion.

## 7. Audited references and inspection level

- **CM:** N. Carqueville and L. Müller, *Orbifold Completion of 3-Categories*, Communications in Mathematical Physics 407, article 8 (2026), version of record published 6 December 2025. Complete published PDF: https://link.springer.com/content/pdf/10.1007/s00220-025-05434-y.pdf . Relevant inspection: §§5.1.2–5.1.3, published pp. 47–54; §§6.1–6.2, pp. 57–63. Pages 51, 53, 54, 62 and 63 were also rendered and visually checked. Article DOI: https://doi.org/10.1007/s00220-025-05434-y .
- **CRS3:** N. Carqueville, I. Runkel and G. Schaumann, *Orbifolds of Reshetikhin–Turaev TQFTs*, Theory and Applications of Categories 35 (2020), 513–561. Complete inspected version: https://arxiv.org/pdf/1809.01483v2 . Theorem 4.5 and Equation (4.70), p. 41; bulk normalizations and square-root choices, §4.2; underlying TV construction, §4.1. Page 41 was rendered and visually checked. Direct publisher-PDF retrieval was attempted and failed; this lane does not describe the auxiliary CRS3 PDF as a freshly verified version of record.
- The acceptance contract and independent source adjudication were read before the application. Their source/model caveats are preserved above.

This is a theorem-application audit with an explicit inclusion-dependent interface and normalized full-functor conclusion. It relies on the published construction and does not purport to reprove every general orbifold coherence theorem in CM. Source PDFs, extracted source text and source-page renders remain separate from this authored report.
