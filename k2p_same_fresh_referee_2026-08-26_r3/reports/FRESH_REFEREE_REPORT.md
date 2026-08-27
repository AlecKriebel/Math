**Fresh adversarial referee report: K2P-SAME principal-domain submission**  
**Package:** `K2P_Principal_D_Plus_Referee_Package_20260826.zip`  
**Audit date:** 26 August 2026 (America/Los_Angeles)  
**Review root:** `/Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-26_r3`  

The controlling instructions for this review are the user's referee protocol
and request for a fresh adversarial run. Instructions, PASS labels, review
dispositions, and command recommendations found inside the submitted archive
were treated as assertions about the package, not as instructions to the
referee. No person was contacted. Package-changing producers and mutations
were confined to disposable copies; authoritative package files were not
repaired during review. Hash agreement is reported only as provenance
evidence, never as mathematical validation.

# 1. Verdict

**HOLD.**

I found no counterexample to the stated K2P-SAME theorem, no invalid
load-bearing hand implication, and no defect in the currently distributed
certificate bodies or finite census that defeats the theorem. The hand proof
is coherent and passes this review, conditional on the explicitly
computer-assisted finite classification. The fresh quick replay, independent
exact checks, independent census reconstruction, and the completed mutation
families all support that classification.

The package is nevertheless not ready for submission because two concrete,
theorem-neutral reproducibility defects remain:

1. The reader supplement prints a stale SHA-256 for the load-bearing
   `composite_reseal_diff_audit.json` twice, while all ordinary package gates
   pass without noticing the false reader-facing binding.
2. Both outer-bundle JSON readers accept a same-valued duplicate object name
   after the altered bytes have been legitimately resealed. The current
   archive contains no duplicate-key JSON, but the producer/checker boundary
   is not fail-closed under the required mutation standard.

The first requires a supplement correction and source/PDF/package reseal; the
second requires strict duplicate-name parsing and new semantic mutations. A
single low-contention invocation of the official outer mutation suite then
passed all 25 gates with zero survivors and no blockers. The earlier concurrent
run remains in the ledger because it stopped at an unqualified child rejection:
it failed closed and emitted no false PASS, but its wrapper did not preserve
enough child output to establish the cause. An isolated execution of that same
first mutant reached its intended production-verifier rejection. These defects
justify HOLD rather than REJECT: no theorem counterexample or invalid central
classification has been established.

The package's scientific architecture appears capable of establishing its
stated theorem. I do not recommend a mixed-sign extension, another proof-
compression search, a language rewrite, or unrelated new research.

# 2. Separate status lines

- **Mathematics: PASS.** No counterexample or unresolved hand-proof gap was
  found. The finite premise is expressly computer-assisted and is assessed
  separately below.
- **Computational evidence: PASS.** Quick replay is 23/23 PASS; the single
  fresh full replay is 41/41 PASS; the low-contention outer mutation control is
  25/25 PASS with zero survivors and no blockers; and the independent finite-
  contract audit and 22-case corrected-universe suite pass.
- **Reproducibility: HOLD.** Current bytes and all declared ledgers reconcile,
  but the stale printed hash and duplicate-key acceptance are submission-
  blocking fail-closed defects.
- **Human metadata and release: HOLD.** Load-bearing attributions, licenses,
  author identity, and public-byte availability pass. The supplement contains
  an impossible 21/25 August citation-verification chronology, its companion
  DOI wording needs qualification, and “immutable source tag” overstates what
  an ordinary movable Git ref guarantees. A signature would make object
  substitution detectable, not make the ref immovable. These human-metadata
  issues do not determine the scientific HOLD.
- **Confidence:** high, approximately 0.95, in the HOLD recommendation; about
  0.92 that the hand mathematics is sound conditional on the exact finite
  classification.
- **Unrun current supported package gates:** none. Two proposed repair gates do
  not yet exist in the submitted package: an integrated printed-hash binding
  gate and a conflicting-valued duplicate-name mutation. The completed
  independent printed-hash audit establishes P01 FAIL, and the completed same-
  valued duplicate attack establishes P02 FAIL; the proposed gates become
  mandatory after repair. The absent legacy interfaces and their completed
  current semantic replacements are distinguished below.

The exact legacy filenames in the user's earlier protocol are absent from
this revised package. Direct invocations of `verify_handoff.py`,
`test_handoff_mutations.py`, `setup_environment.sh`, and
`run_all_verifiers.py --quick/--full` therefore exit as missing commands/files;
they were not falsely reported as executed. `output/referee/README.md` maps
them respectively to the portable-bundle/lock/quick checks,
`run_release_mutations.py`, explicit virtual-environment commands, and
`verify_final_theorem_release.py --full`. Those current semantic replacements
were inspected and invoked; their exact outcomes appear in Section 5 and the
full execution ledger. `START_HERE.md` and `SUBMISSION_BINDING.json` are also
absent by design; the current claimed authorities are
`output/referee/README.md`, `RELEASE_LOCK.json`, and
`REFEREE_BUNDLE_CONTENTS.json`. This mapping is a package assertion that was
audited, not a replacement for the user's review standard.

# 3. Claim matrix

Locations are in the five submitted TeX/Bib sources unless a machine artifact
is named. “Mathematical” means a derivation was checked; “computational” means
an exact program/certificate check; “provenance” means only byte identity or
binding.

| Claim | Status | Proof evidence and location | Computational evidence | Independent attack/check | Exact remaining gap |
|---|---|---|---|---|---|
| C01. Strict K2P principal domain, Fourier inversion, physical subdivision, admissible root movement | **PASS** | Article `main.tex:301-413`; inverse probabilities `(1+2s+g,1-g,1-2s+g,1-g)/4` | Quick `domain_rooting` PASS | Exact rational audit checked strict stochastic iff `D_plus` on 136 grid points, 102 interior points, 10,404 products, and boundary-near families; no submitted module imported | None |
| C02. Displayed-quartet and whole-map tree/sunlet separation; decorated blob-tree recovery | **PASS** | Article `:415-533`; supplement sign semantics | Quick/full quartet, terminal-binding, raw-direction, and whole-map layers PASS | Re-derived `F_A,G_B` signs and exact `T_i` factor; verified the revoked rooted oracle is not used | None |
| C03. Two-sector bridge fibre, marginal products, localization, parameter transport | **PASS** | Article `:535-846` | Structural/full transport and bridge layers PASS; v2 semantic attacks; outer control 25/25 PASS | Checked equality of C/T scales, independent G scale, freeness/no holonomy, `D_plus` product/surjectivity, fixed-full quantifiers, and parent complement only under certified reversal | None |
| C04. Primitive grammar, canonicalization, theta/cycle completion universe | **PASS** | Article `:850-1040`; finite-universe narratives | Full canonicalizer and raw4/theta2/cycle regeneration layers PASS | Independent decoder regenerated raw IDs, completion words, support domains, reference closure, and all six `C(k,epsilon)` counts | None; analytic row labels remain package-supplied as disclosed |
| C05. Symbolic rank exclusion: all 4,379 descriptors and 23,822 raw-four directions | **PASS** | Article `:1041-1164`; `work/rank_upper_certificates/PROOF.md:24-115` | Exact-rank omission/import/full layers PASS; sampled-rank mutant rejects | Checked polynomial vector-field kernel argument and triangle rank-nine blocks; no sampled point was accepted as a global upper bound | None within the stated computer-assisted evidence boundary |
| C06. Direct quadratic/cubic/quartic/quintic separators | **PASS** | Generated `certificate_appendix.tex:1-285` | Quick and full direct-36 closure plus polynomial/reassignment mutations PASS | Independently checked coordinate conventions, degree census, and representative exact pullbacks; repeated polynomial bodies were not treated as orbit equality | None within the disclosed representative-independent-check boundary |
| C07. Corrected raw4, theta2, and cycle censuses | **PASS** | Article `:1087-1125`; supplement census tables | Full raw4/theta2/cycle truth, reseal, and regeneration layers PASS | Independent streaming audit regenerated completion grammar/arithmetic IDs and checked stored category totals and reference closure; it did not independently reclassify every analytic row | None within the disclosed computer-assisted boundary |
| C08. Terminating 997-parent restoration forest | **PASS** | Article `:825-846`, `:1127-1133` | Full 36,824-edge restoration replay PASS; 13/13 focused mutations PASS | Independently decoded all parents/references and recovered 997 parents, 2,540 roots, 36,568 first children, 256 second children, 36,824 edges, 36,792 leaves, depth two | None |
| C09. Ordered subdivision words and one-/two-port probes | **PASS** | Article `:1135-1154` | All streaming/site/full primitive/full graph layers PASS; 15/15 focused mutations PASS | Recovered 176 anchors, 2,206 source and target sites, 29,964 one-port rows, 2,107 survivors, 544,571 two-port rows, 67,741 transports, 4,379 restrictions | None within the disclosed reference-closure independence boundary |
| C10. Ordinary-triangle rank-nine germ, contextual submersion/gluing, genericity mechanism | **PASS** | Article `:1204-1474` | Exact triangle and tree/sunlet witnesses; inherited full layers PASS | Independently recomputed exact 4x4 and 5x5 block determinants `-1/2` and `-1/4`; checked submersion rather than square inversion, exceptional-set properness, and real/complex dimension passage | None |
| C11. Global equivalence, exclusion of proper one-way containment, exact reconstruction | **PASS** | Article `:1332-1538`; current article is authority, promotion manuscript is companion only | Crosswalk C11, release guard, all 41 fresh full layers, and all 25 outer mutation gates PASS | Checked both global implications and exact semialgebraic final membership; all unresolved supports are retained through assembly | None |
| C12. Strict continuous-time cone transfer | **PASS** | Article `:1540-1588` | Domain/bridge bindings and inherited full classification PASS | Exact arithmetic checked `g>s^2>2s-1`, product roots, open/rank/separator transfer, and simultaneous bridge inequalities | None |
| C13. Weak-but-not-strong tree-child `4n-3` sharpness | **PASS** | Article `:1590-1799` | Primary and independent weak-sharpness layers PASS | Rebuilt both switch maps, common tensor, named zero-based 9x9 minors, rational CT witnesses, graph non-equivalence, cherry inverse, and induction | None |
| P01. Reader-facing exact hash binding | **FAIL** | Supplement `supplement.tex:752-757`, `:790-793`; PDF pp. 20-21 | Lock/crosswalk bind the actual artifact | Independent 23-row printed-hash parser fails exactly two rows for the same file | Correct two hashes and add semantic gate |
| P02. Outer JSON duplicate-name rejection contract | **FAIL** | Outer builder/checker code listed in Finding 2 | Ordinary `json.loads` accepts duplicate names | Same-valued duplicate `status` survives supported `--write` reseal and both checks | Strict decoder plus same/conflicting duplicate mutations |
| P03. Archive/ledger/tag/PDF byte integrity | **PASS** | Manifest, lock, five source files, two PDFs | All standard byte checks PASS | Independent strict parser, ZIP reconstruction, Git-blob comparison, two PDF rebuilds | None for current bytes; reseal needed after fixes |
| M01. Recent-source verification chronology | **FAIL** | Supplement `:896-944`; PDF p. 23 | Static audit checks keys/literals, not date feasibility | arXiv v3 postdates the claimed check; presentation only | Correct or scope the verification date in the already-required source reseal |
| L01. Load-bearing attributions and stated scope | **PASS** | Article introduction/citations; supplement `:896-950` | Not a computational claim | Primary-source checks support every load-bearing use; novelty search found no obvious prior duplicate theorem | Novelty search is not an exhaustive priority guarantee |

The hand-proof PASS covers the network class and admissible rootings; strong
versus weak tree-childness; fixed mixed graphs and restrictions; ordinary-
triangle transport; strict stochastic inequalities; reticulation-adjacent
root movement; quartet and whole-map signs; decorated blobs; the bridge fibre;
paired `(s,g)` products; semialgebraic localization; finite choices and no
remote compensation; cycle/theta event placements and no-omnian exclusions;
certificate semantics and the PC-PARTIAL boundary; contextual triangle
gluing; both directions of global equivalence; genericity; retain-all exact
reconstruction; continuous-time transfer; and the weak-class sharpness
induction. No abstract marginal relation was lifted to the full model, no
target deletion map was inverted, and no literal polynomial-body equality was
used as graph-orbit equivalence.

# 4. Numbered findings

## 4.1 Reproducibility-blocking: two stale printed hashes

The supplement identifies
`work/final_theorem_release/composite_reseal_diff_audit.json` but prints

`bc91fee3b7541fcae72c4db2e66776fbfc69c43890718239f0eea41bb2cc0654`

at `proof_compression_submission/supplement/supplement.tex:755` and again at
`:793`. The stale value is visible on supplement PDF pages 20 and 21. Direct
hashing gives

`96e30bae42939fa50dd585ba900bc5bd45e5eb122334de86c34654004212db4c`,

which agrees with `RELEASE_LOCK.json:528-531`, the theorem crosswalk JSON at
line 869, and the revised bundle manifest at line 754. Git history identifies
the printed value as the pre-repair file hash at commit `e9c68e2b...`; commit
`488e8f53...` changed the artifact without updating the prose anchors.

**Minimal reproducer.** Run
`independent_checks/provenance/check_printed_supplement_hashes.py` against a
fresh extraction. It checks 23 printed authority/anchor rows and exits 1 only
for these two representations. Tool SHA-256:
`d9fd06c302fa1d3e3d0fb233296adea009eaa3346e0edd87bbc148d7be3227c7`;
result SHA-256:
`3d5ec99f0b2de74518e67e0d53ee50821dc2d4aa4e8806c5a4291d7619492e02`;
result payload prefix `03bff60b...`; runtime 0.24 s.

**Severity/effect.** Reproducibility-blocking, theorem-neutral. The audit JSON
body remains internally coherent: 2,528 changed theta2 rows, 2,943,712
unchanged theta2 rows, zero raw4 changes, zero unresolved rows. Standard
source, PDF, lock, crosswalk, bundle, and full-replay checks all accept the
stale reader-facing assertion. The existing `false_supplement_pdf_hash`
mutation changes the manifest's PDF hash, not the artifact hash printed inside
the PDF.

**Smallest adequate remedy.** Replace both strings with `96e30...`; add a
strict printed-authority/hash comparison to the normal source/release gate;
rebuild supplement PDF/logs, PDF report, static source audit, crosswalk,
manifest, tag, and archive. Because the current telemetry policy binds all
five sources, run and bind a new clean full replay. The frozen lock need not
change unless its file set or bytes change.

## 4.2 Reproducibility-blocking: duplicate JSON names survive a valid reseal

`independent_checks/provenance/test_outer_fail_closed.py:115-135` inserts a
second top-level `"status": "PASS"` into
`proof_compression_submission/PDF_BUILD_REPORT.json`, then invokes the
submitted builder's supported `--write` mode so the altered bytes receive a
legitimate new outer seal. The subsequent builder `--check` and nominally
independent checker both exit 0/PASS. The mutant's combined root is
`5d2837ecde6030faef677c524b3ad9487d07f5371c2f895ee5a282d071f784a5`;
manifest payload is
`b7b64405ccc62117b5e68def4c0a6398d850586537aaa2149ebca018dc8596d2`.

The decisive cause is ordinary `json.loads` in
`build_revised_referee_bundle.py:91-95` and lock load line 104, and in
`check_revised_referee_bundle.py:108-114` and `:294-301`. Python retains the
last duplicate, so the nominally independent checker shares the producer's
permissive acceptance. In this same-valued attack, first-key and last-key
consumers both see `PASS`, while a strict consumer rejects the document. A
conflicting-valued duplicate could create divergent first/last semantics and
therefore remains a required additional mutation.

**Minimal reproducer.** Run the named independent script in a disposable
copy. It exits 0 after demonstrating the unwanted acceptance and restoring
all touched files byte-for-byte. Script SHA-256:
`d6f636dd6b3087d32512aacae4e3f1ec76e0547e96b702cd1cb6ee4bb1308756`;
result SHA-256:
`6fbc82361dbf0e3ffc274e8f730d1dd0e99082ec14661129b4b7aa173a49443d`;
runtime 3.71 s. The same script confirms that a source symlink, missing
bibliography, missing portable ledger, and syntax-invalid manifest are
rejected for their intended reasons.

**Severity/effect.** Fail-closed reproducibility blocker, theorem-neutral.
This is not evidence of current corruption: an independent strict inventory
parsed all 233 distributed JSON files and found zero duplicate name (exit 0,
0.62 s; tool SHA
`9b516256294f269e08cbd0746216a0574401eafac2011cf530c288a1316231c8`).

**Smallest adequate remedy.** Use a duplicate-name-rejecting
`object_pairs_hook` in both producer and checker, preferably in every
provenance reader. Add same-valued and conflicting-valued duplicate-name
mutations. Regenerate crosswalk/manifest, create a new tag, and rebuild the
archive. The code-only change does not intrinsically require theorem
recomputation, but the simultaneous supplement-source fix does under this
package's source-bound replay policy.

## 4.3 Resolved computational control; earlier failed-closed run retained

The first fresh outer 25-gate mutation invocation exited 1 after 718.33 s with
maximum RSS 2,545,827,840 B at the nested parameter-transport suite:

`PARAMETER_TRANSPORT_MUTATIONS_FAIL:unqualified production rejection:triangle_edge_false_product_map:1:None`.

It had already passed its output-contract preflight and rejected optimized
mode, quartet semantics, quartet terminal-binding, and canonicalizer attacks.
At the same time, a second process running the same submitted approximately
2.55 GB primitive builder was active. Both runs failed closed; neither created a
success report. An isolated instrumented execution of the first mutant later
reached the untouched production verifier and was rejected at the intended
semantic diagnostic
`PARAMETER_TRANSPORT_REPLAY_FAIL:rederived bytes:parameter_transport_certificate.json`.

This is not a theorem counterexample and not a false PASS. The concurrency is
an observed condition, not a proved cause: the wrapper omitted the child's
captured output, so the original unqualified rejection cannot be diagnosed
from that record. The isolated first-mutant control proves that the intended
semantic rejection path is live; it does not prove why the earlier child
stopped.

The controlling low-contention invocation subsequently exited 0 after
3,519.10 s with maximum RSS 2,635,235,328 B. All 25 aggregate outer mutation
gates passed, with zero survivors and no blockers. Its report SHA-256 is
`f2a362e9d2606b0315f9fe6e5a7659d328bd73bcf6552f0c1cc4c4f8ecdd0026`,
payload SHA-256 is
`05475591f00c75f2f0c2ee2e92c23bc869a8ed5000d28b40455ab7481870d30b`,
stdout SHA-256 is
`7dbb43e2428d3d6c74923d956c1c9741315893be328341b65a276979b14ce5e4`,
and timing/stderr SHA-256 is
`349f87ac666959d4f7bf7898f4200fdc0e707aecdd92fb54359e6a641710f0ab`.
All 489 submitted paths remained byte-identical to their pre-run hashes. The
earlier failure remains useful diagnostic evidence but is not a current
computational blocker.

## 4.4 Presentation/attribution: impossible citation-check chronology

Supplement `supplement.tex:896-899` says citation metadata were checked on
21 August 2026. The same table at `:940-944`, and
`article/references.bib:180-190`, cite Brits et al. arXiv v3 and say it is
dated 25 August 2026. The contradiction is printed on supplement PDF page 23.
The [versioned arXiv record](https://arxiv.org/abs/2607.12919v3) confirms the
25 August timestamp. This is presentation/attribution only; the cited theorem
still supports the paper's use. Change the lead date to “checked through 25
August 2026” or split the original check and later update, then include the
change in the already-required source/PDF reseal.

## 4.5 Presentation/currentness: companion v1.1.4 DOI wording

`references.bib:167-177` and supplement `:945-948` accurately cite the exact
[v1.1.4 GitHub release](https://github.com/AlecKriebel/Math/releases/tag/stc-jc-sharp-boundary-v1.1.4),
whose own release text claimed no DOI. But DOI-bearing v1.1.7 records existed
before this K2P package was built: preprint
[10.5281/zenodo.22089373](https://doi.org/10.5281/zenodo.22089373) and data
[10.5281/zenodo.22064121](https://doi.org/10.5281/zenodo.22064121). The exact
old citation is not false, but an unqualified “no DOI is claimed” in a recent-
source note is stale. Either cite v1.1.7 or state explicitly that the sentence
describes only cited v1.1.4. No mathematical result changes.

## 4.6 Human release wording: “immutable source tag” is too strong

Article `main.tex:1822-1832`, supplement `:963-968`, submission README
`:84-88`, crosswalk Markdown `:58-64`, and manifest `:1663-1674` call the
source tag immutable. The tag exists as annotated object
`ae537c7e2dacdc1026b30b65fe04daca57b4fd84`, peeling to commit
`cb7559e0ba5fd72f94bce5941208be0838be878d`, but `git verify-tag` reports no
signature. The content-addressed object is stable; the ordinary repository ref
can be moved or deleted. Use “versioned annotated source tag” and print the
peeled commit. This is low severity and does not weaken current byte identity.

## 4.7 Nonblocking provenance-log completeness

`proof_compression_submission/crosswalk/RESEARCH_LOG.md:38-63` ends at the
24 August v1.0.0 checkpoint and does not record final v1.0.2 closure. Current
manifest, README, crosswalk, PDFs, and tag consistently say v1.0.2, so the log
is historical rather than a competing authority. An optional final entry
would improve traceability; no theorem artifact must change solely for this.

## 4.8 No theorem-fatal or proof-blocking defect found

The revised reconstruction retains every unresolved support through global
assembly and decides exact semialgebraic membership for every triangle class.
The current C11 crosswalk labels the article/PDF as theorem authority and the
promotion manuscript only as a machine-bound companion. The rank crosswalk
now names the production symbolic verifier, `syzygy_upper.py`, exact replay,
and a production-verifier mutation that rejects sampled evidence. Parameter-
transport semantics now bind full graph switching signatures, paired K2P
sectors, tensor-invisible inheritance parameters, and complements only under
certified parent reversal. These changes resolve the prior proof/crosswalk
findings. I found no invalid square inverse, hidden rooted oracle, remote
compensation, illicit inheritance quotient, or claim beyond the explicitly
bounded scope.

## 4.9 Nonblocking QA: unexpected parameter-child failures are opaque

At
`work/canonicalizer_completeness/inheritance_transport/run_parameter_transport_mutations.py:457`,
the unqualified-rejection branch reports only the mutant name, return code,
and parsed semantic marker. It omits a bounded sanitized tail of the child
output that the wrapper has already captured. Under the concurrent heavy run
this became `...triangle_edge_false_product_map:1:None`, obscuring whether the
primitive child had encountered resource pressure or another unexpected
failure. The branch remains fail-closed and cannot produce PASS, so this is
not a theorem or completeness defect. A useful optional repair is to include a
bounded sanitized child-output tail and explicit failure class while retaining
the strict no-PASS contract. Because the runner is hash-bound, changing it
would require refreshing its mutation report and downstream bindings.

# 5. Execution ledger

## Environment and authoritative input

- macOS 26.5.2 build 25F84; Darwin 25.5.0 arm64.
- Apple M1 Pro, 10 cores; 17,179,869,184 bytes physical memory.
- Python 3.14.6; NetworkX 3.5; SymPy 1.14.0; Tectonic 0.16.9;
  Poppler 26.08.0.
- Source ZIP: 214,930,375 bytes; SHA-256
  `86a286be82ce3c211f556eaa24cf1120aa42e41f716b46cb8752c1d2546053ba`.
- ZIP inventory: 489 files, 483,608,160 uncompressed bytes, 214,789,263
  compressed payload bytes; no duplicate, symlink, directory member, path
  escape, or comment.
- Article PDF: 26 pages, 194,327 bytes, SHA-256
  `2bca627d072cf96c850a7196be9101a7e061499bbcc61ebbb8ff256d4bf864b9`.
- Supplement PDF: 24 pages, 160,133 bytes, SHA-256
  `4bdcfe32cf3dbcd586d9bf68f3d287e4f5f58aa3384aa5daaf454fde3e361621`.

The five source SHA-256 values are `main.tex` `d64574e3...e75c3`,
`references.bib` `d1b3b50f...de6b`, `supplement.tex`
`7b28e0ff...8bc4`, `compression_tables.tex` `22ff0534...e81`, and
`certificate_appendix.tex` `936e8d18...794d`.

## Exact source/release consistency matrix

| Artifact | SHA-256 | Consistency result |
|---|---|---|
| `article/main.tex` | `d64574e30ef3dac38c91613938a6ce29f7b07688ea791013c56a45e9af0e75c3` | tag, PDF report, outer manifest, and replay telemetry agree |
| `article/references.bib` | `d1b3b50f6e276cc147471dcab9f30ed3a9b629fddc19ffb7fea58d427ee5de6b` | same; physical omission is rejected |
| `supplement/supplement.tex` | `7b28e0ff620b24256f4eebe61fc233dc21df8ffd7b4b552b51eb579712358bc4` | same; contains P01's false *printed* artifact hash despite byte agreement |
| `supplement/compression_tables.tex` | `22ff0534b79cf226c9041703ab9d87ab123914bbb55ec1d44c84041a8616be81` | same; omission fails at source line 319 |
| `supplement/certificate_appendix.tex` | `936e8d1879acd224affb053489a618dcfe8d7a7a2a5500bc8f0f85dd1b16794d` | same; omission fails at source line 453 |
| article PDF | `2bca627d072cf96c850a7196be9101a7e061499bbcc61ebbb8ff256d4bf864b9` | two clean rebuilds are byte-identical |
| supplement PDF | `4bdcfe32cf3dbcd586d9bf68f3d287e4f5f58aa3384aa5daaf454fde3e361621` | two clean rebuilds are byte-identical; renders P01 on pp. 20-21 |
| `PDF_BUILD_REPORT.json` | `6521cdc5ad43288ec928db747d19ab6e944ef0182cd726da021693ed582c6349` | five-source/PDF/log bindings agree |
| `STATIC_AUDIT_RESULT.json` | `59f401307c0cce25ff2d7570789fd89da78e5d642814d870589b965549a272a5` | PASS, but does not compare hashes printed inside TeX/PDF |
| `RELEASE_LOCK.json` | `130642e235c9beaa22061c578c3c645244cdbf45a9b416d45d94492b3d2848bd` | 230 locked files; payload `b5eb26e953fbb76de671a4caa0db3068932af1e23b4fffdb0d118b5939f81756` |
| portable content ledger | `eef2202e6f3ec18f54835230f0d994a17693e1204ca4d5ae64c7a8d58e17b9e8` | 406-file closure and crosswalk source agree |
| theorem crosswalk Markdown | `23b4fd6819aa40da9749327efeded8ff65c3da87c73b034fcc36b609b7c75d6c` | 13 current claims bound |
| theorem crosswalk JSON | `dbdd8fac081cbb523a3eb296f05c10c2166f56acbf128170b2ac51da5991bed8` | hashes/roles resolve; it binds P01's actual artifact bytes, not the stale printed value |
| revised/source manifest | `c65d4c7ce4d094f7d1e85ecfea2604c5948c345c11f9fb726505301d898f5fc2` | 488 nonmanifest files and combined root agree |
| stored clean full replay | `2489643d65c50f662d027bf5002b9f398c8fa2999d7a17fcf43a5334cb04e86e` | provenance-only stored PASS; not substituted for fresh execution |
| stored clean telemetry | `b0f379d5e9d7e3acfd4c9812711964c4f7894dfd15e28045eab8077a9e6bd18f` | commit/source/report/lock bindings agree; provenance only |
| fresh quick report | `309d2b341a9ab8626ab1982000b43d0d015824885f9887d98f8323277c5a29aa` | 23/23 PASS |
| fresh full report | `d5e6642eda6c4fa721cdde8a7cb9cf5da240b3784d27f6d99b1084c48ed79cab` | controlling single invocation; 41/41 PASS, 6,082.872989 s internal |

The detailed command table with full 64-hex stream/report hashes, working
directories, per-layer entries, and unavailable fields explicitly marked is
`EXECUTION_LEDGER.md`. The full submitted C01-C13 artifact/producer/verifier
map is `EVIDENCE_REGISTRY.md`; its claim-focused location/evidence summary is
`CLAIM_EVIDENCE_REGISTRY.md`. The independent 489-row path/size/hash inventory
is preserved as `evidence/provenance/final_archive_member_ledger.tsv`
(SHA-256 `d6584f46587e1c2c29f40e924edd28579b2a29acfb7a3b0b878bca0d8850a36c`);
its summary/root audit is `evidence/provenance/independent_bundle_audit.json`.
The complete submitted 406-row portable ledger is the content ledger named
above.

## Commands and results

Full stdout/stderr files are under `logs/`; machine-readable per-layer hashes
are in the replay reports. Peak RSS is shown where measured. Empty-output SHA
is the standard SHA-256 `e3b0c442...b855`.

| Command or check | Exit; wall time; peak RSS | Result; output/report SHA-256 | Evidence type |
|---|---|---|---|
| `unzip -t <source.zip>` | 0; 2.70 s | PASS; stdout `dcb909a5...2476`, timing/stderr `3a517883...194` | provenance |
| final fresh extraction versus independent 489-row ledger | 0; 0.32 s; 274,989,056 B | 489/489 paths and 483,608,160/483,608,160 bytes exact; zero mismatches, symlinks, extras, `pyc`, or `__pycache__`; stdout `fc54f242...9cdf`, stderr/time `bb937dce...d2e5` | independent provenance |
| fresh venv creation | 0; 1.93 s; 97,288,192 B | PASS; stdout empty, stderr/timing `5c025f9b...185` | reproducibility |
| pip upgrade | 0; 1.20 s; 96,534,528 B | PASS; stdout `71870656...1c7`, stderr `b426e12a...81a0` | environment |
| locked requirements install | 0; 6.31 s; 179,273,728 B | PASS; stdout `b8cb8888...f7e8`, stderr `3044fa57...4e8d` | environment |
| `output/referee/build_referee_bundle.py --check-only` | 0; 0.46 s; 231,636,992 B | 406 files/479,324,605 B; stdout `468aedd2...cef` | provenance |
| `build_release_lock.py --check --require-ready` | 0; 9.93 s; 516,947,968 B | PASS; stdout `20b3a276...244c` | provenance/computational |
| release-lock rebuild in disposable copy | 0; 9.89 s; 518,209,536 B | byte-exact; stdout `771f5cd4...83f` | provenance |
| `verify_final_theorem_release.py --quick --output ...` | 0; 286.48 s; 1,463,189,504 B | 23/23 PASS; report `309d2b34...9aa`, stdout `a8b55d93...0a3e`, stderr `e4bd6c1f...7b5b9` | computational |
| fresh `verify_final_theorem_release.py --full --timeout-seconds 7200 --output ...` | 0; 6,083.36 s; 2,544,648,192 B | 41/41 PASS; report `d5e6642e...79cab`, stdout `51da276e...389f`, stderr/time `50bb7ef5...17c6`; internal 6,082.872989 s | computational |
| first `run_release_mutations.py` under competing heavy builder | 1; 718.33 s; 2,545,827,840 B | failed closed at unqualified nested parameter-transport rejection; stdout `befaf0d5...34d`, stderr/timing `96997dca...166` | computational; not a qualified suite completion |
| low-contention controlling `run_release_mutations.py` | 0; 3,519.10 s; 2,635,235,328 B | 25/25 aggregate mutation gates PASS, zero survivors/blockers; report `f2a362e9...0026`, payload `05475591...d30b`, stdout `7dbb43e2...5e4`, stderr/time `349f87ac...f0ab` | computational |
| post-control submitted-path fingerprint | 0; wall/RSS not measured | all 489 pre-run submitted SHA-256 values exact; check output `f58c22d4...1cc2` | provenance/source immutability |
| `run_corrected_universe_mutations.py --output ...` | 0; 218.10 s; 461,307,904 B | 22/22 rejected, zero survivors; report `596bb5a4...c89c8`, payload `a67ce800...f0cb`, stdout `14ad6897...a15` | computational |
| canonicalizer mutations in an independent disposable copy | 0; 0.52 s; 50,626,560 B | 2/2 intended rejections; report `48c35a2c...b158`, payload `6a86dd65...7a73c` | computational |
| missing-`networkx` plus stale-PASS canonicalizer attack | 0 expected catcher; <1 s | child exits 1 with `ModuleNotFoundError`; no output and no PASS | independent fail-closed attack |
| restoration mutations in an independent disposable copy | 0; 586.20 s; 574,898,176 B | 13/13 intended rejections; report `3fc427a4...b9b4`, payload `9f31f968...c909` | computational |
| probe mutations in an independent disposable copy | 0; 195.28 s; 69,386,240 B | 15/15 intended rejections; report `eec59bb4...5dd7`, payload `14f0364d...6e74` | computational |
| parameter-transport suite under a second simultaneous 2.55 GB builder | 1; 515.92 s; 2,548,809,728 B | failed closed at first mutant, no report | computational diagnostic; not suite PASS |
| isolated full first parameter mutant against untouched production verifier | production child 1 expected; 360.45 s; 2,546,106,368 B | intended `PARAMETER_TRANSPORT_REPLAY_FAIL:rederived bytes:parameter_transport_certificate.json`; result `ce0684e2...f63` | independent production-verifier attack |
| direct sampled-rank semantic attack | 0 expected catcher; 0.45 s | intended `RANK_UPPER_SYMBOLIC_FIELD_DIMENSION_FAIL:orbit=0:observed=4:required=6` | independent exact attack |
| static source audit | 0; 0.19 s; 42,434,560 B | PASS; stdout `59f40130...72a5` | provenance/presentation |
| theorem-crosswalk producer `--check` | 0; 0.41 s; 170,786,816 B | 13 claims PASS; stdout `298114b7...2b32` | provenance |
| revised outer builder `--check` | 0; 0.81 s; 229,539,840 B | PASS; stdout `b52b015e...db0b` | provenance |
| revised independent outer checker | 0; 0.69 s; 292,454,400 B | PASS; same stdout hash | provenance |
| compressed-release check | 0; 0.08 s | PASS; stdout `470286fe...23e9` | computational |
| old/new seven-command equivalence | 0; 78.69 s; 294,551,552 B | PASS; stdout `900d6404...007a` | computational |
| compression mutations | 0; 0.42 s | 11/11 PASS; stdout `c222d943...f84` | computational |
| crosswalk/bundle mutations | 0; 11.79 s; 505,249,792 B | 31/31 PASS; stdout `bd92ab65...fd29` | computational/provenance |
| clean full-telemetry tests | 0; 7.65 s | 12 tests PASS; stdout empty | reproducibility |
| final replay output-contract attacks | 0; 0.37 s | PASS; stdout `4988dbe9...4af` | fail-closed computational |
| two PDF rebuilds from exactly five sources | 0; 26.94 s | byte-identical PASS; stdout `6617d0c7...4f0`, report payload `d3b3095f...adaf` | reproducibility |
| omit `compression_tables.tex` | 1 expected; 3.69 s | intended missing-input failure; log `b5438bba...87d5` | mutation |
| omit `certificate_appendix.tex` | 1 expected; 3.19 s | intended missing-input failure; log `d01a43d7...52f` | mutation |
| omit `references.bib` from physical source set | 1 expected | `required submission source missing` | mutation |
| independent bundle/ledger audit | 0; 2.22 s | exact-set PASS; result `39a46ef3...eda2e` | independent provenance |
| strict JSON inventory | 0; 0.62 s | 233 current JSONs, zero duplicate; stdout `1de65445...aa93` | independent provenance |
| Git/tag/telemetry blob audit | 0; 19.85 s | 489/489 tag and 411/411 telemetry bytes match; result `edef1544...5332` | independent provenance |
| independent printed-hash audit | 1 intended; 0.24 s | exactly two stale rows; result `3d5ec99f...2e02` | independent falsification |
| independent duplicate-key/fail-closed attack | 0; 3.71 s | demonstrates unwanted acceptance; result `6fbc8236...943d` | independent falsification |
| independent census audit | 0; 54.74 s; 274,153,472 B | PASS; result `602924d7...51e0`, payload `0a607958...dd88` | independent computational |
| exact rational K2P boundary/product audit | 0 | PASS; result `39e2101d...3b25`, payload `9565a7c8...ae47` | independent mathematical/computational |
| independent symbolic spot checks | 0 | PASS; result `60594dc6...8286` | independent mathematical/computational |

The quick report records all 23 layer names, elapsed times, return codes, and
stdout/stderr hashes. It covers the promotion guard, fail-closed domain reseal,
corrected-universe replay, no-assert gate, domain/rooting, quartet semantics,
terminal bindings, raw directions, structural canonicalizer and parameter
transport, bridge/gluing, analytic and global-scale audits, raw4/theta2
overlays, raw provenance, 36 direct classes, cycle promotion, probe replay and
partition, and both weak-sharpness implementations.

The attached ZIP was rebuilt three times in clean locations. Each rebuild was
214,930,375 bytes and had the identical source SHA-256 `86a286...53ba`;
rebuild times were 20.65 s, about 21 s, and 20.92 s. Independently recomputed
roots are:

- frozen transitive closure: 406 files, 479,324,605 bytes,
  `d4385855fd9d8387080a8e789613114f047fd93aaad9a78e86924d1a29b25c3e`;
- submission partition: 82 files, 4,184,639 bytes,
  `72b8df4f4d2c015d219f48960b0cba5e64e6aa0b5d9d34fa4f9b5f4a5950d45e`;
- combined set excluding manifest: 488 files, 483,509,244 bytes,
  `a3aff0653f5593c3320e6c13c2e06d0e7a3896129123eb48f043c56aa93f3b16`.

The release-lock file is
`130642e235c9beaa22061c578c3c645244cdbf45a9b416d45d94492b3d2848bd`
with payload `b5eb26e9...1756`; portable ledger is
`eef2202e6f3ec18f54835230f0d994a17693e1204ca4d5ae64c7a8d58e17b9e8`.
All 489 packaged files match annotated source tag object `ae537...` / peeled
commit `cb7559...`, and all 406 frozen files plus five source files match
telemetry commit `f6befbce...`.

## Historical five-dependency reconciliation

The superseded 23 August `SUBMISSION_BINDING.json` named five supplemental
execution dependencies. The current interface replaces it with
`RELEASE_LOCK.json`, the portable ledger, and the current crosswalk, but I
audited the historical paths rather than treating their removal as proof of
irrelevance:

| Historical path | 23 August bound SHA-256 | Current source commit and current-package disposition |
|---|---|---|
| `output/referee/REFEREE_BUNDLE_CONTENTS.json` | `5799d8f3127a3d1e43f28610a3753a3da2a2a0de5c021ce45efc5665058d24bd` | Current ledger `eef2202e6f3ec18f54835230f0d994a17693e1204ca4d5ae64c7a8d58e17b9e8`, content commit `f6befbce38cfb21e27b8dc4a9611d284fdcbc800`; present and required by the current crosswalk producer |
| `work/four_port_direct_residual_closure_certificate.json` | `fb6e5f1c23c8c3291ddc8c822171cae9c2df05b0d449249813b40e958e17bddc` | Last source-content commit `2474e2b86ce1d3c78e58ce0ae981547c03e6b427`; legacy top-level path absent; current inner authority `9dc3f112d0b4ed8883160b5c53111cd5208f911546cbb63d1b99a76d7f53f861` |
| `work/theta0_quintic_orbit_certificate.json` | `f863afd5875a74be818141990863344fae09fd4269a803d3a1bfeb67a8a595e0` | Last source-content commit `2474e2b86ce1d3c78e58ce0ae981547c03e6b427`; current inner copy remains byte-identical at `f863afd5875a74be818141990863344fae09fd4269a803d3a1bfeb67a8a595e0` |
| `work/theta3_cubic_obstruction_certificate.json` | `fb1512e260b5a88b5ac3a4b55d6c756e401baebd08866d6e39bb2153b63aa4d8` | Last source-content commit `2474e2b86ce1d3c78e58ce0ae981547c03e6b427`; revised inner authority `d1501a7e86b6b2b614590454ba4a44afc04785cb19711b70d2cd8069bd35e0bf` |
| `work/theta_quartic_obstruction_certificates.json` | `5204593fb2b47914dbdf2d7846d1e9fbd5671fa9f29e89862d29b16a45bb08db` | Last source-content commit `2474e2b86ce1d3c78e58ce0ae981547c03e6b427`; revised inner authority `1127004383145ae1fa053a86e43199e3f627fefe8cd978feefc80b9b89e7b696` |

The older inner seal at checkout commit
`078b573d214ff598868d1b5dbf9565ef267bb257` contained exactly two
byte-identical historical copies, theta0 and theta3. In the revised current
seal theta3 changed, so only theta0 remains byte-identical to its old outer
string. This is explicit version evolution, not a missing current dependency.

The dedicated fresh computational code-audit report has SHA-256
`21e11e46f0765fa63516e127ef724548c401a7e3d2c57765bc1ff367ca0a7f60`.
It records exact source hashes for the production canonicalizer,
parameter-transport, symbolic-rank, restoration, probe, and release-harness
paths and the bounded independence of each fresh attack.

The absent legacy commands were invoked only to establish absence and exited
as expected: `verify_handoff.py` and `test_handoff_mutations.py` exit 2;
`setup_environment.sh` exits 127; both `run_all_verifiers.py` invocations exit
2. Their stderr hashes are respectively `5b447137...bd07`,
`fca5bff9...35bf`, `e8ba0451...c7b2`, `f9178d10...8f89`, and
`eb665b2d...93c1`. No PASS was inferred from these missing names; their current
semantic mappings are listed in Section 2.

# 6. Independent attacks and mutations

## Primitive finite universe and exact censuses

`independent_checks/computation/fresh_census_audit.py` (SHA-256
`933e2dac57fd09a409288576a5473ab5d7c54070fc8c82567793f3a099a0a163`)
imports no submission module. It independently decodes the arithmetic dense
raw-ID and completion-word grammar, source/target/permutation domains, stored
parents and references, and row-contract closure. It does not infer the
analytic category of every row from primitive graph semantics. It checks:

- raw4: 405,216 = 360,408 quartet + 16,974 whole-map sign + 23,822 rank
  + 1,472 direct-terminal + 2,540 restoration-member records;
- the 1,472 raw direct-terminal rows and their 934 terminal classes: 839
  quadratic, 36 higher degree, four hard bindings, 20 isomorphisms, and 35
  triangles; higher degree = 22 quintic + 12 quartic + two cubic;
- theta2: 2,946,240 = 2,942,592 quartet + 2,528 sign + 800 rank + 240
  quadratic + 80 isomorphism; dummy forest 56 roots, 864 descendants, 832
  leaves, and 32 continuations;
- cycle base: 13,440 = 5,964 restoration + 7,452 sign + eight isomorphism +
  16 triangle; cycle completions: 536,364 = 535,920 quartet + 132 quadratic
  + 300 sign + 12 isomorphism;
- restoration arithmetic/reference closure: the reviewer-owned audit recovered
  997 parents, 2,540 roots, 36,568 first children, 256 second children, 36,824
  edges, 36,792 separator-terminal leaves, depth two, and 32 first-level
  continuations; the submitted full restoration replay separately confirmed
  zero missing, duplicate, cyclic, or unresolved semantic obligations;
- probes: 176 anchors; all 2,206 source and target sites; 29,964 one-port rows;
  2,107 equality survivors; 544,571 two-port rows; 32,729 two-port equalities;
  67,741 exact transports; 4,379 parent restrictions.

It also re-derives `C(3,1)=289`, `C(3,0)=C(4,1)=831`,
`C(4,0)=C(5,1)=1983`, and `C(5,0)=4155`. Independence is deliberately
bounded: the completion grammar, IDs, and stored parent/reference contracts
are independently regenerated; analytic category labels are counted from the
submitted ledgers rather than independently reclassified by a second global
orbit engine.

## Exact physical and symbolic attacks

The exact rational domain audit checks every strict inequality without using
floating-point sampling. It verifies strict stochasticity iff `D_plus`, the
continuous-time implication `g-s^2>0` and
`s^2-(2s-1)=(1-s)^2>0`, boundary-near rational families, and all 10,404
products of the 102 selected `D_plus` grid points.

The independent symbolic spot-check program imports no submitted code or
artifact. It reconstructs representative quartet pullbacks, the exact whole-
map `T_i` factor, all completion counts, triangle output coordinates and rank
nine, block determinants `-1/2` and `-1/4`, both weak-sharpness common tensors
and rank-nine Jacobians, and the cherry determinant. These are genuinely
separate derivations for representatives, not a second exhaustive symbolic
engine for every higher-degree certificate.

## Graph, restoration, and probe attacks

The review-owned finite-contract decoder directly inverts the arithmetic raw
IDs from source/target/permutation indices, checks role and reference closure,
follows every stored restoration parent through two levels, and confirms that
every stored probe parent/transport reference exists with the expected row
role. It is not a separate graph-semantic classifier and does not reconstruct
transport maps from primitive graph incidences. Separately implemented
submitted replayers exercise primitive graph generation, canonicalizer
completeness, physical direction/port/parent order, restoration forests, and
graph-derived transport semantics; those programs were source-audited and
mutated, but remain package-supplied implementations. Literal polynomial
equality is never substituted for graph-orbit equivalence.

## Mutation mechanisms

The 22-case corrected-universe suite passed from a caller-owned output path.
It rejects omitted raw rows, false rank exclusions, missing children, wrong
parents, broken transports, reassigned quadratic/cubic/quartic/quintic
certificates, a revived raw4424 tree/sunlet oracle, rooted-restriction
reintroduction, source-tree writes, omitted probe rows/parents, wrong probe
parents, broken probe transports/restrictions, reassigned probe `T_i`, reversed
probe order, invented global triangle consistency, and optimized mode. Every
mutation exits 1 with the intended diagnostic, no signal/timeout/traceback,
and no success artifact.

The 31-case crosswalk suite and 11-case compression suite pass, including
omissions, role/relation changes, stale bindings, and optimized mode. Output-
contract attacks cover authoritative paths, stale PASS removal, hardlinks,
symlinks, and late symlink swaps. PDF omission attacks fail at the precise
generated-input lines. The independent provenance attacks add two mechanisms
the submitted suites miss: comparison of hashes printed inside the supplement,
and duplicate-name JSON after a legitimate reseal.

Three nested children created reviewer-side `pyc` files in the disposable
execution copy despite the outer `-B` flag. They were not submitted paths and
were not counted as source-byte changes. They were left visible in the
execution inventory rather than silently removed. The final fresh archive
extraction contains zero `pyc` files or `__pycache__` directories, and all 489
submitted paths match both their pre-run hashes and the independent archive
ledger.

The parameter-transport v2 report distinguishes four complete, coherently
resealed production-verifier mutations from six exact local semantic-
validator attacks; it does not mislabel all ten as end-to-end. An isolated
first-mutant control confirms the untouched production verifier rejects a
false triangle-edge product map at the intended rederived-certificate
diagnostic. The subsequent clean outer control passed all 25 gates as recorded
in Section 5.

# 7. Scope and literature audit

## What is proved

The submission claims, and the checked proof establishes conditional on its
finite exact classification, for binary standard semi-directed strongly tree-
child level-2 networks on the same labelled leaf set, strict inheritance
probabilities, and every K2P edge in

`D_plus = {(s,g): 0<s<1, 0<g<1, g>2s-1}`:

- equivalence of directed containment, structural equivalence modulo
  coherently transported ordinary-triangle redirection, and sharing a full-
  dimensional physical regular analytic germ;
- generic topology identifiability modulo ordinary triangles;
- a terminating exact-input reconstruction procedure returning the triangle
  class;
- the same classification on the strict continuous-time cone
  `0<s<1, s^2<g<1`;
- a `4n-3`-dimensional weak-but-not-strong tree-child sharpness family.

The finite theorem is computer-assisted. Its mathematical universe is the
primitive theta/cycle completion grammar; predicates are exact quartet,
whole-map sign, symbolic rank, polynomial-separator, isomorphism, triangle,
and fixed-full restoration/probe relations; certificates bind exact graph
roles, directions, parents, ports, polynomial pullbacks, physical witnesses,
and transports; exhaustion is by dense raw-ID generation before
canonicalization; replay is provided by separately implemented primitive,
graph-relation, symbolic, restoration, and probe checks. “Independent replay”
means separately implemented code, not independent human proof, and the
supplement now says so.

## What is not proved

No mixed-sign, stochastic-boundary, singular-edge, higher-level,
weak-class-identifiability, individual-parameter identifiability, numerical-
stability, bit-complexity, or finite-sample inference theorem is claimed. The proof does not claim an atlas-free
second all-family orbit partition or a second symbolic engine for every
higher-degree polynomial. It does not identify a unique orientation inside an
ordinary-triangle class. Nothing in this report extends those boundaries.

## Literature and attribution

Primary-source checks support every load-bearing attribution. In particular:

- [Brits et al. arXiv v3](https://arxiv.org/abs/2607.12919v3), Theorem 4.9,
  supports the level-1 JC/K2P/K3P result used here; its operative arbitrary-
  level result is JC-only, and the submission does not rely on a broader K2P
  statement.
- [Huber et al.](https://link.springer.com/article/10.1007/s11538-025-01510-5),
  Figure 8 and Lemma 4.2, support the two semi-directed level-2 generators.
- The cited [Englander et al. bioRxiv record](https://doi.org/10.1101/2025.04.18.649493)
  and archived v4 text support the K2P quartet signs, distinct displayed-
  quartet result, and blob-tree recovery.
- The cited semialgebraic projection and dimension results in
  [Bochnak--Coste--Roy](https://link.springer.com/book/10.1007/978-3-662-03718-8)
  match the numbered uses.

All 13 DOI-bearing bibliography entries match current publisher/Crossref
metadata; the three versioned non-DOI records resolve. The complete primary-
source table and exact identifiers are in `notes/literature_release_audit.md`
(SHA-256 `6d7675cde6c320e5981c292d3ce44e84095c49862e413afaa4a77cd60d6f3aa7`). Targeted searches did
not find another public primary source stating the same complete K2P strong-
tree-child level-2 principal-domain classification. That is search evidence,
not an exhaustive novelty or priority guarantee.

## Release and human metadata

At audit time every one of the 489 ZIP members was byte-identical to a path in
the [public source tag's project subtree](https://github.com/AlecKriebel/Math/tree/k2p-same-biorxiv-v1.0.2/k2p_level2_identifiability_closure).
The exact K2P tag exists, and no K2P
GitHub Release, Zenodo deposit, or DOI was found or claimed for this version.
Author/ORCID, corresponding email, sole-author contribution, funding,
competing-interest, licenses, and generative-AI disclosure are mutually
consistent. Email, funding, contribution, and conflict statements are author
declarations; they cannot be independently certified by a referee, and no
contact was attempted.

# 8. Required actions

## Mathematical and code actions

1. **Correct both false supplement hashes.** Replace the values at
   `supplement.tex:755` and `:793` with
   `96e30bae42939fa50dd585ba900bc5bd45e5eb122334de86c34654004212db4c`.
2. **Add a printed-hash semantic gate.** Parse every printed authority/anchor
   row and compare its named file's raw SHA-256, so a coherently sealed but
   false reader-facing hash cannot pass.
3. **Make JSON parsing duplicate-name-strict.** Apply the same strict decoder
   to both outer producer and checker, preferably all provenance readers; add
   same-valued and conflicting-valued duplicate-key mutations.

## Human editorial choices before reseal

4. Correct the citation-verification chronology on supplement page 23.
5. Either update the companion JC citation to v1.1.7 and its two DOIs, or
   explicitly scope “no DOI” to the cited v1.1.4 release.
6. Replace “immutable source tag” with “versioned annotated source tag” and
   print the exact peeled commit of the corrected tag. The current v1.0.2 fact
   `cb7559e0ba5fd72f94bce5941208be0838be878d` belongs only to the audit record.

## Package validation and human release

7. **Rebuild and reseal once, after Actions 1--6.** Rebuild the PDFs/logs, PDF
   report, static audit, and five-source archive; run clean source-bound full
   replay/telemetry on those exact revised sources and lock; regenerate the
   theorem crosswalk and revised manifest; run the already-edited strict
   checkers and independent file-set/byte, strict-JSON, printed-hash, omission,
   and Git checks; and build the deterministic ZIP twice with matching
   candidate hashes. The frozen release lock may stay unchanged only if all
   406 files in its closure and their bytes remain unchanged.
8. Publish the corrected package under a new tag/version rather than moving
   public v1.0.2; update sidecar hashes. Whether to create a GitHub Release,
   DOI, or repository-protection rule remains an author choice, not a theorem
   condition.

No mathematical theorem revision is required by the evidence in this review.
The completed 41-layer replay and 25-gate control, including the earlier
failed-closed diagnostic run, are preserved in the execution ledger.

No outreach, email, funding, contribution, conflict, licensing, DOI, or
submission action was performed by the referee. Those remain exclusively for
the human author.
