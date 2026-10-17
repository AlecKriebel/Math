# Stage 1 independent adversarial audit: random translate covers

Public mathematical edition. The source problem remains UNSOLVED by this five-stage study. Historical statements with residual swap bound 2m and Azuma denominator 8km² remain valid conservative estimates; the final synthesis uses the sharpened m and 2km² bounds. Stage labels record provenance, not additional assumptions. No claim of external peer review or priority is made.


Date: 14 October 2026. Mathematical study stage 1.

## Status and exact target

No resolution is accepted. Several restricted-class exclusions and two first-moment obstructions are mathematically sound. Their quantifiers do not reach unrestricted adaptive translating sets.

Let p tend to infinity through all primes, k=floor(sqrt(p)), c=floor(100 sqrt(p)), and let A be a uniform k-subset of Z/pZ. The target is Pr[there exists T, |T|<=c, A+T=Z/pZ] -> 1. A negative answer needs a fixed positive failure probability along arbitrarily large primes. Failure of particular strategies, or absence of witnesses in any restricted class, is insufficient.

This audit is confined to shared Stage 1.

## Inspected scope so far

The final mathematical manuscripts in ../proofs/01_CONSTRUCTIVE_AUDIT.md, ../proofs/01_ENTROPY_BOTTLENECK.md, ../proofs/01_STRUCTURE_RESULTS.md, and ../proofs/01_ALTERNATIVE_RESULTS.md have been read. The substantive proofs survive independent checking, with minor wording corrections applied by their authors. The finite-check study's final report, census, checker code, validation receipts, and seed-identity results were inspected and cross-checked independently. This is the final audit of all six shared Stage 1 arguments, counting this audit argument itself.

### 1. A fixed-envelope tail and its precise union-bound scope

For any deterministic S with m=|S|<=M sqrt(p), M fixed, put U_S(A)=|G\\(A+S)|. Its exact mean is

E U_S = p binom(p-m,k)/binom(p,k).

Uniformly over m<=M sqrt(p), the ratio is at least exp(-M-o(1)). If A and A' differ by one exchange, then |U_S(A)-U_S(A')|<=m: relative to the common (k-1)-subset, either added element covers between 0 and m previously uncovered points. A random-order exposure of a uniform k-subset has Doob increments bounded in absolute value by m. To verify this, couple completions after two possible next values by the transposition exchanging those two values; the completed subsets differ by at most one exchange. Thus Azuma gives

Pr[U_S=0] <= exp(-(E U_S)^2/(2 k m^2)) <= exp(-c_M sqrt(p))

for a positive constant c_M and all sufficiently large p. The case m=0 is trivial. This proves simultaneous failure for any predetermined family of exp(o(sqrt(p))) such envelopes, including every polynomial-size family. Selecting a member of that family after seeing A does not escape the union bound.

It does not justify a union bound over arbitrary |T|~C sqrt(p), whose count has logarithm (C/2+o(1))sqrt(p) log p. Nor does it allow the family itself to depend on A without an additional deterministic-envelope or conditional argument.

### 2. Fixed bounded-doubling translating sets are excluded

For each fixed C,K, the statement

Pr[there exists T: |T|<=C sqrt(p), |T+T|<=K|T|, A+T=G] -> 0

is valid, subject only to the standard cited Green--Ruzsa theorem.

I independently inspected [Green--Ruzsa, arXiv:math/0505198v2, Theorem 1.1 and the preceding definition](https://arxiv.org/pdf/math/0505198v2). The theorem puts T inside a coset progression with rank bounded in terms of K and cardinality at most a K-dependent constant times |T|. Its definition has a proper progression and a direct subgroup summand. In a prime cyclic group, a progression of size O_K(sqrt(p))<p cannot have the whole group as its subgroup summand; the summand is therefore trivial.

For a fixed rank bound d and size bound M sqrt(p), all proper progressions form a deterministic family of at most (d+1)p^(2d+1) parameter descriptions: choose rank j<=d, j+1 group elements, and j integer side lengths, each at most p. Overcounting is harmless. Since T lies in its progression P, coverage by T implies coverage by P. The fixed-envelope tail beats this polynomial union bound.

The constants C,K,d,M are fixed in the preceding proof. The final structure manuscript also proves, with explicit finite-p errors, a growing-K extension under K_p^4 log^2(K_p+2)=o(log log p). I checked that extension: M_p=(log p)^o(1), d_p=o(log log p), and the negative logarithm of the fixed-envelope bound is p^(1/2-o(1)), beating the O(d_p log p) envelope entropy. Its hypergeometric lower bound follows from log(1-x)>=-x-x^2 for 0<=x<=1/2. All cardinality and error hypotheses hold eventually.

The small-difference corollary also checks out. If |T-T|<=H|T|, apply [Petridis, arXiv:1101.3507v3, Theorem 3.1](https://arxiv.org/pdf/1101.3507v3) to base set T and increment -T. A nonempty X subset T satisfies |X-2T|<=H^2|X|. Since this contains one translate of -2T, |T+T|<=H^2|T|. Thus fixed H, and the stated slow growing-H regime, reduce correctly to the sum-doubling result.

### 3. A fixed number of affine copies of A is also excluded

The constructive argument's proposed statement is valid: for every fixed r, with high probability every envelope

B(A)=union over j<=r of (s_j+lambda_j A), lambda_j nonzero,

leaves a positive proportion of G outside A+B(A), simultaneously for all choices of its parameters, including parameters chosen after inspecting A. Any T contained in B(A) leaves at least those same holes.

For fixed parameters and a target point x, put an undirected edge between a,b when a+lambda_j b+s_j=x for some j. Each j contributes at most two neighbors at any vertex. There is at most one loop vertex per j unless lambda_j=-1 and x=s_j. Exclude those at most r exceptional values of x. Outside the exceptions, degree is at most 2r and there are at most r forbidden loop vertices.

The event x notin A+B(A) is exactly that A avoids loops and contains no graph edge. After h valid distinct sample points have been exposed, at most r+2rh additional vertices are forbidden. Consequently its probability is at least

product over 0<=h<k of [1-(r+2rh)/(p-h)] = exp(-r-o(1)),

for fixed r. Hence E|G\\(A+B(A))| >= (exp(-r)-o(1))p. Exchanging one element of A alters at most 4rk possible sum values. The same exposure coupling gives a lower-tail bound exp(-Omega_r(sqrt(p))). There are at most p^(2r) parameter vectors, so a union bound proves the simultaneous statement. The exceptional x values affect only O(r) points, not the asymptotic mean.

The assumptions r fixed and nonzero multipliers are explicit. This does not exclude a number of affine copies growing without a verified quantitative extension, or arbitrary T lacking this form.

### 3a. Stronger arbitrary-elementwise-map theorem

The final constructive manuscript substantially strengthens the affine result. Fix r, and allow arbitrary predetermined maps phi_j:G->G. Put T_Phi(S)=union_j phi_j(S) and F_Phi(S)=p-|S+T_Phi(S)|. The theorem holds simultaneously over any predetermined exp(o(k))-size menu of r-tuples, after which the tuple and a subset of its output may be selected fully adaptively.

I independently verified its loop, dependence, and model-transfer steps. For Bernoulli-q B and a fixed x, noncoverage is the intersection of rp indexed decreasing events forbidding the simultaneous inclusion of b and x-phi_j(b). Let L_x count coincidences of those two coordinates; then sum_x L_x=rp. Harris positive correlation applies even when events repeat, giving

Pr[x uncovered] >= (1-q^2)^(rp-L_x)(1-q)^L_x
                  = (1-q^2)^(rp)(1+q)^(-L_x).

Jensen's inequality gives E F_Phi(B)>=p(1-q^2)^(rp)(1+q)^(-r), without assuming degree bounds or map injectivity. Take q=(k+k^(2/3))/p and couple B as the first N points of a uniform random ordering, N~Bin(p,q), with A its first k points. The function F_Phi is decreasing under inclusion. Thus E F_Phi(A)>=E F_Phi(B)-p Pr[N<k]. The error is o(p), since Pr[N<k]<=exp(-Omega(k^(1/3))). Also rpq^2=r+o(1). Therefore E F_Phi(A)>=(e^(-r)-o(1))p uniformly over maps.

One exchange of A changes at most 4rk output sum values. Direct uniform-k concentration, rather than transferring a Bernoulli tail, now gives

Pr[F_Phi(A)<(e^(-r)-epsilon)p]
 <= exp[-epsilon^2 p^2/(128 r^2 k^3)]
 <= exp[-epsilon^2 sqrt(p)/(128r^2)]

for every fixed epsilon in (0,e^(-r)) and sufficiently large p. The exp(o(k)) menu union bound is valid. Subsets of T_Phi(A) leave more holes. Moreover any arbitrary o(sqrt(p)) extra centres cover only o(p) additional points, so cannot repair the positive-density residual. This also absorbs the at most 99-centre discrepancy between the two caps.

The family of all permutations, or of all maps tailored unrestrictedly to A, is not a permissible menu. The final manuscript explicitly limits such examples. This theorem is a meaningful restriction on collective construction mechanisms, not a lower bound on the unrestricted optimum.

### 3b. Seed-compression obstruction

The alternative-route argument supplied a further valid theorem, independent of the map-envelope theorem. Let s=o(k), and fix before sampling A a decoder F assigning to each s-subset B a translating set T_B of size at most m=floor(C sqrt(p)), for fixed C>0. Then with high probability no B subset A makes A+T_B=G. The same is true over exp(o(k)) predetermined decoders, with the decoder and seed selected after seeing A.

Here is the exact conditional argument checked independently. Conditional on B subset A, write A=B union R, where R is uniform among (k-s)-subsets of G\B. Put W=G\(B+T_B). For every x in W, x-T_B is disjoint from B. Thus

E[uncovered | B subset A]
 = |W| binom(p-s-|T_B|,k-s)/binom(p-s,k-s)
 >= (p-sm) binom(p-s-m,k-s)/binom(p-s,k-s).

For s=o(k), the last ratio is exp(-C+o(1)) and p-sm=(1-o(1))p. Exchanging one point of R changes the uncovered count by at most m. Conditional concentration therefore bounds the covering probability by exp[-(e^(-2C)/(2C^2)+o(1))k], uniformly over B and F.

Crucially, one must count eligible seeds by their containment probability, not union-bound over every B in G. If Z(A) counts successful B subset A of size s, then

E Z = binom(k,s) average over all B of Pr[A+T_B=G | B subset A].

This identity follows from Pr[B subset A]=binom(k,s)/binom(p,s). Since log binom(k,s)=o(k), the count still tends to zero after the allowed decoder-menu union bound. The range of a decoder can have more than exp(O(k)) outputs, so this extends the small-fixed-output-menu theorem rather than simply restating it.

It does not prove that every possible covering T admits such a small seed description. Establishing a universal compression theorem of that kind would be a genuinely new and presently missing structural lemma. The final manuscript has been read. It correctly extends to every seed size at most s_p=o(k), and to a positive-density residual (e^(-C)-epsilon)p. Consequently arbitrary o(k) additional translates cannot repair these decoded outputs. The claimed linear-seed tradeoff also checks: if s/k->alpha<min(1,1/C), log L/k->rho, then a sufficient exclusion condition is

rho+h(alpha) < (1-C alpha)^2 exp[-2C(1-alpha)]/[2(1-alpha)C^2].

This is only a sufficient region; reversing the inequality does not imply existence of a cover. Some strictly positive alpha is allowed by continuity at zero, though the resulting constants at C=100 are extremely small.

### 4. Divergent witness expectation survives inclusion-minimality

Let A0={0,...,k-1}, and m=ceil(3p/(2k)). Partition the cyclic order into m consecutive cells of lengths q or q+1, where q=floor(p/m). From each cell choose one start point among its first w=floor(k/24) positions. There are w^m distinct choices of T.

Each cyclic gap between successive starts lies between q-w+1 and q+w. Indeed q>2k/3-13/9 and q<=2k/3; hence q+w<=17k/24<k and q-w+1>5k/8-4/9. Thus every gap is at most k and the sum of every two neighboring gaps is greater than k for k>=24. The first condition is exactly interval-translate coverage; the second says deleting any chosen start creates an uncovered gap. Thus every constructed T is an inclusion-minimal cover of A0.

For the random uniform A, if M(A) counts all inclusion-minimal covers using at most c translates, then m<c eventually and

E M(A) >= w^m / binom(p,k) = exp((1/2+o(1)) k log k) -> infinity.

The coefficient follows from m=(3/2+o(1))k and log binom(p,k)=(1+o(1))k log k. This is a genuine obstruction to proving nonexistence through the untruncated first moment of all witnesses, even inclusion-minimal witnesses. It does not imply that a typical A has a witness. It also does not defeat counting only canonical witnesses, weighting witnesses, truncating to a high-probability class of A, or other tail inequalities.

### 5. Rare structured samples prevent a uniform superlinear fixed-T exponent

Take a deterministic interval T of length floor(C sqrt(p)), with C>2 fixed. Partition G into k consecutive blocks, of lengths floor(p/k) or ceil(p/k). The event that A has exactly one point in every block has probability

product(block lengths) / binom(p,k) = exp(-k+O(log k)).

On this event every cyclic gap between A points is at most 2ceil(p/k)-1, which is below |T| for sufficiently large p. Therefore A+T=G. This lower bound is applicable to C=100 and rules out a bound exp(-omega(k)) uniform over all fixed T at that size.

For 1<C<=2, the same unrestricted one-per-block event does not suffice; one must restrict positions within blocks or change the construction. This issue does not affect the target constant 100.

## Reductions that fail or need additional proof

### Growing-edge nibble

I independently checked the [Alon--Bollobas--Kim--Vu author PDF, Theorem 1.2](https://web.math.princeton.edu/~nalon/PDFS/abkv4.pdf). Its growing-uniformity economical-cover theorem has an exponentially restrictive relation between uniformity, maximum codegree and degree. The constructive argument correctly observes that it fails at uniformity=degree~sqrt(p), even with codegree one. Its edge-splitting corollary does not give the requested square-root cost.

The translate hypergraph has p vertices and p edges, uniformity k and degree k. A small ratio of maximum pair-codegree to degree cannot alone yield a near-perfect matching when k grows. Projective-plane incidence hypergraphs of order q have q^2+q+1 vertices, edge size and degree q+1, and pair-codegree 1, but every two edges intersect, so their matching number is 1. Any matching/nibble invocation must state and verify the theorem's dependence on uniformity. This counterexample challenges a generic implication; it is not a counterexample to the target random-set problem. Indeed pencils of lines give small covers in a projective plane.

### Fresh-reservoir diagonal coverage

A theorem about union_i(A_i+T_i), with T_i chosen before fresh A_i, need not control the actual union_{i,j}(A_i+T_j). Older samples can be used adaptively to choose later translating sets, and the cross terms may supply coverage. A diagonal-only residual calculation is a failed-route diagnosis, not a no-go theorem for the full target. The constructive argument explicitly acknowledged this distinction.

### Bernoulli-to-fixed-size transfer

Conditioning a Bernoulli sample with inclusion probability k/p on cardinality k recovers the exact model, but costs the reciprocal of Pr[Bin(p,k/p)=k], of order sqrt(k). An exp(-c sqrt(p)) error survives this; a bare o(1) error need not. Monotone coupling also requires correctly directed cardinality slack. Concentration around sqrt(p) alone does not identify the exact floor-size model.

### Rounding and quantifier order

The operational cap differs from 100k by 0 through 99. A proof at cap 100k transfers upward, and a negative result for the operational cap transfers downward. Converse claims need additional control. Neither tau<=(100+o(1))sqrt(p) nor tau>=(100-o(1))sqrt(p) resolves the endpoint. All restricted-class results in this audit concern fixed constants; their thresholds may depend on those constants. They do not make any assertion uniform over a parameter growing with p unless separately proved.

## Strongest unproved step

The surviving difficulty is not an estimate for one fixed T. It is a model-correct control of the existence of completely unrestricted A-dependent T of size at most c. Neither bounded-doubling exclusion, bounded-elementwise-map exclusion, nor the seed-compression theorem implies a dichotomy covering all witnesses.

A potentially sufficient negative-route lemma would be a high-probability canonical-witness/structural reduction that reduces all possible covering T to a family whose effective entropy is beaten by a rigorous joint coverage tail. Such a reduction must handle high-doubling T, dependence on A, and rare structured A without counting their huge witness multiplicities. No such lemma is proved here. Equivalently, on the constructive side, no algorithm or existence argument has eliminated all residual holes with a total of at most c translations.

Until that unrestricted step is supplied, the correct outcome is partial progress with the target unresolved.

## Ordinary LP and literature screening

The alternative argument's fractional-program obstruction is exact. Every translate-covering constraint summed over x gives k times the total weight at least p, and uniform translate weights 1/k attain p/k. The dual and fractional matching programs likewise attain p/k by uniform weights, with the reverse inequality obtained by summing all constraints. Thus the ordinary nonnegative LP dual cannot certify a lower bound exceeding p/k; it says nothing about the integral covering number or the strength of higher-order relaxations.

I independently inspected the current [Rodgers--Sahay publisher article](https://onlinelibrary.wiley.com/doi/10.1002/rsa.70089): Theorem 1 fixes the Bernoulli density; Remark 1.2 leaves the decreasing-density regime unpursued; Remark 1.8 distinguishes fixed-size and symmetric-generator models. Lemma 6 is the logarithmic translate-covering bound. These statements do not answer the contract. The paper explicitly distinguishes open from closed neighborhoods, reinforcing that a domination translation must not add automatic coverage of selected vertices.

I also independently inspected [Alon--Pham, Random Cayley graphs and random sumsets](https://web.math.princeton.edu/~nalon/PDFS/randomss5.pdf), Theorems 4, 6 and 8. Their conclusions concern independence, structured subsets contained in sumsets, and arithmetic-progression lengths in A+A. None of those assertions is an adaptive translate cover at the stated budget. No model-preserving reduction has been supplied.

The BJR fixed-T entropy inequality and ordered, diagonal-included Janson convention were checked directly in [the v2 PDF, Remark 4.3 and equation (4.5)](https://arxiv.org/pdf/0910.3815v2). The entropy argument's self-contained derivation and optional Bernoulli-parameter optimization are valid; the latter changes a constant but cannot overcome the rare-interval lower bound.

