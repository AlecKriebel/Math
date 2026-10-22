# Independent mathematical audit of the prior EP-538 matching-order claim

Audit date: 2026-10-10. Problem identifier: 2166 / EP-538.

## Decision and scope

**Accepted as a conventional mathematical proof of the fixed-parameter matching order.** The argument below independently reconstructs all load-bearing steps of the prior STARFLEET claim, including its two stated finite inequalities. No mathematical correction is needed for that scope. This is an audit of a prior public claim, not a new-priority claim.

For each fixed integer r ≥ 2, the maximum reciprocal mass is

    E_r(N) = Θ_r(log N / log log N), as N tends to infinity.

The accepted theorem does not give the exact finite maximum, a sharp leading constant, or matching dependence on an unbounded parameter r. The conventional proof is accepted independently of the publisher's formal-verification assertion. No Lean compiler, dependency installation, build, downloaded script, or source program was executed in this audit. Consequently, a clean formal build and its transitive axiom report are **not independently reproduced** here.

Public sources:

- P. Erdős, *Problems and Results on Combinatorial Number Theory* (1973), section 4, printed p.124, equation (4.5): https://www.renyi.hu/~p_erdos/1973-21.pdf
- STARFLEET Math, *Erdős Problem #538: the matching-order bound*, report in section 10: https://www.starfleetmath.com/
- Associated complete verification archive: https://www.starfleetmath.com/downloads/verify/erdos-538/erdos-538-solution.zip

## 1. Exact problem and finite assertions

Let A be a subset of the positive integers at most N, and put S(A)=Σ_{a∈A}1/a. Admissibility at cap r means that **for every integer m**, the number of pairs (p,a) with p prime, a∈A, and m=pa is at most r. There is no squarefreeness or coprimality assumption on arbitrary admissible A. Since p and a are positive, nonpositive m have no representations; universal quantification over natural m is therefore equivalent.

The inspected original page presents the weighted-incidence upper bound of order r log N/log log N and asks whether it can be improved. Its nearby positive-density construction inside a single interval is not, by itself, a lower bound growing at this reciprocal-mass scale.

Write L(N)=floor(log_2 N) for N≥1, set L(0)=0, and define ell(N)=floor(log_2 L(N)) when L(N)≥1, with ell(N)=0 when L(N)=0. Thus ell(N) is exactly the nested natural-number logarithm used by the archive; there is no interpretation of log_2 0 as an ordinary real logarithm.

The finite statements being accepted are:

1. For every r≥2, N≥2, and admissible A,

       log(log(N+1)) S(A) ≤ 2r (1+log(N²)).

2. For every N≥0 there is A⊆{1,…,N} with global cap two such that

       log(N+1) ≤ 4 + 8192(ell(N)+1) S(A).

   The N=0 case is interpreted with the empty set. The combined submitted theorem states N≥2; its lower-bound component in fact covers every natural N. Increasing the allowed cap from two to r≥2 preserves this same witness.

All logarithms without a subscript in this audit are natural logarithms.

## 2. Universal incidence upper bound

Let P(X)=Σ_{p≤X, p prime}1/p and H_t=Σ_{1≤j≤t}1/j. For any positive integer X,

    S(A)P(X) = Σ_{a∈A}Σ_{p≤X}1/(pa) ≤ r H_{NX}.

Indeed, regroup by m=pa. Every product is at most NX and each fiber is a subset of the full globally bounded representation fiber. Restricting p for this sum does not restrict the admissibility assumption. In particular, this proof is not using a cap only for m≤N.

Unique factorization and geometric series give

    H_N ≤ ∏_{p≤N}(1-1/p)^(-1).

Every integer up to N occurs in the expansion on the right, and all terms are nonnegative. For p≥2,

    log((1-1/p)^(-1)) ≤ (1-1/p)^(-1)-1
                            = 1/(p-1) ≤ 2/p.

Taking logarithms yields log H_N≤2P(N). The integral comparison gives log(N+1)≤H_N≤1+log N for N≥1. Multiplying the preceding bound by S(A)≥0, applying incidence with X=N, and bounding H_{N²} proves assertion 1 exactly.

For N≥2, log(N+1)>1, so log(log(N+1)) is positive. Thus division by the displayed factor is legitimate throughout the claimed upper-bound range. The theorem does not divide by log log N at the small endpoint N=2.

## 3. Finite-field construction: favorable children

Fix k≥2 and put d=k-1. Let K be a field of odd order q. On a palette of m vertices, assign each vertex v a label (phi_v,c_v)∈K^d×K. For a k-subset S define the linear map

    Psi_S(lambda)=Σ_{v∈S}lambda_v phi_v

and the diagonal symmetric bilinear form

    B_S(lambda,mu)=Σ_{v∈S}c_v lambda_v mu_v.

A favorable S has rank(Psi_S)=d, its one-dimensional kernel has a full-support generator lambda, B_S(lambda,lambda)=0, and the coefficient vector c on S is nonzero. These properties are intrinsic and unaffected by rescaling lambda.

Order the child coordinates as 0,1,…,d and normalize lambda_0=1. Write lambda=(1,t_1,…,t_d), with all t_i≠0. The remaining d column vectors b_i=phi_i must be a basis: any relation among those columns would extend by a zero coordinate to a relation on S, contradicting full support. Conversely, choose such a basis and a nonzero tail t, and put

    phi_0 = -Σ_i t_i b_i.

The resulting matrix has rank d and exactly the required kernel. This is a bijection, not just a surjection: the sample determines the b_i and its uniquely normalized kernel determines t.

For fixed t, isotropy is the nonzero linear equation

    c_0 + Σ_i c_i t_i² = 0.

Its solution space has q^d elements; exclude the zero vector. Consequently the exact number of favorable child samples is

    G=(q-1)^d [∏_{i=0}^{d-1}(q^d-q^i)] (q^d-1).

There are q^{(d+1)²} total child samples. Their favorable fraction equals

    q^(-1)(1-1/q)^d [∏_{i=0}^{d-1}(1-q^{i-d})](1-q^(-d)).

If q≥2(d+1), Bernoulli's inequality gives (1-1/q)^d≥1-d/q≥1/2. Every factor in the middle product is at least 1-1/q, so that product is also at least 1/2. Finally 1-q^{-d}≥1/2, since d≥1 and q≥2. The favorable fraction is therefore at least 1/(8q). The dimension d≥1 and the nonzero-c condition are both used here and below.

## 4. The precise dangerous fraction

Fix a favorable child in the preceding coordinates. Write an outside column as phi_x=Σ_i a_i b_i, and its coefficient as c_x. A basis of the parent relation space consists of

    u=(1,t_1,…,t_d,0),
    v=(0,-a_1,…,-a_d,1).

These vectors are independent, are relations, and span the kernel because the parent has d+2 columns and rank d. The restriction of the diagonal form to this plane vanishes identically if and only if its three basis entries vanish. The first, B(u,u), already vanishes. The other two conditions are precisely

    Σ_i c_i t_i a_i = 0,
    c_x = -Σ_i c_i a_i².

The functional a↦Σ_i c_i t_i a_i is nonzero. Otherwise each c_i for i≥1 would vanish, since t_i≠0, and child isotropy would force c_0=0 as well. This contradicts c≠0.

There are consequently q^{d-1} choices of a, and for each a exactly one choice of c_x. The coordinate map a↦phi_x is bijective. Among q^{d+1} outside labels, exactly q^{d-1} are dangerous: the fraction is exactly 1/q².

Call a favorable child safe when none of the other palette vertices has a dangerous label for it. Conditional on its child labels, a union bound gives unsafe probability at most (m-k)/q². Thus, if 2(m-k)≤q², at least half the outside assignments are safe. Independence between distinct children is not required. A fixed child is safe with probability at least 1/(16q), so linearity of expectation supplies a single palette labeling with at least binom(m,k)/(16q) safe children.

## 5. Why every parent has at most two safe facets

Consider a (k+1)-subset T of palette vertices containing a selected facet. Its matrix has rank d, because the selected facet already has rank d, so its relation space has dimension two. A selected facet omitting x contributes a nonzero isotropic vector on that plane whose only zero coordinate is x. Two different omissions give distinct lines: proportional vectors would have the same zero positions.

Suppose three selected facets exist. Let their relation lines be represented by u,v,w. The first two span the plane and w=au+bv with a,b both nonzero, because the third line is distinct from the first two. Symmetry and isotropy imply

    0=B(w,w)=2ab B(u,v).

Odd characteristic gives B(u,v)=0. Together with B(u,u)=B(v,v)=0, this says the form is zero on the whole relation plane. For any of the selected facets, its omitted vertex is then a dangerous extension. This contradicts safety. The cap is therefore two.

Bertrand's postulate supplies a prime 2k<q≤4k. It is odd. Choose m=2k². Both q≥2k and 2(m-k)≤q² hold. The resulting family F of k-subsets of the m-color palette obeys

    |F| ≥ binom(m,k)/(16q) ≥ binom(m,k)/(64k),

with at most two selected facets in every (k+1)-subset. This construction only needs the standard existence theorem for a prime between x and 2x; it makes no effective-complexity or explicit-enumeration claim about the best labeling.

## 6. Weighted transfer and repeated colors

Take any finite collection of k-element supports, with arbitrary nonnegative weights. Color all ground elements independently and uniformly with m=2k² colors. A fixed support fails to be rainbow with probability at most binom(k,2)/m=(k-1)/(4k)<1/2. Weighted expectation therefore produces a coloring whose rainbow supports carry at least half the original weight.

Now fix that coloring and uniformly permute the m colors. Each rainbow support maps to a uniformly distributed k-subset of the palette. It lands in F with probability |F|/binom(m,k)≥1/(64k). Another weighted averaging step chooses a permutation retaining at least 1/(128k) of the original weight. This argument works for completely nonuniform weights; it does not replace weighted mass by support cardinality.

To check the cap after transferring back to a larger ground set, inspect any parent support with k+1 distinct ground elements. If its colors are all distinct, selected deletions correspond to selected facets of one palette parent and there are at most two. If its colors repeat, deletion can leave distinct colors only when the parent has exactly one color appearing twice and every other color appearing once. Only the two occurrences in that repeated pair can then be deleted. In every other repetition pattern there are no rainbow deletions. Equal colors are therefore counted with their full occurrence multiplicity, without breaking cap two.

## 7. Transfer to all integer products

For k≥2, apply the weighted construction to supports of squarefree integers a≤N with exactly k prime factors, assigning weight 1/a. Unique factorization identifies each such integer with its support. It gives a subfamily A_k retaining at least 1/(128k) of the layer's reciprocal mass.

We now check the original condition for **every m**, not just m≤N, and with no restriction on the multiplier prime.

- If m is squarefree and has a representation m=pa with a∈A_k, its prime support has k+1 elements. Distinct representation pairs use distinct primes and correspond to deleting those elements. The preceding colored-parent argument bounds their number by two.
- If m is not squarefree, at most one prime p can make m/p squarefree. Indeed, a prime with exponent at least two must be the deleted prime; its exponent must be exactly two and all other exponents must be one. If either requirement fails there are no such representations. Thus this case has at most one representation.
- m≤0 has none. The family always lies in [1,N] by construction.

For k=1 take all primes at most N. A product of two primes has at most two representations, and a square of a prime has one. This entire layer is already cap-two and trivially retains at least 1/(128k) of its mass. No finite-field argument with d=0 is needed.

Unite independently chosen A_k for 1≤k≤K. In every representation m=pa, the total number Ω of prime factors, counted with multiplicity, satisfies Ω(a)=Ω(m)-1. Thus every representation of a fixed m uses a single exact Ω-layer. Since members of A_k are squarefree, their Ω-value is k. The layer caps do not add when the families are united. If M is the reciprocal mass of their union and W_{≤K} the mass of squarefree integers with 1≤Ω≤K, then

    W_{≤K} ≤ 128 K M.

This proves the crucial global transfer. It is legitimate that the lower witnesses are squarefree: they are a subclass of the sets allowed in the original maximization, whereas the upper estimate applies to arbitrary sets.

## 8. Harmonic mass, truncation, and the constant 8192

Let W be the mass of all positive squarefree integers at most N. Every positive integer can be written uniquely as b²a with a squarefree. Dropping the cutoff on that product, but keeping a,b≤N, gives

    H_N ≤ W Σ_{b≤N}1/b² ≤ 2W.

The last bound is elementary: the b=1 term is one, and for b≥2 use 1/b²≤1/(b(b-1)) and telescope.

Let J=Σ_{a≤N, squarefree}Ω(a)/a. Expand Ω(a) as the number of prime divisors and write a=pb. Enlarging the resulting region to the full prime-by-integer rectangle yields

    J ≤ P(N)H_N.

If T is the mass of squarefree terms with Ω≥K+1, then (K+1)T≤J by termwise comparison. The remaining squarefree terms consist of the unit, the layers 1,…,K, and this tail. Hence

    (K+1)W ≤ (K+1)(1+128KM)+P(N)H_N.

If K+1≥4P(N), then T≤H_N/4≤W/2. Consequently W≤2(1+128KM), and

    H_N ≤ 4+512KM.                                           (A)

For completeness, the prime-harmonic bound needed for the specified K has an elementary derivation without trusting a formal-library theorem. In the block 2^j≤p<2^{j+1}, j≥2, every prime p divides binom(2^{j+1},2^j). The product of these distinct primes is at most that binomial coefficient, which is at most 2^{2^{j+1}}. Comparing logarithms gives at most 2^{j+1}/j primes in the block, and its reciprocal mass is at most 2/j. The j=1 block consists of 2 and possibly 3, with mass at most 5/6≤2. For a partially truncated last block the same bounds hold. Thus, with L=floor(log_2 N),

    P(N) ≤ 2H_L ≤ 4H_L.

For L≥1, split the integers through L into dyadic blocks. Each block has reciprocal mass at most one, so H_L≤floor(log_2 L)+1=ell(N)+1. When L=0 the harmonic mass is zero. Set

    K=16(ell(N)+1).

It follows that 4P(N)≤K≤K+1. Substituting this K into (A), and using log(N+1)≤H_N, gives precisely

    log(N+1) ≤ 4+8192(ell(N)+1)M.

The mildly stronger dyadic prime estimate just proved is only used to validate the existing constant; no claim about a new optimized constant is made. Every step uses a finite sum or an explicitly justified geometric-series bound.

## 9. Endpoints and deduction of the asymptotic order

At N=0 the maximum is zero; at N=1 the maximum is one for every r≥2, witnessed by {1}. Neither endpoint needs the upper theorem's logarithmic denominator. The lower inequality holds there, and ell(0)=ell(1)=0 agrees with the natural-logarithm convention in the formal archive. For 2≤N≤53 the lower displayed inequality is allowed to be vacuous because log(N+1)<4; this does not impair an asymptotic theorem. For every N the denominator 8192(ell(N)+1) is positive.

For example, for N≥ceil(exp(8)) the lower numerator log(N+1)-4 is at least (1/2)log N and ell(N)+1≤4 log log N. The latter follows directly from L≤log N/log 2 and 1/log 2<2. The upper numerator 2r(1+2log N) is at most 6r log N, while log log(N+1)≥log log N>0. Thus the audited finite assertions imply the concrete, deliberately nonsharp comparison

    (1/65536) log N/log log N ≤ E_r(N) ≤ 6r log N/log log N

for every r≥2 and N≥ceil(exp(8)). For fixed r this is the claimed Θ_r order. It says nothing matching about the r-dependence when r grows with N; for example E_r(N) always also obeys H_N. No exact-extremum assertion is inferred from these inequalities.

## 10. Formal statement fidelity and reproducibility limits

The retained Problem538.lean defines a finite set of ordered pairs (p,a), requires positivity and a≤N, quantifies its cap over every m, and uses the rational sum Σ1/a. Enumerating primes only within range(m+1) loses none of the pairs for an admissible set because p≤pa=m. The final theorem uses these definitions directly. Its lower component casts a nonnegative-rational sum to the same real-valued rational mass; there is no changed objective.

Two packaging details must remain explicit:

1. Both archive READMEs refer to an experiment_1_formal_statement path. That path is absent from the shipped ZIP. The actual pinned statement is present in experiment_24_safe_kernel_arithmetic/lean/Research/Problem538.lean. Its exact member name, hash, and size are preserved in SOURCES.json. The stale documentation is not silently repaired or treated as an additional supplied file.
2. The project requests mathlib via a movable stable label in lakefile.toml, but the retained lake-manifest.json pins the immutable mathlib revision fabf563a7c95a166b8d7b6efca11c8b4dc9d911f and lean-toolchain specifies Lean 4.31.0. No dependency refresh was attempted.

The copied final Proof.lean is byte-identical to Research/FinalMatchingOrder.lean. The website's short schematic signature mentions MatchingOrder, whereas the actual file gives the two finite statements directly as the theorem type; the latter is the audited assertion. Static source inspection can establish what text and imports are present; it cannot replace a successful kernel check. The publisher reports a successful build and standard axioms. This audit neither adopts that report as a locally observed run nor suggests that a grep scan certifies all dependencies.

## 11. Independent finite checks and falsification controls

Historical independently authored exact checks covered favorable-child parameter counts and outside danger fractions, the two-dimensional isotropic-line implication, density and rainbow inequalities, sampled complete safe palettes, weighted averaging, repeated colors, integer-layer transfer, harmonic inequalities, and finite endpoint regressions. These checks used exact integer and rational arithmetic and modular Gaussian elimination. No imported candidate code was executed. They passed normal, -O, and -OO modes with byte-identical outputs. These are recorded historical verification results, not new publication-stage mathematical runs.

For the finite integer enumeration, the coverage beyond the inspected rectangle has a proof: if m=pa=qb has two distinct pairs with a,b≤N, then p≠q, p divides b, and q divides a. Therefore p,q≤N and m≤N². Any representation with multiplier p>N is the only representation of that m. Thus the checker does not silently replace the original global condition by a small-product cutoff.

Historical negative controls exposed the failure of a cap restricted to products below N, failure when safety is dropped, the characteristic-two polarization exception, and the changed danger fraction when the nonzero-coefficient condition is omitted. This edition omits optional finite toy parameters, numerical computational witnesses, raw check outputs, and code. The full general arguments and analytic constants in Sections 1–10 and the preceding all-product enumeration lemma are retained.

Finite tests support, but do not prove, the infinite theorem. Acceptance rests on the general derivation in Sections 2–9. Historical checks used explicit exceptions rather than Python assert statements. This prose-and-metadata edition is not an executable reproduction package. Copied third-party source documents, archive bodies, PDFs, datasets and private coordination are excluded. Historical source inspection and check results are accurately limited in SOURCES.json and VERIFICATION.json.
