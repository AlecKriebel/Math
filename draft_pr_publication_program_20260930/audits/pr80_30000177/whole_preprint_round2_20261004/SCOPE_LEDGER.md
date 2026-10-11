# Actual reading and evidence scope

This is the second fresh whole-package review, performed independently by a new reviewer. The scope below records actual reading, not download counts. `SOURCE_FIRST.md` and `FIRST.md` were frozen before any priority supplement or earlier substantive assessment was read. No ROOT or sibling substantive report/verdict, including round one's report, was subsequently read. Administrative snapshots, original byte manifests, primary paper bodies, code, and later provenance ledgers were consulted as specified below.

## Source-first reconstruction

| Primary item | Actual reading | Retained evidence |
| --- | --- | --- |
| OWR report 4/2005, DOI 10.4171/OWR/2005/04 | Bruß's relevant contribution, printed pp.203–205, including the exact W4 question on p.205; unrelated workshop contributions were not reviewed | Original authenticated PDF; own `extract_owr2005_pdf` and extracted text |
| Bruß et al., PRL 93,210501, author PDF | Relevant full four-page article body, model, classification and open question | Own `extract_bruss2004_prl_author_pdf` |
| quant-ph/0407037v3 | Model and target/classification passages; comparison with PRL | Own `extract_bruss2004_arxiv_v3_pdf` |
| quant-ph/0507146v1 | Expanded model, §§3.1,4,5,6,7 and relevant discussion; no claim of line-by-line review of unrelated material | Own `extract_bruss2005_pdf` |

All four original PDF byte identities are in `INPUT_MANIFEST.json`. The administrative review snapshot was read before these papers; its correction-history flags were not used as conclusions.

## Pinned kit

All 312 lines of the pinned TeX source were read before `FIRST.md` was written. Every page of the frozen five-page PDF was personally viewed from our own 110 dpi rendering. The complete verifier, results, README, LICENSE, digest file, local deposit metadata and priority supplement were read. All nine members and the input snapshot were pinned initially and checked again by `verify_kit.py`. A private standalone rebuild and both PDF text extractions were produced. All five rebuilt PNGs and extracted text are byte-identical to their frozen counterparts; the PDFs themselves differ in bytes and creation timestamps. No claim of full PDF-object canonical equivalence is made.

## Closest priority and theorem sources

| Source/version | Actual independently read scope | Judgment and precise limitation |
| --- | --- | --- |
| Winter, quant-ph/9807019v3, 1 February 2001 | Model §II, code/error definitions §III, Theorem 9 and proof §VI, Theorem 10 and relevant surrounding limitations; appendix introduction | Separate independent codebooks and average error support the application. No complete audit of every appendix theorem or authentication of equality to final journal bytes |
| Huang–Zhang–Hou, quant-ph/9911120v5 | Introduction, model, §VI printed pp.9–11 | Prior general MAC dense coding is credited; example sends to common Charlie |
| Cao–Song, CPL 23,290–292 (2006) | All three publisher PDF pages personally viewed after our text extraction proved garbled | Old paired-W Bell decomposition and classical sender disclosure confirmed. Security assertions not certified |
| Pradhan–Agrawal–Pati, 0705.1917v1 | §4 introduction/model pp.32–33; §4.2.3 p.36, Eqs.(108)–(109), with untruncated re-reading of the decisive passage | One Alice owns the two sender qubits; Bell forwarding and two-bit Bell-to-Bell construction confirmed. Other protocols and any possible unstated corollary not fully reviewed |
| Das et al., 1412.6247v1 | §II model, routing, Eqs.(3)–(5),(11), relevant pp.2–4 and conclusion p.10 | Formal LOCC quantities are upper bounds. Final journal body and separate publisher-note body not read/authenticated |
| Muhuri et al., 2211.13057v2 | Introduction/model §II, Eqs.(6)–(7), two-receiver §III C, Fig.3 caption and discussion pp.8–9 | Formal B² quantities are upper bounds. No achieved strict target code in those passages; final journal-body identity not certified |
| Matthews–Wehner–Winter, 0810.2327v2 | Full relevant §4, printed pp.17–19, including correction of dimensional restriction and Eq.(24) | Independent isotropic POVMs work in arbitrary finite dimension; no 2×n exclusion. A separate fixed-instrument bound was reconstructed here. Unrelated discrimination sections not exhaustively reviewed |
| Hayashi–Wang, final PRX Quantum 3,030346 (2022) | Official published PDF title/abstract, Assumption 1, §IV A model pp.7–9, Theorem 2 p.12, relevant §IV G p.13 | Actual published passages, rather than inaccessible local shell body. One message, fixed helper and multiplicity-free assumption block the direct proposed identifications. Other possible corollaries/appendix results not universally excluded |

The first seven were extracted through our own recorded children from authenticated retained PDFs. Hayashi–Wang was read using the web tool at [the final publisher PDF](https://journals.aps.org/prxquantum/pdf/10.1103/PRXQuantum.3.030346). Private raw web receipts are retained; the tool exposed no actual PID/argv, and none is fabricated.

## Broader corpus and fresh leads

After the independent closest-source analysis, the complete target-family `LITERATURE_LEDGER.md` and mechanism-family `SEARCH_LEDGER.md` were read only as provenance ledgers. They record additional actual reading by other reviewers; that reading is not reclassified as our own. We did not independently read the full bodies of Sen(De)–Sen–Lewenstein, Wang–Yan, Shukla–Banerjee–Pathak, Singh, Roy, Liu, Hullamballi, Pauwels–Gühne, and the sender-preprocessing/singlet-conversion family in this round. The package supplement accurately limits its inference to the recorded inspected corpus.

Its unrecovered Yuan papers, Zhao original body, Tsai–Hwang 2013 body, Das publisher-note body, and final Das/Muhuri version identities remain explicitly limited. These are not declared cleared. The distinct 2010 Tsai–Hwang abstract is not substituted for 2013. No secondary description is treated as a complete original-body read.

At 23:51–23:56 UTC a supplemental fingerprint search used:

- `"W state" "dense coding" "2.311"`
- `"W state" "LOCC" "asymptotic" "dense coding"`
- `"Bell" "W" "multiple access" "dense coding"`
- `"four-qubit W" "LOCC" "capacity" achieved`

Two leads were triaged from primary publisher material: [Shi et al., npj Quantum Information 7,74 (2021)](https://www.nature.com/articles/s41534-021-00412-3), abstract and general setting/Theorem 1; and [Subhi–Bacsardi, IET Quantum Communication 6,e70001 (2025)](https://doi.org/10.1049/qtc2.70001), publisher-indexed abstract and §4 model passages. The first uses a common receiver and pairwise product sender-receiver assistance. The second studies IIoT random access with entanglement generation and classical uplinks. Those inspected applications do not supply the fixed symmetric-W4 independent-sender split-receiver achievement. Neither full paper and all auxiliary results were certified. A direct Wiley open returned 403; primary indexed passages were readable in a subsequent search. Search absence is not an originality proof.

## Other read-only checks

The original retained `CANDIDATE.md` bytes, target QUEUE row and `turns.jsonl` were verified without modifying original state. The current named ROOT reconstruction hash and complete two-change code diff were inspected; no ROOT findings/report was read. The manifest checker `zenodo_deposit_tool/zenodo.py` was read at the local `check` branch and entrypoint before running `check`, which returns before credentials/client/deposit state. No staging, upload, publish, credentials, Git/index, PR, native editor or external-person operation occurred.

## Evidence limits

Actual child process identities, exact argv, UTC times, exit codes, complete streams, and prelaunch source copies are recorded by our own capture wrapper. Native tool calls used for browsing, image display and exploratory reads do not supply PIDs; their conversation/tool receipts are distinguished from child process evidence. `private/` contains copyrighted source copies/extracts, renderings and raw receipts and is ignored by this folder's `.gitignore`. Public-safe reconstruction code and result summaries contain no copied third-party paper bodies.
