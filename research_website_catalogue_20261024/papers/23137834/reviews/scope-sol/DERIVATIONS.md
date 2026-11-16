# Actual source-first hand derivations

These calculations precede all foreign/support/program/opinion exposure. They reconstruct scope and proof interfaces from the actual native manuscript. They do not pretend to expand every long table coefficient or resultant, whose exact post-INITIAL check remains pending.

## 1. Constants and all four parameter cusps

Write r²=5, phi=(1+r)/2, c=(11+5r)/2, d=5+2r, m=5-2r. Then phi²=phi+1, phi³=2phi+1, c=5phi+3, c^-1=(5r-11)/2, c-c^-1=11, c+c^-1=5r, and dm=5. In particular the Tate parameter simplifies to

    beta=-lambda/[c(lambda+5r)].

This is a nonconstant Mobius map. Its cusp correspondences are lambda=0 -> beta=0; lambda=-5r -> beta=infinity; lambda=-c -> beta=c; lambda=infinity -> beta=-c^-1. Direct subtraction gives

    beta-c=-5r(lambda+c)/(lambda+5r),
    beta+c^-1=5r/[c(lambda+5r)],
    beta²-11beta-1=-125(lambda+c)/[c(lambda+5r)²].

Thus the allowed finite lambda range maps exactly to the Tate cusp complement P1 minus{0,infinity,c,-c^-1}. One must not accidentally allow lambda=infinity because its Tate image is finite. The full-level Kummer cover is allowed to ramify over cusps that are removed; no such ramification permits dropping an extra smooth fiber.

The two radical ratios reduce without guessing a fifth-power class:

    (beta-c)/(beta+c^-1)=-c(lambda+c),
    (c beta+1)/(beta-c)=-1/(lambda+c).

For the second identity, c beta+1=5r/(lambda+5r). Since c=phi^5, adjoining a fifth root of the first ratio gives the same field as theta^5=lambda+c. A root of the second ratio is u=-1/theta. Its Kummer class is the inverse class of lambda+c, not the same nontrivial fixed class; the inversion must be recorded. Both Mobius involutions in the paper square to scalar matrices: epsilon has matrix[[phi,1],[1,-phi]], square(phi²+1)I; iota has matrix[[c,1],[1,-c]], square(c²+1)I. These constants are nonzero.

## 2. Primitive whole-curve normalization, not one component

Expanding the plane equation by powers of Y gives the stated A,B,C immediately: the X Y^4 coefficient is10X, the radial quartic contributes5phi, the lambda term contributeslambda, and the remaining even powers give B,C. For A=10X+e, e=5phi+lambda, its only root is X0=-e/10. Then

    B(X0)=e³/25-5phi³-2lambda
          =lambda[lambda²+15phi*lambda+25(3phi²-2)]/25
          =lambda(lambda+5r)(lambda+5(phi+1))/25.

The last factorization uses r=2phi-1 and r(phi+1)=3phi²-2. Away from0,-5r, the only possible common A,B root occurs at lambda=-5(phi+1). There e=-5,X0=1/2,5phi³+2lambda=-5, and

    C(1/2)=1/16-5/16+5/4+c-5phi-5=-1.

So there is no vertical component hidden when passing to K(X). Independently, for a=40+20r+8lambda,b=a+5,

    a²-80b=64lambda²+320r*lambda=64lambda(lambda+5r).

Thus the first conic square root is genuinely quadratic over the algebraically closed coefficient field's rational X-field on the allowed range. Conditional on the read explicit F-discriminant and F(-alpha*lambda) identities, the second square root has exactly four odd branch points: three distinct finite F roots and s=0. Infinity has even pole/order because F(s-alpha*lambda)/s behaves as s². The tower has degree4 over Kbar(X), proving quartic irreducibility; Riemann-Hurwitz gives2g-2=2(-2)+4=0. Together with the content check and nonzero degree5 restriction at T=0, this proves geometric integrality of the entire projective member, not merely a selected component. At lambda=-c, one double F root removes two branch contributions, leaving two odd points and genus0; the stated double-root/gcd identity still needs exact arithmetic corroboration. Lambda0 and-5r are reducible line products, and the infinite member TQ² is excluded.

## 3. The included cusp checked directly at a vertex

(1,0) is a pentagon vertex: P(1,0)=2+5phi-5phi³+c=0. Its first partials vanish. Put X=1+u,Y=v. The quadratic term of P+lambda Q² is

    (25+10r+4lambda)u²-25v².

Indeed P_XX(1,0)/2=15+20phi=25+10r, while the Y² coefficient B(1)=-25; Q=2u+u²+v² contributes4lambda*u² at degree2. The exceptional plane value is lambda*=-(25+10r)/4=-5d/4. There the u³ coefficient is(20+20phi)+4lambda*=5, so the local equation starts-25v²+5u³. This is an ordinary cusp, not a smooth plane point or a genus0 conclusion. Rotation transports it to all five vertices.

At this same lambda*, lambda*+5r=-5m/4 and lambda*+c=-3/4; all three relevant factors are nonzero. Therefore the stated cubic discriminant does not vanish and the normalization remains elliptic. The plane-node/cusp distinction cannot be used as a reason to exclude this fiber from the torsion theorem. Moreover -3/4 is not a fifth power in K: its rational norm is9/16, whose3-adic valuation2 is not divisible by5. Conditional on the exact torsion-field interface, this included fiber belongs to the nonsplit degree20 case.

## 4. Origin, infinity and normalized-versus-plane points

At T=0,Y=1, the polynomial is2x(x^4-10x²+5); its five roots are0,±sqrt(d),±sqrt(m). Its X derivative is10(x^4-6x²+1): at0 it is10, and at x²=d,m it is160±80r, both nonzero. All five infinity points are smooth on the plane member, independently of lambda. Since sqrt(m)=r/delta, all lie in M=K(delta). The72degree rotation has cos=(r-1)/4 in K and sin=delta/(1+r) in M; it cyclically permutes them. In characteristic0 an order5 automorphism of an elliptic curve must be translation when its origin-fixing component has no order5. Thus the orbit forms the known subgroup; the imported automorphism fact will be checked in the primary interface.

At cubic infinity ord(xi)=-2,ord(eta)=-3. Hence s=a3/xi has order2,w=eta/xi order-1. The inverse denominator limits z=-alpha*lambda,z+gamma*lambda=(gamma-alpha)*lambda and a+4rt=4(3-r)*lambda are nonzero on allowed fibers, so Y has a simple pole while X tends to-(5phi+lambda)/10. This maps to[0:1:0], whose plane X partial is10, proving that the chosen origins agree rather than merely differing by a translation.

For the residual points, x is neither0 nor beta, and the identity z+gamma*lambda=(gamma-alpha)*lambda*x/(x-beta) makes every displayed inverse denominator nonzero. A zero numerator z is not an exclusion: when z=0, t=-d and X=(b-d²)/(a-4rd)=8lambda/(8lambda)=1,Y=0, a plane vertex. Different normalized branches may therefore be represented by the same singular plane image. The theorem counts distinct points on the smooth cubic/normalization, not necessarily25 distinct points of the plane projective set.

## 5. Exact twist rather than a j-invariant comparison

Completing the square in D_beta gives v=y+((1-beta)x-beta)/2 and

    v²=T_beta(x)/4.

With xi=q(x-beta),eta=(k*delta)^3 v and q=d k², eta²=q³v². Comparison of the four cubic coefficients reduces the isomorphism claim to the compact identities

    a2/q=(beta²+6beta+1)/4,
    a1*a3/q²=beta²(beta+1)/2,
    a0*a3²/q³=beta^4/4.

These conditions imply the whole equation identity, including sign and ordinate scaling. They are stronger than a j match and are finite symbolic identities to check after INITIAL. The last follows by substituting a0=m,a3=-16(7-3r)lambda²(lambda+5r)/5 and using(d/c)²=5(7-3r)/2. Neither k nor q nor a3 vanishes on the allowed range; no special-j denominator is present.

The same comparison predicts the cubic discriminant independently from the Tate one. From beta^5(beta²-11beta-1),

    Delta_beta=125lambda^5(lambda+c)/[c^6(lambda+5r)^7].

Multiplying by q^6 gives2^24[d^6/(125c^6)]lambda^5(lambda+5r)^5(lambda+c). Since((7-3r)/2)^3=161-72r and(d/c)²=5(7-3r)/2, the scalar is exactly the paper's2^24(161-72r). This is an all-parameter check of the discriminant scaling, conditional only on the compact coefficient match, not a selection of numerical j values.

## 6. Division-polynomial completeness and denominator issues

For P0=(0,0), the tangent is y=0; its third intersection is(beta,0), so2P0 is its negative(beta,beta²). Since the sum of these two points and P0 on the appropriate line yields3P0=(beta,0)=-2P0, P0 has exact order5, beta!=0 being guaranteed. Negation on the completed-square model is v->-v.

The printed psi5 has leading coefficient32-27=5 in degree12, consistent with x(x-beta)R and R's degree10 leading coefficient5. At x=0, T=beta²,H6=-beta^5,psi3=-beta³, so psi5(0)=0. Differentiating the displayed formulas gives psi5'(0)=-5beta^9, hence R(0)=5beta^8. At x=beta,T=beta^4, agreeing with the two marked ordinates0,beta². At beta=1 the table's eleven coefficients sum5, an independent arithmetic endpoint check of R_beta(beta)=5beta^12. The full coefficient identity and both resultant identities remain to be checked exactly, not inferred from these partial controls.

If the nonzero resultant identities hold on every nonsingular fiber, they exclude T=0 and psi3=0 at every psi5 root. Thus chord-law denominators for2P and3P are legitimate, and equal abscissae imply2P=±3P. The plus case would force P=O, impossible for an affine point; the minus case gives5P=0. Conversely every nonzero5-torsion point satisfies the relation. In characteristic0 separability gives25 kernel points. The24 nonzero points pair as ±P with12 distinct x coordinates, and no2-torsion intersects nonzero5-torsion. Removing the two marked abscissae leaves ten distinct residual x roots, each with two distinct ordinates. This proves completeness conditional on precisely identified universal identities and separability, rather than counting roots in a test field.

## 7. Exact arithmetic extension and action, including split fibers

N_K/Q(d)=5, so d cannot be a square in K (the norm of a square is a rational square). M=K(delta) is a real quadratic extension of K, while K(zeta5)/K is imaginary quadratic. Thus L=K(delta,zeta5) has degree4. For a=lambda+c in K*, if v^5=a in L and N=N_L/K(v), then N^5=a^4 and(a/N)^5=a. Thus a is a fifth power in L iff it already is one in K; the split criterion does not change after adjoining the two quadratic fields.

Assuming the actual full-level/Verdure interface yields L(E[5])=L(theta), Kummer theory then gives degree1 or5 over L. The twist image of P0 has eta=-k³*d*delta*beta/2 with nonzero K coefficient, so the full E torsion field contains delta, not just an upper bound field. Weil pairing forces zeta5. Consequently the full field contains L and equals L(theta); this lower inclusion is indispensable.

In the nonsplit case, over K(zeta5) the cyclic generator sends theta->zeta5*theta. Complex conjugation fixes the chosen real theta and inverts zeta5, giving D10 over K. Its unique quadratic subfield is K(zeta5), so it cannot contain the distinct real M. Adjoining delta therefore gives D10xC2; in the split case it gives C2xC2. Over K(lambda), valuation at lambda=-c of lambda+c is1, so the generic radical cannot split.

The independent delta involution acts as-I on E[5], hence fixes no nonzero K-rational vector. A complementary basis can be adjusted to be anti-invariant under complex conjugation: if conjugation(Q)=aP-Q, replace Q by Q-(a/2)P in F5. Then the matrices are-I,diag(1,-1), and the nonzero transvection[[1,1],[0,1]], after choosing its generator. Their common invariant line over M is the infinity line; over K the-I kills it. Determinants match the cyclotomic character. This also explains the real-group argument E(R)[5] has order5.

Concrete split/nonsplit controls, conditional on the primary field criterion: lambda=1-c has a=1 and degree4; lambda=2-c has a=2 and degree20, since N(2)=4 has2-adic valuation2, not divisible by5. Both avoid the excluded parameters. The included cuspidal fiber has a=-3/4 and also degree20 by the norm calculation above. No uniform degree20 claim may overwrite these split fibers.

## 8. Exact remaining checks and no provisional promotion

The source-first calculations establish the consistency of the scopes, several nontrivial all-parameter identities and explicit boundary controls. They leave the long geometry/discriminant/table/resultant expansions and the actual imported full-level/specialization/separability interfaces for necessary post-INITIAL checking. This is an evidentiary list, not an assumed PASS or a discovered defect. A failure in a central identity or specialization interface will be reported against the original theorem without repair/narrowing. No finite program output will substitute for the all-fiber proof.
