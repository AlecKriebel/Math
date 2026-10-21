# Independent adversarial audit: ETF span decompositions

Date: 2026-10-21. Scope: unit-norm real or complex ETF with n>d>=2, positive squared coherence q=(n-d)/(d(n-1)), and partitions whose blocks are tight for their individual spans. No full-resolution or novelty claim is certified.

## Source gate

Inspected the recovered publisher text, printed pages 2797–2798, contribution by Alex Fink, Emily King, Cynthia Vinzant, and Shayne Waldron. Question 2 concerns nontrivial disjoint-union decompositions into tight frames for spans. The source explicitly excludes both the whole-frame and all-singletons decompositions as trivial. Proposition 3 and Theorem 4 already address two and three blocks. The contribution also treats general tight frames, not only ETFs. Its final paragraph identifies higher-order and nested decompositions and dualities as ongoing directions. This audit does not reinterpret an existential question as solved by one example or by a dimension-one loophole. Source transcript inspection is not a certification that the literature has no later solution.

## Verified block lemmas

Let a block have m>1 vectors, rank r, Gram H, and tight bound alpha.

1. Trace and squared trace give alpha=m/r=1+(m-1)q and r=m/(1+(m-1)q). These scalar identities are necessary; if r has not independently been established as the actual rank they are not sufficient. The exact sufficient test is H^2=(m/r)H. Alternatively, an independently verified rank r together with trace equality m^2=r tr(H^2) suffices by equality in Cauchy–Schwarz for the positive eigenvalues.
2. Since q>0 and q<1, a nonsingleton block has 1<r<m. The function r(m)=m/(1+(m-1)q) increases strictly. A proper block therefore has r<d and r<1/q.
3. Since m>=r+1, q=(m-r)/(r(m-1))>=1/r^2. Thus r>=1/sqrt(q), and m>=1+1/sqrt(q). Equality characterizes a regular simplex block.
4. For a proper block, alpha<A=n/d. The complement frame operator is A I-alpha P and is positive definite. Consequently n-m>=d, giving the stronger size bound m<=n-d. Applied inside any parent tight block, the same reasoning gives a proper nonsingleton child size at most the parent's nullity. Simplex blocks have no proper nonsingleton tight children.
5. Full spark implies no proper nonsingleton tight block: such a block must be dependent while its rank is below d; full spark makes every subset of at most d vectors independent, and a larger subset spans d. This establishes indecomposability in the source's sense, because any nontrivial partition needs a proper nonsingleton block.
6. A partition into two blocks is impossible under n>d>=2 and q>0. This is already covered by the source and is not new progress.

## Exact divisor sieve

Write q=a/b in lowest positive terms, with a<b. Set D=b-a+am. Then

  ar=b-b(b-a)/D.

For a positive integer m, integer rank is equivalent to D dividing b(b-a). In the divisor-enumeration direction require D congruent to b-a modulo a and m=(D-b+a)/a in the desired range. The quotient b(b-a)/D is then congruent to b modulo a, because gcd(a,D)=1, so the resulting r is automatically integral. Retain only proper blocks, rank bounds, and the geometric matrix condition. Divisors alone never certify that a block exists.

## Additional structural restrictions

These claims were derived and proved during the audit; novelty is not assessed.

- Real blocks satisfy r<=1/q-2, and complex blocks satisfy r<=1/q-1. Proof: the m rank-one projectors have Hilbert–Schmidt Gram (1-q)I+qJ, hence are linearly independent. Thus m<=r(r+1)/2 in the real case and m<=r^2 in the complex case. Substitute m=r(1-q)/(1-rq), with r>1, and simplify.
- For two disjoint tight blocks with projections P_i,P_j and ranks r_i,r_j, tr(P_iP_j)=r_i r_j q. This follows by expanding the squared cross-inner-products and dividing by their frame bounds.
- If the span projections commute, r_i r_j q is the integer dimension of their intersection. It is positive. No pair of proper block spans can be nested: inclusion would force the larger rank to equal 1/q. In particular a commuting partition cannot contain any singleton block.
- In a commuting partition, simultaneous diagonalization identifies coordinate supports for all projections. Each coordinate belongs to at least two supports, because every proper block bound is strictly less than the global bound A. Therefore sum_i r_i>=2d.
- If one block is a regular simplex of rank s=1/sqrt(q) and all block projections commute, every other block rank is a multiple of s, because its intersection with the simplex span has integer dimension r_j/s.

## Commuting-simplex characterization

The proposed characterization is mathematically sound, subject to its explicit restrictive hypothesis. If all k blocks are regular simplices of rank s and all their span projections commute, simultaneous diagonalization gives supports of size s, with every pair meeting in exactly one coordinate. Tightness implies every coordinate belongs to L=ks/d=1+(k-1)/s supports. Thus L is an integer at least two, k is congruent to 1 modulo s, and the coordinate incidences form a 2-(k,L,1) design.

For the unique shared coordinate of any pair of supports, cross-block equiangularity forces every product of coordinate magnitudes to equal 1/s. All entries within each block at that coordinate consequently have constant magnitude; local tightness forces that magnitude to be 1/sqrt(s). Every coordinate is shared, so each local simplex matrix is flat. Multiplication by sqrt(s) and addition of a flat kernel row gives a real or complex Hadamard matrix of order s+1. The kernel is flat because the local Gram projection has constant diagonal s/(s+1). These are exactly the local data of the usual Steiner construction, up to unitary changes, permutations, and vector phases. Conversely those data construct such a decomposition.

This is a characterization of the commuting-simplex subclass, not all ETFs, all tight blocks, or even all partitions into simplices. Its novelty relative to existing Steiner/fusion-frame literature remains unverified.

## Naimark duality claim

Verified: normalized complementary Gram is G'=(nI-dG)/(n-d). For a proper nonsingleton tight block, its principal submatrix has eigenvalues n/(n-d), multiplicity m-r, and (n-d alpha)/(n-d), multiplicity r. Both are positive and distinct. The same index set therefore becomes independent and cannot be tight in the Naimark complement. This is only a statement about the same index set; it does not assert that the complement ETF is indecomposable or has no other tight subsets.

## Independent SIC(3) verification

`independent_audit_check.py` independently computes all 84 three-column determinants in the exact field Q[z]/(z^2+z+1), without SymPy or the primary matrix-identity implementation. It finds exactly the same 12 dependent triples. Pairwise coherence guarantees rank two for each; trace equality then establishes tightness. The scalar sieve admits no other proper nonsingleton block size for (n,d,q)=(9,3,1/4).

Independent disjoint-combination counting verifies 12 partitions with one triple and six singleton blocks, 12 with two triples and three singleton blocks, and four with three triples: 28 nontrivial partitions total. These are unordered partitions of this fixed, labelled ETF; they are not 28 unitary-equivalence classes, and the count is not a universal classification of all ETFs with these parameters. The primary enumeration's loops correctly include mixed singleton tails, which the source's nontriviality definition allows.

## Acceptance boundary

The local lemmas, exact finite example, and restrictive commuting characterization are accepted as partial structural progress. Any claim that these resolve the original open classification question is rejected. Acceptance of a final report requires its text to preserve the n>d>=2 noncollinear scope, distinguish necessary arithmetic from sufficient Gram tests, label known source results, keep novelty unverified, and state that the general problem remains unresolved by this work.

## Additional harmonic (15,8) independent census

`independent_harmonic_check.py` reconstructs the displayed difference-set frame using integer polynomial coefficient arrays and the explicit polynomial Phi_15=x^8-x^7+x^5-x^4+x^3-x+1. It uses neither SymPy nor the primary script's triangle-product characterization. It verifies difference counts and coherence, then applies the full principal-Gram equation K^2=10K to all 3003 five-subsets, where K=8H. Exactly the three residue-class blocks modulo 3 pass. Disjoint-subset counting gives 3 partitions with one five-block, 3 with two five-blocks, and 1 with three five-blocks: seven nontrivial labelled partitions total. The necessary size bound m<=n-d=7 is essential: integrality alone also admits m=9. The exact size-plus-integrality sieve leaves m=5.

Both independent programs use explicit runtime guards, not assertions, and pass normal and optimized (`python -O`) execution. Thus optimization does not silently discard their verification checks. The primary scripts originally used assertions; their author subsequently replaced these with explicit runtime guards and reports successful optimized execution.

The full `RESULTS.md` was reviewed after its five approaches were written. Its mathematical claims are accepted within their stated scope; the addition of the harmonic census was independently verified as above. Hadamard completion should be read with its necessary explicit normalization: if C=sqrt(s)B and u is a unit kernel vector, append sqrt(s+1)u*, which is unimodular and has the same row norm as C.
