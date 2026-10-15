# Independent adversarial review of PR48: algebra and cocycle family

**Mathematical verdict: PASS for the stated partial results. Publication verdict: repair the prior-report provenance wording before accepting the partial. KP-4.85 remains unresolved.** There is no mandatory mathematical correction in this family's review. No paper, DOI, claimed solution or priority claim is justified by these results. This is extensive independent AI checking, not human peer review.

## Exact input and early independence

The audited head is `e2e5c8c3e5ad218f867fa753c465bb96b3687bda`. The GitHub base is `c6975ca76f9f667f1250ba403d0e6da2aafe14d0`, but the actual merge base is `60292bed09f59236aa192cb17aa138f7b4750e1a`. The entire 18-path diff is 80,679 bytes, SHA-256 `994b4bbd4993227d1100cbd9d7493de776c6619c9daa379dca7f4ef3b3a26698`. It contains 17 added scientific files and one queue-row change.

The original preparation manifest is SHA-256 `278e4fd39b5a13c7a181e3f7d494420c41ea4082fa8ab9add34229671a1be3b4`, 574 payload members plus its self-only manifest, 110 directories and 103 genuine command captures. All 574 bodies, complete modes and declared owned topology were independently read and verified. Independent reviewer sibling directories were excluded from preparer ownership; no work from them was read to establish this family's mechanism.

I first read PARTIAL.md, the two plain source records, and the mathematical helpers as text. I wrote `INDEPENDENT_DERIVATION.md` before reading the original review conclusions. Only after fixing the universal argument did I read the old reviews, metadata, source audit, receipts and accounting. The later fresh controls use SymPy free-group normal forms and new compact-action cocycle constructions; they are not copies of the author's permutation checker. `INITIAL_INDEPENDENCE.json` and the research log preserve that sequence. No other fresh family's verdict is adopted as evidence here.

The exact target is a closed orientable smooth four-manifold whose **full** `Diff^infinity_0` has unbounded **ordinary ambient** commutator length. Known surface subgroups, conservative groups, central covers, stable length and fragmentation are not substitute targets. The original ledger consists of two JSONL turn objects, numbered 1 and 2: 2/5 substantive turns. This review contributes zero new substantive research turns and zero budget-counted audit turns. The duplicate 30004403/OWR-17471-009 has the identical target and does not acquire another independent five-turn budget.

## 1. Compression survives the strongest word-order attack

Lemma 1 is correct for arbitrary noncommuting input commutators. With `s_i=c_(i+1)...c_m`, the necessary cancellation is `s_i s_(i-1)^(-1)=c_i^(-1)`, because `s_(i-1)=c_i s_i`. No input commutators are interchanged. Pairwise commutation is used only between distinct conjugate images of `H`.

The proof does not assume these images are an injectively embedded direct product. A universal direct-product word can be mapped to their commuting images; intersections cause no problem. For the identity, no commutators are needed. The one-factor endpoint works. Reversing the displacement commutator or substituting prefixes generally fails, as the genuine negative-control executions confirm.

`INDEPENDENT_DERIVATION.md` supplies the universal proof. New exact controls test 265 arbitrary-word cases, including identity factors, cancellations, noncommuting commutators and a 64-factor example. The restricted wreath model uses the infinite free group on three generators and integer shifts, independently checking inverses, associativity and the actual conjugation convention. These finite normal-form controls are supportive; the universal proof establishes the infinite-group claim.

## 2. The compact support and stabilization argument has the stated scope

The imported smooth perfectness input is appropriate for the explicitly defined compact-total-support isotopy group. Finitely many factor supports fit in `M x B_R`, because `M` is closed and there are finitely many factors. A compactly supported vector field can equal the prescribed translation on the entire finite corridor, so the first `m+1` translated disks really are disjoint. Its flow and the product displacement have compact total support. Only endpoint supports of the original factors need fit in the initial disk, not their entire original isotopy witnesses.

The sphere cutoff factorization is also valid. The second coordinate is fixed, the fiber inverses depend smoothly on the parameters, and `b a=f x id` uses the stated composition order. The explicit paths start at identity and their total supports remain in fixed compact subsets of the two disk charts. No one-parameter group assumption is made about `f_t`. Extending the four compactly supported commutator factors and their isotopies by identity gives factors in the full ambient identity component.

Thus `cl_Diff0(M x S2)(f x id)<=4` is an ambient bound for this particular included subgroup, including all its powers. It is not a uniform bound for arbitrary ambient elements. The singular rotation example in the submitted note is correct. An independent circle-coordinate construction on `S1 x S3` gives another point-dependent-time cutoff with a rank-three derivative on the four-manifold; it confirms why the cutoff cannot simply be applied to arbitrary isotopies.

The classical input is accurately credited: [BIP](https://arxiv.org/pdf/0710.1412) contains the displacement and portable-product results. This review imports established smooth perfectness and audits its application; it does not purport to reprove the full Mather-Thurston theorem by finite computation.

## 3. Homogeneous quasimorphisms and central descent

Homogeneity gives inversion and, after division by powers, conjugation invariance. A single commutator has absolute quasimorphism value at most its defect `D`; a product of `k>=1` commutators has bound `(2k-1)D`. The identity is separately treated. Applying the four-commutator bound to every power gives `|n q(f x id)|<=7D`, hence vanishing on the stabilized subgroup. No claim that all ambient quasimorphisms vanish follows.

An abstract retraction onto the embedded positive-genus surface group would map the four ambient commutators to four surface commutators, contradicting the established full-surface lower bound. No continuity assumption on the retraction is needed. The hypothesis uses every positive genus, including genus one; the genus-zero group is not asserted to have this obstruction. The exact relied surface theorem was checked in the freshly authenticated [BHW manuscript](https://www.math.lmu.de/~hensel/papers/dagger_arxiv.pdf).

For a central extension, a homogeneous quasimorphism descends exactly when it vanishes on the central kernel. Sufficiency uses commuting additivity, obtained from `(az)^n=a^n z^n` and division of the bounded error by `n`. Necessity follows by evaluating the quotient identity. Centrality is part of the theorem and is not dropped. This is a descent criterion for a specified quasimorphism, not a transfer principle for every unbounded length on a covering group.

## 4. The signed-pushforward term is exact and genuinely substantive

The cocycle identity gives the formula in equation (5), with `g_*mu-mu` and the `f` cocycle integrand. It requires finite integrability against both the original and pushed-forward measures, as well as the other displayed terms. The remaining pointwise quasimorphism error has integral bounded by `Dpsi` because the measure is a probability measure. There is no discarded Jacobian, reversed pushforward sign or incorrect choice of integrand.

The invariant-probability obstruction is correct for positive-dimensional closed connected manifolds: local shrinking and moving yield arbitrarily many disjoint images of a relatively compact coordinate ball; invariance forces zero mass; a finite ball cover contradicts mass one. Atomic and singular measures are covered. This excludes the particular invariant-probability implementation, not every possible averaging construction.

The exact remaining gap must be preserved: noninvariance does **not** imply unbounded defect for every cocycle. Uniformly bounded integrands can still give a bounded extra term. Conversely, the stated averaging axioms alone permit unbounded defect even on a closed four-manifold. The independently derived `COMPACT_COCYCLE_COUNTEREXAMPLE.md` uses a finite Borel height on `S1 x S3`, a Dirac measure, and an exact additive cocycle with zero target defect. For smooth circle rotations `f_n` and fixed `g`, its defect is `-n-16/(n+4)`, for every `n>=5`. All required integrals are finite, yet the defect is unbounded. It is a diagnostic of the axioms; the cocycle need not be smooth, and the resulting average is not a quasimorphism on the full group. The original note's cautious scope is correct.

## 5. Ordinary length, ambient scope and source correction

The inclusion inequality is `cl_G(h)<=cl_H(h)`. The fragmentation comparison is an upper bound and cannot supply the desired lower bound. The finite disconnected-component reduction is correct: identity-component maps cannot permute components, projection gives one inequality, and simultaneous padding with identity commutators gives the reverse maximum formula. Compactness supplies finitely many components. No infinite-product argument is hidden here.

The claimed known four-dimensional class is valid. The sum of the two-critical-point Morse functions on `S1` and `S3` has indices 0, 1, 3, 4. The standard connected-sum handle construction gives counts `(1,k,0,k,1)`. Applying the no-middle-handle theorem requires the actual decomposition; it is not inferred from homology vanishing. [Tsuboi's published paper](https://ems.press/content/serial-article-files/43279?nt=1) has the relevant theorem for dimension 4 and smooth regularity, while its general new theorem begins in dimension 6. The [OWR discussion](https://ems.press/content/serial-article-files/46844) already mentions the no-2-handle class. Correcting the overly broad K3 background remark credits old results and does not solve the existence question.

## 6. Literal reproducibility, final input and actual executions

The old reviewed note is genuinely available at commit `2c32c34e6ddfa52ce067805afd3e2157dc32a130`; it was retrieved by actual Git child 93218. It is 14,198 bytes, SHA-256 `0036b78ba3164a52c15a7a24ea73fe4438a3db3c9a206f2882070c23e91cd3b2`. The final note is 14,275 bytes, SHA-256 `196568d2029fd378dfa43919efbf49dcbd11244a2de8c525483f84484f00e5fa`. They differ by exactly the pending-to-completed review-status sentence. No mathematical line changed.

Actual private operator 94977 completed the following, without executing in the frozen original folder:

- Literal author checker: 6,570 assertions, byte-for-byte and recursive-type equality with the saved receipt on the genuine historical note.
- Identical submitted replay checker: 6,570 assertions, the same exact receipt on that note. This is a duplicate, **not independent evidence**.
- Author checker on the final note: 6,570 assertions pass. Its receipt differs only in `partial_sha256`, which correctly binds the final note. It is not byte-identical to the old receipt.
- Historical independent checker: 228 assertions, byte-for-byte and recursive-type equality with the saved independent receipt, using existing SymPy 1.14.0.

There were 36 additional actual read-only Git children in this operator: full scientific bodies and tree/blob/mode bindings, the full diff, and the actual merge-base calculation. The 17 added scientific hunks reconstruct the original files byte-exactly. The single queue hunk changes this target from queued 0/5 to unsolved 2/5 and has no other target change. The original source bodies and accounting are preserved literally.

New actual child 99713 passed 2,004 additional exact assertions. The new control source and all actual streams are preserved. Actual mutation children launched by operator 620 each exited 1 at `two_commutator_identity`, proving the reversed-commutator and prefix mutations are rejected. These are intended negative controls, not failures of original mathematics. Original successful and failed preparation captures were retained, including the missing-head and initial-selection failures. Actual child 1687 checked all 103 original captures' complete streams, genuine prelaunch/operator source hashes, PID/UTC/argv/cwd and outcome consistency, along with completed own captures. Its outer completed capture was created only after that child exited.

Every private Python launch used `/usr/bin/python3 -B`, assertion optimization was disabled, and no package was installed. Full split stdout/stderr, source copied before launch, actual PID, aware UTC, cwd, argv and exit code are available in the family's captures. Earlier read-only inventory lookup at a nonexistent generic `MANIFEST.json` produced a tool-only FileNotFoundError before this family's capture driver existed; it wrote no artifact and was corrected to the actual original-manifest name. It is not retrospectively represented as a captured child.

## 7. Required provenance repair and publication qualifications

**S1, mandatory provenance correction, original SOURCE_AUDIT.md line 7:** the assertion that the research-results entry is null is false for the pinned source. Actual independent raw/SQL child 96768 read 149,266,659 raw bytes and all 15,458 SQLite rows in place, checking complete recursive type identity. For both exact problem codes, the upstream research-results key is **ABSENT**. SQLite contains literal `{}` as the fallback; the original 17-file package has no prior_report file. Each source_record is a plain problem object with an integer ID, not a queue-show wrapper. A missing key, a present null, a present empty object and the wrapper fallback are distinct facts.

Repair the operative source audit and any summaries/cards using that assertion. Preserve the original source audit, records and receipts as dated archive; do not manufacture a null prior artifact or modify the raw cache. A suitable statement is that the upstream key is absent and the local SQLite/show fallback is an empty object. The actual typed source audit in this family and the original preparation bind the full distinctions.

Two further presentation qualifications are required when constructing a current acceptance package, and can be satisfied by explicit archival labeling rather than altering historical evidence:

- Original SOURCE_AUDIT.md line 48 still says review pending, whereas final README, log, readiness and review record the completed September 30 review. Treat that sentence as pre-review authorship history or update the operative version. It cannot serve as current review status.
- The literal saved author receipts bind the historical mathematical note, not the final note. Keep those receipts unchanged and label the hash coverage correctly; supply the separate final-input replay or its exact qualification. The historical model/effort and old all-ref prior-attempt search claims remain dated attribution; this audit does not freshly authenticate runtime configuration or prove exhaustive historical absence.

These are provenance and scope qualifications, not mathematical counterexamples. The old PASS certificate cannot approve a repaired future candidate or a merge by itself.

## 8. Primary source authentication and disposition

All five freshly fetched primary PDF body hashes match their original literal receipts. Nineteen relevant rendered pages were personally inspected. `PRIMARY_READ_NOTES.md` records the scopes; `FRESH_PRIMARY_SOURCE_BINDINGS.json` binds exact bytes/hashes, full actual command captures and page hashes. The underlying foreign PDFs, OCR text and pixels are removed before closure. These references are imported theorem inputs, not a claimed independent reproof of every published result. Fresh bounded primary-source searches located no full-target resolution; there is no exhaustive priority claim.

The strongest verified result is the explicit ambient four-commutator bound on the stabilized subgroup, its quasimorphism/retraction consequences, and the exact cocycle signed-defect identity with the stated invariant-probability obstruction. The exact missing result remains a sequence with ambient ordinary commutator lengths tending to infinity in the full identity component of one closed orientable smooth four-manifold, or a theorem ruling out such an example. No such sequence or theorem is supplied here.

After S1 and the current-package qualifications are satisfied, this family's mathematical review supports accepting a source-qualified **unsolved partial**, with 2/5 original turns and no new scientific turn allocation. It does not approve a future repaired package, native transition, merge, paper, DOI or tracker row. Those actions require ROOT's own current review and exact bindings. Family closure is handed to ROOT for a genuine captured closing execution; the report itself does not invent that future event.
