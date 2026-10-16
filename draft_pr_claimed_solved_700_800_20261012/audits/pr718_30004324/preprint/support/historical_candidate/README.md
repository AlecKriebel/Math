# Tangent-bundle Seshadri characterization: complete candidate

Problem **30004324 / OWR-17296-007**, rank 746. Queue label: **claimed_solved, 2/5**, meaning a checked complete **candidate only**.

Read the [expanded v2 proof](tangent_seshadri_30004324_v2/candidate_proof.md), the [first geometry audit](tangent_seshadri_30004324_v2/review/first_geometry_audit.md), the [second geometry audit](tangent_seshadri_30004324_v2/review/second_geometry_audit.md), and the separate [final delta acceptance](tangent_seshadri_30004324_v2_delta_acceptance/DELTA_ACCEPTANCE.md).

## Claim and review scope

Let X be a smooth integral projective variety of dimension n at least one over an algebraically closed field of arbitrary characteristic. Positivity of the tangent-bundle Seshadri constant at **one arbitrary closed point** is claimed to imply that X is projective n-space. No characteristic-zero, general-point, pre-existing Fano, global-nefness, or separability hypothesis is added.

The proof uses an absolute minimum of ample degree among rational curves through the fixed point. Its one-marked stable-map family has no boundary; every relevant normalization through that point is very free. The inertia-free actual evaluation fiber is proper and quasi-finite over the full projective coarse scheme and thus projective. Its universal P1-family has a genuine contracted marking, and evaluation is surjective. Fiberwise degree-zero line-bundle descent yields Picard number one, then Fano; the established Fano clause of Fulger–Murayama Proposition 4.8(1) supplies the final characterization.

Two independent AI geometry audits found no essential gap. A later independent delta audit accepted the exact expanded proof and strict tooling. These are candidate-level checks, not external human peer review, formal proof verification, an accepted resolution, or a certification of novelty. Specialist review and historical-priority verification remain outstanding. Imported foundations are explicit, and the complete Kollár monograph proof was not independently retrieved. The finite controls do not prove the geometry.

## Immutable history and governing status

Both original and v2 ZIPs are preserved byte for byte. The original proof and its full thirteen-file tree are in the author ZIP. The exact v1-to-v2 patch and machine delta are retained. All 27 v2 files are also directly readable.

The v2 freeze still says that delta review is pending. Those strings are historical and unchanged. The separately pinned final acceptance governs the exact accepted v2 bytes; no old report has been silently rewritten or promoted to cover changed bytes.

The original manifest verifier received **REVISE_REQUIRED** for accepting an extra nested MANIFEST.json. The actual original archive had no such extra file. The v2 strict verifier controls; the vulnerable historical implementation exists only for regression demonstration. The original adverse finding remains visible.

Both full geometry reports and source metadata are already verbatim inside v2. `AUDIT_LAYOUTS.json`, the original independent manifests, and the remaining supplemental files reconstruct the exact original audit packages without repeating those reports.

## Replay

Run `python3 verify_publication.py` or `python3 -O verify_publication.py` from any working directory. Python 3 standard library and the system `patch` command are required. The verifier checks the closed publication inventory, externally hardcoded freeze pins, both ZIPs, every reconstructed audit file, strict manifest checks, 909,136 author finite controls, 85,247 independent finite controls, 14 strict mutation controls, the historical bypass regression, exact delta regeneration, zero-fuzz patch reconstruction, and relocated normal/optimized replays. It propagates optimization to child processes and checks their outputs explicitly.

Optionally pass the expected PUBLICATION_MANIFEST.json SHA-256 as the sole argument for an external top-level binding. Computation is integrity and finite regression evidence only.

Only authored proof/code/review text and public bibliographic/integrity metadata are included. Source PDFs, source text extracts, raw datasets, private sources, and private coordination records are excluded. The queue patch changes only the target row's Status, Turns, and Findings, preserving Chat, DOI, all other bytes, and its stale embedded header. No release, DOI, merge, or external outreach is part of this publication.
