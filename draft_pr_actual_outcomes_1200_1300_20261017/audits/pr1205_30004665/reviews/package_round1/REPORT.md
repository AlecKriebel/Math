# PR #1205: first complete-package adversarial review

Checkpoint: 17 October 2026, America/Los_Angeles. Assigned review completion:
100%. Publication clearance for the bytes reviewed: **withheld pending one
research-provenance disclosure correction**. No mathematical or priority-framing
objection was found to the narrowly attributed corrective note.

## Actionable finding

**P1 / publication blocker: the pre-candidate blindness narrative overstates the
independence of the earlier mutation family.** Manuscript `main.tex:290–292`
(and hence PDF p.5) says its SymPy reconstruction was frozen before inspection
of the submitted candidate; verification `README.md:45–47` makes the same
claim. The archived `reviews/mutation_review.md:9–25` and
`INDEPENDENT_FREEZE.txt` present a corresponding first-candidate-read narrative.
During this review, the parent documented that the original mutation reviewer
was created with a full-history fork containing the candidate. Its first local
read of submitted files may indeed have occurred after its output freeze, but
that fact does not establish blindness to the candidate in inherited context.
This reviewer cannot authenticate an earlier agent's mental state or first
awareness from a later output hash. The current prose invites a materially
stronger inference than the available provenance supports.

Exact repair: distinguish a separately implemented reconstruction from a blind
one throughout the manuscript/PDF, README, review wrapper, provenance marker,
and any repository/publication narrative relying on that chronology. Preserve
historical reports with a conspicuous correction rather than silently altering
the historical account. State that the earlier family could access candidate-
containing inherited context and froze its output before its first local read
of submitted proof files, so it is not evidence of blinded discovery. If the
parent's newly commissioned `fork_turns=none` family independently succeeds,
identify that distinct new family and accurately describe its input, frozen
artifacts, comparison time, and limits. Do not retroactively attribute that
stronger independence to the old family.

The portable `reconstruct.py:162–164` also regenerates a file literally saying
“Independent output frozen before candidate comparison” on every replay. A
replay cannot recreate the historical chronology. Change that generated marker
to a neutral output digest/receipt, or retain the historical marker as an
immutable annotated record and stop overwriting it during ordinary replay.
Rebuild the PDF/archive/manifests/receipts after the disclosure repair and have
the required different fresh reviewer assess the complete revised package.

This issue does not invalidate exact identities, finite certificates, or the
stronger independence of the standard-library and optional implementations as
separate programs. It does prevent unqualified readiness clearance for the
present package.

## Mathematical checks and falsification attempts

I read the entire manuscript, both mathematical-family reports, both priority
reports, root exact/source-scope evidence, priority adjudication, the portable
programs, certificate data, metadata, and archive manifest. This review knew
the proposed result before testing and makes no blind-discovery claim.

I freshly extracted the ZIP under this review folder. All 17 members are
accounted for, and all 16 manifest-bound members match their stated sizes and
SHA256 digests. PDF/ZIP/manuscript/manifest hashes match BUILD_RECEIPT.json.
The archive manuscript is byte-identical to the publication source. No source
PDFs, primary-author programs, original dataset, unexpected paths, duplicate
members, or local environment are in the archive.

The unmodified standard-library verifier passes under normal Python, -O, and
-OO, producing byte-identical results equal to expected_results.json:
SHA256 ed99482136e58761f0df9ad6f59e3fa3a57ef0b1053e10326c1c3ea8de0f27a1.
It verifies the reduced word, the 16-arrow seed, mutable-only optimizing routes,
actual frozen-coordinate normalization, exact polynomial pullback, 22 combined
unit-coefficient terms, the two squared terms, two independently supplied
certificate tables (968 scalar products), dimension/facets, and the unimodular
chamber map. Its 30 built-in corruptions are rejected in all three modes.

I additionally changed actual extracted certificate inputs and invoked the
unmodified checker under -OO. A changed word, clamped squared exponent, zeroed
separator, omitted support row, duplicated support row, and reversed independent
separator sign all produce failures at the appropriate mathematical gate.
These are external corruptions of its real input, not merely conditions encoded
inside the verifier.

A separate SymPy calculation in this review rebuilt the seed and mutation
matrices directly and used simultaneous symbolic substitution to rederive all
five displayed reverse-pullback stages of F7 (after steps 4,3,1,6,2). Every
written intermediate identity agrees exactly; no sampled point evaluation was
used for this check. I parsed every one of the 22 printed-source table rows,
confirmed equality with portable certificate data, and independently multiplied
all 484 table products. Diagonals are -1 and off-diagonals are nonnegative.
Every a.u=1 for the displayed u, so z_j+u is on precisely the selected supporting
hyperplane and strictly satisfies all other inequalities. The elementary
relative-neighborhood argument gives dimension 11 for each distinct facet;
strict feasibility gives cone dimension 12. This deduction has no dependence
on the affected general sufficient theorem.

The optional pinned SymPy programs run in a previously installed SymPy1.14.0
interpreter with bytecode writes disabled. Both braid-graph search orders
recover sizes14,1,5,2 in simple-root order and coefficient set{1}; their output,
original digest marker, and source-control output are byte-identical to the
archive. The published 27-term comparison, its coefficient2, and half-sum
relation reproduce. These are reproducibility checks; they do not independently
authenticate the original pre-candidate chronology.

## Source scope, priority, and repaired contribution

The historical target is real and correctly delimited. I reopened the primary
OWR PDF and published KS2022 source, read the relevant OWR pp.1123–1125 and
KS equation3/Definitions7–9/Proposition5/proof of Theorem2, and visually inspected
OWR printed p.1125. The original conjectural equivalence explicitly uses
canonical W in its designated dual reduced-word torus. KS defines the later
conjecture using the chamber pullback. The potential normalization and reciprocal
mutation equation agree with those sources. The adjacency qualification is
explicitly attributed to GKS rather than silently treating KS's abbreviated
quiver definition literally.

The note uses the specified canonical reduced-word coordinates. It does not
manufacture a large exponent through an arbitrary coordinate change. Its
upper-triangular chamber matrix has determinant1, transports the support by
a->aK, and sends all22 rows into {-1,0,1}^12. Its two displayed transformed
squared rows are correct. This is a counterexample to the historical canonical
necessity assertion, not to KS2022 Conjecture3, its coefficient conjecture, or
the stated sufficient theorem's conclusion. The paper explicitly admits that
it supplies no general repair for the affected theorem-proof step.

I independently parsed the cached primary-author Case267 dataset as inert AST
syntax and compared its complete support with the recomputed chamber image.
All22 rows match; simple-root counts are14,1,5,2. This confirms the positive
prior overlap. The root priority adjudication correctly blocks the claim that
this is a newly discovered example or a first resolution of a problem known
to remain open today. The current abstract, theorem context, priority section,
README and Zenodo description instead credit the earlier word/support and
minuscule nonredundancy results and reject first-priority/current-openness
claims. That is an honest, supportable corrective/verification-note framing.
No mathematical contribution should be promoted under the rejected stronger
novelty narrative in the final PR/repository/tracker records.

The remaining literature gap in the two priority reports is explicit earlier
recognition of this consequence in inaccessible or unindexed sources. This
review does not independently repeat their entire forward-citation survey or
close that gap. Because the paper expressly disclaims exhaustive coverage and
firstness, that bounded gap does not itself invalidate this attributed note.
I do not grant an unconditional novel-full-solution clearance.

## Preprint presentation and metadata

All five PDF pages were newly rendered and visually inspected. Equations,
continuation-table headings/rows, references, page numbers and fonts are
legible; no clipping, overlap, missing glyphs, or broken formula was found.
Five pages matches the metadata description. The PDF table matches the source
and portable data. There is no placeholder text or invented DOI.

Alec Kriebel's ORCID0009-0001-9320-500X, affiliation, version1.0, and17October2026
date agree between paper and Zenodo metadata. AI use, unrefereed status, absence
of external human peer review, and absence of proof-assistant certification are
clearly disclosed. The record's CC-BY4.0 manuscript license and the archive's
separate MIT code license are stated clearly; cited source materials are not
redistributed. DOI and source links identify the supporting publications and
exact historical dataset commit. No layout/metadata repair is required on the
reviewed bytes apart from rebuilding after the provenance wording correction.

## Bound artifacts and review limits

Reviewed PDF SHA256:
83abf5fc7902f3bddf06238c2560ea0f5b1fbd41de08a61776b4b27dfabbc394

Reviewed ZIP SHA256:
e01fa7409322dc92826f28757234485f401d79a71ad1a121af83581cb1aceaff

Checkable review evidence: replay.json, adversarial_controls.json,
formula_and_facet_checks.json, extracted/, rendered/ (the latter two are
review-local artifacts). No individual was contacted. No publication artifact,
PR, git index, branch, Zenodo record, or tracker was mutated. This review is an
internal AI audit, not external human peer review or formal verification.
