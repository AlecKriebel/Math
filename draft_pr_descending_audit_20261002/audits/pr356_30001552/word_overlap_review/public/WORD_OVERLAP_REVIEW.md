# Independent word/overlap audit: alternating antimorphic periods

2026-10-04 UTC. Frozen PR #356 head `12fc989f8635fd202eb66b553b9599f0546d05d3`, original base `efd29c05204703acca9a0860812f54b94fae54b1`.

**Verdict: PASS for the universal mathematical theorem and its stated uniform sharpness witness.** No mandatory mathematical correction identified. This review does not certify priority, human peer review, formal proof-assistant checking, merge status, or local Git binding.

## Source and independence

Read the complete Nowotka/Bischoff contribution, “Word periods under involution,” printed 2219–2222 / PDF 25–28, including visual inspection of every page. Official source: https://ems.press/content/serial-article-files/46296 , DOI 10.4171/OWR/2010/37. Original PDF SHA-256: `e88f211c5be990a68a967f3a9549f5db042279e8473e2cb126ea1e3caaebf98c`.

A source-only baseline was saved read-only at 2026-10-04 00:35:06 UTC before any candidate/review/program exposure; SHA-256 `3ee343260c65a958ac473583b827976c5f38464eee629a7c62fa2bd04544da5b`. Candidate inspection began only after explicit parent release. A separate independent written assessment was saved read-only before the submitted review or any current sibling-family conclusion was read; SHA-256 `5bc861f594267db5e37597de30ab21a58152809af116d99bafcb55dd6d895de8`.

The target is the unnumbered conjecture after Theorem 23 on printed 2220. Alternating theta-period p means prefix membership in `(u theta(u))^omega` for one seed of length p. For every antimorphic involution theta, positive alternating periods p,q of w, and d=gcd(p,q), the claimed implication is `|w|>=p+q-d => d is an alternating theta-period`. The imported problem's unqualified theta-period conclusion is weaker. The candidate correctly proves the stronger original conclusion. Conjecture 27 later in the same source concerns a different morphic/unbordered-factor problem.

## Checkable derivation and finite-word boundary

An involutive antimorphism of the free monoid permutes letters involutively and reverses order: bijectivity preserves the empty word and indecomposable nonempty elements, so no letter can be erased or mapped to multiple letters. Write its letter action as tau.

For an alternating seed u of length p, the bi-infinite repetition of `u theta(u)` satisfies `s(-1-i)=tau(s(i))`. Thus its segment at indices `[-L,L-1]`, where L=|w|, is exactly the canonical finite word W=`theta(w)w`. This shows W has ordinary period 2p even when L ends partway through a block. Applying the same reasoning to the independent q-seed yields ordinary period 2q on the **same** W. No equality of unseen infinite witnesses is assumed.

Ordinary Fine–Wilf (Theorem 20 in the official source) gives period 2d because `|W|=2L>=2p+2q-2d`. The threshold also gives L>=max(p,q)>=d, so the central segment `[-d,d-1]` exists and is `theta(v)v`, where v is the first d letters of w. Compare every right-half position with an in-range central position in the same residue class modulo 2d. Residues below d give v; larger residues give theta(v). This proves the exact alternating conclusion for all finite-prefix truncations.

The word-overlap/Euclidean route's tempting composition of anti-reflections would require unobserved negative indices if applied directly to w. The submitted canonical reflection construction supplies those indices legitimately and avoids that unsupported step. Period subtraction need not be postulated. Once the gcd conclusion holds, multiples of d, including p−q when p>q, are alternating periods by grouping the alternating d-blocks.

## Quantifiers, examples, and exclusions

| Claim or boundary | Audit result |
|---|---|
| Arbitrary alphabets, fixed letters, and two-letter involution orbits | Covered by the letter-permutation argument and word identities |
| Equal periods, divisibility, nonminimal periods | Valid; gcd is already a hypothesis in the degenerate cases |
| Empty word and p or q exceeding L | Cannot satisfy the positive target threshold |
| Incomplete terminal blocks and both witness phases | Covered by the common centered reflected word |
| Stronger alternating conclusion, rather than arbitrary theta-powers | Recovered explicitly from the central 2d-block |
| `abb`, p=2,q=3, ordinary reversal | Valid length-3 example lacking even arbitrary theta-period 1; proves uniform one-letter sharpness |
| Pointwise sharpness for every numerical pair | Not claimed or established; divisibility cases are trivial |
| Morphic involutions and freely mixed theta-powers | Excluded correctly; the reflected ordinary period can fail |
| Signed constraint closure in author checker | Valid finite supplement for listed pairs, not an infinite proof |

Concrete excluded-model controls confirm the limitation: with ordinary reversal, the freely mixed word `ab|ab|ba` does not give ordinary period 4 on `theta(w)w`; with morphic letter swap, `w=aab` has alternating period 2 but its un-reversed theta-image concatenated with w lacks ordinary period 4.

## Reproducible checks and exact limits

All 17 frozen snapshot disk SHA-256 bindings were checked independently against the snapshot manifest, including the own queue row's containing file. This is disk-byte verification; it does not establish literal local Git object binding, which is managed separately by the parent.

Unmodified author `check_turn1.py` exited 0 with no stderr and reproduced `TURN_1_CHECKS.json` byte-for-byte: 526,887 assertions, 18,316 binary qualifying period-pair cases, and 5,050 signed-constraint pairs. Unmodified public `review/run_portable.py` exited 0 with no stderr and reproduced `PORTABLE_CHECKS.json` byte-for-byte: 68,408 assertions, including seven author-file integrity checks and the frozen mathematical loops. The historical original 68,413 receipt additionally includes five private source bindings; those five files were not available as a complete original tree, so that mode was not independently replayed here. Reconstructed/differently rendered files were not substituted into old hashes.

The independently written direct-word checker imports no candidate checker and uses no constraint graph. It passed every ternary word of lengths 1–9 under both identity letter action and an action swapping two letters while fixing the third: 59,046 word/involution cases, 88,542 reflected-period checks, 90,930 qualifying gcd checks (336 nondividing cases), and 1,194 subtraction consequences. It also passed 1,905 deterministic longer seed/prefix cases across five involution types up to p=64, four direct sharpness examples, two excluded-model counterexamples, and two boundary controls. Program SHA-256: `3518d2f6915b287fdd2078b81af570430006b872bfb5573653f82949b174e4f3`. Whole native stdout/stderr and pre-execution pins are retained privately. The finite checks supplement the written proof.

## Exact remaining gap and disposition

Mathematical theorem gap: none found. Additional pointwise optimality is not established and is outside the claim. Historical/current priority and optional original-source integrity replay are not certified. No source raw files, external communications, candidate edits, installs, branch changes, or Git writes were performed by this reviewer.

This family recommends accepting the theorem as a reviewed proof claim while preserving the stated qualifications. Completion estimate for this family at checkpoint: 95%; remaining administrative work is parent approval and one-time read-only namespace sealing, not missing mathematics.
