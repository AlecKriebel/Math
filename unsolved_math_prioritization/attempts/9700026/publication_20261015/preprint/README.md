# Quantitative persistence in a fixed-city area equation

Alec Kriebel · ORCID [0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X) · version 1.0.0 · 15 October 2026.

The five-page research note proves quantitative all-coordinate persistence for the hard weighted-Voronoi area ODE, for every fixed finite collection of at least two distinct interior sites in the unit square and every strictly positive initial probability vector, when beta > 2 alpha. An asymmetric alpha=2, beta=8 three-city instance has every share in [1/4096,2047/2048] for all nonnegative time. This disproves the literal unrestricted alpha > 1 collapse clause in Aldous's 2007 Conjecture 32(a), and the exact catalog conjunction containing it.

Read `note.pdf` for the theorem and proof, `note.tex` for its editable source, and `CURRENT_PRIORITY.md` for exact credit and scope. This does not prove convergence, equilibrium uniqueness, initial-value independence of a limit, or stochastic founding conclusions. Zero initial weights, coincident sites, boundary sites, and n=1 are excluded from the stated theorem. Restricted/critical collapse questions are outside this proof; related counterexamples already exist and are credited.

The model, area exponent and protected-neighborhood mechanism have antecedents in Aldous's notes. Weighted Voronoi/Apollonius geometry and scalar comparison are standard. Ferudun's 14 October 2026 unrefereed paper explicitly discusses Conjecture 32(a); its proved lemmas imply a qualitative two-city counterexample even in this parameter region. The present all-site/all-positive-start quantitative theorem is stronger than that local-basin conclusion within the sources inspected. The original complete PR 880 was recorded 6 October 2026, but neither chronology nor the bounded searches certify firstness or worldwide novelty. Historical negative-search statements in the original freeze remain unchanged as historical records; the current priority note supersedes them for present claims.

OpenAI tools were used extensively in solving, proof development, writing, coding, reproduction and adversarial checking. This preprint is unrefereed; completed external human peer review and formal proof-assistant verification are not claimed. The author is responsible for all claims.

## Contents and assurance boundary

The portable archive includes the current manuscript/PDF, current metadata and priority note, all 40 original frozen files in `source/`, independent analytical/priority audit evidence, primary version/hash locators, and standard-library verification tools. Both original archives, their nested author archive and readable duplicate files are preserved and authenticated. Original labels and receipts are historical objects, not newly certified verdicts or execution events.

The complete portable inventory is `package_index.json`, excluding itself. Its digest must come from a separately trusted publication record. It binds every regular file, including the verifier and checker. No primary publication PDF, source extract, page image, raw corpus/record dump, credential or private correspondence is part of this package.

The verifiers establish byte identities, exact closed inventories, archive consistency and finite diagnostic reproduction. They do not establish an analytic theorem, source interpretation, literature priority or human review. The written proof supplies the continuum geometry and all-time comparison. Exact rational checks support the displayed constants; finite samples and trajectory simulations are not proofs of persistence.

## Trust startup before running a script

Independently authenticate the interpreter, standard library, script bytes and expected index/manifest digest before execution. A script that hashes its own indexed copy after startup cannot establish its own initial trust. Obtain the expected pins from an independently trusted repository/publication seal, not by recomputing them from a possibly replaced package. The outer repository's current publication record provides those separately anchored pins. The included metadata does not bootstrap its own trust.

After independently authenticating the startup bytes, these are the interfaces (replace uppercase arguments with independently supplied values):

```text
python3 -I -S -B verify_package.py EXPECTED_INDEX_SHA256 --root .
python3 -I -S -B verify_package.py EXPECTED_INDEX_SHA256 --root . --full
python3 -I -S -B check_originals.py --root . --verify-only
```

Python 3.10 or newer and the standard library suffice. Add `-O` to test optimized execution. The checks use explicit failure guards, not optimization-sensitive assertions. The root may be in a path with spaces; quote paths in a shell. Run from any working directory with an explicit package root and script path.

The first command authenticates the complete closed inventory. `--full` additionally authenticates all 40 frozen source files, Git blob identifiers, original JSON/archives/manifests/duplicates, then replays the original author witness and self-test plus the independent audit witness and self-test under normal and optimized isolated Python in a fresh relocated directory. It matches complete expected output bytes. The historical root wrapper is authenticated as data and never executed by the current tools. The default replay has eight finite diagnostic receipts; it is not a replay of every historical audit execution. `--verify-only` runs no child diagnostics.

The old wrapper had permissive JSON/inventory/ZIP helpers and lacked pre-execution startup authentication. Those historical limitations are documented in the new artifact audit and are not hidden by rehashing a replacement. Current tools reject unsafe relative names, duplicate/nonfinite JSON (including overflowing numeric literals), malformed typed inventory rows, symlinks, FIFOs, special entries, and unexpected files or directories within the selected trees. They assume no concurrent adversary replaces authenticated files during use; this is not a hostile multiuser execution sandbox.

## Optional complete-input provenance

Source-free runs explicitly report provenance `NOT_RUN`. To request it, supply all four original input locations, plus an optional explicit 2012 PDF mapping when that file has another basename:

```text
python3 -I -S -B verify_package.py EXPECTED_INDEX_SHA256 --root . --full \
  --catalog /path/catalog.json --problems /path/problems.json \
  --reports /path/research_results.json --pdf-dir /path/primary-pdfs \
  --pdf-2012 /path/1209.5120v1.pdf
```

Without `--pdf-2012`, the PDF directory must contain `cities-2012.pdf`; it always needs `cities-notes.pdf`. The four source locations are all-or-none. Source arguments require `--full` in the package verifier. `check_originals.py` accepts the same source arguments directly; source authentication with `--verify-only` does not count as replay.

All three complete corpus files and both primary PDFs must match the literal byte sizes and SHA256 pins before a source child runs. Corpus JSON is parsed strictly. The unique exact target 9700026 / AMR-096-0026 complete record/report pair is 4409 bytes with SHA256 `7b18458d71482e2c4e1c62601be1824eba6ad6243c78135d90d1b75223e8e193`; both catalog bindings are checked. No shortened record is substituted. With sources, two additional normal/optimized finite source-checker receipts are expected. Hash agreement does not prove semantic interpretation of a source.

The trusted adapter uses authenticated read-only ordinary-file hardlinks with the old checker's required basenames; that inspected checker only reads them. It requires source files and the temporary replay directory on a filesystem supporting those links. Link failure rejects instead of silently copying large corpora. The tool never writes, truncates or chmods a source link; temporary links are removed on ordinary and exception exits. An uncatchable crash can leave disposable files. Complete corpus inputs are not redistributed; obtain them independently when available. Primary locators and fingerprints are recorded in the source/audit evidence.

## Rebuilding the archive

Authenticate the builder and verifier startup bytes and external index digest independently. From outside the input tree, run:

```text
python3 -I -S -B build_verification.py ASSEMBLY EXPECTED_INDEX_SHA256 \
  EXPECTED_VERIFIER_SHA256 FRESH_OUTPUT_DIRECTORY
```

The last argument is a fresh or empty directory outside the input assembly, not a ZIP filename. Output is exclusively created as `FRESH_OUTPUT_DIRECTORY/verification.zip`; existing output is never overwritten. The builder authenticates every input and runs a relocated full finite replay before creating the archive. It uses sorted names, fixed 15 October 2026 timestamps, ordinary 100644 ZIP entries and DEFLATE level 9. Identical compressed bytes are claimed only with identical inputs and the same Python ZIP implementation/zlib runtime, whose versions appear in the build receipt. Another runtime's valid compressed representation need not be byte-identical. Building does not execute the optional complete-source provenance path; request that separately.

## Evidence and publication

The current source/analytic families independently checked hard-max model fidelity, null ties, positive-global continuation, local Lipschitz regularity, every-competitor capture, scalar comparison, exact witness and genericity robustness. Distinct bounded priority families checked original/follow-up sources and structural transfer routes. Current artifact receipts reproduce their enumerated processes; the original claim of 106 rejection tests was not independently reconstructed as the same 106 cases and is not reasserted as fresh evidence. Every historical or new finite count has its own scope.

Canonical deposit metadata is `metadata.json`. The separate publication manifest binds the PDF and verification ZIP under `city-ode-persistence-note.pdf` and `city-ode-persistence-verification.zip` using exactly that metadata. The current repository record is [PR 880](https://github.com/AlecKriebel/Math/pull/880); the unchanged original source is anchored at commit `fba74a301786f9648e48722e76f440097b0746c2`. No journal submission or completed external human review is asserted.
