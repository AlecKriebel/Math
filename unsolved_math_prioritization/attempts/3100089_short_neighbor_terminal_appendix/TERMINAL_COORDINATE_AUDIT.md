# Independent acceptance audit: terminal black coordinates

## Verdict and exact version

**ACCEPTED, with no mathematical correction required**, for the complete five-section [terminal-coordinate manuscript](TERMINAL_COORDINATE_THEOREM.md). The distributed edition is identified in [MANIFEST.json](MANIFEST.json).

This accepts the terminal-coordinate equivalence, its constructive proof, the necessary component-separation signatures, all stated boundary qualifications, and Section 5's at-most-four-edge bridge in the auxiliary LCS-at-least-two graph. It does **not** accept or assert general connectivity, a solution of the original four-deletion/four-insertion conjecture, or novelty.

The earlier four-section version was preserved without alteration. The final version differs only by adding Section 5. Both versions were reviewed; this verdict applies to the final five-section mathematical text.

## Imported mathematics and source check

The only external mathematical result needed is pressability existence. Bixby, Flint, and Miklós, *Proving the pressing game conjecture on linear graphs*, Involve 9(1), 2016, pp. 41–56, Theorem 4 on printed p. 47, gives the required existence theorem for arbitrary bicolored graphs whose components contain black vertices. Deleting isolated white vertices supplies the exact variant used in the manuscript. The theorem's scope is not limited to linear graphs. It is distinct from the paper's connectivity result and requires no withdrawn connectivity claim.

Primary source: https://msp.org/involve/2016/9-1/involve-v9-n1-p03-s.pdf

The publisher PDF was independently retrieved and inspected through web text, local text extraction, and a visually inspected rendering of printed p. 47. It has 886,918 bytes and SHA-256 `ba3882a3bdd2688c411630a42cfa78348f0c4d8b0043124e5a0ea7b030e2b3ba`. The article's printed page range was checked through its final printed p. 56. `SOURCE_METADATA.json` records these checks. Copied source PDF/text/images are excluded from the publishable artifact.

The accepted authored foundations were read in full. Their existing public editions are the [full-state trajectory and last-support replacement lemmas](../3100089_positive_connectivity_appendix/STRUCTURAL_LEMMAS.md) and the [coordinate-rich connectivity theorem](../3100089_positive_connectivity_appendix/INTER_FIBER_LEMMAS.md#3-connectivity-when-every-norm-one-quotient-vector-is-a-vertex).

## Proof review

### Quantifiers, quotient, and easy direction

The ambient matrix is finite, symmetric, binary, and successfully pressable. The coordinate in Theorem 1 is initially black. The statement concerns every successful word **containing** that coordinate; it does not require every successful word to contain it. Initial blackness implies a nonzero row, so last-support replacement guarantees at least one containing word and removes vacuity.

The quotient is the full radical quotient, not a principal submatrix. Its coordinate images span it. The diagonal defines the linear norm functional in characteristic two; thus column equality with the full diagonal is exactly equality with the canonical vector. A successful trajectory supplies an orthonormal basis, in which the canonical vector has all coefficients one. Its last-support layer is therefore the final layer, proving that a coordinate representing it can occur only last.

Zero rows, omitted coordinates, repeated quotient representatives, and ambient rank deficiency introduce no exception. Black canonical coordinates have odd rank because the canonical norm is rank modulo two. Rank one and rank zero are correctly separated.

### Constructive converse

After the legal hypothetical press of v, the diagonal is d+c, which is nonzero precisely in the relevant noncanonical case. Its v row is zero. The union C of nontrivial white components has no cross entries to its complement O, and v belongs to O.

The crucial principal-block existence argument is sound. A nontrivial all-white component K of A[C] has b zero on K. Consequently the rank-one correction cannot alter its entries either within C or toward O. It would therefore already be an isolated nontrivial all-white component of A, contradicting successful pressability. Isolated white coordinates are harmless. The source theorem now applies to A[C].

For any successful C-word U, each corresponding full-matrix press is legal. The invariant that the cross block is diag(B) z-transpose is correct: the pivot has diagonal one, so its cross row is exactly z-transpose, and the diagonal changes by the pivot column. Each pivot toggles the O block by zz-transpose. These are full-state identities.

If U has even length, it clears C and its cross block while leaving A[O]. Pressing v then produces H[O]. If U has odd length, v is black immediately before U's final pivot. Since that final pivot clears B, B is its pivot-column outer product, and its diagonal is the pivot column. The full columns of v and the final pivot agree, so replacing that final pivot by v produces the identical full next state. This is the essential parity correction; appending v instead is generally illegal.

In either branch, H[O] retains a black coordinate and has no nontrivial all-white component. Its successful continuation exists and is nonempty. Cleared coordinates cannot be pressed again, so neither branch introduces repetitions. This proves the nonterminal occurrence with all full ambient coordinates accounted for.

### Separation signatures

For rank at least three, a fixed successful first-label class lies in one K2 component: the shared-letter diameter-two theorem applies to rank-(r−1) suffixes. A nonterminal occurrence of a successful first label a joins that first-label component using an ordered pair (a,t). The residual t after pressing a is nonzero; otherwise x_t would be zero or x_a and both letters could not occur in one successful word. This is a legitimate use of nonzero-row replacement, not an assertion that every black coordinate can be pressed first.

Last-support replacement preserves at least r−1≥2 letters. Therefore separation forces the last coefficient of a to be one. Any fixed nonempty proper prefix stays within its first-label component. When the residual a is black, Theorem 1 applies to that successfully pressable full residual matrix and forces its residual coefficients all to be one. This yields exactly the manuscript's suffix-parity implication. The initially odd norm and exclusion of the global canonical vector are justified by the existence of an a-first successful word.

Taking suffix-parity differences at the last zero gives precisely the two stated signature families. In rank six these are exactly 011111, 101111, and 100011. The claimed odd-rank inner-product restriction and even-rank canonical-sum consequence follow by comparing the first coefficient with the first trajectory vector. These are necessary restrictions only.

### Section 5's constructive bridge

If last support is not final, one replacement creates a nonterminal occurrence at a cost of at most one edge. Otherwise, a nonexceptional signature forces a proper-prefix violation of the suffix implication; the all-ones obstruction is excluded because a is a successful first label. Theorem 1 constructs a nonterminal occurrence after that prefix. Fixed-first-label suffix connectivity then costs at most two edges from T. The ordered-pair argument adds at most two edges to S. Identity steps may be removed, and every nontrivial edge retains at least two ordered common letters. The four-edge upper bound is correct. It is not a fixed-four-edit bound above rank six.

## Independent exact and constructive checks

Neither checker imports the author's checker. The C++ checker uses triangular matrix-bit encoding, legal-press recursion over all successful words, and full-state rank-one updates. The Python checker independently uses full row-bit tuples and explicit successful-word enumeration.

### Exhaustive symmetric matrices through ambient size six

Every symmetric binary matrix for n=0,1,...,6 was checked, including zero matrices, isolated coordinates, rank-deficient states, and unsuccessful states:

- Matrices: 2,131,019.
- Successfully pressable matrices: 2,069,970.
- Successful words counted exactly: 53,873,964.
- Initially black coordinate cases in pressable matrices: 6,327,279.
- Black canonical cases: 189,407.
- Noncanonical cases: 6,137,872.
- Explicit constructed-word validation runs: 12,275,744, using the lexicographically first and last successful C-words for each noncanonical case; these two choices may coincide.
- Even-U branch runs: 12,209,664; odd-U replacement runs: 66,080; C-empty runs: 11,964,120.

Every theorem equivalence, occurrence nonvacuity, legal-pivot check, cross-block invariant, parity invariant, odd-branch column equality, full residual identity, nonempty continuation, no-repeat condition, and final zero state passed. Every successful-word length agreed with independently computed binary rank. The imported existence criterion also agreed with exact recursion on every enumerated matrix.

All 31,086 K2 graphs of rank at least three through n=5 were explicitly constructed by ordered-pair incidence. Fixed-first-label membership and nonterminal-first-label membership passed. All these finite K2 graphs were connected, so their cross-component signature checks are vacuous; they are not evidence of an observed separated component.

### Independent row-matrix and bridge checks

The Python implementation independently reproduced every matrix's pressability and exact word counts through n=4. It validated 17,262 nonexceptional ordered-word-pair bridges in that exhaustive range. A further 1,000 deterministic guaranteed-pressable Gram matrices of ranks 3–12, including zero and duplicated coordinate vectors, yielded 959 eligible sampled bridges and 7,719 explicitly replayed terminal-construction witnesses. Every constructed bridge had at most four valid K2 edges; observed paths used at most three.

The binary-string classification was tested independently on every bit string in each rank 3–18. The suffix conditions matched exactly the claimed families, including precisely the three rank-six strings. This finite algebra check supplements the proof; it does not replace it.

### Negative controls

The following small mathematical counterexamples establish the necessity of hypotheses or refute stronger statements. Vertex labels are zero-based and rows are encoded as bit masks:

1. Dropping initial blackness fails: rows (6,3,1), v=2, have unique successful word (1,0,2); v is forced last but noncanonical.
2. Dropping successful pressability fails by vacuity: rows (9,4,2,1), v=0, have no successful word, while v is black and noncanonical.
3. Strengthening nonterminal to first fails: rows (15,7,3,1), v=1, have unique successful word (0,3,1,2).
4. Omitting the odd-U replacement fails: rows (23,19,9,4,3), v=1, have C-word (0,2,3); appending v after that word is illegal. The correct constructed word is (0,2,1,4).
5. An exceptional signature does not imply separation: rows (14,3,5,1) have words S=(1,0,3,2), T=(2,0,3,1), with signature 0111 for S's first letter along T. S and T are directly adjacent in K2, sharing (0,3).

The initially-white unique-word path family was also checked in ranks 2–8, including the rank-two canonical exception and noncanonical terminal coordinates for higher ranks.

## Reproducibility and limits

The C++ checker was compiled in C++17 mode with optimization, strict warnings, warnings treated as errors, and pedantic checking; its rerun output matched byte for byte. The Python checker uses explicit exceptions rather than removable assertions; normal, `-O`, and `-OO` results matched byte for byte. Artifact identity checks and mutation controls verified that altered manuscript bytes, altered results, missing files, and a self-rehashed changed verification record were rejected against its independently fixed identity.

The proof, not finite enumeration, supports the arbitrary-rank theorem. No general pressing-connectivity result, synthetic-letter removal theorem, sufficiency of the exceptional signatures, or novelty claim is established by this audit.
