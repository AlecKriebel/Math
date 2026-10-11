# Acceptance of the ADKT polynomial-shift obstruction

## Decision

**Accept the restricted theorem and its stated consequences without mathematical correction.** PROOF.md retains the full proof. AUDIT.md retains all nine sections of independent logical review, the complete finite-enumeration argument, and the exact remaining gap. Raw finite integer examples have been removed without changing any proof.

This AI-assisted manuscript is unrefereed. Acceptance records an independent internal AI audit, not external human peer review, journal acceptance, or formal proof-assistant certification.

The original infinite four-total-shift question remains unresolved by this work. No novelty, priority, exhaustive literature-survey, or current-openness claim is made.

## Exact accepted statement

Set x=i+1 and

- a=2x(x-1), b=2x(x+1), c=4(2x^2-1)(4x^2-1);
- n1=1;
- n2=4(8x^4-5x^2+1);
- n3=4(64x^8-112x^6+64x^4-13x^2+1).

For n in Q[x], all three expressions ab+n, ac+n, bc+n are squares in Q(x) if and only if n is n1, n2 or n3. No positivity restriction on the polynomial shift is imposed. For every integer x>=2 the triple consists of distinct positive integers, distinct triples occur as x varies, and these three known shifts are positive and distinct. This provides three total shifts, including 1, rather than the requested four total shifts.

Any fixed rational function F in Q(x) that gives three square identities and differs from the known shifts supplies an integral fourth shift at only finitely many positive integer parameters where it is defined. The same is true for any fixed finite list of such sections.

A rational-function shift valid with an integer shift and integer squares for every sufficiently large integer x must be one of the three known shifts. This remains true on every fixed integer arithmetic progression x=qj+r, with integers q>0 and r. This conclusion is not asserted merely for an arbitrary infinite set of parameters.

## Retained analytical proof

A rational function with polynomial square is polynomial by unique factorization. With square roots t,s,r, set U=r-t, V=r+t, f=4x^2+x-2 and g=4x^2-x-1. The squarefree product UV=4x(x+1)fg reduces every polynomial solution to eight complementary factor patterns, with a nonzero rational unit k of either sign. All signs, constants and zero-root possibilities are covered; no degree bound on the shift was assumed.

The leading coefficient of the forced square root is nonzero. In the equal-degree cases it is 4(k^2+4)/k, so there is no omitted rational denominator or cancellation case. The coefficient recurrence determines the only possible root up to sign. All unequal-degree remainders and their surviving case are retained verbatim. The two cubic cases retain every coefficient of A5, B5, A6 and B6 and the exact Bézout identities over F3 and F7. Degree-preserving reduction and Gauss's lemma exclude any common rational factor. All surviving cases have k=+/-2 and yield precisely the three displayed shifts, whose nine square identities give sufficiency.

The rational-integrality lemma divides F=P+H, clears the polynomial denominator, and uses the proper rational remainder tending to zero. A nonzero rational function has finitely many zeros and poles. The fixed-finite-section corollary uses only this lemma and the classification, never a rank or generator claim.

The eventual-square lemma clears denominators in rational square values and applies the K-th forward difference, K=floor(deg(P)/2)+1, to the positive square root. Its derivative tends to zero, forcing the integer forward difference eventually to vanish. Newton interpolation gives a rational polynomial and infinitely many evaluations give the squared polynomial identity. Zero and constant polynomials, eventual positivity, and fixed integer affine substitutions are explicitly covered in the proof and audit.

## Historical evidence and its limits

The original independent audit checked all eight factor patterns, nine square-root identities, and two modular certificates, and reconstructed 8,212 exact conditions under normal Python, -O and -OO. The saved independent outputs are byte-identical: 505,927 bytes, SHA-256 c91db2c6095fe622e8c3f790741a48a49946e660b1433edb8463074570760c19. They include independently reconstructed full shift sets for exactly 1,000 consecutive family parameters, six original source-table triples, two credited later finite leads, and negative/zero edge controls. All compared rows matched. Exactly two of the checked family parameters have more than three shifts.

The complete finite-enumeration proof remains in AUDIT.md: positive divisor pairs of b(c-a), of equal parity, reconstruct the nonnegative square roots and the shift, followed by the remaining exact square test. It includes negative shifts, zero shifts and zero roots, without bounding the shift size. These historical results neither prove finiteness of all exceptional parameters nor supply infinitely many fourth-shift triples. The later website's asserted verification or novelty was not certified. No mathematical program was rerun during preparation.

The complete written proof and explicit polynomial and finite-field certificates are retained. This is not a computational reproduction package: executable code, raw integer search tables and square-root witnesses, copied source documents and images, and private coordination material are omitted. Historical finite checks are supporting evidence; the universal restrictions follow from the written arguments. The historical computations cannot be reproduced from this edition alone.

## Source and acceptance boundary

The primary source is Adzaga, Dujella, Kreso and Tadic, Triples which are D(n)-sets for several n's, arXiv:1703.10659v1. The exact family is Corollary 5. The source's page-8 display lacks Corollary 5's leading factor 4 and its rank/generator discussion is unused. The original audit independently extracted and visually inspected physical pages 6-9 of the authenticated retained PDF. A fresh public PDF text inspection corroborated v1 and relevant formulas, but did not establish a separately downloaded byte-for-byte remote PDF match. SOURCES.json preserves those limits.

No obstruction is proved for infinitely varying sections, arbitrary algebraic base changes, other positive D(1)-triple families, or all exceptional parameters. The accepted result remains PARTIAL_NOT_SOLVED for the original target. The sealed candidate and original audit remain unchanged; ACCEPTANCE.json binds the original authored inputs and the exact distributed proof, audit and this note.
