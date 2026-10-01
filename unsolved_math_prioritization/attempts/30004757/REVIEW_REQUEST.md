# Independent review request

Review the frozen package identified by `FROZEN_MANIFEST.json`. The desired verdict is whether the **partial claims** are correct and safely scoped for an unresolved-target report, not whether the original problem is solved. It is not solved in this package.

## Main attacks requested

1. Turn1: localization of exposed faces, compactness/extreme points, and the disk argument for C¹ away from the inward ray
2. Turn2: radial Legendre transform, singular ODE contraction, convexity/MA identity of the restricted-domain model, and legitimate endpoint-sector limit
3. Turn3: exact anisotropic scaling, convexity and Alexandrov equation of the explicit profile, its conditional uniqueness, and the absence of an actual-source convergence assertion
4. Turn4: valid localization of Jin–Tu–Xiong Theorem1.1 to affine chambers, dimensional and interface-endpoint statements, and the hypotheses on the angular expansion
5. Turn5: radial barriers with identical asymptotic constant, global Perron limit, contact-body Hausdorff convergence, common-facet barrier, use of Mooney Lemma4.2/Proposition4.1, dual uniform convergence, optional fixed-weight rescaling, and the precise C2,beta versus C2 distinction

## Reading copies

Primary files are in `/tmp/30004757-sources/`, with exact checksums and URLs in `source_manifest.json`:

- `owr.pdf`, printed pp1884–1886, especially Problem4 on1886; rendered source pages were visually checked
- `mooney.pdf` and `mooney-arxiv.pdf`: Proposition2.1 and Remark2.2, equation(3) barrier, Proposition2.7, Proposition3.6, Lemma4.2/Proposition4.1, Remark4.6, Section5
- `mooney-rakshit.pdf`: Section5(2) preserves the cone/Hessian question after the later construction/stability results
- `huang-tang-wang.pdf`: Theorems1.1–1.2 require the single-plane/strict-convexity hypotheses
- `jin-tu-xiong.pdf`: exposed-point local regularity and single-plane global classification
- `jin-tu-xiong-singular.pdf`: Theorem1.1 with q=0, proof inSection2.1, and the sharpness/maximum-principle limitations

The check scripts are independently authored in this attempt, use the already-installed SymPy package, and have saved JSON outputs. They do not execute source-provided software. All 40 symbolic checks reproduce, but none is represented as a general PDE verification.

Do not silently promote the local models, collision-limit cone, or conditional angular coefficient into a description of the unknown fixed-separation cone. Preserve any correction and the five-turn exhaustion. No publication before the parent receives an independent verdict.
