# Source and contribution audit:5100015

## Exact source identity

The complete imported statement and upstream OPEN-TRIAGE report are pinned to dataset revision37e53eabe540fb458758e198be61634bd02ee008. Their joint hash8919047adee9899df93fbe6bc3c6cf26509fdd92e826d3ab2d4803b95eae8158 matches the catalog. The statement hash is8c2e3e6b35cb8e99c421a6b9e80f2ba78a1939e86657dba9c7fc2bc8d0e0de90. They were read in full from a read-only cache whose revision and15458 record count matched the repository manifest.

Both source Table4 pages were visually inspected: arXiv:2004.12497v11 p.6 and the published Arnold Math.J.7(2021) p.346 agree on k303,b=A'A'_M, N not0mod4, M=O. There is no edition-numbering or product/quotient repair for this target. The outer polygon's sides are tangent lines to the outer ellipse at the original orbit vertices. Its pedal from O is not the caustic-contact polygon and is not the pedal of the original chords. Signed shoelace areas retain their cyclic traversal order for stars.

The source prescribes a>b>0 and two nondegenerate confocal ellipses. Primitive period is used for the canonical parametrization. Unlike some even-only target statements, the present printed parity condition also admits repeated traversals by a direct argument: a divisor of a number not divisible by4 cannot be divisible by4, and the two areas each scale by the repetition count. PROOF.md spells this out rather than silently changing the period convention.

## Primary inputs actually checked

- Reznik–Garcia–Koiller: complete v11 and published PDFs, Sections1–3.4, Table4, and related table labels. Source reading copies were recovered from previously verified downloads; their hashes are recorded afresh.
- Stachel: complete published PDF of *On the motion of billiards in ellipses*, EJM8(2022),1602–1622, especially Theorem4.3/(4.9) and the caustic-contact phase. The modulus is the caustic eccentricity. The source's adjacent erroneous dn real-shift sign is not used; DLMF supplies the correct signs.
- NIST DLMF22.4, Tables22.4.1–22.4.3: real/imaginary periods, simple poles and zeros, real/imaginary half-period signs, and quarter-period translations, opened directly on2026-10-01. DLMF22.8.1–22.8.3 supply the addition identities. The odd-trace product lemma is proved explicitly using these standard data.
- DLMF22.9 cyclic identities was consulted as related context; no unquoted special cyclic identity is an additional proof assumption.

The proof does not need Chavez-Caliz's area-product theorem or a general-position extension. Its area products reduce directly to the explicitly proved cyclic dn lemma. No private communication, inaccessible proof, or new source executable is a dependency. PDFs, full text extractions and page renderings are excluded from publication.

## Prior-work gate and bounded literature search

All-state PR searches for5100015 and the exact k303/b expression, branch search for5100015, available all-ref attempt-directory history, main queue/catalog, campaign inventory and prior-user context found no located prior exact target attempt. The main-queue-only inventory caveat was respected by additional checks. The old upstream report is third-party triage, not a campaign proof turn. Related-target-groups.json has no exact duplicate.

Focused web searches covered the precise invariant code and Poncelet/outer-pedal area terminology. They returned the original conjecture tables and adjacent topics such as general pedal polygons, negative-pedal curves and bicentric pedal perimeters. None identified an exact prior full proof of this target. This is a bounded search, not an exhaustive novelty certification; no external author was contacted.

## Shared/parallel work and review independence

- The full center-only trace-product mechanism was written at05:11 UTC in TURN1_DERIVATION_CHECKPOINT.md and committed06ca5b9e before reading the k203,a proof. It was safely checkpointed on the remote WIP branch ated599280cf309684c74364a46f5c9cb59ecfb8c7.
- A separate assigned review of k203,a then ran05:11–05:22. That proof uses the same standard dn-area identity, and a different meromorphic simple-pole proportionality mechanism for arbitrary fixed M. The core k303,b pointwise edge-vector reduction and odd-order reflected-zero product lemma predate that reading. The overlap is disclosed rather than claimed as independent discoveries.
- The parallel k303,a author reported a candidate only for primitive2mod4 and arbitrary M. Its frozen proof was not read or used as an input to this candidate. Our odd-period argument and center reduction stand on their own. The overlap at M=O is not a second independent discovery claim.
- Related PR147/148 supplied already-reviewed four-/six-period geometries used only for diagnostic controls. Exact N=6 control values for the present target are40 in both phases. The excluded N=4 pair gives1152 and1250, a scope check, not a counterexample to k303,b. Earlier k110/k111 contact-area results are not substituted for this outer-pedal target.
- A fresh reviewer uninvolved in the present author derivation must check the full result before any claimed-result PR. Reviewing this author's work is distinct from the author's prior review of k203,a.

## Turn count and certificate limits

One substantive author turn:05:06–05:11, pause for the separate review/coordination, then resume05:22. Active research is well under the two-hour cap. A verifier-development check initially used simple substitution where reduction of a cubic term modulo c²+z²−1 was required; the checker was corrected to polynomial remainder. The mathematical identity/proof was unchanged. All final checks and exact source/turn receipts are frozen separately.

Finite exact algebra/geometry checks and high-precision diagnostics support the proof; only the written analytic argument proves all phases and all admissible periods. A successful result may finish before five author turns; no unresolved research search is being skipped by source-only relabeling.
