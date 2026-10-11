# Mathematical audit for problem 30004608

## Decision

**ACCEPT the main sufficient certificate and the 18-line arithmetic, subject to one required terminology correction.** Accept only as a credited, nonexhaustive consequence of established results. The optional assertion that “strict plus-one generatedness” permits the lower bound nu>=2 is false under Abe's standard terminology; use “not nearly free (d3>d2)” instead. The separately authored corrected proof implements that correction. The original candidate remains unchanged.

Audited input SHA256: bbaba19e636128fedb45206fbb4448ccd8ca356cda2ed18f9a363512dd32a481.

## Hypothesis and notation audit

1. **Field and object.** The argument is for distinct complex projective lines. It does not extend the d3<=d-2 bound to arbitrary reduced plane curves or positive characteristic.
2. **Syzygy grading.** The exponents are coefficient degrees of minimal generators of AR(f), not the shifted degrees of the corresponding Milnor-algebra resolution. The lowest one is mdr(f). In a degree-18 arrangement, the resolution summands S(-24), S(-28), S(-29) therefore yield exponents 7,11,12 after subtracting d-1=17.
3. **Essentiality.** Schenck assumes an essential central three-arrangement. A projective pencil is excluded by the plus-one hypothesis: after choosing f=f(x,y), its syzygy module is free on (0,0,1) and (f_y,-f_x,0). There is no hidden essentiality gap.
4. **Tjurina number.** Ordinary k-fold line intersections are weighted homogeneous with local Tjurina number (k-1)^2. Thus the required total is an incidence-count invariant.
5. **Exponent bounds.** d1+d2=d and ordering imply r<=floor(d/2); d3<=d-2 gives 1<=nu<=r-1 and hence r>=2. The actual minimal syzygy degree r enters S. The test's universal quantifier is essential; choosing just one favorable member would be invalid.
6. **Three distinct uses of degree.** Our d is the number of lines/dual points; j is the unexpected-curve degree; d3 is the third exponent. In Abe's original notation, his “d” often means the level, so it cannot be substituted for our d. The generic splitting exponents sum to d-1, whereas the first two plus-one exponents sum to d.
7. **Unexpectedness.** The criterion concerns a generic point with multiplicity j-1 and allows reducible curves. It does not promise an irreducible curve, a curve with arbitrary assigned point/multiplicity, or an explicit equation.

All invoked statements were checked in primary papers. Formula pages were also visually inspected as rendered PDFs. Public source identifiers, hashes, sizes, and exact theorem/page pins are recorded separately.

## Required correction: strict is not non-nearly-free

Abe's Definition 1.1(2), PDF p. 2, defines strictness by a nonzero linear coefficient in the relation. Proposition 5.1, PDF p. 20, proves strictness for every plus-one generated three-arrangement. Nearly free arrangements satisfy d3=d2 and nu=1 but are still strict. Thus strictness does not justify discarding Delta(r)=1. [Abe primary paper](https://arxiv.org/pdf/1808.04697v3).

The correction affects only the optional sharpening. The main S, which retains nu=1, and its proof are unaffected.

## Independent verification of the known 18-line example

A fresh verifier transcribed the 18 public coefficients and grouped intersecting pairs by exact 3x3 determinants and incidence-index blocks, using a separate implementation for this check. It found 47 distinct intersections:

    t2=22, t3=13, t4=7, t5=5.
    sum binomial(k,2)t_k = 153 = binomial(18,2).
    tau = 22+4*13+9*7+16*5 = 217; m=5.

For r=2,...,9, Delta(r) is 42,30,20,12,6,2,0,0. Therefore S={7}, and 5<=8<9 certifies precisely degrees 8 and 9, with general-point multiplicities 7 and 8.

An additional exact rational linear-algebra check independently verified mdr(f)=7. The degree-6 Jacobian relation matrix has size 300x84 and rank 84. Lower-degree relations would multiply into degree 6, so none exist. The degree-7 matrix has size 325x108 and a one-dimensional kernel; an exact nonzero integer relation was checked to have zero residual. No full minimal-resolution recomputation is claimed.

This is not a new arrangement or new numerical discovery. The same exponents, incidence counts, tau, and unexpected degrees already appear together in Malara, Pokora, and Tutaj-Gasinska, [On 3-syzygy and unexpected plane curves](https://doi.org/10.1007/s10711-021-00602-5), Geom. Dedicata 214 (2021), Example 5.10, printed p. 59. Pokora's OWR report repeats the example and poses the question on printed pp. 282-283: [OWR 5/2021](https://ems.press/content/serial-article-files/46883).

## Strength and limits

The certificate eliminates an unknown exponent conservatively by testing every exponent consistent with necessary numerical conditions. It adds a convenient finite arithmetic formulation when plus-one generatedness is independently known. It does not strengthen Dimca's general iff theorem or improve its degree range, and no novelty search sufficient to claim originality was performed.

The lack of necessity is concrete. In the published family of Malara-Pokora-Tutaj-Gasinska Example 5.12, printed p. 60, n=7 yields d=19, exponents (8,11,12), tau=242, and an unexpected curve of degree 9. The inclusive test gives S(19,242)={7,8,9} and fails at r=9 because 10 is not less than 19/2. This limitation uses the family's published resolution and existence result, not a newly recomputed resolution. [Primary paper](https://link.springer.com/content/pdf/10.1007/s10711-021-00602-5.pdf).

Thus a failed certificate cannot mean nonexistence. A full combinatorial decision of plus-one generatedness and unexpectedness is not supplied. Problem 30004608 should not be described as a new complete classification or an original solution on this evidence.

## Integrity and completion

The separate corrected proof is the accepted mathematical text. The original candidate and sealed audit inputs remain unchanged. Arithmetic checks use explicit exceptions and run successfully with ordinary Python, -O, and -OO. Stored source PDFs, page images, raw example coordinates, and detailed local verification material are excluded from the public-file allowlist. Only authored proof/audit and public verification metadata are proposed for any later authorized publication.

## Review status

This proof and audit packet was prepared with AI assistance. No external human mathematical review, referee certification, or formal proof-assistant verification has been obtained. The independent checks described above are computational checks using a separate implementation and primary-source inspection; they are not a claim of independent human review. Acceptance here is the limited mathematical assessment stated in this report, not acceptance by a journal or referee.
