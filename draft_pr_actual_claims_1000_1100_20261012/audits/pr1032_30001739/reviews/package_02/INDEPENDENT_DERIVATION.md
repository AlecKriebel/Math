# Independent derivation for whole-package review 02

This derivation was developed from the candidate statement and the local published FLO, JPSS and LM interfaces before reading the previous package review's report, derivation or handoff. The accompanying `independent_combinatorics.py` imports no candidate or previous checker. It uses integer comparisons, exhaustive finite sets and exact rational polynomial arithmetic. Its ordinary, `-O` and `-OO` outputs agree byte for byte. Computation checks the finite steps below, not the representation-theoretic dependencies or a Hom space.

## Exact target and classification

Work over smooth admissible complex representations, with F=Q3 and E its unramified quadratic extension. Put A=[0,2], B=[1,4], C=[3,3], D=[2,5], T=[4,6]. The segment representation is the essentially square-integrable **quotient** of ascending characters. Its lengths are 3,4,1,4,3; the sum is 15. In order T,D,C,B,A the centers 5,7/2,3,5/2,1 strictly decrease. This is Langlands data; its unique irreducible quotient is the target. The unramified absolute-value characters, and hence these segment representations, are fixed by tau. Uniqueness of the quotient makes the quotient tau invariant.

Being a quotient of a proper induced module is different from being equal to the entire induced module. None of the period-basis or scalar calculations permits replacing the quotient by its standard module.

## Fixed-x complete coordinates

Fix any nonsingular Hermitian matrix x. FLO Corollary 13.6, printed p.291, applies separately to every fixed x and to essentially square-integrable tau-invariant factors satisfying its ordered-pair exclusion. Its period basis has 2^(5-1)=16 elements; this is not a dimension statement obtained only after summing the two Hermitian orbits. FLO (12.1) and (3.13) explain the independence and simultaneous quadratic-twist identification. Fix the T-label equal to zero.

The relation used by that corollary is a<=c<=b<=d for [a,b] followed by [c,d]. It is distinct from linked-segment precedence. In each of TDCBA, TCDBA, TDBCA, all ten earlier/later pairs fail this relation. The independent computation tests these thirty inequalities. Thus the full Hom space on each of these three inductions has the required holomorphic sixteen-element basis at the specialization.

## Scalar orientation and exact zero orders

FLO (4.5) normalizes the open period by a product indexed by ordered pairs. In the period-permutation identity (12.5), use the reverse operator whose domain is the swapped order and whose target is the original order. All factors except the swapped pair cancel. Up to invertible epsilon/constant terms the coefficient is

    gamma(-u, delta_i'^vee x delta_j' x chi) /
    gamma( u, delta_i' x delta_j'^vee x chi),

where chi=eta^(1+epsilon_i+epsilon_j). This is also the explicit orientation of FLO (13.3), printed p.293. Equal labels give chi=eta; opposite labels give chi=1. The inverse orientation would invert the coefficient and introduce poles in place of the relevant zeros.

For lengths n,m and centers c_i,c_j, the JPSS Steinberg-pair exponents are

    h_k = c_i-c_j+(n+m-2)/2-k,  0<=k<min(n,m).

They equal b_i-a_j-k. Swapping the factors gives the dual exponents. Substitute these two lists in gamma(s)=epsilon(s)L(1-s,dual)/L(s). With z=q^(-u), the numerator polynomial is the product of (z-q^(-h)) and (z-q^(-1-h)) over the dual list, with z^(-2r); the denominator has factors (1-q^(-h)z) and (1-q^(-1-h)z) over the forward list. For eta insert a minus sign into each q-power. The code multiplies these polynomials over Q and repeatedly divides by z-1, rather than inferring symbolic orders from floating evaluations.

The resulting opposite-label orders are TD=2, BA=2, TC=1, DB=2, CA=1. All equal-label coefficients are units. Both nested pairs DC and CB have forward exponents [2] and dual exponents [1], hence order zero. Their exact epsilon-free values are 9/13 and 9/7 at q=3 and 81/91 and 81/73 at q=9 for signs +1 and -1. These are not claims to determine every constant of an actual normalized operator. The q=9 positive-sign directional factors give units for the E-side gamma normalizers. Both forward center differences are 1/2>0. FLO Lemma 1.1(3) supplies holomorphy of forward M and reverse N; multiplying by the unit normalizer supplies forward N holomorphy. Meromorphic inverse identities then specialize to genuine inverse maps.

These two swaps have holomorphic complete period bases on both sides. Their scalar coefficients are units for every segment label. Their pullbacks are therefore diagonal up to segment permutation and nonzero scalars, not merely isomorphisms of representations with unspecified action on periods. The two swaps share C and do not commute; the proof uses separate maps from the original chamber, and never assumes that they commute.

## Proper reverse images, open restrictions, and the odd cycle

For each linked adjacency in standard pair-order, the real center difference is positive. FLO Lemma 1.1(4) identifies the holomorphic reverse-N image with the proper forward-M kernel of a length-two rank-one induction. Smooth parabolic induction over C is exact and preserves nonzero objects. In the compact model, compact invariants are exact by averaging, the relevant double-coset set for fixed compact invariance is finite, and a small supported section from any nonzero inducing vector proves nonvanishing. Consequently the induced rank-one image remains a proper submodule in the full induction. Its unique maximal proper submodule contains this image. This is enough for any quotient functional to kill it; no equality of the full kernel with a sum of rank-one images is used.

Expand the quotient functional in the sixteen complete period coordinates of a chamber. Compose with the reverse operator. The resulting functional at the base point is zero. To specialize the meromorphic period equation, extend this finite linear combination with constant coefficients, restrict to sections on the **full union of open orbits**, and evaluate at zero. FLO (6.6), printed p.242, gives entire restricted periods and its isomorphism with the Levi-form space; (12.1) makes the sixteen restricted forms independent. It is unnecessary and generally wrong to require holomorphy/completeness of all full periods in the order after a linked swap. It is also unnecessary to claim that the quotient combination is zero away from the base point.

Independence gives a_epsilon*c_epsilon(0)=0 separately. Since equal-label coefficients are units, every surviving coordinate has opposite labels on that adjacency. The chambers give TD and BA, then TC and DB, then CA. Diagonal unit transport identifies their segment-labelled supports. The graph is the five-cycle T-D-B-A-C-T. Summing its five equations over F2 gives 0=1. Independently enumerated surviving coordinate counts after successive edges are 16,8,4,2,1,0. Every quotient period is zero. The fixed-x argument applies to both Hermitian isometry classes, including the quasi-split stabilizer.

## Every entire proper induction reduces to a segment partition

If an entire parabolic induction is irreducible, exactness and nonvanishing of induction force its data irreducible. Grouping multiple Levi blocks gives a two-factor entire irreducible product of positive degrees. Write these factors L(m),L(n). LM Proposition 2.5(5) and Theorem 2.6 imply that L(m+n) occurs in their product with multiplicity one. Irreducibility and injectivity of the parameterization force m+n=A+B+C+D+T **as multisets of segments**, not only as cuspidal supports. Thus every possible realization belongs to one of the 5+10=15 unordered nonempty partitions of these distinct occurrences.

For each partition a side is a ladder. Singletons always are. The only non-ladder pairs are BC and CD; their respective complements ADT and ABT are ladders. A ladder is strict monotonicity of starts and ends, not a condition of consecutive linkage.

LM precedence is a<c<=b+1 and b<d. In the directed LC graph, X consists of u preceding v; Y consists of the **first** segment shifted left by one preceding v. The edge from (u,v) in X to (u',v') in Y is permitted exactly when (u=u' and v' precedes v), or (v=v' and u precedes u'). The code regenerates every X,Y and the entire adjacency relation in both directions. It separately enumerates every injective matching and every nonempty Hall subset. Their success/failure verdicts agree in all thirty directed candidate graphs. Every partition has a failing direction, and in each such case at least one singleton Hall witness exists. The manuscript's fifteen explicit rows also agree with these definitions and the displayed full Y lists.

LM Proposition 5.20 applies when one side is a ladder; it requires **both** directed LC conditions. The Zelevinsky ring involution sends Z(m) to L(m), permutes irreducible classes positively and multiplicatively, and is its own inverse. Hence product length one is equivalent for Z(m)xZ(n) and L(m)xL(n) at these same parameters. It does not require computing or replacing m,n by dualized parameters. Since a necessary direction fails in every partition, no entire proper induced realization exists.

The finite graph calibration also enumerates 1,260 distinct four-occurrence endpoint configurations on [0,3], including positive matchings. Each of six incorrect shifts/arrows changes a verdict on a saved configuration. This is a bounded calibration, not a proof of a matching algorithm over an infinite universe. Bare failure on the fifteen candidate partitions would not validate those definitions.

## Scope of consequences

OWR Conjecture 4 uses total multiplicity over Hermitian orbits and its noninduced/imprimitive condition. With k=1 the entire-product irreducibility requirement is automatic and the target is imprimitive by the preceding argument, giving zero instead of two. FLO's tau-Witt condition has value zero for this individually tau-invariant cuspidal line, while all Hermitian Witt indices are nonnegative. This gives the stated historical conjecture counterinstances, including the unrestricted quasi-split unitary converse. The quotient is nongeneric because the standard module is reducible, and non-tempered because its real central exponents are not zero. The paper does not transplant generic/tempered induced-space completeness to arbitrary quotient descent.

All deep source theorem arguments remain dependencies. The review checks the precise interfaces and this finite application; it does not reprove FLO, JPSS, LM, spectral multiplicity theorems, or source priority. Luo-Zha's unavailable body, its exact/transformed/twisted/dual parameters, kernel relationship and unitary consequences remain UNKNOWN, as the human explicitly accepted. No firstness, worldwide novelty or current worldwide openness follows from this derivation.
