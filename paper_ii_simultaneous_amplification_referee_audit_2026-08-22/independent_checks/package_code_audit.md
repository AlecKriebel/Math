# Independent package and software audit

**Checkpoint:** 2026-08-22 (America/Los_Angeles)
**Auditor:** independent code-audit subagent
**Package audited:** `delivered_copy/`
**Best-guess completion:** **100% of the assigned package/software audit.** Source inspection, canonical runtime replay/rebuild, independent tag/tree binding, and disposable fault injection are complete.
**Execution boundary:** Every delivered program was inspected before execution. After the source gate was cleared, I ran `run_all_referee_checks.sh` once unchanged through the prescribed logger. Its pip step downloaded the two pinned packages from the configured index into a disposable environment. I did not modify `delivered_copy`, contact anyone, upload, commit, or push. A post-run whole-package manifest check confirmed that `delivered_copy` remained unchanged.

## Bottom line

The delivered bytes are internally complete and consistent with both bundled manifests: 29 outer payload files, 19 sorted regular archive members (18 payloads plus the internal manifest), byte-identical archive/extracted payloads, and byte-identical convenience/source PDFs. The canonical wrapper completed successfully and reproduced the archive and PDF byte-for-byte.

Local and remote tag checks independently strengthened provenance: the local tag and the remote annotated tag both peel to scientific commit `2302d7c6ae17fc061a985da322df6d0600b66672`, and all 17 repository-backed archive members match that commit's blobs and executable modes. The tag is annotated but unsigned, and the standalone package verifier does not itself perform this check.

The most important software finding remains: the mathematical certifiers and bootstrap version checks rely entirely on Python `assert`. Disposable fault injection confirmed that normal replay stopped on an impossible assertion, whereas `PYTHONOPTIMIZE=1` erased it and returned zero while printing every certificate `PASS` message.

## Findings

### CODE-01 — High — verifier soundness — optimization can erase every mathematical check

All four mathematical programs express their checks as bare `assert` statements:

- `certificates/verify_leading_algebra.py:15-66` (11 asserts),
- `certificates/verify_hybrid_lumping.py:159` (the sole assert, repeated in the enumeration loop),
- `certificates/verify_hybrid_coefficients.py:16-106` (21 asserts), and
- `verify_paper_claims.py:32-154` (25 asserts).

The bootstrap's Python and dependency version checks are also assertions (`bootstrap_replay.sh:9-12` and `23-29`). None of `bootstrap_replay.sh`, `replay.sh`, or `run_all_referee_checks.sh` rejects optimized Python or clears `PYTHONOPTIMIZE` (`bootstrap_replay.sh:1-32`; `replay.sh:1-21`; `run_all_referee_checks.sh:1-76`). Each certificate prints a success message after the assertion block, and `run_all_referee_checks.sh:76` prints its aggregate `PASS` after the nested programs return zero.

The failure was confirmed against the actual replay chain in `independent_checks/failure_propagation_fixture/`, a disposable byte copy of the source tree with one injected `assert False` sentinel in `verify_leading_algebra.py`. Normal `./replay.sh` exited 1 at the sentinel (`agent-code-failure-normal`); `PYTHONOPTIMIZE=1 ./replay.sh` exited 0 and printed all four programs' success messages (`agent-code-failure-optimized`). The delivered copy was untouched. Therefore the suite can become a false-pass suite in a supported-looking environment. `PYTHONOPTIMIZE` was unset during the successful canonical run, so there is no evidence that its observed results skipped assertions.

**Required correction:** replace verification-critical assertions with explicit checks that raise exceptions; additionally reject `sys.flags.optimize != 0` using an explicit conditional. Running the certifiers with `-I` and a sanitized environment would reduce import/environment contamination but does not replace explicit checks.

### CODE-02 — Medium standalone-verifier limitation; independently resolved for this audit — Git identity binding

The standalone verifier hard-codes a commit and tag (`verify_referee_package.py:23-24`) and only checks that those strings occur in `VERSION.md` and `README_FIRST.md` (`verify_referee_package.py:149-161`). It does not reconstruct a Git tree or resolve a remote tag. The archive metadata does not contain the claimed commit/tag (`source_and_certificates/BUNDLE_METADATA.txt:1-14`), and the delivered package contains no Git objects or signature. Thus the standalone offline verifier still establishes internal consistency rather than Git provenance.

Independent repository checks closed that gap for this audit:

- Local `refs/tags/simultaneous-amplification-beyond-three-halves-v2.0.1^{}` resolves to `2302d7c6ae17fc061a985da322df6d0600b66672` (commit date 2026-08-22T10:51:35-07:00; subject “Harden isolated Paper II release replay”).
- The remote reports annotated tag object `abad2dd24cceae62fde4b69a2ad95510e24350b2` and peels it to the same commit.
- Direct `git show`/`git ls-tree` comparisons found that all 17 repository-backed internal-manifest members match the commit's bytes and executable modes. The remaining archive payload, `BUNDLE_METADATA.txt`, is synthesized by the matching committed `bundle_manifest.py`; `MANIFEST.sha256` is generated from those payloads.

**Exact conclusion:** the included scientific source/PDF whitelist is bound to the claimed commit and the local/remote tag resolutions agree. Residual limitation: the annotated tag object contains no cryptographic signature, so authentication ultimately relies on the queried remote transport/account and local repository integrity rather than a separately verifiable signer key.

### CODE-03 — Medium — hermeticity/supply chain — the frozen handoff is not offline self-contained

`bootstrap_replay.sh:18-21` creates/uses a virtual environment and performs `pip install --no-cache-dir -r requirements.txt`. `requirements.txt:1-2` pins only `mpmath==1.3.0` and `sympy==1.14.0`; it supplies neither artifacts nor hashes. `README_FIRST.md:61-66` accurately discloses that distributions are not vendored/hash-pinned and that pip and Tectonic may access external resources, notwithstanding the description “self-contained” at `README_FIRST.md:3`.

The base environment has Python 3.14.6 but neither SymPy nor mpmath installed, and the archive contains no wheels or source distributions. The authorized canonical run therefore fetched `mpmath-1.3.0-py3-none-any.whl` and `sympy-1.14.0-py3-none-any.whl` from the configured index into its fresh venv. Tectonic package/resource inputs are likewise not included or individually hash-pinned. The successful byte comparisons detect divergent products but do not make the build offline-hermetic or authenticate the downloaded distribution artifacts.

**Consequence:** runtime replay succeeded on this networked host, but cannot be reproduced from the delivered bytes alone. A genuinely frozen/offline replay would need vendored, hash-pinned dependency artifacts and a pinned Tectonic resource bundle.

### CODE-04 — Medium — deterministic rebuild portability — archive builder ignores the pinned interpreter handle

The canonical wrapper honors `BOOTSTRAP_PYTHON` for bootstrap/replay (`run_all_referee_checks.sh:5,16,53`), but `release_bundle.sh:17-19` invokes bare `python3` for `bundle_manifest.py`. It does not use the venv interpreter, `BOOTSTRAP_PYTHON`, or the interpreter selected by `replay.sh`. Archive bytes depend on Python's `gzip`/`tarfile` implementation (`bundle_manifest.py:155-165`), so the rebuild is not actually tied to the bootstrap interpreter when `python3` resolves elsewhere.

The current `python3` is the claimed 3.14.6, so the inconsistency does not block this host. It does defeat the documented escape hatch when a reviewer must set `BOOTSTRAP_PYTHON=/path/to/python3.14.6` because their PATH's `python3` is different or absent.

**Suggested correction:** pass the selected interpreter through to `release_bundle.sh` and use it for `bundle_manifest.py`, or call the created venv's interpreter explicitly.

### CODE-05 — Low — integrity scope — extracted executable modes are not checked by the standalone verifier

`verify_referee_package.py:62-81` binds outer file paths, regular-node status, and file bytes, but not permission bits. Yet `bundle_manifest.py:136-141` derives archive executable modes from source-tree permission bits. Changing an extracted wrapper from executable to non-executable (or vice versa) does not alter its SHA-256, so `verify_referee_package.py` alone can still report success.

The full `run_all_referee_checks.sh` rebuild-and-`cmp` path would catch such a change because archive metadata would differ (`run_all_referee_checks.sh:54-58`). The delivered copy's modes do match the archive: shell scripts, `bundle_manifest.py`, and `verify_paper_claims.py` are 0755; other archive members are 0644.

## Package identity and completeness checks

Independent checks produced the following verified facts:

- Exactly 30 regular files are present in `delivered_copy`: 29 outer payloads plus `PACKAGE_MANIFEST.sha256`; no symlinks or non-regular nodes were found.
- The outer manifest's set equals the complete payload file set, and all 29 hashes match.
- The detached archive checksum has the canonical exact form and matches the archive bytes.
- The source archive has exactly 19 unique, lexicographically sorted, regular members. There are no absolute paths, `..` components, symlinks, hard links, devices, or directory members.
- All archive members have fixed `mtime=1787356800`, `uid=gid=0`, `uname=gname=root`, and expected modes. The gzip header contains the same fixed mtime, no filename, maximum-compression flag, and OS-neutral byte.
- The internal manifest covers exactly the other 18 archive members; all internal SHA-256 values match.
- `source_and_certificates/` contains exactly the archive member set and is byte-identical to the archive payload, including its manifest.
- The convenience PDF and nested source-tree PDF are byte-identical.
- Archive whitelist source inspection (`bundle_manifest.py:20-41,128-170,174-210`) agrees with the delivered 19-member archive. The builder fixes ordering, metadata, and modes and performs an internal post-write verification.
- Local and remote tag resolutions agree on commit `2302d7c6ae17fc061a985da322df6d0600b66672`; all 17 repository-backed archive members match that commit's blobs and executable modes.

These independent checks reproduce and extend the package verifier's content checks. The residual provenance qualification is the unsigned annotated tag described under CODE-02.

## Canonical runtime and fault-injection results

The unchanged canonical entry point ran as `agent-code-run-all` and exited 0. Salient observed results:

- `verify_referee_package.py` reported 29 matching outer payloads and 19 matching archive members, with the expected archive/PDF hashes.
- The fresh venv used Python 3.14.6 and installed SymPy 1.14.0 plus mpmath 1.3.0.
- The replay reported `R_hyb ~ 1.50285691279056963`, `sigma_* ~ 0.130677282287048377`, and `lambda_* ~ 0.750806483031880492`; enumerated 512 labelled masks and 108 fibres under each rule; and completed all symbolic/rational integration checks.
- Release replay ran the certifiers a second time, rebuilt the 19-member archive, and compiled the PDF.
- The rebuilt archive SHA-256 was exactly `ce62bfbdb22681ba48b2a04653155b2e06f52659f140c13f5e0220db365b9250`; the rebuilt PDF SHA-256 was exactly `f68142b3d99b95f83ca6ba4688539cb9e0fdb88ed96809aef5316ed22a59888f`. Both byte comparisons succeeded.
- A subsequent outer-manifest check again passed all 29 payloads, confirming that the canonical run did not mutate `delivered_copy`.

The disposable failure fixture preserves a checkable reproduction of CODE-01. It was bootstrapped normally, then only the copied `verify_leading_algebra.py` received an impossible assertion at the beginning of `main()`. Normal replay failed at that exact sentinel with exit 1. With only `PYTHONOPTIMIZE=1` changed, replay exited 0 and printed every `PASS` message. This tests the real `replay.sh` interpreter selection and sequential failure propagation, not merely a standalone toy assertion.

## Complete executable/import inventory

No project-local Python module is imported by any certificate. Static AST inspection found only the following:

| Program | Role | Imports | Verification asserts |
|---|---|---|---:|
| `verify_referee_package.py` | outer/archive/extraction/prompt consistency | standard library: `hashlib`, `pathlib`, `re`, `tarfile` | 0 |
| `bundle_manifest.py` | deterministic archive construction | standard library: `argparse`, `gzip`, `hashlib`, `io`, `os`, `pathlib`, `tarfile`, `tempfile` | 0 |
| `certificates/verify_leading_algebra.py` | sextic/root/tangency derivative identities | third party: `sympy` | 11 |
| `certificates/verify_hybrid_lumping.py` | labelled finite transition enumeration | standard library: `fractions`, `itertools` | 1 (inside exhaustive loop) |
| `certificates/verify_hybrid_coefficients.py` | response coefficients, rational specialization, phase algebra | third party: `sympy` | 21 |
| `verify_paper_claims.py` | duplicate algebra plus manuscript marker regression checks | standard library: `fractions`, `pathlib`; third party: `sympy` | 25 |

Shell entry points were all read in full before execution:

- `run_all_referee_checks.sh:1-76`: outer verifier, exact tool-version gates, guarded temporary copy, bootstrap replay, rebuild, byte comparisons, final hashes.
- `bootstrap_replay.sh:1-32`: Python-version assertion, venv creation/reuse, pip installation, dependency assertions, replay.
- `replay.sh:1-21`: interpreter selection and four certificate invocations.
- `build.sh:1-22`: Tectonic build, PDF installation/info, rendered-image deletion/regeneration.
- `release_bundle.sh:1-19`: replay, build, archive generation.
- `all.sh:1-6`: replay plus build.

The TeX source has no local `\input`, `\include`, `\includegraphics`, bibliography file, shell-escape, file-read, or file-write directive. Its external build dependencies are the class/package resources declared at `main.tex:1-9`.

Third-party source inspection is necessarily incomplete: SymPy, mpmath, their distribution artifacts, and the Tectonic resource bundle are not delivered. SymPy/mpmath were installed only into disposable audit venvs for the runtime phase, not into the base interpreter. Standard-library/runtime source was treated as part of the pinned interpreter platform rather than a project import.

## Failure propagation and mutation/safety review

Except for CODE-01, nonzero statuses propagate coherently:

- Every shell wrapper uses `set -eu`; the sequential certificate calls in `replay.sh:18-21`, build/replay calls in `release_bundle.sh:15-19`, and all top-level comparisons in `run_all_referee_checks.sh:16-74` are fail-closed on nonzero exit.
- Required document tools and exact displayed versions are explicitly checked before mutation (`run_all_referee_checks.sh:18-39`). The string equality is intentionally strict and may reject otherwise compatible builds, but it does not create a false pass.
- The top-level runner creates an unpredictable temporary directory under an absolute `TMPDIR`, copies the source tree there, and mutates only the copy (`run_all_referee_checks.sh:9-14,41-61`). Cleanup validates the generated prefix before recursive deletion (`run_all_referee_checks.sh:42-48`). I found no path-expansion route from the delivered values to a broad deletion target.
- `build.sh:19` deletes only `page-*.png` beneath its derived `output/rendered` directory. In the canonical runner that directory is inside the disposable copy.
- `bundle_manifest.py:149-168` writes a temporary sibling and atomically replaces the requested output. A caller can explicitly choose an existing output path, so standalone use is intentionally overwriting; the canonical wrapper supplies a disposable path.
- `bootstrap_replay.sh` writes a `.venv-paper2` and may execute downloaded installation artifacts. `build.sh` may populate Tectonic's resource cache. These are the only implicit external-write/network surfaces found. No delivered Python source imports networking, subprocess, HTTP, email, messaging, cloud, or repository APIs.
- `pdftoppm` diagnostics are suppressed in `build.sh:20-22`, but its failure status still propagates under `set -e`.

## Exact claim-to-code coverage

The package's own `CLAIM_CODE_MAP.md` is substantially candid. The following is the audited boundary, with stronger wording where needed.

| Claim family | Automated content actually checked | Exact gap/limitation |
|---|---|---|
| Model, baseline, theorem quantifiers (`main.tex:141-225,324-336`) | `verify_paper_claims.py:101-157` checks selected byte/text fragments only; the finite lumping code independently implements the two update rules for one instance. | No semantic verification of definitions, graph-family quantifier order, baseline formulas, or main theorem. |
| Strong orbit lumping (`main.tex:341-366`) | `verify_hybrid_lumping.py:16-160` enumerates all 512 configurations and 108 fibres under Bd and dB, comparing labelled and declared off-fibre rates exactly over `Fraction`. | Only `C=3`, two pairs, two pendants, `r=3/2`, `sigma=19/137`, and `epsilon=1/100`. It is neither a symbolic parameter proof nor a check for theorem-scale `C,q,m` or dyadic cuts. Self-loop equality follows from row sums but is not printed separately. |
| Weak-cut Schur trace and compact-uniform convergence (`main.tex:368-441`) | A manuscript marker is required by `verify_paper_claims.py:105-138`. | No matrix construction, Schur-complement computation, perturbation bound, uniform inverse bound, or convergence certificate. Entirely analytic. |
| Effective least-dyadic diagonal (`main.tex:276-322`) | `verify_paper_claims.py:94-98` merely confirms that eight example fractions `1/2^e` are positive and have expected denominators; `101-157` checks phrases. | It does not compute any `e_t`, fixation rational function, supremum, Sturm/subresultant decision, or termination witness. Computability/existence remains solely in the manuscript. |
| Center module, establishment, confinement, cleanup, reciprocal invasion (`main.tex:443-1141`) | `verify_paper_claims.py:101-157` checks regression phrases/formulas are present. | No stopped-chain, coupling, Green-function, exponential-moment, cleanup, or uniform-error calculation is automated. These analytic steps carry the main asymptotic burden. |
| Pair gate leading rates and odds (`main.tex:1142-1247`) | `verify_hybrid_coefficients.py:28-43` encodes four already-reduced leading rates and symbolically derives the two odds corrections; `verify_paper_claims.py:20-47` duplicates response reconstruction. | The programs do not derive the finite gate table from the graph, prove its portal asymptotics, check adverse-reversal error bounds, or verify the global sweep. Correctness of the encoded leading rates is an input to the algebra check. |
| Two response functions (`main.tex:1249-1290`) | Exact symbolic simplification of pair terms, pendant terms, feasibility bounds, and rational margins (`verify_hybrid_coefficients.py:28-69`; `verify_paper_claims.py:20-98`). | No verification of the `o_r(eta)` remainders or compact uniformity; these depend on the unautomated stochastic propositions. |
| Sextic root, tangency, fixed-parameter response optimum (`main.tex:1292-1382`) | Exact polynomial/root counts, feasibility-gap identity, minimum identity, derivative identities, algebraic remainder checks, and supporting decimal diagnostics (`verify_leading_algebra.py:13-71`; `verify_hybrid_coefficients.py:71-112`; `verify_paper_claims.py:50-74`). | Expressions are independently checkable but manually encoded. Some sign conclusions are explained in comments/manuscript rather than exhaustively asserted by code. `nroots` diagnostics are numerical; the root count/remainder checks provide the exact portion. |
| Rational-edge specialization (`main.tex:1384-1416`) | Exact endpoint margins, threshold quadratic identity/interval, and positivity of the Bd response at that threshold (`verify_hybrid_coefficients.py:52-69`; `verify_paper_claims.py:77-98`). | Rationality/existence of the complete least-dyadic graph sequence is not constructed by code; the finite eight-exponent loop is not a certificate for all `t`. |

Accordingly, the successful replay validates the encoded finite algebra and one finite transition instance. It does not validate the main theorem without an independent proof audit of Sections 4-6, especially the weak-cut uniform limit and stochastic gain-scale estimates.

## Environment/tool inventory at this checkpoint

- Host: macOS 26.5.2, build 25F84; Darwin kernel 25.5.0; arm64.
- `python3`: `/opt/homebrew/bin/python3`, Python 3.14.6 (matches claim).
- Base interpreter: SymPy and mpmath not installed. Canonical disposable venv and retained failure fixture: SymPy 1.14.0 and mpmath 1.3.0.
- Tectonic: `/opt/homebrew/bin/tectonic`, `Tectonic 0.16.9` (matches claim).
- `pdfinfo`: `/opt/homebrew/bin/pdfinfo`, Poppler 26.08.0 (matches claim).
- `pdftoppm`: `/opt/homebrew/bin/pdftoppm`, Poppler 26.08.0 (matches claim).
- `PYTHONOPTIMIZE`, `PYTHONPATH`, `PYTHON`, and `BOOTSTRAP_PYTHON`: unset.
- `TMPDIR`: absolute path `/var/folders/cp/bbqcpp814bjd_6mfhk6lxf7r0000gn/T/` (the top-level normalization would remove its trailing slash).
- No `.venv-paper2` or `.venv` is delivered.

## Completion decision

All delivered wrappers, scripts, verifiers, Python imports, manifest/archive generation logic, requirements, TeX resource declarations, and code-facing manuscript claims were inspected before execution. There are no hidden project imports. The canonical runner then completed successfully in a disposable environment, and the source archive/PDF were reproduced byte-for-byte. Local/remote tag resolution and direct commit-tree comparison bind the included scientific whitelist to the claimed commit.

The assigned software audit is complete. CODE-01 remains a high-severity false-pass defect and should be corrected before treating the convenience runner as fail-closed under arbitrary inherited environments. CODE-03 and CODE-04 remain reproducibility limitations. A successful replay is evidence only for the bounded finite/algebraic claims in the coverage table; the principal weak-cut and stochastic asymptotic arguments still require mathematical proof review.
