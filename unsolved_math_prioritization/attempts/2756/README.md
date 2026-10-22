# Kirby Problem 2.8: audited partial results

Problem **2756 / KP-2.8**, rank **908**. Canonical disposition: **unsolved**, **3/5** approaches used.

## Accepted result

For n >= 2, the planar tangle-stabilizer intersection K is the full preimage of the side-preserving spherical bridge Goeritz group G. The accepted exact sequence is

1 -> F_(2n-1) x Z -> K -> G -> 1.

Finite generation and finite presentation are each equivalent for K and G. Known n=2 and n=3 spherical results therefore yield planar finite presentability. For n=2, F3 x Z is an index-four kernel subgroup. Only the kernel extension is split to identify F_(2n-1) x Z; the whole K extension is not asserted to split and the n=2 unknot example cannot split.

The abstract intersection example shows that two finitely presented subgroups can have a non-finitely-generated intersection. It does not give a wicket-intersection counterexample.

**This work does not resolve the general n >= 4 question.** No all-n finiteness theorem, classification, counterexample or novelty certification is claimed. The reflected bar in the source formulation and the correct Distance-paper citation are already handled in the frozen original. The independent audit requires no new mathematical repair.

## Read the accepted work

- [Original proof](original_author/PROOF.md), [source report](original_author/REPORT.md), and [approach log](original_author/APPROACH_LOG.md)
- [Complete independent audit](independent_audit/AUDIT.md) and [exact acceptance](independent_audit/EXACT_ACCEPTANCE.json)
- [Source and full-corpus verification metadata](independent_audit/PIN_VERIFICATION.json)
- [Publication metadata](PUBLICATION_METADATA.json), [checks](PUBLICATION_TEST_RESULTS.json), [file inventory](PUBLICATION_MANIFEST.json), and [checkpoint](RESEARCH_LOG.md)

This is AI-assisted independent mathematical review, not formal proof-assistant verification or established human peer review. Public primary citations, exact theorem scope and retrieval limits are in the report and audit. The inaccessible live problem page is not represented as inspected.

## Preservation and reproduction

The exact author ZIP (13,913 bytes) and audit ZIP (30,176 bytes), their external manifests and all 7 author plus 11 audit members are retained unchanged. The audit includes its own nested original ZIP/manifest. Frozen pending-audit and not-published fields, and the descriptive historical queue_scope Status=partial, record earlier stages. The canonical queue now uses unsolved and 3/5. Only this row's Status and Turns change; its Findings and every unrelated byte are preserved.

Run `python verify_publication.py .` here, then repeat with `python -O verify_publication.py .`. This checks inventories, original pins, acceptance bindings, scope and hostile-mutation controls. It does not execute archive code or check mathematical topology.

Run `python independent_audit/VERIFY_ACCEPTED_AUTHOR.py archives/TANGLE_STABILIZER_2756_AUTHOR_SAFE_FREEZE.zip archives/TANGLE_STABILIZER_2756_AUTHOR_EXTERNAL_MANIFEST.json`, then repeat with `-O`, for the frozen author validator. It verifies packaging only. The frozen audit records 45 source/corpus/archive pin checks, 24 relocated builder cases and a 19-case validator suite per harness mode. Publication replay separately rechecks those results with available local source/corpus inputs; those inputs and private build tools are excluded from publication. No mathematical checker is supplied or claimed.

This publication is a draft PR. No merge, auto-merge, release, DOI or outside outreach is requested. Remote CI is reported separately; local packaging checks are not a claim that CI passed.
