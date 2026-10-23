# Restricted regular bimodule interface

**Shared PASS1, row 1787. 14 October 2026.**

## Result and exact scope

Let \(\iota:\mathcal D\hookrightarrow\mathcal C\) be a full fusion-subcategory inclusion over \(\mathbb C\). Equip \(\mathcal C\) with a spherical pivotal structure, and equip \(\mathcal D\) with its restriction. There is an inclusion-dependent oriented topological interface between the two normalized TVBW theories. Its surface label is
\[
  \mathcal M_\iota={}_{\mathcal D}\mathcal C_{\mathcal C},\qquad
  d\triangleright m\triangleleft c=\iota(d)\otimes m\otimes c,
  \qquad t_m(f)=\operatorname{tr}_{\mathcal C}(f).
\]
This label satisfies the two-sided trace requirements of Carqueville–Müller, Definition 5.16. Their Proposition 5.17, Theorems 5.18 and 6.4, and Example 6.5 therefore put it in an oriented defect TQFT whose two ordinary bulk restrictions are **monoidally naturally isomorphic** to \(\operatorname{TVBW}_{\mathcal D}\) and \(\operatorname{TVBW}_{\mathcal C}\).

This is a direct application of published theory with an explicit verification of its input. It imposes neither pseudo-unitarity nor a braiding or invertible S-matrix. It is an interface relation; no equivalence of the two ordinary theories, invertibility of the interface, universal state-space inclusion, or monoidal natural transformation between the ordinary theories is asserted. Source-model coverage is a separate issue addressed in Section 8 below.

## 1. Algebraic input and bimodule coherence

A full fusion subcategory contains the tensor unit, is closed under tensor products, finite direct sums, direct summands, isomorphisms and duals, and has the ambient morphism spaces between its objects. In particular its simple objects are a subset of the simple objects of \(\mathcal C\), its unit remains simple, and its associator and unit constraints are the ambient ones. Fullness ensures that evaluation, coevaluation and pivotal isomorphisms between its objects lie in the subcategory. The restricted pivotal structure is spherical because its traces are computed by precisely the same diagrams in \(\mathcal C\).

The underlying category of \(\mathcal M_\iota\) is \(\mathcal C\), hence it is a finite semisimple \(\mathbb C\)-linear abelian category with finite-dimensional morphism spaces. Set
\[
 d\triangleright m=\iota(d)\otimes m,\qquad m\triangleleft c=m\otimes c.
\]
The left, right and mixed associativity maps are restrictions of the associator of \(\mathcal C\); the unit maps are its unitors. All left/right module pentagons and mixed compatibility diagrams are instances of the ambient pentagon and triangle. Both actions are exact, since all additive functors in this finite semisimple setting are exact. Thus this is an honest finite semisimple \((\mathcal D,\mathcal C)\)-bimodule category.

For a strong monoidal inclusion rather than a literal inclusion, insert the tensor and unit constraints of \(\iota\) in the left-action maps. The assertion requires that \(\iota\) preserve the selected pivotal structure. This is automatic for the inherited structure, and is not automatic for an independently chosen pivotal structure on \(\mathcal D\).

The inherited-structure hypothesis is necessary. For example, let both underlying tensor categories be \(\mathrm{Vec}_{\mathbb Z/2}\), but put the sign spherical structure on \(\mathcal D\) and the standard one on \(\mathcal C\). The identity tensor functor is not pivotal. For the nontrivial invertible simple \(g\), left compatibility would require \(t_g(1_g)=-t_1(1_1)\), while right compatibility would require \(t_g(1_g)=t_1(1_1)\). Nondegeneracy on the simple unit excludes \(t_1(1_1)=0\). Thus the corresponding regular bimodule cannot carry a common compatible trace. This example is outside, and does not weaken, the inherited-structure theorem.

The bimodule is indecomposable: any decomposition into right-module summands places the simple object \(1\) in one summand, and that summand then contains \(1\triangleleft c\cong c\) for every \(c\). Indecomposability is not needed for existence of the interface, but verifies that an unnecessary direct-sum decomposition is not hidden in this construction.

## 2. Duality and trace conventions

Use left-dual data
\[
 \mathrm{ev}_x:x^*\otimes x\longrightarrow1,\qquad
 \mathrm{coev}_x:1\longrightarrow x\otimes x^*,
\]
and the pivotal right-dual maps
\[
 \widetilde{\mathrm{ev}}_x:x\otimes x^*\longrightarrow1,\qquad
 \widetilde{\mathrm{coev}}_x:1\longrightarrow x^*\otimes x.
\]
Then
\[
 \operatorname{tr}^L_x(f)=\mathrm{ev}_x(1_{x^*}\otimes f)
                              \widetilde{\mathrm{coev}}_x,
 \quad
 \operatorname{tr}^R_x(f)=\widetilde{\mathrm{ev}}_x(f\otimes1_{x^*})
                              \mathrm{coev}_x.
\]
The two agree because \(\mathcal C\) is spherical; their common value is \(t_x(f)\). These formulas use only structural maps belonging to the given state-sum category. No replacement by a different pivotal structure, Frobenius–Perron dimensions, or absolute values is made.

Below, associators and unitors in a displayed composite are suppressed by monoidal coherence. This is a notation convention, not an assumption that the supplied associator is trivial.

## 3. Cyclicity and nondegeneracy on the entire category

Write \(I_{\mathcal C}\) for simple representatives and \(d_s=\operatorname{tr}_{\mathcal C}(1_s)\). First, \(d_s\ne0\) for each simple \(s\). Indeed, rigidity gives
\(\dim\operatorname{Hom}(1,s^*\otimes s)=\dim\operatorname{End}(s)=1\), so \(1\) occurs with multiplicity one in \(s^*\otimes s\). Both \(\widetilde{\mathrm{coev}}_s\) and \(\mathrm{ev}_s\) are nonzero, by the respective duality identities. In a semisimple category, nonzero maps into and out of a multiplicity-one simple summand have nonzero composite. Their composite is \(d_s\).

For a decomposition \(m\cong\bigoplus_s s\otimes V_s\), where \(V_s\) is an ordinary finite-dimensional multiplicity space, the categorical trace is
\[
 t_m(f)=\sum_{s\in I_{\mathcal C}} d_s\,\operatorname{Tr}(f_s).
 \tag{1}
\]
Here \(f_s\in\operatorname{End}(V_s)\); the formula follows by the direct-sum compatibility of categorical trace. It is independent of the chosen decomposition by cyclicity of pivotal trace, equivalently by ordinary trace invariance under change of multiplicity-space basis.

If \(f:m\to n\) and \(g:n\to m\), their blocks are rectangular matrices. Formula (1) and \(\operatorname{Tr}(g_sf_s)=\operatorname{Tr}(f_sg_s)\) give
\[
 t_m(gf)=t_n(fg).
\]
The pairing
\[
 \operatorname{Hom}(m,n)\times\operatorname{Hom}(n,m)\longrightarrow\mathbb C,
 \qquad(f,g)\longmapsto t_m(gf)
\]
is a direct sum of nonzero scalar multiples \(d_s\) of the ordinary rectangular-matrix trace pairings. Each is nondegenerate: a nonzero matrix entry can be paired with the opposite matrix unit. Hence the entire pairing is nondegenerate, for arbitrary finite direct sums, not merely simple objects. Zero morphism spaces cause no exception.

This proves the Calabi–Yau requirement in CM Definition 5.2. Importantly, the dimension of a nonsimple object can be zero when simple dimensions have different signs; this does not contradict nondegeneracy of its endomorphism pairing. No positivity assumption has entered.

## 4. Both partial-trace axioms

### Left action

For \(F\in\operatorname{End}(\iota(d)\otimes m)\), define
\[
 \operatorname{ptr}^{L}_{\iota(d)}(F)=
 (\mathrm{ev}_{\iota(d)}\otimes1_m)
 (1_{\iota(d)^*}\otimes F)
 (\widetilde{\mathrm{coev}}_{\iota(d)}\otimes1_m).
 \tag{2}
\]
This is the left-module partial trace computed from the pivotal structure of \(\mathcal D\): all of its duality maps are the restrictions of those in \(\mathcal C\). The tensor-product duality identities give the nesting identity
\[
 \operatorname{tr}^{L}_{\iota(d)\otimes m}(F)
 =\operatorname{tr}^{L}_{m}
       \bigl(\operatorname{ptr}^{L}_{\iota(d)}(F)\bigr).
 \tag{3}
\]
For clarity, use \((\iota(d)\otimes m)^*=m^*\otimes\iota(d)^*\), expand the evaluation as the evaluation of \(\iota(d)\) followed by that of \(m\), and expand the right coevaluation in the reverse nesting order. The resulting composite is exactly the right side of (3), including the coherence isomorphisms. Therefore
\[
 t_{d\triangleright m}(F)
   =t_m\bigl(\operatorname{ptr}^{L}_{d}(F)\bigr).
 \tag{L}
\]

### Right action

For \(G\in\operatorname{End}(m\otimes c)\), define
\[
 \operatorname{ptr}^{R}_{c}(G)=
 (1_m\otimes\widetilde{\mathrm{ev}}_c)
 (G\otimes1_{c^*})
 (1_m\otimes\mathrm{coev}_c).
 \tag{4}
\]
Expansion of the **right** categorical trace on \(m\otimes c\) gives
\[
 \operatorname{tr}^{R}_{m\otimes c}(G)
  =\operatorname{tr}^{R}_m\bigl(\operatorname{ptr}^{R}_c(G)\bigr).
 \tag{5}
\]
Since the chosen \(t\) is also the right trace, it follows that
\[
 t_{m\triangleleft c}(G)
  =t_m\bigl(\operatorname{ptr}^{R}_{c}(G)\bigr).
 \tag{R}
\]
The distinction between (3) and (5) is important. A pivotal category supplies a regular left-module trace and a regular right-module trace separately; sphericity identifies them. It is the reason a single inherited trace meets both axioms here.

### Simultaneous and mixed compatibility

Regard the bimodule as a left module over \(\mathcal D\boxtimes\mathcal C^{\mathrm{rev}}\), where the reverse tensor category carries the induced pivotal structure. For
\(H\in\operatorname{End}(\iota(d)\otimes m\otimes c)\), (L) followed by (R) yields
\[
 t_{\iota(d)\otimes m\otimes c}(H)
 =t_m\!\left(\operatorname{ptr}^{R}_c
                   \operatorname{ptr}^{L}_{\iota(d)}(H)\right).
 \tag{6}
\]
The two partial closures involve disjoint outer tensor factors. The interchange law and bimodule associator identify the result with the opposite closure order. It is exactly the partial trace for \(d\boxtimes c\): left closure in the reversed tensor factor is right closure in \(\mathcal C\). Finite sums of external simple objects exhaust the semisimple Deligne product; additivity and linearity extend (6) to every object and endomorphism required by the product-category module-trace axiom.

In particular the action functor preserves the product Calabi–Yau trace: on decomposable morphisms its trace is \(\operatorname{tr}_{\mathcal D}(a)t_m(b)\operatorname{tr}_{\mathcal C}(e)\), and linearity gives the general case. Thus neither merely checking dimensions nor merely checking one-sided trace compatibility is being substituted for CM Definition 5.16.

The trace is normalized by \(t_1(1_1)=1\). Among right-regular module traces this fixes it uniquely: applying (R) to \(m=1\) forces any such trace to be \(t_1(1_1)\operatorname{tr}^R\). No arbitrary scale of a module trace is silently chosen.

## 5. Dimensions, orientation and dependence on the inclusion

Set
\[
 \Delta_{\mathcal A}=\operatorname{Dim}(\mathcal A)
  =\sum_{s\in I_{\mathcal A}}d_s^2,\qquad \mathcal A\in\{\mathcal D,\mathcal C\}.
\]
For \(d\in\mathcal D\), \(\dim_{\mathcal D}(d)=\dim_{\mathcal C}(\iota(d))\). Also
\[
 \dim_t(m)=d_m,\quad
 \dim_t(d\triangleright m\triangleleft c)=d_d\,d_m\,d_c,
 \quad
 \sum_{s\in I_{\mathcal M}}\dim_t(s)^2=\Delta_{\mathcal C}.
\]
The last expression is the trace-defined global dimension of the underlying module category. It is **not** an asserted formula for a quantum dimension of an interface 1-morphism, an index, or a multiplier relating all partition functions. The two bulk global dimensions remain distinct. They are nonzero over \(\mathbb C\), as required by the spherical-fusion construction; CM Remark 5.19 explicitly records this characteristic-zero fact.

CM's convention in the paragraph before Definition 5.16, published p. 52, calls a \(\mathcal D\)-\(\mathcal C\) bimodule a 1-morphism \(\mathcal D\to\mathcal C\). We use this categorical arrow convention. Geometrically the \(\mathcal D\)-region is the left-action side and the \(\mathcal C\)-region the right-action side, with orientations assigned by CM's adjacency rules. If one instead draws a positive normal according to Meusburger §4.1, the left-action category is at the **tip**, so for the same named action sides that normal points from \(\mathcal C\) to \(\mathcal D\). A categorical arrow should not be silently equated with that normal.

For an explicit reverse-direction admissible label, take the opposite traced bimodule \(\mathcal M^\#\), a \((\mathcal C,\mathcal D)\)-bimodule on \(\mathcal C^{\mathrm{op}}\). Explicitly,
\[
 c\triangleright m^{\mathrm{op}}\triangleleft d
   =\bigl(\iota(d)^*\otimes m\otimes c^*\bigr)^{\mathrm{op}},
 \qquad
 t^\#_{m^{\mathrm{op}}}(f^{\mathrm{op}})=t_m(f).
\]
The covariant duality functor \(m^{\mathrm{op}}\mapsto m^*\) identifies this with \({}_{\mathcal C}\mathcal C_{\mathcal D}\): reversing tensor order and then using the pivotal isomorphism gives \(c\otimes m^*\otimes\iota(d)\). Spherical trace is invariant under dualization, so this equivalence preserves the specified trace. The actual surface-orientation reversal, evaluation, coevaluation and coherence maps used by the defect functor are those of CM Proposition 4.13 and Theorem 5.18 in the Euler-completed orbifold category. The explicit traced opposite above verifies the admissible reverse-action algebraic input; equality of all Euler-adjusted duality structure maps with Meusburger's presentation is not asserted or needed. No identification of the complete CM and Meusburger state-sum models is made.

The wall is tied to \(\iota\), rather than merely to the existence of the two bulk categories. Its left action functor is
\[
 \mathcal D\longrightarrow\operatorname{Fun}_{\mathcal C}
  (\mathcal C,\mathcal C),\qquad d\longmapsto \iota(d)\otimes-.
\]
Evaluation at \(1\) identifies right-regular module endofunctors with \(\mathcal C\) and recovers \(\iota\), including its tensor constraints. This is a dependence statement, not a claim that inequivalent specified inclusions always yield distinct unpointed bimodule-equivalence classes. When \(\mathcal D=\mathcal C\) and \(\iota\) is the identity, the construction is the regular identity wall.

## 6. Exact published theorem application

The applicable paper is N. Carqueville and L. Müller, *Orbifold Completion of 3-Categories*, Communications in Mathematical Physics 407, article 8 (2026), published online 6 December 2025, [DOI](https://doi.org/10.1007/s00220-025-05434-y).

1. The ground field meets their algebraically closed, characteristic-zero assumption. Both chosen bulk categories are spherical fusion categories.
2. Sections 1–4 above verify a finite semisimple bimodule and a Calabi–Yau trace satisfying **both** action partial-trace conditions of Definition 5.16. Proposition 5.17 therefore makes it an admissible orbifold 1-morphism.
3. Theorem 5.18 places these objects and traced bimodules, together with compatible bimodule functors and transformations, inside the orbifold completion used by the construction. We do not need a separate guess about the existence of a trace on an arbitrary module category.
4. Section 5.1.3 uses an Euler-completed trivial defect theory and, for a bulk \(\mathcal A\), the chosen scalar \(\phi_{\mathcal A}=\Delta_{\mathcal A}^{-1/2}\). A nonzero square root exists over \(\mathbb C\). Choose the required presentation data independently for \(\mathcal D\) and \(\mathcal C\); a common ambient normalization is not substituted for the subcategory normalization.
5. Apply Theorem 6.4 to that Euler-completed defect theory. Its output is a symmetric monoidal functor on the specified category of oriented, conically stratified labelled 3-bordisms with stratified closed 2-manifolds as objects. Example 6.5 identifies the single-bulk restrictions with TVBW via the previously proved orbifold/TV comparison. The formulation is a \((3,2)\)-bordism defect TQFT, not a claim of a separately proved fully extended SO(3)-fixed-point structure.

Use the resulting universal labelled theory, or restrict it to the admissible bordisms involving these bulks, this wall, its reversed wall, and the compatible identities, composites and junction labels needed for the chosen bordisms. There is no need to posit a closed set of junction data consisting solely of one surface label.

## 7. State spaces, sewing and normalization

For a stratified closed surface \(\Sigma\), CM §6.2 takes the colimit of the triangulation-dependent pre-state spaces under the triangulated-cylinder maps. Equivalently, after fixing a triangulation, it takes the image of the cylinder idempotent. A compatible labelled 3-bordism defines a map between these images/colimits. Theorem 6.4 asserts that these maps respect identity cylinders, oriented diffeomorphisms, sewing along matched labelled boundary surfaces, and disjoint unions. Thus this construction supplies state spaces and bordism maps with an interface, not only closed-manifold numbers.

For an unstratified surface or bordism in the \(\mathcal A\)-phase, the bulk comparison is a monoidal natural isomorphism with normalized TVBW. It is not an equality of all unprojected vector spaces or of raw triangulation matrices. More explicitly, Carqueville–Runkel–Schaumann, *Orbifolds of Reshetikhin–Turaev TQFTs*, Theorem 4.5 and equation (4.70), construct the bulk comparison. For a boundary surface with graph \((\Sigma,\Gamma)\) and edge coloring \(c\), its diagonal multiplier is
\[
 f_{\mathcal A}(\Sigma,\Gamma;c)
   =\Delta_{\mathcal A}^{|\Sigma\setminus\Gamma|/2}
      \prod_{e\in\Gamma_1}d_{c(e)}^{-1/2}.
 \tag{7}
\]
Here \(|\Sigma\setminus\Gamma|\) counts complementary regions, and the nonzero square roots are the compatible choices in the orbifold presentation. On the direct sum over colorings this is a diagonal operator, **not** a coloring-independent scalar. With \(F_{\mathrm{in}}\) and \(F_{\mathrm{out}}\) the two such boundary operators, the raw comparison reads
\[
 Z_{\mathrm{orb}}(Y^t)
   =F_{\mathrm{out}}^{-1}\,p_{\mathrm{TV}}(Y^t)\,F_{\mathrm{in}}.
 \tag{8}
\]
In particular it conjugates the cylinder projectors. It induces \(J_{\mathcal A,\Sigma}\) on their images, with
\[
 J_{\mathcal A,\Sigma'}\,Z_{\mathrm{orb}}(Y)
  =\operatorname{TVBW}_{\mathcal A}(Y)\,J_{\mathcal A,\Sigma}.
\]
Disjoint unions factor both the complementary-region count and the edge product, so these identifications are monoidal as in the theorem. Apply this construction separately in each single-bulk restriction; a formula for arbitrary mixed-phase raw boundary normalizations is not being inferred from (7).

For closed triangulated manifolds, the normalization of the \(\mathcal A\)-bulk is
\[
 \Delta_{\mathcal A}^{-v}
 \sum_{\text{edge labels}}\left(\prod_e d_{\lambda(e)}\right)
 \sum_{\text{face labels}}\prod_\sigma W_{\mathcal A}(\sigma).
\]
It matches source equation (48) when its \(\mu_i\) are the inherited categorical dimensions and its normalized \(6j\)-weights are the corresponding categorical ones. In particular \(\operatorname{TVBW}_{\mathcal A}(S^3)=\Delta_{\mathcal A}^{-1}\), in the convention of Turaev–Virelizier, the examples following Theorem 6.1 (p. 16). The \(\mathcal D\)-sum uses \(\Delta_{\mathcal D}\), while the \(\mathcal C\)-sum uses \(\Delta_{\mathcal C}\). This does not give a universal quotient formula for general manifolds.

Selecting a decorated cylinder with a wall can produce a linear map between its specified boundary state spaces. The existence of those decorated maps does not by itself prove naturality with respect to every *undecorated* cobordism, and is not used to claim an ordinary TQFT natural transformation.

No independence of every presentation or square-root choice in the entire defect extension is claimed here. The existence statement and the bulk TVBW isomorphisms suffice for the interface relation. Meusburger's fixed-boundary invariance theorem is not used to promote a state sum to this full functor. CM Example 6.5 explicitly reserves detailed comparison with Meusburger's particular defects for further work.

## 8. Source-model coverage, kept separate from trace existence

The result applies to **every** full fusion-subcategory inclusion with inherited spherical structure over \(\mathbb C\); it is not restricted to pseudo-unitary categories, modular categories, or categories arising from a particular subfactor.

For historical based state-sum data to fall in this formulation, the required bridge is:

- The simple labels and multiplicity spaces reconstruct a finite semisimple linear category and its tensor product; the given associativity/\(6j\) data, including unit normalization, provide the tensor coherence. Duality and the supplied dimension/pivotal data must give the spherical structure used in the state sum.
- The retained labels contain the unit and duals, and are closed under every simple summand occurring in products. Their multiplicity spaces, associator and duality maps are the actual restrictions, rather than another categorification with the same fusion ring.
- Under this identification, the historical tetrahedral weights and categorical state-sum weights agree in a stated basis/gauge, and the historical \(w\) is \(\Delta\) for each separate label system. The boundary formulation must use the corresponding cylinder-projector state spaces and the normalized comparison.

Once these items hold, the full subcategory is simply the additive, idempotent-complete subcategory generated by the retained simple labels, so no additional trace-existence condition remains. An arbitrary linear subalgebra of the complexified fusion algebra need not specify such retained labels or restricted associators. The qualitative historical introduction alone is not a proof that every conceivable polynomial solution called a set of \(6j\)-symbols satisfies every modern reconstruction axiom. That source-identification question must be resolved by the dedicated source-translation lane; it is not settled by an abstract module-trace calculation.

Likewise, an \(\alpha\)-induction example is covered after identifying the actual full, chiral, or ambichiral fusion-subcategory inclusion and its inherited spherical structure, with the algebra-object/subfactor hypotheses required for that identification. No braiding nondegeneracy enters the interface construction once this input exists, so a singular S-matrix creates no additional obstruction here. This statement does not assert that arbitrary algebra objects in arbitrary ribbon categories automatically produce the required inclusion.

## References and independently checked locations

- Carqueville–Müller, published version: p. 6 (ground field and theorem overview), pp. 47–48 (Definition 5.2, Example 5.5), p. 51 (Euler normalization), pp. 52–54 (Definition 5.16, Proposition 5.17, Theorem 5.18, Remark 5.19), pp. 58–63 (oriented bordisms, cylinder colimit, Theorem 6.4, Example 6.5). [Published primary source](https://doi.org/10.1007/s00220-025-05434-y).
- Carqueville–Runkel–Schaumann, *Orbifolds of Reshetikhin–Turaev TQFTs*, Theorem 4.5 and equation (4.70), inspected arXiv v2 p. 41, for the full bulk comparison and boundary multiplier. The published CM paper invokes this comparison; this lane inspected the CRS preprint, not an independently downloaded publisher PDF. [Primary preprint](https://arxiv.org/pdf/1809.01483v2).
- Meusburger, *State sum models with defects based on spherical fusion categories*, Definitions 1.13 and Examples 1.4, 1.6, 1.14–1.15; §4.1 for the explicit positive-normal convention. Used for compatible notation and the opposite bimodule, not for the full-functor inference. [Inspected v2](https://arxiv.org/pdf/2205.06874v2).
- Schaumann, *Traces on module categories over fusion categories*, Definition 3.7 and Remark 3.8 for module-trace conventions and the regular left trace. Proposition 5.8 is not needed for this particular bimodule. [Inspected v3](https://arxiv.org/pdf/1206.5716v3).
- Turaev–Virelizier, *On two approaches to 3-dimensional TQFTs*, the examples following Theorem 6.1 (p. 16) for the normalized sphere value and Theorems 11.1–11.2 for the separate TV/center comparisons, if desired. The latter alone are not the inclusion relation. [Inspected v5](https://arxiv.org/pdf/1006.3501v5).
- Ohtsuki, *Problems on invariants of knots and 3-manifolds*, Chapter 9, especially equation (48), printed p. 509, and Problem 9.4, printed p. 510. [Primary source](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf#page=137).

**Disposition:** the modern restricted-regular interface passes its algebraic and published-theorem hypotheses. Acceptance at the entire historical problem's scope additionally requires the source-translation and \(\alpha\)-induction identifications; this file does not certify novelty or present-day openness.
