# Independent audit: Kirby 3.70, ID 2868

## Verdict and exact object

**ACCEPT_UNCHANGED_STALLED_PARTIAL.** The eight-file author freeze is accepted exactly as supplied. No mathematical correction, source-attribution repair, or changed derivative is needed. The disposition remains stalled_partial, with 3 of 5 approaches used. The unrestricted generation question is neither solved nor refuted, and no novelty is certified.

This acceptance binds `KNOT_SURGERY_2868_AUTHOR_SAFE_FREEZE.zip`, 11,525 bytes, SHA-256 `c3b899805315796d6023af73be74d7133f354703447cfe85dc2b5506ccf09b8d`, and its 2,207-byte external manifest, SHA-256 `886febe0cac1758af13791337f7175a446b9ca0e4c4692909867a4982e0116ef`. The internal manifest is separately bound by that external manifest. All eight ZIP members, CRCs, exact member set, member sizes, hashes, and regular-file status were checked before any author code was executed. Original archive and manifest bytes are preserved inside this audit package.

## Independent mathematical review

### 1. Target, slopes, and inverses

The source target is the smooth, oriented, integral homology cobordism group. K3 Section 3.8 distinguishes it from the topological category; Problem 3.70 asks about all integer denominators and all knots in the 3-sphere. Its remarks distinguish single-surgery nonrepresentation from the bounded-genus result. The report respects those distinctions. [K3](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf), printed pp.181-182.

Independently, in meridian-longitude coordinates, 1/0 fills the meridian and recovers the 3-sphere; it is the identity class, not zero surgery. For any nonzero integer n, first homology of 1/n surgery vanishes because its meridian coefficient is 1. Negative n are allowed. Reflection reverses the ambient orientation, mirrors the knot, and changes the surgery coefficient's sign, giving the oriented identification -S^3_(1/n)(K) = S^3_(-1/n)(mirror K). Thus the listed generating set is closed under inverses. The report uses finite integer linear combinations, not one representative or a uniform complexity bound. All of this is consistent.

### 2. Bounded genus and the quantifier gap

HHL Theorem 1.5 uses g(K) < N and all integer denominators. The source therefore agrees with the author's indexing: genus-one surgeries belong to G_2, whereas G_1 only permits genus zero. The cited statement is properness for each fixed bound, not properness of the union. The historical sentence about the single-surgery question on manuscript p.17 is obsolete in light of NST and is correctly not presented as current status. [HHL](https://arxiv.org/pdf/1802.02008), manuscript pp.2,16-17.

The union calculation was checked directly: a finite linear combination uses finitely many knots; choosing an integer strictly above every genus puts that combination in one G_N. The converse inclusion is immediate. The zero combination presents no exception. Hence G is the increasing union of G_N. In the direct sum of countably many copies of Z, the span of the first N basis vectors is proper for every N, but every group element lies in some such span. This verifies exactly the logical countermodel in the report. It does not construct a missing class in the actual cobordism group. The failure to interchange the two quantifiers is real.

### 3. Orientation-sensitive NST calculation

The published NST p.4703 was independently rendered and visually inspected. Its identity has a minus sign: Sigma(p,q,pqn-1) = -S^3_(1/n)(T_(p,q)). The torus knot is positive; the paper's later left-handed-trefoil description is consistent after reflection and slope reversal. Its example and nonrepresentation corollary apply to positive integer k. The report's Sigma convention is the one fixed by this NST identity, so it does not silently substitute an opposite orientation. [NST](https://content.ems.press/assets/public/full-texts/serials/jems/26/12/11806810/online/10.4171-jems-1371.pdf), pp.4702-4703,4707,4741-4742.

Set A_n = [S^3_(1/n)(T_(2,3))]. Substitution gives [Sigma(2,3,5)] = -A_1 and [Sigma(2,3,6k+5)] = -A_(k+1), since 6(k+1)-1 = 6k+5. Reversing the last summand consequently yields [Y_k] = -2A_1 + A_(k+1). Each generator uses a genus-one trefoil, and reflection preserves genus. Thus [Y_k] lies in G_2. There is no missing sign, shift, or endpoint in the claimed range k > 0. Extending the nonrepresentation assertion to k = 0 would be wrong, but the author does not do so.

By the cited corollary these classes have no single-surgery representative, although the displayed finite sum consists of single-surgery classes. If that set were closed under binary addition, it would be closed under this finite sum, a contradiction. The nonclosure conclusion is therefore justified. The definite-bounding obstruction cannot itself exclude these examples from G, since they already have the displayed expression. This review does not reproduce the instanton-theoretic theorem proofs; it checks their statement, conventions, and application.

### 4. Two-handle trace and boundary hypotheses

For W obtained from Y x I by one framed two-handle, take the pair with the incoming copy of Y. Its relative handle chain complex has Z only in degree two. The long exact sequence contains 0 = H_2(Y) -> H_2(W) -> Z -> H_1(Y) = 0, so H_2(W) = Z. The inclusion of the incoming homology sphere cannot be a homology isomorphism. With m two-handles and no other relative handles, the same argument gives Z^m.

This calculation is absolute H_2(W), not merely relative homology. It does not require the outgoing boundary to be a homology sphere; it remains an obstruction to this particular trace when that boundary is one, including integral framings +1 and -1. A rational 1/n filling for general n is not being modeled by a single integer-framed two-handle. The report correctly limits its lemma to a framed-knot trace and does not infer that every cobordism between the boundaries is impossible. A unimodular surgery matrix controls the outgoing boundary's first homology, not cancellation of these relative handles. Finally, later components in sequential surgery are generally knots in changed ambient manifolds, not automatically in S^3. The two stated construction gaps remain open.

## Inputs, sources, and replay

The complete catalog, problems, and reports files were rehashed independently, rather than trusting author metadata. Their byte counts and hashes match all three supplied pins. The unique complete record, complete catalog item, and empty report were inspected. The statement digest and default-sorted-JSON digest of the entire record/report pair agree with both author and catalog values. No fields were dropped, whitespace-normalized, or rewritten before the pair hash. The inherited material is literature triage, not an uninspected proof.

All three local source PDFs match their author byte/hash pins; fresh text extraction and new page rendering were performed. The relevant public URLs were also opened. This is independent inspection of the pinned local documents, not a claim of a second network binary download. The K3 document is a watermarked preliminary version. No source PDF, extracted text, screenshot, or dataset is in either safe archive. The analytical HHL/NST proofs are cited inputs, not formally verified here.

The author checker and all seven negative controls pass in normal Python, optimized Python, and each mode from a relocated packet and unrelated working directory. Every author byte remains unchanged. Eleven additional controls reject malformed ZIPs, changed bytes, symlink entries, duplicate/nonfinite JSON, or substitution against external pins. These tests are artifact checks, not finite evidence for a cobordism theorem.

One deliberate scope probe rewrites source metadata and its internal hash together. The internal-only author checker accepts that self-consistent rewrite; the immutable externally pinned archive rejects it. This is the expected trust-boundary limitation, not a correction to the author's stated contract. Always retain the independently supplied external archive/manifest pins. The audit checker likewise requires its internal manifest's hash from an external trusted source.

Bounded read-only repository searches returned no exact-ID matches. A fresh bounded public literature search did not identify a resolution. The additional 2026 Chen preprint abstract concerns individual surgery obstructions and second-Betti-number bounds; only its abstract was inspected. [Chen](https://arxiv.org/abs/2607.02028). Neither an empty search nor the date of a problem list proves present-day openness or novelty. Nothing stronger is claimed.

## Acceptance limits

Accepted: exact problem scope; the union lemma and quantifier countermodel; the credited genus-one expression; the two-handle calculation and ambient-manifold gap; source and corpus pins; conservative 3/5 status; immutable artifact replay.

Not established: G = Theta, G proper in Theta, a new topological theorem, exhaustive literature absence, human peer review, or proof-assistant certification. No repository or queue mutation was performed. Checked 2026-10-06 by an independent OpenAI-assisted audit.
