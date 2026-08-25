# K3P sharpness adversarial audit work log

## 2026-08-25 — audit opened

- Scope is strictly confined to `sharpness/adversarial/`; all parent sharpness artifacts and frozen inputs are read-only.
- Parent `PASS` fields are treated as untrusted data.  The audit will reconstruct the graph maps, equality slice, exact rational Krawczyk operator, uniform rank minors, physical inequalities, rooting censuses, and cherry extension independently.
- Planned attacks include alternate center-radius interval arithmetic, deliberately wrong Krawczyk orientations, floating-point box collapse, malformed slices, nonpersistent rank minors, stochastic-versus-CT boundary mutations, an explicit `sd_0` reconstruction check for every rooting, topology invariants, and rank-dropping cherry mutations.
- The cloud script references `sharpness_relative_root.json`, which is absent.  The final rational witness may still be checked as a self-contained proof witness, but its discovery lineage cannot be replayed end-to-end.
- Strongest verified claim at opening: none; parent claims remain hypotheses.
- Exact remaining gap: every assigned sharpness gate.
- Best-guess completion: 8%.

## 2026-08-25 — preliminary topology countercheck

- The labelled underlying graphs have different leaf-distance matrices.  In particular, `d_W(0,1)=4` while `d_Wprime(0,1)=3`.  This alone excludes labelled underlying-graph isomorphism and therefore ordinary-triangle equivalence.
- The all-`n` construction grafts only above leaf 2, so the distance between leaves 0 and 1 is unchanged for every stage.  This provides a direct all-`n` separation invariant independent of the parent contraction argument.
- Strongest verified claim: base and all-`n` labelled nonisomorphism/nontriangle-equivalence, conditional only on the exact graft definition still to be replayed.
- Exact remaining gap: exact analytic certificate, census, class persistence, cherry inverse and full-dimensionality.
- Best-guess completion: 18%.

## 2026-08-25T04:59Z — alternate exact analytic replay passed

- Reconstructed the displayed-tree Fourier maps by DFS reachability in all switchings, then rebuilt the 15 scaled equality polynomials.  The independent expansions agree coefficientwise with the embedded equations and are multiaffine.
- Derived a fresh exact rational inverse of the equality point Jacobian.  Exact center-radius interval arithmetic gives Krawczyk error bound `8.077023076476e-47` and normalized operator radius `9.740999384091e-41` at box radius `1e-50`.
- Independently selected rank-15 minors and proved uniform persistence with bounds `1.543152096600e-45` for `W` and `4.582719524575e-45` for `Wprime`.
- Checked every stochastic and strict-CT inequality throughout the box, plus the effective edge obtained after suppressing the artificial root.  The smallest margins are `4.964484595360e-10` and `1.395195552339e-9`.
- Strongest verified claim: a strict-CT common tensor exists in the slice, is unique in that slice box, and is a rank-15 regular point of both images.
- Exact remaining gap: topology definitions, all-`n` extension, and mutation suite.
- Best-guess completion: 67%.

## 2026-08-25T05:03Z — topology and all-n adversarial replay passed

- Explicitly reconstructed `sd_0` after every enumerated rooting and recovered censuses `W:(5,2,3)`, `Wprime:(7,2,5)`, and `collision:(7,0,7)` without consuming the frozen census.
- Checked simple binary level-2 status, no-omnian failures, exact LSA dominators, and unique orientations.  A synthetic LSA-invalid fixture is accepted only when the LSA condition is deliberately disabled; erasing retained heads is rejected by literal `sd_0` comparison.
- Established the direct leaf-distance separator `d_W(0,1)=4 != 3=d_Wprime(0,1)`, which persists for all prescribed grafts and rules out both labelled isomorphism and triangle equivalence.
- Recomputed the cherry Jacobian determinant as `176/25`, performed an exact positive-branch recovery of all six edge variables and the old tensor, and verified strict-CT cherry spectra.
- Lifted both a tree-child and a non-tree-child rooting through stages `n=4,...,12`, with exact contraction, bridge, blob, triangle, binary, and level checks.  The local induction covers all `n`.
- Strongest verified claim: the full all-`n` sharpness theorem, subject to the remaining falsification suite.
- Exact remaining gap: targeted mutations and reader audit.
- Best-guess completion: 91%.

## 2026-08-25T05:06:53Z — adversarial sharpness audit closed

- All targeted mutations were detected: binary64 box collapse; unsafe interval orientation; transposed preconditioner; under- and over-sized boxes; Krawczyk sign semantics; duplicate/dropped slice data; nonpersistent rank minor; stochastic-but-not-CT edge; zero eigenvalue; LSA omission; arrowhead erasure; duplicate cherry observable; and tied cherry edges.
- Final verdict: mathematical sharpness claim `PASS`; proof gaps none within scope; provenance `PASS_WITH_DOCUMENTARY_GAP` because `sharpness_relative_root.json` is absent.
- Final artifact hashes:
  - `adversarial_audit.py`: `c332e27f3e1ed62d97fcb30485fef692a7f1304acf716bc5817e87bca68d7022`
  - `SHARPNESS_ADVERSARIAL_AUDIT.json`: `fbaf04e09485aa5239de70cb4e613966f0f29af9f2641298a6c7580a61efdead`
  - `SHARPNESS_ADVERSARIAL_AUDIT.md`: `91103d7a3781b4349c1da3853f22391a29b5adc929ac044ec1d7cb4498dcf015`
- Strongest verified claim: for every `n>=3`, the stated weak-but-not-strong binary standard semi-directed level-2 pair is nonisomorphic, nontriangle-equivalent, strict-CT, and shares a full-dimensional regular K3P germ of dimension `6n-3`.
- Remaining mathematical gap: none in the assigned sharpness package.
- Remaining documentary gap: the missing discovery intermediate prevents end-to-end replay of how the rational witness was found, but not exact verification of that witness.
- Best-guess completion: 100%.
