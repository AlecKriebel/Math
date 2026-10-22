# Cup adjunctions and the remaining compatibility problem

The fifth approach seeks a uniform all-k comparison from the functors associated with cups and caps, rather than from pairwise cohomology dimensions.

Let F_A:Db(Vect)→Db(Coh(X)) denote a crossingless cup functor with F_A(C)=E_A. Adjunction identifies each derived Hom complex with

RHom(E_A,E_B)≅F_A^R F_B(C).

Under this identification, composition is induced by the counit in

F_A^R F_B F_B^R F_C → F_A^R F_C.

This is the relevant map: an object-level isomorphism of F_A^R F_B with a tensor product of circle complexes does not yet compare that counit with the prescribed merge/split maps. An all-k proof must choose the circle decompositions coherently with these counits for all triples and with iteration of surgery.

## What the original coherent construction supplies

Cautis–Kamnitzer, arXiv:math/0701194, Section 7.2, constructs the cobordism maps in a target whose 2-morphisms are projective classes of morphisms, hence defined up to a nonzero scalar. Theorem 7.2 proves invariance in that projective target. Theorem 8.2 identifies the link homology with Khovanov homology after regrading. These statements alone do not supply the simultaneous linear, multiplication-preserving choices required for the present Ext algebra.

Mackaay–Webster, arXiv:1502.06011, Theorems 5.10 and 5.11, provide powerful comparisons of knot homologies using categorical skew Howe duality. The inspected theorem statements compare link invariants; no full faithful comparison on the particular half-canonical sheaves and all of their Yoneda compositions was extracted here. The paper invokes strictification results, but converting those to the desired concrete algebra map would require a further argument and precise grading comparison. We have not supplied that argument.

## Why a scalar normalization shortcut is incomplete

Suppose, provisionally, all relevant composition images were known up to nonzero scalars c_ABC relative to chosen diagram maps. Rescaling a lowest-degree generator u_AB by s_AB would change a scalar by

c_ABC ↦ (s_AB s_BC / s_AC)c_ABC.

In a setting where every iterated product is nonzero and cancellable, associativity can turn the c's into a cocycle and permit a normalization argument. Here the rings are nilpotent and many products vanish by degree. A zero product gives no equation after cancellation, and higher-rank allowed image spaces need not even be one-dimensional, as HIGHER_RANK.md shows. Thus this proposed shortcut fails without additional nonvanishing and coherent factorization statements.

## Conflicting apparent prior resolutions

Anno's 2008 preprint arXiv:0802.1070v1, Proposition 6 and Theorem 4, presents a canonical-identification and multiplication claim for the annular setting. However the later joint Anno–Nandakumar preprint arXiv:1602.00768v1, Section 5.3, expressly gives the multiplication as conjectural, despite stronger wording in its abstract. The published 2023 paper's publisher-deposited abstract likewise says that the Ext spaces are computed and the annular algebra structure is conjectured. Consequently we do not treat the earlier claim, or an abstract/search summary of it, as a verified all-k resolution. The annular family is also larger than the planar component collection, so its category and object identifications cannot be silently interchanged.

The 2023 publisher metadata lists an Anno work titled Multiplication in Khovanov cohomology via triangulated categorifications as in preparation. No public primary manuscript with that title was located in this search. A bibliography entry does not establish the missing theorem.

## Outcome

The precise remaining target is a coherent identification of the mixed counit/composition maps with the chosen associative weighted convolution, with gradings and scalar signs controlled. The route yields no full all-k solution in this investigation. Equality of link invariants, projective cobordism invariance, and formality are each weaker than an explicit identification of the entire cohomology multiplication.
