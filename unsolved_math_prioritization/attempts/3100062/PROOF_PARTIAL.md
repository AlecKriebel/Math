# Fixed-variable Rado boundedness: a valuation-coloring partial

**Review status.** Accepted as a correct partial result by the accompanying independent AI-assisted mathematical audit. This manuscript and audit are unrefereed; no external human peer review, journal acceptance, or formal proof-assistant certification is claimed. The general fixed-arity target remains unresolved here.

## Status and exact question

This is a partial result, not a proof or disproof of Rado's boundedness conjecture. No novelty claim is made for the elementary coloring arguments below. The general coefficient-independent bound remains unproved here. Least-term p-adic noncancellation and leading-unit colorings are classical ingredients in proofs of Rado necessity. The explicit finite-distance/cancellation-depth estimate is an auxiliary derivation in this note; it is not asserted to be previously unknown.

For an integer vector a = (a_1,...,a_n), consider

    E_a: a_1 x_1 + ... + a_n x_n = 0, with every x_i in N = {1,2,...}.

Variables need not be distinct. An r-coloring uses at most r colors. Write c(a) for the least r admitting a coloring of N with no monochromatic solution, and put c(a) = infinity if none exists. Thus a finite c(a) means that the degree of regularity is c(a)-1 (allowing degree zero).

The question is whether the finite values c(a) for vectors with at most n active coefficients have an upper bound depending only on n. Equivalently, is there M(n) such that M(n)-regularity implies partition regularity? This is the common target of 3100062 / AMR-030-0062 and 153 / GREEN-065.

Delete zero coefficients first. This preserves every r-regularity property: a solution of the active equation extends by assigning each dummy variable the value of an active variable, and restriction works in the other direction. The all-zero equation is partition regular. Dividing all active coefficients by their positive gcd, permuting them, and multiplying them all by -1 also preserve every regularity property. In particular, a zero coefficient alone must not be used as a zero-sum witness in the simplified one-row form of Rado's criterion. For example x_1 + 0 x_2 = 0 has no positive solution.

For a nonempty vector of nonzero coefficients, Rado's theorem gives partition regularity exactly when a nonempty subset of coefficients sums to zero. All subsequent coloring results concern the complementary case, so all such subset sums are nonzero.

## 1. A finite-distance coloring lemma

**Lemma 1.** Let D be a finite set of positive integers. There is a coloring g of the nonnegative integers with at most |D|+1 colors such that

    |u-v| in D  implies  g(u) != g(v).

**Proof.** Starting with u=0, assign g(u) the least color in {0,...,|D|} not already assigned to a previous vertex u-d with d in D and d<=u. At most |D| colors are forbidden. Every edge is checked when its larger endpoint is assigned. This constructs the required coloring on the entire infinite domain. No finite-computation extrapolation is involved. QED.

## 2. Uniform bound for separated coefficient valuations

**Theorem 2.** Suppose that for some prime p the n integers

    alpha_i = v_p(a_i)

are pairwise distinct. Then

    c(a) <= |{ |alpha_i-alpha_j| : i<j }| + 1 <= binom(n,2)+1.

This bound is independent of p, the coefficients, and the sizes of the valuation gaps.

**Proof.** Apply Lemma 1 to the positive differences D of the alpha_i, and color x by g(v_p(x)). Suppose x_1,...,x_n are monochromatic and sum_i a_i x_i = 0. If two terms had equal valuation, then

    v_p(x_i)-v_p(x_j) = alpha_j-alpha_i,

so the two variable valuations would be adjacent in the distance graph and would have different colors. Hence all term valuations are distinct. The unique term of least valuation cannot cancel: dividing by its power of p and reducing modulo p leaves one nonzero term. Contradiction. QED.

**Examples.** The vector (1,2,-8) has valuation levels (0,1,3) at p=2. The coloring x -> v_2(x) mod 4 avoids its equation, since its distance set is {1,2,3}. This proves only c(1,2,-8)<=4, not equality. The construction also works for (1,2^H,-2^(2H+1)) for every integer H>=1, with at most four colors even though its valuation gaps are unbounded.

**Exact small arities.** M(1)=1 and M(2)=2. For two active coefficients of the same sign there is no positive solution. Opposite coefficients of equal magnitude give a partition-regular equation. If their magnitudes differ, some prime has different valuations on them, so Theorem 2 gives two colors. Conversely x_1-2x_2=0 has positive solutions, so is 1-regular, but the parity of v_2 avoids monochromatic solutions. Zero coefficients are handled by the initial reduction.

## 3. Uniform bounds with bounded p-adic cancellation depth

Fix a prime p. For every nonempty I contained in {1,...,n}, set

    s_I = sum_{i in I} a_i,
    beta_I = min_{i in I} v_p(a_i),
    kappa = 1 + max_{I nonempty} (v_p(s_I)-beta_I).

The assumption s_I != 0 makes kappa finite, and the p-adic triangle inequality makes kappa>=1. Let A be the set of distinct coefficient valuations, and let t=|A|. Define

    D = { |alpha-beta+e| > 0 : alpha,beta in A, |e|<=kappa-1 }.

This is a finite set of positive integers. It satisfies

    |D| <= (kappa-1) + binom(t,2)(2kappa-1).

Indeed, alpha=beta contributes at most kappa-1 distances; each unordered pair of distinct levels contributes at most 2kappa-1 distances after taking absolute values.

**Theorem 3.** With these definitions,

    c(a) <= phi(p^kappa)(|D|+1)
          <= (p-1)p^(kappa-1) [kappa + binom(t,2)(2kappa-1)].

Here phi(p^kappa)=(p-1)p^(kappa-1). Consequently this is a coefficient-independent bound on any class with bounded number of variables, bounded p, and bounded cancellation depth kappa, regardless of valuation gap sizes.

**Proof.** Let g be the distance coloring of Lemma 1. For x>0 write x=p^v u with p not dividing u. Color x by the pair

    (g(v), u mod p^kappa).

There are at most the claimed number of colors. Assume that a monochromatic tuple satisfies the equation. Put

    w_i = alpha_i + v_p(x_i),
    w = min_i w_i,
    S = { i : w_i < w+kappa }.

The set S is nonempty. For i,j in S, |w_i-w_j|<=kappa-1. If v_p(x_i) != v_p(x_j), their positive valuation difference belongs to D, contradicting their common g-color. Thus every x_i with i in S has one and the same valuation v. Let beta=min_{i in S} alpha_i, so w=v+beta.

The common unit-residue color gives a p-adic unit r and integers z_i such that, for i in S,

    x_i = p^v (r+p^kappa z_i).

Therefore

    sum_{i in S} a_i x_i
      = p^v r s_S + p^(v+kappa) sum_{i in S} a_i z_i.

The first term has valuation v+v_p(s_S) <= v+beta+kappa-1 = w+kappa-1, by the definition of kappa. The second is divisible by p^(v+kappa+beta)=p^(w+kappa). Every term indexed outside S is also divisible by p^(w+kappa), by the definition of S. Thus a nonzero residue remains after reduction modulo p^(w+kappa), contradicting the equation. QED.

**Layer corollary.** Suppose that within each valuation level alpha, every nonempty sum of the residues a_i/p^alpha is nonzero modulo p. Then kappa=1: the least-valuation layer in any coefficient subset already has nonzero sum modulo p. Theorem 3 gives

    c(a) <= (p-1)[binom(t,2)+1].

For p=2 this hypothesis forces every layer to contain at most one coefficient. Conversely separated valuations satisfy it. For separated valuations at any prime, Theorem 2 is sharper because the unit-residue coordinate is unnecessary.

## 4. A precise obstruction to making this proof uniform

**Proposition 4.** For every B>=2 and H>=1, there is a primitive non-partition-regular two-variable equation whose cancellation depth is H+1 at every prime p<=B, although its true avoiding number is exactly 2.

**Proof.** Put

    P = product_{p prime, p<=B} p^H,
    a = (1, -(1+P)).

The vector is primitive. Its three nonempty coefficient sums are 1, -(1+P), and -P, so none vanishes. At every prime p<=B both coefficient valuations are zero, whereas the sum has valuation H. Hence kappa_p(a)=H+1. The equation x_1=(1+P)x_2 has positive solutions, so c(a)>=2. Any prime q dividing 1+P separates its two coefficient valuations and Theorem 2 gives c(a)<=2. QED.

This proposition refutes the auxiliary assertion that bounded arity guarantees bounded cancellation depth at one of a bounded set of primes. It does not refute Rado's conjecture. It also shows why merely optimizing a first-digit coloring over finitely many small primes cannot close the argument. The useful large prime q here may grow, but Theorem 2 avoids a q-dependent unit-color factor.

## 5. The known exact-degree family does not contradict boundedness

For completeness, the following credited family makes the quantifiers transparent. This is the Alexeev--Tsimerman construction, not a new result. For n>=2 set b_i=2^i/(2^i-1), 1<=i<=n-1, and consider

    (1-sum_i b_i)x_0 + sum_i b_i x_i = 0.

Clear the odd denominators to obtain integer coefficients. Its least avoiding number is exactly n. To see the lower bound, in an (n-1)-coloring two members of {1,2,4,...,2^(n-1)} have the same color. Write them as y and 2^i y. Assign x_i=y and every other variable, including x_0, the value 2^i y. The left side is 2^i y-b_i(2^i-1)y=0. For the upper bound, the coefficient valuations at 2 are exactly 0,1,...,n-1: the coefficient of x_0 is a 2-adic unit, and v_2(b_i)=i. Coloring x by v_2(x) mod n makes all term valuations distinct in a monochromatic tuple, which is impossible for a zero sum.

Thus any admissible M(n) is at least n, while this family increases the variable count together with the avoiding number. It supplies no unbounded sequence at one fixed n. Golowich later proved the same exact degree n-1 for the simpler family with coefficients 1,2,...,2^(n-2),-2^(n-1); that result has the same quantifier limitation.

## What remains

The unsolved step is to bound c(a) uniformly for every zero-sum-free active coefficient vector of a fixed length, without bounding coefficient height, a chosen prime, or cancellation depth. The separated-valuation criterion does not cover every such vector, and Proposition 4 blocks a naive finite-prime bounded-depth completion. No family of a fixed length with c(a) tending to infinity has been produced. The general target is therefore unresolved by this attempt.

## Public sources and attribution

- Joshua Cooper, *Combinatorial Problems I Like*, Rado paragraph: https://people.math.sc.edu/cooper/combprob.html . This supplies the exact threshold question.
- Ben Green, *100 Open Problems*, current Problem 21 and its comments: https://people.maths.ox.ac.uk/greenbj/papers/open-problems.pdf . Green states fixed-arity boundedness, credits the three-variable upper bound 24 to Fox--Kleitman, and lists higher arities as open. This is the source used for that status, not a claim to have independently read Fox--Kleitman's full paper.
- Jacob Fox and Daniel J. Kleitman, *On Rado's Boundedness Conjecture*, J. Combin. Theory Ser. A 113 (2006), 84--100. The author-hosted PDF at https://math.mit.edu/~fox/paper-FoxKleitman.pdf reportedly returned HTTP 404 during the recorded proof review. The independent audit obtained an internal retrieval error rather than independently reproducing that HTTP status. No full-text inspection is claimed.
- Boris Alexeev and Jacob Tsimerman, *Equations resolving a conjecture of Rado on partition regularity*, J. Combin. Theory Ser. A 117 (2010), 1008--1010: https://arxiv.org/abs/0812.1314 and https://arxiv.org/html/0812.1314v2 . The abstract and full experimental HTML were inspected, including Theorem 1. The credited elementary proof is reproduced in compressed form above.
- Noah Golowich, *Resolving a Conjecture on Degree of Regularity of Linear Homogeneous Equations*, arXiv:1404.3384 (2014), Theorem 1.1 and conclusion: https://arxiv.org/abs/1404.3384 and https://arxiv.org/html/1404.3384v1 . The arXiv submission/version date is used; the experimental HTML renders a later date, which is not treated as a new manuscript date.

Recorded finite checks validate implementations and selected examples; their aggregate metadata is in ACCEPTANCE.json and STATUS.json. The complete analytic proofs above establish the infinite-domain claims and depend on no omitted program, raw output, or dataset. The accompanying audit accepts precisely this partial. Edition preparation reran no mathematical computation and makes no new source-retrieval, literature-completeness, bibliographic-priority, or worldwide-current-openness claim.
