# Independent audit: admissible Gelfand-Zetlin faces

## Verdict

**PASS. Recommend `already_solved`, negative resolution, for ID 30001132 only.**

The published result, the reconstructed smooth example, the 24-choice obstruction,
and the final frozen packet agree. No mathematical correction is required. This is
verification of an existing negative result, not a novel resolution. The frozen
author log records one substantive investigation response, consistent with the
proposed 1/5 accounting. This review adds verification, not an author proof-search
attempt; the five-search exhaustion route was neither used nor claimed.

This audit is bound to the author manifest SHA-256
`0a585b480317c19cc8fd53e08a322d87661e1c8076ff1a49d37e62e77dd1549d`.
All ten listed files match their recorded byte counts and hashes. The inventory
has no extra files beyond its manifest. Frozen author files were not modified.

## Primary-source and quantifier checks

The auditor independently downloaded the published IMRN PDF and the original
OWR report from their public institutional/publisher URLs. Both exactly match
the recorded sizes and hashes. The relevant pages were extracted from these
new downloads, and published p. 2522 and OWR pp. 24-25 were rendered and visually
inspected. The web fetch initially timed out; ordinary direct retrieval succeeded.

- The original OWR report, pp. 24-25, poses the smooth-closure conjecture and
  explicitly describes its Borel freedom relative to a fixed maximal torus.
- The final IMRN article, p. 2522, explicitly reports a smooth SL4 failure.
  It does not identify that example by the permutation 2413 or give its explicit
  certificate at that location. Those are the packet's verified reconstruction.
- IMRN Section 2.3 defines a preceding cell to have codimension one. Consequently,
  Section 3.2 admissibility tests boundary divisors, not every lower cell at once.
  The packet and both submitted algorithms use the correct condition.
- Sections 3.1-3.2 and 5.1-5.3 support the fixed-torus Borel set, the orbit-to-face
  construction, the simple-vertex labeling, and the signed root rule used here.

There are precisely 24 Borels containing the chosen diagonal torus. Fixing one
such Borel gives a Schubert basis, so there is one orbit class representative
relevant to the specified basis element. If B_b=b B+ b^-1, the representative of
[X_w] is the orbit through bw. Its closure is b X_w, and group translation
preserves the cycle class. Thus the 24 candidates are exhaustive for the original
construction. Neither additional coordinate flags for a fixed Borel nor arbitrary
unions of faces enlarge the admissible candidate set in this definition.

GL4 and SL4 have the same complete flag variety and root-orbit data. Scalar
matrices act trivially. The change of group in the final article therefore does
not create a gap in answering the GLn formulation.

## Permutation and smoothness checks

The convention is X_w=closure(B+ w B+/B+), of dimension length(w), with ordinary
function composition. The rank matrices independently give the covers 1423,
2143, and 2314 for w=2413. They give exactly the incidence conditions
F1 subset E2 subset F3; the middle plane is otherwise free between F1 and F3.

Choose a fixed complement C4=E2 direct-sum W. The pair consisting of F1 in E2
and the line F3/E2 in W varies over P1 x P1. Over that base,

    F3/F1 = (E2/F1) direct-sum (F3/E2),

a rank-two vector bundle, and F2/F1 chooses a line in it. Equivalently this
bundle is O(1,0) direct-sum O(0,-1), using the line convention for its second
factor. Its projectivization is smooth of dimension three. This directly proves
smoothness of the exact dimension-indexed variety being tested. It does not rely
on translating a pattern-avoidance or Schubert-polynomial indexing convention.

The independent checker labels vertices by their weights rather than by the
author's chain recipe. If S_r is the sum of row r and S_0 is the top-row sum,
the weight coordinates can be taken to be

    (S1-S0, S2-S1, ..., S_(n-1)-S_(n-2), -S_(n-1)).

At V_sigma this is (-lambda_(sigma^-1(1)), ..., -lambda_(sigma^-1(n))).
It is therefore the ordinary left Weyl action on the highest weight, not the
inverse action. The identity vertex has only negative outgoing roots, as a
highest-weight vertex must; the B+ orbit there has dimension zero. This also
checks the signs in the Borel test and the placement of bw rather than wb.

## Independent exact verification

The submitted diagram enumeration, tangent-cone certificate checker, and six
regression tests were rerun without modifying the frozen directory. All pass.

The new `independent_polytope_check.py` imports neither submitted algorithm.
It starts from all interlacing inequalities, enumerates all full-rank active
subsystems with rational Gaussian elimination, and keeps feasible solutions.
This is complete because every vertex of a full-dimensional bounded polytope
has a full-rank active subsystem. The resulting vertex counts are 2, 7, and 40
for n=2,3,4. It then:

1. Locates each extremal vertex through its weight, independently of chain labels.
2. Obtains each incident edge by retaining all but one active inequality at that
   simple vertex and finding the two endpoints among all enumerated vertices.
3. Reads the oriented root from the weight difference of the endpoints.
4. Selects the B_b roots, constructs the entire face vertex set, and tests face
   inclusion using vertex-set inclusion.
5. Constructs the Bruhat order from rank inequalities, independently of the
   author's downward-transposition cover enumerator.
6. Verifies each supplied witness equation, predecessor, composition, and unequal
   top-row labels. Every one of the 24 rows fails the necessary vertex containment.

Every class/Borel decision agrees with the author's enumerator for n=2,3,4.
All classes have an admissible representative for n=2,3. The nonrepresentable
n=4 classes are exactly 2413, 3412, and 4231. The latter two are the singular
classes; the geometric argument above independently settles the first.

The n=4 checks were repeated for top rows (1,2,3,4), (0,2,7,19), and
(-17,-2,3,31), verifying 72 certificate instances. These numerical choices are
stress tests, not a substitute for the general proof: each certificate failure
compares two distinct top-row labels, so it persists for every strictly increasing
top row. The retained face equations and oriented roots depend only on the order.
Six independently constructed invalid-certificate variants were rejected:
missing or duplicated Borel, wrong composition, non-cover predecessor, wrong
face equation, and wrong predecessor coordinate labels.

The checker also tests the stronger all-lower-cell condition separately. It
excludes four additional Borel/class pairs belonging to classes 3421 and 4312,
without changing which classes have some representative. This is a deliberate
definition-sensitivity control: calling those four pairs counterexamples to the
author's enumeration would misread the source's codimension-one definition.

## Scope, safety, and remaining limits

The proof only needs a necessary condition: if a predecessor vertex lies outside
the candidate face, its entire associated face cannot be contained in it.
There is no invalid inference from vertex containment to face containment.

This verdict concerns one admissible face in the original correspondence. It
does not rule out sums, unions, other face-cycle constructions, or identities
in a polytope-ring quotient. It assumes a regular weight, as the source does.

The audit did not repeat the full external repository/prior-attempt search and
does not claim that the author logs prove absence of undocumented work. The
target webpage access limitation is disclosed in the frozen packet. The primary
OWR and final IMRN sources plus the independent finite proof settle the mathematical
question despite that limitation.

ID 30001133 is equivalent-target metadata only. This audit recommends no separate
queue disposition for it. There were no helpers and no remote writes. The safe
audit files contain authored reasoning, executable checks, results, and public
verification metadata only; retrieved PDFs/text, rendered source pages, corpora,
and private coordination are excluded. The frozen packet's pending-audit language
is historical; this separately bound report supplies the completed review.

## Public sources

- Valentina Kiritchenko, *Gelfand-Zetlin Polytopes and Flag Varieties*, IMRN
  2010(13), 2512-2531. DOI: https://doi.org/10.1093/imrn/rnp223.
  PDF: https://publications.hse.ru/pubs/share/folder/omll7zg0oc/66625291.pdf.
- Valentina Kiritchenko, *Flag Varieties and Gelfand-Zetlin Polytopes*, in
  *Toric Geometry*, Oberwolfach Reports 6 (2009), pp. 22-25.
  DOI: https://doi.org/10.4171/OWR/2009/01.
  Report PDF: https://ems.press/content/serial-article-files/46202?nt=1.

Reproduction: `python3 -B independent_polytope_check.py PATH/TO/certificate.json
--output independent-results.json`, with Python 3.10+ and only its standard library.
