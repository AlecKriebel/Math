# PR210 verification: the odd outer focal-pedal area product

This package supports the accompanying source-specific proof/application note for
`5100033 / AMR-050-0033`, PR210 native head
`2180d64b648b81ac660a792f7823d0b715f9cf12`. The target is the invariant
`k605,a` in Reznik–Garcia–Koiller, arXiv:2004.12497v11, and `k606` in the
published 2021 edition. An earlier literal assertion occurs as `k604` in
arXiv v1, 26 April 2020, Table 5. These edition labels identify the same
primed outer-pedal product; they are not three independent conjectures.

## Precise claim and limits

Let the billiard ellipse have semiaxes `a>b>0` and original foci
`F±=(±sqrt(a²−b²),0)`. Its caustic is a strictly nested, nondegenerate confocal
ellipse: `alpha²=a²−lambda`, `beta²=b²−lambda`, `0<lambda<b²`.
For every odd least period `N>=3` and every admitted coprime star turning number
`1<=tau<N/2`, take the ordered billiard vertices `P_j`. Intersect the consecutive
tangents to the original ellipse to form the outer vertices
`V_j = tangent(P_j) ∩ tangent(P_(j+1))`. Project each **original** focus
orthogonally onto the **line** through `V_(j−1), V_j`, in this cyclic order.
If `B±` are the signed shoelace areas of the resulting straight-edge pedal
polygons, the theorem states that `B+ B−` is independent of phase.

The projections are onto the side lines, including their extensions. Self
intersections use algebraic signed area. The statement covers primitive stars;
that precise formulation is a mathematical reconstruction, not a claim that
the historical source explicitly specified every repetition convention.
An `r`-fold repeated traversal multiplies each signed area by `r` and their
product by `r²`. Odd repeated traversals and the circular limit have separately
justified direct extensions. Even primitive-period products vary in the negative
controls. Hyperbolic, collapsed, or boundary caustics are outside the theorem.
The outer-pedal construction differs from original-chord pedals and focal
inversion.

The universal deduction is supplied by the written proof and independent
analytic reconstructions. Finite symbolic algebra and rational-lattice checks
are checkable corroboration of specified steps. Arbitrary-precision mpmath
calculations are **uncertified numerical diagnostics**, without interval
enclosures. No amount of finite enumeration establishes the all-period theorem
by exhaustion. No formal proof-assistant verification or human peer review is
represented.

## Replay

Use Python 3.10 or newer with exactly `sympy==1.14.0` and `mpmath==1.3.0` from
`requirements.txt`. The exercised runtime is Python 3.14.6. The harness does not
install dependencies, contact the network, or require a repository checkout.
The archive/integrity check uses only the Python standard library.

From this folder:

```text
python -B run_verification.py --integrity-only
python -B run_verification.py --list
python -B run_verification.py
python -B run_verification.py --run root_projective
```

The default runs all ten current jobs. Any ID in the table below can be passed
to `--run`. `-O` and `-OO` disable scientific assertions and are refused. Wrong
scientific library versions are refused. A mismatch is an error requiring
investigation; tolerances and scientific comparison fields are never relaxed
automatically.

The harness validates the complete package manifest and nested provenance
before and after replay. It copies only required inputs into fresh temporary
directories, retaining all required relative layouts, and executes the
archived scientific programs without modifying their bytes. Output files are
written only to those temporary copies. Temporary directories are removed.
Use `--receipt /path/outside/this/folder/receipt.json` to keep a replay receipt;
writing receipts into the sealed folder is refused. A local `TMPDIR` may be set
if temporary files should be kept on a particular filesystem.

Every scientific JSON scalar, list entry, dictionary key and value is compared
exactly with the frozen result, preserving type and sequence order. JSON
whitespace is immaterial. The receipt separately records raw byte equality,
raw hashes and a canonical scientific JSON hash. The **only** excluded field
paths are these top-level metadata fields:

| Job | Exact exclusions | Reason |
|---|---|---|
| `source_domain` | `$.python` | Interpreter version text |
| `meromorphic_divisor` | `$.utc_start`, `$.utc_end`, `$.runtime`, `$.python` | Wall clocks and interpreter path/build text |
| `priority_author` | `$.utc` | Wall clock |
| `priority_classical` | `$.python` | Interpreter build/version text |

No fields are excluded in the other six jobs. Scientific library version
fields remain exact in every result. No elapsed error, numerical residual,
precision, scientific count, source hash, proof hash or program hash is
excluded. The replay receipt records the actual excluded metadata differences.

### External-source hash preflight in the meromorphic job

The preserved meromorphic checker hashes three primary PDFs before computing;
it does not parse them or use their contents in the mathematics. Those
third-party PDFs are deliberately excluded from this archive. Its default
portable replay therefore uses the explicit
`meromorphic_source_preflight.py` adapter. The scientific script remains
byte-for-byte unchanged. The adapter substitutes only `digest()` calls for the
three exact known PDF paths, using the frozen hashes in the source manifest.
The harness checks those values against root's source-reading receipt and the
frozen result before running. All other digest calls execute normally, and
all original mathematical functions and `main()` execute unchanged. The
receipt identifies this as **attested hash preflight**, gives all three values
and their substitution count, and makes no claim of fresh external PDF hashing.

Readers who possess the exact primary editions can run the full original
preflight, with no substitution:

```text
python -B run_verification.py --run meromorphic_divisor --primary-dir /path/to/primary-pdfs
```

That directory must contain `invariants_v11.pdf`, `invariants_final.pdf`, and
`stachel_published.pdf` matching `original_submission/source_manifest.json`.
The harness freshly hashes those files, copies them into the precise relative
mirror expected by the unchanged checker, and runs it directly. A missing or
incorrect PDF is a hard error. Neither mode downloads or redistributes PDFs.
Preparation exercised both the offline and genuine-PDF modes, using existing
local primary copies for the latter. The two mathematical payloads were
required to agree with the same frozen scientific JSON.

## Current jobs

| Job ID | Exact/finite evidence | Separate uncertified numerical diagnostics |
|---|---|---|
| `author` | 20,718 assertions; 4,141 primitive rotations | 15,076 comparisons at 90 digits; 82 odd families, 8 complex-pole cases, 8 even controls |
| `inherited` | 9,303 assertions; 1,104 primitive rotations | 4,941 comparisons at 85 digits; 27 real families and 27 complex-pole cases |
| `source_domain` | 5 symbolic zero identities; 236 finite lattice cases | 86 real rows/430 phases at 75 digits: 82 odd rows including two scaling controls, 4 even rows; 3 analytic cases |
| `physical_geometry` | Projection/circle and local-pole algebra; two genuine exact triangular phases | Cartesian reflection and physical closure bisection without Jacobi functions: 22 cases/194 phases at 170 digits, including 17 strict odd cases, 4 even controls, 1 circle extension |
| `meromorphic_divisor` | 11 symbolic checks including a wrong-residue mutant; 3,503 finite primitive cases, 354,690 pole-phase checks, 88 selected Bezout certificates | 11 real/complex families at 140 digits; 33 local-pole rows and period/sign mutants |
| `priority_author` | 84 exact Euclidean finite checks on two credited triangular phases | None |
| `priority_classical` | 15 zero identities; exact nonconfocal counterexample in two phases | 11 cases/55 phases at 70 digits, including even negative controls and the classical dn bridge |
| `root_exact_geometry` | 113 exact zero assertions, two genuine triangular phases; repetition, isometry and scaling controls | None |
| `root_exact_even` | 96 exact zero residuals; genuine N4 products16 and25, corrected source fixture | None |
| `root_projective` | 10 exact identities, including the corrected plus-focus polarity and a discriminating offset-ellipse example | None |

Counts overlap between programs and must not be added as independent theorems.
Some numerical errors use absolute/normalized scales involving `max(1,...)`;
a small absolute residual need not be a small relative error for a tiny value.
All frozen result rows are retained. Additional independent row checks cover
counts, status flags, modular certificates, declared error thresholds, genuine
outer geometry, and negative controls. Exact JSON equality then covers every
remaining scientific result field as well.

## Provenance and history

- `original_submission/` preserves **all 20** original native files, including
  nested `independent_review/`, with original bytes. `PROVENANCE.json` records
  their native blob identifiers, sizes and SHA-256 hashes from `INTAKE.json`.
  Pending-review/status wrappers and imported source descriptions are historical
  artifacts, not the current claim or publication status. They were not edited.
- `audits/` preserves all **49** authored payload files plus the **five** sealed
  family manifests for source/domain, physical geometry, meromorphic divisor,
  author updates, and classical/general priority approaches. Their original
  directory bases and earlier scoped conclusions remain historical context.
- `audit_receipts/` contains root's source/domain and mathematical acceptance,
  bounded priority acceptance, isolated replays, analytic reconstructions,
  source-reading provenance, presentation repairs and polarity erratum.
  Earlier “priority pending” or “preparation not cleared” receipts are
  chronological; `ROOT_PRIORITY_ACCEPTANCE.json` records the later decision.
- `scope_controls/` contains the three **current** root scripts and frozen results.
  `forensic_history/polarity_sign_intermediate_20261015/` contains the wrong
  polarity intermediate, its old result, progress ledger and historical status.
  That program is **never a current replay job**. The error used the homogeneous
  line vector with `+1` instead of `−1`; the corrected plus-focus bicentric
  center is `−c lambda/beta²`. The erratum records that this supplemental error
  did not alter the original universal proof.
- The original current author/review manifests have 17 matching payload rows.
  The older `MANIFEST_V1.json` has one deliberately superseded `SOURCES.md` hash,
  explained by `METADATA_CORRECTION.md`; it is preserved, reported explicitly,
  and not treated as a current hash failure or silently rewritten.
- `MANIFEST.json` binds every payload file in this folder except itself.
  `python -B integrity.py` verifies it. `seal_verification.py --seal` regenerates
  the seal after an intentional revision; sealing is not review or publication
  authorization. The `--candidate`/`--manifest` options support unsealed local
  preparation inventories outside the package; readers use the final default.

Historical source-ledger/retrieval utilities are preserved to explain provenance:
`audits/priority_author_updates_01/build_source_ledgers.py`,
`retrieve_selected_primaries.py`, and
`audits/priority_classical_general_01/fetch_primary_texts.py`.
They require excluded reading copies and/or network access and are
**not portable scientific replay targets**. Run the documented harness.
Absolute paths in archived reports/receipts are original locators; no such
workspace path is needed for the portable mathematical replay.

All third-party PDFs, extracted full texts, HTML/transport/API reading copies,
rendered pages, caches and private directories are excluded. Authored analyses,
selected source locators, source hashes and access receipts remain. Rechecking
the historical literature requires obtaining primary editions independently;
this archive reproduces the mathematical controls and preserves the recorded
evidence of reading, rather than redistributing the literature.

## Credits, access and research status

Classical auxiliary-circle geometry, canonical Jacobi parametrization,
meromorphic/divisor arguments and cyclic elliptic identities are credited in
the accompanying note and archived derivations. The priority bridges explicitly
compare the published Khare–Sukhatme generalized Landen identity (2004) and
Ferudun's related original focal-inverse result (2026). A geometric reduction
and a related printed theorem do not by themselves establish that the exact
outer-pedal target was previously printed with a proof.

The bounded priority audit found no verified prior exact general target proof;
**historical novelty and public-proof priority remain undetermined**. This is
not a first-proof claim, a claim that the world problem remains open, or a new
general elliptic-method claim. Access was incomplete for the final *Talented*
journal edition and Stachel's *A Triple of Projective Billiards* full PDF; selected primary
passages and finite inventories are not exhaustive literature coverage.
Videos without inspectable proof/transcript provide no absence evidence.

Extensive AI assistance was used for the proof audit, independent approach
families, replay and packaging. “Independent” describes distinct computational
and analytic AI approaches with frozen maps; it does not imply independent
human peer review. Root's acceptance at preparation was case completion **55%**,
with preprint preparation cleared and upload uncleared. This supporting-package
preparation is not either required sequential whole-manuscript adversarial
review, and it authorizes no publication. Final manuscript/metadata integration,
new sequential full-package reviews, corrections, final seals and native guards
remain root's responsibility.

Author: Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X.


## Current review01 revision and conventions

The current harness has ten jobs, including the new exact primitive-even control. The earlier embedded preparation/replay receipts describe the dated nine-job version; their frozen inputs and scientific hashes must not be relabelled as the revised ten-job result. Final current-package root replays and subsequent whole-manuscript reviews are recorded alongside the case, outside this ZIP, to avoid a self-referential approval archive.

`CURRENT_CONVENTIONS_AND_CORRECTIONS.md` explains the exact parity example, related primary-source fixture error, parameter notation and current versus historical interpretation bindings. In the sealed earlier bicentric bridge, section6's `K(m_N)` uses the complete-integral parameter convention: with the modulus convention of its section1 and the current manuscript, this is `K_N=K(sqrt(m_N))`. The `dn(x,m_N)` in that comparison also uses parameter syntax. The historical family document is preserved byte-for-byte.

The original polarity erratum still binds the then-current negative-center program/result. Their stale limits sentence was subsequently corrected under R3; `audit_receipts/ROOT_PROJECTIVE_PRESENTATION_RECONCILIATION.json` binds both preserved older files and the current pair. Only interpretation text changed; all ten symbolic identities and geometric fields are identical. Old receipts are historical, not silently rebound. The relocated old-sign status pointer now correctly resolves to `audit_receipts/ROOT_POLARITY_SIGN_CORRECTION.json`; its wrong-sign program/result bytes remain unchanged. No forensic program is in the current JOBS table.
