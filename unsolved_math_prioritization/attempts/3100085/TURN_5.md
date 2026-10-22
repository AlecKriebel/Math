# Turn 5: exact all-row exclusion through outer span twelve

**Five-turn final scoped result. The unbounded-span existence question remains unresolved.** Applying Turn4's analytic reduction gives an exact finite proof for all binomial rows whenever the outer span is at most12. No search over increasing n is used.

## Theorem

For every integer n>=0 and p in(0,1) with p!=1/2, two equal-probability pairs on four distinct support indices, if they exist, must have outer span at least13. In particular:

- No example with rational odds p/(1-p) can have n<8192
- No rational-odds example occurs in a Mersenne row n=2^a-1 with1<=a<=20

These are scoped exclusions, not a resolution for arbitrary n and p.

## 1. Exhaustive analytic reduction, not a larger row scan

Turn4 proves that after reflection to odds q<1 every candidate has positive u<v and s=r-u-v, with

 0<=A<=max(r-1,floor((r^2-1)/(6(v-u)))+1)-2.

For each such A, an integer solution is possible only when

 P_r(A)^s<P_s(A+u)^r.                                         (1)

If(1) holds, the corresponding equation

 D(B)=P_r(A)^s P_s(B+v)^r-P_r(B)^s P_s(A+u)^r=0                 (2)

has exactly one real root B>A. These are necessary and sufficient equations for the two positive-probability ties at the specified parameters.

For3<=r<=12, the stated finite A ranges contain exactly938 tuples(r,u,v,A). Exact integer comparison(1) rejects879 of them. The remaining59 each receive an adjacent-integer root bracket in TURN_5_CERTIFICATES.json. For every certificate the verifier checks

 A<=L<U=L+1,
 D(L)>0,
 D(U)<0.

By Turn4's uniqueness theorem, the only possible real root lies strictly between these adjacent integers. No integer B exists in any of the59 cases. The maximum recorded endpoint is2240; it is an output of exact root isolation, not a preassigned n cutoff. Every excluded larger B is covered by the monotonicity proof, not by extrapolation from the endpoints.

The verifier independently reconstructs all938 finite A cases, checks the exact sign gate, and verifies that the certificate lists all and only the59 survivors. It does not trust the generator's candidate list. All calculations use integers; there is no floating-point root tolerance. The generator uses exact doubling and bisection, with termination proved in Turn4. The coefficient arithmetic is modest: the full generation took only a small fraction of a second in this execution, but the proof does not depend on machine timing.

This proves the all-n outer-span theorem, provided the complete analytic reduction and exact certificates are independently audited as requested.

## 2. The rational-odds consequences

If q is rational and a pair has span r, Turn1 proves r<=floor(log2 n), by comparing any nonzero prime valuation with the maximum valuation of a binomial coefficient. The first part now gives r>=13 for any two-pair collision. Consequently n>=2^13=8192.

For a Mersenne row n=2^a-1, the credited Farhi formula from Turn3 gives e_2(n)=0. If1<=a<=20, then n+1=2^a<3^13. Every odd prime therefore has e_ell(n)<13 as well. The divisibility root K_13(n) is1. Turn3's rational-odds criterion excludes any collision in those rows. This applies, for example, at n1048575 without enumerating that row or its pairs. It does not exclude irrational-odds examples in those large rows.

## 3. Precisely what remains open

The original Galvin question asks whether any biased binomial row admits two distinct equality pairs. This work has neither an example nor a proof excluding every outer span. Surviving possibilities require span>=13, the biased nesting orientation, the finite left-tail cutoff for their particular span, the unique-root integer condition, and the small-prime divisibility constraints. Those restrictions do not jointly give an all-span contradiction.

Five genuine author turns are complete. The earlier branch-name-only artifact did not contain a recoverable proof turn; the uncertainty about vanished uncommitted work remains in PRIOR_GATE.json. No sixth author search is proposed. Subsequent work is independent review, correction with preserved provenance if required, and accurate scoped publication under the parent gate.

Known inputs, including the row-LCM identity and squarefree-row boundary, are credited. The original author-maintained problem page and the complete upstream OPEN-TRIAGE research record were checked. No historical novelty certification, new tree-independence-polynomial classification, or human peer-review claim is made.
