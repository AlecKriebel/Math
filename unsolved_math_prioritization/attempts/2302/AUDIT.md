# Mathematical audit: Erdős Problem 783 / record 2302

This is an AI-assisted, unrefereed authored mathematical audit edition. Acceptance means an independent internal AI audit of the precisely scoped written arguments and their explicitly retained classical dependencies. It is not external human peer review, journal acceptance, formal proof-assistant certification, or a novelty or priority claim.

This is not a computational reproduction package. The complete substantive ten-section audit and the full authored finite counterexample are retained, including every mathematical set, fraction, inequality, count, correction, dependency and limitation. Executable code, raw calculation outputs or datasets, copied source documents or text, source images and private coordination material are not distributed.

Retrieval, inspection and mathematical-check statements describe the original audit of October 11, 2026 UTC. Editorial preparation performed no new scholarly-source retrieval, source-body inspection, literature survey or mathematical execution. Historical finite checks concern one finite witness only; they do not establish an eventual optimizer or the general harmonic-rigidity claim.

Audit date: 11 October 2026 (UTC).

## 1. Disposition

The three claims require different dispositions.

1. **Sharp leading asymptotic value: accepted, with explicit local repairs.** For fixed C > 0, the minimum unsieved proportion over pairwise coprime A ⊆ {2,…,N}, μ(A) ≤ C, is ρ(e^C) + o(1), uniformly in A. Tao's February 22, 2026 reduction supplies the general-modulus lower bound using the classical prime-modulus result. A correctly budgeted prime tail supplies the upper bound. The proof below makes the necessary normalization, truncation, and indexing corrections explicit.
2. **Harmonic rigidity for arbitrary near-minimizers: not established by the inspected February 25 proof.** Chojecki's fixed-parameter integral-equation compactness argument and its application to prime sets above a fixed power cutoff survive corrections. The general reduction, however, loses fixed errors and then treats them as vanishing errors. The final theorem also changes the cutoff quantifiers. These are substantive proof obligations. No counterexample to the full rigidity statement is established here.
3. **Literal exact finite greedy rule: false as an all-N rule.** At N = 100, C = 1/2, the descending-prime greedy set leaves 62 integers, whereas an admissible prime set leaves 57. The separate authored finite proof gives exact fractions and exact counts. This single witness does not refute an eventual fixed-C rule, classify exact minimizers, or challenge the leading asymptotic value.

This audit is not a claim of a new resolution of the underlying number-theoretic problem. It credits the earlier work, distinguishes its proved content from its stronger claims, supplies local repairs and independently checked counterexamples, and identifies the remaining logical bridge.

## 2. Exact target and attribution

Write

μ(A) = Σ(a∈A) 1/a,
σ_N(A) = N^−1 #{1≤m≤N : a∤m for every a∈A},
m_C(N) = min{σ_N(A) : A⊆{2,…,N}, A pairwise coprime, μ(A)≤C}.

The minimum exists because the admissible class is finite. The pairwise coprimality, exclusion of 1, exact budget, and integer floors are part of the question. C is fixed while N grows; A can change with N.

Erdős's 1973 printed page 135, equations (14.3)–(14.4), asks which admissible set minimizes the uncovered count. His suggested descending-prime construction permits either an extremal or a nearly extremal interpretation. The imported record explicitly says N is large and appends a corrupted serialized difficulty fragment, which has no mathematical meaning. Neither source licenses silently replacing the exact optimization question by a uniqueness theorem.

Hildebrand established the classical prime-case asymptotic lower bound. Granville and Soundararajan gave a different proof through an integral equation and classified its equality cases. Chojecki's January 23 note treats the elementary C≤log 2 value range and the prime-tail upper construction. Tao's February 22 note extends the value lower bound to pairwise coprime moduli. Chojecki's February 25 note expressly claims to complete the additional stability steps in its final section; it is therefore not adequate to describe that entire document as merely a conditional program. Its unconditional claim must be audited, as done here.

The inspected forum search result records Tao's February 23 statement that he did not plan journal publication of his preprint. That is a dated statement of intent, not proof of mathematical correctness, present publication status, or peer-review acceptance. The tracker treats an asymptotic interpretation as resolved. This audit uses the actual arguments rather than the tracker label.

Public references:

- Erdős, *Problems and results on combinatorial number theory* (1973), printed pp. 117–138, target p. 135: https://users.renyi.hu/~p_erdos/1973-21.pdf
- Tao, *Sieving by coprime numbers*, February 22, 2026, third version, 8 PDF pages: https://terrytao.wordpress.com/wp-content/uploads/2026/02/erdos783-3.pdf
- Chojecki, *Extremal coprime coverings under a reciprocal budget and a Dickman-type conjecture*, January 23, 2026, 6 pages: https://www.ulam.ai/research/erdos783-final.pdf
- Chojecki, *Erdős Problem #783: sharp asymptotic value and a stability program*, February 25, 2026, 25 pages: https://www.ulam.ai/research/erdos783-rem.pdf
- Granville and Soundararajan, *The number of unsieved integers up to x*, arXiv:math/0308009v1 (2003), subsequently Acta Arithmetica 115 (2004), 305–328: https://arxiv.org/abs/math/0308009
- Public discussion and dated author statements: https://www.erdosproblems.com/forum/thread/783

## 3. Authentication and inspection boundary

Historical byte-authentication independently checked all 86 listed source-collection members against their recorded sizes and hashes without executing the supplied verifier. This establishes byte identity, not the truth of a theorem. The source PDFs and extracted-text identities are individually recorded in SOURCES.json. No author software, proof assistant development, or author computation was executed.

The complete January note, complete February note, and complete Tao note were read in text, with critical formulas checked visually against their PDFs. The entire Granville–Soundararajan text was read; its value/equality argument in sections 5–7 and the dictionary in section 2 were inspected for the uses made here. The original Erdős target page was read and visually checked; unrelated problems in the 1973 article were not audited.

This is an ordinary mathematical audit using cited classical analytic number theory, not a formal verification of its entire dependency closure. In particular, Hildebrand's separate original long paper and all earlier proofs of the prime number theorem, Mertens' theorem, and Dickman asymptotics were not re-audited. The Granville–Soundararajan proof contains numerical inequalities and cites earlier integral-equation machinery. Their published theorem is treated as a classical dependency; the paper's reported numerical checks were not rerun as an interval-arithmetic certification. The present acceptance is explicit about that boundary, rather than mistaking retrieval or reading for mechanized certification.

## 4. The asymptotic upper bound, with the exact budget repaired

Let q_1>q_2>… be the primes at most N. Choose the largest k for which Σ(i≤k)1/q_i≤C, and let G_N={q_1,…,q_k}. For fixed C and sufficiently large N, the next prime q_{k+1} exists, because the total prime reciprocal sum diverges. Also q_{k+1}→∞: for any fixed B, the sum over B<p≤N eventually exceeds C, so the greedy process stops before reaching B.

Therefore

0 ≤ C−μ(G_N) < 1/q_{k+1} = o(1).

Put y_N=q_{k+1}, so G_N={p:y_N<p≤N}. Mertens' theorem now gives

log log N−log log y_N=C+o(1),
log y_N/log N=e^−C+o(1).

The uncovered integers are exactly the y_N-smooth integers. Fixed-parameter Dickman asymptotics and a monotonicity sandwich in y_N yield

σ_N(G_N)=ρ(e^C)+o(1).

The sandwich avoids assuming uniformity under an unspecified moving parameter: for every small fixed η>0, eventually N^(e^−C−η)≤y_N≤N^(e^−C+η); apply the two fixed-exponent asymptotics and then let η decrease to zero.

This corrects two printed problems:

- February Lemma 5 asks for the maximal feasible y in [2,N]. That maximum is always N, giving an empty tail and μ=0. Its budget-saturation assertion is false under that definition. One must select the maximal number of descending primes, or equivalently the smallest feasible cutoff in the relevant discrete convention. This is a local but necessary correction, not a permissible silent normalization.
- The January note's adjustment by a bounded number of boundary primes is not justified by a bare o(1) error in Mertens' theorem. The excess can exceed any fixed multiple of 1/y. If primes are actually removed while y is unchanged, the exact identity U(A;N)=Ψ(N,y) is also no longer true. Choose the corrected greedy cutoff instead, or remove a possibly growing number of boundary primes having total reciprocal mass o(1), track the resulting o(N) difference, and update the cutoff.

For 0≤C≤log 2, the lower bound σ_N(A)≥1−μ(A)≥1−C is the union bound and needs no coprimality. The upper construction above gives ρ(e^C)=1−C. At the endpoint C=log 2, if one specifically wants the overlap-free proof, start with primes above √N. If their total budget is too large, remove the smallest such primes until feasible; if it is too small, leave it unchanged. The reciprocal mass still tends to log 2, all remaining products of two primes exceed N, and their number is o(N), so floor errors are o(N). Thus the endpoint is covered without asserting that the exact greedy cutoff always lies above √N.

The January Remark 3.3's informal claim that maximizing coverage becomes precisely the largest-prime rule is not an exact finite theorem. Equal leading coverage per reciprocal cost does not eliminate integer-floor effects. The finite counterexample demonstrates this distinction even below log 2.

## 5. Auditing the general-modulus lower bound

Here is a complete reconstruction of the reduction, relative to the classical prime-modulus theorem and Dickman log-concavity. It also records why the printed defects do not invalidate the value result.

### 5.1 Truncation and elementary counting

If A contains moduli above N, discard them. This leaves σ_N unchanged and decreases μ. Since ρ is decreasing, proving the bound for the truncated set is sufficient. In the present target A⊆[2,N] already.

Every composite a≤X has a prime factor at most √X. Pairwise coprimality makes these factors distinct across members, hence there are at most π(√X) such composites. Dyadic summation gives

Σ(a∈A, a>Z, a composite)1/a = O(Z^−1/2),

uniformly in the coprime set. The union bound gives

|σ_N(A)−σ_N(B)|≤μ(A△B)

for arbitrary finite sets. Thus large composites can be removed at uniformly small cost.

### 5.2 Inclusion-exclusion with uniform floor control

Define

T_{N,r}(A)=Σ(j=0,…,r)(−1)^j Σ(q_1<…<q_j in A, q_1…q_j≤N)1/(q_1…q_j).

Bonferroni applies to the events q|n. Because the moduli are pairwise coprime, their intersections consist of multiples of the product. The truncation error is bounded by μ(A)^(r+1)/(r+1)!.

For the floor replacement, fix j and q_1,…,q_{j−1}, put Q=q_1…q_{j−1}, and suppose a possible largest q_j exists. Ordering implies Q^(1/(j−1))≤q_j≤N/Q, so N/Q≥N^(1/j). The elementary composite count plus a prime-counting upper bound gives

#{q∈A:q≤N/Q} ≪ jN/(Q log N).

Summing over ordered prefixes bounds the total normalized floor error by

(log N)^−1 Σ(j≤r) j μ(A)^(j−1)/(j−1)! ≪ r e^{μ(A)}/log N.

For j=1, the same bound follows directly; the expression with exponent 1/(j−1) is not used. Hence

σ_N(A)=T_{N,r}(A)+O(μ(A)^(r+1)/(r+1)!)+O(r e^{μ(A)}/log N).

The middle indicator in Tao's printed equation (2.1) is written as gcd(n,q)=1 for all q. For composite q that is a different event. With A={4}, n=2 it is false, whereas the event 4∤2 is true. Replacing that indicator by the actual avoidance event restores exactly the Bonferroni proof above; subsequent floor formulas already use divisibility by products. This is a genuine printed error with a direct local repair, not a counterexample to the theorem.

### 5.3 Splitting scales

For A_1⊆[2,z_-] and a prime set A_2⊆(z_+,N], compare T_{N,r}(A_1∪A_2) with T_{N,r}(A_1)T_{N,r}(A_2). Extra terms of total degree between r+1 and 2r have total absolute weight at most Σ(j=r+1,…,2r)μ^j/j!.

For a degree-j term whose separate small and large products are at most N but whose full product exceeds N, fix all but its largest prime. That prime must lie in a multiplicative interval of ratio at most z_-^r, entirely above z_+. A prime-counting upper bound and dyadic partial summation bound its reciprocal mass by O(r log z_-/log z_+). Summing the other factors gives the error O(r e^μ log z_-/log z_+). Thus the splitting estimate is uniform in the sets.

Printed corrections in Tao Lemma 2.4: the undefined endpoint z_2 must be z_+; the degree range includes j=2r; and the index describing the last small element must refer to q_{j_1}, not q_{j−1}. The displayed error bound already includes degree 2r. These edits restore the preceding explicit combinatorial comparison.

If z_-^r≤N, the truncated sum for A_1 has no product cutoff through degree r, and comparison with its finite Euler product gives

T_{N,r}(A_1)=Π(q∈A_1)(1−1/q)+O(Σ(j>r)μ^j/j!).

### 5.4 Parameter order and conclusion

Fix C and a desired error ε. Choose r sufficiently large, then a fixed Z sufficiently large, and finally N sufficiently large. Delete composites above Z. Set z_j=Z^(r^(2j)) for j=0,…,r, and choose one of the r intervals (z_{j−1},z_j] having reciprocal mass at most C/r. The printed sum beginning at j=0 uses an undefined z_{−1}; it must run from j=1 to r.

Remove that interval and define the remaining sets A_1≤z_- and A_2>z_+. Here A_2 is prime, z_+ = z_-^(r²), and z_- is fixed before N grows. All estimates above therefore combine to give

σ_N(A)=Π(q∈A_1)(1−1/q) σ_N(A_2)+O_C(ε).

Apply the classical prime-only lower bound to A_2. Put R(t)=ρ(e^t). For q≥2, 1−1/q=R(1/q). Dickman log-concavity implies R(x)R(y)≥R(x+y) for x,y≥0. Multiplying these inequalities gives

σ_N(A)≥R(μ(A_1)+μ(A_2))−O_C(ε)≥R(C)−O_C(ε).

The estimates are uniform in A. Let ε decrease to zero. Applying the same argument with budgets varying in [0,C], or keeping μ(A) in the last displayed line and the uniform errors, yields σ_N(A)≥ρ(e^{μ(A)})−o_C(1).

Dickman log-concavity is explicitly retained as a classical dependency in this audit. The following calculation checks the continuation mechanism and the way that dependency is used; it is not represented as a new standalone certification of the entire Dickman theory. For clarity about that input: positivity and the integral identity uρ(u)=∫(u−1,u)ρ(v)dv show that h(u)=−ρ'(u)/ρ(u) satisfies

h(u)=[∫_0^1 exp(−∫_t^1 h(u−s)ds)dt]^−1.

On (1,2), h(u)=1/[u(1−log u)] has positive derivative. At 2 its one-sided derivatives are log 2/[4(1−log 2)²] and (3 log 2−2)/[4(1−log 2)²], both positive. For u>2, differentiating the displayed integral identity expresses h′(u) as a positive weighted integral of integrals of h′(v) with u−1<v<u. A first zero of h′ would therefore still have a strictly positive right-hand side, a contradiction. Thus h is increasing and log ρ is concave. Moreover (log R)′(t)=−e^t h(e^t) is strictly decreasing for t>0. Since log R(0)=0, integrating that derivative on [x,x+y] and [0,y] proves log R(x+y)≤log R(x)+log R(y), strictly for x,y>0. No assertion of a second derivative at every integer join is needed.

This proves the general value lower bound after the listed local corrections, and section 4 provides the matching feasible upper bound.

## 6. The February stability claims: what survives

### 6.1 Strictness

For t>0, log R(t) is strictly concave: composition of the decreasing concave log ρ with e^t gives strict decrease of the first derivative. Equivalently, away from the finitely many relevant joins, its second derivative is strictly negative; continuity and one-sided derivatives handle the joins. Consequently

R(a)R(b)>R(a+b) whenever a,b>0.

Compactness makes the ratio uniformly greater than 1 when a and b stay in a fixed compact positive range. This repairs the differentiability shorthand in Lemma 17. In Corollary 19, x_N+y_N≤C+o(1) does not imply eventual ≤C, but one can use C+1 as the compact upper bound. Lemmas 18 and 38 then have their intended strictness. Empty compact constraint sets are handled vacuously.

### 6.2 Fixed-u compactness is valid

For fixed u≥w>2, put λ(dt)=dt/t on [1,u] and ν=(1−χ)λ. The class 0≤ν≤λ with ν([1,u])=log w is weakly compact. Its elements have no atoms. Products ν^{⊗j} assign zero mass to the hyperplane t_1+…+t_j=u. The inclusion-exclusion functional

S_u(ν)=Σ(j≥0)(−1)^j ν^{⊗j}({Σt_i≤u})/j!

is continuous, by weak convergence of finite products and a uniform exponential-series tail bound. In fact j>u contributes zero in this fixed lower-cutoff model.

The GS equality theorem at w>2 identifies the unique zero-gap measure as λ restricted to [u/w,u]. The set having ν([1,u/w])≥δ is compact: domination by λ ensures no endpoint atoms, or Portmanteau directly gives closedness of that superlevel set. If the set is nonempty, the minimum objective there exceeds ρ(w); if it is empty, the desired assertion is immediate. This establishes the fixed-u stability conclusion of Proposition 33. The same compactness argument works for w varying near a fixed w_0, with moving endpoints controlled by their λ-measure. It establishes Lemma 36.

The equality theorem was read in the actual GS source, including its proof in sections 5–7. Its statement does supply the step-function equality classification used here. It is not merely a lower bound for the value, and it is not already a uniform stability assertion as u→∞.

### 6.3 The discretization lemma and two errors in Corollary 35

The integral/harmonic comparison in Lemma 34 follows by partial summation and θ(X)∼X. Boundary terms are O(1/log y), and the extra derivative term contributes O(1/log y). The error can be taken uniformly for 1≤a≤b≤u when u is fixed. One should define χ=1 on the tiny initial range where θ(y^t)=0; its displayed quotient is otherwise 0/0 there. All comparisons used here integrate t≥1, so this convention causes no change.

Corollary 35, as printed, is false for two independent reasons.

**Missing small-prime hypothesis.** Take f completely multiplicative, with f(2)=0 and f(p)=1 for every odd prime. Choose any fixed u≥1 and u_0=u. For t≥1,

1−χ_f(t)=log 2/θ(y^t),

so its first integral tends to zero and the second integral is zero. Yet for any Y=y^{u+o(1)}, the asserted prime symmetric difference contains 2 and has weight at least 1/2. Choosing δ<1/2 contradicts the conclusion. The correction is to assume f(p)=1 for p≤y, as is indeed true in Theorem 37's application, or explicitly retain the omitted sum over p≤y.

**The two errors add.** Even with that hypothesis, two integrals each bounded by δ imply a total harmonic distance at most 2δ+o(1), not δ+o(1). This is not cured by changing Y by an o(1) amount in its exponent: such a change affects only o(1) reciprocal mass. For a concrete asymptotic family, use u=4, u_0=2, δ=1/10, s=3/40, and exclude precisely the primes in (y,y^{e^s}] and (y^{2e^s},y^4]. Both integrals tend to s<δ, while distance to any cutoff Y=y^{2+o(1)} tends to 2s=3/20>δ. Partial summation gives these limits. The corrected bound is 2δ+o(1).

Theorem 37 already has the missing condition f(n)=1 for n≤y. Taking a smaller input tolerance in the compactness step absorbs the factor 2. Its moving endpoint u/w_x stays at least 1 because E_χ(u)≤u, not merely because w_x→w. With these local repairs, Theorem 37 proves harmonic rigidity for near-extremal prime sets contained in (N^{1/u},N] for one fixed u≥w.

## 7. The general reduction: explicit defects and a repairable portion

### 7.1 The auxiliary power bound is true, but its printed derivative is wrong

February Lemma 39 is valid: for 0≤x≤1/2, log(1−x)≥−x−x², and hence Π(1−1/q)≥e^{−3μ/2}.

In Lemma 40, differentiating g(u)=u^{3/2}ρ(u) correctly gives

g'(u)=u^{1/2}[(3/2)ρ(u)−ρ(u−1)],

not the displayed expression with an additional factor u multiplying ρ(u−1). Monotonicity of ρ alone does not give the printed conclusion. The repair is the integral identity

uρ(u)=∫_(u−1)^u ρ(v)dv≤ρ(u−1).

Therefore g'(u)≤u^{1/2}(3/2−u)ρ(u)<0 for u≥2. Since 2^{3/2}(1−log 2)<1, it follows that ρ(u)<u^{−3/2} for u≥2. The bound survives, with this added argument.

### 7.2 Proposition 41's stated proof does not give its stated strength

Its ε is chosen from a fixed δ and held fixed as N→∞. Its factorization and bookkeeping give errors O_w(ε)+o(1), not o(1). In particular:

- μ(A_1), μ(A_mid)=O(ε) together with μ(A)=C+o(1) imply only μ(A_2)=C+O(ε)+o(1).
- Multiplying σ_N(A_2) by a factor σ_∞(A_1)≤1 gives a lower bound on σ_N(A_2), not the displayed upper bound. An upper bound can be recovered using σ_∞(A_1)≥1−μ(A_1), but it still has a fixed O(ε) loss.
- Choosing τ=ε after invoking a strictness modulus depending on τ is circular unless a relation between those moduli has been proved. Choose τ from the target tolerance first, and then choose ε sufficiently small for that τ.
- Step 5's positive contradiction gap need not equal the arbitrary requested δ. Choose its own positive gap depending on w.

None of those fixed errors disappears merely because ε can be chosen small before N grows.

### 7.3 A rigorous consequence that can be recovered: composites have o(1) mass

The following repair proves the actual Hypothesis 29 without the extra fixed-power-cutoff conclusion.

First, Tao's uniform lower bound and strict decrease of R imply μ(A)=C+o(1) for any near-minimizer at budget C. Fix r and use the scales in Proposition 41, with u_*=w r^{2r+2}, z_0=N^{1/u_*}, z_j=z_0^{r^{2j}}. After deleting the composites above z_0, their mass is o(1). Select a gap having mass ≤(C+o(1))/r and split into A_1, A_mid, A_2. All remaining composites lie in A_1; A_mid and A_2 are prime. The previously checked sieve estimates give, uniformly for fixed r,

σ_N(A)=σ_∞(A_1)σ_N(A_2)+O_w(E_r)+o(1),
μ(A_1)+μ(A_2)=C+O_w(E_r)+o(1),

where E_r→0 as r→∞ (factorial tails plus O_w(1/r)). The small-product requirement holds because z_{r−1}^r=N^{1/(wr³)}≤N.

The repaired power bound gives a positive gap d=w^{−3/2}−ρ(w)>0. Since σ_∞(A_1)≥w^{−3/2}+o(1) and σ_N(A_2)≥1−μ(A_2), choose c_0>0 small enough and then r large enough that μ(A_2)≤c_0 would force σ_N(A)>ρ(w)+d/4. This contradicts near-minimality. Thus μ(A_2)≥c_0 eventually.

Now fix any τ>0. On the compact set a≥τ, b≥c_0, a+b≤C+1, strictness gives R(a)R(b)−R(a+b)≥k_τ>0. Choose r still larger, depending on τ, so E_r is much smaller than k_τ. The prime lower bound and the Euler-product inequality then force μ(A_1)<τ for all sufficiently large N; otherwise the factorization yields a fixed excess over ρ(w).

All composites are either in A_1 or among the already removed o(1)-mass composites. Hence

limsup_(N→∞) μ({a∈A:a composite})≤τ.

Since τ was arbitrary, that mass is o(1). Take P=A∩{primes}. Then

μ(A△P)=o(1), μ(P)=C+o(1), σ_N(P)=ρ(w)+o(1),

the last equality following from Lipschitz continuity and the value lower bound. This recovers Hypothesis 29. The proof also gives tightness of reciprocal mass away from logarithmic scale zero: for every τ>0 there is a fixed u_*(w,τ) with limsup μ(A∩[2,N^{1/u_*}])≤τ. It does not say that one fixed u_* makes that mass o(1).

## 8. Why Theorem 42 does not follow yet

Theorem 42 applies Proposition 41 as if it supplied a prime set above N^{1/u_*}, with u_*=u_*(w) fixed, together with all three o(1) conclusions. Proposition 41 is stated with u_*(w,δ), and even those fixed-δ vanishing density conclusions were not established by its proof.

The repaired consequence in section 7.3 yields an arbitrary prime set P with o(1) composite-removal loss. It does not ensure P⊆(N^{1/u_*},N] for any fixed u_*. Taking a diagonal sequence δ_N→0 can make the loss vanish, but then u_*(w,δ_N) can tend to infinity. Theorem 37 and the compactness stability modulus in Proposition 33 are proved only for fixed u. There is no stated bound controlling that modulus as u grows.

Nor is it enough simply to retain a fixed δ cutoff: the resulting density error is fixed, while the required stability tolerance η(u,w,δ_target) may be much smaller. The fact that both quantities can be made small, with interdependent parameters, is not a proof that they can be made compatible.

A sufficient repair would be any one of the following, actually proved:

1. A near-extremal reduction with o(1) loss above one fixed positive-power cutoff.
2. A prime-case stability theorem uniform in the expanding scale parameter, with quantitative bounds strong enough for the reduction.
3. A compactness/equality theorem for finite exclusion measures on (0,1] whose total mass is bounded and tight near zero, without assuming they vanish on an initial interval. Passing the value inequality to that limit is easier than passing uniqueness of equality; the latter must be justified.

No such repair is supplied in the inspected note, and this audit does not claim to have proved one. Therefore the general harmonic-rigidity assertion remains **unaccepted from this proof**, rather than disproved or certified globally open.

## 9. Exact optimization and cardinality

The complete finite witness is in PROOF.md. It shows an actual improvement, not merely a different near-minimizer or unused budget. Both sets contain only primes and have disjoint covered multiples; all budgets and counts are exact.

The verified statement is narrowly quantified: at N=100 and C=1/2 the literal greedy tail is not an exact minimizer. A fixed-C assertion holding for all sufficiently large N is not contradicted by that one example. The original wording and the imported “large N” formulation therefore still require a separate exact/eventual analysis. This audit neither classifies the eventual exact optimizers nor proves that no such classification exists.

February Corollary 44's cardinality computation is correct for the specified model tail: for fixed w>1, π(N)−π(N^{1/w})∼N/log N. Its threshold N^{1/w} is an asymptotic model and does not automatically satisfy the exact finite reciprocal budget. Moreover harmonic distance o(1) does not imply counting symmetric difference o(N/log N). For example, remove all primes in (N/2,N] from a prime tail. Their harmonic mass is O(1/log N)=o(1), but their number is asymptotic to N/(2 log N). This verifies the warning in Remark 43 and prevents upgrading harmonic rigidity to cardinality rigidity.

## 10. Recommended mathematical status

- Sharp fixed-C leading value: prior result accepted with the explicitly written repairs and classical dependencies above.
- C≤log 2: asymptotic value and asymptotic prime-tail attainment accepted; exact-greedy language must be qualified.
- Fixed-power-cutoff prime stability: accepted after the small-prime hypothesis/factor-2 corrections.
- o(1) composite mass for near-minimizers with C>log 2: recovered by the corrected two-parameter argument in section 7.3.
- General prime-tail harmonic rigidity: proof gap identified; further work required at the cutoff/uniformity bridge.
- Exact finite descending-prime optimizer for every N: disproved by the authored N=100 witness.
- Fixed-C eventual exact optimizer and complete classification: no resolution claimed.

The bounded current-source check located the same third Tao version and the February rigidity manuscript, and surfaced the dated author discussion. It was not an exhaustive literature search. A failed direct forum fetch and search indexing dates are recorded as access limitations, not evidence of absence of later work.

This publication edition contains independently authored audit text, the complete mathematical counterexample, and public-source and verification metadata. Verification code and raw results are retained only in the original audit records and are not distributed here. Raw PDFs, extracted source texts, screenshots, dataset records, and private coordination material are excluded.
