# Fresh independent derivation: invariant and constant-quotient family

Written before reading any submitted historical AUDIT, ACCEPTANCE, PASS, STATUS, or prior review. Target input is the ten-file snapshot pinned in INPUT_PIN.json, especially PROOF.md SHA-256 546d9df387da3266b1b20d31b1cd6017a65fe9f497f1b37d2a99319e6194755c at PR head e87236a97c4b87818d2768cd5789043c7c3f4e39. This derivation addresses Sections 3 and 5 independently of the other fresh review family. It does not depend on a source's asserted Catalan basis theorem.

## Exact claim and separated obligations

The intended matrix has one row and column for every set partition of [n], not only noncrossing partitions. Its entries are integral polynomial sums of interlayer edge subsets, using exactly one predetermined unweighted block tree in each input partition. The target is divisibility of its determinant by (det A)^C_n in Z[a_ij] for every n >= 1 and generic independent variables a_ij. Exact multiplicity, irreducibility, novelty of this method, and priority are outside the claim.

For the invariant family, the precise obligation is to prove a constant rational surjection Phi from the Bell-dimensional partition space onto W = Lambda(U tensor Q^2)^SL2, with dim W = C_n, and det rho(g) = (det g)^C_n for g in GL(U). Given the additional interface equations Phi L_A = G_A Phi and det(G_A|W) = (det A)^C_n, the ring-level divisibility follows. The two interface equations require the exact forest extraction and Gaussian calculation in Sections 2 and 4; an invariant-space calculation alone does not prove them. They remain explicitly separated here.

## A. Infinitesimal invariants and rank

Let M be a tensor power of the standard complex SL2 module or an exterior power of a direct sum of its copies. Give the standard plus/minus basis the orthonormal Hermitian form, and use the induced tensor or wedge form. Define E to send minus to plus and plus to zero; F sends plus to minus and minus to zero. Extend as sums over tensor slots or degree-zero exterior derivations. Directly on the two-dimensional standard module [E,F] = H, H acts with weights +1,-1, and E* = F. These identities persist under both constructions. In particular no Berezin adjoint convention is being used in this argument.

For a weight-zero v, Ev = 0 implies

    ||Fv||^2 = <v,EFv> = <v,(FE+H)v> = 0.

Thus such a v is killed by E,F,H. Conversely, invariant vectors satisfy those conditions. Since E and F are nilpotent and their exponentials generate the upper and lower unipotent subgroups, and those generate SL2, the invariant subspace is precisely ker(E:M_0 -> M_2).

Surjectivity is a separate step. If w in M_2 is orthogonal to the image of E from M_0, the adjoint identity says Fw=0. Therefore

    2||w||^2 = <w,[E,F]w> = ||Fw||^2 - ||Ew||^2
               = -||Ew||^2.

Positivity forces w=0. The image has no nonzero orthogonal complement, so E:M_0 -> M_2 is onto. Consequently dim M^SL2 = dim M_0 - dim M_2. The sign of [E,F] is essential: replacing it by [F,E] while retaining a positive weight would invalidate this proof. All these operators have integer matrices in the ordinary tensor or wedge bases. Their kernels and ranks over Q equal the corresponding ones over C by extension of scalars, so the argument certifies a rational invariant space as well.

## B. Paired tensor invariants really span

In V^(tensor 2r), weight zero has binomial(2r,r) words and weight two has binomial(2r,r+1). Hence its invariant dimension is Catalan_r. In odd tensor degree the central element -I acts by -1, so there are no invariants.

For a matching M of 1,...,2r, place epsilon = (+ tensor -) - (- tensor +) in each paired set of slots, with the earlier endpoint first. The resulting invariant tensor has 2^r terms. Order words lexicographically with + greater than -. Its largest term is the word with + at every left endpoint and - at every right endpoint, coefficient +1. In any other term, the earliest changed endpoint is a left endpoint, so that term is strictly smaller.

For noncrossing matchings the largest words are distinct: they are Dyck words and the stack rule uniquely reconstructs the matching. The number of such words is binomial(2r,r) - binomial(2r,r+1), using reflection at the first prefix with a surplus of minus signs. Distinct largest terms imply linear independence by choosing the largest largest-term among tensors appearing with nonzero coefficient in an alleged relation. One must not say merely that different matchings give different expanded tensors; crossing matchings have dependencies and may have coinciding largest words. For example (1,3)(2,4) and (1,4)(2,3) both have largest word ++--. Restricting to noncrossing matchings is essential only for this tensor-basis construction.

Their number equals the full invariant dimension, so these tensors form a basis of all invariant tensors. This proof uses neither semisimplicity nor an external first fundamental theorem.

## C. Tensor-to-exterior projection and quadratic generation

Set Z = U tensor V. For k >= 0, the map

    iota(z_1 wedge ... wedge z_k)
       = (1/k!) sum_sigma sign(sigma) z_sigma(1) tensor ... tensor z_sigma(k)

is an equivariant embedding into Z^(tensor k). The exterior projection pi is a left inverse, since pi iota = identity. The factorial inverse is allowed over Q. Thus every exterior invariant has an invariant tensor lift; this avoids making an unjustified claim that an arbitrary equivariant quotient automatically surjects on invariants.

Reordering ordinary tensor slots identifies Z^(tensor 2r) with U^(tensor 2r) tensor V^(tensor 2r), where SL2 acts trivially on the U part. Taking invariants gives exactly U^(tensor 2r) tensor (V^(tensor 2r))^SL2: expand in any basis of the U factor and check each coefficient is invariant. The invariant tensor basis above therefore supplies paired epsilon tensors for every lift.

Exterior projection sends the epsilon pairing in slots with coefficients u,v to

    xi(u) barxi(v) - barxi(u) xi(v)
       = xi(u) barxi(v) + xi(v) barxi(u) = b(u,v).

For multiple pairs, regrouping the slots only supplies the ordinary permutation sign. This sign does not affect spanning. Hence W is spanned by products of b(u,v), including the empty product in degree zero. This proves generation in every degree, rather than only degree two or a numerically inspected degree range.

## D. From the quadratic generators to all partition states

For n>=2 let u_i=e_i-e_n, i<n. In the abstract difference algebra let x_i=xi(u_i), y_i=barxi(u_i). Then

    b(u_i,u_i)=2 x_i y_i=2 q_in,
    q_ij=(x_i-x_j)(y_i-y_j),
    b(u_i,u_j)=q_in+q_jn-q_ij for i!=j.

The diagonal factor 2 is real, not removable by notation. Since we work over Q, q_in=(1/2)b(u_i,u_i) is legitimate. There is no claim here of an integral invariant lattice basis.

All b(u,v) are rational linear combinations of these b(u_i,u_j), so all of W lies in the algebra generated by q_ij. Repeated q edges vanish because q_ij^2=0. For distinct edges, a cycle makes the edge-difference vectors dependent, which makes the unbarred wedge vanish. A forest product depends only on its component partition: its edge vectors are a unimodular basis of the zero-sum lattice on each component, and the determinant sign of a basis change is squared between barred and unbarred wedges. Therefore each surviving monomial is a partition forest product f_P, for an arbitrary partition P.

This proves that the full all-partitions map Phi(e_P)=f_P is surjective. It does not prove independence of all f_P, and that independence would be false once Bell_n > Catalan_n. The constant map is defined entirely over Q and contains no entries involving A, edge weights, row sums, or det A. Its kernel is a constant rational subspace.

## E. Degree dimensions and Catalan total, including endpoints

Let m=dim U=n-1. On Lambda^(2r)(U tensor V), a weight-zero basis vector contains r plus and r minus generators; a weight-two vector contains r+1 plus and r-1 minus generators. Thus

    d_r=binomial(m,r)^2-binomial(m,r-1)binomial(m,r+1), 0<=r<=m.

Binomial coefficients outside [0,m] are zero. Odd degrees have no invariants because -I acts by -1. Vandermonde sums give

    sum_r binomial(m,r)^2=binomial(2m,m),
    sum_r binomial(m,r-1)binomial(m,r+1)=binomial(2m,m-2).

The difference equals Catalan_(m+1). For m=0 and m=1 the second term is zero under the stated convention. For m>=2 one may simplify the factorial quotient directly; this produces the same formula. In particular m=0 gives W=Q, dimension 1=C_1, and no determinant-character division by m is needed.

The explicit formula satisfies d_r=d_(m-r). Pairing the r and m-r terms proves

    sum_r 2r d_r = m sum_r d_r = m d.

The endpoints r=0,m each have dimension one; omitting either would corrupt both the total and the scalar determinant calculation.

## F. The complete GL(U) determinant character

The GL(U) action commutes with SL2 and preserves degree, hence restricts to W. On a diagonal g=diag(t_1,...,t_m), the exterior algebra decomposes into multidegree weight spaces, with weights alpha_i in {0,1,2}. Each multidegree subspace is stable under E,F,H, so W decomposes into intersections with those weight spaces. The determinant of g on W is a single monomial product_i t_i^A_i, where A_i is the sum of the i-th multidegree over a weight basis of W. These are nonnegative integers.

Permutation matrices on U conjugate the diagonal torus and give isomorphic W actions; the determinant is invariant under that conjugation. Thus A_i are all equal to a common A. On tI, degree 2r scales by t^(2r); its determinant is t^(sum_r 2r d_r)=t^(md). On the other hand the torus character is t^(mA), so A=d for m>0.

The formula is now established on all diagonal matrices and therefore on every matrix conjugate to a diagonal matrix over C. Matrices with distinct eigenvalues form a nonempty Zariski-open subset, hence a dense subset, of all m-by-m matrices; its invertible part is dense in GL_m. The entries of the exterior action and of its restriction to a constant rational basis of W are polynomial in the entries of g. Therefore the difference det rho(g)-(det g)^d is a polynomial vanishing on that dense set, so vanishes identically. This certifies every characteristic-zero field by the rational coefficient identity, not only diagonal, scalar, or numerical inputs. It even extends as a polynomial identity to singular g. For m=0 the action on Q is the identity; the n=1 transfer case is treated separately.

## G. Constant quotient to a polynomial determinant divisor

Assume the independently necessary forest interface Phi L_A=G_A Phi and the Gaussian determinant identity det G_A=(det A)^d. Let R=Q[a_ij]. The exact sequence of rational vector spaces

    0 -> N -> V_n -> W -> 0

splits by choosing a rational basis of W and constant rational lifts. Tensoring with R preserves this split exact sequence, so ker Phi_R=N tensor R is a free direct summand. This is stronger and more useful than merely asserting that the kernel has the correct generic dimension. The intertwining equation makes this actual polynomial submodule invariant under L_A.

With a basis of N followed by lifts of a basis of W, the matrix of L_A is block triangular with lower-right block G_A and upper-left block K_A over R. The basis and its inverse have only rational constant entries; this excludes all denominators involving A, row sums, or det A. No generic eigenvector construction is involved. Column-vector conventions yield L_A(P-column,Q-row)=T(P,Q), so L_A has matrix T-transpose and det L_A=det T.

Taking determinants gives det T=(det K_A)(det A)^d as an identity in Q[a_ij]. This has much stronger content than generic spectral equality: the quotient factor is an actual polynomial, not a rational function that can carry an inverse power of det A.

Finally det T is integral by its edge-subset definition and det A is primitive. Its power remains primitive by multivariate Gauss's lemma. For a rational quotient h, factor its coefficient content as a/b times an integral primitive h_0 with gcd(a,b)=1. The product (det A)^d h_0 is primitive, and integrality of a/b times that product forces b=1. Thus the quotient is integral. This also handles det T=0. Nothing proves exact exponent, and none is required. For n=1 the graph condition forces the unique X-Y edge, giving T=[a_11] and the claimed exponent C_1=1 directly.

## H. Exact interface to the other proof family

The invariant family supplies an all-partitions constant surjection and its determinant character. The separate proof family must establish, with the same generator order and edge-subset counting:

1. G_A f_P = sum_Q T(P,Q) f_Q, including +1 surviving signs and no internal-tree multiplicity.
2. On W tensor Q(a_ij), G_A=(det D) M_S rho(g_B) H_D, where B=D^-1 A has B 1=1, S=E-A^T D^-1 A is symmetric with zero row sums, and det g_B=det A/det D for the row-coefficient hyperplane U.
3. H_D lowers exterior degree with identity degree-preserving part, M_S raises it with identity degree-preserving part, and both preserve the actual W. These are the reasons their determinants equal 1.
4. The calculation initially inverts nonzero row sums only in the fraction field; the original G_A matrix has polynomial entries on the constant space W, so the final determinant equality is polynomial and specializes at zero row sums.

I checked the stated algebraic interface for consistency: the row-vector convention, quotient eigenvalue 1, scalar factor (det D)^dim W, the order rho(g_B) H_D, and the symmetric difference-quadratic S are compatible with the independently derived determinant character. My invariant-family verdict is conditional on the exact transfer/operator identity being verified by its assigned family. Neither this conditional interface nor finite checks is being presented as an independent verification of every edge-subset transfer matrix entry.

## Preliminary result before source/history comparison

No mathematical gap or counterexample was found in the invariant-generation, Catalan dimension, determinant character, or constant-kernel polynomial lifting mechanisms. The all-n arguments are checkable and include m=0,n=1, rational normalization, and integer descent. Fresh exact computational checks and deliberate incorrect variants are being constructed next; those checks will be reported separately with reproducible code and outputs. Historical acceptance has not been used as evidence.
