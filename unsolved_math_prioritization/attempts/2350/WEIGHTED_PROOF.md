# Reflected-core weighted bound

Date: 12 October 2026 UTC. Target: frozen queue row 1741, problem 2350 / Erdős 864.

This is a substantive partial proof, not a solution of the conjectured constant.

## Result

Let A be a subset of {1,...,N}, with at most one integer T having more than one unordered representation a+b with a,b in A and a<=b. If such a T exists, put

C = A ∩ (T−A),  k = |C|,  m = |A|,  u = m−k.

If no such T exists, use C=empty and k=0. Write

W = u+k/√2 = m−(1−1/√2)k,     Q = u+k/2 = m−k/2.

For every integer h>=1, with L=max A−min A for nonempty A,

(1)        W² <= (L+h)(Q+h−1)/h.

In particular,

(2)        m−(1−1/√2)k <= √N + (3/2)N^(1/4),

and equivalently,

(3)        m+(√2−1)u <= √(2N) + (3/√2)N^(1/4).

Thus any sequence with m=(√2−o(1))√N has u=o(√N): near equality in the known √2 bound forces almost all elements into the reflected core. If k=o(√N), instead m<=(1+o(1))√N. These are parameter-dependent improvements and a stability conclusion, not a better unrestricted leading constant.

The previously retained proof splits A at T/2 and obtains √(2N)+O(N^(1/4)). The weighted inequality incorporates information that split proof discards, namely how many points actually participate in the exceptional sum.

## 1. Exact difference structure

For d>0 let R_d={(a,b) in A²:a−b=d}. Suppose (a,b) and (c,e) are different members of R_d. Then a+e=c+b. The two unordered pairs {a,e} and {c,b} are different: equality would either identify the two ordered difference pairs, or require a=b, which is impossible. Consequently a+e=c+b=T. Thus

(c,e)=(T−b,T−a).

There cannot be three distinct representations, because the second is uniquely determined by the first. Every doubled difference therefore consists of two reflected representations, and all their endpoints belong to C.

Conversely, if (a,b) is a positive-difference pair in C, its reflection (T−b,T−a) is another such pair. It is the same ordered pair precisely when a+b=T. Otherwise the difference has two representations.

This elementary reflection lemma was independently derived in this attempt before locating the public Erdős Problem a Day working report, whose section 2 already states it. It is therefore expressly not claimed as a new lemma. The report's computation claims are not used here.

As a useful exact check, let δ be 1 if T/2 belongs to A and 0 otherwise, and let p=(k−δ)/2 be the number of two-element reflection orbits. The number D of doubled positive-difference values is

(4)        D = (binom(k,2)−p)/2 = (k²−2k+δ)/4.

Indeed all unordered distinct pairs of C except the p complementary pairs are in two-element reflection orbits; each such orbit is exactly one doubled difference. This includes midpoint cases. Consequently the ordinary additive energy satisfies

sum_s #{(a,b) in A²:a+b=s}² = 2m²−m+k²−2k+δ.

These identities are not needed to prove (1).

## 2. A weighted difference inequality

Assign weight w(a)=1 to a in A\C, and w(a)=1/√2 to a in C. For each d>0 put

r_w(d)=sum_{a−b=d} w(a)w(b).

If d has one representation, its product weight is at most 1. If d has two representations, every endpoint is in C by section 1 and its total weight is 2(1/√2)²=1. Thus

(5)        r_w(d)<=1  for every d>0.

For an arbitrary integer h>=1 define the sliding window

F_h(x)=sum_{a in A} w(a) 1_{0<=x−a<h},   x in Z.

Its support has at most L+h integer points; sum_x F_h(x)=hW. Expansion of its square gives the exact identity

sum_x F_h(x)² = hQ+2 sum_{d=1}^{h−1}(h−d)r_w(d).

Using (5), the right side is at most hQ+h(h−1). Cauchy–Schwarz gives

h²W² <= (L+h) sum_x F_h(x)² <= (L+h)h(Q+h−1).

Division by h² proves (1). Empty A is immediate without a diameter convention.

This argument is a weighted version of the standard shifted-interval proof of the Sidon bound. It is self-contained; no unproved dense-Sidon existence input or numerical asymptotic fit is used.

## 3. A uniform explicit error term

Section 1 implies each positive difference occurs at most twice. Hence

m(m−1)/2 <= 2(N−1),

so m <= (1+√(16N−15))/2 <= 2√N+1. In particular Q−1<=m−1<=2√N.

Take h=ceil(N^(3/4)). Since L<=N−1, h−1<=N^(3/4), and h>=N^(3/4), inequality (1) yields

W² <= (N+h−1)(1+(Q−1)/h)
    <= (N+N^(3/4))(1+2N^(−1/4))
     = N+3N^(3/4)+2N^(1/2)
    <= (√N+(3/2)N^(1/4))².

All quantities being nonnegative, taking square roots proves (2). Equation (3) is obtained by substituting k=m−u and multiplying (2) by √2.

For the stability assertion, divide (3) by √N. If m/√N tends to √2, then (√2−1)u/√N tends to zero. This is uniform over the location and multiplicity of the exceptional sum.

## 4. Quantitative structural exclusions

Let α=1−1/√2. The following are immediate from (2).

* If k<=κ√N+o(√N), then m<=(1+ακ+o(1))√N.
* If k<=ρm+o(√N) for a fixed 0<=ρ<=1, then
  m<=(1/(1−αρ)+o(1))√N.
* Therefore the conjectured 2/√3 upper constant is proved for families satisfying
  k/m <= ρ₀+o(1),  where ρ₀=(1−√3/2)/(1−1/√2).
  The limiting constant ρ₀ is approximately 0.4574. The statement is about the exact algebraic expression, not its rounded decimal.

A further location-sensitive corollary is available. Put

ℓ=min(T/2−1, N−T/2).

When T is exceptional, ℓ>=0. The lower half of C is a Sidon set contained in an interval of diameter at most ℓ: it lies in [max(1,T−N),T/2), and twice its size differs from k by at most one. The standard Sidon interval bound gives k<=2√ℓ+O(N^(1/4)). Combining this with (2) gives

(6)        m <= √N+(2−√2)√ℓ+O(N^(1/4)).

For completeness, the standard interval bound follows without an external theorem. If b_1<...<b_s is Sidon in an interval of diameter H, the positive differences b_{i+j}−b_i for 1<=j<=v, 1<=i<=s−j are all distinct. Their number is M=vs−v(v+1)/2, their sum is at least M(M+1)/2, and telescoping for each j bounds their total by v(v+1)H/2. Thus s<=√((v+1)H/v)+(v+1)/2 whenever s>v. Choosing v=max(1,floor(H^(1/4))) gives s<=√H+O(H^(1/4)+1); s<=v and H<1 are immediate. This proves the asserted uniform error in (6).

## 5. What fails to reach the conjectured constant

The obstruction is now concentrated on sets with a large reflected core. Setting k=m in (1) gives exactly the same leading √2 upper constant. For a single constant weight t on all core elements, a doubled difference forces 2t²<=1, so taking t larger than 1/√2 is not permitted. This specifically explains why the present constant-core-weight argument stops; it is not a theorem that more elaborate methods cannot work.

An exact symmetric reduction also clarifies the missing arithmetic input. After centering and discarding a possible midpoint, write a symmetric set as A=±B, where B consists of positive numbers in a translate of the integer lattice or half-integer lattice. Then A has no repeated unordered sum except 0 if and only if:

(a) B is Sidon;
(b) (B+B) ∩ D⁺(B)=empty, where D⁺(B)={b−b':b>b', b,b' in B}.

Equivalently (b) says B ∩ (B+B+B)=empty, with repetitions allowed. To check the equivalence, positive sums of elements of ±B arise either as B+B or as a positive difference B−B. Uniqueness within each class follows from the Sidon property, while (b) exactly excludes collisions between classes. Negative sums follow by reflection and zero is the permitted exception. The midpoint case can be removed at a cost of one point before applying this reduction; adding it back is not automatically valid.

A fully symmetric A of diameter L has B in (0,L/2]. The sharp conjecture even for this subclass would require the stronger conclusion

|B| <= (1/√3+o(1))√L,

or equivalently |B|<=(√(2/3)+o(1))√(L/2), from (a) and (b). The ordinary Sidon bound only gives |B|<=(1+o(1))√(L/2). No proof of the stronger implication is supplied here. Even such a symmetric-subclass theorem would still need an argument controlling nonsymmetric additions in the general problem.

Residual: the unrestricted gap 2/√3 to √2 remains. This attempt proves an explicit weighted inequality and a quantitative reflected-core obstruction, but neither a matching upper bound nor a counterexample to it.

## 6. Source and verification scope

The exact target was checked against the frozen row1741 record and the retained original Paul Erdős paper, “Some of my Forgotten Problems in Number Theory” (1992), printed pages 39–40, including both scanned page images. Source: https://hrj.episciences.org/125/pdf . The retained PDF has 4,630,109 bytes and SHA-256 51faf4558eacab8e188efbcb028937f75dcb10d37865ab71ef1522df33361c72. The original source states the conjectural constant and credits joint work with Freud.

An earlier splitting proof and reflected-Sidon construction were read before this proof was prepared. The splitting proof is credited there to Desmond Weisenberg's 11 August 2025 comment, not to this attempt.

A bounded public search on 12 October 2026 located https://www.erdosproblemaday.com/report/864 . Its section 2 already contains the difference–reflection lemma and its closing section gives an equivalent symmetric residual. It labels itself an AI working report. Its computational claims and broader literature assertions are not premises of any proof here, and its code was not executed. The author independently proves the elementary structural claims used above. No claim of novelty is made for the weighted corollary either: the bounded search does not establish priority.

The authored diagnostic, not distributed in this prose edition, enumerates only all subsets of {1,...,N} for 1<=N<=14. It checks the original sum condition, the exact reflection and midpoint identities, the weighted difference bound, the sliding-window identity, and (1) for finitely many specified h. All arithmetic comparisons involving √2 are reduced to exact rational comparisons. This is a finite implementation diagnostic, not a proof of the theorem or a new extremal-computation record.
