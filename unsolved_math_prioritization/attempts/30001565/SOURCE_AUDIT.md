# Removing the source's spectral hypothesis by a credited split-algebra algorithm

**Proposed disposition: already_solved, 0/5 author research turns, pending independent source/full-correspondence audit.** This packet checks a published algorithm against the original qualitative computability question. It does not propose a new factoring-free polynomial-time algorithm.

## 1. Published input and exact algorithmic qualifications

G. Ivanyos, L. Rónyai and J. Schicho, “Splitting full matrix algebras over algebraic number fields,” *Journal of Algebra*354(2012),211–223, DOI[10.1016/j.jalgebra.2012.01.008](https://doi.org/10.1016/j.jalgebra.2012.01.008).

The complete [author manuscript1106.6191v3](https://arxiv.org/abs/1106.6191v3) was read, including Theorem1, its following remark, the algorithms in §§2–3 and the termination proof. Publisher metadata and abstract were also checked. A complete publisher-layout PDF was not accessed; the full primary proof copy is the author manuscript. The arXiv record dates v3 to21December2011 and says Theorem2 and Lemma8 were corrected; the retrieved PDF's title-page date is26September2018. We bind the exact bytes and version identifier rather than using that rendered title date to infer a different publication year.

Theorem1 takes:

- an algebraic number field K, in a standard exact finite representation;
- an associative K-algebra B supplied by structure constants;
- the promise B is isomorphic to M_m(K).

It constructs an explicit isomorphism B→M_m(K), equivalently an irreducible B-module. The actual algorithm outputs an element x of **reduced matrix rank one**, then uses left multiplication on Bx. The rank-one property is in the abstract full matrix algebra M_m(K), not necessarily rank one in a larger supplied matrix embedding.

The polynomial-time statement is an **ff-algorithm** with bounded field degree, discriminant and m (equivalently the published abstract fixes K and bounds m). An ff-algorithm has oracles for factoring integers and univariate polynomials over finite fields. The paragraph immediately after Theorem1 explicitly says the algorithm still constructs the isomorphism without bounded parameters, although its running time can be exponential in them. Factoring is decidable without an oracle, so replacing those calls by terminating exact procedures gives an unconditional terminating algorithm; no polynomial-time conclusion is then asserted.

The proof searches finitely many lattice combinations in a maximal order, after possible reductions to smaller matrix corners. Theorem7 supplies a bounded rank-one element, Lemma8 bounds nonsingular short vectors, and Lemma6 bounds lattice coefficients. The search therefore terminates. The real/complex embedding subroutines and the factoring oracles must not be omitted from its computational requirements. There is no assumption that a chosen self-adjoint input element already has all distinct roots in K.

## 2. Why the coherent-configuration component satisfies the input promise

Use the exact Schurian source setting: G is a finite permutation group on Omega, pi its permutation representation, and K is a supplied splitting number field for G. For *-calculations it is convenient to choose K stable under complex conjugation, for example a cyclotomic splitting field containing the required roots of unity. A merely character-value field must not be substituted: it need not split the representations. If an initial splitting field is not conjugation-stable, pass to its compositum with its conjugate for the Hermitian step. There is no free or uniform-complexity claim for constructing this field.

The orbital 0–1 matrices form a basis for

A_K = End_(KG)(K^Omega).

Because K is a genuine splitting field and characteristic is zero, the usual completely reducible decomposition gives

K^Omega = direct sum_chi V_chi tensor K^(m_chi),
A_K isomorphic to direct sum_chi M_(m_chi)(K).

This is the classical centralizer decomposition, with multiplicities m_chi rather than irreducible group dimensions dim(V_chi). It is precisely the distinction used in the source.

Given the character data available at the source's step, compute the usual central projection

e_chi = (dim(chi)/|G|) sum_(g in G) chi(g^-1) pi(g).

Its efficient class-sum implementation is not required for the qualitative claim. For each occurring chi, B=e_chi A_K is a *-closed simple K-algebra isomorphic to M_(m_chi)(K). Gaussian elimination on the known matrices e_chi A_i produces a K-basis and its structure constants. Thus B has exactly the input type of the published algorithm. The selected spectral X is not an input and need never be found.

For an arbitrary, possibly non-Schurian coherent configuration, the same correspondence applies whenever the desired split simple component and a splitting number field are supplied. The particular original question appears after the Schurian character-projector construction. This packet does not silently presume that every character-value field, or the rational algebra of every non-Schurian configuration, is already split.

## 3. Recovering the irreducible action over K

Run the published algorithm on B and obtain a reduced-rank-one x. The left ideal I=Bx has K-dimension m=m_chi. Compute a K-basis u1,...,um by Gaussian elimination on the products b_j x. For each source basis matrix A_i, solve

e_chi A_i u_j = sum_l R_i(l,j) u_l.

These linear systems give R_i in M_m(K). Extending linearly defines an algebra representation R of A_K. It is irreducible and its restriction to B is an isomorphism: under any abstract identification B=M_m(K), Bx is a minimal nonzero left ideal, and the left action is the defining m-dimensional module. Equivalently, its kernel on simple B is zero and both B and End_K(I) have dimension m². Extension of scalars to C remains irreducible because the image is all of M_m(C).

If the physical embedding of B has a repeated factor, x may have larger physical matrix rank. For example I_r tensor E_11 has physical rank r, but the left ideal in I_r tensor M_m(K) still has dimension m. The check program includes this control. Confusing the two ranks would invalidate the reduction.

## 4. Obtaining the required standard *-representation

The algebra action R need not preserve the standard Euclidean Hermitian form in the arbitrary basis u_j. Use the positive trace form inherited from the original matrix embedding:

H_ij = Tr(u_i^* u_j).

The basis matrices are linearly independent, so H is positive-definite Hermitian at the specified complex embedding: c^*Hc=Tr(U^*U)>0 for U=sum_j c_j u_j nonzero. With a conjugation-stable K, its entries belong to K. This uses the actual positive matrix involution in the source, not an arbitrary involution on a split abstract algebra.

For every a in A_K, left multiplication obeys

R(a)^* H = H R(a^*),

because <a u,v>=<u,a^*v> for the inherited trace form. The ideal need not be closed under *; it only needs to be invariant under left multiplication by a and a^*, which it is.

Compute an exact Hermitian LDL or Gram–Schmidt factorization H=C^*C. Its divisions are valid because H is positive definite. The diagonal factors are positive real algebraic numbers; adjoining their positive square roots gives a finite algebraic extension L inside C. Then

phi(a)=C R(a) C^-1

satisfies phi(a^*)=phi(a)^*. It is still irreducible and has exactly m rows and columns. Thus it is the desired irreducible complex *-representation from the source. Every operation is effective in exact algebraic-number arithmetic. The unnormalized irreducible action stays over K; only the standard-* normalization may require the stated extension.

This extension is a genuine qualification. A splitting field for a representation is not automatically a field admitting an orthonormal realization. For example the rational two-dimensional S3 representation preserves H=[[2,-1],[-1,2]], of determinant3, and its invariant symmetric forms are scalar multiples of H. If a rational change of basis made it orthogonal, H would be scalar-congruent over Q to the identity, impossible since 3 is not a rational square. A suitable real algebraic extension removes this obstruction. The original source targets matrices over C and already admits quadratic normalization irrationals, so it does not impose that stronger rational orthonormal requirement.

No characteristic polynomial of the source's special X is factored in this reduction because no such X is selected. This is not a claim that the published split-algebra subroutine itself avoids all characteristic polynomials, root operations or the explicit ff factoring calls.

## 5. Corroborating later implementation and what is not claimed

Hymabaccus and Pasechnik, *Journal of Open Source Software*5(50)(2020),1835, [DOI10.21105/joss.01835](https://doi.org/10.21105/joss.01835), documents exact cyclotomic representation decomposition, unitarization and centralizer computation in RepnDecomp, crediting Serre's formulas and Dixon's algorithms. The current author documentation's Chapters3,5,6 further distinguishes the routines and irreducible inputs. Its `IrreducibleDecompositionDixon` entry is expressly an unimplemented placeholder; the Chapter5 Serre/author decomposition routines are separate, and no claim of executing the placeholder is made. This is corroborating evidence of later computational tools in the same setting, not a substitute for the complete split-algebra theorem and the correspondence above. No downloaded package has been executed and no benchmark improvement is claimed.

The negative conclusion of the earlier literature desk note is therefore too broad if read as saying that the source's particular spectral assumption is still necessary for an exact algorithm. The known2012 theorem supplies a general alternative, with the qualifications above. Proposed status is **already_solved0/5** for the literal qualitative source question. A uniform factorization-free polynomial-bit algorithm, an optimal practical implementation, or a standard-* realization inside an arbitrarily prescribed original field is a different and stronger target, not answered by this packet.

This is a credited source specialization and normalization check, not a new research theorem or an independent reimplementation of the entire2012 lattice algorithm. Separate full review must confirm the source interpretation and every reduction before publication.
