# v1.0.9 PDE and nonlinear referee research log

Target: immutable source commit `94d5177485b9680be8b77f13448abf1f923963e8`.
No manuscript files are edited in this effort.

- 2026-09-06T18:05:47Z — 10% complete. Began a new, independent proof audit
  of main Sections 6 onward and Supplement S5 onward, with particular
  attention to the new near-threshold cubic and all-mode checks. Success
  requires identifying exact hypotheses, reconstructing the PDE proof,
  independent algebraic verification, and an adversarial search for omitted
  or false cases. Prior verdicts are not accepted as evidence.
- 2026-09-06T18:10:17Z — 75% complete. Read the full relevant main text,
  the correction/gauge and sectorial arguments, the current near-threshold
  verifier, and the generic recurrence-to-cubic bridge. The new near-threshold
  verifier does derive its Jacobian and Hessian from the reaction list and
  proves simplicity, transversality and all higher-mode stability. A second
  implementation using polynomial differentiation and Bernstein interval
  certificates has passed. It also passed exact contractions in four
  dimensions, symbolic-L mass-gauge checks, eight exact endpoint contractions,
  and independent regeneration of all four modulus polynomials. A generic
  gauge-summation bridge and the final adversarial interpretation review remain.
- 2026-09-06T18:12:25Z — 95% complete. Generic all-dimensional mass-gauge
  summation and cubic-margin identities passed. Full independent script PASS
  is saved. No new mandatory nonlinear/PDE change was found; the old
  near-threshold concern is closed by the current code and a separate exact
  proof. Detailed report prepared; independent cross-review is requested
  before promoting the combined parent report.
- 2026-09-06T18:15:48Z — 98% complete. Independently verified the algebra
  referee's two supporting-export omissions using exact counterexamples and
  a contextual reading. Both summaries need explicit diagonal diffusion;
  the proof skeleton additionally needs `det J=0`. The main theorem already
  states both. This is a minor correction to the exports, not a PDE theorem
  failure. Reciprocal review of the near-threshold conclusion is pending.
- 2026-09-06T18:17:18Z — 100% complete for this delegated review. The algebra
  referee independently agrees that S9 proves primary transverse subcritical
  onset on exactly the stated domain, with no missing uniformity caveat.
  Reports and exact artifacts are ready for the root's final consolidation
  and publication checkpoint. No manuscript or snapshot files were changed.
