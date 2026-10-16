# Fourier witness adversarial audit: PR 1071 / problem 30002170

**Verdict: accept the stated mathematical lower bound. P0: none. P1: none.
P2: none. P3: none in the submitted mathematical claim.**

The strongest verified result is: for every fixed (H\in(1/4,1)), independent
standard fBm components, every (T>0), every integer (n\ge1), and every
square-integrable estimator measurable with respect to **both** complete
uniform component grids,

\[
\left\|\int_0^T B^1_s\,dB^2_s-F\right\|_2
\ge \frac{2\pi(4/45045)}{D_H\sqrt{\overline P_f\overline P_g}}
       T^{2H}n^{1/2-2H}>0.
\]

Here (D_H,\overline P_f,\overline P_g) are exactly the explicit definitions
in submitted proof formulas (6)-(7), (15). The target is the canonical
iterated integral, with its standard covariance and normalization. The
constant depends only on (H), is not asserted sharp, and no limiting error
constant or error law is proved. Endpoint, adaptive, arbitrary-mesh,
unequal-Hurst, and correlated-component extensions remain excluded.

This is acceptance of mathematics and its exact scope only. It is not a
first/world-priority, global-novelty, current-open-status, journal, human
peer-review, or formal proof-assistant certificate.

## Pinned input and independence

The exact audited head is `fc37aa5169a0fe6adae0a254c9ee6c1531a2911f`, target
tree `unsolved_math_prioritization/attempts/30002170`. Before mathematical
reading, all nine original Git blobs, the entire target tree, the raw commit,
and exact submitted-pin bytes were preserved locally. Every blob agrees
with its declared SHA-256 and the submitted snapshot. See
[INPUT_CUSTODY.json](INPUT_CUSTODY.json), [SUBMITTED_PINS.original_bytes.json](SUBMITTED_PINS.original_bytes.json),
`pinned_objects/`, `frozen_target_tree/`, and `git_target_tree.raw`.

The full independent derivation was written and frozen at
`2026-10-14T03:49:22.241962+00:00`, before reading the prior independent audit,
status, provenance, README, manifest, or source-ledger contents. The freeze
records the derivation hash and precise read scope. Only after that freeze
were those six remaining original files read for consistency. The earlier
acceptance labels were not proof evidence. No other family review was read
or contacted. See [INDEPENDENCE_FREEZE.json](INDEPENDENCE_FREEZE.json).

## Proof mechanism and falsification attempts

The complete independently reconstructed proof, with all equations, is in
[INDEPENDENT_DERIVATION.md](INDEPENDENT_DERIVATION.md), preserved unchanged after
its freeze. A [readable presentation copy](DERIVATION_READABLE.md) restores
three inline TeX locations without changing mathematics. The main checks were:

1. **Normalization and signs:** The real conjugate-symmetric Hilbert space
   has a real inner product, the kernel has squared increment distance
   (|t-s|^{2H}), and real polarization gives the exact standard fBm
   covariance. The conjugation in (u_h) cancels correctly in the second
   inner-product slot, leaving the specified inverse transform. A missing
   conjugation or complex-Gaussian factor of two would fail this check.
2. **Endpoints and all-(H) Fourier bounds:** The zero extensions of
   (f=\phi'), (g=\phi), (\phi=x^4(1-x)^4), have zero traces through
   order 2. Their third weak derivatives contain no endpoint masses, although
   (f''') itself has endpoint value 24. Three integrations by parts and the
   explicit odd-series integral bound prove bounded periodization for the
   whole (\alpha=2H+1\in(3/2,3)), not just (\alpha<2).
3. **Scaling and variance:** The Gram scaling is exactly
   (\Delta^{2H+2-\alpha-1}=1). Selected covariance paths have a uniform
   **upper** Gram estimate. No false rough-range increment coercivity is
   imported. Component independence gives (\operatorname{tr}(AC)), and
   positive semidefiniteness gives the trace bound despite signed entries.
4. **All information and nonlinear estimators:** Every witness coordinate
   has zero covariance with every sampled coordinate. Joint Gaussianity
   proves independence of the entire witness vector from the entire
   (2n)-dimensional observation vector. The centered product witness is
   therefore orthogonal to every (L^2) observation-measurable estimator.
5. **Exact target pairing:** Finite Euler covariance identities factor
   between the two independent components. A checked (L^2) area limit and
   classical deterministic Riemann-Stieltjes convergence give exactly
   (E[X_TY]=na\Delta^{2H}). No rough stochastic Fubini, estimator
   linearity, hidden asymptotic-to-finite-(n) interpolation, or uniform-in-(n)
   interchange of limits is used.
6. **External witnesses and convention:** A precise joint-law transfer from
   finite sums to their (L^2) limits justifies witnesses on an isonormal
   representation even if they are not path-measurable in an original
   model. The Euler-to-polygonal correction has its exact factor one half
   and tends to zero in (L^2) in all three Hurst regimes. Thus the area
   convention is the actual canonical iterated integral.

The exact remaining gap in the stated mathematical conclusion is **none**,
within the ordinary explicitly stated foundation of standard Gaussian/Fourier
theory and standard (L^2) fBm area existence. That existence premise is not
an optimal-estimation lower bound or an equivalent transfer of the central
difficulty. The all-(H) lower bound does not use the smooth prior theorem.

## Source interface: independent sufficient check and external source error

The original target was freshly read in the full primary OWR PDF at printed
pp. 2524-2525 (PDF pages 32-33), including visual inspection. It asks for the
stated inequality and its vector conditioning includes both components.
[Original primary report](https://ems.press/content/serial-article-files/46412),
DOI [10.4171/OWR/2012/41](https://doi.org/10.4171/OWR/2012/41).

The NTU PDF was freshly downloaded as
[arXiv:0902.0497v1](https://arxiv.org/pdf/0902.0497v1). The entire needed
Theorem 1.1 proof in Section 3.2, printed pp. 11-14, was read in addition to
the integral/Euler definitions, analytic-area existence, moment formulas,
and local-area decomposition in printed pp. 1-10. The theorem statement,
definitions, and proof pages were visually checked. The source is standard
independent fBm and the same iterated integral. Its current PDF has v1 on the
margin but a March 22, 2022 internal typesetting date; the arXiv record lists
the v1 submission on February 3, 2009. The journal PDF was not obtained and
is not represented as inspected. Journal DOI:
[10.1016/j.spa.2009.10.007](https://doi.org/10.1016/j.spa.2009.10.007).

**External source defect, not a submitted lower-bound defect:** NTU v1
equation (27), printed p. 12, asserts a rough-range (o(m^{1-4H}))
off-diagonal contribution. Its preceding bound proves (O(m^{1-4H})),
and fixed lag-2 pairs make the stronger little-o assertion false. Specifically
its valid separated-cell product kernel implies

\[
E[I_0I_2]\ge\tfrac14H^2(2H-1)^2 3^{4H-4}>0
\quad(H\ne1/2),
\]

and there are (2(m-2)) such ordered pairs. Consequently the normalized
off-diagonal contribution has a positive lower limit. This audit does not
adopt that stronger remainder or certify the source's exact coefficients.

The necessary convergence is independently verified at the sufficient
strength in the frozen derivation: finite diagonal/neighbor terms plus the
separated-cell bound (C_H(r-1)^{4H-4}), counted with (2(m-r)) pairs,
give squared Euler-error upper bounds
(O(T^{4H}m^{1-4H})), (O(T^{4H}m^{-2}\log m)), and
(O(T^{4H}m^{-2})) in the respective regimes. Each tends to zero for
(H>1/4); Brownian convergence is separately exact. Together with the
independently checked polygonal correction this closes the needed source
interface even after challenging the cited proof. A future publication can
cite only the needed convergence and retain this sufficient derivation to
avoid relying on the erroneous stronger step.

The credited smooth prior was checked directly in the primary
author-uploaded July 14, 2015 Neuenkirch-Shalaiko preprint: Theorem 1 has
positive liminf and finite limsup for (H>1/2), for this integral and both
component observations. Remark 5 gives the Brownian optimum. This preprint
is distinct from the journal PDF. Local PDF download was denied with HTTP
403; the successful browser-tool PDF text read is preserved as a private
extract and no local PDF byte hash or local visual inspection is claimed.
[Primary author-uploaded text](https://www.researchgate.net/profile/Taras-Shalaiko/publication/280310281_The_maximum_rate_of_convergence_for_the_approximation_of_the_fractional_Levy_area_at_a_single_point/links/55b14b8208aec0e5f431112a/The-maximum-rate-of-convergence-for-the-approximation-of-the-fractional-Levy-area-at-a-single-point.pdf),
journal DOI [10.1016/j.jco.2015.09.008](https://doi.org/10.1016/j.jco.2015.09.008).

## Original-nine consistency and new checks

All nine original files were inspected completely after preserving their
contents; the mathematical three came before the independent freeze, and
the other six after. The manifest's eight member hashes and byte counts
match the actual files, its nine-member list matches the complete original
tree, and submitted pins additionally bind the manifest. The prior audit,
README, status, and provenance state the same target, grid, covariance,
quantifiers, exclusions, and non-priority limits. Their scope assertions are
consistent with the independently verified result. Their historical
inspection claims were not replayed or represented as newly verified
executions. Current primary PDF hashes match their recorded public-source
identities, independently of those labels.

Fresh [supplementary_checks.py](supplementary_checks.py) ran successfully
using the bundled Python with NumPy. Its reproducible outputs are
[SUPPLEMENTARY_CHECK_RESULTS.json](SUPPLEMENTARY_CHECK_RESULTS.json).
Exact rational identities include (a=4/45045), the first three zero
endpoint traces, and Brownian cell Gram norms (4/45045,24/5005), giving
the sharper constant for this same witness (1/\sqrt{54}<1/2).

Floating computations test Hurst values 0.251, 0.3, 0.49, 0.5, 0.51,
0.749, 0.75, 0.751, 0.9, and 0.999, with Gram sizes 1, 2, and 8.
They check derivative/Fourier signs, inversion, bounded sampled
periodization, signed-covariance trace estimates, cell-scaling cancellation,
finite Euler pairings, and the polygonal correction. Maximum sampled
Fourier-inversion discrepancy is (1.583\times10^{-7}); relative scaling
discrepancy is (1.518\times10^{-16}). The finite Euler pairing converges
to its independently exact target. These are finite, truncated,
non-interval-validated numerical checks; their discrepancies are not
rigorous quadrature error certificates and they do not prove universality.
Tiny Brownian off-diagonal numerical signs are truncation noise; its exact
Gram matrices are diagonal. The universal result is the analytic proof.

## Custody and work boundary

Source bodies, extracts, and rendered images remain in ignored private
`sources/raw/`; the local `.gitignore` was verified using read-only
`git check-ignore`. Public-source fetch metadata and hashes are in
[SOURCE_FETCH_RECEIPTS.json](SOURCE_FETCH_RECEIPTS.json). Exact read/visual
scope, member consistency, and output hashes are in the terminal receipts.
Checkpoints and percentage estimates are recorded in
[RESEARCH_LOG.md](RESEARCH_LOG.md).

All writes stayed within `reviews/fourier_witness_01`. No branch/index/Git
mutation, remote operation, PR publication, outside communication,
other-shard editing, or nested subagent was performed. The original
submission and older stages were left intact.
