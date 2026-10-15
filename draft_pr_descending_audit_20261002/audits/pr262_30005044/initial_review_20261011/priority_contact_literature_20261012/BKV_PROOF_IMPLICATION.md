# What BKV's existing ray proof implies

Authored independently by the contact-literature priority family, 2026-10-12 UTC. This is an audit derivation, not a new paper. Input: fresh published Bartha–Komjáthy–Valesin (BKV), *Degree-penalized contact processes*, 85 pages, DOI 10.1017/fms.2025.10144, SHA256 `320fea7622aadb9658130c5ebad7dba12bef171bbf379400c625f45c19f59922`. Exact source: Definition 3.1/equation (19), p.17; Definition 6.1 and Proposition 6.2/proof, pp.46–48, equations (100)–(107). Do not substitute the unavailable historical BKV hash.

## Published statement and interpretation boundary

Proposition 6.2 states positive global survival of the down-directed process for weak power-law offspring tail exponent alpha, P(D>=1)=1, max penalty f(x,y)=max(x,y)^mu, and alpha+mu<1, for any positive lambda and almost all trees. The published proposition does not repeat the section introduction's mu>=1/2 restriction. The zero-penalty case mu=0 is therefore directly inside the published statement and proof. The 2023 arXiv v1 proposition, pp.39–41, does explicitly restrict mu to [1/2,1); candidate alpha=1/4 is covered there by mu=1/2, and monotonicity transfers to classical rates.

Global survival as an abstract conclusion does not imply explosion. In this particular proof, the degree growth and the first-arrow race give more. BKV does not state a simultaneous finite-time explosion theorem in Proposition 6.2. The derivation below is an immediate proof corollary with an explicit timing and memoryless recovery addendum. It must be credited as such; saying only that BKV is a related survival method understates the prior-proof overlap.

## Selective implementation of BKV's exploration

Choose their constants 1<s1<s2 and epsilon>0 so that

    gamma = 1-alpha*s1-epsilon*s1 > 0,
    delta = gamma-mu*s2 > 0,
    epsilon < alpha*(s2-s1)/(s2+s1).

At the current ray vertex with offspring L>=K, BKV's A1 event supplies at least L^gamma/4 children with offspring in [L^s1,L^s2], up to harmless integer rounding. Keep a deterministic number of these eligible children, and implement their allowed choice of an infected child by the FIRST arrow to this set. Inspect no recovery marks after that arrow.

Let S_m be arrival time at v_m; take S_0=0 and the positive-probability event that the root's offspring is at least K rather than searching for a later high-degree vertex. On A1, the total rate R_m to the inspected children satisfies

    R_m >= c_mu*lambda*L_m^delta,
    L_m >= K^(s1^m),

where c_mu>0 is constant. To repair the paper's occasional use of offspring D in place of graph degree d=D+1 and nonintegral child counts, one may take c_mu=2^(-mu)/8 for sufficiently large K. Root degree is L_0 and later graph degrees are L_m+1; the inequality d_u<=2L_m^s2 absorbs this distinction. These finite factors do not change delta or summability. For mu in [0,1], c_mu>=1/16 is convenient.

The first arrow wait W_m has law Exp(R_m), independent of the vertex's first recovery wait H_m~Exp(1), conditionally on the selectively exposed tree/ray history and the eligible degrees. Stage success is W_m<H_m. The winning child identity may depend on the eligible degrees and on arrow clocks, but this does not expose that child's outgoing clocks or its recovery after arrival. The unused descendants and outgoing clocks keep their conditional product laws. The ray event A includes A1 and W_m<H_m at every finite stage. The existing BKV bounds (101),(102),(104)–(107) show P(A)>0 for K large.

## Finite traversal time follows from the existing rates

Let I_m record that exploration reaches stage m and that A1 holds there. Treat failed/later unreached contributions as zero. The conditional race calculation is

    E[W_m*1{W_m<H_m} | history, eligible set]
      = integral_0^infinity t R_m exp(-(R_m+1)t) dt
      = R_m/(R_m+1)^2 <= 1/R_m.

Consequently

    E[sum_m (m+1) I_m W_m 1{W_m<H_m}]
      <= (c_mu*lambda)^(-1) sum_m (m+1) K^(-delta*s1^m)
      < infinity.

Tonelli's theorem gives sum_m(m+1)W_m<infinity almost surely on A. Hence S_m=sum_{j<m}W_j increases to S_infinity<infinity on A. Every S_m and every infection path to v_m uses only finitely many arrows. This establishes cumulative finite-time spread, but we still must check simultaneous infections.

## Residual recoveries give simultaneity on the same ray event

At stage m, conditional on W_m=w, stage success H_m>w, winning child and the past selective history, the recovery residual E_m=H_m-W_m has Exp(1) law. It is independent of w and of the winning child. The elementary factorization is

    P(H_m>w+z | H_m>w,W_m=w) = exp(-z).

More formally, the local joint density of successful wait w, winner i and residual z factors as an arrow/winner term times exp(-w)dw times exp(-z)dz. Later ray choices use only descendants and never return to v_m in the down-directed process; they do not inspect E_m. Finite-stage induction therefore makes the E_m iid Exp(1), independent of the entire selective ray skeleton, including A, degrees, successful waits and winners. This remains valid at the countable limit by cylinder events. It would be false to condition on full contact-process history containing these residual marks; that larger sigma-field is deliberately not used.

Given this skeleton on A,

    sum_m (S_infinity-S_(m+1))
      = sum_{j>=1} j W_j < infinity.

The probability that v_m has its first recovery between its outgoing arrow at S_(m+1) and S_infinity is

    1-exp(-(S_infinity-S_(m+1)))
      <= S_infinity-S_(m+1).

Conditional Borel–Cantelli shows that only finitely many ray vertices have recovered during these residual intervals. Thus ALL BUT FINITELY MANY v_m are simultaneously infected at S_infinity almost surely on A. For each such v_m the root-to-v_m path consists of finitely many successful arrows and recovery-free vertical pieces; it then remains vertical to S_infinity. These are exactly finite paths admitted by equation (19), or increasing finite-ball restrictions. No infinite path itself is traversed as a single infection path, no infection originates at infinity, and no post-explosion strong Markov restart is used.

An alternative, weaker conclusion is available without the weighted sum: at any fixed h with S_infinity<h, conditional survival indicators 1{E_m>h-S_(m+1)} are independent, with probabilities at least exp(-h)>0 when S_0=0. Their sum is infinite almost surely. Therefore P(|X_h|=infinity)>=P(A and S_infinity<h). Since A has positive probability and S_infinity is finite on it, at least one deterministic integer h has strictly positive explosion probability. By choosing K larger and using the unweighted wait expectation bound, this can also be arranged before any prescribed positive horizon, but no candidate-specific numerical lower bound follows from BKV's stated constants.

## Almost-every-tree and every-rate boundary

The direct argument above establishes positive annealed explosion probability. BKV's proposition states an almost-every-tree survival conclusion, but that statement alone cannot replace a quenched explosion proof. A short hereditary argument supplies the latter for the candidate's offspring law (and the analogous positive-offspring weak power-law class): if a child subtree has positive probability of finite-time explosion from its root, a finite initial infection path to that child and future independent marks give positive probability from the original root. This uses finite times only. The root's removed parent edge changes only finitely many initial rates, which remain positive, and does not alter the zero/positive status. If q is the probability of a bad tree, independence gives q<=E[q^D]. Annealed positivity implies q<1; D>=1 and P(D>=2)>0 imply E[q^D]<q for q in (0,1). Hence q=0. Countable rational rates and graphical monotonicity give one full-measure set with positivity for every lambda>0. No uniform quenched time or probability is produced.

## Priority conclusion

1. Published theorem statement: global survival, not an explosion theorem.
2. Valid immediate proof corollary: simultaneous finite-time explosion with positive probability, in the candidate's model, follows from the existing growing-degree ray proof plus the explicit short timing/residual-recovery argument above.
3. Stronger deterministic recovery-window construction: not needed for that existential conclusion. The candidate uses it to give an elementary explicit deterministic horizon and lower bound.
4. Candidate-specific content: tail m^(-1/4), D_n=16^(n+2), deterministic horizon 1/(2lambda), and lower bound (7/30)exp(-3/(2lambda)) are not stated in BKV's examined proposition/proof. Absence from the examined source is not proof of novelty elsewhere.
5. Quenched every-rate assertion: readily derivable by hereditary zero-one and monotonicity; it should not be advertised as a major new feature without a broader priority basis.
6. Credit: describe the existence result as an explicit quantified consequence/specialization of BKV's established infection-ray argument; retain the distinction between their published statement and this derivation. A claim to newly solve the existential mechanism or to introduce a new ray method would be misleading.

Independent adversarial verification of the selective-conditioning step is recorded separately in the owned `timing_adversary` folder. This report was frozen before reading any other priority-family outputs.
