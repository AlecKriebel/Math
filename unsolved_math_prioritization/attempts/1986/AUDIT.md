# Independent audit: integer progression permutations, EP195 / 1986

This is an AI-assisted, unrefereed research edition. The independent check described here is an internal AI audit, not external human peer review or formal proof-assistant certification. Source results retain their named attribution. No novelty claim is made. This prose-and-metadata edition is not a computational reproduction package: code, raw result files, copied source documents, source text, and images are not distributed. Historical execution and inspection statements describe the authenticated research and audit records; no mathematical code or formalization was rerun during publication preparation. Hashes authenticate bytes, not mathematical truth. The complete written mathematics is retained below, with the single safe-prefix orientation correction disclosed in ACCEPTANCE.md and nonmathematical publication edits.

## Verdict and scope

**Accepted as partial mathematical research, with one required wording correction. No solution of the all-integer four-term question is established.**

The audited target is a bijection p: N0 -> Z. A forbidden k-term arithmetic progression is a subsequence at increasing indices whose values are a, a+d, ..., a+(k-1)d, where d is any nonzero integer. Negative differences count. The indices need not be consecutive. Neither an arbitrary linear order on Z nor a Z-indexed doubly infinite permutation is interchangeable with this target.

The known forced threshold under this convention is 3 or 4: every such enumeration contains a three-term progression, whereas a known enumeration avoids five-term progressions. The inspected September 2026 result resolves the analogous four-term avoidance question on N0 and N, not the present all-integer question.

The audit independently checks the written deductions, reconstructs the two source constructions, and reproduces the reported finite numerical findings with a separately written checker. It does not run candidate scripts, source-author code, Lean, or build systems. It makes no novelty claim. Publication status is separate from mathematical validity; the Ho manuscript is an arXiv preprint, and the later repository proof is not treated as a certified formalization.

The sole correction is the orientation of a finite safe list in the first paragraph of candidate REPORT section 3. Its unqualified phrase “A reverse-binary finite listing is safe” is ambiguous and false if it means listing in the same fixed reverse-binary order as the tail. The correct claim is:

> A finite set listed in the reverse of Ho's fixed tail order is a safe word.

For example, the fixed tail order puts 1 before 2 and 3 before 4. Thus the same-orientation prefix (1,2), followed by that tail on N0, contains (1,2,3,4). The opposite list (2,1) is safe. Candidate section 2 already states the correct two-opposite-orders lemma, so this wording issue does not invalidate the later arguments. The audit supplied a patch while leaving the authenticated original unchanged. That exact patch has now been applied only to the publication working copy used for PROOF.md. ACCEPTANCE.md records the exact changed sentence and original/corrected identities.

## 1. Input authentication and source provenance

The candidate MANIFEST.json has SHA-256

7490b3084d598fb2a7f1c48b58e25406acf950cd653391db303f0d5421409f0d.

All 22 recorded members match both byte counts and SHA-256 values. The audited target uses the one-sided convention of the primary literature, fixed explicitly above. A secondary web search result used an explicitly doubly infinite interpretation; that separate interpretation is not substituted for this target. Public source identities and inspection limits are recorded in SOURCES.json.

The following are source results, not new deductions of this packet:

1. Sarosh Adenwalla, *Avoiding Monotone Arithmetic Progressions in Permutations of Integers*, arXiv:2211.04451v7, 23 July 2024; published in *Discrete Mathematics* 347 (2024), 114183. Theorem 1 constructs a five-term-avoiding one-sided enumeration of all Z. Theorem 2 concerns a different, doubly infinite target. The audit read the introduction and the complete Theorem 1 proof on PDF pages 3-5, and visually inspected those three pages. The full 16-page article was not audited. Sources: https://arxiv.org/abs/2211.04451v7 and https://doi.org/10.1016/j.disc.2024.114183.
2. Jesse Geneson, *Density bounds for permutations avoiding monotone arithmetic progressions*, arXiv:2608.12604v1, 12 August 2026. Its Corollary 1.3 is explicitly a supremum assertion. Theorem 1.2 supplies sets whose lower symmetric densities approach one; it does not supply density exactly one or an enumeration of all integers. The audit inspected definitions, statements, binary-order lemmas, and the section 5 construction and proof, with the density quantifier checked directly. No audit of the unrelated three-term density arguments is claimed. Source: https://arxiv.org/abs/2608.12604v1.
3. Boon Suan Ho, *A 4AP-free permutation of the positive integers*, arXiv:2609.12780v1, 11 September 2026. The complete five-page written manuscript was read, including its definition, both lemmas, algorithm description, exhaustion, references, and formalization claim. PDF pages 2-4 were also visually inspected. The mathematical proof is reconstructed below. Its stored PDF is 404497 bytes, SHA-256 42f3878948d2e26c5085cd36c2eb585174ba2ea85ee06cb87c1f9e29ce1e090b. Source: https://arxiv.org/abs/2609.12780v1. The linked https://github.com/boonsuan/4ap is a source-author formalization claim; no build certification is inferred.
4. The complete human proof at https://github.com/coleski/erdos196/blob/main/FINAL-HUMAN-PROOF.md was inspected. It is dated 14 September 2026, explicitly acknowledges Ho's earlier result, uses adaptive binary-tree witnesses, and proves the same N0 result. Its source-to-Lean correspondence is a repository claim, not an independently checked theorem certificate.
5. Geneson's 2018 manuscript, https://arxiv.org/abs/1803.06334, is retained only as historical context for the older six-term bound. No independent audit of that superseded construction is claimed.

The current arXiv metadata for the three numbered arXiv versions above was checked on 11 October 2026. The source PDFs were inspected from authenticated local snapshots, rather than silently treated as freshly downloaded PDFs. A bounded fresh search found no all-integer resolution. Direct access to the maintained EP195 tracker failed. Neither an inaccessible tracker nor a negative bounded search proves current global literature completeness.

The snapshot's retrieval and earlier-run history are authenticated records of what it reports. This audit does not independently certify that earlier normal/-O/-OO runs occurred. Instead, it performs its own three optimization-mode runs with new code and records their identical results.

## 2. Binary orders: the shared elementary mechanism

For each node of the binary residue tree, choose which of its two child residues comes first. Two unequal integers, including negative integers, differ at a least binary digit; their lower-digit common prefix determines a node, whose choice decides their comparison. The induced order is total and transitive. For transitivity, refine to a depth that separates any given finite triple; their comparisons are exactly those of a finite ordered tree. Thus there is no reliance on negative integers having finite unsigned binary expansions.

Let d != 0 and let j be the exponent of 2 dividing d. Consecutive terms of an arithmetic progression have identical digits below j and alternating digits at j. Therefore the middle of a three-term progression is on one side of both endpoints in every such order. This excludes both numerically increasing and decreasing three-term progressions.

For four terms a,b,c,e in progression, a and c have the same digit at j, as do b and e. All four use the same node. Consequently

a precedes b if and only if c precedes e.

Reversing every child preference reverses the total order. If a finite set is listed in an order T and its complement follows in the reverse of T, a four-term progression would have exactly two terms in each part: three terms within either part are impossible. The first pair must be increasing in T, while the last must be decreasing in T, contradicting the pair identity. This proves the two-order completion lemma on Z or N0.

It does not prove an omega-enumeration exists: an arbitrary tree order can give an element infinitely many predecessors. Finite avoidance and omega-enumerability are distinct issues throughout this audit.

## 3. Complete reconstruction of Ho's N0 proof

This section verifies a source theorem. It is not an authored solution of EP195.

Fix the tree order T that prefers digit 1 at every node. Its odd elements precede its even elements, and after normalizing either parity the induced order is again T. On N0 its greatest element is 0. Given a finite word P, let C(P) be P followed by its unused nonnegative integers in T order. Call P safe if C(P) avoids four-term progressions.

The two-order lemma shows that listing any finite set in reverse T order is safe. The extension statement is: for every safe P and finite target F subset N0, some finite safe Q begins with P and includes F.

Prove this by strong induction on m=max(P), with m=0 for the empty word. If m=0, P is empty or (0). List P union F in reverse T order; 0 comes first when required. For m>0, restrict P to evens and odds and normalize by x/2 and (x-1)/2. Both resulting words are safe because restricting C(P) and normalizing gives precisely their completions. Their old maxima, including the empty-child convention 0, are at most floor(m/2)<m.

First extend the even child to contain every even target. Let E be its newly added entries after rescaling and set h=max(E), or h=0 if E is empty. Next extend the odd child to include every odd target and every normalized nonnegative integer below h. Let O be the new odd entries. Every odd integer at most 2h is now in P or O. Form Q=P;O;E. Its parity projections have safe completions by construction, and Q has distinct entries, preserves P, and covers F.

The completed order is

P ; O ; E ; unused odds ; unused evens.

For an even x and odd y outside P with y<=2x, y precedes x in this order. If x belongs to E, x<=h and the forced buffer contains y. If x is unused, it lies in the final block, after every odd integer.

Suppose a,b,c,e form a four-term progression in C(Q). If the difference is even, the safe parity completion excludes it. Otherwise the parities alternate. The third term c cannot be in P: if it were, the first three terms would be in P and the fourth would still follow them in C(P), violating old safety. Thus c,e are outside P.

If c is even, e is odd and e=2c-b<=2c because b>=0. The preceding buffer property forces e before c, a contradiction. If c is odd, b is even. In this case b cannot lie in P, since then a,b would be old and c,e would occur in old odd-before-even tail order, again violating old safety. Therefore b,c are outside P. Now c=2b-a<=2b because a>=0, so the buffer property forces c before b. This is also impossible. The extension is safe.

The induction is well founded despite arbitrarily large new targets: its parameter is the largest old prefix value, not the size of an output or target. Starting with the empty word and successively requiring 0,1,2,... yields finite nested words with lengths tending to infinity. Every position eventually exists and then stays fixed; every nonnegative integer appears exactly once. Any forbidden progression would be contained in one finite stage, contradicting safety. Adding one to every value gives the result on N.

Both signed differences were handled throughout. The uses of a,b>=0 are essential to this particular parity-buffer argument. Replacing N0 by Z removes those inequalities and does not preserve the proof. The later adaptive-tree repository proof has the same signed/nonnegative boundary: its parity merge relies on a nonnegative earlier term in the identities e=2c-b and c=2b-a. Its singleton base, induction on the old maximum, flexible child witnesses, and stable finite-prefix limit are valid on N0. The child witnesses need not themselves converge.

## 4. Audited new deductions about the attempted Z transfer

The claims in this section are deductions in the research packet, not statements asserted by Ho. Their validity is proved independently here; no novelty or priority is claimed.

### 4.1 Fixed reverse-binary completion cannot be exhausted

Continue T, the digit-1-preferred order, to all integers using their residues modulo powers of two. Suppose there were nested finite safe words exhausting Z, with the unused tail always in T order. In their omega-union, only finitely many values precede -1. Choose a later positive value larger than all of them and take a stage containing it. Its maximum M occurs after -1 and is nonnegative. Both 2M+1 and 3M+2 are outside that stage.

Set t=M+1 and j=v2(t). The two tail values 2t-1 and 3t-1 agree below j; their digits at j are respectively 1 and 0. Hence 2M+1 precedes 3M+2 in T. The completion therefore contains

-1, M, 2M+1, 3M+2,

a four-term progression of positive difference M+1. This contradiction proves the fixed-invariant obstruction.

In particular (-1) itself is safe, since the tail is three-term-free, but no finite safe extension beginning with -1 can contain a nonnegative value. This is a failure of a specified extension invariant, not a universal four-term forcing proof. Adaptive tails are outside this obstruction.

### 4.2 Exact signed parity-splice residual

Let the old prefix P have a four-term-free completion whose tail puts parity A before parity B. Let U be new A values and V new B values. Consider

P ; U ; V ; A tail ; B tail.

Assume distinctness, four-term avoidance of each completed parity restriction, and unchanged A-before-B root preference in the old completion. Put M=max(0,|p|:p in P) and H=max(0,|v|:v in V). Assume every A value of absolute value at most 2H+M belongs to P union U.

Then the new completion avoids four-term progressions exactly when, for each u in U and v in V,

2v-u belongs to P union U, or 3v-2u belongs to P union V.  (R)

To prove this, even differences are excluded by the parity assumptions. An odd-difference progression a,b,c,e alternates parity; its old entries form an initial segment. Three or four old entries would already violate the old completion. With exactly two old entries, the pattern ABAB would also already violate old safety. In the remaining BABA pattern, c must lie in V and e in the A tail; but |e|=|2c-b|<=2H+M, contrary to the buffer.

With at most one old entry and pattern BABA, the chronology forces b in U, c in V, e in the A tail, and a in P. Thus |e|=|(3c-a)/2|<=(3H+M)/2<=2H+M, again impossible. With at most one old entry and pattern ABAB, chronology forces b in V, c in the A tail, and e in the B tail. If a were old, |c|=|2b-a|<=2H+M would be impossible; hence a lies in U. This is precisely the failure of (R). Conversely, if (R) fails, u,v,2v-u,3v-2u occupy the four successive new/tail blocks and form a nonconstant progression. The difference is odd and therefore nonzero.

In this residual case, |c|>2H+M. The relation a=2b-c then gives a and c opposite signs, while e=2c-b has the sign of c. This identifies the actual cross-sign difficulty. It is not an unspecified failure of a bound.

For a smallest illustration, take P empty, A odd, U=(1), B even, V=(0), and reverse-binary tails. Both normalized parity completions have a singleton prefix and are safe; the required buffer is empty. Nevertheless (1,0,-1,-2) occurs. On N0 the same finite prefix is safe. The change of domain matters.

### 4.3 A symmetric buffer is structurally incompatible with the residual

Suppose V has at least two values and the stronger buffer covers every A value of absolute value at most K=2H+M+2. Let u_- and u_+ be the extrema of U, and v_-<v_+ the extrema of V. Parity spacing supplies buffer A values at most -2H-M-1 and at least 2H+M+1. Their absolute values exceed M, so they belong to U. Thus

u_-<=-2H-M-1 and u_+>=2H+M+1.

For (u_-,v_+), the fourth value 3v_+-2u_- exceeds both H and M, and the third value 2v_+-u_- exceeds M. Consequently (R) would force 2v_+-u_- into U, implying u_-+u_+>=2v_+. Symmetrically, for (u_+,v_-), the fourth value lies below both -H and -M and the third lies below -M. Therefore (R) would force 2v_--u_+ into U, giving u_-+u_+<=2v_-. This contradicts v_-<v_+.

The argument is independent of within-parity ordering. It rules out this finite symmetric-buffer merge with two new B values, not all conceivable binary-tree or nonbinary constructions.

## 5. Packet deductions: finite-prefix certificates and their exact limitations

Let P be a prospective finite initial word with support S. It must itself avoid four-term progressions. An ordered three-term progression a,b,c in P must have its continuation 2c-b already in S and earlier than c; otherwise that continuation occurs later and creates four terms. For an ordered pair a,b in P with c=2b-a and e=3b-2a both outside S, the future must put e before c. These demands form a finite directed graph. A directed cycle is an impossibility certificate.

For P=(-2,-1,3,2), the prefix has no three-term progression. Its pairs (-2,-1) and (3,2) respectively demand 1 before 0 and 0 before 1. Thus the prefix is dead. A two-cycle on missing x,y necessarily comes from prefix pairs (3x-2y,2x-y) and (3y-2x,2y-x). Writing y=x+t gives six distinct values x-2t,x-t,x,x+t,x+2t,x+3t; four of them must already be in the prefix. This validates the stated six-term geometry and four-entry lower bound.

For P=(-2,-3,-1,9,6), again there is no three-term progression. Pairs (-2,-1), (-3,-1), and (9,6) demand 1 before 0, 3 before 1, and 0 before 3. Independent enumeration of all ten demand edges finds no two-cycle and finds minimum cycle length three. Checking only two-cycles would miss this obstruction. The previous example has six demand edges and minimum cycle length two; all recorded edge labels were reproduced exactly.

These conditions are only necessary for an unspecified future enumeration. For a fixed three-term-free binary tail T, they become sufficient when the demand edges are required to agree with T. A forbidden progression would have four, three, two, one, or zero terms in P. The first three cases are the finite internal, missing-continuation, and pair-demand tests. The last two require three tail terms in progression and are impossible. This gives an exact finite safety decision for that infinite completion. It still does not guarantee an exhaustive chain of safe extensions.

## 6. Packet deduction: residue-grouped radial shells

Assume a chronological block decomposition with a current shell containing [R,Rnext), an immediately preceding shell containing [Rprev,R), and every integer in [0,Rprev) occurring earlier still. Require R>=3Rprev, Rnext>=3R, and a modulus 2<=m<=Rprev. Suppose the current block puts entire residue classes modulo m in successive groups.

Choose distinct residues r,s whose groups occur in that order. Let a be the representative of 3r-2s in [0,m), and choose b congruent to 2r-s modulo m in the integer interval [ceil((R+a)/2),R). This interval contains floor((R-a)/2)>=m integers because R>=3m and a<=m-1. Such a b exists. It satisfies b>=R/2>=Rprev and b>a.

Set c=2b-a and e=3b-2a. Then R<=c<e<3R<=Rnext, c has residue r, and e has residue s. The terms a,b occur in the two earlier chronological regions and c,e occur in that order in the current block. Thus a,b,c,e is a four-term progression.

The integer endpoints and strict bounds are valid, including the boundary case m=Rprev. The result excludes this class of complete residue-grouped shells, including many varying-modulus choices. It does not apply to arbitrary block orders or to the gapped support in the density construction. The negative half of a shell is not needed to construct this positive-difference witness, but the support and chronology assumptions are essential.

## 7. Packet deduction: exact predecessor-bound compactness criterion

An avoiding omega-enumeration of Z exists if and only if there is a single function B:Z->N0 such that, for every N, [-N,N] has an avoiding finite order in which x has at most B(x) predecessors for every included x.

An omega-enumeration supplies B(x) equal to the global position of x. Conversely, take one finite order for each N and diagonalize over the countably many comparisons between distinct integers, passing to a subsequence on which each comparison stabilizes. Every finite tuple is eventually present. The limiting comparisons give a strict total order because totality and transitivity can each be checked on finitely many comparisons. A four-term progression in this limit would occur in all sufficiently late chosen finite orders, a contradiction.

If x had B(x)+1 distinct predecessors in the limit, their finitely many comparisons with x would all hold in sufficiently late finite orders, again a contradiction. Hence every predecessor set is finite. Define the rank of x to be its predecessor count. If x has q predecessors, those predecessors form a finite chain whose ranks are exactly 0,...,q-1. Therefore the ranks attained form an initial segment of N0. They are all distinct and there are infinitely many elements, so this initial segment is N0 itself. The limit has order type omega and enumerates all Z.

The bound B must be fixed simultaneously for all N; choosing unrelated growing rank bounds gives no conclusion. For N>=1, any three-term-free order of [0,N] with 0 first has 2^(j+1) before 2^j whenever 2^(j+1)<=N, because 0,2^j,2^(j+1) is a progression. Thus 1 has at least floor(log2 N)+1 predecessors. This proves the claimed finite-to-omega warning. The logarithmic example is naturally stated for N>=1; N=0 has no value 1 and is immaterial.

## 8. Independent reconstruction of the known three/five bounds

### 8.1 Three terms are universally forced

In any omega-enumeration fix a value a and a nonzero integer q. The distinct values a+2^j q eventually all lie after a because a has finitely many predecessors. Their positions cannot eventually be strictly decreasing nonnegative integers. Therefore infinitely many adjacent pairs of exponents have increasing positions, yielding infinitely many ordered progressions a,a+2^j q,a+2^(j+1)q. This proves the lower bound three without appealing to a density statement or finite computation.

The next two observations are packet deductions, not claims attributed to the source theorem. This proof does not force four terms through a fixed anchor. Indeed, put 0 first and, for each nonzero integer x=2^v u with u odd, define its signed odd terminal label t=3^v u. Order labels by increasing absolute value, positive before negative at a tie; within each fiber put increasing v. For a fixed t the allowed v are 0,...,v3(|t|), so the fiber is finite and these fibers enumerate all nonzero integers with finite predecessor sets. The values 3x and 2x share label 3^(v+1)u and have exponents v and v+1, respectively. Thus 3x always occurs before 2x, excluding every ordered quadruple (0,x,2x,3x).

Imposing the analogous unconditional final-pair reversal for both anchors 0 and 1 is impossible. For x>=2 choose a in {0,1} with x congruent to a modulo 2. The rule requires (3x-a)/2 before x. This is an integer larger than x. Iteration gives infinitely many distinct integers whose positions strictly decrease, impossible in an omega-order. The rule is stronger than ordinary anchored avoidance, so this contradiction is not a four-term forcing theorem.

### 8.2 The five-term-avoiding construction

Define A=(0,4,2,6,1,5,3,7) and

X1=(-8,-4,4,-6,2,-2,6,-7,1,-3,5,-5,3,7).

For i>=2, concatenate the lists 8X(i-1)+r with r in A order for odd i and reverse A order for even i. Take the infinite word

P=0 ; X1 ; -1 ; X2 ; X3 ; ... .

The exact support of Xi is [-8^i,-8^(i-1)-1] union [8^(i-1),8^i-1], by induction on the affine residue copies. These finite supports are disjoint and, with 0 and -1, cover Z. Thus P is a genuine omega-enumeration.

For a power of two m, let rho_m be the rank in least-significant-bit-first order with digit 0 preferred. For m not dividing d, the first differing digit gives both

rho_m(a)<rho_m(a+d) iff rho_m(a+d)>rho_m(a+2d),

rho_m(a)<rho_m(a+d) iff rho_m(a+2d)<rho_m(a+3d).

These statements allow nonadjacent equal residues. They avoid a potentially misleading assumption that every progression modulo 8 has four distinct residues.

The finite X1 has no three-term progression. In Xi, a progression whose difference is divisible by 8 lies in a single residue copy and normalizes to one in X(i-1). If the difference is not divisible by 8, the middle-rank identity prevents three consecutive progression terms from traversing residue groups in chronological order. Induction proves every Xi is three-term-free.

A four-term progression across Xi and X(i+1) would have exactly two terms in each, since three in either shell are impossible. If its difference is not divisible by 8, the pair identity gives the same orientation to the first and second pairs under A, whereas adjacent shells reverse their residue-group order. Contradiction. If the difference is divisible by 8 and i>=2, all four values use a common residue r; replacing x by (x-r)/8 gives the same two-plus-two pattern across X(i-1),Xi. This is a valid induction on i for all differences, including those whose normalized difference is no longer divisible by 8.

At i=1 the only same-residue ordered pairs are (-4,4),(-6,2),(-2,6),(-7,1),(-3,5),(-5,3), all with difference +8. Their two continuations in X2 normalize to (1,2), but 2 occurs before 1 in X1. Hence the last pair cannot appear in progression order. This completes the adjacent-shell four-term avoidance proof.

The initial sixteen-term word 0;X1;-1 is three-term-free. This is an exact finite claim, checked independently over all possible first/last endpoints; equivalently it follows by recursively checking contiguous binary residue groups in that word.

Suppose a1,...,a5 is an ordered progression in P. If a2 is in Xi and a3 is in a later shell, then a1,a2 lie in [-8^i,8^i-1], so the common difference has absolute value strictly less than 2*8^i. The next three magnitudes are strictly below 3*8^i,5*8^i,7*8^i. Being later than Xi, all three must therefore lie in X(i+1), contradicting its three-term avoidance.

If a2,a3 lie in the same Xi, a4 cannot lie there. In the i=1 case a4 cannot be the exceptional intervening -1 either, since that would give a three-term progression within the initial sixteen terms. Thus a4 is in a later shell. The analogous bounds put a4,a5 in X(i+1), contrary to the adjacent-shell four-term avoidance of a2,a3,a4,a5.

The only remaining possibilities have a2 or a3 equal to 0 or -1. Neither can equal 0, which is first. If a3=-1, the first three terms would be in the three-term-free initial portion. If a2=-1, then a1 lies between -8 and 7 and the step has absolute value at most 8. The last three magnitudes are at most 9,17,25; all three are later than -1 and must lie in X2, again impossible. This exhausts the cases and proves five-term avoidance.

This reconstructs Adenwalla's known theorem, not a new upper bound. The source's Case 2 strict endpoint inequality must be relaxed to <=8^i because -8^i is present; the step bound remains strict since the shell never contains +8^i. The displayed combined residue sequence on source PDF page 4 has a duplicated 4 where a 5 is intended. The binary-pair proof above removes reliance on that list. The intervening -1 case is addressed explicitly. These are repairs to the exposition, not changes to the construction or theorem.

### 8.3 Packet deduction: infinitely many four-term progressions remain

For each n>=1, the word contains 0,-8^n,-2*8^n,-3*8^n in that order. The second value lies in Xn; the final two lie in X(n+1). Their comparison descends repeatedly through the residue-zero copies to the comparison -2 before -3 in X1. The common difference is -8^n, so these are genuine negative-difference progressions. At n=1 their zero-based positions are (0,1,119,123). Therefore this particular five-term-avoiding construction cannot resolve four-term avoidance.

## 9. Independent finite checks, controls, and acceptance boundary

The historical standalone independent checker used no candidate imports or source-author execution. Its progression detector enumerates first/last endpoints; its binary comparator repeatedly divides matching parity pairs; its infinite-completion safety test compares the finite prefix/tail order directly for progressions with two initial prefix values. Thus the principal algorithms were reconstructed rather than invoked from the candidate.

All three runs, normal, -O, and -OO, passed and produced byte-identical reports. Explicit exceptions, rather than optimization-removable assertions, enforce checks. Their common report SHA-256 is 00852aabeb796a4c99901a6ddd53c4cc2490388499c07c9cb16a8245ebde6b5c.

Reproduced findings include:

- 86,870 modular binary-identity cases for powers of two through 256.
- Exact supports and three-term avoidance for shells of sizes 14,112,896; no four-term progression across either of the first two adjacent-shell pairs.
- Prefix lengths 16,128,1024 with four-term counts 0,2,685 and five-term counts all zero.
- The first three scaled negative-difference four-term witnesses, including their exact positions.
- Every demand edge in the two dead-prefix examples and minimum cycle lengths two and three.
- 704,808 residue-shell witness cases, and 996 anchor-pair reversals in the 2997-entry terminal-fiber prefix.
- 10,001 fixed-tail record comparisons, 324 impossible singleton extensions, 145 eligible small signed splices with 20 residual failures, and 27,360 extremal buffer cases.
- Positive, negative, and nonmonotone detector controls; the signed (1,0,-1,-2) example; and the (1,2,3,4) orientation-correction example.

Finite checks corroborate, but do not replace, the global proofs above. No finite successful search is promoted to an exhaustive integer enumeration. No source formalization is represented as executed. A hash authenticates bytes, not the correctness of the mathematical claims; both layers are explicitly present.

The remaining task is exactly whether some omega-permutation of all Z avoids four-term arithmetic progressions. The valid fixed-tail and buffer obstructions exclude particular strategies, while the compactness equivalence identifies the missing uniform predecessor bounds. Neither establishes an arbitrary construction or a universal forcing theorem. The audit therefore accepts partial research only.

The snapshot verifier also passed 33 independent fixture controls: a valid snapshot and ten rejection cases in normal, -O, and -OO modes. The rejection cases cover wrong pins, changed or missing members, extra files, manifest changes, symlinks, duplicate entries, and parent-path traversal. These are integrity controls, not mathematical evidence.

No public repository changes, queue edits, or copied-source publication were made during the audit.
