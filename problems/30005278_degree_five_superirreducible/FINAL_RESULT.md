# Final author result: 30005278 / OWR-11695860-018

**Original degree-five existence problem unresolved, five substantive turns completed. Recommend unsolved 5/5 after full independent review.** No degree-five 2-superirreducible polynomial or integer quadratic counterexample to the studied candidate has been certified.

## Exact target and prior credit

The source is Wooley's Question 9, OWR 50/2022, printed 2945: https://ems.press/content/serial-article-files/46986 . It attributes the question to Bober, Fretwell, Kopp, Du and Wooley. Report year 2022 and actual publication 27 July 2023 are both retained. The authors' explicit later definition makes the substitution degree positive (one or two) and tests the composition in Q[x]; constants and content factors are not meaningful counterexamples. See SOURCE_GATE.md.

The candidate f(X)=X^5+2X+1 and its known irreducibility under every integer substitution ax²+c are due to Lara Du, https://arxiv.org/abs/2409.16206v2 . This packet supplies scoped deductions beyond that class, with no historical novelty claim. Capelli, finite-field norm criteria, Dedekind and Chebotarev are credited dependencies; no splitting field is confused with the degree-five root field.

## Verified author claims, pending independent review

1. **Exact dyadic boundary.** For g=ax²+bx+c, a nonzero, the discriminant element 4a theta+b²−4ac is a square in the full dyadic algebra K tensor Q_2 exactly when b is nonzero and v_2(a)>2v_2(b). Thus all complementary integer quadratics, including every odd a, preserve irreducibility over Q. The locally split class is not declared globally reducible.
2. **Global sparsity restriction.** Every nonconstant linear-square witness z²=M theta+N in K uses all five power-basis coordinates. Exact elimination gives the affine plane equation R(s,t)=0 in TURN_2.md, with all rational exceptional denominators excluded. The finite coefficient box is not a complete rational-point computation.
3. **Prime-certificate boundary.** For D=Norm(4a theta+b²−4ac), a full-degree irreducible prime reduction exists exactly when D is in neither of the rational square classes 1 and 11317. The proof includes a concrete S_5 certificate and uses credited Dedekind/Chebotarev. In particular there is an infinite family of globally irreducible compositions with no full-degree irreducible reduction at any prime; x^10+2x²−1 is a monic example. Square norm remains insufficient for a global square.
4. **Three global discriminant bands.** For a=±2 and b odd, irreducibility holds whenever b²−4ac=n²+8r with n positive odd and r=-1,0,1. A consecutive-square estimate proves every n>=200; a complete exact 600-case certificate handles the initial range. This lies inside the dyadically split class and is not just an enlarged numerical search.
5. **Odd-degree integral descent and exact remaining gap.** For every fixed monic irreducible integer polynomial of odd degree, quadratic superirreducibility over integer substitutions is equivalent to the rational-substitution version. The proof constructs square residues modulo M from an odd-degree norm-square identity, then gives an explicit integer counter-substitution if a global witness exists. This closes the integrality gap left in the historical Turn 2. It is not asserted for arbitrary nonmonic polynomials. For the monic quintic candidate, superirreducibility is now exactly equivalent to R having no rational point. The curve is proved to have points over the reals and every Q_p, but its rational points are undetermined.

The fifth claim does not promote a necessary norm condition to a sufficient root-field square. It only converts a genuine global square witness into an integer substitution. Likewise points over all completions do not supply a rational point; the local construction uses a separately chosen parameter at each place.

## Reproducibility and remaining limit

All five exact receipts replay byte-for-byte, totaling **78,440 assertions**. Turns 1 and 4 use only Python's standard library; turns 2, 3 and 5 additionally use SymPy, tested at 1.14.0. TURN_4_SMALL_CERTIFICATE.json contains every one of the 600 finite initial cases; the proof covers the entire remaining infinite range analytically. Other finite boxes and sample prime reductions are labelled diagnostics.

FINAL_AUTHOR_MANIFEST.json binds all public author files, preserving every historical turn manifest and receipt. SOURCE_HASHES.json and SOURCE_ADDENDUM_TURN_3.json bind separately supplied primary evidence. PDFs, screenshots, extracted source texts, raw imports and retrieval logs are not redistributed.

The decisive global rational-point statement for R remains open here. A proof or counterexample for all degree-five candidates has not been obtained. The five author turns are complete, no sixth search is planned, and the full frozen source/proof packet is submitted for independent review.
