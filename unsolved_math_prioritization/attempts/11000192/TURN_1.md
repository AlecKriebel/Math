# Author turn 1: invariant-side witnesses and a precise construction gap

**Outcome: scoped partial; original problem unresolved.** This is an unreviewed author finding, not a verdict on the entire preprint. No public PR or resolution promotion is warranted.

## Source and exact target

Goldman's Problem2.5 in the book (printed211/PDF218) asks for an orientation-preserving pseudo-Anosov mapping class of a closed orientable surface acting nonergodically on its full SU(2) character variety, with Goldman symplectic measure. Genus2 is sufficient. The standalone chapter calls the same question2.8. Brown's relative punctured-torus examples, and Saadi's earlier representation-variety invariant, are not substitutes for this target. Saadi2505.08105v1 claims the exact genus2 result; the follow-up's Theorem3.1 requires checking separately from its invariant construction.

## 1. An exact nonconstancy family

Use the two-vertex, four-square groupoid of the source, with unit quaternions A1,...,A4,B1,...,B4 satisfying

 A1 B2 = B1 A1,
 A2 B1 = B2 A3,
 A3 B3 = B4 A2,
 A4 B4 = B3 A4.

Gauge the tree edge A4 to1. The source proposes the two projective imaginary directions

 v=A4(A2−A3),
 w=B1^(-1) A1(A2−A3) B1.

The rational angle function is

 F=<v,w>²/(|v|²|w|²),

where defined. It is unchanged by simultaneous SU(2) conjugation. Put

 A1=a+b i, A2=k, A3=−k, A4=1,
 B1=B2=i, B3=B4=j, a²+b²=1.

All four relations hold directly, and v=2k, w=−2a k+2b j, so F=a². The representations are irreducible because their image contains noncommuting i and j. Rational choices (a,b)=(3/5,4/5) and(5/13,12/13) give9/25 and25/169. In the source's rank argument, the relevant image planes are span(j,k) and span(i,k), so their intersection really is one-dimensional at these points. This establishes the desired nonconstancy without inferring joint variation from two separate surjectivity statements.

Goldman–Xia's full-measure irreducible locus is connected and smooth, with finite positive symplectic volume on nonempty open sets. If the rational invariance is established on a dense regular domain, two such smooth nonconstant witnesses yield positive-measure neighborhoods, and exclusion of the countable orbit of the rational denominator-zero set is the appropriate way to obtain an invariant full-measure domain. The witness calculation alone does not supply a pseudo-Anosov map or prove the complete source theorem.

## 2. Explicit action controls

The exact quaternion checker records the following pullback coordinate maps, with unchanged coordinates omitted:

 A: A1→A1 B2
 E: A4→B3 A4
 C: A2→A2 B1 B3, A3→A3 B3 B1
 B: B1→B1 A3^(-1) A1^(-1), B2→B2 A1^(-1) A3^(-1)
 D: B3→B3 A2^(-1) A4^(-1), B4→B4 A4^(-1) A2^(-1).

They preserve the square relations. The inverses reverse the right/left factors as recorded in the code. Products of automorphisms are composed right-to-left on group elements, so their pullback maps are evaluated left-to-right on representation tuples. This distinction is explicit in the tests.

For a second nonsingular rational family, take A1=a+b j, A2=(1+i+j+k)/2, A3=j A2 j^(-1), A4=1, B3=B4=j, B1=A1 A2 j, B2=A1^(-1)B1 A1. At(a,b)=(3/5,4/5), the angle is1/100. C,D and the source word

 R=E^(-2) (CD)^(-1) B(CD) E²

preserve that value whenever defined. The tempting opposite conjugation E^(-2)(CD)B(CD)^(-1)E² instead gives961/62500. Thus merely reversing the displayed conjugation is not an established repair of the invariant argument.

Some exact tuples map into the denominator-zero set, so pointwise everywhere-defined invariance must not be claimed. Rational invariance almost everywhere remains the correct scope to audit.

## 3. The displayed pseudo-Anosov route is not filling under the stated conventions

Let b,c,d,e be the standard chain curves for B,C,D,E in the source's Birman–Hilden presentation. Adjacent curves meet once; nonadjacent ones are disjoint. Let

 r=E^(-2)D^(-1)C^(-1)(b), so T_r=R.

All the following are exact mapping-class identities, not finite-search evidence.

First, the braid relation CDC=DCD gives (CD)C(CD)^(-1)=D. As C and E commute, and B and D commute, conjugation gives [R,C]=1. The two curve classes are distinct: in the abelianized based coordinates (a1,a2,b1,b3) after setting the tree edge A4 to1, c has class b1+b3 while r has class a1−b1+b3, up to simultaneous sign conventions. These are not equal up to sign. Therefore i(r,c)=0.

Second, for the adjacent pair D,E, the braid relation implies

 (DE²)²=(DE)³=(E²D)².

The common element is central in the two-generator braid group, and hence

 D E² D E^(-2) D^(-1)=E^(-2) D E².

Equivalently, D E²(d)=E^(-2)(d) as unoriented curve classes. Consequently

 i(r,d)=i(b, C D E²(d))
       =i(b, C E^(-2)(d))
       =i(b, C(d))
       =1.

The penultimate equality uses that E is disjoint from both b and c. The last uses i(b,d)=0 and i(b,c)=i(c,d)=1: a single twist about c creates exactly one intersection. Also i(c,d)=1. Thus c,d,r form a three-curve chain, rather than the filling six-intersection system described beside Figure4 in the preprint.

A regular neighborhood of a three-curve chain is a genus-one surface with two boundary circles. In a closed genus-two surface, at least one of these boundary classes is essential; otherwise capping the two disk boundaries would embed a closed genus-one component in the connected genus-two surface. The twists C,D,R preserve the resulting essential boundary multicurve. Therefore their entire subgroup is reducible, and contains no pseudo-Anosov element of the closed genus-two surface.

This invalidates **this displayed generating route** as a proof of the required pseudo-Anosov step. It does not prove that the larger projected lifted intersection Γ contains no pseudo-Anosov, that no corrected construction exists, or that Goldman's original question has a negative answer. It does not justify a broad statement that the preprint's theorem is false. The word/curve convention discrepancy itself remains subject to independent review before any PR.

## Remaining target and next route

Find a genuinely pseudo-Anosov element of the invariant stabilizer, perhaps from a larger part of the source's lifted intersection, or a corrected filling construction with a verified character invariant. All three requirements must hold together: pseudo-Anosov type on the closed surface, quotient-level nonconstant invariant, and full Goldman-measure nonergodicity. A nonconstant invariant for a reducible subgroup does not solve the original problem.
