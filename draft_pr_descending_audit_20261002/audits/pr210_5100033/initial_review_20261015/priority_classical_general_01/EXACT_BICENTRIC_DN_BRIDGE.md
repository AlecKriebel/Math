# Exact reduction to an old arbitrary-order Jacobi dn identity

UTC checkpoint: 2026-10-15T12:34:00Z. Completion estimate for this priority approach: 70%. This is a fresh audit derivation. It is not represented as a historical publication of the focal-pedal theorem, and it does not rely on the submitted two-pole cancellation.

## 1. Definitions and convention

Let the original ellipse have semiaxes a>b>0, common foci (±c,0), c²=a²−b². Let the fixed elliptical caustic have semiaxes α>β>0, α²−β²=c². Set λ=a²−α²=b²−β²>0, k=c/α∈(0,1), k'=β/α. Jacobi notation below uses modulus k; software uses parameter m=k².

Use Stachel's phase P(w)=(-a sn(w,k),b cn(w,k)), vertices w+jδ, δ=2v=4Kτ/N, gcd(τ,N)=1 and 0<τ<N/2. Put a=α dn(v,k)/cn(v,k), b=β/cn(v,k), so 0<v<K. All areas are ordered signed cross-product areas.

Write T_+(x,y)=(a²(x+c)/(a²+cx), a²y/(a²+cx)). Its homogeneous matrix is [[a²,0,a²c],[0,a²,0],[c,0,a²]]. On the original ellipse it is exactly the perpendicular foot from (c,0) onto its tangent. It maps that ellipse onto S: X²+Y²=a². Its denominator is positive on the closed ellipse interior. Consequently tangent lines at P_j map to tangent lines of S at Q_j=T_+(P_j).

## 2. Circle/conic and then genuine bicentric geometry

The caustic image is

(a⁴/α²)(X−c)²+(b⁴/β²)Y²=(a²−cX)².

In the form A X²+B Y²−2D X+C=0,

A=a⁴/α²−c², B=b⁴/β²,
D=c a²λ/α²>0, C=−a⁴β²/α²<0.

Here A−B=−c²λ²/(α²β²)<0 and D²=−C(B−A). Thus this is a noncircular ellipse with one focus at O and the other at (2D/A,0). It is not a bicentric circle pair at this stage. It contains O: T_+^{-1}(O)=(-c,0), which lies strictly inside the original elliptical caustic because c<α.

Now polarize with respect to the actual radius-a circle S: the polar of q is q·R=a². The third homogeneous line coordinate is **−a²**, not +a². The inverse conic matrix, or its adjugate, gives the dual circle

R_X²+R_Y²−2d R_X+(d²−R²)=0,
d=−cλ/β²<0, R=α b²/β².

The inner circle remains S, centered at O, radius r=a. These two circles are not mutually concentric. Since the caustic image is strictly inside S and contains O, its polar circle is strictly outside S. This is a genuine nested bicentric pair.

Let V_j be the intersection of the original tangents at P_j and P_{j+1}; let R_j=T_+(V_j). It is the intersection of the tangents to S at Q_j and Q_{j+1}. Hence R_j lies on the displayed outer circle, and Q_j is the contact point on side R_{j-1}R_j. This fixes the index, including the cyclic closing edge.

Sanity check on the sign: the ellipse (X−1)²/4+Y²/3=1 has focus O, and its unit-circle polar is X²+Y²+(2/3)X−1/3=0, centered at (−1/3,0).

## 3. Stars and positive tangent lengths

Choose orientation so each original chord has the caustic on its left. The projectivity preserves this side relation on the ellipse interior because its denominator never vanishes or changes sign. The image chord Q_jQ_{j+1} supports the image caustic, containing O, on its left. Thus det(Q_j,Q_{j+1})>0. The forward angle between Q_j and Q_{j+1} on S is in (0,π), even for a primitive star. Its half-angle ε_j therefore has t_j=r tan ε_j>0.

The tangents at Q_j,Q_{j+1} meet at R_j. Both tangent segments from R_j have length t_j. The segment on side R_{j-1}R_j has length t_{j-1}+t_j and is oriented with O on its left. Consequently

A_R=r Σ_j t_j,
B_+=r³ Σ_j t_j/(r²+t_j²).

These are signed area identities valid with the stated order; no unsigned face decomposition is substituted. In this chosen orientation both sums are positive. Reverse orientation changes both areas' signs and leaves the final product unchanged.

## 4. Exact phase, modulus and tangent-length map

Intersecting tangents at w=z−v and w=z+v with the Jacobi addition identities gives

V(z)=(-a dn(v)/cn(v) sn z, b/cn(v) cn z)
    =(-a²/α sn z, b²/β cn z).

Thus the midpoint phase of R_j is z_j=w+v+jδ. Direct substitution into T_+ gives

(R_X(z)−d)/R=(k−sn z)/(1−k sn z),
R_Y(z)/R=k' cn z/(1−k sn z).

Set k_b=2√k/(1+k), m_b=k_b²=4k/(1+k)²,
K_b=(1+k)K, K_b'=(1+k)K'/2,
u=(1+k)(z−K)/2.

The classical quadratic Gauss/Landen transformation gives

[(k−sn z)+i k' cn z]/(1−k sn z)
 = −[1−2 sn²(u,m_b)+2i sn(u,m_b)cn(u,m_b)].

A self-contained verification is available without assuming a remembered shift formula. Let f(z)=sqrt((1−k)/(1+k)) dn(z,k)/(1−k sn(z,k)). Its derivative is sqrt((1−k)/(1+k)) k cn z/(1−k sn z). Direct differentiation gives

f''=((1+k)²/4)[(2−m_b)f−2f³], f(K)=1, f'(K)=0.

ODE uniqueness identifies f(z)=dn(u,m_b). Both circle-coordinate expressions above have the same value −1 at z=K and the same angular derivative (1+k)f(z), proving the stated circle identity. This also verifies the phase origin and the modulus-vs-parameter convention.

After translating to the circumcenter and rotating by π, R_j has the usual Jacobi bicentric form R(1−2sn²u_j,2sn u_j cn u_j), and its incircle is centered at (−d_0,0), d_0=−d>0. Set

t_M²=(R+d_0)²−r²>0.

Then t_j²=|R_j|²−r²=t_M² dn²(u_j,m_b). Positivity selects t_j=t_M dn(u_j,m_b). The successive phase increment is

σ=(1+k)δ/2=(1+k)v=2K_b τ/N.

The original opposite-focus relation is Q_-(w)=−Q_+(w+2K). Areas are unaffected by this central reflection, so B_-(w)=B_+(w+2K). The same phase change is exactly u→u+K_b. This alignment is essential; an arbitrary pair of bicentric polygons is not asserted to have constant area product.

## 5. Contact/bicentric area ratio by a local identity and cyclic reindexing

The original canonical formulas imply

R+d_0=(α+c sn²v)/cn²v,
r/(R+d_0)=cn(v,k)dn(v,k)/(1+k sn²v),
(R−d_0)/(R+d_0)=(1−k sn²v)/(1+k sn²v).

The classical quadratic Gauss formulas identify these last two expressions with cn(σ,m_b) and dn(σ,m_b). Thus

sn²(σ,m_b)=t_M²/(R+d_0)²,
dn(σ,m_b)=(R−d_0)/(R+d_0)>0.

The Jacobi addition identity reads

dn(u+σ)+dn(u−σ)
 =2 dn(u)dn(σ)/(1−m_b sn²u sn²σ).

Since r²+t_M²dn²u=(R+d_0)²(1−m_b sn²u sn²σ), summing over u_j=u_0+jσ cyclically gives

B_+= [r³t_M/((R+d_0)² dnσ)] Σ_j dn u_j
    = [r³t_M/(R²−d_0²)] Σ_j dn u_j,
A_R= r t_M Σ_j dn u_j,
B_+/A_R=r²/(R²−d_0²).

The reindexing is valid because Nσ=2K_bτ is a true period of dn. Denominators are strictly positive on all real phases. This is a fresh audit derivation using classical addition formulas, rather than an unverified appeal to an older contact-area theorem.

## 6. The old arbitrary-order identity and exact conclusion

For q_b=exp(−πK_b'/K_b), choose m_N∈(0,1) whose nome is q_b^N and write K_N=K(m_N). The old generalized Landen identity is

S_N(u)=Σ_(j=0)^(N−1) dn(u+2jK_b/N,m_b)
      =(N K_N/K_b) dn((N K_N/K_b)u,m_N).

Khare–Sukhatme, arXiv:math-ph/0312074v1, Eqs. (13)–(15), pp.3–4, §2.1 proof pp.5–7, states the arbitrary-integer-p sum identity in reciprocal normalization. A published companion is *Connecting Jacobi elliptic functions with different modulus parameters*, Pramana63(2004),921–936, DOI10.1007/BF02704331; the final primary PDF was fetched from the Indian Academy of Sciences and independently read: Eq. (7) on printed p.923, proof §2.1 on pp.924–926, and odd-p summary Eq. (58) on p.931. The final PDF SHA256 is b095489fbd2de419b945af14933cda159f34b42a775b9d212031b62e1682de4c. No full-text PDF is retained in this authored package.

There is also an independent checkable proof from the classical Fourier series for dn (DLMF22.11.3). In Σ_j dn(u+2jK_b/N), the root-of-unity sum kills every Fourier mode except multiples of N. The surviving coefficients are precisely those for nome q_b^N, with the displayed scale. Uniform absolute convergence on the real axis legitimizes the finite sum rearrangement. Coprimality reorders jτ modulo N, so every primitive star uses exactly the same S_N.

For odd N, u→u+K_b changes the reduced argument by N K_N, congruent to K_N modulo 2K_N. The classical identity dn(x,m_N)dn(x+K_N,m_N)=sqrt(1−m_N) yields

B_+(w)B_-(w)
 = [r³t_M/(R²−d_0²)]² (N K_N/K_b)² sqrt(1−m_N),

independent of w. The source target is exactly recovered, for all odd primitive N, including coprime stars. Also q_b=sqrt(q_original), hence q(m_N)=q_original^(N/2), agreeing with the separately reconstructed trace lattice.

For even N the focus switch shifts the reduced argument by a full real period and gives equal focal areas, not constant product; finite even controls expose the distinction. The circular limit may be handled separately by regular-star rotation. No hyperbolic or collapsed caustic extension has been made.

## 7. Priority disposition

The arbitrary-order dn identity, quadratic transformations, and local addition formula are demonstrably older published analytic tools. The exact projectivity, circle/conic-to-bicentric identification, ordered contact-area telescope and original-focus phase alignment were freshly derived here. An older primary publication of those geometric steps for this exact observable has not been verified in this audit. Thus this bridge proves dependence on old analytic identities and supplies an alternative exact proof; it does **not**, by itself, establish that the focal-pedal theorem was previously resolved or historically new.

Radic2011's conjugate-bicentric area/perimeter product is a general conjecture in the read passage, and has not been used. RGR's limiting-point-pedal perimeter theorem is not a contact-area theorem. Generic projective equivalence does not preserve area, as exact controls show. The strongest responsible repair is to credit the generalized Landen identity explicitly and characterize any contribution as the source-specific geometric reduction/application, with priority of that application unresolved unless further primary evidence is obtained.
