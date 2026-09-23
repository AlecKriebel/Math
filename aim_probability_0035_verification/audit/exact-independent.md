# Independent exact reconstruction and adversarial audit

Checkpoint: **2026-09-23 04:12:29 UTC**. Estimated completion: **100% of this bounded mathematical verification**, with publication priority handled separately. Verdict: **the stated finite counterexample is correct**.

This report was produced by a separate agent role in the same research session, not by an unaffiliated researcher. The integer-fibre construction and its first successful execution were completed before reading the coordinator's verifier or encountering the previously published implementation descriptions. The task supplied the candidate graph, words and expected answers, so this was not a blind discovery exercise.

## Claim and scope

For the zero-field three-colour ferromagnetic Potts law on edges `AB AC AD BC BE DE`, with activity 30 and all-zero initial state, compare `CEBCBAEBE` with `CEBCBABE`. At the common ninth scheduled opportunity, the second process has done nothing at opportunity seven. The claim is that the first process is farther from the **full, unconditioned** Gibbs law in total variation.

The claimed difference is exactly

\[
\frac{7905357280856578194954129502105}
{766036711510586802141859485820665762204}>0.
\]

It disproves the universal finite deterministic update-word censoring property. It does not establish a random-scan comparison, a mixing-time improvement, minimality, or failure for every number of colours or every positive coupling.

## Independent mechanism

`verification/independent.py` enumerates all 243 configurations and their global Gibbs weights. For a chosen site it partitions configurations into fibres with all other coordinates fixed. If a fibre's relative Gibbs weights are integers \(w_i\), with sum \(d\), and its current integer probability numerators sum to \(m\), its new probabilities are proportional to \(mw_i/d\). A least common multiple makes all new numerators integral; a global greatest common divisor reduces the shared denominator after each update.

This derives transitions by conditionalizing global weights. It does not use the candidate's neighbour-count conditional formula, the candidate's reduced marginal formulas, or Fraction-valued transition propagation. Fractions are used to report final statistics and traces.

For every step and every site as applicable, explicit checks verify normalization, nonnegative masses, stationarity of the full Gibbs law, detailed balance on all fibre pairs, idempotence of heat-bath resampling and contraction of each chain's own TV distance. Checks use `require` and remain active under Python optimization.

The direct enumeration gives the energy histogram

| Monochromatic edges | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Configurations | 18 | 66 | 90 | 42 | 24 | 0 | 3 |

Thus the candidate's partition polynomial and \(Z=2207656998\) are independently correct. The two TV distances are exactly

\[
\frac{511715038479158504505751178946687363011}
{766036711510586802141859485820665762204},\qquad
\frac{9300189570967998685056395332640723}
{13922371260779084768671794660693282}.
\]

Every one of the fourteen colour-swap orbit representatives has the claimed nonzero signs. The JSON result records the exact marginal deficits, not merely their signs. Boundary controls for the same two words give zero gap at activity 1 and negative gap for two colours at activity 30.

## Adversarial semantic checks

**The unupdated vertex is legitimate.** Both evolved laws have support exactly the 81 states with \(D=0\). The reference measure still has all 243 states and stationary slice mass \(\pi(D=0)=1/3\). The computation does not normalize the slice to a conditional Gibbs law. A finite update word need not visit every vertex. If the word were repeated forever, its failure to update D would obstruct convergence to the full Gibbs law, but no convergence assertion is used in this finite comparison.

**The TV reduction is valid.** The final E update gives both evolved laws and the Gibbs law the same conditional E factor on the D=0 slice. Let \(X\) be the evolved ABC marginal and \(p\) the unconditioned stationary ABC slice mass. Then \(\sum X=1\), \(\sum p=1/3\), and the outside-slice contribution is \(2/3\). Consequently

\[
\begin{aligned}
\|\rho_X-\pi\|_{\rm TV}
 &=\tfrac12\left(\tfrac23+\sum|X-p|\right)\\
 &=\tfrac12\left(\tfrac23+\sum(X-p)+2\sum(p-X)_+\right)\\
 &=\tfrac23+\sum(p-X)_+.
\end{aligned}
\]

The positive deficits being small is consistent with, and does not remove, the obligatory 2/3 contribution.

**No contraction theorem is contradicted.** Each individual update contracts TV to its invariant measure. The extra update at opportunity seven initially helps. The full-minus-censored distances after common opportunities seven, eight and nine are respectively

\[
-\frac{27914154287275768550}{2677087697911935887107633027},\qquad
-\frac{28224495376926645875040665}{13821317041101522814975417021487},\qquad
\frac{7905357280856578194954129502105}{766036711510586802141859485820665762204}.
\]

Applying the common suffix BE can reverse the ordering of two distances while decreasing both distances. Shared invariance and individual contraction do not preserve such an ordering.

**The scheduling interpretation agrees with the primary historical source.** Holroyd's [2011 paper](https://arxiv.org/pdf/1101.4690), introduction and final paragraph of Section 3, uses finite deterministic single-site heat-bath sequences and asks about the ferromagnetic constant-start setting. This matches the witness. The original unsolvedmath endpoint could not be fetched by this agent; the separate statement/priority audit supplies that mapping. No claim about an additional random-scan restriction is inferred.

## Cross-review after the independent construction

The coordinator's `verification/verify.py` was inspected only after the integer construction passed. Its adjacency list, single-site law, R/F/Q formulas, stationary marginal formula, all 27 sign rows and full 243-state TV reference are consistent with the candidate. The chained comparison checking the exact positive gap and the conditional expression selecting boundary checks have correct Python precedence. No logical or arithmetic defect was found.

The coordinator verifier was rerun and its entire parsed output, including all 27 marginal rows, was checked equal to the retained `verification/certificate.json`. The independent integer method exposes complete distributions through `FibreChain().run(word)`: the returned law is `(numerators, denominator)` in the chain's lexicographic `states` order, allowing per-configuration comparison rather than only comparison of TV distances.

## Reproduction and priority boundary

Run from the effort directory:

```text
python3 verification/independent.py
python3 -O verification/independent.py
```

Both runs completed successfully and produced byte-identical JSON output. One copy is retained as `verification/independent-results.json`; `verification/run_all.py` repeats and checks both modes. The implementation uses only the Python standard library.

After constructing and running this verifier, a scope search encountered an exact prior public match at [Evidence Press](https://evidencepress.org/releases/potts-censoring-counterexample/), dated 6 September 2026 and citing [DOI 10.5281/zenodo.22546547](https://doi.org/10.5281/zenodo.22546547). The graph, activity, words and gap agree exactly. This verification cannot be represented as a new discovery without a separate justified provenance claim. Mathematical correctness and originality are separate conclusions.
