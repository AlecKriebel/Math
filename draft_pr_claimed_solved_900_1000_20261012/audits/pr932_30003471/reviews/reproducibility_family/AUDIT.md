# PR932 / 30003471 — independent reproducibility and hostile-verification audit

Audit date: 2026-10-15 UTC. This family reconstructs the code's actual scope, authenticates the frozen packet, reproduces its computations and challenges its verification boundary. It does not adopt a historical mathematical acceptance label as evidence. Original author accounting is 1/5; this audit and its separate packaging repair add zero author proof-search turns. No substantive mathematical proof repair was made. No external person, other shard, or other current audit family was contacted.

## Disposition

**The frozen files authenticate and their finite diagnostics execute, but the legacy exact full-replay gate rejects on this platform.** The rejection is retained in every tested parent mode. A separate current gate passes with a precisely disclosed, single-field bounded comparison. No original file was changed. The historical exact-replay result is not relabeled PASS.

The discrepancy is confined to `numeric_max_jacobi_error`, the maximum error of a sampled finite-difference check against the spherical Jacobi formula:

| Quantity | Value |
|---|---:|
| Historical saved maximum | 1.3423678835167152e-10 |
| Current maximum | 1.5367479511141369e-10 |
| Original per-sample validation bound, strict | 3e-7 |

After the already documented omission of nine external-PDF hash checks and addition of the explicit `NOT_RUN_NO_SEPARATELY_SUPPLIED_SOURCES` field, every other independent-result key, type and value matches. The error maximum is a nonproof diagnostic. Its changed final bits do not falsify the sampled inequality, much less the universal mathematical theorem. They do falsify a claim that this platform reproduces the complete historical independent receipt exactly. The platform mechanism of the last-bit difference was not isolated to a particular library operation; this report does not claim that it was.

The strongest mathematical result of this family is finite algebraic and numerical consistency evidence, including explicit failure examples when hemisphere or interpolation conditions are removed. This family neither proves nor independently source-verifies the universal Dirac/trace/compactness theorem. Mathematical acceptance remains conditional on the other required mathematical and primary-source checks. No priority, firstness, openness, or publication finding is made here.

## Independent reconstruction and static review

`INITIAL_RECONSTRUCTION.md` was written before reading historical audit narratives, saved verdicts and acceptance prose. The original programs necessarily contain some acceptance strings and constants; those were read as code, not accepted as mathematical conclusions. The complete charter, selected source record, proof, all six Python programs, portable patch, and all remaining original files were read before executing any original program. `STATIC_REVIEW.json` records the six programs, imports, hashes and zero AST assertion nodes.

The exact mathematical candidate is stronger than the original target. Given compact full-dimensional convex three-polytopes P and Q with a fixed face-lattice correspondence, all weak inequalities between corresponding interior dihedral angles are claimed to imply equality of the complete outward-unit-facet-normal Gram matrices. Reversing the ordered pair would rule out all-strict dominance and imply the original one-edge weak comparison. Nonsimple vertices are included; support numbers, edge lengths and full metric congruence are not conclusions.

The proof's mechanism is a compatible degree-one hemisphere map, smooth convex inner approximations, exact fractional-arclength contraction in two-active-facet regions, logarithmic cutoffs near all vertices, a vanishing L2 error on the actual moving boundary, uniform H1-to-L4 trace control, a smooth-domain Dirac index/energy result, a nonzero constant limit and Clifford intertwining. Code cannot supply those universal analytic steps. In particular an exact finite commutant sample is not Schur's lemma, a planar integral is not the full actual-boundary estimate, and an octahedral or pyramidal sample is not a universal localization proof. The original proof and code explicitly say finite computation is diagnostic only.

`public/controls.py` performs 5,066 checks: Clifford and boundary identities on finite integer samples, sampled commutants, finite target logic, sampled hemisphere dilation and planar cutoff rates. `audit_b/independent_controls.py` and its portable adapter provide 4,137 nonsource checks using exact symbolic algebra and numerical samples. The original historical script also requires nine source PDFs and a historical sibling layout, producing 4,146 checks in its recorded environment. The portable patch changes only input paths, CLI handling and optional external source hashing; the complete mathematical computation body is unchanged. The frozen full-publication check-only gate confirms the exact diff.

## Immutable identity and closed inventory

The independent authentication used actual local Git objects, not merely the root audit's JSON or a self-published manifest:

* Immutable head: `c09ef9df8b1f4642be0396ba6343344be8fa25b0`.
* Exact Git subtree: `unsolved_math_prioritization/attempts/30003471`.
* Actual Git blob count and disk regular-file count: **29**.
* Exact relative directories: `audit_a`, `audit_b`, `public`; no additional directory or file.
* Every Git mode is `100644`; disk files are `0644`, directories/root `0755`.
* Proof: 21,855 bytes; SHA256 `6015fcacefd914217ddadc816a5c84c1be250ec58838df891f267835f9198415`.
* Outer manifest: SHA256 `d1b3a0528bf518640a117c2cfecff5bc81d21f58632f7b4f647ae998eb4dcedd`.
* Independent all-29 snapshot: SHA256 `f05112fa43eb99a0c9cd4687b14beeef5eb4d190dcebae9b15c1d84c9acc656f`.

`PINNED_SNAPSHOT.json` contains all 29 byte counts, SHA256 hashes, actual Git blob OIDs and Git modes. `AUTHENTICATION_START.json` and `AUTHENTICATION_END.json` bind closed inventories and confirm actual Git agreement. The independently reconstructed records also agree with the supplied root authentication record. The shared branch remains main; no checkout, index, branch, commit, push, service, PR, Zenodo, Sheet or native-ledger action was performed.

`PACKET_GUARD.py` validates the externally pinned snapshot, exact regular-file/directory inventory, exact modes and every byte before execution. It rejects lexical dot/parent/double-slash paths, root and ancestor symlinks, file/directory symlinks, unexpected empty directories, FIFOs and sockets. Special entries are rejected before opening them. File reads additionally use lstat/fstat regularity, bounded reads and available no-follow/nonblocking flags. This is a serial local check: it does not defend a check/use race against a concurrent attacker, malicious trusted runtime, or replaced external bootstrap anchors.

## Actual legacy reproductions

The six original entry points were each run from authenticated disposable copies under four parent configurations: ordinary Python, `-O`, `-OO`, and a nonisolated `-B` parent inheriting `PYTHONOPTIMIZE=2`. Python environment variables are otherwise removed. The first three configurations use `-I -B`; isolated child invocations ignore Python environment injection. Every copied Python file and all 29 packet members authenticate before each direct original entry point, and closed inventory/bytes are rechecked afterward. Deliberate direct boundary experiments are explicitly identified below and authenticate all copied executing code after changing data.

| Original entry point | Result in each of four parent modes |
|---|---|
| `public/controls.py` | Exit 0; all 5,066 checks; stdout byte-identical to `CONTROL_RESULTS.json` |
| `public/verify_packet.py --self-test` | Exit 0; 5,066 checks and 19 rejected negative cases; saved result recursively exact |
| `PORTABLE_INDEPENDENT.py` | Exit 0; 4,137 checks; exactly one disclosed numerical maximum differs |
| `audit_b/independent_controls.py` directly | Exit 1, expected `FileNotFoundError` for absent historical sibling `polytope_dihedral_30003471/packet/MANIFEST.json` |
| `VERIFY_PUBLICATION.py`, full replay | Exit 1: `REJECT: Independent replay differs beyond disclosed source selection` |
| `TEST_MUTATIONS.py` | Exit 0; stdout byte-identical to saved 132-case `MUTATION_RESULTS.json` |

The historical author receipt stores a parsed result, not raw historical stdout. The new run exactly matches that result with recursive types, and its stdout equals the canonical reserialization of that result. This is distinguished from raw-byte equality to a saved stdout artifact. The 343-byte author control receipt and 12,263-byte mutation receipt really are raw stdout byte-identical. Their SHA256 hashes are respectively `9a086794385467668ae9aeec3f33bef5802127249a1fb580532010b8eb606c3f` and `8af53ec18e15d0573bba9a197bdd81bf3fc14877800ea852c87b1d73aef5b6a9`. The canonical author self-test stdout hash is `161b18f0d373885857088251db5f0b05f8c22f9c3ad89376311019bf859a93c7`.

Each original mutation-harness invocation actually executes 44 cases in each of its three child modes: 132 cases, three clean acceptances and 129 controlled rejections. The four parent invocations reproduce the same saved stdout. Cases include malformed/duplicated/nonfinite JSON, exact integer typing, unsafe paths, inventory/mode drift, symlinks, a FIFO, unsupported claims, frozen inner anchors and independently pinned wrapper replacement. These checks authenticate the wrapper outside the mutable packet before execution. They do not prove the mathematics or defend replacement of both external anchors.

The historical B script's layout failure is documented, rather than hidden by rewriting it. No source PDFs are included or were separately supplied. This family therefore does **not** claim to reproduce the original nine external source hashes or the full 4,146-check source-bearing historical run. The portable result transparently reports 4,137 checks and the nine omissions. Source titles/URLs/hashes in output are expected metadata, not fresh verification of PDF contents.

## Independent hostile controls and actual trust limits

The current suite runs **92** actual disposable-copy cases across four parent modes: four clean acceptances and **88** controlled rejections. Every test mode first executes a positive marker control to demonstrate that the marker can really execute. Altered copies of all six entry points, including changed checker and mutation-harness code, are rejected before their untrusted markers run. Actual `assert False` payloads are also rejected before execution under all four parent modes. Their rejection does not depend on an assertion remaining active. The suite separately verifies that explicit exceptions still fail under optimization and that an optimized parent starts an unflagged `-I -B` child at optimization level zero. No untrusted marker executes.

The independent cases cover rebound proof/outer metadata, missing/extra files, empty directories, file/directory modes, file/directory/root/ancestor symlinks, noncanonical paths, FIFOs and Unix sockets. No special-file read blocks. An additional read-only copy authenticates all 29 files at `0444` and directories `0555`; two actual write probes fail under UID 501. Both the legacy check-only publication gate with the readonly profile and the author verifier run on that copy without changes. Permission denials are useful integrity evidence under this ordinary user, not an OS sandbox.

Three direct legacy-boundary witnesses are retained:

1. Without the full packet gate, the portable script accepts changed `SOURCE_METADATA.json`, echoes a boolean source byte count and an unsupported hash, and prints `pass: true` while still saying source verification was NOT_RUN. Its executing code was separately authenticated. The fixed all-29 guard rejects this data mutation. It is a standalone metadata-authentication limit, not a bypass of the fixed frozen publication gate.
2. The legacy full gate's check-only mode accepts the authentic packet through a symbolic ancestor. No changed payload is accepted. The current guard rejects the ancestor before any original code is run.
3. The legacy JSON parser rejects literal `NaN`/`Infinity` but accepts `1e999` as an infinite float. The pinned frozen JSON contains no such value, so this is not a demonstrated fixed-anchor packet bypass. The new parser recursively rejects overflow as well as literal nonfinite constants, malformed JSON and duplicate keys. Its exact-type comparison distinguishes integers, floats and booleans.

These are distinguished from the legacy strict numerical-receipt rejection. The old verifier's need for an externally authenticated checker and external manifest is documented and sound within its stated trust model. A checksum supplied by the same mutable attacker-controlled metadata cannot bootstrap trust; no new report claims otherwise.

## Separate current gate and its validation

`RELEASE_GATE.py` is a new artifact; it does not edit, impersonate or replace `VERIFY_PUBLICATION.py`. Before every original entry-point execution it authenticates all 29 copied files against the fixed independent snapshot. It runs the old identity-only gate, author self-test, raw author controls and portable independent controls in three explicit isolated child modes. Its own parent was tested normally, with `-O`, with `-OO`, and with inherited `PYTHONOPTIMIZE=2`.

The only relaxed equality is the **value** of `numeric_max_jacobi_error`. Both historical and current values must be exactly Python floats, finite, nonnegative and strictly below the original `3e-7` test bound. The exemption is not a global tolerance or schema weakening. All other keys, types and values remain recursively exact, including every count, status, proof/manifest/source pin, other numerical maximum and explicit noncertification flag. Nine omitted source checks are handled by the preexisting disclosed portable source-selection transform, not by a new exception. The gate reports both actual values, the bound, whether exact equality holds, its nonproof scope and the fact that the legacy exact gate has not been superseded.

Eighteen independent comparator negatives challenge altered theorem/status flags, count values and types, proof hashes, source-witness types, another numerical diagnostic, extra/missing keys, integer/boolean/negative/nonfinite diagnostic values, equality to and excess over the bound, and invalid historical values. All reject. The observed single-field drift is accepted. The repair is appropriate because it reruns the genuine underlying diagnostics and preserves their original validation bound; it does not waive a failed mathematical control or treat sample agreement as a theorem.

## Independent finite mathematical controls

The new suite performs **466** finite checks. These include integer-complex Clifford basis anticommutators/volume, the positive boundary branch, an explicit nonzero half-turn intertwiner and wrong-sign failure, removable zero-angle endpoint behavior, near-hemisphere endpoint bounds, and explicit expansion outside a hemisphere. The same-normalized-linear-weights endpoint example expands by approximately 1.869, and the nonhemisphere example by approximately 2.942. They support why the proof needs fractional arclength and a hemisphere margin. Logarithmic planar rate checks and a nonlogarithmic cutoff example distinguish the critical boundary scale; the H1-to-L4 pairing uses `1/2+2/4=1`.

The independent geometric model is the square pyramid

    x+z<=1, -x+z<=1, y+z<=1, -y+z<=1, -z<=1.

Its apex is `(0,0,1)` and its four base vertices are `(±2,±2,-1)`. Exact integer incidence gives four incident facets at the apex and three at each base corner. Opposite side facets meet only at the apex, testing the nonadjacent-pair case. Unit normals are used for smooth samples. An independent 128-panel composite-Simpson quadrature evaluates the actual infinitely flat double-integral bump, and radial bisection gives 51 actual level-set samples at lambda 100, 1,000 and 10,000. Forty-two have at least three active facets; 30 include a nonadjacent opposite side pair. Maximum sampled lambda times radial shift is about 2.164, and maximum sampled lambda times vertex distance is about 2.164. All relevant active-set and hemisphere diagnostics pass.

These are floating numerical samples, not interval-certified computations. The octahedral original has 396 actual smooth-level samples, 209 with at least three active facets. Neither model certifies arbitrary valence, nearly degenerate universal constants, trace/extension uniformity, moving-boundary L2 estimates, no loss of mass, or the Dirac index sign. Nearly flat positive normal-arc angles are included in the original numerical grid; degenerate zero/pi adjacent angles are outside the stated polytope theorem. The route that would promote samples or strings to a universal analytic certificate is blocked because it merely transfers the central difficulty to an unsupported claim.

## Runtime, bootstrap and reproduction

The executed runtime is Python 3.14.6, NumPy 2.3.5, SciPy 1.17.0 and SymPy 1.14.0 on the platform recorded verbatim in `REPLAY_RESULTS.json`. UID is 501. No library was installed or changed. The documented library versions match; bitwise numerical portability across machines is not guaranteed. A system Python entry point that requires an unaccepted Xcode license was unavailable, so the already available audit virtual environment was used. This is an environment choice, not a change to the frozen code.

First authenticate `VERIFY.py` using its independently supplied external SHA256. Obtain the independent digest of this folder's `MANIFEST.json` from the root audit receipt. The self-excluded map enumerates exactly 15 curated public artifacts and their byte counts and SHA256 hashes; `tmp/` is explicitly private and unauthenticated. Raw source bodies, caches, transient subprocess stdout and scratch copies are excluded. Neither an internally printed checksum nor running an untrusted verifier establishes its own trust.

With the already available scientific Python selected, an independently authenticated `VERIFY.py` can run:

    python -I -B VERIFY.py --expected-manifest EXTERNAL_PUBLIC_MAP_SHA256
    python -I -B VERIFY.py --expected-manifest EXTERNAL_PUBLIC_MAP_SHA256 --run --packet ABSOLUTE_ORIGINAL_PACKET --repository /Users/alec/Documents/Math

The first command checks the curated map without importing its other code. The second actually runs `REPRODUCE.py`: it authenticates actual Git/disk bytes, reproduces the original suites and expected failures, runs the hostile and mathematical controls, executes the separate current gate, and writes a fresh receipt under private `tmp/`. Its receipt expressly retains `EXACT_LEGACY_RECEIPT_MISMATCH`; successful completion of the independent pipeline does not make the old strict receipt identical. `REPRODUCE.py` can also be invoked directly after external authentication, with explicit packet, repository, scratch and output arguments. All work should remain in this family's scratch directory.

Subprocess calls are wall-time bounded, and the main replay children additionally receive CPU, output-file-size and file-descriptor limits. Bytecode writes and inherited Python injection are suppressed. These are reproducibility controls, not a claim of containment against malicious native libraries or concurrent attackers. The complete checkable outputs, code, exact pins, modes, receipt comparisons, bounded exception and limitations accompany this report.

## Remaining gap and promotion conditions

The historical exact full replay continues to reject on the tested platform. Any public promotion must disclose that fact and name the separate current bounded-diagnostic policy. That required reproducibility disclosure is addressed here without changing historical bytes. There are no required mathematical corrections established by this family, and this family alone cannot supply a full mathematical acceptance.

Universal validity still requires independent verification of the proof and applicable primary smooth-domain theorem: hemisphere construction/gluing, nonsimple localization, uniform radial transport and functional analysis, actual-boundary logarithmic L2 control, index/representation conventions, nonvanishing limit and facet traces. These are exact mathematical obligations, not tasks completed by these finite controls. Full external source hashing, firstness and deep literature priority were not performed. No publishable paper, ZIP, release metadata, DOI or outreach was prepared.
