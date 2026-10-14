# Fresh adversarial package review 02 — PR 815 / problem 30006166

**Verdict: CLEAR. Required fixes: none. Unresolved concerns within the assigned
scope: none.** This is a fresh manual mathematical and package review of the ten
current core files sealed by `PACKAGE_SEAL_R2.json`, the closed verification
archive, and the separately pinned corrected `pr815_revision_r1b` repository
assembly. No central mathematical gap, missing required credit, unsupported
publication claim, archive inconsistency, reproduction failure, metadata drift,
or visual defect was found.

Reviewed October 13, 2026 America/Los_Angeles / October 14 UTC. Frozen original
head: `5bee5139501a399da653f634147eab9433774ac7`. Only PR 815 and numeric problem
30006166 were audited. Original proof effort remains **3/5**; this review made
**zero new central proof-search responses**. No original/core edits, Git writes,
PR writes, Zenodo actions, sheet writes, or external communication occurred.

## Independence, exact target, and mathematical result

I first read current `note.tex` and the complete text of its five-page PDF, then
independently reconstructed and attacked the argument against the primary CJMST
statements. `INDEPENDENT_PROOF_RECORD.md` was saved before reading previous
review conclusions or the seal's `previous_clear` field. Prior acceptance did
not supply any premise of this reconstruction. Historical reviews and the first
final package review were consulted only afterward.

The complete selected database record and its empty prior report were read with
a read-only query. Independently calculated statement SHA-256 is
`33441e0172f1653aaa85c1528ce39b90030aec6726589b622a2511fbf5f0c597`;
the complete-record/empty-report review fingerprint is
`db8ab75699d8f143e031873e1d7326fad1d0d6fbd8b637b59a82bd2c63793f91`.
The related-target ledger has no entry for this ID. The full primary contribution
on printed pp.114–115 of [Oberwolfach Report 2/2025](https://doi.org/10.4171/owr/2025/2)
defines all continuous Cantor actions and whole-space Borel hyperfiniteness;
Question 3 has exactly the target claimed here.

The strongest independently checked deduction is: a dense G-delta in the full
space of continuous actions of the restricted countable group Z wr Z on Cantor
space has an entire hyperfinite Borel orbit relation. The auxiliary theorem
covers arbitrary Borel actions **with an equivariant Borel profinite shift
height**, including stabilizers. Neither a free/minimal/pmp ambient subspace nor
a conull/comeager phase-space restriction replaces the target. The statement
does not cover arbitrary Borel W-actions without the height hypothesis.

The independent proof record checks the full mechanism and its quantifiers:

- Finite-factor constraints are clopen, and the finite-valued continuous maps
  form a countable family. The fiber product has an exact action. Its nonempty
  clopen atoms are finite unions of Cantor copies, allowing an atom-preserving
  homeomorphism. Refinement by all tested inverse-image partitions and a
  symmetric finite controlling set handles every constrained group coordinate
  and inverse. Refining the old factor fibers preserves the prescribed reduction.
- Every later-selected factor is already in the fixed countable obligation
  family. Recursion along factorial moduli therefore produces a coherent
  continuous equivariant inverse-limit height. Compactness proves surjectivity;
  no measurable selection across actions is needed.
- Prescribed residues give a Borel coordinate bijection even with nonfaithful
  lamp actions. The correct conjugation is `t^(-r) a t^r = a_(-r)`. Finite-degree
  partial-move graphs give proper Borel extended metrics. A fixed palette per
  width works at every scale. Threshold chains project into a single base color
  component without requiring their connecting paths to have that color.
  Cardinality at most `m C_R` gives diameter at most `R(m C_R - 1)`.
- Divisibility gives literal graph nesting and next-distance control by the old
  distance. Dimensions may vary by stage. On the invariant noninteger-height
  piece, every edge eventually appears, and a finite word fits in one late slab.
  The only permanently omitted forward edge starts at height -1, which belongs
  to the exceptional integer-height saturation.
- The entire exceptional preimage can be uncountable. Integer normalization
  gives the lamp orbit test in both directions. A base point has exactly one
  lift at each integer height; cutting the pulled-back finite relation to
  `|h| <= j` makes its classes finite. These banded relations are Borel,
  increasing, and exhaustive. Combining both invariant pieces finishes the
  whole-space proof.

Falsification checks included empty/nononto residue maps, width one, equal lift
moduli, inverse topology, periodic shifts, trivial/repeated lamp images,
arbitrary stabilizers, the reversed conjugation sign, wrap edges, colored paths
with differently colored interiors, unbounded stage dimensions, deletion of only
one exceptional fiber, negative heights, and unbanded infinite-to-one pullbacks.
None leaves an unsupported step. There is no amenability shortcut or general
increasing-union closure for hyperfinite relations.

The exact [CJMST manuscript](https://math.berkeley.edu/~marks/papers/polycyclic_v13.pdf)
inputs were directly inspected: Lemmas 2.2/3.1, Definition 3.2 and its following
Borel characterization, Corollary 5.5, the full Theorem 7.3 statement/proof, and
Corollary 7.5. Corollaries 5.5/7.5 explicitly allow any Borel action; Theorem 7.3
allows separate finite dimensions. The different free-action main theorem was
not substituted. These are deep imported results, checked for exact applicability
and credited, rather than independently reproved or certified by the programs.
The primary author block supports the B. M. Seward attribution.

## Attribution and bounded priority

The note, metadata, README and priority summary give appropriate predecessor
credit. I directly read the relevant primary statements:

- [AGW, 2008](https://doi.org/10.1090/S0002-9947-08-04450-4), Theorem 3.3 and
  equation (3.7), plus the adding-machine factor paragraph, supplies the earlier
  conditional compatible-lift structure for single homeomorphisms.
- [Doucha v3](https://arxiv.org/abs/2211.08145v3), Proposition 2.12(3) and its
  perturbation proof, supplies the all-group extension mechanism. Live arXiv
  metadata confirms the cited March 8, 2024 version.
- [DMT v1](https://arxiv.org/abs/2507.05474v1), Proposition 3.2, Definition A.3,
  Proposition A.7, supplies all-action admissible Boolean coding and generic
  existential closure. The present finite partition equations are an explicit
  specialization, with consistency furnished by the fiber product. This was
  already in July 2025 v1; live metadata confirms the April 2026 v2 revision.
- [Iyer–Shinko](https://ems.press/journals/ggd/articles/14298740?na) is correctly
  credited as a 2025 published online-first GGD paper, DOI 10.4171/GGD/896.
  The inspected v1 introduction, LCL transfer, and Theorems 18–19 retain the
  local finite-asymptotic-dimension hypothesis. W itself is finitely generated
  and contains undistorted Z^d lamp windows of arbitrarily high rank, so this
  baseline does not directly settle the target.

The potentially additional deduction presented here is the slab-compatible
metric union plus the full exceptional exhaustion. No worldwide novelty of
that combination is certified. The package correctly answers a historically
posed question without claiming first proof or worldwide current openness.

I checked the priority audit's harder GMRS composition issue directly against
[GMRS v1](https://arxiv.org/abs/2608.22565v1), its two-parameter definition,
Theorem C/4.7, and Conjecture F(2), and against the DS v4 Theorem 6.12/Corollary
6.13 and Davila Chapter 4 formulas. Even granting the advertised/repaired
ordinary bound and lossless generic LCL transfer, W has O(s) colors at
O(s^3) diameter from those formulas, giving `(a,b)=(3,1)` rather than the proved
criterion `a b <= 1/4`. The older multiplicity/Lebesgue-number quantity does not
supply this colored diameter control. The single-variable subexponential
implication remains a conjecture. This excludes an immediate implication from
these inspected bounds; it is not a lower bound or an impossibility result for
all other applications.

Direct primary comparisons also confirm the recorded boundaries of the newer
commutative-monoid results (commutativity), Naryshkin–Vaccaro (treeability),
Thornton's generic corollary (finite asymptotic dimension), and almost-finiteness
results (finite partitions need not be increasing). The groupoid manuscript
expressly disclaims the needed Borel hyperfiniteness consequence. Fresh targeted
searches supplied no exact earlier full resolution in the returned evidence;
search summaries were treated as leads rather than theorem authority.

Inspection scopes and actual primary PDF hashes are in `SOURCE_INSPECTIONS.json`.
Existing ignored sibling primary copies were read; no fresh PDF download is
claimed. Live publisher/version metadata was separately checked. The inaccessible
final Iyer–Shinko publisher PDF and CJMST publisher bot response remain disclosed
limits in the archived audit. Bounded corpus inspection is suitable for the
qualified preprint framing and is not worldwide priority certification.

## Archive, code, reproduction and prepared repository

All executable verifier/diagnostic/integrity code was read before executing it.
Its enforcement uses runtime conditions, survives optimization, binds source
before running it, and does not rely on bytecode caches. All replay and mutation
copies were confined to this review's ignored `private_sources/` directory,
including child integrity-suite temporaries through TMPDIR.

`review_checks.py` independently established:

- Exactly 121 unique, safe regular ZIP members, valid CRCs, a closed index, all
  indexed bytes/hashes, no duplicate JSON keys, and exact current paper/metadata
  correspondence. No downloaded primary content is distributed.
- All 61 original publication-freeze files equal their SHA-256/byte/Git-blob
  records and `git show` at the exact frozen head. Full replay verifies all
  three original ZIPs and their 51 extracted members. The historical author,
  reviews, results, and status labels are unchanged and accurately framed as
  dated history by current wrappers.
- Full inner verification from a relocated path containing spaces, working
  directory `/`, isolated/no-bytecode Python, normal and optimized modes, passed
  with identical stdout. All 68 historical integrity rejections and current slab
  evidence reproduced. Sixteen further rejections cover a wrong external pin,
  tampered note, missing/extra files, empty/cache directories, symlink and FIFO.
- The corrected outer assembly has a closed 192-file inventory pinned by
  `f1b7993fd3c2a056da0e97e38711d30f194a481c8ed29c9b50ffea954d5e8fd7`.
  Full outer normal/optimized replay also passed identically, with its inner
  result equal to the independent archive replay and no generated source cache.
- All 192 prepared mapping entries are unique and confined to the numeric
  target prefix. Their local bytes equal commit
  `9fed4b0d038281cd4145fdc40dbc3a8a86618b99`. Its target tree is closed, its
  change set against its specified main base is confined to the target plus the
  queue, and every non-target QUEUE byte is preserved.

After the root supplied newer local preview
`8f1b80939c574bcb70b7094edc43a86a55e1a28e`, I independently checked that its
target subtree has the same OID `10b95122c72fb715d21fb5567d95959c39e95ec0` and no
target diff from the preceding preview; the updated mapping and non-target queue
preservation also pass against its newer stated base. This check transfers the
byte-bound review to identical target material, without approving unrelated
base work. Neither preview was pushed by this reviewer. The unused earlier r1
assembly was not used.

The preprint builder also ran in a disposable reconstructed input tree and
reproduced the **exact ZIP and index bytes**, as recorded in
`DETERMINISTIC_REBUILD.json`. These checks establish artifact identity and finite
software behavior. They do not prove the infinite theorem, Baire category,
imported source theorems, or novelty. Manifests are integrity bindings, not
signatures; the documented independently trusted digest requirement is correct.

## PDF and metadata readiness

I freshly rendered and visually inspected all five supplied PDF pages. The
title/author/date/ORCID, mathematical symbols, equations, theorem statements,
proof transitions, citations, links and references are legible, with no clipping,
overlap, missing glyph, unresolved citation, or placeholder. The short final
reference page is acceptable. A clean disposable TeX rebuild succeeds without
warnings and yields exactly the same complete five-page layout text;
`PDF_SOURCE_IDENTITY.json` records the digest. PDF binary identity across
recompilation is not asserted.

Standalone metadata equals the upload manifest's metadata object exactly and
is identical inside the archive and repository package. Title, author/ORCID,
date/version, affiliation, preprint classification, license/access, exact whole-
space theorem scope, bibliography, and predecessor attribution agree with the
paper. Both named upload files exist and are sealed. No fabricated DOI or
journal acceptance is claimed. AI use is disclosed extensively; the note is
unrefereed and claims no completed external human review or proof-assistant
verification. CC BY 4.0 applies to authored material, while cited primary sources
retain their terms and are excluded.

## Final binding and limits

`DECISION.json` contains all ten **actual rechecked** core hashes, the outer pin,
the exact reviewed target/head, the prepared target-tree identity, and this
report's hash. The two fresh final-review outcomes agree, but this decision is
based on the independent proof record and fresh checks described above.

No required repairs or unresolved in-scope concerns remain. The package is ready
for its stated unrefereed preprint workflow within this review's scope. This
receipt performs or authorizes no service mutation by the reviewer. External
human assessment could add independent scrutiny; no outreach was prepared or
initiated. Imported-theorem reliance, manual AI review, finite tests, and bounded
priority inspection remain explicit limits, not formal verification or worldwide
firstness certification.

**Assigned review completion: 100%.** This is a workflow estimate, not a numerical
probability of theorem correctness or historical novelty.
