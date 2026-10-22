# Exact higher-order matrix decomposability: research and partial results

Row 1834, ID30004154, source OWR16938-002. Research date 2026-10-21. **Not a resolution of the full original problem.** No queue or GitHub changes made.

## Target and source gate

For a real symmetric PSD Q, characterize when Q = sum_{|S|=k} E_S Π_S E_S^T with every Π_S PSD, k>2, and zero residual. This is membership in FW_k. Blocks overlap and are not required to equal Q's principal submatrices. Recovered source: printed pp.1594–1595 in the official OWR report (public URL in SOURCE_GATE.md). Frangioni paper Appendix A, Eq.(37), already provides the generic SDP formulation for k=3 and its extension. Thus restating primal/dual SDP feasibility is not a new solution.

## Approach 1: literature audit

- Boman, Chen, Parekh, Toledo (2005), On factor width and symmetric H-matrices, DOI 10.1016/j.laa.2005.03.029. Author text: https://www.cs.tau.ac.il/research/doron.chen/Pubs/factorwidth.pdf. Gives FW2 characterization and normalized absolute-value spectral lower bound.
- Johnston, Moein, Plosker (2025), The Factor Width Rank of a Matrix, https://arxiv.org/abs/2405.11556 and DOI 10.1016/j.laa.2025.03.016. Gives chordal/bandwidth sufficient conditions, factor-width-rank results, and explicitly describes numerical SDP membership. Factor-width-k rank is different from factor width.
- Gouveia, Kovačec, Saee, On sums of squares of k-nomials, https://arxiv.org/html/1912.01371v2. Gives known dual description, extreme-dual-ray results when k=n−1, and symmetric-quadratic results. Theorem 4.8 describes non-PSD extreme rays using ranks of principal submatrices; Proposition 4.9 parametrizes the 4-by-4 case. These are structural partial results, not an unrestricted simple characterization.
- Absolutely k-incoherent results quantify over all orthogonal/unitary conjugates and must not be substituted for ordinary membership of a fixed matrix.

No general new solution was verified. Novelty of deductions below is not claimed; exact identities and counterexamples are independently derived here.

## Approach 2: complete permutation-symmetric slice

Let Q have diagonal d and off-diagonal c, with n≥k≥2. Then Q∈FW_k iff

    d ≥ (n−1)c/(k−1) when c≥0;
    d ≥ −(n−1)c when c≤0.

The second condition is simply PSD for this negative-c slice and implies ordinary diagonal dominance. For c≥0 necessity follows by testing with Y=kI−J: every k-principal submatrix is PSD and tr(YQ)=n[(k−1)d−(n−1)c]. Sufficiency is explicit: put on every k-subset a block with diagonal d/C(n−1,k−1) and off-diagonal c/C(n−2,k−2). These blocks sum to Q. Their two eigenvalues are the diagonal minus off-diagonal (multiplicity k−1), and diagonal+(k−1)off-diagonal, exactly yielding the displayed conditions. In the c≤0 case the same construction also applies. This symmetric characterization is already known in the Gouveia–Kovačec–Saee setting, so it is not presented as novel.

## Approach 3: strict rational counterexample to the spectral-bound characterization

Let B have rows (1,1/2), (1,−1/2), (1,3/4), (1,−3/4). Set

Q=BBᵀ =
[5/4, 3/4, 11/8, 5/8;
 3/4, 5/4, 5/8, 11/8;
 11/8, 5/8, 25/16, 7/16;
 5/8, 11/8, 7/16, 25/16].

All entries are positive. If C is its diagonal normalization, the two nonzero eigenvalues of C=|C| are 72/25 and 28/25. In particular ||C||₂=72/25<3.

Nevertheless Q is not in FW3. Any rank-one term vvᵀ in a PSD decomposition has v∈range(B), so write v=Bu. A three-sparse Bu must vanish in one row: u is proportional to (−t,1), where t∈{±1/2,±3/4}. For H=diag(−1,3/4), all those directions have uᵀHu>0 while tr(H)=−1/4. Since Q=Σ(Bu_j)(Bu_j)ᵀ would imply I₂=Σu_ju_jᵀ, taking the H pairing is impossible.

An explicit ambient dual certificate is Y=M/2704, where

M=[3247, −881, −2481, −561;
   −881, 3247, −561, −2481;
   −2481, −561, 2447, −81;
   −561, −2481, −81, 2447].

All principal minors of Y of sizes 1,2,3 are positive. Ordered by increasing size then lexicographic subsets, they are
3247/2704,3247/2704,2447/2704,2447/2704;
903/676,331/1352,1411/1352,1411/1352,331/1352,553/676;
15/676,15/676,115/676,115/676.

Thus all 3-principal blocks are positive definite, but tr(YQ)=−1/4. Construction: B+=(BᵀB)⁻¹Bᵀ, P=I−BB+, Y=2P+B+ᵀHB+.

This extends to a full-rank counterexample: Qε=Q+I/1000 is positive definite and tr(YQε)=−12781/52000<0. Its normalized absolute-value spectral norm is still at most72/25<3: normalized diagonal remains1 while every off-diagonal positive entry decreases; Perron monotonicity applies. Equivalently Cε=Dα C Dα+I−Dα² with α_i²=Qii/(Qii+ε), so Cε≼I+(72/25−1)Dα²≼(72/25)I. Therefore the normalized-absolute spectral lower bound is genuinely insufficient even for strictly positive definite 4-by-4 matrices at k=3.

Exact replay: python verify_exact.py. All certificate checks use rational SymPy arithmetic; no numerical optimization is used.

### All-k spectral counterexample family

For every k≥3 put n=k+1, p=ceil(n/2), q=floor(n/2), and take B with p rows (1,3/4) and q rows (1,−3/4). Then Q=BBᵀ has factor width exactly n. Indeed every vector Bu with any zero coordinate is proportional to B(−3/4,1)ᵀ or B(3/4,1)ᵀ. Every nonnegative combination of the corresponding two outer products in coefficient space has first diagonal entry 9/16 times its second, and so cannot equal I₂. Consequently no decomposition with supports<n exists.

Every diagonal of Q is25/16. Its normalized matrix C is entrywise positive with within-group entries 1 and cross-group entries 7/25. Its maximum row sum is p+7q/25=n−18q/25≤n−36/25<n−1=k, so ||C||₂<k. This defeats sufficiency of the normalized-absolute spectral bound for every k≥3. It is an independently derived elementary counterexample family, with no novelty claim. The separate rational 4-by-4 certificate above supplies a concrete positive-definite example rather than merely a rank-deficient family.

## Approach 4: range, kernel, and sparsity structure

Let Q=BBᵀ have rank r with B full column rank. For each size-k set S, define L_S=ker(B_{S^c})⊂R^r. All allowable rank-one factors are Bu for u∈L_S. This is because any x∈ker Q has 0=xᵀQx=Σ(xᵀv_j)², forcing every v_j⊥ker Q.

If every L_S has dimension≤1, pick a nonzero generator u_S for every nonzero L_S and discard duplicate lines. Then

    Q∈FW_k iff I_r=Σ_S λ_S u_Su_Sᵀ for λ_S≥0.

This is a finite scalar nonnegative linear feasibility problem in r(r+1)/2 equations, with no PSD block variables. It supplies an explicit decomposition Q=Σ λ_S(Bu_S)(Bu_S)ᵀ. If feasible, conic Carathéodory yields at most r(r+1)/2 distinct rays. Rational B gives rational rays and, when feasible, rational scalar coefficients.

For a full-spark B (every r rows independent), nonzero u has at most r−1 vanishing coordinates in Bu, so FW(Q)≥n−r+1. At the critical k=n−r+1 every omitted set has r−1 independent rows, hence dim L_S=1 and the finite linear test applies. This is a structural restricted-rank solution, not a characterization of arbitrary full-rank matrices. Zero rows must first be removed; if effective dimension n≤k membership is automatic.

For rank 2, after zero rows are removed and k<n, every L_S has dimension≤1. LOW_RANK.md gives the complete angular criterion and multiplicity test. The framework is equivalent to finite scalable-frame feasibility, so priority is not claimed.

Graph approach: a PSD matrix supported on a chordal graph with clique number≤k has FW≤k by clique decomposition (known). A chordal supergraph yields the sufficient bound FW≤treewidth(G)+1. These are not necessary: dense diagonally dominant PSD matrices have FW2. A graph-only criterion cannot decide membership for a given dense matrix: a strictly diagonally dominant dense matrix is FW2, whereas dense rank-one J is not FW_k for k<n.

## Approach 5: exact construction and obstruction to elimination

FW_k is not closed under scalar Schur complements for any k≥3. Let n=2k−1 and
v=(1,1_{k−1},0_{k−1}), w=(1,0_{k−1},1_{k−1}).
Q=vvᵀ+wwᵀ is explicitly in FW_k. Its Schur complement after eliminating coordinate 1 is

    (1/2)zzᵀ, z=(1_{k−1},−1_{k−1}).

A rank-one PSD matrix has factor width equal to the support of its defining vector, so this Schur complement has factor width 2k−2>k. Thus an elimination strategy cannot silently reuse the k=2 closure property. This identity requires no numerical assumptions. The support graph before elimination is two size-k cliques sharing one vertex, illustrating that a favorable chordal decomposition can be destroyed by a bad elimination order.

The symmetric-block formula, finite-ray positive coefficients, and rational dual counterexample give exact constructive certificates in their stated scopes. None resolves the unrestricted structural characterization requested by the original problem.

## Outcome

Five approaches completed to useful stopping points. Concrete advances: exact singular and strictly positive-definite n4,k3 counterexamples to a tempting spectral test; ambient rational dual witness; finite-ray criterion at the generic critical rank; complete symmetric slice (known); and explicit failure of Schur-complement closure for all k≥3. General classification remains unresolved. The independent mathematical audit in AUDIT.md accepts these restricted claims.
