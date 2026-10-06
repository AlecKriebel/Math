# Independent surface derivations for original PR293

Scope: the exact Lemmas A and B in original-head `6e717193f93c8a321cce1ce35a00eed1ecfb56e7`, `PUBLIC_TURN_2.md`. This is an adversarial AI mathematical review, not a priority audit or human peer review. The initial derivation in `INDEPENDENT_INITIAL_DERIVATION.md` was recorded before reading the author proof or any prior reviewer proof. Subsequent derivations below compare and check the author's exact mechanism.

## 1. Lemma A and the positive-characteristic traps

Let $k$ be algebraically closed of any characteristic, $X$ a smooth integral projective surface, and $H$ a nef Cartier divisor with $H^2=e\ge2$. Let $C\in|H|$ be integral. Put $p_g=h^0(X,\omega_X)$, $q=h^1(X,\mathcal O_X)$, and $a=p_a(C)$.

If $p_g>0$, multiply a nonzero canonical section by the square of the section defining $C$. The product is nonzero on the integral surface, giving a section of $\omega_X(2H)$. Thus any obstruction must have $p_g=0$.

In that case Serre duality gives $H^2(X,\mathcal O_X)=0$. In a square-zero thickening the obstruction to lifting a line bundle lies in $H^2(\mathcal O_X)\otimes I$. More explicitly, the sequence $1+I\mathcal O_X\to\mathcal O^*_{X_T}\to\mathcal O^*_{X_R}\to1$, with $1+I\mathcal O_X\simeq I\mathcal O_X$, gives surjectivity on $H^1$ when the $H^2$ obstruction vanishes. The Picard scheme is therefore smooth at the identity. Its tangent dimension is $q$, and its reduced identity component is dual to $A=\operatorname{Alb}(X)$. Hence

$$
q=\dim A.
$$

This equality is not asserted for arbitrary positive-characteristic surfaces. Nonreducedness would make tangent dimension exceed the reduced dimension; it cannot occur in this $p_g=0$ branch. If it occurs outside this branch, the preceding $p_g>0$ argument already supplies the required section. Liedtke pp.13–14 and Kleiman Proposition 5.19, including its square-zero proof on pp.46–47, verify the exact implication without a characteristic-zero assumption.

Let $\widetilde C$ be the normalization of $C$. It is a smooth projective curve because $k$ is perfect. Choose a $k$-point over $C$ as the origin of the Albanese map. The map $\widetilde C\to A$ factors through its Jacobian. For positive genus this is Milne, *Jacobian Varieties*, Proposition 6.1; for genus zero the map from $\mathbf P^1$ is constant (Milne, *Abelian Varieties*, Corollary 3.8), and the zero Jacobian has the same universal property. Let $B\subset A$ be the reduced image abelian subvariety of the induced homomorphism.

Suppose $B\ne A$. The quotient map $b:X\to A/B$ is constant on $C$. If $M$ is ample on $A/B$, then $N=b^*M$ is nef and $N\cdot H=N\cdot C=0$. Its square is nonnegative. This can also be checked without a general nef-cone theorem: a large power of $M$, and thus of $N$, is globally generated, and its two general divisors have nonnegative intersection. Algebraic Hodge index with $H^2>0$ forces $N\equiv0$. Kleiman Theorem B.27 directly states this implication with $H^2>0$; it does not require $H$ ample.

If $b$ were nonconstant, an integral curve $D\subset X$ would map nonconstantly. One precise existence argument uses Milne AVs Lemma 3.5: integral curves through any fixed smooth $k$-point form a dense union. If every such curve mapped constantly, they would all map to the same point, so its closed fiber would be dense and $b$ would be constant. On the normalization of a nonconstant $D$, the pullback of $M$ has positive degree: the morphism onto its image curve is finite of positive degree, including any inseparable degree. This contradicts $N\equiv0$. Thus $b$ is constant, contrary to generation of $A$ by the Albanese image. Therefore $B=A$.

An alternative independent verification avoids depending on the quotient construction. By Poincaré reducibility (Milne AVs Proposition 12.1), choose $B'\subset A$ so $r:B\times B'\to A$ is an isogeny. By Milne AVs §8 there is an isogeny $s:A\to B\times B'$ with $s r=[n]$ for some $n>0$, including characteristic dividing $n$. Then $\rho=\operatorname{pr}_{B'}s$ is surjective and kills $B$; if $B\ne A$, its target has positive dimension. Apply the same ample-pullback argument to $\rho a$. The quotient used by the author also exists; Conrad's Homework 8 Exercise 1 describes its construction by exactly this reducibility/finite-quotient mechanism. That exercise is corroboration, not a substitute for the independent sufficient-homomorphism argument just given.

Surjectivity $J(\widetilde C)\to A$, not any injection of tangent spaces, gives

$$
q=\dim A\le g(\widetilde C)\le a.
$$

For the last inequality use $0\to\mathcal O_C\to\nu_*\mathcal O_{\widetilde C}\to T\to0$, where $T$ has finite nonnegative length. Taking Euler characteristics gives $a=g(\widetilde C)+\operatorname{length}T$. In particular $a\ge0$.

Arithmetic adjunction and algebraic surface Riemann–Roch give, with signs written out,

$$
K_X\cdot H=2a-2-e,
\qquad \chi(\mathcal O_X)=1-q\quad(p_g=0),
$$
$$
\begin{aligned}
\chi(\omega_X(2H))
&=\chi(\mathcal O_X)+\frac{(K_X+2H)\cdot2H}{2}\\
&=1-q+(2a-2-e)+2e\\
&=e+2a-1-q\ge e+a-1\ge1.
\end{aligned}
$$

These are algebraic formulas in all characteristics, including characteristic two; division by two concerns integer intersection numbers, not inversion of two in $k$. Kleiman Proposition B.26 supplies the characteristic-free RR input. Arithmetic adjunction can alternatively be derived from RR applied to $0\to\mathcal O_X(-C)\to\mathcal O_X\to\mathcal O_C\to0$, so it adds no characteristic assumption.

By Serre duality $h^2(\omega_X(2H))=h^0(\mathcal O_X(-2H))=0$: an effective nonzero divisor equivalent to $-2H$ would intersect nef $H$ in $-2e<0$, while an everywhere nonvanishing section would make $-2H$ trivial and force $e=0$. Consequently $h^0=\chi+h^1\ge1$. Lemma A passes without Kodaira vanishing, surface classification, analytic Hodge theory, or separability.

## 2. Resolution, general section, and Lemma B

Let $S\subset\mathbf P^3_k$ be integral of degree $e\ge2$, $\nu:Y\to S$ its finite normalization, and $q:X\to Y$ a projective resolution chosen to be an isomorphism over $Y_{\rm reg}$. Finite-type schemes over a field are excellent; Lipman's surface resolution as stated in Stacks 54.14.5 applies in all characteristics. Normalized blowups can be centered at singular closed points. Their normalizations are finite, so the resulting resolution is projective and preserves the regular locus. Normal surfaces are Cohen–Macaulay by $S_2$, and their singular locus has codimension at least two, hence consists of finitely many points. A regular surface over the perfect field $k$ is smooth.

Set $f=\nu q$, $H=f^*\mathcal O_S(1)$. This is globally generated and nef. The intersection projection formula gives

$$
H^2=[k(X):k(S)]\,\mathcal O_S(1)^2=e,
$$

since $f$ is birational. Kleiman Appendix B.15–B.16 supplies the intersection formula without a characteristic restriction.

A general plane section $E\subset S$ is geometrically irreducible by Stacks Lemma 37.32.3. Its hypotheses hold for the complete hyperplane system of the embedded integral surface: it is basepoint free, and two suitable hyperplanes meet it in codimension two, with a third avoiding a chosen point of that intersection to satisfy the stated codimension-two test. Applying Stacks Lemma 33.47.3 to the smooth open $S_{\rm reg}$, where the system defines an immersion, makes $E$ generically smooth and reduced. A hypersurface curve is Cohen–Macaulay and has no embedded components; hence $E$ is integral. This use of smooth Bertini is on the embedded smooth open of $S$, not on the pullback system on $X$.

Choose the plane also to avoid the finitely many points in $S$ that are images of the $q$-exceptional curves. Normalization is finite and contracts no curves; thus every $f$-contracted curve lies above one of these points. The divisor $C=f^*E\in|H|$ has no such component. Every component maps onto $E$, whose generic point lies in $S_{\rm reg}$. Over that point $f$ is an isomorphism, so exactly one component occurs and its multiplicity is one. As a Cartier divisor on smooth $X$, $C$ is Cohen–Macaulay with no embedded components. It is therefore integral. Meeting the conductor does not disturb this argument, and no separability or smoothness at the conductor is asserted. Lemma A applies to $X,H,C$.

## 3. Canonical forms, finite duality, and the conductor

The canonical module $\omega_Y$ on normal $Y$ is rank one, torsion free, and $S_2$, hence reflexive. Because $Y\setminus Y_{\rm reg}$ has codimension two, Stacks Lemmas 31.13.12–31.13.13 give

$$
\omega_Y=j_*\omega_{Y_{\rm reg}}.
$$

Restrict a local section of $q_*\omega_X$ to the inverse image of $Y_{\rm reg}$, where $q$ is an isomorphism. It defines a section of this extension. Restriction is injective because a section of a line bundle on integral $X$ vanishing on a dense open is zero. Thus $q_*\omega_X\hookrightarrow\omega_Y$. Equality is not needed and is not asserted: no rational-singularity assumption is hidden here.

For completeness, finite canonical duality admits a direct check in the present Cohen–Macaulay setting. On an affine $S$-open with coordinate ring $A$, write $B$ for its finite normalization algebra. Let $T$ be the sheaf on $Y$ corresponding to $\operatorname{Hom}_A(B,\omega_S)$. Finite adjunction gives, naturally for every coherent $F$ on $Y$,

$$
\operatorname{Hom}_Y(F,T)
=\operatorname{Hom}_S(\nu_*F,\omega_S)
=H^2(S,\nu_*F)^*
=H^2(Y,F)^*
=\operatorname{Hom}_Y(F,\omega_Y).
$$

Finite pushforward is exact, and Serre duality on the proper equidimensional Cohen–Macaulay surfaces $S,Y$ gives the second and last identifications (Stacks Lemma 48.27.5). Yoneda identifies $T=\omega_Y$; it does not require $\nu$ flat. Equivalently,

$$
\nu_*\omega_Y=\operatorname{Hom}_S(\nu_*\mathcal O_Y,\omega_S).
$$

Kollár, with an appendix by Hailong Dao, Definition 46 and equation (48.1), corroborates this formula. Its additional finite-map hypothesis (18.2) preserves codimensions zero and one; it holds for the finite birational normalization of these integral finite-type surfaces. The direct Cohen–Macaulay derivation above independently avoids importing a more general TfS2 assertion without checking its hypotheses.

Since $S$ is a degree-$e$ hypersurface, $\omega_S=\mathcal O_S(e-4)$. In the common fraction field, every $A$-linear map $B\to A$ is multiplication by $t=\phi(1)\in A$, with $tB\subset A$. Therefore

$$
\operatorname{Hom}_A(B,A)=\mathfrak c:=\{t\in A:tB\subset A\},
$$

the conductor. Projection formula then gives

$$
f_*\omega_X(2H)\hookrightarrow\nu_*\omega_Y\otimes\mathcal O_S(2)
=\mathfrak c(e-2)\hookrightarrow\mathcal O_S(e-2).
$$

Lemma A supplies a nonzero global section of the left side, and both inclusions preserve its nonzero value. At the generic point of a singular curve of $S$, the local ring is a nonregular one-dimensional domain. If it were normal it would be a DVR and regular. Hence it is nonnormal. A unit $t\in\mathfrak c$ would force $B=A$ after localization, so every conductor element lies in the generic-point maximal ideal. Its image vanishes on the entire reduced integral singular curve. This proves the exact vanishing required by Lemma B; it does not claim a prescribed scheme-theoretic order on the singular locus.

Finally the hypersurface sequence, twisted by $e-2$, is

$$
0\to\mathcal O_{\mathbf P^3}(-2)\to\mathcal O_{\mathbf P^3}(e-2)\to\mathcal O_S(e-2)\to0.
$$

The standard projective-space line-bundle cohomology gives $H^1(\mathbf P^3,\mathcal O(-2))=0$ over any field; this also follows from the usual monomial Čech computation, in which only cohomological degrees zero and three can survive. Thus the nonzero section lifts to a nonzero degree-$e-2$ homogeneous polynomial vanishing along every reduced singular curve. Since $H^0(\mathcal O(-2))=0$, the lift is unique. Lemma B passes.

## 4. Explicit boundaries and a conductor check

- $X=\mathbf P^2$, $H=\mathcal O(1)$: $H^2=1$, $\omega_X(2H)=\mathcal O(-1)$, and $h^0=0$. The lower bound $e\ge2$ cannot be dropped.
- $X=\mathbf P^1\times\mathbf P^1$, $H=(1,1)$: $H^2=2$, a general member is integral rational, and $\omega_X(2H)=\mathcal O$, so $h^0=1$. The bound is attained.
- On the same surface $H=(1,0)$ has square zero and integral fiber members, but $\omega_X(2H)=(0,-2)$ has no sections. Positive square matters.
- The integral cubic cone $y^2z-x^3=0\subset\mathbf P^3$ has singular line $x=y=0$, including characteristics two and three. On the affine chart $z=1$, put $K=k(w)$ at the generic point of the line. Its cusp ring is the localization of $K[t^2,t^3]\subset K[t]$ at $(t^2,t^3)$, with $x=t^2$ and $y=t^3$. The conductor consists of powers of $t$ of exponent at least two, namely $(t^2,t^3)$. The degree-$1=e-2$ forms $x,y$ vanish along the singular line. In characteristic two the $y$-derivative vanishes; in characteristic three the $x$-derivative vanishes; the singular-line and conductor conclusions still hold. This is a hand derivation illustrating the duality boundary, not a finite computation substituting for the proof.

No counterexample or unsupported equivalent central claim remains in the assigned surface mechanism. This report makes no conclusion about priority, preprint readiness, publication, the author's 3,888 supplemental controls, or the remainder of the line-configuration proof.
