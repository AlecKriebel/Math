# GREEN-070 / ID 158 / row 1894: five residual approaches

## Disposition

**OPEN; no asymptotic solution claimed.** This work gives independently reproducible finite computations and a counterexample to one tempting extension of the seed method. It does not prove the residual lower bound c(log p)^2. No claim of literature novelty is made for the finite results. No QUEUE edit or publication was performed.

The recovery author gate and its primary-source files were the starting point, not results of this proof-search turn. Credit: Bedert, *On unique sums in Abelian groups*, arXiv:2303.15134v2, Combinatorica 44 (2024), supplies established superlogarithmic lower and O(log^2 p) upper progress. Cao–Yuan arXiv:2608.06728v1 claims the intermediate log p log log p bound and improved construction. Hou–Yang arXiv:2610.09349v1, dated 7 October 2026, claims 2^-80(log p/log log p)^2 and logarithmic exponent 2; its Question 5.1 explicitly leaves the constant-factor quadratic-logarithmic lower bound open. These recent manuscripts are inspected claims, not fully audited proof dependencies here. No finite result below depends on their compression theorem.

Public references:
- https://arxiv.org/abs/2303.15134
- https://arxiv.org/abs/2608.06728
- https://arxiv.org/abs/2610.09349
- https://people.maths.ox.ac.uk/greenbj/papers/open-problems.pdf (current Problem 27)

## Exact convention and scope

For odd prime p, let m(p) be the minimum |A|≥2 such that every represented residue has at least two unordered multiset representations a+b, with a=b permitted. Let u(s) count those multisets, r(s) count ordered pairs, and d(s)=1 if s/2 belongs to A and 0 otherwise. Then r(s)=2u(s)−d(s). Consequently the exact ordered criterion is r(s) not in {1,2} for every s, not merely r(s)≠1. Translation and multiplication by any nonzero residue preserve the property. Every set of size≥2 has an affine image containing 0 and 1; enumerating all such sets is exhaustive though not duplicate-free.

### Attempt 1: pair capacity, energy, and Fourier obstruction

Write n=|A| and S=A+A. Since u(s)≥2 on S,

2|S|≤n(n+1)/2, so |S|≤floor(n(n+1)/4).

Cauchy–Davenport gives |S|≥min(p,2n−1). Thus

min(p,2n−1)≤floor(n(n+1)/4).

This excludes all n≤6 for p≥11, but ceases to improve with p once n≥7. It is used as an exact necessary-condition pruning rule in the exhaustive search, never as a sufficient condition.

An energy refinement retains the diagonal information. On 2A, r is odd and at least 3, so r²≥4r−3. On S\2A, r is even and at least 4, so r²≥4r. Since |2A|=n,

E(A)=sum_s r(s)^2≥4n²−3n.

For the unnormalized Fourier transform this implies

sum_{t≠0}|Ahat(t)|^4≥p(4n²−3n)−n^4.

When the right side is positive and n<p, Parseval implies

max_{t≠0}|Ahat(t)|²≥[p(4n²−3n)−n^4]/[pn−n²].

For n=o(sqrt(p)) this guarantees only squared magnitude about 4n, far below the n² scale that would force near-concentration in a short arc. Thus this first-moment/energy route does not close the logarithmic gap. The inequalities are valid partial structural statements, not a new asymptotic lower bound.

### Attempt 2: affine rectification and midpoint determinants

Any affine image of A contained in an integer interval of diameter at most (p−1)/2 has a uniquely represented least sum: after translation, 0+0 is the only pair with sum 0 mod p. Therefore a NUS set resists every such rectification.

Diagonal repairs make A balanced: for each a, 2a=b+c with b,c distinct from each other and from a. Choose an inclusion-minimal nonempty balanced subset B of size k≤n, and one repair per point. Its integer rows are 2e_i−e_{b(i)}−e_{c(i)}. A rational kernel vector's maximal level is closed under the chosen repairs, hence is a nonempty balanced subset. Minimality forces the kernel to be constant, so the row rank is k−1. Delete an anchor column and select k−1 independent rows, obtaining D. Modulo p, the nonzero label-difference vector annihilates D, hence p divides its nonzero determinant.

Each row is (e_i−e_b)+(e_i−e_c). Multilinearity expands det D into 2^(k−1) incidence minors, each of absolute value at most one (by expansion along a row with ≤1 nonzero, or the zero row-sum case). Thus p≤|det D|≤2^(k−1)≤2^(n−1). This recovers the classical balanced lower bound n≥1+ceil(log_2 p); it is not claimed as new. It also makes a finite classification of possible seven-point NUS sets sufficient for a global eight-point bound, as in Attempt 5. Merely reusing diagonal repairs or rectification gives an exponential-in-n obstruction, not the needed exponential-in-sqrt(n) obstruction.

### Attempt 3: removing the compressed-height loss

The inspected Hou–Yang proof maintains an integer quotient with K=O(sqrt(n)+n/log p) anchor coordinates, and bounds every actual point's l1 coordinate norm by n^18. A full-rank compressed minor has row norms at most 4n^18. Hadamard consequently gives

log p≤(K−1)log(4n^18).

In the relevant n<(log p)^2 range this contains a log n factor. Eliminating that factor would require a new joint determinant/height estimate, not just the displayed dimension bound. Replacing Hadamard's maximum by the geometric mean only helps after proving sum_i log||row_i||=O(K), whereas the current stated hypotheses allow O(K log n). A generic degree-zero rank-defect row q(e_1−e_2) already illustrates that dimension plus modular defect alone does not bound determinant by exp(O(K)); its determinant after anchoring is q. This example is a linear-algebra obstruction, not asserted to arise from a NUS set.

I inspected the short-forest/height recurrence in Section 4: the round height factor is bounded by 60 while the moving count shrinks by 2/3. Earlier promoted cores persist and later point offsets can involve them, so counting fewer late cores does not by itself bound their coefficients or the determinant geometric mean. No valid cancellation theorem or improved height bound was obtained. The recent manuscript's compression theorem has NOT received a complete proof audit here and is used only to locate the remaining loss, not as a certified lemma supporting our finite conclusions.

### Attempt 4: higher-arity seeds to improve the upper bound

The known weak ternary seed mechanism uses a nontrivial certificate 3x=u+v+w at every seed point. It repairs the exceptional pair {2x,x+y} in C+C because the remaining two certificate entries still sum to an element of C+C. Replacing the arity by four looks attractive for a base-four shrinkage construction, but loses exactly this two-term closure.

There is a concrete counterexample to the naive replacement. In F_13, take C={0,1,4}. Every point is weakly quaternary-balanced:

4·0=1+4+4+4 (mod 13),
4·1=0+0+0+4 (mod 13),
4·4=0+1+1+1 (mod 13).

All three are nontrivial four-term multiset certificates. But C+C={0,1,2,4,5,8}, whose unordered representation counts indexed 0 through 12 are

[2,1,2,2,2,2,2,1,2,2,2,0,1].

Thus sums 1,7,12 are unique, respectively {0,1}, {2,5}, {4,8}. Weak quaternary balance does NOT imply C+C is NUS. This rigorously eliminates that proposed transfer, not other higher-arity constructions with stronger hypotheses or larger sumsets.

### Attempt 5: exact certificates and collision-lattice diagnostics

The exhaustive program `exact_search.py` enumerates combinations containing 0 and 1, rejects an unordered count equal to 1, and stops at the first witness at the first possible cardinality. All smaller non-pruned sizes are completely exhausted. The JSON records candidate counts, witnesses, and full unordered count vectors. Results:

p:    3  5  7  11 13 17 19 23 29 31
m(p): 3  4  5   7  7  8  9 10 11 11

For p=29 the n=7,8,9,10 exclusions check 80,730; 296,010; 888,030; 2,220,075 normalized candidates. For p=31 they check 118,755; 475,020; 1,560,780; 4,292,145. Exact witnesses are in `exact_results.json`; they are part of the authored certificate, not external dataset contents.

The separate C++ search exhausts seven-point sets for every prime 17≤p≤61, finding none. Attempt 2 excludes seven-point NUS sets for p>64. Combined with the pair-capacity exclusion of n≤6, this gives the finite/global corollary

m(p)≥8 for every prime p≥17,

with equality at p=17. This is a computer-assisted elementary corollary with explicit search code and bounded cases, not a novelty claim or an improvement over the large-p literature.

For each displayed minimal witness, `lattice_check.py` groups unordered pairs by their sum and takes differences against one representative per group. These rows span the full collision lattice: any two pairs' difference in that group is a difference of the selected rows. Deleting the last column identifies the sum-zero integer lattice with Z^(n−1). SymPy Smith normal form returns diagonal (1,...,1,p) in every case, so for these witnesses the full collision quotient has index exactly p. This is a finite diagnostic, not a universal assertion about minimal NUS sets or a formal proof certificate for the SNF implementation.

The implication “minimal witness → full rational rank n−1” also follows from the maximal-level argument for all pair collisions. Nothing in the observed invariant factors yields an n-versus-p asymptotic improvement without a new upper bound on their product.

## Acceptance limits

The five approaches were completed as bounded investigations. Attempts 1–3 recover useful constraints and identify a genuine quantitative obstruction; Attempt 4 refutes a specific tempting transfer; Attempt 5 supplies exact finite certificates and a global small-cardinality corollary. None resolves the asymptotic residual question. Finite computation cannot establish Theta(log²p), and the October preprint's exponent claim is not a full solution to the original order-of-magnitude question. Independent review is recorded separately against hashes of the reviewed artifacts; publication, if any, needs a separate parent decision and must exclude private source files.
