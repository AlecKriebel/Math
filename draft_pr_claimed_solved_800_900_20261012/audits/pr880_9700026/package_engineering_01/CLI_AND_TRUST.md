# PR880 current package interfaces and trust

These tools authenticate artifacts and reproduce finite diagnostics. They do not certify a universal mathematical statement, source interpretation, priority, novelty or historical execution counts. They preserve all forty original files unchanged in portable `source/`; the original root wrapper is authenticated as data and never executed by these tools.

## Authenticate startup before execution

An index containing a program's own digest cannot authenticate that program's initial execution. Obtain the program digest and the index/outer-manifest digest through an independently trusted channel. Authenticate the bootstrap, interpreter and standard library independently as well. Do not replace an expected digest with a hash recomputed from an untrusted copy and call that authentication.

The following small trusted caller illustrates authentication **before** compiling or executing the script bytes. Supply `EXPECTED_SCRIPT_SHA`, the script path and its ordinary CLI arguments as positional arguments to this caller. Its startup digest must itself come from outside the untrusted tree. It is an example for a trusted local caller, not a concurrent-adversary sandbox.

```python
# Invoke as: python3 -I -S -B trusted_start.py EXPECTED_SCRIPT_SHA script.py [arguments...]
import hashlib, os, re, stat, sys
from pathlib import Path
expected, filename, *arguments = sys.argv[1:]
if not re.fullmatch(r"[0-9a-f]{64}", expected):
    raise SystemExit("invalid expected script digest")
path = Path(filename).absolute()
if not stat.S_ISREG(path.lstat().st_mode):
    raise SystemExit("script must be an ordinary file")
fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
             | getattr(os, "O_NONBLOCK", 0))
with os.fdopen(fd, "rb") as stream:
    info = os.fstat(stream.fileno())
    if not stat.S_ISREG(info.st_mode) or info.st_size > 1024 * 1024:
        raise SystemExit("unsafe script type/size")
    raw = stream.read(1024 * 1024 + 1)
if len(raw) != info.st_size or hashlib.sha256(raw).hexdigest() != expected:
    raise SystemExit("script startup pin mismatch")
sys.argv = [str(path), *arguments]
exec(compile(raw, str(path), "exec"), {"__name__": "__main__", "__file__": str(path)})
```

All current scripts require Python 3.10 or newer with `-I -S -B`. Optimized execution adds `-O`; their checks do not rely on `assert`. Child programs execute only authenticated byte copies in fresh relocated directories from unrelated working directories. The scripts reject symlinks, FIFOs and other nonregular entries inside selected trees, including empty extra directories. They use strict JSON parsing and typed inventory rows. They assume no concurrent adversary replaces authenticated inputs during use.

## Portable checker and verifier

```text
check_originals.py --root PORTABLE [--verify-only]
    [--catalog CATALOG --problems PROBLEMS --reports REPORTS --pdf-dir PDF_DIRECTORY]
    [--pdf-2012 EXPLICIT_2012_PDF]

verify_package.py INDEX_SHA256 --root PORTABLE [--full]
    [--catalog CATALOG --problems PROBLEMS --reports REPORTS --pdf-dir PDF_DIRECTORY]
    [--pdf-2012 EXPLICIT_2012_PDF]
```

`check_originals` authenticates the fixed source manifest, its exact forty-file subtree, Git blob identities, file modes, every original JSON document, both archives, the nested author archive, internal manifests and readable duplicates. By default it replays the original author witness/self-test and independent audit witness/self-test under normal and optimized Python, matching complete expected stdout bytes. `--verify-only` performs authentication without executing any original child; finite diagnostics and source replay are explicitly `NOT_RUN`.

`verify_package` requires an externally pinned `package_index.json` with exactly `schema`, `problem_id`, and `files`; schema is `city-ode-verification-v1`, problem ID is the string `9700026`. Rows contain exactly `path`, integer `bytes` and lowercase hexadecimal `sha256`. The index excludes itself. It must include the checker, verifier, builder and `root_evidence/SOURCE_MANIFEST.json`; the complete file and directory inventory must match. `--full` adds the checker replay. Source locations require `--full` here.

The four source locations are all-or-none in every interface. `--pdf-2012` additionally requires all four; it explicitly maps an ordinary file such as private `1209.5120v1.pdf` to the original checker's `cities-2012.pdf`. The notes PDF remains `PDF_DIRECTORY/cities-notes.pdf`. Every complete corpus and both PDFs must match fixed size/SHA pins, all corpus JSON is strictly parsed, exact int/string target IDs must be unique, and the complete canonical record/report pair must match 4409 bytes / SHA256 `7b18458d71482e2c4e1c62601be1824eba6ad6243c78135d90d1b75223e8e193` before any child starts. Source-free runs always say `NOT_RUN`; supplying sources with `--verify-only` can authenticate them but cannot claim source replay.

Complete inputs are never copied into a public tree or ZIP. For optional legacy replay, only verified ordinary-file hardlinks with required basenames are made in a temporary directory. The inspected original source checker reads them without writing, changing permissions or truncating them. No negative fixture uses these links. Same-filesystem link support is required; a failed link operation rejects the run rather than silently copying a corpus. Temporary links are removed on normal and exception exits; SIGKILL/crash cleanup is not guaranteed.

## Deterministic portable ZIP builder

```text
build_verification.py ASSEMBLY INDEX_SHA256 VERIFIER_SHA256 OUTPUT_DIRECTORY
```

Authenticate the builder's startup bytes externally before invocation. The builder authenticates the external index, the verifier's independent digest, its own indexed copy and every assembly file. It runs the authenticated verifier with `--full` on a relocated byte copy before creating the archive. Source replay is not part of this builder interface; run it separately with explicit source locations.

`OUTPUT_DIRECTORY` is a directory, not a ZIP filename. It must be fresh or an empty ordinary directory outside the input assembly. A symlink leaf, a nonempty directory, an ordinary file/FIFO, an assembly descendant or an input collision is rejected. The output file is exclusively created as `OUTPUT_DIRECTORY/verification.zip`; existing output is never overwritten. Parent directories can be created before replay, but no archive is written on a validation failure. This assumes no concurrent replacement of output ancestors.

The archive uses sorted relative paths, timestamp 2026-10-15 00:00:00, Unix ordinary-file mode 100644 and DEFLATE level 9. Compressed-byte reproducibility is asserted only for identical inputs and the same Python ZIP implementation/zlib runtime; the receipt records those runtime versions. The independent verifier checks index/inventory identity, not mathematical truth.

## Current outer wrapper and exact layout

Copy `local_tools/pr880_verify_current_publication.py` to the current outer root as `verify_current_publication.py`, and authenticate its startup digest externally. Its CLI is:

```text
verify_current_publication.py OUTER_MANIFEST_SHA256 --root CURRENT_ROOT [--full]
    [all four source locations] [--pdf-2012 EXPLICIT_2012_PDF]
```

The current `PUBLICATION_MANIFEST.json` has exactly `schema`, string `problem_id`, and `files`, using schema `city-ode-current-publication-v1`; it excludes itself and closes the entire outer file/directory tree. The wrapper requires current root `README.md`, `RESEARCH_LOG.md`, `CURRENT_PUBLICATION.json`, itself, and the manifest. Thirty-eight other frozen root paths, including the historical wrapper, must remain byte-identical. All forty originals, including the archived README/manifest, remain unchanged inside the portable subtree.

The layout is fixed:

```text
CURRENT_ROOT/
  [38 preserved frozen original paths]
  README.md
  RESEARCH_LOG.md
  CURRENT_PUBLICATION.json
  verify_current_publication.py
  PUBLICATION_MANIFEST.json
  publication_20261015/preprint/
    note.tex
    output/pdf/note.pdf
    README.md
    metadata.json
    CURRENT_PRIORITY.md
    check_originals.py
    verify_package.py
    build_verification.py
    package_index.json
    verification.zip
    zenodo-deposit.json
  publication_20261015/verification_package/
    [complete closed portable tree]
```

The ZIP guard rejects prefix/trailer bytes, gaps between local members and the central directory, and disagreement between local and central header metadata/names. This is a representation-boundary check and does not claim that a valid DEFLATE compressed bitstream is unique.

The preprint directory has exactly eleven core files. The portable copy has its own externally anchored index; the ZIP must have exactly its sorted member set and byte-identical contents, with the deterministic metadata above. The preprint note, PDF, README, metadata, priority text, three programs and index must agree with their portable counterparts (`note.pdf` at portable root). Additional evidence belongs outside the eleven-file preprint core or inside the indexed portable tree and must be explicitly listed by the outer manifest.

`CURRENT_PUBLICATION.json` must expose `zenodo_metadata`, identical to preprint `metadata.json`, portable `metadata.json`, and `zenodo-deposit.json`'s `metadata`. The deposit object has exactly `metadata` and `files`; its two upload bindings are `output/pdf/note.pdf` → `city-ode-persistence-note.pdf` and `verification.zip` → `city-ode-persistence-verification.zip`. These are consistency checks; the tools perform no deposit, release, Git, PR, sheet or network writes.

Counts are dynamic. If the portable tree has `P` files including its index and there are `E` additional outer evidence files outside the fixed root/core/portable sets, the current outer inventory has `P + 54 + E` files including its manifest. The minimum portable document/core/original arrangement has 50 files, but the parent supplies the real evidence allowlist and derives the final count. No production count, index hash or archive hash is asserted by the engineering fixture receipts.

## Explicit local assembly helper

```text
pr880_assemble.py BASE_DIRECTORY SPEC_JSON SPEC_SHA256 OUTPUT_DIRECTORY
```

The helper's startup and the spec digest must be independently authenticated. A spec has exactly `schema: city-ode-explicit-assembly-v1`, `kind: portable|outer`, and `files`. Each row has exactly `source`, `path`, `bytes`, and `sha256`; `source` is a safe relative input path within `BASE_DIRECTORY`, and `path` is its safe relative destination. Every input is read as an ordinary bounded file and pinned before writes. All portable originals must be explicitly listed. It generates only the appropriate excluded-self index and rejects generated-index exact/ancestor/descendant path collisions before output creation. Output must be fresh or empty and must not collide with input files. It reports `ASSEMBLED_REQUIRES_INDEPENDENT_VERIFICATION`; the parent must then run the authenticated current verifier, builder and outer wrapper as appropriate.

The helper does not discover evidence, choose publication scope, edit prose, execute supplied programs, certify claims, or publish. The parent has not supplied real paper/evidence lists yet; this engineering effort retained no real assembly, final index, final ZIP or outer candidate.

## Receipt versions

`GUARD_RESULTS_SOURCE_FREE.json` is the final-source-byte bridge: it directly records final outer hash `b8279f4945b2f05b3755bfec20ae6c78dbbb00d053abdb04f87d8068f2ff62a7` and assembler hash `939fea38779e6df5e81f7930a6a39153a082bcea046ad2879dabc4e0b8115055`, together with the unchanged three portable tool hashes. `GUARD_RESULTS_WITH_PROVENANCE.json` retains prior outer hash `465f9f4875740f282db18a13d1ea57137bb71708d3e87c1c6d8cf881d191abc6` and assembler hash `4523285345f0d9df2d8024db419769915494406e4446c27b882d005a62a8a893`. The two changed module docstrings are exactly reconstructible in `DOCSTRING_PROVENANCE.json`; stripping only those initial docstrings gives identical operational ASTs. The source-free fixture bridge executes the final outer/assembler CLIs successfully. No full-input PASS is invented for the final source-free invocation, and no complete-source replay was repeated solely for a documentation change.
