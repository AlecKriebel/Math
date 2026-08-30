# Independent referee report: fourth revision

Date: 29 August 2026

Reviewed package:
`/Users/alec/Documents/Math/k3p_level2_fourth_revision_referee_final_2026-08-29`

## Recommendation

**Mathematical recommendation: valid subject to explicitly named minor release
corrections.  Reproducibility status: current verification PASS; current full
regeneration incomplete at 38/55 before filesystem `ENOSPC`, so no fresh
fourth-revision 55/55 PASS is claimed.**

I find the stated mathematical theorems correct within their express scope,
conditional on the disclosed exact finite computations.  I found no
theorem-level counterexample, circularity, quantifier shift, physical-domain
gap, or regression from the third revision.  The four defects that motivated
this resubmission are substantively repaired:

1. the official runner's three mode-drifting writers preserve `0644` and are
   covered by a focused negative control;
2. both cut-transfer verifiers now bind the complete typed nine-step analytic
   declaration and reject coherently resealed claim-body attacks;
3. the 16/16 mutation count and the local/downstream resealing description are
   accurate; and
4. both source archives now have a fully bound, final-commit, cached-only build
   contract, and four fresh offline builds reproduced the two PDFs exactly.

The official combined replay was launched once in a clean, network-denied copy
and was never duplicated.  Its 4-command verification phase passed completely.
The regeneration then passed commands 1--38, but command 39—the hour-scale
probe producer—encountered a filesystem `ENOSPC` condition at two-port
parent 600/2,107.  It failed while flushing gzip ledgers; commands 40--55 were
not invoked, and I did not rerun it.  This is an explicit fresh-regeneration
limitation, not an observed semantic failure; command 39's later checks and
commands 40--55 were not reached.  The changed cut/mode/four-port/anchor/
restoration cone had already passed, the current 20-child integrated replay
had passed, and the probe/restoration/four-port/sharpness directories are
byte-identical to the preceding package whose independent exact-once run
passed all 55 command bodies.  I therefore do not treat the disk event as
evidence against the theorem, but I do not claim a fresh 55/55 fourth-run PASS.

Three localized release issues remain.  A fourth JSON writer omitted from the
new control still creates mode `0600` when the integrated verifier is invoked
directly with its default report path, although every declared runner route
avoids that sealed-output path.  The historical release ledger still labels
third-revision hashes and counts “current.”  Finally, the supplied folder
already contains an unsealed `review_runs/` tree despite the documented clean
starting state, and excluded runtime control paths should reject pre-existing
symlinks before use.  None affects the proof or my clean fresh execution
through its disclosed `ENOSPC` stop, but all should be corrected at the next
reseal.

My confidence that the theorem statements are correct within their stated
domain is **96% (high)**.  Confidence in the prior-fix dispositions and the
three residual release findings is **at least 99%**, because each follows from
fresh execution or direct source/data-flow inspection.

## The result reviewed

For binary standard semi-directed strongly tree-child networks of level at
most two on the same finite labelled leaf set, using the paper's one-step root
suppression convention, fixed observable `C/G/T` sectors, strict inheritance
probabilities, and principal-positive K3P edge parameters, the source-relative
regular containment relation satisfies

`N <= N'  iff  N and N' are ordinary-triangle equivalent  iff  their images
share a regular germ full-dimensional in both`.

Ordinary-triangle equivalence requires equal labelled reduced trees of blobs,
labelled mixed-graph isomorphism of corresponding nontriangle complete
factors, and coherent redirection of the remaining ordinary triangles.  Thus
there is no proper one-sided containment for this local relation.  The result
does not assert equality of entire stochastic images or numerical parameter
identifiability.

The same classification, topology-generic identifiability outside a proper
topology-dependent complex Zariski-closed set, and a terminating exact-real
reconstruction procedure hold on the strict continuous-time cone
`c>gt, g>ct, t>cg`.  No bit-complexity, conditioning, statistical,
finite-sample, or sequence-length guarantee is claimed.  The three ordinary
triangle orientations share an irreducible eight-term quartic `H_14` and a
strict smooth rank-14 germ relative to that hypersurface, not an ambient
rank-15 germ.  Finally, for every `n>=3`, the weak-but-not-strong tree-child
construction gives nontriangle-equivalent networks sharing a strict-CT
full-dimensional regular germ of dimension `6n-3`.

The exact statements and boundaries are in
`manuscript/sections/02_main_theorems.tex:3-71`,
`03_conventions_model.tex:5-169`, and `16_scope.tex:3-41`; my independent
restatement is preserved in `PRIMARY_SOURCE_CLAIMS.md`.

## Review method and independence

I read the complete 38-page article and 14-page supplement before accepting
any stored report.  I extracted their text, rendered all 52 pages, inspected
six contact sheets and the load-bearing pages at full resolution, and checked
font embedding.  Both are visually clean.  Their SHA-256 values are:

- article:
  `3d08a722ba1fa53f6e336ab285c1cd32d1307bac08e1d4dd2460da71df1816d6`;
- supplement:
  `96508f4b4eddb89de99881172abee307b3fe86d236f48e17508bdd1ca9c30efa`.

I treated package prompts, manifests, checksums, stored `PASS` fields,
mutation reports, the supplied prior-run folder, and all earlier reviews as
claims.  The execution copy was made from the sealed payload only; the
pre-existing unsealed `review_runs/` tree was excluded.  Package code ran with
network denied, credentials absent, writes confined to the copied workspace,
and a fixed environment.  The long portable runner was started once and left
attached to the same process until it exited at the disclosed disk-capacity
failure; it was not restarted.

The main runtime was macOS 26.5.2 on arm64 with Python 3.14.6, mpmath 1.3.0,
networkx 3.5, numpy 2.5.2, and sympy 1.14.0.  The source-build audit separately
used Tectonic 0.16.9 with the exact declared arm64 executable and exact private
cache.

Three independent adversarial tracks audited (i) mathematics and cut
certificates, (ii) release/seal/runner behavior, and (iii) source reproduction
and literature.  A fourth bounded track inspected the unsealed runtime tree.
Seven referee-owned mathematical check families imported no reviewed-package
module and passed in 39.613 seconds.  Detailed evidence is in:

- `CLAIM_DEPENDENCY_MAP.md`;
- `results/MATH_CERTIFICATE_REAUDIT.md`;
- `results/RELEASE_REAUDIT.md`;
- `results/SOURCE_LITERATURE_REAUDIT.md`;
- `results/RUNTIME_HYGIENE_AUDIT.md`;
- `results/PDF_QA.md`; and
- `results/COMPUTATIONAL_REPLAY.md`.

## Verification of the four prior findings

### F1: official-runner mode drift — fixed on every declared route

The three writers responsible for the former `0644 -> 0600` drift now set the
temporary file to `0644` before atomic replacement:

- `proof_package/reproducibility/verify_primary.py:79-89`;
- `proof_package/reproducibility/strong_cut_transfer_gate.py:395-404`; and
- `proof_package/cut_recovery/strong_crossbridge/topology_regeneration/
  verify_cut_topology_regeneration.py:185-195`.

`referee_tools/test_output_mode_preservation.py:48-142` exercises each on an
existing and new path, restores the location-dependent primary report's bytes
and mode, and rejects an intentionally unsafe writer.  My fresh bounded
execution saw all six enumerated cases at `0644`, restored the canonical report to
`0644`, and detected the negative `0600` mutation.  The runner invokes this
control before each phase and rejects undeclared byte, mode, type, symlink, or
virtual-environment drift (`run_active_verifiers.py:49-98,547-625`).

The one residual writer in `verify_k3p_same_classification.py` is discussed
under R1 below; static route tracing and fresh execution establish that it is
not used as a sealed output by the official `verify`, `regenerate`, or release
suite routes.

### F2: cut-certificate semantic fidelity — fixed

The evidence now has a typed nine-row implication contract, not unconstrained
nonempty prose.  The producer defines it at
`cut_recovery/strong_crossbridge/global_transfer/
build_k3p_cut_inclusion_evidence.py:26-111`, the direct verifier carries its
own full expected object at `verify_global_transfer.py:43-126`, and the
separately implemented adversarial verifier carries another at
`adversarial/verify_global_transfer_adversarial.py:83-167`.  Literal equality
is required at direct lines 309-311 and adversarial lines 424-426.

Fresh referee-owned execution established:

- the producer rebuilt the delivered evidence byte-identically with SHA-256
  `eea8d603b835d315c39b6a87f8ae691e897e8e982b65a92cfd1f2acd84449689`;
- 72/72 ordinary mutants (four semantic attack styles for each row and both
  implementations) were rejected;
- 18/18 optimized-Python claim mutations were rejected;
- all four ordinary/optimized direct/adversarial unbound-path attacks were
  rejected; and
- the release wrapper passed once in ordinary and once in optimized mode.

The release wrapper now freshly executes both semantic implementations
(`global_transfer/verify_release.py:304-369`), and the active outer gate invokes
that wrapper in both Python modes
(`reproducibility/strong_cut_transfer_gate.py:152-182,364-365`).  The article
and supplement now accurately distinguish machine binding of the finite typed
contract from the handwritten proof of its analytic implications.

### F3: stale mutation metadata — fixed

`proof_package/ACTIVE_MANIFEST.json:319-321,395-397` says and binds 16/16 cut
gate mutations.  The coherent-legacy attack now says exactly that its local
attack cone was resealed and unrelated downstream reports were not
(`test_cut_transfer_gate_mutations.py:121-127,163-172`).  The new manifest
version identifies the certificate-fidelity repair.

In a fresh exact detached worktree at commit
`10bd695cc7b7e0fd98a187026059b043589244f0`, the complete Git-bound
release-engineering suite rejected 37/37 attacks, passed 12/12 controls, left
the scoped Git state clean, and reproduced the stored logical payload.  I
treat this as packaging evidence, not as proof of the mathematical theorem.

### F4: incomplete source/PDF contract — fixed

The revised verifier binds the Tectonic executable bytes and version, bundle
URL and digest, exact 725-file/57,507,581-byte cache inventory, `--only-cached`
command, and an exact minimal 12-key Tectonic environment
(`release/verify_source_reproduction.py:70-219,340-444`).  It performs two
builds, checks the cache before and after, and requires equality with the
committed PDF (`:447-560`).  The outer manifest seals both final-commit reports
and all four transcripts.

An independent checker imported no package implementation.  It matched 23/23
article and 1/1 supplement source members to exact Git blobs and reconstructed
both canonical ZIP byte strings exactly.  Under network denial, one successful
article verifier process performed two builds in 7.155 seconds and one
supplement verifier process performed two builds in 2.012 seconds.  Every
output matched the delivered and committed PDF byte-for-byte and every fresh
logical report payload matched its sealed counterpart.

There were three source-verifier process invocations and four completed
Tectonic builds.  The initial article launcher failed in 0.2 seconds before
Tectonic started because macOS's `/usr/bin/git` shim was sandbox-blocked.  The
outer launcher was changed to the installed Homebrew Git; no completed
successful verifier invocation was repeated, exactly the four intended
internal builds completed, and no network or child-build restriction was
relaxed.

The arm64 Tectonic binary and approximately 56 MB cache remain external rather
than vendored.  Their bytes and inventory are exactly bound and the limitation
is disclosed; byte-identical source rebuilding therefore requires a matching
toolchain/cache, not merely the source ZIP.

## Mathematical correctness

The mathematical article sources `01` through `16` are byte-identical to the
third revision.  Only the reproducibility disclosure and reader supplement
changed.  I rechecked the formerly load-bearing cut argument and the other
handwritten transitions against the finite evidence boundaries; I found no
mathematical regression.

### Topology and directed cut transfer

The fixed semi-directed convention and inverse-Fourier principal/strict-CT
domains are explicit and consistently used.  A true cut has flattening rank at
most four (`04_physical_topology.tex:66-80`).  A source noncut is detected
generically by the displayed-tree wrong-quartet minor (`:82-142`), rather than
by the retired JC pointwise theorem.  Directed inclusion then follows by
pulling a target cut polynomial back to the source open set (`:144-159`).  The
reverse inclusion uses the crossing-hull/one-component-hull alternatives and
the 204 one-active directions only after these facts, with no premature common
bridge-tree premise (`:274-362`).

The exhaustive finite inputs report 808,642 balanced words, 379,742 reduced
palette presentations, zero switching survivors, and the displayed-tree 5-by-5
minor.  The package's producer, no-import verifier, direct/adversarial gates,
and mutations agree; an independent bounded derivation reproduced the
combinatorial count and determinant structure.  No JC premise remains
load-bearing.

### Local geometry, bridges, and gluing

The literal tree--sunlet circuits give the claimed strict separator.  The
eight-term triangle pullback has generic rank 14, lies on the stated irreducible
quartic `H_14`, and has a nonzero gradient on a strict physical point.  The
three orientations therefore share the same relative smooth germ; the paper
does not mistake that for ambient rank 15
(`05_three_leaf_geometry.tex:1-212`).

The three-sector bridge factorization has the stated gauge freedom and becomes
free after normalization.  Marginal localization rules out remote
compensation, and the capped strict inequalities keep the glued parameters
inside both principal and strict-CT domains
(`06_bridge_fibre.tex`, `07_marginal_localization.tex`, and
`12_continuous_time.tex`).  Referee-owned exact checks covered bridge degrees
3 through 16 and both domain gluing constructions.

### Four-port completeness, anchors, restoration, and probes

I traced the full four-port producer from its primitive graph presentations to
the 405,216-case universe.  The separate verifier independently derives the
27,834 post-topology cases, exact rank/polynomial partition, restoration
handoff, and `40=38+2` quotient without reading the producer, historical atlas,
frozen raw ledger, or fourteen-orbit lock.  Exact polynomial separators,
syzygy rank upper bounds, saturation assumptions, coordinate/port transports,
and directional witnesses are checked before the quotient is consumed
(`08_four_port_classification.tex` and the mapped code in
`CLAIM_DEPENDENCY_MAP.md`).

The starting universe is likewise derived rather than assumed: 133 non-four
anchors, 144 raw four-port equality parents, 26 direct generators, 1,260 first
restoration requests, 96 second requests, zero unmatched obligations, and the
176-row designated serialization.  The 424 physical descendants induced by
root movement are reconciled with existing one-port rows rather than discarded.
The restoration replay has 36,824 rows, and the independent semantic probe
route reconstructs all 574,535 insertion/restriction/transport rows.

I did not manually reproduce those two largest enumerations by hand.  I
inspected their independent implementations and import boundaries, ran the
complete four-port producer/verifier and current integrated restoration/probe
verification routes; the standalone fresh probe producer did not complete.
The current integrated route nevertheless independently streamed the full
delivered restoration/probe censuses, semantically reconstructed all 574,535
delivered probe rows, and rejected its seven coherent mutations; referee-owned
checks reconstructed representative rows spanning each one-port status plus a
two-port restriction.  This is strong computer-assisted evidence, not a claim
that the enumeration has been formalized in a proof assistant.

### Global analytic implications, genericity, and reconstruction

Once cuts and complete factors agree, the local classification permits only
ordinary-triangle redirection.  Contextual triangle gluing uses the same
labelled contraction and the bridge gauges simultaneously across sectors.  The
analytic target sections are constructed inside the relevant physical domain;
the proof does not infer an open physical section merely from complex
dimension.  The global necessity and sufficiency chain in
`10_global_classification.tex` consumes the finite local results in their
proved directions.

The exceptional set is topology-dependent and proper.  The exact-real
reconstruction argument terminates by finite polynomial-sign decisions and
real-closed-field quantifier elimination; it makes none of the computational
or statistical efficiency claims that would require conditioning or bit-size
analysis (`11_genericity_reconstruction.tex`).  Restriction to the strict-CT
cone preserves full dimension and all constructive margins.

### Weak-class sharpness

At three leaves the two weak-but-not-strong maps have certified rank 15 on a
rational strict-CT box.  The Krawczyk self-inclusion proves uniqueness only on
the declared slice, exactly as stated; the interval rank and physical margins
are outward checked.  The six-dimensional labelled-cherry inverse then raises
the common-germ dimension by six at each extension, giving `6n-3` for every
`n>=3` (`13_sharpness.tex`).  My independent interval reconstruction and cherry
Jacobian check passed.  No claim of global parameter uniqueness is inferred.

### Adversarial boundary and counterexample search

I specifically tested the most plausible ways to overread the result.  Boundary
inheritance values, equality in the CT inequalities, zero/signed Fourier edge
eigenvalues, higher level, weak tree-child networks, nonbinary vertices,
untransported state-sector permutations, and full numerical-parameter recovery
are all outside the theorem rather than silently absorbed into an open-domain
claim.  Ordinary-triangle equivalence is contextual and labelled; it does not
identify arbitrary triangles or claim equality of their complete stochastic
images.  The generic result removes a topology-dependent proper closed set and
does not assert pointwise topology recovery on rank-drop loci.

I looked for remote compensation across a bridge, a nonphysical analytic
section, port or direction reversal in transported four-port witnesses,
discarded root-movement descendants, an unmatched restoration request, a
source/target reversal in the cut argument, and a hidden use of the retired JC
premise.  Static tracing, exact representative calculations, exhaustive active
checks, and coherent mutations found none.  The weak-class construction itself
is the advertised sharp boundary: relaxing strong tree-childness produces the
full-dimensional ambiguity, so the theorem does not improperly extend across
that boundary.

## Code and certificate fidelity

The active evidence graph is recorded in `CLAIM_DEPENDENCY_MAP.md`.  The main
separation-of-implementation checks are genuine: the four-port no-import
verifier, graph-only anchor derivation, all-row semantic probe replay, cut
palette verifier, and adversarial typed cut verifier do not simply read a
producer's Boolean.  Hash equality is used for identity/provenance after the
semantic or exact-arithmetic checks, not in place of them.

Exact arithmetic is rational/integer/symbolic where the proof requires exact
rank, polynomial, graph, and census decisions.  The interval portion uses
outward-safe rational bounds.  Failure paths check exit codes and sentinels,
ordinary and optimized Python modes are covered where assertion elision could
matter, and coherent mutations target both data and binding layers.  The
mutation suites do not prove completeness, but no tested attack survived.

The sole certificate-interface defect I found is R1, which concerns report
mode and seal preservation, not semantics.

## Computational reproducibility and package integrity

The initial integrity check passed on a clean sealed-only copy:

- outer payload: 635 files and 161,122,700 bytes, with bytes and modes bound;
- expanded canonical proof core: 597 members and 160,213,642 bytes;
- proof source and package builder commit:
  `10bd695cc7b7e0fd98a187026059b043589244f0`;
- package-manifest SHA-256:
  `c67c1c524ef59217a2327e7dd4016cd82a9b8be1e8f188e6cc61a4fe1fd6c725`;
- outer checksum-list SHA-256:
  `5bf8045cf745754092f0eb7e1a00bd7842ba475dc70d74091b099e135b974fa4`.

An independent Git reconstruction selected 594 committed files totaling
160,051,159 bytes and matched each to the expanded proof package, then matched
the outer copied tools, logs, and PDFs.  Fresh mode and symlink mutations were
rejected.  The compressed canonical TAR container is not delivered and is not
covered by the extracted-package checker; the package states this boundary.

Fresh verification passed 4/4 in 2,977.293 seconds.  The 20-child integrated
replay took 2,961.961 seconds; all four required sentinels were observed; the
workspace and virtual-environment drift sets were empty.  The verification
report/transcript SHA-256 values are
`df3fc24df0f7a42a70506e4118bd00d033038f9af93acff4cd6bd3a1010da457`
and
`98b7bc561e8900074e12bc8f0d925237915d331dddf5d2fbf66f58cec301a99f`.

Regeneration produced 38 clean PASS result rows with a child-time sum of
2,138.644 seconds before the external failure.  Those rows include the revised
cut cone, the 405,216-presentation four-port producer, 133-row anchor producer,
36,824-edge restoration producer and independent replay, and their mutations.
The complete partial transcript SHA-256 is
`9eaeaf563fd1ee219e533142addb893db90f4191ac12747a86042facd2e80153`.
After exit, a fresh integrity check again passed the 635-file/597-member seal,
and an independent comparison found no change in the 6,635-entry virtual
environment.  Exact command accounting, failure text, unexecuted names, and
evidence reconciliation are in `results/COMPUTATIONAL_REPLAY.md` and
`results/official_replay/REPLAY_SUMMARY.json`.

The source reproduction, release mutation replay, and seven independent
mathematical spot families are additional bounded evidence.  Their artifacts
and full command/accounting reports are preserved in this audit folder.

## Remaining release and presentation findings

### R1. Omitted fourth atomic writer

**Severity: minor release-interface/portability defect; no theorem effect.**

`proof_package/reproducibility/verify_k3p_same_classification.py:2189-2198`
uses `NamedTemporaryFile` and `os.replace` without a `chmod`.  Fresh calls on
an existing `0644` path and a new path both produced `0600`.  The focused test
enumerates only the other three writers
(`referee_tools/test_output_mode_preservation.py:48-58`).

The artifact-only and release-suite routes use `--no-write-report`, the fresh
integrated route writes under `release/work/`, and the official runner restores
the canonical location-dependent report.  Thus R1 does not invalidate the
declared replay.  Direct default invocation can nevertheless change a sealed
report's mode and make the package seal fail.  Add
`os.chmod(temporary, 0o644)` before replacement and cover this fourth writer's
existing/new cases.

### R2. Stale “current” wording in the historical ledger

**Severity: minor editorial release metadata.**

`proof_package/release/FINAL_RELEASE_ENGINEERING_REPORT.md:3,22-54` describes
the second-referee repair, 32 release mutations, third-revision PDF hashes, and
624-file handoff as current.  Lines 66-70 make the manifests authoritative and
`START_HERE.md:13-18` explicitly calls the file historical; the current
manifest and machine reports are correct.  Relabel the opening status/heading
as historical or add a current fourth-handoff addendum.

### R3. Pre-populated excluded runtime tree and no-follow setup

**Severity: minor delivery hygiene and low security hardening in this review,
because the prior run was not relied upon; it would become a moderate
provenance defect only if represented as authenticated acceptance evidence.
No current exploit or theorem effect.**

The supplied folder contains 27 files totaling 14,899,839 bytes under
`review_runs/`, although `START_HERE.md:28-29,54-55` says that tree is created
by the reviewer and absent from a clean delivery.  Integrity intentionally
skips all descendants (`verify_package_integrity.py:73-92`).  The files are
ordinary and internally hash-consistent, but their self-contained hashes do
not authenticate them.  I treated them as untrusted and did not use them.

The current tree has no symlink or special object.  Prospectively,
`RUN_REVIEW.sh:18-21` creates `review_runs/runner_control/home` and `tmp` before
integrity preflight, so a hostile pre-existing excluded symlink could redirect
the control `HOME`/`TMPDIR`.  The required external sandbox limits impact but
does not close this path check.

Ship a clean folder.  If the prior run is evidence, seal it under a separate
non-runtime path.  Perform integrity first, reject pre-existing symlink or
non-directory control-path components with `lstat`, and create the private
runtime directory with no-follow semantics.

## Scope, novelty, and literature positioning

The paper's novelty claim is appropriately narrower than “first K3P network
identifiability result.”  Nearby primary work proves full identifiability for
level-1 semi-directed networks modulo ordinary-triangle redirection on the
authors' restricted `Theta_0` parameter space under JC/K2P/K3P
([Brits et al.](https://arxiv.org/abs/2607.12919v3)), and generic JC
identifiability for binary, triangle-free, strongly tree-child level-2
semi-directed networks
([Englander et al.](https://doi.org/10.1101/2025.04.18.649493)).  Other nearby
work gives partial
level-2 invariant separations
([Ardiyansyah](https://arxiv.org/abs/2104.12479)), local triangle
semialgebraic results
([Currie et al.](https://arxiv.org/abs/2606.26673)), local sunlet
implicitization
([Cummings and Hollering](https://arxiv.org/abs/2311.07678)), and level-1
dimension formulas
([Gross, Krone, and Martin](https://arxiv.org/abs/2307.15166)).  The claimed
advance is the complete strong level-at-most-two K3P regular-containment
classification, including triangles, with exact finite certification and a
weak-class sharpness construction.

A bounded check of the closest named and current primary sources found no
result that subsumes that theorem.  The article accurately limits the novelty
of rank 14: earlier computations foreshadowed the dimension, while the paper
claims the exact quartic, certification, physical smooth germ, and use in the
global classification.  Literature priority remains inherently bounded; this
audit cannot rule out unindexed or unpublished work.

## Unexecuted or unresolved checks

1. The current full regeneration did not complete: 38/55 commands passed,
   command 39 failed only with `Errno 28`, and commands 40--55 were not invoked.
   Per the user's instruction it was not rerun.  The unchanged-code prior full
   run, current fresh verifier, current partial run, and independent checks are
   the basis for the mathematical assessment; they are not relabelled as a
   fresh current 55/55 run.
2. I did not hand-enumerate all 405,216 four-port presentations or implement a
   third exhaustive generator.  I inspected and ran the producer and its
   independent no-import verifier, mutations, and representative exact checks.
3. I did not write a new all-row implementation for all 574,535 probe
   semantics.  The package's separate all-row semantic replay ran; I
   independently streamed the full census and reconstructed representative
   cases across every status family.
4. For sharpness, the rational center, frozen coordinates, selected columns,
   and radius are certificate inputs.  I independently rebuilt the literal
   maps, interval operations, Krawczyk image, rank bounds, physical margins,
   and cherry inverse; no uniqueness beyond the stated slice is claimed.
5. I used the exact existing Tectonic executable and cache.  I did not download
   or regenerate the 725 cache files from the bundle URL, and the toolchain is
   platform-specific and nonvendored.
6. The compressed canonical archive container is not delivered, so I checked
   the expanded core and its canonical selection rather than container bytes.
7. The literature search was bounded to the closest primary results and
   current adjacent records; it cannot establish absolute priority.
8. R1--R3 remain uncorrected in the package reviewed here.  Their repairs have
   therefore not been tested in a later reseal.

## Conditions and final verdict

Before treating the package as the clean final referee handoff, I recommend:

1. repair and test the fourth atomic writer (R1);
2. relabel or update the historical release ledger (R2); and
3. remove or separately seal the supplied prior-run evidence and harden the
   excluded runtime control path against pre-existing symlinks (R3).

No theorem statement, mathematical lemma, four-port case, probe row, or source
archive needs revision on the evidence found.

**Final verdict: valid subject to explicitly named minor corrections.**
Mathematically valid within the explicit assumptions and finite-certificate
boundary; the remaining work is localized release-interface, provenance, and
editorial hardening.  This is not a fresh fourth-revision reproducibility PASS:
regeneration remains incomplete at 38/55.
