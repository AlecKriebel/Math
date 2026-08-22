# Preliminary independent software-referee report

**Manuscript:** *Positive Recurrence for Single-Linkage Bimolecular Weakly Reversible Stochastic Reaction Networks*  
**Packet:** `bimolecular_positive_recurrence_ai_referee_packet_v1_2_4`  
**Track:** separated software review, before execution and before access to committed reports  
**Checkpoint timestamp:** 2026-08-21T22:22:09-07:00 (America/Los_Angeles)  
**Status:** PRELIMINARY STATIC ASSESSMENT ONLY

## 1. Information barrier and scope

I first read and visually inspected all 16 pages of
`bimolecular_positive_recurrence_submission_v1_2_4/manuscript/main_jap.pdf`.
I then read every line of the nine Python modules under
`code/src/bimolecular_pr/` (1,846 lines), every line of all seven test files
under `code/tests/` (868 lines; 57 statically identified test methods), and the
packaging and replay tooling named below. I also inspected the PDF-build,
release-manifest, archive-build, and release-tool safety scripts because they
are invoked by the packet runner.

I did **not** run the tests, verifier, package runner, or `RUN_ALL_CHECKS.sh` in
this preliminary pass. I did **not** open either copy of
`verification_report.json`, any manifest contents, `audit/`, `preservation/`,
`validation/`, research or revision logs, expert-audit material,
`supplement/reviewer_checklist.md`, prior mathematical/literature audits, the
packet build log, packet checksum list, or any expected/golden output file.
References below to golden reports and manifests describe only what the
scripts do, based on script source.

No contact or communication with any outside individual occurred.

## 2. Pre-review snapshot and provenance

### Supplied locations

- Packet root: `/Users/alec/Documents/Math/bimolecular_positive_recurrence_ai_referee_packet_v1_2_4`
- Submission root: `/Users/alec/Documents/Math/bimolecular_positive_recurrence_ai_referee_packet_v1_2_4/bimolecular_positive_recurrence_submission_v1_2_4`
- Journal PDF: `/Users/alec/Documents/Math/bimolecular_positive_recurrence_ai_referee_packet_v1_2_4/bimolecular_positive_recurrence_submission_v1_2_4/manuscript/main_jap.pdf`
- Software root: `/Users/alec/Documents/Math/bimolecular_positive_recurrence_ai_referee_packet_v1_2_4/bimolecular_positive_recurrence_submission_v1_2_4/code`

### Environment

- Operating system: macOS 26.5.2, build 25F84; Darwin 25.5.0, arm64.
- Python: CPython 3.14.6.
- Tectonic: 0.16.9.
- The packet root contains no `.git` directory. `git -C <packet> rev-parse`
  resolves only because the packet is sitting inside the larger
  `/Users/alec/Documents/Math` checkout. The copied packet therefore does not,
  by itself, establish a commit or tag.

### Independently computed hashes

- `manuscript/main_jap.pdf`:
  `77b4f098a1f0655ed4e04423caccec79a051cf11297b17d5fa2d630d539e7c4d`
- `manuscript/paper_content.tex`:
  `00c0d9f2b281d6f36a388ff45776d9f90f9d6388dce0e83d9eb7b6aa80a4deba`
- `manuscript/references.bib`:
  `00bd5723e1c518841e94e8bd02637c709b0295891f191ed65dffbcc10a034e61`
- `RUN_ALL_CHECKS.sh`:
  `579383c84cae29c0b2c62e41bbbb0254dfa1cd0b5e3e968f6e85899c5bb4944e`
- `code/reproduce.sh`:
  `4dd4055c2e6d15e498589a0822a692d052c9f4468704ab7b00609b7118467fac`
- SHA-256 of the sorted hash inventory for every source, test, packaging, and
  release-tool file inspected in this pass:
  `bfd8291b868b3aff7a5339d8c896545cb2a59662a727c3864a88e231426553a8`.
  The per-file inventory is reproduced in Appendix A.

### Release-tag availability

The manuscript says the supporting material is available in the “tagged
Version 1.2.4 repository directory” (`paper_content.tex:1139-1145`, journal PDF
p. 14). The containing checkout's tag list ends at
`bimolecular-positive-recurrence-v1.2.3`, and a direct read-only
`git ls-remote --tags https://github.com/AlecKriebel/Math.git
refs/tags/bimolecular-positive-recurrence-v1.2.4` returned no matching ref at
this checkpoint. Thus the packet content is inspectable, but the claimed v1.2.4
Git-tag provenance is not presently available. This is an exact artifact claim
discrepancy, not evidence for or against the mathematical theorem.

## 3. Manuscript claim to which the software is auxiliary

The theorem states that a finite stochastic mass-action network which is
weakly reversible, has one linkage class, and has every complex of molecularity
at most two has, for every positive rate vector and initial population, a
reachable set that is a closed communicating class; a nonabsorbing class has a
nonexplosive positive-recurrent minimal CTMC, while an absorbing singleton has
point-mass stationary law (`paper_content.tex:240-247`; journal PDF p. 3).

The manuscript accurately states that no computation is used in the universal
proof and that the finite checks are only reproducibility/falsification aids
which neither prove recurrence nor enumerate the analytic exceptional set
`K` (`paper_content.tex:1143-1146`; journal PDF p. 14). The README repeats this
limitation (`code/README.md:55-68`). Static inspection confirms that limitation:
the package checks selected exact identities, finite examples, and finite
top-complex atlases, but it contains no general positive-recurrence prover.

## 4. Complete static implementation map

| Manuscript interface or claim | Code and tests | What the check actually establishes | What it does not establish |
|---|---|---|---|
| Falling factorial and enabled reaction semantics | `network.py:16-22,65-80`; `test_network.py:31-40` | Exact integer falling factorials, including `0`, `2S_i`, mixed binary complexes, disabled reactions, and successors in the tested cases. | Validity of arbitrary user-supplied state dimensions is not comprehensively enforced; universal stochastic dynamics are not enumerated. |
| Lifted state-return cycle and reachability symmetry | `state_cycle.py:27-113,116-169`; `verification.py:274-341`; `test_publication_v1_1.py:87-158` | A BFS finds a complex return path and explicitly lifts it with fixed residual; finite examples include zero complex, boundaries, multiple linkage classes, parallel channels, equal displacements, parity shells, and an absorbing singleton. | It is finite witness construction, not a proof that every weakly reversible input satisfies the premise. The finite graph symmetry routine only applies to a supplied finite closed set. |
| Labelled-channel mark and population successor | `target_augmented.py:38-50`; `test_network.py:70-77` | The returned mark is the actual channel target, so equal population displacements with different sources/targets remain distinguishable. Source probabilities are exactly aggregated by source. | No augmented-state class is constructed. Markov property, closure, irreducibility, autonomous projection, and the reachable-mark characterization in manuscript Section 3 are not tested. |
| Exact target/source log-factorial increment | `target_augmented.py:15-35`; `verification.py:179-194`; `test_network.py:13-29` | Two algebraically different exact rational calculations are compared for 3,318 two-species, state-`0..4`, binary-complex instances, across every enabled carried target/source and every binary outcome. The outcome cancellation is genuinely exercised. | This finite enumeration is not needed for, and does not replace, the direct factorial derivation. Properness of `V` and its finite sublevels are not checked. |
| Source-probability entropy rewrite | `target_augmented.py:42-50,85-150`; `verification.py:197-238`; `test_episode.py:57-86` | Both sides are represented exactly as rational prime-exponent log signatures. The finite cases include zero source, pure/mixed binary complexes, and parallel source-rate aggregation; the README states 172 cases. | The entropy upper bound involving `C_0` is not evaluated, and the calculation does not establish drift for a universal network. Both sides share the same source-probability implementation. |
| Target-following episodes | `episode_bounds.py:48-68`; specialized recursions in `publication_v1_calibrations.py:43-85` and `publication_v1_1_calibrations.py:94-166`; ACK generic comparison in `verification.py:344-422` | Exact path probabilities, the empty-path probability, one three-complex rate-degeneration episode, and the complete ACK example are encoded. The ACK closed form is compared with a generic source-probability/factorial-signature calculation. | There is no general implementation of Lemma 4.1's episode recursion, all deviation branches, stopping-time property, or backward propagation on an arbitrary graph. The empty-path check is only `product([])=1`, not the final ordinary jump in a zero-length episode. |
| Scalar envelope | `episode_bounds.py:13-45`; `verification.py:241-271`; `test_episode.py:18-39` | The endpoint/interior maximizer branch at and around `M=-1/q` is checked for four `q` values; pointwise monotonicity is exact because the increment reduces to `qp(M_2-M_1)`. | The code never evaluates either displayed value of `F_q(M)`, never includes `C_0`, and does not computationally check `F_q(M)->-infinity` or backward recursion. The analytic calculus proof remains load-bearing. |
| Normalized-log compactification | none | Nothing computational. | Diagonal extraction, zero-weight divergent coordinates, falling-factorial asymptotics, and passage to a top face remain purely analytic. |
| Bimolecular top-complex trichotomy | `top_complex_dichotomy.py:36-97`; independent certificate validator at `:100-180`; deterministic atlas in `verification.py:446-524`; fixed-seed stress test at `:526-569`; `test_top_complex.py:11-164` | For each generated input, the classifier returns an availability or invariant certificate, and a second routine which does not call the classifier recomputes the top set and validates strict height separation/bounded-coordinate supply or exact invariant constancy. The deterministic atlas covers every nontrivial subset of the ten three-species binary complexes, 55 specified rational weights, and every enlargement of positive-weight support by zero-weight divergent coordinates (98,261 cases). Five thousand four-species cases use fixed seed 20260806. | The 55 weights are a finite atlas, not all real normalized weights or all normal-fan cells; four-species coverage is sampled. Actual divergent sequences and bounded residual values are absent. Certificate validation is useful falsification evidence but not a universal proof. |
| Exceptional Foster set `K` | none | Nothing computational. | Finiteness, nonemptiness, rate dependence, and measurable deterministic selection of episodes are not implemented or enumerated. |
| Stopped random-time Foster/supermartingale step | `publication_v1_calibrations.py:121-149`; `test_publication_v1.py:53-70` | One finite transition list verifies the one-step algebra `E[V_next]-V+1<=0`, and a stopped state returns zero increment. | There is no stochastic process, stopping time, filtration, integrability bound, optional stopping, monotone convergence, or expected hitting-time proof. Calling this a “random-time Foster calibration” is only a toy interface check. |
| Finite trace chain and jump-return conversion | no trace-chain implementation; only finite reachability utilities | No direct check. | Irreducibility of the trace, geometric domination of trace returns, Tonelli/tail-sum conversion, and projection from marked returns to population returns remain analytic. |
| CTMC nonexplosion and regenerative occupation | `publication_v1_calibrations.py:88-118`; `publication_v1_1_calibrations.py:169-194`; corresponding tests | Correct exact occupation normalization is checked for a two-state bidirectional CTMC and a finite directed cycle; absorbing law is an exact point mass. | No general CTMC is constructed. The lower-rate bound, nonexplosion argument, finite expected physical return time, and general regenerative occupation formula are not verified by software. |
| Rate-separated example | `publication_v1_calibrations.py:43-85`; `publication_v1_1_calibrations.py:27-50`; tests at `test_publication_v1.py:14-51` and `test_publication_v1_1.py:162-175` | Exact rational formulas capture the fixed-rate large-`m` coefficient `-kappa_2/(kappa_1+kappa_2)` and the distinct fixed-`m`, `kappa_2->0` limit. | It is one network and a few rates, not a general arbitrarily separated-rate stress oracle. |
| Boundary and edge cases | tests listed above plus `test_boundary_lattice.py` and `calibrations()` at `verification.py:572-732` | Zero complex, coordinate face samples, parity classes, repeated species, absent species, zero-weight divergent species, parallel/equal-displacement channels, finite class, zero-length product, and absorbing state each have at least one explicit calibration. | Coverage is uneven: see Findings 3-6 below. |

## 5. Verifier and test design assessment

### 5.1 Canonical report generation is genuine

`code/reproduce.sh:33-51` first runs the test suite, then invokes
`python -m bimolecular_pr.verification` twice into two fresh temporary files,
requires those files to be byte-identical, and finally compares the regenerated
bytes to the committed report. It does not copy the committed report into the
temporary output and expressly refuses to overwrite it. `verification.py:735-774`
recomputes all stable checks and source hashes; `main()` writes sorted canonical
JSON at `:788-808`. Subject to later execution, this is real regeneration rather
than copying.

The comparison still establishes reproducibility against an author-generated
golden artifact, not mathematical truth. If code and golden report were changed
together, the internal comparison would agree. The outer manifest and packet
checksum layers make accidental or isolated modification fail, but without the
claimed v1.2.4 tag they are not presently anchored to the claimed Git release.

### 5.2 Hard-coded expected answers

The following are deliberately hard-coded:

- Three-species atlas counts and SHA-256 digest
  (`verification.py:86-102`).
- Fixed-seed four-species counts and digest (`verification.py:103-113`).
- Wheel SHA-256 (`test_verification.py:56-60`).
- Package/schema/status strings (`verification.py:740-744`) and many small
  calibration constants (`verification.py:648-731`).

The top-atlas values are not merely returned: the atlas is recomputed, every
certificate is validated, a fresh digest is built, and the whole result is
compared at `verification.py:474-524`. The seeded stress result is likewise
recomputed at `:526-569`. The fixed values are therefore regression anchors,
not copied answers. In contrast, several small unit tests re-express the same
formula as the production helper and are weakly independent—for example the
rate-degeneration branch aggregation in `test_publication_v1.py:14-39` and the
scalar pointwise-increment test in `test_episode.py:26-39`.

The best independent internal comparisons are:

- direct residual factorials versus falling-factorial ratios
  (`verification.py:179-194`);
- entropy left/right log signatures (`:225-238`);
- ACK specialized formula versus generic source-probability/factorial episode
  (`:358-422`); and
- top classifier versus a certificate validator that does not invoke the
  classifier (`top_complex_dichotomy.py:100-180`).

They are still part of one author-supplied codebase and share low-level
primitives, so independent referee oracles remain warranted.

### 5.3 Finite and random scope

- Factorial identity: two species; population coordinates `0..4`; all six
  binary complexes; 3,318 exact instances (`verification.py:179-194`).
- Entropy identity: two fixed two-species networks and coordinates `0..4`;
  README reports 172 instances (`verification.py:197-238`).
- Scalar branches: four `q` values, six `M` values per `q`, and three `p`
  values for pointwise monotonicity (`verification.py:241-271`).
- State cycles: two small example networks and bounded state grids, plus a
  finite parity shell (`verification.py:274-341`).
- ACK: two fixed rate vectors and `n=2..12` (`verification.py:399-422`).
- Top atlas: exhaustive only relative to the explicitly finite three-species
  subset/weight atlas (`verification.py:446-524`).
- Four species: exactly 5,000 pseudorandom samples from a documented generator
  and seed (`verification.py:526-569`).

No floating-point numerical calculation is used. Exact `Fraction` arithmetic
and prime-exponent log signatures avoid tolerance and stability issues within
their finite domains.

### 5.4 Source allowlist and fail-closed behavior

`SOURCE_FILES` is explicit (`verification.py:58-84`). At report generation,
the verifier discovers all `*.py` files under `src/` and `tests/`, rejects a
missing or unexpected Python path, and hashes every allowlisted file
(`verification.py:129-159`). A missing fixed non-Python file reaches
`file_hash()` and fails with a file error. A changed allowlisted file changes
the report and should fail the later golden comparison.

Limitations:

- Discovery is closed only over Python files plus six fixed root files. A new
  non-Python file under `src/` or `tests/` is not rejected by `source_hashes()`.
  The README precisely promises failure only for “an unlisted Python source or
  test” (`README.md:63-66`). The outer durable-tree manifest is the broader
  safeguard.
- `test_source_hashes_use_closed_allowlist` checks the returned key order, not
  predeclared digest values (`test_verification.py:25-26`). Digest anchoring is
  supplied only by golden-report/manifest comparisons.
- The top classifier itself has incomplete public-input validation: it does not
  reject mismatched complex dimensions, out-of-range divergent indices, or
  positive weight support outside the divergent set before indexing/zipping
  (`top_complex_dichotomy.py:36-63`). The separate validator does reject these
  at `:113-125`, and every atlas/stress result is passed to that validator, so
  canonical verification uses valid inputs and fails on malformed certificates.

### 5.5 Version and deterministic-output handling

- Python `>=3.11` is checked before test execution
  (`code/reproduce.sh:7-19`), matching `pyproject.toml:10`. The canonical report
  omits environment data; provenance is written separately
  (`verification.py:777-785`).
- `PYTHONHASHSEED=0` and a local `random.Random(20260806)` are used
  (`reproduce.sh:29-31`; `verification.py:526-541`). JSON keys are sorted and
  separators fixed (`verification.py:116-123`). All enumeration orders are
  explicitly sorted or tuple-ordered. A changed pseudorandom sequence will
  change the fixed digest and fail rather than silently pass.
- `RUN_ALL_CHECKS.sh:16-18` initially checks only that `tectonic` exists, despite
  mentioning 0.16.9. The actual PDF builder subsequently requires exact output
  `Tectonic 0.16.9` (`manuscript/build.sh:11-20`), so the complete replay does
  fail closed on the wrong version.
- The release environment records a Tectonic bundle-content digest, but the PDF
  build script only prints that digest and passes the configured bundle URL to
  Tectonic (`manuscript/build.sh:53-63`); it does not independently hash a
  downloaded bundle. Byte-comparison of all rebuilt PDFs remains the output
  safeguard.
- The software metadata consistently says package version `1.2.0`
  (`__init__.py:3`, `pyproject.toml:8`, `build_backend.py:13`,
  `verification.py:742`), while the outer submission is Version 1.2.4. No tool
  cross-checks outer-release version against package version. This may be an
  intentional unchanged software-package version, but it should be explicitly
  documented to prevent provenance ambiguity.

### 5.6 Release tooling

- `RUN_ALL_CHECKS.sh:44-92` parses the packet checksum list with duplicate,
  traversal, separator, symlink, missing, changed, and unexpected-file checks.
- `supplement/verify_manifest.py:66-131` independently walks the durable tree,
  rejects symlinks, and detects missing, changed, or unexpected durable files.
  Its ignored set is explicit at `:22-55`.
- `supplement/build_release_archive.py:48-76,110-162` validates each manifest
  member and digest, relies on a fresh complete-manifest check, sets fixed
  timestamps/modes/order/compression, CRC-tests the result, and byte-compares a
  fresh archive with the committed ZIP.
- `RUN_ALL_CHECKS.sh:21-35` saves the supplied PDFs before rebuilding, and its
  exit trap restores those original bytes after success or failure. It compares
  each rebuilt PDF to the saved bytes at `:116-120`.
- `build_backend.py:54-71` builds a deterministic stored wheel with fixed entry
  order, timestamp, permissions, and RECORD; the test rebuilds it twice and
  checks a fixed digest/license metadata (`test_verification.py:40-76`).

These scripts are designed to fail closed on isolated mutations. Their claims
remain unexecuted in this preliminary report.

## 6. Preliminary findings, severity-ranked

### Major S1 — Claimed v1.2.4 Git tag is unavailable

**Location:** journal PDF p. 14; `paper_content.tex:1139-1145`.  
**Evidence:** no `.git` directory is supplied in the packet; neither the
containing checkout's tag list nor a direct remote tag query returned
`bimolecular-positive-recurrence-v1.2.4`. Existing matching tags stop at
v1.2.3.  
**Effect:** content hashes and deterministic rebuilds can still be checked, but
the manuscript's present-tense tagged-release and exact-commit provenance claim
cannot currently be verified.  
**Repair:** publish and independently resolve the claimed tag to the released
tree/commit, or revise the manuscript to state that v1.2.4 is a standalone
submission packet whose Git tag is not yet available.

### Minor S2 — All-self-channel reduction is not represented

**Location:** manuscript `paper_content.tex:285-305`; `network.py:50-53,82-92`;
`test_network.py:58-68`.  
**Evidence:** `enabled_channels()` correctly omits self-channels, but
`combined_parallel()` discards them and then constructs a `Network` that
requires at least one remaining channel. A network consisting only of
self-channels therefore cannot be reduced through this helper; the test covers
a self-channel only when genuine birth/death channels remain.  
**Effect:** no theorem defect; this is an unexercised boundary of the verifier's
data model.  
**Repair:** either explicitly document that all-self networks bypass
`combined_parallel()` and are handled as absorbing, or allow an empty reduced
channel tuple and add the boundary test.

### Minor S3 — Scalar-envelope coverage is narrower than the displayed lemma

**Location:** manuscript Lemma 4.2, `paper_content.tex:571-596`;
`episode_bounds.py:13-45`; `verification.py:241-271`.  
**Evidence:** code returns only the maximizer branch and checks pointwise
monotonicity. It does not compute the two values in equation (22), the continuity
at the branch point, or the limit to `-infinity`.  
**Effect:** the report's phrase “branch conditions and pointwise monotonicity”
is accurate, but the software does not check the full scalar-envelope lemma.
The missing pieces remain analytic obligations.  
**Repair:** add an exact symbolic representation of the nonlogarithmic pieces
and an independent calculus/inequality oracle, while continuing to state that
the limiting implication is analytic.

### Minor S4 — Several edge-case labels exceed what their tests show

**Locations:** `test_boundary_lattice.py:7-19,23-45`;
`episode_bounds.py:54-68`; `verification.py:729-730`.  
**Evidence:** the coordinate-face helper suppresses successors beyond a chosen
population cap, so it samples face invariance but cannot show closure of the
displayed finite set. The zero-length-path calibration establishes only that an
empty product is one; it does not exercise the manuscript's required final
ordinary jump.  
**Effect:** these remain useful small checks, but their names should not be read
as proof of the full boundary/episode interfaces.  
**Repair:** assert face preservation for every enabled successor in an explicit
state range without filtering it out, and add a zero-length episode oracle that
computes the final-jump expected increment.

### Note S5 — Top-complex exhaustiveness is finite and correctly limited

**Location:** `verification.py:446-569`; `README.md:48-55`.  
The “98,261-case exhaustive” description is accurate only for the stated
three-species finite subset/weight atlas. It does not exhaust real weights or
all species dimensions. The README and canonical classification appear to
state that finite scope, and the manuscript disclaims use as proof. No
correction is required unless a later report describes the atlas as universal.

### Note S6 — Software does not test most probabilistic load-bearing steps

There is no implementation of augmented-chain irreducibility/projection,
properness, general episode stopping/deviations, compactification, `K`, optional
stopping/integrability, trace-chain conversion, nonexplosion, or the general
regenerative law. This is not a hidden failure because the manuscript and
README explicitly disclaim computation as proof. A passing replay can validate
only the finite interfaces in Section 4 of this report.

## 7. Planned independent execution, oracle, and mutation phase

After all separated preliminary reports are fixed, the software track should:

1. Run `./RUN_ALL_CHECKS.sh`, recording the full outcome, all skips/failures,
   exact test counts, Python/Tectonic/OS output, and reported hashes.
2. Recompute the factorial identity with an oracle that uses direct products of
   consecutive integers and residual factorials, importing none of the
   production helpers.
3. Recompute the ACK and rate-degeneration episodes by direct channel/event
   enumeration, not by `expected_increment_signature()` or the specialized
   calibration routines.
4. Build an independent small-dimension top oracle that enumerates candidate
   availability pairs and independently verifies invariant vectors, then
   compare classifications on all two-species complex subsets and a separately
   generated weight grid.
5. In a disposable copy, reverse the factorial ratio, alter a top certificate,
   perturb the ACK recursion, and change a scalar branch threshold; require the
   appropriate independent tests to fail.
6. Change a byte in the committed report and require `reproduce.sh` to reject
   it; add an unlisted `.py` file and require the source allowlist to reject it;
   add a non-Python source-like file to confirm the inner allowlist limitation
   and the outer manifest's broader rejection.
7. Run the canonical report twice under every locally available supported
   Python minor version and compare bytes. Current environment availability has
   not yet been inventoried beyond Python 3.14.6.
8. Mutate manifest path separators, traversal, duplicates, symlinks, a PDF byte,
   and archive member order in disposable copies; require each relevant layer
   to fail closed.

## 8. Preliminary software conclusion

Static inspection finds a substantive, deterministic, dependency-free
falsification package. It genuinely recomputes its canonical report rather than
copying it, has unusually explicit finite scopes, uses exact arithmetic, and
independently validates top-complex certificates. It also contains fixed golden
digests and several calibration tests that are only weakly independent. Most
of the universal theorem's probabilistic and limiting interfaces are not
implemented, exactly as the manuscript's limitation statement says.

No static code error found here falsifies the theorem. The material artifact
discrepancy is the presently unavailable v1.2.4 Git tag. Dynamic replay,
independent oracles, mutations, and artifact byte comparisons remain pending;
therefore this preliminary software report makes **no final validity or journal
recommendation**.

**Completion estimate:** 100% of the required blind static pass; approximately
55% of the full software/computation audit, with replay, independent mutation
testing, and post-barrier comparison still outstanding.

## Appendix A. Hashes of statically inspected software/release files

```text
579383c84cae29c0b2c62e41bbbb0254dfa1cd0b5e3e968f6e85899c5bb4944e  RUN_ALL_CHECKS.sh
1446f53072118fcfbe11be4965284a1b08b22029ff128be44165e5f7e19b6ad5  REPRODUCIBILITY.env
bac4dc8ba1997063d73c453a73d68db7595e9dd2d0be026cfb29e339252d13c7  code/README.md
782108c8907da6f76f2510354b0519dc8f86fe1ace31253a22a044ffdf4fb183  code/build_backend.py
71b2d810f00b3370eee1da63bf6309bb47d70f42b8df66d76086012a500788e4  code/pyproject.toml
4dd4055c2e6d15e498589a0822a692d052c9f4468704ab7b00609b7118467fac  code/reproduce.sh
acaba656e14849c6a546eada97fa12c88bc627f61bef4e5d182fe288c847e13a  code/src/bimolecular_pr/__init__.py
e402cbb9bc4796ab8619ec014a99821128ebb38ed284eb59c0889abdfe5ead4c  code/src/bimolecular_pr/episode_bounds.py
b2c2ad24c89b19e96f4f348ef0d5ede201bebcc6352c31e674b2f48db85a050c  code/src/bimolecular_pr/network.py
dd59612aeb0b8d97c538f0731bd15e2aa0322fc60df036f617443c6e5963c80b  code/src/bimolecular_pr/publication_v1_1_calibrations.py
9c966dba9e5680d4c010adf364c839f0ec8ea4e4fab3492c4bd8700e9fa2ccf8  code/src/bimolecular_pr/publication_v1_calibrations.py
ae95de78612e0cd9f5c365265f936f3da9eee664b1ba4bd01521ed49a5dfbe4c  code/src/bimolecular_pr/state_cycle.py
942000897de07f1535f9b9848ffd3c4e608eeaca5b6b44a5a9e492eaea36165a  code/src/bimolecular_pr/target_augmented.py
71325fc0b185895bb7cc52266796ccc3ef12b52dca76c8cad06f91ade877f721  code/src/bimolecular_pr/top_complex_dichotomy.py
a0299c54b5ba04e8fdf6a8aa70868493f3ab620686fabe3fab958dff16254bd2  code/src/bimolecular_pr/verification.py
040223686a9defa5b21a1a2ea0d1f77aa0ca3c3ee61f4c2734abe36cc168be10  code/tests/test_boundary_lattice.py
411b53efb55df40ea73116be526bc90076adc21f0cadcbb228fae5b7ea94b95f  code/tests/test_episode.py
97fb6d76970e7488f6c6f18966e756f739634a41dc2af9278211f39f6d60bef2  code/tests/test_network.py
c9582a90542d50d3d28406ba8ac4c9da2f7f03b7d7b65722165ca23c00a47dad  code/tests/test_publication_v1.py
e9c753363f4eeec518ab6ee623d92150c20c5dc409819b63a33d9d1f2852f7bc  code/tests/test_publication_v1_1.py
061c7df9433b9df4ad272352ca244466dac9b629fbee3030656bb99392a9025b  code/tests/test_top_complex.py
8ea0b762a45713bc3512b49c00d2f5c6a00c8bed90c8f3ecbee9c2ce245abe56  code/tests/test_verification.py
1ad498bc4bc50880e7d3e16f8f1a0ef3d2f27077a59ac979b094822d20534379  manuscript/build.sh
370036442427997f146ae1adb193e00e5195dcbea9cb7aadd26bcf558c4a1804  supplement/build_release_archive.py
f4a40b350207eff97b3f422f5fdbaca46a6ae76a501410298cf38d631db54449  supplement/test_release_tools.py
1204d9070ebd429542e4e0088b0517f015f64af097b236a3010c5472e8220241  supplement/verify_manifest.py
```

## Appendix B. Research checkpoint log

- **2026-08-21T22:22:09-07:00 — blind static checkpoint.** Manuscript-first
  reading, complete source/test/tool inspection, environment and independent
  hashes, finite-scope map, and planned adversarial phase recorded. Best-guess
  completion: 100% of preliminary static deliverable; 55% of total software
  audit. Strongest verified static result: canonical output is recomputed twice
  from exact finite checks and then compared; it is not copied. Exact remaining
  gap: no commands have been executed and no committed expected output has been
  opened, so dynamic reproducibility and fail-closed behavior are not yet
  independently observed.
