# Independent derivation before inherited audits

Frozen inputs: TeX SHA256 8eb445dc33481825b99cdec1001cd425b6961903472873282d5ddc1d9ce8285b; PDF SHA256 9ed04da332b9815dd91a7fe25b76217f788228ce3b1a75ff5ccd2193750fb95e. I read the entire current TeX first. No historical root derivation, family derivation, PASS report or verdict was read before this file was written. This is my all-n mathematical reconstruction and attempted falsification, not a conclusion inherited from those files.

## Exact target

For each n >= 1, A has n² independent commuting entries in Z[a_ij]. T is indexed by all Bell partitions. The input partition has one arbitrary fixed unweighted tree on each block. Each interlayer edge subset appears once, and survives only if the resulting graph is a forest and every component meets the output layer Y; its output state is the component-intersection partition on Y. The target is divisibility by (det A)^C_n over Z[a_ij]. No exact valuation, irreducibility or complementary factor is claimed. This statement permits nonsymmetric, nonplanar, signed, singular and zero-row-sum specializations. A calculation only on noncrossing states, positive matrices or nonzero numerical row sums would not suffice.

## Forest product, orientation, normalization

In an exterior algebra take two odd generators ξ_v and ξ̄_v per vertex and q_uv=(ξ_u−ξ_v)(ξ̄_u−ξ̄_v). These q have degree two, commute, square to zero and do not depend on edge orientation. For s edges with incidence row vectors u_e, reordering the bars gives

q_H = (−1)^(s(s−1)/2) [∧_e ξ(u_e)] [∧_e ξ̄(u_e)].

A cycle makes the incidence vectors dependent, annihilating the first wedge. A tree on B has |B|−1 edge incidence vectors that form an integral basis of the sum-zero lattice on B: each e_v−e_root is an integral path sum and these vectors already form a basis. Therefore the change between any two trees has determinant ±1. Both wedges undergo the same change, so its squared determinant equals +1. Thus all tree choices on each block give the same exterior product f_P, including singleton product 1. This argument establishes representative independence without averaging over trees.

Order X pairs first, and let I_X extract Ω_X=ξ_x1 ξ̄_x1 ... ξ_xn ξ̄_xn on the left. The exponential of ∑ a_ij q_xiyj equals ∏(1+a_ij q_xiyj) because its even summands commute and square to zero. Its expansion has exactly one term a_E q_E per subset: there is no factorial, multiplicity, tree count or rooted count. Multiplying by f_P produces the selected forest/cycle product. Cycles vanish. A component containing k X vertices and no Y vertex has total degree 2(k−1), and cannot supply all 2k X generators, so vanishes under I_X.

For every surviving forest, select a Y root in each component and replace its exterior tree product by the star at that root; this is the established tree equality for that particular edge subset and introduces no new subsets. Each X leaf pair can arise only from the +ξ_x ξ̄_x term of q_xy. The pair is even, so extracting every X pair contributes +1 without permutation signs. What remains is exactly the star forest on the Y component intersections, i.e. f_Q. Therefore G_A f_P=∑_Q T(P,Q) f_Q exactly, with the required sign +1 and arbitrary fixed input trees.

## Constant image, generation and dimensions for every n

Let U={row u∈Q^n: u1=0}, m=n−1, and V=Q² standard SL₂ module. The difference algebra is Λ(U⊗V). Its invariant algebra W contains every f_P. It remains necessary to prove that all Bell f_P span W, and that dim W=C_n; merely citing a finite rank table is insufficient.

On tensor powers of V and exterior powers of a direct sum of its copies, choose their induced Hermitian form with E*=F and [E,F]=H. For a weight-zero v with Ev=0, ||Fv||²=<v,EFv>=<v,(FE+H)v>=0. Thus invariants are precisely ker(E:M₀→M₂), since E,F exponentiate to the two elementary SL₂ subgroups, which generate the group. If w∈M₂ is orthogonal to E M₀, then Fw=0. Hence 2||w||²=<w,[E,F]w>=−||Ew||², forcing w=0. E:M₀→M₂ is onto. Invariants therefore have dimension dim M₀−dim M₂. Rational coefficient matrices allow descent of these dimensions to Q. This proof applies at every tensor/exterior degree and does not assume complete reducibility as an unexplained central step.

For V^(⊗2r) the weight difference is binom(2r,r)−binom(2r,r+1)=C_r. Noncrossing matchings of 2r slots give C_r invariant epsilon tensors with ε=e_+⊗e_−−e_−⊗e_+. The bijection with Dyck words is the stack matching, with reflection counting non-Dyck balanced words. In lexicographic order e_+>e_−, a matching tensor's leading word has plus at all left endpoints, minus at right endpoints, coefficient +1. Reversing any pair first changes a left endpoint from plus to minus, producing a lower word. Different noncrossing matchings give different leading Dyck words. In a relation choose the greatest participating leading word; smaller leading words cannot cancel it. Thus these tensors are independent, attain the dimension, and span all tensor invariants. Odd tensor degrees have none because −I acts negatively. This is a basis device for invariant tensors, not a restriction of T to planar or noncrossing states.

For k=2r, the map
ι(z₁∧...∧z_k)=1/k! ∑_σ sgn(σ) z_σ1⊗...⊗z_σk

is an equivariant embedding into the tensor power, and exterior projection π is its left inverse because each permutation contributes the same exterior product after multiplying by its sign. Rearranging ordinary tensor factors identifies tensor invariants with U^(⊗2r)⊗(V^(⊗2r))^SL₂. Their exterior projections are products, up to slot reordering signs, of

ξ(u)ξ̄(v)−ξ̄(u)ξ(v)=ξ(u)ξ̄(v)+ξ(v)ξ̄(u)=b(u,v).

The second equality uses odd anticommutation. This explicitly fixes epsilon and factor normalization. With u_i=e_i−e_n, b(u_i,u_i)=2 q_in and b(u_i,u_j)=q_in+q_jn−q_ij. Since char 0 permits division by 2, the q_ij generate W. Each q-monomial with repeated edge vanishes; each with a cycle vanishes; every other one is a forest and hence some full Bell f_P. The constant map Φ:e_P↦f_P from the whole partition space onto W is therefore surjective.

Degree 2r has weight-zero dimension binom(m,r)² and weight-two dimension binom(m,r−1)binom(m,r+1), so

d_r=binom(m,r)²−binom(m,r−1)binom(m,r+1).

Vandermonde gives ∑d_r=binom(2m,m)−binom(2m,m−2)=C_(m+1)=C_n, with out-of-range terms zero. Complementation gives d_r=d_(m−r), and pairing degrees yields ∑2r d_r=m d. This checks m=0 too: W=Q, d=1. It is separated below because the scalar character argument divides by m.

## Determinant character without specialization assumptions

The action ρ(g) of GL(U) on W is a polynomial exterior substitution action. For diagonal g its determinant is a monomial ∏t_i^α_i: W decomposes into torus weight spaces because its defining equations commute with that torus. Conjugation by coordinate permutations makes the exponents equal α. On scalar tI the determinant is t^(∑2r d_r)=t^(md), while the diagonal formula gives t^(mα). For m>0, α=d. Thus detρ(g)=(det g)^d for diagonal g. Conjugation extends this to diagonalizable invertible matrices. Invertible matrices with distinct eigenvalues form a dense open set over C; the two sides are polynomial functions, so equality extends everywhere and descends to Q and all characteristic-zero extensions. It cannot be a conclusion solely from scalars: the torus exponent symmetry step is essential and is supplied here.

## Gaussian factorization and its sign

Work over K=Q(a_ij), temporarily allowing inverses of the generic nonzero row sums r_i. Define D=diag(r_i), E=diag(c_j), B=D^(−1)A, S=E−AᵗD^(−1)A. B1=1, Sᵗ=S and S1=0. Expanding without interchanging odd factors gives

∑a_ij q_xiyj=(ξ−Bη)ᵗD(ξ̄−Bη̄)+ηᵗSη̄.

The top extraction convention gives I_z exp(zᵗDz̄)=∏r_i=det D, without a factor (−1)^(n(n−1)/2), because the reference top monomial is ordered as paired generators. This is the convention that must be audited; unpaired reference order would change the coefficient.

Define H_D f(ξ,ξ̄)=(det D)^(−1) I_z [exp(zᵗDz̄) f(z+ξ,z̄+ξ̄)]. Because f uses differences, extraction leaves only differences among ξ generators. Simultaneous SL₂ action on z and ξ preserves the exponential, paired top form and translation, so invariants are preserved. The z-free term in f contributes f exactly by the displayed normalization. Every other surviving f-term supplies a positive even number of z generators: for each index the Gaussian supplies the whole z_i z̄_i pair or nothing. It strictly reduces the remaining ξ-degree. Thus H_D on W is degree-lowering triangular with identity on each diagonal degree block, determinant 1.

Multiplication M_S by exp(ηᵗSη̄) preserves the difference algebra since row/column sums vanish and ηᵗSη̄=∑_(i,j<n) S_ij(η_i−η_n)(η̄_j−η̄_n). Its symmetric coefficients express this quadratic as a combination of b(u_i,u_j), with diagonal using half b(u_i,u_i). It is invariant. Consequently M_S preserves W and is degree-raising triangular with unit diagonal, determinant 1.

For row u, ξ=Bη is u↦uB. Since B1=1, U is preserved and the 1-dimensional quotient of Q^n by U acts as identity. Thus det(g_B)=det B=det A/det D. Odd translation ξ=z+Bη leaves the integrated top coefficient unchanged: only a monomial already containing all old integrated generators can supply all new ones, and its paired top coefficient is +1. All exponential arguments are even. Substitution in the completed square now gives the ordered identity

G_A=(det D) M_S ρ(g_B) H_D.

H_D must act first. In general it does not commute with the substitution or M_S, and I have not moved it across them. Its extracted result evaluated at ξ=Bη is exactly the expression f(z+Bη) required by the translated integral. Taking determinants on the d-dimensional W gives (det D)^d×1×(det A/det D)^d×1=(det A)^d. Both the overall sign and scalar are +1, fixed by paired top extraction and the unit diagonal factors.

Before any localization, G_A on W had polynomial entries: the intertwining identity and constant spanning Bell images ensure this on a fixed rational basis. Therefore the determinant equality proved in K holds in Q[a_ij]. It specializes to singular A, any or all vanishing row sums, and arbitrary signed matrices. One need not define the rational intermediate factors at those exceptional inputs.

## Constant splitting and integral lifting

Let L_A e_P=∑_Q T(P,Q)e_Q. Its column convention is Tᵗ, so det L_A=det T. Intertwining is ΦL_A=G_AΦ. Since Φ is a constant rational surjection, extend a rational kernel basis by fixed rational lifts of a W basis; this is an honest A-independent basis of the entire Bell space. Scalar extension gives kernel N⊗Q[a_ij], and intertwining makes it invariant. L_A is block upper triangular with polynomial kernel block K_A and quotient block G_A. Therefore det T=det K_A×(det A)^C_n over Q[a_ij]. No variable-dependent splitting, nonfree kernel, localized denominators or rank inference is involved.

T is an integer polynomial matrix by its subset definition. det A is primitive (nonzero coefficients ±1); its power and its product with any primitive integer polynomial remain primitive by multivariate Gauss. Write a rational quotient as (a/b)h with h primitive integral and coprime a,b. Integrality of (a/b)(det A)^C_n h implies b=1, proving divisibility in Z[a_ij], even when the quotient is zero. For n=1 there is one Bell state and only the single interlayer edge meets the requirement, so T=(a₁₁) and C₁=1. This supplies the omitted m=0 character case.

## Initial adversarial assessment

I attempted to break the argument at the repeated-edge expansion, tree basis sign, integration without Y roots, epsilon plus/minus convention, factor 2 for diagonal quadratic invariants, tensor-to-exterior surjectivity, leading word dependence, scalar-only character inference, lowering-order commutation, row-versus-column hyperplane, zero-row-sum specialization, rational kernel splitting and integral quotient. The current TeX supplies each necessary step. I find no all-n mathematical gap in Sections 1–5 on this first independent reconstruction. This conclusion is provisional pending primary-source, whole-package and page inspections; it is not a publication-readiness assertion.
