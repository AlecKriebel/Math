# Independent analytic-family and source-convention audit of PR148

Audit target: original_submitted_attempt, supplied original HEAD 538fd2584f7dc7375e4eaa91d73daddde3d073cd and supplied manifest efd273eb031989bddae0ae89cad8d2e92cc6f531d2076d20d09155a8b508cb02. This is a mathematical audit only. No other reviewer or inherited checker was consulted.

## Precise hypothesis and source scope

The literal claim is constancy of (A'/A)/S, S=product sin(theta_i/2), on a fixed directed confocal-ellipse billiard family with N=2 modulo 4. A is the orbit's signed polygon area and A' the signed area of the polygon of consecutive tangents to the outer ellipse. The proposed falsification has N=6, outer ellipse x^2/4+y^2=1 and caustic x^2/(32/9)+y^2/(5/9)=1.

Both primary PDFs have the exact hashes in the submitted manifest:

- preprint_v11.pdf: c56bb4ea29734ed04ee153206bb8619286df544714fd3f77fe97bdc945dfe1da;
- published_2021.pdf: c2a2e644521fd03a15833a23bd57c2498b5644036f6bc8fe682c40581f640d42.

Fresh page renders preprint-03/04/05.png and published-03/04/05.png were generated directly from these PDFs and inspected. Table 2, preprint p.5 and publication p.345, visibly gives k103=A'/A, k105=product sin(theta_i/2), k108=k103/k105 for N=2 modulo 4, with '?' in the proof column. Preprint p.3 and publication p.343 explicitly define signed cross-product areas. The Section 3.1 definitions on preprint p.4 and publication p.344 separate the outer polygon A' from the caustic-contact inner polygon A''. No relevant restriction excludes convex N=6 trajectories or axial starting points.

Source wording nuance: Section 3.1 calls theta_i the polygon's 'angles', without the adjective 'internal'. The ordinary internal-angle reading is independently forced by the displayed normalization sum cos(theta_i)=JL-N and supported by the source bibliography's relation phi=pi-theta_i for the pedal turning angles. For the convex examples below the ordinary polygon angle is unambiguous. The submitted phrase 'internal angles' is a correct interpretation, not a verbatim Section 3.1 definition.

## A return-map derivation independent of the submitted checker

Scale coordinates by x=2X, y=Y. The outer ellipse becomes the unit circle X^2+Y^2=1, while the inner ellipse becomes X^2/(8/9)+Y^2/(5/9)=1. Parametrize the outer circle by t=tan(phi/2), including t=infinity:

    (X,Y)=((1-t^2)/(1+t^2), 2t/(1+t^2)).

The chord joining parameters t,u has equation

    (1-tu)X+(t+u)Y=1+tu.

Tangency to the inner ellipse means

    8(1-tu)^2+5(t+u)^2=9(1+tu)^2,

equivalently

    F(t,u)=(5-t^2)u^2-24tu+5t^2-1=0.                (1)

As a quadratic in u its discriminant is

    20t^4+472t^2+20 > 0

for all finite real t. Thus there are two distinct real tangent chords, with the projective chart used when one endpoint is at infinity. Choose the directed chord with the caustic on its left. The caustic is strictly nested and encloses the origin, so the advance in the outer-circle angular coordinate lies strictly between 0 and pi. This branch is a continuous map T of the entire circle.

For consecutive vertices with parameters t,u, the incoming chord corresponds to one root of F(u,v). Reversing that chord would place the caustic on the right, so the true next vertex v is the other root. Vieta therefore gives, in a generic chart,

    v=(5u^2-1)/[(5-u^2)t].                            (2)

Write A=5-u^2 and B=5u^2-1. The next root after v is

    w=(5v^2-1)/[(5-v^2)u].

The following polynomial identity is the independent closure certificate:

    (5t-u)B^2+(5u-t)A^2 t^2 = (-At-uB) F(t,u).       (3)

Using (1)-(2), identity (3) gives

    t(5v^2-1)+u(5-v^2)=0,

and consequently

    w=-1/t.                                          (4)

Equation (4) means T^3 sends every outer vertex to its antipode. It first holds away from finitely many chart poles, then on the whole circle by continuity of the geometric tangent map. Applying it twice gives T^6=id.

There is no hidden reversal in (2): both tangent choices are distinct everywhere, and incoming reversal is the opposite directed branch. Nor is the map merely a period-three or repeated period-two correspondence. T has no fixed vertex because the caustic is strictly inside the outer ellipse. T^3 has no fixed vertex by antipodality. A period-two orbit would satisfy T(p)=-p by (4); its chord would then pass through the center of the inner ellipse, and could not be tangent. Since every least period divides six, every vertex on this directed family has least period six.

Each angular increment is in (0,pi). Three increments send a vertex to its antipode, so their sum is an odd multiple of pi in (0,3pi), necessarily pi. Six increments total 2pi. Thus all family members are simple strictly convex counterclockwise hexagons. The two proposed orbits belong to this single continuous one-parameter family, with turning number one, rather than to different winding components. This establishes closure, branch, family, convexity and least period without using a porism theorem.

## Why the tangent map is the physical billiard map

For a general ellipse x^2/a^2+y^2/b^2=1 and confocal inner ellipse with parameter lambda in (0,b^2), put n=(x/a^2,y/b^2) and C=diag(1/(a^2-lambda),1/(b^2-lambda)). For an arbitrary direction v and boundary point p, the discriminant of the line's intersection with the caustic satisfies

    (p.Cv)^2-(p.Cp-1)(v.Cv)
        = det(C)[a^2 b^2 (n.v)^2-lambda |v|^2].       (5)

For a checkable derivation, the two-dimensional Gram determinant gives the left side as v.Cv-det(C)(p cross v)^2. After dividing by det(C), this is

    (b^2-lambda)v_x^2+(a^2-lambda)v_y^2
        -(x v_y-y v_x)^2.

Using x^2/a^2+y^2/b^2=1, the coefficients b^2-y^2 and a^2-x^2 become b^2 x^2/a^2 and a^2 y^2/b^2. The expression is therefore (bx v_x/a+ay v_y/b)^2-lambda|v|^2, exactly the right side of (5) divided by det(C).

For a unit tangent direction, (5) gives |n.v|=sqrt(lambda)/(ab). At the present caustic this is J=1/3. Euclidean specular reflection in the ellipse tangent changes n.v to its negative and preserves |v|, so preserves caustic tangency by (5). Moreover J<1/a<=|n| because lambda<b^2, so the incoming ray is never exactly normal to the boundary and its reflection is distinct from incoming reversal. The reflected ray enters the outer ellipse and is precisely the other tangent selected in (2). Hence this algebraic Poncelet family is a family of ordinary billiard trajectories. This also derives the source's Joachimsthal normalization directly.

## Two members recovered from the map

At starting parameter t=0, (1) gives next parameter u=1/sqrt(5) on the chosen branch. Applying (2) and (4) gives

    H: 0, 1/sqrt(5), sqrt(5), infinity, -sqrt(5), -1/sqrt(5).

These yield exactly the submitted P_H under the outer-ellipse parametrization. At t=1, (1) gives the forward root 3+2sqrt(2), and the same return map gives

    V: 1, 3+2sqrt(2), -(3+2sqrt(2)), -1,
       -(3-2sqrt(2)), 3-2sqrt(2).

These yield exactly the submitted P_V. Thus the two data sets are reconstructed from one global directed map, not only tested separately for a shared caustic.

## Area evaluation without reconstructing outer intersections

For any convex outer-ellipse vertices of angular parameters phi_i and increments Delta_i in (0,pi), affine scaling from the unit circle gives

    A=(ab/2) sum sin(Delta_i),
    A'=ab sum tan(Delta_i/2).                         (6)

The second identity follows by decomposing the unit-circle tangent polygon into triangles of unit altitude; the two tangent lengths at a contact point are tan(Delta_(i-1)/2) and tan(Delta_i/2). It uses signed areas in the positive orientation and does not reconstruct the tangent intersections.

For H let cos(alpha)=2/3, sin(alpha)=sqrt(5)/3. Its increments are alpha four times and pi-2alpha twice. Equation (6) gives

    A_H=20sqrt(5)/9, A'_H=16sqrt(5)/5, A'_H/A_H=36/25.

For V let sin(eta)=1/3, cos(eta)=2sqrt(2)/3. Its increments are pi/2-eta four times and 2eta twice. Equation (6) gives

    A_V=32sqrt(2)/9, A'_V=5sqrt(2), A'_V/A_V=45/32.

All increments lie in (0,pi), so all tangent intersections are finite, all decomposed triangles positive and all four areas nonzero.

## Angle evaluation from the normal and caustic constant

Specular reflection and (5), rather than the submitted edge-vector dot products, give for the internal polygon angle theta

    cos^2(theta/2)=J^2/|n|^2,
    sin^2(theta/2)=1-J^2/|n|^2.                       (7)

Here |n|^2=x^2/16+y^2=1-3x^2/16 and J=1/3. For H, the two axial vertices have |n|^2=1/4 and the other four |n|^2=2/3. For V these two values are 1 and 1/3. Positive internal half-angle sines therefore give

    S_H=(5/9)(5/6)^2=125/324,
    S_V=(8/9)(2/3)^2=32/81.                         (8)

The k101 normalization also follows without invoking an invariant theorem. Reflection gives cos(theta_i)=2J^2/|n_i|^2-1, while

    incoming_unit-outgoing_unit=2J n_i/|n_i|^2.

Dotting with the vertex and summing cyclically gives L=2J sum 1/|n_i|^2; hence sum cos(theta_i)=JL-N. Thus the source's sign selects internal rather than exterior turning angles. The numerical cosine sum for both examples is -26/9, consistent with L=28/3 and J=1/3.

## Result and adversarial convention checks

Equations (6)-(8) independently give

    k108(H)=11664/3125,
    k108(V)=3645/1024,
    k108(H)-k108(V)=553311/3200000 > 0.

The literal printed assertion is therefore falsified at primitive convex N=6. No mathematical blocker was found.

Potential repairs tested or bounded:

- Signed versus unsigned area: the polygons are convex and positively oriented, so these agree here. Reversing the common orientation changes A and A' together and leaves their ratio unchanged. Cyclic indexing has no effect.
- Internal versus exterior turning half-angle: the source normalization selects the internal convention. Even substituting exterior turning angles yields products 1/81 for both members, and the two area ratios remain unequal. This substitution does not rescue this pair's quotient.
- Reflex or directed internal-angle lifts: theta -> 2pi-theta leaves sin(theta/2) unchanged for this positive convex case. Consistent orientation sign changes cannot remove the inequality.
- Outer versus caustic-contact polygon: the source names these separately as A' and A''. Substituting an inner, pedal or antipedal area would be a different claim.
- Repeated odd periods or different winding classes: the exact return map proves least period six and turning number one on the connected chosen branch. No period reduction or component switch is available.
- Axial starts or symmetry exceptions: all geometric quantities are finite and strictly positive; the whole family is smooth. Even an unprinted exclusion of axial starts would not salvage constancy, because the unequal values persist on disjoint sufficiently small neighborhoods by continuity.
- Degenerate caustic or billiard: lambda=4/9 lies strictly between 0 and b^2=1; both caustic semiaxes are positive, the inner ellipse is strictly nested, and a>b>0. Chord contacts are interior to the outer chords because of strict nesting.

Repairable source wording: distinguish the source's experimental unproved table assertion from an already-proved theorem; say the ordinary internal-angle interpretation is confirmed by k101 rather than implying the text explicitly writes 'internal' for theta_i. The submitted package already states that no repaired all-period theorem or official erratum is proved. The observed product (A'/A)S=5/9 in these two members is corroborative, not a general theorem.

PASS scope: mathematical falsification of the literal printed k108 expression for convex primitive six-period trajectories in one nondegenerate confocal billiard family. This does not decide novelty, historical priority, an official correction, all-period repaired formulas, repository attempt provenance or publication workflow. Original effort 1/5 is backed by one approach in turns.json; no timestamped native chat-turn transition ledger was supplied. That provenance limitation is outside this mathematical PASS.

The standard-library checker check_analytic_family.py independently expands identity (3), checks the homogeneous tangent relation and antipodality for both recovered projective parameter cycles, evaluates both areas from the angular support formulas, and checks both positive internal half-angle products from normal lengths. It also certifies exact positivity of the angular half-tangents, cosine sums, exterior half-angle products and exact nonzero quotient difference. exact_check_output.json records its successful run; no floating-point arithmetic is used.
