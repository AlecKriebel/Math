# Stage 1: additive structure and the random translate-covering problem

Public mathematical edition. The source problem remains UNSOLVED by this five-stage study. Historical statements with residual swap bound 2m and Azuma denominator 8km² remain valid conservative estimates; the final synthesis uses the sharpened m and 2km² bounds. Stage labels record provenance, not additional assumptions. No claim of external peer review or priority is made.


Date: 14 October 2026. Mathematical study stage 1.

## 1. Model and main result

Let p tend to infinity through primes, put k=floor(sqrt(p)), and let A be a uniform k-element subset of G=Z/pZ. For a set B write U_B(A)=p-|A+B|. The requested event is the existence of a translating set T, chosen after observing A, with |T|<=floor(100 sqrt(p)) and U_T(A)=0.

**Theorem 1 (bounded-doubling translating sets are uniformly excluded).** For every fixed C>0 and K>=1,

Pr[there exists nonempty T subset G with |T|<=C sqrt(p), |T+T|<=K|T|, and A+T=G] -> 0.

The quantifier over T is fully adaptive. The theorem does not say that every small T has bounded doubling and therefore does not answer the main problem. It says that any successful bounded-multiplicity construction must leave every fixed bounded-doubling class with high probability.

A quantitative consequence is also established below: if K_p^4 log^2(K_p+2)=o(log log p), the conclusion still holds with K replaced by K_p. In particular, one can take K_p tending to infinity. A fixed sufficiently small absolute constant times (log log p)^(1/4)/(log log log p)^(1/2) is also allowed using the explicit inverse-theorem constants.

## 2. Exact-size concentration, including the finite-p error

This proof is included so the argument does not require a Bernoulli-to-uniform-model substitution. It agrees with the independently developed swap-Lipschitz route in ../proofs/01_CONSTRUCTIVE_AUDIT.md, Sections 1-2.

For a fixed B of size b<=p-k, define

q_b = binom(p-b,k)/binom(p,k),  mu_B = p q_b.

Each x is absent from A+B precisely when A misses x-B, so E U_B=mu_B exactly.

**Swap bound.** If A and A' are k-sets differing by one exchange, then |U_B(A)-U_B(A')|<=b. Indeed, with their common part Q, the two union sizes are |Q+B|+|(a+B)\\(Q+B)| and |Q+B|+|(a'+B)\\(Q+B)|. Both increments belong to [0,b].

Expose an ordered sample without replacement a_1,...,a_k. Conditional on the first i-1 draws, compare two choices x,y for draw i. Couple the remaining ordered samples by swapping the labels x and y. The final unordered k-sets either agree or differ by a single exchange. Consequently the two conditional expectations of U_B differ by at most b. Each Doob martingale increment has absolute value at most b. Azuma's inequality therefore gives the safe (not optimized) bound

Pr[U_B<=mu_B-z] <= exp(-z^2/(2 k b^2)).                 (2.1)

In particular,

Pr[A+B=G] <= exp(-p^2 q_b^2/(2 k b^2)).               (2.2)

The stronger bounded-conditional-range constant is unnecessary here.

An explicit lower bound for q_b is useful when envelope size grows. If b/(p-k+1)<=1/2, use log(1-x)>=-x-x^2 for 0<=x<=1/2 in

q_b = product_{i=0}^{k-1}(1-b/(p-i)).

This gives

q_b >= exp[-kb/(p-k+1) - k b^2/(p-k+1)^2].           (2.3)

If b<=M sqrt(p), M>=1 and M=o(p^(1/4)), define

D_p(M) = M sqrt(p) k/(p-k+1)
         + M^2 p k/(p-k+1)^2.

Then D_p(M)=M+O((M+M^2)/sqrt(p)) and q_b>=exp[-D_p(M)]. Since k<=sqrt(p) and b^2<=M^2 p, (2.2) yields

Pr[A+B=G] <= exp[-sqrt(p) exp(-2D_p(M))/(2M^2)].      (2.4)

For a fixed M this is exp[-c_M sqrt(p)] with a strictly positive constant. It is uniform over all fixed B satisfying the cardinality constraint; it does not mean the same random A simultaneously works for all B.

**Envelope union bound.** If a deterministic family E_p contains N_p sets, each of size <=M_p sqrt(p), then

Pr[there exists B in E_p: A+B=G]
 <= N_p exp[-sqrt(p) exp(-2D_p(M_p))/(2M_p^2)].        (2.5)

Any family of candidate translating sets whose members are contained in members of E_p is excluded by the same estimate: T subset B and A+T=G imply A+B=G. Counting envelopes rather than their arbitrary subsets is essential.

## 3. Progression envelopes and proof of Theorem 1

A proper rank-r progression in Z/pZ has the form

P={v_0+n_1 v_1+...+n_r v_r: 0<=n_i<L_i},

where the displayed sums are distinct; hence |P|=product L_i. For |P|<p each L_i is an integer in [1,p]. For any nonnegative integer d, the total number of such progressions with rank at most d and any allowed volume is at most

sum_{r=0}^d p^(r+1) p^r <= (d+1)p^(2d+1).           (3.1)

This overcounts heavily, which is harmless. In particular, every fixed-rank progression of O(sqrt(p)) volume belongs to a polynomial-size deterministic family.

The sole non-elementary structural input is Green and Ruzsa, *Freiman's theorem in an arbitrary abelian group*, arXiv:math/0505198v2, Theorem 1.1 (PDF p.2). If |T+T|<=K|T|, it puts T inside a coset progression P+H of rank at most

d(K)<=D K^4 log(K+2)

and size at most

f(K)|T|,  f(K)=exp[D K^4 log^2(K+2)],

for one absolute constant D. The paper's definition (PDF p.1) makes P proper and the addition of subgroup H direct. These precise features were checked in the primary PDF. Only this theorem and its hypotheses are used; it is not a covering theorem.

In a group of prime order, H is either trivial or the full group. For fixed C,K and sufficiently large p, f(K) C sqrt(p)<p, so H cannot be the full group. Thus T lies in a proper progression P of rank <=d(K) and volume <=M sqrt(p), M=C f(K) (increase M to 1 if needed).

Apply (2.5) to all these progressions, using (3.1). The bound is

(d+1)p^(2d+1) exp[-c_M sqrt(p)] -> 0.

This proves Theorem 1, including adaptive choice of T and all sufficiently large primes. No exchange of a fixed-K limit and a growing-K limit has been made.

**Related envelope families.** The same proof excludes translating sets contained in a union of a fixed number h of bounded-rank progressions whose total volumes are O(sqrt(p)). There are still polynomially many envelope unions, and their cardinalities satisfy the required bound. This covers more than just a single small-doubling class.

## 4. A justified growing-doubling version

Let K=K_p>=1 depend on p. Set

d_p=ceil[D K_p^4 log(K_p+2)],
M_p=max(1,C exp[D K_p^4 log^2(K_p+2)]).

Suppose M_p sqrt(p)<p and M_p=o(p^(1/4)). The same explicit proof gives

Pr[there exists a cover T with |T|<=C sqrt(p), |T+T|<=K_p|T|]
 <= (d_p+1)p^(2d_p+1)
    exp[-sqrt(p) exp(-2D_p(M_p))/(2M_p^2)].            (4.1)

Thus it suffices that

log(d_p+1)+(2d_p+1)log p
 =o(sqrt(p) exp(-2D_p(M_p))/M_p^2).                  (4.2)

If K_p^4 log^2(K_p+2)=o(log log p), then M_p=(log p)^o(1), d_p=o(log log p), and D_p(M_p)=M_p+o(1). The right side of (4.2) is p^(1/2-o(1)), whereas its left side is O(log p log log p). All size and error hypotheses hold. This proves the stated growing-K conclusion.

One may instead choose K_p so D K_p^4 log^2(K_p+2)<=(1/2)log log p. Then M_p<=max(1,C sqrt(log p)), d_p=O(log log p), and the same argument works, since exp[-2C sqrt(log p)]=p^-o(1). Therefore there is an absolute sufficiently small a>0 such that

K_p = a (log log p)^(1/4)/(log log log p)^(1/2)

is allowed for every fixed C, for all sufficiently large p. Constants are not numerically evaluated; this is an asymptotic structural exclusion, not a finite practical bound.

### Small difference sets

The fixed-K exclusion also holds with |T-T|<=H|T| for any fixed H. Indeed, apply the Plunnecke estimate to A=T, B=-T: there is a nonempty X subset T with |X-2T|<=H^2|X|. A translate of -2T is contained in X-2T, so |T+T|<=H^2|T|. This is Theorem 3.1 of Petridis, arXiv:1101.3507v3, PDF p.7, used with h=2; the primary theorem and its proof were inspected. Then apply Theorem 1 with K=H^2. The same argument allows growing H_p whenever H_p^8 log^2(H_p+2)=o(log log p).

## 5. Why energy and Fourier structure do not finish the split

Write r_T(d)=|T intersect (T+d)| and E(T)=sum_d r_T(d)^2. Cauchy-Schwarz gives E(T)>=|T|^4/|T-T|, but the converse conclusion needed here is unavailable: large energy does not imply the whole T has bounded doubling. Standard energy inverse statements isolate a large structured subset. A cover by T does not imply that this subset covers.

The obstruction can be seen without an inverse theorem. Let I={0,...,m-1}, with 2m<p, and let R be any disjoint m-set. Then T=I union R has size 2m and

E(T)>=E(I)=(2m^3+m)/3 >=|T|^3/12.

R may be arbitrary. There are binom(p-m,m) choices, with entropy of order sqrt(p)log p when m is a fixed positive multiple of sqrt(p). Thus even a constant-fraction maximal-energy class contains an enormous arbitrary remainder. A proof must control that remainder or find a cover-specific reason it cannot matter.

Large doubling does not imply small energy either. For m^2<p, take I as above and R={0,m,2m,...,(m-1)m}. The union has 2m-1 points and contains I, so its energy is still Omega(m^3). Meanwhile R+I={0,...,m^2-1} is an interval of m^2 residues, so |T+T|>=m^2 and |T+T|/|T|>=m^2/(2m-1). Also R-I is an interval of m^2 residues, giving the same lower bound for the difference ratio. This explicit family has both growing doubling and high normalized energy. It happens to be a union of two progressions and is covered by the stronger envelope exclusion, but demonstrates the failure of the simple doubling-versus-energy dichotomy.

A nontrivial large Fourier coefficient similarly need not force an O(sqrt(p))-cardinality envelope. For instance, choose arbitrary sparse T inside the arc {0,...,floor(p/8)}. Every term has real part at least 1/sqrt(2) at frequency 1, so |T_hat(1)|>=|T|/sqrt(2), yet this class has exp(Theta(sqrt(p)log p)) members at square-root cardinality. Its enclosing arc has Theta(p) points and cannot be inserted into (2.5) with bounded M.

For unnormalized Fourier transforms and f=1_A*1_T,

sum_x |f(x)-k|T|/p|^2
 = (1/p)sum_{r!=0}|A_hat(r)|^2 |T_hat(r)|^2.          (5.1)

An upper bound for this variance does not establish the presence of a zero when the mean is 100. A lower bound for this variance also need not establish a zero. Neither conclusion follows merely from a random-set bound on max_{r!=0}|A_hat(r)|. The exact integer positivity condition f(x)>=1 for all x is the unresolved issue.

## 6. An exact first-moment obstruction

There is a particularly concrete problem with counting all translating sets and seeking a uniform small upper bound for their covering probabilities.

Fix A_0={0,...,k-1}. Put m=ceil(p/k), and S={0,k,2k,...,(m-1)k} modulo p. The intervals A_0+s cover every residue, so A_0+S=G. For any integer t>=m, every t-set containing S is a cover of A_0. If N_t(A) counts all t-element translating sets that cover A, then exactly

E_A N_t(A) >= binom(p-m,t-m)/binom(p,k).              (6.1)

Take t=floor(C sqrt(p)) for a fixed C>2. Stirling's estimate for sparse binomial coefficients gives

log E_A N_t(A) >= ((C-2)/2+o(1))sqrt(p)log p.         (6.2)

For C=100 the leading coefficient is 49. The first moment over all T diverges enormously because extremely rare structured A admit extremely many padded translating sets. Consequently a direct union bound, evaluated by this unrestricted first moment, cannot prove the desired negative result, even if the typical covering event eventually turns out to be false.

The separate entropy proof in ../proofs/01_ENTROPY_BOTTLENECK.md, Sections 5-6, is stronger: even the first moment of inclusion-minimal covers diverges, by a family of interval-set covers. Thus minimality alone does not repair the first moment. Conditioning on a sufficiently strong typical-A event or a suitable entropy-compression argument remains an additional, unproved step. Simply seeking a universally exponentially tiny fixed-T covering probability is also untenable: whenever a fixed T admits even one covering k-set A, its covering probability is at least binom(p,k)^-1, which is exp[-(1/2+o(1))sqrt(p)log p], not exp[-c p].

The same entropy proof, Section 4, also constructs a fixed interval T at the requested cap with covering probability at least exp(-k-2). Hence the sqrt(p) exponential scale in a uniform fixed-T concentration bound is genuinely sharp; a bound with an extra divergent factor in its exponent cannot hold for every T. This strengthens the elementary atom-size observation above.

## 7. The Cayley domination formulation and the missing theorem

Form a bipartite graph with two copies of G, left vertices t and right vertices x, and edges t--x iff x-t belongs to A. Every vertex has degree k. A translating set T covers exactly when its left neighborhood is all right vertices. Equivalently, in the directed Cayley graph with arcs t -> t+a, the union of the outgoing neighborhoods of T must equal G, with loops retained if 0 belongs to A. This is an open-neighborhood covering condition. A convention that automatically counts every selected vertex as dominated would instead correspond to replacing A by A union {0}; it must not silently replace this model.

The random graph is a union of k randomly selected perfect matchings indexed by differences. Edges sharing a difference are perfectly correlated. It is not the independent-edge random graph and is not the uniform random k-regular bipartite graph. Any domination theorem imported from those models needs an explicit transfer; degree, codegree, or spectral resemblance alone is not that transfer.

For a fixed T the exact joint empty-neighborhood probabilities are

Pr[x and y are uncovered]
 = binom(p-(2|T|-r_T(x-y)),k)/binom(p,k).              (7.1)

For m distinct test points x_1,...,x_m, the analogous probability depends on the whole union of x_i-T, rather than only pair correlations. Thus energy information controls some second-order data but does not supply the needed high-order, uniform, adaptive covering bound.

A complete negative route would need to handle translating sets outside every low-complexity progression envelope while controlling the entropy and rare-A obstruction in Section 6. A complete positive route would need an adaptive construction with cardinality at most the exact cap and a proved success probability. Neither is established here.

## 8. Scope and sources

- Primary structural input: Ben Green and Imre Z. Ruzsa, *Freiman's theorem in an arbitrary abelian group*, arXiv:math/0505198v2, https://arxiv.org/pdf/math/0505198v2 ; Theorem 1.1, PDF p.2, and proper/direct definition on PDF p.1. Inspected via the web PDF tool on 2026-10-14.
- Difference-to-sumset input: Giorgis Petridis, *New Proofs of Plunnecke-type Estimates for Product Sets in Groups*, arXiv:1101.3507v3, https://arxiv.org/pdf/1101.3507v3 ; Theorem 3.1, PDF p.7, inspected 2026-10-14.
- Bibliographic record: Journal of the London Mathematical Society 75 (2007), 163-175, https://doi.org/10.1112/jlms/jdl021 .
- Main open-problem reference, already scoped separately: Ben Green, *100 Open Problems*, Problem 39, https://people.maths.ox.ac.uk/greenbj/papers/open-problems.pdf#page=20 .

No BJR theorem is invoked in a regime excluded by the construction contract. No theorem here asserts that all candidate covers have low doubling, low energy, or low description complexity.

## 9. Independent checks within this pass
