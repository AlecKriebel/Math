# Fixed-diagonal projection paving: five approaches and priority audit

21 October 2026. Problem 20000566. CLAIMED_SOLVED for the recovered finite universal fixed-diagonal formulation: the prefix inequalities characterize strict r-pavability of every member, with a common positive gap on each fixed finite fiber. This is not a solution of stronger prescribed-gap, dimension-uniform, or existential formulations, and not a novelty claim. This publication derivative preserves all five mathematical approaches.

## Scope and answer

Let P=P*=P² on F^n, F=R or C, and 1≤r≤n. Write π_r(P)=min_partition max_j ||P[S_j,S_j]||, with r nonempty coordinate blocks. Quantitative paving means π_r(P)≤ε; finite strict paving means π_r(P)<1. A dimension-independent strict gap means a single ε<1 works for an entire family with unbounded n. These are different.

The abbreviated live Dan Edidin question concerns dimension-independent conditions on diagonals for fixed r, not n=4. Its existential/universal quantifiers and tolerance were not specified there. However, the same workshop’s 2014 participant contribution A.4 explicitly asks the universal finite-fiber ε_d>0 question, matching Casazza–Edidin Problems 9.4/9.7. Approach 4 proves a complete characterization for that precisely recovered formulation; it does not compute the optimal ε_d or give a gap uniform across dimensions. The four-dimensional generated question is a valid, narrow corollary/synthesis of known work, not a full answer. Its exact result is correct:

For every complex half-diagonal 4×4 projection,
π₂(P)=1/2+min(|p12|,|p13|,|p14|),
with full image [1/2,1/2+1/(2√3)]. Every real member has π₂=1/2.

For sorted admissible d, the recovered universal finite-fiber question has the exact answer Σ_{i=1}^{kr+1}d_i<(r−1)k+1 for all k≥0 with kr+1≤n. Sufficiency is explicitly prior art; necessity is proved below by a fractional Schur–Horn coupling, independently checked, with novelty unestablished.

A broader distinction is essential: every finite projection with diagonal at most 1−1/r is strictly r-pavable, by the classical matroid partition theorem. For admissible constant diagonals α this threshold is exact. In particular every finite half-diagonal projection is strictly two-pavable. Nevertheless, across all dimensions the half-diagonal two-paving constants have supremum 1. The known nonuniform examples do not contradict finite strict paving.

## Approach 1: projection equations and exhaustive partition types

Put a=|p12|, b=|p13|, c=|p14|. From (P²)ii=Pii=1/2, every off-diagonal squared row sum equals 1/4. Subtracting these four row equations gives |p12|=|p34|, |p13|=|p24|, |p14|=|p23| and a²+b²+c²=1/4. One can obtain the complementary equalities by adding row equations 1+2−3−4, and cyclic variants.

Each 2×2 compression on {i,j} has eigenvalues 1/2±|pij|. Thus the three balanced partitions have maximum norms 1/2+a, 1/2+b, 1/2+c. Every 1+3 partition has value 1: rank P=2, so its two-dimensional range intersects the three-dimensional coordinate subspace nontrivially, producing a compression eigenvector with eigenvalue 1. This proves the claimed per-projection formula, including all seven partitions. The minimum of a,b,c is at most 1/(2√3).

For full attainment use real a,b,c≥0 with a²+b²+c²=1 and
S(a,b,c)=[[0,a,b,c],[a,0,ic,−ib],[b,−ic,0,ia],[c,ib,−ia,0]].
Direct multiplication gives S*=S and S²=I. Hence P=(I+S)/2 is a half-diagonal projection. Set a=b=t and c=√(1−2t²), 0≤t≤1/√3. Then π₂(P)=(1+t)/2, covering the entire interval. At t=1/√3 all six off-diagonal magnitudes coincide; at t=0 the value is 1/2. These are explicit representatives, not a claim to rederive the entire phase classification.

For the real conclusion suppose all six off-diagonal entries of S=2P−I are nonzero. A diagonal sign conjugation makes S12=a,S13=b,S14=c positive. Write S23=x,S24=y,S34=z, real. The three off-diagonal equations (S²)12=(S²)13=(S²)14=0 are bx+cy=0, ax+cz=0, ay+bz=0. Substitution gives −2abx/c=0, impossible. Thus some off-diagonal entry is zero; the complementary equalities give a zero incident to coordinate 1, and the formula yields π₂=1/2. No classification of the real fiber is required.

Outcome: complete exact narrow profile by elementary equations. Limitation: no novel broad fixed-r theorem. Giol et al. already supply the structural parametrization and real zero-entry obstruction.

## Approach 2: tight frames and Bloch-sphere geometry

Write P=V*V with V a 2×4 coisometry. Its columns v_i have squared norm 1/2. Set w_i=√2 v_i, so ||w_i||=1 and Σ w_i w_i*=2I₂. For complex unit vectors write w_i w_i*=(I+n_i·σ)/2, where σ are the Pauli matrices and n_i∈R³ are unit vectors. The tight-frame equation becomes Σn_i=0. Taking traces of products yields |pij|²=(1+n_i·n_j)/8.

Since n1+n2=−n3−n4, opposite pair dot products agree, recovering the complementary magnitudes geometrically. At the upper endpoint all off-diagonal squared magnitudes are 1/12, so all distinct pair dot products are −1/3: the Bloch vectors are a regular tetrahedron. Conversely a regular tetrahedron has zero sum and yields such a tight frame. Orthogonal spinors give antipodal Bloch vectors and a zero matrix entry, explaining the lower endpoint. For real vectors the Bloch vectors lie in a plane; the algebra in Approach 1 proves that this restriction forces a zero pair.

Outcome: a geometric explanation of the extremizer, aligned with the workshop's vector-configuration motivation. Limitation: this reformulation is dimension/rank-specific and does not classify higher-rank diagonal fibers. It is not independent evidence of novelty; the explicit algebra supplies the proof even without geometric terminology.

## Approach 3: centered operators and a prior-art cross-check

For the half-diagonal fiber A=P−I/2 is Hermitian, zero-diagonal, and has norm 1/2; S=2P−I has norm 1. These are not projections. For a balanced pair compression, A has eigenvalues ±|pij|, giving ||P_pair||=1/2+||A_pair||. For a triple compression, P has eigenvalues 1,1/2,0: the eigenvalue 1 follows from range intersection, 0 from kernel intersection, and the remaining eigenvalue from trace 3/2. Consequently ||A_triple||=1/2. Thus, specifically on this fiber, the centered absolute two-paving parameter is min(a,b,c), and π₂(P)=1/2+α₂(A). Its normalized centered parameter β₂(A)=α₂(A)/||A|| equals 2min(a,b,c).

This identity is not a general identity for arbitrary Hermitian matrices: adding a scalar identity shifts the largest eigenvalue, not the operator norm symmetrically. Weiss–Zarikian Proposition 6.2.2 proves the universal normalized centered bound 1/√3 for all zero-diagonal complex Hermitian 4×4 matrices. Applied to A and the triangle inequality it already gives π₂(P)≤1/2+1/(2√3). The explicit family proves sharpness inside this smaller projection fiber.

Outcome: independent consistency check and a decisive priority correction. The upper endpoint was already an immediate 2010 theorem consequence. The exact fiber range was not located verbatim, but is an elementary specialization with no established novelty.

## Approach 4: complement frames and finite strict paving

Let Q=I−P. For a coordinate subset J, Q[J,J] is the Gram matrix of {Qe_i:i∈J}, since Q*=Q²=Q. Also P[J,J]=I_J−Q[J,J], and 0≤Q[J,J]≤I_J. Therefore ||P[J,J]||<1 iff Q[J,J] is positive definite iff these complement columns are linearly independent.

By Edmonds's matroid partition theorem (equivalently the vector-space Rado–Horn criterion),
π_r(P)<1 iff |J|≤r rank Q[J,J] for every J⊆[n].
The theorem gives at most r independent parts; when r≤n split parts to get exactly r nonempty ones. Splitting preserves independence. The finitely many resulting positive eigenvalue gaps have a positive minimum, but that minimum depends on P and n.

Since eigenvalues of Q[J,J] lie in [0,1], rank Q[J,J]≥trace Q[J,J]=Σ_{i∈J}(1−d_i). If all d_i≤1−1/r then the criterion holds. A slightly more flexible diagonal-only sufficient condition is
Σ_{i∈J}(1−d_i)>floor((|J|−1)/r) for every nonempty J.
Indeed integer rank must then be at least ceil(|J|/r). For each cardinality it suffices to test the subset with the largest d_i. The following completion proves necessity for the universal, not individual, finite strict property.

Necessarily n≤r rank Q=r(n−rank P), by applying the criterion to all coordinates. Also every d_i<1 is necessary. For a constant diagonal α=rankP/n, the necessary rank bound says α≤1−1/r, and the preceding sufficient result proves the converse. Hence finite constant-diagonal strict paving has the exact threshold α≤1−1/r, over both fields whenever such a projection exists.

### Exact universal finite-diagonal criterion (classical-input derivation)

Assume d∈[0,1]^n and Σd_i is an integer, so the real and complex projection fibers are nonempty. Set q_i=1−d_i and m=Σq_i. Then the following are equivalent:

1. Every projection with diagonal d is strictly r-pavable.
2. For every nonempty J, |J|≤r ceil(Σ_{i∈J}q_i).
3. For every nonempty J, Σ_{i∈J}q_i>floor((|J|−1)/r).

Sufficiency was proved above by the rank/trace bound. For necessity fix J, put s=|J|, t=n−s and a=Σ_Jq_i=f+θ, f=floor a and 0≤θ<1. We construct a REAL projection Q with diagonal q and rank Q[J,J]=ceil a. This construction works separately for each J; no simultaneous rank minimization is claimed.

If θ=0, Schur–Horn supplies block projections of ranks f and m−f with diagonals q_J and q_Jc. Their direct sum suffices, including ranks zero and empty blocks. The majorization condition holds because entries are in [0,1] and their sums equal the proposed integer ranks.

If 0<θ<1, necessarily f+1≤s and m−f≤t, and m−f−1≥0. Start with a projection Q0 having f coordinate eigenvalues 1 inside J, m−f−1 coordinate eigenvalues 1 inside Jc, and the 2×2 rank-one block [[θ,√(θ(1−θ))],[√(θ(1−θ)),1−θ]] coupling one remaining coordinate from each side; all remaining entries are zero. Its two compression spectra are (1 repeated f, θ, zeros) and (1 repeated m−f−1, 1−θ, zeros). Each spectrum majorizes the respective target diagonal: partial sums before its last nonzero eigenvalue are bounded by the number of terms because q_i≤1, and all later sums are bounded by the total mass. The real symmetric Schur–Horn theorem supplies separate orthogonal conjugations on J and Jc realizing the target diagonals. Their block-diagonal conjugation preserves projection status and both compression spectra, so rank Q[J,J]=f+1=ceil a.

If condition 2 fails for J, take P=I−Q. The matroid criterion rules out strict r-paving for this P. Therefore a violating diagonal has a witness in the real fiber, and the universal criterion is identical over R and C. Conditions 2 and 3 are equivalent because ceil a≥ceil(s/r) iff a>ceil(s/r)−1=floor((s−1)/r). Sorting q increasingly reduces condition 3 to prefix inequalities. Only prefix lengths j=kr+1≤n need checking: the right side floor((j−1)/r) is constant between successive such lengths, while prefix sums increase. Equivalently, for d sorted decreasingly, Σ_{i=1}^{kr+1}d_i<(r−1)k+1 for every k≥0 with kr+1≤n. For rank-two projections in M4 and r=2, this is exactly 0<d_i<1 for all i: the length-one test excludes d_i=1 and the length-three test uses Σd_i=2 to exclude d_i=0.

For fixed n and fixed d, the fiber is compact and π_r is continuous (the minimum of finitely many continuous partition-norm functions). Thus if condition 1 holds, there is an ε(d)<1 bounding every projection on that fixed fiber. This compactness bound need not remain below 1 uniformly for varying dimensions or varying d.

The sufficient sorted inequalities are explicitly Proposition 9.6 of Casazza–Edidin, *Equivalents of the Kadison-Singer Problem*, and Proposition 9.3 already gives the max-diagonal finite strict threshold. Their Problem 9.7 asks necessity and Proposition 9.8 proves the equality obstruction. The fractional coupling argument above completes necessity for this precisely formulated finite problem, and compactness gives precisely the ε_d formulation of their Problem 9.4. This is a verified mathematical conclusion about that formulation, not a claim that the argument is unpublished or that the older question is still open. It does not supply a prescribed ε or a dimension-independent gap. The 2014 live wording asks dimension-independent conditions without specifying ε or quantifiers; under the universal finite-strict interpretation the criterion gives a dimension-independent rule (with dimension-dependent finite prefix range), but a full-status assertion for other interpretations is not justified.

For individual projections, even strict pavability is not determined by the diagonal in larger dimensions. Put J=the 3×3 all-ones matrix. Define Q_bad=diag(J/3,I₃−J/3) and Q_good=[[I₃/3,√2 I₃/3],[√2 I₃/3,2I₃/3]], and P_bad/good=I₆−Q_bad/good. These are real rank-three projections with common diagonal d=(2/3,2/3,2/3,1/3,1/3,1/3). The first three Q_bad columns have rank one, violating the two-part matroid test, so π₂(P_bad)=1. For P_good the first-three/last-three partition has compression norms 2/3 and 1/3; the diagonal lower bound makes π₂(P_good)=2/3. Thus the same diagonal permits one strictly pavable member and one not strictly pavable member. This explicit synthesis was independently checked; novelty is not asserted.

Outcome: an exact test for a particular projection and an exact constant-diagonal finite-strict classification. Limitation: the individual test uses ranks of compressions, whereas the universal criterion uses diagonal prefix sums; the inputs are classical and neither supplies a dimension-independent quantitative gap. Do not call a bound α<1/4 the best finite strict two-paving condition.

## Approach 5: quantitative diagonal tests, known bounds, and the nonuniform obstruction

For any partition, ||P[J,J]||≥max_{i∈J}d_i and ||P[J,J]||≤Σ_{i∈J}d_i. Thus π_r≥max_i d_i, and a partition of diagonal masses into r bins each of sum≤ε guarantees π_r≤ε for every projection with that diagonal. If rankP=1, each nonzero compression is rank one with norm exactly its trace, so this scalar bin-packing optimum is exactly π_r. This is one fully solved diagonal-only subclass. For rankP>0 also π_r≥1/r: writing P=V*V with VV*=I_k, the r frame operators V_J V_J* sum to I_k, and each has norm≤π_r.

For quantitative guarantees independent of n, MSS gives π_r(P)≤(1/√r+√α)² for max d_i≤α (one may cap the bound at 1). For r≥2, Leake–Ravichandran Theorem 1.4 improves this to (√(1/r−α/(r−1))+√α)² when 0<α≤(r−1)²/r². It is strictly below 1 when α<(r−1)²/r². In particular α<1/4 suffices for a uniform two-block gap; α=1/2 gives a strict four-block gap. These are quoted verified sufficient theorems, not asserted to be the current sharpest bounds or exact characterizations. Allowing r to vary with α is not a solution for prescribed r.

Here is a self-contained verification of the published CFMT half-diagonal obstruction. For integer m≥1 let U be a unitary Fourier matrix of size 2m, all squared entry magnitudes 1/(2m). Form B1=U D1 and B2=U D2, where the first m−1 entries of D1 are √2 and the remaining m+1 entries are √(2/(m+1)); D2 has first m−1 entries zero and remaining entries √(2m/(m+1)). Stack B1 over B2 to form B of size 4m×2m. Each row has norm 1, and B*B=2I. Therefore Q=BB*/2 and P=I−Q are projections of size 4m, rank 2m, diagonal 1/2.

In any partition into two blocks, one block contains at least m of the first 2m row indices. Choose a unit coefficient vector supported on those indices which annihilates the first m−1 columns of B1; there is such a vector by dimension. On the remaining columns B1 is scaled by √(2/(m+1)) relative to U, so its Gram Rayleigh quotient is at most 2/(m+1). Thus Q has a compression Rayleigh quotient at most 1/(m+1) on that vector, and the corresponding P compression has norm at least m/(m+1). Hence π₂(P)≥m/(m+1)→1. Approach 4 simultaneously proves π₂(P)<1 for every fixed m.

Outcome: a rigorous separation of finite strict and uniform quantitative paving, with an explicit family. Limitation: this is a reconstruction of published CFMT examples, not a new obstruction. Neither the 4×4 profile nor the matroid test settles universal exact prescribed-ε diagonal classification.

## Priority and claims ledger

- Original scope: Dan Edidin, AIM workshop Beyond Kadison–Singer, December 2014. Live notes are abbreviated; the same workshop participant contribution A.4 (printed p4, version 30 November 2014) explicitly supplies the universal finite-fiber formulation. Its subsequent geometric sentence incorrectly uses nonempty intersection where containment corresponds to the universal quantifier; the next paragraph again uses the universal premise. We adopt the explicit quantified mathematical statement, not that geometric slip. No source text or source document is reproduced here. https://aimath.org/WWN/beyondks/beyondks.pdf
- Giol–Kovalev–Larson–Nguyen–Tener, arXiv:0906.0139, §3.2: explicit half-diagonal complex 4×4 parametrization and real zero-entry obstruction. https://arxiv.org/pdf/0906.0139
- Weiss–Zarikian (2010), Proposition 6.2.2: centered 4×4 bound implying the upper endpoint. https://files.ele-math.com/articles/oam-04-17.pdf
- Casazza–Edidin, *Equivalents of the Kadison-Singer Problem*, §9: finite strict threshold (Prop.9.3), sufficient prefix criterion (Prop.9.6), necessity question (Problem9.7), equality obstruction (Prop.9.8), and compactness discussion. https://www.aimath.org/WWN/kadisonsinger/123.KS.pdf
- Carlen–Lieb, *Short proofs of theorems of Mirsky and Horn on diagonals and eigenvalues of matrices*, arXiv:0904.0734v3, explicitly recalls/proves the real-orthogonal form of Schur–Horn used above. https://arxiv.org/pdf/0904.0734
- Edmonds (1965), Theorem 1: matroid partition criterion used in Approach 4. https://nvlpubs.nist.gov/nistpubs/jres/69B/jresv69Bn1-2p67_A1b.pdf
- Casazza–Peterson (2011): modern elementary proof of Rado–Horn. https://arxiv.org/abs/1112.0161
- Casazza–Fickus–Mixon–Tremain (2010), Proposition 3.1: nonuniform half-diagonal family used in Approach 5. https://arxiv.org/pdf/1005.2164
- MSS: dimension-free variable-bound theorem. https://arxiv.org/pdf/1306.3969
- Leake–Ravichandran, Theorem 1.4: refined sufficient bound. https://arxiv.org/pdf/1609.04195

Status: five substantive approaches completed; exact narrow profile verified and broader finite-strict consequences clarified. Broad quantitative fixed-r prescribed-diagonal classification is not solved here. The finite universal prefix criterion answers the explicit finite question in both the located Casazza–Edidin source and the same-workshop 2014 participant formulation; current novelty and broader interpretation remain unestablished. No assertion of current open status beyond the bounded source screen; no novelty assertion. Exact symbolic identities and exhaustive finite checks accompany this report.
