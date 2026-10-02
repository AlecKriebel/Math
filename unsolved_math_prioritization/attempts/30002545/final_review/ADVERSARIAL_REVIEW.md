# Independent full source/method review: 30002545

2026-10-02. **PASS for a complete credited combinatorial proof presentation after one author turn.** Recommended category already_solved1/5 as a literature-derived proof of the known result; no new theorem or historical-priority claim. The requested method is met by the supplied static-bijection/symmetry argument. No mandatory mathematical correction.

## Source and method

The complete OWR question was independently retrieved from the official report. It samples labelled decreasing rooted plane trees and then a uniform vertex, and asks for a combinatorial proof without generating functions, induction or assuming convergence. Its printed total-leaf formula is inconsistent; the proof correctly does not use it. The relevant primary Janson contour description and Janson–Kuba–Panholzer Theorems1–2 were checked in local full text. These establish the credited correspondences. The unavailable full corrigendum remains an access limitation, not a claim of a fully audited source. The final numerical formula was already known.

The written proof does not use a recurrence or induction to infer enumeration, nor assume a limit. It describes finite inverses by interval containment and reads their entry/exit order directly. These are combinatorial finite constructions; recursive traversal code used for checking is not an inductive proof of the asserted probability. The use of two known bijections does not prevent compliance with the mathematical method requested. The aesthetic word 'simple' has no objective formal threshold, but the actual argument reduces to two explicit maps and equal totals of three slot types.

## Bijection audit

Reversing labels makes root0 and preserves the uniform finite class and leaves. In the plane contour, pair intervals are laminar because any crossing would force opposite strict inequalities of labels. Minimal containing intervals give parents and ordered disjoint intervals give siblings. The entry/exit events recover precisely the word and tree. Leaves correspond to adjacent equal letters; the root exception at size1 is handled separately.

For the ternary inverse, the maximal component of entries at least i containing its pair exists and includes both copies of every contained label. Otherwise a pair would cross a smaller boundary entry, violating the defining condition. Components for distinct thresholds are nested or disjoint and distinct. Each of the three gaps cut by the pair of i is exactly the component of its minimum label when nonempty. This proves there are at most three immediate children in the assigned slots. Conversely a subtree contour is maximal for its threshold because its outside neighbors, when present, are strict-ancestor labels. The two maps are inverse at every finite size. A plateau means exactly an empty middle slot.

The global cyclic slot permutation is a bijection preserving increasing labels; it need not act freely. Every m-vertex ternary tree has3m slots and m−1 occupied slots. Summing and rotating shows the average empty-middle count is(2m+1)/3. With m=n−1 and the uniform vertex choice, the exact probability is(2n−1)/(3n) for n≥2. Therefore the limit exists and equals2/3. The single-vertex case has probability1.

## Exact checks and integrity

All13 final-manifest entries and manifest SHA256691f380104d4e965fce9c14c5f180a9cc2cee96372c538ac5f1620270e6e29a4 were verified. The author replay is byte-identical:3,346,451 assertions across146,599 objects through n=8. A separately written checker enumerates all multiset words through Stirling order5, filters the defining condition, reconstructs both interval trees without importing author code, verifies contour inversion, leaf/plateau/slot equality and global slot-rotation totals. It passes9,483 exact assertions on1,069 valid objects. These finite checks supplement the explicit all-size bijections.

Publish the result as a credited method-compliant reconstruction. Do not describe the limit, exact mean or classical bijections as newly discovered; do not let the printed typo become the claimed research outcome. Source PDFs/raw records remain local.
