# Flat surface bundles: the flux quotient and the remaining relation problem

## Disposition and conventions

This is an AI-authored, unrefereed partial analysis of K3 Problem 2.32 (UnsolvedMath 2780). It does **not** solve the unrestricted problem for closed oriented fibers of genus at least two, over either surfaces or three-manifolds. No novelty is claimed. The main input is Kotschick–Morita's extended-flux theorem, and the stabilization argument belongs to the existing Kotschick–Morita framework.

The source problem asks whether bundles with surface fibers over two- or three-dimensional manifold bases always carry a foliation transverse to the fibers. The hyperbolic-fiber version is the intended research target here. Throughout Sections 2–5, the fiber is the closed oriented smooth surface S_g, g >= 2, the structure group preserves orientation, and diffeomorphisms and foliations are smooth. No marked point, prescribed section, or invariant deck transformation is imposed. Statements about area-preserving holonomy are explicitly distinguished from unrestricted smooth holonomy.

K3 Chapter 2 defines oriented surfaces but does not impose g >= 2 in the displayed Problem 2.32. Its monodromy-lifting equivalence requires care in lower genus. Section 1 gives a literal low-genus counterexample, kept separate from the intended unresolved question. This is a scope issue, not a claimed solution to that question.

## 1. A low-genus boundary counterexample

Let h:S^3 -> S^2 be the Hopf circle bundle. The map

    p:S^3 x S^1 -> S^2,    p(x,z)=h(x)

is a smooth oriented T^2-bundle. It has no smooth flat connection.

Indeed, for a compact-fiber bundle over a compact base, a smooth horizontal distribution admits parallel transport along every finite smooth path: horizontal lifts solve an ordinary differential equation in the compact total space. If the distribution is integrable, its holonomy is invariant under homotopy of paths relative to endpoints. On a simply connected base, parallel transport from one fixed fiber therefore gives a global bundle trivialization. A flat T^2-bundle over S^2 would consequently be S^2 x T^2. But

    pi_1(S^3 x S^1) = Z,    pi_1(S^2 x T^2) = Z^2.

The total spaces are not even homotopy equivalent. This proves nonflatness. The mapping-class monodromy is trivial, so its trivial lift alone does not determine this bundle's topology. Pulling p back by S^2 x S^1 -> S^2 gives a T^2-bundle over a closed oriented three-manifold which is also nonflat: restricting any flat connection to S^2 x {z} would make p flat.

For g >= 2, contractibility of Diff_0(S_g) eliminates this particular discrepancy. The associated classifying space BDiff^+(S_g) has homotopy type K(Mod(S_g),1), so an oriented bundle over a connected smooth base is classified by its monodromy up to conjugacy. Thus a homomorphic lift of that monodromy to Diff^+(S_g) does give a flat structure on the specified underlying bundle. The Earle–Eells input and its relevance are also explained in [BCS, pp. 2–3] and [H, Section 3].

## 2. The elementary flux obstruction always vanishes after changing lifts

Fix an area form omega on S_g. Put

    G = Symp(S_g,omega),    N = Symp_0(S_g,omega),
    M = Mod(S_g),           V = H^1(S_g;R),
    H = Ham(S_g,omega),     q:G -> M.

We use the following precise existing inputs from [KM, Theorem 2 and Section 2]: q is onto with kernel N; Flux:N -> V is onto with kernel H; and there is a crossed homomorphism c:G -> V extending Flux. With the left action m.v=(m^{-1})^*v, the crossed identity is

    c(ab)=c(a)+q(a).c(b).

The following argument is purely algebraic once these inputs are given.

### Proposition 2.1

The map

    Psi:G -> V semidirect M,    Psi(a)=(c(a),q(a))

is an onto homomorphism with kernel H. In particular, as abstract groups,

    G/H is isomorphic to V semidirect M.

The subgroup K=ker(c) maps onto M, and its kernel under q is H.

**Proof.** Give the semidirect product multiplication (v,m)(w,n)=(v+m.w,mn). The crossed identity proves that Psi preserves products. Its kernel consists of a in N with Flux(a)=0, exactly H. This also proves normality of H in G.

For any (v,m), choose a in G with q(a)=m. Choose n in N with Flux(n)=v-c(a), which is possible by surjectivity. Since q(n)=1,

    c(na)=Flux(n)+c(a)=v,    q(na)=m.

Thus Psi is onto. Its kernel calculation and the first isomorphism theorem give the asserted quotient. Taking v=0 shows q(K)=M. The crossed identity shows K is closed under multiplication; c(a^{-1})=-q(a)^{-1}.c(a) shows it is closed under inverses. Finally K intersect N=H. QED.

### Corollary 2.2

Let Gamma have a presentation with generators x_j and relators r_l, and let rho:Gamma -> M be a homomorphism. One can choose representatives A_j in G of rho(x_j) such that **every** relator word r_l(A_j) belongs to H, simultaneously.

**Proof.** Choose every A_j in K using Proposition 2.1. Each word r_l(A_j) lies in K because K is a subgroup. Its mapping class is rho(r_l)=1, so it also lies in N. Therefore it lies in K intersect N=H. QED.

For a closed genus-h base, in particular, the product D=product_i [A_i,B_i] can always be arranged to have Flux(D)=0 without changing any prescribed mapping class. Here [a,b]=aba^{-1}b^{-1}. In the language of K3 Remark (3), zero is always attained by Flux composed with the relator-defect map. This rules out nonvanishing ordinary flux for every choice of representatives as an obstruction. The same argument applies to presentations of three-manifold groups.

Crucially, D in H does not mean D=1. Nor does a flat representation necessarily take values in K: its extended flux can be a nonzero crossed cocycle on the base group. The proof above permits changing generator representatives; those changes need not preserve an already satisfied relation. We make no claim that all flat representations can be normalized into K.

## 3. Exact stabilization cost and its limitation

Fix rho:pi_1(S_h) -> M and a standard surface presentation. For any tuple L=(A_1,B_1,...,A_h,B_h) lifting its generator images, set

    D(L)=product_i [A_i,B_i] in N.

Let cl_N(u) be the least number of commutators of elements of N whose product is u. Set cl_N(u)=infinity if u is outside [N,N], and cl_N(1)=0. The minimum below ranges over **all** tuples L, not just tuples in K.

### Proposition 3.1

The minimum number r of topologically trivial base handles needed to make the given bundle area-preservingly flat is

    r = min_L cl_N(D(L)^{-1}).

It is finite. Moreover r=0 if and only if the original bundle admits an area-preserving flat connection.

Here topologically trivial stabilization means adding r handles to the base, retaining rho on the original generators, and giving all added generators the identity mapping class. Equivalently it is the pullback along the standard degree-one pinch map S_{h+r} -> S_h, up to the usual smooth bundle classification.

**Proof.** For fixed L, a lift of the stabilized presentation must choose U_j,V_j in N on its added generators. Its sole relation is

    D(L) product_{j=1}^r [U_j,V_j] = 1.

This is possible exactly when D(L)^{-1} is a product of at most r commutators in N. Identity commutators pad shorter products. Taking the minimum over L proves the formula and the zero-cost equivalence.

To prove finiteness, first note [N,N]=H: the abelian flux quotient gives [N,N] contained in H, and perfectness of H gives H=[H,H] contained in [N,N]. Perfectness is a classical input recorded in [KM, Section 2]. Corollary 2.2 supplies at least one L with D(L) in H. Its inverse has finite commutator length, completing the proof. QED.

For a fixed tuple with nonzero flux, adding only identity-component holonomies cannot cancel the defect. Changing the original representatives removes that obstruction. Perfectness yields some finite stabilization, not a way to remove its extra handles. No positive lower bound for the minimized cost r is proved here. An unbounded commutator-length function on H alone would not establish a positive minimum over all representatives of any particular rho.

### The exact Hofer question left over

Define

    D_H(rho) = {D(L): L lifts rho and D(L) lies in H}.

This set is nonempty by Corollary 2.2. Let epsilon(rho) be the infimum of the Hofer norm over D_H(rho). Area-preserving flatness is equivalent to 1 belonging to D_H(rho). A strictly positive epsilon would obstruct it. But epsilon=0 does not imply attainment of the identity: nondegeneracy of a norm concerns each fixed element, not attainment of an infimum over a varying set. No compactness or attainment theorem is supplied here.

Taking the infimum only over the zero-extended-flux representatives in K would be a different, more restrictive question. A positive lower bound on that smaller set would not by itself obstruct all area-preserving flat connections. Finally, failure of area-preserving flatness would still require an additional argument to imply failure of unrestricted smooth flatness.

## 4. Genuine flat subcases and the relation between base dimensions

### Proposition 4.1

If rho:pi_1(B) -> M factors through a free group F, then the S_g-bundle over B admits an area-preserving flat connection.

**Proof.** Write rho=v composed with u, with u:pi_1(B) -> F and v:F -> M. Choose a free basis for F and lift each basis image through q:K -> M. The universal property of a free group gives a homomorphism v_tilde:F -> K with q composed with v_tilde=v. Then v_tilde composed with u is a homomorphic lift of rho to G. Its suspension has the specified monodromy and hence is isomorphic to the given bundle by hyperbolic-fiber classification. QED.

Consequences include bundles with infinite-cyclic monodromy image; bundles over a compact connected oriented surface with nonempty boundary; and bundles over a closed three-manifold #^k(S^1 x S^2). Simply connected bases give trivial bundles in this g >= 2 regime. The empty free basis covers k=0, with S^3 as the base. None of these arguments treats an arbitrary nonfree surface-group image.

### Proposition 4.2

For any surface bundle E -> S_h, its pullback to S_h x S^1 is flat if and only if E is flat. The assertion holds both smoothly and with area-preserving holonomy.

**Proof.** Pull back a flat structure for the forward construction. Conversely, restrict a flat structure on the pullback to S_h x {z}; the restricted bundle is E. Pullback preserves transverse foliations and the prescribed holonomy category. QED.

Thus a negative answer over surfaces would yield a negative answer over three-manifolds. A positive answer for all three-manifold bases would imply a positive answer over surfaces. No converse covering all three-manifold bundles is proved.

## 5. Why nearby obstruction results do not close the gap

An instructive concrete example is the product bundle S_g x S_g -> S_g with the first projection and the diagonal section. The bundle is flat, with horizontal leaves S_g x {y}. Its diagonal cannot be a horizontal section for any smooth flat connection when g >= 2. Its oriented normal bundle has Euler number 2-2g, whereas the derivative holonomy of a horizontal section would make that normal bundle a flat oriented real two-plane bundle, whose Euler number has absolute value at most g-1 by Milnor's inequality. Since 2g-2>g-1, this is impossible. The normal-bundle identification is (u,v) modulo the diagonal tangent plane mapped to v-u, giving TS_g up to the irrelevant orientation sign.

This is precisely the distinction between section-preserving and unrestricted flatness emphasized in [BCS]. That paper's Atiyah–Kodaira theorem likewise forbids a deck-invariant flat connection, with invariance essential; it does not rule out every flat connection on those closed-fiber bundles.

The MMM obstruction classes of degree at least six have zero pullback to a base of dimension two or three for dimensional reasons. Their vanishing is not a construction of holonomy lifts. Nonzero signature also does not alone obstruct flatness, by [KM]. Modern homology-surjectivity and bordism results, including [N24, Section 1], change or compare bundle bordism classes; they do not identify a flat representative on the same prescribed base and bundle. Different regularity categories must also remain separate.

These observations do not prove absence of all other obstructions. The unrestricted genus-at-least-two question and the full area-preserving relation problem both remain unresolved by this analysis.

## Sources

- [K3] R. Inanc Baykur, Robion C. Kirby, Daniel Ruberman (editors), *K3: A New Problem List in Low-Dimensional Topology*, author's preliminary version; Chapter 2 conventions, printed p. 84; Problem 2.32 and remarks, printed pp. 111–112. https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf
- [KM] D. Kotschick and S. Morita, *Signatures of foliated surface bundles and the symplectomorphism groups of surfaces*, Topology 44 (2005), 131–149; inspected arXiv:math/0305182v1, Theorem 2, Sections 2–3. https://arxiv.org/abs/math/0305182 ; https://doi.org/10.1016/j.top.2004.05.002
- [BCS] M. Bestvina, T. Church and J. Souto, *Some groups of mapping classes not realized by diffeomorphisms*, Comment. Math. Helv. 88 (2013), 205–220; inspected arXiv:0905.2360v2, Theorems 1.1 and 1.3 and the accompanying open question. https://arxiv.org/abs/0905.2360
- [H] J. A. Hillman, *Sections of surface bundles*, Geometry & Topology Monographs 19 (2015), 1–19, Section 3. https://msp.org/gtm/2015/19-1/gtm-v19-n1-p01-p.pdf
- [N24] S. Nariman, *On flat manifold bundles and the connectivity of Haefliger's classifying spaces*, arXiv:2202.00052v3 (15 May 2024), Sections 1–2. https://arxiv.org/abs/2202.00052

The literature check is bounded and dated 2026-10-06. No theorem resolving the unrestricted target was located; that search outcome is not a proof of current global open status. Mathematical claims here are the displayed scoped deductions, with their existing inputs credited.
