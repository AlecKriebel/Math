# Independent first assessment — frozen before candidate access

UTC: 2026-10-04 14:53:48. Completion estimate: 15% of this adversarial classical-priority audit.

I have not read the candidate, other reviewer reports, or any primary renewal source yet. I will review the classical route alone and decline candidate access unless a later mathematical need appears. The supplied task statements are hypotheses to check, not findings being adopted.

## Exact target and success criteria

Let X be strictly positive, finite almost surely, non-lattice, and have infinite mean. For ordinary renewal S_0=0, define N(t)=max{k:S_k<=t} and D_t=S_{N(t)+1}-S_{N(t)}, for all real t>=0. The target asks whether some increasing positive deterministic scale produces a proper nondegenerate weak limit. An adversarial obstruction succeeds if one explicit admissible law rules out every positive deterministic scale, including nonmonotone scales, without assuming a continuous limiting law or omitting mass at zero.

Historical success requires (i) a fully proved implication of a verified old theorem, and separately (ii) actual evidence that an earlier source explicitly answered the later named problem. These are distinct criteria. A corollary of an old theorem is a substantial novelty obstruction even when explicit prior discussion of the later problem is not found. I will not infer global firstness or explicit prior resolution solely from the corollary.

## Independent preliminary mathematical assessment

1. If r(x)=P(X>x), then for x>=t the crossing event with length >x should equal the disjoint union over k of {S_k<=t, X_{k+1}>x}. Strict positivity and x>=t make X_{k+1}>x imply S_{k+1}>t. Thus the exact identity P(D_t>x)=r(x)U(t) appears valid even at x=t and with atoms. Finiteness of U(t) still requires proof.
2. If r is slowly varying at infinity, tends to zero, and U(t)r(t)->1, the identity at x=ct for each c>=1 should imply D_t/t->infinity in probability.
3. If D_t/phi(t) has a proper finite weak limit, tightness together with the preceding escape should force phi(t)/t->infinity, through a bounded-ratio subsequence contradiction. This should hold for arbitrary positive phi, not just increasing phi.
4. Then for any fixed positive a,b, both a*phi(t) and b*phi(t) exceed t eventually. Slow variation implies the ratio of their survival probabilities tends to one. At positive continuity points of the limit distribution, all limiting survival values must be equal. Properness at infinity should force that constant to be zero, hence the limit is zero almost surely. This argument needs a careful choice of continuity points, especially when there are atoms and mass at zero.
5. The original theorem must cover the slowly varying (alpha=0) endpoint, not only regular variation with 0<alpha<1; it must cover ordinary renewal counting and the stated positivity hypotheses. The theorem's normalization, strict/weak renewal endpoints, and any arithmetic hypothesis must be inspected in the original article.

## Potential falsifiers and gaps at freeze

- Failure of the alpha=0 renewal asymptotic, or a different U convention not asymptotically interchangeable.
- A slowly varying tail example failing positivity, infinite mean, non-lattice, or finite-a.s. hypotheses.
- A proper weak limit that retains a positive atom but evades survival comparison because only continuity points may be used.
- An oscillating scale that evades the tightness contradiction.
- Confusing an exact old-theorem corollary with documentary evidence of a prior author explicitly solving Thorisson's named problem.

The explicit tail r(t)=1/(1+log t), t>=1, appears promising for an elementary verification but its renewal asymptotic remains unproved at this freeze. No central difficulty has yet been transferred to an unsupported claim; authenticating or independently proving that asymptotic is the main next task.
