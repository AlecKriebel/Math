## Accepted partial theorem; exact asymptotic unresolved

For the classical Hofstadter consecutive-sum sequence with seed (1,2), each
later term is the least integer strictly greater than its predecessor that is
a sum of at least two consecutive earlier terms. The accepted theorem gives,
for every integer n>=2, with all logarithms natural,

    a_n-n >= (log(log(n))-log(log(5)+log(2)/3))/log(4).

The finite plateau lemma gives V<Q<=2*T^2*(T-1)^2<2*T^4 for any
constant-deviation interval 3<=r<=s, where T=a_r, V=a_s and Q is the least
2*4^k strictly above T^2*(T-1)^2/2. This subfamily of powers makes 8Q a square;
the positive one-sided crossing error is excluded by a difference of squares.
The all-index threshold recurrence handles skipped levels and nonempty
plateaus and starts at M(0)=5. No mathematical correction was required.

The result improves the specific log20 coefficient displayed in Theorem 1.4
of [Quanyu Tang, The Hofstadter consecutive-sum sequence omits infinitely
many positive integers, arXiv:2603.09939v2](https://arxiv.org/abs/2603.09939v2),
revised 23 March 2026. Tang's plateau and threshold-function strategy is
credited explicitly. The prior polynomial upper bounds are recorded with
attribution and are not independently re-proved here. Public metadata describes
a submitted manuscript; no journal acceptance is asserted.

The original formulations were historically checked in [Erdős 1977, printed
p. 71](https://www.renyi.hu/~p_erdos/1977-27.pdf) and [Erdős–Graham 1980,
printed p. 83](https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf).
Complete source-file retrieval, text-reading scope and visual inspection
are distinguished in SOURCES.json. No newly verified live problem-tracker
status or exhaustive novelty review is claimed.

The exact asymptotic, b_n=o(n), and even an O(n) upper bound for a_n remain
untouched. A plateau-length upper bound supplies no upper control on the
frequency of omissions. Synthetic crossing obstructions are not established
actual greedy prefixes. No global novelty, priority or optimality is claimed.

## Complete proof, audit and review boundary

The complete original proof and complete independent mathematical audit are
preserved byte-for-byte as initial portions of their edition files, followed
only by appended edition/review statements. Original acceptance fields are
retained with an added scope note. Acceptance is an independent internal AI
audit of this specified partial result. The AI-assisted work is unrefereed;
no external human peer review, journal acceptance or formal proof-assistant
certification is claimed.

Historical independent checks used explicit exception guards. Normal Python,
-O and -OO yielded byte-identical mathematical reports. Separately implemented
generators agreed for 4,000 terms; the entire through-value-200000 sequence hash
matched the candidate: 199,224 terms, final deviation 776. Checks covered 765
observed plateaus, 775 threshold recurrences, 2,604,372 allowed crossing
constants, and 2,044 subset prefixes. Ten package-integrity mutations were
rejected per mode. These finite checks supplement the written infinite proof.

The candidate's own assertion-based verifier now rejects optimized modes.
That is distinct from the independent audit checker's successful -O/-OO runs;
no optimized-mode pass of the candidate's mathematical assertions is claimed.

Exactly eight prose and public verification-metadata files are additions under
attempts/2112. Programs, raw datasets, detailed execution receipts, full
computational certificates, copied sources/text/images and private coordination
material are excluded. This edition is not an executable reproduction package.
Preparation checks byte integrity and publication structure without new
mathematical test execution or scholarly-source retrieval/inspection. Original
sealed packages, QUEUE.md and all unrelated repository paths are unchanged.

## Exact public-file identities

- `ACCEPTANCE.json`: 3,068 bytes; SHA-256 `2700052d8d2177eca16b24aee987d02b781bffecf50f9101b2fde254f880cd2e`.
- `ACCEPTANCE.md`: 4,141 bytes; SHA-256 `e4f15f9e604ceddbf5762dad95403136ffae55f340179c0e335761a6f5101f3b`.
- `AUDIT.md`: 11,058 bytes; SHA-256 `db8e5b5d264d2a471191f605690c26609ed5bf7ef6e509f7049c627eb057ef7c`.
- `MANIFEST.json`: 1,692 bytes; SHA-256 `5a75b3192f51ce1ffe940ee1f40b5d4df06aff55b0d8cea43ccec3166497bdae`.
- `PROOF.md`: 7,566 bytes; SHA-256 `6ff98a5240b1af8958c1e277bff40f5060d34d331629a6b6280c694a5ff8f84f`.
- `README.md`: 3,172 bytes; SHA-256 `7c6eba3816b6d7da7bbd1dcdc989494edfa9262170063411149387fa42babeb2`.
- `SOURCES.json`: 6,030 bytes; SHA-256 `e91c80ea19cc4dd708654883706f0cc0f3843939287626ff1490033877f77b53`.
- `VERIFICATION.json`: 2,907 bytes; SHA-256 `24c53ce68b3eaa03a2ed8cdbe3094fed4465e69ad4b306e79c93a5a39cf3c3ca`.

MANIFEST.json lists all eight members and hashes the other seven; this body independently pins its digest.

