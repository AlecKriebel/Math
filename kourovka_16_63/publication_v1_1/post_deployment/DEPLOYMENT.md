# Version 1.1.0 deployment checkpoint

Timestamp: 2026-09-15 14:04:53 UTC.

Task completion estimate: **100%** for the requested revision, repository publication, live-site verification, and preparation of the manual Zenodo package. This is workflow tracking, not a mathematical confidence percentage. Author-controlled Zenodo publication and any external correspondence remain separate next steps.

## Fixed publication snapshot

- Publication commit: `b575b59086c1f9756c4c65991f6aa8905a73304e`.
- Annotated tag: `kourovka-16-63-v1.1.0`, resolving to that commit.
- Main and the tag were pushed atomically to `AlecKriebel/Math`.
- No GitHub release was created and no Zenodo deposit was submitted.
- GitHub Pages build `1216966626` reports `built` for the publication commit, completed at `2026-09-15T14:02:57Z`.
- Deployment workflow: https://github.com/AlecKriebel/Math/actions/runs/34978685446 — successful.

## Live verification

All five URLs returned HTTP 200 and matched the local published files byte-for-byte after deployment:

| Artifact | URL | SHA-256 |
| --- | --- | --- |
| Publication page | https://aleckriebel.github.io/Math/papers/kourovka-16-63/ | `1e31e5546415e60f7653fa2ebcab3a2ff1cc9d42e2969ea56b71d23b3e2fc5ab` |
| Paper | https://aleckriebel.github.io/Math/papers/kourovka-16-63/paper.pdf | `9d94db98b4b599a176e95bc74ae8048f69db81d852cf8d557e22f2191c298248` |
| Source and certificates | https://aleckriebel.github.io/Math/papers/kourovka-16-63/source-and-certificates.zip | `33560d8879bbe3df578f92a8e6311010e504b7d2b669af6678163a7c8f96a7a4` |
| Zenodo upload kit | https://aleckriebel.github.io/Math/papers/kourovka-16-63/zenodo-upload-kit.zip | `e5ed2b111cbf3a390a655f18fd25605e88ee719286d9a11a03002dab826b4fd3` |
| Homepage | https://aleckriebel.github.io/Math/ | `aeb3365fcd8a06ca885bcb1134edb87b18d835abe71b44780074ee357c65b608` |

The source archive, upload kit, mathematical-input integrity check, revised manuscript, and scoped review are frozen at the publication tag. This post-deployment record intentionally sits outside the frozen archive and its manifest; recording deployment does not require regenerating artifacts or moving the tag.

## Remaining author actions

Use the existing Zenodo draft holding DOI **10.5281/zenodo.22770864**; confirm its record/version identity, choose the intended license, upload the two files in `UPLOAD_THESE_FILES`, paste the prepared metadata, and publish. The assistant has not accessed the private draft or confirmed its unpublished state. The supplied DOI was not publicly resolvable when checked during revision preparation.

After publication, verify the DOI and deposited files. Any contact with Notebook editors or a specialist must be performed by Alec personally under the project's independent-research policy. No outreach has been drafted or sent. The optional author-responsibility declaration remains a personal decision; no unconfirmed undertaking or license grant was added.

The paper remains an unrefereed preprint supported by the recorded AI-assisted audits and exact computational checks. No proof-assistant formalization or external human peer review is claimed.
