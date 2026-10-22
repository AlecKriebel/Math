# PR1337: bounded diagnostic repair, preparation 02

The nonblocking diagnostic improvement from the first fresh whole-package
review is implemented. The four-page paper and its TeX source are byte-identical
to preparation01. The new edition changes only the checker diagnostic and
its expected output, documentation/provenance, control count in matching
metadata/deposit proposal, and affected manifests/archives.

The preparer read the complete first review REPORT and MINOR_DIAGNOSTIC.json.
Its PASS applies to preparation01, seal
08f11bcaf7dc4b45de2341b1de2fa8e7d8af8eedbdf411e2ef32c5d5df7896db.
The review itself is closed under seal
97cecc4e842aca5be7a20369092f90d0c6c75bf17eecf8c13dcbdbb59261586c.
This repair is author QA, not a second independent whole-package review.
Root will assign a fresh second reviewer to the new closed edition.
Publication readiness remains false. Overall research estimate remains80%.

## Exact repair

The old control `not any([1]*4)` was a constant observation. It could not
detect a regression in the constructed quotient. The existing raw monomial
relation presentation and integral unit-pivot reducer now also support degree
one. Since the actual generators have degrees two and three, that homogeneous
layer has no relations. Its coordinates are obtained through the same reducer,
rather than supplied as the control's constant vector.

The new `sum_y_witness` sums the actual coordinates of the y-generators and
then multiplies the derived vector by every x/y generator using the actual
quadratic quotient. It checks each x-product against (n-1)v_i, checks each
y-product is zero, and verifies x-products are nonzero precisely when
p does not divide n-1. It is tested at (n,p)=(3,2) and (4,2). At width3,
p divides n-1, the degree-one vector is nonzero and all products vanish.
At width4, p divides n, the vector is still nonzero and each x-product is
nonzero. Thus scalar n is not confused with the degree-one sum.

A thirteenth false control deliberately adds the incorrect relation
sum(y)=0 to the degree-one presentation. The diagnostic rejects that corrupted
linear layer before trusting multiplication. This is a targeted zero-sum
regression test, not an assertion that the corrupted layer describes the
original algebra. The original constant control is replaced by an observation
of the actual quotient-derived witness. DIAGNOSTIC_CHANGE.patch gives the
complete checker diff. Other finite case ranges and the universal proof are
unchanged; no broader matrices or research scope were added.

## Verification and packaging

Normal/-O/-OO checker outputs agree exactly, SHA256
dbf116e2ad1d77a0fb7dad2968ff972cab4bd61471a4ebd30270a3b345f2c58b.
All earlier finite cases remain: widths1–7,72 integer general-form cases,
2170 exhaustive finite-field forms,872 injections,and width-three generation
through6. The expected output now includes both explicit sum-y witnesses and
thirteen rejected false controls. The source reproduction validator runs all
three modes and passes.

Exactly seven of eighteen scientific source members change:
verification/exact_checks.py, verification/EXPECTED.json, CODE_PROVENANCE.json,
README.md, zenodo-metadata.json, zenodo-deposit.json, and PUBLIC_MANIFEST.json.
The other eleven are byte-identical, including main.tex, paper.pdf,
BUILD_RECEIPT.json and PDF_VISUAL_QA.json. The original four-page inspection and
compilation evidence is carried unchanged; no new PDF or compiler run was
needed or claimed. Paper version1.0.0 and date22October2026 remain unchanged
because this is an unpublished internal preparation repair.

All eighteen source ZIP members and all five upload-kit members were read back
and compared with the new source/release bytes. A fresh extraction rebuilt all
six release files byte-identically. The PDF remains SHA256
0885cf6a89f82e819666b379ce04783351bbde54a9362375022851683030960b.
ROUNDTRIP_RECEIPT.json records complete member and release hashes.
SCIENTIFIC_CHANGESET.json records every changed and unchanged source hash.

The original priority/duplicate evidence is retained by immutable reference
to preparation01 and the first fresh review; this bounded code repair makes no
new literature, novelty, firstness, openness, or duplicate-absence claim.
No source author/claimant mathematical code was executed. No new independent
review is credited to this preparer. All-phase AI, unrefereed status, author,
ORCID, CC BY prose/MIT code and scientific-scope disclosures remain intact.

## Preservation and limits

All writes stayed in publication_preparation_02. Unchanged source members were
copied with native clonefile, independent inodes and nlink1; no hard links.
Preparation01 and review01 were verified against their closed seals, then all
188 old files, including both seals, were compared by bytes, hashes, modes and
nanosecond mtime at final closure. Every old byte remains unchanged.
No cache, toolchain, Git/index/ref, STATE, service, provider, row, approval,
publication, merge, release, or DOI action was performed. There was no outside
person or unrelated-agent contact. The new packet is below4MiB and guarded
writes preserve the150MiB available-space reserve.

The next required action is root's fresh independent second whole-package
review of this exact sealed preparation02 edition, followed by root adoption
or any further repairs. This report conveys no publication authority.
