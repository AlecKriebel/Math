# Primary-source pins and direct access record

Accessed independently on 2026-10-05 UTC. These local source copies are audit
evidence; they are not authored findings or a request to redistribute the papers.
No primary-source access failure remains for the dependencies checked here.

## Submitted item

- Parent-specified immutable PR head: `7271f51995532791220ac8e6b738a578d5d59143`.
- File read: `../source_intake_20261005/submitted/COUNTEREXAMPLE.md`.
- SHA-256: `e22eb257358431f1c7e4dbdb2c8550c26972da1b24a573581aed8f84c14db0dd`.
- No Git commands were run to change or inspect the index; the parent supplies
  the association between this immutable file and the cited PR head.
- The submitted prior review was not opened before, during, or after this audit.

## Nash original theorem

- John Nash, *The Imbedding Problem for Riemannian Manifolds*, Annals of
  Mathematics, Second Series, 63(1), 1956, pp. 20-63.
- Primary paper hosted by Rutgers:
  [original 1956 paper](https://sites.math.rutgers.edu/~feehan/teaching/math866/nash.pdf).
- Local PDF: `sources/nash1956.pdf`; 45 PDF pages; 3,707,449 bytes.
- SHA-256: `1cd36149cfa1a9fe81ee98850635f22d4027bef33b0689413e8fdff7011183b6`.
- The PDF begins with a JSTOR cover. Printed p. 20 is PDF page 2; printed p. 59
  is PDF page 41 (all PDF page locators in this document are one based).
- Visually inspected original printed pp. 20, 21, and 59, including the entire
  Theorem 2 statement and surrounding compact-manifold summary.
- Exact import: compact positive `C^k` metric has a `C^k` isometric embedding,
  for `3<=k<=infinity`, in ambient dimension `(n/2)(3n+11)`.
- Hypothesis match: closed smooth hyperbolic surface, positive `C^infinity`
  metric, `n=2`. Ambient dimension is exactly the available bound 17.
- The source distinguishes its smooth result from the separate `C^1` theorem;
  no `C^1` regularity substitution is made in this audit.
- Extraction limitation: this is a scanned PDF, and `pdftotext` produced no
  substantive text. The theorem was verified by direct rendered-page inspection.
  This is an extraction limitation, not a source-access gap.
- Relevant visual evidence: `sources/nash_theorem2_actual_p59.png` and
  `sources/nash_intro_actual_p20.png`, `sources/nash_definitions_p21.png`.

## Hatcher author-hosted textbook

- Allen Hatcher, *Algebraic Topology*, author's online book version hosted at
  Cornell, PDF metadata dated 2022-10-26.
- Primary author source:
  [author's book](https://pi.math.cornell.edu/~hatcher/AT/AT.pdf).
- Local PDF: `sources/hatcher_at.pdf`; 560 pages; 8,121,741 bytes.
- SHA-256: `bebb3032bf9021b956da3bd070eb6c67dc662cf849be9cdf6679f677560e5618`.
- Directly inspected printed p. 51 (surface group presentation), p. 61
  (Proposition 1.32, sheet number is subgroup index), pp. 66-67
  (Proposition 1.36 and Theorem 1.38, subgroup realization and path connected
  covering classification). PDF pages are respectively 60, 70, 75, 76.
- Exact topological hypotheses: base path connected, locally path connected,
  semilocally simply connected. All follow from connected smooth surface disk
  neighborhoods. Kernel of the displayed surjection has index two.
- Upgrade to a smooth, Hausdorff, second countable, compact oriented cover is
  proved directly in `PROOF.md`; it is not silently attributed to a theorem
  about arbitrary nonsmooth spaces.
- Relevant visual evidence: `sources/hatcher_surface_p51.png`,
  `sources/hatcher_prop132_p61.png`, `sources/hatcher_prop136_p66.png`, and
  `sources/hatcher_theorem138_p67.png`.

## Original OWR contribution

- Arthur J. Krener, *Open Problem: Global Observability of Spaces of Negative
  Curvature*, OWR 11/2009, printed pp. 674-675.
- Primary publisher source:
  [original report](https://ems.press/content/serial-article-files/46211).
- Local PDF: `sources/owr11_2009.pdf`; 88 pages; 747,670 bytes.
- SHA-256: `ef407f7cb1bcf1793d9fb02001b1aa68515342649009e8bdd1c9aecfbf1b7fe9`.
- Directly read and visually inspected the full contribution on PDF pages
  82-83, corresponding to printed pp. 674-675.
- Relevant definition: initial state to full output-history injectivity for
  observability; local injectivity for local observability. The source uses
  local state coordinates on a manifold and arbitrary Euclidean output size `p`.
- The stated integral uses fundamental matrix `Phi`, Jacobian `H`, and the
  Euclidean output inner product. Its assumptions use some fixed `T>0` and
  uniform positive/bounded Gramian, uniform negative curvature, and geodesic
  completeness. The review independently checks the geometry of these data.
- The source does not specify a background metric or a global tangent frame for
  its uniform matrix bounds; `PROOF.md` gives both intrinsic and fixed-atlas
  meanings. Overall source/target identification is another review family's job.
- Relevant visual evidence: `sources/owr_krener_actual-82.png` and
  `sources/owr_krener_actual-83.png`.

## Dependencies proved here instead of silently imported

The concrete polygon metric (including its vertex), smooth cover upgrade,
finite-cover compactness, Euler characteristic multiplication, exact history
Gramian, curvature scaling, geodesic completeness on this compact manifold,
and history fiber size are derived in `PROOF.md`. Basic hyperbolic disk geometry,
the smooth local ODE existence/extension theorem, and the classification of
closed oriented surfaces are standard background facts used with their
hypotheses explicit. The counterexample does not depend on the genus labels
once the disk quotient and double cover have been constructed.

