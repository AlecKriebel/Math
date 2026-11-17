# Source-first adversarial derivations — row176

These are actual hand calculations after the complete original manuscript/PDF/pixels/metadata and before support code, archived opinions/results, new outside primary bodies or peer coordination. They check the full stated theorem and reductions, without treating the cited problem's interpretation or historical overlap as already established.

## 1. Exact class and normalization

For a holomorphic injection on the disk, a zero derivative would give a local mapping of multiplicity at least two, contradicting injectivity. Thus P=f''/f' is holomorphic. Real Taylor coefficients imply conjugation symmetry and conversely by uniqueness of power series. On the real interval f' is real, continuous, nonzero and starts at one, hence stays positive. A real-on-real injection with arbitrary nonzero real derivative can be affinely normalized without changing its pre-Schwarzian quotient.

For z≠0 the original centered quantity equals z A_f(z)/(1-|z|^2). Its modulus is |z| |A_f(z)|/(1-|z|^2), so strict shrinking of the SAME centered disk is exactly the asserted M(z)<4. At z=0 the original expression is zero while A_f(0)=f''(0), and these must not be conflated.

## 2. Exterior injection and coefficient equality

For normalized F, F(z)/z has no zeros, including its value one at zero, so the logarithm L is globally well-defined on the simply connected disk. The exterior map H(w)=w exp[-L(w^-2)/2] satisfies H(w)^2=1/F(w^-2) and is odd/nonzero. Equal values force w_2=±w_1 by injectivity of F; the minus choice is excluded by oddness and nonvanishing. Thus H really is an exterior injection, rather than just a formal Laurent expansion.

For each R>1 the image circle is a simple analytic Jordan curve. The map extends conformally at infinity with leading term w, so its exterior maps to the unbounded component and its standard enclosing orientation is positive. Fourier orthogonality in the Green integral gives area/pi=R^2-Σ n|b_n|^2 R^(-2n). The Laurent series and derivative converge uniformly on the fixed circle. Bound every finite nonnegative partial sum by R^2, take R down to one, then increase the partial sum length; no unjustified exchange of an infinite sum with a boundary limit is needed.

Here b_1=-a_2/2. Equality |a_2|=2 exhausts the entire coefficient budget, forcing b_n=0 for n≥2, while oddness forces b_0=0. Hence H=w-lambda/w, |lambda|=1, and F(z)=z/(1-lambda z)^2. Conversely the difference numerator is (z-w)(1-lambda^2 zw), whose second factor cannot vanish in the disk. This verifies both the inequality and its complete equality classification used later.

## 3. Equality images versus equality functions

For phi_a(w)=(a+w)/(1+conj(a)w), phi_a'(0)=1-|a|^2 and phi_a''(0)=-2conj(a)(1-|a|^2). Expanding the normalized transform directly gives 2a_2(T_a f)=(1-|a|^2)P_f(a)-2conj(a)=A_f(a). Equality therefore classifies T_a f, not f itself. Its image implies that f(D) is the complement of one affine ray.

An explicit adversarial control shows why skipping that distinction would be false. Let g=T_(i/2) k_+. The general connection covariance at w=-i/2 gives A_g(-i/2)=4. But a_2(g)=(6+4i)/5 has modulus squared52/25<4 and is not real, so g is neither a Koebe rotation nor a member of S_R. Equality at a nonreal point can occur in the full class S. This is not a counterexample to the real-class claim; it isolates the essential symmetry argument.

For real-class f its image and the single missing ray are conjugation invariant. The unique finite endpoint is real; conjugation preserves the ray's direction, forcing that direction real as well. Zero lies in the image, so the ray must be (-infinity,c] with c<0 or [c,infinity) with c>0. The appropriate g=4|c| k_± has the same image and g(0)=0. Thus g^-1 f is a disk automorphism fixing zero, and its positive real derivative is1/(4|c|). A disk automorphism fixing zero is a rotation, so |c|=1/4 and that rotation is the identity. Consequently the only real-class functions able to attain the classical equality anywhere are k_+ and k_-.

## 4. Exact Koebe deficit and real-axis obstruction

Direct logarithmic differentiation gives P_(k±)=(±4+2z)/(1-z^2). Therefore

A_(k±)(z)=[±4(1-|z|^2)+4i Im z]/(1-z^2).

Since |1-z^2|^2=(1-|z|^2)^2+4(Im z)^2, the squared modulus is16-48(Im z)^2/|1-z^2|^2, strictly below16 at every nonreal point. For real x it is respectively+4 or-4. These two opposite endpoints also force classical minimal radius even if one is allowed to recenter the disk at any nonzero real evaluation point. At zero that recentering statement must still be distinguished from the identically zero original quantity.

## 5. Compactness: exclusion of a bad maximizing sequence

Pointwise strictness alone is insufficient: a sequence of functions could in principle approach the boundary value four at one fixed nonreal point. The source's normalization prevents degeneration. The universal disk bound gives |P_f(re^(i theta))|≤(4+2r)/(1-r^2). Integrating gives log|f'(z)|≤log(1+r)-3log(1-r), and integrating the derivative bound gives |f(z)|≤r/(1-r)^2. Thus the family is locally uniformly bounded.

Any locally uniform subsequential limit has f(0)=0,f'(0)=1, so is nonconstant. For each fixed w, the divided differences (f_n(z)-f_n(w))/(z-w), extended at w, converge locally uniformly and have no zeros. Their limit cannot be identically zero without making f constant. Hurwitz therefore preserves injectivity and the nonzero derivative. This proves closedness as well as normality; reflection symmetry is also closed. Hence S_R is compact in the metrizable compact-open topology.

If functions f_j at a fixed nonreal z had |A|→4, compactness and convergence of derivatives/denominator would give a real-class equality function there, contradicting the exact deficit. The same contradiction works for z_j in a compact nonreal K by also taking z_j→z in K. This independently explains both attained maxima and compact-set-uniform strictness. It is not a merely finite sample bound.

## 6. Real-transform covariance and orbit coordinate

For real a, f'(a)>0 ensures the transform stays in the normalized real class; direct composition gives T_-a T_a f=f. Chain rule gives

A_(T_a f)(w)=[(1+a conj(w))/(1+aw)] A_f(phi_a(w)),

whose prefactor has modulus one. Also 1-phi_a(w)^2=(1-a^2)(1-w^2)/(1+aw)^2 and Im phi_a(w)=(1-a^2)Im w/|1+aw|^2, proving delta invariance directly. The source's formula for a solves x a^2-(1+r^2)a+x=0; its chosen root has modulus below one because 1+r^2>2|x| inside D. It sends z to a purely imaginary point. Conjugation handles the sign. The invariant delta=t/(1+t^2) is strictly increasing on0<t<1, with inverse2delta/(1+sqrt(1-4delta^2)). Thus it really labels these evaluation-point orbits rather than merely giving a necessary invariant.

## 7. A non-Koebe real-class control

For h(z)=z/(1-z^2), h(z)-h(w)=(z-w)(1+zw)/((1-z^2)(1-w^2)), so it is globally injective in D, not merely locally univalent. Its pre-Schwarzian is2z(3+z^2)/(1-z^4), and A_h(it)=8it/(1+t^2). Real transforms transport this lower bound to every evaluation-point orbit. It is a LOWER bound, never a positive upper gap.

At z=i/2, delta=2/5. The real Koebe squared value is208/25, while this h gives256/25; thus the two Koebe maps cannot be the only extremizers there. This does not prove h is an extremizer. The two lower branches cross when16-48delta^2=64delta^2, i.e. delta=1/sqrt7, corresponding to t=(sqrt7-sqrt3)/2. No formula for the unknown M is inferred from their maximum.

## 8. Global-gap and endpoint controls

Fix an interior real x_0 and take z=x_0+i epsilon inside D. The Koebe value tends to four, so a positive gap uniform over all nonreal points is impossible. Independently, z=it→i gives h's value8t/(1+t^2)→4. Both sequences escape every compact subset of D\R and do not contradict the theorem.

Merely Im z→0 at an endpoint does not force delta→0. For z=1-s+i c s with fixed c>0 and small positive s, the point is inside D and delta→c/(2sqrt(1+c^2)), strictly between zero and one-half. Thus endpoint geometry must be expressed in delta rather than just imaginary height, as the note does. No boundary point is inserted into the interior compactness argument.

## 9. Remaining source-import/verification questions

The literal Hayman–Lingham Problem6.86 fixed-point wording and its dated update remain to be read from an actual primary edition after this seal. Classical Montel/Hurwitz and disk-automorphism facts are the only general analysis inputs used above; the note itself derives the needed coefficient equality and distortion bounds. Historical overlap with Jenkins/Aleksandrov–Popova and the proposed Rodemich shortcut are not certified by reading the candidate's discussion. No firstness/current-openness or sharp-radius conclusion is presumed. No code, exploratory Loewner output or external mathematical body has been used for these checks.
