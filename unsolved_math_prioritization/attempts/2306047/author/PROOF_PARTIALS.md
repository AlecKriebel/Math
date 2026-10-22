# Partial results for Function Theory 6.47

This is an authored partial investigation, not a solution or a novelty claim.

## 1. Exact target and conventions

Let D = {z in C : |z| < 1}. Let S consist of holomorphic injective functions on D with f(0)=0 and f'(0)=1. Write f(z)=z+sum_{n>=2} a_n z^n. Set

    U = {f in S : f' is injective on D},
    A_n = sup_{f in U} |a_n|,  n >= 2.

The target is to determine the sharp coefficient maxima A_n for the entire class U, including n=2. There is no assumption of real coefficients, convexity, starlikeness, boundary regularity, or injectivity of f^{-1} on D. This is not the bi-univalent inverse problem. The derivative is not normalized as an element of S: its constant coefficient is 1. A constant derivative is not injective, so the identity is not in U.

The governing source is Hayman–Lingham, Problem and Update 6.47, printed pages 135–136 of arXiv:1809.07200v2. The problem is an extremal question, not the assertion that A_n=1.

## 2. Normalization, attainment, and coefficient transfer

**Proposition 1.** Every f in U has a_2 != 0, and

    h(z) = (f'(z)-1)/(2a_2)

belongs to S. Consequently, the Bieberbach–de Branges theorem gives

    |a_n| <= 2|a_2|(n-1)/n,   n>=2.                 (1)

In particular A_n <= min(n, 2A_2(n-1)/n).

**Proof.** A holomorphic injective function has nonzero derivative everywhere. Apply this to f' at zero to get f''(0)=2a_2 != 0. Affine normalization preserves injectivity, and h(0)=0, h'(0)=1. Its coefficient of z^{n-1} is n a_n/(2a_2). Apply the coefficient theorem to h. The separate inequality |a_n|<=n follows by applying the same theorem to f. This uses an established theorem, not a new proof of it. Notice that dividing by 2A_2 instead of 2a_2 does not, for arbitrary f, give derivative 1 at zero.

**Proposition 2.** For every n>=2 the supremum A_n is attained by a member of U.

**Proof.** The normalized schlicht class S is compact in the topology of uniform convergence on compact subsets. Limits of injective holomorphic functions are either injective or constant. If f_j in U converge to f in S, then f_j' converge to f'. Thus f' is injective or constant. In the constant case the normalization gives f(z)=z. It follows that U union {z} is closed in S and compact. The function z/(1-z) belongs to U: its derivative is (1-z)^{-2}, injective because 1/(1-z) maps D to Re w>1/2 and squaring is injective on that half-plane. Its coefficients are all 1. Hence the maximum of |a_n| on the compact enlargement is at least 1, whereas the added identity has a_n=0. The maximum is therefore attained in U.

The addition of the identity in this compactness argument is essential; U itself is not closed.

## 3. An explicit nonsharp upper bound

Define C=(2+sqrt(13))/3, approximately 1.8685170918.

**Proposition 3.** A_2 < C. Therefore, for every n>=2,

    A_n < 2C(n-1)/n.

This is a strict but nonsharp upper bound; the argument does not give an explicit amount by which A_2 is below C.

**Proof of the weak bound.** The area theorem applied to the exterior schlicht function 1/f(1/zeta) gives

    |a_3-a_2^2| <= 1.                               (2)

Indeed its Laurent expansion begins zeta-a_2+(a_2^2-a_3)/zeta, and the area theorem bounds the sum of k times the squared moduli of its negative Laurent coefficients by 1. The n=3 instance of (1), requiring only the classical second coefficient theorem for h, gives

    |a_3| <= 4|a_2|/3.

With a=|a_2| these imply a^2 <= 1+4a/3. Solving this quadratic gives a<=C.

**Equality exclusion.** Rotate f by f_theta(z)=exp(-i theta)f(exp(i theta)z) so that a_2=a>0. If a=C, equality in the preceding triangle inequalities forces a_3=4a/3, hence the second coefficient of h is 2. The equality case of the second coefficient theorem forces h(z)=z/(1-z)^2. For completeness, it follows directly from the area theorem: the odd normalized schlicht function H(z)=sqrt(h(z^2)) has exterior reciprocal zeta-b_2/(2zeta)+..., so |b_2|=2 makes every subsequent negative Laurent coefficient vanish. Thus h(z)=z/(1-(b_2/2)z)^2; here b_2=2.

Integration then forces

    f(z)=P_a(z):=z+2a[1/(1-z)+log(1-z)-1],           (3)

with the analytic logarithm equal to zero at zero. Section 4 proves that P_a is not injective whenever a>2/(pi-2). Since C>9/5>2/(pi-2), equality a=C is impossible. Proposition 2 ensures the maximum A_2 exists, so the pointwise exclusion implies A_2<C. The rational inequalities C>9/5 and 9/5>2/(pi-2) follow from sqrt(13)>17/5 and pi>28/9, respectively.

The area theorem and the second-coefficient theorem are standard inputs. No assertion of priority for this combination is made.

## 4. Explicit derivative models and a local/global obstruction

### 4.1 The affine Koebe derivative

For positive a define P_a by (3). Then

    P_a'(z)=1+2a z/(1-z)^2,
    [z^n]P_a = 2a(n-1)/n, n>=2.

The derivative is injective for every a!=0, because k(z)=z/(1-z)^2 is injective: k(z)=k(w) implies (z-w)(1-zw)=0.

**Proposition 4.** If a>2/(pi-2), P_a is not injective on D.

**Proof.** Its coefficients are real. For 0<=r<=1,

    Im P_a(ir)=r+2a[r/(1+r^2)-arctan(r)]=J_a(r).

Near zero J_a(r)=r+O(r^3)>0, while

    J_a(1)=1+a(1-pi/2)<0.

The formula extends continuously to r=1, since i is not its singularity. The intermediate value theorem gives 0<r_0<1 with P_a(ir_0) real. Conjugate symmetry gives P_a(ir_0)=P_a(-ir_0) at distinct interior points.

A particularly clean control is a=9/5. Its derivative numerator is z^2+(8/5)z+1, with zeros -4/5 +/- 3i/5, both on the unit circle. Thus P_{9/5} is locally injective everywhere in D and P_{9/5}' is globally injective, yet P_{9/5} is not globally injective. Exact rational interval checks place a collision radius between 19/20 and 49/50. This disproves the proposed shortcut that derivative injectivity plus absence of critical points suffices for membership in U.

No sufficiency theorem for the entire range a<=2/(pi-2) is claimed here.

### 4.2 A convex-image normalization control

The elementary function

    G(z)=-(1/3)z-(4/3)log(1-z)

has G'(z)=(1+z/3)/(1-z)=1+(4/3)z/(1-z). The derivative is a Möbius map onto a half-plane, hence is convex and injective. Also

    1+zG''(z)/G'(z) = 1+z/(1-z)+z/(3+z).

For |z|<1, Re[z/(1-z)]>-1/2 and Re[z/(3+z)]>-1/2. Their sum with 1 is positive. The standard analytic convexity criterion proves G is convex and injective. Its coefficients are

    [z^n]G = 4/(3n), n>=2.

This checks the normalization and coefficients of the example in the source update. The rendered update prints a subclass bound in the form 4n/3 and calls this example sharp. The displayed value 4n/3 cannot be the sharp value for this example: its coefficient is 4/(3n). We do not silently use the printed expression as a sharp theorem for the whole convex subclass, and we have not independently inspected the cited 1983 proof of that subclass theorem.

## 5. The published candidate: exact coefficients and an authored limit

Hayman–Lingham attribute to Barnard–Suffridge a member F of U defined by

    F(0)=0,
    F'(z)=(1+z)/(1-z)^2 exp Q(z),
    Q(z)=(2/pi) sum_{k>=0} (-1)^k z^{2k+1}/(2k+1)^2.

The coefficient calculations below are proved here. Membership F in U is taken from that published report; the underlying 1983 proof was not accessible in this investigation and is not represented as independently verified.

Put x=1/pi. Direct formal multiplication, which is valid analytically in D, gives

    a_2(F)=3/2+x,
    a_3(F)=5/3+2x+(2/3)x^2,
    a_4(F)=7/4+(22/9)x+(3/2)x^2+(1/3)x^3.

The first value is approximately 1.8183098862. It exceeds the old proposed value 2/(pi-2), approximately 1.7519383939. Thus the earlier conjectured value of A_2 is not a current target.

**Proposition 5.** The coefficients of this explicitly defined analytic F satisfy

    lim_{n->infinity} a_n(F)=2 exp(2G_C/pi),          (4)

where G_C=sum_{k>=0}(-1)^k/(2k+1)^2 is Catalan's constant. The limit is approximately 3.5832456241.

**Proof.** Write exp Q(z)=sum_{j>=0} h_j z^j. The coefficient sequence of Q is absolutely summable, because sum (2/pi)/(2k+1)^2 < infinity. The Banach algebra of absolutely summable power series is closed under multiplication and the exponential series, so sum |h_j| < infinity. The coefficient of z^m in (1+z)/(1-z)^2 is 2m+1. Hence

    a_n(F)=sum_{j=0}^{n-1} ((2n-2j-1)/n) h_j.

For each fixed j the multiplier tends to 2 and has absolute value at most 2 when 0<=j<=n-1. Extend it by zero for j>=n and apply dominated convergence to the absolutely summable sequence h_j. The limit is 2 sum h_j=2 exp Q(1)=2 exp(2G_C/pi).

Conditional only on the published membership assertion, this implies liminf A_n >= 2 exp(2G_C/pi). Neither (4) nor finite coefficient agreement proves any coefficient maximum, or the membership assertion itself. The all-n extremal problem remains open in this package.

## 6. A rigorous obstruction to real-coefficient symmetrization

**Proposition 6.** The operation T f(z)=(f(z)+overline{f(overline z)})/2 need not preserve U, even when a_2 is already positive real.

**Proof.** Take the entire function

    E(z)=z-(exp(2iz)-1-2iz)/40.

It has E(0)=0, E'(0)=1, E''(z)=exp(2iz)/10, and a_2(E)=1/20. Its derivative is

    E'(z)=1+(exp(2iz)-1)/(20i).

For z in D,

    |E'(z)-1| < (e^2+1)/20 < 9/20 < 1,

using e^2<8. Thus Re E'>0. To see directly why this implies injectivity, for distinct z,w in the convex disk divide the line-segment integral E(z)-E(w) by z-w; the quotient is the average of E' on the segment and has positive real part.

The derivative E' is an affine transform of exp(2iz). If E'(z)=E'(w), then 2i(z-w)=2pi i k for an integer k, so z-w=pi k. Since |z-w|<2<pi, k=0. Thus E' is injective and E belongs to U.

However,

    TE(z)=z+(1-cos(2z))/40,
    (TE)''(z)=cos(2z)/10.

The latter vanishes at z=pi/4, which lies in D. Therefore (TE)' cannot be injective, and TE is not in U. Both E and TE have the same positive real a_2=1/20. In fact TE itself remains injective, because Re(TE)'>0 follows by averaging the two positive-real-part derivatives; it is specifically derivative injectivity that fails.

This is an obstruction to a proof strategy, not a counterexample to Clunie's extremal problem or to the possibility that some extremizer has real coefficients.

## 7. Exact remaining gap

No formula for the sharp A_2 or for the sharp A_n (n>=3) has been proved. There is no proof that a complex-coefficient extremizer may be chosen real. The source candidate's membership is reported by the governing collection but the original proof was not independently inspected. Current-status searches found no verified complete resolution, which is not proof that none exists. All mathematical partials here may already be known; no novelty claim is made.

## References

- W. K. Hayman and E. F. Lingham, Research Problems in Function Theory, arXiv:1809.07200v2, Problem and Update 6.47, printed pp. 135–136. https://arxiv.org/abs/1809.07200
- R. W. Barnard and T. J. Suffridge, On the simultaneous univalence of f and f', Michigan Mathematical Journal 30(1), 9–16 (1983). https://doi.org/10.1307/mmj/1029002783
- T. J. Suffridge, Typically real functions with typically real derivative, Complex Variables, Theory and Application 7(1–3), 215–230 (1986). https://doi.org/10.1080/17476938608814200. Bibliographic metadata verified; full proof not inspected.
- L. de Branges, A proof of the Bieberbach conjecture, Acta Mathematica 154, 137–152 (1985). https://doi.org/10.1007/BF02392821. Used as an established theorem; publisher metadata inspected, original proof not reverified.
