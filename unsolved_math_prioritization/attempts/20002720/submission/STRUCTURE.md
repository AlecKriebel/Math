# Scalar boxed convolution: an explicit audit of the known structural answer

This is a verification note, not a novelty claim. The Hopf-character description is due to Mastnak and Nica; the faithful-matrix interpretation of a multivariable S-transform is explicitly proposed by Friedrich and McKay. The arguments below specify which parts of that algebraic answer are valid without importing stronger statements about minimal representations, arbitrary tuples, or the full center.

## 1. Exact setting

Fix a finite integer s >= 1 and a commutative unital ring R. The original problem has R = C. Variables z_1,...,z_s do not commute. All series have zero constant coefficient; there is no convergence condition. For a nonempty word w = i_1...i_n and an ordered subset B of positions, w|B retains the original order. Put

    f[w;pi] = product over B in pi of f[w|B],
    (f box g)[w] = sum over pi in NC(n) of f[w;pi] g[w;K(pi)].

K is the right Kreweras complement. In permutation form it is p_pi^(-1)(1 2 ... n); its blocks are the cycles of that permutation. In particular K(0_n)=1_n, K(1_n)=0_n and |pi|+|K(pi)|=n+1. The scalar boxed law is associative, with identity e = sum_i z_i. Associativity is a standard property of this law, assumed in AIM Problem 5.2 and also established by the Hopf coassociativity proof of Mastnak--Nica, Section 3. Its identities are integer polynomial identities and therefore remain valid over any commutative R: they hold over C for arbitrary coefficient assignments, so every polynomial coefficient vanishes over Z.

The unit group is denoted G_s(R). Its normalized subgroup U_s(R) consists of the series with all linear coefficients 1. The claim about noncommutativity below assumes R is not the zero ring. No positivity, traciality, self-adjointness, or analytic realizability restriction is imposed on the formal series.

## 2. Units and the central factor

A series f is a unit if and only if each f[i] is a unit of R. Necessity follows from (f box g)[i]=f[i]g[i]. For sufficiency, construct a right inverse recursively. Set r[i]=f[i]^(-1). For |w|=n>=2, let A_w=product_j f[i_j], and put

    r[w] = -A_w^(-1) sum_{pi != 0_n} f[w;pi] r[w;K(pi)].

Every right-inverse coefficient on the right has word length < n. The recursion forces f box r=e. Independently, a left inverse l is obtained by

    l[i]=f[i]^(-1),
    l[w]=-A_w^(-1) sum_{pi != 1_n} l[w;pi] f[w;K(pi)].

Then l box f=e, and associativity gives l=l box(f box r)=(l box f)box r=r. These divisions use only the stipulated units, so zero divisors cause no problem.

For lambda in (R^times)^s let D_lambda=sum_i lambda_i z_i. Only the discrete partition contributes to D_lambda box f, and only the one-block partition contributes to f box D_lambda. Hence

    (D_lambda box f)[w] = (f box D_lambda)[w]
                        = (product_j lambda_{i_j}) f[w].

Thus the linear torus is central. Set lambda_i=f[i] and

    u[w] = f[w] / product_j lambda_{i_j}.

Then u is normalized and f=D_lambda box u uniquely. Since the section is central,

    G_s(R) is canonically isomorphic to (R^times)^s x U_s(R).

This is a direct product, not merely a potentially nontrivial semidirect product. It does not identify the whole center.

## 3. Hopf coordinates and a concrete faithful representation

Let H_s=Z[Y_w : |w|>=2], an ordinary commutative polynomial algebra. Set Y_i=1 for one-letter words. Give Y_w weight |w|-1. Define

    Delta(Y_w)=sum_{pi in NC(|w|)} Y[w;pi] tensor Y[w;K(pi)],
    epsilon(Y_w)=0.

Extend both maps multiplicatively. Mastnak--Nica, Definition 3.2, Lemma 3.4, and Proposition 3.6 verify this connected graded Hopf algebra over C; the same integer polynomial argument gives the integral construction. The grading follows directly because the weights of a coproduct term are n-|pi| and n-|K(pi)|, whose sum is n-1. The antipode exists recursively because H_0=Z and all reduced coproduct factors have lower weight.

Characters H_s -> R correspond bijectively to u in U_s(R) via chi_u(Y_w)=u[w]. Their convolution law agrees term by term with boxed convolution. This is the normalized-group structure in Mastnak--Nica, Theorem 1.2 / Proposition 3.7. Over C, one may equivalently describe U_s as the BCH group of the completed Lie algebra of infinitesimal characters, using convolution logarithm and exponential. Convolution powers in these formal series terminate on each fixed weight; no analytic exponential is intended.

Here is a concrete faithful matrix construction which avoids a claim of unique minimality. Let V_d be the free R-module with basis the monomials in the Y_w of total weight <= d. There are finitely many because s is finite and all generators have positive weight. Define

    T_u(h) = (id tensor chi_u) Delta(h),  h in V_d.

Coassociativity gives T_u T_v = T_(u box v), with the usual column-vector matrix convention. The order is as written, not reversed. Every T_u is invertible, with inverse T_(u^(-1)). If monomials are ordered by increasing weight, T_u(h)-h has strictly smaller weight. Hence its matrix is upper triangular with every diagonal entry 1.

Moreover epsilon(T_u(Y_w))=u[w]. Therefore the representation on V_d detects every coefficient with |w|<=d+1 and gives a faithful representation of the degree-(d+1) quotient. The representations for increasing d restrict compatibly. Their entire family is faithful on the full normalized group.

Combine this family with the diagonal matrix diag(lambda_1,...,lambda_s) of the central factor. This gives an explicit injective homomorphism from G_s(R) to a group of compatible upper-triangular matrices. The direct-product proof shows the two blocks multiply independently. Thus a faithful matrix-valued multiplicative transform exists for every finite s, with no appeal to minimality or arbitrary choices beyond an ordering of a specified monomial basis.

For tuples a with phi(a_i) invertible, set S_reg(a)=rho(R_a), where rho is the representation just constructed. For two freely independent families with invertible means, the multiplication formula for R gives

    S_reg(a_1 b_1,...,a_s b_s)=S_reg(a) S_reg(b).

Faithfulness concerns their formal distributions (equivalently their R-series), not distinct tuples in an arbitrary algebra. This is the formal matrix-valued meaning of the higher S-transform used by Friedrich--McKay. It is not asserted to be a canonical smallest matrix model or an analytic transform on positive measures.

For s=1 the classical scalar transform F(f)=f^(-1,composition)(z)/z identifies G_1(C) with C[[z]]^times, as in Nica, Notation 14.2 and Theorem 14.3. The regular representation is a redundant faithful encoding of the same group, from which f and consequently F(f) can be recovered. It need not literally equal the scalar series F(f).

## 4. Filtration and noncommutativity

For m>=2 put F^m U_s={u : u[w]=0 for 2<=|w|<m}. Projection to coefficients of word length <m is a group homomorphism, so F^m is normal. For normalized f,g,

    (f box g)[w] = f[w]+g[w]
                  +sum_{0_n<pi<1_n} f[w;pi]g[w;K(pi)].

It follows that F^m/F^(m+1) is the additive group R^(s^m). If f is in F^p and g in F^q, a surviving internal term requires a block of pi of size >=p and a block of K(pi) of size >=q. Thus

    n-|pi|>=p-1,  n-|K(pi)|>=q-1,
    n-1>=p+q-2.

All internal terms vanish when n<p+q-1. Therefore

    [F^p U_s,F^q U_s] is contained in F^(p+q-1) U_s.

The degree-N quotient U_s/F^(N+1) has dimension sum_{m=2}^N s^m over a field, has a faithful unitriangular representation as above, and is nilpotent of class at most N-1. The full group is the inverse limit of these quotients. Over C this is a pro-unipotent group. A degree-N quotient must not be confused with degree-N polynomials embedded in the full group.

In degree three the three intermediate noncrossing partitions yield

    (f box g)[ijk]=f[ijk]+g[ijk]
                 +f[ij]g[jk]+f[jk]g[ik]+f[ik]g[ij].

Take f=e+z_1 z_1 and g=e+z_1 z_2. Then (f box g)[121]=1 while (g box f)[121]=0. This proves noncommutativity for s>=2 over every nonzero commutative ring. It also proves that no faithful homomorphism to an abelian multiplicative group can exist. It does not rule out the matrix-valued construction in Section 3.

## 5. Center bounds and adversarial controls

There is more in the center than the linear torus. Let h be radial: h[w]=c_|w|. The value h[w;pi] depends only on the block sizes of pi. In the sum for h box f, change variables rho=K(pi). The partitions K^(-1)(rho) and K(rho) differ by a cyclic rotation, since K^2 is rotation. They have the same block sizes. Hence the result is exactly f box h. In particular Zeta_s, whose coefficient at every nonempty word is 1, is a nonlinear central unit. The whole center Z(U_s) for s>=2 is not classified here, and was not separately demanded in the printed question. No claim that the torus exhausts Z(G_s) is valid.

Three simple tests prevent overreading the literature:

1. The degree-two coordinates of a normalized product add. By central splitting the map f -> (u[ij]) is a homomorphism from G_s to an additive group. Every commutator has all these coordinates zero. The element e+z_1^2 does not. Thus the equality [G_s,G_s]=U_s printed as equation (35) in Friedrich--McKay is false over any nonzero commutative ring. For s=1 the whole group is abelian, making the failure especially immediate.
2. In one variable, (z+z^2) box (z+z^2) has coefficient 3 at z^3 over C. The finite-degree polynomial sets are therefore not subgroups of the full formal group, contrary to the ascending-subgroup wording in their Proposition 6.3(2). The correct finite objects are quotients; their inverse-limit statements can be used in that corrected sense.
3. Commutative coefficient rings are essential. If coefficients are 2x2 matrices and one naively keeps the scalar formula, take f=Az, g=Bz, h=z+z^2, where A=((1,1),(0,1)) and B=((1,0),(1,1)). The degree-two coefficients of (f box g) box h and f box (g box h) are respectively ABAB=((5,3),(3,2)) and A^2 B^2=((5,2),(2,1)). Associativity fails. This is not the operator-valued free-probability theory, which has different operations.

The short 2013 announcement also defines its representation on the normalized group before writing a transform for arbitrary tuples. Both announcements require an invertible-mean restriction to use a group representation. The longer preprint uses the full unit group but still overstates its tuple domain and does not establish a canonical unique minimal representation. None of these overstatements are premises of Sections 2--4.

## Verification scope

The exact finite program checks 1,980 assertions, including Catalan/Kreweras controls through size 7; products and inverse recursions over Q and Z/4Z, Z/8Z, Z/9Z; the filtration through degree 6; and faithful regular-representation multiplication in dimensions 12, 23 and 91. This supplies reproducibility and falsification controls, not an alternative to the general arguments or expert review.
