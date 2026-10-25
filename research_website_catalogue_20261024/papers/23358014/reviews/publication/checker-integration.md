# Remaining shared checker integration: critical wave

This editor did not edit or run shared scripts. The existing renderer was inspected and uses `normalized_receipt_view`; the raw receipt's `assets` list stays unchanged. At preflight the shared final-content checker did not register 23358014. Add this exact source path:

```python
'23358014': 'published-source/critical_wave_verification/manuscript/critical_wave_growth.tex',
```

Use the exact abstract normalizer already present in the owned check-bindings.py:

```python
def normalized_wave_abstract(body):
    return ' '.join(body.split()).replace('$L^2$', 'L²').replace('$L^\infty$', 'L∞').replace('$L^1$', 'L¹').replace('$\{0\}$', '{0}').replace('$o(\norm{u}_{L^2}^2)$', 'o(‖u‖²L²)')
```

Wire this into abstract-token comparison and require full text equality, one paragraph, six sentences and 116 words. Bind TeX SHA-256 `bf4e13509ee738d1c5f73555e322ce77b9f2041b2306e4f80dfc588c98289584` and the exact frozen scope/content.json abstract. No excerpt replaces it.

Required rendered checks:

- Exact title/author/ORCID/DOI, printed and metadata version 1.0 and 14 October 2026 date; record creation `2026-10-14T05:39:12.680683+00:00` separate from priority. Six-page PDF and one verification ZIP, no extra/embedded readers. Standard supplement field; exact PDF/ZIP/receipt/source bindings. Raw receipt bytes and assets key must not be rewritten.
- Real 3D unit ball, homogeneous Dirichlet boundary, zero position/velocity, defocusing quintic, T=1. Controls in L²(0,1;H), H=L²(B), and small positive pointwise-in-time Hilbert cap; never a scalar pointwise space-time cap.
- Retain γ=β₁=1, quartic L⁴L¹² state cost and sparse L¹(H) cost; remove only β₂. Fixed finite ν≥0 optional H⁻¹ terminal-velocity cost. No ν=∞ assertion.
- Genuine unique global nonlinear optimizer zero for target πe, full cubic lower bound over all feasible controls, ordinary critical cone {0} with vacuous strict test, and actual nonlinear pulses defeating L²-squared growth in both L² and L∞ neighborhoods. The eigenmode identity is a linear projection, not a nonlinear invariant-subspace reduction.
- Global optimizer existence and every-selection radial displacement/target ratio divergence. Corollary's local L¹-squared growth and every-global-optimizer fixed-basepoint upper bounds. Arbitrary target change w with ε=‖w‖H; upper constants/neighborhood uniform over finite ν. Positive radial lower-comparison neighborhood may depend on fixed ν. Preserve the Θ(ε) and exponent bracket without sharpness.
- No perturbed uniqueness, pairwise Lipschitz selection or perturbed L∞ convergence; no all-target/all-cap failure. The explicit target-zero positive-quadratic-growth countercase remains visible.
- Classical concentration/noncoercivity/Dunn/subgradient/PDE credit. KM author v1 is not the unread journal-final body. Original OWR pp.438–440 addresses retaining the ordinary-cone implication unchanged, not rejection of all β₂=0 theories or strengthened sufficient conditions.
- FINAL root clearance SHA-256 `7ecd074783bbf82d6a7a6f31074cd6c6e0bf22fa9180400cc96949c259a5b8cf`. Preserve original custom scope status `SCOPE_COMPLETE_PENDING_MATHEMATICAL_REVIEW`, mathematical_pass=false and promotion_authorized=false, with separate later root resolution. Do not use the unsealed spacing draft as authority.
- Extensive AI/unrefereed status, no human-review/formal-certification/firstness/current-open claim, passive substantive collaboration and null follow-up. No private replay counts or dated audit story in public HTML.

Root must inspect actual generated public copy and scholarly/canonical/citation metadata, byte-identical PDF/ZIP links/downloads, index/sitemap integration and live desktop/mobile/browser behavior before native tracker updates. Owned pre-render editorial checks do not replace those gates.
