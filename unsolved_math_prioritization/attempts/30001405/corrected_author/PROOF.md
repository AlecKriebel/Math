# A missing openness condition in the literal definable-quotient question

Problem 30001405 / OWR-4196-003, rank 975. Authored mathematical note, 7 October 2026. Unrefereed. No novelty or priority claim.

## 1. Result and limits

The literal assertion with (i) a locally contractible logic quotient and (ii) fibers that are countable decreasing intersections of definably contractible **sets**, without openness or continuity, is false. A two-class equivalence relation on a semialgebraic 2-sphere is a counterexample in degree 2.

This does **not** refute a formulation requiring open approximants or a continuous projection. In particular, it does not contradict the comparison theorem of Achille and Berarducci [AB18]. Their Theorem 12.2 assumes a triangulable quotient and contractible open approximants. The locally contractible, open-approximant variant is not settled by this note. A literature theorem in a stronger setting is not a proof that its extra hypotheses follow from the question.

## 2. Ambient structure and conventions

Fix a sufficiently saturated elementary extension M of the ordered real field R, in the pure ordered-field language, with saturation cardinal kappa greater than the cardinality of R. This is a special case of the saturated o-minimal expansion-of-a-field setting of the source.

All definability allows finitely many parameters. All subsets of M^r have the topology induced by the order topology. The interval for definable homotopies is [0,1]_M. A decreasing sequence means D_(j+1) is contained in D_j; equality is allowed. The saturation discussion below explains why this convention matters.

Write

    X = {(x,y,z) in M^3 : x^2 + y^2 + z^2 = 1},
    N = (0,0,1),   S = (0,0,-1),
    A = {N},      B = X \ {N}.

Define E on X by

    a E b  if and only if  (a = N iff b = N).

This is a definable equivalence relation with precisely the two nonempty classes A and B. In particular it is type-definable and has bounded index 2 < kappa. Let q:X -> Y = X/E be the quotient map, and use N and q(N) as basepoints.

## 3. The fibers are definably contractible

A is a singleton and is contractible by the constant homotopy.

For (u,v) in M^2 put r = u^2 + v^2 and define

    Q(u,v) = (2u/(1+r), 2v/(1+r), (r-1)/(1+r)).

The denominator is positive. Expanding the numerator gives

    (2u)^2 + (2v)^2 + (r-1)^2 = (r+1)^2.

Thus Q takes values in X, and its last coordinate cannot be 1 because r-1 != r+1. Hence Q maps M^2 into B.

Conversely, if (x,y,z) is in B, then 1-z is nonzero, and

    P(x,y,z) = (x/(1-z), y/(1-z))

is well-defined. The relation x^2+y^2 = 1-z^2 gives

    (x^2+y^2)/(1-z)^2 = (1+z)/(1-z).

Substituting proves Q(P(x,y,z)) = (x,y,z), while direct cancellation gives P(Q(u,v)) = (u,v). P and Q are continuous rational maps on their domains and are mutually inverse definable homeomorphisms.

A definable contraction of B to S is therefore

    H(b,t) = Q((1-t) P(b)),    b in B, 0 <= t <= 1.

It satisfies H(b,0)=b, H(b,1)=S, and H(S,t)=S. The displayed denominator calculation ensures the homotopy remains in B throughout.

For every natural number j set A_j=A and B_j=B. These are countable decreasing sequences of definably contractible definable sets, and their intersections are exactly A and B. Thus the fiber condition in the literal question holds.

## 4. The logic quotient is discrete and locally contractible

By the definition of the logic topology, C is closed in Y exactly when q^(-1)(C) is type-definable. There are four subsets of Y, and their inverse images are the definable sets empty, A, B and X. Every subset of Y is therefore closed, and also open. Thus Y is the discrete two-point space. The logic topology is not assumed to be the ordinary final topology of q, and they differ in this example. It is compact, Hausdorff, second countable, locally contractible, and even triangulable as a finite zero-dimensional simplicial complex.

For every n >= 1, a continuous based map from the ordinary real sphere S^n to Y is constant: S^n is connected and a continuous image of a connected space is connected, while a discrete space has only singleton connected subsets. Consequently

    pi_n(Y,q(N)) = 0,    n >= 1.

The counterexample is not caused by a failure of quotient triangulability.

## 5. Nontriviality of the definable second homotopy group

The based identity map of X represents a nonzero class in pi_2^def(X,N). Here is a proof that avoids using any conjectural quotient comparison.

Suppose this class were zero. There would be a definable continuous H:X x [0,1]_M -> X with H(a,0)=a and H(a,1)=N (and H(N,t)=N for a based nullhomotopy).

Fix an ordered-field formula phi(a,t,b;c) and a finite parameter tuple c defining the graph of this particular H. For this fixed formula, the following is one first-order ordered-field sentence: there exists c such that phi defines a single-valued total function on X x [0,1], its values lie in X, the endpoint identities hold, and the function is continuous. Continuity is expressible by the usual quantified epsilon-delta condition, with squared Euclidean distances and domain membership expressed by polynomial formulas. Thus no quantification over functions is involved: only one already chosen graph formula is used.

That sentence holds in M, so by completeness of the theory of real closed fields it holds in R. It produces a continuous homotopy from the identity of the ordinary real 2-sphere to its north-pole constant map.

For completeness, the topological obstruction is integral second homology. Triangulate the real 2-sphere by the boundary of a tetrahedron, oriented with vertices 0,1,2,3. Its simplicial chain group in degree 3 is zero. In degree 2, let the ordered faces be [012],[013],[023],[123]. The cycle

    z_2 = [123] - [023] + [013] - [012]

has zero boundary and is nonzero. More precisely, equating the coefficients of edges in the boundary of

    a[012] + b[013] + c[023] + d[123]

gives (a,b,c,d)=(-d,d,-d,d). Hence the cycle group in degree 2 is infinite cyclic generated by z_2, and, since there are no 3-simplices, H_2 is Z. The standard identification of simplicial and singular homology and homotopy invariance now give a contradiction: the identity induces the identity on this nonzero group, whereas a constant map factors through a point and induces zero. These are ordinary foundational homology facts [H02], not assumptions about definable quotients.

It follows that pi_2^def(X,N) is nonzero, which already suffices to disprove the proposed isomorphism with zero. In fact the established semialgebraic/o-minimal comparison, for example [AB18, Corollary 12.3] applied to this parameter-free closed bounded sphere, gives the sharper familiar computation

    pi_2^def(X,N) = Z.

This last computation is credited background, not a new theorem of this note and not needed for the counterexample.

## 6. Exactly which continuity condition fails

The singleton {q(N)} is open in Y but its inverse image {N} is not open in X. For instance the definable continuous curve

    c(s) = (2s/(1+s^2), 0, (1-s^2)/(1+s^2)),  s >= 0,

has c(0)=N and c(s) != N for every s>0. Thus q is not continuous.

Also B is not closed in X, because N lies in its closure by the same curve. Therefore this construction satisfies neither a requirement that all approximants be open nor a requirement that all approximants be closed. The literal statement imposes neither requirement.

**Conclusion.** The stated set-based fiber condition and local contractibility of the logic quotient do not imply the claimed higher-homotopy identification. The missing topological control is substantive. The corrected continuous/open-approximant problem remains separate.

## References

[AB18] Alessandro Achille and Alessandro Berarducci, *A Vietoris-Smale mapping theorem for the homotopy of hyperdefinable sets*, Selecta Mathematica 24 (2018), 3445-3473. DOI: https://doi.org/10.1007/s00029-018-0413-3 . Accepted postprint (final revision 10 April 2018): https://arpi.unipi.it/retrieve/e0d6c92a-cebc-fcf8-e053-d805fe0aa794/selecta-2nd-revision.pdf .

[H02] Allen Hatcher, *Algebraic Topology* (2002), Chapter 2, foundational homology and homotopy-invariance results. Author's Chapter 2: https://pi.math.cornell.edu/~hatcher/AT/ATch2.pdf ; book page: https://pi.math.cornell.edu/~hatcher/AT/ATpage.html .

[OWR10] Alessandro Berarducci, joint work with Marcello Mamino, *On the homotopy type of definable groups in an o-minimal structure*, contribution body on printed pp. 27-28, with its last reference on p. 29, in *Model Theory: Around Valued Fields and Dependent Theories*, Oberwolfach Report 01/2010. DOI: https://doi.org/10.4171/owr/2010/01 .
