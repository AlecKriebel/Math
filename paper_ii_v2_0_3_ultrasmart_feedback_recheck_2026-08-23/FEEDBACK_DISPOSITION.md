# Feedback disposition for Paper II v2.0.3

Status: final; reconciled against three independent audits.

## Reproduced mathematical and computational claims

- **Exact algebra:** accepted.  The frozen replay reproduces the sextic endpoint signs, Sturm isolation, optimized values, response identities, rational margins, and rational threshold.
- **Finite lumping:** accepted at the supplied audit size.  The exact labelled-chain and orbit-chain calculation agrees on all 512 configurations and 108 fibres of the nine-vertex audit graph.
- **Weak-cut and large-population numerics:** useful corroboration, not a replacement for proof.  The manuscript already states this boundary explicitly.
- **References and build:** the cited bibliographic records and three Zenodo DOI targets checked in this audit resolve as represented; the deterministic manuscript remains 21 pages with no undefined references or overflow warnings.

## Requested issues

1. **Concrete finite-size thresholds — not added.**  The quoted values reproduce as separated-trace/leading-correction estimates.  They are not bounds for the connected family because the proof does not quantify the weak-cut diagonal or all finite remainders.  The manuscript's statement that it gives no useful finite-size bound is therefore the honest one.
2. **Floor-induced nonmonotonicity — already addressed.**  v2.0.3 states that `floor(lambda_* t)` contributes order-$t^{-1}$ oscillations to the scaled finite response and that positivity need not appear monotonically before the eventual regime.  Changing to nearest-integer rounding is unnecessary and would alter a frozen construction without strengthening the theorem.
3. **Mechanistic singular limit — already addressed.**  v2.0.3 records $F_r(0)=r(2r-3)$ and explains that the singular limit recovers the $3/2$ response endpoint while positive pair weight shifts the tangency to $R_{\rm hyb}$.
4. **Proof-level points:**
   - The $O(K/C)$ sharpening is valid and already incorporated.  The hub-change/ordinary-change hazard ratio is $O(C^{-1})$ at every pre-$K$ state, not $O(K/C)$, and the stopped embedded walk makes $O(K)$ expected changes.
   - Uniformity of the deficit-odds remainder is already stated immediately before the display as uniform in the hub and pendant coordinates.
   - The global-sweep union-bound logic is already clarified: failure requires a reversal, while a reversal need not imply failure.
   - The stronger numerically observed reciprocal decay is not needed and is not claimed.
5. **Weak-edge exponent — not added.**  Small-graph linear response in $\varepsilon$ does not prove polynomial growth of the sensitivity constant with population size.  Moreover, because the uniform interval reaches down to $r=1+1/t$, the complete-graph baseline is of order $1/t$; an absolute perturbation slope $c_t$ would heuristically require $\varepsilon_t\lesssim t^{-5}/c_t$, not the suggested $t^{-4}/c_t$.  The exact diagonal is intentionally effective without an unsupported complexity bound.

## Cosmetic and metadata points

- **Figure 1:** already fixed.  The schematic now draws all ten edges of the displayed five-vertex clique and moves the heavy-edge and weak-edge labels clear of the dashed representatives.
- **Rational threshold form:** no change.  Reducing $5069/6439$ to $37/47$ is correct but makes the single radical expression less compact and adds no mathematical information.
- **Abstract:** already fixed to define the supremum over values of $R$ with the full quantifier meaning.
- **MSC:** no change.  MSC 60J10 accurately covers the discrete Moran update chains defined in the paper.  The continuous-time clocks are a statewise time-change proof device, so adding 60J27 would be permissible but is not a correction.
- **Python:** confirmed.  Python 3.14.6 is the installed replay interpreter and is enforced by the bootstrap; SymPy 1.14.0 and mpmath 1.3.0 are supplied as hash-pinned pure-Python wheels.
- **Zenodo:** all three DOI URLs used in the manuscript resolve to the intended earlier-version records.  The manuscript correctly says that none is a persistent identifier for the superseding v2.0.3 revision.

## Release conclusion

No further manuscript edit is justified for the bioRxiv handoff.  The scientific source, PDF, source archive, referee folder, and transferable referee archive remain byte-for-byte identical to the frozen v2.0.3 handoff.

For a later strict Journal of Mathematical Biology submission, the human author must first provide truthful city and country for the title page; the live JMB guide requires these even for an unaffiliated author.  That journal-only metadata pass can also add an explicit prose citation of Figure 1 and apply journal caption/reference styling.  These are not scientific or bioRxiv blockers.
