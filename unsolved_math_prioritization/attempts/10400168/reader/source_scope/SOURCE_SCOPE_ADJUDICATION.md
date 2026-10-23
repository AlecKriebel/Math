# Source-scope adjudication: Kawahigashi Problem 9.4

**Target:** 10400168 / AMR-103-0168. **Review date:** 14 October 2026 UTC.

## Decision

**An explicit formulation of the proposed relation is required before a resolution can be accepted.** The source poses a qualitative structural question, not a uniquely specified assertion to prove or disprove. This does not make the question meaningless: it leaves several legitimate kinds of answer available.

The source scope is recovered sufficiently to proceed to an inclusion-specific literature application. In particular, a substantive existing defect-TQFT theorem was identified in Carqueville–Müller, beyond the initially supplied comparison literature. No mathematical proof attempt or proof audit was undertaken here. **Neither a complete resolution nor present-day openness is certified.**

## 1. Authenticated source and its limits

Kawahigashi's Problem 9.4 occurs in Ohtsuki's *Problems on invariants of knots and 3-manifolds*, printed p. 510, one-based PDF p. 138. It compares the state-sum TQFT of fusion data with the theory obtained from a fusion-rule subalgebra and the restricted 6j-symbols. No direction of map, equality, isomorphism, scalar formula, or required comparison level is stated. The main question imposes no braiding or modularity assumption. The following remark singles out α-induction from finite semisimple ribbon input with an additional algebraic object; it emphasizes singular S-matrices without replacing the general question by that case. [Primary source](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf#page=138).

The surrounding model uses finitely many labels, fusion multiplicity spaces, associativity/6j data, dimensions, and label-system-dependent normalization. Its historical presentation invokes tetrahedral symmetry, unitarity, and pentagon equations; it is not a complete modern categorical axiomatisation. The preceding isomorphic-TQFT question is Problem 9.3, not the present target. [Sections 9.1–9.2](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf#page=134).

## 2. Operational formulation recommended by this audit

The following is an **audit convention**, not an extra claim attributed to Kawahigashi.

Take admissible ambient state-sum data A, a specified compatible based subsystem B, and the restriction map identifying B's labels, multiplicity spaces and associativity data inside A. Both inputs must satisfy the hypotheses of the chosen construction. Name the resulting theories Z_A and Z_B and then state the proposed relation R(B ↪ A).

A useful modern branch is an inclusion D ↪ C of full fusion subcategories equipped with the inherited spherical structure, over a declared ground field. This is an operational translation to be justified for the class being treated. It must not silently replace the historical input by every abstract spherical category, or by only unitary categories, without explaining coverage. An arbitrary linear subalgebra of a complexified fusion algebra is not automatically an admissible restriction of simple labels and 6j-symbols.

The output should specify one of these levels:

1. **Numerical relation:** a formula for partition functions of a stated class of closed 3-manifolds, with both normalizations explicit.
2. **Interface or defect relation:** a construction tied to the specified inclusion, with the two undeformed bulk theories identified and its sewing interpretation stated.
3. **Ordinary TQFT map or equivalence:** maps on surfaces, their compatibility with cobordisms and disjoint unions, and the claimed direction and invertibility.
4. **Categorical/center relation:** the precise functor, correspondence or algebraic construction, followed by the theorem transporting it to the claimed TQFT level.

No ordering among these outputs is imposed by the question. A rigorous inclusion-dependent interface can be a meaningful answer without being a natural isomorphism of undecorated theories. Conversely, a property shared by unrelated theories does not explain the role of the supplied restriction. This last requirement is our relevance criterion, not a hidden assertion that the source demanded uniqueness or canonicity.

For any chosen branch, record closure under the tensor unit, duals and simple summands; inherited rather than replaced associators; dimension conventions; and the global-dimension normalization of each theory. Distinguish triangulation-level spaces from cylinder-projector images. A counterexample to an invented universal equality or injection would reject that formulation alone, not answer the entire qualitative question.

## 3. The α-induction context is neither modular-only nor arbitrary inclusion theory

### Böckenhauer–Evans–Kawahigashi, already cited as [62]

The paper's Assumption 2.1 fixes a type III subfactor and a finite braided endomorphism system, with a subsystem containing the dual canonical endomorphism. Its introduction explicitly permits degenerate braiding; Theorems 3.9 and 4.6 give intertwiner-space formulae in that setup. Corollaries 3.10 and 4.8 impose nondegeneracy to obtain product descriptions of quantum doubles of full and chiral induced systems. The chiral statement involves the ambichiral system. Accordingly, “degenerate cases had no results” and “this paper covers every fusion-subcategory inclusion” are both unjustified descriptions. These are established results, not new findings about the mathematics. [Complete inspected preprint, pp. 3–4, 15–16, 19, 21](https://arxiv.org/pdf/math/0002154v1).

### Kirillov–Ostrik, already cited as [222]

The algebra-object definition distinguishes an object with multiplication and unit in a braided category from a fusion-rule subalgebra. Module and local-module constructions require their own hypotheses. Therefore an argument about a Frobenius algebra, its subalgebras, or local modules must identify the actual fusion inclusion being compared. Shared terminology does not supply this identification. [Inspected definition, p. 4](https://arxiv.org/pdf/math/0101219v3).

### Sato's conditional degenerate comparison

In the inspected preprint, the degenerate center is assumed even (p. 5), and a nondegenerate extension is assumed minimal (p. 13). Proposition 4.2 and Theorem 4.3 additionally use an abelian finite group, producing a crossed-product/centralizer description of the double. Section 5 explicitly applies Theorem 4.3; Theorem 5.3 gives a surgery expression, and Remark 5.4 distinguishes the proved special case from a nonabelian claim attributed to Ocneanu. This is genuine relevant progress for special inclusions. It is not a theorem for arbitrary ambient fusion data or arbitrary singular ribbon input. [Complete inspected preprint, pp. 5, 13–17](https://arxiv.org/pdf/math/0404509v1); [published article record](https://doi.org/10.1007/s00220-005-1292-y).

### Alterfold flatness result

The inspected Theorem 4.7 concerns equivalence of flatness of an α-induced bi-invertible connection with commutativity of a Frobenius algebra, in the paper's categorical setup. This conclusion is different from a comparison of two TQFTs obtained by restricting fusion data. It must not be promoted to that comparison without an additional argument. [Inspected preprint, p. 29](https://arxiv.org/pdf/2412.12702v1).

## 4. What center and defect theorems actually supply

### Center comparison: powerful, but applied separately to each input

Turaev–Virelizier Theorems 11.1–11.2 identify TVBW with RT of the center, including an isomorphism of TQFTs, for a spherical fusion category over an algebraically closed field with nonzero categorical dimension. This is more than equality of closed-manifold invariants. It supplies two individual identifications when applied to C and D; the inclusion-dependent link between them remains to be specified. The bare equations TV(C) ≅ RT(Z(C)) and TV(D) ≅ RT(Z(D)) are not that link. [Inspected statements, p. 34](https://arxiv.org/pdf/1006.3501v5).

### Meusburger: state-sum invariance is not itself the full defect functor

The model uses spherical fusion categories for regions and traced bimodule categories for defect surfaces. Theorem 5.16 and Corollary 5.18 establish triangulation independence with boundary labels fixed. Crucially, pp. 50–51 discuss passage to a defect TQFT as a plausible analogous construction, rather than state it as an accomplished theorem there. Example 1.14 supplies the regular bimodule trace precisely in the spherical case. Thus arbitrary-module trace existence is not the only possible route: restriction of a regular action is the natural candidate to examine for an inclusion. [Definitions and Example 1.14, pp. 9–10; construction p. 28; statements/discussion pp. 49–51](https://arxiv.org/pdf/2205.06874v2).

Schaumann Proposition 5.8 guarantees module traces for pseudo-unitary input with its canonical spherical structure. That is a useful general sufficient condition, but should not be imposed as a necessary condition on a particular restricted regular bimodule. [Inspected statement, p. 30](https://arxiv.org/pdf/1206.5716v3).

### Additional primary source: an actual defect-TQFT construction

Carqueville–Müller's *Orbifold Completion of 3-Categories* was published online on 6 December 2025, in CMP 407, article 8 (2026). Both the complete arXiv v3 and the complete published PDF were obtained. Theorem 5.18 includes spherical fusion categories and traced bimodule categories in the orbifold construction; Theorem 6.4 constructs a defect TQFT. Example 6.5 identifies its single-bulk restrictions with TVBW and explicitly supplies defects between these theories from traced bimodules. The ground field is algebraically closed of characteristic zero. Their detailed agreement with Meusburger's particular defects is explicitly left for later comparison. No such agreement should be silently assumed. [Published version, pp. 6, 52–54, 62–63](https://doi.org/10.1007/s00220-025-05434-y); [arXiv v3, pp. 5, 45–46, 52–53](https://arxiv.org/pdf/2307.06485v3).

## 5. Consequence for the next mathematical step

The preferred next step is an **existing-result application audit**, before searching for a new theorem:

- Declare a spherical modern model and a specified inclusion D ↪ C.
- Test the concrete candidate consisting of C with one regular action restricted along that inclusion and with its spherical trace. Verify the bimodule/trace axioms with the actual inherited pivotal data and fix the orientation convention.
- Apply the published defect construction with those verified inputs and identify both bulk restrictions and normalization choices.
- Explain exactly what inclusion-dependent relation results, and what is not being claimed about equivalence, natural transformations, or invertibility.
- Separately map the α-induced systems and any extra algebra-object hypotheses into that construction. Do not label this step “the singular-S case is solved” solely because a spherical defect formalism exists.

This list is a proposed acceptance test, not an executed proof. The existence of the published general theorem makes it inappropriate to manufacture a residual “open problem” merely by requiring an unjustified stronger conclusion. It also makes it inappropriate to declare the original question settled without the input and output identifications.

## 6. Bounded search, inspection level and bibliographic corrections

The supplementary search covered exact problem wording/number, fusion-subcategory TV comparisons, the named degenerate-double paper, and defect constructions directly suggested by the inspected sources. Nine discovery queries and targeted primary-page checks were used. Searching stopped after the new relevant defect theorem was inspected and the principal scope distinctions were established. This was not an exhaustive citation search and does not exclude differently worded or inaccessible resolutions.

One additional recent lead was screened only at abstract/metadata level: Faria Martins–Meusburger's 2026 geometric defect TQFT for untwisted Dijkgraaf–Witten theory. Its stated setting is narrower than arbitrary fusion data; no theorem-level inclusion comparison is certified from that screen. [Official arXiv record](https://arxiv.org/abs/2410.18049v2).

Two provenance details were independently corrected:

- Ohtsuki's bibliography entry [62] is on printed p. 546 / PDF p. 174, not PDF p. 175. Its printed volume 31 is a bibliographic error; the journal record gives PRIMS 37(1). [Publisher record](https://ems.press/journals/prims/articles/2605).
- The retained Sato v1 PDF with SHA-256 beginning ddd5aea4 displays **13 November 2018** on its title page, while its arXiv margin identifies v1 of 28 April 2004. The inspected file does not display 1 February 2008. These presentation dates must not be substituted for arXiv revision or journal publication dates.

All theorem claims above are statement-and-hypothesis inspections, not independent proof verification. The accompanying public metadata records exact files, hashes, sizes, versions and inspection locations. Copied source documents, extracted text, and renders are excluded from the public deliverable.

**Final disposition:** source scope adjudicated; formulation and inclusion-specific existing-result verification remain required. No current-open, novelty, or full-resolution claim.
