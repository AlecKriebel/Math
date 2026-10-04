# Root initial mathematical review of PR316

The root read all 18 target files at frozen submitted head c96a3b2019ed3d6aabe0612b31491161dcb275e8 after recording the independent source-first criteria. The complete TURN_1 proof, author and inherited independent checker bodies, source/claim summaries, historical adversarial report and all manifests were read. Both original checkers ran natively with exact complete outputs matching the submitted 379-byte/80-byte records: 7,852 and 646 assertions. These are finite controls, not proofs of the infinite quantifiers.

## Independent analytical deductions

The law is admissible: p_n=2^(-2^n), a_n=2^(4^n); p_0 is the remainder on a uniform [1,2] component. Since 2^j>=j+1, sum_n p_n<=1/3, so p_0>=2/3. Countable finite atom locations and a finite continuous component give finite samples almost surely; X>=1 precludes renewal accumulation. For each d>0 the continuous component has zero mass in dZ, hence the whole law has mass at most 1-p_0<1 there. Since p_na_n=2^(4^n-2^n) tends to infinity, the expectation of this nonnegative law is infinite.

The submitted Tonelli identity is sound. X_j times 1{K_n>j} has expectation (1-q_n)^(j-1) M_n, because the first j-1 draws are failures and the jth draw contributes X_j times its own failure indicator. Summing gives M_n/q_n. The hit type has mass p_n/q_n. The proof correctly uses a union bound without assuming independence between the preceding sum and hit type. If T_n<=t_n and the first threshold hit has length a_n>t_n, all preceding sums are <=t_n and that hit ends strictly after t_n, including T_n=t_n. Thus the source's strict-after convention indeed yields D_(t_n)=a_n. The estimates q_n-p_n<=p_n^2/(1-p_n), M_n<=a_(n-1), q_n>=p_n imply the displayed vanishing error with exponent 1+2^n-3*4^(n-1).

An independent **geometric-count** proof avoids the expectation/Markov step entirely. Every failure before K_n has length at most h_n=a_(n-1). Put L_n=floor(t_n/h_n)+1. If K_n<=L_n, then T_n<=(L_n-1)h_n<=t_n. Therefore

P(D_(t_n)!=a_n) <= (q_n-p_n)/q_n + P(K_n>L_n)
                    <= p_n/(1-p_n) + (1-q_n)^L_n
                    <= p_n/(1-p_n) + exp(-p_n L_n).

Here p_n L_n>p_n t_n/h_n=2^(3*4^(n-1)-2^n-1). For n>=2, the exponent is at least 2^n-1 and tends to infinity; the geometric error consequently tends to zero. This supplies the same universal concentration input through a different deterministic bound on the preceding sum and a direct geometric tail.

For any eventually finite nonzero deterministic scale, the normalized subsequence is equal to c_n=a_n/phi(t_n) with probability tending to one. If it has a proper weak limit, its tightness and intersection with the high-probability equality event bound c_n eventually in a compact interval. A convergent c_n subsubsequence then forces the same weak limit to a single point mass, using bounded continuous test functions. This excludes all proper nondegenerate laws, including mixtures with an atom at zero, and does not require monotonicity, continuity or divergence of phi. It does not exclude degenerate limits or classify laws admitting scales.

At t_n, the lower support is strictly below t_n and the upper support is strictly above it, so m(t_n)=M_n+t_n q_n exactly. Its ratio to a_n tends to zero by the displayed bound. On the same event of probability tending to one, D_(t_n)/m(t_n)=a_n/m(t_n) tends to infinity. This proves failure of proper tightness for the proposed truncated mean along the inspection times. The zero delay is admissible, and N_t in this example is always >=1, avoiding the arbitrary-delay X_0 convention.

## Findings and remaining gates

No central mathematical gap was identified in the root initial read. The submitted SOURCE_GATE cites the Angus–Ding article number as 108747, whereas the current primary publisher listing and author's record give 108745. This is a bibliographic defect in historical source prose, not a dependency of the elementary counterexample; correct the current audit/preprint references globally while preserving the original 18 historical files. The original primary PDF binary remains inaccessible; current indexed institutional text supplies the exact relevant hypotheses and Problem1.2, and the publisher authenticates the article's metadata but only provides a subscription preview. Do not claim full original visual inspection or a line-by-line preprint/published comparison.

Mathematical acceptance remains pending completion and independent root verification of both fresh families, plus current manifest/source authentication. No priority, merge, preprint or publication acceptance is inferred. The original author count remains 1/5. Root mathematical verification estimate 45%; PR316 workflow estimate 15%; estimates concern completed audit work, not truth probabilities.
