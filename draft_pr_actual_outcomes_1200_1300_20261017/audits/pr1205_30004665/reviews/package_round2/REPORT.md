# PR1205 / problem30004665: second fresh whole-package adversarial review

Completed 2026-10-17, approximately 17:11 UTC. Completion estimate: **100% of
this assigned package review**. This reviewer knew the candidate and makes no
blind-discovery claim. Earlier round1 conclusions were read only after the
fresh mathematical reconstruction and exact mathematical checks described
below.

## Disposition

**CLEAN for the expressly attributed corrective/verification preprint.**
No mathematical, publication, priority-framing, or provenance-disclosure
blocker remains in the exact PDF/ZIP bytes bound below. There are no actionable
P0, P1, or P2 findings from this round. This is not clearance for a first
discovery claim, a currently-open-problem claim, or a novel-full-solution claim.

The strongest verified result is an explicit counterexample to the necessity
direction of the literal canonical-W exponent converse on Schumann's OWR2021
p.1125. It uses the designated reduced-word canonical chart, not an arbitrary
monomial change chosen to manufacture an exponent. The later varsigma and
coefficient conjectures are not refuted. The established old support and
minuscule results are substantive prior work and are correctly credited.

## Exact artifact binding

| Artifact | Bytes | SHA256 |
|---|---:|---|
| Canonical_W_D4_Note_v1.0.pdf | 77127 | `1edcf5f41308f1369f45dde8aa75111b69d73c56a5a1cdf6724f636ee2d9dcb1` |
| Canonical_W_D4_Verification_v1.0.zip | 63134 | `f5ccf88733160c457423613fa1e0e329a562a29bad15bd71ed118114e9b98eef` |
| manuscript/main.tex | 15136 | `d15c70dcc7ee0744a6ea34cd72049abacddebb43dd7034becd8d6fa153d86c22` |

Initial and final hashes agree exactly, including BUILD_RECEIPT.json
(`1afca2dc6b363b112423871b883b4bcf223c70c112b1e28055d5d42542ca84dd`)
and zenodo-deposit.json
(`8a37c0fd4b15743b17a7e4d17ef61eb51847eb24b0b75a23e23fceeac0398f2e`).
The build receipt's PDF/ZIP sizes and digests, manuscript digest, manifest
digest, and 26-member count all match the actual bytes. Every one of the 25
manifest-bound archive members has the stated size/hash and is byte-identical
to its publication/verification counterpart. The manifest plus those members
are exactly the ZIP member set; no duplicate, escaping, unexpected, source-PDF,
third-party program, original dataset, or environment member is present.
The archived manuscript equals the publication manuscript. The compile
receipt also binds that same source and PDF. I did not recompile the TeX in
this round; all five final PDF pages were independently rendered and checked
against the manuscript.

## Fresh mathematical checks

I first read the full manuscript and the relevant primary-source definitions,
then wrote a separate non-blinded implementation, independent_math.py. It
imports no candidate or earlier-review code. The implementation was executed
with installed SymPy1.14.0 and bytecode writes disabled before the parent
removed that disposable environment to relieve disk exhaustion.

Its mechanisms differ materially from the package's primary verifier:

- It realizes D4 explicitly as the Euclidean roots +-e_i+-e_j, with simple
  roots e1-e2, e2-e3, e3-e4, e3+e4. Direct reflection matrices give the twelve
  displayed positive inversion roots and product -I4.
- It builds the seed from the next-occurrence and Dynkin rules and mutates
  positive arrow multisets by oriented two-path creation, reversal and
  two-cycle cancellation. It obtains precisely the stated 16 arrows and
  frozen positions 7,9,11,12.
- It evolves all X coordinates **forward** as exact rational functions using
  KS equation(3), rather than using the package's reverse sparse y-polynomial
  engine. All four supplied routes are mutable-only, and each final frozen
  row has exactly b[f,10]=-1. Inverting the actual final frozen coordinate
  gives summand counts14,5,2,1 and every coefficient1.
- It parses all22 exponent/separator rows directly from the actual TeX table.
  The complete forward reconstruction equals that table and a separately
  expanded compact formula. In particular the only y6-squared rows are21,22,
  giving canonical X6 exponent-2.
- It independently multiplies all484 displayed table pairings: diagonal-1,
  off-diagonal nonnegative. Every a.u=1 for the displayed frozen-marker u.
  Thus u is strict interior and each z_j+u lies on exactly its selected
  hyperplane while strictly satisfying every other inequality. The local
  hyperplane-neighborhood argument gives dimension11 for every facet and
  dimension12 for the cone. Distinctness is certified without an LP solver.
- It computes the Cartan matrix as the Euclidean Gram matrix, builds K, and
  verifies det(K)=1, aK in {-1,0,1}^12 for all22 rows, and both explicitly
  displayed transformed rows21,22. The support rank is12.

The initial detailed JSON write failed because the shared disk was full;
the complete PASS output is in the tool record. The exact executed source was
retained after space returned. I do not represent a nonexistent detailed JSON
file as evidence. Subsequent standard-library evidence files were written
successfully.

displayed_intermediate_checks.py additionally compares all five written
reverse-pullback stages, after steps4,3,1,6,2, to literal polynomial expansions.
They agree exactly, with term counts5,8,9,11,14. This additional comparison uses
the distributed sparse arithmetic engine, not another independent engine;
the separate forward-X reconstruction above independently supports its final
answer.

I also wrote graph_and_third_certificates.py, with no candidate-code imports.
It independently enumerates all2316 reduced words and12504 directed braid or
commutation edges, checks arrow/frozen-set transport by positive-arrow
mutation, and verifies all150048 chamber-coordinate identities by exact
monomial/binomial signatures. The positive string-braid lift is
(u,v,w)->(vw/(uw+v),uw,(uw+v)/w). This directly checks compatibility of the
canonical source convention, chamber map, and later string convention.

That script independently rechecks the source-only family's additional22
exclusive-violation and relative-interior facet certificates:968 integer
pairings and the strict interior, with exact support equality to the original
tables after the stated X/y sign change. These are additional checkable
certificates, not reliance on a solver's feasibility declaration.

## Exact extracted replay and falsification

I independently extracted the frozen ZIP into this review's extracted/.
The actual unmodified primary verifier passes normal Python, -O and -OO.
Each result is byte-identical to expected_results.json, SHA256
`ed99482136e58761f0df9ad6f59e3fa3a57ef0b1053e10326c1c3ea8de0f27a1`.
All30 built-in negative controls remain active in all three modes.

replay_and_controls.py changes actual review-local extracted inputs and code,
invokes the checker under each of those three modes, and restores the exact
original bytes. All36 external corruption runs fail appropriately. The twelve
families change the squared exponent, zero a primary separator, alter an
independent support row, zero an independent separator, alter word metadata,
omit a row, duplicate a row, reverse a separator sign, remove inclined-edge
Dynkin adjacency, truncate an optimizing route, transpose the mutation sign,
and double one claimed coefficient. The final pristine rerun again gives the
expected digest. No publication file was changed.

I did not replay the distributed optional SymPy implementations in this round:
the installed environment was removed after my own symbolic reconstruction,
as coordinated to recover disk space. I inspected their exact distributed
code and immutable data; the parent's optional replay receipts are inherited
evidence, explicitly not my own executions. The primary replay, fresh
forward-X execution, complete graph check and all integer certificate checks
above are my own executions.

## Primary sources, old data and precise scope

I read the cached primary OWR pp.1123-1125, KS2022 equation(3), Definitions7-9,
Proposition5, multiplicity-free definition/Conjecture3, Theorem2 proof and
minuscule theorem, and GKS section4.2.2. I visually reopened OWR printedp.1125
and the KS Definition9 and Theorem2-proof pages from the actual source PDFs.

OWR's converse really refers to coordinate exponents of W on its designated
dual torus. KS defines W_f as the inverse frozen coordinate in an optimized
seed, with all adjacent mutable arrows entering that frozen vertex. Its
mutation sign converts to exactly the displayed reciprocal-y rule. GKS
explicitly provides the Dynkin-adjacency qualification omitted from the
abbreviated literal KS quiver display; the note attributes it correctly.
The chamber pullback exponent matrix for X is -K; hence y=X^-1 has K as in
the manuscript. Exponent bounds can change under this unimodular map, while
inequality irredundancy is preserved. Our example disproves the stated
equivalence in the affected Theorem2 proof step, without disproving that
theorem's conclusion or providing a general repair. The proof in this note
does not invoke the affected assertion.

prior_and_provenance.py independently decompresses the cached original
primary-author data and parses Case267 as inert AST syntax; it executes no
source-author code. The word agrees, and all22 historical string-support rows
agree exactly, separately by simple root in sizes14,1,5,2, with the freshly
checked chamber image. Compressed source SHA256 is
`b7022bbc90d285f7827b7146254e91359639af6c2c38ef71a68db7098084119b`.
I also inspected the cached Git-history records and the original 2022
Koshevoy-Mironov preprint's explicit repository reference. Git dates remain
repository provenance, not independently certified dates of public access.

The earlier support computation, and published minuscule nonredundancy for
the three leaf summands, are substantial prior overlap. The current abstract,
priority section, README, and Zenodo metadata accurately credit it and disclaim
firstness, first resolution, present openness and exhaustive literature
coverage. A narrowly attributed coordinate correction with independent exact
certificates is defensible. I did not repeat the earlier families' entire
literature survey, establish absence of an earlier explicit correction, or
exclude inaccessible/unindexed work. Those limits are disclosed and do not
invalidate this stated contribution.

## First-round provenance blocker: resolved without retroactive upgrade

Only after the independent mathematical work did I inspect round1's report
and the correction. I checked the revised manuscript/PDF, README, archive
chronology document, historical mutation-review wrapper, replay programs,
original-family marker, new source-only-family report/receipt, and root log.

The revised current package explicitly says that the earlier mutation family
inherited candidate-containing context and was **not blinded**. Its separate
implementation and local freeze before file comparison are not sold as
blindness. Historical text is preserved under a conspicuous correction.
Ordinary reconstruct.py replay writes a neutral OUTPUT_DIGEST.txt and no
longer generates a historical-sounding freeze marker.

The later source-only family is separate. Its original and packaged initial
receipt are byte-identical, SHA256
`af766d1da012b3358d7aedd1955cd27aaa61cba6f2ac60a52b0f837440de8553`.
Its initial frozen support remains
`7881d1d0ef80ff7ca036f16a06d2d7f23cb666bab223500226d6cded3f66a30d`,
distinct from the earlier family's
`fc5a5208035b011683168d1114af93c613de4f001e19ab49ce70a464e0b0d459`.
All nine checked packaged receipt/report/code/data files match that family's
original files exactly. Its log records an initial16:49UTC freeze, a16:54:33Z
receipt after parent acknowledgment, and continued noninspection; the root
comparison is separately dated17:01:08Z. The chronology is consistent and the
reviewer-versus-parent comparison scopes are accurately separated.

The source-only replay reads and compares the historical freeze and does not
write the receipt/freeze; supplementary computations compare existing neutral
outputs or create them only when absent. I found no current replay that
manufactures an earlier initial chronology. The correction expressly labels
all this as internal AI research provenance, without externally certified
timestamps or external human peer review. I can verify preserved bytes and
code behavior; I cannot independently authenticate a past agent's awareness
or turn internal records into an external timestamp. The package does not
claim that stronger certification, so this is a disclosed limit rather than
an unresolved blocker.

## Presentation, metadata and additional acceptance draft

All five final PDF pages were freshly rendered at90dpi and visually inspected.
No clipping, overlap, missing glyph, broken equation or illegible table row was
found. The table continuation preserves all22 rows. The mutation table ends
above the footer with adequate separation. References, page numbers, date,
version and ORCID are readable. The manuscript and metadata agree on Alec
Kriebel, independent-researcher affiliation, ORCID0009-0001-9320-500X (checksum
also checked), version1.0 and17October2026. Five pages agrees with the deposit
description. No invented DOI or publication-completion assertion is present.

Extensive AI use, unrefereed status, absence of external human peer review and
absence of proof-assistant certification are conspicuous. CC-BY4.0 authored
text and separate MIT original code licensing are stated; the original
unlicensed dataset and downloaded third-party sources/programs are excluded.

At the parent's later request I also read publication/PR_ACCEPTANCE_DRAFT.md.
Its mathematical scope, old-data attribution, separate old/new review-family
descriptions, frozen PDF/ZIP hashes and pending-publication status are
consistent with this review. Retaining the original historical proof edition
while adding a clearly current corrected publication edition is compatible
with this scope; neither the old narrative nor this clearance should be
promoted into an unqualified firstness/blindness claim.

## Boundaries of this review

This is internal AI adversarial review, not external human peer review or a
proof-assistant certificate. No individuals were contacted. No publication,
PR, Zenodo, tracker, Git index/branch/commit, or original research artifact was
mutated. All review writes and intentional corruptions stayed in this review
folder. Main was checked at the start and end. Disk exhaustion initially
blocked even small writes; no files belonging to another effort were deleted.

Checkable local evidence: independent_math.py; replay_and_controls.py/json;
prior_and_provenance.py/json; graph_and_third_certificates.py/json;
displayed_intermediate_checks.py/json; initial_hashes.json; final_hashes.json;
the extracted archive and rendered final/source pages; and RESEARCH_LOG.md.
