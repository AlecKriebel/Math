# Exact transformations and obstruction certificates

Authored audit derivations, 2026-10-15. These certify what the tested transfers require; they do not constitute a claim of historical novelty. The source-to-claim ledger gives prior-source coverage separately.

## 1. The standard two-pole theorem contains the final analytic step

Let L,H>0 and let F be meromorphic with periods L and 4iH. Assume F(u+2iH)=-F(u) and that its only poles modulo these periods are simple poles at R and R+2iH. Let a be the residue at R. The second residue is -a by the anti-period. Choose the unique real modulus k_* in (0,1) with K_*'/K_*=2H/L, and put λ=2K_*/L. (The standard ratio of complete elliptic integrals ranges continuously and monotonically from infinity to zero.)

The function λ a cs(λ(u-R),k_*) has exactly the same periods, anti-period and principal parts: cs has residue 1 at 0, anti-period 2iK_*', real period 2K_*, and its second pole is at 2iK_*'. Subtracting leaves a holomorphic elliptic function, hence a constant; the anti-period makes that constant zero. Therefore

    F(u)=λ a cs(λ(u-R),k_*).

The ordinary Jacobi quarter-period identity then gives

    F(u)F(u+L/2) = -(λa)^2 k_*'.

Indeed, cs(z+K_*)=-k_*'/cs(z). This is the cs instance of Khare–Lakshminarayan–Sukhatme, *Cyclic Identities II*, arXiv:math-ph/0207019v2 §4(i), equation (66). The arbitrary-pole principal-part reconstruction is expressly treated in their *Local Identities*, arXiv:math-ph/0306028v1 §4.1, equations (40)–(45). This audit's displayed normalization is an independent deduction from those standard properties.

For the present candidate, the submitted target-specific lemma gives L=4K/N, H=K', and two simple pole classes for the cyclic inverse-edge sum. If that lemma is accepted, its half-period product is a classical elliptic-function consequence. The old sources do **not** identify the present outer-original-focus area trace or verify its pole cancellation. The necessary bridge is the explicit squared-distance factorization and inverse-edge principal parts, including coalescence at N=3. Thus: do not advertise a new general elliptic trace theorem, and do not mistake the availability of this standard final step for a pre-existing geometric proof.

The KLS hypothesis must be respected. Their unscaled Eq. (2) assumes fixed signs under both 2K and 2iK' translation. The present unsummed inverse-edge E(u) is not, in general, a single fixed-sign class under real 2K. It cannot simply be inserted into one master cyclic identity. One may first use E_e=(E(u)+E(u+2K))/2 and E_o=(E(u)-E(u+2K))/2, which respectively have (P,Q)=(1,0) and (1,1), and compute all principal parts. Alternatively the already reduced two-pole F, after the above rescaling of its torus, is a type-I function to which the principal-part reconstruction applies. Neither option supplies the missing target-specific pole data without further work.

## 2. Polarity and pedalization give a precise, but non-bicentric, bridge

Work in coordinates centered at f=(c,0). The unit-circle polar of a point q is the line

    (q-f)·(x-f)=1.

Its perpendicular foot from f is f+(q-f)/|q-f|², precisely the unit inverse of q. Consequently, if Q is the tangent-intersection outer polygon, its vertex inversions are the pedal vertices of the polar polygon Q* with pedal point f. The edges of Q* are the polars of the vertices of Q. Straight-edge shoelace area is retained under this construction; no circular arcs are substituted.

For a centered ellipse with coordinate semiaxes A,B, the focal-coordinate polar curve has equation

    (A²-c²)X²+B²Y²-2cX-1=0.                 (P)

To verify it, write a tangent as n·x=h where h²=A² n_x²+B² n_y². Its offset from f is h-c n_x; its pole has (X,Y)=n/(h-c n_x). Then (1+cX)²=A²X²+B²Y², which is (P).

The polar curve is a circle exactly when A²-B²=c². Thus the original boundary E has a circular polar, but the outer-locus ellipse O generally does not. In fact, using the canonical quantities t=sn²(v), q=1-t and k=c/α,

    A_o²-B_o² = c²(1-2t+k²t²)/q²,
    (A_o²-B_o²)-c² = -α² k²(1-k²)t²/q² < 0.

This strict difference holds throughout the stated noncircular, noncollapsed domain. The polar Poncelet family Q* is inscribed in the circle E* and circumscribed about the noncircular ellipse O*. It is **not** the bicentric family required by Roitman–Garcia–Reznik's limiting-point pedal theorem. That source's Appendix A gives the polarity/pedal mechanism, but its constant is perimeter for a different conic pair. Also, the two original foci use two different polarities and generally produce two different circle–ellipse pairs; one cannot silently treat them as the two limiting points of one bicentric pair.

This blocks the specific circle-pair transfer. It does not exclude a stronger theorem for special circle–ellipse pairs; none has been verified here.

## 3. Exact counterexample to an all-concentric inner-focus theorem

Take outer ellipse O: x²/4+y²=1 and inner ellipse E: x²+y²/(1/4)=1. They are concentric and homothetic by factor 1/2. Every affine image of a regular inscribed equilateral triangle is tangent to E, so these are one Poncelet triangle family. The foci of E are f_±=(±√3/2,0).

Two phases are

    T_0=((2,0),(-1,√3/2),(-1,-√3/2)),
    T_1=((√3,1/2),(-√3,1/2),(0,-1)).

Both have signed area 3√3/2. Invert their vertices in unit circles about f_± and use trajectory-order straight edges. Exact shoelace calculation gives

    T_0: B_+=(-27+42√3)/169, B_-=(27+42√3)/169,
         B_+B_-=27/169;
    T_1: B_+=B_-=3√3/14,
         B_+B_-=27/196.

The product difference is 729/33124, which is nonzero. All inversion denominators are nonzero; the explicit vertices and centers make this check immediate. `check_controls.py` reproduces the exact symbolic computation.

Therefore an alleged theorem asserting this focal product for **every** concentric odd Poncelet pair, with foci of the inner conic, is false even at N=3. AST's true all-concentric area-ratio theorem cannot be extended to this inverse-area product merely by changing the observable. The target's outer pair has additional billiard structure, so this is a counterexample to a transfer, not to k904,a.

The same failure occurs in general position. Keep O: x²/4+y²=1, now take E: 9x²/16+9y²=1 with axes (4/3,1/3), and use its foci (±√15/3,0). Two phases are

    U_0=((2,0),(-4/3,√5/3),(-4/3,-√5/3)),
    U_1=((4√2/3,1/3),(-4√2/3,1/3),(0,-1)).

All vertices lie on O. Each side n·x=h satisfies h²=nᵀdiag(16/9,1/9)n; the contact points lie strictly inside their segments. The script checks this exactly. Inversion products are respectively 1125/12544 and 9/128, with nonzero difference 243/12544. The complex conic intersections have x²=128/27, y²=-5/27, giving four distinct points with transverse tangent directions. Thus excluding homothetic/non-general-position pairs does not rescue the generic transfer.

## 4. Affine/grid and rationality alone are insufficient

The grid correspondence transports untransformed polygons by a fixed diagonal affine map, so their signed areas have a fixed ratio. It does not give a constant Jacobian after circle inversion. The differential determinant of unit inversion at x is -|x-f|^-4; anisotropic affine stretching does not preserve this weight. Already I_0(diag(2,1)(1,0))=(1/2,0), while diag(2,1)I_0(1,0)=(2,0). Thus an additional relation must be shown before transporting an inverse-area identity through the grid map.

Likewise, a trace being rational/meromorphic and invariant under the cyclic orbit shift does not make it constant as phase varies. On any elliptic curve with an N-torsion translation, a nonconstant meromorphic function on the quotient pulls back to a nonconstant invariant function. An explicit Jacobi model is f(u)=dn(Nu,k): its sum over u+4Kτj/N is N dn(Nu,k), which varies with u for 0<k<1. Constancy requires cancellation of poles or another genuine rigidity input.

## 5. The aligned inverse-area ratio remains a possible alternative route

If one established B_±(w)=r_± A_±(w) for the original inverse areas A_±, with r_± independent of phase, the original inverse-area product theorem would transfer to the outer product. This is the separate k806,a route. The correct corresponding outer parameter is Q(w+v) for consecutive original vertices P(w),P(w+2v). The authored diagnostics find constant B_+/A_+ in primitive N=3, N=5 convex and N=5 star examples after this alignment. Misaligned Q(w) gives a varying ratio in the odd-turn examples, so it is not a valid control of k806,a.

No established prior general proof of k806,a was verified in this audit. A conjectured ratio plus a conjectured original-vertex product merely relocates the difficulty. A campaign proof from 2026 is not evidence that a pre-2026 broad theorem anticipated the present exact target.
