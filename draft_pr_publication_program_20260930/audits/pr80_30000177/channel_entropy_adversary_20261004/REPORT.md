# PR80 independent channel and entropy audit

**Verdict: PASS for the original candidate's affirmative asymptotic LOCC-DC claim.** No mathematical defect was found within the assigned channel/entropy/physical-instrument approach family. No repair or new central proof search was required. Audit completion: 100%.

The verified claim is C_LOCC(W4) >= 3/2+h(1/4)>2 bits per shared copy, with separate local unitary sender codebooks and the designated transmissions A1 to B1 and A2 to B2. The explicit interior independent-message pair (9/8,9/8), total 9/4, is asymptotically achievable with vanishing average error by the cited established theorem. W4 is not LO-DC in the original shell convention. Priority, novelty, optimal capacity, finite blocklength performance, one-copy accessible-information advantage, and zero-error distinguishability were not audited or promoted.

## Immutable scope and independence

- Target: problem30000177 / OWR-785-003, the report's question about four-qubit W membership in the LOCC dense-codeable class.
- Original/current submitted head: dcfeb5d8ad68b397ec509c70e85c6fca46cd01e3.
- Candidate: original_head/unsolved_math_prioritization/attempts/30000177/CANDIDATE.md from the authenticated custody folder; Git blob 7adfc78adb9561d2fdaaa091559de190cf13f673; 11679 bytes; SHA256 fb8646bbe3cd8512ec7736fc180fa08a76740ac8b0dbb60b539a0320328c6404.
- Historical ledger supplied by ROOT: literally claimed_solved, 1/5; treated as immutable data, with no turns, native queue/status/PR/Git/index/main/editor/publication/outreach modifications.
- All new files and computation outputs are confined to this dedicated assigned audit folder.
- FIRST_SOURCE_ONLY.md was fixed before candidate exposure: SHA256 44d709b8b9997d383453938445edbadff0c6fc722ec49407714182d2591656f9, 6153 bytes, UTC 2026-10-04T21:46:58.669101Z. FIRST_CANDIDATE_VERDICT.md was fixed before author-checker exposure: SHA256 980c9f8fcb7330822ed43d766e628be25e2279498c31c9b6d40571cc95d00d81, 5287 bytes, UTC 2026-10-04T21:52:06.712924Z. Both FIRST files remain byte unchanged.
- No sibling conclusion, ROOT mathematical conclusion, author review, author SOURCES, or author priority assessment was read. The author checker was inspected/run only after the independent first verdict had been fixed. ROOT was informed after the first verdict freeze.

## Source calibration and actual computations

The original report pp.203-205 and the Bruß2004 published PRL, Bruß2004 arXiv v3, and Bruß2005 original were independently extracted with byte/input pins. Printed report pp.203-205 and relevant classification pages were visually checked. The standard W definition was followed through PRL's Dür-Vidal-Cirac citation to primary Eqs.(29)-(31), including its explicit normalized W4. Source-only exact arithmetic verified all one- and two-qubit marginals, rank/eigenvalues, and all 24 tensor permutations before reading the candidate.

source_calibration.py independently verifies the normalization and marginal baseline. independent_channel.py constructs all sixteen input pairs and all sixty-four output blocks from actual signed Pauli matrices in physical order A1,A2,B1,B2. It independently crosschecks an explicit tensor permutation, signed Bell-basis preimages, the full Bell orthogonality/completeness relation, Pauli unitarity including XZ, all matrix units for the Pauli twirl, normalized output traces, exact characteristic polynomials in the complete sixteen-dimensional cq space, formal entropies, conditional mutual information, and every two-copy projection (4096 checks). The complete output includes the integer amplitude vector and probability of every branch.

| State | Nonzero eigenvalues | Rank / dimension | Entropy, bits |
|---|---|---|---|
| fixed x,y output | 1/2; 1/4 twice | 3 / 16 | 3/2 |
| fixed x, averaged y | 1/4 twice; 1/16 eight times | 10 / 16 | 3 |
| fixed y, averaged x | 1/8 eight times | 8 / 16 | 3 |
| average x,y | 3/32 eight times; 1/32 eight times | 16 / 16 | 5-(3/4)log2(3) |

Both conditional MAC information quantities are 3/2; the joint bound is 7/2-(3/4)log2(3)=2.311278124459133. The strict interior test uses 27<32 exactly. All branch weights are included; a zero block contributes zero entropy without ever dividing by its trace. XZ's non-Hermitian real representative has the correct transpose adjoint and differs from Y only by a scalar phase. The both-Bell negative control independently returns exactly 2 bits.

Actual independent checker process: PID 89449, exit 0, UTC completion 2026-10-04T21:49:56.145980Z; stdout 11692 bytes, SHA256 518a4294fcf017865d9ff2f5a09a4c495308a8d9a51ddc57648891bddbd4e8a5. Full streams, argv, cwd, UTC, PID, source snapshots and input snapshots are under process_evidence/independent_channel. Python was launched with -E -B and active assertions. The independent code imports only standard-library modules.

## Finite algebra versus asymptotic achievability

The local Bell instrument is complete and trace preserving. Each sender encodes on its own qubit; each measurement occurs only after the designated qubit reaches B1. Its outcome is delivered classically to B2. Independent tensor resources and copywise instruments produce a finite memoryless cq MAC whose entire output Q=JR is at B2. Pinching the theorem's POVM by the classical J^n basis preserves probabilities and gives conditional local POVMs on R^n. No inter-receiver quantum system or extra entanglement is used, and no measurement outcome goes to a sender.

The asymptotic existence step is Winter's established cq MAC direct coding theorem, independently read from quant-ph/9807019v3, Sec.II and Theorem9 pp.4-5, after candidate exposure. Its independent inputs, product prior, finite output, memoryless extension, separate codebooks, output POVM and vanishing average-error convention match this physical channel. This audit checks applicability; it does not substitute finite entropy calculations for the theorem or numerically simulate asymptotic codes. DERIVATION.md supplies the complete algebra and physical bridge.

## Author comparison after independence freeze

The original author checker was then copied byte exactly into author_run and executed there with an assertions-active wrapper and -E -B. SHA256 f63d1593dc997ad14a83cf295e37a86d23295d7adcb57e0f84552c0d358cdec1, 6699 bytes. It reports PASS with 903 exact assertions, agreeing on the states, spectra, entropies, information values and both-Bell control. Actual process receipt: process_evidence/author_checker_run, PID91752, exit0, UTC2026-10-04T21:53:11.280906Z. This comparison is corroboration and did not change the independently fixed verdict.

## Remaining issues, boundaries and evidence hygiene

No unresolved technical defect remains in this audit's assigned scope. The strongest verified conclusion is the stated asymptotic strict gain and shell membership. The exact optimal C_LOCC, constructive finite blocklength decoder performance, any one-copy gain, experimental implementation and novelty/priority remain outside scope. The historical ledger/accounting and whole PR readiness remain ROOT's responsibility; this verdict is not a ledger/status mutation or an independent assessment of unpublished novelty.

One source fetch attempted nonexistent Dür v3 and failed; a separately recorded successful unversioned fetch returned v2. Winter page rendering returned a harmless Type3 glyph bounding-box warning, with all theorem text legible. During source-first preparation, ENOSPC temporarily prevented record creation. Only byte-identical redundant files inside this audit were hardlinked, reclaiming 1398156 logical bytes while retaining snapshot paths and exact full content. A failed hardlink of a zero-byte stderr was immediately restored to the empty bytes matching its existing receipt. No required evidence was discarded. All substantive subprocess receipts and stream hashes are preserved; evidence_manifest.json records current byte identities. No pyc files were produced.
