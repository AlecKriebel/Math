# Author turn 4: extensions with a flat duality quotient

## 1. Result and conventions

Call a group good if it is of type FP (a finite-length resolution of the trivial integral module by finitely generated projectives) and its total regular-coefficient cohomology is finitely generated as a **right** group-ring module. This is the exact convention in the source gate, not FP-infinity.

**Theorem.** Suppose

\[
1\longrightarrow N\longrightarrow G\longrightarrow Q\longrightarrow1
\]

is a group extension, N is good, and Q is FP with

\[
H^p(Q;\mathbb ZQ)=0\quad(p\ne d),\qquad
D=H^d(Q;\mathbb ZQ)\text{ torsion-free over }\mathbb Z.
\]

Then G is good. More precisely, writing M_q=H^q(N;ZN), there is a canonical right G-action on M_q extending its usual right N-action, and

\[
H^{d+q}(G;\mathbb ZG)\cong D\otimes_{\mathbb Z}M_q,                 \tag{1}
\]

where

\[
(z\otimes m)g=(z\bar g)\otimes(mg).                              \tag{2}
\]

All other degrees are zero. No splitting of the extension is required. The hypothesis on Q is the usual integral duality-group hypothesis with its Z-flatness explicitly included; it is not a claim that concentration alone implies flatness. This argument uses standard Hochschild--Serre and duality machinery and carries no priority claim.

## 2. G is FP

Let the finite projective resolution lengths for N and Q be a and b. For every left ZG-module A, the Hochschild--Serre spectral sequence is

\[
E_2^{p,q}=H^p(Q;H^q(N;A))\Longrightarrow H^{p+q}(G;A).             \tag{3}
\]

It is confined to 0<=p<=b, 0<=q<=a, so cd(G)<=a+b. Each cohomology functor for N and Q commutes with filtered direct limits, by computing with its finite-type projective resolution. The equivariant N-cohomology functor does so in the category of Q-modules as well: the underlying isomorphism is natural and hence respects the quotient action. Filtered direct limits are exact, and the spectral sequences have uniformly bounded finite filtrations. Comparing (3) for a filtered system therefore shows that every H^n(G;-) commutes with filtered direct limits. The finite-cohomological-dimension FP criterion now gives G of type FP.

This criterion is explicitly recalled after Theorem 3.3 on p.5 of Davis, *Poincare duality groups* (already bound in SOURCE_MANIFEST). Alternatively it follows from the usual FP-infinity filtered-colimit criterion and truncating a finite-type resolution at the finite cohomological dimension. The cohomological Hochschild--Serre construction and naturality used in (3) are Theorem 4.3.12 of Sharifi's *Homological Algebra*, bound additively in SOURCE_ADDITION_T4.

## 3. The right G-action on the kernel cohomology

On inhomogeneous N-cochains with coefficients ZN define

\[
(C_g f)(n_1,\ldots,n_q)
=g f(g^{-1}n_1g,\ldots,g^{-1}n_qg)g^{-1}.                         \tag{4}
\]

Normality of N makes this well-defined; conjugation respects the differential, and C_g C_h=C_{gh}. Define on cohomology

\[
m\cdot g=C_{g^{-1}}m.                                            \tag{5}
\]

This is a right action. For n in N it is the natural coefficient right multiplication. Here is the inner-action verification, including its homotopy. In the homogeneous bar resolution, the map

\[
R_n(n_0,\ldots,n_q)=(n_0n,\ldots,n_qn)
\]

is N-equivariant. The prism

\[
h_q(n_0,\ldots,n_q)=
\sum_{i=0}^q(-1)^i(n_0,\ldots,n_i,n_i n,\ldots,n_q n)
\]

satisfies partial h+h partial=R_n-id by cancellation of the interior faces. Thus precomposing homogeneous cochains with R_n acts as the identity on cohomology. In inhomogeneous coordinates this precomposition is the usual inner action

\[
f\longmapsto [\,(n_1,\ldots,n_q)\mapsto
 n f(n^{-1}n_1n,\ldots,n^{-1}n_qn)\,].
\]

The operator C_n is this operator followed by coefficient right multiplication by n^{-1}. Hence C_n(m)=mn^{-1}, and (5) gives m dot n=mn as asserted. No inner action on the coefficient bimodule has been discarded.

## 4. A bimodule identification with the quotient regular module

Finite-type projectives for N give the natural right G-module identification

\[
H^q(N;\mathbb ZG)\cong M_q\otimes_{\mathbb ZN}\mathbb ZG.         \tag{6}
\]

The left quotient action in (3) is represented by

\[
L_g(m\otimes h)=C_g(m)\otimes gh=(m\cdot g^{-1})\otimes gh.       \tag{7}
\]

It is balanced because C_g(mn)=C_g(m)(gng^{-1}), it commutes with the coefficient right G-action, and inner elements of N act trivially on cohomology. Thus (7) descends to Q.

There is an isomorphism of left ZQ, right ZG bimodules

\[
F:\mathbb ZQ\otimes_{\mathbb Z}M_q
 \longrightarrow M_q\otimes_{\mathbb ZN}\mathbb ZG,
\quad F(q\otimes m)=(m\cdot\widetilde q^{-1})\otimes\widetilde q. \tag{8}
\]

Changing a lift to n tilde(q) gives
(m dot tilde(q)^{-1}n^{-1}) tensor n tilde(q), which is the same balanced tensor. In a coset decomposition of ZG, (8) is an abelian-group isomorphism on each summand; an inverse sends m tensor h to bar(h) tensor (m dot h). Its left Q-action is regular on the first tensor factor. Its right G-action is

\[
(q\otimes m)g=q\bar g\otimes(m\cdot g).                          \tag{9}
\]

For instance, to check (9) in (8), use tilde(q)g as the lift of q bar(g): the first factor becomes
m dot g(tilde(q)g)^{-1}=m dot tilde(q)^{-1}. Formula (7) checks the left action just as directly. This is why the nonsplit case does not require a chosen homomorphic section.

## 5. Collapse, and why flatness is sufficient

Let P_* be the finite-type projective resolution for Q and C^*=Hom_{ZQ}(P_*,ZQ). Finite projectivity gives, naturally with all commuting actions,

\[
\operatorname{Hom}_{\mathbb ZQ}(P_*,\mathbb ZQ\otimes M_q)
\cong C^*\otimes_{\mathbb Z}M_q.
\]

Every C^i is Z-free. The cochain universal-coefficient sequence has tensor term H^p(C) tensor M_q and torsion term Tor_1^Z(H^{p+1}(C),M_q). The latter vanishes since the sole nonzero cohomology D is Z-flat. Consequently

\[
H^p(Q;H^q(N;\mathbb ZG))=
\begin{cases}D\otimes M_q,&p=d,\\0,&p\ne d.\end{cases}           \tag{10}
\]

The right G-action on (10) is exactly (2): right multiplication by g on (9) multiplies the regular Q coefficient by bar(g) and applies the automorphism m mapsto mg to M_q. The universal-coefficient map is natural for these two commuting operations.

The spectral sequence (3) now has one nonzero column. Every differential into or out of it is zero, and each total degree has only one nonzero associated-graded term. This proves (1) as a right G-module isomorphism, with no module-splitting assertion about a multiple-piece filtration.

## 6. Finite generation in the diagonal action

First D is finitely generated over ZQ. In the finite projective cochain complex C^*, successively split off each surjection onto the top projective term above degree d, since that top cohomology vanishes. This leaves a finite projective complex ending in degree d, so D is the quotient of its finitely generated top term. This observation does not require the dualizing module to be finitely generated as an abelian group.

Choose right Q-generators z_1,...,z_r for D and right N-generators m_1,...,m_s for M_q. Then the rs pairs z_i tensor m_j generate (1) over G. Indeed, choose a lift g of q. For every m,

\[
z_iq\otimes m=(z_i\otimes(m\cdot g^{-1}))g.
\]

Express m dot g^{-1} as a finite ZN-linear combination of the m_j. Elements of N act trivially on D, so this expresses the tensor in the right G-span of the indicated pairs. There are only finitely many nonzero q, because N has finite cohomological dimension. G is therefore good.

## 7. Scope and next obstruction

This proves closure under extensions by an integral duality quotient, including nonsplit extensions. It includes the familiar duality-by-duality extension theorem as a special situation, but here N need only be good and may have cohomology in several degrees. The source's original arbitrary-FP question remains open in this packet. In particular, the proof neither removes quotient flatness nor claims that finite generation descends from G to an arbitrary normal subgroup.

The next and final turn tests the finite-kernel obstruction inside an actual group ring of a good FP group. Producing such a matrix is still weaker than producing that matrix in the group's own regular-coefficient cochain resolution.
