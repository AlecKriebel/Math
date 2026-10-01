# Independent full review of the corank criterion for 30002597

Date: 2026-10-01 UTC

## Verdict

**PASS: complete at the stated source-matched scope.** The equivalence between an allowed stable proper disk extension in some compact bounding 3-manifold and maximal free corank of the one-relator quotient is correct. The cited coefficient-free rank algorithm supplies a terminating decision procedure for every finite combinatorial input. This covers arbitrary prescribed curves, not merely a negative answer to universal existence.

The result is an application of established topology and group-theoretic algorithms. No novelty, priority, efficient implementation, or human peer-review claim is certified. This report is an independent AI mathematical/source audit.

Exact frozen artifact reviewed:

- `CORANK_CANDIDATE.md`
- SHA256 `e86a939d63d618cd7cafccf9b0ba1f847970aa319f990517d9e592b5f756d020`

Review completion estimate: 100% of the assigned full mathematical and primary-source audit.

## 1. Exact scope

The input is a generic immersion of one parametrized circle in a closed connected oriented surface S_g. The target permits the usual stable generic maps of an oriented disk to a 3-manifold, including simple branch points. It does not require an embedded or everywhere immersed disk. The ambient manifold is not assumed orientable; the proof explicitly disposes of that ambiguity.

The original OWR passage, printed p.1445, asks for this surface-curve disk-extension existence problem and then distinguishes the analogous framed-four-graph problem. The candidate does not use the framed-graph statement as a solution of the surface problem. Its compact/smooth formulation is compatible with the imported record and the ordinary smooth/PL 3-dimensional general-position conventions. The decision algorithm's finite input requirement is explicit; it does not claim to process a noncomputable smooth-map oracle.

The quotient is independent of basing, orientation of the parametrized circle, and the chosen marked surface presentation. Conjugating or inverting the relation does not change its normal closure. Dependence only on the free homotopy class of the prescribed curve is justified by the relative-boundary map construction, rather than assumed without proof.

## 2. Stable disk maps versus null-homotopies

The forward implication is immediate: any disk extension is a null-homotopy. For the converse, the fixed collar `(z,t) -> (gamma(z),t)` has regular half-sheet boundary points and transverse double half-sheet boundary values, because gamma already has only transverse double points. One can extend the inner collar circle by a null-homotopy, move the remaining compact disk image off the boundary, smooth relative to the collar, and perturb only away from that collar.

The relative general-position theorem recalled in Funar's proof of Lemma4.1, printed p.302, explicitly retains the boundary and introduces only simple branch points plus normal double/triple strata. Ben Hadar Definition1.1 and p.1676 identify these as the generic stable local models, including the two boundary models. This supplies the correct relative statement; mere unrelative density would not have been enough.

The source disk is retained throughout. In particular, the later branch-removal surgery in Funar can add source handles and is not invoked. The candidate correctly allows the branch points instead. Preserving a generic collar also preserves the strong condition `f^{-1}(boundary M)=boundary D`.

## 3. Nonorientable fillings

For an orientable boundary surface of a 3-manifold, the orientation local system restricts trivially to that boundary: its normal line is a trivial collar line. Thus the orientation double cover has two separate copies of S_g over the single boundary component. The simply connected source disk lifts, with its entire boundary in one of the copies. Filling the other copy with an appropriately oriented handlebody leaves a compact oriented manifold with exactly the required boundary and the same lifted disk.

No orientation assumption on the original M has been silently introduced. Extra closed components can be discarded. The lift and the new filling do not add boundary preimages to the disk.

## 4. Arbitrary oriented filling to handlebody

This is the main geometric implication, and it passes the audit.

Start with a collar of S_g and successively add neighborhoods of compressing disks for its current inner boundary in the remaining manifold. The complexity used in the candidate is valid. For a separating essential compression of a positive-genus surface it decreases by1, for a nonseparating compression in genus greater than1 by2, and for a torus compression by1. Sphere components contribute zero. Hence the process terminates.

The resulting connected region C is a compression body, permitting sphere holes. Every positive-genus frontier component is incompressible in its complementary component, so its fundamental group injects there by the Loop Theorem. The frontier also injects into C by the compression-body product-plus-1-handles description. Sphere frontier groups are trivial and require no irreducibility or ball-bounding assumption.

For a disconnected complement and possibly several attachments to the same complementary component, van Kampen is a graph of groups, not just one amalgam. Both edge maps are injective, and the normal-form theorem injects the C vertex group into the group of the whole filling. Therefore a loop from S_g that dies in the original filling already dies in C. This is stronger and more precise than an unjustified assertion that the entire boundary group surjects the ambient group.

Filling each negative boundary of C with a handlebody, and each sphere with a newly chosen ball, gives a handlebody with outer boundary S_g. The dual 1-handle description proves that assertion. Null-homotopy survives these attachments. The argument remains valid for reducible fillings and does not confuse abstractly filling a sphere with finding a ball inside the original manifold.

Carter's printed p.879 already states the handlebody reduction via the Loop Theorem. The candidate provides the missing details instead of treating that sentence as a black box.

## 5. Maximal corank and geometric realization

The upper bound `corank(pi1(S_g)) <= g` is correct: pullback on H^1 is an injective isotropic subspace of the 2g-dimensional symplectic first-cohomology space. The standard handlebody quotient attains g, so equality holds. A quotient cannot have greater corank.

If gamma dies in a genus-g handlebody, the inclusion-induced boundary epimorphism factors through the quotient, proving its corank is g.

Conversely, Leininger–Reid Lemma2.2, printed pp.39–40, applies to exactly an epimorphism from the closed oriented genus-g surface group onto F_g. It realizes that epimorphism by a boundary homeomorphism followed by handlebody inclusion, with the required group identification. Applying it to the composite from the candidate quotient kills the prescribed curve. One may use a smooth representative of the boundary homeomorphism, since surface homeomorphisms are isotopic to diffeomorphisms; null-homotopy is unchanged. This standard smoothing point does not require altering the candidate's statement.

Genus0 is treated separately by a ball. In genus1, the primitive meridian direction parallel to the input homology vector kills even a nonprimitive multiple of that vector; zero homology is already null-homotopic on the torus. The proof therefore does not impose an unwarranted primitiveness requirement on gamma.

## 6. The algorithm really terminates

The finite presentation has all2g surface variables and the surface relator plus the word of gamma. These are coefficient-free equations. It is important not to omit variables absent from the curve word, since they can contribute to the maximal quotient; the candidate and its input code retain them.

Razborov Section9, printed p.151, defines solution rank to be the rank of the subgroup generated by the solution tuple, and system rank to be its maximum. It explicitly relates this to maximal free homomorphic images. Theorem3 on printed p.156, proved through p.158, supplies an algorithm computing that rank.

Razborov's associated radical coordinate group is not the same group as an arbitrary ordinary finite presentation, but no false identification is needed. Lemma1.2 and its remark on p.117 give the same free-group solution correspondence for the ordinary presentation. Each solution tuple gives a free image of the actual quotient, and conversely every free quotient gives such a tuple. Thus the computed integer is exactly the quotient's corank. No residual-freeness or ordinary word-problem algorithm for the quotient is assumed.

The comparison with g is therefore a terminating correct test on both YES and NO inputs. A mere enumeration of successful quotients would only semidecide YES; the candidate properly uses Razborov for the terminating decision and labels positive-witness enumeration as optional. It does not claim a practical complexity bound or claim that the published rank procedure was implemented here.

The optional realization citation also matches its scope. Blackwell–Kirby–Klug–Longo–Ruppik (2025), Definition2.1 with b=0, reduces to a closed surface epimorphism onto a rank-g free group; Theorem2.10 provides the stated diagram construction. This is not needed for termination of the YES/NO decision.

## 7. Computational checks and their limits

The author's `verify_corank_inputs.py` was inspected and rerun; its output reproduces `corank_input_verification.json` byte-for-byte, with6185 finite assertions. It is correctly labeled as coefficient-free encoding and positive-witness controls, not a corank solver.

A separately authored `independent_controls.py` imports none of the author's code. It passes6881 checks, including1681 torus homology vectors with Bezout surjectivity witnesses, nonprimitive meridian multiples, genus0, and preservation of all surface generators in genera1–12. These controls support the finite encodings and edge cases only. Neither script certifies the topological proof or implements Razborov; those parts are checked by mathematical argument and the primary theorem statements.

The known Carter negative example is consistent with the criterion and remains a credited classical obstruction. This review did not run a full corank algorithm on it. Carter's p.887 Problem6.2 itself already formulates that genus-two example as failure of its displayed quotient to surject onto a rank2 free group, providing additional attribution evidence.

## 8. Source access and publication limits

Primary sources independently checked:

- OWR26/2014, Manturov contribution, printed p.1445: original scope
- Carter (1991), author-posted primary text, printed pp.879 and887: handlebody reduction and explicit free-quotient formulation
- Leininger–Reid (2002), original PDF, printed pp.38–40: closed oriented convention, corank and realization lemmas
- Razborov (1985), full publisher PDF text in the web reader, printed pp.117,151,156–158: finite-presentation correspondence, rank definition, algorithm
- Funar (2008), primary paper, printed pp.302–303: boundary-relative general position and the separate genus-changing surgery that must not be used
- Ben Hadar (2017), publisher PDF, pp.1675–1676: proper generic/stable local models
- Sikora (2005), primary preprint introduction: independent corroboration of arbitrary finite-presentation corank computability
- Blackwell et al. (2025), complete published PDF, Definition2.1 and Theorem2.10: optional effective geometric realization

Razborov's PDF text was readable directly, but a facsimile screenshot request returned cache-miss errors and the author's local download had returned403. No visual-page check or local PDF recovery is claimed for that source. The theorem statement, rank definition, and relevant proof text were nonetheless available from the primary publisher PDF reader.

The complete criterion is an established-results consequence. The source's problem-list placement and later computational difficulty of particular flat knots do not invalidate theoretical decidability, but they also do not support a claim that this package introduced a new algorithm or solved every classification problem about free-knot/virtual-string cobordisms.

No remote write, publication, merge, release, or outreach was performed by this reviewer. The review does not spend another author proof-search turn or reopen earlier campaign attempts. Publication and final queue decisions remain separate.
