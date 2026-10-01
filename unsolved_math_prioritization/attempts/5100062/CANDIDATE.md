# k903,a: odd-period focal-inverse area product

**5100062 / AMR-050-0062. Substantive author turn 1. Complete candidate pending separate adversarial review.**

## 1. Exact target and source

Let

    E: x²/a² + y²/b² = 1,        a>b>0,
    C: x²/alpha² + y²/beta² = 1,
    alpha²=a²−lambda, beta²=b²−lambda, 0<lambda<b².

Fix a Poncelet family between these ellipses of odd primitive period N≥3. Put c=sqrt(a²−b²)>0 and f_+=(c,0), f_−=(−c,0). Invert each original orbit vertex P_i about the unit circle centered at f_+ or f_−, preserving traversal order, and join successive inverted vertices by straight segments. Denote their signed shoelace areas by F_+ and F_−.

The claim is that F_+F_− is constant as the original orbit varies. This is k903,a in [Reznik–Garcia–Koiller, arXiv:2004.12497v11](https://arxiv.org/pdf/2004.12497v11), Table 10, p. 12; the inversion is defined in Section 3.9, pp. 9–10. The shorter published *Fifty New Invariants* companion does not contain a k903 row. Its differently numbered inverse-object table must not be substituted for this target.

The exact general odd-period assertion also appears as Conjecture 1 following the N=3 result in [Reznik–Garcia–Helman, The Talented Mr. Inversive Triangle in the Elliptic Billiard](https://arxiv.org/pdf/2012.03020), p. 6. That paper's Proposition 7 covers N=3, not all odd periods. The published [bicentric paper](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0188.pdf), Table 1, p. 629, labels the general odd focal-area product as an experimental phenomenon. These historical statements do not certify its current novelty.

The proof below uses the standard genus-one Poncelet flag framework, as described in [Chavez-Caliz, More About Areas and Centers of Poncelet Polygons](https://armj.math.stonybrook.edu/pdf-Springer-final/020-0154.pdf), p. 98. It does not use the AA' theorem, a conjectural area identity, or a private communication. No novelty or priority claim is made.

## 2. The flag curve and reversal

Let X consist of flags (P,l), where P lies on E and l is a tangent to C through P. The projection pi:X→E has degree two and branches at E∩C. The two conics are transverse over the complex numbers: with c²=a²−b², their four intersections satisfy

    x²=a²alpha²/c²,    y²=−b²beta²/c².

Their coordinates are nonzero, and the determinant

    1/(a²beta²)−1/(b²alpha²)
       = lambda c²/(a²b²alpha²beta²)

is nonzero. It also excludes shared points at infinity. Thus X is a smooth connected compact genus-one curve.

Define sigma(P,l)=(P',l), exchanging the intersections of l with E, and tau(P,l)=(P,l'), exchanging the two tangents to C through P. The Poncelet map is T=tau sigma. It is a translation of exact order N. No nonidentity power of T has a fixed point.

For a flag u, set P_i(u)=pi(T^i u), with indices modulo N. The areas F_± obtained after a fixed focal inversion are meromorphic functions on X and are invariant under T, since T cyclically relabels vertices.

The identity tau T^i=T^(−i) tau shows that tau reverses the vertex order while leaving the fixed inversion center unchanged. Hence

    F_±(tau u)=−F_±(u).

Since sigma=T^(−1)tau and F_± are T-invariant, also

    F_±(sigma u)=−F_±(u).                                (1)

All products and areas in this complexification are algebraic, using the bilinear dot product and the usual determinant; no complex conjugation of the parameter is introduced.

## 3. The four special contacts and their disjoint orbits

Write B=diag(1/a²,1/b²), R=BP and d=R·R. The four points on E with d=0 are

    P=(epsilon a²/c, eta i b²/c),    epsilon,eta∈{+1,−1}.  (2)

The tangent R·z=1 to E at such a point is also tangent to C, since

    alpha² R_x²+beta² R_y²
       = a² R_x²+b² R_y²−lambda d = 1.

Conversely, subtracting the normalized dual equations of a common tangent to E and C gives d=0. Thus (2) are precisely the E-contact points of the four common tangents. Each gives a sigma-fixed flag s=(P,tangent_E(P)).

These contacts are not on C: their C-equation residual is

    x²/alpha²+y²/beta²−1 = −lambda²/(alpha²beta²) ≠ 0.

Therefore pi is unramified over them. Each contact has two flags, s and tau s=Ts, which belong to the same T-orbit.

Crucially, distinct sigma-fixed flags lie in distinct T-orbits when N is odd. If s and T^j s are both fixed by sigma, then sigma T^j=T^(−j)sigma gives T^j s=T^(−j)s, hence N divides 2j. Oddness of N forces j=0 modulo N. Thus the four sigma-fixed flags define four disjoint T-orbits.

Separate these into S_+ (the two orbits with epsilon=+1 in (2)) and S_− (the two with epsilon=−1). A single orbit contains no contact from the other set, nor the other contact from its own set. Within the orbit of s, the only vertices attaining any contact (2) have indices 0 and 1 after cyclic relabeling, and both tend to the same contact P.

## 4. Complete pole analysis of focal inversion

Use complex affine coordinates Z=x+iy and W=x−iy on E. For a real focus coordinate f=±c, unit inversion has complex coordinates

    U_f = f + 1/(W−f),    V_f = f + 1/(Z−f).              (3)

For real points, V_f is the complex conjugate of U_f. Formula (3), interpreted rationally, is the meromorphic complexification of the specified Euclidean inversion.

At either infinite point [a:±ib:0] of E, both Z and W have simple poles with nonzero leading coefficients a∓b and a±b. Both expressions in (3) are therefore bounded and extend holomorphically, with value f. There are no inversion poles at infinity.

For f=c, the line Z=c is tangent to E at (a²/c, i b²/c); the line W=c is tangent at (a²/c,−i b²/c). Each has contact order two. At either contact, the other denominator in (3) is nonzero, with value 2b²/c. Thus exactly one of U_c,V_c can have a double pole; the other is holomorphic. These are the only finite poles. For f=−c the corresponding contacts are the two points with x=−a²/c, and the same assertion holds (the other denominator is −2b²/c).

Because pi is unramified at the contacts, these are at most order-two poles on X as well. By Section 3, F_+ can have poles only in S_+, and F_− only in S_−.

We must check the order of an area, rather than merely its vertices. In complex coordinates its shoelace expression is

    F_f = (1/(4i)) sum_j (V_f(P_j) U_f(P_(j+1))
                             − U_f(P_j) V_f(P_(j+1))).    (4)

Near a sigma-fixed flag s in S_+, only the vertices indexed 0 and 1 can be singular for f=c. They both tend to the same contact. Thus the same one of their two complex coordinate functions has at most a double pole, and the other coordinate functions are holomorphic. In their mutual determinant term, a product of two singular coordinate functions never appears. All other determinant terms have at most one singular factor. Therefore F_+ has at most a double pole at s, not an apparent fourth-order pole. The same analysis applies to F_− at S_− and to all translates by T.

There are no other poles omitted in this argument: rational inversion has been checked at every finite denominator zero and at both points at infinity; the odd-order orbit argument lists every singular vertex near each such flag.

## 5. Reversal lowers the pole order and supplies the opposite zero

The involution sigma is nonidentity and fixes s. On a smooth complex curve, a nonidentity holomorphic involution at a fixed point has a local coordinate t for which sigma(t)=−t. In such a coordinate, (1) says that the Laurent expansion of F_+ is odd. Since its pole order is at most two, its even coefficient t^(−2) vanishes. Consequently F_+ has at most a simple pole at s.

The function F_− is holomorphic at s∈S_+, because no vertex in this T-orbit is a contact belonging to S_−. This includes any infinite original vertices, where (3) is holomorphic. Applying (1) at the fixed point s gives F_−(s)=−F_−(s), hence F_−(s)=0. Its vanishing order is at least one, unless it vanishes identically, which is harmless.

Thus F_+F_− has a removable singularity at s. The identical argument with the foci interchanged handles S_−. T-invariance transfers the conclusion to every translate of every possible pole.

The product F_+F_− is therefore holomorphic everywhere on the compact connected curve X. It is constant. Restriction to the real Poncelet family proves the stated odd-period invariant.

## 6. Scope, signs, and attribution

The argument treats any odd primitive period and any allowed star traversal. It uses signed areas, not the areas of unsigned unions of lobes. Reversing traversal changes each factor's sign and preserves their product. Real focal inversions are always defined because both foci lie strictly inside E and no orbit vertex equals a focus.

No division by either area is used, so zero signed areas would not cause a gap. Unit inversion is fixed throughout. A common inversion radius rho would multiply each area by rho^4 and the product by rho^8, but that scaling observation is not a replacement for the specified unit normalization.

Oddness is used in separating the four common-tangent orbits. For even N, opposite contacts can belong to the same orbit, and the zero-versus-pole argument does not apply. No even-period product assertion is made. Hyperbolic/degenerate caustics and circular outer boundaries are outside the source-corrected a>b>0 strict-ellipse scope.

The N=3 case is already published. This proof attempt addresses all odd N using the established flag framework plus the local focal-inversion analysis. The same general framework was used in the author's separate k303,a attempt, but no conclusion from that target is assumed here. Historical novelty has not been established.

## 7. Exact controls

For a²=8,b²=5,lambda=40/9, the caustic has alpha²=32/9,beta²=5/9. Two genuine three-period orbits are

    H: (2sqrt(2),0), (−4sqrt(2)/3,5/3), (−4sqrt(2)/3,−5/3);
    V: (0,sqrt(5)), (−8/3,−sqrt(5)/3), (8/3,−sqrt(5)/3).

Direct unit inversions about ±sqrt(3) give

    F_+(H) = (7−2sqrt(6))/(16(−sqrt(3)+2sqrt(2))),
    F_−(H) = (7+2sqrt(6))/(16(sqrt(3)+2sqrt(2))),
    F_+(V) = F_−(V) = sqrt(5)/16.

Both products equal 5/256, consistent with the known three-period formula. The author-written checker verifies incidence, caustic tangency, the reflection law, and direct signed areas. An even-period negative control distinguishes the unsupported extension. These finite tests are implementation controls only; the general proof is Sections 2–5.

Independent review should especially check: the exact inversion convention; the double contacts of Z=±c and W=±c; unramified pullback; odd-period separation of sigma-fixed orbits; the two singular vertex indices; the absence of order-four or order-three area poles; the local odd Laurent character; zeros of the opposite focal area; and completeness of the pole list. A full correctness claim awaits that review.
