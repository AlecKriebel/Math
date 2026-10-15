# Fresh independent mathematical adversary: PR254

**Verdict: PASS for the exact stated mathematical theorem. No mathematical repair is required.** This is not a priority verdict, a claim of novelty, or a publication recommendation before the separate priority gate.

Audited original head: `73efd1fb8ba2d3039ed6692b3ad1dfa1e3085755`.
Problem: `5100020 / AMR-050-0020 / k403,a`.
Submitted proof: 14,705 bytes, SHA256 `ff2b1d78a1b94997d366d5173243ea95b949d5ae24574471639740b35cf2c16e`.

## Independence and exact accepted claim

I read the entire submitted proof, the two author scripts, the two original independent-review scripts, source gate, source manifest and authenticated intake. I did not read the conclusions of any new sibling adversary. I separately rebuilt the complex analytic argument and wrote new exact and near-pole checkers; neither imports submitted code. The derivation in `INDEPENDENT_DERIVATION.md` is the universal mathematical evidence.

For an elliptic billiard with a strict nested nondegenerate confocal elliptical caustic and least odd period `N>=3`, the ordered signed-area product of the origin pedal and origin antipedal of the original orbit is phase independent. Coprime primitive stars are included. All real antipedal intersections are finite. The theorem avoids divisions by derived areas. Reversal preserves the product, and the circular billiard is proved separately. Hyperbolic or collapsed caustics, repeated lists used to change least-period parity, and unsigned region areas are not accepted extensions.

This family reviews the proof of that precisely identified target. The historical priority gate and full independent primary source-table audit belong to the parent workflow. I directly checked the classical Jacobi period, pole, zero and shift facts against [DLMF 22.4](https://dlmf.nist.gov/22.4), and addition identities against [DLMF 22.8](https://dlmf.nist.gov/22.8), accessed 2026-10-13 UTC. I found no mismatch in the Jacobi input used by this proof.

## Critical adversarial findings

1. **The support-line area formula names the right antipedal.** Solving the two original vertex-normal line equations gives the submitted intersections. An independent symbolic one-vertex shoelace decomposition and subsequent edge assembly give exactly the rational function `F(P,Q)` used in the proof. Bilinear complex dot products are appropriate for the algebraic continuation; no conjugation or square-root normalization is hidden.

2. **The complete chord determinant divisor is correct.** The addition formula reduces independently to `B(u)=2ab sn(v)cn(v)dn(u)/D(u)`. Its `D=0` roots at `p±v` are distinct and simple, with derivatives `±2cn(v)dn(v)/sn(v)` and nonzero determinant residues. At `p`, the determinant has a simple zero even though the individual Jacobi functions have poles. Its endpoints are finite and opposite. At `K+p`, it has a simple zero with finite coincident endpoints. The degree-two `sn²` divisor and the `dn` zero/pole classification exhaust the possibilities. This includes the frequently dangerous extra opposition zero.

3. **Coincidence and opposition were not conflated.** At coincidence, the exact numerator factorization makes the edge expression removable even for isotropic complex endpoint vectors. At opposition, the expression has at most a simple pole and the endpoints' squared norms are nonzero in the canonical family. The proof retains this pole.

4. **Individual incident terms can have double poles, but their sum cannot.** I computed the nonzero candidate double Laurent coefficient explicitly. The incoming and outgoing terms satisfy the exact symmetry `G(z)-G(-z)`, so their even negative powers cancel. The argument is not a finite-sample residue assertion. Odd primitivity prevents any edge from simultaneously containing two pole vertices.

5. **N=3 remains valid.** At a pole vertex phase, the unique opposite-endpoint edge is index `(N-1)/2`. For three-periodic trajectories it joins the two finite neighbors, while the two other edges are precisely the incident cancellation pair. The opposition term adds at most a simple pole and does not undo the cancellation. At the corresponding coincidence phase the antipedal remains regular, while the original-side pedal has its allowed pole. Both types were independently examined analytically and numerically.

6. **The odd star arithmetic supplies the required genuine torus.** Because `gcd(2tau,N)=1`, period `delta` together with `2K` gives `ell=2K/N`. Opposition midpoint poles reduce to the vertex classes since `v=tau ell`. The area functions are on the compact torus with periods `ell,4p`, and have antiperiod `2p`. No antiperiod is improperly used as a true period.

7. **The trace has the claimed poles and exactly the needed zeros.** At each of its two quotient poles there is a single contributing original trace term, with nonzero residue. Evenness and the imaginary antiperiod force two distinct regular zeros at `p+ell/2` and `3p+ell/2`. Equality of total zero and pole orders makes them simple and complete. Thus the half-shift trace product is holomorphic and constant. The residue uniqueness argument consequently puts the antipedal area in the span of the trace without assuming the target invariant.

8. **The pedal cancellation and the final shift are correct.** I verified the chord tangent equation for both original endpoints and reconstructed the origin foot. The quarter-period chart is `Q(K+p+z)=cn(z)/(k sn²z) * (alpha dn(z), i beta/k')`, an even coordinate function with at most a double pole. Neighbor subtraction is odd and kills the double area pole. The pedal area therefore lies in the span of `S(u+K)`. The actual orbit pedal uses `u=w+v`; `(v+K)/ell=tau+N/2` is a half-integer precisely for odd `N`, so the final product uses the proved half-shift identity.

9. **Limits and interpretation are sound.** Strict nesting supplies every denominator and regular-neighbor condition used in the proof. The proof holds for every interior modulus, including arbitrarily small positive modulus or modulus close to one, but asserts no hyperbolic/collapsed endpoint theorem. The separate circle argument has the correct radius factors and signed star area. Both coefficients have area units and the invariant has length-to-the-fourth units. The supplied four-periodic negative control is consistent with the exact parity obstruction.

## Fresh reproducible evidence

Run with Python plus SymPy and mpmath:

```
python fresh_exact_checks.py
python fresh_near_pole_diagnostics.py
```

`EXACT_CHECKS.json` records **25,369 exact assertions**, including generic symbolic line-intersection/shoelace, Jacobi addition, divisor slope/residue and quarter-chart identities, plus **4,225 finite primitive odd lattice families** through period 203. These finite lattice checks corroborate the all-index modular/Bezout proof; they do not establish it by enumeration.

`NEAR_POLE_DIAGNOSTICS.json` records **3,494 high-precision comparisons over 19 billiard families** at 220 decimal digits. These include periods 3, 5, 9, 21 and 31, maximal coprime star winding, modulus `1e-20` and `1-1e-25`, regular real and complex phases, and both vertex/opposition and coincidence/pedal collision phases at complex offsets `1e-10 K` and `1e-22 K`. Direct actual antipedal intersections and actual original-side feet were compared with the analytic expressions. The maximum scaled residual was **2.96395561209e-121**, below the predeclared `1e-80` tolerance. These are unvalidated diagnostics, not interval certificates or a replacement for the universal proof.

The first fresh exact checker launch had an unmatched closing parenthesis and failed before any mathematical assertion executed. Its original bytes are retained in `fresh_exact_checks_initial_syntax_failure.py`; the corrected final checker and its PASS output are pinned separately. A quarter-chart explanatory comment was also corrected before the successful run. This was a reviewer artifact error and did not identify a defect in the submitted proof. Two meaningless constant-only assertions from an intermediate successful script were removed before the final run; the reported final count and manifest refer to the final script.

## Remaining gaps and disposition

**Mathematical remaining gap: none within the stated domain.** No hidden equivalent unsupported invariant was found. No repair to the mathematical submission is requested. The exact opposition pole and N=3 collision must remain visible when condensing the proof into a research note.

**Outside this verdict:** historical priority, novelty or firstness, preprint drafting, final source-table reconciliation, submission metadata, author disclosures, and upload/merge decisions. A mathematical PASS does not authorize claiming the original problem was previously unresolved. Those gates should continue independently.

All owned final evidence and all 23 immutable submitted source files are pinned in `FROZEN_HASHES.json`. Full external papers have not been copied into this owned review packet. The retained initially failed script is historical failure evidence and is not part of the executable PASS package.
