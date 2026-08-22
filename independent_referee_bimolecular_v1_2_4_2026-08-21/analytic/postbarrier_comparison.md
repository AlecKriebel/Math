# Post-barrier comparison of the blind analytic report with author-generated records

**Comparison date:** 2026-08-21 22:42 PDT (2026-08-22 05:42 UTC)  
**Blind report fixed before access:** `analytic/preliminary_report.md`  
**Completion estimate:** 100% of the requested post-barrier analytic comparison  
**Status of this document:** coverage comparison only; author-generated audits, logs, checklists, reports, and provenance declarations are not treated as independent evidence

## 1. Materials reviewed after lifting the barrier

I read the following only after the blind report had been completed, hashed, committed, and sent to the lead referee:

- every Markdown file in `audit/`;
- every provenance Markdown file in `preservation/`;
- `research_log.md` and the complete `revision_log.md`;
- `expert_audit_note.md` and `submission/expert_audit_topics.md`;
- `supplement/reviewer_checklist.md`;
- `supplement/v1_1_mathematical_audit.md`;
- `supplement/publication_v1_1_literature_audit.md`;
- `supplement/quantitative_limitations.md`;
- `supplement/ai_use_full_statement.md`;
- `manuscript/supplementary_note.tex`;
- `validation/GIT_TAG_AND_COMMIT.txt` and `validation/REPRODUCTION_RECORD.md`; and
- the canonical `validation/VERIFICATION_REPORT.json` (the copies in `code/` and `supplement/` have the same SHA-256 digest).

I did not read another referee track's report. I did not use any author audit to modify the already-fixed blind mathematical assessment.

## 2. Bottom line

The author-generated records and the blind analytic report **agree on every one of the twelve load-bearing mathematical interfaces**. I found no post-barrier mathematical fact that changes the blind status **VALID AS STATED**.

That agreement has a limited evidentiary meaning. The expert note and reviewer checklist are explicitly orientation/falsification inventories; the audit and revision records were produced inside the same author-directed, heavily AI-assisted workflow that developed and edited the proof; and all three canonical verification reports are byte-identical copies of one generated report. These materials are useful for checking whether the blind review missed an intended interface. They are not additional independent validation.

The post-barrier review did strengthen one nonmathematical finding: the Version 1.2.4 validation records speak prospectively or declaratively of a canonical public tag, but the tag is not currently on the remote. Earlier Version 1.2--1.2.3 tags are present and match their preservation records. The Version 1.2.4 tag/provenance claim therefore remains unverified and presently inconsistent with the public remote state.

## 3. Item-by-item comparison

| # | Blind finding | Author-record coverage | Comparison |
|---:|---|---|---|
| 1 | Lifted return paths make reachability symmetric and classes closed | `expert_audit_note.md` §1; checklist §1; the focused Version 1.1 mathematical audit §1; Version 1.2 submission audit item 1 | **Agreement.** The author audit gives the same fixed-residual lift and the same zero-complex, face, parity, parallel-channel, equal-displacement, and absorbing checks. |
| 2 | Marked labelled-channel augmentation is Markov and irreducible; population projection is autonomous | expert note §5/§8; checklist §3; Version 1.2.1 audit and revision log | **Agreement.** The records emphasize the same source/target-label issue and show that projection autonomy was made explicit in Version 1.2.1. They mostly inventory the obligation rather than supply a new proof. |
| 3 | Residual log-factorial potential is proper and has the exact target/source increment | expert note §§4--5; checklist §4; verification classification | **Agreement.** The exact identity and entropy positioning match. The author materials add no independent algebra beyond the manuscript and generated checks. |
| 4 | Target-following episodes stop on every deviation and satisfy the exact recursion, including path length zero | expert note §6; checklist §5; verification report | **Agreement.** The same exact-channel continuation event and terminal ordinary jump are stressed. |
| 5 | Scalar envelope has the stated two branches, is monotone, and propagates terminal negative drift backward | expert note §6; checklist §6; revision log Version 1.0 | **Agreement.** The log records that monotonicity was made explicit in an earlier revision. The blind derivation independently verified the calculus and finite backward composition. |
| 6 | Normalized-log compactification retains divergent coordinates of zero limiting weight | expert note §6; checklist §7; Version 1.2.1 audit | **Agreement.** Both reviews identify the slower-divergent-tier distinction as essential. |
| 7 | The A/B/C bimolecular top-complex split and unary/companion/signed-invariant subcases are exhaustive | checklist §8; Version 1.2.1 audit; Version 1.2 submission audit; verification atlas | **Agreement.** The revision log records earlier clarification of \(\mathcal J\), the displayed trichotomy, and the signed invariant. The current manuscript contains those repairs, and the blind report independently checked them. |
| 8 | The exceptional set \(K\) is finite and nonempty | checklist §9; supplementary note, “Nonemptiness of the Foster set”; Version 1.2.3 audit | **Agreement.** The logs specifically record the edit making the properness sequence \(V(z_n)>n\) literal. The blind report found that current argument valid. |
| 9 | The stopped endpoint-chain supermartingale is integrable and gives finite mean hitting of \(K\) | expert note §8; checklist §10; Version 1.2.1 audit | **Agreement.** The revision history confirms that the stopped supermartingale and residual-versus-population bound were added explicitly. The present proof supplies the deterministic finite-horizon bound checked blindly. |
| 10 | The finite trace chain converts hitting of \(K\) to finite positive return to one marked state, then to population jumps | expert note §8; checklist §11; supplementary note, “Hitting versus positive return” | **Agreement.** The author note highlights the same first-jump distinction and Tonelli excursion expansion. |
| 11 | Recurrent holding-time subseries proves nonexplosion; the rate lower bound gives finite physical return; the cycle occupation law is stationary | expert note §8; checklist §12; supplementary note, “Stationary occupation balance” and “Nonexplosion in physical time”; Version 1.2.3/1.2.4 audits | **Agreement.** The revision record shows that nonexplosion was deliberately placed before physical-time expectation. The supplementary note adds an elementary balance proof behind the Asmussen citation. |
| 12 | Irreducibility gives uniqueness; absorbing singleton classes carry point masses | expert note §§2, 8--9; checklist §§11--12; supplementary note, “Absorbing singletons” | **Agreement.** The author records use the same separate convention and do not force a positive-return definition onto an absorbing state. |

## 4. Agreements beyond the twelve-item table

### 4.1 Worked examples and rate degeneration

The focused Version 1.1 mathematical audit independently states the same exact formulas that I rederived blindly:

- the initial marked reward in the Anderson--Cappelletti--Kim example is zero;
- the three later total-rate denominators and rewards give
  \(J_n=-\alpha\log n+O(1)\) with the same positive \(\alpha\); and
- for \(0\to A\to A+B\to0\), the fixed-rate coefficient is
  \(-\kappa_2/(\kappa_1+\kappa_2)\), while the fixed-\(m\) limit as
  \(\kappa_2\downarrow0\) is \(a_m(1+p_m)>0\).

The quantitative-limitations note correctly emphasizes that the terminal ordinary jump supplies the restoring logarithm and that the calculation only rules out a network-size-only uniform bound for this proof's \(K\). This matches the blind interpretation.

### 4.2 Prior-work comparison

The author literature audit supplies a more detailed Anderson--Cappelletti--Kim Section 6 dependency map than the blind report. It confirms the precise boundary sequence:

1. the pure-complex assumption supplies \(S_v\) or \(2S_v\);
2. D-tier maximality excludes \(2S_v\); and
3. the forced unary complex \(S_v\) supplies the source-rate comparison.

This fills a bibliographic-detail omission in the blind report but is not a missing premise of the new proof. The author record also identifies and corrects an earlier locator error: the historical exact numbers were from arXiv Version 2, not the published JAP layout. The current manuscript's stable Section 6/6.1 locators are appropriate.

The Paulevé--Craciun--Koeppl Lemmas 4.5--4.6 comparison, Xu's broader nonexplosion result, and the cautious ConStRAINeD status wording agree with the primary-source checks made in the blind pass.

### 4.3 Independent finite checks versus the packaged report

The packaged canonical report records 3,318 exact factorial checks and a 98,261-case three-species top atlas, plus a fixed-seed 5,000-case four-species stress test. My blind pass used a separately written standard-library oracle and checked 136,020 exact factorial instances and 56,728 independently parameterized top-split configurations. The counts differ because the enumeration schemes differ; no result conflicts. Neither finite computation proves the theorem.

## 5. What the author materials add that the blind report omitted

1. **Exact ACK published/arXiv locator history.** The author literature audit records the renumbering and the exact Section 6 dependency chain. The blind report verified the earlier theorem and example but not that full published-version mapping.
2. **Proof-evolution history.** The revision log records localized defects already repaired before Version 1.2.4: the augmented chain was named explicitly, the signed invariant was displayed, scalar-envelope monotonicity and the stopped supermartingale were made explicit, the top trichotomy and \(\mathcal J\) were clarified, self-channel deletion/projection autonomy/integrability were stated, and the stationary-law interface was expanded. The blind report checked the repaired current text and found these interfaces sound.
3. **Elementary stationary-balance route.** The supplementary note explains why the regenerative occupation measure satisfies statewise balance, reducing dependence on a black-box Asmussen citation.
4. **Disclosure of audit provenance.** The AI-use statement makes clear that generative AI was used materially for proof search, derivation, counterexample search, adversarial proof review, symbolic verification, literature work, drafting, and successive audits. It expressly disclaims independent expert human validation.
5. **Sharper release-state chronology.** The research log says on 20 August that local mathematical/release bytes were complete but “only public release sequencing remains.” This helps interpret why the copied packet can be internally complete while the advertised Version 1.2.4 tag is absent.

## 6. What the author materials omit or do not independently establish

1. **No independent human mathematical review.** The materials explicitly say none occurred. The expert topics file is only a list of possible future questions and contains no outreach or response.
2. **The central Version 1.1 audit did not reopen the central proof.** Its declared scope says the “load-bearing marked-target recurrence proof was not reopened”; it audits the new closure lemma, the rate limit, and the ACK example. It therefore cannot support the full theorem chain.
3. **Later full-proof verdicts are mostly summary assertions.** The Version 1.2 submission/frontier audits say they reconstructed all interfaces and found no blocker, but they do not preserve a second full derivation comparable to the manuscript. They are useful inventories, not checkable independent proofs.
4. **The reviewer checklist is a prompt, not a result.** It nearly exactly predicts the twelve interfaces in the user's referee prompt. Its presence explains the excellent coverage of author audits but adds no truth evidence.
5. **The expert note is derivative.** It expressly says it is not a substitute for reading the proof and largely restates the manuscript's mechanism.
6. **The canonical report copies are not independent.** All three have SHA-256
   `dc14127494eaa6ccf3b36a91f5d714ba6f79e76476f8d199760bd3b5faeed586`.
   Copy agreement proves packaging consistency, not multiple verification.
7. **Book citations were metadata-checked, not theorem-checked.** The literature audit verifies the Norris, Meyn--Tweedie, and Asmussen bibliographic fields and DOIs but gives no exact theorem locator or quotation for the invoked results.
8. **Novelty remains necessarily incomplete.** The author records repeat that no public two-species manuscript was located and that no external expert was contacted. They cannot rule out unpublished or newly public overlapping work.
9. **Production tests and author audits share provenance.** The same AI-assisted workflow contributed to the proof, verifier, tests, canonical report, and audit prose. Passing/cross-agreeing artifacts cannot be multiplied as independent evidence.

## 7. Disagreements and discrepancies

### 7.1 Mathematical disagreements

**None.** No author record contradicts a blind mathematical derivation, and no author-reported earlier correction exposes a defect still present in Version 1.2.4.

### 7.2 Release-tag discrepancy

The blind report recorded that `bimolecular-positive-recurrence-v1.2.4` was absent both locally and from the remote. Post-barrier records sharpen the discrepancy:

- `validation/GIT_TAG_AND_COMMIT.txt` calls it the canonical annotated tag;
- `validation/REPRODUCTION_RECORD.md` gives checkout/replay commands that require it and labels 20 August 2026 the release date;
- the manuscript says the supporting materials “are available” in the tagged Version 1.2.4 repository directory; but
- the research log says public release sequencing remained outstanding.

A fresh remote query found annotated tags Version 1.2, 1.2.1, 1.2.2, and 1.2.3, with tag objects and peeled commits exactly matching the preservation records, but no Version 1.2.4 tag. Thus earlier preservation claims are externally consistent, whereas the current tag claim is premature as of this comparison. This is an artifact/provenance finding, not a defect in the theorem.

## 8. Circular-reliance assessment

The author materials do not contain a fatal logical circle inside the mathematical proof; the manuscript's analytic implications stand on their own. There is, however, substantial **validation-provenance circularity** if the records are treated as corroboration:

1. AI systems helped create and revise the proof.
2. The same project workflow used AI systems to adversarially review that proof.
3. It also generated and revised the verifier and tests.
4. The verifier generated the canonical report, which was copied to three locations.
5. Later editorial audits cite the unchanged verifier/report and earlier proof reconstructions while declaring the theorem unchanged.
6. The expert note and reviewer checklist were derived from the same final proof and audit history.

Accordingly, “the audits agree,” “all reports agree,” and “the tests pass” are not independent mathematical justifications. The appropriate evidentiary hierarchy is:

1. direct proof reconstruction and exact derivations;
2. independently written falsification calculations;
3. primary-source checks for external comparisons;
4. author audits/checklists as coverage inventories; and
5. copied/generated validation summaries as reproducibility records.

The blind pass followed that hierarchy and was completed before items 4--5 were visible. Its agreement with the author inventories is therefore procedurally meaningful as a missed-interface check, although it is still an AI referee report rather than independent human expert validation.

## 9. Standard external-theorem interfaces

### 9.1 Norris, *Markov Chains*

The manuscript uses Norris for three standard facts:

1. a finite irreducible jump chain/CTMC is positive recurrent and nonexplosive;
2. for a nonexplosive irreducible countable-state CTMC, positive recurrence is equivalent to existence of an invariant probability distribution; and
3. standard finite-chain/trace facts.

The manuscript actually proves the nonstandard interface it needs most: Proposition 7.2 derives nonexplosion and finite physical return from positive recurrence of the embedded chain plus \(\inf_x\Lambda(x)>0\). Anderson--Cappelletti--Kim identify the corresponding standard jump-chain statement as following from Norris Theorem 3.5.1. Xu's primary Version 2 paper cites Norris Theorem 3.5.3 for the positive-recurrence/stationary-law interface. The author literature audit, however, verifies only Norris's metadata, not these theorem numbers.

### 9.2 Meyn--Tweedie, *Markov Chains and Stochastic Stability*

The citation is contextual. The paper does not invoke an unstated random-time Foster theorem: it defines the endpoint chain, proves the one-episode drift, establishes integrability by deterministic coordinate bounds, constructs the stopped nonnegative supermartingale, and applies monotone convergence directly. Hence no petite-set, aperiodicity, or general-state-space hypothesis is silently imported.

### 9.3 Asmussen, *Applied Probability and Queues*

The official book record places “Regenerative Processes” in Chapter VI, pp. 168--185. The author package gives no exact theorem number. The needed claim is nevertheless checkable directly. For one finite-mean return cycle, let \(N_y^{\rm out}\) and \(N_y^{\rm in}\) be the departure and arrival counts. Pathwise, including the initial departure and terminal return at \(x_*\),

\[
N_y^{\rm out}=N_y^{\rm in}\quad\text{for every }y.
\]

Conditional holding-time means give

\[
E\!\int_0^{T^+_{x_*}}\!1_{\{X(t)=y\}}dt
=\frac{E N_y^{\rm out}}{\Lambda(y)}.
\]

Taking expectations of the arrival decomposition yields

\[
\pi(y)\Lambda(y)=\sum_x\pi(x)q(x,y).
\]

The expected jump count in the cycle is finite, so the flow sums are integrable. Together with the previously proved nonexplosion, this gives stationary balance for the normalized occupation probability. Irreducibility gives uniqueness. Thus the exact Asmussen pinpoint remains bibliographically unverified, but there is no mathematical dependency gap.

### 9.4 Paulevé--Craciun--Koeppl and contextual citations

The exact external interface is Definition 1.4 and Lemmas 4.5--4.6: their combinatorial “recurrence” is symmetric population reachability, and weak reversibility implies it. The manuscript proves the lift independently and correctly distinguishes this from stochastic positive recurrence. ACK and Xu are prior-work/context comparisons, not premises of the theorem. Horn--Jackson and tier citations position the potential and compactification; the proof uses only the displayed Stirling and normalized-log calculations.

## 10. Effect on the blind verdict

The post-barrier materials reveal no substantive mathematical omission or disagreement. They corroborate that the blind report covered every issue the author considered load-bearing, while also confirming that the author records are not independent validation and that no independent expert human review occurred.

**Analytic mathematical status remains: VALID AS STATED.**

**Analytic journal recommendation remains: accept on mathematical content alone.**

The overall referee report should separately carry the unresolved Version 1.2.4 tag/provenance discrepancy, software/artifact findings from the other tracks, and the residual limitation that novelty and exact book pinpoints were not exhaustively verified.

## 11. Checkpoint log

- **2026-08-21 22:29 PDT — 15%:** lifted the barrier and inventoried all proof-facing author records without reading other referee tracks.
- **2026-08-21 22:34 PDT — 55%:** compared the expert note, checklist, mathematical/literature audits, and revision history to the twelve blind findings.
- **2026-08-21 22:39 PDT — 80%:** reviewed validation summaries, quantitative limitations, supplementary trace/physical-time note, and AI provenance.
- **2026-08-21 22:41 PDT — 92%:** independently rechecked remote predecessor tags and isolated the missing Version 1.2.4 tag discrepancy.
- **2026-08-21 22:42 PDT — 100%:** completed this post-barrier comparison; no commit or push performed.
