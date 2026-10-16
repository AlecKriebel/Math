# PR906 / problem 30006419: independent Reshetnyak proof audit

**Verdict: the explicit negative construction passes this analytic audit.**
No material defect or unsupported central step was found in
`author/PROOF.md` at original head
`32eaecaa8907dbf674e65b138b000cdcc49004ae`. The strongest verified result is
a compact smooth Riemannian sphere receiving a smooth homeomorphism from the
round sphere that is locally minimizing for Reshetnyak energy against every
same-trace `W^{1,2}` competitor and is not infinitesimally quasiconformal for
any finite constant. This is a negative result for the general-energy
interpretation that admits Reshetnyak energy. It does not resolve a separately
restricted Korevaar–Schoen question, and it does not establish historical
priority.

The full checkable reconstruction is in `INDEPENDENT_DERIVATIONS.md`. Six
independently written finite/adversarial controls pass in
`CONTROL_RESULTS.json`; they support the analytic review and are not a formal
proof of Sobolev facts.

**Utility revision.** The active control and manifest utilities now use explicit
exception guards that remain enabled under `-O` and `-OO`, and the verifier
supports standalone packaging. `UTILITY_REPAIR.md` and
`UTILITY_REPAIR_RESULTS.json` distinguish this distribution repair from the
unchanged analytic theorem and unchanged control results. The initial sealed
review is preserved in `history/initial_revision/`; its archived utilities
retain their original limitations and are not the active verification entry
points.

## Independence, inputs, and authority limits

I read the immutable authored `PROOF.md` and reconstructed its mechanisms
before opening any old audit material. **No old audit report or old audit code
was read at any stage.** The source ledger was used only to identify primary
sources; each relevant definition was inspected independently in the live
primary text. No author check code was imported or run. The original snapshot
hash list was used solely for final integrity verification.

The original packet was not modified. This review makes no Git mutation,
deposit, release, merge, Sheet edit, external communication, new proof-search
attempt, or candidate repair. It audits the existing route inside the original
attempt budget. Raw PDFs are confined to the ignored `private_sources/`
directory. Publication is governed by the enclosing audit, not this verdict.

## Exact scope checked against primary sources

The [arXiv v1 paper](https://arxiv.org/pdf/2503.08553v1) includes Reshetnyak
energy in its admissible class (Definition 3.1), tests quasiconvexity in
finite-dimensional normed targets (p. 10), and defines harmonicity by one
neighborhood per point followed by all relatively compact Lipschitz
subdomains and all same-trace Sobolev competitors (Definition 6.1).
Definition 2.3 uses the ratio between directional stretches almost everywhere.
Question 1.9 asks about harmonic spheres under Theorem 1.3's target assumptions.
The [Oberwolfach report](https://ems.press/content/serial-article-files/52249),
printed p. 1625, fixes a suitable energy and then asks Question 1. This
validates the authored general-energy interpretation. The final publisher
text was not inspected, and a claim limited to a different fixed energy must
be treated separately.

## Mechanisms, adversarial checks, and exact gaps

| Mechanism / assumption | Independent verification and attack | Status / exact gap |
|---|---|---|
| Reshetnyak density | For a compact smooth target, embed it in Euclidean space, identify the weak tangent differential and approximate metric differential, and obtain `sigma_max^2`. Domain conformal factors cancel in dimension two. | Pass. No density or metric-convention gap found. |
| Ambient 1-Lipschitz angular coordinate | Use a strongly geodesically convex ball entirely within the flat belt. Its ambient minimizing geodesic gives `|y(p)-y(q)|<=d_X(p,q)`. A seam-crossing angular chart is a concrete failing negative control. | Pass. The authored proof explicitly supplies the otherwise essential ambient-distance hypothesis. |
| Universal flat-belt competitors | Extend the angular coordinate by McShane; compose every competitor with it. The fixed scalar trace is `x`, and `int|grad(x+w)|^2=|Omega|+int|grad w|^2`. | Pass for every matching-trace Sobolev competitor, including maps leaving the image patch or target belt. No continuity or homotopy restriction was introduced. |
| Exact calibration of conformal patches | A cutoff supported in an image neighborhood with area below half the target area gives a coefficient in `[-b,1]`, equals 1 near the reference image, and has zero sphere integral. Ordinary degree-two de Rham cohomology gives a smooth global primitive. | Pass. The cutoff is constructible from arbitrarily small neighborhoods; exactness does not assume the conclusion. |
| Pullback at critical `W^{1,2}` | Represent the primitive as a finite sum `f dg`. Bounded scalar mollification gives convergence of the pulled-back one-forms in `L^2` and wedges in `L^1`; ordinary scalar chain rules identify the differential pullback. | Pass. No smooth target-valued density theorem or unjustified critical-dimensional limiting argument is required. |
| Trace, product, and gluing | A compact smooth embedding has a Lipschitz inverse for intrinsic distance versus chord distance. Matching traces permit ordinary componentwise Sobolev gluing; scalar Lipschitz trace composition retains the target trace. | Pass. The gluing map remains target-valued almost everywhere. |
| Boundary invariance without a homotopy restriction | The difference of primitive pullbacks is `L^2` with support compactly inside `U`. Its distributional derivative is `L^1`; a cutoff equal to 1 on that support has zero integration-by-parts pairing. | Pass. Exact forms annihilate sphere periods; the full nonexact sphere area form is a failing control. |
| Signed Jacobian bound | The comass bound gives `v^*omega<=|Jac v|dA<=sigma_max^2dA`, while the orientation-preserving conformal reference attains equality. | Pass. Negative Jacobians and competitors with multiplicity do not invalidate the signed inequality. |
| Smooth compact target poles | The target metric becomes exactly `|dz|^2` and `|dzeta|^2` in the two pole charts; it is constant near the apparent absolute-value point. | Pass. No pole degeneration, boundary, or equatorial metric singularity. |
| Smooth homeomorphism and rank defect | `a>=0`, vanishing only at 0, makes `h` strictly increasing and onto. At both poles the map is the complex scaling `e^c`. It is smooth and compact-domain Sobolev, although the inverse need not be smooth at the equator. | Pass. Smooth homeomorphism does not imply diffeomorphism, and the proof does not require one. |
| Cover and seams | The belt domain `|t|<1` and conformal domain `|t|>1/2` plus poles overlap and cover; the thresholds `1/2` and `1` belong to the other open set. | Pass. No boundary seam is untreated. |
| Essential distortion failure | Away from the equator near zero the singular values are `cosh(t)` and `t^2 cosh(t)`. Every finite bound is violated on a punctured open band of round area `4 pi tanh(delta)>0`. | Pass. The zero-area equator is not used to establish almost-everywhere failure. |
| Geodesicity and small-diameter spheres | Smooth compact completeness gives geodesicity. A positive uniform convexity radius places small-diameter image spheres in a contractible ball. | Pass. The small-diameter condition is on the full image, as required. |
| Local quadratic isoperimetry | Uniform biLipschitz charts and a cone preserving the given boundary parametrization give area at most `L^4 ell^2/4` below a uniform short-loop threshold. | Pass. Lipschitz fillings are Sobolev fillings, and the estimate counts parametrized area. |
| General-energy admissibility | Continuity, monotonicity, homogeneity, and rotation invariance are direct. Unit-sublevel seminorms are uniformly bounded and equicontinuous. Convexity of squared matrix operator norm and Jensen verify the source quasiconvexity inequality. | Pass. Neither strict convexity nor Dirichlet harmonicity is silently assumed. |

All mechanism families above are verified; none transfers the central
difficulty to an equivalent unsupported claim. There is no remaining analytic
gap in the explicitly audited construction.

## Controls and material limitations

The independent control script uses exact rational polynomial integration for
the scalar cross term and Dirichlet negative variation. It checks cutoff
comass/zero-period algebra, explicit distortion ratios and seam points, and a
wrapped-cylinder coordinate that falsifies a naive ambient Lipschitz claim.
The cutoff's displayed quadrature is floating-point illustrative evidence
with no certified error bound; the proof instead uses exact analytic bounds
`47/192<=c<11/24`, in particular `c>0`. Numerical agreement is not promoted
to proof of smoothness or Sobolev boundary invariance.

Two nearby conclusions are false and were independently separated from the
result: the map has energy surplus `4 pi c>0` over a conformal map in the same
degree-one homotopy class, and a compactly supported positive-belt variation
has strictly negative Dirichlet first variation. Thus the global
homotopy-minimizer quasiconformality theorem and the classical Dirichlet
conformality theorem do not conflict with the construction.

This is a human-readable independent analytic audit, not a machine-checked
formalization. Its scope is the original explicit Reshetnyak construction and
the inspected primary general-energy formulation. It makes no exhaustive
literature or historical-priority assessment, and no statement about an
uninspected publisher version. Best-guess completion of the assigned analytic
audit is **100%**.
