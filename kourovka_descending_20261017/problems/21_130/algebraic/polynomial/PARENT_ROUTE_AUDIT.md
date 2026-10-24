# Independent audit of the parent algebraic/probabilistic route

Audited at 2026-10-24T19:36:02Z. Best-guess full-goal completion estimate remains **8%** for this subroute; this audit adds confidence, not full-scope coverage. Read-only target: `../PARTIAL_RESULTS.md`.

**Verdict:** no substantive error found in the first-moment, canonical-event local-lemma count, or large-least-prime-factor rectification arguments as written. The imported random-injection negative-dependency theorem itself is not independently reproved here; the audit checks that the construction fits its described canonical-event framework.

Checks:

1. With Q=n(n−3)/2 disjoint template-edge pairs, there are 8 maps per template/target edge-pair pair. A template vertex belongs to 2(n−3) template pairs, hence at most 16(n−3)T bad events. A target vertex a belongs to R_a equal-color edge pairs, hence 8QR_a bad events. For an event with four domain and four image points, the support-overlap closed-neighborhood bound 64(n−3)T+32QR is valid, with permissible overcounting. A supergraph of a negative-dependency graph remains valid since it imposes the condition on fewer nonneighbor subsets.
2. Multiplying this neighborhood bound by p=1/(n)_4 and canceling n−3 for n≥4 gives (64T+16nR)/(n(n−1)(n−2)). The coarse bounds on T and R give the stated 32e(r−1)<n−2 sufficient condition. Both counts use edge color classes being matchings, which holds by cancellation in any abelian group.
3. The rational-span contradiction is valid: choose a full-rank q×q row minor; Cramer's rule clears every rational row coefficient by its nonzero determinant d. Thus d(e_i−e_j) is an integer combination of relation rows. Hadamard gives |d|≤2^q≤2^(n−1), so every prime dividing |G| being greater than 2^(n−1) implies gcd(d,|G|)=1. Multiplication by d is injective on finite G, contradicting a_i≠a_j.
4. The finite union of coordinate-coincidence hyperplanes cannot cover the rational nullspace; this produces a rational labeling preserving every original equal-sum edge relation. The displayed parity-chain graph is a single cycle for n≥3. Its skip-one edge sums increase strictly between the two end-edge sums; this remains correct at n=3 and n=4.
5. The first-moment probability 4/((n−1)(n−2)) is correct also for n=4, where it is 2/3. Directed-cycle contraction avoids treating an unoriented two-block cycle as an ordinary cycle count.

All these methods leave their declared boundary cases unresolved: dense color classes/small prime factors. No universal extension follows merely from the audited formulas.
