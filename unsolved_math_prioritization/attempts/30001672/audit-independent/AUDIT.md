# Independent adversarial audit: Boolean coalition influence

Problem 30001672, OWR-4791-032, rank 619. Audit date: 2026-10-04 UTC.

## Verdict

**PASS. The recorded question has an existing negative resolution.** The frozen author packet correctly reduces the original question to Theorem 1.1 of Kahn--Kalai (2013), also published as Theorem 1.1 of Bourgain--Kahn--Kalai (2024). No new mathematical discovery is claimed. No substantive correction to the author proof is required.

The mathematical recommendation is to accept `already_solved`, with outcome `negative`, preserving the attribution and the distinction between a proof using an existing theorem and a new independent theorem. This audit makes no recommendation about administrative publication requirements or unrelated repository checks.

Reviewed author-manifest SHA-256:

`ff5e02d9d7dc9d20ee690b6b523de26e2bbb54cd852680d9c310bac7963b635b`

Every listed author file matched that manifest before and after the audit. The frozen files were neither edited nor overwritten. All computations and this report are separate from that packet. No remote writes were performed.

## 1. Original target and quantifiers

I independently inspected the publisher's original report, including the rendered printed pages 75--76 (PDF pages 71--72). It defines influence as the probability that uniformly and independently fixing the variables outside S leaves both possible outputs available. It asks whether an absolute c in (0,1) guarantees influence at least 1-c^n for a set of at most n/3 variables. The mean may be merely bounded away from 0 and 1; exact balance is not required. There is no monotonicity assumption. The suggested other fractions are fixed fractions below 1/2. [Original report, pp. 75--76](https://ems.press/content/serial-article-files/46314#page=71).

Thus it suffices to find one fixed nondegenerate mean and arbitrarily large dimensions in which every permitted coalition fails the exponential guarantee. Exactly balanced examples are stronger than needed. Even allowing c to depend on a fixed lower bound for the distance of the mean from 0 and 1 would not rescue the conjecture: the counterexamples all have mean 1/2.

The dimension must tend to infinity. Small-dimensional counterexamples or successful controls alone would not prove this status. The author does use an asymptotic construction, not finite evidence as a substitute.

## 2. Published dependency: what was actually checked

I read the definitions, Theorem 1.1, Lemmas 3.1--3.2, and its proof in the 2024 paper. The theorem explicitly quantifies over all sufficiently large n and all coalitions of size at most (1/2-delta)n. Its proof starts above the desired mean and removes 1-inputs, preserving the one-sided upper bound. I also independently read the 2013 theorem and corresponding proof. Its exact-size formulation extends to smaller coalitions by containment. [Bourgain--Kahn--Kalai, pp. 2, 6--8](https://toc.cs.uchicago.edu/articles/v020a004/v020a004.pdf), [Kahn--Kalai, pp. 2, 6--8](https://arxiv.org/pdf/1308.2794).

The published statement for arbitrary real alpha formally requires the usual realizability qualification, since a Boolean function on a finite uniform cube has dyadic mean. This does not affect alpha=1/2, which is exactly realizable in every positive dimension. The proof's deletion step is valid for this specialization. In particular, replacing an approximately balanced function by an arbitrarily modified exactly balanced function would be unsafe, but that is not the argument used.

The 2013 displayed inclusion comparison contains an obvious repeated-function typographical error in the bound after the support inclusion. The 2024 version has the correct comparison between the two functions. The inequality itself follows immediately from inclusion of the sets of reachable outside assignments, independently of either typography.

The substantive theorem dependency is the existence of one fixed C and a family f_n such that, for all sufficiently large n,

- E f_n = 1/2;
- J_S^+(f_n) <= 1-n^(-C) simultaneously for all |S| <= floor(n/3).

This follows by alpha=1/2 and delta=1/6. Weakening the paper's strict inequality to a weak one is harmless. Enlarging the fixed exponent preserves the bound and allows C>0. All the relevant quantifiers are in the correct order: C is independent of n, the coalition S, and the proposed exponential base c.

## 3. Complete application proof

For an outside assignment u, let A mean that the fiber contains an input with value 1, and B mean that it contains an input with value 0. Every fiber is nonempty, so A union B has probability one. Write J_S^+=P(A), J_S^-=P(B), and U_S=P(A intersection B). Inclusion--exclusion gives

U_S = J_S^+ + J_S^- - 1 <= J_S^+.

The paper's shifted quantities satisfy I_S^+=J_S^+-E f and I_S^-=J_S^--(1-E f), so I_S^++I_S^-=U_S. Neither shifted quantity alone is the original influence.

Consequently the cited f_n satisfy U_S(f_n) <= 1-n^(-C) for every permitted S. Given any c in (0,1), put a=-ln c>0. Since ln n/n tends to zero, C ln n<a n for all sufficiently large n. Exponentiation gives n^(-C)>c^n. Therefore

U_S(f_n) < 1-c^n

for every permitted S, contradicting the proposed guarantee. More explicitly, for every proposed c and every starting dimension N, one can choose n>=N above the construction and comparison thresholds, and then no S of the allowed size works.

Coalition monotonicity is also elementary. For S contained in T, any input from which output 1 is reachable by changing S still has output 1 reachable by changing T. Taking uniform input probabilities yields J_S^+<=J_T^+. The outside-assignment and full-input formulations agree because all fibers for a fixed S have the same cardinality. Thus a theorem stated only for sets of size floor(n/3) still controls all smaller sets.

For any fixed r in (0,1/2), delta=1/2-r gives the same refutation for size at most rn. This makes no claim at r=1/2 and no optimality claim about the polynomial exponent.

## 4. Exact balance and explicit parameter audit

Here is a complete specialized derivation of the needed construction, using the existing random-clause idea. It is included to expose constants, rounding, and balancing, rather than to claim a new construction or a reproof of every result in either paper.

For large integer n, set

- s=floor(n/3);
- k=ceil(6 log_2 n);
- q=2^(-k);
- b=ln(4/3);
- m=floor(b/q).

Eventually 1<=k<=n-s. Independently choose m clauses. Each clause is a disjunction of literals on a uniformly chosen k-subset of the n coordinates; independently and uniformly choose its literal signs. Let g be their conjunction.

### 4.1 A clause misses every proposed coalition

For fixed S of size s, a random clause avoids S with probability

p_n = binom(n-s,k)/binom(n,k).

Writing this ratio as a product of k factors shows p_n=(2/3)^k(1+o(1)). To justify the relative error, n-s=(2/3)n+O(1), and each factor's logarithmic error is O(k/n), so the total is O(k^2/n)=o(1).

Since m=(b+o(1))2^k,

m p_n = (b+o(1))(4/3)^k.

The exponent 6 log_2(4/3) is strictly greater than 1; an exact check is (4/3)^6=4096/729>2. Hence m p_n/n tends to infinity. For each fixed S, the probability no clause avoids S is (1-p_n)^m<=exp(-m p_n). There are at most 2^n sets S. The probability some size-s S has no avoiding clause is at most exp(n ln 2-m p_n), which tends to zero.

If an avoiding clause exists, exactly a q fraction of outside assignments falsify it. For those assignments, every completion inside S makes g zero. Therefore J_S^+(g)<=1-q. The same bound holds for smaller S either by extension to size s or by the coalition monotonicity proved above.

### 4.2 The mean is above 1/2 with high probability

Let X=E_x g(x), where the expectation is uniform over inputs and the randomness of X is the random clauses. Each fixed input satisfies a clause with probability 1-q, so E X=(1-q)^m tends to exp(-b)=3/4.

A direct second-moment check avoids treating concentration as an unexplained black box. For inputs x,y that agree on t coordinates, put

r_t = binom(t,k)/binom(n,k), with binom(t,k)=0 when t<k.

A clause fails on both inputs with probability q r_t: its support must lie inside the agreement set and its signs must be the unique falsifying signs there. Thus the probability both inputs satisfy a clause is 1-2q+q r_t. Independence of the m clauses gives

E X^2 = E_T (1-2q+q r_T)^m,

where T is a binomial random variable with parameters n and 1/2.

For T<=3n/5, the product formula gives r_T<=(3/5)^k. Hence

(1-2q+q r_T)^m / (1-q)^(2m)
 <= exp(m q (3/5)^k/(1-q)^2) = 1+o(1),

because m q tends to b and (3/5)^k tends to zero. For T>3n/5, the integrand is at most 1. Since Var T=n/4, Chebyshev's inequality bounds the probability of this tail by 25/n. It follows that

E X^2 <= (E X)^2(1+o(1)) + 25/n.

Nonnegativity of variance gives Var X=o(1). Since E X tends to 3/4, Chebyshev again yields P(X<=1/2)=o(1).

Both this mean event and the coalition-avoidance event hold with probability tending to one, so there is a g satisfying both for every sufficiently large n. No independence between those two events is assumed or needed.

### 4.3 Delete 1-inputs to obtain exact balance

Such a g has more than 2^(n-1) 1-inputs. Choose any subset F of g^(-1)(1) of exactly that cardinality and let f be its indicator. Then E f=1/2 exactly. For each outside assignment, reachability of output 1 under f implies reachability under g, so J_S^+(f)<=J_S^+(g)<=1-q.

This argument does not assume that U_S itself decreases under support deletion: that assertion is false. Its safety comes from retaining the J^+ obstruction and only then using U_S<=J_S^+.

The ceiling in k gives q>(1/2)n^(-6). For n>=2 this is at least n^(-7), with strict inequality in the resulting comparison. Thus the specialized construction provides the convenient fixed bound

J_S^+(f) <= 1-n^(-7)

for every |S|<=floor(n/3) and every sufficiently large n. The exponent 7 is a safe rounded audit bound, not an optimal rate or an attribution of this exact numerical exponent to the published theorem.

### 4.4 Cross-check against the published lemma hypotheses

The paper's log means log_2. With delta=1/6, its suggested multiplier 1/delta is 6. The first lemma needs k=o(sqrt n) and (2/3)^k m=omega(n), both verified above. Taking xi=0.1 in the second lemma gives an exponentially small quantity compared with the limiting positive mean, and m(0.3)^k=O((0.6)^k)=o(1). Thus neither lemma is being invoked outside its parameter range. Integer rounding only changes fixed factors, covered by the exponent 7 above.

## 5. Computational checks and adversarial counterchecks

The frozen verifier's run function was invoked without its writing entry point, with bytecode generation disabled. Its returned object exactly equaled the frozen control-results object. All 1,050,698 function--coalition pairs in dimensions 0 through 4 passed. See `replay_results.json` and the reproducible `replay_frozen.py`.

A separately written implementation, `independent_checks.py`, uses direct counts on outside-coordinate projections instead of the frozen bitset-fiber algorithm. It checks all the same function--coalition pairs, both one-sided upper bounds, the influence identity, the shifted normalization, and monotonicity under coalition inclusion. It additionally exhausts support-inclusion pairs through dimension 3 to test that shrinking 1-support cannot increase J^+; records the deliberate counterexample to the analogous false claim about U; and checks the single-clause joint-success formula exactly for every dimension 1 through 6, every clause size, and every Hamming distance. See `independent_results.json` for exact totals.

These are controls of definitions, arithmetic, and proof mechanisms. They are not numerical proofs of asymptotic existence, concentration, or polynomial-versus-exponential domination. The latter assertions are proved symbolically above.

## 6. Corrections and remaining scope

Required mathematical corrections: **none**.

Optional presentation improvements to the author packet:

1. Add one sentence explaining that the theorem obtains exact balance by constructing at a higher limiting mean and deleting 1-inputs. This directly addresses a natural reader objection.
2. If desired, link the original publisher PDF without the optional query parameter; that direct URL was independently readable during this audit.
3. Keep the already present caveat that the proof is a reduction to existing literature. Do not describe finite controls as verification of the infinite construction or claim optimality of C.

The general dyadic-mean convention and the 2013 typographical comparison are source-level cautions, not gaps in the exactly balanced specialization. The full theorems for all parameters, the separate second construction, and all results of the papers have not been independently reproved. The theorem-dependent application in section 3 is complete; section 4 separately supplies a complete specialized construction check sufficient for this exact target.

## Sources and portable boundary

- Original report: [publisher record](https://ems.press/journals/owr/articles/4791), [PDF, pp. 75--76](https://ems.press/content/serial-article-files/46314#page=71), DOI 10.4171/OWR/2011/01.
- Kahn and Kalai, *Functions without influential coalitions* (2013): [arXiv record](https://arxiv.org/abs/1308.2794), [PDF](https://arxiv.org/pdf/1308.2794).
- Bourgain, Kahn and Kalai, *Influential Coalitions for Boolean Functions I: Constructions*, Theory of Computing 20(4) (2024), 1--13: [publisher record](https://toc.cs.uchicago.edu/articles/v020a004/), [PDF](https://toc.cs.uchicago.edu/articles/v020a004/v020a004.pdf), DOI 10.4086/toc.2024.v020a004.

The portable audit consists only of this newly written report, validation code/results, and the manifest. It contains no source PDFs, scans, full-text extracts, dataset corpora, credentials, or private coordination records. Bibliographic links identify the sources without redistributing them.
