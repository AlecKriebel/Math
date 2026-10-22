# Absolute linear Harbourne constants: one finite-plane completion approach

## Outcome and scope

The original all-fields conjecture remains unresolved in general after **one substantive approach (1/5)**. This report proves exact all-fields values on substantial subranges by combining a discrete incidence bound with the published finite-linear-space theorems of Erdős–Mullin–Sós–Stinson (EMSS, 1983). Those theorems and the finite-plane constructions are credited inputs, not discoveries of this report. No worldwide novelty claim is made. The proofs below are complete relative to the explicitly stated published inputs; this is not an independent reproof of the whole EMSS paper.

Let q≥4 be a prime power, N=q²+q+1, d=N−i, and 0≤i≤2q−1. The conjectured value is established here in each of these cases:

1. **0≤i≤q.**
2. **i=2q−1.**
3. **i=q+1+a**, where 0≤a≤q−3 and U_q(a)<L_q(a), with
   - U_q(a)=floor[a(a−1)/(2(q−1))];
   - L_q(a)=q−a for even q, and ceil[(q−a)(q+1)/(q−1)] for odd q.

A convenient sufficient condition is a²+(2q−3)a−2q²+2q<0 for even q, or a²+(2q+1)a−2q²−2q<0 for odd q. The integer test above is slightly stronger.

In particular, this proves every stated-band value for q=7,8,9,11,13, beyond the source's already established d≤31 cases. It does **not** determine the omitted d-ranges between prime-power bands. The first band value not settled by this approach is q=16, a=13, i=30, d=243. This means first unresolved by this argument, not first open in the literature.

The remaining middle-band problem has an exact structural reduction: a counterexample must dualize to a realizable nondegenerate finite linear space with d=q²−a points, q²+q blocks, maximum block size q, and positive total degree excess above q+1. An arbitrary abstract incidence table is not enough.

### A genuine source exception, not new research

The special formula as literally printed fails at q=2, i=3, d=4: it gives −6/5, while H(4)=−4/3, already in the same paper's table. The advertised endpoint construction counts (q−1)² multiplicity-(q−1) points; for q=2 these are nonsingular and must be excluded. We preserve this discrepancy explicitly rather than silently changing the formula or using it to claim a new counterexample. The residual endpoint claim must exclude q=2. All d≤31 values and H(q²+q+1)=−q are pre-existing results.

## 1. Exact source target

For d distinct projective lines over a field K, let P be the set of **all** points where at least two of the lines meet. Write s=|P| and m_P for their multiplicities. For d≥2,

H(K,L)=(d²−Σ_P m_P²)/s,

and H(d) is the minimum over all fields K and all such configurations L.

In OWR 14/2016, printed p.696, Conjecture 1, and Dumnicki–Harrer–Szpond (DHS), arXiv:1507.04080v2, Conjecture 1.2, q is the least prime power with d≤q²+q+1, and i=q²+q+1−d. The printed main formula, asserted only for i≤2q−2, is

h(d)=[N−i−ε₁m₁−ε₂m₂−t_(q−1)(q−1)−t_q q−t_(q+1)(q+1)]
      /[ε₁+ε₂+t_(q−1)+t_q+t_(q+1)],

where

- m₁=q+1−i; m₂=2q+1−i;
- ε₁=1 for 0≤i≤q−1, and 0 otherwise;
- ε₂=1 for i>q+1, and 0 otherwise;
- t_(q−1)=qi−q²−q for i>q+1, and 0 otherwise;
- t_q=qi for i≤q+1, and 2q²−(i−2)q−1 otherwise;
- t_(q+1)=q²+q−iq for i≤q+1, and 0 otherwise.

For i=2q−1 the separately printed formula is

H(d)=−(q³−q²+2q−2)/(q²+q−1).

No extension to other i is made. For q≥3 these expressions simplify, within their stated domains only, to the following target C_q(i):

- 0≤i≤q−1: C_q(i)=−qd/N;
- i=q: C_q(i)=(−qd+1)/(N−1);
- q+1≤i≤2q−2: C_q(i)=−qd/(N−1)=−d/(q+1);
- i=2q−1: C_q(i)=(−qd+2)/(N−2).

The displayed simplification is algebra, not a new conjecture. Throughout this band d≥q²−q+2>(q−1)²+(q−1)+1, so the least-prime-power condition is automatic when q is a prime power.

## 2. Dual linear spaces, degeneracies, and the credited inputs

Dualize L combinatorially: its d lines become points, and each singular point becomes the block consisting of the lines through it. Every pair of points lies in a unique block, all blocks have size at least two, and the blocks have total size I=Σ_P m_P. If L is not a pencil, all blocks are proper subsets. The dual is a finite linear space with v=d points and b=s blocks. A near-pencil means one block of size d−1 and d−1 two-point blocks.

The degeneracies are handled first. A pencil has H=0. A near-pencil has s=d, I=3(d−1), hence H=−2+3/d. For q≥4 every C_q(i)<−2, so neither can violate the desired lower bound. This last inequality follows directly from the four formulas; their least d in the band is q²−q+2, and qd>2N for q≥4. Thus EMSS is applied only to its **nondegenerate** spaces (NLS): proper blocks and no near-pencil. No assumption on characteristic, underlying field, or maximum block size is silently added.

We use these precise published EMSS results with n=q:

- Theorem 3.6 (p.53): q²+2≤v≤N implies b≥N; equality implies embedding in a projective plane of order q.
- Lemmas 3.11 and 3.14, Corollary 3.12 (pp.56–57): v≥q²−q+3 implies b≥N−1. At equality the maximum block size is q or q+1; for v=q²+1 it is q+1. If it is q+1, one point has degree q and every other point degree q+1.
- Lemmas 3.7–3.8 (pp.54–55): v=q²−q+2 implies b≥N−2; for q≥4 equality embeds in a projective plane of order q.
- Theorem 3.23 (p.61): for v=q²−a, b=N−1, maximum block size q, and the applicable sufficient strict polynomial condition stated in the Outcome, the NLS embeds in a projective plane of order q.

“Embedding” here is the induced linear-space embedding: intersect ambient blocks with the chosen point set and discard intersections of size less than two. The containing plane need not be Desarguesian. We use its incidence axioms only. For actual upper-bound realizations we always use the field plane P²(F_q).

## 3. The discrete incidence lower bound

Every pair of distinct lines meets exactly once, so

Σ_P m_P(m_P−1)=d(d−1),   H=(d−I)/s.

For every positive integer k and every integer m,

(m−k)(m−k−1)≥0.

Summing gives

I≤[d(d−1)+k(k+1)s]/(2k),

and therefore

H≥G_k(d,s):=−(k+1)/2 + d(2k−d+1)/(2ks).                 (3.1)

For every case used below, d>2k+1; thus G_k(d,s) is strictly increasing as a function of s>0. The inequality is valid across **all fields**, not only for realizable finite-plane deletions. It is a necessary lower bound, never an assertion that an arbitrary multiplicity list is realizable.

### Nonminimal configurations in the upper band

For 0≤i≤q−1, set d=N−i. EMSS gives s≥N. If s≥N+1, use k=q and compute

G_q(d,N+1)−C_q(i)=A_q(i)/[2qN(N+1)],

A_q(i)=q⁴−q−Ni²+(−q²+q+1)i.

This is concave in i. Its endpoint values are A_q(0)=q⁴−q>0 and A_q(q−1)=2(q²−1)>0, so it is positive throughout [0,q−1]. Thus any nonminimal configuration has H>C_q(i).

For i=q, d=q²+1 and s≥N−1. When s≥N,

G_q(d,N)−C_q(q)=(q−2)(q²+1)/[2q(q+1)N]>0.             (3.2)

### Nonminimal configurations in the middle band

Set i=q+1+a with 0≤a≤q−3, so d=q²−a and C_q(i)=−d/(q+1). EMSS gives s≥N−1. For s≥N use k=q−1. The difference

D_q(a)=G_(q−1)(q²−a,N)+(q²−a)/(q+1)

is a concave quadratic in a, and its endpoint values are

D_q(0)=q(q−1)/[2(q+1)N]>0,

D_q(q−3)=(q²+2q−9)/[(q−1)(q+1)N]>0.

Consequently H>C_q(i) for every nonminimal configuration in the entire middle band, without the polynomial restriction from the Outcome.

### Nonminimal configurations at the special endpoint

For i=2q−1, d=q²−q+2 and s≥N−2. If s≥N−1, again use k=q−1:

G_(q−1)(d,N−1)−C_q(2q−1)
 = (q−3)(q³−q²+3q−2)/[2q(q−1)(q+1)(N−2)]>0           (3.3)

for q≥4. Thus only configurations with the exact EMSS minimum number of singular points can attain or beat the conjectured value.

## 4. Defect counting inside an arbitrary projective plane

This section proves the minimum for **every** subarrangement of a projective plane of order q≥3 in the band, not merely for the particular known construction.

Start with a projective plane of order q, with N points and N lines. Retain d=N−i of its lines. Let u₀ count points on zero retained lines, and u₁ count points on exactly one retained line. Then

s=N−u₀−u₁,  I=d(q+1)−u₁,

so

H=(−qd+u₁)/(N−u₀−u₁).                              (4.1)

These identities also apply after dualizing an induced point-set embedding. All pairwise intersections remain in the ambient finite plane; scalar extension of a field realization introduces no new intersections.

A point counted in u₀ requires deletion of all q+1 lines through it; a point counted in u₁ requires deletion of q of them. Two such deficient points require at least 2q−1 distinct deleted lines because their pencils share at most one line. Thus:

- If i≤q−1, u₀=u₁=0, and every deletion has H=−qd/N.
- If i=q, only (u₀,u₁)=(0,0) or (0,1) is possible. The latter has the smaller quotient, because qd>N, and is obtained by deleting q lines of one pencil.
- If q+1≤i≤2q−2, the only possibilities are (0,0), (0,1), (1,0). The least quotient is −qd/(N−1), achieved by (1,0). Delete a complete pencil and any further i−q−1 lines.

For i=2q−1, three deficient points would require at least 3q−3>2q−1 deletions, by inclusion–exclusion on three q-element subsets of pencils. Also (1,1) requires at least 2q deletions and (2,0) at least 2q+1. Therefore the possible pairs are now (0,0), (0,1), (1,0), (0,2). The quotient for (0,2) is no greater than that for (1,0), since

qd−2(N−1)=q²(q−3)≥0.

It is also no greater than the other two. It is attained by deleting the line through two distinct points, plus q−1 other lines through each point. This uses exactly 2q−1 lines and leaves each chosen point on exactly one retained line. The resulting minimum is (−qd+2)/(N−2). For q=3 the (1,0) construction ties; for q≥4 it does not.

All constructions in this paragraph can be made in P²(F_q) when q is a prime power. They coincide with the credited DHS constructions in Proposition 5.1, apart from proving optimality within **all** deletions and identifying the q=2 endpoint defect.

## 5. Exact all-fields conclusions

For 0≤i≤q−1, Section 3 excludes s>N; at s=N, EMSS Theorem 3.6 embeds the dual NLS in a projective plane of order q. Section 4 gives H=C_q(i). This proves the first upper subband over all fields.

For i=q, the minimum singular count is N−1. At equality, EMSS Lemma 3.14 and Corollary 3.12 give one dual point of degree q and all others degree q+1. Thus I=(q+1)d−1 and H=(−qd+1)/(N−1). Equation (3.2) excludes nonminimal configurations.

For i=2q−1, the minimum count is N−2. EMSS Lemma 3.8 embeds every equality case for q≥4; Section 4 supplies its lower bound. Equation (3.3) excludes nonminimal cases.

For i=q+1+a, only s=N−1 remains. If the maximum block size is q+1, Corollary 3.12 gives H=(−qd+1)/(N−1)>C_q(i). If it is q and the sufficient polynomial condition holds, EMSS Theorem 3.23 embeds it, and Section 4 gives H≥C_q(i). More generally, under the integer test U_q(a)<L_q(a), the degree-excess argument in Section 6 gives δ=0 directly, again giving H=C_q(i). The explicit field construction supplies the opposite inequality in all cases. This proves the conclusions in the Outcome.

These are consequences of the source results plus the displayed incidence estimates; neither the established small cases nor the already known upper bounds are represented as new.

## 6. Exact remaining obstruction

In the still-unsettled middle-band cases, set d=q²−a with 0≤a≤q−3. By the preceding arguments, a counterexample must have

s=q²+q,  max_P m_P=q,

and its dual must be a nondegenerate finite linear space realizable by projective lines over some field. Every dual point x has degree r_x≥ceil((d−1)/(q−1))=q+1. Define the nonnegative integer

δ=Σ_x(r_x−q−1)=I−(q+1)d.

Then exactly

H=−d/(q+1)−δ/[q(q+1)].                              (6.1)

Therefore the residual conjecture is equivalent to **δ=0 for every such realizable minimal NLS**. A realizable example with δ>0 would be a genuine counterexample; a merely formal incidence solution or abstract nonrealizable NLS would not.

For these minimal maximum-q spaces, (3.1) with k=q−1 and s=q²+q gives δ≤(a²−a)/(2(q−1)); this is also EMSS Lemma 3.21. EMSS Lemmas 3.16–3.17 and the proof of Lemma 3.20 give, when δ>0, a number c of disjointness equivalence classes satisfying

1+q(q−a)/(q−a+δ)≤c≤1+floor(q/2).

Solving yields δ≥q−a for even q, and δ≥(q−a)(q+1)/(q−1) for odd q. Since δ is an integer, necessarily L_q(a)≤δ≤U_q(a). Thus U_q(a)<L_q(a) forces δ=0 and proves the target. Comparing the unrounded bounds yields the weaker sufficient polynomial conditions stated above.

Source audit: the displayed parity labels in EMSS Lemma 3.20 are interchanged. The proof immediately underneath gives the even/odd bounds just derived, and Lemma 3.22 and Theorem 3.23 use those same correct bounds. This report follows the proof and records the discrepancy rather than silently trusting the mislabeled display. The embedding theorems are still credited inputs; the integer sharpening and ratio deduction are supplied here. The q=13,a=10 case illustrates the useful integer sharpening: δ≤90/24=15/4 and, if positive, δ≥42/12=7/2. No integer δ fits. Thus the entire q=13 band is established too. The first remaining cases by d are q=16,a=13,d=243, where δ∈{3,4,5} remains possible, and q=16,a=12,d=244, where δ=4 remains possible. Neither existence nor realizability is asserted.

This finite-plane completion/defect analysis is the one substantive approach performed. It stops at this explicit obstruction, without launching another approach or treating abstract feasibility as geometry.

## 7. Standalone check: the one-line-deficit family

There is also a shorter proof for i=1 requiring only the classical de Bruijn–Erdős equality theorem. Put d=q²+q and N=d+1. A nonpencil configuration has s≥d. Equality s=d is either a near-pencil or a projective plane. A projective plane has n²+n+1 points for an integer n, and d lies strictly between the counts for n=q−1 and n=q; thus it cannot occur. After handling the near-pencil, s≥d+1=N. Equation (3.1) with k=q gives H≥−qd/N, and deleting one line from P²(F_q) attains it.

Equality in this lower-bound argument requires s=N and every multiplicity in {q,q+1}. This statement alone is not a classification of all equality configurations as field-plane deletions; no such stronger assertion is needed here.

## 8. Verification and limitations

The all-q arguments are the proofs above. The EMSS embedding inputs were read and visually checked in the public primary scan but are cited published theorems, not newly independently certified proofs. The [independent mathematical audit](INDEPENDENT_AUDIT.md) accepts the bounded partial theorem relative to those inputs. Neither this report nor that audit resolves the general conjecture or establishes worldwide novelty.

## References

1. J. Szpond (joint work with M. Dumnicki and D. Harrer), contribution to *Mini-Workshop: Arrangements of Subvarieties, and their Applications in Algebraic Geometry*, Oberwolfach Reports 14/2016, pp.695–697. Conjecture 1, p.696. https://ems.press/content/serial-article-files/46618
2. M. Dumnicki, D. Harrer, J. Szpond, *On absolute linear Harbourne constants*, arXiv:1507.04080v2; Finite Fields and Their Applications 51 (2018), 371–387, DOI 10.1016/j.ffa.2018.03.001. Definition 1.1, Conjecture 1.2, Theorems 1.4/1.6, Proposition 5.1. https://arxiv.org/abs/1507.04080v2
3. P. Erdős, R. C. Mullin, V. T. Sós, D. R. Stinson, *Finite linear spaces and projective planes*, Discrete Mathematics 47 (1983), 49–62, DOI 10.1016/0012-365X(83)90071-7. https://users.renyi.hu/~p_erdos/1983-05.pdf
