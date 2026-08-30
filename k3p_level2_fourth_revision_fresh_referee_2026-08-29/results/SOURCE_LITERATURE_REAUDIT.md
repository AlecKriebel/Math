# Source/PDF reproducibility and literature re-audit

**Audit date:** 2026-08-29

**Reviewed package:**
`/Users/alec/Documents/Math/k3p_level2_fourth_revision_referee_final_2026-08-29`

**Audit workspace:**
`/Users/alec/Documents/Math/k3p_level2_fourth_revision_fresh_referee_2026-08-29`

**Package proof-source and builder commit:**
`10bd695cc7b7e0fd98a187026059b043589244f0`

## Verdict

**The prior F4 source/PDF reproducibility finding is closed.** The fourth
revision binds the TeX resource contract, constructs a minimal Tectonic child
environment, forces cached-only operation, and seals final-commit reports and
all four build transcripts. A fresh offline replay in this audit completed four
Tectonic builds—two article and two supplement builds—and every output was
byte-identical to the corresponding delivered and committed PDF. An independent
checker, which imports no package implementation, also found that every source
member equals the pinned Git blob and independently reconstructed both ZIP byte
strings exactly.

The bounded primary-source literature regression found no identified result
that subsumes the paper's claimed complete strong level-2 K3P containment
classification. That is a bounded novelty check, not proof that no relevant
unindexed or unpublished result exists.

I found one **minor, nonblocking release-documentation inconsistency**:
`proof_package/release/FINAL_RELEASE_ENGINEERING_REPORT.md:22-54` continues to
call third-revision commits, PDF hashes, and a 624-file handoff “current.” The
same file explains at lines 66-70 that these are historical and that manifests
are authoritative, and `START_HERE.md:13-18` explicitly labels the report a
historical execution ledger and points to the current sealed evidence. The
current `PACKAGE_MANIFEST.json`, PDFs, source ZIPs, JSON reports, and transcripts
are mutually correct. This wording should be repaired if the package is resealed,
but it is not a failure of the current source-reproduction certificate.

| Prior F4 obligation | Fresh result |
|---|---|
| Source ZIP members equal exact final-commit Git blobs | **PASS**: article 23/23; supplement 1/1 |
| Source ZIPs satisfy their manifests and canonical byte rules | **PASS**: both independently rebuilt byte-identically |
| Tectonic bundle/cache is immutable and inspectably bound | **PASS**: URL, bundle digest, exact 725-file inventory, and manifest hashes bound |
| Caller environment is not inherited by Tectonic | **PASS**: exact 12-key child environment enforced |
| PDF run is forced cached-only and cache is unchanged | **PASS**: `--only-cached`; exact inventory verified before and after |
| Final-commit reports/transcripts are delivered and sealed | **PASS**: two reports and four transcripts in the 635-file outer seal |
| Fresh final-commit article replay | **PASS**: two completed builds, both exact |
| Fresh final-commit supplement replay | **PASS**: two completed builds, both exact |

## 1. Independent source-archive and Git-blob checks

The checker at `independent_checks/source_contract_check.py` reads the source
ZIPs directly, obtains the source bytes with `git show` at the package-declared
commit, implements canonical JSON/ZIP construction locally, and imports no code
from the reviewed package. It also checks the exact cache inventory and both
sealed and fresh source-reproduction reports.

| Property | Article | Reader supplement |
|---|---:|---:|
| Source ZIP bytes | 103,178 | 58,031 |
| Source ZIP SHA-256 | `25a5730c31cdeffba4158203307a1be2d583e56e9cac5b0cc9922f8899ff3dba` | `34441c556277f152c96b88f2165afa450f905e1d7563aeeeb2115bd70148d5be` |
| Total ZIP members | 26 | 4 |
| Git-bound TeX/Bib/figure source members | 23 | 1 |
| Git-blob mismatches | 0 | 0 |
| Git-source logical payload SHA-256 | `69b99af144229f8e6e5cd108ec6f30a078a87ef848d0fd68f2ecc525c2a8be52` | `b754c898f1d6aebf1435e84865a7a1a392741db179ce8f3a1960ef2184d0a252` |
| Archive-manifest logical payload SHA-256 | `bf26665553018c27394618d176870b58057859b5b3c1bf3d3100e398f1a71f34` | `4b4400a270c6e6da2b121e01b4bca25a3fdf601c2ccb32e855d4373a8af84e37` |
| Independent canonical reconstruction | byte-identical | byte-identical |

Both copies of each source ZIP—under `proof_package/release/dist/` and
`proof_package/source_archives/`—are identical. The archives bind commit
`10bd695c...` and commit epoch `1788044340`; the independently checked member
timestamp is 2026-08-29 22:59:00 UTC. The article archive contains its 23
committed manuscript sources plus `SOURCE_BUILD.json`,
`TECTONIC_CACHE_MANIFEST.json`, and `ARCHIVE_MANIFEST.json`; the supplement has
its one committed TeX source plus the same three metadata members.

The delivered PDFs themselves equal Git blobs at the declared commit:

| PDF | Pages | Bytes | SHA-256 |
|---|---:|---:|---|
| Article | 38 | 258,655 | `3d08a722ba1fa53f6e336ab285c1cd32d1307bac08e1d4dd2460da71df1816d6` |
| Reader supplement | 14 | 130,849 | `96508f4b4eddb89de99881172abee307b3fe86d236f48e17508bdd1ca9c30efa` |

Relevant package implementation is fail-closed on the checked properties:

- `release/verify_source_reproduction.py:70-124` requires the complete build
  metadata, command, toolchain, resource, environment, and execution-policy
  fields.
- Lines 127-219 validate the cache manifest and require equality of the entire
  expected and observed cache file sets; missing, extra, and changed files fail.
- Lines 222-323 compare archive source members with committed Git blobs.
- Lines 340-350 pin both Tectonic version and executable bytes.
- Lines 381-444 construct the 12-key child environment and execute the exact
  cached-only command.
- Lines 447-560 perform exactly two builds, recheck the cache, require equality
  with the committed PDF, and emit the report and transcripts.

## 2. Bundle, cache, executable, and environment contract

The package now binds:

- bundle URL:
  `https://relay.fullyjustified.net/default_bundle_v33.tar`;
- bundle digest:
  `6ffe055852f8faf66c0acbe1a7fb27f87b869a90bad1204f3bf4d9683f597c7c`;
- cache-manifest file SHA-256:
  `c6908223e76a095fec120af0c267567a057de56c3e497b61c20829fb2433297a`;
- cache-manifest logical payload SHA-256:
  `1edd1b2750c04fba762ef5094f97f572fdef1905e1ba0447ab13985f232b07ba`;
- exact cache inventory: 725 regular files and 57,507,581 bytes;
- Tectonic version: `Tectonic 0.16.9`;
- executable:
  `/opt/homebrew/Cellar/tectonic/0.16.9/bin/tectonic` (Mach-O arm64);
- executable SHA-256:
  `38eff9059ed622672c9a2590415a8f01c043df4232baa459628a2cd86e512d95`;
- command policy: explicit bundle plus `--only-cached`;
- a 12-key child environment with fixed `/usr/bin:/bin` `PATH`, private
  `HOME`, `TMPDIR`, XDG, and TeX directories, fixed epoch, UTC, and C locale.

The host's shared Tectonic cache contained all 725 expected files with correct
bytes but also one unrelated extra file,
`bundles/data/6ffe.../lmri8.pfb`. I therefore did not relax the contract or use
that nonexact cache. I made a private audit copy, removed that explicit extra
member at
`bundles/data/6ffe055852f8faf66c0acbe1a7fb27f87b869a90bad1204f3bf4d9683f597c7c/lmri8.pfb`,
and independently established an exact 725-file match before building.
The private cache remained exactly 725 files and 57,507,581 bytes, with no
missing, extra, or changed member, after all four builds. The package verifier's
set-equality check would correctly reject the unmodified shared cache.

This closes the former unbound-resource and inherited-environment defects. It
does **not** make the source ZIPs universally self-contained: the 56 MB cache
payload and the arm64 executable are intentionally not vendored. That boundary
is accurately disclosed in `START_HERE.md:157-167` and
`proof_package/release/ENVIRONMENT.md:15-33`. A byte-identical rebuild is fresh
and feasible on this matching Apple-silicon host when the declared external
binary and exact cache are supplied; it is not feasible from the extracted ZIP
alone on an arbitrary architecture.

## 3. Sealed final-commit reports and transcripts

`PACKAGE_MANIFEST.json` binds 635 payload files and identifies both the proof
source and package-builder commit as `10bd695c...`. Its current PDF, archive,
report, and transcript rows agree with the files delivered in the package.

| Evidence | Sealed file SHA-256 | Bound logical/transcript SHA-256 |
|---|---|---|
| Article report | `8ca6a34c91202f6b4f6afcb04ffb224108960eaeb49dde330eaed80cf2a80a50` | logical `d404ad7b99cd4b75386c97aa4fd6d700eba53f1eee8c4039b1b843afa539cd4f` |
| Article run 1 | — | `5e7646240aabd5da7861f72b114f4ac0b62dfbff816e028c1a3995ec97eb34aa` |
| Article run 2 | — | `5e7646240aabd5da7861f72b114f4ac0b62dfbff816e028c1a3995ec97eb34aa` |
| Supplement report | `de78b77c9c59eb6ab4940fbd5b046518ca79eb933ba0a41471eced6cecc64973` | logical `9431b8d933ec9a236c30dd288f5bbbdbe21f6710e1746bd313192d1fe77c423e` |
| Supplement run 1 | — | `97e163812cc2ccabcb28b405dd835741a1d12e914ec35d5e0ba140105456575b` |
| Supplement run 2 | — | `a95ec4949256ae3dc81654c3491bb55b71abc674748a801fa9264418b856f661` |

The independent checker recomputed each report's internal logical hash,
recomputed the four transcript hashes, and compared both full JSON files to
their byte/size/mode rows in the outer manifest. All checks passed. The fresh
full JSON files have different hashes because they contain fresh timings and
audit-local transcript paths—article
`a527e45f6f21c95a96600bf562c92aac5d79bf6e26af88f73b2ff2b05ab91cf6`,
supplement
`015d74378256caff22dc56a92ed6d099a1ee600cf70c79b41b06cd2355091042`—
but their logical payload hashes equal the sealed reports exactly, and every
fresh transcript hash equals its sealed counterpart.

## 4. Fresh offline build execution

I first inspected the entire 569-line source verifier and the canonical archive
helpers. I then used a local detached checkout at exact commit `10bd695c...`, a
private manifest-exact cache, and the default-deny macOS Seatbelt profile
`logs/source_reproduction_offline.sb` (SHA-256
`b54c077bf83c46d890dad35895c5503008fb0947df4a580fba1b9b4b5c206330`).
The profile denies network access and allows writes only inside this audit's
ignored execution area. No `RUN_REVIEW`, theorem regeneration, or hour-scale
producer was invoked.

The exact successful article command, run from the detached project root
`/Users/alec/Documents/Math/k3p_level2_fourth_revision_fresh_referee_2026-08-29/execution/source_literature_reaudit/repo/k3p_level2_identifiability_final`,
was:

```sh
/usr/bin/sandbox-exec -f /Users/alec/Documents/Math/k3p_level2_fourth_revision_fresh_referee_2026-08-29/logs/source_reproduction_offline.sb /usr/bin/env -i HOME=/Users/alec/Documents/Math/k3p_level2_fourth_revision_fresh_referee_2026-08-29/execution/source_literature_reaudit/runtime_home TMPDIR=/Users/alec/Documents/Math/k3p_level2_fourth_revision_fresh_referee_2026-08-29/execution/source_literature_reaudit/runtime_tmp PATH=/opt/homebrew/bin:/usr/bin:/bin LANG=C LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 release/verify_source_reproduction.py --kind article --tectonic /opt/homebrew/Cellar/tectonic/0.16.9/bin/tectonic --tectonic-cache-root /Users/alec/Documents/Math/k3p_level2_fourth_revision_fresh_referee_2026-08-29/execution/source_literature_reaudit/cache --report release/work/source_literature_reaudit/article.json
```

It returned `K3P_SOURCE_REPRODUCTION_PASS` in approximately 7.155 seconds. Its
two internal builds took exactly 3.0540879999753088 and 3.062378417002037
seconds. Both produced 258,655 bytes with SHA-256 `3d08a722...`, equal to each
other, the delivered PDF, and the Git blob.

The exact successful supplement command differed only in kind and report:

```sh
/usr/bin/sandbox-exec -f /Users/alec/Documents/Math/k3p_level2_fourth_revision_fresh_referee_2026-08-29/logs/source_reproduction_offline.sb /usr/bin/env -i HOME=/Users/alec/Documents/Math/k3p_level2_fourth_revision_fresh_referee_2026-08-29/execution/source_literature_reaudit/runtime_home TMPDIR=/Users/alec/Documents/Math/k3p_level2_fourth_revision_fresh_referee_2026-08-29/execution/source_literature_reaudit/runtime_tmp PATH=/opt/homebrew/bin:/usr/bin:/bin LANG=C LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 release/verify_source_reproduction.py --kind supplement --tectonic /opt/homebrew/Cellar/tectonic/0.16.9/bin/tectonic --tectonic-cache-root /Users/alec/Documents/Math/k3p_level2_fourth_revision_fresh_referee_2026-08-29/execution/source_literature_reaudit/cache --report release/work/source_literature_reaudit/supplement.json
```

It returned `K3P_SOURCE_REPRODUCTION_PASS` in approximately 2.012 seconds. Its
two internal builds took exactly 0.8178287500049919 and 0.8013161248527467
seconds. Both produced 130,849 bytes with SHA-256 `96508f4b...`, equal to each
other, the delivered PDF, and the Git blob.

For complete command-count accounting, there were **three source-verifier
process invocations and four completed Tectonic builds**. Before the successful
article command, one article invocation with outer launcher
`PATH=/usr/bin:/bin` exited in about 0.2 seconds, before Tectonic or either build
started, because macOS's `/usr/bin/git` developer-tool shim could not read the
`xcode-select` state under the narrow sandbox. It emitted
`K3P_SOURCE_REPRODUCTION_FAIL` at `git rev-parse --show-toplevel` and created no
report or transcript. The launcher was then changed to prefer the already
installed `/opt/homebrew/bin/git`; no sandbox permission and no Tectonic child
policy was relaxed. The package constructs the actual Tectonic child separately
with its exact fixed 12-key environment and `/usr/bin:/bin` child `PATH`.
There was one completed article verifier run and one completed supplement
verifier run, each performing its specified two builds; neither successful
command was repeated.

The independent post-build command was:

```sh
python3 independent_checks/source_contract_check.py --package /Users/alec/Documents/Math/k3p_level2_fourth_revision_referee_final_2026-08-29 --repo /Users/alec/Documents/Math --cache-root execution/source_literature_reaudit/cache --fresh-reports execution/source_literature_reaudit/repo/k3p_level2_identifiability_final/release/work/source_literature_reaudit
```

It completed in approximately 0.6 seconds with `"status": "PASS"`. The checker
itself has SHA-256
`2b62cb3891adb8501c2995087429ad6706700ab30047868ec9f1d3fd94f70b1c`.

## 5. Bounded primary-source literature regression

I compared the manuscript's positioning at
`manuscript/sections/01_introduction.tex:31-84` and its precise use of Brits et
al. at `manuscript/sections/05_three_leaf_geometry.tex:46-51` against direct
primary-source pages available on 2026-08-29. The most relevant checks were:

- [Brits, Holtgrefe, van Iersel, and Martin, arXiv:2607.12919v3](https://arxiv.org/abs/2607.12919v3)
  is the current 25 August 2026 revision. Its main full-identifiability result is
  for level-1 semi-directed networks (with ordinary-triangle redirection as the
  familiar ambiguity), not a complete general level-2 K3P containment theorem.
  Its tree--sunlet statement has the restricted stochastic/nonidentity/positive-
  definite parameter-space qualifications that the manuscript expressly records.
- [Englander et al., bioRxiv DOI 10.1101/2025.04.18.649493](https://doi.org/10.1101/2025.04.18.649493)
  treats strong, triangle-free level-2 identifiability under JC and related
  displayed-quartet tools; this does not subsume the K3P theorem with triangles.
- [Currie et al., arXiv:2606.26673](https://arxiv.org/abs/2606.26673)
  studies semialgebraic identifiability of the three triangle orientations under
  JC. That is relevant local triangle geometry, but a different model and not a
  global K3P level-2 containment classification.
- [Cummings and Hollering, arXiv:2311.07678](https://arxiv.org/abs/2311.07678)
  develops multigraded implicitization and K3P four-/five-leaf sunlet invariant
  computations. It is local low-degree implicitization, not the claimed global
  classification; the manuscript's four-leaf computation and 100-day comparison
  are consistent with the primary text checked.
- [Ardiyansyah, arXiv:2104.12479](https://arxiv.org/abs/2104.12479)
  gives distinguishability results for some simple and semisimple level-2
  networks, appropriately described by the manuscript as partial.
- [Hollering and Sullivant, arXiv:1909.13754](https://arxiv.org/abs/1909.13754)
  concerns algebraic-matroid identifiability, including K2P/K3P level-1 cycle
  networks, not the present level-2 classification.
- [Gross, Krone, and Martin, arXiv:2307.15166](https://arxiv.org/abs/2307.15166)
  studies dimensions of level-1 group-based networks and does not supply the
  asserted level-2 result.
- A very recent adjacent paper,
  [Cummings et al., arXiv:2608.03544](https://arxiv.org/abs/2608.03544),
  studies level-1 networks under a multispecies-coalescent/quintet-concordance
  framework. Its data and model are different and it does not supersede the K3P
  site-pattern containment theorem.

No checked primary source contradicted the manuscript's model/scope
qualifications, and no checked source supplied the same complete theorem. This
conclusion is an inference from a bounded check of the named closest literature
and current arXiv results, not an exhaustive novelty guarantee.

## 6. Remaining limitations and recommended disposition

1. **External platform-specific inputs remain necessary.** The arm64 Tectonic
   binary and 56 MB cache are hash-bound but not vendored. I used existing local
   bytes; I did not independently download or reconstruct the cache from the
   bundle URL. A reviewer on a different architecture cannot reproduce the PDF
   byte strings from the source ZIP alone.
2. **The package source verifier requires the exact live Git checkout.** This is
   disclosed at `START_HERE.md:142-148`; the portable mathematical runner is a
   different entrypoint. My build used a detached checkout at the exact commit.
3. **Cached-only is not a general hostile-executable sandbox.** The verifier
   controls the command and environment and tells Tectonic not to fetch. The
   audit additionally used OS-level network denial, as the package documentation
   recommends.
4. **Literature review was bounded.** It covered the manuscript's closest named
   primary sources and current adjacent arXiv results, not every database or
   unpublished manuscript.
5. **This track did not rerun mathematical producers or perform a new visual
   page-layout audit.** Those tasks are outside this source/literature sub-audit.

Recommended disposition for this track: **no source/PDF or literature blocker**.
Treat the stale “current” wording in the historical release ledger as a
**minor/low-severity documentation defect** and relabel it at the next safe
reseal. Do not conflate that historical prose with the current sealed JSON
evidence, which independently passed.
