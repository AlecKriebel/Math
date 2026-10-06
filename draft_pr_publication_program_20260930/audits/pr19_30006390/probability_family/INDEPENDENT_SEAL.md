# Independent probability audit: sealed reconstruction

UTC checkpoint: 2026-10-01 17:23:58. Audit-family completion estimate: 25%. Original conjecture completion estimate: no growing-factor lower bound established; this audit does not claim progress toward that missing theorem.

This reconstruction was written after reading only root `AGENTS.md`, the exact-head `source_snapshot/BASELINE.md`, and `source_snapshot/source_records.json`. No historical reviews, author/reviewer scripts, sibling reports, or root conclusions had been read. Exact target head: `f1053196b6405623d5f5d8611289939765918d72`. Baseline SHA-256: `9e0a930e61d849799c4395024c85d4f9c75b63ae2172321ef78ebf643f283c82`. Snapshot contains 13 files.

## Claim and quantifiers

For every finite projective plane of order q, n=q²+q+1 points and lines, take independent point Bernoulli(1/2) variables. Let tau(R) be the minimum size of B contained in R meeting all *nonempty* line sections. The asserted baseline is tau(R) >= q+sqrt(q)+1 and tau(R) <= (1+o(1))q ln(q), with probability tending to one as q tends to infinity through orders for which planes exist. Its elementary probability bounds can be uniform over all planes at a given order. The primary conjecture instead asks tau(R)/q to diverge in probability, potentially at least c ln(q). Neither follows from this baseline. Source records say the original Conjecture 5 restricts q to large prime powers; a proof for every existing projective plane would be stronger and must avoid coordinates or classification.

The nonempty-section convention avoids the impossible requirement of intersecting an empty set. The original all-section convention and this one agree outside the empty-line event, whose probability is at most n*2^(-(q+1)). q is an integer at least 2 in the nondegenerate setting. There is no finite-q guarantee of the displayed high-probability lower bound, nor a claim that its event is nonempty for every tiny q.

## Independently reconstructed checks

1. Empty and whole-line events each have probability at most n*2^(-(q+1)); their union costs at most 2n*2^(-(q+1)). Line events are correlated but a union bound does not require independence. On their complement, B meeting sections is an ordinary blocker, and no B contained in R can contain a whole line. A line-free blocker of k=q+a+1 points satisfies r_L<=a+1 by the q disjoint lines through a point in L outside B. Double counting gives k(k-1)<= (a+1)(k(q+1)-n), whose right-minus-left is q(a²-q). This proves a>=sqrt(q), uniformly for arbitrary planes. It gives only a factor tending to one, not infinity.

2. Put t=sqrt(3(q+1)ln(q)) and s=sqrt(3n ln(q)). Two-sided Hoeffding plus union gives all line sizes in [(q+1)/2-t,(q+1)/2+t] and |R| in [n/2-s,n/2+s], with failure at most 2(n+1)q^-6. Each individual line sum is binomial; independence between different lines is unnecessary. Thus m=(1+o(1))q/2 and |R|=(1+o(1))n/2 uniformly over the plane. For sufficiently large q, m>ln(q+1)>0.

3. Conditional on such R, independently thin its points at rho=ln(q+1)/m. For a fixed line of size r its miss probability is (1-rho)^r<=exp(-rho*m)=1/(q+1). Add one existing R-point from every missed line. Additions may coincide, so cardinality is at most |T| plus the number of missed lines. Linearity of expectation, not independent miss events, gives a realized blocker of size at most |R|ln(q+1)/m+n/(q+1). The explicit deterministic upper bound is [(n/2+s)/((q+1)/2-t)]ln(q+1)+n/(q+1), whose ratio to q ln(q) tends to one. The existential choice from the expectation is valid for each fixed good R; no unjustified claim about high probability over T is needed.

4. For distinct lines, joint empty probability is 2^(-(2q+1)); each marginal is p=2^(-(q+1)), so joint=2p² and covariance=p². This alone defeats literal line independence. For any fixed ordinary blocker B, conditioning on B contained in R ensures all its sections are already hit; multiplying additional per-line failure probabilities would be logically invalid. For an adaptively selected B(R), containment probabilities cannot be assigned as if it were fixed in advance.

5. On the no-empty-line event, tau(R)<=k iff some inclusion-minimal ordinary blocker of size <=k lies in R. Each fixed B contributes exactly 2^(-|B|); union bounding over deterministic minimal blockers proves P(tau<=k)<=n*2^(-(q+1))+W_q(k). The weighted first moment is only sufficient, not necessary. W need not tend to zero when the probability does, because overlapping blockers can create large multiplicity.

6. If, uniformly over planes, W_q(floor(Cq)) tends to zero for each fixed C>0, tau/q diverges uniformly in probability. Diagonalization yields a universal slowly growing f(q) with P(tau/q>f(q)) tending to one. This does not produce f=Omega(ln(q)). For a single plane sequence the same diagonalization works without uniformity, but f may depend on the sequence; the two quantifier scopes must not be confused. The fixed-C estimates themselves remain unproved. Counting all k-subsets costs exp(Cq ln(q)+O(q)), and replacing that family by minimal blockers is not an enumeration theorem.

## Initial verdict and attack plan

No mathematical failure found in the reconstructed probability baseline. The central difficulty remains excluding all ordinary line-free blockers of size Cq from a random half-set for every fixed C. Fresh controls will check explicit failure bounds, conditional dependence, the first-moment multiplicity limitation, and the fixed-C diagonal quantifiers. The upper-bound proof and lower-bound reduction use only projective-plane incidence axioms and therefore require no Desarguesian assumption.

An imported concentration inequality and the source's incidence-deletion comparison still need primary-source verification. Historical evidence and scripts will be inspected only after this seal is saved.
