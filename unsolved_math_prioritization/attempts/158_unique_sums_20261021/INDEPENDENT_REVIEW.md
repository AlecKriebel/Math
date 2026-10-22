# Independent adversarial review

Reviewed 2026-10-21 UTC. Verdict: the finite-search and lattice certificates listed below pass the stated checks. This does not resolve the residual asymptotic lower-bound question or establish any unverified external theorem.

## Definition and completeness checks

The specified minimum is over subsets of size at least two of the odd-prime cyclic group. A singleton fails at its double, so using nonempty subsets would give the same minimum. Allowing the empty set would instead make the minimum zero by vacuity. For odd p, at most one diagonal pair contributes to any sum. If U(s) counts unordered multiset representations and D(s) is its diagonal indicator, the ordered count is R(s)=2U(s)-D(s). Thus U(s)=1 is equivalent to R(s) in {1,2}; the independent checker rejects BOTH values. Merely rejecting ordered count one would be incorrect. Unrepresented sums are allowed.

For any A with at least two distinct elements a,b, x -> (x-a)/(b-a) is a bijection modulo prime p taking them to 0,1. It bijects unordered multiset representations and sends a sum s to (s-2a)/(b-a). Every affine class therefore has a candidate containing 0,1. Enumerating every (n-2)-subset of {2,...,p-1} is complete, although not duplicate-free by affine class. The two recursive C++ enumerators' terminal bounds include every such subset once. No minimality claim relies on enumeration after the first successful candidate at the minimum size.

Capacity pruning is valid: n(n+1)/2 unordered pairs and at least two per represented sum imply |A+A| <= floor(n(n+1)/4). Cauchy-Davenport implies |A+A| >= min(p,2n-1). The strict comparison in exact_search.py is precisely the resulting obstruction. The independent exhaustive search DOES NOT USE this pruning; it checks even these excluded sizes (and separately the singleton).

## Exact reruns and independent ordered search

Original Python scripts were copied to a temporary directory and executed without altering the reviewed result files. Every JSON field in exact_results.json matches the rerun except the intentionally variable seconds field. lattice_results.json matches its rerun exactly as parsed JSON.

An independently written C++ checker (independent_ordered.cpp) uses ordered double loops rather than upper-triangular unordered loops. It exhausts every normalized candidate at each size below the minimum, with no capacity pruning, and stops at the first success at the minimum. Its complete output is independent_ordered_results.txt. Every smaller-size candidate count equals binomial(p-2,n-2), every first-success position and witness equals the supplied results, and direct ordered-to-unordered count conversion reproduces all supplied witness counts.

Verified (p,minimum): (3,3), (5,4), (7,5), (11,7), (13,7), (17,8), (19,9), (23,10), (29,11), (31,11).

For the largest cases, complete unsuccessful counts at n=7,8,9,10 are respectively:

- p=29: 80,730; 296,010; 888,030; 2,220,075. First n=11 success at candidate 4,977.
- p=31: 118,755; 475,020; 1,560,780; 4,292,145. First n=11 success at candidate 64,701.

## Seven-point extension

Compiled and reran seven_point_check.cpp; its text output matches seven_point_results.txt byte-for-byte. An independent ordered implementation, independent_seven.cpp, also returns NONE at n=7 for every prime 17 through 61. Each count equals binomial(p-2,5):

17: 3,003; 19: 6,188; 23: 20,349; 29: 80,730; 31: 118,755; 37: 324,632; 41: 575,757; 43: 749,398; 47: 1,221,759; 53: 2,349,060; 59: 4,187,106; 61: 5,006,386.

Together with the balanced-set determinant bound p <= 2^(n-1), this covers every possible p for n=7, since the remaining primes p>=67 exceed 64. Capacity excludes n=2,...,6 for all p>=17, and singletons fail. The self-contained proof of this bound in REPORT.md was subsequently reviewed and passes (details below), so the computer-assisted global conclusion m(p)>=8 for every prime p>=17 passes this review. The computation alone would not have established the bound. The independent seven-point output includes a redundant singleton sanity line for each prime; this does not change its n=7 exhaustive test.

## Lattice checks using a different normal form

lattice_check.py constructs star differences within each equal-sum fiber and deletes the last coordinate. Star differences generate every difference in that fiber. Every full relation vector has coordinate sum zero, so deleting any one coordinate is an integral isomorphism from that ambient sum-zero lattice to Z^(n-1), not a lossy rational projection.

The independent_lattice.py checker instead constructs ALL pairwise differences in each equal-sum fiber, deletes the FIRST coordinate, and computes column Hermite normal form of the transposed generator matrix. This independently checks the lattice and uses a different normal-form algorithm from the original Smith computation. For every witness its HNF is square of dimension n-1 with absolute determinant p. A finite abelian group of prime order p is cyclic, so the Smith invariant factors must be n-2 copies of 1 followed by p, exactly as reported. Original row counts also match the rerun. The independent HNF computation still uses SymPy, so it is not an independent arithmetic-library verification.

## Weak-quaternary transfer counterexample

Modulo 13, C={0,1,4} has a nonconstant four-term representation of 4x for every x in C:

- x=0: 1+4+4+4=13=4*0 (mod 13).
- x=1: 0+0+0+4=4=4*1 (mod 13).
- x=4: 0+1+1+1=3=4*4 (mod 13).

Nevertheless B=C+C={0,1,2,4,5,8} is not NUS: its sums 1,7,12 have exactly the single unordered representations {0,1}, {2,5}, {4,8}, respectively. This disproves the general claim that the stated weak-quaternary condition makes C+C NUS. It does not disprove a stronger construction with additional hypotheses.

## Limits

These are exact bounded computations plus the explicitly proved small-cardinality global corollary, not a solution of the residual asymptotic question. Affine normalization uses primality; no claim is made for composite moduli or p=2. The minimum-size convention must exclude the empty set. The original timing values were not reproduced and are not mathematical evidence. No claim is made that every minimum witness, or every possible collision lattice, was enumerated. This review does not certify outside scholarly sources or publication status.

## SHA-256 bindings

- exact_search.py: da636b0b410e1d3e144242dc4d2db448baa09976a6a6a6514da39f11a61d611a (955 bytes).
- exact_results.json: 607796b4bb06fa61ea9006f3e6a32d6ad7042b030d4af2cdb08cd3c65c5cd318 (8922 bytes).
- lattice_check.py: 51a71428f39235a27d39653012eab5c9dd0283985d29ed2f8d4bebfd3e725e7c (819 bytes).
- lattice_results.json: 1b4d011d40e22fb44150b761239b13990dd3b39fed5b7617d1778d600fb7bbb2 (1441 bytes).
- seven_point_check.cpp: fc1f5f2d06e025c5c79a8616606c148fdd95b37c453ad1b17ac4c0c890d344cc (629 bytes).
- seven_point_results.txt: 09af92d09975199d4820ea18cf43b964ac8496ab6ca986f3f67bf41bf5ffe13b (178 bytes).
- independent_ordered.cpp: 4b1892c9911e8c17c5f5c2a96392353f37279d88c7c66c5d8a1617a2897044e0 (844 bytes).
- independent_ordered_results.txt: 1a1e2e7811c58210c33326788cd5124fea385883bfb52e9f47c7b49d47cb2977 (2636 bytes).
- independent_seven.cpp: 3447de0a9fb6d9167156a21d53593bdc3b3154c66d09867d90de0fefef86e836 (853 bytes).
- independent_seven_results.txt: 5e591cf1941ec6e48a69125aadb5ecb9aa40e7bf5f03a6ccdd8feb44fef78538 (778 bytes).
- independent_lattice.py: 1a21884537a4030362d8b5f59c0094b704c71505a2334f683494919bef41846a (1450 bytes).
- independent_lattice_results.json: 857830c81a4c10b25d6778b95b1d7043577fff237bfc548bdcae4c85021889e1 (3289 bytes).

## Authored REPORT.md mathematical audit

The reviewed REPORT.md hash is listed below. Its five attempts are explicitly bounded investigations, not five successful solutions. It consistently marks the asymptotic question open, distinguishes finite conclusions from the source compression discussion, and disclaims novelty. No substantive error was found in the following authored arguments:

1. Energy and Fourier: r^2>=4r-3 on the n diagonal residues follows from odd r>=3; r^2>=4r elsewhere follows from r=0 or r>=4. Summing gives E>=4n^2-3n. Unnormalized Fourier orthogonality gives sum|Ahat|^4=pE and the zero mode n^4. Nonzero Parseval mass is pn-n^2, so division by this positive quantity for n<p gives exactly the asserted maximum-coefficient lower bound. The asymptotic comment describes scale only, not a universal optimality theorem for energy methods.
2. Rectification and determinant: in an interval of diameter at most (p-1)/2, translating its least point to zero leaves all ordinary pair sums between 0 and p-1, so only the least point twice represents zero. NUS implies a distinct midpoint repair at every point because a diagonal alternative cannot repeat that point or have two equal entries. In an inclusion-minimal nonempty balanced subset, the maximum level of any rational kernel vector is closed under its selected repairs; it is therefore itself balanced and must be the whole subset. This proves rank k-1. After anchoring, the modular label-difference vector is nonzero and is killed by the selected square integer matrix, so p divides its nonzero determinant. Each of the 2^(k-1) multilinear terms is an anchored directed-incidence minor, of determinant 0 or +/-1. Expansion along a row with at most one nonzero, or zero row sum when every row retains both entries, proves this recursively. Therefore p<=2^(k-1)<=2^(n-1), with the precise exponent claimed. The uniform eight-point corollary is consequently justified, not conditional on an unaudited external lemma.
3. Compression discussion: given its explicitly conditional dimension and height hypotheses, the Hadamard estimate and the example q(e_1-e_2) are correct. I did not verify that the cited manuscript really establishes those hypotheses or inspect its forest recurrence; those source-dependent statements are outside this review. No unsupported compression theorem is needed for the certified finite or global conclusions.
4. The quaternary counterexample and its full 13-entry unordered count vector were independently checked, not only the three failing sums. The discussion of the known ternary mechanism is background and was not independently source-audited here.
5. Exact minima, the seven-point exclusion, and all displayed collision quotient orders pass the computational checks above. The additional full-rank statement for a minimum NUS witness is also valid: for any rational vector annihilating all collision rows, pairs from its maximal-level subset can only collide with other pairs in that subset. Thus that nonempty subset is itself NUS. Minimum cardinality forces it to be all of A, hence the kernel consists of constants and full rational rank is n-1.

Public-source titles, publication dates, literature-status claims, and the asserted manuscript compression/height recurrence were not independently audited in this review. This limitation does not affect the elementary calculations and finite certificates explicitly checked above. No publication or QUEUE changes were made by this reviewer.

- REPORT.md: 7e8bade56450160c0c24256e0b3b3d4879848a90e25d777e1bcfca56df268141 (10051 bytes).

## Ordered-checker regression

Independently recomputed p=11, A={0,1,2,4,7}: ordered counts are [3,2,3,3,3,2,2,2,3,2,0]. There is no ordered count one, but sums 1,5,6,7,9 have ordered count two and therefore exactly one unordered representation. This confirms that the flawed r!=1 test accepts a non-NUS set and the corrected checker must reject both 1 and 2.

- checker_regression.json: 808714d38a46cecc28bc06c779f677af454f8c8c4e12edac1b3e77aa6453538b (357 bytes).
