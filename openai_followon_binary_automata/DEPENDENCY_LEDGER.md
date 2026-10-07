# Dependency ledger

Pin: openai/math adc7f1241b42e322a6451854ab7e4b4c146bf78a. Upstream read-only.
Exact hashes are in SOURCE_MANIFEST.json and the independent audit hash files.

| ID | Precise dependency | Assumptions / use | Validation basis | Status / gap |
|---|---|---|---|---|
| D1 | OWL_h 2DFA bound 2^floor((h−2)/31)≤4(s+2)², h≥2; sharper s+1 for zero-step acceptance | Full relation alphabet; finite-run target conventions; apply exact sh² pullback | Entire central manuscript mechanism, actual theorem and semantic definitions independently inspected; degree≤4 Brauer corner/support falsification tests | No substantive gap found; see upstream_determinization.md. This is handwritten audit, not reproduced formal verification |
| D2 | Product-emptiness 2NFA bound 2^floor((h−2)/127)≤2(s+1), h≥2 | All relation words, complement universe Σ_h*, zero-step finite acceptance | Central representation/order-reversal/transport/nesting/amplification mechanism independently inspected against actual declarations; width1 exhaustive / width2 seeded falsification | No substantive gap found; see upstream_complementation.md. Formal build unverified |
| R1 | Fixed h² adjacency encoding with N_h=(3h³−h)/2+2 marked source, N_h−1 ordinary source, exact sh² target | All binary words; malformed lengths reject; canonical pullback of full complement | Uniform explicit proof in main.tex; separate original derivation and independent adversarial implementation; 227,136 and 4,472,832 pullback comparisons | Proven as uniform reduction; finite tests supplementary |
| R2 | h³ fooling set lower bound for strict-block source | All malformed lengths reject; ordinary/no-left finite-run source | Explicit cross-concatenation proof; separate compiler, priority and adversarial checks | Proven; cubic order only for this precise total language |
| F1 | Lean source kit matches pinned input; advertised Comparator signatures match | Only source-level evidence is invoked | 41 byte-identical modules and source lexical scan; exact toolchain and dependency pins retained | Build, theorem axiom sets and Comparator were NOT reproduced; disk failure recorded. No formal verification claim |
| P1 | Priority/attribution | No first or independent breakthrough claim; distinguish existing coding and restricted targets | Dated primary-literature statement inspection and citation chain; older 2011/2013 coding and R816 public antecedent; upstream release-date evidence | No duplicate unrestricted exponential binary theorem found in inspected sources; negative searches not proof of novelty |

The upstream lower bounds are external mathematical theorems, checked by
independent handwritten audits here. A source scan, favorable verdict or
finite test alone cannot establish them. Any subsequently found pivotal gap
invalidates unconditional promotion until repaired.
