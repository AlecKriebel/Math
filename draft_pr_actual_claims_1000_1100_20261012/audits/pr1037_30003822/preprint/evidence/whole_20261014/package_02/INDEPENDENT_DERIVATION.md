# Independent whole-proof derivation, before historical verdicts

Scope: Derived after reading the current candidate mathematics, but before reading previous reviewers' verdicts, reports or root acceptance labels. This is an adversarial logical reconstruction; no receipt is used as a proof premise.

## Exact claim and normalization
For n>=1, T is indexed by every set partition on both sides, one fixed unweighted tree per input block, and each admissible X-Y edge subset once. Admissibility: fixed input forest plus E acyclic; each component touches Y; Y intersections yield Q, including isolated singleton Y. Target: det(A)^C_n divides det(T) over Z[a_ij]. Success requires all-n proof, no assumptions of positive/symmetric/planar weights, no numerical row-sum restrictions. Exact exponent, cofactor irreducibility and factorization are outside scope.

## Forest/exterior interface
Set q_uv=(xi_u-xi_v)(barxi_u-barxi_v). These even nilpotents commute. For s edges, regrouping gives (-1)^(s(s-1)/2) times unbarred edge wedge times barred edge wedge. Cyclic incidence vectors are dependent. A tree gives a Z basis of the zero-sum lattice on its vertex set by root-path sums; changing the tree has unimodular determinant +/-1 in both wedges, whose square is +1. Hence forest product depends on partition, with singleton factor 1.

The exponential is precisely product (1+a_ij q_xiyj); no factorial or tree sum. For each selected forest meeting Y, replace each component tree by the star at a Y root as an identity, not as an additional selection. All X vertices become leaves, so top X coefficient must select xi_x barxi_x from each leaf edge; coefficient +1 and even pairs prevent reorder signs. The remaining edges yield f_Q. An X-only component of k vertices has degree 2(k-1), too little for all 2k X generators. Cycles give zero. Thus G_A f_P=sum_Q T(P,Q) f_Q under paired top coefficient extraction.

## Constant Catalan image
U is the zero-sum row subspace of Q^n, m=n-1. W=Lambda(U tensor Q^2)^SL2. For tensor/exterior modules with E*=F and [E,F]=H, ker(E:M0->M2) is invariant: E v=0 at weight0 implies norm(Fv)^2=0. Surjectivity follows since orthogonal complement in weight2 has Fw=0 and 2||w||^2=-||Ew||^2. Hence dim invariants=dim M0-dim M2. Rational kernels allow descent.

In degree2r, d_r=binom(m,r)^2-binom(m,r-1)binom(m,r+1). Sum is binom(2m,m)-binom(2m,m-2)=C_(m+1)=C_n; symmetry d_r=d_(m-r) gives sum 2r d_r=m C_n. No odd degrees survive -I.

For invariants in V^(tensor2r), noncrossing epsilon-pair tensors have distinct lexicographic Dyck leading words, each coefficient1; select the largest leading word to prove independence. The same weight formula gives exactly C_r, so they span. Equivariant antisymmetrization embeds exterior invariants into tensor invariants and projection gives products b(u,v)=xi(u)barxi(v)+xi(v)barxi(u). With u_i=e_i-e_n, b(u_i,u_i)=2q_in, b(u_i,u_j)=q_in+q_jn-q_ij. Thus all invariant elements are spanned by products of q_ij. Repeated edges or cycles vanish, all other products are f_P. All Bell partitions span W. Phi:e_P->f_P is constant rational surjective; no noncrossing restriction on T.

For g on U, det rho(g) is torus monomial product t_i^alpha_i, permutation conjugacy equalizes exponents; scalar tI gives total exponent m C_n, so alpha_i=C_n when m>0. Dense diagonalizable matrices extend det rho(g)=(det g)^C_n; this is a polynomial identity.

## Ordered Gaussian elimination
Over K=Q(a_ij), D=diag(row sums), E=diag(column sums), B=D^-1 A, S=E-A^t D^-1 A. B1=1, S symmetric, S1=0. Complete exponent as (xi-B eta)^t D(barxi-B bareta)+eta^t S bareta, with unchanged odd factor order. Translation preserves top extraction coefficient1.

H_D f=(det D)^-1 I_z[exp(z^t D barz) f(z+xi,barz+barxi)] remains in differences and is SL2-equivariant: each z_i barz_i and top paired z form are invariant. Its degree-preserving term is f because I_z exp(...)=det D. Any other survivor supplies a complete pair from f and lowers remaining degree. Thus H_D is unipotent by degree. M_S multiplies by exp(eta^t S bareta): zero sums rewrite this in differences and symmetry makes it a quadratic SL2 invariant; raising degrees makes determinant1. Substitution acts on rows u->uB, preserves U and acts identically on ambient quotient, hence det g_B=det A/det D.

Exact composition G_A=(det D) M_S rho(g_B) H_D (rightmost acts first). No commutation of H_D and rho is asserted: it is generally false. Taking determinants gives exactly (det A)^C_n, including constant +1. The identity was computed over K but G_A is already a polynomial matrix on constant W, so all exceptional row-sum inputs follow by polynomial identity. Singular and signed inputs cause no exclusions.

## Full Bell determinant and integral lifting
The matrix of L_A:e_P->sum_Q T(P,Q)e_Q is T^t, so determinants agree. Phi L_A=G_A Phi. Constant rational N=ker Phi extends to N tensor R exactly, so choose constant rational N basis plus lifts of W basis to obtain block upper triangular L_A with polynomial kernel block over Q[a]. This yields det T=det K_A(det A)^C_n, without variable denominators. det A has content1 and its power remains primitive by multivariate Gauss. If rational quotient=(a/b)h with h integral primitive, product is primitive, so integrality of det T forces b=1. Zero quotient trivial. n=1 separately: only E={x1y1} is admissible, T=[a11], C1=1. n=0 is outside asserted domain. No exact multiplicity follows.

## Adversarial risks targeted next
Check column/row transpose, paired extraction signs, antisymmetrization/leading-word independence, H/rho order failure controls, arbitrary internal tree invariance, singular/zero/signed/zero-row cases, source claim matching and exact PDF/ZIP custody. Mathematical proof appears complete at this stage but source/package verdict remains pending.
