# Independent partial mathematical audit: ideal-LLL obstructions

Date: 2026-10-20 UTC. Problem 8800068 / AMR-087-0068.

## Verdict and exact scope

**PASS for the mathematical statements reviewed below, subject to their stated hypotheses. NOT acceptance of a solution to the overall problem.** No counterexample or substantive mathematical error was found in this review. The broad varying-monic-polynomial first-vector/SVP sharp-rate target remains unresolved in the reviewed material.

Reviewed files:

- `PROOF_ATTEMPT_1.md`;
- `computation/check_attempt_1.py`;
- `CYCLIC.md`.

This is an independent adversarial review of the written proofs and their mathematical scope. It does not independently authenticate the historical PDFs, repeat the literature search, certify novelty or open status, reproduce the unrelated randomized unimodular-input experiment, review other ongoing attempts, or certify publication readiness.

## 1. Increasing-degree triangular classification: valid

The support hypothesis is essential: the ordered vectors have increasing degree, with positive diagonal coefficients in the fixed coefficient order `(1,X,...,X^(n-1))`. This is not an arbitrary triangular basis up to a coordinate permutation or rotation.

For `i<n`, multiplication of `b_i` by X has degree exactly i, so no quotient-polynomial reduction occurs. Looking downward from the highest coordinate in its integer basis expansion removes all basis vectors above index i+1. Comparing coordinate i gives the positive integer `d_i/d_(i+1)`. The LLL inequalities imply `d_(i+1)^2 >= d_i^2/2`; a positive integer ratio at least 2 violates this. Hence all diagonal entries equal a positive integer a.

The ideal then contains `a, aX,...,aX^(n-1)`. Its covolume is `a^n`, so it is exactly `a Z^n`. All Gram–Schmidt coefficients are integers and size reduction forces zero. The claimed exact basis, not merely its lattice, follows.

Boundary checks: n=1 is covered; positive diagonal signs are explicitly assumed; reducible q, nonprincipal ideals, and negative/large lower coefficients in q do not affect the proof. Full rank is needed for the determinant and basis arguments. The claim cannot be transferred to an LLL basis after swaps merely because the original input was HNF.

## 2. General-lattice control family and finite checker: valid

The recursive basis has orthogonal components `t^(i-1)e_(i-1)` and coefficients `2^(-(i-j))`. The strict lower bound `t^2>1/2` supplies strict Lovasz, while adjacent size-reduction coefficients equal 1/2. Thus the stated stationary-input convention must retain the stated tie rule.

The vector `2b_n-b_(n-1)` really has only its final coordinate nonzero. It supplies an upper bound on lambda_1, which is the correct direction for the claimed approximation-ratio lower bound. No claim that it is itself shortest is needed. Common denominator clearance preserves this ratio and LLL reducedness.

Since `1<t^(-1)<sqrt(2)`, X times the first scaled basis vector cannot have an integral expansion. The obstruction is independent of the quotient polynomial because it occurs before wraparound. There is no overlooked rational/integral scaling escape.

Re-ran `computation/check_attempt_1.py` successfully for every n=2,...,16. Its finite checks support, but do not replace, the universal argument. It checks integral common scaling, exact GSO and reduction conditions, the displayed short vector, and the nonintegral obstruction. The code does not perform exhaustive search over ideals or identify a shortest vector. Its particular rational t choices are test inputs, not a universal algorithmic proof of the density-of-rationals step.

## 3. Lexicographic-minor argument: valid, with the following explicit justification

Assume `1 <= d <= n`, and let C be the integer d-by-n row coefficient matrix of the independent short lattice vectors. Let I be the lexicographically largest increasing d-tuple for which `det(C[:,I])` is nonzero. In the row convention used in the proof, `B=M G` with M unit lower triangular.

For increasing d-tuples J and I, a lower-triangular minor `det(M[J,I])` can be nonzero only if `j_k >= i_k` for every k. Indeed, if `j_k < i_k`, the first k selected rows have zero entries in all selected columns from position k onward, so their support lies in only k-1 selected columns and the minor vanishes.

Cauchy–Binet therefore gives

    det((CM)[:,I]) = sum_J det(C[:,J]) det(M[J,I])
                   = det(C[:,I]).

Every nonzero contribution except J=I would have J componentwise at least I and lexicographically greater, contrary to the choice of I; the principal minor `M[I,I]` has determinant 1. Thus the selected coefficient remains a nonzero integer even though the other transformed coefficients need not be integral.

The wedges of the orthogonal rows of G are mutually orthogonal. Consequently the length of the selected wedge component is at least `product_(i in I) sqrt(D_i)`, and the full wedge norm is at least that length. This supplies precisely the lower bound on volume used in the file.

For editorial precision, “coefficient ... has absolute value at least product sqrt(D_i)” should be read as the coefficient in the **normalized** orthogonal wedge basis, or as the **length of the selected orthogonal wedge component**. In the unnormalized wedge basis `G_(i1) wedge ... wedge G_(id)`, the coefficient is the nonzero integer minor and its absolute value is at least 1. The mathematics and the ensuing inequalities are correct under the intended interpretation.

Finally, `D_i >= D_1 2^(-(i-1))`, and the sum of the largest d elements of `{0,...,n-1}` is `d(2n-d-1)/2`. Together with Hadamard, these give the claimed bound

    ||b_1|| / lambda_1(L) <= 2^((2n-d-1)/4).

No assumption of orthogonality between the short vectors, primitivity of their span, or integrality of the Gram–Schmidt coefficients is being smuggled in. Boundary checks give the standard bound `2^((n-1)/2)` for d=1 and the strengthened bound `2^((n-1)/4)` for d=n. The lemma would be meaningless for d=0, which should be excluded explicitly if it is restated standalone.

As a finite adversarial check, `computation/check_audit.py` tested maximal-minor invariance in 544 exact rational cases with n=1,...,7, every possible d, random integer coefficient matrices and random rational unit lower triangular matrices. All passed. The triangular-minor support implication was also tested directly. These checks are not an exhaustive proof; the Cauchy–Binet argument above is the proof.

## 4. Orthogonal-orbit and negacyclic consequences: valid

Independent equal-length orbit vectors generate a full-rank sublattice, whose covolume is an integer multiple of that of L. Therefore the determinant inequality has the correct direction. Hadamard yields `det(L) <= lambda_1(L)^n`. Combining it with the classical LLL Hermite bound yields the stated first-vector/SVP exponent 1/4.

For n a positive power of two, including n=1 if that convention is used, `X^n+1` is irreducible over Q and multiplication by X is an orthogonal signed rotation in the coefficient norm. The quotient over Q is a field, so every nonzero element has n linearly independent consecutive powers under this action. Independence over Q is equivalent to independence over R here because all vector entries are rational. Hence the negacyclic corollary applies to every shortest nonzero vector and every LLL-reduced basis.

For arbitrary cyclic or negacyclic q, the orbit dimension of a representative f is `n-deg(gcd(f,q))`, as follows from its annihilator `q/gcd(f,q)`. Thus the full-span/coprimality criterion is correct. Irreducibility must not be assumed for arbitrary non-power-of-two negacyclic degree.

For a sequence satisfying the exponent-1/2 lower target, the d-vector bound implies `d/n -> 0`: taking logarithms and dividing by n yields an upper bound `1/2-d/(4n)-1/(4n)`. This is a necessary condition, not a construction or a sufficient condition. A full-span or uniformly positive-density shortest-vector orbit rules out that sharp target. It does not rule out all exponential badness, and it does not address nonorthogonal multiplication by X.

The scalar-ideal corollary is also correct regardless of which unimodular input basis is used. It excludes the exponent-1/2 target on scalar lattices, not every weaker exponential lower bound.

## 5. Rank-one cyclic shortest-vector example: valid

For n>=2, the lattice `m Z^n + Z(1,...,1)` is exactly the set of integer vectors whose coordinates are all congruent modulo m. Its quotient index is `m^(n-1)`, and cyclic rotation preserves it. Since X fixes the all-ones polynomial modulo `X^n-1`, it is precisely the ideal generated by m and that polynomial.

A nonconstant vector has two coordinates differing by a nonzero multiple of m. The inequality `x^2+y^2 >= (x-y)^2/2` gives squared norm at least `m^2/2`. Under the stipulated **strict** condition `m>sqrt(2n)`, this exceeds n. Nonzero constant integer vectors have squared norm at least n, with equality exactly for the two all-ones sign choices. Thus the shortest-vector orbit really has dimension one.

The determinant-to-minimum ratio becomes unbounded as m tends to infinity for any fixed n>=2. This refutes a universal cyclic determinant inequality, but does not exhibit any poorly reduced LLL basis. The n>=2 restriction is material to unboundedness.

Additional finite check: for n=2,3,4,5 and respective m=3,3,3,4, `computation/check_audit.py` enumerated all congruence-lattice vectors in `[-m,m]^n` with nonzero squared norm at most n and found exactly the two claimed vectors; it also checked the determinant formula. Any vector with squared norm at most n lies in that box for these parameters, so these are complete shortest-vector checks for those four instances only.

## Audit conclusion

The restricted obstruction proofs are sound. Their presentation should retain the increasing-degree flag restriction, Euclidean coefficient metric, exact LLL parameters, explicit tie convention, and distinction between an SVP ratio and a determinant-normalized Hermite ratio. The exterior-power sentence can be made more precise as described above; no mathematical repair is required. Nothing in this audit accepts the broad sharp-rate construction as solved, proves an HNF-start lower bound, or certifies a historical open-status claim.

## 6. Extension: attempt 2, independently reviewed after initial audit

Additional files reviewed: `PROOF_ATTEMPT_2.md` and `computation/check_attempt_2.py`.

**Reverse-family obstruction: PASS.** Denominator clearance cancels from the multiplication-action equations. Already the equation at i=2 requires `2t` to be an integer, while `sqrt(2)<2t<2`; this rules out every n>=2, not only n=2. The further recurrence for i>=3 is also correct: its two distinct coordinate coefficients require both 2t and t integral. The argument genuinely eliminates the quotient polynomial's wraparound contribution and does not mistakenly reuse the increasing-degree hypothesis.

**General companion-HNF criterion: PASS.** With columns as lattice basis, `C^(-1)TC` integral is necessary and sufficient for X-stability, and X-stability is necessary and sufficient for ideal closure. The use of `d=|det C|` rather than a signed determinant causes no problem: `J=d C^(-1)` is an integer matrix. Each congruence is entrywise modulo the positive integer d. The added block `d I` gives the column lattice full row rank, so its column HNF is a nonsingular square integer basis. Membership of the integer right-hand side is exactly integrality of `H^(-1)r`. This establishes feasibility for an integer c, not merely a necessary rational condition. The program uses a consistent row-major vectorization and transposes its row-basis input correctly.

**Cyclic additive quotient characterization: PASS.** In a finite unital ring with cyclic additive group of order m, the additive order r of 1 annihilates the entire ring since `(r 1)x=0`; thus m divides r, and r divides m. Consequently 1 is an additive generator, and the ring is canonically isomorphic to Z/m. This crucial step justifies the powers-of-a kernel rather than an arbitrary cyclic quotient functional. Conversely a kernel of evaluation modulo m is an ideal in a fixed quotient exactly when q(a)=0 modulo m; the displayed choice `q=X^n-a^n` always supplies some monic q. The trivial quotient m=1 is harmless. This statement does not imply cyclic rotation invariance.

**Quadratic positive example: PASS.** The two determinant-300 columns span the entire evaluation kernel, and the norm decomposition exhausts every integer combination. In particular lambda_1 is exactly `sqrt(325)=5 sqrt(13)`, not merely bounded above by it. Independently computed multiplication by X in this basis gives the integer matrix

    [[-266, -283],
     [ 268,  284]].

Its trace is 18 and determinant 300, consistent with the stated polynomial. The discriminant -876 proves irreducibility over Q. GSO and strict Lovasz are correct; the size-reduction tie remains subject to the declared tie convention. This is a valid nonoptimal reduced basis of an irreducible coefficient ideal, but gives no asymptotic or canonical-input statement.

**Finite rotation searches reproduced.** Ran the unmodified checker at t=5/7: 8, 72, 576 presentations with 1, 0, 0 hits respectively for n=2,3,4. Ran the same exact code with only t replaced by 3/4: the same presentation counts with 2, 0, 0 hits. The named quadratic example is one of the t=3/4 hits. These are precisely the specified finite search sets, including duplicate identity presentations, and say nothing exhaustive about all rational rotations.

## 7. Extension: large-modulus rank-one cyclic obstruction

Additional file reviewed: `CONSTRUCTION_ATTEMPT.md`.

**Large-modulus theorem: PASS.** Every k-by-k coordinate minor of k lattice vectors is divisible by `m^(k-1)`: in its multilinear expansion, all terms with at least two copies of the common all-ones row vanish. This remains true for arbitrary integer coefficients of that row. The first k basis vectors are independent, so a nonzero minor exists. Cauchy–Binet therefore gives prefix volume at least `m^(k-1)`; primitivity of the prefix is not needed.

For the largest nonzero basis coefficient c_k of u, projection onto the complement of the first k-1 basis vectors gives precisely `c_k b_k*`. Thus `D_k <= n/c_k^2 <= n`. Backward use of the LLL inequality gives `D_i <= 2^(k-i)n`. Multiplying, taking square roots, and then the (k-1)-st root for k>=2 yields exactly

    m <= n^(k/(2(k-1))) 2^(k/4).

The second derivative of the base-2 logarithm of the right side is `log_2(n)/(x-1)^3>0`. A convex function on [2,n] has its maximum at an endpoint, giving the stated maximum of `sqrt(2)n` and `n^(n/(2(n-1)))2^(n/4)`. The singleton n=2 case is correctly handled. Strictly exceeding that maximum excludes all k>=2. If k=1, shortestness and integrality force `u=+/-b_1`.

The strict inequality in the theorem is material; equality is not eliminated. The threshold automatically exceeds `sqrt(2n)` for n>=2, so no circular use of the uniqueness-of-shortest-vector result occurs. Its asymptotic equivalence to `sqrt(n)2^(n/4)` is correct. The comparison with the weaker generic recovery threshold of order `sqrt(n)2^(n/2)` is also correct.

The argument leaves the indicated intermediate-modulus range open and does not exclude the sharp exponent there. No poor reduced basis is produced. The accompanying randomized and frozen-first experiments were **not independently rerun or code-audited in this extension**; their empirical outcomes are not part of this acceptance verdict.

## Updated partial verdict

The additional universal algebraic statements and the concrete quadratic example pass review. Both finite exact rational-rotation result counts were reproduced. The earlier exterior-power wording has now been clarified in CYCLIC.md by its author. Neither these accepted partial obstructions nor the finite searches establish the requested growing-dimensional sharp-rate family or settle the overall historical problem.

## 8. Extension: growing evaluation-kernel family, attempt 3

Reviewed `PROOF_ATTEMPT_3.md` and `computation/check_attempt_3.py`.

**Necessary determinant and relation-size scales: PASS.** Evaluation is surjective through the constant coordinate, so the determinant is m. Taking logarithms of the Hermite inequality gives the stated necessary quadratic-size lower bound on log_2(m) for the sharp target, including the term `n log_2(lambda_1)`. The n-1 relations `a e_i-e_(i+1)` are independent even when a=0, and have common norm `sqrt(a^2+1)`. The earlier exterior-power proof permits any common norm upper bound A, not only lambda_1. Substituting d=n-1 yields exactly `||b_1|| <= sqrt(a^2+1) 2^(n/4)`. Thus neither a fixed determinant nor a fixed evaluation point can achieve the requested exponent; these are necessary conditions only.

**Explicit growing ideals and shortest vector: PASS.** For the chosen a>=2 and m=`a^(n-1)+1`, `q(a)=a m`, so the evaluation map on the quotient is well-defined and its kernel is `(m,X-a)`. The relation rows and `e_0+e_(n-1)` have determinant of magnitude m, hence span the whole kernel. Every unit coordinate vector fails the congruence because `0<a^j<m`. These are the only nonzero integer vectors with squared norm below 2, proving lambda_1 exactly sqrt(2). The log-scale calculations are valid but do not imply the existence of a bad basis. The case n=2 is included without coordinate collisions in the displayed vector or basis.

**Balanced-digit short-vector lemma and large-a recovery: PASS.** With every coordinate of w smaller in absolute value than `(a-1)/2`, the stated geometric-series bound indeed yields `|k-c|<1` for the integer difference k-c, including n=2. Hence k=c. The bound `|w_0-c|<a-1<a` makes the first congruence imply equality; each subsequent coefficient is divisible by a and has absolute value less than a, so vanishes. Consequently w is an integer multiple of the planted vector. The conclusion can be vacuous at small a, which does not invalidate it.

The standard LLL bound here is exactly `2^(n/2)`. The strict condition `a>2^(n/2+1)+1` puts every reduced first vector inside the strict radius of the lemma. A basis vector cannot be a nontrivial integer multiple of a lattice vector, so the resulting multiple of v must have coefficient +/-1. This proof does not need uniqueness of all shortest vectors in the family. Equality at the threshold is not established, and no claim of an optimal threshold is justified.

**Experiment reproduced.** Executed the checker unchanged. All 112 reductions succeeded, with no errors; every first squared norm was 2, in dimensions 2,3,4,6,8,10,12,16 with 14 starts each. The independent reduction, congruence, and determinant assertions all passed. This confirms only the finite stated experiment, not absence of adversarial reduced bases or an asymptotic success theorem.

The overall sharp-rate target remains unresolved after attempt 3.

## 9. Extension: exact cyclic constant-loss controls

Reviewed `NEXT_ATTEMPT.md` and `computation/verify_countercontrols.py`.

**Exact shortest norm: PASS.** Splitting by the common residue modulo m gives a lower bound m on any nonzero residue-zero vector and sqrt(n) on any nonzero-residue vector. The two witness vectors yield equality with `min(m,sqrt(n))` for all positive m,n, including m=1 and n=1. If m>=3 and m>sqrt(n), equality forces all coordinates to be +/-1, and congruence prohibits mixing signs. The m=2 mixed-sign exception is real and must not be suppressed in shortest-span claims.

**Dimension-three control and minimal dimension: PASS.** Independently checked the displayed three-dimensional determinant, Gram–Schmidt data, size bounds and Lovasz conditions. The first boundary is equality, which is allowed. In dimension two, the Hermite bounds and the integer norm spectra eliminate m=1,2; for m>=3 the nonconstant norm lower bound exceeds the generic LLL upper bound of squared norm 4. A nonshortest constant multiple of u cannot be a basis vector. Thus dimension three really is the first possible nonshortest-first example within this family.

**Universal constant-loss family: PASS.** The basis with first rows `m e_1,u` and remaining coordinate rows is a permutation of the standard lattice basis. Direct orthogonal projection gives the stated Gram–Schmidt lengths and every displayed coefficient. For i>j>=3, the coefficient denominator is indeed `n-j+1`, so the largest absolute value is 1/2, not a potentially larger near-end value. The parameter interval implies `n-1>=2m`; the tight small case is m=3,n=7. The three classes of Lovasz boundaries evaluate as stated. Since n<m^2, the shortest-set condition is satisfied and the first vector is strictly nonshortest.

For every even m>=4, n=3m^2/4 is integral, remains at most m^2-1, and gives exactly the claimed constant ratio sqrt(4/3). This is a genuine growing-dimensional cyclic ideal family with only two shortest vectors. It is not an exponential-loss construction. Any statement that every reduced basis of these cyclic lattices is shortest-first is thereby disproved.

**Coordinate-prefix limitation: PASS.** For k-1 distinct coordinate rows followed by u, the kth orthogonal squared length is n-k+1 and the immediately preceding coefficient is 1/m. Therefore that Lovasz boundary requires `n-k+2 >= 3m^2/4`. When m>sqrt(n), this bounds the first-vector/SVP ratio by sqrt(4/3); when m<=sqrt(n), the first vector already has shortest norm m. Thus the whole specified prefix ansatz has at most this constant loss, irrespective of suffix choices. This does not constrain arbitrary noncoordinate prefixes.

**Finite controls reproduced.** Executed `computation/verify_countercontrols.py`; all exact assertions passed for the n=3,m=2 example and the four stated rank-one examples. The squared ratios were 9/7, 4/3, 25/19 and 4/3 for (n,m)=(7,3),(12,4),(19,5),(27,6), respectively.

The updated mathematical conclusions remain partial: a verified constant-loss lower family, several no-go regions, and no established sharp exponential-rate family or global impossibility theorem.

## 10. Extension: relation-prefix/tail obstruction, attempt 4

Reviewed `PROOF_ATTEMPT_4.md`.

**Main proposition: PASS.** The reverse triangle inequality for the two shifted coefficient embeddings gives the claimed minimum singular bound a-1. Each selected raw row has coefficient 1 in its own unused coordinate of relation-coefficient space, so its distance to preceding raw rows is at least a-1. Arbitrary raw-row ordering, signs, and lower-unitriangular integer row additions preserve the relevant pivots. General unimodular mixing does not: for example, replacing two relation rows by `N r_1+r_2` and `(N-1)r_1+r_2` preserves their lattice while the second Gram–Schmidt pivot tends to zero as N grows. The manuscript correctly excludes that extension.

For a basis prefix, the projected tail is a genuine rank-r lattice basis and inherits all LLL conditions. The planted v lies outside even the full relation span, so its projection is nonzero and has norm at most sqrt(2). The r-dimensional SVP bound thus gives first projected length at most `2^(r/2)`. Combining with the cross-boundary lower bound `(a-1)/sqrt(2)` proves `a-1 <= 2^((r+1)/2)`. Both r=1 and k=1 are valid endpoints of the proposition. The asymptotic minimum tail size `n/2-O(1)` for the specified a is correct.

**Required edge-case correction identified.** The two-dimensional-tail consequence in section 4 must require n>=3. The proposition assumes `1<=k<n`, whereas that consequence sets `k=n-2`. With n=2 the prefix is empty and no such obstruction holds for arbitrary completions. The initial wording omitted this restriction, incorrectly encompassing all reduced bases in dimension two. The author added n>=3, and the corrected text was verified. The main proposition and the corrected corollary now both pass review.

No finite search was relied on for this universal proof. It excludes only the specified preserved natural flags and their completions, not arbitrary transformed relation-prefix bases or the general sharp-rate target.

## 11. Extension: value-and-derivative ideals, attempt 5

Reviewed final `PROOF_ATTEMPT_5.md` and `computation/check_attempt_5.py`.

**Algebraic construction and index: PASS.** The dual-number evaluation formula is valid over Z/m without any primality assumption. Both q(a) and q'(a) vanish modulo m, so the map descends through q. Its image contains 1 and epsilon=X-a, proving surjectivity. Monic division by `(X-a)^2` establishes the exact kernel ideal `(m,(X-a)^2)`, not only containment. Thus its additive quotient has order m^2 and is `(Z/m)^2`; here m>=9, so it is genuinely noncyclic. The explicit triangular basis has the asserted determinant and both congruences, independently certifying the full coefficient kernel.

**Unique shortest-vector theorem: PASS.** The assumption r>=1 gives n>=3. The three coefficients of h^2 occupy distinct coordinates even at r=1. Every integer vector of norm at most sqrt(6) has coefficient absolute values at most 2. The two division formulas, including constant terms and the empty intermediate index ranges at r=1, are correct. The exact positive difference

    (a-5)(a^r-1)/(a-1)

proves the first remainder evaluates strictly between -m and m, while the lattice congruence makes its value divisible by m. Once that value is zero, repeated base-a reduction is valid because every coefficient has absolute value strictly below a. The derivative step requires invertibility of `r a^(r-1)` modulo m; this follows from r dividing a and `gcd(a,a^r+1)=1`. It is not silently assuming r is prime or m is prime. The second remainder has the stated bounds and vanishes by the same argument. Therefore every nonzero lattice vector of norm at most sqrt(6) is precisely +/-h^2. Both the minimum and uniqueness are proved, not inferred from reduction outputs.

**Growing scales and relation bounds: PASS.** The selected a is at least 8 and divisible by r. Since n=2r+1, its logarithmic determinant has leading term n^2/4 with error O(n log n), as claimed. The n-2 shifts of `(X-a)^2` are independent and retain their coefficient norm, giving exponent `(n+1)/4` in the general d-vector bound. At the chosen a this bound does not exclude the target. The shortest polynomial has maximal permitted degree and is killed by X modulo q; it does not generate independent short rotations. No claim of irreducibility, orthogonality, cyclic coefficient invariance, or a sharp bad basis follows.

**Final finite experiment reproduced.** Ran the final checker unchanged: all 42 recorded runs passed in dimensions 3,5,7,9,13,17, with first squared norm 6 in every case and no errors. The centered residue operations are exact additions of multiples of m and mX, so they preserve the lattice. All membership, determinant and reducedness assertions passed. The preliminary failed SymPy call described in the manuscript was not replayed and is not mathematical evidence; the final script result is independently reproducible. The six scrambles per dimension start from a reduced baseline, as disclosed, and are not independent samples from all lattice bases.

## Final audit scope and freeze

This audit is complete for the five numbered proof attempts, CYCLIC.md, CONSTRUCTION_ATTEMPT.md, and NEXT_ATTEMPT.md reviewed above. The only substantive scope omission identified was the n>=3 qualifier in attempt 4's two-dimensional-tail corollary; that correction has been applied and verified. The earlier exterior-power wording was also clarified. All remaining reviewed mathematical assertions pass within their explicit hypotheses.

Verified deliverables are partial structural obstructions, exact ideal and shortest-vector families, and constant-loss reduced examples. **The broad asymptotic first-vector/SVP exponent-1/2 construction is not established, and no global impossibility theorem is established.** This audit is not a certificate of novelty, historical open status, all-source authenticity, or all experimental provenance. Specific reproduced computations and excluded empirical reviews are identified above.
