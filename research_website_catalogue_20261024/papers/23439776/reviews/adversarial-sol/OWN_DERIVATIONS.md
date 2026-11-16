# Independent source-only adversarial derivations

These are my own source-derived hand calculations before foreign supporting proofs, native code/results or other-family findings. They are deductions about the explicit printed data and do NOT yet authenticate the canonical GHKK identification or exact historical target. No mathematical program has run in this family.

1. Signed-permutation attack on reducedness. Use the Cartesian D4 roots alpha1=e1-e2, alpha2=e2-e3, alpha3=e3-e4, alpha4=e3+e4. The first three simple reflections swap the corresponding adjacent coordinates; s4 swaps and negates coordinates3,4. Right multiplication by the word gives successive column-image lists:
(2,1,3,4), (2,3,1,4), (2,3,4,1), (2,4,3,1), (2,4,-1,-3), (2,-1,4,-3), (-1,2,4,-3), (-1,4,2,-3), (-1,4,-3,2), (-1,-3,4,2), (-1,-3,-2,-4), (-1,-2,-3,-4).
Thus the product is -I4. Its successive inversion roots in Cartesian coordinates are e1-e2,e1-e3,e1-e4,e3-e4,e1+e3,e1+e4,e1+e2,e2-e4,e2+e3,e3+e4,e2+e4,e2-e3: all twelve distinct positive D4 roots. This independently checks length12 and the source's simple-root expansions, rather than assuming a braid-search output.

2. Occurrence/quiver control. Next occurrences are (7,4,9,6,11,8,13,10,13,12,13,13); the frozen indices are exactly7,9,11,12 and mutable count8. The horizontal arrows are1->7,2->4,3->9,4->6,5->11,6->8,8->10,10->12. Applying the printed strict interlacing and Dynkin adjacency gives exactly6->1,3->2,8->3,5->4,10->5,7->6,9->8,11->10. This matches all sixteen arrows with multiplicity one. I explicitly checked the tempting f11 mutation at10: path11->10->5 cancels the existing5->11 arrow; it does not leave an extra outgoing edge. Frozen-frozen erasure also removes the created11->12 edge. Hence this short boundary control is consistent with an optimized f11 row.

3. Candidate polynomial support/cancellation attack. Treat the displayed F7/F9 as candidate expressions, without yet importing their canonical identity. F7 has 2+3+6+3=14 terms: base1,y6; y6y8 times A (three); y6y8y10 times (1+y5)A (six); and times B(1+y6+y1y6) (three). B terms are distinguished from all preceding terms by y4. The final two are distinguished by exponent2 at y6 and then presence of y1. No collisions occur. F9 has1+1+3=5 terms, F11 has2 and F12 has1. Different frozen markers prevent inter-summand collisions, so the printed candidate has22 coefficient-one monomials. Each term contains exactly one frozen marker and no other frozen variable. Its only exponent2 occurs in y6 in the two stated terms, so these are genuinely X6^-2, and6 is mutable.

4. Dimension/lineality adversary independent of certificate arithmetic. Let a_j denote the printed lexicographic rows. The following row combinations generate the standard coordinate basis:
e12=a1; e11=a2; e9=a4; e7=a7; e10=a3-a2; e8=a5-a4; e6=a8-a7; e3=a14-a9; e2=a17-a14; e5=a12-a10; e4=a13-a11; e1=a22-a21.
Thus row rank is12. In particular the candidate inequality cone has no hidden lineality: Az=0 forces z=0. The source's u=e7+e9+e11+e12 has a_j.u=1 for every row by the frozen-marker observation, giving a strict interior point and full dimension12. Distinct primitive normals cannot be positive scalar duplicates: each has a frozen coordinate1.

5. Direct sparse separating controls, including BOTH large-exponent terms. For row22, z=-e1 gives a22.z=-1 and all other rows0, because only the last monomial contains y1. For row21 take z=e1-e6+e7. On F7 terms the dot product is a1-a6+1: it is1 on the constant-in-F7 term,0 on ordinary y6 terms, -1 on row21,0 on row22. All other summands give0. Thus neither offending monomial can be redundant independently of the rest of the table.
Additional hand controls: row1 uses -e12 (unique y12); row2 uses -e5+e10-e11 (every y5 in other groups is accompanied by y10, and the second F11 term cancels); row3 uses e8-e10 (all other y10-bearing terms have y8 except F11, selected row3); row7 uses -e1+e6-e7; row8 uses2e2-e4-e6+e8; row20 uses-e4-e5+e6+2e9. Inspecting the four frozen-marker term groups gives diagonal-1 and off-diagonal nonnegative in each case. For row20 in particular every y4 term of F7 has y5 and y6; the squared-y6 terms give0, and F9's frozen y9 contributes2. These checks target coordinates where a sign/index mistake would be consequential. I have NOT yet checked all484 table dot products; that remains an explicit finite verification task.

For any such verified separating vector z_j, p_j=z_j+u has selected dot0 and all other dots>=1. Because a_j is nonzero, an open neighborhood inside its11-dimensional hyperplane remains feasible; the selected inequality is a facet. The same argument applies to all22 only AFTER all table inequalities or an independent certificate are actually checked. No sampling or floating-point tolerance is a premise.

6. Full hand chamber-map calculation. From the printed occurrence/Cartan rule the twelve K rows are:
K1=e1-e2-e4-e6+e7;
K2=e2-e3+e4;
K3=e3-e4-e6-e8+e9;
K4=e4-e5+e6;
K5=e5-e6-e8-e10+e11;
K6=e6-e7+e8;
K7=e7-e8-e10-e12;
K8=e8-e9+e10;
K9=e9-e10-e12;
K10=e10-e11+e12;
K11=e11-e12;
K12=e12.
They are upper triangular with diagonal1, so determinant1. Multiplying the22 printed exponent rows gives, in their displayed order:
1:e12
2:e11-e12
3:e10
4:e9-e10-e12
5:e8-e12
6:e8+e10-e11
7:e7-e8-e10-e12
8:e6-e10-e12
9:e6+e8-e9-e12
10:e6+e8-e9+e10-e11
11:e5-e6
12:e5-e9
13:e4
14:e3-e4-e12
15:e3-e4+e10-e11
16:e3+e5-e4-e6-e8
17:e2-e12
18:e2+e10-e11
19:e2+e5-e6-e8
20:e2+e4-e8
21:e2+e4+e6-e7
22:e1.
Every coefficient lies in{-1,0,1}. In particular a22=a21+e1 and adding K1 to the21st output cancels e2,e4,e6,-e7, leaving e1. This independently exhibits why a unimodular monomial map need not preserve the absolute-exponent bound while preserving the cone presentation. No contradiction of the later string-coordinate conjecture follows from this example.

7. Falsification status/remaining interfaces. The printed candidate data survive these internal attacks, but survival is NOT a scientific verdict. The main outstanding risks are external: is the seed/optimization/pullback formula genuinely the canonical normalized potential in the exact cited conventions, and does the full published1125 target literally put the proposed absolute bound in those canonical coordinates? The later proof's claimed equivalence must be read in full hypothesis context; a source paraphrase cannot settle it. The complete remaining finite certificate arithmetic and exact canonical pullbacks also need a selected reproducible check. Earlier Case267 word/support credit must be authenticated if relied upon; Git dates alone are not public-availability proofs. No repaired/narrower claim or priority assertion will be substituted if an interface fails.
