# Independent adversarial audit: problem 30006060

## Verdict and scope

**PASS for all retained scoped mathematical conclusions. Mandatory verifier hardening is supplied and tested separately. The smooth-concordance question remains UNSOLVED, 5/5 approaches.**

This review was conducted independently of the author investigation. It inspected the exact frozen proof, source record, results and executable; checked the original scholarly statements and geometric conventions; reconstructed the matrices from the displayed words; and wrote a separate exact-arithmetic implementation. It is an independent computational/mathematical review, not human peer review or a claim of novelty.

The author archive SHA-256 is `5afa68a626f8d999ef63d646b2757ffe910fc9858d672ee9f3bc2228e8d4cc48`; its manifest SHA-256 is `42ba7eb94cb501338e4c600eeb65bc89f173d6f34ee74a780c924085e4618b67`. Every manifest entry and the original archive were verified. They were not edited.

The exact inputs, with positive Artin generators and coherent braid orientations, are

- K = closure of a^3 b^3 a^6 b^6;
- J = closure of a^3 b^5 a^3 b^7;
- a = sigma_1, b = sigma_2; D = K # -J, where -J is the concordance inverse.

The reported pair was visually checked on printed page 2545 of [Oberwolfach Report 43/2024](https://ems.press/content/serial-article-files/50050). Its surrounding contribution, printed pages 2543–2546, explicitly uses smooth oriented concordance. The report gives the pair as an unresolved example, not an affirmative concordance. The supplied catalog and underlying problem identify the same words. No crossing-minimality assertion follows merely from the eighteen letters.

## 1. Geometry before matrix arithmetic

The matrix is not accepted merely because its Alexander polynomial happens to agree with the Burau answer.

Apply the braid version of the Seifert construction: three disks, eighteen positive bands. The resulting surface retracts to the graph with three vertices and one edge for each band. Between consecutive bands joining the same two disks, take the closed rectangle curve on the surface. These curves give an integral homology basis: on the retract, they are successive differences of parallel edges. For either family of parallel edges, their change of basis to differences with its first edge is integral triangular with diagonal entries one. The first edge of each generator supplies a spanning tree connecting the three vertices. Thus the sixteen curves generate the entire integral cycle lattice, not just a rational subspace.

The independent program first lists consecutive band endpoints in chronological order and applies the geometric push-off cases. Only after computing every entry does it reindex by generator, to compare with the author's A-then-B basis.

The corrected [Collins Seifert-matrix paper](https://webhomes.maths.ed.ac.uk/~v1ranick/julia/SeifertMatrix.pdf), Sections 3.1–3.3, supplies the local linking calculation. Its displayed diagrams on pages 11–12 were inspected visually. In its convention each positive rectangle has self-linking -1. Two successive rectangles in one column give the lower-triangular entry +1. An a-rectangle and later-starting b-rectangle have an upper-triangular +1 exactly when their endpoint intervals interleave. Nested or disjoint intervals contribute zero. The reverse ordering is irrelevant to the unique cross-column interaction here. A transposed global definition of the Seifert pairing would not affect any conclusion in this audit.

For K the a-band positions are 1,2,3,7,8,9,10,11,12 and the b-band positions are 4,5,6,13,14,15,16,17,18. The unique cross-column interleaving is (3,7) with (6,13): these are A_3 and B_3. There are eight curves in each column.

For J the a-band positions are 1,2,3,9,10,11 and the b-band positions are 4,5,6,7,8,12,13,14,15,16,17,18. The unique interleaving is (3,9) with (8,12): these are A_3 and B_5. There are five a-curves and eleven b-curves.

Every other pair is adjacent in one column, nested, or disjoint. Consequently the exact displayed author matrices are geometrically valid. Their symmetrizations are minus the matrices S = 2I-C of the two stated trees. [Baader's brick-diagram discussion](https://ems.press/content/serial-article-files/44257?nt=1), Section 2, independently corroborates the underlying linking graph. Baader uses the opposite overall signature sign; that does not change the graph. The independent verifier calibrates the convention on the positive trefoil represented as the positive stabilization 1112, producing V = [[-1,0],[1,-1]] and signature -2.

This geometric argument is the load-bearing link between the actual knots and all later matrix computations. Integer identities alone would not establish it.

## 2. Alexander polynomial, genus and signature functions

Both braid permutations are three-cycles, so both closures have one component. The connected canonical surface has Euler characteristic 3-18 = -15 and genus eight.

The independent implementation uses integer Burau evaluations, fraction-free determinants, and finite polynomial identity checking with explicit degree bounds. In particular, det(I-rho(beta)) has degree at most 18, so agreement with (1+t+t^2)P(t) at nineteen distinct integers proves that polynomial identity. Separately, det(V-tV^T) has degree at most sixteen, so seventeen evaluations suffice. These are exact polynomial identities, not numerical sampling on the unit circle.

In ascending degree order the shared P has coefficients

[1,-1,-1,6,-13,21,-29,35,-37,35,-29,21,-13,6,-1,-1,1].

Thus Delta(t)=t^(-8)P(t), P(1)=1, P(-1)=-243, and the degree bound proves that both genera are exactly eight. Their determinants are 243 and their Arf invariants are one. The Fox–Milnor norm condition on D passes because the two symmetric Alexander polynomials agree. This does not prove algebraic concordance.

For the adjacency matrices, the audit computes the characteristic polynomial using traces and Newton identities, independently of the author's matching recurrence. It also enumerates all 2^15 edge subsets in each graph. Both methods agree with the author's matching counts

[1,15,89,269,443,393,172,29,1].

The common characteristic polynomial, in ascending degree order, is

[1,0,-29,0,172,0,-393,0,443,0,-269,0,89,0,-15,0,1].

These are symmetric real matrices, so identical characteristic polynomials imply identical real spectra, including all multiplicities.

Here is the argument covering the whole circle. For omega different from one let d=|1-omega|>0. In H=(1-omega)V+(1-conjugate(omega))V^T, each diagonal entry is -d^2 and each tree-edge entry has modulus d. Set a unit phase at a root. Once the parent's phase is fixed, there is a unique child phase making that conjugated edge entry the positive real number d. Since a tree has no cycles, all these choices are compatible. Hence H is unitarily conjugate to dC-d^2I. Its eigenvalues are d(lambda-d), with lambda the adjacency eigenvalues.

The two H matrices therefore have identical spectra for every omega different from one, not just matching signatures. This proves equality of signature and nullity also at singular parameters. At omega=1 the two chosen sixteen-dimensional matrix families are both zero; their matrix nullities are sixteen. This last endpoint is a convention for these matrix families, not a claim that matrix-size nullity at one is invariant under stabilization of arbitrary Seifert matrices. On the usual domain S^1 minus {1}, the knot signature/nullity functions agree without this convention issue.

Leading-principal-minor signs independently verify inertia(S)=(15,1,0), so the chosen ordinary knot signatures are -14. The nullity there is zero. [Conway's survey](https://arxiv.org/abs/1903.04477), Section 2.4, confirms the needed caution: raw values at arbitrary Alexander roots are not universally concordance invariants. Equality here is stronger than what the legitimate signature obstructions require; it gives no missing obstruction.

## 3. Branched covers and the metabolizer

The standard branched-cover presentation by V+V^T identifies its cokernel with that of S; the linking form is represented by S inverse modulo integers, up to a common global orientation sign. This global sign has no effect on whether the difference form is metabolic.

An independently implemented integer row/column Euclidean algorithm gives the complete Smith diagonals:

- K: fourteen entries 1, followed by 9,27;
- J: fourteen entries 1, followed by 3,81.

In particular, the homology groups are not isomorphic: their exponents are respectively 27 and 81. This establishes non-isotopy. It does not establish non-concordance.

Exact rational inversion separately reproduces the author's proposed cyclic generators and their orders. With zero-based indices, take x=e_0 and y=e_8-20e_0 for K; take x'=e_0 and y'=e_3-29e_0 for J. The resulting orthogonal diagonal pairings are (16/27,5/9) and (50/81,1/3). Enumerating their generated classes gives all 243 elements in each cokernel, so this is a full group decomposition, not a pairing on an unverified subgroup.

The difference pairing has cyclic orders (27,9,81,3) and diagonal (16/27,5/9,-50/81,-1/3). The proposed generators

(3,0,0,1), (0,3,0,0), (0,0,9,0)

have integral self-pairings 5,5,-50 and zero mutual pairings. Their orders are 9,3,9 and they are independent, yielding 243 elements. The audit additionally enumerates every one of the 59,049 elements of the ambient group and tests orthogonality to all three generators. The orthogonal complement is exactly this subgroup. Thus the claimed metabolizer is valid.

Neither the group decomposition nor this metabolizer proves rational homology cobordism of the covers, algebraic sliceness of D, or vanishing of Casson–Gordon/Floer correction-term obstructions.

## 4. Smooth invariants and theorem hypotheses

Positive braids are fibered and strongly quasipositive. The relevant equality tau=g_4=g is applicable, giving tau=8 on both inputs. [Rasmussen's positive-knot theorem](https://arxiv.org/abs/math/0402131), Theorem 4 and Section 5.2, gives s=16. These are smooth statements.

[Truöl's version 2](https://arxiv.org/abs/2108.03674v2), Proposition 3.2(C) and Lemma 4.11, was checked against the actual hypotheses. Both words have ell=0 and r=2, every exponent is at least two, the final b exponent is at least three, and the first a exponent is at least three. The closures are knots. The formula gives v=Upsilon(1)=-18/2+2=-7. Her corollary then yields minimal block-pair number 8-7+1=2.

The [Ozsváth–Stipsicz–Szabó paper](https://arxiv.org/abs/1407.1795v3) supplies the initial Upsilon slope -tau, its quasi-alternating signature formula, and the L-space Alexander-polynomial restriction. The coefficient -37 excludes L-space knots. A quasi-alternating input would have Upsilon slope sigma/2=-7, contradicting -tau=-8; hence neither input is quasi-alternating. No full Upsilon function follows from this argument.

[Cheng–Hedden version 2](https://arxiv.org/abs/2504.13005v2), dated July 14, 2026, concerns next-to-top Floer information; its theorem is not a complete filtered complex computation for this pair. [Borodzik–Truöl version 3](https://arxiv.org/abs/2504.04894v3), Proposition 1.3 and Question 1.5, explicitly separates its nonfibered concordant examples from the fibered situation. Neither source supplies a resolution of the target.

## 5. Actual six-saddle cobordism and Baker's restriction

The stated exponent movie is

(3,3,6,6), (3,3,5,6), (3,3,4,6), (3,3,3,6), (3,4,3,6), (3,5,3,6), (3,5,3,7).

For each transition the audit finds an actual letter position whose deletion produces the shorter word; the insertion steps reverse that local operation. Smoothing a crossing in a coherently oriented braid is an oriented band surgery. Its trace is an embedded oriented saddle. Reversing this trace remains a saddle, not a local maximum or minimum. Taking separate time intervals and sufficiently small crossing neighborhoods therefore realizes these transitions by an embedded oriented surface in S^3 x [0,1].

The intermediate level component counts are 1,2,1,2,3,2,1. They must not be mistaken for disconnectedness of the total surface. Start with a connected cylinder and attach one-handles to its boundary in succession. No handle attachment can disconnect that surface, and no birth introduces a separate component. There are no births or deaths. The final surface has two boundary components and Euler characteristic -6, hence genus three. Thus g_4(D)<=3 is justified. There is no asserted positive lower bound.

The independent longest-common-subsequence calculation also reproduces 15 after all cyclic rotations and generator swaps. This only proves optimality within that restricted literal-word deletion/insertion search. It says nothing about arbitrary braid equivalences, stabilizations, or other surfaces.

[Baker's revised paper](https://arxiv.org/abs/1409.7646), Lemma 2 and Theorem 3, was read with its proof. Fibered strong quasipositivity implies the tight-fibered hypothesis. Lemma 2 gives minimality among fibered knots under homotopy-ribbon concordance, excluding either direction between these distinct inputs. Theorem 3 excludes ribbonness of D. Its conclusion does not exclude a smooth slice disk. Consequently an annulus between K and J, if one exists, would produce a Slice–Ribbon counterexample. The genus-three movie does not produce such an annulus.

## 6. Required correction, controls and acceptance boundary

The author checker is implemented using `assert b`. Python optimization removes this check while leaving its reported counter and output intact. The audit replaced the expected symmetrized determinant -243 by the false value -242 in a temporary copy. Normal execution rejected it; `python -O` exited successfully and emitted the original results byte-for-byte. This is a genuine false-positive verification mode, not a mathematical error in the unmodified results.

`VERIFY_HARDENING.patch` and `corrections/verify.py` replace that assertion with an explicit conditional raise. The patched code produces exactly the original results in normal and optimized modes and rejects the same corruption in both. Keep the author freeze unchanged; apply this correction to any derivative working copy used as a verifier.

The independently authored `independent_verify.py` uses explicit exceptions throughout. Its 163 checks and all 20 subprocess controls pass. Both normal and optimized executions replay identically after relocation. Wrong polynomial, word, geometric cross-edge, metabolizer, and movie mutations are rejected in both modes. Arithmetic checks support the written proof and do not substitute for the geometric or cited theorem arguments.

Accepted outcome: identical Alexander and full signature/nullity data; equal listed smooth homomorphisms; different branched-cover groups with a metabolic difference pairing; a genus-three upper bound; and a ribbon/homotopy-ribbon obstruction. No stronger concordance verdict, algebraic-concordance verdict, novelty claim, or exhaustive literature claim is accepted. No new proof attempt is charged to or appended to the five author approaches: this is verification and correction of their stated scope.
