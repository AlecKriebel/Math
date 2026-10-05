# Independently reconstructed universal certificate

This verifies an exposed candidate; it is not a blind discovery. The initial seal records a source-order violation. All mathematical statements below apply to the frozen currentv2 RESULT and are separately checkable without trusting any old verdict or finite control count.

Let t range over R/(2pi Z), c=cos t, s=sin t, g=(c,s,(c²-s²)/4), w=(-c³,s³,1), r=sqrt(1+c⁶+s⁶), and B=w/r. The once-covered circle projection makes g an embedded smooth closed regular curve. Direct differentiation gives g'=(-s,c,-sc), g''=(-c,-s,-c²+s²), g'''=(s,-c,4sc), and g'×g''=w. Thus |g'|²=1+c²s²>0, while w_z=1 proves everywhere positive Frenet curvature. Its osculating planes vary smoothly and B is exactly their unit Frenet binormal. In particular compatibility is with both first and second derivatives, not just an arbitrary normal framing.

B_z=1/r>0. Its ratios -B_x/B_z=c³ and B_y/B_z=s³ recover c and s by unique real cube roots. Equal B values therefore imply the same circle parameter. This gives global injectivity, including cardinal and antipodal points. Differentiating w=rB shows that B'=0 forces r'=0 by its z component, and then w'=0; conversely w'=0 gives r'=B'=0. The system w'=(3c²s,3s²c,0)=0 on c²+s²=1 is exactly cs=0. Thus B has precisely four stationary parameters. Its torsion is w·g'''/r²=3cs/r², which vanishes at those parameters. Smooth injectivity does not imply regularity of the spherical parametrization.

For every 0<e<1/3 define P=g+eB. On the convex closed unit disk extend B by F(x,y)=v/|v|, v=(-x³,y³,1). Here |v|>=1 and Dv has operator norm <=3. Normalization has differential (I-vv^T/|v|²)/|v|, of norm <=1/|v|. Consequently ||DF||<=3 and its planar projection F_xy is 3-Lipschitz, by integrating along the line segment joining any two disk points. For Q_e(p)=p+eF_xy(p),

    |Q_e(p)-Q_e(q)| >= (1-3e)|p-q|,
    |DQ_e(p)u| >= (1-3e)|u|.

Both lower bounds are strictly positive for distinct p,q or nonzero u. Restriction of Q_e to the circle is an injective immersion and therefore, by compactness, a smooth embedding. It is the planar projection of P, so P is also embedded. This holds for the entire claimed e interval, not merely an unspecified sufficiently small radius.

The global polynomial diffeomorphism H(x,y,z)=(x,y,z-(x²-y²)/4) has inverse adding the same polynomial and determinant1. The maps subtracting lambda times that polynomial form an ambient isotopy, 0<=lambda<=1. H(g) is the unit circle in z=0, spanning the oriented planar unit disk D. Direct substitution gives

    H_z(P)=e/r[1+(c⁴+s⁴)/2-e(c⁶-s⁶)/(4r)]
           >= e/r(1-e/4)>0.

The bound follows from r>=1, |c⁶-s⁶|<=1 and c⁴+s⁴>=0 and holds simultaneously for all t and every 0<e<1/3. Thus H(P) misses the entire disk D, not just its boundary. The two embedded loops are disjoint and their linking number, the algebraic intersection of the second loop with a spanning surface of the first, is zero. H preserves linking; hence Lk(g,g+eB)=0 for every such e. Orienting either loop differently cannot change zero. At e=0 disjointness fails; the distance bound is strict only below1/3, so no endpoint or wider interval is asserted. The compact normal-bundle theorem also supplies a thin embedded ribbon for sufficiently small positive widths. The claimed full interval is for the two boundary loops, not an unsupported full-strip embedding assertion.

The actual dated Ni–Zhang–Zhang v1 section2 prints V=(x,y,x⁴-y⁴), normal n=(-4x³,4y³,1)/sqrt(1+16x⁶+16y⁶), and gamma_a=(ac,as,a⁴(c⁴-s⁴)), a>0. Direct differentiation yields gamma_a'×gamma_a''=a²(-4a³c³,4a³s³,1). It is never zero; the graph normal along this embedded curve is its unit Frenet binormal. Its ratios recover c,s, proving injectivity. On the circle c⁴-s⁴=c²-s². For a=4^(-1/3), positive ambient homothety by1/a sends gamma_a exactly to g and preserves the unit Frenet binormal. It sends gamma_a+delta B to g+(delta/a)B. Therefore every 0<delta<a/3 inherits the complete embedded/disjoint/zero-linking certificate. This is exact prior-construction coverage. It does not establish that the source explicitly announced a Ghomi/linking theorem or the earliest historical recognition of that consequence.

A separate direct certificate for the printed a=1 graph disk uses alpha=e/|(-4x³,4y³,1)|>0 on x²+y²=1. For e<1/4, alpha<=e and 0<=1-4alpha x²<=1. Thus |x-4alpha x³|<=|x| and |y+4alpha y³|>=|y|. The normal offset q=(x-4alpha x³,y+4alpha y³,x⁴-y⁴+alpha) satisfies

    q_z-q_x⁴+q_y⁴
      =alpha+[x⁴-(x-4alpha x³)⁴]+[(y+4alpha y³)⁴-y⁴]
      >=alpha>0.

It misses the whole graph disk. Smooth normal-bundle embedding holds for sufficiently small offsets; this alternative argument does not assert embedding for every e<1/4.

For retained conditional statements, use arclength tangent T and C² compatible unit B with B·T=B·T'=0 and N=B×T. Orthogonality differentiation gives T'=kN, B'=-tau N and N'=-kT+tau B without dividing by k. Under an arbitrary positive speed v all derivatives acquire v. The twist density T·(B×B')=tau; rotating the normal framing by theta adds theta'. If B is regular then tau is continuous, nowhere zero and has fixed sign sigma. Its spherical unit tangent is U=-sigma N, d ell=|tau|ds, and (dU/dell+B)·(B×U)=k/|tau|. Therefore the spherical curvature form pulls back to k ds. A regular simple spherical B bounds a Jordan disk of area0<A<4pi; Gauss–Bonnet gives |integral k ds|=|2pi-A|<2pi. If k has one sign, this contradicts Fenchel's integral |k|ds>=2pi for a regular closed space curve. This conditional proof cannot apply at the four stationary points of our example. Nonzero framing twist alone never excludes writhe cancellation.

The signed-crossing formula can be independently reconstructed under its regular smooth embedded hypotheses. For generic fixed u, put a=u·T,b=u·N,c=u·B. Then a'=kb,b'=-ka+tau c,c'=-tau b. The blackboard normal V=(u×T)/|u×T| has moving angle with cos theta=c/sqrt(b²+c²), sin theta=-b/sqrt(b²+c²), yielding theta'=-tau+kac/(b²+c²). At each zero c=0, b!=0 and theta'=-tau!=0. Counting the two regular angle values gives relative framing degree -#(c=0)sign(tau)/2. Its linking is the signed planar diagram crossing sum, so Lk(g,B)=Cr(g_u)+#(u·B=0)sign(tau)/2. Angle lifts are interval-valued; a nonzero degree does not give a globally periodic real angle. The crossing sum is signed and can cancel. These hypotheses and reasoning do not extend this formula to our stationary-binormal example.

The ruled strip g+rN has second fundamental matrix [[0,tau],[tau,0]] at r=0 with identity metric, so K=-tau² there. The printed graph has Hessian determinant -144x²y² and K=-144x²y²/(1+16x⁶+16y⁶)², zero on axes. More generally K<0 makes the surface shape operator invertible, so its normal derivative on a regular curve cannot vanish. The four stationary values exclude the later strictly negative-curvature surface hypothesis. Neither that later question nor Nirenberg rigidity is resolved here. A continuous unit compatible binormal on a nonzero-curvature planar subarc is constant; every regular closed planar curve has such an arc, whereas straight intervals allow normal variation. These precise boundary qualifications in currentv2 are correct.
