# Immersed leaf approximation: audited scoped partials

Target **10300062 / AMR-102-0062**, rank 670, Calegari Question 14.2.
Campaign disposition: **unsolved, 5/5**. The original question remains unresolved.
The log records five distinct approach families; the campaign ledger is not a claim that each tool call or family was a separate chat response.

## Accepted result and exact limits

A smooth taut suspension on a nonzero-Euler circle bundle obstructs coherent compact-domain approximation by **closed, fundamental-group-injective immersed surfaces**. The obstruction also holds after finite ambient covers. This is a valid scoped partial theorem, not an unqualified answer to the original question.

The source describes converging images of expanding balls without fully specifying its convergence topology or immersed-surface conventions. Closedness and fundamental-group injectivity are explicit conventions of this packet. The torus-cover control shows that image convergence of a given sequence need not provide coherent lifts; it does not disprove the original existential image-approximation assertion. Surfaces with boundary are outside the obstruction. The Seifert-fibered construction does not cover a hyperbolic-only ambient restriction.

Other proved partials include coherent approximation for a specific irrational linear foliation of the three-torus, a folded-double kernel, a transverse invariant-measure obstruction, and a precisely scoped area estimate. No novelty, first-resolution, exhaustive literature-open, or formal proof-assistant certification is claimed.

Read the [full authored proof](packet/PROOF_AND_PARTIALS.md), [five-approach log](packet/APPROACH_LOG.md), [limitations](packet/LIMITATIONS.md), and [complete independent audit](independent-audit/AUDIT.md).

## Frozen history and controlling verification

All nine original author files and all eight safe independent-audit files are preserved byte-for-byte, along with the exact audit archive. Historical audit-pending and no-publication wording in the author freeze describes its earlier state. The completed, separate independent audit accepts only the expressly limited theorem; no mathematical correction was required. Independent AI review is not human peer review.

The original author inventory checker ignores unlisted nested files named MANIFEST.json and does not externally bind its own root manifest. Keep that checker as historical evidence. The audit's stronger verify_binding.py and this publication wrapper are controlling: they pin the original manifests and enforce exact file sets. The wrapper also rejects nested manifests, extra files/directories, missing or changed files, special files, and symlinks. It binds the release manifest by a hard-coded digest and checks the audit archive against the expanded audit.

Trust the verifier from the reviewed Git commit. No self-contained package can authenticate a verifier replaced by an attacker. PUBLICATION_MANIFEST.json inventories the 19 payload files; the verifier and that manifest are the two explicitly excluded trust-root files. Exact remote Git-blob verification covers all 21 artifact files.

## Portable replay

Python 3.10 or newer and only its standard library are required. From this directory, or from any working directory using the script's full path:

    python3 -B verify_release.py

Integrity only:

    python3 -B verify_release.py --integrity-only

Add adversarial package controls:

    python3 -B verify_release.py --self-test

The wrapper validates integrity before executing anything from the payload. Replays run in disposable copies with Python isolation and assertions enabled, even if the wrapper itself is started with -O. The author results and independent replay output must reproduce byte-for-byte. Finite algebraic checks are guardrails, not proofs of the topology, asymptotics, or convergence interpretation.

Frozen bindings:
- Author manifest: 1,648 bytes, SHA-256 1f64af140ad77607cfd4a0ea61ed418853f9af99740387632b6f30545050b1f6.
- Audit manifest: 1,535 bytes, SHA-256 17bd438880d29f36f4a1ae1007ca2c0463e461d8393654028d3258387bde2615.
- Audit archive: 13,241 bytes, SHA-256 253082ed4706b701e2e45988bf6bb861cc0bf8b783130be1e2fbe469fbb06263.

## Publication boundary

Only authored mathematics/code, the full safe audit, and public bibliographic/verification metadata are added. No source PDFs, extracted source text, datasets, private sources, or coordination files are included. The separate queue edit changes only this target's Status and Turns, preserving Findings, links, the existing header, and every other byte of the actual base blob. No queue command, merge, release, DOI, or outreach is part of this draft.
