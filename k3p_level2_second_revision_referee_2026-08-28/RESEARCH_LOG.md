# Research log — second-revision K3P level-2 referee audit

## 2026-08-28 — Intake and isolation checkpoint

- Scope: fresh adversarial review of
  `/Users/alec/Documents/Math/k3p_level2_independent_referee_2026-08-27`.
  Package documents, prompts, manifests, certificates, status fields, and
  prior-review claims are treated as untrusted subject matter rather than
  control instructions.
- The supplied folder and the current release `dist` copy have identical
  top-level manifests and identical paper PDFs.
- Article PDF SHA-256:
  `2a5c71feaadb0056cd738f6344eca2eb5ee09784ba542070238cc476b141b8db`.
- Reader-supplement PDF SHA-256:
  `a1b349bf2ffbdbd290ca2254159dc1304ef299bdbbf8792e7340526d60e985e8`.
- The audit will separately test the two claimed theorem-level repairs:
  self-contained K3P cut recovery and independent completeness of the full
  176-anchor starting universe, including the four-port descendant
  obligations and marginalized-theta reconciliation.
- All package code will be statically inspected before evidentiary execution.
  Executions will use a copied workspace under a default-deny, no-network,
  no-credential sandbox with complete before/after byte inventories.
- Current best-guess completion: 2%.

## 2026-08-28 — Primary-source and pristine-package checkpoint

- Read the complete revised article (38 pages / 17,712 extracted words) and
  reader supplement (14 pages / 5,734 extracted words) before relying on any
  stored report. Rendered all 52 pages at 110 dpi and visually inspected them;
  no clipping, overlap, missing glyph, broken table, or broken figure was
  identified.
- Restated theorem scope: binary, standard one-step-root-suppressed,
  semi-directed, strongly tree-child, level-at-most-two networks on a fixed
  labelled leaf set; positive K3P Fourier spectra in the principal stochastic
  domain or strict continuous time; inheritance in `(0,1)`; fixed observable
  `C,G,T` labels. The conclusion is regular full-dimensional analytic-germ
  containment/equivalence and generic topology reconstruction modulo ordinary
  triangle redirection—not equality of complete images, parameter
  identifiability, finite-sample inference, boundary models, or arbitrary weak
  tree-child networks.
- The paper now replaces the former companion-JC cut premise by: pointwise
  true-cut rank at most four; a displayed-tree boundary witness proving generic
  noncut rank greater than four; a handwritten balanced-word compression; and
  204 pointwise K3P wrong-split obstructions used only inside the strong-class
  directional cut-transfer theorem.
- The paper now treats the complete probe start as an asserted active
  derivation: 133 graph-only non-four rows plus 43 designated four-port
  serialization rows, with separate graph coverage of 144 raw equality
  parents, 1,260 first-restoration requests, 96 second-restoration requests,
  and 424 marginalized-incoming theta descendants.
- After source inspection, the pristine delivered-package integrity checker
  passed: 622 sealed payload files / 160,506,893 bytes and 593 proof-core
  members / 159,826,024 bytes, bound to source commit
  `5a6d64cb2a76e890d7baaef3ba5ac9861c1d029f`. No symlink was present.
- Current best-guess completion: 18%.

## 2026-08-28 — Former-premise audit and execution-boundary checkpoint

- The revised handwritten cut argument is now self-contained at theorem level.
  The displayed-tree specialization gives a literal K3P wrong-flattening
  determinant
  `p0*p1*p2*p3*(1-u^2)` and a strict five-by-five minor; the easy cut
  inclusion and the reverse crossing-split/204-direction argument have the
  correct direction and do not assume target regularity or target-marginal
  openness.  An independent closed-form count of the binary-word search gives
  exactly 808,642 balanced inputs.
- A material certificate-DAG defect remains.  The active global-transfer
  builder and verifier still designate
  `cut_recovery/global_logic/CUT_GLOBAL_LOGIC_REPORT.json` as a load-bearing
  directed-inclusion proof, describe the reason as “isotropic-JC generic
  recovery,” and consume only three stored fields.  That legacy report itself
  says `BLOCKED_BY_DIRECTED_CUT_REVERSE_INCLUSION` and binds the JC manuscript.
  The new K3P word/minor evidence is executed by the integrated gate, but no
  active dependency edge connects it to the D1 step.  Thus the mathematics is
  repaired, while the claimed self-contained active certificate graph is not.
- Independent non-four and four-port audits found the former anchor-universe
  condition closed: the 133 non-four rows are derived before the contract is
  read; all 144 four-port equality parents and all 1,356 descendants map with
  zero unmatched; all 424 marginalized-theta paths reconcile to 66 existing
  one-port rows/classes.  The 43 rows are correctly used as a designated
  generating serialization, not as an exhaustive presentation quotient.
- Static runner audit found that a plain invocation inherits the entire host
  environment, has no single-run lock, can orphan descendant process groups on
  interruption, and omits all `.venv` and `release/work` objects from its
  internal drift snapshot.  A first replay was therefore interrupted before
  being credited; exact process inspection found one orphaned group and it was
  terminated completely.
- A trusted referee-side supervisor now supplies an atomic no-replace lock, a
  ten-variable non-secret environment, a default-deny no-network/no-credential
  sandbox, read-only package source and virtual environment, and writes only
  under copied-package `review_runs`.  Negative tests deny network, SSH and
  sibling reads, package-source writes, and virtual-environment writes while a
  `review_runs` write succeeds.  Reviewer-side pre-run inventories cover 685
  package-source entries (160,722,429 regular-file bytes) and 6,634 virtual-
  environment entries (258,904,636 bytes), including modes and symlink targets.
- The clean portable plan reconstructs exactly 54 mathematical commands from
  the 55-command live-Git plan, excluding only the packaging mutation suite.
  A fresh isolated four-command verification is now running; the aborted run
  will not be reported as a pass.
- Current best-guess completion: 42%.

## 2026-08-29T03:33:29Z — release-mutation isolation design checkpoint

- Static inspection confirms that the excluded packaging suite comprises 32
  hostile cases plus ten deterministic/coverage controls.  It needs a live Git
  checkout, temporary fixture repositories, and the ignored `release/work`
  tree; it does not need network access or writes to tracked source bytes.
- The intended replay commit is
  `5a6d64cb2a76e890d7baaef3ba5ac9861c1d029f`.  A sparse shared clone reached
  that exact detached clean state, but it was rejected as an execution
  boundary because its Git alternate would expose unrelated monorepo objects
  to reviewed code.
- A referee-owned builder and supervisor now specify a self-contained exact
  partial checkout containing only the target commit/root/project objects,
  with no Git alternate and no usable remote.  A separate default-deny profile
  allows writes only to its fixture temp area and ignored `release/work`;
  source Git state, the active package replay, the pinned environment, and the
  external transcript/summary remain unwritable.
- No release-engineering package code has been executed at this checkpoint.
  Checkout construction and the short mutation replay will wait until the
  active full four-port verifier releases the CPU, avoiding interference with
  theorem replay.
- Current best-guess completion: 47%.

## 2026-08-29 — Coherent premise-substitution checkpoint

- In a separate disposable copy, replaced the legacy
  `CUT_GLOBAL_LOGIC_REPORT.json` by a deliberately proof-free and internally
  contradictory fixture that preserved only the three values inspected by the
  downstream transfer scripts.  The fixture changed the schema and verdict,
  removed the containment identity and genuine source/target metadata, set
  `proof` to null, and emptied the provenance hash map.
- `build_global_transfer.py` nevertheless regenerated a `PASS` certificate
  coherently bound to the substituted fixture's SHA-256
  `f82a8f610a73a878896d471dfc2f6928b4d03e1afd1b3b2cb5aa05e34e959ca0`;
  `verify_global_transfer.py --no-write-report` then returned `PASS` on that
  regenerated certificate.  The accepted certificate retained the stale
  “isotropic-JC generic recovery” rationale.
- This directly verifies that these two semantic consumers do not validate the
  premise's schema, verdict, proof, blocked status, or provenance.  Fixed hashes
  in outer adversarial/release/manifest layers still reject an unresealed byte
  substitution; this bounded test did not attempt a full downstream reseal.
- Frozen commands, fixture, transcript, accepted certificate, hashes, and the
  precise logical boundary are in
  `results/coherent_premise_substitution/`.  The run used `env -i`, no network,
  disabled bytecode writes, and wrote neither to `package_copy` nor its active
  `review_runs` session.
- Current best-guess completion of this bounded substitution test: 100%.

## 2026-08-29 — Corrected sandboxed substitution checkpoint

- The preceding `env -i` execution is now explicitly uncredited because it did
  not enforce a network or filesystem sandbox.  Its commands and transcript
  remain only as superseded debugging history.
- Repeated the complete baseline/substitution experiment in a new disposable
  tree under a frozen macOS `sandbox-exec` profile whose first operative rule is
  `deny default`.  Every probe and package-script execution received exactly
  ten non-secret environment variables; network access, credential locations,
  sibling projects, the concurrent `package_copy/review_runs` tree, and writes
  outside the disposable tree were denied.
- Mandatory pre-execution negative tests all passed: TCP connect, existing
  `~/.ssh` listing, sibling `AGENTS.md` read, concurrent-review directory
  listing, and package-source write each failed with `EPERM`; the
  package-source read and disposable write positive controls succeeded.  The
  source-write marker remained absent.
- Under that enforced boundary, both baseline commands and both mutated
  commands again returned `PASS`.  The regenerated mutated certificate bound
  fixture SHA-256
  `f82a8f610a73a878896d471dfc2f6928b4d03e1afd1b3b2cb5aa05e34e959ca0`
  and had SHA-256
  `891faa25e45f5aa7f0c5ed1d19b9951ebbeb4cd89c20d89f66950c196c9325`.
- Credited commands, transcript, sandbox profile, boundary probe, and accepted
  certificate are frozen under `results/coherent_premise_substitution/`.
  Relevant package-source mtimes and sizes remained unchanged, and the active
  verification session continued in its separate `package_copy/review_runs`
  workspace.  The disposable replay tree was deleted after evidence freezing.
- Current best-guess completion of the corrected bounded test: 100%.
