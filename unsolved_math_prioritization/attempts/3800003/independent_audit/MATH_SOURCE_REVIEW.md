# Independent mathematical source audit

Problem 3800003, AMR-037-0003, queue rank 927. Reviewed on 6 October 2026.

## Conclusion

The mathematical claims reviewed in PROOF.md and REPORT.md pass. The existential question asking for a convex 4-polytope with at least twice as many degenerate facets as vertices was answered by the cited prior work. The stated cubical witness is valid. The Nevo-Santos-Wilson construction gives a genuine convex lower bound of exponent 3/2. The authored quadratic upper bound is correct. These facts do not determine the sharp maximum.

No blocking mathematical correction was found. Two precision improvements are advisable: state the domain N >= 5 when defining D_4(N), and describe the Avvakumov-Hubard theorem using its explicit lower-bound quantifiers rather than the potentially ambiguous phrase “order N^(5/4).” Neither changes the conclusions.

This audit checks the use of the external existence theorems, their hypotheses and conclusions, the relevant construction-to-polytope implication, and the independent counting argument. It does not claim a new proof of either external construction, a coordinate realization certificate, or an exhaustive current-literature survey.

## Definition and original question

The first problem on [Jeff Erickson's original page](https://jeffe.cs.illinois.edu/open/comb.html) defines degeneracy by a facet having more than d vertices in dimension d. For a convex 4-polytope, every facet is three-dimensional, and a three-dimensional polytope with exactly four vertices is a tetrahedron. Thus “degenerate” here means a nontetrahedral, equivalently nonsimplex, facet. It does not refer to a zero-volume cell.

The page asks the general extremal question, singles out the 2N existence question, and also expresses interest in the restricted quasisimplicial case. Its dated November 1999 update already reports a superlinear cubical construction. The historical page's informal theorem parameters should not replace the actual paper's weak inequalities. The packet correctly relies on the paper. Cubical facets have square ridges, so that witness does not establish a result in the quasisimplicial subclass.

## Joswig and Ziegler realization and the witness

[Neighborly cubical polytopes, arXiv:math/9812033v2](https://arxiv.org/abs/math/9812033v2), Theorem 16 on PDF page 11, provides a deformed combinatorial m-cube and a linear projection to a cubical d-polytope when m >= d >= 2r+2, preserving the r-skeleton. Taking d=4 and r=1 is permitted at equality and works for every integer m >= 4. The projection of a convex polytope is convex, and the theorem explicitly supplies dimension four and cubicality. A cube graph alone would not suffice to establish cubicality; here it is a separate theorem conclusion.

The paper's definitions on PDF page 3 make each three-dimensional facet a combinatorial cube. Its introduction on PDF page 2 independently states the resulting facet count. Publication metadata agrees with [Discrete & Computational Geometry 24, 325-344 (2000)](https://link.springer.com/article/10.1007/s004540010039).

The counting step can be checked without importing that stated count. Preserving the cube graph gives

- f_0 = 2^m
- f_1 = m 2^(m-1)

A cube has six square facets, and every ridge in the boundary of a convex 4-polytope belongs to exactly two facets. Hence 6f_3 = 2f_2. The boundary is a 3-sphere, with Euler characteristic zero, so

f_0 - f_1 + f_2 - f_3 = 0,

and consequently

f_3 = (f_1-f_0)/2 = (m-2)2^(m-2),   f_2 = 3f_3.

At m=10 these identities give (f_0,f_1,f_2,f_3) = (1024,5120,6144,2048). Every facet has eight vertices and is therefore degenerate. Thus D_4(1024) >= 2048 = 2(1024). More generally f_3/f_0 = (m-2)/4 is unbounded. The packet correctly makes no claim that 1024 is the globally smallest witness, or that this family has every possible vertex count.

## Nevo Santos and Wilson and convexity

[Many triangulated odd-spheres, arXiv:1408.3501v1](https://arxiv.org/abs/1408.3501v1) separates the quadratic sphere construction from the convex result. Construction 2 on PDF pages 13-14 specifies odd k and arbitrary positive integer l; the nontrivial instances used here have odd k >= 3 and l >= 1. Theorem 4.6 on page 14 provides a regular subdivision of 2kl+2+l^2 points with (2k-2)l^2 triangular-bipyramid cells. The regularity proof occupies pages 15-16. Corollary 4.8(1) on page 17 explicitly takes the convex hull of lifted points and states the convex 4-polytope conclusion. The theorem numbering being cited is that of this inspected preprint.

Regularity requires an appropriate placement of the points, rather than being asserted for every placement on the two lines. The proof chooses successive blocks along each line to be translated copies and centrally symmetric; it explicitly permits the equally spaced points a_i=(i,0,1) and b_j=(0,j,-1). Thus the necessary placement exists for the parameter choices used here.

Regularity is the essential bridge: a maximal three-dimensional regular-subdivision cell lifts affinely to a supporting facet of the four-dimensional convex hull. Affine lifting preserves the bipyramid's five-vertex combinatorial type. An arbitrary subdivision, or a sphere formed by a topological closing operation, would not supply this implication.

The count is a vertex count after lifting, not merely an unqualified count of input points. The original a_i and b_j lie on two opposite edges of their three-dimensional convex hull. Consequently none can be an interior vertex of a three-dimensional hole. The S-filling replacement preserves the boundary of each hole, as in Lemma 3.2 and Theorem 3.3 on PDF pages 7-9, and adds one center vertex per hole. Thus all 2kl+2 original vertices and all l^2 centers occur as subdivision vertices. In a regular subdivision, any vertex of a cell lifts to a vertex of the corresponding lower face; a vertex of a face is a vertex of the whole convex hull. This justifies the exact count 2kl+2+l^2. Even without this argument, the point count would be an upper bound on hull vertices, but that alone would not establish exact-N assertions.

Set k=l=s with s odd and s >= 3. The displayed counts become

N_s = 3s^2+2,   B_s = 2s^3-2s^2.

Dividing by N_s^(3/2) gives a limit of 2/(3 sqrt(3)) > 0. This independently verifies the exponent. The corollary itself gives, for each epsilon > 0 and all sufficiently large N, at least ((2-epsilon)/3^(3/2)) N^(3/2) bipyramidal facets. A triangular bipyramid has five vertices, so these are degenerate facets.

The all-N conclusion is stronger than an unbounded-subsequence statement and has a standard direct interpolation justification. Choose the largest odd s with N_s <= N. Consecutive admissible counts differ by N_(s+2)-N_s=12s+12, so at most O(s) extra vertices are needed. Add each new vertex just beyond one facet and beneath the other facet hyperplanes, close enough to the relative interior of that facet. This retains old vertices and all other old facets, replacing only the selected facet. At most one of the original counted bipyramids is lost per addition. The final N-vertex convex polytope therefore has at least B_s-O(s) such facets. Since N=N_s+O(s), the same positive leading constant, and hence the every-sufficiently-large-N Omega(N^(3/2)) bound, follows. This interpolation argument does not assert that all facets are bipyramids or simplices.

The [publisher record](https://link.springer.com/article/10.1007/s00208-015-1232-x) confirms the journal title Many triangulated odd-dimensional spheres, online publication on 30 May 2015, and volume 364 (2016), pages 737-762. Neither this audit nor the packet infers that every remaining facet is simplicial, or that the resulting entire polytope is quasisimplicial.

## Avvakumov and Hubard and the sphere distinction

[Cubulating the sphere with many facets, arXiv:2503.18047v1](https://arxiv.org/abs/2503.18047v1), dated 23 March 2025, states on PDF page 1 that for each fixed d >= 3 and every N >= 2^(d+1), a cubulation of the d-sphere exists with at most N vertices and at least c(d)N^(5/4) facets. These are topological cube complexes. The theorem does not assert that the constructed complexes are boundaries of convex polytopes. Its sphere dimension d=3 corresponds to the boundary dimension relevant here.

PDF page 2 identifies finding a subquadratic bound as a challenge even under convexity, in the cubical setting under discussion. This statement is context, not a proof that no subsequent result exists or that the general nonsimplicial-facet problem is currently open. REPORT.md respects that distinction. Prefer the explicit “at most N vertices and at least cN^(5/4) facets” wording to avoid suggesting an exact-vertex-count or matching Theta assertion.

## Independent upper bound proof

Let P be any full-dimensional convex 4-polytope on N >= 5 vertices, and let D be its number of nontetrahedral facets. Fix a total ordering of its vertices. Pull each face using the restriction of this same ordering. Pulling triangulations restrict to the pulling triangulations of subfaces, so the facet triangulations agree on their overlaps. They form a simplicial complex K with underlying space the entire boundary of P and with exactly the original N vertices. No extra vertices are introduced.

Every extreme vertex of an original facet must appear in a triangulation covering that facet with original vertices: an omitted extreme vertex cannot be a convex combination of the others. A triangulation consisting of one tetrahedron uses only four vertices. Therefore each nontetrahedral original facet contributes at least two tetrahedra. Tetrahedra in distinct original facets have disjoint relative interiors and are distinct maximal simplices of K. Writing t=f_3(K), it follows that 2D <= t.

Because K triangulates a closed 3-manifold, every triangle lies in exactly two tetrahedra. Counting incidences gives 4t = 2f_2(K), hence f_2(K)=2t. The Euler relation for the 3-sphere gives

N-f_1(K)+2t-t=0,

so t=f_1(K)-N. An abstract simplicial complex has at most one edge for each unordered pair of its vertices. Thus

t <= binomial(N,2)-N = N(N-3)/2.

Combining the inequalities and using integrality proves

D <= floor(N(N-3)/4).

Taking the maximum over P proves the claimed bound for D_4(N). No upper-bound theorem, simpliciality of P, or realization of an arbitrary abstract sphere is required. The proof makes no sharpness claim. Numerical enumeration of face-count identities is only an arithmetic diagnostic and is not a substitute for this argument.

## Acceptance boundaries and verification

The accepted mathematical output is a literature correction and a rigorous partial-bound result. It is not a resolution of the full extremal problem in dimension four or in all even dimensions. In particular, the verified lower and upper exponents are 3/2 and 2; a matching bound is not supplied. The full sharp maximum and the additional restricted quasisimplicial question remain undetermined by this packet.

The three inspected PDF hashes and byte counts match VERIFICATION_METADATA.json. Relevant text was independently extracted, and rendered pages were checked for Theorem 16, Theorem 4.6, Corollary 4.8, and Theorem 1.1. The arXiv abstract and submission-history pages inspected on the review date list math/9812033v2, 1408.3501v1, and 2503.18047v1 as their latest versions. Publisher pages independently confirm the two cited journal records. Independent exact arithmetic reconfirmed the cubical identities for m=4 through 100 and the m=10 witness. These checks do not independently certify the datasets, prior-work search, live catalog status, or repository history, which are outside this mathematical review.

No third-party source documents, extracted source passages, dataset contents, private sources, or private coordination material are included in this audit. The accompanying metadata contains only public source identification, hashes, byte counts, inspection locators, and authored verification outcomes.
