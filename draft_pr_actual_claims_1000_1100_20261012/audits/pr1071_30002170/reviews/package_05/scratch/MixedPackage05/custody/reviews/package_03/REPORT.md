# PR1071 — NEW complete whole-package adversarial review 03

Completed 16 October 2026 UTC. Literal candidate: `NEWpreprint_v1_0`.
Submitted head: `fc37aa5169a0fe6adae0a254c9ee6c1531a2911f`.
This is a fresh complete review of the current mathematical paper, its essential
primary-source interfaces, all operative support code, reproducibility, PDF,
metadata/citation/rights, current workflow claims and full historical custody.
It is not the bounded CASE-1071 repair review, a human referee report, a formal
proof certificate, a novelty clearance, or permission to publish.

**One actionable P3 support finding remains; no P0, P1 or P2 finding.**
The mathematical theorem survives independent reconstruction and adversarial
checks within its exact stated scope. The physical case-alias repair survives
the actual tests. The advertised Python compatibility does not: the documented
checker fails on installed Python 3.11.8. No candidate repair was made.
Delegated complete-review execution is **100%**; publication readiness and
issues-resolved remain false, publication remains held after PR1032, and a
bounded repair followed by a NEW complete whole04 is required.

## Finding WHOLE03-P3-01 — promised Python 3.9+ checker replay fails on 3.11

Locations: current `README.md:11` and `scripts/check.py:18` (call at line44).
The README says Python3.9+ standard library is sufficient for integrity,
archive building and finite-checker replay, and supplies ordinary and `-O`
checker commands. On a clean extraction of the exact reviewed ZIP, both
documented wrapper commands executed with installed **Python3.11.8** exit1
at the full-result equality guard:

`RuntimeError: Original checker mathematics differs from frozen original result.`

`PYTHON311_PORTABILITY.json` retains exact argv, cwd, version, return codes,
full stdout/stderr and every differing field. `PYTHON311_RESULT_NORMAL.json`
and `PYTHON311_RESULT_OPTIMIZED.json` preserve actual computed results. The
unchanged original program itself returns0 with its assertions active under
normal3.11; a separate byte-exact original `-O` run also returns0 and has the
same result as3.11 normal, ignoring utc only. Both wrapper invocations fail
during their first normal subpass, before reaching the optimized subpass.
The original's assertions are disabled in its separate optimized execution;
that fact is not presented as independent optimized mathematical validation.

There are **26 non-utc differences**, all floats in the covariance cross-check
list. For example, at H=.251,m=7, the frozen direct value is
`0.28537809429370337` and3.11 gives `0.2853780942937034`; the corresponding
direct-minus-grouped field changes from0 to `5.551115123125783e-17`.
The largest absolute difference is `2.220446049250313e-16`. Every exact-rational
field, normalization identity and sampled constant field agrees. This is a
reproducibility contract defect, not a counterexample to the analytic theorem
or evidence that the finite covariance identity is false. It is consistent
with the documented change to float summation in Python3.12.
[Official Python3.12 change record](https://docs.python.org/3.12/whatsnew/3.12.html).

Required repair: state and validate the actual runtime requirements for exact
baseline replay, or implement an explicitly justified cross-version validation
contract that retains complete field coverage, exact rational comparisons,
normalization/source fault detection and correct optimized-mode qualifications.
Do not silently drop float fields or call finite floats interval certificates.
The mathematical paper and original historical checker need not change merely
because a wrapper portability promise is corrected. The supported commands
must then be tested on their promised runtimes, followed by a NEW complete
whole04 review. This review does not choose or implement that repair.

## Independent mathematical work and strongest verified claim

Before reading candidate mathematics or prior reviewer reasoning, I hash-froze
every726 preexisting audit regular files and saved an independently developed
tensor/dual-localization derivation, with an explicit open quantitative Gram
gap. `EARLY_DERIVATION_PIN.json` seals those early bytes. The early sketch
contained my Brownian exponent slip; the separate `DERIVATION_COMPLETION.md`
corrects it explicitly without rewriting the early record. Its correct order
is n^-1/2 RMS. The completed independent verification supplies every central
normalization, regularity, covariance-path, Gram, source-convergence, witness,
variance, nonlinear-estimator and scaling argument in checkable form.

The strongest verified claim is exactly this: for independent centered standard
equal-H fBm components, each fixed H in (1/4,1), canonical iterated
`X_T=integral_0^T B1 dB2`, both complete uniform grids, every T>0, n>=1, and
every square-integrable grid-measurable estimator F, RMS is at least
`[2pi(4/45045)/(D_H sqrt(Pbar_f Pbar_g))] T^(2H)n^(1/2-2H)`.
The constant is explicit, strictly positive and H-only. The Gaussian Fourier
normalization and essential conjugation are correct. Endpoint traces justify
the zero-extension weak derivatives and three Fourier integrations by parts.
The two-sided periodization bound and finite Parseval give the simultaneous
upper Gram bound with the displayed2pi factor. Joint Gaussian independence
from the entire observation vector covers nonlinear F. The signed PSD trace
bound needs neither independent cells nor commuting covariance matrices.
The area pairing uses a fixed n,T limit of finite sums, so it makes no coupled
limit or stochastic-Fubini assumption. Auxiliary directions transfer through
the joint law of target and observations.

The canonical bridge is separately checked below/at/above H=1/2 and at the
H=3/4 summability transition. Separated-cell differentiation avoids singular
same/adjacent cells; lag counts give a sufficient vanishing Euler variance.
The polygonal half-correction has the stated exact covariance formula and
vanishes for H>1/4. The n=1 cell and arbitrary positive T are included directly.
At H=1/4 the correction's diagonal does not vanish; at H=1 the Fourier
normalization diverges and endpoints recover the area. Neither is included.
The halved antisymmetric area differs by observed information; the unhalved
difference has twice the residual RMS.

The new `independent_math_checks.py` uses unconditional exceptions and gives
exactly equal result JSON in normal and optimized modes. It adds16 exact
Brownian fine-polygon conditional tensor projections (including n=1), with
variance `(r-1)/(4nr)` and limit1/(4n), exact polynomial identities, a signed
noncommuting3x3 PSD trace example, an exact finite odd-series comparison and
a countermechanism to false rough increment lower coercivity. It removes each
of14 non-utc baseline fields in turn and confirms rejection by the actual
full-result guard; a utc-only change is accepted. These are meaningful finite
falsification controls, not a universal numerical proof. The original checker
replays successfully on Python3.14.6 in both wrapper modes and compares all
result fields except utc; its original optimized assertions remain disabled,
with explicit wrapper validation supplying the comparison.

No sharp constant, exact normalized limit, limiting distribution, endpoint,
H-uniform constant, adaptive/nonuniform grid, unequal-H or correlated-component
extension is accepted. Brownian optimum and smooth asymptotic rate are prior.
Historical theorem/method priority, full novelty and worldwide current-open
status remain **UNKNOWN**.

## Primary-source interfaces and attribution

`SOURCE_READ_LEDGER.json` pins the actual retained primary bodies and exact
read extents. The original OWR target's two pages were read completely; they
use this iterated convention and vector information and give the prior
Brownian optimum. A2012 conjecture does not prove present-world openness.
The NTU journal-formatted institutional copy was read for Theorem1/Theorem2,
Proposition6, Remark10, separated covariance and the near/tail lag split;
actual images of p229 and pp235-236 were viewed. It supplies the needed
canonical construction/Chen interface. The paper's sufficient convergence
argument avoids dependence on exact Euler coefficients.

The pinned NTU arXiv v1 Eq26/27 was read independently, including its actual
p12 image. Positive lag2 disproves the discarded all-lag little-o in that
specific version. The institutional journal proof retains near lags through
log n and removes only the tail, so the current paper correctly avoids a
journal-error assertion. No full census of exact source coefficients or
publisher-delivered byte identity is certified.

The retained NS author text was actually read through its main proof conclusion,
with scope and inherited extraction boundaries recorded; it establishes the
smooth-H liminf/limsup and Brownian credit and explains the failed rough
increment coercivity. A complete journal/PDF identity is not asserted. Actual
thesis pp56-57 and the2009 Dagstuhl abstract were read at their precise scopes.
Wu-Xiao's local Fourier bump/projection proof and Xiao's spectral LND statement
were read as antecedents, without pretending they already supply this
quantitative bilinear area bound. The full prior bounded priority report and
checkable implication comparisons were read. Its56 queries/20 controls were
not re-executed; two additional narrow searches were noisy and add no absence
certificate. Inaccessible Dickinson method bodies and the complete Jackowski
formula body remain unverified, with applicability UNKNOWN.

Fresh primary opens succeeded for NTU institutional/arXiv and Wu-Xiao bodies;
three DOI opens failed and were replaced by authenticated retained primary
body reads. No downloaded third-party body, extraction or pixel was duplicated
into this review or redistributed. The current paper, abstract, supplement,
README, citation and metadata preserve the required attribution and UNKNOWN
priority boundaries. No scientific or priority finding beyond those already
qualified limitations was found.

## Actual package execution, filesystem controls, archive and PDF

`COMMAND_RECEIPTS.json` contains173 actual primary-suite commands, with29
expected successes and144 expected rejections, all matching their expectations
on Python3.14.6. The separately retained3.11 portability reproductions are the
new finding, not included in an all-pass banner. Exact commands and full
stdout/stderr are retained, rather than a planned checklist.

Both modes cover clean default absent bindings, current strict present bindings,
explicit required valid bindings, optional explicit missing bindings, required
missing bindings, malformed/corrupt PDF/ZIP/manifest bindings, missing archives,
binding symlinks, original checker replay and deterministic archive building.
Bootstrap-manifest symlink/directory cases reject before JSON parsing; actual
archive commands reject the bootstrap symlink before ZIP creation. Ordinary
members and member ancestors reject symlinks too. Twenty coherent-manifest
current-status mutations are rejected semantically, including attempted
readiness/publication promotion and removal of root or whole03 gates.

All three actual writers were exercised in both modes on real case-insensitive
samefile premises in my disposable extraction: canonical script root to alias
target and the reverse, nested existing parents, missing multilevel internal
parents, direct internal paths, parent traversal, existing files/directories,
hardlinks, symlinks, dangling leaves, linked parents/ancestors and absent
external parents. Every expected rejection precedes output creation; a real
executable compiler sentinel never runs on a rejected PDF location. Physically
external case aliases reach the writers; the PDF positive control reaches
the sentinel. Reused checker/compiler output directories containing aliases
at14 child filenames reject before any child canary change. No canonical
candidate inode was used for destructive alias testing. This is static local
preflight evidence, not a concurrent-race or arbitrary-compiler guarantee.

The explicit166-member CLOSED ZIP was independently rebuilt, closed, and
compared byte-for-byte. Sorted names, every payload and CRC, ZIP_STORED,
fixed2026-10-14 timestamps, Unix create-system and regular0644 headers agree.
The current ZIP remains1,597,595 bytes, SHA256
`807f4b259966b3d32a2cb9be40c52886658a445a95944123653aa5ce62559903`.

Actual standalone PDF compilations in ordinary and optimized wrapper modes
each reproduce the unchanged93,113-byte PDF exactly, SHA256
`33b90a4d846db58ea93efd453c13455fbeb3a29dcaa3e4cc49a68c0a8ebdff5b`.
All seven actual pages were individually rendered and viewed, with no observed
clipping, overlap, missing glyph or reference-layout defect. The PDF skill was
read and followed; no authoring marker was repeated for this read-only
reproduction of unchanged paper source. Compiler logs report no overfull boxes.
TeX remains SHA256
`4ffbe0d65609213fd91aecf675661ff278e4e1bd5037db8836f1291f5bdc1d78`.

## Native metadata, custody, rights, workflow and scope

All operative package modules and original checker were read completely; the
actual native uploader source and local check dispatch were inspected. The
actual repository `zenodo.py check` was executed only locally, including both
Python wrapper modes, against `publication/zenodo-deposit.json`. It selects
the exact current PDF and ZIP. Its metadata equals the bare metadata object
and both included wrappers exactly. Included `deposit.json` is correctly
described as historical metadata wrapper, not native uploader input. The plain
UTF8 scholarly citation agrees with the title, author, ORCID, version/date,
preprint kind, license and AI/unrefereed/priority disclosures. The invalid old
CFF is explicitly inactive history. Rights language licenses newly authored
work and excludes cited third-party bodies. No invented DOI or peer-review
claim was found.

`CUSTODY_RECHECK.json` independently verifies every4,346 historical row:
all2,788 original rows against their original source manifests, values/order,
old resolution and new exact current/before resolution; plus all1,558 later
terminal rows against their actual source arrays. It also verifies668 repair
baseline inputs, all9 before/after edits,659 protected unchanged records,
322 current candidate rows,684 current-audit rows,39 repair outputs,25 core
protected identities, all128 exact source/copy pairs, the first116 map rows
and order, all39 individually recorded omissions across three ledgers, and
the separately pinned AGENTS bytes. Every omission is an exact pinned local
record, not a claim that an omitted program or old ZIP was newly replayed.
The scoped case-alias evidence is correctly labeled an excerpt; its exact
section is present in its fully pinned original report. No full-source-copy
claim was substituted. All nine submitted originals were additionally read
from the actual Git objects at the stated head and compared as bytes, without
an index/branch/commit/remote mutation.

All726 inputs frozen at this review's entry are unchanged at recheck. Every
dated old report, pin, seal, status and root adoption retains its original
bytes and historical meaning. Current CASE_ALIAS_REPAIR_STATUS accurately
held the package for this new complete review. This new review's completion
and new finding are external evidence until root adoption; I did not rewrite
that status or reinterpret old whole02 as having found this later issue.

Initial ENOSPC prevented folder creation/freeze, before any candidate/prior
reasoning read; work resumed after storage became available. Retained artifacts
are confined to this assigned folder. Two initial default-checker subprocesses
inherited platform temporary-directory selection and automatically removed
those temporary outputs; both were repeated with TMPDIR confined to my own
scratch. All own extraction/build/render/alias derivatives were individually
pinned after commands settled and then removed; the3.11 computed results are
retained separately. No preexisting audit artifact, third-party cache, runtime,
candidate or old report was deleted or edited.

No new subagent, outward correspondence, PR/queue/tracker operation, remote
Git action, deposit/stage/publish/DOI operation or ordered-service bypass was
performed. Outside expertise could help locate poorly indexed precedents;
that remains a research gap only, with no outreach prepared or initiated.

**Terminal handoff:** whole03 is complete with P0=0,P1=0,P2=0,P3=1.
Root should adopt WHOLE03-P3-01, perform a bounded support repair, and obtain
a NEW complete whole04. Root terminal integrity adoption and the PR1032 hold
remain in force. No review-completion percentage in this folder confers
readiness, priority clearance or publication authority.
