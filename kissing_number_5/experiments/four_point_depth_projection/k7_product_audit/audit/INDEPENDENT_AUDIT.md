# Independent audit of the K7 product candidate

Audit timestamp: 2026-07-24T05:58Z.

## Verdict

`candidate_k7_product_extension.json`, SHA-256

```text
1b5e262592e1872cfe9f26b344d82da5066d8332efc5104a34a433d9d5564b00
```

is a genuine exact **local symmetric K7 distribution**, not merely a
floating-point discovery artifact.  It is not a global 41-point code, an
overlap-consistent family of all K7 subsets, a Lasserre certificate, or a
lift of the frozen 74-orbit K6 product distribution.

## Independent geometry and marginals

The script in this directory imports neither candidate verifier nor discovery
code.  It authenticates the candidate, source, pool, and frozen K6 files; checks
the 53 selected pool rows; and uses ordinary rational Gaussian elimination on
all

```text
53 * (2^7 - 1) = 6,731
```

principal submatrices.  Every principal minor is nonnegative, all minors of
orders six and seven vanish, and every atom has a positive fifth-order minor.
The minimum positive normalized fifth minor is \(3/512\).  Every atom is
therefore PSD of rank exactly five, and every off-diagonal entry is an exact
quarter-grid value at most \(1/2\).

The 53 exact weights are positive and sum to one.  Independent edge and
triangle reconstruction gives expected counts

\[
21\alpha/40,\qquad 35\nu/1560=7\nu/312.
\]

After uniform symmetrization, a fixed K7 edge and triangle consequently have
marginals \(\alpha/40\) and \(\nu/1560\).

## Product and deletion checks

For five of the 39 residual vertices, the exact inclusion probabilities are

\[
p_1=5/39,\qquad p_2=10/741.
\]

Applying these to
\(C+I\le MH+rG-rM\) gives, with no floating-point step,

\[
741c+78i\le78Mh+78rg-10rM.
\]

The direct verifier evaluates this row from explicit set memberships for both
orientations of every base-colored edge.  The separate face verifier deletes
each K7 vertex and evaluates the already established K6 row.  The abstract
identity

\[
\sum_{\text{seven K6 faces}}F_6=2F_7
\]

was checked for all 57,344 five-point membership patterns and again for all
\(53\cdot560=29,680\) atom/state pairs.  Both exact paths find all 560 current
direction/capacity rows nonnegative, with 65 zero state keys and minimum
strictly positive twice-symmetrized slack

\[
\frac{
621356053751757820879468470110075171035859371
}{
30090524476568270576550820092000000000000000
}.
\]

The 560-state catalog and seven capacity families are imported from the
separately hashed direction/capacity verifier; the present audit confirms the
candidate against that exact catalog, not against every future local
inequality someone might derive.

## Relation to the frozen K6 distribution

The K7 candidate induces a perfectly valid K6 face distribution, but not the
earlier 74-orbit one.  Canonicalizing all \(53\cdot7\) deleted faces gives 325
K6 orbit types.  Only two meet the frozen 74-orbit support.  Its exact induced
mass outside that support is

\[
\frac{
3936200435868713179173616576291348691773640557
}{
4107356591051568933699186942558000000000000000
}
\approx0.958329.
\]

This is consistent with the independently certified theorem that the frozen
74-orbit K6 distribution has no K7 lift.  The positive K7 result changes the
K6 marginal; it does not contradict that obstruction.

## Reproduction

```sh
PYTHONPATH=. .venv/bin/python \
  experiments/four_point_depth_projection/k7_product_audit/audit/independent_geometry_audit.py

PYTHONPATH=. .venv/bin/python \
  experiments/four_point_depth_projection/k7_product_audit/verify_candidate_k7_product.py

PYTHONPATH=. .venv/bin/python \
  experiments/four_point_depth_projection/k7_product_audit/verify_candidate_k7_via_k6_faces.py
```

The full shipped K7 product suite has four exact verifiers and ten tests; all
pass under CPython 3.14.6.  Rerunning the discovery/exactification program
reproduces the candidate byte-for-byte.  As with the K8/K9 verifiers, the
shipped K7 verifiers use Python `assert` and must not be invoked with
`python -O`; this independent geometry audit uses explicit exceptions.
