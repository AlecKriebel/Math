# A smooth Reshetnyak-harmonic sphere with unbounded distortion

Alec Kriebel, independent researcher. ORCID: https://orcid.org/0009-0001-9320-500X.
Version 1.0, 13 October 2026. AI-assisted, unrefereed research note.

The six-page paper gives a negative answer for the Reshetnyak member of the
general-energy harmonic-sphere question in the inspected OWR 30/2025, Question 1,
printed p. 1625, and Meier–Vikman–Wenger arXiv:2503.08553v1, Question 1.9. It constructs
a compact smooth Riemannian sphere and smooth sphere homeomorphism which
minimize operator-norm-squared energy on each sufficiently small neighborhood
against all same-trace Sobolev competitors, but have essentially unbounded
distortion. The map is not a global homotopy minimizer and is not KS-harmonic.
The paper also proves the separate complete-target KS theorem with the nonsharp
bound `4 + sqrt(17)`. The energy and minimization class are essential.

Source binding is to the authenticated 2025 arXiv v1 PDF and Oberwolfach report.
The revised 2026 journal body was inaccessible. Neither unchanged final wording,
continued open status through 2026, first bibliographic priority, nor optimal
constants are asserted. The bounded independent priority audit records 71
queries, 32 source entries, exact earlier hypothesis comparisons, inspected
primary passages, metadata-only citation leads, and access gaps.
`PRIORITY_ACCESS_ADDENDUM.md` records a later root inspection of the original
Sacks–Uhlenbeck text through the web PDF reader, with direct local download
still forbidden and no local byte hash claimed. Old sealed reviews retain
their actual earlier coverage; the addendum qualifies that one access gap.

The ZIP includes the authored PDF, LaTeX source, unchanged 30-file historical
candidate, fresh independent analytic/computational/source/priority reviews,
source metadata, and reproduction tools. It contains no copied third-party
PDFs, raw source text, screenshots, upstream dataset contents, credentials, or
private coordination files. The only payload below a `private_sources/` name
is a declared 14-byte ignore guard. Historical initial utility reviews are
retained explicitly under `history/initial_revision/`; active utilities repair
their portability and disabled-assertion weaknesses without changing the
analytic theorem or original control results.

## Reproduce from an extracted closed package

Use Python 3 with the pinned versions in `requirements.txt`. Create the virtual
environment **outside** the package; its directory must not become an extra
payload. Obtain the trusted SHA-256 of `PACKAGE_MANIFEST.json` from the public
prepublication/acceptance receipt in the PR's audit folder. An internally
self-consistent replacement is not authenticated merely by hashing itself.

```sh
python3 -m venv /tmp/harmonic-sphere-verify-env
/tmp/harmonic-sphere-verify-env/bin/python -m pip install -r /path/to/package/requirements.txt
/tmp/harmonic-sphere-verify-env/bin/python -I -B /path/to/package/verify_package.py --expected-manifest TRUSTED_PACKAGE_MANIFEST_SHA256
/tmp/harmonic-sphere-verify-env/bin/python -I -O -B /path/to/package/verify_package.py --expected-manifest TRUSTED_PACKAGE_MANIFEST_SHA256
```

`--integrity-only` (alias `--check-only`) needs only the Python standard library
and checks closed file/directory membership, byte counts, SHA-256, fixed original
proof pins, and all symlink/special-entry guards. Optional `--pdf /path/to/paper.pdf`
also checks the separately submitted PDF against the identical `note.pdf` in
the archive. Every full replay runs in disposable copies. An isolated worker
always runs active children without optimization, even when the outer wrapper
is optimized. It clears `PYTHONOPTIMIZE`, avoids bytecode writes, and leaves the
authenticated package unchanged.

The original public manifest is externally fixed at
`acab12ef33c8e2dc566337cfe01b94f2fe81f06ede4b31f1c363e055741fb0df` and the
original accepted PR head is `32eaecaa8907dbf674e65b138b000cdcc49004ae`.
The 30 historical files are preserved, including their historical prepublication
language. The public current acceptance/publication receipts supersede that
language; they are not substituted into or rehashed as the original candidate.
The original two substantive author approaches remain 2/5.

## What the checks establish

- The 257 exact author algebra controls replay byte-identically. Audit A uses
  mixed exact/symbolic and numerical controls: it reproduces within relative
  tolerance 1e-9 and absolute tolerance 1e-10, and need not be byte-identical on
  another runtime.
- The source-free audit B adapter executes 673 checks and omits two original
  PDF-input identity checks. The historical 675 count is not the source-free
  count. No source is retrieved by the replay.
- The wrapper also runs 67 historical integrity mutations, six fresh proof
  control families, the fresh KS angular/stress controls, 43 independent exact
  controls plus explicitly nonrigorous numerical diagnostics, and 19 additional
  integrity mutations. Full working precision is retained in the corrected
  cross-precision diagnostic; earlier rounded outputs are labeled historical.
- Active proof-family utilities separately passed 126 workspace/standalone
  receipts under normal, `-O`, and `-OO`, including nonregular-entry and tampering
  rejection. Those retained receipts describe that completed utility audit;
  the main replay does not pretend to rerun every historical receipt.

The new wrapper's numeric comparator excludes Boolean values from numeric
float comparisons. The unchanged historical helper has a looser boundary;
the independent review documents it. A newly supplied outer historical anchor
does not authenticate a changed envelope under the fixed original PR anchor.

Finite algebra and numerical controls supplement the universal written proofs.
They do not prove Sobolev product/gluing rules, global analytic stress arguments,
historical priority, or optimality. Numerical quadrature has diagnostic
tolerances, not rigorous interval error enclosures. No formal proof-assistant
certification is claimed.

Compile `note.tex` with a standalone LaTeX compiler such as Tectonic. The supplied
PDF is the reviewed output; another compiler may produce byte-different PDF
metadata while rendering the same document. Do not replace it in the closed
verification package without a new manifest and corresponding review.

AI tools were used extensively in development, verification, adversarial review,
and writing. Independent AI-assisted reviews are not independent human or
journal peer review; neither has occurred. Authored materials use CC BY 4.0.
Cited third-party documents retain their own rights and are not redistributed.
