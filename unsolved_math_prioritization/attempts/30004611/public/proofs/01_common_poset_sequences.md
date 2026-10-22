# Common-poset logarithmic sheaf sequences: proved partial construction

Target: Mücksch, *On Yuzvinsky’s lattice sheaf cohomology for hyperplane arrangements*, arXiv:2008.13700v3, Problem 6.3, p. 18. This is a constructive partial answer, not a resolution in every rank and not a novelty claim. It does not identify Euler multiplicity with Ziegler multiplicity.

## 1. Scope and canonical comparison spaces

Let K be any field, let A be a finite central essential arrangement in V=K^ell, ell>=2, and fix H in A with equation alpha=0. Write S=Sym(V*), R=S/(alpha), A'=A\{H}, B=A^H, and m=m^H for the usual Ziegler multiplicity. All functors below are covariant for inclusion of subspaces and hence are sheaves on the upper Alexandrov topology.

Put P=L(A)\{0}, ordered by inclusion. Its logarithmic sheaf is D_X=D(A_X), with actual inclusion maps as structure maps. Put Q={X in P:X⊆H}. This is a lower ideal and hence a closed subspace. The map i:Q→P is its inclusion. There is a canonical identification Q=L(B)\{0}. Let D''_X=D(B_X) and Z_X=D(B_X,m|_{B_X}) on Q, as sheaves of R-modules, also regarded as S-modules through S→R.

For deletion, use P'_geom=L(A')\{0}, removing the literal zero subspace only if it belongs to the lattice. Define the extended deletion sheaf D'_X=D(A'_X) on this poset. If A' is essential, this is exactly the source's sheaf and punctured lattice. If A' is nonessential, its nonzero center T'=intersection(A') is retained. This is an explicit extension of the center-punctured convention; restriction to L(A')\{T'} recovers that convention, but their cohomology need not agree.

Define

c:P→P'_geom,   c(X)=intersection{L in A':X⊆L},

with the empty intersection equal to V. Since X⊆c(X), c(X) is nonzero. It is an order-preserving closure map. The identity A'_{c(X)}=A'_X proves that F:=c^*D' has stalk F_X=D(A'_X).

The inclusion j:P'_geom→P is canonical. For each X in P, the subposet of deletion flats Y with X⊆Y has the least element c(X). Thus, for every sheaf G on P'_geom,

(j_*G)_X=G_{c(X)}.

Consequently c^*G=j_*G, j_* is exact, and H^k(P,c^*G)=H^k(P'_geom,G) naturally for every k. One proof of the cohomology statement is that inverse image is exact, so j_* preserves injectives; together with exactness of j_* and equality of global sections, this gives the assertion. If T'≠0, P'_geom has a minimum T', so its positive-degree cohomology vanishes for every sheaf. No freeness characterization from the essential case is being transferred to that extension.

Likewise i_* is exact: its stalk at X is the original stalk if X∈Q and zero otherwise. It preserves cohomology: H^k(P,i_*G)=H^k(Q,G).

## 2. The geometric coefficient ideal

Let S_P denote the constant covariant sheaf with value S. Define the ideal sheaf I=I_H by

I_X=alpha S if X⊆H, and I_X=S otherwise,

with the evident inclusion structure maps. Equivalently I is the kernel of the canonical map S_P→i_*R_Q. The ideal does not depend on scaling the defining equation alpha.

Every stalk of I is free of rank one, but I is not in general an invertible sheaf or a constant grading shift. In particular, an arrow from Q to its complement has transition alpha S→S. Under generators alpha and 1 this is multiplication by alpha. In the usual coefficient grading, I_X≅S(-1) on Q and I_X≅S off Q.

## 3. Ordinary restriction: exact identified kernel

Define rho:D→i_*D'' by reducing derivations modulo alpha at X∈Q, and by the zero map at X∉Q. At X∈Q, H∈A_X, so derivations preserve (alpha) and reduction is defined. The local identity

(A_X)^H=B_X

holds as arrangements with duplicates removed. Indeed X⊆H, so X⊆L∩H is equivalent to X⊆L. Thus the reduction lands in precisely the named restriction sheaf. Naturality within Q follows from the inclusion maps; naturality across Q→P\Q is immediate because the target structure map is zero. There are no arrows P\Q→Q.

Multiplication defines an injective morphism

mu:I⊗_S F→D.

On Q this is alpha S⊗D(A'_X)→D(A_X); off Q it is S⊗D(A_X)→D(A_X), since H∉A_X there.

At X∈Q, a derivation in ker(rho_X) has every coefficient divisible by alpha. Writing theta=alpha eta, divisibility by the distinct linear forms defining L∈A'_X implies eta(alpha_L)∈alpha_L S, because alpha and alpha_L are coprime. Thus ker(rho_X)=alpha D(A'_X). Conversely alpha D(A'_X) is tangent to every member of A_X and reduces to zero. Off Q, ker(rho_X)=D(A_X)=F_X. This proves, on every poset point, the left-exact sequence with fully identified terms:

0→I⊗F→D→i_*D''.

The cokernel is supported on Q and is exactly the local ordinary restriction defect. The kernel was computed from an independently defined deletion transport and ideal sheaf, rather than being renamed.

## 4. Genuine right exactness in useful classes

The sequence in §3 is short exact if rho_X is onto for every nonzero flat X⊆H. This condition holds unconditionally for ell<=3, over every field.

Here is an elementary proof. The localized arrangement A_X has rank codim_V X≤2. If its rank is one, X=H and A_X={H}; reduction onto Der_K(R) is surjective. If its rank is two, choose linear coordinates z=alpha, t, u_1,...,u_{ell-2}, with X given by z=t=0. Every hyperplane of A_X has equation a z+b t; except for H, b≠0. Consequently B_X consists of the single hyperplane t=0 in H, and

D(B_X)=R t∂_t ⊕ direct_sum_j R∂_{u_j}.

The elements z∂_z+t∂_t and ∂_{u_j} lie in D(A_X) and restrict to the displayed generators. This proves surjectivity without a characteristic assumption.

Thus for every central essential arrangement of ambient dimension 2 or 3,

0→I_H⊗c^*D'→D_A→i_*D_{A^H}→0.                 (O)

A second class is arbitrary rank with H a coloop, equivalently A' nonessential in this essential setting. Choose a vector v spanning T' with alpha(v)=1 and decompose V=H⊕Kv. Every defining form of A' is independent of the alpha coordinate. For X⊆H, reduction is a product-coordinate projection and all derivations of B_X lift with alpha-independent coefficients. Therefore (O) is short exact for a coloop in every rank, even when deletion localizations are not free.

A third sufficient condition is that D(A'_X) is free for every nonzero flat X⊆H. The ordinary free-surjection theorem, applied to each A_X, then proves surjectivity. For a simple arrangement its Euler-multiplicity restriction is the ordinary restriction. The relevant credited result is Abe–Denham, arXiv:2203.04816v3, Theorem 1.2; their text credits the multiplicity-free theorem to earlier work of Abe. This use does not substitute Ziegler multiplicity for Euler multiplicity.

## 5. Parallel canonical Ziegler construction

Define E_X={theta∈D(A_X):theta(alpha)=0} for every X∈P, including X outside H. Inclusions give a sheaf E. Evaluation on the chosen defining equation alpha gives a natural short exact sequence

0→E→D→I_H→0.                                (N)

On Q, all evaluations are divisible by alpha and the Euler derivation evaluates to alpha. Off Q, choose v∈X with alpha(v)=1. The constant derivation ∂_v is tangent to every member of A_X and evaluates to 1. Thus evaluation is onto I_H at every stalk. This proof needs neither a chosen global splitting nor a characteristic assumption. The ideal I_H and the sheaf E are invariant under replacing alpha by lambda alpha for lambda in K^*. The evaluation map itself is natural relative to the chosen equation and changes by multiplication by lambda; the resulting exact sequences are isomorphic through that unit on I_H.

Define pi:E→i_*Z by reduction modulo alpha on Q and by zero elsewhere. To verify the Ziegler multiplicity, take one fiber of the restriction map on hyperplanes. After normalizing equations, its members have equations beta+c_j alpha. Since theta(alpha)=0, theta(beta+c_j alpha)=theta(beta). These distinct linear forms are pairwise coprime, so their product divides theta(beta). Reducing gives beta^m dividing the reduced derivative. This is precisely the Ziegler condition, not the Euler condition.

The same coefficient-division argument proves

ker(pi)=I_H⊗E.

The local defining multiplicity is the actual localized global multiplicity m|_{B_X}: if X⊆L∩H, the entire fiber over L∩H contains X. Naturality is therefore immediate under localization.

For rank(A_X)≤2, use the coordinates above and normalize the other hyperplanes as t+c_j z=0. Put q=product_j(t+c_j z). Then

E_X=S q∂_t ⊕ direct_sum_j S∂_{u_j},

and the target is

Z_X=R t^(number of j)∂_t ⊕ direct_sum_j R∂_{u_j}.

Reduction sends the displayed basis to the displayed basis. Thus, for ell≤3, there is a second genuine short exact sequence

0→I_H⊗E→E→i_*Z→0.                           (Z)

Together (N) and (Z) relate the actual logarithmic sheaf D_A to the named Ziegler restriction, with an independently defined normal-kernel sheaf. The same proof works for a coloop in every rank; its Ziegler multiplicities are all one. More generally local freeness of every A_X with 0≠X⊆H yields Ziegler surjectivity by the classical free Ziegler restriction theorem.

## 6. Cohomology consequence and limits

Whenever (O) is short exact, it yields a natural long exact sequence

...→H^k(P,I_H⊗c^*D')→H^k(P,D_A)→H^k(Q,D_{A^H})→H^(k+1)(P,I_H⊗c^*D')→... .

The I_H factor cannot be dropped or replaced globally by S(-1). Already at the top flat V, both D_V and F_V equal Der_K(S), while (i_*D'')_V=0. Multiplication by alpha has proper image alpha Der_K(S), so the naive globally shifted deletion sequence fails exactness there for every arrangement. To connect its cohomology to genuine deletion cohomology, the following additional short exact sequence is available:

0→I_H⊗F→F→i_*(R⊗_S i^*F)→0.

Stalkwise, this is alpha multiplication on the torsion-free module D(A'_X) on Q, and the identity injection off Q. The middle cohomology is H^k(P'_geom,D') by §1. The last term is the explicitly identified deletion reduction, not silently the ordinary restriction derivation sheaf.

Likewise (N) and (Z) provide genuine long exact cohomology sequences for the Ziegler restriction. No automatic addition–deletion freeness theorem is claimed from these sequences alone.

For ell=2 the restriction is one-dimensional, beyond Mücksch's standing dimension>=2 assumptions. The same functor construction on Q={H} is well defined and (O), (N), (Z) remain true. However its only stalk is Der_K(R), and its global sections need not equal the full module D(A^H). For example, the two-coordinate-line arrangement restricts to a one-hyperplane arrangement in a line; its punctured-poset sheaf has global sections R∂_t, while the derivation module is Rt∂_t. Do not apply the source's global-section or freeness statements across this boundary.

In ranks>=4, local rank>=3 restriction defects may survive at nonzero flats. The universal constructions above remain natural and left exact, but their right exactness is not asserted without a sufficient hypothesis. This does not refute all possible formulations of Problem 6.3. The result here is a rigorously specified common-poset partial answer with actual named deletion and restriction terms, and all off-H points included.

## Public primary sources

- Mücksch, arXiv v3: https://arxiv.org/abs/2008.13700v3 . Definitions of lattice sheaves in §3 and §4; Problem 6.3, p. 18. The published related paper is https://doi.org/10.1007/s00208-022-02499-1 ; no identical numbering or byte identity is assumed.
- Original workshop problem: https://ems.press/content/serial-article-files/46883 , printed p. 288.
- Abe–Denham, arXiv:2203.04816v3, Theorem 1.2: https://arxiv.org/abs/2203.04816v3 . Credited module-level ordinary/Euler-multiplicity surjection theorem.
- Abe–Kawanoue, arXiv:2406.00305v2, pp. 2–3: https://arxiv.org/abs/2406.00305v2 . Distinguishes the Euler and Ziegler maps and their different domains; the displayed sequences there do not assert unconditional terminal surjectivity.

The proof above is an elementary common-poset construction and local computation. The earlier row-992 deletion investigation is reused with credit and is not claimed to resolve this target.
