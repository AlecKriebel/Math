# PR1080 verification kit, version 1.0 repaired candidate

This accompanies **A credited finiteness deduction for restricted boundary-twist factorizations**, by Alec Kriebel, independent researcher, ORCID [0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X). Authored materials use CC BY 4.0. Extensive AI assistance was used. This is unrefereed, with no external human peer review or formal certification. The native metadata records local preparation on 14 October 2026 UTC. One complete whole-candidate review found two package issues; this repair requires a fresh complete second review. Publication readiness remains false. `CURRENT_STATUS_REPAIR01.json` supersedes dated pending-count statements without changing historical records.

For each fixed g>=1 on oriented compact S(g,1), maps and isotopies fix its sole boundary pointwise. Ordered positive factorizations of ONE positive boundary twist use non-null-homotopic simple closed curves, permit repetitions and require pairwise geometric intersection <=1. There are finitely many simultaneous-conjugacy classes, hence finite attained M(g), with 4g(2g+1)<=M(g). Peripheral factors are singleton only; otherwise factors are nonseparating. M(1)=12 and M(2)=40 are credited prior deductions.

The separately printed restricted arbitrary-length clause in Wajnryb/Farb, printed126/PDF133, is answered negatively under these conventions. Exact M(g) for g>=3, explicit upper formulas, an effective stopping criterion, extremizers, Hurwitz, positive Artin, T-move and A5/D6 classifications remain unresolved in this work. Historical novelty, exact application priority and worldwide current-open status are UNKNOWN. This is a credited deduction/exposition, with CT2208.05869v3 Cor4.13 explicitly supplying the finite-alphabet prior corollary, JMM/MRT support methods and the CFP ribbon/complement mechanism explicitly adapted to a marked disconnected bordered union. HKM, Smith, the chain relation and BMVHM lengths remain credited premises.

## Included evidence and historical boundaries

`preprint.tex` is standalone; its delivered PDF is external to this kit. `originals/submitted` preserves all six original files exactly. Complete subsequent mathematical and priority reports, frozen derivations, root adoption, authored source/custody metadata, reviewer programs and selected finite outputs are preserved under `originals`. Historical verdicts are unchanged and describe their earlier scope; later CT prior-corollary adoption controls the current framing. `COPY_EXCLUSION_LEDGER.json` individually maps every preexisting audit artifact and every path/hash entry in copied historical receipts to an exact canonical copy or an explicit omission. A mapped duplicate is not a recreated original path.

No third-party full PDF, extracted body, source image, raw service/Git filename capture, environment or duplicate archive is included. Some historical receipts reference omitted artifacts; their seals cannot all be rerun in this kit. Source versions, hashes, actual historical read scopes and access gaps remain metadata. No preprint/journal byte equality or exhaustive priority search is certified.

The original six-file edition has no executable. `run_checks.py` is a NEW portable adapter of the three subsequent reviewer programs. It copies original program bytes to temporary scratch, replaces every assertion with an explicit runtime guard, and leaves preserved files unchanged. The word checker matches the old result exactly; the surface checker matches excluding its run timestamp and uses the canonical six-file snapshot. The priority adapter keeps all mathematical computations, cuts only the historical workspace/52-input custody tail at a checked AST anchor, and verifies kit custody separately. It does not replay those omitted historical inputs. All adapter source hashes are pinned explicitly. Empty words, repetitions, noncentral targets, scrambled equivalence, missing normality, nonerasing expansions, ribbon order, isolated circles and multiple crossings have finite controls. These are fault detection, not a universal proof of geometry, Higman or cited theorems.

## Clean extraction and positive commands

From the delivery folder containing `verification_kit.zip`, run these exact commands with Python 3.11 or later, `unzip`, `cmp`, and Tectonic available. Python checks use only the standard library. Tectonic may need its normal package cache or network access for initial TeX packages; no special local source files are needed. The standalone PDF need not be byte-identical across TeX runtimes; the ZIP rebuild is byte-identical.

```sh
unzip -q verification_kit.zip -d clean_check
cd clean_check/verification_kit
python3 -I verify.py
python3 -I run_checks.py
python3 -I -O run_checks.py
python3 -I fault_checks.py
python3 -I output_guard_checks.py
python3 -I build_archive.py --output ../rebuilt.zip
cmp ../../verification_kit.zip ../rebuilt.zip
python3 -I verify.py --require-binding --binding ../../EXTERNAL_BINDING.json --pdf ../../preprint.pdf --archive ../../verification_kit.zip
mkdir -p ../compiled
tectonic --outdir ../compiled preprint.tex
```

The default verifier works from clean extraction without any external binding. If an adjacent `../EXTERNAL_BINDING.json` exists, it is always checked strictly, including bound PDF and ZIP files. `--binding` also checks strictly and fails for a missing, malformed or mismatched supplied binding. `--require-binding` fails if neither an explicit nor adjacent binding is available. Artifact overrides support relocated extraction. A PDF/ZIP/binding combination must come from the same candidate.

Current Python checks and archive/binding rebuilds were actually rerun after repair. Real compilation and all seven page views were last checked by complete whole01 on the unchanged paper. This bounded interface repair makes no new compilation or page-view claim; fresh complete whole02 must check them again. Captured earlier preparation and review receipts retain their exact dated meaning.

`fault_checks.py` checks three altered mathematical mechanisms and eight custody faults under normal and optimized Python: omitted conjugation, wrong parity, an erasing expansion, changed member, extra file, unsafe manifest path, symlink, missing required/explicit binding, malformed present binding and wrong present binding. Every injected fault must fail with nonzero exit. Temporary copies are removed automatically; the kit stays unchanged.

## Archive integrity contract

`ALLOWLIST.json` is the explicit sorted member list. `MANIFEST.json` hashes every allowlisted member except itself, avoiding a self-hash cycle. The external binding hashes that manifest and metadata and binds the delivered PDF and ZIP; it is excluded from the ZIP, as are the PDF, wrapper reports, render scratch and delivery metadata duplicates. The verifier rejects missing/extra files and directories, noncanonical or unsafe paths, symlinks and incorrect copy hashes. Without an external binding, this is internal consistency and accidental-corruption detection, not a signature or authentication of author intent.

`build_archive.py` verifies existing pins before building and never silently regenerates them. It uses stored ZIP members in explicit sorted order, UTC date 2026-10-14 00:00:00, Unix regular-file mode 0644, no directory records and no archive comments. The deterministic promise therefore does not depend on a zlib version. There is no program in this kit for resealing changed evidence. Any revised candidate requires a newly reviewed manifest and binding.

## Native metadata, historical stage resolution, and output safety

`metadata.json` is native Zenodo API metadata and equals the external bare metadata and the `metadata` object of the external `{metadata, files}` upload manifest. `research_metadata.json` preserves the original custom research object unchanged; it is historical research metadata rather than API metadata. The external binding checks both objects and the complete upload manifest before affirming attachment identities. Its manifest hashes have no cycle: native/custom metadata and captured-before stage copies are kit payloads; the live PDF, ZIP, upload manifest and binding remain external.

`REPAIR01_STAGE_COPIES.json` enumerates exact immutable old-stage copies. `REPAIR01_HISTORY_RESOLUTION.json` checks all 309 immediate inputs, all 194 preparation inputs, all 90 preparation outputs, all 289 whole01 inputs and all 17 whole01 outputs against exact current/captured-stage copies or individual omissions. The prior 269-reference ledger is also checked unchanged. An omitted primary body is not represented as a delivered or replayed source. Captured old code and archives are history, not current executable instructions.

The archive builder accepts only a fresh output file outside the kit, with an existing ordinary parent directory. It rejects the unresolved leaf and every symlink ancestor before any archive write, including dangling symlinks and paths through aliases. Every existing destination is rejected, covering hardlinks to all kit inputs, external PDF/TeX, upload metadata, descriptors, and sentinels. Creation uses exclusive mode, so an existing file or leaf symlink appearing between preflight and open is not truncated. A fresh independent outside rebuild destination works in both Python modes. Rebuild commands require a fresh filename; remove only your own previous rebuild before repeating them.

`output_guard_checks.py` exercises direct and nested protected paths, hardlinks to every kit input and external delivery-like files, outside symlink targets, symlinked ancestors (including paths containing `..`), and existing sentinels under normal and optimized Python. Rejections are checked against all protected input and sentinel hashes. Positive rebuilds are byte-identical. Other command interfaces expose no user-supplied file destination; reviewer calculations write only their own fresh temporary scratch. Direct Tectonic compilation is a separately documented source compilation command, not a writer offered by the kit CLI.

## Dated metadata administrative substage

Native metadata workflow notes now explicitly describe the bounded-repair checkpoint on 14 October 2026, in the past tense. They do not assert a permanent pending review or nonpublication state. The title, description, authors, ORCID, publication date, version, license, mathematical paper and source credits are unchanged. Later readiness/publication state is recorded separately. The dated-metadata substage on 15 October 2026 is still pending a NEW complete whole02; current readiness/publication remain false and services remain held at PR1032. Completed repair01 outputs and its 42-output inventory/seal remain immutable captured stages. The existing stage-copy ledger appends exact new before/captured-output copies, and the history-resolution ledger preserves every old row and appends exact successor-stage references with individual omissions. `METADATA_DATE02_ADMIN_STAGE.json` records the dated successor checkpoint. No new compilation, rendering or page view occurred in this administrative substage.
