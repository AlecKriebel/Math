# Turn 1: full 5-torsion of the normalized pentagonal pencil

**20000450 / AIM-ALGEBRAIC_NUMBER_THEORY-0102. Complete candidate after 1/5 substantive author turns, pending independent review.** The infinity-line and quotient reductions in the imported report are credited and checked here. Tate normal form, division polynomials and the full-level modular cover are classical; no historical novelty is claimed.

## 1. Conventions and answer

Put
\[
r=\sqrt5,\quad K=\mathbb Q(r),\quad \phi=(1+r)/2,\quad
 d=5+2r,\quad \delta^2=d,\quad c=\phi^5=(11+5r)/2.
\]
Use the following fixed equations for the regular pentagon and its circumcircle:
\[
Q=X^2+Y^2-T^2,
\]
\[
P=2(X^5-10X^3Y^2+5XY^4)+5\phi(X^2+Y^2)^2T
 -5\phi^3(X^2+Y^2)T^3+\phi^5T^5.
\tag{1}
\]
In the specialized arithmetic assertions lambda belongs to K; in the generic assertions lambda is an indeterminate and the base is K(lambda). The projective pencil is \(\Gamma_\lambda:P+\lambda TQ^2=0\). Let \(E_\lambda\) be its smooth projective normalization, with origin \(O=[0:1:0]\). We work with finite parameters
\[
\lambda\ne0,-5r,-c.
\tag{2}
\]
For every such parameter the normalization is geometrically integral of genus one. These are exactly the finite parameters with an elliptic normalization; the fiber at infinity is not elliptic either.

Here is the full arithmetic answer over K. Choose a primitive fifth root \(\zeta\) and any \(\theta\) with \(\theta^5=\lambda+c\). Then
\[
\boxed{K(E_\lambda[5])=K(\delta,\zeta,\theta).}
\tag{3}
\]
The same equality holds generically over \(K(\lambda)\). For \(\lambda\in K\) satisfying (2), its degree over K is four if \(\lambda+c\in K^{\times5}\), and twenty otherwise. In the latter case its Galois group is \(D_{10}\times C_2\), with \(D_{10}\) the dihedral group of order ten. Generically the degree is twenty. Also
\[
E_\lambda(K)[5]=0,\qquad E_\lambda(K(\delta))[5]\cong\mathbb Z/5\mathbb Z.
\tag{4}
\]
The latter subgroup is exactly the five infinity points.

Sections 2–5 give an explicit model, birational maps, and coordinates for all twenty-five geometric torsion points. Thus (3) is supplemented by a full division scheme, not just a semisimplification. The specified K-model has a rational origin and is not a nontrivial Tate–Shafarevich torsor. No local-solubility or arbitrary-twist assertion is made.

## 2. Checking the pentagon and reducing to a cubic

The side product (1) can be checked in complex coordinates Z=X+iY, W=X-iY. With \(\zeta=e^{2\pi i/5}\), the side factors can be scaled to
\[
L_j=Z+\zeta^{2j+1}W-(1+\zeta)\zeta^jT.
\]
Their product is
\(Z^5+W^5+5\phi Z^2W^2T-5\phi^3ZWT^3+\phi^5T^5\), which is (1). Consequently P is precisely a nonzero scalar multiple of the regular pentagon's five side equations.

Work affinely with T=1. Set
\[
\begin{aligned}
A(X)&=10X+5\phi+\lambda,\\
B(X)&=-20X^3+2(5\phi+\lambda)X^2-5\phi^3-2\lambda,\\
C(X)&=2X^5+(5\phi+\lambda)X^4-(5\phi^3+2\lambda)X^2+\phi^5+\lambda,\\
h(X)&=4X^2+2X-1.
\end{aligned}
\]
The equation is \(A(X)Y^4+B(X)Y^2+C(X)=0\). Direct expansion gives
\[
B^2-4AC=h^2(20X^2-aX+b),\quad
 a=40+20r+8\lambda,\quad b=a+5.
\tag{5}
\]
Put \(V=(2AY^2+B)/h\), so \(V^2=20X^2-aX+b\). With \(t=V-2rX\), this conic is parametrized by
\[
X=(b-t^2)/(a+4rt),\qquad V=2rX+t.
\tag{6}
\]
The conic discriminant is \(64\lambda(\lambda+5r)\), nonzero under (2).

Let
\[
z=t+5+2r,\quad \alpha=1-r/5,\quad \gamma=2r/5,\quad m=5-2r,
\]
and define the explicit cubic
\[
\begin{aligned}
F(z)={}&z^3-((3+r)\lambda+40+20r)z^2\\
 &+((60+36r)\lambda+900+400r)z\\
 &+(48+16r)\lambda^2+(500+220r)\lambda.
\end{aligned}
\]
Substitution into the original equation yields exactly
\[
Y^2=\frac{m\,z^2F(z)}{400(z+\gamma\lambda)^2(z+\alpha\lambda)}.
\tag{7}
\]
Thus, with \(s=z+\alpha\lambda\), \(w=20Y(z+\gamma\lambda)/z\), the function field has equation
\[
w^2=mF(s-\alpha\lambda)/s.
\tag{8}
\]
The substitution \(x_0=1/s,\ y_0=w/s\) makes this a cubic:
\[
y_0^2=a_3x_0^3+a_2x_0^2+a_1x_0+a_0,
\tag{9}
\]
where
\[
\begin{aligned}
a_0&=5-2r,\\
a_1&=(-26+10r)\lambda-20r,\\
a_2&=(42-86r/5)\lambda^2+(-100+100r)\lambda+500+200r,\\
a_3&=(-112+48r)\lambda^2(\lambda+5r)/5.
\end{aligned}
\tag{10}
\]
Since a3 is nonzero, the monic model with \(\xi=a_3x_0,\eta=a_3y_0\) is
\[
\boxed{W_\lambda:\quad \eta^2=\xi^3+a_2\xi^2+a_1a_3\xi+a_0a_3^2.}
\tag{11}
\]

For clarity, the inverse rational map to the plane is completely specified by
\[
s=a_3/\xi,\quad z=s-\alpha\lambda,\quad t=z-5-2r,
\quad X=(b-t^2)/(a+4rt),\quad
Y=\frac{\eta z}{20\xi(z+\gamma\lambda)}.
\tag{12}
\]
These formulas are inverse on dense opens; at their finitely many vanishing denominators they mean their unique extensions between smooth projective curves. They are not asserted as affine coordinate formulas at poles.

At s=0, F(-alpha lambda) is nonzero, while Y has a pole and X is finite. Its image is O=[0:1:0]. Thus the point at infinity of (11) corresponds to the required origin, not a translated group law. In fact the plane point O is always smooth, since its X-partial derivative is 10.

## 3. Smoothness and exceptional parameters

The exact discriminant of (11) is
\[
\Delta_W=2^{24}(161-72r)\lambda^5(\lambda+5r)^5(\lambda+c).
\tag{13}
\]
This proves nonsingularity under (2). To justify that it is the normalization of the entire plane curve rather than a selected component, the quadratic extension defining the conic in (5) is nontrivial over \(\overline K(X)\) when its discriminant is nonzero. Over that conic the remaining square root in (8) has four distinct branch points: the three roots of F and s=0. Indeed
\[
F(-\alpha\lambda)=(-16/5+16r/25)\lambda^2(\lambda+5r),
\]
\[
\operatorname{disc}F=(24064+10752r)\lambda(\lambda+5r)^3(\lambda+c).
\tag{14}
\]
Thus the original quartic in Y is irreducible over \(\overline K(X)\), and all the displayed transformations identify its field with (11).

At lambda=0 the curve is the five side lines. At lambda=-5r equation (1) becomes the same line-product identity with phi replaced by its conjugate (1-r)/2, so it is again a union of five lines. At lambda=-c, (8) remains a valid birational field description, but F has a double root and no triple root (its discriminant has a simple zero there). The normalization then has genus zero, rather than one. Finally the pencil member at infinity is TQ^2=0.

No extra exclusion is imposed merely because a plane vertex is not an ordinary node. For example the vertex tangent cone degenerates at lambda=-(25+10r)/4, but (13) is nonzero there; its normalization is still elliptic. The source asks about the genus-one normalization, and the formulas cover that parameter too.

## 4. Exact identification with a quadratic twist of Tate normal form

Define
\[
\beta=\frac{(11-5r)\lambda}{2(\lambda+5r)},\qquad
 k=\frac{4(\lambda+5r)}r,\qquad q=dk^2.
\tag{15}
\]
Let
\[
D_\beta:\quad y^2+(1-\beta)xy-\beta y=x^3-\beta x^2.
\tag{16}
\]
This is the standard Tate family; (0,0) has exact order five and its discriminant is \(\beta^5(\beta^2-11\beta-1)\). Under (2), beta is nonzero and not a root of that quadratic.

Here is an actual coordinate isomorphism over K(delta), not just a j-invariant match:
\[
\boxed{\xi=q(x-\beta),\qquad
\eta=(k\delta)^3\bigl(y+((1-\beta)x-\beta)/2\bigr).}
\tag{17}
\]
Expanding (17) gives exactly (11). Equivalently, if
\(T_\beta(x)=4x^3+(\beta^2-6\beta+1)x^2+2(\beta^2-\beta)x+\beta^2\), the polynomial identity is
\[
[q(x-\beta)]^3+a_2[q(x-\beta)]^2+a_1a_3q(x-\beta)+a_0a_3^2
 =q^3T_\beta(x)/4.
\tag{18}
\]
The formulas and this identity stay valid at j=0 or 1728. Conjugating delta to -delta composes (17) with elliptic negation, so (11) is the d-quadratic twist of (16), with the indicated K-rational scaling.

## 5. Coordinates for all twenty-five torsion points

On D_beta the known five are the origin and
\[
(0,0),\ (0,\beta),\ (\beta,0),\ (\beta,\beta^2).
\tag{19}
\]
The remaining twenty are obtained as follows. Let R_beta(x) have coefficients, in decreasing powers x^10 through x^0,
\[
\begin{array}{c|l}
10&5\\
9&5(\beta^2-5\beta+1)\\
8&\beta^4-7\beta^3+44\beta^2-38\beta+1\\
7&\beta(\beta^4+3\beta^3-26\beta^2+127\beta-9)\\
6&\beta^2(\beta^4+3\beta^3+19\beta^2-248\beta+36)\\
5&\beta^3(\beta^4+3\beta^3-71\beta^2+322\beta-84)\\
4&\beta^4(\beta^4-12\beta^3+94\beta^2-293\beta+126)\\
3&5\beta^5(\beta^3-10\beta^2+36\beta-25)\\
2&5\beta^6(2\beta^2-13\beta+16)\\
1&10\beta^7(\beta-3)\\
0&5\beta^8.
\end{array}
\tag{20}
\]
For each of its ten roots x, take both values
\[
y=\frac{-((1-\beta)x-\beta)\ \pm\sqrt{T_\beta(x)}}2.
\tag{21}
\]
Map (19)–(21) by (17) to (11), and if desired by (12) to the normalization of the original plane model.

To check completeness, set b2=beta^2-6beta+1, b4=beta^2-beta, b6=beta^2, b8=-beta^3. The standard fifth-division recurrence gives
\[
\begin{aligned}
\psi_3&=3x^4+b_2x^3+3b_4x^2+3b_6x+b_8,\\
H_6&=2x^6+b_2x^5+5b_4x^4+10b_6x^3+10b_8x^2\\
 &\qquad +(b_2b_8-b_4b_6)x+b_4b_8-b_6^2,\\
\psi_5&=T_\beta(x)^2H_6-\psi_3^3
       =x(x-\beta)R_\beta(x).
\end{aligned}
\tag{22}
\]
The identity is exact. In characteristic zero multiplication by five is separable, so these are precisely the twelve distinct x-coordinates of the twenty-four nonzero torsion points. None is a two-torsion x-coordinate, and all twenty choices in (21) are distinct. This also explains why a degree-ten polynomial, with the accompanying y-values, is a full coordinate computation rather than a mere torsion-line result.

## 6. The exact division field

We spell out the established modular input to prevent a false split-extension inference. Choose zeta with 1+zeta+zeta^(-1)=phi; changing the primitive root does not change the fields in (3). Over a field L containing zeta, fix the marked point P=(0,0) on D_beta. A complementary point Q with e5(P,Q)=zeta has five choices, Q+jP. The associated finite étale degree-five full-level cover has no residual pointed automorphism: an elliptic automorphism fixing a point of order at least four is the identity.

Fisher's Lemma 3.4 and its proof identify this cover by
\[
\beta=\tau\frac{f(\tau)}{g(\tau)},\quad
f=\tau^4+3\tau^3+4\tau^2+2\tau+1,\quad
g=\tau^4-2\tau^3+4\tau^2-3\tau+1.
\tag{23}
\]
The universal full-level interpretation, rather than an arithmetic rank theorem over Q, is what is base-changed here. With
\[
\varepsilon(\tau)=\frac{\phi\tau+1}{\tau-\phi},\qquad
\iota(v)=\frac{\phi^5v+1}{v-\phi^5},
\]
an exact identity is
\[
\tau f(\tau)/g(\tau)=\iota(\varepsilon(\tau)^5).
\tag{24}
\]
Both fractional-linear transformations are involutions. Thus the cover (23), over L, is precisely the Kummer cover
\[
\varepsilon(\tau)^5=\iota(\beta).
\]
For our value (15),
\[
\iota(\beta)=-1/(\lambda+c).
\tag{25}
\]
Consequently its splitting field is L(theta), with theta^5=lambda+c. This is an equality: the cover parametrizes the choices of Q, whose coordinates together with P give a full torsion basis, and conversely a full torsion basis determines that cover point. Equations (23)–(25) identify their finite étale fibers, including split specializations, not only the generic function field. All excluded cusp values have already been removed by (2).

Now take L=K(delta,zeta). The twist is trivial over L, so (17) proves
\(L(E_\lambda[5])=L(\theta)\).
To remove the prefixed L, first note that the infinity polynomial is
\(2X(X^4-10X^2Y^2+5Y^4)\), so the four nonorigin infinity points have X/Y equal to \(\pm\sqrt{5+2r}\) and \(\pm\sqrt{5-2r}\). Their field is K(delta). Rotation through 72 degrees preserves the pencil and cycles these points. On a genus-one curve in characteristic zero, an order-five automorphism is translation, since its origin-fixing part cannot have order five. Thus these points form an exact order-five subgroup, as already observed in the source and proved in the imported report. The full division field therefore contains delta. It also contains zeta by the Weil pairing. Hence it contains L, proving (3).

## 7. Degree, Galois group and rational torsion

The extension M=K(delta) is quadratic: the norm of d to Q is five, not a rational square. It is real, whereas K(zeta)/K is imaginary quadratic. Thus L/K is biquadratic.

For lambda in K put a=lambda+c, which is nonzero. If a is a fifth power in K, theta can be chosen in K and (3) has degree four. Conversely, if a is a fifth power in L, let u^5=a with u in L. Then N(u)^5=a^4, so (a/N(u))^5=a; it was already a fifth power in K. Thus if a is not a fifth power in K it is not one in L, and the Kummer extension L(theta)/L has degree five.

In the latter case K(zeta,theta)/K has Galois group D10: the order-five automorphism multiplies theta by zeta, and complex conjugation fixes the real fifth root theta while inverting zeta. Its unique quadratic subfield is K(zeta), which is distinct from M. Thus adjoining delta gives D10 times C2. Generically the valuation of lambda+c at lambda=-c is one, so it is not a fifth power and the same degree-twenty conclusion follows over K(lambda).

The full Tate torsion field K(D_beta[5]) is contained in K(zeta,theta). Formula (17) shows that the nontrivial automorphism of M fixing this latter field acts as -I on E_lambda[5]. It follows that no nonzero 5-torsion point is K-rational. Over the real field M, any rational 5-torsion lies in E(R)[5], which has exactly five elements; the infinity subgroup supplies all five. This proves (4).

The representation itself can be described as well. In the degree-twenty case, choose a basis whose first vector generates the infinity line. After choosing generators of the Galois factors and adjusting the second vector, their matrices are
\[
 \sigma_\delta\longmapsto-I,\qquad
 \sigma_\zeta\longmapsto\begin{pmatrix}1&0\\0&-1\end{pmatrix},\qquad
 \sigma_5\longmapsto\begin{pmatrix}1&1\\0&1\end{pmatrix}.
\tag{26}
\]
Here sigma_delta changes delta while fixing zeta and the real theta, sigma_zeta is complex conjugation, and sigma_5 is a suitable generator of the Kummer group. To justify the normalization, complex conjugation fixes the first basis vector and has determinant -1; adding a multiple of that vector makes the second anti-invariant. The nontrivial order-five subgroup acts by a nonzero transvection fixing the first vector, and its generator can be normalized as shown. In the degree-four case omit sigma_5. The Kummer class in the displayed full-level coordinate is -1/(lambda+c), equivalently lambda+c after inversion. This supplies the extension data that the infinity line and its Weil-pairing composition factor alone do not determine.

## 8. Dependencies, boundaries and review

The universal X(5) map is credited to Fisher, JEMS 3 (2001), Lemma 3.4, p.194; Tate normal form and the pointed-automorphism fact occur in Lemma 1.1 and equation (2), p.172. The primary PDF and relevant rendered pages were checked. The fifth-division recurrence is standard; exact expansion (22) and the coordinate identities are verified by the supplied script. The source gate records the original AIM question and its unspecified field/scaling conventions.

The claimed answer is for the explicitly normalized regular-pentagon pencil, with all elliptic fibers accounted for. General nonregular pentagons and arithmetic twists with no rational point are separate variants in the source remarks. No claim of a new Tate–Shafarevich class, local solubility, or historical novelty is included. Independent review must especially check the full-level cover interpretation, specialization of the division-field equality, the twist sign, and completeness of the exceptional set.
