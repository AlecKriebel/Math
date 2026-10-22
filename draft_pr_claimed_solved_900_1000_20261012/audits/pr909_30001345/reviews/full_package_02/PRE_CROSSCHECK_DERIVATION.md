# Independent derivation before crosschecking earlier reviews

Recorded 2026-10-15T04:52:52.324532+00:00 (original file creation/modification time), after reading final `note.tex` and visually inspecting all four independently rendered final PDF pages, and before reading earlier review verdicts.

## Claim and falsifiable success criteria

The exact claim is a negative example for *the unrestricted sum of local rough* K(K+D) in a fixed ball. It is not a claim about a marked section, a unibranch central curve, fine M, new configurations/methods, priority, or current openness. Success requires a reduced flat complex analytic family for every complex |t|<1/4; finite simultaneous normalization including t=0; a common transverse boundary retaining every singularity; and central/local summed delta 36, rough 7 versus 12. The input geometry and deformation mechanism can be classical while this explicit corollary is valid.

## Incidence and equation

For q^3=1, the three classes are X=qY, Y=qZ, Z=qX. Same-class lines intersect in three coordinate vertices, with three distinct directions each. A cross-class intersection has nonzero coordinates [q_i q_j:q_j:1]; exactly the third line with q_k=(q_i q_j)^(-1) also contains it. The nine cross points are distinct and each has exactly three incident lines. Twelve triples account for 12*3=36 unordered line pairs, equal to C(9,2), excluding every other intersection.

L=X+2Y+4Z misses vertices and cross points: its value at the latter has modulus at least 4-2-1=1. Thus all projective intersection points are finite in this chart; in particular no two affine lines have the same direction. Substituting Z=(1-u-2v)/4 and (u,v)=(x/t,y/t), clearing denominators gives the displayed ninth-degree F. Its factors are x-qy; qx+(4+2q)y-qt; -(1+4q)x-2y+t. The product of the latter two cubic products matches the formula because q ranges over all roots, and the x^9 coefficient is 1*1*(-65)=-65. At t=0 the distinct affine directions give exactly nine distinct homogeneous linear factors.

## Flatness, normalization, and analytic restrictions

Dividing F by -65 makes it monic in x, so C[x,y,t]/(F) is free rank 9 over C[y,t] and hence C[t]-flat. This alone does not prove analytic flatness. Locally s=t-t0 is a non-zero-divisor in the analytic quotient: sg=Fh implies F_t0*h_t0=0 in the domain of convergent germs; F_t0 is nonzero as a germ, so h=sh1 and g=Fh1. Over the one-dimensional regular base ring torsion-free implies flat. The reasoning holds both at singular and smooth points and every t0.

The total hypersurface is reducible and nonnormal. Each factor defines a smooth graph plane over (y,t), since its x coefficient is nonzero (q,1,or -(1+4q)). In the polynomial or convergent local UFD, distinct prime factors have intersection equal to product. Thus the map into the product of component rings is injective, finite (a finite product of cyclic quotients), birational in the reduced total quotient ring, and has a normal target. A finite integral birational normal extension is the integral closure: any further element integral over the base is integral over the target and therefore lies in it. On every fiber the factors are still distinct smooth lines, including t=0; their disjoint union is its normalization. This special-fiber check is essential and does not follow just from total normalization. Restriction to an open ball is a base change of the finite map. The normalization projection is smooth, although the open-ball projection is not proper.

## Ball and all complex parameters

Vertices in chart have norms at most 1. Cross points have two numerator moduli 1 and denominator modulus at least 1, so every singularity of the t fiber has norm <=sqrt(2)|t|<sqrt(2)/4<1/2. For ax+by+ct=0 the distance to 0 is |ct|/sqrt(|a|^2+|b|^2); the three group bounds are 0, |t|/sqrt(5), |t|/sqrt(13), since |4+2q|>=2 and |1+4q|>=3. The closest point is -ct*(conj(a),conj(b))/(|a|^2+|b|^2), orthogonal in the Hermitian metric to v=(-b,a)/sqrt(|a|^2+|b|^2). Therefore the stated radius sqrt(1-d^2) parameterization is a transverse circle, smooth as a real function of the complex parameter, and bounds a disk. Boundary circles cannot intersect because all line-pair intersections are in the half ball. This supplies a link isotopy along any smooth parameter path, without invoking a proper open projection. Homogeneity in (x,y,t) preserves the construction in all scaled ball radii.

## Local invariants and limiting cases

An ordinary r-point has r smooth branches with pairwise intersection multiplicity 1; delta=C(r,2). For r>=3 one embedded blowup produces E^2=-1 and E.C'=r. Adjunction gives K.E=-1, hence K=E with this exceptional support convention. D=C'+E and K(K+D)=E(C'+2E)=r-2. The sign would be wrong for K=-E, which adjunction excludes. For a node the minimal embedded resolution is the identity and rough is 0, agreeing with r-2. Consequently 9 branches give delta36/rough7, and twelve triples delta12*3=36/rough12. The normalization has nine components, not a single rational component; branch count is not genus. K+D is relatively nef here since its pairing with E is r-2>=0.

## Universal extension separately from computation

For any n>=3 use all nth roots of unity. The same intersection classification gives three n-points and n^2 triples. Pair counting 3*C(n,2)+3n^2=C(3n,2) is an identity, independent of finite checks. The same L misses intersections by the same strict lower bound; all directions remain distinct and each affine factor remains a graph. Distances have the same group bounds, independently of n. Scaling produces the same finite simultaneous normalization and common ball argument. Rough on nonzero fibers is 3(n-2)+n^2; at zero it is 3n-2, so excess n^2-4 is positive for every n>=3 and unbounded. At n=2 vertices are nodes, excess0. At n=1 vertices are smooth and r-2 is not their rough formula; the extension does not assert that case. Tangent moduli of ordinary points do not affect this single-blowup calculation; equisingularity need not mean an analytic isomorphism of all r-tuples.

## Remaining independent checks

The algebra/analysis above verifies the explicit mathematical statement conditional only on the stated invariant convention. Source pages must still verify the scope of the original question and attribution. Bytes, executable replay, publication metadata, count uncertainty, live PR state, and proposed administration still require separate checks. Computation cannot establish the analytic universal argument, priority, or a human referee verdict.
