# Adversarial boundary and inseparability controls

These are mathematical examples and local calculations, followed by explicitly limited finite sanity checks. They are not a proof by finite sampling of Lemmas A/B.

## 1. The numerical threshold is necessary

For X=P^2 and H a line, H is ample, H^2=1, and C is integral, but K_X+2H=-H has no section. Thus Lemma A would be false with the bound e>=1. The printed e>=2 bound excludes this case.

For X=P^1 x E with E elliptic, let H=P^1 x {e}. Then H is nef, integral and H^2=0. Its image in Alb(X)=E is a point, q=1>pa(H)=0, and (K_X+2H)|_H=O_{P^1}(-2), so K_X+2H has no nonzero section. This shows exactly where the positive-square argument is needed.

For X=P^1 x P^1 with H=(1,1), e=2, C has genus zero, K_X+2H=0 and h^0=1. The lower bound e+pa(C)-1=1 is attained.

If pi:Bl_z(P^1 x P^1)->P^1 x P^1 is a point blowup and H=pi^*(1,1), H is nef of square 2 but not ample. The strict transform of a smooth (1,1)-curve avoiding z is integral in |H|. Since K_X+2H is the exceptional divisor, it has a section. Contracted curves with zero H-degree therefore cause no failure.

## 2. A purely inseparable conductor family in every positive characteristic

Fix a prime p and let

S_p = V(x_0^p x_1 - x_2^p x_3) subset P^3_k,

where char(k)=p. It is integral: viewed as a polynomial in x_1, it is primitive of degree one over k[x_0,x_2,x_3], with coprime leading and constant coefficients. Its partial derivatives are

(0, x_0^p, 0, -x_2^p),

so its reduced singular locus is the line D=V(x_0,x_2). The surface degree is e=p+1, and the required adjoint degree is e-2=p-1. The explicit polynomial x_0^(p-1) already vanishes on D.

On x_3=1 its coordinate ring is

A=k[x,y,z]/(y^p-x^p z)=k[x,xt,t^p] subset B=k[x,t],

with x=x_0, y=x_2, z=x_1 and t=y/x in the common fraction field. The element t is integral over A, B is finite over A, and B is integrally closed, so B is the normalization. On the preimage of D the map is t |-> z=t^p, which is purely inseparable of degree p.

A monomial x^a t^b belongs to A if and only if a>=b mod p, where the residue is between 0 and p-1. Consequently x^a t^b lies in the conductor if and only if a>=p-1: multiplication by all powers of t cycles through every residue. Hence

cond_{B/A}=x^(p-1)B=(x,y)^(p-1)A.

This is a direct conductor calculation with no separability assumption. It also shows that the conductor need not be reduced when p>2, while it still vanishes on the entire reduced singular line.

The plane x_0+x_1+x_2=0 gives the plane curve

x_0^p(x_0+x_2)+x_2^p x_3=0.

It is integral by the same primitive degree-one argument, now in x_3, because x_2^p and x_0^p(x_0+x_2) are coprime. Its pullback on the normalization chart is

x(1+t)+t^p=0.

This is integral since 1+t and t^p are coprime. At the conductor point x=t=0 it is smooth (the derivative in x is 1), although its intersection with the conductor x=0 has length p. Thus a nonreduced fiber along the inseparable conductor does not force a nonreduced pullback curve.

For completeness, the normalization is smooth globally. The chart x_1!=0 has the symmetric normalization k[v,s] with x_2=v, x_0=vs and x_3=s^p. All points outside these two charts have x_1=x_3=0 and lie in the smooth locus of S_p. These charts and the regular locus cover its normalization. The plane curve is smooth away from its unique singular point on D (its three plane partials vanish only at x_0=x_2=0); the calculation above resolves that point. Hence this chosen pullback is a smooth rational curve on the smooth normalization, not merely a reduced curve. This explicit family is consistent with the asserted integral-pullback and conductor mechanisms in arbitrarily large characteristic.

## 3. Why a general plane really is needed

In characteristic 2, the special plane x_0+x_1+x_2+x_3=0 pulls back on x_3=1 to

x(1+t)+t^2+1=(t+1)(x+t+1),

which is reducible. The section x_1=0 gives t^p=0 on the normalization chart and is nonreduced. The original proof asks for a general integral plane section and never claims this for all planes, so these are boundary controls, not counterexamples to its claim.

## 4. Nonreduced Picard schemes

The checked source Liedtke, printed p. 26, Definition 6.5, gives nonclassical Enriques surfaces in characteristic 2 with pg=q=1 and b_1=0. Their Picard schemes are not smooth, but they fall in the pg>0 branch of Lemma A. Thus this genuine characteristic-p pathology does not invalidate the pg=0 implication used in the proof. No classification theorem is used to prove Lemma A.

## 5. Reproducible finite checks

Run `python3 finite_controls.py` from this directory. The script uses only the standard library. It verifies the derivative identity, the normalization parametrization on finite-field points, the conductor threshold in finite monomial boxes, coprimality at t=-1, smoothness at x=t=0, and the special characteristic-2 factorization for p in {2,3,5,7,11,13}. All checks passed. The universal statements above are justified by the displayed algebra, not by the finite output.
