" PR39 / 9500008 independent primary scope and accounting audit

**Finding: the frozen partial approximation theorem is valid in the full stated bounded-piece class. It does not settle the original random-origin question.** The old review contains one false joint-law sentence that should receive a preserved addendum; the submitted mathematical artifact does not use that false claim. The original local attempt ledger records two of five attempts coherently. Neither the native PR head nor current main contains corresponding `queue.py` state/history events, so this audit does not claim canonical queue-state accounting that is absent.

This is a source-first verification of existing work, with zero new substantive attempts and no novel mathematics search, paper, outreach, Git write, branch change, merge, release, or remote write. All new audit work is in this family folder. The original16 files, old review, and other families' files were preserved.

## Independence and exact scope

At 2026-10-02T10:10:52.924828Z I sealed the primary scope before reading `PARTIAL.md`, the old review, sibling reports, or the root certificate. Only the pinned original record/report, root pinned record/report, PR metadata, snapshot manifest, and applicable instructions were read before that seal. The independently fetched author page and v4 paper supplied the definition, assumptions, known-theorem boundaries, and literal Problem7.7. `PRIMARY_SCOPE_SEAL.json` and `.md` preserve that sequencing.

The complete literal definition is preserved at lines396–397 of `foreign_sources/burdzy_open_mathjax_20261002.html` and Definition2.1 in the v4 PDF/TeX/text. Its mathematical requirement is existence of a finite random real time S for which

\[
 (X_{S+t}-X_S)_{t\ge0},\qquad (X_{S-t}-X_S)_{t\ge0}
\]

are independent standard Brownian motions. S need not be a stopping time, deterministic, or a piece junction. In the paper this is 2BM; the more restrictive origin-zero law is 2BM(0).

The input consists of independent stopped pairs \((T_k,B^k_{[0,T_k]})\), indexed by all integers. Their laws may differ. Each Brownian motion is Brownian relative to the filtration for which its duration is a stopping time. Zero durations are allowed. Both duration sums diverge almost surely. One **deterministic** finite c satisfies \(T_k<c\) almost surely for every k. Endpoint information belongs to the stopped pair even though the concatenation formula uses half-open intervals. The countable index set lets the individual almost-sure bounds be imposed simultaneously.

The author's live [Problem8](https://sites.math.washington.edu/~burdzy/open_mathjax.php) and [Burdzy–Scheutzow v4](https://arxiv.org/abs/1302.6958v4) take priority over the corpus's abbreviated statement. The corpus omits the random-origin definition. The omission is repaired by the primary source when interpreting the target; it is not permission to substitute fixed-origin Brownianity or an iid subclass.

The live author page still presents Problem8 without a solution notice. This is scoped evidence of its author-maintained status, not a certificate of exhaustive current literature or novelty. The supplementary [Pitman–Tang2015 discussion](https://www.columbia.edu/~wt2319/Slepian.pdf), printed page3, distinguishes the iid finite-mean result from nonidentical pieces; it does not supply the exact target's quantifiers.

## Full source-proof coverage and limitations

I read the complete operative Definitions2.1–2.2 and the complete proofs of Theorems5.1–5.3, printed pages18–21, plus the entire literal Problem7.7 and surrounding open-problem context. Source hashes, URLs, the supplementary passage, TeX disambiguation, and precise read coverage are in `SOURCE_PROOF_COVERAGE_RECEIPT.json`. The referenced renewal stationarization, boundary hitting-tail, and heavy-tail sum theorems are recognized external inputs; this audit did not independently reconstruct the cited books and papers.

**Theorem5.1, actual iid finite-mean proof.** Strong decomposability means identical laws for the entire stopped pairs, not merely identical durations. Finite positive mean permits a random renewal-stationarizing shift Θ. The source chooses Θ from the junction configuration without additional dependence on the stopped trajectories. An independent uniform shift on [a,2a] gives junction configurations converging in total variation to the stationary shifted configuration. Conditional on durations, iid pairs provide one common stopped-path kernel for every index. Transferring this kernel carries total variation convergence to the centered whole-path laws. Since every sufficiently far-right deterministic window is exactly a Brownian two-sided window, the stationary shifted limit has the exact 2BM(0) law on every finite window and hence on the whole line. Thus Θ supplies the required finite random origin. For nonidentical pairs the conditional path kernel can depend on the index; the source does not establish this transfer in that class. The argument is not a proof that the original junction is Brownian. Zero-duration iid pieces may be removed by iid thinning to positive durations; divergence excludes the all-zero law.

**Theorem5.2, rotation and heavy-tail obstruction.** This theorem concerns iid square-root-boundary stopping times with moments below one. Its proof rotates each reversed negative piece by 180 degrees while keeping endpoints. The rotated comparator is Brownian, because it is a forward concatenation of sign-reflected stopped Brownian pieces. A macroscopic surviving piece and one-sided comparison yield a positive separation from a hypothetical backward Brownian scaling limit. The extracted PDF text makes the radical placement easy to misread. The independently fetched [v4 TeX source](https://arxiv.org/src/1302.6958v4), member `ForwardBM_postPTRF.tex`, lines1225–1232, gives the separation

\[
 c_1\sqrt{\beta/2}-\tfrac{c_1}{2}\sqrt\beta
 =c_1\sqrt\beta\,(\sqrt2-1)/2>0.
\]

`check_source_qualifications.py` verifies the coefficient exactly. The primary rotation construction is known prior work and is correctly credited in `PARTIAL.md`. Its use as a comparator does not construct an exact random origin.

**Theorem5.3, uniform-moment failure.** The source uses independent time-zero activation coins and nonidentical rare pieces stopped when a unit forward increment hits c_j. Inactive lengths are zero; positive-index lengths are one. For prescribed \(\alpha>0\), the active duration has a finite \(\alpha\)-moment \(\lambda(c_j)\); setting \(p_j=1/\lambda(c_j)\) makes every duration's \(\alpha\)-moment one. The block lengths \(k_j=\lceil1/p_j\rceil\) give infinitely many active negative pieces almost surely, so their length sum diverges. Increasing c_j are chosen to make Brownian unit-increment hits before a growing deterministic horizon have probability at most one half. These pieces have unbounded support; a uniform prescribed moment does not satisfy the deterministic duration bound.

The literal displayed source proof needs two qualifications when checking its final hitting-time inequality. They are presentation issues in the known obstruction and are not new target-solving mechanisms:

1. A terminal forward increment +c becomes a backward increment −c. The source displays \(Y(t)=X(S-t)-X(S)\) and then a +c event. Under its hypothesized Brownian law, use the globally reflected path \(\widetilde Y(t)=X(S)-X(S-t)\), also Brownian. This restores the event orientation. It does not assert invariance of the joint stopped-pair law.
2. A continuous unit-increment curve that begins above c at time1 may reach a value at least c later without hitting exactly c after time1. The source's displayed equality-hit bound omits this initial-level boundary case. Add \(\mathbb P(\widetilde Y(1)\ge c_{m+1})\), which tends to zero for Brownian motion as \(c_{m+1}\to\infty\).

Here is the checkable completed deduction. Write \(D_m=\sum_{i=1}^{k_1+\cdots+k_m}T_{-i}\). The first active piece beyond block m exists almost surely; preceding inactive pieces have duration zero, so its right endpoint is −D_m. Its terminal unit increment is \(c_j\ge c_{m+1}\), after choosing the thresholds increasing as allowed by the source. If \(-D_m<S<m\) and \(D_m+1<u_m\), the reflected backward unit-increment curve reaches that value at time \(S+D_m+1\in[1,u_m+m)\). Continuity gives an exact c_{m+1} hit unless the time1 increment already starts at or above that level. Consequently, for \(H_c(y)=\inf\{t\ge1:y(t)-y(t-1)=c\}\),

\[
\begin{split}
\mathbb P\{H_{c_{m+1}}(\widetilde Y)\ge u_m+m\}
\le{}&\mathbb P(S\ge m)+\mathbb P(S\le-D_m)\\
&+\mathbb P(D_m+1\ge u_m)
+\mathbb P(\widetilde Y(1)\ge c_{m+1}).
\end{split}
\]

Every term tends to zero: S is finite, \(D_m\to\infty\) almost surely, the third term is at most \(2^{-m}\), and the last is a Gaussian tail. The source's choice of thresholds gives the Brownian probability on the left at least one half, a contradiction. Thus the moment obstruction survives; this audit does **not** claim every step of the source's literal final display is already correct without these qualifications. Exact orientation, the continuous initial-above-level example, and the Gaussian tail limit are preserved in `SOURCE_QUALIFICATION_RESULTS.json`.

**Problem7.7.** Its literal claim asks whether a decomposable FBM can have an almost surely finite pathwise supremum of the lengths and fail to be BBM. That supremum may be random and is weaker than a deterministic common bound. Failure of BBM is stronger than failure of 2BM. This is related to Problem8 but not equivalent by the cited definitions. This audit does not promote it into an alternative target.

## Independent proof audit of the frozen partial

The proof's valid comparator uses only the original negative stopped pairs, in order −1,−2,…, changing signs but not reversing each piece internally. With \(A_j=\sum_{i=1}^jT_{-i}\),

\[
 W_{A_{j-1}+u}=-\sum_{i<j}B^{-i}_{T_{-i}}-B^{-j}_u,
 \qquad 0\le u\le T_{-j}.
\]

For each original Brownian motion, its negative is still Brownian for the same filtration and T remains a stopping time. The measurable transformation of independent stopped pairs preserves independence. It need not preserve their joint laws. Finite concatenations of these independent valid stopped-Brownian pairs, followed by an auxiliary independent Brownian tail, are Brownian by repeated strong-Markov splicing. They agree with the infinite comparator through A_J. For each fixed horizon L their path laws differ by at most \(\mathbb P(A_J\le L)\to0\). Therefore the infinite comparator is Brownian. The auxiliary tails are only a verification device; the actual W is a measurable function of the original negative stopped pairs and exists on the original space.

This finite-splice argument includes zero durations without conditioning on randomly selected positive indices. Repeated junction values agree. Divergence ensures each fixed horizon is covered after finitely many indexed pieces, even with arbitrarily small or many zero lengths. No deterministic lower bound or renewal-rate estimate is used.

The nonnegative half of X uses only k≥0 and is Brownian by the same argument. Independence of the two entire countable stopped-pair families gives independence of the two process sigma-fields. Thus the comparison process \(Z_t=X_t\) for t≥0, \(Z_t=W_{-t}\) for t≤0, has the genuine 2BM(0) law on the same probability space.

In a negative piece starting at \(a=A_{j-1}\) with duration T, direct evaluation from the source indexing gives

\[
 X_{-(a+u)}=W_a+W_{a+T}-W_{a+T-u},\quad
 X_{-(a+u)}-W_{a+u}
 =[W_{a+T}-W_{a+T-u}]-[W_{a+u}-W_a].
\]

Both increments have duration u≤T<c. If a+u≤R, their endpoints lie in [0,R+c], including a horizon cutting the last piece. Hence the exact bound

\[
 \sup_{0\le t\le R}|X_{-t}-W_t|\le2\omega_W(c;R+c)
\]

holds pathwise and at repeated endpoints. This does not assert Brownian time reversal of a stopped piece.

The deterministic cover by [jc,(j+2)c], with 2^m+2 intervals for \(R_m=c2^m\), and reflection/Gaussian tails give

\[
 \mathbb P\{\omega_W(c;R_m+c)>r\}
 \le4(2^m+2)e^{-r^2/(16c)}.
\]

With \(r=8\sqrt{cm}\), these probabilities are summable. Overlap causes no problem because only a union bound is used. Borel–Cantelli and monotonicity between consecutive dyadic radii prove the simultaneous almost-sure logarithmic estimate. c is positive because otherwise duration divergence is impossible. No piece-count control is hidden in the covering argument.

Thus the strongest verified result is

\[
 \sup_{|t|\le R}|X_t-Z_t|=O(\sqrt{\log(2+R)})\quad\text{almost surely},
\]

and, for each finite nonnegative L, \((r^{-1/2}X_{rt})_{|t|\le L}\) converges in law to 2BM(0) on that compact interval in uniform topology. The scaled coupling difference tends to zero almost surely; Brownian scaling supplies the exact comparator law for every r. No almost-sure convergence of rescaled Brownian paths to a single path is needed.

The fixed-junction diagnostic \(T=\min(\tau_{-1},1)\) is valid: on the positive-probability event of hitting −1 before1, the reversed final negative piece is positive on an initial interval, an event of probability zero for Brownian motion started at zero. Yet the stopped pairs are iid with finite positive mean, so Theorem5.1 gives an exact random origin. The example disproves 2BM(0) only. Grouping periodic entire stopped-pair laws into m-piece blocks also legitimately invokes the known iid theorem; periodic durations alone would not suffice.

The exact remaining gap is construction of one finite random S giving two independent exact Brownian half-paths for every nonidentical bounded-piece sequence, or a counterexample for which every such S fails. The approximation alters each negative piece internally. Brownian windows at deterministic observations a→∞ and diffusive error estimates supply no finite exact origin on the original whole trajectory. This route remains blocked at the stationary marked-shift step unless a materially new mechanism is supplied.

## False old-review wording and required qualification

The old review's sentence at original `review/REVIEW.md` line22 claims reflection preserves each stopped-pair law. This is false. For \(T=\min(\inf\{t:B_t=-1\},1)\), the event \(T<1,B_T=-1\) has positive probability. For the reflected pair \((T,-B_{[0,T]})\), its terminal value on T<1 is +1, so the corresponding −1 event has probability zero. `check_source_qualifications.py` also preserves an exact eight-input stopped-walk analogue with event counts4 versus0.

The correct statement is that −B remains Brownian in the same filtration, T remains a stopping time, and the transformed independent pairs remain independent valid stopped-Brownian pairs. The finite-splice proof above then applies. `PARTIAL.md` already uses this valid claim and contains no assertion of unchanged joint laws. The old review's absolute statement that it required no corrections should therefore receive a scoped addendum. Preserve the historical review; no change to the frozen approximation formulas or proof mechanism is necessary.

## Original package, actual corpus, diagnostics, and accounting

All16 original files were read completely, including `PARTIAL.md`138 lines, old review79 lines, both submitted scripts52 lines each, independent script87 lines, all results, readiness, source/report, source checksums, turns, README, and log. The entire 49,891-byte741-line diff was read in three untruncated segments and checked byte-for-byte against native `git diff` between c6975ca76f9f667f1250ba403d0e6da2aafe14d0 and 652b8115080e5e97b2274cb602de3faf8c551f20. Every frozen file matches its native original blob, declared hash, size, and exact relative member. The17 changed paths are the queue row and the16 attempt artifacts. `check_original_packet.py` performs these checks against the actual packet and native objects.

The raw corpus check independently hashed 149,266,659 bytes across `problems.json` and `research_results.json`, verifying both against manifest revision37e53eabe540fb458758e198be61634bd02ee008. It contains15,458 records and exactly one AMR-094-0008. That key has an actual nonempty prior report; no fallback was used. The SQLite catalog was opened with URI `mode=ro`, has the same count and revision, and its entire selected payload/report pair equals the raw JSON pair. The frozen and root-pinned full record/report equal that pair. `CORPUS_ACCOUNTING_RECEIPT.json` records the complete receipt; `raw_source_record.json` and `raw_prior_report.json` preserve the entire selected objects.

Calling the actual pure `queue.score(p,r,cfg)` reproduces literal statement hash8657a696… and sorted full-pair review hashee839ad6…. These hashes match readiness and the desk assessment. The abbreviated corpus report contains no prior proof attempt. A full-statement keyword scan finds85 related Brownian/concatenation/two-sided records and no second exact normalized statement; the selected ID has no literal match in related-target groups. Such a corpus scan is not an exhaustive mathematical equivalence or literature search.

The original local `turns.json`, readiness used-count, README, log, PR body, and proposed queue row agree on2/5: an unresolved iid/finite-window extension route and the partial rotation estimate. Numbering is sequential, the artifact seals agree, no full candidate is declared, and the original stated two-hour bounds are05:36:50Z–07:36:50Z. Logged original work and review lie inside that period. Historical metadata claims Astra/xhigh; the current policy text says Astra/ultra. This audit records both and does not independently certify the historical model configuration or infer unauthorized choice without the full human instruction history.

Native base, native current main3d6aef8006c971dc044e0eebc3fee8af8d96612d, and the current working tree have no attempt9500008 directory and show queued0/5. Native PR head has16 attempt files and its queue row says unsolved2/5, but `state.json` and `history.jsonl` still have no9500008 events there. `NATIVE_LEDGER_SCOPE.json` preserves this absence truth. Local PR accounting is coherent; it must not be described as evidence that `queue.py turn` recorded those responses in canonical state/history. This audit made no shared accounting edits.

The actual three original scripts were copied and replayed with `/usr/bin/python3`, using the already installed SymPy1.14.0. All pass, and generated outputs are byte-identical to their frozen expectations:12,288 finite configurations and48 prefix laws;12 independent named groups,144 path configurations,2,256 rotation equalities, and16 randomized zero-duration prefix laws. These diagnostics check algebra, finite regeneration analogues, constants, and indexing. They do not establish Brownian process laws, almost-sure estimates, or the random-origin claim; those are evaluated separately above. The default Homebrew Python3.14.6 fails to import SymPy; its actual return code and traceback are preserved in `default_python_failure.json` and the replay receipt. The original snapshot was unchanged.

Real mutations of the actual packet reject iid narrowing of the full source statement, erasure of the actually present prior report, and a coherent six-attempt ledger beyond the five-attempt limit. Altering the actual independent script's rotation sign causes an actual assertion failure and a packet-byte rejection. `NEGATIVE_CONTROL_RESULTS.json` retains commands, return codes, complete outputs, and failed inputs rather than synthetic pass markers.

The independently fetched v4 paper and supplementary PDF match original source hashes byte-for-byte. The live author HTML is18,645 bytes/hash42d29873…, while the original declared source was18,646 bytes/hashdc059a22…. Simple newline variants do not match. This mismatch is preserved; this audit does not falsely claim reproduction of the earlier HTML bytes. Its exact operative live definition and assumptions were independently read and sealed. `HTML_BYTE_NORMALIZATION_CONTROL.json` records the failed variants.

## Disposition and own-family closure

Accept the result only as a scoped valid partial checkpoint, with the full target unresolved and novelty unconfirmed. Credit the known iid theorem and source rotation. Add the old-review joint-law correction without overwriting the historical report. Do not create a paper or describe the estimate as a solution or new-discovery certificate.

`check_family_manifest.py` seals the exact entire own-family root. It distinguishes preserved foreign downloads/extractions from first-party prose, code, receipts, original replays, and real negative-control ledgers; both categories have exact member and byte checks. Only the manifest at its **exact root-relative path** excludes itself. A nested file with the same basename receives no exemption. `run_manifest_controls.py` tests actual copied own-root baseline, nested-basename injection, removal of a first-party checker, and foreign-PDF corruption, preserving the outcomes and failed trees.

The investigation's original15% full-resolution estimate remains a historical estimate, not evidence of new progress toward the exact origin. Audit completion is reported separately in this family's research log. No new substantive proof response was consumed.
