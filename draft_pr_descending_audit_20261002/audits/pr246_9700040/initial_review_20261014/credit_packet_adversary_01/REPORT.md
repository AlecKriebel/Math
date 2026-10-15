# Final adversarial review of the proposed PR246 credit packet

Review date: 2026-10-15 UTC. Completion timestamp and exact final seals are in
FINAL_STATUS.json and FINAL_ARTIFACT_MANIFEST.json. Completion estimate: 100%
of this bounded packet review, not of the larger research goal.

## Verdict and scope

**PASS: no mandatory correction and no optional correction identified in the
final revised local packet.** The packet accurately preserves a valid proof and
implementation while correcting its classification/credit to an earlier
covered mathematical consequence. The full candidate law follows from the
identified older stationary construction and full joint shape laws. The
additional published LRW2001 determinant route also survives direct inspection
and falsification tests. None of these conclusions relies on BO2013's heuristic
tableau dynamics, agreement of single-coordinate marginals, or search silence.

The proposed disposition is supported in its expressly defined sense:
`already_solved` records complete earlier mathematical coverage, followed by
the claimed_solved-only scope skip. It does **not** establish an earlier author
explicitly acknowledging a solution to the February 2018 posting, the proposer's
endorsement of the descriptive standard, worldwide firstness, or an earlier
publication of the exact rational enclosure/software. The final packet preserves
each distinction. A useful explicit identification, corrected presentation, or
verification implementation can remain authored work without establishing a
new underlying stationary law.

This reviewer changed no packet file. All writes are in this reviewer shard.
No native classifier, provider mutation, Git/index/ref operation, paper/deposit,
tracker update, merge/close/comment, external individual communication, or
message to another shard chat occurred. The parent coordinator's guarded native
application and readback remain separate required workflow steps; this report
does not claim that they have occurred.

## Exact final inputs and preservation

The first packet reading preceded the parent-notified LRW credit addition. Its
earlier pins are explicitly historical in RESEARCH_LOG.md. This verdict binds
the **actual revised 35-file packet**, including its nested originals:

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| current FROZEN_MANIFEST.json | 5772 | 288fecd76d8e1c81a4a4149b1c96f0ee077c49faa67fe292e4ae7749c038512f |
| current PUBLICATION_MANIFEST.json | 5938 | dffb6a9f1b6dda955f24f6a92b074b2a54097b06a4a8de0317ed776303f127c4 |
| current PRIORITY_AUDIT.md | 7559 | bfd2c5c19f196c711b3904c0f614cf41af2ddaf89fb9e22aedefeadaee214318 |
| root PROPOSED_CURRENT_PACKET_MANIFEST.json | see binding receipt | 92785e5d653b4acdb322862a64622f9ccfba3f3121b2843d961ac12bf518ee1e |

audit_packet.py independently verifies every actual file against both current
manifests and the external proposed-packet manifest, with exact file-set checks,
duplicate/path escape checks, sizes and SHA-256 hashes. The current frozen
manifest excludes itself and the publication manifest; the publication manifest
includes the frozen manifest and excludes only itself. It correctly includes
the nested original manifests. No basename-based omission remains.

All 20 original archive files independently match every INTAKE.json object by
size, SHA-256 and directly computed native Git-blob SHA-1; no Git command is
used. The archive has exactly the expected 20 files. Mathematical Sections 1–7
are byte-identical from their Section 1 marker through EOF. stationary_law.py,
verify_exact.py and exact_receipt.json are byte-identical to the original inputs.

The historical frozen/publication manifests resolve relative to
original_submission/. The historical review manifest resolves relative to its
original_submission/independent_review/ directory. Its author-proof and author-
manifest header hashes point to the archived original proof and frozen manifest,
not to the edited current PROOF header. FROZEN_VERIFICATION's author and six
source hashes were also checked against those archived bindings. All eleven
current primary byte pins match the local primary files; the original six
source entries remain exactly intact. FINAL_PACKET_BINDINGS.json records every
input and binding rather than just a PASS summary.

## Fresh executable evidence

I copied the actual source programs into three separate local execution
directories, then ran fresh isolated Python processes. Complete parsed receipts
and the complete stdout bytes match their historical expected receipts, not
merely a status field or assertion count:

| Run | Exact assertions | Whole receipt |
| --- | ---: | --- |
| corrected current author checker | 49,618 | byte-identical, SHA-256 58883d2785104bacbbf17d3ed3932274a44cdf32eb0e8d0812d02939d222fbd3 |
| archived original author checker | 49,618 | byte-identical to the same receipt |
| archived original independent checker | 15,580 | byte-identical, SHA-256 2d93ec7ca6aae450ca286031622a1460fed050efbc883c5e5258e205bbb56e00 |

The source programs remained unchanged. Fresh comparisons of all six
independently generated three-threshold raw coefficient lists with the current
evaluator reproduce all 42 historical cross-comparisons. See
ISOLATED_REPLAY_RESULTS.json, the three full receipts, independent_controls.py
and INDEPENDENT_CONTROL_RESULTS.json.

The implementation qualifications in VERIFICATION.md are accurate. The
documented evaluator accepts nonempty strictly increasing positive rational
thresholds, positive integer indices and a nonnegative integer cutoff satisfying
N+2>x_m. Arbitrary query normalization is a mathematical preprocessing rule, not
an unimplemented promise of the command-line interface. Exact fractions provide
the certificates. The display_only floats can round inward, collapse or
underflow; Python conversion, recursion, caches, memory and runtime impose
practical limits. No claimed uniform practical runtime or effective evaluation
of unspecified noncomputable real coordinates remains.

## Direct mathematical and source challenge

I read the earlier completed lane reports, but did not accept their verdicts as
substitutes for the following primary-source reconstruction. SOURCE_INSPECTION
pins the primary inputs, inspected full-page renders and source-archive members.
The older reports were treated as leads and checked deductions, not additional
independent votes within this new lane.

### 1. Does the old object really have the exact stationary law?

The [1993 unfinished notes](https://www.stat.berkeley.edu/~aldous/Research/OP/patience.pdf),
printed 36–37, define the exact positive-drift nearest-right process and give
the joint Gamma(B_r) representation in (41)–(42), including independent Poisson
spatial arrivals. The draft's sign and quantitative coupling displays are unsafe;
the packet explicitly avoids relying on them as correct proofs.

The [1995 published paper](https://www.stat.berkeley.edu/~aldous/Papers/me71.pdf),
manuscript 5–7, supplies the empty-start longest-chain/nearest-right graphical
construction and simultaneous area-preserving scaling. For its inverse counts
Z_i(t), set Y_i(s)=exp(s) Z_i(exp(s)). The inverse coordinate transform is
u=x exp(-s), v=exp(s), with determinant 1. Between events Y_i has derivative
Y_i; transformed events retain unit space-time intensity and the nearest-right
rule. The first k positions are autonomous. Area-preserving quadrant scaling
shifts the entire s trajectory, so invariance is joint stationarity, not merely
a family of equal one-time marginals. The candidate's a.s. synchronous coupling
gives finite-k uniqueness without the bad numerical mean estimate. The result
at s=0 is exactly the empty-boundary field at height 1. This closes the model,
rate, drift-sign, boundary and stationary-identification objections.

### 2. Is there a missing joint law hidden in the old ranks B?

The [1999 published account](https://www.stat.berkeley.edu/~aldous/Papers/me86.pdf),
printed 418, identifies the **entire** first row of the insertion P-tableau with
the sorted pile-top row, and supplies the RSK bijection. A specified standard
tableau t of size n and shape lambda has probability f^lambda/n!, since the
recording tableau has f^lambda choices. This determines more than the shape at
one size.

The required restriction is to small **values**, not to initial positions of
the original permutation. Direct bumping induction proves that deleting all
tableau entries above q agrees with first deleting the word entries above q
and then inserting. Large values cannot bump small values; after a small-value
insertion first bumps a value above q, all further affected values are above q.
The restricted subword is uniformly ordered, giving the coherent tableau law
jointly for all q. The shortcut that confuses this with the original position
prefix is false, for example at word (2,3,1), and is retained as a negative
control. Finiteness of B_r follows by searching disjoint value blocks for an
increasing subsequence, with failure bounded by
(1-1/r!)^floor(n/r), tending to zero for r>=2; r=1 is immediate.

Independently marking rate-one spatial arrivals by independent uniform heights
gives exactly this coherent tableau and a Poisson clock independent of B.
Consequently, **jointly at every queried pair**, Gamma(B_r)>x iff B_r>N(x)
iff the first-row length of the restriction through N(x) is at most r-1.
There is no unproved infinite-tableau correlation or interchange of infinite
limits in a finite query. The new control independently tests 46,233 value-
restriction identities and 352 full-tableau multiplicities through n=7.

### 3. Does BO2004 give the whole path with the correct factorials?

Yes. In the [versioned primary paper](https://arxiv.org/pdf/math-ph/0402064v2),
printed 3 gives one-box up probability f^nu/((n+1)f^mu). Equation (1.9),
Remark 1.5 and Theorem 2.3 explicitly admit C(x)=(x,1) and identify its whole
shape trajectory with the nested Poisson rectangles. Its size has rate-one
births and no deaths. For d births, multiplying the up probabilities along a
particular path telescopes to (f^nu/f^mu)n!/(n+d)!. There are f^(nu/mu) paths;
the independent Poisson births supply exp(-Delta)Delta^d/d!. Multiplication over
all cuts therefore gives precisely

    exp(-x_m) [f^(lambda^m)/|lambda^m|!]
      product_j [Delta_j^d_j f^(lambda^j/lambda^(j-1))/d_j!].

This is the submitted D-weight after exponential specialization. Starting at
the explicit M_(x_1) for x_1>0 removes any entrance-at-zero objection; its mass
is exactly the algebraic empty-to-first-shape factor. Summing the simultaneous
first-row barriers permits arbitrary nonmonotone indices. This is an actual
joint identification, not a marginal match. Missing the birth d! would already
miscount the empty-to-(2) raw weight over Delta=1 as 1/2 instead of 1/4.

### 4. Is Nica merely another general-purpose ingredient?

No. [Nica v1](https://arxiv.org/pdf/1404.4015v1), Theorem 3.2 and Remark 3.3,
printed 5, already display the normalized positive **multi-time** skew-Schur
product and its exponential/tableau specialization. [The v3 source](https://arxiv.org/src/1404.4015v3)
contains the same correct Schur display and the counting proof, as well as the
real typo in the factorial display's right exponent. The exact finite-square
map in the packet is correct: theta=sqrt(x_m) and
(u,v)->(u/theta,theta v). Its positive branch runs through the query widths in
reverse order at s=theta-x/theta. The shape at s=0 is lambda^m. The unobserved
branch gives D_theta(lambda^m), while successive positive-branch drops supply
D_(Delta_j/theta)(lambda^j/lambda^(j-1)). Since the skew sizes sum to the final
size, theta cancels. This is the identical candidate chain weight without an
asymptotic limit. Transposition then supplies the fixed determinant size.

I independently checked 1,026 nested chains through total size 6, using
cell-poset tableau counts for the old weights and the actual submitted
determinants for the candidate, obtaining exact rational agreement of BO, Nica
and candidate weights. These controls supplement the general identities.

The independent canonical [Nica version record](https://arxiv.org/abs/1404.4015v3)
readback records v1 in 2014 and v3 in 2015; the [BO record](https://arxiv.org/abs/math-ph/0402064v2)
records v2 in 2004. I also independently opened the pinned v3 archive: the
90,536-byte TeX member matches the local extracted file, uses article and has no
explicit date command. Its theorem and correct Schur expression are present.
The later PDF title dates are compilation-dependent evidence, not the earlier
publication dates, and today's exact PDF bytes are not asserted to have existed
in their version year. The packet handles this honestly.

### 5. Does the new LRW credit add an unsupported route?

No. I inspected the full-page displays in the [published 2001 source](https://www.math.uni.wroc.pl/~pms/files/21.2/Article/21.2.11.pdf):
printed 420 defines the finite pure-jump process and last-no-jump event; 423
(2.4) supplies exp(-y_k)H_(k-1); 425 (2.10), Theorem 2.5 and (2.13) give the
entire ell-series and determinant with row i/column j entry ell_(i-j)(y_j).
These are multivariable results, not just the later diagonal marginal.

For 0<x_1<...<x_k=a, start at y_j=a-x_(k-j), x_0=0. Unrestricted patience
sorting of that increasing initial row followed by rectangle events has U
tops below a, where

    U=max_(j=0,...,k-1) [j+L((y_j,a)x(0,1))].

The **finite** first-k count is min(k,U). Its last coordinate stays at a iff
U<k. The false uncapped count identity is not present in the final packet.
Rotating both axes sends suffix rectangles to prefixes and preserves increasing
chain lengths while reversing chain order. This turns the no-jump event into
all L(x_i,1)<=i-1 simultaneously. The result is exactly the displayed LRW
determinant with arguments a-x_(k-j). This is a finite deterministic bridge;
it does not use an invariant-law conjecture or an infinite limiting argument.

Continuity supplies ties and zeros. For arbitrary selected queries, the
nondecreasing z_i=max({0} union {t_j:r_j<=i}) gives exactly the same event by
particle ordering, so all joint probabilities follow. The determinant is empty
at k=1 and gives the known ell_0 gap expression at k=2. Fresh independent
controls test 1,043 distinct-coordinate histories for each of the capped-count,
variational and reflected-event identities, including outside-strip events,
and compare all coefficients through degree 6 at unequal-gap k=2,3,4 queries
with the submitted positive sum. The one-particle initial2/arrivals1/2,1
counterexample to unrestricted pile count <=k is retained. An initial test
generator's repeated-coordinate tie cases were corrected because they are
outside the almost-sure Poisson distinct-coordinate setting; this is recorded
in the log, rather than misrepresented as a candidate counterexample.

## Global wording, credit and remaining limits

I reviewed every current prose/metadata file and both manifest contents. The
current header, README, metadata, priority audit and disposition consistently
state complete earlier coverage and no novelty claim. The old rank law,
classical RSK/Schur ingredients and explicit BO/Nica/LRW laws receive concrete
credit with locators. The unsafe 1993 displays, unproved BO2013 route, Nica
typo, source chronology and non-established exact-wrapper priority remain
explicit. The published sampling source locator is correctly Section 6 rather
than the archived original's Section 6.3.

The unchanged mathematical Sections 1–7 remain valid: the exact finite dynamics,
stationary construction, uniqueness, direct joint RSK count, determinant
transposition, normalization and shared-normalizer rational enclosure have no
new gap introduced by the credit edit. The finite checks are expressly bounded
diagnostics; they do not replace these arguments. Numerical diagnostics in
other lanes are not relabeled as certified intervals.

AI use and unrefereed status are explicit, with no human peer review claimed.
Current preprint and DOI fields are null. No new preprint, Zenodo deposit,
tracker row, merge or closure is implied. Historical original statuses remain
unchanged only in the clearly labeled original_submission archive. The packet
log accurately describes a locally prepared correction awaiting native
application; this review's PASS does not certify a future provider action.

**Mandatory findings: none. Optional findings: none.** The only remaining
evidential limits are the expressly unclaimed historical acknowledgement,
proposer-acceptance and exact-wrapper-priority questions, and the parent's
separate execution of the authorized guarded disposition.
