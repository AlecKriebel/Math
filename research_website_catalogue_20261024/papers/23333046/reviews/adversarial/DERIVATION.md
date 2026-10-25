# Independent adversarial derivation

The object checked is the entire original theorem, not a modified deformation problem. The whole actual five-page PDF and controlling TeX were read before the immutable early packet. This derivation develops that packet's separate ring-injection route and rank-two formal-series calculation. It does not use any sibling conclusion, archived review narrative, universality of a Klein-four hull, or numerical approximation.

## Exact objects and the counterexample

Let k=F4=F2[u]/(u²+u+1), G=(k,+), N={0,1}, Q=G/N, and rho(a)(t)=t/(1+at). All rings are local Artinian W(k)-algebras with identified residue field k. The deformation functor takes lifts of this action modulo coordinate changes reducing to the identity. Such coordinate changes may have nilpotent constant terms. D_N^Q is the fixed subfunctor of the actual deformation functor, not a chosen hull's fixed scheme. A prorepresentable recipient means h_R for a complete Noetherian local W(k)-algebra with residue k.

The assertion is that no such recipient F, and no natural f:D_N^Q→F←D_Q:g through which (res,ind) factors, can make D_G→D_N^Q×_F D_Q formally smooth. No dimension restriction on TF is needed. In particular, the recipient whose tangent space is H¹(Q,ThetaSharp/ThetaN) cannot work.

The proof will exhibit, for every f,g, the same missing target point over the small extension A=k[e]/e²→k. This is stronger than only disproving a proposed formula for f or g.

## Local and quotient actions

Direct substitution gives rho(a)rho(b)=rho(a+b). For a≠0, rho(a)(t)-t has order two, so this is a faithful weakly ramified action of conductor one. Set

    y = t²/(1+t).

Then t²+yt+y=0 and rho(1)(t)=t+y. The subring k[[y]] is the invariant ring for N. One way to see this without invoking an uncomputed quotient is to use the unique expansions k[[t]]=k[[y]]⊕t k[[y]]. Their existence and uniqueness follow recursively by cancelling leading even and odd orders, since y=t² times a unit. Invariance of a(y)+t b(y) under t↦t+y forces y b(y)=0, hence b=0. The same argument gives the invariant Laurent field. Using u(u+1)=1, rho(u) induces sigma(y)=y/(1+y). Thus Q is the usual weakly ramified characteristic-two involution.

The induction morphism on all Artinian lifts is an actual morphism of deformation functors: the product of the lifted N-orbit of t is an invariant parameter, and induction on the length of the coefficient ring proves that all invariants are power series in that parameter. This is the precise original primary interface, rather than an assumption of base-change exactness of arbitrary invariants. Only the naturality of this morphism and its basepoint are needed below; no formula for its tangent map is needed.

## The full derivation module, with constants included

Theta=Der_k(k[[t]]) is k[[t]]d/dt. This statement does not silently impose a continuity condition: over perfect k of characteristic two, every h(t) uniquely has the form a(t)²+t b(t)². Any k-derivation therefore satisfies d(h)=d(t)b(t)²=d(t)h'(t). Conversely every a(t)d/dt is a derivation. In particular, constant coefficients are present.

The derivative of y is t²/(1+t)². A derivation b(y)d/dy of k((y)) has the unique extension

    a(t)d/dt,   a(t)=b(y)(1+t)²/t²

to the separable quadratic extension k((t))/k((y)). Uniqueness implies that the extension commutes with N. For nonzero b, ord_t(a)=2 ord_y(b)-2, so it is regular precisely when b is divisible by y. Consequently the exact restriction image is

    ThetaN = y k[[y]]d/dy ⊂ ThetaSharp = k[[y]]d/dy.

For example, b=y extends to (1+t)d/dt, which has nonzero constant term. Excluding this vector changes the problem. This explicitly tests the hidden zero-section hypothesis rather than assuming it away.

## Infinite-series cohomology without finite-jet inference

The involution acts on coefficients by

    T(f)(y)=(1+y)² f(y/(1+y)).

Put z=y²/(1+y) and R0=k[[z]]. The invariant z is fixed by sigma. Cancelling successive leading orders proves the free decomposition k[[y]]=R0⊕y R0, so M=y k[[y]]=yR0⊕y²R0. This proof uses completeness and the increasing orders 2m and 2m+1; it is not a formal identification based on finitely many coefficients.

Now T(y)=y+y² and T(y²)=y². In the free basis (y,y²),

    T = [[1,0],[1,1]],     T-1 = [[0,0],[1,0]].

In characteristic two the norm 1+T equals T-1. Solving the two-coordinate equations over the entire ring R0 gives

    ker(1+T)=y²R0=im(T-1).

An explicit primitive of y²b(z) is yb(z), for every formal b. Hence H¹(Q,ThetaN)=0. This proves the universal formal-series statement. Any finite exact calculation is only a check on the displayed basis identities.

For comparison, in basis (1,y) for ThetaSharp,

    T-1 = z [[1,1],[1,1]],

because y²=z+zy. Since z is a nonzero divisor in R0, its kernel is R0(1,1) and image is zR0(1,1). Therefore

    H¹(Q,ThetaSharp)=R0/zR0 ≅ k,

represented by 1+y. Also ThetaSharp/ThetaN is the one-dimensional trivial Q-module, so H¹(Q,ThetaSharp/ThetaN)=k. Thus the nonzero target tangent direction really exists, and the original requested tangent space is one-dimensional. No recipient tangent dimension is assumed in the contradiction.

## Restriction is injective on the actual tangent sets

First-order local-action deformations modulo identity-reducing coordinates identify with H¹ of the full Theta module. This follows by writing a lift as (id+e c(g))rho(g); the group law is exactly the cocycle condition and conjugation is a coboundary. Restriction is cocycle restriction.

Here is a direct kernel proof, without importing the desired injection from a spectral-sequence conclusion. If a cocycle c:G→Theta restricts to a coboundary on N, subtract that coboundary, making c(N)=0. For the other generator u, commutativity implies n c(u)=c(u) for every n∈N, so c(u)∈ThetaN. The relation u²=1 says (1+T)c(u)=0. The full-series calculation above supplies m∈ThetaN with c(u)=(T-1)m. Subtracting the coboundary of m kills c(u) and preserves c(N)=0. It kills c on both generators and hence on G. Therefore

    res : D_G(k[e]/e²) → D_N(k[e]/e²)

is injective, and remains so with its actual fixed-subfunctor codomain. This is an assertion about all first-order deformations, not a sample of fractional-linear lifts.

## The nonzero target class is killed by every prorepresentable recipient

On A=k[e]/e², let v be the class of sigma_e(y)=(y+e)/(1+y). Its square is the identity since the corresponding matrix M_e=[[1,e],[1,1]] squares to the unit scalar (1+e)I. Its difference from sigma has constant coefficient e. For an arbitrary identity-reducing coordinate y+e h(y), the first-order conjugacy correction is h(sigma(y))-sigma'(y)h(y); its constant coefficient is h(0)-h(0)=0. Thus v≠0, even when nilpotent constant terms in h are allowed. Equivalently its cocycle is the nonzero class 1+y computed above.

Consider the genuine injective morphism i:A→B=k[w]/w³, e↦w². Write M_d=[[1,d],[1,1]] and C=[[1+w,w],[0,1]]. Exact multiplication gives

    M_(w²) C = (1+w) C M_0.

C reduces to the identity and has unit determinant. Its fractional-linear coordinate (1+w)y+w is therefore an allowed coordinate change. This proves D_Q(i)(v)=D_Q(i)(0). This same collision is explicitly the established Byszewski–Cornelissen Proposition 6.1, but the displayed conjugacy and all-natural-map consequence were independently derived in the early packet.

For every prorepresentable F=h_R the map F(i) is injective: two ring homomorphisms R→A that agree after an injective A→B agree pointwise. This argument includes mixed-characteristic R, since A and B are objects in the W(k)-category via W(k)→k. Naturality of every eta:D_Q→F now gives

    F(i)(eta_A(v)) = eta_B(D_Q(i)v)
                   = eta_B(D_Q(i)0) = F(i)(eta_A(0)),

so eta_A(v)=eta_A(0). Mere nonprorepresentability of D_Q would not imply this statement; the injection collision supplies the missing mechanism.

The paper's alternative cubic self-map j(w)=w+w² gives the same conclusion: its fixed ring is k+kw² and its reduction to A=k[w]/w² consists of constants. Naturality and the explicit parameter-shift conjugacy force any represented map of the cubic deformation to factor through these constants after reduction. Both exact finite-ring identities were checked independently. The injection conjugacy in fact remains polynomially valid over longer truncations; only the parameter-shift identity used here depends on w³=0. An initial diagnostic expectation confusing those two boundaries was rejected by exact multiplication and corrected in our unsealed control script, with the failed development run retained in EXACT_RESULTS.json. No early sealed object or original source was changed.

## The missing point and the universal contradiction

For arbitrary natural f:D_N^Q→F←D_Q:g, naturality from the unique k-point implies f_A(0_N)=g_A(0_Q). The preceding result gives g_A(v)=g_A(0_Q). Hence (0_N,v) is a point of the actual fibre product at A, reducing to the unique point over k. This does not assume that every tangent map is linear.

If D_G→D_N^Q×_F D_Q were formally smooth, the small extension A→k would supply w∈D_G(A) mapping to (0_N,v). Its restriction is zero; the injectivity proved above forces w=0_G. Naturality of induction then gives ind(w)=0_Q, contradicting v≠0. This rules out every stated recipient, every choice of f,g with the specified factorization, and in particular the refined tangent-space version. It is already a first-order failure of formal smoothness.

## Scope of the verified assertion

The assertion concerns the unframed local deformation functors over the stated category, the actual fixed subfunctor, and prorepresentable recipients. It does not establish a statement for framed functors, section-preserving coordinates, a fibre product of versal hulls, arbitrary nonrepresentable recipients, global deformation functors, or the variant assuming D_N and D_Q prorepresentable. In this example D_Q is not prorepresentable. The original conditional Byszewski obstruction theorem is therefore not contradicted.

The source's entire mathematical conclusion is supported by this derivation. No central gap or counterexample to the original theorem was found. Novelty, priority, current openness, formal certification, human peer review and publication clearance are not established by this packet.
