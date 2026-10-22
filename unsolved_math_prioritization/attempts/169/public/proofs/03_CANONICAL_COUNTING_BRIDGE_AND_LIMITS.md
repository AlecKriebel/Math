# Stage 3 entropy argument: canonical covers, weighted certificates, and the missing additive bridge

Public mathematical edition. The source problem remains UNSOLVED by this five-stage study. Historical statements with residual swap bound 2m and Azuma denominator 8km² remain valid conservative estimates; the final synthesis uses the sharpened m and 2km² bounds. Stage labels record provenance, not additional assumptions. No claim of external peer review or priority is made.


Date: 14 October 2026. Mathematical study stage 3.

## Decision

No upper bound resolving the unrestricted covering event is proved. This pass does not reuse the rare interval or stratified first-moment examples as though they survived stronger typicality.

The report gives:

1. a noncircular template for a simultaneous typical event that excludes the previously established simple covering classes, with the necessary quantifier guard;
2. an exact normalized count of genuine inclusion-minimal covers, eliminating padding and multiple-witness overcounting;
3. a proved weighted, fixed-codebook compression criterion that would settle the negative direction if an appropriate additive compression theorem were supplied; and
4. an explicit abstract incidence countermodel showing that fixed-witness rarity, prescribed simple-core exclusions, translation symmetry, genuine minimality, and sublinear-seed decoder barriers do not themselves imply that compression theorem or an adaptive probability bound.

The countermodel is **not** an additive counterexample. It does not purport to satisfy the identities specific to A+T, the exact hole means, swap-Lipschitz residuals, or all of the previous constructive examples. Its role is to falsify a counting-only implication and identify the indispensable missing use of the sumset equations.

## 1. Exact contract and a legal simultaneous truncation

Let p tend to infinity through primes, `k=floor(sqrt(p))`, `c=floor(100 sqrt(p))`, and let P_p be uniform on the k-subsets of G=Z/pZ. Define

`E_p={there exists T subset G, |T|<=c, A+T=G}`.

For sufficiently large p, `0<k<c<p`.

A negative answer requires `P_p(E_p)<=1-epsilon` along arbitrarily large primes for some fixed epsilon>0. A bound tending to zero would be stronger. We do not claim either.

### 1.1 A concrete admissible typical-event template

Fix in advance the following parameters and families:

- a fixed number r of progression components;
- a fixed affine-envelope size R, which may be chosen at least 8;
- the explicit growing threshold `K_p=(log log p)^(1/8)` for sufficiently large p;
- a predetermined family of seed decoders of size exp(o(k)), with seeds of size at most a specified s_p=o(k), and outputs of size at most c.

Take H_p to be the intersection of:

(a) the precise autocorrelation/Fourier/energy Good event proved in Stage 2;

(b) absence of a cover of size at most c that is a union of at most r cyclic arithmetic progressions;

(c) absence of a cover of size at most c with doubling at most K_p;

(d) the previously proved positive-density hole condition for every bounded affine envelope X-A with |X|<=R;

(e) failure of all the specified decoder/seed outputs to cover.

Every quantifier in this definition is over a class for which a simultaneous result was proved in Stage 1 or Stage 2. In (c), `K_p^4 log^2(K_p+2)=o(log log p)`, so the audited growing-doubling theorem applies. Since the intersection has a fixed finite number of high-probability conditions,

`P_p(H_p)=1-o(1)`.

The stratified exceptional family from Stage 2 is removed by (b), because it has a short interval cover. The Singer examples from Stage 2 are removed by (d) when R>=8, by their explicitly proved eight-shift containment and the resulting O(k) residual. Therefore those examples do not refute a count genuinely restricted to H_p.

This template can be specialized to any fixed, explicitly stated finite collection of the already audited classes. It is not a simultaneous statement over every conceivable decoder or every conceivable finite menu.

### 1.2 The essential quantifier guard

Stage 1 proves that for each predetermined menu F_p with log|F_p|=o(k), the probability of finding a cover in F_p tends to zero. It does not provide one high-probability set of inputs that works for every possible such menu at once.

Every individual T is itself a one-element predetermined menu. Taking the union of the success events over all singleton menus is exactly E_p. Thus a claim that one may freely intersect the failure events for every low-entropy menu would already assert the desired negative conclusion.

The same issue applies to arbitrary decoders: a decoder with empty seed can hardcode any chosen T. Its index/description must be counted in a family fixed independently of A. A decoder chosen after seeing A without paying for its identity is not a compression theorem.

## 2. Exact normalization of genuine minimal witnesses

For a given A let M_c(A) be the family of inclusion-minimal translating covers T with |T|<=c, and put `m_c(A)=|M_c(A)|`.

Every cover contains an inclusion-minimal subcover. Hence

`E_p = {m_c(A)>0}`.

Define the contribution of a witness T to be zero when m_c(A)=0, and otherwise

`w(A,T)=1[T in M_c(A)] / m_c(A)`.

Then the following is an exact finite identity:

`P_p(H_p and E_p)`

` = sum_{1<=|T|<=c} E_p[1_Hp 1[T in M_c(A)] / m_c(A)]`.       (2.1)

This count imposes coverage and minimality jointly. Padding is not counted as a new minimal witness, and the normalization counts each successful A exactly once, whatever its number of minimal covers.

Equivalently, when the conditioning event has positive probability, a summand is

`P_p(H_p and T in M_c(A))`

`  * E_p[1/m_c(A) | H_p and T in M_c(A)]`.                     (2.2)

A deterministic canonical selector, for example least cardinality followed by lexicographic order, gives another exact identity by replacing the weight with the indicator that T is the selected witness. Its events are disjoint across T. It does not by itself estimate their probabilities.

### 2.1 What symmetry supplies, and what it does not

For a nonempty proper T in a prime cyclic group, its p translations are distinct. If T covers A inclusion-minimally, every translate T+x also does, with the same cardinality. Consequently

`m_c(A)>=p` whenever E_p occurs.

This permits an automatic factor-p normalization. Its logarithm is only O(log p), whereas candidate-set entropy is of order k log k. No stronger witness-multiplicity conclusion follows solely from translation symmetry.

A genuine finite additive warning is available: at p=19,

`A={0,2,3,7}`

has maximum nonzero autocorrelation 1, minimum covering number 6, and exactly 19 minimum covers. The set

`T={0,2,6,10,11,13}`

is one of them, and its translations are all the minimum covers. Thus even a Sidon set can have only one minimum-cover orbit. This refutes a blanket finite lemma asserting many minimum-cover orbits from low codegree. It does not refute an asymptotic statement for a stronger H_p, and the cap 100 is vacuous at this small prime.

### 2.2 The actual missing normalized estimate

To prove a negative answer by this route, it would suffice to prove that the right side of (2.1) is at most 1-epsilon along an unbounded prime sequence; an o(1) bound would be stronger. Existing fixed-T bounds only control the first factor of (2.2). They do not bound its product with the conditional inverse multiplicity strongly enough after summation.

Typicality must be imposed inside the conditioning event. Replacing the second factor by an unconditioned expected inverse count, or treating private witnesses as independently sampled data, would be unjustified. A lower bound on an unconditional witness count does not provide the needed lower bound on m_c(A) under each cover-conditioned law.

Thus normalization repairs the exact overcounting defect, but the remaining cover-conditioned inverse-multiplicity estimate is an additional mathematical theorem, not an automatic consequence of canonical choice.

## 3. A proved weighted compression criterion

Here is a sufficient bridge that genuinely applies to the full target if its stated compression premise can be proved.

Fix, independently of A, a finite or countable collection of deterministic decoders F_j. Each decoder accepts a subset B of G of size at most s_p and returns a translating set of size at most c. Give the decoders nonnegative fixed weights w_j with

`sum_j w_j <= 1`.

Its code cost is `-log w_j`, with zero-weight decoders unusable. This is a weighted-codebook formulation; no literal programming-language description is required.

Suppose `s_p=o(k)`, and define

`Z(A)=sum_j w_j sum_{B subset A, |B|<=s_p} 1[A+F_j(B)=G]`.

Then

`E_p Z(A) <= exp[-(gamma_100+o(1))k]`,                       (3.1)

where `gamma_100=exp(-200)/(2*100^2)>0`.

### 3.1 Proof and exact conditioning

Use the already audited conditional-completion bound from Stage 1. For a fixed seed B of size s and any fixed T of size at most c, condition a uniform k-set A on B subset A. The remaining k-s points are uniform outside B. At least p-sc points lie outside B+T, and for each such point the probability of being missed by the remaining translates is at least

`q_s=binom(p-s-c,k-s)/binom(p-s,k-s)`.

The uncovered count changes by at most c on an exchange of a remaining sampled point. Exposing the sample and coupling completions by a transposition gives the finite Azuma estimate

`P_p[A+T=G | B subset A] <= exp(-D_s)`,

`D_s=((p-sc)q_s)^2 / [2(k-s)c^2]`,                           (3.2)

provided s<k, sc<p and c<=p-k. These conditions hold uniformly over 0<=s<=s_p for large p. Also, uniformly in that range,

`D_s=(gamma_100+o(1))k`.

The seed is fixed before applying (3.2), so T=F_j(B) is fixed in that conditional calculation. Double counting all seeds gives

`E_p sum_{B subset A, |B|=s} 1[A+F_j(B)=G]`

` <= binom(k,s) exp(-D_s)`.

Multiply by w_j, sum over j using its total mass at most one, then sum over s. Since

`log sum_{s<=s_p} binom(k,s)=o(k)`,

equation (3.1) follows. Nonnegative sums justify the same argument for countably many decoders. Adaptively choosing a seed after observing A is fully allowed by the counting argument.

### 3.2 The sufficient additive compression theorem

Suppose one could prove the following statement for a particular H_p with P_p(H_p)=1-o(1):

Whenever A belongs to H_p and has any cover of size at most c, there exist B subset A with |B|<=s_p=o(k) and one of the predetermined decoders with code cost at most b_p=o(k), such that A+F_j(B)=G.

Then Z(A)>=exp(-b_p) on H_p intersect E_p. Markov and (3.1) give

`P_p(H_p and E_p) <= exp(b_p) E_p Z(A) -> 0`,

and therefore P_p(E_p)->0.

The decoder may output a canonical minimal cover, any other minimal cover, or any legal cover. What matters is that the decoding rules and weights are fixed independently of the sampled A, and that both the seed and decoder index budgets are paid.

This is a proved implication, not a proof of its compression premise. No argument in this pass shows that optimal translating covers admit such compression. The statement would need a new theorem exploiting the actual equations x=a+t.

Hardcoding all c-element T as decoders is permitted, but their equal code cost is

`log binom(p,c)=(100+o(1))k log k`,

far outside the o(k) allowance. Letting the hardcoded decoder depend on A without recording that cost would discard the essential assumption.

## 4. An abstract countermodel to a counting-only compression claim

The following construction shows precisely why the known counting and minimality facts cannot themselves prove the missing premise. It is not a construction of sets satisfying A+T=G.

Let Omega be the family of all k-subsets and Y the family of all c-subsets. Both decompose into translation orbits of size p. Write

`N=|Omega|=binom(p,k)`, `M=|Y|=binom(p,c)`.

For each A prescribe a forbidden list F(A) of at most f_p candidate c-sets. Assume

`f_p=exp(o(k log k))`.

Examples of allowable lists include specified low-entropy outputs. They also include c-subsets of a specified polynomial-size family of O(k)-sized envelopes: a fixed envelope has at most 2^(O(k)) subsets. Bounded affine envelope families X-A are of this kind, even though the envelopes depend on A.

This does not license forbidding every cap-sized superset of an arbitrary small core: such a family can have exp(Theta(k log k)) members. Small non-successful sets and successful cores must not be conflated.

### 4.1 Orbit assignment

For each A-orbit, union the forbidden lists of its p members. At most p f_p T-orbits meet that union. Greedily assign each A-orbit a distinct T-orbit that meets none of its forbidden lists. This is possible if

`M/p > N/p + p f_p`,

or equivalently

`M > N+p^2 f_p`.                                            (4.1)

Here `log N=(1+o(1))k log k`, `log M=(100+o(1))k log k`, so (4.1) holds for all sufficiently large p.

Declare a candidate c-set successful for A exactly when it lies in the orbit assigned to the orbit of A. Declare no smaller translating set successful. For larger translating sets, declare success when they contain an assigned c-set. This defines a monotone witness relation in the translating-set variable.

It has all of these properties:

- every input A has a successful witness;
- each A has exactly p cap-sized witnesses, all inclusion-minimal and of minimum possible successful size c;
- success is invariant under translating A and under translating T independently;
- no prescribed forbidden cap output is successful;
- for every fixed T, its success probability is exactly p/N if its orbit is used, and zero otherwise.

Thus fixed-T probabilities are at most

`p/N=exp(-(1+o(1))k log k)`,

much smaller than the available uniform fixed-T exponential bounds, while the adaptive success probability equals one.

If the forbidden list includes every c-subset of a specified large envelope, that envelope is also unsuccessful in the upward extension. All smaller proposed cores are unsuccessful by construction. These statements concern the abstract relation only.

### 4.2 Decoder barriers also coexist with universal success

Take any predetermined family of L_p=exp(o(k)) decoders using seeds of size at most s_p=o(k). The total possible output range is at most

`L_p sum_{s<=s_p} binom(p,s) = exp(o(k log k))`.

Each output succeeds on at most p inputs. Therefore the fraction of inputs for which any such decoder can succeed, even with an adaptively selected seed, is at most

`[p L_p sum_{s<=s_p} binom(p,s)] / binom(p,k)`

` = exp(-(1-o(1))k log k) -> 0`.                             (4.2)

The argument is uniform over the chosen decoder rules; it uses only their domain/range count. Nevertheless every A has a cover in this abstract relation. Its canonical witness necessarily retains essentially all the input-orbit information, of entropy log(N/p).

Hence the facts that a cover is genuine and minimal, fixed witnesses are extraordinarily rare, specified simple outputs are absent, and sublinear-seed decoding fails do not force a small-description canonical cover. Additional information specific to additive covering is essential.

### 4.3 Scope limitation of the countermodel

The constructed relation is not claimed to be generated by translates of a k-set. It need not have the correct exact expected residual, exchange-Lipschitz behavior, pair intersections, private-point incidence equations, monotonicity when A changes size, or fixed-interval lower bounds. It cannot refute an argument that genuinely uses such additional properties.

What it does refute is a purported general counting lemma whose only inputs are the properties listed in Sections 4.1-4.2. Normalizing by p gives exactly one witness orbit per A in this model, so canonicalization does not manufacture a small event probability.

## 5. Remaining mathematical task

The stronger H_p removes the known simple exceptional examples without any invalid universal intersection. Genuine cover/minimality can be imposed exactly through (2.1). Neither step supplies the needed numerical bound.

A successful continuation needs one of the following genuinely additive statements:

- a uniform or appropriately averaged cover-conditioned inverse-multiplicity estimate making (2.1) at most 1-epsilon on an unbounded prime sequence;
- a predetermined sublinear-seed, sublinear-advice compression theorem of the form in Section 3.2, applying to a non-negligible fraction of hypothetical successful inputs; or
- another cover-specific certificate theorem with an explicitly controlled codebook and a verified probability bound.

No such statement is proved or assumed here. The useful outcome is the exact criterion and a countermodel to deriving it from the already available counting facts alone. The full probability-limit question remains open after this argument.

