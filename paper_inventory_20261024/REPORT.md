# Complete paper inventory and editorial assessment

24 October 2026. Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X.

## Delivered inventory

The existing [Full List tab](https://docs.google.com/spreadsheets/d/1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20/edit?gid=1052646184#gid=1052646184) contains 244 manuscript entries, grouped into 229 scientific paper lines after explicit version and consolidation judgments. This is not a count of 229 independently new discoveries or peer-reviewed publications.

The inventory includes all 202 standalone Zenodo manuscript records, 40 individually identifiable manuscripts within published Zenodo repository archives, and two verified public repository papers with no Zenodo match. The archived manuscripts include a withdrawn JC cleanup draft; its surviving local identity receives a score of 2, while its rejected main theorem is explicitly excluded from that score. Older presentation copies and precursor manuscripts remain visible.

All 226 owned records were accounted for, including software/source deposits and one unpublished empty draft. Fully paginated public ORCID/name searches recovered exactly the same 225 published owned records, with no additional author/coauthor records surfaced. All 211 direct manuscript PDFs matched their published checksums and sizes. Every one of 276 distinct PDF payloads in the 20 relevant ZIP releases received a disposition, including historical editions, supports, figures, literature and the withdrawn manuscript. All 17 direct/archive duplicate payloads were independently checked by MD5 and SHA-256.

Large ZIP members were acquired by byte ranges and checked against their central-directory CRC32 and size, then SHA-256 hashed. Whole-ZIP advertised MD5 was not recomputed for those large archives; the inventory does not claim otherwise. Both non-ZIP source/certificate tar archives were fully hash-checked and contained no further PDFs. All 30 canonical supplemental website PDFs were fetched and matched to the scoring copies.

Each row provides conditional impact, added contribution, journal assessment, plain-English result, score rationale, surprise, boundaries, DOI/source link, publication date or edition qualification, authors, review depth, dependency limits, next step, source-member locator, work group and PDF SHA-256. Source links for embedded papers are expressly labelled shared archive references, not paper-specific DOIs.

## What the scores mean

Conditional impact follows the user's existing rubric: assuming correctness, genuine novelty and publication, how important is the stated result in its actual subfield? Added contribution uses the same importance scale after crediting imported results and established reductions. Neither is a correctness probability, citation count or measured reception score. Typical editorial calibration uncertainty is roughly half a point to one point.

Several conclusion-level scores of 8–9 depend on credited external breakthroughs. They must not be presented as the author's independent solutions of those upstream problems. In particular, sparse finite-field factorization is recommended for its added sparse oracle reduction; its uniformly deterministic dense implementation remains dependent on the external input.

Review depth is recorded individually. Most entries received targeted manuscript triage of exact claims, proof architecture, attribution and limits, supported where appropriate by previous checksum-bound reviews. Selected candidates received deeper independent reading and exact replay. This is not a new complete proof audit of every manuscript or an exhaustive contemporary novelty search. Internal AI review is not independent human refereeing or journal acceptance.

## Most surprising result

My selection is [Free spanning-forest degree can decrease under squaring](https://doi.org/10.5281/zenodo.23575190), conditional impact **7/10**. In the specified infinite vertex-transitive grandparent graph, adding every distance-two edge raises the available graph degree from 8 to 40 but lowers the expected degree in the free uniform spanning forest from `(24-sqrt(2))/7 = 3.2265409…` to at most `3.208526010913748780`.

Fresh independent verification regenerated the finite graph and all 40 root neighbors and checked all 797,240 integer currents, 122,800 divergence equations and the exact total energy. Separate exact network elimination checked the finite reductions, and both written free-exhaustion arguments were challenged. No substantive gap was found in that bounded audit. The headline is about this infinite free-boundary forest on a nonunimodular graph, not finite uniform spanning trees or a counterexample in the unimodular/Cayley subclass. Bibliographic firstness is not certified.

## Publication judgment

The 244 row-level recommendations are: **60 strong submission candidates, 83 specialist submission candidates, 77 technical notes or papers to merge, eight holds for specific dependency/proof/overlap review, 15 superseded editions, and one withdrawn manuscript.** These classify whether a submission campaign is worthwhile; they do not promise acceptance or readiness to publish unchanged. Credentials and AI assistance are not automatic score deductions.

A manageable first group, chosen for identifiable added contributions and checkable mechanisms:

| Paper | Conditional impact | Why prioritize it |
|---|---:|---|
| [Free spanning-forest degree can decrease under squaring](https://doi.org/10.5281/zenodo.23575190) | 7 | Short explicit counterexample with an exact independently replayed certificate and carefully separated infinite proof. |
| [Nonconvexity of fixed odd-power sum-of-squares cones](https://doi.org/10.5281/zenodo.23191301) | 7 | Clear general theorem and a substantive disjoint-copy obstruction; the explicit cube example is high-dimensional, not a small-dimensional witness. |
| [Three anti-invariant classes on a nonintegrable four-manifold](https://doi.org/10.5281/zenodo.23422055) | 7 | Concise explicit geometric construction preserving three cohomology classes while producing nonintegrability. Exact conjecture scope and earlier examples still merit specialist comparison. |
| [An explicit odd-order p-group with as many automorphisms as elements](https://doi.org/10.5281/zenodo.22770864) | 7.5 | A concrete named existence target with substantial lattice/Lie machinery and exact infrastructure. Full automorphism and log/exp arguments need specialist scrutiny beyond the matrix certificate. |
| [Minimum Bell-Setting Complexity for Qubit POVM–PVM Separation](https://doi.org/10.5281/zenodo.21699161) | 7.5 | A clean architecture-minimum question with potential quantum-foundations interest. Align the public v1.1 manuscript with the newer local formalized endpoints; do not describe every manuscript step as formally verified. |
| [Output-sensitive sparse factorization over finite fields from dense factorization](https://doi.org/10.5281/zenodo.23205034) | 7 | Substantive sparse descent invariant. Lead with the oracle reduction and distinguish the externally dependent derandomization corollary. |

The full sheet makes the same judgment for every other paper. The highest conditional theorem score alone is not the best submission-priority rule.

## Verification and evidence

All 6,500 cells in `Full List!A1:Z250` were read back and compared exactly with the prepared values. The header was visually checked in Google Sheets, its clipped labels repaired, and the filter and six frozen header rows verified. The existing Papers, Math Puzzles and Impact Scoring values remained identical. Other tabs were outside every mutation request.

Machine-readable inventory and source provenance are in `outputs/inventory.json`, `outputs/inventory.csv`, and `outputs/source_manifest.json`. Independent coverage, per-entry integrity, calibration and finalist-falsification reports are under `reviews/`. Private tracker/account snapshots and extracted source texts remain local. No individual was contacted, no submission was made, and no GitHub release or DOI was created.
