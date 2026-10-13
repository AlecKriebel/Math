# Full stress stratifications determine a labelled graph

Alec Kriebel, independent researcher; ORCID [0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X).

This research note proves that, for simple graphs on the same labelled vertex
set and positive ambient dimension, the complete connected coordinate-sign
stress partitions of the full Cartesian configuration space are equal exactly
when the edge sets are equal. Collisions are retained. Intrinsically, a pair is
an edge exactly when its collision diagonal is a union of whole strata.

This completely answers the **literal equality** interpretation of Problem 4
in Karpenkov (2018). Arbitrary ambient or abstract equivalence, generic-only
or collision-free comparisons, and pure-condition comparisons are different
questions. The paper gives nonisomorphic path/star graphs with ambient-linearly
equivalent full stratifications, demonstrating this scope boundary.

The collapsed-edge detector is credited to Panina; collinear stress-matroid
invariance and incidence normalization are established ingredients. No priority
is claimed for those ingredients. The supplement reports a bounded priority
search; absence of an exact competing theorem in inspected sources is not a
proof of originality.

AI tools were used extensively in solving, verifying, source auditing, and
preparing this package. It is an unrefereed preprint. The independent reviews
are AI adversarial reviews; no conventional human peer review is claimed.

## Contents and reproduction

- `research_note.pdf` and `research_note.tex`: the complete proof, comparison
  convention, boundary example, prior credit and disclosures.
- `SUPPLEMENT.md`: scope, sources, priority, review provenance and limitations.
- `checks/`: two unchanged PR diagnostics and a fresh independent exact checker.
- `expected/`: pinned outputs for all mathematical fields; environment identity
  is separately recorded rather than silently matched to a historical UID.
- `run_checks.py`: replays three checkers in normal, `-O` and `-OO` modes, then
  six actual source mutations in all three modes. All guards use explicit
  exceptions and survive optimization.
- `evidence/`: fresh receipts, input/source pins and independent review records.
- `PACKAGE_MANIFEST.json`: file sizes and SHA-256 hashes, excluding itself.

Use Python 3.10 or later, with no third-party packages:

```sh
python3 run_checks.py --output verification-receipt.json
```

The optional output is a full execution receipt. Without it the runner writes
only its concise result to stdout, with mutant files confined to a temporary
directory. The checks use exact rational arithmetic. They corroborate explicit
identities, kernels, sign support, selected boundary cases, and sensitivity to
defective formulas. They do not prove universal topology or connectedness;
those claims are justified in the written proof. They do not replay the
original historical UID1000 permission-control harness, certify a security
sandbox, supply a formal proof-assistant certificate, or decide source intent.

The TeX source uses standard article, AMS, geometry, lmodern, microtype and
hyperref packages; it can be compiled with a usual LaTeX engine or Tectonic.
The included PDF has been rendered and visually inspected.

The authored material in this package is made available under
[Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
External papers are cited and linked, not redistributed. Preserve citations
and disclosures when reusing the package.
