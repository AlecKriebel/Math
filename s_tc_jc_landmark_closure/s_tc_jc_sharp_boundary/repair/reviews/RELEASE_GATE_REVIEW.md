# Adversarial release-gate review

**Date:** 2026-08-09  
**Audited checkout:** `1a245c9f8bc31509f5d58be8359d42503c920df4`  
**Scope:** release/source structure, reproducibility, PDF/source consistency, and prior-work scope only  
**Mathematical posture:** the global theorem is **not assumed** and is not re-audited here  
**Release verdict:** **BLOCKED**

The current tree is not submission-ready.  The authoritative repair status says
that the positive theorem is unresolved and withheld (`repair/STATUS.md:3-9`),
and every mathematical dependency gate remains open
(`repair/DEPENDENCY_GATES.md:5-13`).  Historical positive-theorem source,
editorial material, PDFs, certificates, and transcripts remain intermingled
with the active tree.  They must be preserved as audit history but excluded
from any repaired release.

This review does **not** conclude that the desired theorem is false.  It
concludes that the present source and release artifacts cannot support or
advertise it.

## 1. Ranked findings

### P0 — The manuscript still uses the invalidated bridge chart

The load-bearing source says that the complete bridge ambiguity is one scalar
per bridge (`source/paper/sections/04_bridges.tex:35-46`) and then removes only
that gauge to obtain an analytic product chart with independent bridge
directions (`source/paper/sections/04_bridges.tex:67-86`).  The global
localization and no-compensation argument explicitly invokes that chart
(`source/paper/sections/08_global.tex:35-61`), and the reconstruction promises
one recovered bridge multiplier per edge
(`source/paper/sections/09_genericity.tex:53-56`).

This is precisely the dependency now marked open as Gate B, with downstream
Gates G and P also open (`repair/DEPENDENCY_GATES.md:6,9,11`).  Therefore:

- the current manuscript source cannot be the source of a submission;
- the current manuscript PDF and all collateral asserting the theorem must be
  quarantined;
- no release verifier may infer global closure from the historical bridge
  certificate or synthesis status.

The submitted 48-page PDF visibly contains the same bridge claim on pages
11--12.  The PDF is source-consistent in the unhelpful sense that
`source/paper/main.pdf` and
`submission/Generic_Identifiability_STC_Level2_JC.pdf` are byte-identical
(SHA-256
`1e0548d69262bd56071ccbf16815c86b08c5fb343404654b8d1c3d76dff4920f`).

### P0 — The clean-clone release commands fail before verification

The independent sparse clean checkout passed only the initial clean-tree test.
The historical integrity verifier then failed exactly as follows:

- **missing:**
  `reproducibility/publication/certificates/theta_k6_weak_signatures.bin`,
  `submission/LaTeX_TikZ_Source.zip`, and
  `submission/STC_JC_Reproducibility.zip`;
- **unmanifested:** `repair/CANDIDATE_GLOBAL_REPAIR.md`,
  `repair/DEPENDENCY_GATES.md`, `repair/RESEARCH_LOG.md`, `repair/STATUS.md`,
  and `reproducibility/GIT_MIRROR_VERIFICATION.txt`;
- **hash mismatch:** `README.md`; the manifest expects
  `1aefb88d4a68929c34adf197bc5c652f2b74eb67c7f899d84eb4405007f276b1`,
  while the committed withdrawn notice hashes to
  `765d91b4b0173a0344b1dea38e3be8a5bdf860683c91e07aad197e048ae3c3d7`.

The three omitted large/generated files are nevertheless required at
`MANIFEST.sha256:110,167,169`.  The README explains why they are omitted at
`README.md:51-69`, but `reproducibility/verify_integrity.py:22-29` requires exact
equality between the physical inventory and the manifest.  The two policies
are incompatible.

Both advertised wrappers call this failing integrity check **before** they
build the missing archives (`reproducibility/verify_quick.sh:4-11` and
`reproducibility/verify_full.sh:8-23`).  Consequently neither command can
bootstrap a clean Git checkout.

The transcript claiming a 169-file integrity pass is not a clean-clone
certificate for the current tree.  It also expressly says that the PDF was not
rebuilt (`reproducibility/GIT_MIRROR_VERIFICATION.txt:1-8`) while later
advertising the positive global theorem and an all-checks-passed status
(`reproducibility/GIT_MIRROR_VERIFICATION.txt:79-89`).

### P0 — Release status contradicts active source and collateral

The README and repair ledger now fail closed (`README.md:1-24`), but the active
release tree still makes unconditional positive claims:

- manuscript informal theorem and novelty statement:
  `source/paper/sections/01_introduction.tex:7-15,53-58,63-69`;
- referee guide: `docs/REFEREE_GUIDE.tex:8-21`;
- cover letters: `docs/COVER_LETTER.tex:13-19` and corresponding JMB/BMB files;
- release scope: `RELEASE_METADATA.json:23-26`;
- positive final report/certificates under `reproducibility/exact_release/`;
- submission PDFs under `submission/`.

The review and archive scripts test for the old positive wording rather than
the authoritative repair status.  In particular,
`reproducibility/publication/review/review_submission_package.py:53-68`
requires selected positive phrases but never checks that all repair gates are
`VERIFIED`.  A PASS from that script is therefore a packaging attestation, not
a theorem or status attestation.

### P1 — There is no safe canonical build target

`reproducibility/build_paper.sh:30-43` builds in `source/paper/`, overwrites
`source/paper/main.pdf`, and then copies it into `submission/`.  The editorial
build writes directly into `submission/` (`build_paper.sh:12-28,45-48`).  Thus
source, cache, and release output are mixed.

The source-side and submission-side manuscript PDFs are currently identical.
The generic and JMB cover-letter PDFs are also byte-identical (SHA-256
`54bcbd2eb457df1e4a070b65029e4ec25927bcbf26646b6b0bde9564d39e4c79`).
This is not a content error, but it confirms that duplicated generated bytes,
not one canonical distribution directory, are being maintained.

`reproducibility/build_component_archives.py:29-54` then assembles archives
from those mixed trees and includes historical positive release metadata and
transcripts.  Until status and theorem gates close, this can only reproduce a
withdrawn bundle.

### P1 — The declared build environment is incomplete

In the current shell, `latexmk`, `biber`, and `pdffonts` are unavailable.  A
direct isolated paper build stops at `reproducibility/build_paper.sh:32` with
`latexmk: command not found`.  The declared Conda environment
pins Python, the algebra packages, compilers, `latexmk`, and `biber`
(`reproducibility/environment.yml:1-12`) but omits Poppler, even though the
build requires `pdfinfo` and `pdffonts`
(`reproducibility/build_paper.sh:20-27,36-42`) and the independent PDF review
requires both (`reproducibility/publication/review/review_submission_package.py:10-18`).

The current shell also uses Python 3.14.6, while the declared environment pins
3.13.5.  That is not itself a mathematical defect, but a release transcript
must identify which environment produced each result.

### P1 — The bibliography and novelty comparison need a current-version pass

As of 2026-08-09:

1. The Englander et al. record is stale.  The bibliography says “Version
   posted December 23, 2025” (`source/paper/references.bib:29-32`), while the
   current bioRxiv record is v4, posted July 4, 2026:
   <https://www.biorxiv.org/content/10.1101/2025.04.18.649493v4>.
   All references to Theorem 3.2 and especially the version-specific
   Proposition 2.26 (`source/paper/sections/01_introduction.tex:5,28,53-54`)
   must be checked against explicitly named versions.  One bibliography key
   should not silently denote both an April 2025 proposition and a July 2026
   theorem numbering.

2. Sullivant, *Phylogenetic Network Models as Graphical Models*,
   arXiv:2507.23056, is absent from the bibliography:
   <https://arxiv.org/abs/2507.23056>.  Its local-modification,
   stacked-reticulation, and 2-blob phenomena are directly relevant to the
   claimed boundary and should be included in the scope comparison.

3. The existing current identifiers for Ardiyansyah
   (<https://arxiv.org/abs/2104.12479>), Brits et al.
   (<https://arxiv.org/abs/2607.12919>), Currie et al.
   (<https://arxiv.org/abs/2606.26673>), Cox--Gross--Martin
   (<https://link.springer.com/article/10.1007/s11538-025-01506-1>), and
   Holtgrefe et al.
   (<https://link.springer.com/article/10.1007/s12064-025-00453-8>) are present
   at `source/paper/references.bib:2-7,17-28,57-61`.  Their theorem numbers,
   conventions, and version dates still require a final literal cross-check
   after the repaired theorem statement is known.

4. The present novelty table says that the paper covers the entire class and
   proves triangle redirection is the only ambiguity
   (`source/paper/sections/01_introduction.tex:53-58,63-69`).  Those are
   downstream theorem claims, not safe prior-work statements while Gates B,
   A, S, G, and R are open.  Until closure, the defensible scope is limited to
   independently verified component results, especially the all-`n` Theta
   sharpness theorem in `W_TC \setminus S_TC` identified by
   `repair/STATUS.md:9`.

### P2 — PDF presentation is visually serviceable, but the PDFs are stale

Visual checks were made on manuscript pages 1, 10--12, 47--48, both referee
guide pages, and the generic cover letter.  No clipping, overlap, unreadable
figure, or obvious typesetting failure was observed in those samples.  The
manuscript is 48 US-Letter pages, the referee guide is two, and each cover is
one; all are PDF 1.7 and untagged.  Embedded-font status could not be replayed
because `pdffonts` is absent.

The clean appearance does not cure the content/status blockers.  In
particular, manuscript pages 11--12 visibly reproduce the stale bridge-gauge
argument.  No current submission PDF should be distributed.

## 2. Canonical build layout

Adopt exactly one source-of-truth/generated-output split.  The least disruptive
layout is:

```text
s_tc_jc_sharp_boundary/
  source/paper/                 # manuscript TeX/Bib/TikZ only; never PDFs
  docs/                         # editorial TeX and human review documents
  reproducibility/              # pinned environment, generators, verifiers
  repair/                       # authoritative status, gate ledger, reviews
  quarantine/v1.1.1-withdrawn/  # preserved historical positive bundle
  dist/                         # generated atomically; absent before a build
    manuscript.pdf
    cover_generic.pdf
    cover_jmb.pdf
    cover_bmb.pdf
    referee_guide.pdf
    LaTeX_TikZ_Source.zip
    STC_JC_Reproducibility.zip
    MANIFEST.sha256
```

Rules:

1. `source/paper/`, `docs/`, and `reproducibility/` are immutable inputs during
   a release build.
2. Compilation occurs in a temporary staging directory.  No auxiliary file or
   PDF is written under `source/` or `docs/`.
3. `dist/` is the only release output.  It is assembled only after all
   mathematical and prior-work gates pass, then atomically promoted.
4. The source archive contains source inputs, not generated PDFs.  The
   reproducibility archive contains live proof/replay inputs and certificates,
   not withdrawn transcripts presented as current evidence.
5. The final manifest is generated **last**, from the complete `dist/` bytes.
   A separate immutable-input manifest may be checked before building, but it
   must not list outputs that do not yet exist.
6. `submission/` is not a second build target.  Either remove that name from
   the repaired layout or make it a generated alias of `dist/`, never a second
   independently maintained copy.

The static TeX input graph currently passes: `source/paper/main.tex` closes
over 24 TeX files, and its referenced bibliography and figures exist.  The
layout defect is generated-output placement and status, not missing TeX source.

## 3. Quarantine set

Quarantine means “preserve for audit, exclude from every repaired release and
from every current theorem attestation.”  No file was moved by this review.

### Entire generated submission set

- `submission/Generic_Identifiability_STC_Level2_JC.pdf`
- `submission/Referee_Guide.pdf`
- `submission/Cover_Letter.pdf`
- `submission/Cover_Letter_JMB.pdf`
- `submission/Cover_Letter_BMB.pdf`
- any regenerated `submission/LaTeX_TikZ_Source.zip`
- any regenerated `submission/STC_JC_Reproducibility.zip`
- `source/paper/main.pdf`

### Positive synthesis artifacts

- `reproducibility/exact_release/report/FINAL_SHARP_BOUNDARY_THEOREM.md`
- `reproducibility/exact_release/report/FINAL_SHARP_BOUNDARY_THEOREM.pdf`
- `reproducibility/exact_release/certificates/final_theorem.json`
- `reproducibility/exact_release/certificates/final_theorem_output.txt`
- `reproducibility/exact_release/review/final_synthesis_review.json`
- `reproducibility/exact_release/review/final_synthesis_review_output.txt`
- `reproducibility/exact_release/verification_output.txt`
- `reproducibility/exact_release/full_adversarial_verification_output.txt`
- all “clean/full/author-ready” transcripts that attest the withdrawn global
  theorem rather than regenerate the repaired dependency graph

The local generators and certificates inside `reproducibility/exact_release/`
may eventually be salvaged one by one, but the directory must be treated as a
historical bundle until each item is bound to a verified repair gate.

### Historical release metadata and collateral

- `MANIFEST.sha256`
- `reproducibility/GIT_MIRROR_VERIFICATION.txt`
- `RELEASE_METADATA.json`
- current positive-title/scope `CITATION.cff`
- current cover-letter and referee-guide TeX sources
- prior-work/novelty and theorem-crosswalk documents insofar as they assert the
  withdrawn global theorem

The manuscript TeX itself is a repair input, not disposable history, but it is
release-excluded until the mathematical gates and its dependent sections have
been rewritten and independently reviewed.

## 4. Exact clean-clone release gates

The repaired project should have one top-level, fail-closed release command.
It must execute the following gates in order and stop at the first failure.

### G0 — exact committed checkout

- Create a sparse detached checkout of the exact commit.
- Require `git status --porcelain` to be empty.
- Record the commit, platform, compiler, Python, SymPy, NetworkX, TeX, Biber,
  and Poppler versions.

### G1 — authoritative status lock

- Require `repair/STATUS.md` and `repair/DEPENDENCY_GATES.md` to be committed.
- If any theorem dependency is not `VERIFIED`, permit research builds only and
  prohibit positive submission collateral.
- Reject any contradiction among README, manuscript, metadata, cover letters,
  referee guide, reports, and certificates.

### G2 — canonical source graph and immutable-input integrity

- Require exactly one manuscript entry point and one editorial source per
  output.
- Resolve every TeX input, bibliography, and figure.
- Reject generated files under `source/` or `docs/`.
- Verify an input-only manifest that does not name absent generated outputs.

### G3 — complete pinned environment

- Recreate the declared environment from scratch.
- Include and version-pin Poppler (`pdfinfo`, `pdffonts`, `pdftoppm`) in
  addition to Python 3.13.5, the algebra packages, C++17, `latexmk`, and Biber.
- Fail with a complete missing-tool list before running any verifier.

### G4 — mathematical dependency closure

- Require Gates D, B, A, S, G, and R to be independently `VERIFIED` before P
  can pass.
- Regenerate every load-bearing algebra/census result from primitive inputs.
- Run independent implementations and mutation tests; a hash of a historical
  transcript is not a mathematical replay.
- Treat every component certificate as scoped; no synthesis script may promote
  a component beyond its verified hypotheses.

### G5 — prior-work/version lock

- Fetch or vendor the exact cited versions and record their hashes/version
  identifiers.
- Recheck definitions and theorem numbers literally.
- Update Englander et al. to current v4 or use distinct versioned bibliography
  entries for claims taken from older versions.
- Add Sullivant arXiv:2507.23056 and reconcile the claimed novelty.
- Reject “first,” “entire class,” “only ambiguity,” and similar claims unless
  both the repaired theorem and exact comparison support them.

### G6 — two isolated deterministic builds

- Build manuscript and editorial PDFs twice in two fresh staging directories
  with a fixed `SOURCE_DATE_EPOCH` and locale/time zone.
- Compare corresponding SHA-256 hashes.
- Reject undefined references/citations, overfull boxes, missing fonts,
  unexpected page counts, or source-tree writes.

### G7 — PDF and source consistency

- Extract text and render representative pages, including every theorem page,
  dense table, figure, bibliography ending, cover, and referee-guide page.
- Check page geometry, embedded fonts, links, metadata, and accessibility
  policy.
- Verify that the sole manuscript PDF in `dist/` is the output of the audited
  source build.

### G8 — archive assembly and self-contained replay

- Build both ZIPs only after G0--G7 pass.
- Test CRCs and internal manifests.
- Extract each archive into a second empty temporary directory and rerun the
  promised quick and full commands using only extracted bytes.
- The command called “full” must regenerate the load-bearing inputs; otherwise
  rename it to an attestation check.

### G9 — final distribution manifest and status scan

- Generate `dist/MANIFEST.sha256` last.
- Verify it against the completed distribution.
- Re-scan every distributed text/PDF for scope, theorem status, version,
  filenames, commands, and hashes.

### G10 — no leakage or mutation

- Require the original checkout to remain unchanged.
- Require no build artifacts outside `dist/`.
- Require no quarantined historical positive artifact in the final archive.

The current read-only diagnostics are:

```bash
python3 repair/independent/release/audit_release_layout.py
bash repair/independent/release/run_clean_clone_gate.sh
```

The second command uses a sparse shared clone of the committed repository,
runs the historical commands only inside that clone, and removes only its
validated temporary directory.  On the audited checkout it deterministically
ends with:

```text
CLEAN-CLONE RELEASE GATE: BLOCKED (3 failed gate(s))
```

The three high-level failures are the independent layout/status/toolchain
audit, the historical manifest verifier, and the missing build toolchain.  The
isolated checkout itself is clean before and after the attempted gates.

## 5. What passes now

- **PASS:** the authoritative repair documents correctly withhold the theorem.
- **PASS:** a sparse detached checkout of the exact commit is clean.
- **PASS:** the static TeX/Bib/TikZ input graph is complete (24 TeX files).
- **PASS:** the source-side and submission-side manuscript PDFs agree byte for
  byte.
- **PASS:** sampled PDF pages are visually clean and expected page counts and
  page geometry are present.
- **PASS:** the core Ardiyansyah, Brits, Currie, Cox--Gross--Martin, and
  Holtgrefe records are present, subject to final version/theorem-number checks.
- **PASS:** the diagnostic clean-clone attempt leaves the checked-out source
  unchanged.

These are release-engineering passes only.  None promotes the unresolved
global theorem.

## 6. Release decision

**Do not submit or distribute the current manuscript, covers, referee guide,
or positive reproducibility bundle.**  First close the mathematical repair
gates; then rewrite the dependent manuscript/collateral; update the prior-work
comparison; migrate to the canonical source/staging/`dist` layout; and pass
G0--G10 from a clean checkout.

**Audit completion:** 100% for the requested release/source/prior-work review.
**Theorem completion:** unchanged—global positive theorem unresolved; all
dependency gates remain open.
