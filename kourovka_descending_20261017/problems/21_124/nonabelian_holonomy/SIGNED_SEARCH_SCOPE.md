# Scope of the exact signed/permutation searches

These bounded calculations are supporting evidence. They do not prove an arbitrary finite-group assertion, and root's later exact positive Pell multiset defeats that assertion.

For triples of signed permutation matrices of dimension n, the horizontal equations form the 3n-by-3n integer matrix with row blocks [pi Si,-qi I,Si-I]. A solution with A=0 has B=0, by comparing the two distinct nonzero qi in the norm equations. Its T belongs to the common fixed space. Thus if that fixed space has dimension k, the maximal possible rational matrix rank is 3n-k; this rank excludes horizontal solutions.

`signed_search.js` computes the common fixed dimension using an exact integer signed graph. Each constraint is T_(sigma(j))=sign_j T_j. A connected component contributes one free coordinate exactly if its edge signs are consistent; otherwise the whole component is zero. No modular rank estimate is used for this dimension. The main matrix is screened modulo the prime65521. A modular rank equal to the maximal possible rank proves the same rational rank. Lower modular ranks are only candidates and are checked by the separate Fraction-based `check_signed_candidates.py`.

The first matrix is taken up to conjugacy in the ambient signed permutation group. Conjugacy classes are classified by the unordered list of signed cycle lengths: within each cycle, diagonal sign conjugacy moves all negative signs onto a single edge, retaining only their product. An ordinary permutation relabels cycles. The second and third matrices are unrestricted. Thus every triple is represented up to simultaneous conjugacy; repeated or nontransitive actions are included.

Results:

| Ambient action | Dimension | First classes | Tested triples | Modular candidates | Exact horizontal witnesses |
|---|---:|---:|---:|---:|---:|
|signed permutation B3|3|10|23,040|0|0|
|signed permutation B4|4|20|2,949,120|14|0|
|ordinary permutation S6|6|11|5,702,400|0|0|

B3 includes the rotational signed-standard S4 representation missing from the prior degree-five permutation search. S6 extends the prior permutation bound to degree six. Neither observation controls general irreducible dimension or arbitrary finite group order. The S6 negative result is consistent with the later positive multiset, whose expanded list has approximately9.54×10^34 entries.

Reproduce with Node.js and standard-library Python:

    node signed_search.js 3 > signed_results_3.json
    node signed_search.js 4 > signed_results_4.json
    python3 check_signed_candidates.py
    node signed_search.js 6 --unsigned > permutation_results_6.json

Elapsed seconds depend on runtime. Structural counts and exact rational conclusions are the reproducible fields. These searches have not received the separate full adversarial audit given to the dihedral theorem; they are not premises of that theorem or of the positive certificate.
