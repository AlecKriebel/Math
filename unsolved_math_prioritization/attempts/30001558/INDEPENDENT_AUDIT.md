# Mathematical audit of the candidate counterexample

## Artifact binding and verdict

Audited artifact: `RESULT.md`.

SHA256: `28d6abc59e213d42375ac5b48d61f05e4b8607beeb53d7bc96ba34cc2330669a`.

Verdict: **PASS for the stated partial result.** The specified first-gap-deleted Thue–Morse candidate admits a nontrivial two-coordinate modification preserving squarefreeness. The proof does not settle existence or nonexistence of any fragile infinite ternary squarefree word. This audit does not certify novelty or exhaustive literature coverage.

## Source identity and exact target

The inspected primary source is Jeffrey Shallit's contribution to *Mini-Workshop: Combinatorics on Words*, Oberwolfach Reports 7 (2010), printed pages 2232–2233, Problem 39. DOI: https://doi.org/10.4171/OWR/2010/37 . Primary PDF: https://ems.press/content/serial-article-files/46296 .

The source specifies gaps of ones between successive zeros of the binary Thue–Morse word beginning 01101001, followed by deletion of the first gap. This is exactly the convention used in the audited artifact. The separately solved robustness question is not the target.

The inspected PDF has 463460 bytes and SHA256 `e88f211c5be990a68a967f3a9549f5db042279e8473e2cb126ea1e3caaebf98c`; both values were recomputed and agree with the source metadata.

## Symbolic checks

1. A square AA in the gap word produces E(A)E(A)0 in the binary word, where E(a)=01^a. Writing E(A)=0u makes this an overlap 0u0u0. The following zero exists because the word is infinite. Classical binary Thue–Morse overlapfreeness therefore proves the gap word squarefree.

2. Applying the binary substitution to each block E(a), with the next block's initial zero closing the last gap, gives h(0)=1, h(1)=20, h(2)=210. These gap lists concatenate without omissions or duplicate gaps, so the fixed-point identity g=h(g) is justified.

3. In an h-image, every occurrence of 1 either lies inside 210, with neighbors 2 and 0, or is the whole image h(0). For a singleton, any preceding block ends in 0 or 1 and any following block begins in 1 or 2. Consequently 010 and 212 are impossible. At the left endpoint the absence of a preceding symbol cannot create an extra occurrence of either triple.

4. In a proposed occurrence 1201, its first 1 cannot be the internal 1 of 210, since it is followed by 2. It is therefore h(0). The following 20 is exactly h(1), since h(2) begins 21. The final 1 begins a block and must be h(0), because no other image starts with 1. Thus 1201 in h(g) forces 010 in g, a contradiction.

5. For x=1g[3:]=120121..., every square not starting at zero is already in a suffix of g. A square starting at zero with period at least 4 repeats 1201 at a positive position, also inside g. The remaining comparisons are: period 1 compares 1 with 2; period 2 compares 12 with 01; period 3 compares 120 with 121. All fail.

6. For v=2x=212012..., every square not starting at zero is already in x. A square at zero with period at least 3 repeats 212 at a position at least 3, hence inside g[3:]. The remaining comparisons are: period 1 compares 2 with 1; period 2 compares 21 with 20. All fail. The report's extra check of the triple at position 1 is correct but not required for these periods.

7. The original word is w=10g[3:] and the modified word is v=21g[3:]. They differ at exactly positions 0 and 1. No insertion, deletion, reindexing, or alphabet permutation is being substituted for the required finite coordinate changes.

8. The stated finite-certificate characterization is valid. For a fixed prefix length n there are finitely many alternative prefixes. If each alternative concatenated with the unchanged infinite tail fails squarefreeness, each has a finite square witness. Taking the maximum endpoint of these witnesses gives a single finite certificate. Requiring this for every n is equivalent to arbitrary-finite-change fragility, not merely single-coordinate delicacy.

## Independent computational checks

A fresh exhaustive implementation generated squarefree words by checking all suffix squares after each one-letter extension. It reproduced all listed length-24, length-28, and length-32 totals and singleton-group counts:

- Length 24: 7032 words; counts 3372, 1500, 282, 96, 12, 0.
- Length 28: 20220 words; counts 9696, 4260, 816, 306, 54, 0.
- Length 32: 58446 words; counts 28074, 12492, 2424, 906, 144, 6.

The six length-32 singleton representatives are exactly the alphabet permutations stated in the report. Each has exactly one length-33 squarefree continuation and no length-34 squarefree continuation.

A separate backward-prefix computation using 512 unchanged tail symbols reproduced counts 2, 4, 10, and 35 for cuts 2, 5, 8, and 12, respectively. At cut 2 the prefixes are exactly 10 and 21. These are finite checks, not the basis of the infinite proof.

The encoding obstruction is also exact: E(212)0=011010110 contains 10101 at zero-based positions 2 through 6. Consequently squarefree gap inputs need not encode overlapfree binary words. The candidate modification additionally changes the total gap sum by 2, so a binary same-index finite-flip theorem is inapplicable without another argument.

## Scope and limitations

The exact proof validates a counterexample to the suggested construction only. It does not validate a proof of the original existence problem, an impossibility theorem, or an assertion of globally current openness. The bounded computational exploration does not exhaust infinite continuations beyond the explicit dead-end witnesses. No source text is reproduced in this audit.
