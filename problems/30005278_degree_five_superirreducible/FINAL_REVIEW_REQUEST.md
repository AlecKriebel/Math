# Full independent review request: 30005278

This is the complete five-turn author freeze. Start FINAL_RESULT.md, SOURCE_GATE.md, all five TURN_n.md, FINAL_REPLAY.json and FINAL_AUTHOR_MANIFEST.json. Review the whole mathematical packet and exact source scope. Earlier progress files remain immutable and retain their historical unresolved substeps; Turn 5 expressly closes Turn 2's integrality gap.

## Primary evidence

Primary files are supplied separately; SOURCE_HASHES.json binds OWR 50/2022, Du v2 and the finite-field authors' paper. SOURCE_ADDENDUM_TURN_3.json binds Conrad's Dedekind/Chebotarev statements. Visually inspect OWR printed2945.png. The original shorthand degree<=2 is interpreted through the authors' explicit positive-degree/fraction-field definition, not a constant or content loophole. Dates: 2022 report, 27 July 2023 publication; Du v2 posted 17 June 2025 with PDF front-page date June 18.

## High-risk checks

- Turn 1: the dyadic object is Q_2[X]/(f), not a field. Check reducedness modulo two, primitive-square parity, the F_2 x F_16 trace obstruction, the complete converse via contraction, and the exact valuation boundary for all a,b,c, including b=0. The globally irreducible 2x²+x example is certified modulo 11; local splitting is not global reducibility.
- Turn 2: verify all three quadrics, every zero-coordinate exclusion, the rational-root theorem candidate lists, and the denominator identity R(s,s²)=f(s)². The nonconstant rational-point correspondence is exact. The 161,050-vector box is only diagnostic.
- Turn 3: audit the S_5 proof from the mod-17 (2,3) type plus a 5-cycle, the unique quadratic subfield, total signs in the five paired roots, and both directions of the 10-cycle criterion. Check the nonmonic-to-monic polynomial change used for Chebotarev and all degree-drop qualifications. Square norm is not sufficient for reducibility.
- Turn 4: audit the integer translation/reflection normal form, both signs of leading coefficient ±2, all 600 initial certificate rows, the exact expansion, and the universal n>=200 bounds/signs. No other integer points of the norm curves are claimed classified.
- Turn 5: scrutinize the odd-degree norm-square/CRT lemma at primes dividing both M and N, especially two, and the construction G=Mx²+2rx+(r²−N)/M. Verify the monic restriction, denominator clearing, and the closure of the earlier integrality gap. Check the convergent local square-root series, all five leading terms, the nonzero denominator coefficient 1/1024, and why all-completions points do not imply a rational point.

Run all five Python scripts and compare stdout with their frozen JSON receipts. Turns 2, 3 and 5 require SymPy; the others use the standard library. Regenerating the initial certificate must agree byte-for-byte with its frozen version. 78,440 is the author assertion count, distinct from the number of diagnostic vectors or norm inputs scanned.

The author recommends unsolved 5/5 for the original source, with the scoped positive theorems and exact remaining global curve gap retained. No full solution, novel-discovery certification or human peer review is claimed. Freeze a bound full source/proof verdict separately and report any mandatory correction promptly. Do not extend the author search or add a sixth author turn.
