# Problem 30006308: toric deformation spaces

**Outcome: unresolved after five substantive approaches.** No full solution,
new toric counterexample, publication priority, or general current-open-status
certification is claimed.

The original item combines Questions 4 and 5 on p. 914 of [Oberwolfach Report
19/2025](https://ems.press/content/serial-article-files/51856). The first concerns
recovery of a deformation hull from its tangent cone. The second asks for a
relation between component counts and first-order simplicial-complex counts.

Useful results:

- Two published smooth projective toric threefolds give an explicit failure of
  numerical component determination from four natural first-order-complex counts,
  even with the same tangent dimension seven. Their hulls have one and two
  components. This consequence uses Ilten–Robins's existing examples.
- A proved equal-weight sufficient criterion and an exact countermodel show why
  torus equivariance plus integrability of each weight direction is insufficient
  by itself. The countermodel is not known here to be a toric deformation hull.
- A genuine nine-parameter toric candidate is reduced to an explicitly uncomputed
  residual formal series after removing its nondegenerate quadratic pair.

Read `PROOF.md` for all claims and limits, `SOURCE_GATE.md` for provenance and
status checks, and `ATTEMPT_LOG.md` for the five approaches.

Reproduce the exact checks with Python 3 and SymPy (tested 1.14.0):

```
python verify.py > /tmp/toric-verification.json
python -m json.tool /tmp/toric-verification.json
```

The script checks smooth cone determinants, complete bounded degree supports,
first-order complex counts, quadratic cycle coefficients, and coordinate-change
identities. It does not calculate the missing residual series or prove the
universal statement. `verification_results.json` records an actual successful
run. `FROZEN_MANIFEST.json` hashes the public files frozen for review.

Only original analysis and small verification code belong in this directory.
Primary-source PDFs, extracted texts, catalogue records, and the full dataset are
excluded from the publication payload.
