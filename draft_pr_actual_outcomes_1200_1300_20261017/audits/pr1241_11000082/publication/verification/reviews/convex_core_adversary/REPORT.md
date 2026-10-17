# Independent adversarial review of the frozen reconstruction

**Verdict: PASS.** No mathematical gap was identified in the frozen original-question reconstruction. The compact convex-core subgroup supplies a valid uniform bound on ambient conjugacy fusion; the remaining interfaces preserve the fixed genus, fixed Johnson depth, and exact common dilatation. This is a correctness review only, with no novelty or priority clearance.

The authenticated input manifest has SHA-256 `42315a3967fad4d35303871413bc5cd0ce05befd91ecd460202641618f991f9b`. All seven files listed in it matched both their byte counts and hashes. The manifest and authored inputs are checked again in `FINAL_INPUT_CHECK.json`. The reconstruction remains sealed and unchanged.

The exact reviewed claim is: for each fixed closed oriented genus g>=2 and each fixed finite k>=3, and every N>=1, I_g(k) contains N pseudo-Anosovs with one exact dilatation and pairwise distinct orientation-preserving Mod_g conjugacy classes. The common value can vary with N. Powers are included. No result for simple loops, ambient primitive classes, a single infinite-multiplicity value, or the intersection of all depths is inferred.

| Adversarial interface | Result |
|---|---|
| Outer Johnson convention and index | Verified by lifting quotient inner automorphisms, then using the automorphism centrality calculation; separating twists lie in I_g(2). |
| Genus 2 and filling pair | Source assertion confirmed; independent measured-lamination argument has no genus-2 exception. The elementary lower bound mu>=4 is sufficient and need not be sharp. |
| Matrix formulas (3.2)-(3.3) | Expanded independently as a full matrix and checked exactly in 750 general cases. q=0 gives trace 2, confirming why q!=0 matters. |
| Fixed depth | r, c, M, L and H are chosen after k is fixed and before the requested multiplicity grows. |
| Independent endpoints and high powers | Parabolic conjugation sends both old endpoints toward 0, which is excluded from the old pair. Four separated half-planes produce a genuine Schottky group with compact convex core. |
| Compact K and finite S | Cocompactness supplies JK=X; properness and discreteness make S finite. The overgroup need not be finitely generated. |
| Fixed reference point | For each u, one x in K is fixed before considering every t with tut^-1 in J. Moving tx back to K puts jt in the same finite S. |
| Uniformity and powers | No length, word length, power exponent, centralizer-size or finite-index estimate enters the bound. |
| Full ambient Mod_g conjugacy | Every conjugator preserves D by uniqueness of the disk stabilized by the resulting pseudo-Anosov. |
| Derivative kernel | Injection on H, not ambient faithfulness, identifies H and J classes. The full stabilizer's finite kernel causes no extra loss. |
| Horowitz and length conventions | Original recurrence, universal trace scope, and linear exponents verified; lift signs and the factor log(lambda)=ell/2 are consistent. |

The strongest attempted counterexample is explicit: in a rank-two Schottky group G=<a,b>, the normal kernel Q of a->0,b->1 has infinitely many Q classes b^n a b^-n inside one G class. Its noncompact core is the precise obstruction. This falsifies the version with arbitrary subgroups and confirms the necessity of the frozen proof's compactness step; it does not contradict that step.

The supplied exact verifier was run on an ignored copy; its result matches the frozen JSON byte for byte. Independent controls additionally examine general matrices, degenerate trace representations and cyclic markers through 64 words. All pass. These checks are explicitly finite consistency evidence. Complete infinite claims rest on the checked derivations in `DERIVATIONS.md` and the standard primary inputs recorded in `SOURCE_RECEIPTS.json`.

Three primary PDFs were independently retrieved, their recorded hashes reproduced, and the exact inspected page scope was logged. The PDF skill was used for read-only rendering and visual inspection. Source bodies and renders are ignored under `.evidence/`. No candidate, other review, priority/outcome material, queue, or PR content was read. No individual was contacted, no other agent was used, and no Git/index/branch/push/PR, Google Workspace or Zenodo mutation was performed. All authored output is confined to this review folder.

There are no required corrections. Optional exposition: spell out the fixed-reference-point quantifier order and the four-half-plane compactness argument in any later presentation. These are expansions of valid steps, not missing hypotheses.
