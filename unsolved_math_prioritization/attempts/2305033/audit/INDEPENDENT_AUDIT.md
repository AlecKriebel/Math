# Independent source and scope audit: Function Theory 5.33

Audit date: 2026-10-05 UTC. Target: rank 680, ID 2305033, AMR-022-5033.

## Verdict

**PASS for a source-verified `already_solved` disposition, with the access and
proof-verification limits below.** No blocking mathematical correction to the
frozen author packet was found. This is not a new solution, a proof of the
historical coefficient estimate, or grounds for labeling this investigation a
new `verified_solved` result.

The reviewed author manifest has SHA-256
`6f3763c7b21f9577a9145979b94eacc4fc124669d0ff326889350b4300eb1d81`.
All eight author files, including the manifest, were inspected. The seven
manifest-listed file sizes and hashes were independently recomputed. The
eight-entry author archive contains exactly the corresponding author bytes.
The frozen author directory and archive were not changed.

## Sources actually checked

1. [Hayman and Lingham, Research Problems in Function Theory (New Edition),
   arXiv:1809.07200v2](https://arxiv.org/pdf/1809.07200v2#page=98):
   Problem and Update 5.33, printed page 97 / PDF page 98, read through the web
   reader and visually checked in an independently rendered page of the existing
   local PDF. The update expressly attributes the affirmative answer and
   `a_n = O((log n)^(-1/2))` to reference 416. Bibliography entry 416, printed
   page 228, identifies the article below. No extra normalization appears in the
   problem statement. The source is an authors' draft, not represented here as
   a final published edition. Its [arXiv landing page](https://arxiv.org/abs/1809.07200)
   identifies v2, dated 21 September 2018, as the latest displayed version.
2. [Hayman, Patterson and Pommerenke, On the coefficients of certain automorphic
   functions](https://www.cambridge.org/core/journals/mathematical-proceedings-of-the-cambridge-philosophical-society/article/abs/on-the-coefficients-of-certain-automorphic-functions/D77B4B2DAE33D91F925F9BD9BB80C026):
   publisher metadata and opening extract checked. The authors, journal,
   volume 82, issue 3, November 1977, pages 357-367, and
   [DOI 10.1017/S0305004100054013](https://doi.org/10.1017/S0305004100054013)
   agree with bibliography entry 416. The online date, 24 October 2008, is
   distinct from the original publication year. **The full 1977 proof was not
   retrieved or inspected by this reviewer.**
3. [Patterson, A footnote to 'On the coefficients of certain automorphic
   functions'](https://www.cambridge.org/core/journals/mathematical-proceedings-of-the-cambridge-philosophical-society/article/abs/footnote-to-on-the-coefficients-of-certain-automorphic-functions/DAD0CD2E256D05B849E593D9165907F4):
   publisher search result metadata and extract independently checked. They
   support the 1978 sequel's identity and stated sharpening purpose. No theorem
   from that sequel is used and no full-proof inspection is claimed.

The existing local Hayman-Lingham PDF is 1,706,228 bytes, SHA-256
`8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0`.
These are independently recomputed local-file properties, not a certificate
that this review freshly downloaded the public PDF or compared fresh remote
bytes. A web screenshot request failed; the successful visual check used a new
local render. No blocked download was retried or circumvented. Source PDFs,
text extractions, page images, and imported records are excluded from this
public-safe audit directory.

## Scope audit

- Writing a regular triangular lattice as `L = b + c(Z + exp(i*pi/3)Z)`, with
  `c != 0`, covers the target's rotations, translations, and nonzero scales.
  The function is the holomorphic universal covering projection from the disk
  onto `C \ L`. It is surjective and has nonvanishing derivative. Mere omission
  of lattice values does not impose the covering condition.
- The Taylor coefficients are ordinary coefficients at the disk origin.
  The reported conclusion concerns each fixed covering map and lattice as
  `n -> infinity`. Allowing the implied constants and threshold to depend on
  that fixed map is a conservative interpretation of the source's big-O
  statement. It does not assert a common constant across all basepoints or
  similarity scales.
- There is no justified additional requirement `f(0)=0` or `f'(0)=1`. In the
  standard lattice, zero is omitted. For a fixed lattice and basepoint, source
  rotations can change derivative phase but not magnitude.
- Target similarities change each positive-index coefficient by the same
  nonzero scale; translations affect only the constant term. A source rotation
  multiplies coefficient `n` by a number of modulus one raised to power `n`.
  These transfer identities are exact.
- A general disk automorphism is a conformal covering isomorphism of the disk,
  so precomposition still gives a universal covering projection. Its coefficients
  need not transform diagonally. Applying the source-reported assertion to this
  new member of the class is legitimate. No unsupported general theorem about
  preservation of coefficient decay under arbitrary analytic composition is
  needed or claimed.
- Independently read Update 5.7, printed page 87, and the relevant Update 5.5
  and Problem/Update 5.40 discussion, printed pages 86 and 100. Their different
  scope for arbitrary subordinate maps makes it particularly important not to
  extend Problem 5.33 to all functions omitting the lattice. The packet does
  not make that extension. The sentence about a remaining subordinate-function
  question in Update 5.7 is not adopted as a standalone current-open-status
  claim; the neighboring updates give additional results and counterexamples.

This is a verification of the scope reported by Hayman-Lingham. It does not
claim direct inspection of the original 1977 theorem's hypotheses or its proof.

## Independent review of the elementary arguments

1. **Decay from the imported estimate:** for positive epsilon, choosing a
   threshold beyond the estimate's starting index and
   `exp((2C/epsilon)^2)` makes every later coefficient smaller than epsilon.
   This proves only the elementary implication, not the estimate itself.
2. **No scale-uniform bound:** the cover is unbounded by surjectivity onto an
   unbounded domain. A polynomial is bounded on the disk, so the cover has
   nonzero coefficients at arbitrarily large indices. Scaling at one such
   index violates any proposed pair of constants common to all scales.
3. **Bounded analytic comparison:** Parseval on each circle gives a uniform
   bound for the square sum with radial weights. Taking radial limits in
   finite partial sums, then taking their supremum, proves square summability
   and coefficient decay. The covering map is unbounded, so this cannot be
   substituted for the required theorem.
4. **Lacunary Bloch negative control:** the series with terms `z^(2^k)` and
   its derivative converge normally inside the disk, as follows by comparison
   with the full geometric series and its derivative. Its coefficients at
   powers of two equal one. For `r <= 1/2`, the full derivative majorant is
   at most four. For larger `r`, set `t=-log r`; the integrand on `[x/2,x]`
   is at least `exp(-tx)`, which proves the displayed integral bound for each
   `x=2^k`. Summing the adjacent dyadic intervals bounds the derivative by
   `2/(rt) <= 4/t`. Finally `1-r^2 <= 2t` proves the claimed Bloch seminorm
   bound of eight. This is a correct counterexample to the generic Bloch
   shortcut, not a counterexample to the target.

No hidden appeal to finite experiments is required for these infinite
statements. The stated proofs supply the needed arguments.

## Computation and repository checks

Both author scripts were read before execution. The integrity script passed.
The finite exact-arithmetic script passed and its stdout matches
`EXPECTED_CHECKS.json` byte-for-byte. The category counts were also inspected:
72 affine/rotation evaluations, 24 translation controls, 44 finite lacunary
Bloch controls, and 22 sparse-coefficient controls, totaling 162. These checks
use rational arithmetic and have the modest scope explicitly stated by the
author. They do not numerically or formally certify the historical theorem.

A fresh read of the [public queue](https://github.com/AlecKriebel/Math/blob/main/unsolved_math_prioritization/QUEUE.md)
at blob `dce961ea85917a765b29405f55dec6347d326660` still shows rank 680 / ID
2305033 as `queued`, `0/5`. Fresh exact-ID searches returned no PR and no
branch. The broader historical searches documented by the author were not
all rerun. Therefore the correct interpretation is **no prior repository
attempt or duplicate found in the specified bounded searches**, not an
exhaustive assertion that no historical duplicate can exist.

The raw upstream statement/report files were not obtained, their imported
hashes were not independently reproduced, and the upstream AI report remains
uninspected. The public catalog identifiers bind the intended target; they do
not certify complete raw-record inspection. These limits must remain visible.

## Accounting and publication interpretation

- Preserve the author's historical record of zero new proof-search turns.
- For this campaign's ledger, count the substantive prior-literature response
  as **one turn out of five**. An author-local proof-search count and a campaign
  response count measure different things; the former must not reset or erase
  the latter. The audit itself is verification, not another proof-search turn.
- The justified outcome is `already_solved` with explicit attribution, not a
  novel result or a reconstructed proof. No extra artificial approaches are
  warranted once the verified prior-resolution stopping condition is reached.
- No source or dataset contents, private-source files, or private coordination
  records should be published with this audit. The author files and this audit
  contain authored analysis/code or permitted public verification metadata.
- This reviewer made no remote writes and no changes to the frozen author
  packet. Repository status changes and publication, if any, are separate
  actions, not established by this audit.

The accounting clarification and bounded-search wording above are publication
interpretations, not changes to the frozen historical packet. No mathematical
correction overlay is required.
