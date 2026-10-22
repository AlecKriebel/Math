# Source, scope and prior-work gate

## Identification and exact question

The requested [catalogue entry 2914](https://www.unsolvedmath.com/problems/2914) returned HTTP 403 on 2026-10-03. A pinned catalogue record was used only to identify KP-4.38 and the K3 source. Its generated literature/status text was not treated as evidence.

The exact primary question and all four adjacent remarks were then checked in *K3: A New Problem List in Low-Dimensional Topology*, Problem 4.38, printed p. 221, PDF page 221 (zero-based index 220), including the page image. Its source is the [author-hosted 2026 volume](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf). A fresh direct download matched the working PDF byte for byte.

The target is asphericity of every smooth/PL ribbon-disk complement. The remarks identify the old number as Kirby 1997 Problem 1.103, relate the question to Whitehead asphericity, report the locally indicable special case, distinguish a locally flat homotopy-ribbon variant, and warn of an incorrect historical general proof. This deliverable does not substitute the locally flat variant or accept the historical blanket proof.

## Proof sources and limits

1. Tony Bedenikovic, *Asphericity results for ribbon disk complements via alternate descriptions*, Osaka J. Math. 48 (2011), 99–125, [DOI](https://doi.org/10.18910/4901), [full publisher-repository PDF](https://ir.library.osaka-u.ac.jp/repo/ouka/all/4901/ojm48_01_099.pdf). Read the LOT description in §1 and Appendix B, the geometric construction in §2 and Appendix A, and the complete proofs of the stated graph and relative-homotopy criteria in §§3–4. The public note uses the LOT model, not an unconditional conclusion from these conditional criteria.
2. Jens Harlander and Stephan Rosebrock, *Injective labeled oriented trees are aspherical*, Math. Z. 287 (2017), 199–214, [DOI](https://doi.org/10.1007/s00209-016-1823-6). The [24-page arXiv v6 author manuscript](https://arxiv.org/pdf/1212.1943v6) was retrieved and its relevant proof chain inspected: §1 reductions, §3 relative Stallings test and its proof, §4 orientation/generator-inversion correspondence, and §5 induction proving the injective theorem. The note retains the injectivity condition. Its new finite method check is independently verified from relator words, not inferred merely from this theorem.
3. Harlander and Rosebrock, *Local indicability in the presence of diagrammatic reducibility*, Canad. Math. Bull., online May 26, 2026, [DOI](https://doi.org/10.4153/S0008439526102069). The complete 11-page primary article was inspected, including the introduction's unresolved-status statement and §4's conditional hypotheses. This is a recent status check, not a proof that no solution could have appeared subsequently. The note does not invoke its conditional theorem to resolve all LOTs.
4. James Howie's 1985 *On the asphericity of ribbon disc complements*, [DOI](https://doi.org/10.1090/S0002-9947-1985-0779064-8), is cited historically in the above primary sources. The AMS full text returned HTTP 403. Its proof was not freshly audited and is not a deductive dependency of the elementary partial results in PROOF.md. Incorrect guessed AMS suffixes were discarded; only the verified bibliographic DOI above is retained here.

Classical tools used explicitly in the authored arguments are cellular homology, covering-space theory, Fox differentiation, the Hurewicz theorem, and Whitehead's theorem. None is used to infer asphericity from the ordinary homology of a nonsimply-connected complex. The general linear-algebra and lower-central-series assertions used in the note are proved there.

## Primary-file fingerprints

These SHA-256 hashes identify the inspected local PDFs, which are not part of the redistributable bundle:

- K3: `ae56518166fe38aaaf555c58614329228afe734e743b111badec4060877fa12f`
- Bedenikovic 2011: `4017a3f85f0f854bb438f459503884efd101086766041c8ac8ae0a3f47015be6`
- Harlander–Rosebrock arXiv v6: `87b0371007521b8b008e768b292983116cd534caf2487566b9af6b4aacdfb135`
- Harlander–Rosebrock 2026: `0796c706e77f615e0a86c8b5613c32f2ff05244bccb3c10f024b658d18542106`

## Actual prior-work check

The live [main-branch queue](https://github.com/AlecKriebel/Math/blob/main/unsolved_math_prioritization/QUEUE.md), blob `c87c275c638939b8008fd58db80657491d14971e`, had rank 534 / 2914 / KP-4.38 at `queued`, `0/5`. The queued row alone was not used as proof of no prior attempt.

On 2026-10-03, all-state PR searches in AlecKriebel/Math for `2914`, `4.38`, and the joint terms `ribbon` and `asphericity` returned no matches. The ID branch search returned no branches. Default-branch code search for `2914` returned no matches, although the queue itself contains the ID; consequently this code-search result is explicitly not treated as exhaustive. No existing proof attempt or corresponding PR was verified through these bounded checks. Artifacts stored under unrelated names could be missed.

## Classification and reproduction

**Unresolved after five substantive approaches; no full proof or counterexample.** The note is an honest partial-result/method-obstruction record. No novelty or first-resolution claim is made. The source gate is sufficient for this scoped result; it is not a certificate that the conjecture has been solved or a fresh audit of the inaccessible Howie proof.

`python3 verify.py` reproduces `verification.json` using only the Python standard library. The finite checks are separated from the general proofs and do not test universal-cover asphericity. Only the authored note, source gate, attempt log, status, README, verifier and verifier output are intended for redistribution. Downloaded papers, extracted text, the identification cache and query receipts are excluded.
