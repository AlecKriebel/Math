# Turn 3: split-prime independence and integral lifting

Attempt: upgrade the credited prime-ideal images to the entire geometric ell-adic image, avoiding the invalid inference that two surjective projections must have product image.

Let ell>=7 be prime and R=O tensor Z_ell. The Tate module of the generic Jacobian is free of rank two over R. The principal polarization and Rosati-self-adjoint RM identify the geometric image H with a closed subgroup of SL_2(R). Here the trace pairing of the unramified algebra R is perfect, and the polarization can be written Tr(beta det(v,w)) with beta a unit; preservation is equivalent to determinant one. All identifications are up to a choice of R-basis.

If ell is inert in K, Turn 2 already gives the full reduction SL_2(F_{ell^2}). If ell splits, the two reductions each equal SL_2(F_ell). To prove joint surjectivity, use Goursat's lemma and the following standard finite-group facts, with ell>=5: the only proper normal subgroups of SL_2(F_ell) are {1} and its scalar center; PSL_2(F_ell) is simple; every automorphism of PSL_2(F_ell) is induced by PGL_2(F_ell). The last statement has no field-automorphism factor because the field is prime.

A proper subdirect product would therefore identify the two projective representations through a PGL_2-conjugacy. Such an identification preserves the invariant trace(g)^2/det(g). A single common inertia element at infinity rules it out. In the two embeddings its traces are -w and -w', where w+w'=-1 and w-w'=sqrt(5). Thus w^2-(w')^2=-sqrt(5), nonzero modulo every prime above ell !=5. This contradicts equality of projective trace invariants. Hence reduction modulo ell is the full product.

For completeness the required lifting lemma has an elementary proof. Let R be a finite product of unramified extensions of Z_p, p>=5, and let H be closed in SL_2(R), surjecting modulo p. Write K_n for the kernel of reduction modulo p^n. Then K_n/K_{n+1}=sl_2(R/pR), additively. Select h in H lifting a unipotent I+E_12 in one residue-field factor and identity in the others. Its p-th power is I+pE_12 modulo p^2 in that factor and identity in the others. To check this for an arbitrary lift h=I+E_12+pA, expand modulo p^2. The correction sum is p times a polynomial sum of degree at most two in the conjugation index; sums of 1,j,j^2 vanish modulo p for p>=5. Since E_12^2=0, the asserted leading term follows.

The image of H intersect K_1 in K_1/K_2 is invariant under conjugation by SL_2(R/pR). The F_p-span of the conjugates of E_12 is all of sl_2(k) in each factor k: diagonal conjugation supplies square multiples of E_12; differences of squares span k; the Weyl matrix supplies E_21; and conjugating E_12 by [[1,0],[1,1]] supplies the diagonal direction. Thus the first layer is full, independently in each factor. Raising I+p^n X to the p-th power gives I+p^{n+1}X modulo p^{n+2}, for every n>=1, so every later layer is full. Induction gives surjectivity modulo p^n for every n. Closedness gives H=SL_2(R).

Therefore, for the generic geometric representation, for every prime ell>=7,

Im(G_{Qbar(t)} on T_ell J_t) = SL_2(O tensor Z_ell).

The proof uses the credited Darmon--Mestre residual theorem and its infinity inertia trace, the displayed elementary lifting argument, Goursat's lemma, and the stated standard finite-group facts. It does not use finite numerical evidence as an all-primes proof. It does not address 2,3,5, simultaneous independence across different rational primes, or equality after specializing t to a rational number.

Outcome: exact generic geometric local Tate images at every ell>=7. This is a reconstruction from established inputs, with no historical novelty claim.
