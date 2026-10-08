# Independent audit: rank-one-isotropy S5 sphere question

Problem 30001260 / OWR-3477-004; queue rank 970. Audit date: 2026-10-07 UTC.

## Verdict

**ACCEPTED AS CORRECT PARTIAL WORK, NOT AS A SOLUTION.** All five authored approaches are mathematically sound within their stated scope. No correction patch is required. The author files and their original ZIP remain unchanged. The target smooth existence question remains **unsolved, 5/5 author turns**. This is an independent mathematical audit, not journal peer review and not a claim of novelty.

The audited claims are the linear obstruction, necessary smooth fixed-set constraints, compatible local representations, failure of the specified induction/join repair, and the conditional thickening-boundary calculation. Neither existence nor nonexistence of the requested nonlinear smooth action follows.

## 1. Exact object and preservation

The audited author ZIP has 21,349 bytes and SHA-256
`80adc712a807f61e5b3daf948e356002d475cd44b5763408b05af1f70491aba0`.
Its manifest SHA-256 is
`3f689988d6844b90d70a1f3bbeb18dcbdecc769c8a98ed6c6f5f34053bc01757`.
All fourteen ZIP members, including the manifest, match the supplied author directory byte for byte. `AUTHOR_PACKET.zip` in this audit is an exact copy of that archive.

Every authored mathematical document, both author Python programs, captured checks, source metadata, disposition, gate summary, and corpus identity was read. The corpus files were separately hashed and parsed: both byte counts, both hashes, both record counts, the unique target problem, and absence of an exact research-result key agree with the packet. No dataset contents are included here. Historical remote search negatives in the attempt gate remain bounded author search evidence; this audit does not certify the absence of every inaccessible or unindexed prior attempt.

The author verifier passed in isolated normal and optimized Python, including after relocation. Independent mutation tests reject changed, missing, extra, symbolic-link and subdirectory entries, changed manifests, and wrong pins in both modes. See `ORIGINAL_PACKET_CHECKS.json`.

## 2. Problem and source/category audit

The original Question 4 is the smooth S5 sphere-action question in Yalcin's contribution to the 2009 Oberwolfach report, printed page 1499 / PDF page 13. It does not assume linearity or restrict all stabilizers to cyclic prime-power groups. The packet correctly interprets rank-one isotropy as rank at most one, so trivial stabilizers are allowed. [Original report](https://doi.org/10.4171/owr/2009/27).

Hambleton, Pamuk and Yalcin's established Theorem A produces a finite S5-CW complex homotopy equivalent to a sphere, with rank-one 2-power isotropy. In S5 these 2-groups are cyclic. Their introduction also records the linear obstruction and distinguishes the smooth question. The audit verified these statements, not the full proof of their realization theorem. [Published paper](https://ems.press/content/serial-article-files/43319).

The May 2026 survey repeats that finite-CW theorem as Theorem 8.1 and explicitly retains the smooth question in Remark 8.2. Its current arXiv record displays v1, submitted 4 May 2026; the PDF is dated 30 April. This is strong dated support for the packet's open-status wording, not a universal assertion about all later communications. Targeted fresh searches found no later resolution. [Survey, Section 8](https://arxiv.org/html/2605.02760v1#S8).

The 2016 rank-one-isotropy and 2015 preprint / 2017 published prime-power-isotropy results also concern finite equivariant CW realizations. Neither supplies an automatic smooth standard-sphere realization. The distinctions among standard smooth spheres, smooth homotopy spheres, topological spheres, and complexes of sphere homotopy type are retained throughout. [2016 paper](https://yoksis.bilkent.edu.tr/pdf/files/11968.pdf), [prime-power manuscript and publication record](https://arxiv.org/abs/1503.06298).

All five author-hashed PDFs were retrieved anew and exactly match their recorded byte counts and SHA-256 hashes. The auditor additionally retrieved the full 2014 Borel-Smith reference from the authors' institutional host; its Definition 5.1 and preceding hypotheses were read and visually checked. This expands the evidence beyond the author's accurately disclosed search-passage-only inspection. Source files, page images, extraction text, and private coordination material are excluded from this audit packet. Public source metadata is in `AUDIT_SOURCE_METADATA.json`.

## 3. Turn 1: complete linear obstruction

**Accepted.** The incidence map from the five-letter permutation module to the ten unordered pairs has Gram matrix 3I+J, hence is injective. Its orthogonal complement supplies an actual five-dimensional real module. The reduced permutation, sign-twisted, and exterior-square constructions are actual representations. Their character formulas, orthogonality, dimensions, and invariant averages are all correct.

As a genuinely different computational route, `independent_checks.py` builds the seven irreducible characters from partitions of five by the Murnaghan-Nakayama rule, then compares all 120 values of every row with the authored constructions. It independently recovers the invariant dimensions:

- dimensions 1, 4, 5, 6, 5, 4, 1 in partition order;
- E_A-invariants 1, 1, 2, 0, 2, 1, 1;
- E_B-invariants 1, 2, 2, 1, 1, 0, 0.

There is exactly one irreducible with no E_A invariants, the six-dimensional exterior square, and it has one E_B invariant. Semisimplicity makes the obstruction valid for every nonzero representation, with arbitrary multiplicities, rather than only a bounded-dimensional search. Complexification commutes with fixed vectors, so the conclusion applies to real representations as written.

A separately generated complete subgroup lattice has 156 subgroups. It contains exactly twenty V4 subgroups in conjugacy orbits of sizes five and fifteen, and no elementary abelian subgroup of order eight. Odd-prime rank two is impossible by the order 120. Thus avoiding every V4 fixed set is precisely the rank-at-most-one isotropy condition here. The argument does not exclude mixed-prime rank-one subgroups: the enumeration includes such subgroups of orders 6, 10 and 20.

The passage from fixed vectors to a forbidden point on the unit sphere is valid. There is no passage from this global representation obstruction to an arbitrary nonlinear smooth action. The packet makes that limitation explicit.

## 4. Turn 2: Smith/Borel hypotheses and edge cases

**Accepted, including the dimension -1 convention and r=0 case.** The input is a smooth finite-group action on a compact ordinary sphere. Restricting to a finite p-group gives the finiteness setting for Smith theory. Fixed sets are compact boundaryless smooth submanifolds, componentwise, for example by averaging a metric and using the local fixed tangent subspace.

Smith theory concerns p-subgroups. It says that a nonempty such fixed set has mod-p sphere homology, allowing S^0, and the empty set has the formal dimension -1. This audit does not replace that conclusion by integral sphere homology or by a diffeomorphism to a sphere.

The possible disconnected case has been handled correctly. If the homological sphere dimension is positive, H_0 over the field has rank one, so the fixed set is connected. Its manifold dimension equals its homological dimension, by the nonzero mod-2 top fundamental class. If the homological dimension is zero, there are two connected components and no positive-degree mod-2 homology. A positive-dimensional closed component would contribute a positive-degree fundamental class; hence both components are points. This rules out hidden positive-dimensional acyclic components. In particular, the equality-of-dimensions argument later in the turn does not silently assume every Smith sphere is connected.

The Borel subgroup-quotient identity used is the one in Definition 5.1(ii), and the preceding paragraph of that source specifies empty fixed sets using -1. It applies to the E_A and E_B actions and to the P/<z> action on F=M^<z>. Faithfulness of the quotient action is not needed. [2014 paper, printed page 360](https://yoksis.bilkent.edu.tr/pdf/files/8083.pdf).

Both V4 fixed sets are empty, exactly because of the isotropy hypothesis. Consequently n+1=3(a+1) and n+1=2(b+1)+(a+1). Their symbolic subtraction gives a=b=r and n=3r+2. Since n is a nonnegative sphere dimension and r is integral, r cannot be -1 or smaller. Thus r>=0; n=0 and n=1 are excluded. These equations by themselves do not assert existence when r=0, nor for any other surviving value.

For c=(1234), z=c^2 and s=(13), P=<c,s> is D8, z is central, and P/<z> is V4. Two of its three order-two preimages are V4 and the third is C4. Their fixed-set dimensions in F are -1,-1,dim M^<c>; F^P is empty. Applying the same formula yields dim M^<c>=r. Smith theory applies independently to C4, so for r>0 its fixed set is a closed r-manifold inside the connected closed r-manifold F. The inclusion is locally open and globally closed; it is nonempty, hence surjective. For r=0 both fixed sets are two-point sets and inclusion is again equality. This establishes M^<c>=M^<c^2> without omitting empty or disconnected possibilities.

At an involution-fixed point, the invariant normal space is its minus-one eigenspace and has dimension 2r+2. Its determinant is positive. Orientation sign is constant on the connected ambient sphere, so every involution, and then every product of transpositions, is orientation preserving. This proves the whole-action statement, not only a statement at the fixed points. Along the common C4/C2 fixed manifold, an invariant normal bundle is available, and the derivative of c squares to minus the identity on that bundle. It therefore defines a genuine complex bundle structure of rank r+1.

The local D8 models are compatible with these consequences. The independent code checks explicit 3-by-3 rotation matrices and their normal-plane square. These are necessary local constraints only. No use is made of Smith theory for arbitrary mixed-prime fixed sets, and no differential conclusion is extended to arbitrary nonsmooth topological actions.

## 5. Turn 3: local Sylow representations

**Accepted.** Twisting the three-dimensional reduced S4 permutation representation by sign makes its determinant trivial. Its restriction to D8 has traces 3 at the identity, -1 at all involutions, and +1 at the four-cycles. An explicit matrix model verifies the claimed line-plus-plane splitting and all D8 relations.

The displayed representations are actual direct sums, with complex dimensions twelve. The odd-prime characters have zero invariants, and their constant nonidentity character values respect every allowed fusion. Four copies of the D8 representation have zero invariants under both V4 types. The independent script checks all relevant conjugation comparisons, six hundred in total, rather than only the named generators. Realification doubles dimensions: the local spheres have dimension 23 and the nontrivial cyclic 2-subgroup fixed spheres have dimension 7.

The independent audit also checks all p-subgroup Borel-Smith section conditions for this particular proposed local dimension data: 35 elementary-abelian order-four quotient sections, 15 cyclic-four parity sections, and 16 odd-prime parity sections. There are no quaternion-eight p-subgroup sections. This is a diagnostic for the local dimension data, not a construction or proof of its smooth sufficiency.

The nonexistence of a global representation restricting to V2 follows from Turn 1. The Qd(p) eligibility assertion is sound: any section has order dividing 120, whereas Qd(p) has p-part p^3 for an odd p. A prime not dividing 120 is excluded a fortiori. Eligibility for a finite-CW theorem does not supply normal bundles or a smooth action. No dimension-23 smooth S5 construction is claimed.

## 6. Turn 4: induction and joins

**Accepted.** The fixed-coset character formula is valid, including at permutations with no fixed letters. As an independent check, Frobenius reciprocity gives

Ind(S4 to S5) W = exterior^2 U + (sign D) + (sign U).

Its dimension is 6+5+4=15, and its E_A and E_B invariant dimensions are 3 and 2. This agrees with the defining induction computation in the author script. The induced sphere therefore has the forbidden fixed S^2 and S^1.

The join argument uses the endpoint factors correctly. An E-fixed endpoint remains E-fixed irrespective of the other factor; an interior fixed point requires fixed coordinates in both factors. For nonempty factors the join fixed set is empty precisely when both factor fixed sets are empty. Consequently joins cannot erase the induced sphere's forbidden points. Conversely, joins of actions already satisfying the condition preserve it.

The whiskered-sphere example is a valid local-manifold warning. Near the free whisker endpoint the local factor is a half-interval. Joining with S^k gives a local half-interval times R^(k+1) model there, whose local homology at the distinguished point vanishes. A closed manifold has nonzero mod-2 top local homology. Homotopy type alone therefore does not repair the defect. This example does not claim to exclude all special equivariant realization procedures.

## 7. Turn 5: conditional thickening and duality

**Accepted.** Existence of an appropriate equivariant smooth thickening is expressly an extra hypothesis. An equivariant retraction sends any point to a point with a containing stabilizer, so it preserves the required upper bound on stabilizer rank, also on the boundary.

For a connected oriented D-manifold N homotopy equivalent to S^n, integral duality places its only nonzero relative groups at D and D-n. The assumption D>=2n+3 separates these degrees and their shifts from n. The pair sequence consequently gives boundary homology Z in degrees 0,n,D-n-1,D-1, and zero otherwise. At degree zero, the adjacent relative groups vanish, so the boundary really is connected. No torsion ambiguity or extension ambiguity remains in these separated degrees.

The model S^n times D^(D-n) independently corroborates this pattern. Since both intermediate groups are nonzero and distinct, the untreated boundary is not a homology sphere. This rejects the raw boundary construction under its favorable hypothesis, not every possible equivariant surgery strategy. The packet correctly requires further equivariant handle, normal-data and smooth-structure analysis before any smooth standard-sphere claim.

## 8. Reproducibility, limits and accepted disposition

`independent_checks.py` is a standard-library-only implementation and does not import the author's programs. Its output is reproduced in `INDEPENDENT_CHECK_RESULTS.json`; normal and optimized executions agree. It uses explicit exceptions rather than optimization-sensitive asserts. Four deliberately false group/character claims are rejected. The original and audit verifiers are integrity/replay tools, not formal proof assistants.

The written universal proofs, not bounded enumeration, justify the fixed-dimension relation and boundary homology formula. The finite computations corroborate all group-theoretic and character data. Classical Smith theory, Borel's formula, equivariant local linearization for smooth finite actions, and integral manifold duality are used as standard mathematical theorems; this audit verifies their applicability rather than reproving them from foundations. Published realization theorems are credited and their relevant statements checked, not recertified in their entirety.

Accepted queue disposition: **unsolved; 5/5; five audited partial approaches, no smooth construction or nonexistence proof.** A concise findings description may mention the reproduced linear obstruction, necessary n=3r+2 and C4/C2 constraints, the explicit compatible Sylow data, and the unresolved smooth realization step. Preserve the dated nature of the survey's open-status evidence and the absence of any novelty claim.
