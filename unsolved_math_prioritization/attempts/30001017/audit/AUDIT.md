# Independent adversarial audit: first Voronoi intersection numbers

Problem 30001017, rank 662. Audit date: 2026-10-04 UTC.

## Verdict

**Accept as an unresolved five-approach partial-results packet, with the two clarifications in CORRECTIONS.md.** No proof of the all-genus conjecture, counterexample, or evaluation of the missing genus-five intersection has been found. The proposed disposition remains **unsolved, five of five approaches exhausted**. This acceptance certifies the stated limited arguments and exact arithmetic, not novelty or a solution of the problem.

The first required zero outside the cited EGH theorem is precisely the genus-five stack degree L^2 D^13. It remains unevaluated. None of the identified preprint inconsistencies supplies a counterexample.

## Frozen input and independent replay

The author archive is 25,801 bytes, SHA-256 b4843f6a1906674e6a0ad15e5f05e4b23e08692f039cd6847780559663e07797. Its 14 files comprise 13 manifest entries plus the manifest. The archive path allowlist, member bytes, sizes, and hashes were checked. The author manifest checker passes. Running the author arithmetic checker in an isolated extraction reproduces CONTROL_RESULTS.json byte for byte. The original archive and every original safe file remain unchanged.

The independent checker imports no author code. It starts with formal inversion of (1-exp(-x))/x, computes the two-variable Todd coefficients by power-series multiplication, substitutes theta/Poincare polynomials directly, and reduces the projective-bundle variable by xi^2=xi*P. Thus it does not reuse C_g(a,b) or the author's simplified term-I formula. Its four outputs agree with the author for every genus 2 through 10.

Additional controls include 177 Todd coefficients (including pure and constant terms), 100 exterior-algebra versus determinant tests for one through four factors, 256 exact rational residual-stencil assignments, the strict theorem range through genus 60, and explicit sign and normalization witnesses. All pass. These are finite algebra controls, not computations of deeper-boundary Chow classes.

## Claims audited

- C1, exact target: the official Oberwolfach report, printed p.2187, and EGH Conjecture 1.2 match the triangular-exponent statement. First Voronoi and perfect cone are the intended compactification.
- C2, support cutoff: valid. A sufficiently divisible Hodge class is pulled back from an ample globally generated class on Satake; more hyperplanes than the image dimension have empty intersection. Chow localization justifies the stated range, with a strict inequality. A same-dimensional cutoff would be false.
- C3, abelian weights: valid for the symmetric rigidified polarization and normalized Poincare classes on the stated abelian schemes. Functoriality gives p_*[m]_*beta=p_*beta, while finite-flat degree gives [m]_*[m]^*alpha=m^(2h)alpha. Combining these yields the claimed vanishing. It does not make [m]_* the identity on Chow(B). The factorwise degrees are m^(2h), and the off-diagonal Poincare weights are m. The determinant normalization has off-diagonal entries u_ij, not u_ij/2. In particular the elliptic value of P^2 is -2.
- C4, EGH range: correctly imported as an external theorem, not reproved. N<3g-3 is equivalent to n>T_(g-3). The g=2, N=3 calculation is correctly labeled a consistency check outside that strict range.
- C5, finite arithmetic: independently reproduced. In genus five, I=-1/1296, II=-3637/2520, III=1063/7560, and their sum is -59123/45360. These are the known N=9 numbers, not N=13.
- C6, source inconsistencies: all five listed v1-specific observations are corroborated by independently retrieved identical PDF bytes, direct reading of the relevant pages, and independent arithmetic. They remain version-specific. The journal PDF was not inspected.
- C7, birational support: the degree identity is valid under its stated rational-Cartier and support assumptions. The proof as written invokes globally generated hyperplanes without including that assumption in its abstract statement. CORRECTIONS.md supplies a projection-formula proof that establishes the stated numerical conclusion without it. The actual Satake application already has the needed Hodge positivity. The common-refinement comparison is conditional on the specified boundary classes and discrepancy support; it does not remove the rank-three term.
- C8, residual extraction: valid. The strict theorem leaves exactly (g-3)(g-4)/2 required zeros for g>=3. The first is n=2 at g=5. The four-point numerator kills degrees 0, 2, and 3 and multiplies the linear coefficient by 12, giving denominator 12*105=1260. Assigning a13=1 in a formal polynomial remains compatible with the known coefficients, but is not a geometric counterexample.
- C9, global target: unresolved. The data do not establish support over A_1 in genus five, and the residual A_2 contribution is uncomputed.

## Boundary, stack, and theta conventions

The degree-two universal-abelian cover of the Kummer boundary contributes 1/2. With rigidified theta, the boundary pullback is -2theta; with the unnormalized theta divisor it is -2theta'+L, where theta'=theta+L/2. The packet keeps these conventions separate and its cancellation calculation is correct. A base twist has weight zero and can produce positive-codimension pushforwards, so the smooth-family argument cannot be recycled across degeneration without proof.

For the specified coarse divisor classes whose pullbacks equal the stack classes, stack integrals are half coarse integrals. The genus-four numerical controls match that conversion. This does not license applying a factor two to unrelated divisor definitions or dropping stack stabilizers on deeper strata.

A further source caution was found: the rank-one display on OWR p.2188 lacks the Kummer factor 1/2 when read in these conventions. At g=3 it gives 1/360 from H_2=1/2880, while the report's own p.2187 table gives 1/720. The author's normalized rank-one formula already includes the correct factor. No packet result needs to be changed because of this additional warning.

## Version-specific numerical discrepancies

For the inspected arXiv:0707.1274v1 only:

1. The printed Proposition 9.4 correction differs from its preceding finite calculation; multiplying that correction by 2^(2g-4)(2g-2)! restores agreement for every tested genus 2 through 10. This audit does not promote that bounded check to a new all-genus symbolic summation theorem. At genus three, the displayed simplification gives -119/1920 while the direct computation and table give -1/80.
2. Table (30), genus six: the finite formulas give II=-23837/630 and III=1639/630, half the displayed values. Term I agrees.
3. Table (30), genus seven: the finite III value is 203645/189, not 17594928013/16329600. Terms I and II agree.
4. Theorem 7.5's displayed expression omits the H_(g-2) factor present in its proof.
5. The top theta-pushforward display on p.33 has the opposite sign. At g=2,k=2,n=1 its left side is 1, but the printed right side is -1. The subsequent finite double sum has the correct sign.

The v1 submission is from 9 July 2007; the PDF's 2021 typesetting date is not a new arXiv version. No claim is made about whether any of these issues survives in the 2010 journal publication.

## Prior overlap

The true related catalogue item is ID20000348, AIM-ALGEBRAIC_GEOMETRY-0348. The official AIM Problem 6.2 is a broader six-part Shepherd-Barron question; part (3) asks for all divisor intersections and plurigenera. Its existing partial report concerns conditional Cox-ring/restriction consequences and expressly leaves the full intersection problem open. It is related background, not the same completed triangular-vanishing target. The ID-to-problem-number correspondence was independently checked against the authorized catalogue bytes identified by the author. No unrelated Voronoi or qutrit item was treated as a duplicate.

## Sources and limits

Public source identifiers, retrieval hashes and inspection scope are in SOURCE_AUDIT.json. Independently retrieved EGH v1, OWR, A4, and theta-relations PDFs match the author hashes. Relevant formula pages were read in text and, for EGH and OWR, also visually. The published EGH journal endpoint could not be inspected; the author's publication list verifies the 2010 bibliographic reference only. The 2026 cohomology preprint was checked at abstract/version level, which cannot rule out every implication of its full text.

This audit did not rerun exhaustive literature or repository searches and does not prove current global openness. It did not independently reprove EGH's singular-fiber GRR theorem, establish new higher-corank geometry, mutate a queue, contact third parties, or make remote writes. No sources, extracted text, dataset records, or private coordination material are redistributed in this audit packet.
