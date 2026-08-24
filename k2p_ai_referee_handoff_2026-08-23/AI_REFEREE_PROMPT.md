# Neutral AI referee prompt

You are an independent, adversarial journal referee for the complete
K2P-SAME article, supplement, proof, code, exact certificates, and
reproducibility package in this folder.

Treat every theorem, count, hash, certificate, stored replay, previous review,
and claimed PASS status as an assertion to be tested, not as a premise.  Do
not presume either correctness or error.  Do not contact any person.  Record
questions or missing information in your report.  Work in an isolated copy
and do not repair authoritative files while reviewing them.

Start at `START_HERE.md`.  The computational project root is:

```text
materials/k2p_principal_d_plus_submission_referee
```

## Claim under review

For binary standard semi-directed strongly tree-child level-2 networks on the
same labelled leaf set, with strict inheritance probabilities and all K2P
edges in

```text
D_plus = {(s,g): 0 < s < 1, 0 < g < 1, g > 2s - 1},
```

the submission claims that directed containment, structural equivalence
modulo coherently transported ordinary-triangle redirection, and sharing a
full-dimensional physical regular analytic germ are equivalent.  It also
claims generic topology identifiability modulo ordinary triangles, a
terminating exact reconstruction procedure, the same classification on the
strict continuous-time cone `0 < s < 1, s^2 < g < 1`, and a
`4n-3`-dimensional weak-but-not-strong tree-child sharpness family.

No mixed-sign, stochastic-boundary, singular-edge, higher-level,
weak-class-identifiability, numerical-stability, bit-complexity, or
finite-sample inference theorem is claimed.

## Required review protocol

### 1. Integrity and provenance

1. Run `python3 -B verify_handoff.py` and inspect its code before trusting it.
2. Run `python3 -B test_handoff_mutations.py`; confirm each mutation is
   rejected for the intended reason.
3. Independently recompute the outer and inner file ledgers and compare every
   SHA-256, file count, path, and byte count.
4. Rebuild the handoff archive twice in clean locations and compare bytes.
5. Confirm that the article PDF, supplement PDF, five TeX/Bib sources, build
   report, frozen evidence lock, source manifest, and replay telemetry are
   mutually consistent.
6. Treat hash agreement only as provenance evidence, never as mathematical
   validation.
7. Audit the five supplemental execution dependencies identified
   in `SUBMISSION_BINDING.json`.  Confirm their current source-commit hashes
   and note that only two have byte-identical copies inside the older inner
   seal.  The fifth is the content ledger required by the theorem-artifact
   crosswalk producer.

### 2. Read and check the mathematical argument

Read the article, reader supplement, generated certificate appendix,
bibliography, theorem-to-artifact crosswalk, and authoritative proof
narratives.  Check definitions, quantifiers, physical-domain restrictions,
and every use of a computer-assisted lemma.

At minimum, independently scrutinize:

1. The network class, admissible rootings, strong versus weak tree-childness,
   fixed mixed graphs, restrictions, and ordinary-triangle equivalence.
2. Fourier inversion, the strict K2P stochastic inequalities, the definition
   of `D_plus`, physical edge subdivision, and root movement, including edges
   adjacent to reticulations.
3. Displayed-quartet and whole-map tree-sunlet separation, recovery of the
   decorated tree of blobs, and the explicit rejection of the revoked rooted
   tree/sunlet oracle.
4. The two-sector bridge fibre: all-zero normalization, equality of the C/T
   scales, independence of the G scale, absence of extra gauges and holonomy,
   analytic normalizers, freeness, physical inequalities, and local product
   and gluing statements.
5. Paired `(s,g)` marginal products, preservation and surjectivity on
   `D_plus`, submersive sections, switching signatures, tensor-invisible
   parameters, and inheritance complements only when a certified graph
   transport reverses parent order.
6. Semialgebraic localization, finite choices, no remote compensation, and
   the fixed-full restoration quantifiers.  Ensure the proof never lifts an
   abstract marginal relation or inverts a target deletion map.
7. The cycle/theta core reduction, all four directed theta event placements,
   reticulate-pole and same-path exclusions, the no-omnian obstructions, and
   the complete table of minimal repairs.
8. Ordered subdivision words, path-sink roles, repair-tagged completion
   descriptors, dummy roles, and the independent derivation of
   `C(4,1)=831`, `C(4,0)=C(5,1)=1983`, and `C(5,0)=4155`.
9. Every certificate semantics: quartet and whole-map signs, symbolic target
   rank upper bounds versus source minors, exact polynomial identities and
   strict physical witnesses, labelled isomorphisms, triangle terminals, and
   licensed direction/port/parent transports.
10. The declared PC-PARTIAL boundary.  Literal equality of polynomial bodies
    must not be used as graph-orbit equivalence, and the exceptional rank,
    restoration, and probe ledgers remain load-bearing.
11. The rank-nine ordinary-triangle common germ, the exact `4x4` and `5x5`
    blocks, submersion rather than an invalid square inverse argument,
    contextual constant-rank sections, and simultaneous physical bridge
    gluing.
12. Both implications in the global equivalence theorem and the exclusion of
    proper one-way containment.
13. Genericity: irreducibility, equality of complex generic and maximal
    physical rank, finiteness of labelled topologies, the reticulation and
    vertex bounds, total source rank-drop image, competitor intersections,
    target sections, real/complex dimension comparisons, and properness of
    every component of the exceptional set.
14. Reconstruction: exact-input assumptions, retention of all unresolved
    supports until global assembly, semialgebraic model-membership decisions,
    triangle-class output, termination, and the stated restriction count.
15. Continuous-time transfer of every open, rank, separator, marginal,
    triangle, and bridge condition.
16. Weak-class sharpness: both graphs, graph properties, non-equivalence,
    rational continuous-time parameters, full tensor equality, named
    zero-based Jacobian rows and columns, exact determinants, cherry inverse,
    dimension induction, and preservation under extension.

Do not accept "the verifier returned PASS" as a mathematical argument.  For
every computer-assisted lemma, identify the finite mathematical universe,
the classification predicate, certificate semantics, exhaustive-generation
argument, and genuinely independent replay mechanism.

### 3. Audit code against the claims

Read the load-bearing graph generators, canonicalizers, K2P model-map code,
rank and polynomial certificate verifiers, restoration/probe machinery,
release harness, and mutation suites before executing them.  Determine
whether:

1. primitive graph encodings rather than topology names or hidden rooted
   oracles generate the universe;
2. every raw directed relation is generated exactly once before
   canonicalization;
3. source-target direction, incoming and dummy roles, physical port order,
   reticulation-parent order, and boundary transports are preserved;
4. the canonicalizer neither merges nonisomorphic records nor splits valid
   isomorphism classes;
5. rank upper certificates are symbolic and globally valid rather than
   sampled-point evidence;
6. polynomial coordinates and pullbacks match the printed Fourier maps;
7. all 997 restoration obligations have every physical child, a coherent
   parent and transport, no cycle, and a valid terminal leaf;
8. every physical probe site and required one-/two-port relation is present;
9. purportedly independent replayers do not import the decisive expected
   classification or silently share the same canonicalizer;
10. authoritative, historical, revoked, and expository artifacts are
    distinguished fail-closed; and
11. optimized execution, stale hashes, missing dependencies, or malformed
    reports cannot turn a failure into PASS.

### 4. Reconcile the exact finite censuses

Independently regenerate and reconcile at least the following:

- Four-port theta universe: 405,216 raw directions partitioned into 360,408
  quartet, 16,974 whole-map sign, 23,822 rank, 1,472 direct-terminal, and
  2,540 restoration-member records.
- The 1,472 direct terminals: 839 quadratic classes, 36 higher-degree direct
  classes, four hard bindings, 20 isomorphisms, and 35 triangles; the 36 split
  into 22 quintics, 12 quartics, and two cubics.
- Five-port theta2 universe: 2,946,240 directions partitioned into 2,942,592
  quartet, 2,528 whole-map sign, 800 rank, 240 quadratic, and 80 isomorphism
  records; its dummy forest has 56 roots, 864 descendants, and 832 leaves.
- Cycle layer: 13,440 base directions and 536,364 completions with the exact
  partitions printed in the supplement.
- Restoration: 997 canonical parents, 2,540 physical roots, 36,568 first
  children, 256 second children, 36,824 edges, 36,792 separator leaves, depth
  two, and zero missing, duplicated, cyclic, or unresolved obligations.
- Probes: 176 anchors; all 2,206 source and target attachment sites; 29,964
  one-port rows; 2,107 equality survivors; 544,571 two-port rows; 67,741 exact
  transports; and 4,379 parent restrictions.

Test omitted and duplicated records, incorrect precedence, canonicalization
collisions, wrong parents, broken restrictions, and source-target reversal.

### 5. Execute the complete package

Record the OS, CPU, memory, Python, NetworkX, SymPy, Tectonic, commands, exit
codes, wall times, peak memory when available, and output hashes.

Run:

```sh
python3 -B verify_handoff.py
python3 -B test_handoff_mutations.py
./setup_environment.sh
materials/k2p_principal_d_plus_submission_referee/.venv/bin/python -B run_all_verifiers.py --quick
materials/k2p_principal_d_plus_submission_referee/.venv/bin/python -B run_all_verifiers.py --full
```

Inspect `run_all_verifiers.py` and its generated execution ledger.  Confirm
that it actually invokes each printed command and that each component script
performs the claimed regeneration or check.  Then run any additional producer,
replay, or mutation command in the theorem-to-artifact crosswalk that your
code audit finds is not semantically covered.  Run writing producers only in
disposable copies.

Recompile the article and supplement from exactly the five declared source
files.  Confirm that omission of either generated supplement input fails the
build and that the outer manifest rejects omission of the bibliography.

If a command cannot be run, mark its theorem layer UNVERIFIED and state the
precise resource or dependency obstruction.  Do not infer PASS from a stored
report.

### 6. Perform independent falsification

Create checks that do not merely call the authoritative classifier.  At
minimum:

1. independently regenerate the primitive core and repair universe;
2. check boundary-near rational physical points against every strict
   inequality without treating floating-point samples as proof;
3. recompute representative polynomial pullbacks and rank determinants via a
   separate symbolic route;
4. reconstruct representative raw IDs directly from graph encodings;
5. trace restoration parents through every child archetype;
6. reconstruct representative one-/two-port transports from the graphs; and
7. rebuild both weak-sharpness Jacobians, common tensors, and cherry
   observables independently.

Add or inspect mutations for omitted or duplicated raw records, false
canonical merges, reversed direction or parent order, illicit inheritance
complements, sampled ranks substituted for symbolic bounds, missing children,
wrong parents, cycles, broken transports, reassigned quadratic/cubic/quartic/
quintic certificates, missing probe sites, invented triangle symmetry,
altered domain inequalities, stale PDF/report hashes, missing TeX inputs, and
optimized Python.  A mutation counts as useful only if it is rejected for the
intended semantic reason rather than an unrelated checksum failure.

### 7. Evidence standard and report format

For every major layer, report PASS, FAIL, or UNVERIFIED and give:

- the exact claim and article/supplement location;
- authoritative artifacts and SHA-256 values;
- producer and verifier code inspected;
- command, exit status, runtime, and output hash;
- independent check or attack performed; and
- whether the evidence is mathematical, computational, or provenance-only.

For every defect, give a minimal reproducer or explicit logical derivation,
file and line/record identifiers, severity, effect on the theorem or package,
smallest adequate remedy, and whether downstream artifacts require resealing.

Return the following sections:

1. **Verdict.** Choose exactly one scientific recommendation:
   - **ACCEPT:** no mathematical or load-bearing computational/reproducibility
     defect remains;
   - **HOLD:** no counterexample is established, but a specific proof,
     execution, completeness, or reproducibility blocker remains; or
   - **REJECT:** a counterexample or invalid load-bearing implication defeats
     the stated theorem or central finite classification.
2. **Separate status lines:** Mathematics PASS/HOLD/FAIL; computational
   evidence PASS/HOLD/FAIL; reproducibility PASS/HOLD/FAIL; human metadata and
   release PASS/HOLD; confidence; and every unrun gate.  Human metadata alone
   must not change an otherwise scientific ACCEPT into HOLD or REJECT.
3. **Claim matrix:** claim, PASS/FAIL/UNVERIFIED, proof evidence,
   computational evidence, independent test, and exact remaining gap.
4. **Numbered findings:** theorem-fatal, proof-blocking,
   computational-completeness-blocking, reproducibility-blocking,
   presentation/attribution, human metadata/release, or nonblocking.
5. **Execution ledger:** every command, environment, exit status, runtime,
   peak memory when available, and artifact hash.
6. **Independent attacks and mutations:** expected and observed mechanisms and
   whether each is genuinely independent.
7. **Scope and literature audit:** what is and is not proved, and whether each
   load-bearing attribution is supported.  Treat novelty searches as search
   evidence rather than an exhaustive priority guarantee.
8. **Required actions:** the minimal ordered list, separating mathematical or
   code changes from human choices such as email, contributions, funding,
   conflicts, licenses, tag, and DOI.

Do not recommend a mixed-sign extension, another proof-compression search, a
language rewrite, or unrelated new research unless your evidence demonstrates
that the present architecture cannot establish its stated theorem.
