# Root mathematical review: PR1268 /10900050

2026-10-17T23:30Z. Estimate: mathematical verification 85%; packet 10%.

All ten original records were read completely, including the editorial map. The
new review concerns the exact prime-element graph and the displayed equality in
Long's Question 7.2 of arXiv:1512.04620v1. The statement has a complete elementary
negative resolution in the submitted scope. Independent adversarial seals must
still be authenticated before this is promoted to a mathematical gate.

## Scope checked against actual primary pages

The root freshly retrieved both pinned primary PDFs on 17 October 2026. Their
byte counts and SHA256 identities equal the submitted pins. The root read the
question's setup, displayed formula and reference 19, and the author manuscript's
definition and Section 3 discussion and Theorem 3.1 proof. PDF pages 5, 6 and 7
of the problem list and pages 1, 9 and 10 of the 16-page manuscript were rendered
locally and visually inspected. The problem list has no PID premise. The graph
adds prime-element differences to unit differences; the manuscript explicitly
defines prime cliques by condition (i) alone, where the differences generate
prime ideals. Condition (ii), concerning unit-group surjectivity, belongs to the
more restricted Lenstra-Hurwitz cliques. An irreducible-difference interpretation
would change the problem and invalidate this particular two-color argument.

The printed manuscript theorem uses a minimum principal-ideal norm whereas the
question displays a minimum prime-ideal norm. This review does not identify those
minima, repair the manuscript theorem, or use its proof as an imported lemma.
It directly evaluates every term of the question's displayed equality. A separately
imposed PID-only question is outside the accepted claim.

## Complete arithmetic and ideal argument

1. The monic polynomial X squared minus 10 is irreducible and totally real.
   If r+s sqrt(10) is integral, trace and norm are integers. Writing m=2r
   yields 40s squared integral; a reduced denominator v of s has v squared
   dividing 40, hence v is 1 or 2. Put n=2s. The congruence m squared minus
   10n squared equal to zero modulo 4 forces n and m even. This proves the
   full ring is Z[sqrt(10)], rather than just a suborder. Conversely each
   integer-coefficient element satisfies the displayed monic quadratic.
2. Constant coefficient modulo 2 is a surjective ring homomorphism onto F2;
   multiplication respects it because 10 is even. Its kernel is exactly
   P=(2,sqrt(10)), so P is nonzero, proper, maximal and prime, of index 2.
3. Multiplication by a+b sqrt(10) has matrix [[a,10b],[b,a]]. For a nonzero
   element its determinant is nonzero, and the principal ideal's index is
   the absolute determinant, by the integer lattice index theorem. If P
   were principal, that determinant would be plus or minus 2. Reduction
   modulo 5 demands a square equal to 2 or 3; both are impossible. Thus P
   is nonprincipal. No class-number, unit-group, or prime-search data enter.
4. For every nonzero prime ideal Q, choose a nonzero delta in Q. The same
   determinant formula makes O/(delta), and hence O/Q, finite. A finite
   integral domain is a field. This proves maximality of every such Q
   without importing the full Dedekind-domain theory.
5. A proper ideal contains no units. If a prime element p lay in P, the
   nonzero maximal ideal (p) would be contained in P and hence equal to P,
   contradicting nonprincipality. Therefore no allowed graph difference is
   in P. The two residues modulo P properly color both graphs. The edge
   {0,1} attains the bound, so both clique numbers are exactly 2.
6. Every proper-ideal quotient has at least two elements; P attains two
   among nonzero prime ideals. Including the zero prime cannot lower that
   minimum because its quotient is infinite. The displayed values are
   consequently 2 and 2 times 2, which are unequal.

## Adversarial boundaries and provenance

The element 2 is irreducible but not prime here: its absolute norm is 4 and a
factorization into nonunits would require norm-two factors, already ruled out;
norm-one elements are units by conjugation. The nonzero residue of sqrt(10)
in O/(2) has square zero. Thus the graph with irreducible differences contains
the triangle {0,1,2}. Replacing nonprincipality by mere primality also fails: in
Z[sqrt(2)] the principal prime (sqrt(2)) has norm 2 and contains its prime
generator. These controls isolate assumptions used by the universal proof.

Original acceptance and source-inspection records remain historical records
dated 11 October. Current output bytes, protected ranges and exact replacements
in the editorial map can be authenticated. Missing removed historical input
bytes cannot be recreated from their hashes, and this review does not claim a
complete replay of that earlier editorial operation. Current mathematics is
reviewed directly from the available proof and sources.

The source-only family independently found the same ideal and counterexample
before seeing any candidate material. This is independent reconstruction of
the same mechanism, not evidence for a materially different mathematical proof.
Fresh candidate and reconstruction adversaries are being recorded separately.
All finite diagnostics supplement the elementary universal proof. No novelty,
priority, current openness, human peer review or formal certification is inferred.

An extensive fresh priority audit and publication package remain pending the
mathematical acceptance gate. AI tools were used extensively in this work.
