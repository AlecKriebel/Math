# Independent review: 11000192, pseudo-Anosov dynamics

**Verdict: PASS_SCOPED_PARTIALS_WITH_CURRENT_SOURCE_CORRECTION. Original target remains unsolved after five substantive author turns.** No mathematical revision to the frozen five-turn proofs is required. The additive withdrawal/prior-credit notice is mandatory context for this verdict.

## 1. Exact binding and current source status

This review binds `FROZEN_MANIFEST.json`, SHA-256 `f1e0be7ccf538e8b52a5eefbcaa3cf9a2095edfeeffa3b429494f95e5389e0ac`, and its 42 entries. The original 39-entry manifest, SHA-256 `1ca24a6704b3637859a23b276ff844b87d736d65f6e180788707d20cebc73f22`, is preserved in `source_status_history/FROZEN_MANIFEST_before_withdrawal_note.json`. Every original entry remains unchanged. `RESULT.md` has SHA-256 `3d838f68aa8afeb9cc8faa853a756c5b78efa8f211775541d34ee361dd2c1f85` and `TURN_5.md` has SHA-256 `71b98802441957371c393faca35ddaf8f4f713d7e95af99c8c28ffbd71f13c2e`.

The live [arXiv record](https://arxiv.org/abs/2505.08105), independently read on 1 October 2026, identifies the manuscript as withdrawn in v2 on 28 September 2026. Its author states: “This manuscript has been withdrawn due to a mistake in Theorem 3.1”. The v1 PDF is a historical input, not a currently maintained affirmative theorem. The public framing must retain `SOURCE_STATUS_2026-10-01.md` (SHA-256 `39170f7117d1a0c2a5ecdb9bfad4a8d080b095a37d789e81ac8d6dc6344fe32e`) and the new README. The withdrawal predates this attempt. Neither this review nor the packet claims to have discovered the withdrawal's reason or to have disproved the broad existence assertion.

Direct earlier credit also matters: Saadi 2404.00372v2, p. 2, explicitly attributes the obstruction to invariant polynomial functions to a discussion with Julien Marché using Charles–Marché. Turn 3's finite-support consequence is therefore a credited known observation. No historical novelty is certified here.

The exact original target is Goldman's Problem 2.5, printed p. 211 in the book, or Problem 2.8 in the standalone chapter: an example of a pseudo-Anosov mapping class of a closed surface whose action on the full SU(2) character variety is not ergodic for Goldman measure. A relative punctured-torus example, a representation-space invariant, or a null-dimensional embedded family does not answer that target.

## 2. Independence and validation

The reviewer did not contribute to the five-turn author route. I read all five frozen proofs, the relevant complete primary inputs and source figures, checked the geometry and analytical deductions below, and replayed the author programs in a separate directory. All ten PDF hashes, all five historical checkpoint manifests, and the frozen author hashes match. All five author outputs reproduce byte-for-byte: 268 + 236 + 14,022 + 725 + 89 = **15,340 grouped controls**.

Two independently written programs import no author checker:

- `independent_geometry.py` derives source-word relations, provides explicit surface-relator reduction traces for the based chain identity on every generator, checks the origami gluing and dihedral monodromy, and tests the nongauged quaternion identity using exact rational arithmetic.
- `independent_cohomology.py` derives adjoints directly from quaternion multiplication, rewrites Schreier generators, constructs an actual basis of the cocycle kernel modulo conjugations, and calculates the resulting 6-by-6 cohomology action. It independently reconstructs the relative tangent plane and its exact intertwining. This is a distinct verification from extracting the answer by division of raw characteristic polynomials.

The receipts give their exact grouped counts and scopes. Finite controls supplement, and do not replace, the written surface, multicurve, KAM, measure, and covering arguments. Replay commands are given in the source/scope note. No numerical spectrum is used in the verdict.

## 3. Turns 1 and 2: source geometry and based lifts

The source's Figure 3 and the four-square relations match the frozen labeling. Horizontal permutation (1)(23)(4) and vertical permutation (12)(34) give two vertex classes and Euler characteristic -2. The a1 and a4 edge interiors are distinct and their endpoints are the two different vertex classes. Their two-edge cycle is consequently an embedded circle, rather than a curve declared simple from its homology alone.

Both exact quaternion families satisfy all four square relations. The first gives irreducible nonconstant angle values 9/25 and 25/169; the second gives 1/100 at the stated parameter. The supplied singular denominator examples do not endow the original quotient with values there. Analytic nonzero denominators on the connected irreducible locus have null zero sets, and the countable orbit union permits the asserted conull invariant domain. Full support and density are used only as stated.

The displayed source word is a three-chain construction. The commuting and adjacent-intersection calculations, including the DE² braid identity, give intersections 0,1,1 for c,r,d, with c and r noncoincident. Their regular neighborhood has essential boundary in the closed genus-two surface; its twist subgroup is reducible. This diagnoses that displayed construction and does not infer that arbitrary intersections of unbased subgroups have the same property.

I independently used the ordered based generators (a,d,b,z), with relator a^-1 b^-1 a d b z d^-1 z^-1, to verify all five lifts preserve the surface relation. For Q=(ABC)^4, the equality Q=Ad_(z^-1) E² holds on every generator. The independent receipt records exact relation replacements; it uses no assumption that the reduction procedure is a complete word-problem algorithm.

The Turn 2 sufficient criterion respects composition and precomposition conventions. From Q=Ad_(z^-1)E² and fixed z, its conjugated word lies in the two stipulated *based* subgroups when the precise hz^k fixing hypothesis holds. The line functions transform with Ad_(rho(h)^-1) in the required order. The failed naive power tests remain tests of specified words, not universal nonexistence arguments. The h=a specialization stays in the reducible subgroup indicated by the proof.

## 4. Turn 3: exact function and stabilizer

The nongauged quaternion calculation is valid. With delta=A2-A3, V=A4 delta, P=A1 delta, A=A1 A4^-1 and b=B1, the square relations imply V and P are imaginary, P is perpendicular to Im(b), and P=AV. Thus Pb=b^-1P and VP=-|delta|² A^-1. The unsquared numerator equals |delta|² Re(A^-1b²), so the source angle is

F = (tr rho(q))² / 4,   q=(a1 a4^-1)^-1 b1²,

where defined. The trace-square formula is its regular extension, not a claim that the original denominator never vanishes.

The embedded a=a1 a4^-1 cycle is essential and nonseparating: the indicated integral cellular cochain is closed and pairs to 1. The actual twist action A(a)=b1 a, A(b1)=b1 gives q=(A^-2(a))^-1, proving q simple geometrically.

The published Charles–Marché multicurve theorem applies to SU(2), permits parallel components, and gives linear independence of the relevant functions. The function 4F is that of two parallel copies of q. It is not the trace of a twice-traversed q. Equality under a mapping class therefore forces preservation of the unoriented isotopy class q. Conversely that preservation fixes F. The exact stabilizer equality is justified. Almost-everywhere preservation extends by continuity and full support on the smooth irreducible locus, then density. No element of this stabilizer is pseudo-Anosov.

The separate finite-trace-algebra consequence uses a unique finite multicurve expansion: a nonempty finite support invariant under a pseudo-Anosov would contain an essential curve with finite orbit. This consequence is valid and already credited in the earlier source as noted above. It does not prove that every measurable or arbitrary rational invariant is constant, nor does it imply ergodicity.

## 5. Turn 4: genuine branched-cover pseudo-Anosov, relative stability only

The automorphism phi(a)=ab, phi(b)=bab fixes the commutator exactly and induces the stated hyperbolic torus matrix. The character map T and Fricke invariant agree with that convention. The chosen negative root of X^4-3X^3+2X²+2X-1, with eta=xi/(xi-1), supplies an actual irreducible SU(2) representation. Its vector Gram minor is 3/4 and its commutator trace is -1. The relative tangent multiplier has trace 2-sqrt(13) and determinant 1.

Non-root-of-unity is proved using the conjugate 2+sqrt(13), not by numerical rotation. The Baker–Wüstholz argument controls q log(alpha)-2p log(-1), hence the argument's Diophantine and Brjuno property. It does not confuse an algebraic multiplier with an algebraic angle. The cited real-analytic, area-preserving two-dimensional Rüssmann result has the required stability conclusion without silently assuming a nonzero first Birkhoff coefficient. It applies here to the relative smooth character surface. A power remains stable on that relative surface.

For each odd n, the shift/reflection dihedral monodromy gives one boundary component and genus (n+1)/2 after capping. Its period-three cycle under phi is an identity in the infinite dihedral group, so phi³ lifts. The pulled-back measured foliations have the required branch prongs and expanding factor; this gives a genuine closed-surface pseudo-Anosov, including genus two when n=3.

At n=3 the SU(2) commutator itself satisfies C³=I by its trace and Cayley–Hamilton, not just Ad(C)³=I. The representation extends over the cap. The dense-image proof, finite-index restriction argument, transfer/injection and relative symplectic calculation support the immersed two-dimensional family. Right-sheet and left-permutation conventions define the same stabilizer subgroup; they are not silently mixed. The resulting relative family has zero Goldman measure inside the six-dimensional smooth closed-surface character space. Its relative stable neighborhoods cannot establish the requested ambient nonergodicity. Countable unions in the stated extension have the same measure limitation.

The abandoned factoriality route remains correctly abandoned. The cited Q-factorial/local-factorial results do not supply a global UFD or the needed control of arbitrary invariant rational quotients.

## 6. Turn 5: direct full tangent reconstruction

I independently reconstructed the four Schreier generators, the capped relator, both directions of the free cover automorphism, actual quaternion adjoints and intertwiner. The scalar parts agree as SU(2) elements; an adjoint-only sign ambiguity is not used. Normalization by O^-3 is consistent with the fixed-character action.

For left logarithmic cocycles the relation matrix D and conjugation matrix B have rank 3, DB=0, and the normalized word derivative L satisfies the two stated chain identities. Rather than only dividing characteristic polynomials, I formed a basis of ker(D) beginning with im(B), solved the induced action, and took its six-dimensional quotient. I also computed the relative trace constraint, the two-dimensional quotient of its kernel, and its restriction into the capped surface cohomology. That inclusion has rank 2 and intertwines the full quotient action with the cube of the relative action.

The transverse factor is exactly

N(t)=t^4 - ((53-5sqrt(13))/2)t³ + ((705-163sqrt(13))/2)t² - ((53-5sqrt(13))/2)t + 1.

Writing r=t+t^-1 gives a quadratic whose discriminant is positive, vertex is greater than 2, and value at 2 is positive. Exact rational bounds on sqrt(13) imply both roots r exceed 2. Thus all four normal eigenvalues are positive real, off the unit circle, in two reciprocal pairs. The relative cubed trace is 80-22sqrt(13), strictly between -2 and 2.

The relative elliptic plane therefore lies at a genuine ambient saddle, with two expanding and two contracting normal directions. The strong unstable manifold rules out Lyapunov stability of this point in the full six-dimensional space. This does not prove ergodicity of the mapping class, exclude some other nonergodic mechanism, or settle the original problem.

## 7. Disposition and required scope

The five-turn partial results and explicit limitations pass. The original target remains **unsolved 5/5**. There is no full nonergodicity example in the packet and no global ergodicity theorem. The historical source analysis must be presented together with the already-issued withdrawal and direct Marché credit. Source status checks establish the status of the named versions, not literature-wide openness.

Historical progress percentages, if retained in author logs, are subjective checkpoint estimates, not calibrated probabilities or evidence. They play no role in the verdict. No novelty claim is certified. Publication remains subject to the campaign's separate authorization gate.
