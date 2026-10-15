# Independent all-index cylinder and stopped-cost derivation

This is the reviewer's reconstruction, made before consulting any author verifier or other review. The candidate theorem is treated as a hypothesis. Finite rational controls supplement the following derivation; they do not prove its limits. Let q=3/4 and r=1/4. The source begins with a fair bit and has self-transition q and change-transition r; the stationary vector is (1/2,1/2). Different strings are independent.

## Exact coding, endpoints and singleton cost

For nonempty word w of length d, pi(w)=(1/2) product of its d-1 transitions; pi(empty)=1. Construct I(empty)=[0,1] and successively split each interval into its 0 and 1 children in the appropriate conditional probabilities, using the fair split at the root. Write I(w)=[L(w),R(w)] before deciding endpoint ownership. Then R(w)-L(w)=pi(w), and

    L(w) = sum_{i: w_i=1} pi(w_1...w_{i-1}0).

This follows directly by adding the left child mass at each move to a right child. Every length-d mass is at most (1/2)q^(d-1), so the maximum cylinder diameter tends to zero. A nested sequence determines one rank value. A string has probability zero because its length-d prefix probabilities tend to zero. The source has full support, so the only duplicated rank values are between adjacent strings W0 111... and W1 000...: there are no intermediate words, and equality of their distribution functions follows from atomlessness. If a suffix is not the appropriate extremal suffix, a positive-probability cylinder can be put strictly between the strings, so there is no additional duplication.

Assign an internal rank boundary to its right cylinder. The resulting h agrees with the source convention h(t)=sup{s:F(s)<=t}. Any other endpoint assignment gives the same law for uniform U, since all finite-cylinder endpoints form a countable set. Away from this set, h is order preserving and one-to-one. Hence iid uniform U_i give the required independent strings, and sorting commutes with h almost surely. This is an exact distributional coupling, not an approximation by finite words.

For a list A of strings and a rank k, the operational recursion is:

    T(A,k)=0 when |A|<=1;
    T(A,k)=|A|+T(A_0,k) when |A|>=2 and k<=|A_0|;
    T(A,k)=|A|+T(A_1,k-|A_0|) otherwise.

Here A_b consists of strings whose next bit is b, with that bit removed. Along the selected path, the size at depth d is Lambda_{n,d}. These sizes are nonincreasing; once the size is one there can be no later charged operation. Therefore the recursion is exactly sum_{d>=0} Lambda_{n,d} 1{Lambda_{n,d}>1}. Depth zero is the root charge n for n>=2, and the cost for n=1 is zero. Distinct strings separate at a finite depth almost surely. Charging a singleton indefinitely would change the problem and give an infinite cost; it is explicitly excluded here.

For s extending a nonempty prefix w, the sum of the terms strictly beyond w is between 0 and

    pi(w) sum_{ell>=1} q^ell = 3 pi(w).

Two such tails lie in the same interval [0,3pi(w)], so their difference is at most 3pi(w), not 6pi(w). This proves the candidate's modulus for all infinite words, including eventually constant endpoint words.

## Sparse word, all-index transition counts and rank series

Let v_i=1 exactly at squares j^2 with j>=2. For any finite prefix, its remaining suffix contains both a future 1 and a future 0. Thus the rank F(v) lies strictly between the endpoints of that prefix cylinder: a positive-mass lexicographically smaller cylinder is found at a future 1, and a larger one at a future 0. It follows that t=F(v) is no finite-cylinder boundary, is in (0,1), and h(t)=v. More concretely 27/128<t<1/2.

The interiors of the nested prefix cylinders form neighborhoods of t. The preceding modulus therefore implies m(h(u))->m(v) as u->t. This conclusion includes any legitimate value chosen at other nearby boundaries; it does not infer continuity merely from a plot or a finite prefix.

For j>=2 let W_j be the prefix of length j^2-1. It begins and ends with 0. The 1s in it occur at 2^2,...,(j-1)^2 and are isolated. Every such 1 contributes two changes. There are j-2 such 1s, 2j-4 changes, and (j^2-2)-(2j-4)=j^2-2j+2 preservations. Thus

    P_j=pi(W_j)=(1/2)r^(2j-4)q^(j^2-2j+2).
    P_{j+1}/P_j=r^2 q^(2j-1).

These identities hold at j=2 as well: W_2=000 and P_2=(1/2)q^2=9/32. The initial symbol is not a transition.

The only positive contributions to L(v) are at its 1s. The bit immediately preceding every such 1 is 0; the left child at this position therefore has mass qP_j. Atomlessness and shrinking cylinder diameters imply

    t=sum_{j>=2} qP_j,
    tau_j=sum_{i=2}^j qP_i.

The latter is exactly the common boundary of W_j0 111... and W_j1 000..., not a numerical approximation to that boundary. The tail is strictly positive. Using the displayed successive ratio,

    P_j q^(2j)/16 < t-tau_j
      <= [P_j q^(2j)/16]/[1-r^2 q^(2j+1)]
      < P_j q^(2j)/15 < P_j q^(2j)/12.

The first strict inequality holds because infinitely many positive terms follow the first omitted term. The upper geometric estimate uses the largest ratio among the subsequent terms; those ratios decrease. This independently confirms the candidate's weaker rank-distance bound. No finite truncation is identified with t.

## Endpoint means and local cylinders

Set C_j=sum_{d=0}^{j^2-1} pi(v^{(d)}). For a_j=W_j0 111..., the first new step is a 0->0 transition q, the next is a 0->1 transition r, and all later ones preserve 1. For b_j=W_j1 000..., the first new step is 0->1 with r, the next is 1->0 with r, and all later ones preserve 0. Consequently

    A_j=m(a_j)=C_j+P_j q[1+r/(1-q)]=C_j+(3/2)P_j,
    B_j=m(b_j)=C_j+P_j r[1+r/(1-q)]=C_j+(1/2)P_j,
    A_j-B_j=P_j.

The factor for the first terminal switch cannot be omitted. At tau_j, the right-inverse value is b_j and the left limit corresponds to a_j. Neither convention is used to identify v with an endpoint.

For K>=1, the cylinder W_j0 1^K ends exactly at tau_j and has length P_j q r q^(K-1)=P_j q^K/4. The cylinder W_j1 0^K begins there and has length P_j r^2 q^(K-1)=P_j q^K/12. These formulas would fail at K=0; the candidate takes K_j=floor(j/2)>=1, so that boundary case is avoided. The next 1 after j^2 is at (j+1)^2, leaving exactly 2j zero positions between the two 1s. Thus W_j1 0^(2j) starts at tau_j and has length P_j q^(2j)/12. The actual rank is strictly inside it, consistent with the tail bound above.

Take w_j=P_jq^j and K_j=floor(j/2). The smaller local cylinder has length P_jq^K_j/12. Both w_j-wide one-sided rank windows lie in the stated cylinders exactly when 12q^(j-K_j)<1; this holds for all j>=17, while it fails for j<=16. The theorem only needs eventual inclusion. Applying the common-prefix modulus to the two cylinders gives errors <=(3/4)P_jq^K_j on the left and <=(1/4)P_jq^K_j on the right. The candidate's common upper bound P_jq^K_j is valid.

## Uniform approximation to the exact stopped cost

Let H=ceil(5 log n/log(4/3))+1 and d_n=sqrt(2 log n/n)+n^-2, for n>=2. At any deterministic grid point x=r/n^2, a centered binomial tail is at most 2 exp(-2n epsilon^2); this follows by integrating the bound 1/4 on the second derivative of the Bernoulli log moment generating function and optimizing. With epsilon=sqrt(2 log n/n), each grid tail is at most 2n^-4. There are n^2+1 grid points; their union bound is <=4n^-2. Monotonicity of empirical and uniform CDFs adds no more than one grid spacing, proving the asserted empirical-CDF event.

A fixed pair agrees to depth H with probability sum_{|w|=H} pi(w)^2. This is at most max pi(w) <=(1/2)q^(H-1), since the probabilities sum to one. The pair union bound is <=n^2 q^(H-1)/4<=1/(4n^3). On its complement all depth-H buckets have size <=1, and all later stopped counts are zero.

On the empirical-CDF event, every cylinder count differs from npi(w) by <=2nd_n. Endpoint avoidance holds simultaneously almost surely, so it does not require a data-dependent union bound. Replacing a count by its singleton-truncated value changes it by at most one. There are exactly H relevant depths, 0 through H-1. The uncharged deterministic mean tail is bounded by

    sum_{d>=H} pi(s^{(d)}) <= 2q^(H-1)<=2n^-5.

Therefore, simultaneously for all s, on an event G_n with probability >=1-4n^-2-1/(4n^3),

    |Z_n(s)-nm(s)| <= R_n=2nH d_n+H+2n^-4.

This is a pointwise deterministic implication of measurable events. No measurable random supremum or independence between G_n and the rank-window events is required. The estimate remains valid when s is the sampled selected string.

## Scales and an explicit eventual cost-band bound

Let n_j=ceil(w_j^-2). Since w_j->0,

    1<=sqrt(n_j)w_j<=sqrt(1+w_j^2)->1;
    sqrt(n_j)P_j>=q^-j->infinity.

Since P_j>=4^(-(j^2-1)) and q^j>=4^-j, n_j<=2*16^(j^2+j-1). Hence log n_j<=3(j^2+j), and H_{n_j}<=91j^2 for j>=2. The last two inequalities are deliberately crude, but suffice. Also sqrt(2log n_j)<=3j. Direct substitution into R_n gives, for all j>=2,

    R_{n_j}/(n_jP_j)
      <=546j^3q^j+182j^2q^(4j)+91j^2q^(2j)+2q^(10j).

For the small terms we used n_j>=P_j^-2q^-2j and P_j<=1. Every displayed term tends to zero. This proves the required little-o estimate independently of finite numerical checks.

In addition, the exact rational control at j=100 proves that this bound plus q^floor(j/2) is strictly below 1/8. All the polynomial times exponential terms decrease thereafter (their successive ratios are (1+1/j)^a q^b<1 and decrease with j), while q^floor(j/2) is nonincreasing. Thus the candidate's two cost bands are valid on their respective rank-window events intersected with G_{n_j} for every j>=100. This explicit threshold is an optional strengthening, not needed for the limit proof.

Finally (t-tau_j)/w_j <=q^j/12->0. The jumps shrink on the unscaled mean profile and their locations approach its continuity point. Their square-root-rescaled heights still diverge; these statements are compatible.

## Probability and arbitrary deterministic centering

For k_n=floor(nt)+1 and x_n=t+z/sqrt(n), the exact identity is

    P(U_(k_n)<=x_n)=P(Bin(n,x_n)>=k_n).

The centered binomial characteristic function has logarithm -u^2 x_n(1-x_n)/2+O(n^-1/2) at argument u/sqrt(n); the error is uniform when x_n is near the fixed interior point t. Thus (Bin(n,x_n)-nx_n)/sqrt(n) tends to N(0,t(1-t)). Its threshold (k_n-nx_n)/sqrt(n) tends to -z because the floor error is bounded. This proves sqrt(n)(U_(k_n)-t) tends to N(0,t(1-t)); the normal distribution has no atoms at the threshold.

For the two windows (tau_j-w_j,tau_j) and (tau_j,tau_j+w_j), their rescaled endpoints about t tend to (-1,0) and (0,1). Both event probabilities therefore tend to

    rho=Phi(1/sqrt(t(1-t)))-1/2>0.

Since G_{n_j} has probability tending to one, intersection with it subtracts o(1) without an independence assumption. The preceding deterministic estimates then put the selected cost in each of the two bands

    n_j[A_j-P_j/8,A_j+P_j/8],
    n_j[B_j-P_j/8,B_j+P_j/8]

with probability >=rho-o(1), respectively. Their distance is 3n_jP_j/4. For any fixed M, a window of length 2M sqrt(n_j) eventually cannot meet both, because sqrt(n_j)P_j->infinity. Uniformly for every real center a,

    limsup_j sup_a P(|Y_{n_j}(k_{n_j})-a|<=M sqrt(n_j))<=1-rho.

Consequently every deterministic centering sequence has tail probability >=rho-o(1) outside [-M,M] along this subsequence, for every fixed M. Choosing epsilon<rho proves failure of tightness; weak convergence to a real-valued law would imply tightness.

Centering by the expectation is legitimate: the cost is integrable. Indeed it is bounded by the cost of all non-singleton buckets in the full trie. For a depth-d bucket with count N_w, N_w 1{N_w>1}<=N_w(N_w-1), so its expected contribution is <=n(n-1)pi(w)^2. Summing over all buckets and depths is finite, since sum_{|w|=d}pi(w)^2<=(1/2)q^(d-1) for d>=1. This also confirms that the theorem's expectation example does not conceal a divergent mean.

## Assessment and exact scope

No mathematical gap or counterexample was found in the submitted theorem. Its operational definition matches equations (2)-(3) in the independently retrieved primary process preprint. The preprint's Section 2.4 defines the deterministically centered rank process, Proposition 2.9 gives existing boundary-rank non-tightness, and the later open-marginal sentence remains present. The OWR contribution asks the marginal question on printed page 2856. This audit verifies a negative universal assertion at an explicit fixed nonboundary continuity rank, including every deterministic centering. It does not classify other ranks, establish failure almost everywhere, settle data-dependent centering, claim historical priority, or verify every publisher-typeset wording. The cylinder and probability mechanisms are elementary except for the classical binomial CLT, independently reduced above to its characteristic-function expansion.
