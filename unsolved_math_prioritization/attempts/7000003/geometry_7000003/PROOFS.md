# Retained proofs and exact controls

These are restricted results and independent elementary derivations of standard geometry. No first-discovery claim is made. Smooth means C∞ unless a weaker class is explicitly stated. None of the theorems below settles Problem 1.3.

## 1. Fixed boundary and the infinitesimal rotation field

Let F be a C² immersed surface and V a C² field along F satisfying the infinitesimal isometry equations

    <dF(X),dV(Y)> + <dF(Y),dV(X)> = 0.

At each point there is a unique vector y such that dV(X)=y×dF(X) for all tangent X. Indeed, in an oriented orthonormal tangent basis e₁,e₂, the three strain equations say precisely that the map eᵢ↦dV(eᵢ) is the restriction of a skew-symmetric endomorphism of R³; its three coefficients determine y uniquely. In coordinates, equality of mixed derivatives gives

    y_u×F_v = y_v×F_u.

At the point choose coordinates with F_u=e₁,F_v=e₂. Writing y_u=(a,b,c) and y_v=(d,e,f), this equality reads (-c,0,a)=(0,f,-e). Hence c=f=0: every derivative of y is tangent to the surface.

Suppose V vanishes pointwise on a regular boundary arc γ, parametrized by arclength, with tangent T and unit surface normal n. Then 0=dV(T)=y×T, so y=λT along γ. Taking the normal component of its derivative yields

    0 = <y',n> = λ<T',n> = λ κ_n.

Consequently, wherever the boundary normal curvature κ_n is nonzero, y=0 and dV=0. This determines the infinitesimal Cauchy data there. It does not by itself prove global continuation or nonlinear uniqueness.

**Tangent-boundary obstruction.** If the tangent plane of a C² surface coincides along a boundary arc with the fixed plane containing that arc, its continuously chosen normal is constant there. Thus dn(T)=0. The shape operator has a nonzero kernel vector and K=0 on that arc. In particular, the motivating tangent-boundary class cannot be treated as having K<0 all the way through a noncharacteristic boundary. Negative curvature in the interior is consistent with this degeneracy.

## 2. All-mode infinitesimal rigidity of a rotational annulus

**Theorem.** Let I=[a,b] and

    F(s,θ) = (r(s)cosθ,r(s)sinθ,z(s)),  θ∈R/(2πZ),

where r,z are C², r>0, r'²+z'²=1, and z' has no zeros on I. Every C¹ infinitesimal isometry V which is zero on the parallel s=a is zero on the whole annulus.

This theorem is stronger in boundary-data count but much narrower in surface class than the target. It does not even require K<0. The coordinate s is meridian arclength.

**Proof.** Write e_r=(cosθ,sinθ,0), e_θ=(-sinθ,cosθ,0), e_z=(0,0,1), and V=Ae_r+Be_θ+Ce_z. The three strain equations are

    r'A_s+z'C_s=0,
    A+B_θ=0,
    rB_s+r'(A_θ-B)+z'C_θ=0.

Take Fourier coefficients with convention ∂_θ↦im for every m∈Z. Differentiation under the integral is legitimate for C¹ fields. The second equation gives A_m=-imB_m. The first and third then give

    B_m' = -(r'/r)(m²-1)B_m - im(z'/r)C_m,
    C_m' = -im(r'²/(rz'))(m²-1)B_m + m²(r'/r)C_m.

All coefficients are continuous on I. Fixed boundary gives B_m(a)=C_m(a)=0. Uniqueness for a linear first-order ODE forces B_m=C_m=0, including m=0; hence A_m=0. Completeness of the Fourier basis for continuous periodic functions gives A=B=C=0. ∎

For a catenoid parametrized by height u, meridian arclength satisfies ds/du=cosh u, so z_s=sech u>0 on every compact segment. The theorem applies. At a tangent planar boundary of a rotational surface, z_s=0, which is exactly an excluded endpoint. No limit argument through that singularity is asserted.

**Nonlinear rotational control.** If another immersion with the same rotational coordinates and axis has the same metric, positive radius, and meridian arclength parameter, its radius is r and its height derivative is ±z'. With z' nowhere zero the sign is constant by continuity. Thus it differs by a vertical translation or a reflection followed by translation. If both boundary heights are fixed, their difference is nonzero because z' has constant nonzero sign, and only the identical height remains. This comparison is restricted to the same rotational-coordinate class; it does not show that arbitrary isometric embeddings are rotational.

## 3. The catenoid–helicoid associate does not descend

On the universal covering strip (u,v)∈[a,b]×R define

    C=(cosh u cos v,cosh u sin v,u),
    H=(sinh u sin v,-sinh u cos v,v).

Direct differentiation gives H_u=-C_v and H_v=C_u. Also C_u⊥C_v and |C_u|²=|C_v|²=cosh²u. Therefore F_α=cosα C+sinα H has first fundamental form cosh²u(du²+dv²) for every α.

However,

    F_α(u,v+2π)-F_α(u,v)=(0,0,2πsinα).

The immersion is single-valued on the annulus only when sinα=0. Those associates are C and -C, related by a Euclidean isometry. For every other parameter the proposed boundary parallels fail to close. Even the infinitesimal field ∂_αF_α|₀=H is not periodic. Local metric preservation cannot repair this exact global period obstruction.

## 4. A direct obstruction for saddle graphs

**Theorem.** Let f be C² on an open planar set Ω and assume det Hess f<0. Let γ:R/(LZ)→Ω be a regular C¹ closed curve. If its lift (γ,f∘γ) is asymptotic on the graph, the tangent lines of γ cover the plane.

Here a point p is missed by every tangent line exactly when det(γ-p,γ') is nowhere zero. This is the strict locally-star-shaped condition relevant to this theorem, not an assumption that every Jordan curve has such a point.

**Proof.** Put J(x,y)=(-y,x) and Q=Hess f. The graph's second fundamental form is Q divided by the positive factor sqrt(1+|∇f|²), up to orientation. Thus asymptoticity says γ'·Qγ'=0. Since Q is invertible and γ' never vanishes, there is a continuous nowhere-zero λ with Qγ'=λJγ'. It has constant sign. Suppose p is missed by all tangent lines. Then (γ-p)·Jγ' is continuous, nowhere zero, and has constant sign. The periodic C¹ scalar

    h(t)=f(γ(t))-(γ(t)-p)·∇f(γ(t))

satisfies

    h' = -(γ-p)·Qγ' = -λ(γ-p)·Jγ'.

Its derivative has constant nonzero sign, contradicting periodicity. ∎

This gives an elementary version of a known obstruction in the Panov/Arnold/Ghomi–Raffaelli line of work. It does not supply a globally suitable projection or graph for the annulus. Negative curvature alone certainly permits closed asymptotic curves, as §5 shows.

## 5. Closed-characteristic monodromy and a realized neutral ribbon

### 5.1 Return multiplier

Use coordinates (x,t)∈(R/(ℓZ))×(-ε,ε) around a closed asymptotic curve t=0. Write the second fundamental form as

    L dx²+2M dx dt+N dt²,

with L(x,0)=0 and M(x,0)≠0. The latter follows from negative determinant on the core. The asymptotic branch tangent to the core has slope dt/dx=a(x,t) determined by L+2Ma+Na²=0 and a(x,0)=0. The implicit function theorem gives

    a_t(x,0)=-L_t(x,0)/(2M(x,0)).

The variation w=∂t(x;t₀)/∂t₀|₀ solves w'=a_t(x,0)w and w(0)=1. Its first-return multiplier is therefore

    P'(0)=exp[-(1/2)∫₀^ℓ L_t/M dx].

A nonzero exponent makes this closed characteristic hyperbolic and isolated, by applying the one-variable inverse-function theorem to P(t)-t. A zero exponent does not decide isolation or global rigidity. Han–Khuri's equation (2.3) identifies the integrated coefficient, up to sign conventions, with their closed-curve nondegeneracy integral. We do not assert that the latter is automatically nonzero in the target class.

### 5.2 An explicit embedded curve with nonzero torsion

Set c=cos2q and

    γ(q)=((4+cos2q)cos q,(4+cos2q)sin q,sin2q), q∈R/(2πZ).

The cylindrical radius is at least 3. Its angular coordinate is q modulo 2π, so γ is injective as a circle map. Its speed satisfies

    |γ'|²=(4+c)²+4 ≥ 13.

The scalar triple product is

    D=det(γ',γ'',γ''')=-6(c³-24c²+32).

For -1≤c≤1,

    c³-24c²+32 = 7+(c³+1)+24(1-c²) ≥ 7,

because c³+1=(c+1)(c²-c+1)≥0. Hence D≤-42. The curvature is nonzero, since γ'×γ''=0 would force D=0. Its torsion τ=D/|γ'×γ''|² is strictly negative. Reparametrize by arclength s and use the periodic Frenet frame (T,N,B), with κ>0 and τ<0.

### 5.3 The ribbon is negatively curved and has neutral core

Define X(s,t)=γ(s)+tN(s). The Frenet equations give

    X_s=(1-tκ)T+tτB,   X_t=N,
    E=(1-tκ)²+t²τ²,   F=0,   G=1,
    n=((1-tκ)B-tτT)/sqrt(E).

Since τ≠0, E>0 for all real t. The coefficients of the second fundamental form satisfy

    II(X_t,X_t)=0,   II(X_s,X_t)=τ/sqrt(E).

Thus

    K=-τ²/E²<0.

For sufficiently small ε>0, the restriction |t|≤ε is embedded by the tubular neighborhood theorem for the compact embedded curve γ. At t=0, X_ss=κN is tangent, so the core is asymptotic. In the notation of §5.1, L(s,0)=0, M(s,0)=τ(s), and differentiating L=<X_ss,n> gives L_t(s,0)=τ'(s). Therefore

    ∫ L_t/M ds = ∫ τ'/τ ds = 0,

and P'(0)=1. This is an actual embedded negative-curvature annulus with a closed asymptotic curve and neutral multiplier, not just a freely assigned quadratic form failing Gauss–Codazzi.

### 5.4 Exact failure of the required boundary hypothesis

At q=0,π,π/2 the points of the offset curve γ+tN are respectively

    (5-t,0,0),  (-(5-t),0,0),  (0,3+t,0).

For |t|<1 they are noncollinear and span z=0. At q=π/4 the height of the offset is

    1-5t/sqrt(70),

because N_z=-5/sqrt(70) there. This is positive for |t|<1. Consequently neither boundary t=ε nor t=-ε is planar when ε<1. Neither can be a convex planar curve. The explicit ribbon is excluded from Problem 1.3 and proves no negative answer.

The construction shows exactly why the unconstrained ribbon strategy stops: negative curvature, embeddedness, and a neutral closed characteristic are compatible, but the required global boundary geometry has not been attained. No extension preserving all target hypotheses is supplied.
