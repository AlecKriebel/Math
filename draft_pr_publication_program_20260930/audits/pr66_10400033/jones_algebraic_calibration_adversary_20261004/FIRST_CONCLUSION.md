# First independent conclusion — algebraic calibration

Saved 2026-10-04 UTC, before reading any original verifier, README, SOURCES,
research log, review, verification JSON, or another family's verdict.

**Finding:** no falsification found. The candidate's equation (4) agrees with a
fresh exact full-Jones calculation on 344 executed classical knot closures
(311 distinct strand-count/word pairs), including 265 mixed-sign rows.
This is finite normalization/transcription calibration, not an all-knots proof.

## Exact claim and boundaries

The claim under test is that the signed, unbased three-crossing subset sum
with coefficient 1/2 on P=((3,0),(5,1),(2,4)) and coefficient 1 on
T=((3,0),(1,4),(5,2)) equals the normalized v3 of every classical knot diagram.
The target uses n crossings of any supplied diagram. It makes no minimality,
positivity, primeness, or alternatingness assumption. Multicomponent braid
closures are excluded; they are links, outside this knot claim.

## Primary-source reading and algebraic derivation

1. The publisher Ohtsuki source, PDF pages 31 and 33 (printed 403 and 405),
   defines the mirror-odd primitive degree-three invariant as +1 on the right
   trefoil and states the floor n(n^2-1)/24 target. The image is Z x Z; an
   integrality claim is part of the cited normalization, not something inferred
   solely from the candidate's half-weight expression.
2. Ohtsuki printed page 380 gives the Kauffman bracket with empty bracket 1,
   loop factor delta=-A^2-A^-2 and Jones normalization
   delta^-1*(-A^3)^(-w), with q=A^-4. I use the equivalent closure trace
   delta^(number_of_loops-1). Positive braid generators are
   A*I+A^-1*e_i; negative ones are A^-1*I+A*e_i. Exact integer Laurent
   polynomial coefficients are retained through the entire computation.
3. Willerton v1 Section 1 gives v3=-(J'''(1)+3J''(1))/36. For
   J(q)=sum a_k q^k this is exactly -sum a_k(k^3-k)/36. All checked
   knots have J(1)=1 and J'(1)=0. Thus the formula simplifies further to
   -sum a_k k^3/36. No floating-point differentiation is used.
4. I visually inspected a high-resolution rendering of Polyak–Viro 1994
   printed p. 448, Theorem 2 equation (5), and the arrows have precisely the
   candidate's directions: P has the upward vertical arrow and two horizontal
   arrows in opposite directions; T has the upward vertical arrow and both
   diagonal heads below. All three arrows have single arrowheads.
   The theorem's normalization is 0 on the unknot, +1 right trefoil, -1 left.
5. Polyak–Viro's earlier prose uses the word representations/embeddings;
   its literal interpretation as distinct endpoint maps would overcount T's
   three rotational symmetries. CDM Section 13.1.1 instead explicitly defines
   pairing by coefficients in the sum of subdiagrams (presented there for
   based/long diagrams). CDM 13.4.2 identifies PV's first degree-three formula
   as unbased. The trefoil's exact Jones polynomial independently fixes the
   unbased T coefficient to 1: its one triple contributes 1, whereas counting
   three labelled cyclic embeddings with coefficient 1 gives 3. This is a
   convention clarification supported by source normalization and exact
   examples; the tests alone do not establish a universal theorem.

Primary URLs:

- https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf
- https://arxiv.org/pdf/math/0104061v1
- https://www.math.stonybrook.edu/~oleg/math/papers/1994-Polyak-Viro.pdf
- https://www.math.cinvestav.mx/~mostovoy/cdbook/cdbook-as-submitted.pdf

## Fresh computation and adversarial controls

The implementation `independent_tl_calibration.py` uses Temperley–Lieb
matching multiplication and closure trace, rather than a crossing-state
bracket enumeration. Its independent braid-to-Gauss conversion follows actual
top-strand paths through each crossing, then joins bottom position i to top
position i. Only one-component closures are evaluated.

The corpus covers strand counts 1–5 and every diagram crossing count 0–14:
curated torus knots and both trefoils, the figure-eight, all signed 3-braid
words of length 1–5 whose closure is a knot, 160 seeded signed words of
length 6–14 on 3–5 strands (discarding links), plus mirror, orientation
reverse, cyclic-word, positive/negative Markov stabilization, RII insertion,
and positive/negative braid-RIII controls. There were 1330 skipped
multicomponent requested closures. The seed is 10400033.

Full Jones checks include:

- right trefoil: q+q^3-q^4, v3=1;
- left trefoil: q^-1+q^-3-q^-4, v3=-1;
- figure-eight: q^2-q+1-q^-1+q^-2, v3=0;
- T(3,4): q^3+q^5-q^8, v3=10;
- trefoil # trefoil: full polynomial equals the square of the trefoil
  polynomial, v3=2;
- trefoil # mirror trefoil: full polynomial equals the two factor polynomials'
  product, v3=0.

There are 54 rows with nonzero P signed counts, so agreement does not only
test the T term. The 4-crossing closure (-2,-1,-2,-1) has P signed count -2
and T count 0, yielding -1: coefficient 1/2 is exercised. All 344 signed P
counts are even, and every Jones/arrow v3 is integral. All rows satisfy both
the stated floor bound and, for even n, n(n^2-4)/24. These are finite tests.

One initial execution failed because Python (-1)**negative_writhe returns a
float. It was corrected to integer parity before the successful run. The
failure receipt is preserved; no mathematical mismatch was hidden. A source
image crop attempt failed for missing Pillow; native pdftoppm cropping then
succeeded. No source or original-verifier files were modified.

## Strongest verified result and remaining gap

The imported source formula's pictures and normalization agree with the
candidate, and a separately implemented exact algebraic model supplies no
counterexample in the bounded corpus. I have not independently re-proved
Polyak–Viro's all-classical-knots theorem. Consequently this family's finite
result is a calibration certificate, not a replacement for the primary
theorem or for the candidate's graph proof. Novelty/current literature status
and publication decisions remain outside this family's conclusion. No new
central proof route was opened, and the original 1/5 program ledger is
unchanged.

Checkpoint estimate: 70% complete for this assigned algebraic audit; phase two
will inspect/replay the original verifier only after this file is saved.
