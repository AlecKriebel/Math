# PR166 independent cylinder geometry adversarial review

The theorem in the exact original submission survives this independent adversarial audit. No substantive mathematical defect was found. The verified conclusion is that, for the stated positive stationary binary Markov source, the explicitly constructed fixed nonboundary continuity rank has no tight square-root-scaled cost family under any deterministic real centering sequence. This is a negative answer to universal fixed-rank marginal convergence, with the precise scope stated by the candidate.

Original head: `efc3f35a72543ad9ae76fd31a860116f1ffd4a32`.
Candidate: `COUNTEREXAMPLE.md`, 13938 bytes, SHA256 `c72a38099e93b4d593be231e8f0c4ad726a399c3d61283da9f7b1f7e55801a5c`.

The independent first assessment was sealed on 2026-10-12T10:33:34.939072+00:00. `FIRST_ASSESSMENT.md` and `FIRST_ASSESSMENT_SEAL.json` are mode 0444, preserved unchanged. No original author verifier, author review, status/gate/frozen verdict, root review or sibling assessment was consulted before that seal. None was needed or consulted afterward. The mathematical source check used freshly retrieved primary sources only.

The cylinder mechanism is valid at every required index. The initial fair bit contributes no transition; W_j contains 2j-4 changes and j^2-2j+2 preservations. This gives the stated P_j and the rank series. The infinite word has both digits arbitrarily far out, placing its rank strictly inside every prefix cylinder and proving both nonboundary status and continuity of the mean profile. The two eventual endpoint strings have means C_j+(3/2)P_j and C_j+(1/2)P_j. The first switch into their terminal strings is present; the jump is exactly P_j. The gap between square positions leaves exactly 2j zeros, and the cylinder geometry gives the claimed rank-distance estimate with strict inequalities.

The exact algorithm stops on a singleton. Its recursive bucket cost equals the candidate's count sum, including the depth-zero charge and excluding all continuation of singleton buckets. The uniform approximation to n m(s) is established on explicit empirical-CDF and pair-separation events. It applies to the selected random string without an independence or supremum-measurability assumption. The scales w_j=P_jq^j and n_j=ceil(w_j^-2) give diverging rescaled jump height and negligible relative cost error. The binomial order-statistic CLT supplies positive limiting probabilities for the two adjacent rank windows. The two cost bands separate by 3n_jP_j/4, so every deterministic center misses one band eventually on each fixed square-root-scale window. This proves non-tightness, rather than merely an incorrect centering or a process-level obstruction.

Adversarial controls were independently written and reproducibly executed:

| Check | Coverage/result |
| --- | --- |
| Exact rational partitions, prefix masses, left ranks and inverse coding | 8191 words through depth 12 |
| Square-position counts, endpoint means, jump, local-cylinder lengths and rank tails | j=2 through 50 |
| Operational recursive selection versus stopped prefix-count sum | 9216 rank cases on distinct four-bit inputs, including singleton lists |
| Deliberate erroneous conventions | Six mutations all detected: initial transition, missing terminal switch, wrong rank increment, K=0 length formula, omitted root charge, and continued singleton charging |
| Deterministic reproducibility | Full control output reproduced byte for byte |
| All-index analytic scale check | Independent derivation; an additional exact conservative bound validates the two cost bands for every j>=100 |

Two potentially sensitive boundary cases were checked explicitly. The local length formulas need K>=1; this holds because K_j=floor(j/2) and j>=2. Inclusion of the w_j windows in both local cylinders starts at j=17 and fails before that threshold; the candidate asserts only eventual inclusion, which is sufficient. Finite controls are diagnostic. The asymptotic conclusion is proved by the all-index estimates in `INDEPENDENT_DERIVATION.md`.

The independently retrieved process preprint confirms the exact cost and quantile definitions. Its existing boundary-rank non-tightness and the subsequent open-marginal sentence are both present. The OWR contribution contains the marginal question on printed page 2856. The construction adds a nonboundary continuity rank and rules out every deterministic centering there; it does not claim an all-rank or almost-everywhere classification or exclude random, data-dependent centering. No historical-priority audit or assertion is made, and the final publisher-typeset wording was not examined. The newly retrieved OWR PDF differs in bytes from the author's allowed source manifest, so this source check reports the actual retained digest and independently inspected content rather than claiming byte identity.

`RESULT.json` records the machine-readable result. `FINAL_MANIFEST.json` inventories every retained file and input by SHA256, size and mode, excluding only itself; its digest is delivered externally. `PUBLIC_OUTPUT_WHITELIST.json` explicitly lists own outputs eligible for publication. All copied inputs, primary-source PDFs and text extractions remain private and outside that whitelist. No outside human communication, Git/index/ref/branch/checkout change, remote mutation or release was performed.

Strongest verified result: the full submitted non-tightness theorem. Remaining mathematical gap within that theorem: none identified. Remaining questions outside its stated scope: other-rank and almost-everywhere classification, and historical priority. Audit completion estimate: 100%.
