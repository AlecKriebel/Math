# Source and scope audit

Numeric ID 30006020, OWR-14298589-005, rank 240. Checked 2026-10-01 UTC.
The pinned dataset statement and the statement/review hashes agree with the
campaign catalog; `TARGET.json` records the hashes. There is no separate
upstream research-results entry for this later OWR record. Its dated triage
is part of the problem record and is not a proof of openness.

## Exact primary question

Delecroix's contribution to OWR 41/2024, printed pp.2384–2387, defines the
fixed-genus sampling measure before Problem 2 on p.2387. The square count N
tends to infinity first; genus tends to infinity afterward. The applicable
known ensemble is the principal holomorphic quadratic stratum
Q(1^(4g−4)). We count maximal horizontal cylinders and normalize by total
surface area. Vertical cylinders have the same marginal by rotation.
The candidate makes no assertion of joint horizontal/vertical independence.

The requested example is area between 1/sqrt(g) and 2/sqrt(g). Problem 3,
the diagonal N=floor(alpha g) ensemble, is distinct and is not bundled into
Problem 2. Neither all strata nor every individual surface is asserted.
Cylinder core curves are counted once each; this is not a restriction to
primitive square-tiled coverings or height-one cylinders. The source's
automorphism-weighted and uniform sampling conventions have the same
limiting law here, as noted in its sampling discussion.

## Published inputs used, with exact locations

The full final Delecroix–Liu paper is JEMS 27 (2025), 5093–5131,
DOI 10.4171/JEMS/1469. Its Theorem 1.4 (PDF p.5) identifies the
normalized cylinder-area law with the length partition law. Theorem 3.2
(PDF p.15) and equations (3.1)–(3.3) give the stable-graph mixture.
The polynomial F in (2.1) excludes the graph automorphism factor; the
mixture divides by that factor. For the one-vertex k-loop graph it is
2^k k!. This prevents a potential factor-of-two error in the assembly
weights. Simplex measure is the ordinary coordinate measure; no Euclidean
surface-measure sqrt(k) factor is inserted.

Equation (6.1), (6.2), Lemma 6.4, and its proof (printed pp.5116–5118)
give uniform positive correlator coefficients and the monomial expansion.
The candidate explicitly derives a uniform density comparison from these
coefficients. It does not relabel Theorem 4.1's stated test-function conclusion as a
uniform total-variation estimate. Summing unrestricted heights
means m=infinity, giving zeta(2j), and integrating each monomial gives a
Dirichlet law of parameters 2j. Thus the total Gamma parameter is 6g−6.

The full published DGZZ paper is Inventiones 230 (2022), 123–224,
DOI 10.1007/s00222-022-01123-y. Theorem 1.7 identifies the cylinder-count
law with the multicurve-component-count law. Theorem 1.12 (PDF p.15)
gives its probability-generating asymptotic for |t|<8/7. Theorem 5.2
(PDF p.83) has a uniform low-k multi-vertex error
O((log g)^25 g^(-1) 2^k). The candidate uses k<=0.6 log(6g−6),
strictly inside that range. It does not use the apparently unrestricted
wording of the subsequent corollary at impossible one-vertex k>g.

## Source cautions and credit

The OWR microscopic summary prints scale 4g−4. The candidate does not use
that summary or silently change it into the exact mixture's Gamma total
6g−6. The mesoscopic result follows directly from the full published
formula, and intensity dx/(2x) is invariant under a fixed scale change.
The microscopic endpoint itself is outside the new mesoscopic theorem.

The cited authors' stable-graph, volume, correlator, and count estimates
are substantial established inputs. The finite checker is not a substitute
for them. Current primary-source checks found the published DL result and
the OWR reference to a small-components paper in preparation; no exact
published resolution of this mesoscopic question was identified. This is
not an exhaustive novelty search or a priority guarantee.

Full PDFs were read locally. URLs and byte hashes are in
`source_manifest.json`; PDF reading copies are not publication artifacts.
