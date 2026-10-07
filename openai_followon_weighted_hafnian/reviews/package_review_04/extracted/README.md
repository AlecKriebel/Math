# Binary rational hafnians: an exact reduction and approximation and sampling consequences

Alec Kriebel — ORCID https://orcid.org/0009-0001-9320-500X . Research note, October 6, 2026.

The exact construction maps a nonnegative rational symmetric matrix A of order 2m to a simple unweighted graph H with #PM(H)=D^m haf(A). A weight W uses 4 bits(W)-2 gadget vertices and has terminal signature (W,1,0,0); total graph size is polynomial in binary input length. Zero support is decided exactly and the empty hafnian is one.

**Approximation consequence.** Citing OpenAI's family-113 general-graph FPRAS, the reduction supplies a uniform rational hafnian FPRAS with every-execution bit time polynomial in full input length, epsilon inverse, and log delta inverse. Its positive-input estimate is made positive on every tape using exact feasibility plus a harmless failed-zero replacement.

**Sampling consequence.** For expanded order N=2s and TV tolerance eta, the wrapper uses at most s² counting calls (relative error eta/(4s), failure eta/(4s²)), at most s²+1 witness calls, and s ceil(log2(4s²/eta)) additional draw bits. Its unconditional TV error is below 5 eta/6 < eta. Every output is feasible, even if estimates fail. Projection gives the rational weighted law; total time is polynomial in input length and eta inverse.

These are consequences of the cited unweighted theorem, not a new approximation breakthrough. Binary rational weight removal was already proved by McQuillan (2013); logarithmic integer path gadgets by Dell–Husfeldt–Wahlén (2010); counting self-reduction is classical. Our contribution is explicit exposition, a Horner variant with exact signature and bit bounds, a specified finite-bit wrapper, boundary handling, and finite reproducibility checks. No first-publication or novel complexity-classification claim is made. The dated priority audit records exact primary sources and search limits.

The upstream manuscript audit found no substantive mathematical gap. The actual Lean statement and 415-module source closure were inspected, but no compatible dependency build/kernel recheck was reproduced; that remains unverified. The weighted follow-on theorem is not formalized. The external theorem is explicitly cited rather than asserted to have been independently solved.

## Contents

- `main.tex` / `paper.pdf`: standalone six-page note with an inline bibliography.
- `proofs/`: full independent gadget and sampling derivations.
- `code/gadget.py`: exact graph construction and exponential reference counters.
- `code/sampling.py`: sampler requiring supplied counting and witness algorithms; exact helpers are test-only.
- `code/test_*.py`: deterministic exact finite checks, including integrated finite-bit output laws.
- `code/upstream_cell_checks.py`: independent finite falsification check of upstream label-cell and repair assertions.
- `data/`: saved test outputs, supporting finite evidence only.
- `research/`: dependency, formal-scope, and priority audit reports, plus the authored optional source inspector and original static inspection receipt.
- `DEPENDENCY_REFERENCES.json`: pinned external source identities and hashes.
- `reproduce.py` and `PAYLOAD_SHA256.json`: clean-copy reproduction and integrity verification.

No practical implementation or benchmark of the upstream FPRAS is included. Exponential enumeration does not certify the polynomial approximation algorithm. Nonnegative rational entries only; no signed/complex hafnian or unrestricted Gaussian-boson-sampling claim.

## Reproduction

Extract the source-and-verification ZIP into a fresh directory. Python 3.10 or later and the standard library suffice for all mathematical finite checks:

```
python3 reproduce.py --output reproduction-receipt.json
```

The script verifies every declared package hash before working, copies only those verified payload bytes and the manifest into a temporary directory, and runs all three exact checks there. It accepts the documented receipt path inside the extraction, excludes unlisted files from its copy, and rejects receipt paths that collide with a payload file or the manifest (including symlink/hardlink aliases). Tests overwrite only that temporary copy's data. It records Python version, return codes, output hashes and exact reports. The release was tested with Python 3.14.6. For an optional fresh PDF build, use an existing LaTeX compiler; Tectonic 0.16.9 was used to export the deposited PDF:

```
tectonic --outdir rebuilt main.tex
```

Create `rebuilt` first. PDF metadata timestamps may differ; compare extracted mathematical text and inspect rendering rather than expecting byte equality. The source was also compiled successfully in Codex's built-in editor. No toolchain installation is required for the standard-library checks.

The theorem-state document is a dated prepublication assembly snapshot. Complete-package reviews and subsequent publication/tracker receipts are maintained separately in the [project repository](https://github.com/AlecKriebel/Math/tree/main/openai_followon_weighted_hafnian), outside the frozen archive.

For optional static source inspection, obtain the exact pinned upstream Git repository and run `python3 research/lean_source_inspection/audit_sources.py --source /path/to/math/lean` in a fresh extracted copy. Supply `--lean /path/to/the/pinned/lean` for a dependency-availability probe. It writes copied sources and a new report only beside itself; it is not a full kernel build or one of the three finite checks. The saved original inspection receipt is included separately.

For a future upstream Lean kernel verification, obtain the exact pinned OpenAI repository and dependencies and follow its comparator instructions. The formal-scope audit records the actual theorem, configuration, missing-build evidence, and exact remaining verification step. Our source inspection is not a kernel certificate.

AI tools were used extensively in research, drafting and verification. At publication the preprint has not undergone conventional human peer review or refereeing. Automated adversarial reviews are evidence, not human peer review. Newly authored prose/data use CC BY 4.0; code uses MIT; see the license files.
