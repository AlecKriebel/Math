# Independent PASS1 audit: restricted-regular interface

**Target:** Kawahigashi Problem 9.4, Ohtsuki (2002), printed p. 510 / PDF p. 138.  
**Date:** 14 October 2026 UTC.  
**Audit type:** independent adversarial verification of a proposed application of existing results.  
**Status:** PASS for the adopted interface relation on all complete finite spherical Barrett–Westbury inputs over C and their compatible based restrictions. Core construction, functor scope, normalization and the declared historical/α-induction model correspondences accepted. Supplementary center structure and exact example computations also pass independent review.

## 1. Exact mathematical statement accepted

Let `i: D → C` be a full fusion-subcategory inclusion over `C`, with the spherical pivotal structure on `D` inherited from `C`. Take the finite semisimple category `M_i=C`, with actions

`d ▷ x = i(d) ⊗ x`, and `x ◁ c = x ⊗ c`,

and with trace `t_x(f)=tr_C(f)`. This is a traced `(D,C)`-bimodule in the precise sense of Carqueville–Müller (CM), Definition 5.16. Consequently it labels an oriented topological surface defect in the `(3,2)`-dimensional defect TQFT constructed by CM, Theorem 6.4 and Example 6.5. Its two constant-bulk restrictions are the normalized TVBW theories of `D` and `C`.

This is a meaningful existing-result answer to the source’s qualitative question in the explicitly adopted spherical/based interface interpretation. It is an inclusion-dependent interface construction, not just a property independently shared by the two theories. It does not claim an equivalence or an ordinary monoidal natural transformation between their undecorated TQFT functors.

The main categorical statement holds for all spherical fusion categories over `C`, including nonunitary and non-pseudo-unitary examples. No braiding or invertibility of an S-matrix is used.

## 2. Trace-axiom verification

### 2.1 Finite semisimplicity and coherence

The underlying category is the already finite semisimple category `C`. Associativity and unit constraints for the restricted left action, regular right action, and mixed action are those of `C`, with the tensor constraints of `i` inserted if it is presented as a strong monoidal embedding rather than a strict inclusion. The module pentagons, triangles, and mixed coherence diagram reduce to the pentagon and triangle of `C` and the monoidal coherence of `i`.

Fullness is not needed merely to restrict an action, but it is needed for the stated input to represent the given fusion-rule based subsystem without adding or deleting intertwiner spaces. The retained simple labels must contain the unit and be closed under duals and all simple summands of their tensor products. The inherited associator is essential: a different categorification of the same fusion ring is a different input.

### 2.2 Calabi–Yau trace: cyclicity and nondegeneracy

For any decomposition `x ≅ ⊕_s s^{⊕n_s}` into simples of `C`, the spherical trace is

`t_x(f) = Σ_s d_s Tr(f_s)`, where `d_s=dim_C(s)`.

Every `d_s` is nonzero. Indeed, the tensor unit occurs with multiplicity one in `s*⊗s`. The evaluation and opposite coevaluation are nonzero maps to and from this unique summand; their composition is nonzero. This is also exactly Turaev–Virelizier (TV), Lemma 4.1(b), pp. 10–11. Thus the pairing on arbitrary Hom spaces is a direct sum of ordinary rectangular-matrix trace pairings multiplied by nonzero scalars. It is nondegenerate. The ordinary matrix identity `Tr(AB)=Tr(BA)` gives cyclicity, also supplied by pivotal trace cyclicity.

This verifies the whole of CM Definition 5.2, not just the dimension identity on simple objects. CM Example 5.5, p. 48, independently confirms that a spherical fusion category has this Calabi–Yau structure.

### 2.3 Both partial-trace identities

For `a∈D` and `f∈End_C(i(a)⊗x)`, closing the `a` strand first and then `x` gives

`t_{i(a)⊗x}(f) = t_x(ptr^L_a(f))`.

The duality, pivotal maps, evaluations and coevaluations of `a` are precisely their images from `D`, because the structure is inherited. This is the left identity in CM (5.13).

For `c∈C` and `g∈End_C(x⊗c)`, closing `c` first gives

`t_{x⊗c}(g) = t_x(ptr^R_c(g))`.

Sphericity identifies the closures needed on the two sides. This is the right identity in CM (5.13). These are identities for all endomorphisms, not just identities `dim(a▷x)=dim(a)dim(x)`.

The combined `D⊠C^rev`-module trace identity follows by applying the right and then left partial traces (or the other order, using coherence). There is no separate unverified bimodule-trace axiom left over. The regular bimodule already has this trace (Meusburger, Example 1.14, p. 10); restricting one action simply restricts the range of an identity that already holds.

### 2.4 Nonzero global dimensions and trace scale

Over `C`, a spherical fusion category has nonzero global dimension, as recorded in TV §4.2, p. 12, and CM Remark 5.19, p. 54. The same statement applies to the inherited spherical fusion category `D`. Thus a separate pseudo-unitary restriction is unnecessary.

The construction fixes the inherited trace `tr_C`, not an arbitrary nonzero rescaling. Rescaling a module trace may change associated defect normalizations. A claim of a specified interface must therefore retain this choice. The module dimension with this trace is `Σ_{s∈Irr(C)}d_s²=Dim(C)`; it must not be silently substituted for either bulk's dimension when normalizing that bulk.

### 2.5 Adversarial necessity check

The pivotal-compatibility hypothesis is genuine. Take the same underlying tensor category `Vec_(Z/2)` on both sides, but give `D` the spherical structure with dimension `-1` on the nontrivial invertible object and `C` its standard dimension `+1`. For the identity tensor embedding, a putative trace on the regular underlying bimodule would satisfy `t(g⊗x)=-t(x)` from the left action and `t(x⊗g)=t(x)` from the right action. These contradict nonzero simple traces. Thus the result must not be generalized to inclusions with unrelated spherical structures.

## 3. Exact scope of the TQFT theorem

CM's published version uses an algebraically closed characteristic-zero ground field, stated on pp. 6 and 45. The theorem applies in particular over `C`.

- Definition 5.16, pp. 52–53, is the trace definition verified above.
- Proposition 5.17, pp. 53–54, places a traced bimodule in the orbifold completion.
- Theorem 5.18, p. 54, includes spherical fusion categories, traced bimodules, bimodule functors and bimodule natural transformations.
- The construction on pp. 62–63 defines surface state spaces as colimits over triangulations, equivalently as cylinder-idempotent images. Bordisms induce maps between those state spaces.
- Theorem 6.4, p. 63, gives a symmetric monoidal defect TQFT `Bord^def_(3,2)(D_orb) → Vect`.
- Example 6.5, p. 63, identifies constant-bulk restrictions with TVBW TQFTs, using the earlier CRS3 comparison.

The exact bulk comparison dependency was also checked independently: Carqueville–Runkel–Schaumann (CRS3), complete arXiv v2, Theorem 4.5 and Equation (4.70), p. 41. For a colored boundary graph, let `F_A` be the invertible diagonal map with entries `Dim(A)^(|Σ\Γ|/2) Π_e d_{c(e)}^(-1/2)`. On pre-spaces, the type-correct relation is `Z_orb(Y)=F_out^(-1) p_TV(Y) F_in`. These maps intertwine cylinder projectors and induce a monoidal natural isomorphism on actual state spaces. The factor is coloring-dependent, not a single scalar. The Euler/global-dimension parameter and roots are chosen separately and consistently for each bulk. The complete published CM PDF was inspected; the auxiliary CRS3 comparison was verified in arXiv v2, not a newly retrieved publisher PDF.

Thus diffeomorphism invariance, gluing/sewing and disjoint-union behavior are supplied at the functor level. Meusburger's fixed-boundary triangulation invariance alone would not justify this conclusion; CM does. Conversely, this is a full `(3,2)` defect functor, not a claim that an oriented theory extended to points has been constructed. CM Remark 5.19 explicitly distinguishes the expected SO(3) homotopy-fixed-point issue.

CM's convention on p. 52 treats a `(D,C)`-bimodule as a 1-morphism `D→C`. A geometric normal-direction convention must be stated separately and consistently. It must not be imported from a different model without checking orientation conventions.

CM Example 6.5 explicitly leaves its detailed agreement with Meusburger's defects to future work. The present application does not need or establish that comparison.

## 4. Why the output really depends on the supplied inclusion

The left action is the monoidal functor `D→End_C(C_C)` sending `d` to `i(d)⊗−`. Under the regular right-module identification `End_C(C_C)≃C`, evaluation at the tensor unit recovers `i(d)`. Hence the construction uses the actual tensor inclusion and its inherited associativity data, rather than assigning an unrelated wall to any pair of categories.

This does not assert that inequivalent embeddings always yield inequivalent unpointed bimodules. Conjugacy and equivalence can identify interface data. Such injectivity or uniqueness is not required by the qualitative source question or by the adopted contract.

A wall placed in a product cylinder can furnish a map for that decorated cylinder. It does not follow that the resulting maps are an ordinary natural transformation against every undecorated cobordism: moving a wall across topology-changing bordisms is an additional statement. No such statement is used.

## 5. Normalization and independent finite-group checks

Ohtsuki's displayed Eq. (48), printed p. 509 / PDF p. 137, uses `w^{-v}`, where `w=Σ_i μ_i²`, edge weights `μ_i`, and the given tetrahedral weights. Restricting the allowed labels changes `w` to the global dimension of the restricted system. The bulk identified with `TV(D)` uses `Dim(D)`; the bulk identified with `TV(C)` uses `Dim(C)`.

TV §5.2, p. 14, and the examples following Theorem 6.1, p. 16, give the standard normalization `TV_C(S³)=1/Dim(C)`. The same theory assigns a one-dimensional state space to `S²` (TV §9.5, pp. 30–31).

For untwisted `Vec_G` and connected triangulated `M`, admissible edge colorings are flat G-connections. There are `|G|^{v-1}|Hom(π₁(M),G)|` such colorings: fix a spanning tree, use vertex gauge transformations to trivialize it, and retain the residual global gauge freedom. Multiplication by the `|G|^{-v}` normalization gives

`TV_(Vec_G)(M)=|Hom(π₁(M),G)|/|G|`.

Equivalently it is the groupoid cardinality `Σ_[ρ] 1/|C_G(imρ)|`. It is generally different from the unweighted number of conjugacy classes of representations. Ohtsuki p. 510 uses the latter phrase. The audit records this as a prose-versus-displayed-formula convention discrepancy; it is not used to reject the source's construction. The package must state the convention it follows and cannot identify the two quantities.

For the full subcategory `Vec_(C3)⊂Vec_(S3)`:

- `TV_(Vec_C3)(S³)=1/3` and `TV_(Vec_S3)(S³)=1/6`.
- Torus state-space dimensions are respectively `9` and `8`.
- For `S3`, the three conjugacy types have centralizers `S3`, `C2`, `C3`, with `3`, `2`, `3` irreducibles, summing to `8`.
- For `C3`, all three conjugacy classes have centralizer `C3`, giving `3+3+3=9`.

An independent direct enumeration of commuting pairs modulo simultaneous conjugation agrees: `C3` has 9 orbits, `S3` has 8. Therefore a universal injection of the subcategory torus state space into the ambient one is impossible. The two ordinary TQFTs are not isomorphic. Neither observation obstructs the accepted interface.

### Supplementary exact-validation audit

The completed validation report and all executable code were inspected. An exact snapshot of `verify_examples.py` (SHA-256 `6e087dd31e62b0d24672051e6a8265ec1e70d982729bd5b3153898784e48b0b3`) was replayed independently under normal Python, `-O`, and `-OO`. All three executions passed 17,857 explicit checks and produced the same output hash, `698e921b5b199738d7d6af5d1b98b73c81ee2830740e0cb86ccbe92f0a3b454f`. Deliberately false guards raised the expected exception in every mode.

The code constructs a rational gauge-average cylinder projector on commuting pairs, checks idempotency entry by entry, and obtains ranks 9/8 by exact elimination. This correctly distinguishes state-space dimension from the surface groupoid mass, which is 3 in both examples. It also exhaustively checks flat labels on a five-vertex sphere and its six-vertex 1–4 subdivision: C3 gives 81/243 labelings and normalized value 1/3 in both. Incorrect ambient normalization gives 1/96 then 1/192, hence is not invariant. Matrix-unit tests include off-diagonal endomorphisms, rectangular cyclicity, inherited sign-pivotal examples and incompatible pivots. The signed category's underlying tensor category remains pseudo-unitary; the example concerns a non-positive chosen spherical structure.

These finite tests are supplementary consistency evidence. They are not represented as a computational proof of CM's general functor or as an identification of a specific CM wall matrix with a finite-group pushforward.

## 6. Historical input and α-induction coverage: acceptance boundary

The source asks for a relation between theories made from a fusion rule algebra and a compatible based restriction of its 6j data. It does not ask for an arbitrary linear subalgebra, arbitrary fusion-ring categorification, or arbitrary unrelated pivotal structure. The relevant modern statement is for complete admissible TVBW/spherical data and inherited full subcategory data.

The historical introductory account names tetrahedral symmetry, unitarity and pentagon relations but does not print a complete list of rigid/pivotal/unit axioms. A reconstruction argument must therefore specify complete admissible data and explain why it is the source's state-sum model. It cannot prove that an arbitrary array satisfying only three loosely named equations automatically reconstructs a spherical fusion category. Conversely, this editorial incompleteness is not evidence of an actual uncaptured mathematical counterexample or a new open problem.

The historical source itself cites Barrett–Westbury [41]. Independent inspection of Barrett–Westbury v3, Definitions 2.1–2.13, confirms that the categorical state-sum input is finite semisimple spherical data; positivity and braiding are not imposed. The model lane’s skeleton construction preserves the specified multiplicity spaces, associator, unit, duality and pivotal data, and its based-closure proof gives the required inherited full subcategory. This closes the source-to-model obligation at the declared interpretation rather than substituting a unitary special case.

For α-induction, an algebra object is additional input; it is not itself a fusion-rule subalgebra. The genuine inclusion must be named. In BEK's setting the full, chiral, ambichiral and chosen subsystem tensor categories provide such inclusions, with their C*-spherical structures. The α-induction functor itself need not be fully faithful and must not be renamed an inclusion.

BEK Assumption 2.1 (p. 4) fixes a type III subfactor, a finite braided endomorphism system and a subsystem containing the dual canonical endomorphism. Theorems 3.9 (p. 15) and 4.6 (p. 19) allow degenerate braiding. Corollaries 3.10 (p. 16) and 4.8 (p. 21) have additional nondegeneracy assumptions. Neither “only modular cases had results” nor “BEK covers all abstract ribbon algebra-object data” is acceptable.

The nonunitary categorical α-induction context is also matched: in Kirillov–Ostrik, let B be finite semisimple ribbon with simple unit and let A be their connected commutative rigid algebra, with nondegenerate algebra pairing, `dim_B(A)≠0`, and trivial twist. Definitions 1.8/1.11, Theorems 1.5/1.10/1.15/1.17/1.18, Remark 1.19 and Theorem 3.3/Lemma 3.4 show that `Rep⁰(A)⊂Rep(A)` is a full spherical fusion inclusion, with dimension `dim_B(X)/dim_B(A)`. Finiteness follows because every module is a summand of a free module and there are finitely many original simples. These statements precede the additional modularity assumptions in §4. They were independently inspected. The forgetful functor to B and the free-module functor from B are not being relabelled as that full inclusion.

The interface theorem is S-matrix independent once the actual induced fusion categories and spherical inclusion have been established. That is an answer at the interface level, not a formula for the complete quantum double, a classification of singular-S input, or an extension of BEK's product decompositions without their hypotheses.

## 7. Supplementary relative-center audit

The center lane's explicit identification `E_i=Fun_(D|C)(C,C)≃Z_D(C)` was checked with composition tensor `F⊗G=F◦G`. Evaluation at the tensor unit identifies right-module functors with left tensoring; the remaining left-module constraint is exactly the relative half-braiding `x i(d)→i(d)x`. Its product and morphism equations have the stated types and order.

The two central lifts use `σ_a^(-1)` on the D side and the ambient half-braiding on the C side. Their mutual double braiding is the identity. Kong–Zheng Definition 2.6.1/Example 2.6.3, p. 13, and the first paragraph of the proof of Theorem 3.3.7, p. 23, confirm that the canonical functor `overline{Z(D)}⊠Z(C)→Z(E_i)` is a braided equivalence. The overline reverses braiding, not tensor order. The product orientation is `D^(rev⊗)⊠C` at the center level. The theorem's algebraically closed characteristic-zero, fusion and nonzero semisimple module hypotheses all hold. This is a braided tensor statement; compatibility with selected ribbon structures or numerical wall normalizations is not inferred from it.

Gelaki–Naidu–Nikshych, Remark 2.4, p. 5, applies to arbitrary fusion-subcategory inclusions, giving fusion of the relative center and its Frobenius–Perron dimension product. No grading assumption is imported from that paper's later theorems, and FP dimension is not substituted for spherical bulk normalization.

The report's direct fixed-bulk equivalence proof was also checked: any right-regular module equivalence is `L_u` with u tensor-invertible, and left linearity gives `u i(d)≅j(d)u`. Thus the untraced wall can forget inner conjugacy. Literal preservation of the chosen trace requires `dim(u)=1`; in the sign case `dim(u)=-1` it fails. This is not promoted to a classification in the Euler-completed defect theory. The balanced-product and reversed-endofunctor tensor formulas are coherent. The argument that invertibility of this distinguished bimodule forces i itself to be a tensor equivalence is valid. None of these results asserts Morita equivalence of the two bulk categories merely from their inclusion.

## 8. Source and novelty limits

The categorical trace argument is a direct restriction of the standard regular bimodule trace. The existence of the defect functor and its TVBW bulk restrictions is an application of published CM results, not a new theorem proved by this pass. Novelty of presenting this application to Problem 9.4 is not certified. Current openness of stronger questions is also not certified.

The completed trace/interface, source-to-model/α-induction, full-functor/normalization, relative-center and exact-example reports were independently checked and are accepted at their explicit scopes. No independent mathematical gap has been found in the adopted interface relation. This verdict does not cover arbitrary bare arrays, linear subalgebras without a compatible simple-label restriction, unrelated pivotal structures, unspecified algebra objects, or stronger undecorated-theory conclusions. These are boundaries of the input/output actually named, not newly manufactured residual conjectures.

## Primary references inspected

- Ohtsuki (ed.), *Problems on invariants of knots and 3-manifolds*, §§9.1–9.2 and Problem 9.4, printed pp. 506–510. https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf
- Carqueville–Müller, *Orbifold Completion of 3-Categories*, published CMP 407, article 8 (2026), pp. 6, 45, 47–48, 52–54, 62–63. https://doi.org/10.1007/s00220-025-05434-y
- Meusburger, *State sum models with defects based on spherical fusion categories*, v2, Definitions 1.13 and Examples 1.14–1.15, pp. 9–10. https://arxiv.org/pdf/2205.06874v2
- Turaev–Virelizier, *On two approaches to 3-dimensional TQFTs*, v5, §§4–6, §9.5, Theorems 11.1–11.2. https://arxiv.org/pdf/1006.3501v5
- Carqueville–Runkel–Schaumann, *Orbifolds of Reshetikhin–Turaev TQFTs*, complete arXiv v2, §4.3, Theorem 4.5 and Equation (4.70), pp. 40–41. https://arxiv.org/pdf/1809.01483v2
- Barrett–Westbury, *Invariants of Piecewise-Linear 3-Manifolds*, arXiv v3, Definitions 2.1–2.13, pp. 4–8. Primary PDF inspected via web text; no new local byte verification by this auditor. https://arxiv.org/pdf/hep-th/9311155v3
- Kirillov–Ostrik, *On a q-analog of the McKay correspondence and the ADE classification of sl(2) conformal field theories*, v3, §§1, 3 and modularity boundary in §4. https://arxiv.org/pdf/math/0101219v3
- Kong–Zheng, *The center functor is fully faithful*, arXiv v3, pp. 10, 13, 22–23; Definition 2.6.1, Example 2.6.3, Proposition 2.4.4, Theorem 3.3.7. https://arxiv.org/pdf/1507.00503v3
- Gelaki–Naidu–Nikshych, *Centers of graded fusion categories*, arXiv v1, pp. 3–5, Definition 2.1 and Remark 2.4. https://arxiv.org/pdf/0905.3117v1
- Böckenhauer–Evans–Kawahigashi, *Longo–Rehren subfactors arising from α-induction*, v1, Assumption 2.1, Theorems 3.9/4.6, Corollaries 3.10/4.8. https://arxiv.org/pdf/math/0002154v1

The diagram defining the partial traces in CM (5.13), published p. 53, CRS3 p. 41, and Kong–Zheng p. 13 were visually inspected in addition to text inspection. Source files remain outside this authored audit deliverable.
