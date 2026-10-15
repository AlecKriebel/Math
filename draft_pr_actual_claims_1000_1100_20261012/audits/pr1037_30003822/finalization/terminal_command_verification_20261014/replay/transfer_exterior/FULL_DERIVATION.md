# Independent transfer-family derivation

Review start: 2026-10-13 22:28:31 UTC. Input head: `e87236a97c4b87818d2768cd5789043c7c3f4e39`. Submitted PROOF.md SHA-256: `546d9df387da3266b1b20d31b1cd6017a65fe9f497f1b37d2a99319e6194755c` (25,072 bytes). This derivation was written after reading PROOF.md and before reading submitted AUDIT.md or ACCEPTANCE.md. No previous pass finding is a premise.

## Exact claim and assumptions

For n >= 1, work in Z[a_ij], with all n^2 entries independent commuting variables. Index the matrix by every labelled set partition, so its size is Bell(n), not Catalan(n). For each input partition P take one fixed weight-one spanning tree in each block. An interlayer edge subset E is admissible exactly when its union with those trees is a forest on the entire X + Y vertex set, every component intersects Y, and its Y intersections form Q. Isolated Y vertices count as singleton blocks. Each subset contributes its squarefree monomial once. The claim is divisibility of det T by (det A)^C_n in the integral polynomial ring. It does not claim an exact valuation, an irreducible quotient, positivity, planarity, symmetry, or a particular specialization. The derived identities are characteristic-zero identities, followed by integral descent.

I independently reconstruct the complete argument below, concentrating on the forest/coefficient-extraction/Gaussian machinery. The partition quotient and its determinant character are also reconstructed here; their final independent specialist audit belongs to the other assigned family and must be combined with this verdict before promotion.

## 1. Forest products, signs, and internal tree choices

Let each vertex have two exterior generators x_v and b_v, and write q_uv=(x_u-x_v)(b_u-b_v), with unbarred factor first. It is unchanged if u and v are exchanged. Since q is even, different q's commute, and q_uv^2=0.

For oriented edge differences u_1,...,u_s in the coordinate vector space,

    product q_e = (-1)^(s(s-1)/2) (x(u_1) wedge ... wedge x(u_s))
                                           (b(u_1) wedge ... wedge b(u_s)).

The sign counts moving b(u_i) through the later s-i unbarred factors. An oriented cycle yields a signed linear relation among its edge vectors. Its unbarred wedge is zero, and so is the product including any additional edges. This applies to nonplanar graphs just as to planar graphs.

For a tree on a k-element block B, the k-1 oriented edge differences form a Z-basis of the sum-zero lattice on B. To check this without assuming a determinant: root the tree at b. Every e_v-e_b is the signed sum of edge differences along its unique path. Thus the edge differences generate the lattice. They number exactly its rank and are linearly independent (one can remove a leaf inductively). The matrix changing to any other tree basis is integral with an integral inverse; its determinant is +1 or -1. Each of the two exterior wedges changes by that same determinant. Its square is 1. The number s and the fixed sign above also agree. Thus any spanning tree produces exactly the same element, with no sign, scalar, or tree-counting multiplicity. Products over disjoint blocks produce f_P; singleton blocks give 1.

A useful combinatorial check is that the admissible interlayer subsets themselves do not depend on which internal tree was fixed. Contract each internal tree to one vertex. The graph is a forest before contraction iff the contracted multigraph is a forest (parallel interlayer edges can create cycles). Its connected Y sets are also unchanged. Thus the tree replacement in the algebra and the graph definition agree, even though neither definition sums over internal trees.

## 2. Transfer equals forest coefficient extraction

Order all X generators before Y generators, and within X use x_1 b_1 ... x_n b_n. Let I_X extract this top X word, leaving it to the left of Y coefficients. For independent weights,

    exp(sum a_ij q_xiyj) = product_(i,j) (1 + a_ij q_xiyj)
                        = sum_E (product_E a_ij) product_E q_e.

The finite exponential has this identity because the q's commute and square to zero. There is one choice (use or omit) for each edge, and no factorial remains. Multiplying by the single f_P gives the edge product for its fixed input forest union E.

If that union has a cycle, Section 1 kills it. If a forest component has k X vertices and no Y vertex, its factor has degree 2(k-1), hence cannot supply the required 2k X variables. Other components cannot provide those variables either. Its top X coefficient is zero.

For any forest whose components all meet Y, replace each component tree by a star rooted at one of its Y vertices. This is an equality of an already chosen product, not a sum over new forests. Every X vertex is a leaf, present in only its root edge factor. In q_xy, the x_x b_x term has coefficient +1, and no other factor contains x_x or b_x. Top X extraction must choose this term. These pairs have even degree, so putting their product in the prescribed X order gives +1. Once these X pairs are removed, the remaining edges form stars on each component's Y intersection. Their product is exactly f_Q by Section 1, including isolated Y vertices. Consequently

    G_A f_P := I_X[exp(sum a_ij q_xiyj) f_P] = sum_Q T(P,Q) f_Q.

This equality contains exactly the intended edge-subset weights once. A potential bad convention is summing over internal trees: that would multiply rows by block tree counts and is a different object. A potential bad convention is a rooted-tree coefficient: no root count is present here because the root was chosen for an algebraic identity, not enumerated. The convention x_v b_v rather than b_v x_v fixes the surviving coefficient +1.

## 3. Independent reconstruction of the constant quotient

Let U be the n-1 dimensional sum-zero row-vector space over Q, and V=Q^2 with its standard SL2 action. Let E=Lambda(U tensor V), realized by difference variables. Set W=E^SL2. Each q and f_P is invariant. The linear map Phi from the Bell-dimensional rational partition space, Phi(e_P)=f_P, has no weights in its coefficients.

For completeness, the submitted spanning and dimension mechanism can be checked as follows. In a tensor or exterior power of copies of V, the weight-zero invariant dimension is dim M_0 - dim M_2. One proof uses the ordinary positive definite Hermitian inner product: E^*=F and [E,F]=H. If v has weight zero and Ev=0, then ||Fv||^2=<v,(FE+H)v>=0, so it is killed by E,F,H. Conversely a fixed vector has those properties. The map E:M_0 -> M_2 is onto: if weight-two w is orthogonal to its image, Fw=0, giving 2||w||^2=||Fw||^2-||Ew||^2, which forces w=0. Fixed Lie-algebra vectors are fixed by upper and lower unipotents, which generate SL2. Rational kernels have the same dimensions after complex scalar extension.

In V tensor 2r the invariant dimension is binom(2r,r)-binom(2r,r+1)=C_r. Put the alternating epsilon tensor at the pairs of a noncrossing perfect matching. Its lexicographically leading word has + at every opening and - at every closing. The leading coefficient is 1: choosing the first epsilon term at each pair gives that word; changing the first affected pair changes its opening + to -, making the word smaller. Each Dyck opening/closing word determines the unique noncrossing matching by the stack algorithm. Hence the leading words are distinct and the matching tensors independent. There are C_r Dyck words by the reflection argument, so these tensors span all invariants. Odd tensor degree has none, since -I acts by -1.

Normalized antisymmetrization embeds an exterior power equivariantly into the tensor power and has exterior projection as a left inverse over Q. Since SL2 acts only on V slots, every invariant tensor is a sum of U-slot tensors times paired epsilon tensors. Exterior projection sends one pair to

    b(u,v)=x(u)b(v)+x(v)b(u),

because b(u)x(v)=-x(v)b(u). Thus invariant exterior elements are generated by b(u,v). For the sum-zero basis u_i=e_i-e_n,

    b(u_i,u_i)=2q_in,
    b(u_i,u_j)=q_in+q_jn-q_ij for i != j.

The q's therefore generate W over Q. Every monomial in q's is zero if an edge repeats or if its graph has a cycle; otherwise it equals a forest partition product by Section 1. Hence all f_P span W. This establishes the required constant surjection rather than a quotient depending rationally on A.

Put m=n-1. At exterior degree 2r, weight zero requires r unbarred and r barred variables, and weight two requires r+1 and r-1. Thus

    d_r = binom(m,r)^2 - binom(m,r-1)binom(m,r+1).

Summing gives binom(2m,m)-binom(2m,m-2)=C_(m+1)=C_n. The boundary binomial coefficients outside 0,...,m are zero. The symmetry d_r=d_(m-r) gives sum 2r d_r = m C_n.

For a linear g on U acting identically in the unbarred and barred copies, the induced W action rho(g) has determinant (det g)^C_n when m>0. On a diagonal torus the determinant is one monomial in the torus parameters, since W decomposes into torus weight spaces. Permuting U basis directions conjugates the action, so its exponents are all equal, say alpha. A scalar tI acts by t^(2r) on degree 2r, giving total exponent m C_n. Hence m alpha=m C_n and alpha=C_n. Conjugacy extends the formula to diagonalizable invertible g; such matrices are Zariski dense over C, so the polynomial identity holds for every invertible g. This does not assert that a selected Catalan set of f_P is a basis, and it does not require a noncrossing restriction on T.

## 4. Gaussian completion, translation, and the operator order

Work temporarily over K=Q(a_ij). Set r_i=sum_j a_ij, c_j=sum_i a_ij, D=diag(r_i), E=diag(c_j), B=D^-1 A and S=E-A^T D^-1 A. Because the a_ij are independent variables, each r_i and det A is a nonzero polynomial, hence invertible in K. Their possible zero values at a later specialization are irrelevant at this stage.

Let X variables be xi,barxi columns and Y variables eta,bareta columns. Direct expansion, with each unbarred factor left of its barred factor throughout, gives

    sum a_ij q_xiyj
      = xi^T D barxi - xi^T A bareta - eta^T A^T barxi + eta^T E bareta
      = (xi-B eta)^T D (barxi-B bareta) + eta^T S bareta.

The second cross coefficient is B^T D=A^T; the remaining product is B^T D B=A^T D^-1 A. No commutation of odd factors was used. S is symmetric even when A is nonsymmetric because D and E are diagonal. Since A 1=D 1 and A^T 1=E 1, B1=1 and S1=0; symmetry also gives 1^T S=0.

Top coefficient extraction in X is invariant under the change xi=z+B eta, barxi=barz+B bareta. To prove this directly, expand an arbitrary monomial in X variables and Y coefficients. Translation cannot increase its degree in z. Only an original full top-X monomial can contribute the full top-z monomial; that contribution takes every original X variable as its corresponding z variable in the same order, with coefficient +1. This is an exterior-algebra substitution, not an analytic Jacobian argument. Y terms may anticommute with z, but none of those terms participates in the only top-z contribution; thus there is no missing sign.

Define the normalized lowering map

    H_D f(xi,barxi) = (det D)^-1 I_z[exp(z^T D barz) f(z+xi,barz+barxi)].

Its degree-preserving term is exactly f: use no z from f and obtain the top z coefficient det D from product_i(1+r_i z_i barz_i). Any other surviving term takes both variables at one or more z indices from f, since the Gaussian gives either an entire pair or neither. It lowers the remaining degree by a positive even amount. Therefore H_D is lower triangular by exterior degree with identity diagonal blocks, so det H_D=1 on any stable finite graded subspace.

The stability details matter. A difference x_i-x_j becomes z_i-z_j+xi_i-xi_j, so after extraction only remaining differences occur. The z Gaussian is SL2 invariant because z_i barz_i is its pair wedge; the top z form is invariant as well. Simultaneous action on z and xi commutes with the substitution and with top extraction (the action preserves each z degree). Therefore H_D preserves W. The definition is normalized by det D, not by its square or its reciprocal Gaussian determinant. Omitting the normalization would change every diagonal entry by det D.

The raising map is M_S h=exp(eta^T S bareta)h. The zero row and column sums yield

    eta^T S bareta = sum_(i,j<n) S_ij(eta_i-eta_n)(bareta_j-bareta_n).

Its symmetry writes off-diagonal pairs as S_ij b(u_i,u_j), and a diagonal term as (S_ii/2)b(u_i,u_i). Thus its exponent lies in W_2. Multiplication preserves W; it adds only positive degree to the identity. Consequently det M_S=1. Invertibility also follows from the negative exponential.

Substituting xi=B eta acts on row coefficient vectors by u -> uB. The equation B1=1 gives (uB)1=u1, so this map preserves the sum-zero hyperplane and acts as identity on the one-dimensional quotient. The determinant of its restriction g_B to U is det B=det A/det D. This remains true for arbitrary row-stochastic B; no symmetry, column-stochasticity, orthogonality, or positivity is needed.

Translation and completion now give the exact ordered identity

    G_A = (det D) M_S rho(g_B) H_D.

In particular H_D is applied first to f as a function of its remaining xi variables; only then is xi replaced by B eta. The two operations generally do not commute. The scalar det D comes from undoing the normalization of H_D. All exponential arguments involved are even, so moving exp(eta^T S bareta) out of top coefficient extraction has no sign. Given the independently reconstructed determinant character,

    det(G_A | W) = (det D)^C_n * 1 * (det A/det D)^C_n * 1
                  = (det A)^C_n.

The constants are fixed: top Gaussian coefficient +det D, top translation coefficient +1, diagonal H_D and M_S entries 1, and quotient determinant det B, not a signed square root. For n=1, U=0 and W consists of constants; H_D=M_S=rho=1, while G_A multiplies by a_11. Thus the same scalar calculation works, and the direct forest transfer is the 1 by 1 matrix (a_11).

## 5. Polynomial continuation and integral descent

The forest formula already gives a polynomial matrix for G_A on a constant rational basis of W. Indeed Phi is a constant surjection and the equality G_A Phi=Phi L_A determines the quotient matrix using any constant rational right inverse. Therefore its determinant lies in Q[a_ij]. The calculation in K proves equality of two elements of Q[a_ij], whose inclusion into K is injective. It is a polynomial identity, so it holds at all substitutions, including zero row sums, a singular A, all-zero A, negative weights, and cancellations in row or column sums. The expression using D^-1 need not be numerically evaluated at these substitutions. This is why polynomial continuation is sufficient; it is not a limiting assertion.

Define L_A(e_P)=sum_Q T(P,Q)e_Q. Its matrix in column coordinates is T^T, with the same determinant as T. Let N=ker Phi over Q. Tensoring with R=Q[a_ij] preserves the exact sequence, since R is a Q-vector space and therefore flat. Thus the polynomial kernel is exactly N tensor R, with a constant rational basis. The intertwining identity makes it L_A-invariant. Extend that basis with rational lifts of a W basis. The polynomial matrix is block upper triangular with diagonal blocks K_A on N and G_A on the quotient. Its basis change and inverse are constant rational matrices, so K_A has polynomial entries over Q; no variables occur in its denominators. Hence

    det T = (det K_A)(det A)^C_n in Q[a_ij].

This constant-kernel assertion is essential. A rational quotient depending on A alone would establish a field factorization and would not imply polynomial divisibility.

Finally, det T is integral by its edge-subset definition. det A is primitive since its distinct determinant monomials have coefficients +/-1. A product of primitive multivariate integral polynomials is primitive: reduce modulo any prime and use that a polynomial ring over a field is a domain. Thus its C_n-th power is primitive. Write the rational quotient as (a/b)h with h primitive integral, b>0, and gcd(a,b)=1. The product (det A)^C_n h is primitive. If multiplying it by a/b gives an integral polynomial, b divides every coefficient multiplied by a. Coprimality forces b to divide every coefficient of a primitive polynomial, hence b=1. A zero quotient is already integral. This proves the exact claimed Z-polynomial divisibility, and no claim about the quotient's nonvanishing, irreducibility, or exact exponent follows.

## Current result before historical-note reading

The independent symbolic derivation above finds no mathematical obstruction in the assigned forest/transfer/Gaussian/descent family. It checks all displayed signs and normalizations, including n=1. The final all-n conclusion also needs the constant invariant quotient, Catalan dimension, and determinant character; these were reconstructed here and must be reconciled with the other independent family's final verification. Source identification and fresh executable checks are still pending at this checkpoint. Completion estimate: 45% of assigned review.
