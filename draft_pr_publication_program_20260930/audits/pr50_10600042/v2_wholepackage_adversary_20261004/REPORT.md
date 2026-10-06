# Frozen v2 whole-package adversarial review

**Verdict: mathematical statement passes independent reconstruction; v2 promotion is on HOLD.** One mandatory diagnostic improvement is needed, and historical novelty remains unresolved. This review does not approve publication as a novel contribution, establish first priority, certify present openness, or authorize a release. The fixed manuscript's ordinary-closure formulation is a complete valid conditional consequence of its established classical and virtual Markov inputs; the diagnostic issue does not refute that proof.

## Review boundary and exact inputs

This was a fresh review of `publication_package_v2/even_strand_markov.tex`, its separately uploaded PDF, `even-strand-markov-verification-v2.zip`, and `zenodo-deposit.json`. `RECONSTRUCTION.md` was written before accessing older reviews or ROOT conclusions. No earlier review text was read as proof evidence. The actual primary PDFs/scans were independently hashed, copied into ignored `private/primary/`, and personally read. Initial hashes are in `INPUT_PINS.json`; final released-input and supplemental evidence hashes are in `FINAL_INPUT_PINS.json`. The final sweep detected only ancillary v2 `RESEARCH_LOG.md` drift: ROOT reported its genuine 01:10:59 preparation checkpoint had been appended after initial pins. That log is neither a ZIP member nor a released upload. The TeX/PDF/ZIP/deposit and all ten members stayed byte-exact. The initial sweep's strict assertion failure is preserved; the retry explicitly distinguishes this administrative change.

| Input | Bytes | SHA-256 |
|---|---:|---|
| TeX | 15,613 | `d6f663f6efc3295b546f0e061bd2d8b918082bcf932f501c774ebebfe4822493` |
| PDF | 62,145 | `2afa0517148f0b44f3cab081e3c2ca64c9e73699498c81770e2addf147961d57` |
| v2 ZIP | 20,964 | `b5da353b660ed0f261e7fe617e6ff347ee0561c8269d5a67606f0d3699e97481` |
| Deposit plan | 2,287 | `6cd1cecbd1779f20fcf48dbf998993c7159058c47a8a2ec97332cbeba0b91945` |
| Actual ZIP checker | 10,895 | `1f68f6f5ce1b87cac4d86be799a6c35c67f86abfd775602f2fca02c3999b975c` |
| Expected stdout | 1,056 | `729d2e4d5532db6420fb9248d4b4a3aad909e0c8603e548848eccf35351d8fff` |

Root and queue AGENTS were read. The exact source record has numeric ID **10600042**, Problem 42 in Fenn–Ilyutko–Kauffman–Manturov (2014). The four-line source item was personally verified on published p.37 and author-preprint p.34; its braid terminology is unqualified and has no locality or minimality requirement. Supplying both classical and virtual ordinary-closure calculi meets that literal interpretation. A plat theorem alone would not: the identity two-strand braid distinguishes ordinary from plat closure. [Published survey](https://doi.org/10.4064/bc103-0-1), [author preprint](https://arxiv.org/abs/1409.2823v1).

Read-only PR inspection at 2026-10-04 01:17 UTC confirmed [PR 50](https://github.com/AlecKriebel/Math/pull/50) remains OPEN and draft at `7260315f8b8b193020c09d4ef6df9d943a3a13ff`. Its submitted-head QUEUE row says `claimed_solved`, `1/5`. The working checkout is `main`, whose local QUEUE row instead remains `queued`, `0/5`; these are different snapshots. The retained original turn log records exactly one candidate turn and does not establish novelty. This audit made no queue or counter change and supplied no new central discovery attempt.

## Universal mathematical verification

The written proof has two logically separate directions. For soundness, C is conjugation; BC is conjugation on N−1 strands followed by positive stabilization on both sides; T compares permitted stabilizations of the same prefix; D is two successive stabilizations. R/L are the primary virtual exchanges; BR/BL exchange at N−1 then positively stabilize. Their syntactic bounds make those auxiliary operations legitimate. Odd proof objects do not become allowed calculus states.

For completeness, use the actual map P(m,w)=(m,w) at even m and (m+1,wσ_m) at odd m. It preserves ordinary oriented closure, fixes every even endpoint exactly, and sends every unrestricted generator to a permitted even edge:

| Unrestricted edge | even original count | odd original count |
|---|---|---|
| Defining relation in a whole context | same relation | same context with σ_m retained |
| Conjugation | C | BC |
| Right stabilization, either classical sign or virtual | D | T |
| Right virtual exchange | R | BR |
| Left virtual exchange | L | BL |

For odd left exchanges the old blocks shift from support through m−2 to support through m−1, while the padding crossing σ_m stays separate. This checks the most delicate BL index distinction. Reversibility handles every inverse edge. Nothing requires deciding braid equivalence, suppressing tags, or assuming the even calculus complete in order to prove soundness. The result uses unrestricted Markov completeness as an explicitly credited input; it does not replace that difficulty with an unsupported equivalent theorem.

The classical presentation and conjugation/signed right-stabilization input match Gorsky–Kivinen–Simental's Theorems 2.1–2.2, personally read on full p.5 including diagrams. The oriented scope was additionally checked against Lambropoulou–Rourke's full pp.1–2, which explicitly use isotopy classes of oriented links and corresponding-endpoint closure. [GKS v1](https://arxiv.org/abs/2108.10356v1), [Lambropoulou–Rourke v3](https://arxiv.org/pdf/math/0405493v3).

Kamada's full pp.4–7 were read as text and pixels: Definition 2.2 is exactly the stated virtual presentation, with no added welded relation; the diagrams have top-to-bottom orientation; Proposition 3.1 gives representation; Theorem 3.2 includes conjugation, all three right stabilization types, and both exchanges. The printed exchange has a negative first classical crossing, positive second crossing, and a left inclusion that shifts the old blocks. The formulas and signs were also checked on Kauffman–Lambropoulou's full p.30. These imported inputs match the manuscript. [Kamada v1](https://arxiv.org/abs/math/0008092v1), [Kauffman–Lambropoulou v3](https://arxiv.org/abs/math/0507035v3).

Boundary checks: the one-strand empty word pads to (2,σ1), the unknot; N=2 BC has empty blocks and R/L reduce to identities; the first odd exchange m=3 gives N=4, so BR/BL's minimum is correct. Empty words at tags 2 and 4 are distinct unlinks. Every positive-strand closure is nonempty, making the optional isolated zero-strand empty state necessary. Arbitrary finite blocks and support constraints are part of the statement; the proof establishes no geometric locality bound or minimal list. The certificate height is m+(m mod 2), nondecreasing in m, hence 2 ceil(M/2) for a supplied certificate. It says nothing about finding one.

The displayed illicit T and R counterexamples are correct. Fox 3-coloring gives 9 versus 3 for σ1³ and σ1; the signed ordered intercomponent matrices distinguish σ1² from σ1v1σ1v1 even after component relabeling. The invariant's Reidemeister justification is adequate: RI contributes only self-crossings, RII cancels signed pairs, RIII retains ordered component crossing data, and detours add no classical crossings. No units or numerical-stability issue arises in these exact finite-field/integer computations.

## Actual archive reproduction and independent falsification

The actual ZIP has exactly ten flat regular members, safe paths, normalized timestamps and permissions, good CRCs, and member bytes equal to the corresponding frozen package files. `ZIP_INVENTORY.json` records each member hash. The author checker was run from that extraction with `python3 -B verify_even_calculus.py`, actual child PID 67748, UTC 01:09:49.919866–01:09:49.991518. It exited 0 with 1,056 stdout bytes and no stderr: exactly the expected hash, 7,106 checks, 316 edge cases and 1,716 relation-context cases. The builder, PID 67747, rebuilt exactly the same 20,964-byte ZIP and SHA-256. These are new actual review executions, not reconstructed historical author executions.

`independent_controls.py` imports no author checker. It computes diagram closures with union-find and directed signed crossing records, and counts Fox colorings by Gaussian elimination of the closed linear system over F3. This differs materially from the supplied checker's permutation-cycle and color-enumeration implementation. It checked 29,108 legal scheme instances across all four classical/eight virtual families and N=2,4,6, including empty, short exhaustive and longer seeded blocks; 5,146 classical instances also passed Fox checks. Independent controls detect illicit T, R and BR support, idle-strand padding, and omission of a BL buffer. These necessary invariants are falsification tools, not sufficient equivalence tests or the universal proof.

Actual isolated mutations detect changing BL's buffer index, dropping a T terminal sign, and corrupting either the TeX or expected-result checksum. The ZIP builder refuses an existing ZIP by construction; extraction/rebuild succeeded before TeX generated ancillary files. All raw streams and process receipts are in ignored `private/commands/`; mutation bodies/hashes are in `MUTANT_INPUTS.json`. No stdin bodies were supplied: the execution helper explicitly uses DEVNULL. Helper source files are preserved and hashed. Four initial inventory/read commands preceded this helper; the tool exposed their outputs and elapsed times but no PIDs, and this audit invents none. Web/view tools expose no process PIDs; retained metadata says so.

## Mandatory finding F01: left-shift diagnostic common-mode failure

**Severity: P2, mandatory verification improvement before promotion.** The v2 checker calls the same `shift` helper for both its supposedly independent unrestricted construction and its even construction. Erasing the helper's `i + 1` increment changes both sides together. The actual 10,891-byte mutant, SHA-256 `ef5392e19e9625e15ab1f8b1a3aa44ef58448e638cefe21dea5bb79380615cbf`, ran with PID 71246 at UTC 01:13:59.929931–01:13:59.999550 and still returned exactly the original PASS JSON/hash. Thus the existing test counts cannot alone certify left shifting; shared-helper agreement is insufficient.

The present source correctly increments indices, and the universal proof and primary formulas are correct. This is a verification coverage defect, not a theorem counterexample. A minimal repair is a literal nonempty source-bound witness, plus a genuine new recorded run rather than rewriting the old attribution:

- At N=4, a=b=σ1, L must generate literal σ2σ1⁻¹σ2σ1 ↔ σ2v1σ2v1. Both true endpoints have two components and zero ordered intercomponent matrix. The zero-shift mutant instead gives σ1² and σ1v1σ1v1 with two idle strands; both have four components, but their active matrices are respectively [[0,1],[1,0]] and [[0,2],[0,0]]. They are unequal under simultaneous relabeling.
- For BL at N=4 with the same blocks, append the literal **unshifted σ3** to both true L words. Both true endpoints have one component. The zero-shift mutant has three components and the same distinct active matrix pair.
- Keep the syntactic BL block bound (indices at most 1) and reject a block touching index 2; preserve signs and virtual-letter types. Label the two constructions as separately prescribed rather than independent when they share helpers.

`literal_source_controls.py` embodies these primary-transcribed endpoints and uses the separate union-find invariant implementation. It loads the author code solely to test its actual endpoint generator; it is not the independent proof. Actual original-source run PID 72971 exited 0; actual zero-shift mutant run PID 72970 exited 1, with both endpoint and invariant mismatches recorded. Fixing diagnostics should produce a new version, new expected output and provenance while preserving frozen v2 and its historical author-run attribution. No package edit was made here.

## Priority and prior-work hold F02

Nencka's printed 1996 pp.147–148 and the ISBN/copyright leaf were personally read from their actual scans. The primary text first defines ordinary Markov equivalence by corresponding same-link closures, then introduces an interwoved-string representation and announces a different generalized equivalence on power-of-two braid groups. The signed tail visibly contains ± signs; any positive-only objection would be false. For n≥1, its 2^n tail crossings group into successive signed double stabilizations, so this cannot be dismissed merely because the counts form a subset of the even numbers. [Scanned authored contribution](https://ru.djvu.online/file/OzKCMNnU4ojPn).

The v2 qualification is fair **for these two pages**: they do not define the new equivalence/representation well enough or give a proof connecting its theorem to ordinary closure; their one-strand convention is unclear. They do not state a virtual exchange calculus. Neither certifying an earlier ordinary-closure solution nor refuting the announcement follows from those facts. Fiedler's negative double-move result is only used as a qualified comparison; this reviewer did not obtain or certify his complete proof, and the manuscript explicitly says so. The current padding proof does not depend on that counterexample. [Fiedler publisher record](https://doi.org/10.1142/S0218216503002561).

**Historical novelty remains HOLD.** The later primary leads are material: Nencka, *Cantorian braid groups*, MFAT 4 (1998), no.2, 66–75, MR1770817; and *On some extensions of Artin's braid relations*, Contemporary Mathematics 233 (1999), 221–233, DOI 10.1090/conm/233/03432. This reviewer independently authenticated the former at the official journal page, which currently says full text is Coming Soon; the latter is an authenticated lead supplied to the review, not a theorem personally read here. [Official MFAT entry](https://mfat.imath.kiev.ua/article/?id=71), [AMS DOI](https://doi.org/10.1090/conm/233/03432).

ROOT's separate priority agent is pursuing the full follow-ups. Until they are read and compared, absence of an earlier full formulation, or a novel independently verifiable contribution meeting the user's goal, is not established. A no-priority disclaimer is accurate but does not resolve the user's novelty requirement. This review performed no exhaustive literature-absence proof and grants no first-priority approval. This remains separate from F01 and the verified mathematical resolution.

## PDF, metadata, licenses and portability

All five published pages were rendered and individually inspected. The schemes, signs, indices, proof, support counterexamples and bibliography are readable with no overlaps, clipped text, broken glyphs, or visible overflow. Page numbering is consistent. The actual ZIP TeX compiled with Tectonic, PID 67745, exit 0. Neither supplied nor rebuilt log contains overfull/underfull boxes or undefined references; the sole real warning is the harmless UTF-8 engine ignoring `inputenc`.

The rebuilt PDF has the same complete extracted text and **exactly identical pixels on all five pages at 100 dpi**. Its PDF-byte hash differs because the creation time differs; PDF bytes were not claimed reproducible. The published metadata title/author are correct and CreationDate is UTC 2026-10-04 01:05:39. Author/ORCID and all nine embedded web links match the source. `ARTIFACT_CONSISTENCY.json` records both PDFs, character bounds, text/pixel checks and links.

Deposit file paths are relative basenames and resolve to the intended PDF and v2 ZIP; the metadata clearly says preprint, unrefereed, extensive AI use, no formal/human review and no priority/present-openness claim. The CC BY 4.0 text and MIT Python scopes are explicit both in license files and the deposit description despite the single record-level CC license field. The package redistributes no third-party source body or scan. No local paths, credential patterns, DOI placeholder, private key or personal data beyond the intentional public author/ORCID were found in the released payload. Audit scans/raw records remain ignored; `git check-ignore` confirmed that boundary.

The diagnostic code is standard-library Python and made no network or file writes. The ZIP builder verifies members, normalizes permissions/order/time, reads them back, and refuses overwrite. TeX has its bibliography inline and no external source/image input. Compiler/fonts and transitive installed libraries were not vendored by this audit; runtime executable pins and page readback document the actual local reproduction without claiming universal compiler-byte identity.

No Git index/refs, package payload, native editor, remote PR, Zenodo or Sheets were written. No external person was contacted. ROOT owns repairs and any publication decision.
