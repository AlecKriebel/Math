# Independent mathematical audit for publication strategy

Audit date: 2026-09-14 UTC (2026-09-13 local). Completion estimate: 100% of this bounded manuscript audit; this is not a percentage guarantee of theorem correctness or journal acceptance. No production files were changed, no individual was contacted, and no new mathematical claim was promoted.

## Scope and conclusion

I read the complete current `paper/main.tex` and `paper/appendices.tex`, inspected both exact verifiers, and ran `run_all.sh` before consulting earlier referee reports. I found no clear fatal gap in the current manuscript's main argument. This is a substantive specialist theorem with an unusually strong verification package. The main publication need is a coherent updated public manuscript that foregrounds the universal two-input theorem and accurately connects it to the existing Lean work, followed by independent subject-matter scrutiny.

The result is **not** simply another example of a useful nonprojective measurement. For each finite, input-dependent output architecture, it claims equality of the shared-randomness convex hulls of all bipartite qubit POVM and PVM behaviors when both parties have two inputs (`main.tex:62–99`, `1666–1705`). It then combines this with an explicit three-by-two separator to obtain the sharp minimum setting architecture. Zero effects, identity projectors, mixed states, variable output labels, and deterministic/stochastic output processing are included (`267–313`). It neither proves raw-set equality nor requires the simulation to preserve the original state (`282–293`, `1707–1728`). Those qualifications are mathematical content, not cosmetic caveats.

## Independent proof assessment

| Component | Mechanism and assessment | Current source |
| --- | --- | --- |
| Exact separation | Rational Bell coefficients; explicit positive rank-one effects; CHSH deficit bounds control state bias and Bob-axis overlap; all ternary projective supports bounded. The polynomial robustness certificate holds on a larger box than the physical parameter domain, so omitted geometric compatibility cannot invalidate it. | `main.tex:411–678`; `appendices.tex:1–95` |
| Binary-party simulation | Compress Bob's steering cone to dimension at most three. Minimal positive ray relations are two-versus-two; purification turns both decompositions into one complete projective strategy per shared branch. Common, rather than input-by-input, randomness is explicitly preserved. | `main.tex:685–835` |
| Extreme residual reduction | Compact convex separation selects an extreme maximizing behavior. Common-span filtering forces the local measurement spans to intersect only in the identity; dimension and POVM extremality leave one binary and one ternary measurement per party. Full-rank marginals justify the filtering contradiction. | `main.tex:837–971` |
| Physical coordinates | An invertible effect frame gives a Lorentz metric and five null incidences. The reconstruction supplies actual positive effects, a normalized pure two-qubit state and all Born probabilities. Zero joint probabilities do not invalidate two-sided variation because the reconstruction itself guarantees positivity. | `main.tex:1007–1243` |
| Multiplier sign | Finite POVM duality and adjugate pullback identify the geometric multipliers. A zero multiplier permits deterministic replacement of an entire input at unchanged score, yielding a local behavior and contradicting strict separation. This is a particularly important conceptual bridge for a domain expert to review. | `main.tex:1258–1398` |
| Residual exclusion | The compatible second form has inertia `(4,12)`; rank at least two gives an uphill normalized tangent. The full projective-fiber analysis handles exceptional divisors for rank one; rank zero reduces to an explicit bounded transport construction. The stated case split is exhaustive. | `main.tex:1400–1692`; `appendices.tex:287–585` |

The most valuable adversarial targets are the bridges from extreme physical strategies to the residual model and from incidence stationarity to physical improvement. They are addressed explicitly in the manuscript; they are not established merely by a passing symbolic identity check. I independently checked the sign of the second-variation argument, the normalization correction, and the deterministic-replacement mechanism and found them consistent.

The simple certified gap is `3(2−√2)/250 ≈ 0.00703`. The stronger attained strategy gives `L1 ≈ 28.92517633`, versus the manuscript upper bound `U ≈ 28.91724181`, a gap of approximately `0.00793452`. No optimum is claimed for either bound. The result's importance lies principally in the exact architecture classification, not experimental robustness; the paper correctly leaves more robust witnesses open (`1730–1738`).

## Fresh verification and limits

`sh qubit_povm_pvm_minimum_settings/run_all.sh` passed in this audit with Python 3.9.6 and the required SymPy 1.14.0. All eight artifact hashes passed, followed by both exact separation strategies, all closure algebra checks, and the rank-zero simulator. Python 3.14.6 is recorded as the reference version; the script does not require that exact Python release.

The closure verifier contains genuinely symbolic identities for the metric, quadratic inverse, exceptional fibers and transport algebra. Its pure-state conformal-Lorentz and Hessian checks include exact regression instances (`artifacts/two_by_two_closure/verify_exact.py:131–192`), not general formal proofs. `appendices.tex:588–611` correctly states this boundary. I did not treat these tests as a complete independently formalized proof and did not run a new full Lean build in this subtask.

After forming the assessment above, I read the existing referee material. Its earlier strict-domain objection has already been repaired: current `main.tex:1040–1051` explicitly keeps Lorentz signature separate from scalar positivity. Do not describe that old issue as an outstanding defect. The reports also establish that extensive principal-result Lean formalization already exists; the dedicated Lean audit should determine the current certificate status. Current main-paper verification prose (`1747–1754`) still discusses only exact scripts, leaving a material public-facing integration opportunity.

## Novelty and impact

My independent conditional impact estimate under the supplied rubric is **7.8/10**, assuming correctness, novelty, and successful publication: an upper-end strong specialist result. Arbitrary-output convexified equality and a sharp architecture threshold are substantially more useful than an additional isolated Bell inequality. They rule out a whole class of proposed qubit measurement-certification schemes and identify the first possible setting architecture. I would reserve an 8-plus “major subfield advance” assessment for stronger evidence of centrality or adoption of the method. This is not an average of prior scores.

The broad existence question concerning POVM advantage was answered by [Vértesi and Bene (2010)](https://arxiv.org/abs/1007.2578). Therefore a description suggesting that this manuscript first solves Gisin's broad original question would overstate novelty. Its defensible central contribution is the matching arbitrary-output two-setting lower bound.

The neighboring [Panahi et al. dimension theorem](https://arxiv.org/abs/2505.20519), [Cerf–Ollivier perturbative work](https://arxiv.org/abs/2603.26875), and [Oszmaniec et al. operator simulation framework](https://arxiv.org/abs/1609.06139) address different questions. Their primary abstracts corroborate the manuscript's distinction between dimension bounds, local/raw-set geometry, and same-system operator simulation. This bounded check is not a claim of exhaustive priority clearance.

**Essential new related work:** [Zhu, Chen, Wang and Zheng, v2, 31 August 2026](https://arxiv.org/html/2608.01317v2) gives a different rational three-by-two witness, an analytic arbitrary-state qubit-PVM bound, a Lean separation certificate, and an exact unrestricted-dimensional quantum optimum. Their discussion explicitly leaves the exactly-two-settings-per-party question unresolved. Thus the analytic-witness and formal-verification components overlap, while this manuscript's universal two-input equality and minimum architecture remain distinct. Cite and compare this work in the next revision; its appearance materially strengthens the case for foregrounding the equality theorem. Publication dates alone establish no claim about influence or misconduct.

## Concrete publication implications

1. Update the publicly archived paper and its literature comparison, incorporating the corrected strict-domain definition and an accurately scoped pointer to the existing Lean theorem package. Make the distinction between principal endpoints and auxiliary prose proofs explicit.
2. Seek external subject-matter assessment of novelty and physical modeling, not another cycle of undirected algebra checks. The most useful expertise is finite-dimensional Bell correlations, POVM simulation, and the residual geometric argument. Only the human user may initiate any communication.
3. Do not delay submission for a new full Lean project or for global optimum calculations: substantial formalization is already present and exact global optima are unnecessary for the principal classification.
4. Treat a short, bounded public-comment period after the coherent revision as a practical opportunity to catch objections, not as a prerequisite that requires replies. If no substantive mathematical objection remains, proceed with the journal submission rather than wait indefinitely for attention.

This audit proposes no manuscript edits, external messages, journal submission, or immutable release by itself.
