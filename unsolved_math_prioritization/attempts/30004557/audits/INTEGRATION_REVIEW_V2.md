# Corrected constructive Morita release integration review

Problem 30004557, rank 452. Review date: 2026-10-03 UTC.

Reviewed release: `corrected_release_v2`, frozen author-manifest SHA-256 `353e9636e2f20b69dba8198f73e77abaffec8183c3550c73deda89798b627d77`.

## Verdict

**PASS for the narrow integration of the previously reviewed conditional-proof repairs. Original-scope HOLD remains unchanged.**

The corrected release faithfully incorporates the full proof audit and independent scaffold/graph supplement. Its exact conditional hypotheses remain attached. It does not introduce a claim that the source-intended constructive semantic Morita premise supplies those hypotheses. Its original-scope result is still unresolved after five substantive attempts, with no original counterexample and no global literature-status assertion.

This review approves integration of the corrected mathematical text. It does not authorize publication, a final PR, or any other remote write. The release's historical “integration review pending” fields correctly describe its state when frozen; this separate review is the subsequent verdict and does not require mutating the frozen manifest.

## Scope and checks

I read the complete corrected Attempts 3 and 5, the precise changes to Attempts 1, 2 and 4 and RESULT, DATA_CONVENTIONS, CHANGE_MAP, STATUS, README, REVIEW_REQUEST and the independent supplement. I compared their repairs to the previously completed all-five-attempt audit. This was a bounded integration review, not a new literature search or a sixth author attempt.

### Constructive data hypotheses

DATA_CONVENTIONS explicitly governs all five attempts. It preserves supplied syntax/proof sets, raw presentation and equality records, universal-property factorization operations, and structure-preservation comparisons with evidence. The pretopos-functor, nullary/empty-sort and set-indexed finite-stage conventions remain explicit. The text does not turn bare full faithfulness, essential surjectivity, or classical existence into an effective construction by assertion.

### Attempt 1 and Attempt 2

Attempt 1 now includes the missing short regularity link: a locally surjective matrix is identified with its kernel quotient using its converse relation, making it a kernel-pair coequalizer, with pullback stability. This matches the audit clarification and introduces no section.

Attempt 2 now states that stage-4 relations use stage-3 branch formulas and that stage-5 functions use expanded graphs rather than a predicate name introduced in the same stage. This faithfully preserves the uniform five-stage argument and eliminates the apparent same-stage dependency.

### Attempt 3

Both corrected hom-lift formulas are correctly typed. The F-lift cancels the automorphisms `a_B = F(epsilon_B) delta_(FB)^-1`; the symmetric G-lift does the same with `b_A = G(delta_A) epsilon_(GA)^-1`. Their identities use naturality and faithfulness, without imposing triangle identities on the input.

The K-lift conjugates by theta and applies the G-lift, with its source and target stated. The normalized comparison `nu_X: J K X -> X` is the K-lift of `id_(KX)`. Its inverse and naturality follow by K-faithfulness, and `K(nu_X)=id_(KX)`. The corrected text uses this normalized comparison to transport S-presentation diagrams, avoiding an unnoticed counit automorphism.

The internal language now has literal coherent axiom schemas linking every original multi-ary function or predicate to its designated C graph or subobject. Constants and nullary predicates use the terminal tuple object and empty conjunction. Mono names, equality records, structural diagrams and nonchosen-diagram comparison maps are included as actual axioms. This discharges the audit's syntactic-descent concern; external interpretation alone is no longer doing the work.

Fresh library carriers are explicitly distinguished from C-sorts. Branch maps are constructed by coordinates and formula equivalences, followed by the named presentation covers. The canonical-comparison lemma gives both totality directions, both functionality directions, inverses, and `b c=q`. It identifies an already present copy projection with that graph, rather than redefining an old symbol.

The same upper signature and axiom presentation includes both T and S libraries, both comparison families and both equations `p_X^T c_X^T=q_X^T` and `p_X^S c_X^S=q_X^S`. The symmetric endpoint arguments explain why the opposite-side definitions are derived theorems. Empty families retain branch-local witnesses and vacuous sequents. The added construction stages remain globally bounded.

### Attempt 4

The corrected universal-property argument explicitly uses raw-presentation/equality operations and supplied preservation evidence. Its call to Attempt 3 names the repaired graph schemas, hom-lifts and both scaffold equations. Its result is explicitly conditional on supplied pseudonatural equivalences in presented pretoposes. The text still explains why a premise quantified only over Grothendieck toposes, or only over Bishop-set models, does not license the generic evaluation used here.

### Attempt 5

The effective interface now expressly includes section-index smallness, assigned covers, local-surjectivity and finite-subcover operations, effective Yoneda hom-lifts, equality/factorization reflection, and uniform action on presentation records. Using the output of the supplied cover operation per object record does not invoke an additional choice principle.

Graph compactness is derived from the finite family into Y consisting of all `f e_i` together with all `d_j`. It covers because the second subfamily covers, and its cross kernel components are exactly the graph pullbacks. Thus the stated compact-kernel hypothesis suffices; the release does not assume that arbitrary subobjects are compact. Matrix totality, functionality, saturation, composition and empty-cover cases are included.

The release explicitly retains the interface and semantic comparison data as hypotheses. The plus/sheafification discussion remains a possible route with outstanding obligations, not an established constructive comparison theorem. The representative-section implication to excluded middle is unchanged.

## Integrity and accounting

- The release manifest matches the requested SHA-256 exactly. All 24 listed files match both their recorded hash and byte count.
- All seven entries in the initial author packet and all ten entries in the frozen five-attempt packet still match their historical manifests. Both historical manifest hashes remain unchanged.
- Both full audits, their JSON records and the independent supplement are byte-identical to their source review files. The two lineage manifests, source manifest, attempt log, verification program and frozen control output are also unchanged copies.
- CHANGES.patch is exactly the generated unified diff for the five attempts, RESULT and STATUS against the frozen five-attempt packet, including its full 51,879 bytes.
- The verified control program was rerun. Its output exactly matches the frozen 626-control result: 18 identities, 90 compositions, 466 associativity cases, 34 equalizer predicates and 18 image/kernel cases. These remain finite-set controls, not categorical or foundational proof.
- The original result and accounting remain `unsolved`, five substantive attempts out of five. The corrections are review integration, not a sixth attempt. No new source or semantic closure claim appears.

No release or historical file was edited by this review. No remote write, publication, external communication, or new search was performed. The remaining mathematical blocker is still the original semantic-to-presented-comparison implication identified in the full audit.
