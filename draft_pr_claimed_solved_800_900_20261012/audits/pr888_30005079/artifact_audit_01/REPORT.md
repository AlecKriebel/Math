# PR888 / PID30005079: independent artifact and reproduction audit

This audit authenticates and reproduces the frozen 21-file package at Git head `a7571ddbbbe2de3600b96bd7ccccf86e4d5748e7`. The normal publication driver succeeds, both regenerated check-result files exactly match their originals, and an independent implementation validates the correction chain and exact endpoint certificates. The original driver deliberately rejects optimized Python. Neither this report nor successful execution constitutes a full mathematical verdict, a new mathematical acceptance, or a novelty determination.

The native target asks for an explicit nontrivial canonical degeneration of a Fano variety with a nondivisorial entropy-minimizing valuation. Its mathematical success criteria require the geometric construction, a genuine nondivisorial valuation, the actual canonical degeneration, and global minimization. The code covers only the auxiliary arithmetic described below. The original `claimed_solved` classification and research effort `1/5` are not changed by this artifact review.

## Independence and provenance

The attack plan was frozen at 2026-10-16T05:18:48.908137+00:00, before executable source or proof inspection. Its SHA256 is `d89459cd8a1714c6be94af393fa5507d2b428927a54fcd7e0b0186fcf6cac00b`, 2,925 bytes. The target native pair was read first. The parent's receipt reports full hashing of all three native corpora before target extraction; this audit does not claim to have repeated those large-corpus checks.

Limited verdict blinding is disclosed: reading the packet's reproduction instructions in `PUBLICATION.md` exposed its historical two-acceptance disposition before the preliminary assessment. The stored historical check-result claims were also read. The actual full acceptance reports A and B were withheld until the independently frozen preliminary artifact assessment at 2026-10-16T05:23:11.936762+00:00, SHA256 `0ce397ac27fb7333baef41edbea926e410f4dddc7626da12f899cf0a6b4b0d8b`, 3,626 bytes. The checks and negative controls reported here come from actual execution and source inspection, not those historical verdicts.

`SOURCE_AUTHENTICATION.json` records independent read-only Git `ls-tree` and actual `cat-file blob` authentication. Every one of the 21 extracted files matches its actual immutable Git blob bytes, Git object identifier, SHA256, byte count and head-tree mode. All tree modes are `100644`; extracted permission bits were also recorded. The exact total is 98,055 bytes. The head tree, external inventory and extracted inventory agree with no extra or missing file. The external source manifest itself is SHA256 `49a72d6bf90d3a74be69ed855c7a9cfc0f3b1d83a4e4e3ce997c0ca7c07d1cbc`, 5,587 bytes. This external manifest is distinct from the original packet's bibliographic `SOURCE_MANIFEST.json`.

All three Python executables were fully read before execution: the publication driver, author checker and reviewer-B checker. The inventory contains no other executable or launcher. All execution and all mutations used this audit's own private copies. The original extracted source was not executed in place. Exact before/after source inventories are retained in `REPLAY_RECEIPTS.json`; the final receipt reconfirms them. No candidate, Git index, branch, reference, configuration, remote, publication or release was modified by this audit.

## Actual reproduction

The current replay used Python 3.14.6, SymPy 1.14.0 and mpmath 1.3.0. This extends the demonstrated environment beyond the packet's historical Python 3.12.14 claim; it does not independently establish that historical run.

| Actual run | Exit | Observed result |
|---|---:|---|
| Original driver, normal Python | 0 | 21 files, four editions and three correction links verified; both regenerated result JSONs byte-identical |
| Original driver, actual `-O` | 1 | Explicit rejection: `Run with assertions enabled, without -O or PYTHONOPTIMIZE` |
| Author checker, normal Python | 0 | Regenerated 1,614-byte original result exactly |
| Reviewer-B checker, normal Python, supplied expected proof layout | 0 | Regenerated 5,514-byte original result exactly |
| Author checker, actual `-O` | 0 | Same result bytes, with assertion checks removed |
| Reviewer-B checker, actual `-O` | 0 | Same result bytes and PASS text, with assertion checks removed |

Normal and optimized direct-checker runs are observations, not equivalent validations. Each checker has 13 syntactic `assert` statements. On Python 3.14, normal compiled assertion-load opcode counts are 13 for the author and 14 for reviewer B; both counts become zero when optimized. The reviewer additionally loses its candidate-proof read and hash check because that entire expression occurs inside an assertion. The driver uses explicit `require` calls and refuses optimization before doing its work.

Two controlled demonstrations establish the practical difference. Removing the reviewer's expected candidate proof makes its normal invocation fail with `FileNotFoundError`; its actual optimized invocation exits zero and prints that the candidate hash is unchanged. Changing one author fan normal from `(1,0)` to `(2,0)` makes the normal checker fail its determinant assertion; the optimized checker exits zero and emits `toric_fan_unimodular: true`. Those modified checkers were tested directly, outside the intact driver's hash gates. They do not show that the original normal driver accepts these mutations.

The driver itself did not change its private packet copy. It creates a temporary layout, copies the exact proof to the reviewer's expected `authored/PROOF_CANDIDATE_v4.md`, runs each unchanged checker with `sys.executable -B`, requires a zero exit code and compares regenerated JSON bytes against their frozen originals. The reviewer checker is layout-dependent when run directly; the original driver supplies that layout correctly.

A subprocess audit hook observed both child command lines. A separate harmless externally located `PYTHONPATH` startup probe measured the actual root and both children: `optimize=0`, `isolated=0`, `no_site=0`, and bytecode disabled. The external startup hook ran in all three processes while the original full replay still succeeded. Thus the temporary layout provides relocation and limits packet writes; it is not Python environment isolation or an operating-system sandbox. The earlier subprocess-hook field showing an empty explicit environment did not mean inherited environment variables were absent. `CHILD_ENVIRONMENT_RECEIPT.json` is the actual flag measurement.

## Exact certificates and mathematical coverage

The original normal runs actually check two symbolic exponential-moment identities, density masses 5 and 4, first moments 5/12 and 2/3, exact rational Taylor endpoint signs, four toric determinants and polynomial coprimality. Reviewer B additionally checks a toric slice/barycenter identity. The author's five sampled resultants concern ratios `(1,1)`, `(1,2)`, `(2,1)`, `(3,2)`, `(2,3)` and have degrees 12, 18, 18, 30, 30. These finite samples do not establish an all-denominators statement. The author's `len({1,2,3,4})==4` assertion is a literal finite tautology and supplies no further geometric evidence.

The author's displayed decimal enclosure endpoints round to the same shown number on each side. Its source nevertheless makes its sign comparisons using exact rational sums and remainder bounds. Reviewer B's JSON retains the full distinct rational endpoint fractions.

`independent_certificates.py` does not import either original checker. Using only standard-library `Fraction` arithmetic, it independently integrates the supplied polynomial pieces, derives the exact L1 values 9/4 and 2, recomputes all four degree-32 endpoint enclosures, matches every full stored fraction exactly and confirms the required strict signs. It checks the Taylor hypothesis `0 < t*radius < 1` at each endpoint. The elementary bound `exp(1)<3` is justified by comparing `1/k!` for `k>=2` with `2^(-(k-1))`, strictly for `k>=3`. No floating-point value is used by these independent endpoint checks. This validates the finite certificates for the displayed densities; it does not authenticate that those densities are the geometrically required ones.

The scripts do not certify the all-rational-ratios valuation-at-infinity proof, smooth/Fano and singular/klt geometry, the real filtered Segre-ring identification, canonical discrepancy shift, finite generation for the full filtration, the singular product-soliton argument, applicability of cited existence/stability theorems, global minimization over all valuations, or canonical uniqueness. Those are mathematical proof and primary-source obligations. This audit identifies their location and does not replace them with successful arithmetic or historical audit prose.

## Manifests, edition chain and source references

The author's `PACKAGE_MANIFEST.json` authenticates 11 named files and explicitly excludes itself, giving a 12-file original author package. Its own exact bytes are pinned in the publication driver. The publication manifest authenticates the other 20 packet files and excludes itself, yielding the 21-file packet. All recorded hash/size pairs independently match their actual files.

The original driver reconstructs v2 by reversing the combined v2-to-v4 citation patch, v1 by reversing the v1-to-v2 numerical patch, and v3 by reversing the v3-to-v4 polystability patch. It authenticates the four edition hashes and sizes and replays the three links forward. The edition history's v2-to-v3 descriptive change does not imply a separately stored v2-to-v3 patch; the actual stored combined v2-to-v4 patch is accurately identified by the publication guide and patch-verification records.

An independent system implementation, Apple `patch 2.0-12u11`, applied all three actual links in both directions with zero fuzz. All six transformations produced the exact expected edition SHA256 and byte count. This avoids relying solely on the packet's own custom patch parser.

The original bibliographic source manifest lists six absent PDFs with hashes, byte counts totaling 3,425,423, and inspection labels, plus one web-only primary source without a byte pin. These source copies are intentionally not distributed. This artifact audit authenticates that metadata as original Git bytes and checks its scope; it does not claim to authenticate absent scholarly bytes or to reverify the cited theorems. Those checks belong to the separate primary-source review. No raw primary source, corpus, render or private coordination file is included in this audit's safe inventory.

After the preliminary assessment was frozen, both original full audit reports were read. Both refer to the exact current proof hash, and reviewer B's pinned v3 hash and v3-to-v4 patch hash match the reconstructed chain. Their normal arithmetic-reproduction claims agree with the present observations. Their full mathematical acceptances and assertions about historical independence are preserved historical claims; they are not promoted into a new acceptance by this audit. The original stored negative-control report contains historical claims, not test implementations or full raw receipts; the new named controls below are separately recorded observations.

## Bounded negative controls and limitations

`MUTATION_RECEIPTS.json` records 24 actual integrity-only controls. Twenty reject: malformed JSON syntax, empty inventory, duplicate file entries, malformed SHA256, negative length, traversal and absolute paths, changed proof, changed proof with only the outer manifest rebound, changed author or reviewer checker with outer rebind, damaged patch with and without outer rebind, changed bibliographic metadata with outer rebind, missing source metadata, missing audit, extra file, extra directory, symlink, and omission of a file together with its outer-manifest entry. Some path controls reject at inventory comparison before reaching the explicit path-safety check; the receipt does not attribute them to a later check they never reached.

Four controls accept:

- A duplicate root `files` key is parsed with last-key-wins semantics; the final value is the original valid inventory.
- An unrecognized field containing nonstandard JSON `NaN` is ignored.
- Changing a file's filesystem permissions is not detected by the packet's byte-only integrity model.
- Changing the driver and rebinding its hash in the self-excluded outer manifest permits a harmless added driver marker to execute and the integrity-only invocation to succeed.

The last control establishes the unanchored trust-root limitation of executing a self-checking packet. It does not bypass the independently authenticated immutable Git head or an externally trusted manifest digest. The packet correctly describes its manifest as integrity metadata rather than a signature. These finite controls do not establish general security, hostile-filesystem race resistance, complete schema validation or safe execution of arbitrary code.

Four direct parser probes were also run outside the intact hash gates. A header-only patch, bad counts and wrong context are rejected. An inconsistent new-file hunk coordinate is accepted and the text change is applied: forward application does not validate that coordinate. The actual original patch bytes remain authenticated, and all actual transforms also pass the separate zero-fuzz system implementation. Thus this parser limit is not evidence of damage to the frozen correction chain.

## Execution incidents and remaining scope

The default and bundled interpreters initially lacked SymPy. The first private pinned install, with package caching disabled, failed with `Errno 28` after an initial free-space measurement of 201 MiB, while creating the optional `isympy` entry point. Only this audit's own generated bytecode was removed: 151 directories, 30,190,065 bytes. Imports then succeeded. Local installed RECORD checks found all 1,568 hashed nonbytecode SymPy files and all 93 hashed nonbytecode mpmath files present and matching; this is not an independent downloaded-wheel provenance attestation and does not turn the failed install command into a successful one.

The initial replay harness mistakenly resolved the venv executable symlink to the base interpreter, causing missing-SymPy failures and a final `CalledProcessError`. That harness mistake was corrected before the successful replay. A zero subprocess exit is now required before a frozen-result byte match can count as reproduced; preexisting result files are not treated as execution evidence. An initial bytecode probe looked only for an older assertion opcode, reported zero and was corrected to include Python 3.14's actual `LOAD_COMMON_CONSTANT(AssertionError)` instruction before finalization. These incidents and their corrections are recorded explicitly.

The strongest artifact result is exact immutable-source authentication, successful normal replay, independent correction-chain reconstruction and independent exact finite certificates. The exact remaining mathematical gap for this audit is all of the non-arithmetic proof and primary-source applicability listed above; it renders no full mathematical verdict. Packaging limitations are permissive JSON parsing, external trust anchoring, ordinary environment inheritance, byte-only filesystem integrity and the documented optimization restriction. The parent audit owns any later portable wrapper; no candidate repair or new publication was attempted here.

The safe manifest explicitly excludes itself, its companion external-pin receipt, all scratch/runtime/dependency bodies and the original source directory. It includes only this audit's authored report/code and sanitized receipts. Its SHA256 and byte count, and this report's SHA256 and byte count, are supplied in `EXTERNAL_PINS.json` and in the audit handoff. These hashes are reproducibility pins, not signatures.
