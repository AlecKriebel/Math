# Fresh final adversarial review after the queue repair: PR384

**Verdict: PASS for the five scoped results at exact repaired head 1747a651d5865cfbbe3c4eef7ab3c8142fc117f4. Mandatory repairs: none. Original universal question: unsolved, 5/5 substantive author turns. This review does not certify novelty, an original-question solution, merge readiness, a sixth author search, a paper, release, or DOI.**

This is a fresh whole-package audit. The source-first reconstruction was written before reading any candidate proof or prior verdict. The initial materially distinct falsification mechanisms were sealed in PRECOMPARISON_SEAL.json. All five candidate proofs and eight executable sources were then read in full. The fresh control code and its complete 23,293-assertion output were sealed in FRESH_CONTROL_SEAL.json before initial-family, root, historical-review, or original-final-adversary comparison. Subsequent comparisons agree; earlier PASS statements are not proof premises.

## Exact primary question and success criteria

The primary source is Benson's complete contribution in [OWR14/2019](https://ems.press/journals/owr/articles/16776), printed pp.847–849, with the question on p.849. The publication date recorded by EMS is 27 February 2020, although the volume year is 2019. All three relevant pages were freshly rendered and visually inspected, including the conjugation bars on p.849.

For every finite group G and every coefficient field k of characteristic p, form the split Green ring whose additive basis is the complete set of isomorphism classes of finite-dimensional indecomposable kG-modules. Multiplication is diagonal tensor product over k. The functional-analytic scalar field is C. Its completion A has dimension-weighted l1 norm

    ||sum c_M[M]|| = sum |c_M| dim_k M,
    (sum c_M[M])* = sum conjugate(c_M)[M*].

The original target is Spec_A(x*x) contained in [0,infinity) for EVERY completed element x, equivalently every dimension-bounded unital species obeys s(M*)=conjugate(s(M)). Completed elements may be signed, complex, and infinitely supported; support is countable even if the whole basis is uncountable. Ordinary characters, positive module-growth statements, stable/projective quotients, maximal quotients, nil-radical results, and further C*-completions cannot substitute for this quantifier. An original-question solution would require a universal proof or an actual finite-group/module-field nonsymmetry certificate valid in the full completion. The package provides neither.

## Primary sources, versions, hashes and access qualifications

All six candidate source PDFs were fetched independently anew. Their byte counts and actual SHA256 hashes match SOURCE_MANIFEST.json and SOURCE_ADDITION_T3.json exactly; SOURCE_FETCH.json and LANGER_FETCH.json record the fresh retrieval. These are raw PDF hashes, not inferred from HTTP ETags. The downloaded PDFs, extracts and renders are ignored private source material.

[Benson arXiv:2008.13155v2](https://arxiv.org/abs/2008.13155v2), dated 30 April 2022, is the controlling accessible 120-page accepted manuscript. Definition1.1.1, Proposition2.9.10, Proposition3.4.2, the field/growth discussion on pp.67–69, and Question5.15.2 on p.111 were read and visually inspected. Chapter4 permits arbitrary k of characteristic p. The separately fetched author-hosted book has 123 pages and PDF creation metadata 11 June 2020; its question on p.113 was visually inspected. It must not be relabeled a newer edition.

The 2024 Memoirs publication is identified by the candidate as volume298, no.1488, DOI10.1090/memo/1488. A fresh official AMS endpoint returned403, and the full publisher PDF was not retrieved. This review does not certify identity of that edition with the accepted text or report its full text as inspected. [Langer arXiv:0803.0252v1](https://arxiv.org/abs/0803.0252v1), submitted 3 March 2008, was freshly obtained; p.5 was visually inspected for Proposition2.2 and its right-module/left-matrix convention.

The frozen [Kua–Lim v3](https://arxiv.org/abs/2603.11533v3), dated 24 August 2026, concerns the particular symmetric group on p letters and tensor decompositions modulo projectives; the frozen [He v2](https://arxiv.org/abs/2408.04196v2), dated 4 February 2025, concerns counts of indecomposable tensor-power summands and asymptotics. Their scope pages were freshly inspected. These narrower statements do not establish all-species symmetry. Current He arXiv metadata includes Ark.Mat.64(2026),91–120; this does not change the bound v2 PDF used here.

Two separately fetched primary Benson–Symonds author manuscripts corroborate the inherited endotrivial input. [bs1-final.pdf](https://personalpages.manchester.ac.uk/staff/peter.symonds/preprints/bs1-final.pdf) p.13 explicitly imposes p divides |G| in Theorem7.5; that hypothesis holds for every nontrivial subgroup/p-group use here. Its arbitrary-field introduction and Section7 give the Carlson core-dimension bound, elementary-abelian gamma detection, Dade classification, and gamma-one implication. The older [bs1.pdf](https://personalpages.manchester.ac.uk/staff/peter.symonds/preprints/bs1.pdf) p.12 has the earlier wording. Their fresh hashes are separately bound in BS1_FRESH_FETCH.json. The original Carlson1981 and Dade1978 proof texts were not independently reread. Their results remain explicitly credited inputs through accessible primary theorems, not newly proved classification claims. No exhaustive literature search, historical nonexistence proof, or novelty certificate is made. Newly rendered text/PNG bytes are not claimed to reproduce old historical renders.

## Independent mathematical verification

### Turn1: arbitrary algebraic extensions, countable closures and compactness

For finite K/k of degree d, extension E is multiplicative and commutes with duality, while restriction R need only be additive. Positive decompositions preserve dimensions, so ||Ex||<=||x|| and ||Ry||<=d||y|| for every complex finite combination. RE=d id then forces equality. This handles cancellations, repeated summands, nonsplitting fields and inseparability. It does not assert that a scalar-extended indecomposable stays indecomposable.

For infinite algebraic K/k, the finitely many decomposition matrices, summand idempotents and repeated-type isomorphisms for a fixed finite support descend to a single finite subextension. A descended summand cannot decompose there if it is indecomposable upstairs; distinct upstairs types cannot become isomorphic downstairs. The deliberately repeated types are already identified by the descended isomorphisms. Thus the exact norm occurs at that finite stage; density proves isometry of the full completions and closed range. Norm equality on every power gives equality of spectral radii for x and x*x. The commutative radius criterion transfers symmetry without claiming arbitrary spectral permanence or extension of every subalgebra character.

The fresh inseparable control shows why a different argument would be invalid: over F2(t), the division factor F2(t)[s]/(s²-t) becomes dual numbers after adjoining s. The new nonzero square-zero radical invalidates blanket radical-preservation assumptions, while RE=d id stays valid. The candidate uses the valid norm mechanism.

The one-module tensor/dual closure is countable and closed under product summands. Its closed coordinate span is a unital *-subalgebra with the inherited norm. Ambient symmetry descends by power norms; conversely ambient characters restricted to each such subalgebra respect duality on every basis vector if all these subalgebras are symmetric. Continuity handles the completion. A basis defect z=s(M), w=s(M*) gives a nonreal value on at least one of M+M* and i(M-M*), because their imaginary parts are Im(z)+Im(w) and Re(z)-Re(w).

The compact disk product with ALL unit/product equations and a FIXED positive rational defect gives exactly the stated finite-intersection criterion. Every solution is a contractive species by the weighted coordinate estimate. Feasible finite prefixes or defects that shrink toward zero do not certify a global non-Hermitian species. This route is blocked as a universal solution until a new exclusion mechanism or compatible actual construction is supplied. The nonstandard-star l1(Z) control is expressly outside the Green axioms.

### Turn2: all completed endotrivial directions and full p-group factors

The stable unit k is nonzero and indecomposable when p divides |G|. Tensoring with an invertible stable object is an equivalence and preserves indecomposability. Stable Krull–Schmidt plus removal of projective summands yields a unique actual nonprojective indecomposable core E_t. The exact coordinate norm identifies its stable closed span with l1(T,w), w(t)=dim E_t, with inverse symmetry and submultiplicativity of weights.

The credited gamma-one theorem supplies lim w(t^n)^(1/n)=1 for every t and its inverse. A bounded species has |chi(t)|^n<=w(t^n), giving |chi(t)|<=1; inverse powers give the reverse inequality. Conversely every unitary group homomorphism yields an absolutely convergent bounded multiplicative Fourier sum. Hence ALL characters are unitary and ALL completion elements obey the Hermitian criterion. Neither finite generation nor ambient character extension is assumed. Endotrivial twisting rotates the stable duality defect by a unit scalar and preserves its absolute value.

For a nontrivial p-group, kG is local, all finite projectives are free, and P=kG is the unique indecomposable projective. e=P/|G| is a self-adjoint norm-one idempotent, ea=dim(a)e, and A=Ce times (1-e)A. The stable quotient identifies with the second factor, whose unit is 1-e. For the canonical nonprojective representative x, Jx=x-D(x)e has the exact norm ||x||+|D(x)| between ||x|| and2||x||. Multiplicativity follows from the idempotent projection; D itself is not multiplicative in the stable ring. The full projective/endotrivial closed span is therefore symmetric. The equivalence of full and entire stable symmetry transfers the central difficulty and remains blocked as a universal resolution. The trivial/semisimple boundary has no nonzero stable unit and is handled separately.

### Turn3: actual Q8 signed ambient spectrum

Langer's maps match after a=I,b=J,K=IJ,K'=a³b. Their left multiplication defines right-module maps. Inverse-action conversion preserves the trivial module, tensor products, projectives and duality. Exact zero composites and ranks7,9,7,1, with nonzero F2 minors, prove the literal four-periodic complex exact in every characteristic-two field. Augmentation-zero entries make it minimal. The symmetric group algebra is self-injective, so a projective summand of a minimal kernel would split inside the cover's radical, contradicting Nakayama. The dimensions1,7,9,7,1 and norm-image trivial module give Omega^4=k and exclude stable periods1 and2. Schanuel and tensoring projective presentations give the stable tensor law and inverse duality.

For x=Omega+Omega³-2k-(3/2)P, the candidate's nonzero Fourier idempotents establish the ambient stable roots and polynomial inverse excludes all other values. The scalar-zero full lift produces full spectrum{0,-2,-4}. My fresh check independently works in the ACTUAL full five-coordinate multiplication, with dimensions1,7,9,7,8. It verifies x(x+2)(x+4)=0 and the following nonzero real polynomial spectral idempotents, in that ordered basis:

    q_0  =(1/4, 1/4, 1/4, 1/4,-5/8),
    q_-2 =(1/2,   0,-1/2,   0, 1/2),
    q_-4 =(1/4,-1/4, 1/4,-1/4, 1/8).

They satisfy q_lambda²=q_lambda, sum q_lambda=1, and (x-lambda)q_lambda=0. Nonzero actual Green coordinates force each lambda to persist in ANY containing unital algebra; a polynomial inverse excludes the complement. Thus the ambient result does not rely on a general extension-of-characters theorem.

The unique nontrivial elementary abelian subgroup is central C2. Both odd syzygies restrict as k+3kC2, P as4kC2, so x restricts zero; dimension zero handles the trivial subgroup. Radius4 versus restricted radius0 defeats a signed/complex restriction inequality. All its spectral values are real. It neither defeats symmetry nor contradicts the positive actual-module gamma-detection theorem.

### Turn4: complete abstract axioms and all-field nonrealizability

The P-twisted group-ring ideal and its unitization have associative positive integral multiplication; the identity basis permutation is a valid star. Nonunit products have zero unit coefficient, so the strengthened closed axiom holds. The cubic coefficient is 2c+m plus c² when g²=1, at least2. All nonunit dimensions d=c+m are positive and multiplicative. The positive rho=sum x_g obeys x rho=dim(x)rho, verifying the crucial regular axiom rather than just positivity.

Fourier eigenvalues of P are d and c=q-1, nonzero for q>=2, hence the entire complex algebra is C^(m+1) and radical zero. Its complete characters are bounded in the exact dimension norm. A character nonreal on an element of order>2 evaluates a self-adjoint basis vector nonreally. Square values can be nonreal or negative, including the order-four boundary. Positive elements are self-adjoint, so their square-radius identities hold in every specified quotient by spectral mapping, without symmetry. The example is a valid axioms-only obstruction.

Based, dimension- and duality-preserving realization as the COMPLETE finite-group split Green ring is separately excluded over every field. If k is projective, Maschke makes the invariant identity in M tensor M* a trivial direct summand, contradicting zero unit coefficients. Otherwise the indecomposable projective cover of k has dimension d. Its first syzygy has dimension d-1 and is indecomposable through stable autoequivalence and End_st(k)=k; self-injectivity/Nakayama excludes projective summands. Since d>=4, d-1 is neither1 nor d and is missing from the complete proposed basis. This is not a nonrealizability claim about unbased complex algebras or a finite-group nonsymmetry counterexample. An axioms-only route is blocked without new actual representation constraints.

### Turn5: actual induction, then bounded completed blocks

For E=H times K, induction gives M_t tensor kK and End_E identifies with End_H(M_t) tensor(kK)^op. The first factor is local by Fitting. Its radical tensor ideal and the augmentation tensor ideal are nilpotent and commute as ideal products. Their sum is nilpotent and the quotient is the division algebra End_H(M_t)/rad. Thus the special tensor algebra is local over arbitrary k. This does not use a false rule that every tensor product of local algebras is local.

Ordinary order-p restrictions recover H: those inside H contain copies of a nonprojective endotrivial restriction, whose dimension is prime to p; those outside H are free by Mackey and trivial intersection. Copies cannot make a nonprojective summand projective. These lines generate H and prove nonprojectivity of the induced module. Restriction back to a fixed H gives [E:H] copies, and Krull–Schmidt recovers t. Hence all modules are distinct actual indecomposable coordinates BEFORE formal symbols, normalized multiplication, or l1 independence.

Fresh concrete controls use induced cyclic cores of dimensions1,2,4 at p=2,3,5 with actual commuting action matrices. Nilpotent Jordan-power ranks distinguish the inducing line from every other line. Exact centralizer equations and exhaustive centralizer idempotent enumeration for p=2,3 yield precisely0 and1. Actual diagonal coset G-set tensor orbits for ALL subgroup pairs of C_p² at p=2,3,5 independently establish the induction multiplicity and intersection stabilizer. This is stronger than assuming a formal semilattice table, but remains finite control rather than a general classification theorem.

The index identity [E:HK][E:H intersect K]=[E:H][E:K] gives normalized stable coefficient1. Trivial intersection is projective zero. The actual independent e_H coordinates admit a finite invertible zeta transform; Mobius p_H are nonzero orthogonal self-adjoint idempotents summing to the stable unit. The H-level of Phi_H(f) is exactly f, while lower levels are weighted restricted core values. Therefore

    ||f|| <= ||Phi_H f|| <= C_H ||f||,
    C_H = sum_(1!=L<=H) |mu(L,H)|.

Lower restriction collisions cannot cancel the unchanged H-level; restriction cannot increase core dimensions. Density extends these bounds to every weighted l1 element. Bounded below yields closed range. Projected generators all belong to that range and are dense in p_H B, giving onto. The finite product has bounded forward map (max C_H) and bounded inverse (sum C_H), with block units p_H. The product decomposition is a genuine Banach *-isomorphism. Credited growth makes every weighted endotrivial block symmetric. The full algebra adds Ce through J with the exact1-to2 distortion.

As an independent norm stress, the actual full permutation subring retains its projective q_0 rather than discarding it. For C_p² its Mobius idempotent norms in dimension-weighted coordinates are1 for q_0,2 for each line, and2p+2 for the full subgroup. Fresh code verifies both inverse directions on signed inputs and exact constants for p=2,3,5. This is an actual finite subring control, not an assertion that its one-dimensional blocks equal all endotrivial blocks.

The F8,C2³ two-dimensional witness is indecomposable because its centralizer F8[J] is local, nonprojective because2 is not divisible by8, and free on every ordinary cyclic subgroup because1,z,z² are F2-independent. Every induced-endotrivial coordinate has some nonfree cyclic restriction, so this missing coordinate lies outside the closed span, at weighted distance2. Shifted-cyclic projectivity detection is stronger than ordinary subgroup tests; a nonzero shifted operator acts as zero here. The witness proves properness, not a non-Hermitian species. Rank-one cyclic cases, nontrivial-subgroup premise, arbitrary fields, negative endotrivial classes, and potentially uncountable indexing are handled with the correct units and countable supports.

## Byte preservation, complete replays, and the queue repair

INTEGRITY.json verifies all52 repaired snapshot paths against exact Git blobs and their declared byte counts/SHA256 hashes. All51 target artifact files match the ORIGINAL head682f6fd29dce0c9ca5625d14461d0e6e1eb2e6d6 byte for byte. EXACT_DIFF_SET.json independently verifies the original52 snapshot/Git bindings too, and shows the repaired-versus-main-parent changed set is EXACTLY the51 target artifacts plus QUEUE at main264c26d539d616b0da6f8df76478a213d20939e4.

The actual repaired Git parents, in order, are

    682f6fd29dce0c9ca5625d14461d0e6e1eb2e6d6
    264c26d539d616b0da6f8df76478a213d20939e4.

The tree matches the repair receipt and the second parent was main at repair time and is an ancestor. Relative to that pinned main parent, the queue has exactly one changed physical line421, with only pipe-split cells8(status) and9(turn count) changed to unsolved and5/5. Every other main-parent queue byte and every other cell is preserved. During final sealing, concurrent root publication advanced workspace main to2e20baa9abde91b0d030e826d41a47babb0f2ee3. CURRENT_MAIN_QUEUE_REFRESH.json independently checks that this newer main has exactly the same queue as the repair parent, so all other current-main queue bytes remain preserved and only target cells8,9 differ. FINAL_STATE_BEFORE/AFTER record the concurrent HEAD/index change; it was not caused by any Git mutation in this audit. The current-main changed-file set can additionally include those root audit publications and is not falsely called52. QUEUE_ACTUAL_DIFF.patch is the actual Git diff. The merge integrates main changes, so “queue-only repair” means all candidate mathematics was preserved and only its target queue cells changed relative to current main; it does not mean the whole repository equals the stale original tree except QUEUE.

REPLAY_BINDINGS.json checks all213 nested candidate entries:117 historical checkpoint entries and96 author/review/publication entries. It directly compares42 author WIP files against59ecabf2953d6c0d39e51a341a554152927b7b6c and all six old review files against original head. All are preserved. Repeated historical bindings are intentionally counted as entries rather than unique files.

Only own ignored private copies were executed. Every turn program, author wrapper, historical reviewer program and publication wrapper ran successfully with zero stderr; all receipt-bearing complete stdout bytes equal their frozen receipts. Author checks total184,604 and old-review checks14,871. The five counts are23,589;61,260;746;47,981;51,028. This checks complete outputs, not only selected parsed values. Copy hashes were checked after execution too.

COMPARISON_BINDINGS.json independently verifies all80 sealed earlier-audit entries (44 initial-family/nested entries plus36 original-final entries). It records the reports read after the fresh seals. The original final59,132-control code was privately copied and its complete stdout freshly reproduced byte for byte. Its controls remain that earlier audit's work. My23,293 controls import no candidate or previous audit code. The materially distinct new mechanisms are actual coset orbit decomposition with full projective Mobius norms, explicit induction centralizer equations/idempotents, and full-Q8 real polynomial spectral idempotents. Initial-family control executions by root remain root executions and are not relabeled mine.

Earlier fresh read-only observation confirmed PR384 OPEN/DRAFT/CLEAN/MERGEABLE at the exact repaired head and source branch math/30004106-reviewed-green-ring. After the concurrent main advance, the saved refreshed observation reported OPEN/DRAFT with UNKNOWN mergeability during GitHub recomputation. PR384_READONLY_REMOTE_FINAL.json records the final bounded recheck; no readiness conclusion is inferred from either observation. They also confirm PR385 already MERGED at806de71764d5cb4724aa7b0797bc0456778cf155 on2026-10-03T02:40:41Z. These are observed remote states, not readiness certification or permission to merge. Root owns any subsequent integration decision.

## Strongest verified result, exact gap and mandatory repair list

The strongest positive result remains intrinsic symmetry of the actual projective/induced-endotrivial closed span for every nontrivial elementary abelian E over arbitrary characteristic-p k, with bounded completed Mobius blocks and an explicit actual module outside the family. The reductions, endotrivial theorem, Q8 signed restriction obstruction, and abstract axiomatic nonrealizability survive independent scrutiny.

The exact unresolved original gap is whether EVERY bounded species on all other actual indecomposable directions respects duality, or whether an actual finite group and module field produce a full-completion nonsymmetry certificate. Hermitian restriction to a proper subalgebra does not settle an ambient species. No additional universal-discovery completion is certified.

Mandatory repair list: empty. Preserve the source-access/version qualification, credited Carlson/Dade dependencies, finite-control scope, proper-family scope, original unsolved5/5 endpoint, and absence of novelty claims. These qualifications are already present in the candidate. Earlier historical CURRENT_STATE files remain historical; CURRENT_STATE_T5.json is authoritative.

Only repaired_final_adversary/ was written. No global or candidate queue write, Git index/branch/commit/push, service mutation, or outside-individual communication occurred. Raw source/private copies are ignored by this folder's .gitignore. Research log checkpoints give UTC times and completion estimates. Audit completion:100%; no claim of100% completion of the original mathematical discovery.
