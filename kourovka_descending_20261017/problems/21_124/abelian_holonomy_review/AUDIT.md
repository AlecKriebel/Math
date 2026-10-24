# Fresh adversarial audit: Pell candidate and finite abelian holonomy

UTC: 2026-10-24T22:31:00Z. **Verdict: PASS for the stated partial obstruction.** There are no outstanding substantive mathematical objections to the frozen `ABELIAN_HOLONOMY_DELTA.md` hash `33950bfa915b7de499f98a9bc0470d3dd5e825b0f8f7ba2a6d638bc83da7ef06`. This is neither a solution of 21.124 nor an originality certificate. Audit completion estimate: **100%**. The discovery estimate for the full problem is not being revised by this reviewer.

I did not author the candidate, delta, or author checker. I read the workspace policy and the exact candidate and delta, wrote a separate checker, and did not change author files. The original theta/CAT(0)/free-by-cyclic eligibility package has a different reviewer; the present verdict concerns the new abelian-holonomy deduction from the displayed presentation. No external communication or git operation occurred.

## Exact claim and representation scope

Let G have the presentation in `PELL_CANDIDATE.md`, with pairs (3,2), (20,14), (119,84). For every homomorphism from G to a finite-dimensional real Euclidean-by-finite group whose finite linear image is abelian, the images of a and b have finite order. In particular, such a homomorphism cannot be injective on either of the displayed rank-two vertex groups. No bound on the Euclidean dimension or on the exponent of the finite abelian group is imposed.

The power argument does not assume that the original images of a, b, t are translations. Choose a positive M divisible by the orders of their linear parts. Then their Mth powers are translations, with vectors A, B, T. Because [a,t]=[b,t]=1 in G,

    (a^p t)^M = a^(pM) t^M,

and likewise on the b side. Conjugation of a pure translation by an affine isometry (v,S) changes its vector by S; the affine displacement v cancels. Thus the original relations really imply

    S_i(p_i A+T) = q_i B+T.

This verifies the scope in the presence of arbitrary affine cocycles and vertex rotational parts. Finite abelian linear image makes the S_i commuting finite-order complex-linear operators, so simultaneous diagonalization after complexification is legitimate. Orthogonality is more than is needed here; any finite linear action can in any case be made orthogonal by averaging an inner product.

On a simultaneous eigenspace, use x,y,z for the eigenvalues of S_1^-1,S_2^-1,S_3^-1. Multiplying by S_i^-1 gives exactly the rows `[p_i, -lambda_i q_i, 1-lambda_i]`, rather than their uninverted convention. These eigenvalues are roots of unity. No decomposition of the vertex translations as real one-dimensional characters is assumed; complexification covers nonreal characters and arbitrary multiplicities.

The independent checker expands the determinant from the six signed permutations of its three columns, without importing the author's polynomial. It reproduces

    det/2 = -99x+812y-714z-714xy+820xz-105yz.

At x=y=z=1, the first two equations have 2-by-2 determinant -2 in A,B, so these components vanish even though T can survive. At every other character triple the full determinant is nonzero once the torsion-zero assertion below is proved. Hence A=B=0 in all character spaces. A zero translation vector together with the already killed linear part means that the images of a^M,b^M are the identity. This is an actual finite-order obstruction, not merely a failure of discreteness.

## Arbitrary root orders, minimal subsums, and monomial lattices

I checked the stated elementary proof of the needed Mann bound, including its use of relative orders rather than absolute orders. After dividing a minimal rational relation by one of its roots, let N be the least common multiple of the remaining root orders. For p^e exactly dividing N and e>=2, the extension over Q(zeta_(N/p)) has degree p; the p residue classes of the p-primary exponent are therefore linearly independent. Each nonempty class would be a vanishing subsum. Minimality forces a single class, which must be class zero because the normalized first term is 1, contradicting the definition of N. Thus N is squarefree.

For squarefree N and p|N the corresponding degree is p-1, and the sole dependence among 1,zeta_p,...,zeta_p^(p-1) is their sum. If p exceeds the number k of terms, a residue class is empty. All grouped coefficients must then be zero. Minimality again leaves one class and removes p from N, a contradiction. The normalized N consequently divides the product of primes <=k. This also covers p=2: the relevant degree is 1. There is no assumption that k is the sum of coefficient magnitudes; k is the number of nonzero rational-coefficient terms.

A vanishing six-term relation can always be partitioned recursively into minimal vanishing subsums. Singletons are impossible. A pair requires equal absolute coefficient magnitudes, so the only possible pair is the two 714 terms. For a three-term subsum, Mann gives relative phases in mu_6. I did not rely solely on the prose classification of six directions: `independent_check.py` tests every coefficient triple and every pair of relative sixth-root phases in the exact basis 1,zeta_6. It finds no zero. This handles both unequal signed collinear lengths and noncollinear cases.

The independent checker also visits all 203 set partitions of the six indices. After excluding singletons, triples and unequal-magnitude pairs, only the full six-block or the 714 pair plus its four-block complement remains. Thus no minimal-partition type is omitted.

For the full six-block, Mann controls all monomial ratios by mu_30. The exponent differences between x and xy, between x and xz, and between y and xy are respectively `(0,-1,0)`, `(0,0,-1)`, `(-1,0,0)`. They form a unimodular basis. Hence x,y,z themselves lie in mu_30. This explicitly rules out a hidden positive-dimensional translated subtorus or a larger monomial-lattice index in this case.

For the other partition, the two negative 714 terms require z=-xy, with the minus sign retained. Ratios in the four-block give z and x/y in mu_6. The pair relation gives xy in mu_6 as well. Consequently x^2 and y^2 lie in mu_6, whence x,y lie in mu_12 and z lies in mu_6. The possible index two has therefore been accounted for. Both alternatives are contained in mu_60^3. No unsupported upgrade from bounded orders to arbitrary orders remains.

## Independent exact computation and reproduction

The author's checker uses the degree-16 Phi_60 quotient. I independently used the tensor basis u^i v^j (0<=i,j<4), with Phi_12(u)=u^4-u^2+1 and Phi_5(v)=v^4+v^3+v^2+v+1. Here w=uv is primitive of order 60: its exponent relative to standard zeta_60 is 17, coprime to 60. Moreover Q(u,v)=Q(w), of degree phi(60)=16, so the 16 tensor coordinates are independent. This avoids reusing the author's cyclotomic polynomial reduction.

The separate integer computation checks all 216,000 triples and finds the unique zero exponent triple (0,0,0). It also derives the determinant and verifies the small-relation/partition arithmetic described above. Results are preserved in `independent_results.json`; there is no floating-point root test. Running

    python3 independent_check.py

from this folder reproduces it using only the standard library. The measured original run took approximately 1.27 seconds.

I additionally imported the author's `run()` function without executing its certificate-writing main block. Every non-timestamp field matched the frozen author certificate. The independent rerun output is preserved separately as `author_rerun.json`; no author certificate was overwritten.

## Primary-source and presentation checks

Mann's original article metadata is verified at the [publisher](https://www.cambridge.org/core/journals/mathematika/article/abs/on-linear-relations-between-roots-of-unity/346C7FE8D77A7D987662F7310265271D): H. B. Mann, *On linear relations between roots of unity*, Mathematika 12(2) (1965), 107–117, [DOI 10.1112/S0025579300005210](https://doi.org/10.1112/S0025579300005210). The publisher extract alone does not expose the theorem. The theorem's exact rational-coefficient nondegenerate scope is independently corroborated, with its cyclotomic proof mechanism, in Jan-Hendrik Evertse's primary research paper [*The number of solutions of linear equations in roots of unity*, Section 2, pp. 3–4](https://pub.math.leidenuniv.nl/~evertsejh/98-roots.pdf). The delta includes its own proof, so inaccessible pages of Mann are not treated as evidence for an unstated stronger theorem. No priority claim for the Pell obstruction has been established by this audit.

There is one nonblocking editorial defect in the author checker comment: “Minimal three-term rational root-of-unity relations require equal magnitudes” is false without the noncollinearity qualification. The relation 1+1-2=0 is minimal and collinear. The written proof and the executable condition correctly include the alternative that one magnitude is the sum of the other two, so this comment does not change the computation or result. Suggested correction: “A three-term relation in mu_6 has equal magnitudes or one magnitude equal to the sum of the other two.”

## Unresolved scope

The proof also works if merely the three stable-letter linear parts commute and have finite order, even if an ambient finite linear group is larger. It supplies no obstruction when those three parts fail to commute. Independent complex eigenspaces then need not exist, and the scalar determinant reduction cannot be used. No inference is made from bounded permutation searches to arbitrary nonabelian finite holonomy, or from this partial obstruction to failure of virtual specialness. The full candidate remains unresolved and must not be promoted to `solved_verified` or published as a solution of 21.124 on this evidence.
