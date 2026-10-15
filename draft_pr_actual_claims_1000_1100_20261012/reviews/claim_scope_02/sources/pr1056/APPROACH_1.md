# Sparse real low rank matrices and zero squares

## Outcome and exact target

**Status: partial result only. Approach 1 of 5. The original conjecture remains unresolved by this report.**

For an n by n matrix M, let z(M) be the largest integer t for which some t rows and t columns induce an all-zero submatrix. The selected rows and columns need not be consecutive. Write E for the number of nonzero entries, r for the rank over the stated field, p=E/n², and δ=1−p.

The target is the existence of one absolute C such that every real matrix with E≤εn² and 0<ε<1/2 satisfies

    z(M) ≥ n exp(−C sqrt(εr)).

The source is Conjecture 5, printed page 2309 of Oberwolfach Report 42/2025 (PDF page 67). It also appears as Conjecture 1.8, page 4, of Hunter–Milojević–Sudakov–Tomon, arXiv:2411.13510v1. The source statement and the related theorem on page 6 were visually inspected. No exact solution or counterexample to the original real-rank statement was established in the source search.

This approach combines sparse row bases with oversampling column spans. It proves, over every field:

1. z(M) ≥ max{0, ceil(n−sqrt(rE))}.
2. For every integer k>r≥1,

       z(M)/n ≥ [(k−r)/(2k−r)] δ^k.

   There is also the stronger implicit inequality

       δ^k ≤ h + [k/(k−r)]h(1−h),   h=z(M)/n.

3. Consequently, under the original density hypothesis,

       z(M) ≥ ceil(n exp(−6 max{sqrt(εr), εr})).

In particular, the requested square-root exponent is proved with C=6 throughout εr≤1, and with C=2 throughout εr≤1/4. For εr tending to infinity, the proven exponent is linear in εr rather than its square root. This is the remaining gap.

The argument is an elementary refinement/adaptation of the probabilistic dimension-drop method in Singer–Sudan, Section 3. No claim of priority or of improving the best known real-field bound is made. Its purpose here is an explicit, fully proved baseline and a precise diagnosis of this approach's limitation. The small-density endpoint also has a clear antecedent in HMST Lemma 4.7(2), which guarantees a half-sized zero rectangle at density at most 1/(16r); Lemma 1 below implies a half-sized zero square already at density at most 1/(4r). This comparison is a verified parameter comparison, not a novelty claim.

## Verified literature boundary

- Hunter, Milojević, Sudakov and Tomon, *Disjoint pairs in set systems and combinatorics of low rank matrices*, arXiv:2411.13510v1: Conjecture 1.8 is exactly the arbitrary-real support-density problem. The body of Theorem 1.12, page 6, and its restatement as Theorem 4.8, page 19, give exponent O(log r+sqrt(εr)) for nonnegative entries in {0}∪[1,∞), with ε bounding the **mean of the entries**. The stronger-sounding abstract is not a substitute for the body theorem. The current arXiv page listed only v1 on 10 October 2026; the separately retrieved author-hosted PDF retained the same hypotheses and logarithmic term.
- Singer and Sudan, *Point-hyperplane incidence geometry and the log-rank conjecture*, arXiv:2101.09592v5 / ACM TOCT 14(2), Article 7 (2022): Theorem 1.7 and Section 3 give a general incidence biclique lower bound by sampling hyperplanes and using dimension drops. The proof below works directly with matrix column spans, allows repetitions and zero rows/columns, and uses oversampling to remove an r-dependent prefactor from the displayed all-field baseline.
- Sudakov and Tomon, *Matrix discrepancy and the log-rank conjecture*, arXiv:2311.18524 / Mathematical Programming 212 (2025), 567–579: its discrepancy bound and density-decrement argument concern binary matrices. Applying that theorem to the Boolean support of a real matrix requires a separate bound on the support matrix's real rank; that rank need not equal r.
- Balla, Hambardzumyan and Tomon, *Factorization norms and an inverse theorem for MaxCut*, arXiv:2506.23989 / Mathematische Annalen (2026): the inspected Boolean-matrix structural results do not supply an arbitrary-real support-density reduction preserving the target parameters.
- Hunter, Milojević, Sudakov and Tomon, *Communication Complexity of Disjointness under Product Distributions*, ECCC TR26-040 (March 2026): Lemma 3 gives cross-disjoint rectangles for independent distributions over subsets. The stated lemma's disjointness parameter lies below 1/2. It does not itself identify arbitrary real orthogonality with disjointness, and no such identification is assumed here.

These are bounded source checks, not a claim that every possible paper has been exhausted. Exact public URLs and retrieved-file hashes are recorded separately in the source ledger.

## The sparse row basis lemma

**Lemma 1.** Let M be an n by n matrix over any field with rank r and E nonzeros. Then

    z(M) ≥ max{0, ceil(n−sqrt(rE))}.

**Proof.** If r=0, the matrix is zero, E=0, and z(M)=n. Suppose r>0, so E>0, and put D=sqrt(E/r). Let A be the set of rows having at most D nonzero entries. If H rows are excluded, those rows contain more than HD nonzeros; hence H<E/D=sqrt(rE). Thus

    |A| > n−sqrt(rE).

Choose a basis for the span of the rows indexed by A, using rows of A themselves. It has at most r elements. The union U of their supports has size at most rD=sqrt(rE). Every row in their span vanishes outside U, because a linear combination cannot be nonzero at a coordinate where every summand is zero. Therefore M[A,[n]\U]=0 and

    |[n]\U| ≥ n−sqrt(rE).

Both cardinalities are integers. If the displayed real lower bound is positive, both are at least its ceiling; taking equal-sized subsets proves the claim. If it is nonpositive, the asserted lower bound is merely zero. No cancellation-free factorization, entry-sign assumption, or magnitude bound was used. ∎

For s=εr≤1/4, Lemma 1 gives z(M)/n≥1−sqrt(s). Since log(1−x)≥−2x for 0≤x≤1/2,

    z(M) ≥ n exp(−2sqrt(s)).

This is a genuine part of the requested real-matrix conclusion, not merely a constant-sized-rectangle assertion that loses the s→0 limit.

## Oversampling column spans

**Theorem 2.** Let M be an n by n matrix over any field of rank r≥1, with zero density δ. Set h=z(M)/n. For every integer k>r,

    δ^k ≤ h + [k/(k−r)]h(1−h).

In particular,

    h ≥ [(k−r)/(2k−r)]δ^k.

**Proof.** Factor M=UV with U having r columns and V having r rows. Write u_i for the rows of U and v_j for the columns of V, so M_ij=u_i v_j. The standard bilinear pairing here is nondegenerate over the chosen field; no real inner-product geometry is used.

Sample J_1,…,J_k independently and uniformly from [n], with replacement. Let

    H_0={0},
    H_t=span(v_{J_1},…,v_{J_t}),
    q(H)=|{j:v_j∈H}|/n,
    X=|{i:u_i w=0 for every w∈H_k}|/n.

For row i, let δ_i be its fraction of zero entries. A row annihilates H_k precisely when all k sampled entries in that row vanish. Hence

    E[X]=(1/n)Σ_i δ_i^k ≥ [(1/n)Σ_i δ_i]^k=δ^k.

The inequality is Jensen's inequality. Independence is conditional on the fixed row; an equality δ^k without row-regularity would generally be incorrect.

For each t=1,…,k define the adapted indicator

    I_t=1{ q(H_{t−1})≤h and v_{J_t}∈H_{t−1} }.

Conditional on the first t−1 choices, the next sample is uniform, so

    E[I_t | J_1,…,J_{t−1}]
      =1{q(H_{t−1})≤h}q(H_{t−1})≤h.

Thus E[Σ_t I_t]≤kh.

Now consider any outcome for which X>h. Every row counted by X annihilates every earlier H_t. If q(H_t)>h for any t, those rows and the columns with factors in H_t would form a zero rectangle having both sides strictly greater than hn=z(M). Because the side lengths are integers, that would contain a square of side at least z(M)+1, a contradiction. Consequently q(H_t)≤h for every earlier span on the event X>h.

The dimension of H_t increases by one whenever v_{J_t} is not in H_{t−1}, and otherwise does not increase. There can be at most r increases. Among k samples there are therefore at least k−r dependent choices. On X>h, every such choice is counted by I_t. Pointwise,

    (k−r)1{X>h} ≤ Σ_t I_t.

Taking expectations gives

    P(X>h)≤kh/(k−r).

Since 0≤X≤1, splitting at h gives

    E[X]≤h P(X≤h)+P(X>h)
         =h+(1−h)P(X>h)
         ≤h+[k/(k−r)]h(1−h).

Together with E[X]≥δ^k this proves the stronger statement. Dropping the factor 1−h≤1 yields

    δ^k≤h(2k−r)/(k−r),

which rearranges to the claimed explicit bound. ∎

**Important scope checks.** Repeated columns and zero columns are included in q(H). Repeated rows and zero rows are included in X. No selection assumes distinct factors. The field may be finite or infinite; the probability space is always finite. If δ=0, the theorem reduces to a trivial inequality. If δ=1, M has rank zero and is treated separately. The argument needs k>r, not merely k≥r.

Taking k=2r gives the particularly simple bound

    z(M) ≥ ceil(nδ^(2r)/3).

For a user-supplied upper density ε, δ≥1−ε, so the same statement holds with (1−ε)^(2r). This is a lower bound on a real number, followed by a ceiling because z(M) is an integer; no floor loss is required.

## A single bound across all density regimes

**Corollary 3.** Under 0<ε<1/2 and E≤εn²,

    z(M) ≥ ceil(n exp(−6 max{sqrt(εr), εr})).

**Proof.** Rank zero gives equality z(M)=n. Let r≥1 and s=εr>0.

For s≤1/4, Lemma 1 and the preceding logarithm inequality give h≥exp(−2sqrt(s)), which is stronger than required.

For 0<ε<1/2, log(1−ε)≥−2ε. Theorem 2 therefore gives

    h≥(1−ε)^(2r)/3≥exp(−4s)/3.

If s≥1, then 4s+log 3≤6s, proving the claimed estimate.

If 1/4≤s≤1, put t=sqrt(s)∈[1/2,1]. The convex quadratic 4t²−6t+log 3 has value log 3−2<0 at both endpoints. It is therefore nonpositive throughout the interval. Thus 4s+log 3≤6sqrt(s), which proves the middle regime. The three regimes cover all s>0. Take the ceiling of the resulting bound. ∎

This yields the desired form on every bounded εr range, with a constant depending only on the chosen range, and in particular a universal C=6 when εr≤1. It gives no universal square-root exponent for unbounded εr.

## Exact rank one boundary

If r=1, write M=uvᵀ with u and v nonzero. If their support sizes are a and b, then E=ab and the support of M is exactly the rectangle supp(u)×supp(v). A zero rectangle must omit all supported rows or all supported columns. Therefore

    z(M)=max(n−a,n−b)=n−min(a,b)≥n−sqrt(E).

Taking a=b shows that the square-root loss in Lemma 1 is exact for rank one whenever E is a square compatible with n. This also checks the regime εr→0 and explains why a bound exp(−O(εr)) alone cannot hold all the way to zero.

## An exact barrier for field independent arguments

This subsection is **not a counterexample to the real-rank conjecture**.

Let d≥1 and index the rows and columns by x,y∈F₂^d. Form M_xy=x·y in F₂, so n=2^d. The rank over F₂ is exactly d: factorization through the d coordinates proves the upper bound, and the submatrix indexed by the standard basis vectors is the identity. Each nonzero x has n/2 nonzero pairings, while x=0 has none. Thus

    E=(n−1)n/2,
    ε=E/n²=(1−2^(−d))/2<1/2.

If A×B is a zero rectangle, then span(A) and span(B) are orthogonal. If their dimensions are a and b, nondegeneracy gives a+b≤d. Also |A|≤2^a and |B|≤2^b. Consequently every zero square has side at most 2^floor(d/2). Coordinate-orthogonal subspaces, with a floor(d/2)-dimensional space on one side and a suitable equally sized subset of its annihilator on the other, attain this bound. Hence

    z(M)=2^floor(d/2),
    z(M)/n=2^(−ceil(d/2)).

Since εr is asymptotic to d/2 over F₂, the true exponent is linear in εr. Thus the all-field baseline's exponent has the right order in this broader class. A general theorem obtained solely from field-independent span and support properties cannot establish the requested square-root bound across all fields. A successful proof of the actual conjecture must exploit a property that excludes this characteristic-two configuration, for example an essentially real-field feature.

If the same array is regarded as a real 0/1 matrix, its rank is n−1, not d. For d≥2 the Gram matrix of its n−1 nonzero rows is

    (n/4)(I_(n−1)+J_(n−1)),

because the diagonal row inner products are n/2 and the off-diagonal ones are n/4. This Gram matrix is positive definite. The zero row gives the matching upper bound, proving real rank n−1. For d=1, the real rank is directly 1. Therefore the construction does not violate the original real-rank conjecture.

## The real sharpness family with exact parameters

The familiar set-intersection construction can be stated without the informal rounding k=sqrt(εr). Fix integers d≥2 and 1≤k≤d/2. Index rows and columns by the k-subsets of [d], set n=binom(d,k), and put M_AB=|A∩B|.

The exact support density and largest zero square are

    p=1−binom(d−k,k)/binom(d,k),
    z(M)=binom(floor(d/2),k).

The rank over R is exactly d. Indeed, if W is the k-set/element incidence matrix, M=WWᵀ. Its d by d Gram matrix WᵀW has diagonal binom(d−1,k−1) and off-diagonal binom(d−2,k−2), with the latter interpreted as zero when k=1. The eigenvalue on the orthogonal complement of the all-ones vector is binom(d−2,k−1)>0, and the eigenvalue in the all-ones direction is positive. Thus rank W=rank M=d.

For the zero-square formula, let U and V be the unions of the row-family and column-family sets. Cross-disjointness forces U∩V=∅. If |U|=a, the two family sizes are at most binom(a,k) and binom(d−a,k). Their minimum is at most binom(floor(d/2),k). Splitting the ground set into two parts of sizes floor(d/2) and ceil(d/2) attains that minimum, proving the formula.

Also z(M)/n≤2^(−k), by comparing the k factors in the binomial ratio. If d≥4k², then p≤k²/d≤1/4 by a union bound. Meanwhile

    1−p=product_(j=0)^(k−1)(1−k/(d−j))≤exp(−k²/d),

so p≥1−exp(−k²/d)≥k²/(2d). Therefore sqrt(pd) lies between k/sqrt(2) and k. As k grows with d≥4k², this exact real construction confirms that an exponent smaller in order than sqrt(pr) is impossible. The all-field proof above still guarantees only an exponent of order pr in this regime.

## Invalid reductions explicitly excluded

1. **Support density is not entry mean.** Multiplying nonzero entries by large positive scalars, even a common scalar, can make the mean arbitrarily large without changing support or rank. Signed entries additionally permit cancellation in the mean. The HMST mean-based theorem therefore cannot be applied using ε merely because E≤εn².
2. **Entrywise squaring does not preserve rank.** If M=UV has rank r, the symmetric-tensor factorization gives rank(M∘M)≤r(r+1)/2. Equality can already occur at r=2: the matrix with rows (1,1,0), (1,0,1), (2,1,1) has rank 2, while its entrywise square has rank 3. Moreover, squaring does not control the mean by the original support density.
3. **The Boolean support need not have rank r.** The support indicator is a nonlinear operation. In the same rank-two example just displayed, the 0/1 support indicator has rank 3 as well. A theorem whose hypothesis is the rank of that indicator cannot be invoked with the rank of M without a separate proof.
4. **A finite-field obstruction is not a real-field counterexample.** Both ranks are computed explicitly above.
## Continuation boundary

Approach 1 has reached a natural stopping point: it proves the low-εr target regime and a uniform linear-εr baseline, while its field-independent mechanism has an exact characteristic-two obstruction to the desired general improvement. A later approach must add real-specific structure or another hypothesis not shared by the F₂ example. The original problem remains open within this work; no full-resolution publication or queue status is warranted.
