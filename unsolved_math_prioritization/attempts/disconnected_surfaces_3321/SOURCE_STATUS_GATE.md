# Source and prior-work gate: disconnected drawings on surfaces

Checked 21 October 2026. Queue rank 1876; ID 3321; OPG-322. No queue edits or publication were performed.

## Exact scope

The recovered record asks whether **every** crossing-minimal drawing of a disjoint union of two graphs on a surface has no crossing between the two graphs. This is a universal statement about optimal drawings and arbitrary surfaces. It is not merely the existence of a separated optimum, nor only a torus statement. The original Garden page confirms that quantifier. Proper drawing conventions exclude edges through unrelated vertices and degenerate intersections; assumptions must be made explicit in any proof.

Primary problem page: https://garden.irmacs.sfu.ca/op/drawing_disconnected_graphs_on_surfaces

## Verified prior literature and formulation differences

1. DeVos, Mohar and Šámal, *Unexpected behaviour of crossing sequences*, arXiv:0911.0452v2, Problem 1.5 and Proposition 1.6 (printed pp. 3–4). The general published question uses **existence** of a separated optimum. The projective-plane proof obtains a strict crossing reduction from an intersecting optimum, supporting the stronger version there. https://arxiv.org/pdf/0911.0452
2. Beaudou, Gerbaud, Grappe and Palesi, *Drawing disconnected graphs on the Klein bottle*, arXiv:0810.0508v2, Theorem 2 (printed p. 3). This proves the stronger every-optimum statement for two connected graphs on the Klein bottle. Thus the old Garden comment that all surfaces except plane/projective plane are unresolved is stale. The proof uses strict reduction, not just a nonincreasing replacement. https://arxiv.org/abs/0810.0508
3. Cabello, Mohar and Šámal, *Drawing a disconnected graph on the torus (Extended abstract)* (2015), Problem 1.1 and Theorem 2.2. The paper gives a sufficient two-dimensional integer-vector inequality for the existential torus question and solves a special case; it is not a general-surface solution. https://eurocomb2015.w.uib.no/files/2015/08/endm1983.pdf
4. **Recent announcement:** Robert Šámal, joint work with Bojan Mohar, *Drawing a Disconnected Graph on the Torus with Help from Minkowski*, SCMS conference, 26 September 2026. Handbook printed p. 19 (PDF index 18) announces the exact torus crossing-number equality and hence an optimum with one graph in a disk. It describes a lattice/zonotope proof using mixed areas, successive minima and polar bodies. This is primary evidence of an announced solution to the **existential torus version**, not a full manuscript proof audit and not evidence that every optimum is separated. No full proof of that new announcement was located in this pass. https://scmscomb.github.io/assets/Conference_Handbook.pdf ; https://scmscomb.github.io/conference

## Gate outcome

**OPEN / QUALIFIED PRIOR-WORK GATE, not solved.** No full solution or counterexample to the exact arbitrary-surface, every-optimum formulation was verified. A fresh torus announcement materially changes the prior-work baseline. Do not label a new proof of torus existence or the old lattice inequality novel without checking that work. Do not upgrade the conference abstract into a peer-reviewed or independently verified theorem. Preserve the quantifier distinction throughout.

The full corpus contains 15,458 problem records and 6,701 research-result entries. The exact statement has only one match (ID 3321); the exact OPG-322 research-result key is absent. Keyword screening for disconnected/disjoint drawings on surfaces returned no other relevant problem record. This is a bounded corpus duplicate check, not proof of uniqueness across all mathematical literature. Dataset byte counts and hashes are in RECOVERY_METADATA.json.

## Required acceptance targets for future research

- For the original question: any claimed counterexample must certify optimality and exhibit a crossing between distinct components; a mere crossing drawing does not suffice.
- Any positive solution must exclude **all** intersecting optima, normally by a strict improvement argument. Nonincreasing separation establishes only existence.
- The plane, projective plane and Klein bottle are known territory. The torus existence question now has a September 2026 primary announcement. Higher surfaces and the universal-optimum distinction remain the relevant unverified scope.
- Source documents and verbatim recovered record remain private. Public artifacts contain authored analysis and verification metadata only.
