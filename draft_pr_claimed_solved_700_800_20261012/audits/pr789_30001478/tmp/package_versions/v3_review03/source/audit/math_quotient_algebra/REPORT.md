# Independent adversarial audit: direct quotient algebra for PR #789

UTC: 2026-10-16T16:16:52.165Z
Problem: 30001478 / OWR-4335-003.
Reviewed immutable head: aa44dec3baf8c1cd179cf8b55f32be95c74ee81a.
Verdict: **PASS; no required mathematical repairs.**
Completion estimate for this assigned mathematical audit: 100% (mathematical and custody checks complete).

## Independence and scope

Before reading the candidate or any earlier mathematical review, I read only the three authorized intake identity/eligibility records and froze INITIAL_POSITION.md at 2026-10-16T16:09:52.635348Z (SHA256 5ca5d89a9fb7f6743997f860f0dc45bd3a33329e5adee30475d8dfbaf90efa24). I independently found the scalar quotient sending all four generators to one polynomial variable. I then reconstructed the stronger two-generator projective-line quotient, froze PRE_CANDIDATE_PROJECTIVE_LINE.md at 16:11:31.369861Z (SHA256 5f7871583551f3c70d024545d946e16b37279218cd515c83698d17fd76b200bf), and only afterward received permission to inspect the original candidate. No root or peer mathematical report was read. The matching original quotient was not a premise of my initial construction.

After that freeze I read the original author proof, first mathematical audit and scope addendum, second mathematical review, operative verification wrapper, and relevant source metadata. I authenticated all 58 original artifacts by SHA256 and Git blob identifiers and replayed the original executable gates and suites. These custody/replay statements do not claim that every line of every ancillary file received substantive mathematical review.

I independently downloaded the official OWR report and arXiv1101.0737v2. I inspected extracted official source text, including the six-relation display and conjectures, and the preprint's corresponding introduction, Theorem 3.5 and parameter definitions. I make no fresh rendered-page-inspection claim here. The source-definition family separately assigned by the parent is independent; I did not contact it. Third-party PDFs and text bodies are kept only in the owned scratch directory and excluded from this authored packet. This assignment performs mathematical/source scope verification, not a priority audit.

## Exact result and hypotheses

Let k be any field and let alpha,beta in k satisfy beta squared unequal to 1. For the six literal homogeneous quadratic relations in the selected record, set

I=(x3-x1,x4-x2).

Then I is a nonzero homogeneous two-sided completely prime ideal, strictly contained in the augmentation ideal R_+, and

R/I = B(P^1_k,O(1),sigma),
sigma([s:t])=[s+beta*t:beta*s+t].

The quotient map is graded, unital, surjective, and has infinite-dimensional image of GK-dimension 2. The line bundle is sigma-ample. Thus the map is nontrivial even under the stronger requirement of a positive-dimensional target and image with GK-dimension at least 2. This applies to every field/parameter pair in the literal problem: algebraic independence of alpha,beta over the prime field implies beta squared unequal to 1. Uncountability and algebraic closure are allowed but unnecessary in this proof.

The stronger conclusion does not classify primes, identify all coordinate-ring maps, embed R in the target, provide equal graded quotient rings, or give a surface-dimensional image. Such conclusions are outside the verified theorem.

## Exact quotient, rather than relation evaluation alone

Let F=k<x1,x2,x3,x4> and L=(x3-x1,x4-x2). The quotient F/L is exactly the free algebra k<a,b>, through x1,x3 mapping to a and x2,x4 mapping to b. The six defining relations have images

0,0,0,0,g,g,
g=beta*a^2-a*b+b*a-beta*b^2.

Successive quotienting therefore proves R/I=k<a,b>/(g) exactly. It does not merely show that an unspecified quotient maps onto the proposed algebra. The first four relations vanish as noncommutative expressions, before any commutation is imposed, so the construction does not accidentally replace R by its commutativization.

## Independent tensor-ideal proof identifying the entire kernel

Write V=ka+kb and let T:V->V be the linear transformation T(a)=a+beta*b, T(b)=beta*a+b. Put D=1-beta^2, nonzero by hypothesis. The extension of T to the free algebra and to the ordinary polynomial algebra is an automorphism. For n>=0 define an invertible linear operator on V tensor n by

C_n(v1...vn)=v1 T(v2) T^2(v3)...T^(n-1)(vn).

Products on the right of this formula are free-algebra concatenations, not commutative products. Let c=ab-ba. Direct expansion gives C_2(g)=-D*c. Also, for every linear transformation T on a two-dimensional space, simultaneous substitution sends the alternating tensor c to det(T)*c; this identity is valid in characteristic 2 as well.

For arbitrary words u of length r and v of length s, n=r+2+s, we obtain

C_n(u*g*v) = -D^(r+1) C_r(u) * c * T^(r+2)(C_s(v)),

where the asterisks in this single identity denote concatenation in the free algebra. Since D is invertible, C_r and T^(r+2)C_s are invertible linear maps, and words span their tensor spaces, this identifies, onto, each subspace of relation placements at a fixed position. Summing over positions proves that C_n carries the entire degree-n component of the two-sided ideal (g) onto the degree-n component of (c). Thus it induces an isomorphism of graded vector spaces k<a,b>/(g) -> k[a,b].

This vector-space isomorphism also identifies multiplication. For homogeneous u of degree m and v of degree n,

C_(m+n)(uv)=C_m(u) T^m(C_n(v)).

Consequently the quotient algebra is exactly the graded twist P^T of P=k[a,b], whose multiplication is f star h=f T^m(h) for deg f=m. This gives a second proof of the author's complete-kernel conclusion, independent of its normal-form dimension comparison.

Associativity follows by expanding a triple product, and the identity is 1. Inhomogeneous domainhood follows from highest nonzero homogeneous components: f_m star h_n=f_m T^m(h_n) is nonzero because P is a domain and T is an automorphism. Every degree-n vector space has dimension n+1, so the Hilbert series is (1-z)^(-2), the generating-space growth through degree n is (n+1)(n+2)/2, and GK-dimension is2. The algebra is generated by its degree-one part because P_n T^n(P_1)=P_(n+1).

The author's shorter argument is also sound. Its change U=X-Y,V=Y is invertible without dividing by 2; the relation rewrites VU as a combination of UV and U^2, strictly decreasing a fixed-length lexicographic word order with V>U. The resulting U^i V^j words span, giving dim A_n<=n+1. The surjection to P^T gives the reverse inequality. Confluence is not assumed or needed by this dimension comparison. The separate Ore proof in the first review is consistent with the same result.

## Primeness and geometric target

The original relation ideal is generated in degree 2, so its degree-one component is zero and R_1 has basis x1,x2,x3,x4. Thus x3-x1 is nonzero in R, and I is nonzero. It is homogeneous and two-sided by definition. Its quotient is a nonzero domain, making I completely prime; this implies ordinary two-sided primeness and graded primeness. Since I lies in R_+ and x1 maps to the nonzero section s, I is proper and strictly smaller than R_+.

The nonsingular matrix [[1,beta],[beta,1]] induces the displayed projective automorphism sigma of P^1. Pullback on linear forms is T in the explicit chosen convention; no inverse is inserted. Pullbacks of O(1) are O(1), so the tensor product of the first n pulled-back line bundles is O(n). Its global sections are P_n and the THCR multiplication is f sigma^(m*)h=f T^m(h). With these identifications the graded twist is B(P^1,O(1),sigma). The usual sigma-ampleness criterion reduces to that for O(n) on P^1. There is no finite-dimensional image, point target, or augmentation ambiguity.

The optional surface-target embedding in the original second review is correct: degree-n sections f map to f tensor z^n in B(P^1 times P^1,O(1,1),sigma times id), for fixed nonzero z in H^0(O(1)) on the second factor. Its multiplication is compatible and its degree-n maps are injective. It still has image GK-dimension 2; no surface-dimensional-image claim follows from this optional observation.

## Boundaries, hidden assumptions, and falsification

* Algebraic independence gives D!=0 in every characteristic. It does not require replacing alpha or beta by finite-field elements. The proof uses no domain/noetherian theorem about R and no birational-dynamics classification.
* In characteristic 2, diagonalizing with a+b and a-b is invalid. The tensor proof remains valid. Alternatively put U=a+b,V=b. Then g=beta*U^2+(beta+1)(UV+VU), yielding an Ore/Jordan plane since beta+1!=0. The projective T may have finite order in characteristic 2, but finite order does not invalidate the twist-domain or Hilbert-series proofs.
* At beta=1 the relation factors (a+b)(a-b); at beta=-1 it factors -(a-b)(a+b). The nonzero linear factors survive, giving zero divisors. These parameters are excluded, and the stronger theorem is not extended to them. In characteristic 2 the two excluded values coincide; the factor is the square of a nonzero linear form.
* Replacing the target multiplication by ordinary commutative multiplication leaves beta(a^2-b^2), generically nonzero. Replacing T by its inverse adjugate lift produces2beta(a^2-b^2) before determinant division; this fails generically outside characteristic 2. In characteristic 2 that residual vanishes, as the inverse is projectively the same automorphism; it is not a valid characteristic 2 negative test. The independent checker records this limitation explicitly.
* The journal/preprint parameters c=(theta-1)/(theta+1),d=(rho-1)/(rho+1) are invertible fractional transformations in characteristic different from2. In characteristic 2 they collapse to1 when defined. Thus the present characteristic 2 theorem concerns the literal displayed algebra, not identification with the collapsing journal parameter family. The original first-audit addendum already states this necessary distinction correctly and should accompany any new paper.

## Source fidelity

The freshly retrieved official report's Theorem 3 on printed p. 1361 has all six literal relations, with the same signs and generator indices. The adjacent conjectural assertions on p. 1362 concern nontrivial graded prime ideals and nontrivial maps to THCRs. Neither printed assertion imposes injectivity, equal quotient rings, or minimum image dimension. The surrounding discussion does address stronger birational/embedding obstructions, which must not be conflated with the literal conjectures. arXiv1101.0737v2 repeats both assertions on preprint p. 4 and the corresponding presentation in Theorem 3.5 on p. 9, with the fractional parameter distinction above.

I do not infer that the conjectures remain open today merely because historical source texts contain them. Priority and later literature remain outside this mathematical verdict.

## Reproduction and evidence limits

check_algebra.py imports no author/prior-review code. Its arithmetic is exact over Z[alpha,beta] in a free algebra. It checks all six quotient images, the scalar quotient, the determinant/tensor relation and simultaneous-substitution identities, the division-free normal form, singular factorizations and convention counterchecks. It verifies 129 tensor-ideal-placement identities through degree 6 and 1364 explicit telescoping certificates for the scalar-kernel normal form. Six source-relation sign perturbations are all detected.

Five finite-field parameter choices, including both non-prime-field admissible beta values in GF(4), give45 field-degree cases through degree 8. Exact ranks of the full degree-n quadratic-relation ideal give quotient dimensions n+1. These computations are diagnostic checks, not a proof for transcendental parameters or all degrees. The universal proof is the tensor-ideal argument above.

REPLAY_RESULTS.json records independent mathematics and the original publication wrapper in normal/optimized Python 3.14.6 and3.12.14. The original wrapper replays its three frozen gates, 47/16/20 named suites and actual ephemeral path-patch test. The wrapper's complete 58-file custody scope and historical self-symlink caveat remain distinct: the wrapper, rather than a frozen old self-resolving verifier, is the operative publication entrypoint.

The sealed packet checker requires externally supplied checker/manifest hashes, closes its file and directory inventories, rejects links/nonregular entries, authenticates 62 intake inputs including58 original files with Git blob/SHA256 checks, and recomputes the exact selected statement/full-review hashes. Optional primary-body rehashing uses the four current scratch PDF/text files. Its normal core replay does not require downloaded external bodies. All 18 disposable custody controls passed: two positive modes and 16 rejection controls, including nonregular files, symlinks/hardlinks, rehashed input/head mutations, unsafe paths, duplicate keys and nonfinite JSON. The harness uses the owned ordinary audit parent because the macOS default temporary directory has a symlink ancestor, correctly rejected by the verifier. This is ordinary local integrity and replay, not a formal proof or protection against arbitrary concurrent filesystem races.

## Final mathematical disposition

No required correction, unresolved mathematical gap, hidden characteristic restriction for the direct presentation, or counterexample to the claimed quotient was found. The exact literal two assertions are refuted by a positive-dimensional THCR quotient with a nonzero proper completely prime homogeneous nonaugmentation kernel. Preserve the characteristic 2 parameter-scope qualification and the absence of novelty/current-open/firstness claims. Proceed to an independent priority audit before promoting any result as a novel solution.
