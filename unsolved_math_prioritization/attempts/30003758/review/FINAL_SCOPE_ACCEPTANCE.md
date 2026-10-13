# Final reader acceptance: subsampled-SDP clustering hold

**30003758 / OWR-15999-007 · queue row 1768 · 13 October 2026 UTC**

**ACCEPTED, for source interpretation and a readiness hold only.** The reviewed
seven-file package recommends `deferred`, contributes zero new substantive
proof-attempt passes, and leaves the lifetime count unknown. It does not resolve
a mathematical conjecture, clear readiness for proof work, or classify the full
historical question as `already_solved`. No change to the reviewed package was
required or made.

## Scope findings

- The original unquantified extrapolation question is preserved. The reader
  identifies the missing quality, sampling, data, access, computational, and
  probability specifications without silently adopting a replacement problem.
  This interpretation agrees with the question and surrounding definitions on
  printed pp. 785–786 of the [Oberwolfach report](https://ems.press/content/serial-article-files/46736).
- Known positive results remain conditional. The [2022 proceedings paper](https://proceedings.mlr.press/v151/zhuang22a.html)
  and [2024 journal article](https://academic.oup.com/imaiai/article/13/3/iaae016/7713562)
  are not promoted to an unrestricted theorem for arbitrary data. Planted-label
  recovery, geometric optimal-partition recovery, and lower-bound certification
  retain their distinct roles.
- Uniform fixed-size sampling in the historical construction remains distinct
  from independent Bernoulli sampling in the cited theoretical guarantees. No
  transfer of probability guarantees is claimed.
- The reader does not impose sample-only access or invent a universal
  impossibility argument from an omitted cluster. It does not select a later
  paper's conjecture as the original question.
- Source-statement inspection is clearly distinguished from a full proof audit.
  No published-paper error is alleged, and the acceptance does not depend on an
  unexamined theorem boundary. Global openness and exhaustive literature coverage
  are expressly left uncertified.

## Sources, versions, and publication boundary

The five recorded source representations were independently matched to their
stated byte counts and SHA-256 digests. These are representation-identity checks,
not authentication or proof certificates. Titles, authors, dates, publication
locations, and inspection limits were compared with the source records.

The 2018 report's [publisher record](https://ems.press/journals/owr/articles/15999)
gives a January 2019 publication date. The [2022 arXiv version](https://arxiv.org/abs/2211.15744)
and the final 2024 journal article retain their different author naming/order and
representation identities. No final journal PDF is falsely claimed. The
[2017 certificate paper](https://arxiv.org/abs/1710.00956) is not represented as
the source of the historical extrapolation wording.

All five package-relative links resolve. All 13 distinct external URLs were
checked for source identity and retrieval. The OUP DOI resolves to the correct
article but returned HTTP 403 on direct retrieval; the canonical article was
readable through web retrieval and the official article-minimal endpoint returned
HTTP 200. Thus this review does not claim universal link availability. The DOI
identity is corroborated by the journal article itself.

All seven public files, including the verifier source, were read. They contain
authored analysis, public bibliographic/inspection metadata, and one short
historical-question quotation. They do not redistribute source documents,
datasets, private material, or task-specific internal identifiers. Generic
path/URI checks in the verifier do not expose private task identifiers.

## Reproducibility checks

- `python3 verify.py`, `python3 -O verify.py`, and `python3 -OO verify.py` each
  returned success with 95 explicit checks. No optimization-removable assertion
  occurs in the verifier.
- An independent test harness exercised 44 negative cases in all three modes:
  **132 of 132 tampering runs were rejected**. Cases included same-length content
  changes, missing/extra entries, symlinks, manifest corruption, and resealed
  changes to status, pass accounting, sampling laws, proof/audit claims, source
  metadata, source URLs, the historical quotation, and key scope safeguards.
- All seven reviewed files remained byte-for-byte unchanged after testing.

The verifier and these tests establish the tested integrity and scope guards.
They are not a general semantic-tampering detector, a remote-source authenticity
check, or mathematical verification. This acceptance applies only to the exact
file identities below; modified bytes require a new review.

## Exact accepted identities

Seven files, **22,969 bytes total**. The manifest inventories the other six files.

- MANIFEST.json — 1,078 bytes; SHA-256 `79b4442c7756847b56169b297e30119710c82f909a1cd8f0abda5dd071918a08`
- README.md — 2,153 bytes; SHA-256 `93b68b7583681ee92dddaf44b35d4b45b31ba108fb322d59b6ecb13d2f4fb152`
- RESEARCH_LOG.md — 1,000 bytes; SHA-256 `21230d6cd5db547feebfff10d61462591065e63a0e0b785e622ce4090677e673`
- SCOPE_AUDIT.md — 4,997 bytes; SHA-256 `628defc0509b5b88b5abdd5a376979fb18d552231ee10838de9b7b01bc483a1b`
- SCOPE_RECORD.json — 1,042 bytes; SHA-256 `a84e9b59c37dc0e0bc32f6fd5712184d21ea090c21fcf83e8167d5329e93158f`
- SOURCE_INSPECTION.json — 5,880 bytes; SHA-256 `4a9d4f6aa39c06587e818bd28b964d707a44bf714f8a4d6303791e46233691a4`
- verify.py — 6,819 bytes; SHA-256 `f300dd55fba4ec5774166b21cac745074829fb7f3f63a7cd97d000d2fb6c5644`

Final reader QA is complete. Mathematical readiness remains uncleared. This review
performed no mathematical proof search and added zero substantive proof passes.
