# Independent adversarial audit: problem 30000203 / OWR-793-006

Date: 2026-10-04 UTC.

## Verdict

**PASS for the frozen partial-result package. No mathematical correction to its eight propositions is required.** The package does not solve the universal strict-inequality question. Retain **unsolved, five substantive approaches exhausted (5/5)**. This audit is verification of those attempts, not a sixth research attempt or a publication authorization.

The strongest checked result is the exact minimum subdegree 15 for the specified A5-by-A6 twisted-wreath datum. The exact subgroup reduction, both sufficient criteria, their stated limitations, the Burnside calculation, and the A8 class minimum all withstand the audit.

One additional discrepancy in the accessible 2006 source rendering is recorded below. It is not repeated or used in the frozen proof, and therefore does not require changing the frozen package.

## Freeze and scope

Audited directory: `../bundle`.

SHA-256 of its `SHA256SUMS`:

`a47a8f04704665f6667eb78191cc870d83990f2055580f07290320ca85f9da39`

All 11 payload entries pass their recorded hashes. The manifest and payload were checked before and after the audit. No frozen file was modified. Audit code, outputs, observations and their hashes are separate in this directory. No helper agent, remote write, third-party communication, source-PDF redistribution, or public release was performed.

Read in full: the frozen proof, approach log, reproducibility instructions, code, result files, source-status/provenance files, and readiness record. The selected original desk review and assessment were read. The official OWR statement and 2021 manuscript passage were visually checked in their available source-page images. The 2019 primitivity criterion was checked in the private preprint text. Relevant sections of the 2006 author-upload rendering were independently reopened, including its full target, construction, and example.

This audit verifies mathematical content, local evidence consistency and reproducibility. It does not independently repeat the entire literature search, refetch the full pinned dataset, or recertify live repository/branch/PR duplicate-search results. Those remain explicitly bounded provenance claims of the research package. A current repository publication gate is a separate operation.

## Exact target and original desk review

The original question is universal: for every finite primitive group of twisted-wreath type and its natural primitive component H, must its minimum nontrivial subdegree be strictly smaller than k times that of H? The official OWR Question 4 agrees with the target in the package. Proving the non-strict bound, a family of positive cases, or a single finite minimum does not answer that question.

The desk review suggests a point supported in one coordinate. The package tests this suggestion correctly: its stabilizer is exactly the preimage in Q of the component-value stabilizer. Consequently a shortest component value gives exactly k m. There is no unjustified promotion of the desk-review suggestion to a proof of strictness.

## Proof audit, including orientation and kernels

### Proposition 1: exact subgroup maximum

The convention f^p(x)=f(px) is a right action: (f^p)^r(x)=f(prx)=f^(pr)(x). It preserves right-Q equivariance. Cosets xQ are left cosets, so the stated transversal terminology is consistent.

For rq=r'q', the element q'q^-1=(r')^-1r lies in R intersect Q. Because q'=h q with h in that intersection, fixedness of t under phi(h) gives the same assigned value at both representations. The order of automorphisms has not been reversed. Left translation by R preserves the support RQ and its values.

For the converse, replacing a nonidentity f by f^p with f(p) nonidentity preserves its orbit size. Its new stabilizer intersects Q in a subgroup fixing f^p(1). It is therefore among the subgroups over which M is maximized. This gives the required lower bound, while a subgroup of maximal order gives the upper bound. The proof need not assert that every constructed function has stabilizer exactly its chosen R; maximality handles that issue.

C_t is a subgroup of Q, including ker(phi). Thus m=|Q|/max|C_t| is correct even for noninjective phi. There is no substitution of image order for preimage order. Since Inn(T) is contained in phi(Q) and T is centerless, P is not admissible and no unwanted nonidentity globally fixed point is introduced.

**Result:** the formula s=|P|/M and equivalence of the target to M>c hold with the stated scope. This is an exact reduction, not progress past the remaining universal existence problem by itself.

### Proposition 2: support-one saturation

The support of f^p is p^-1 Q. Equality with Q forces p in Q; evaluation at 1 then forces p in C_t. Conversely each such p fixes every value. The support argument and the claimed orbit size are correct.

### Propositions 3 and 4: normalizers and the shortest-class obstruction

C is normal in its normalizer N, and C is contained in N intersect Q, so both quotient groups used are well defined. Taking a full preimage of K gives the stated intersection and order. A prime missing from |A| gives a disjoint Sylow subgroup by Lagrange. The warning that mere enlargement N beyond N intersect Q does not imply a disjoint subgroup is correct.

For a 5-cycle value in A5, |R intersect Q| is 1 or 5 and its index in R is at most six. In the trivial-intersection case, order six would give a regular action, contradicted by the fixed points of A6 involutions. In the order-five case, the remaining possible larger orders are 10, 15, 20 and 30. In orders 10, 15 and 20 the Sylow 5-subgroup is normal and its unique fixed letter must be preserved by R, contradicting the purported proper intersection with Q. An order-30 subgroup would be transitive with odd-order point stabilizers, incompatible with an involution fixing a letter. This proves the exact maximum five for a fixed 5-cycle value. It does not incorrectly assume that a global optimum must use a shortest component value.

### Proposition 5: Sylow fixed points

The congruence counts all points of B, including its identity. The fixed-point set has positive size divisible by p, hence contains a nonidentity point. A containing point stabilizer makes its index divide the Sylow index, exactly as asserted. The strictness condition is sufficient, not necessary.

The A20/A19 comparison uses an explicit available centralizer rather than an unproved formula for the component minimum. All stated Sylow orders and the factorial centralizer value are correct. The cited primitivity criterion applies to this datum and the A6/A5 and A9/A8 data: the natural top action is primitive, the twisting image is inner, and simplicity prevents the smaller alternating group from being its homomorphic image.

### Proposition 6: double cosets and averaging

The well-definedness condition on R s Q is exactly fixedness under phi(s^-1 R s intersect Q). Independent choices on double cosets give the stated direct product, with pointwise multiplication even when T is nonabelian. There is no reversal of R and Q.

If all nonidentity orbits had length at least L, their total size would be at least (a-1)L. Therefore the proposed strict reverse inequality is a valid sufficient test. Its failure in A6 is correctly described as failure of that test, not failure of the desired theorem.

### Proposition 7: the elementary minimum 15

The component centralizer orders are 3, 4 and 5. For an admissible subgroup R, write |R|=d r with d<=5 and r<=6. If |R|>24, then d=5 and r is 5 or 6. Order 25 violates divisibility in 360; order 30 gives the involution contradiction already described. This lower bound is independent of subgroup-lattice enumeration.

The even stabilizer of the three unordered pairs has order 24. Its intersection with Q fixes 5 and 6 individually and is the displayed Klein four group. It centralizes the proposed double transposition. Thus M>=24 as well, and the exact reduction proves s=15. All hypotheses used in asserting primitivity are satisfied. The orbit-15 construction is established source material; the package appropriately makes no novelty claim.

### Proposition 8: A8 and the A9 witness

The alternating centralizer criterion is correct: the symmetric centralizer contains an odd element unless the cycle lengths are odd and distinct. Both existence arguments for odd commuting permutations are valid, including repeated fixed points. The eleven nonidentity even cycle types and split-class multiplicities exhaust A8, and their class sizes sum to 20159.

The four-transposition centralizer has order 192, giving the exact minimum 105. For A9, the stated 3-cycle centralizer of order 1080 supplies an admissible subgroup and hence the valid bound 168<945. The report correctly avoids asserting that 168 is the exact minimum on the strength of that witness alone.

## Independent computation

1. The frozen `controls.py --full-lattice` was rerun without bytecode writes. Its JSON output is byte-for-byte identical to the frozen `CONTROL_RESULTS.json`.
2. `independent_checks.py` is a fresh implementation; it imports no frozen code. It uses opposite permutation composition and enumerates subgroups by closing conjugacy classes, expanding one representative per class. Every generated overgroup is reached up to conjugacy, which establishes completeness independently of the frozen left-coset pruning scheme.
3. This finds 501 A6 subgroups in 22 conjugacy classes, with the exact same order histogram, 432 admissible subgroups, maximal admissible order 24 and fixed-5-cycle maximum five.
4. A six-coordinate representation directly produces the complete 15-element orbit of the witness and its exact order-24 stabilizer. 10,800 action-law checks cover this orbit, all top-group elements and a generating pair.
5. Fixed functions are independently counted by following coordinate cycles and their twisting maps. Every cycle-type count agrees, giving 129607960 orbits and average nonidentity orbit size 46655999999/129607959.
6. Direct commutation tests over all 20160 elements of A8, with no partition-centralizer formula, reproduce every listed class size and its minimum 105.
7. Two small exhaustive induced-action controls test the formulas beyond the principal example: a nonfaithful map with kernel order two on 27 functions, and a nonabelian S4/S3 example on 1296 functions. The latter checks the direct fixed-point count against the double-coset product for every one of its 30 subgroups. These are formula/orientation tests, not primitive-simple-socle cases or evidence of the universal target.

No points of A5^6 were exhaustively enumerated. The A8 direct check is a separate audit check, not a change to the frozen program's stated bound of order 360. The independent script has a 120-second guard; the observed complete run took about one second.

## Source checks and version-limited cautions

- The [official OWR report](https://doi.org/10.4171/owr/2005/12), printed p. 692, has the exact strict question.
- The [2006 author-upload rendering](https://www.researchgate.net/publication/228677624_On_minimal_subdegrees_of_finite_primitive_permutation_groups), Section 4, supports the construction attribution. Example 4.15 already gives the same orbit-15 witness. Its all-n component claim has the stated A8 exception; substituting 105 at n=9 makes its displayed ratio nonintegral.
- An additional sentence in that rendering lists a suborbit of length 24 for the A5/A6 example. This would require an order-15 subgroup of A6. Sylow theory makes any order-15 group cyclic, while a permutation on six letters cannot have order 15. Thus that rendering's value is also incompatible with the example. The frozen report neither repeats nor relies on it. The publisher's version was not inspected.
- The [2021 Burness--Shalev manuscript](https://seis.bristol.ac.uk/~tb13602/docs/BSh_final.pdf), Remark 3.9, visually says 12. The checked minimum is 15. Its two-point-stabilizer conclusion survives, as the package explains. No statement about the whole paper's validity or version of record follows.
- The [2019 author preprint](https://arxiv.org/abs/1801.02456), Theorem 2.3, has the sufficient primitivity hypotheses needed above.

The three local PDF hashes agree with `SOURCE_PROVENANCE.json`. No source PDF, extracted full text, or page image is included in this audit deliverable.

## Remaining gap and release boundary

For arbitrary valid primitive data, the outstanding task remains finding an admissible R with |R| greater than the largest |C_t|, or providing a valid primitive equality example and excluding every larger admissible subgroup. None of the five approaches, the rerun, or this audit closes that gap.

The accepted outcome is an audited, unsolved partial package. No Findings alteration, queue promotion to solved, claim of novel discovery, blanket refutation of a cited source, or remote publication is warranted by this audit alone.
