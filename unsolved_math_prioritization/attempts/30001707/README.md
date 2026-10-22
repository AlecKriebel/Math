# Multiplicity-free quantization: scoped partial and source correction

**Problem 30001707 / OWR-4799-003, rank 834: unsolved, 3/5 substantive approaches. No novelty claim.**

The [independent audit](audit/INDEPENDENT_AUDIT.md) accepts the limited mathematics and a separately corrected execution boundary. This work does not resolve the original noncompact one-way implication from a zero-or-one geometric orbit count to multiplicity-free restriction.

## Mathematical scope

Read the unchanged mathematical [result](corrected/RESULT.md) together with the audit. The authenticated catalog's single-orbit equivalence strengthens the original source's one-way statement. For CP² with uncorrected holomorphic quantization by O(1), the restricted representation has three distinct circle weights, but every interior moment-level quotient has continuum cardinality. This refutes that single-level converse under the explicit convention. Its geometric antecedent fails, so it cannot refute the forward implication.

For O(k), the exact weight multiplicity is floor((k-|j|)/2)+1 when |j|≤k. Multiplicity already exceeds one at k=2. The CP² construction is not a scaling-family counterexample. A central-character parameter family tests a broader, explicitly specified product convention; its compact coadjoint orbits and compact semisimple factor do not resolve the intended noncompact family formulation.

The noncompact holomorphic symmetric-pair scalar-type results in Kobayashi–Nasrin (2018) and the SL(2,R) continuous branching example in their 2003 work receive prior credit. No general resolution, novelty, exhaustive literature status, external human peer review, or formal proof-assistant certification is claimed. The live catalog page could not be inspected; the authenticated corpus and inspected primary source are distinguished.

Exactly three substantive approaches are recorded in [APPROACHES.md](corrected/APPROACHES.md): explicit single-level/unrestricted-family examples, tensor-power scaling, and the credited noncompact benchmark. Source triage, independent auditing, and publication are not extra proof attempts.

## Original vulnerability and actual correction

The immutable [original author archive](archives/MULTIPLICITY_FREE_30001707_AUTHOR_SAFE_FREEZE.zip) and its extracted members are historical evidence. The original verifier imports hashlib before checking inventory. A benign hostile hashlib.py executed before rejection in normal and -O modes. A nonzero exit did not imply rejection before execution. Do not describe or use the original execution boundary as fail-closed in a hostile directory.

The [actual patch](audit/AUTHOR_PATCH.diff) changes only README.md, certificate.py, controls.py and verify.py. It requires isolated/no-site startup and propagates those flags to child interpreters. The mathematics, EXPECTED.json and other members are unchanged. [PATCH_APPLICATION.json](audit/PATCH_APPLICATION.json) records real application and exact nine-member comparison. The separately frozen [corrected archive](archives/MULTIPLICITY_FREE_30001707_CORRECTED_SAFE.zip), its extracted corrected directory, and the audit's corrected copy agree byte-for-byte.

The required mathematical-package entry point is [ISOLATED_VERIFY.py](audit/ISOLATED_VERIFY.py), SHA-256 38a043f47a90d1a7dcb2e59adc5c187be0e5ac04cc65a5584ddc2152693810fd. It authenticates the corrected external manifest and all nine members before launching package code. The manifest SHA-256 is fa1046d7262b9682a98007bc12ad2b33de095e692dc3ee8e94b0f77e39f1bb30. Retain these pins through an independent trusted channel; a replaced receipt is not a trust anchor.

## Replay

Use a trusted Python 3.10+ interpreter and the standard patch command. No third-party Python dependencies or source corpora are needed. Independently authenticate PUBLICATION_MANIFEST.json and verify_publication.py before executing the latter. From this directory:

    python -I -S -B verify_publication.py TRUSTED_PUBLICATION_MANIFEST_SHA256
    python -I -S -B verify_publication.py TRUSTED_PUBLICATION_MANIFEST_SHA256 --full
    python -I -S -O -B verify_publication.py TRUSTED_PUBLICATION_MANIFEST_SHA256 --full

The wrapper checks the entire strict inventory, all three archives and every member before any packaged executable runs. Full mode launches the mandatory isolated bootstrap, actually applies the patch and compares all nine resulting members, and replays the independently authored acceptance suite. Both acceptance modes include eight corrected positives, 58 hostile controls (ten hostile archives), four historical control runs and two positively reproduced original shadow exploits, plus independent finite mathematical checks. Original vulnerable runs occur only as deliberate benign diagnostics in temporary directories.

For the already-authenticated corrected package alone:

    python -I -S -B audit/ISOLATED_VERIFY.py corrected manifests/MULTIPLICITY_FREE_30001707_CORRECTED_EXTERNAL_MANIFEST.json
    python -I -S -O -B audit/ISOLATED_VERIFY.py corrected manifests/MULTIPLICITY_FREE_30001707_CORRECTED_EXTERNAL_MANIFEST.json

Isolation flags must be present at interpreter startup. Guards cannot undo unsafe startup. This is an integrity/reproducibility boundary for a trusted runtime and quiescent filesystem, not an operating-system sandbox. Finite checks do not prove the general conjecture or establish continuum cardinality.

## Publication boundary

The three archives and all historical members remain unchanged. Frozen pre-publication statements are historical snapshots; the current acceptance is this scoped audit. Contents are authored mathematical text/code/patches, audits, acceptance records and public verification metadata only. No copied source PDFs, extracts, rendered source pages, dataset contents, private sources, personal data or coordination records are included. The queue edit changes only this row's Status and Turns cells, to unsolved and 3/5.
