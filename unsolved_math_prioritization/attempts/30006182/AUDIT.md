# Prior-result audit: problem 30006182 / OWR-14299084-004

This AI-assisted, unrefereed edition records an internal AI audit of a prior published result. Acceptance here is an internal mathematical assessment, not human peer review or formal proof-assistant certification. Finite checks are corroboration only. This is a full written proof and audit edition, not a computational reproduction package. Source retrieval and inspection described below occurred during the preceding audit on 11 October 2026; this editorial preparation performed no fresh scholarly-source retrieval or inspection.

## Decision

ACCEPT THE PRIOR RESULT FOR THE FINITE, STATISTICAL, NON-ROBUST EXISTENCE INTERPRETATION. Do not give the under-specified original question an unqualified all-interpretations acceptance.

The full primary manuscript is now available and its relevant proof has been reconstructed in `PROOF.md`. For every finite multiparty function and every positive error tolerance, there is an additive randomized encoding into a finite abelian group, with independent local randomness, pointwise statistical correctness, and output-only total-variation privacy. The reconstruction gives explicit finite parameters and a complete multiparty reduction. No cryptographic hardness assumption is needed for that precisely stated finite existence result.

The positive statistical theorem was publicly posted on 8 August 2025. This edition credits that prior result and audits the precise finite-existence interpretation; it makes no new universality or first-resolution claim.

Perfect correctness, perfect privacy, robust/insider security, and efficient statistical AREs for every polynomial-time family are not accepted. The original does not explicitly choose among these conventions, so its ambiguity must remain visible in any later status change.

## Original target and source authentication

The target is *Information-Theoretic Additive Randomized Encodings*, problem OWR-14299084-004, recorded under numeric identifier 30006182. The official source is *Cryptography*, Oberwolfach Reports 3/2025, DOI 10.4171/OWR/2025/3, https://ems.press/content/serial-article-files/51349 . The complete Ishai Part 1 contribution spans printed pp. 150-151, physical PDF pp. 10-11; both pages were textually and visually checked in the preceding audit, including the continuation on the second page. The adjoining Bitansky Part 2 contribution is explicitly about computational assumptions and was not conflated with Part 1.

The original object is additive encoding into a finite abelian group. There is no requirement of affine dependence on the input, or of a specified field. The finite field F_2 appearing inside the later proof is an internal tool, not a replacement of the target.

The original report was fully retained but only pp. 10-11 were inspected for this audit; unrelated workshop contributions were not proof-audited. Its PDF has 34 pages, 320825 bytes, SHA256 bccf58bfcfb3a74979ec08e6f201d0d06649c75ff4f95ac0305c855d2e429d6c.

## Primary result and exact source identity

Nir Bitansky, Saroja Erabelli, Rachit Garg, Yuval Ishai, *Shuffling is Universal: Statistical Additive Randomized Encodings for All Functions*, https://eprint.iacr.org/2025/1442 . Full PDF: https://eprint.iacr.org/2025/1442.pdf . Published STOC 2026 proceedings identity: pages 1836-1846, DOI https://doi.org/10.1145/3798129.3800890 . The institutional publication record identifies publication on 9 June 2026; conference dates are a separate matter.

Inspected ePrint PDF: 23 pages, 383423 bytes, SHA256 45510b5dcac7eae92afbaf9a575b02fe861373e713adac4a6987c0f2ac282b3a. This is not the 11-page ACM proceedings file, and no byte-equivalence between those versions is asserted.

Version provenance was checked in the live ePrint history at https://eprint.iacr.org/archive/versions/2025/1442 : the 20260617:165144 entry is a metadata-only update, whereas 20250808:032523 is a PDF update. This explains the PDF's August 2025 creation timestamp and prevents falsely calling it a newly rewritten June 2026 manuscript. The current landing page marks it published elsewhere at STOC 2026.

Theorem 1.1 is on physical p. 3, not p. 2 in this authenticated file. Its quantified scope is every k-party f:D^k -> D on a finite domain, for every epsilon>0, with both statistical correctness and privacy errors bounded by epsilon. Definition 2.1, pp. 7-8, gives the encoders, deterministic decoder, pointwise quantifier over all inputs, and output-only simulator measured by total variation. The introductory threat model on p. 2 expressly excludes insiders.

## Retrieval and inspection history

The preceding audit recorded unsuccessful direct IACR landing/PDF and ACM full-text retrievals (HTTP 403), and unavailable PDF parsing through a separate retrieval route. It subsequently retrieved the canonical public ePrint PDF on 11 October 2026 at 05:06:11 UTC via the paper link on the author page https://wp.nyu.edu/sarojaerabelli/ . The successful file retrieval does not establish that the earlier failed routes became available. No HTTP response code was exposed for the successful retrieval. The ePrint landing page, author records, institutional proceedings records, official STOC contents, and ePrint version history supplied bibliographic cross-checks. The ACM proceedings PDF was not retrieved or byte-compared with the 23-page ePrint manuscript. These are recorded historical retrieval boundaries, not new retrievals or source inspections performed for this edition.

All 23 extracted text pages of the ePrint manuscript were read, including references and Appendix A. Visual checks were performed on pp. 3, 7-12, 14, 16 and 23. The core proof in Sections 3-4 was checked line by line against an independent probability argument. Section 5.2's finite multiparty use was reconstructed explicitly. Sections 5.3-5.4's stronger efficiency claims were read to determine their scope and dependencies, not accepted merely because they appeared in the manuscript. Appendix A was inspected only as evidence of the correctness boundary and for a local typo check; it is unnecessary for the accepted theorem.

## Proof audit outcome and dependency closure

The accepted proof uses the following elementary dependencies, all demonstrated in the reconstruction:

1. A uniform group element plus any independent group element is uniform; fresh coordinates give product distributions.
2. Additive sharing over F_2: any proper subset of shares is uniform, and masking by independent zero-parity shares makes the derived output shares independent of the full input-sharing tuple, conditional on output parity.
3. Union bounds, total-variation coupling, triangle inequality for independent conditional hybrids, and monotonicity under randomized postprocessing.
4. A finite perfect DRE built from independently shared rows of a randomly shifted truth table. Its entire output law is explicitly simulated from the function output.
5. A coordinator-local seed and two-party bit-OT AREs remove the auxiliary DRE's shared-randomness requirement. Every actual participant's encoding is local and independently randomized.

The final construction uses T bit-OT instances, bounds correctness by 16tT/q and privacy by T2^(1-t), and gives explicit t,h with H=F_2^h and q=2^h. These bounds apply to all inputs, not just an average input distribution. They imply both errors <=epsilon while all groups remain finite.

The final encoded length is stated explicitly and is exponential in total input length for this elementary DRE. The construction is uniform given a full finite truth table, and efficient as the accuracy parameter varies with f fixed. Neither statement supplies a polynomial-size statistically secure encoding for every succinct polynomial-time function family. The primary paper's sharper bounds rely on additional DRE and amplification results. They are not needed for, and are not silently included in, this acceptance.

## Textual and quantitative cautions

- The informal overview on p. 5 has a displayed sum indexed to d where t is the number of shares; the formal construction and correctness proof on p. 11 use t. Our reconstruction uses t throughout.
- Proposition 4.5's displayed simulator uses a failure marker in its rare all-one branch. Our simulator outputs a fixed group element in that branch, retaining the same TV bound and satisfying the exact G-valued syntax.
- Theorem 5.2 on p. 14 displays final error epsilon+delta from an OT batch for one receiver. A direct composition over k-1 receiver batches yields epsilon+(k-1)delta unless delta has already been budgeted globally. The theorem is stated without a detailed proof there. This audit does not certify the factor-free literal bound or infer a contradiction with finite existence. It explicitly budgets every OT invocation and proves the resulting bounds. Asymptotic amplification can absorb such factors, but exact error arithmetic must not be omitted.
- Appendix A p. 23's second correctness bullet says the leaky decoder falsely outputs 0 in the false-alarm case; the stated construction requires a false output of 1. This is a local typo and not used in the accepted reconstruction. The existence of an abort-detecting variant is not perfect correctness.
- The p. 7 preliminary definition of group efficiency gives a |G|^c time bound, while later asymptotic families require polynomial cost in the security parameter. We avoid importing an ambiguous efficiency claim by explicitly choosing bitwise XOR groups.
- No claim is made that all finer efficiency statements in the paper have been independently proved or disproved. In particular the multiplication-code/amplifier discussion in Section 5.4 is a sketch with external dependencies.

## Reproducibility and limits

The authored finite checks exhaust small distributions for the leaky encoder, the share-masking independence lemma, and the finite DRE. They also test parameter inequalities. They are corroboration, not a proof by experiment. Only our own checker and integrity tooling were executed, under normal Python, -O and -OO; no author code, downloaded executable, proof-assistant project or third-party certificate was run.

The preceding audit authenticated its source inventory by exact sizes and SHA-256 hashes. Historical integrity checks ran in ordinary Python, -O and -OO, including negative controls for altered, missing or extra entries, linked or unsafe paths, altered semantic status, and incorrect seal pins. Successful integrity checks prove byte/closure consistency, not mathematical truth. Public verification metadata appears in `VERIFICATION.json`; the full written reconstruction, rather than finite test output or an integrity check, supplies the mathematical argument.

This edition distributes only authored proof, audit, acceptance prose and public verification metadata. Source PDFs, extracted source text, page images, code, raw finite-check outputs and dataset contents are not distributed. No source-author code was executed. Publication status of the cited STOC paper does not imply external review or endorsement of this separate AI-assisted reconstruction. No novelty, perfect-security, perfect-correctness, insider-robustness, uniform infinite-domain or general succinct polynomial-size claim is made.
