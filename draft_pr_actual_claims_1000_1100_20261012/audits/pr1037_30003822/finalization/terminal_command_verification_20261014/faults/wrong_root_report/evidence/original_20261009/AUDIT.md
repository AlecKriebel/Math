# Independent audit of the restored forest determinant proof

## Verdict and exact scope

**Accepted.** The frozen proof establishes, for every integer n at least 1, that the Catalan power (det A)^{C_n} divides det T in the polynomial ring Z[a_ij], where T is the full Bell-partition transition matrix in Teufl and Wagner's Problem 1. No mathematical defect or missing hypothesis was found.

This verdict applies to the complete text of **RECONSTRUCTED_PROOF.md**, 25,072 bytes, with SHA-256:

546d9df387da3266b1b20d31b1cd6017a65fe9f497f1b37d2a99319e6194755c

The entire proof, including all seven lemmas, the determinant lifting argument, the n=1 case, and the attribution section, was read and checked in this audit. The assessment is based on these newly reconstructed bytes. It does not inherit an acceptance of an earlier file or infer identity from an earlier checksum. This is a fresh audit of the restoration of the same proof, not a further research turn.

The conclusion is divisibility. It does not assert the exact multiplicity of det A, irreducibility of the remaining factor, worldwide priority, or present unresolved status of the 2018 problem. The review found no restriction to planar graphs, noncrossing partition states, symmetric matrices, positive weights, nonsingular numerical specializations, or matrices with nonzero numerical row sums.

## Exact problem match

The primary source is Elmar Teufl and Stephan Wagner, “A determinant related to set partitions,” in Oberwolfach Report 23/2018, printed pp. 1457–1458. Both pages were text-checked and visually inspected. [Report DOI](https://doi.org/10.4171/OWR/2018/23); [public report PDF](https://ems.press/content/serial-article-files/46745).

The restored definition uses all set partitions on each of two n-vertex layers. One unweighted tree per input block is fixed. Only interlayer edge subsets are summed, each once. Their union with those fixed trees must be a forest; every component must meet the new layer; and the component intersections must induce the prescribed output partition. These requirements match the source. In particular, the proof does not multiply a transition by a count of possible internal block trees.

The source PDF independently hashed in this audit has 1,261,683 bytes and SHA-256 6512c6b53d12d362868ca481bc7445bb97fc465da1e37d2ffdf40127d600e97f. Printed pages 1457 and 1458 are PDF pages 77 and 78. The source's Bell-state determinant question is exactly the theorem addressed by the proof.

## Forest products and all coefficient signs

The proof's ordered edge polynomial is q_uv=(xi_u-xi_v)(barxi_u-barxi_v). All q_uv are even, commute, and square to zero. Separating a product of s edge factors into its unbarred and barred wedges introduces the stated sign (-1)^{s(s-1)/2}. This sign is independent of which tree represents the same block.

A cycle creates a linear dependence among its incidence differences and annihilates the unbarred wedge. For a tree on a block, the oriented incidence differences form an integral basis of the sum-zero lattice: path sums generate every difference from a root, and their number is the lattice rank. Changing trees therefore changes the two wedge bases by the same unimodular matrix. Their two determinant signs cancel. This proves tree independence with coefficient +1, not merely up to sign.

The exponential expands as the product of (1+a_ij q_ij), so every interlayer subset occurs with coefficient exactly its weight and with no factorial or tree-count factor. A component wholly in the old layer has insufficient exterior degree to survive extraction of all its old-layer variables. In every other forest component, its polynomial may be represented using a star at a new-layer root. Each old-layer vertex then occurs in just one factor. Extracting its ordered pair necessarily chooses the xi_x barxi_x term, whose coefficient is +1. The even pairs can be moved into the specified integration order without a sign.

Consequently the remaining new-layer polynomial is exactly the polynomial of its component partition, and the operator identity G_A f_P=sum_Q T(P,Q) f_Q is proved with the correct positive coefficients. Replacing an already chosen forest by a star is an algebraic identity, not an additional combinatorial summation. This also checks that the use of arbitrary fixed block trees is legitimate.

## Invariant spanning without an unproved basis assumption

The fixed quotient is W=Lambda(U tensor Q^2)^{SL_2}, where U is the (n-1)-dimensional sum-zero space. It is independent of A.

The weight-space lemma is valid for the tensor and exterior modules used. With E adjoint to F and [E,F]=H, a weight-zero vector killed by E is also killed by F. Conversely, invariants are in that kernel. A vector in weight two orthogonal to the image of E must satisfy Fw=0; the commutator then gives 2||w||^2=-||Ew||^2, forcing w=0. Thus E from weight zero to weight two is surjective, and invariant dimension is the difference of the two weight dimensions. Rationality is justified by the rational matrices of the defining kernels.

The proof of quadratic generation is complete. In an even tensor power of the standard representation, the invariant dimension is Catalan. The tensors associated with noncrossing epsilon matchings are invariant and have distinct lexicographically maximal Dyck words, each with coefficient 1. In a linear dependence, the largest leading word among the nonzero coefficients cannot be canceled by any term with a smaller leading word; this proves independence. The Catalan count therefore proves spanning. Odd tensor powers have no invariants because the central element -I acts negatively.

Normalized antisymmetrization gives an equivariant section of exterior projection in characteristic zero. After separating U and standard-representation tensor factors, the preceding spanning theorem descends to products of b(u,v)=xi(u)barxi(v)+xi(v)barxi(u). There is no unproved assertion that invariants of an arbitrary quotient lift: the explicit equivariant section supplies the lift here.

For the root-difference basis, b(u_i,u_i)=2q_in and b(u_i,u_j)=q_in+q_jn-q_ij. Thus the edge polynomials generate W over Q. Their monomials either vanish by repetition or a cycle, or equal a forest-state polynomial. This proves surjectivity of the constant map from the full Bell-state space onto W. The noncrossing objects in the tensor-basis argument do not restrict any input or output partition of T.

## Catalan dimension and the determinant exponent

For m=n-1, exterior degree 2r has invariant dimension

d_r = binom(m,r)^2 - binom(m,r-1) binom(m,r+1).

This follows from the weight-zero and weight-two monomial counts just proved. With out-of-range binomial coefficients interpreted as zero, summing gives binom(2m,m)-binom(2m,m-2)=C_n. Symmetry d_r=d_{m-r} implies sum_r 2r d_r=m C_n.

The determinant character on W is checked rather than assumed. On a diagonal change of basis of U it is a monomial in the diagonal entries. Permuting those entries forces equal exponents. The scalar change tI acts in degree 2r with factor t^{2r}, so the preceding degree sum makes each exponent exactly C_n. Conjugacy gives the result on diagonalizable matrices, and polynomial density extends it to all invertible matrices in characteristic zero. Thus det rho(g)=(det g)^{C_n}, with no unknown scalar or sign. The m=0 exception is kept out of this argument and treated directly at n=1.

## The ordered Gaussian factorization

The row sums r_i and det A are nonzero polynomials in the generic coefficient field. It is therefore legitimate temporarily to use D=diag(r_i), B=D^{-1}A, and S=diag(column sums)-A^T D^{-1}A. No numerical nonvanishing assumption has been imposed on the final theorem.

The completion of the quadratic form has the exact stated signs. In the proof's species order,

sum_ij a_ij q_ij = (xi-B eta)^T D (barxi-B bareta) + eta^T S bareta.

Expanding this expression does not exchange odd factors. The identities B1=1, S=S^T, and S1=0 all hold without assuming that A is symmetric.

The lowering operator H_D is well-defined and preserves the difference algebra: after substitution, every input difference remains a sum of an integrated difference and an unintegrated difference. It also preserves SL_2 invariants. The simultaneous SL_2 action fixes each integrated pair, the Gaussian, and the integrated top form; coefficient extraction is consequently equivariant. The normalized top Gaussian coefficient is det D. The degree-preserving contribution to H_D is the identity, while every other nonzero contribution uses a positive even number of integrated variables from the input and strictly lowers its remaining degree. Hence det H_D=1.

The symmetry and zero row and column sums of S express eta^T S bareta as a quadratic invariant in differences. Multiplication by its exponential therefore preserves W and is identity plus strictly degree-raising terms. Hence det M_S=1. Neither triangular argument requires H_D to commute with the middle substitution.

For row coefficient vectors, B preserves U because B1=1. Its action on the one-dimensional quotient by U is the identity, giving det(B|U)=det B=det A/det D. The odd translation used in coefficient extraction has coefficient +1 on the full old-layer top monomial; no lower-old-degree monomial can produce that top monomial after translation. This verifies the Berezin shift without an additional Jacobian sign.

The ordered factorization is exactly

G_A = (det D) M_S rho(B|U) H_D.

Taking determinants gives (det D)^{C_n}(det A/det D)^{C_n}=(det A)^{C_n}. The raising and lowering factors both have determinant 1. The normalization fixes equality, not equality only up to a nonzero constant. Since G_A already has polynomial entries from its original edge-subset definition, the field identity is a polynomial identity. It remains valid when some row sums vanish or A becomes singular.

## Constant kernel and integral descent

With the proof's column-vector convention, the partition-space operator has matrix T^T, whose determinant is det T. The transfer identity makes the kernel of the constant rational surjection invariant. Extension from Q to Q[a_ij] gives exactly the scalar-extended kernel. A rational basis of the kernel together with rational lifts of a quotient basis is a constant basis of the Bell-state space. In that basis the matrix is block triangular with the quotient operator G_A on the diagonal.

The complementary kernel block has polynomial entries over Q[a_ij]. No variable-dependent basis, denominator cancellation assumption, or specialization of the kernel is used. Its determinant supplies a polynomial rational quotient, proving divisibility in Q[a_ij].

The determinant polynomial det A is primitive over Z, so its Catalan power is primitive. Multivariate Gauss's lemma then forces the rational-polynomial quotient to have integral coefficients. The proof includes a correct content argument and allows the zero quotient. This is genuine divisibility in Z[a_ij], rather than a pointwise numerical vanishing statement. The direct n=1 calculation completes the full asserted range.

## Independent finite checks

The all-n acceptance above is based on the written argument. Independently written finite calculations were used only to check conventions and identify possible exceptional-case errors.

The supplementary checks passed as follows:

- Symbolic edge-subset transfers, exterior coefficient extraction, and determinants for n=1 and n=2. In particular, the latter determinant is (a_11 a_22-a_12 a_21)^2 with positive sign.
- Star-versus-path equality of all forest-state polynomials and their ranks modulo 1,000,003 for n=1 through 6. The ranks were 1, 2, 5, 14, 42, and 132. These finite ranks are not being substituted for the general invariant-space proof.
- Cycle annihilation for cycles of lengths 3 through 6.
- Exact integer edge-subset enumeration compared against direct exterior integration on every state of seven n=3 or n=4 examples. These included generic matrices, singular matrices, the zero matrix, and invertible matrices with a zero row sum. Changing the fixed input-block trees from stars to paths left every tested transfer matrix unchanged.
- On every one of those examples, the constant forest-state map intertwined the full transfer with its quotient, and the quotient determinant equaled (det A)^{C_n}. For the zero-row-sum invertible n=3 example, det A=-5 and the quotient determinant was -3125. For the n=4 example, det A=2 and the quotient determinant was 16384 even though the full transfer determinant was zero; this correctly leaves room for a vanishing complementary factor.
- Direct exact-rational calculation of the three ordered Gaussian factors agreed with independent edge-factor integration for every Bell state of two n=3 examples and one n=4 example, including negative matrix entries and a negative row sum. This checks the placement of H_D before substitution and both species' signs.
- The finite n=4 full determinants also agreed with the additional permanent-factor formula stated in the 2018 source. This observation is not used to infer an all-n formula or an exact factor multiplicity.

## Attribution review and final disposition

The report correctly treats the forest algebra as established. The relevant earlier source is Caracciolo, Sokal, and Sportiello, *Grassmann Integral Representation for Spanning Hyperforests*, J. Phys. A 40 (2007), 13799–13835, Sections 4–5. [Version 2](https://arxiv.org/pdf/0706.1509v2); [DOI](https://doi.org/10.1088/1751-8113/40/46/001). Its Corollaries 4.3–4.5 and their proof span pp. 15–17; the partial-integration statements occur on pp. 18–19. The proof's final citation includes the continuation onto p. 17.

Sportiello's thesis supplies a detailed earlier Catalan-basis treatment in Chapter 10, Theorem 10.3 and Lemma 10.6, with the latter's triangular argument on printed pp. 211–213. The inspected text explicitly uses lambda-independent selected coefficients. The normalized lambda-zero formulation and nonplanar transfer context support the report's limited attribution. [Public thesis PDF](https://pcteserver.mi.infn.it/~caraccio/PhD/Sportiello.pdf). The restored proof nevertheless establishes its own invariant spanning and dimension, so it does not depend on an unproved announcement or an invalid zero-parameter specialization.

The sole change during the final audit was the bibliography-only page-range correction from 15–16 to 15–17. Reversing exactly that replacement recreates the earlier draft's hash; no mathematical text changed. The accepted hash stated at the beginning is the final corrected file.

**Final disposition: accept the restored proof for the precise all-n integral determinant-divisibility theorem stated. No mathematical revision is required.** This audit does not authorize or claim any external publication, queue update, or new novelty conclusion.
