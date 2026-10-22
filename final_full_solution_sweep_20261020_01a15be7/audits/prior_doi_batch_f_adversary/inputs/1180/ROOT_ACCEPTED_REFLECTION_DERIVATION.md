# Backward barriers from an earlier bounded-dimension sieve

This is an independently authored transfer argument for the bounded priority audit. It does not assert that the forward theorem alone implies the backward theorem, that the same witnesses work, or that the earlier authors printed this corollary.

## Published input actually used

Tao–Teräväinen, *Quantitative correlations and some problems on prime factors of consecutive integers*, arXiv:2512.01739v2 (25 April 2026), Section2, printed pp11–23, constructs a nonnegative finite sieve weight nu_+(n) on the integer interval I=[x,2x]. Its parameters are K=floor(log log x/C0), w=sqrt(log x), W=product_{p<=w} p^2, and R_r=x^(100^(-r)). The weight is

    nu_+(n) = 1_I(n) 1_{W|n}
               product_{r=1}^K (sum_{d|n+r} a_r(d))^2,
    a_r(d) = mu(d) tilde_eta(log d/log R_r),

where d has no prime factor <=w and a_r(d)=0 for d>R_r. The fixed real smoothing function is bounded. The published conclusions needed are its normalization (2.23), Z_+=sum nu_+=x^(1-o(1)), and divisibility axioms(i)–(iv) on pp12–13. These are identified established analytic inputs, not consequences of the disputed Lau proof. The full Section2 text was read here; the antecedent standard analytic literature is not re-proved.

## Finite reflection lemma

Define nu_-(n) by replacing every n+r in the weight by n-r; n-r>0 throughout I for sufficiently large x. For any finite list (q_j,k_j), define

    S_+ = sum_{n in I} nu_+(n) product_j 1_{q_j|n+k_j},
    S_- = sum_{n in I} nu_-(n) product_j 1_{q_j|n-k_j}.

Expand the K squares. A fixed divisor configuration imposes W|n and congruences n=-r modulo [d_r,d'_r], together with n=-k_j modulo q_j, in the plus system. The minus system negates every residue. They have the same compatibility conditions: a solution maps to its negative. If compatible, each is exactly one residue class modulo the same least common multiple. In any interval of consecutive integers, counts of two residue classes modulo one modulus differ by at most one. Incompatible systems both count zero. This holds for arbitrary noncoprime moduli and arbitrarily large prime powers.

Let M=max(1,sup_{u>=0}|tilde_eta(u)|). Each expansion coefficient has modulus at most M^(2K), and the number of configurations is at most product_r floor(R_r)^2. Consequently, uniformly in the whole list of imposed divisibility conditions,

    |S_--S_+| <= B_x := M^(2K) product_r floor(R_r)^2
                       <= x^(2/99+o(1)).                 (1)

Only a coefficient absolute sum is bounded; signed main terms are never ordered. Taking the list empty gives |Z_--Z_+|<=B_x. Since Z_+=x^(1-o(1)), Z_->0 and Z_-=x^(1-o(1)). Each weight is nonnegative. Thus 0<=S_+<=Z_+, and ordinary fraction subtraction gives

    |S_-/Z_--S_+/Z_+| <= 2B_x/Z_-
                       <= x^(-97/99+o(1))
                       <= x^(-.95)                      (2)

for all sufficiently large x, after absorbing constants. No equality of the two distributions or of individual witnesses is asserted.

## Transfer of the source axioms

Use the same fixed C0 as in the earlier proof and only query 1<=k<=floor(log x), so all n-k are positive on I.

* Axiom(i), n in I and W|n, holds exactly for nu_-.
* In(ii), the product of at most four queried primes is <=R_1^4=x^.04. The absolute probability error (2) is therefore negligible even relative to the reciprocal-product main term and its negative power of log x error.
* In(iii), at most two primes are <=R_k<=x^.01. Its product bound (1/q) product(log p/log R_k)^2 is at least x^(-.02)(log2/log x)^4. Hence (2) is negligible relative to this upper-bound scale and can be absorbed into its fixed implied constant.
* In(iv), the probability relation is a higher-power probability minus a rescaled lower-power probability. Every rescaling factor is at most one, so transporting both terms adds at most 2x^(-.95), negligible compared with the permitted O(x^(-.1)). The tiny-prime version, rescaled from second powers, has the same property.

Thus the earlier four axioms hold for nu_- with every n+k replaced by n-k. This is a finite congruence calculation followed by the already-proved moment estimates; no new many-dimensional analytic normalization is needed.

## Union bound and every endpoint

The source's Section2.1 deduction from its axioms uses prime-factor identities, upper bounds for the positive queried integer by 3x, ordinary second/fourth moments, and a summable failure bound 1/(10 k^(3/2)). All apply to n-k, which is positive and at most2x in the queried range. Their union bound therefore supplies, for each sufficiently large x, an n in[x,2x] such that

    Omega(n-k)<=Ck, 1<=k<=floor(log x),

for one absolute C. For floor(log x)<k<n, the deterministic bound

    Omega(n-k)<=log(2x)/log2<= (2/log2)k

holds for sufficiently large x, including n-k=1 with Omega(1)=0. Increase the same C once. Arbitrarily large x give infinitely many distinct n for which the inequality holds for every integer1<=k<n.

Set epsilon=1/C>0. For every positive m<n, k=n-m is an allowed shift and

    m+epsilon*omega(m)<=m+epsilon*Omega(m)<=n.

This answers the exact original existential-epsilon question, including the nearest endpoint. It says nothing about coefficient one. It uses a newly specified elementary reflection of an established proof mechanism; it is not an asserted implication of the bare forward theorem. It bypasses Lau's logarithmic result and all of its contested printed steps.

## Scientific interpretation

The PR's fixed-epsilon conclusion is complete, but no new open-problem mechanism is necessary for it: the established earlier bounded-dimension sieve transfers directly as above. Lau's stronger logarithmic theorem is also already explicitly stated before the PR. The authored repairs may have independent expository or proof-correction value; neither this derivation nor the present bounded review establishes priority or novelty of those repairs. They must be preserved, not called mere partial work. A worldwide historical-firstness claim is not certified here.
