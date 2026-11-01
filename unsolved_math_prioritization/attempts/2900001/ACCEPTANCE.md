# Independent finite case audit and acceptance

Date: October 11, 2026.

This is an independently implemented computational and mathematical-reduction audit within the same research workflow. It is not external peer review. The original acceptance concerns the complete retained evidence set; the public package omits executable code and raw certificates, so this acceptance report is not itself a publicly replayable substitute for that evidence.

## Decision and exact accepted statement

No reproducible mathematical or computational gap was found in the finite result identified by manifest SHA-256

`2c697a418516bb9f41bc0d5ba3161d7be54dde2ad0def0f750439d9fbaefec64`.

For every field K, let S = K[x1,x2,x3,x4,x5,x6], let I be a squarefree monomial ideal with exactly five minimal generators, and let J = (I:x6), regarded as an ideal of the same six-variable ring. If their Betti posets are isomorphic, then sdepth_S(I) = sdepth_S(J).

The accepted evidence is a complete finite computation, with checked exact depth witnesses and impossibility certificates. It is not a proof of the general Betti-poset conjecture, a result for arbitrary five-generator ideals in unrestricted ambient dimension, an independent new quotient theorem, or a novelty finding. This audit did not adjudicate the current open status or priority of the general conjecture.

All 18 files named by the creator's manifest match both their byte counts and hashes. Creator files were read only. Neither the creator's `search.py` nor its `verify.py` was imported or executed; their code was inspected. No source-author research software was executed. The publication package contains the authored analysis and aggregate verification findings, with the computational evidence excluded as described below.

## Independent checks and results

The newly authored `audit.py` uses a different route at each central stage:

1. It enumerates five-element antichains directly on six variables before computing or minimizing any colon.
2. It expands every retained representative through actual variable permutations and compares the resulting labelled ideal set with that direct six-variable enumeration.
3. It constructs every proper open lcm-interval order complex and computes integral Smith forms on its boundary matrices. This is independent of the creator's crosscut conversion and strengthens the creator's direct order-complex check over F2.
4. It separately reconstructs and checks every stored crosscut complex.
5. It enumerates all 729 Boolean intervals via ternary words and checks every depth obstruction by bottom-up induction, rather than reusing the searcher's interval list or recursion.

The following counts all agree:

- 304,752 five-element antichains on the six-variable Boolean lattice.
- After genuinely minimizing the colon: 2,145 cases have one generator; 19,515 have two; 93,035 have three; 121,385 have four; and 68,672 have five.
- The 68,672 retained labelled cases are exactly the expansion of the submitted representative set. None is missing and no extraneous case survives that set comparison.
- 2,146 five-variable base antichains; 48 variable-permutation types; 1,536 representative lifts.
- 702 Betti-isomorphic representative pairs, covering 29,857 labelled pairs.
- Both ideal depths are 4 in 546 representative pairs and 5 in 156. Labelled counts are respectively 24,257 and 5,600.
- 606 eligible representatives have nonuniform lift masks.
- 51 eligible representatives have lcm-lattices of different sizes.
- 1,156 actual open-interval order complexes and all 704 stored crosscut complexes checked integrally.
- Across the cached integral-complex calculations, 5,403 boundary matrices and 30,583 nonzero Smith factors were inspected; every nonzero Smith factor is a unit.
- All 702 distinct ideal-depth certificates passed: complete lower partitions and 9,402 upper-obstruction states, including every one of 8,974 distinct legal branching edges.
- The worked example and both of its certificates agree exactly with the master records.

Five deliberate mutations were rejected: a missing partition interval, an increased claimed depth, a missing obstruction root, a missing obstruction child, and an invalid obstruction pivot. Both ordinary Python and optimized Python runs passed; the checks use explicit exceptions, not removable assertions.

## Why the reduction retains every eligible ideal

Every minimal generator of a proper nonzero monomial ideal is an atom of its lcm-lattice. Its proper lower interval is empty, so its reduced homology in degree -1 is K. It is therefore present in the positive-degree Betti support over every field. Conversely, every non-atom of the lattice lies above an atom, and that atom is still present in the Betti support. Thus the minimal elements of this Betti poset are exactly the minimal generators.

Consequently, isomorphic Betti posets here require five minimal generators on both sides. Colon formation removes x6 from each squarefree generator and then minimizes the resulting list. If a resulting generator is duplicated or redundant, the colon has fewer than five minimal generators and cannot be eligible. If a resulting generator is 1, the colon is S; its quotient is zero and it likewise cannot have the required Betti support. This special case does not depend on a convention about adjoining the degree-zero summand.

Every eligible colon is therefore a five-element antichain of nonempty subsets of x1,...,x5. Conversely, multiplying any subset of the five generators of such an antichain by x6 preserves incomparability, and coloning removes that factor exactly. This proves the lift parametrization. The direct six-variable enumeration independently confirms the count and minimized-colon exclusions.

The 1,536 records need not be distinct orbits of pairs: stabilizers of a base can identify lift masks. The creator correctly describes them as a covering set. The weighting is nevertheless valid because every permutation carrying one labelled base to another transports the entire set of 32 lift choices bijectively. The audit verified the weights and also bypassed that argument computationally by expanding the actual labelled sets and checking their classifications for consistency.

## Betti-poset identification and the field claim

Each lcm degree is uniquely determined by the set of generator atoms below it, since the lattice is atomistic. This atom-set representation is injective and order-reflecting. All its generator atoms remain in the Betti poset. An abstract Betti-poset isomorphism must permute those atoms, and its image on every other element is then forced by its lower atoms. Testing all 120 atom permutations is therefore sufficient and necessary; no larger class of poset isomorphisms is omitted. Variable permutations used for enumeration and generator permutations used for this isomorphism test are logically distinct, even though both act on five-bit masks.

The source identifies positive Betti support using nonzero reduced homology of proper open lcm intervals. The creator's atom crosscut calculation is valid: the order complex is covered by subcomplexes above the atoms; each nonempty intersection has a least element given by the corresponding join and is contractible. Its nerve is precisely the complex of atom subsets with join strictly below the target. Empty intervals at atoms are handled using the augmented degree -1 chain group.

The audit does not rely solely on that conversion. It computes integral boundary matrices for every actual open interval and checks that consecutive boundaries multiply to zero. Every nonzero Smith invariant is 1. Thus each boundary matrix has identical rank over every field, and the reduced homology dimensions obtained from adjacent ranks are field-independent. This justifies **every field**, including all finite characteristics. Checking only rational and binary ranks would not justify that scope, but that weaker inference is not being made here.

The stored homology records are rank summaries rather than archived unimodular change-of-basis matrices. Acceptance of the all-field claim comes from fresh exact integer recomputation, not from trusting their boolean certification flags.

## Stanley-depth interpretation and certificate completeness

The characteristic poset used throughout consists of supports of squarefree monomials **inside the ideal**, in all six ambient variables. It is not the quotient's standard-monomial poset. In particular, the colon is extended to S rather than evaluated only in the five-variable subring.

For a squarefree ideal, a Boolean interval [A,B] yields the Stanley space x^A K[x_i : i in B]. Disjoint intervals cover all monomials according to their support. Conversely, the squarefree monomials in a summand with squarefree base A and variable set Z form [A,A union Z], whose top size is at least |Z|. Summands with nonsquarefree base contain no squarefree monomials. Thus existence of a partition whose tops all have size at least d is equivalent to Stanley depth at least d.

Every submitted positive partition was checked for legal endpoints, disjointness, full ideal coverage, and top cardinalities. For the upper bound at d+1, every remaining element of cardinality below d+1 must belong to some interval with top size at least d+1. Choosing such an element as pivot is exhaustive: any valid partition contains one of the enumerated intervals covering it. Removing that interval strictly reduces the remaining set. The audit enumerates all intervals, requires each legal child to have already been proved impossible, checks a low-cardinality pivot at every stored state, and rejects unreachable states. A state with only high-cardinality elements would admit singleton completion and cannot be certified as dead by these checks. Induction proves the submitted root is impossible. Together with the lower partition, this establishes exact depth.

## Source interpretation

[Katthän, arXiv:1509.08275v2](https://arxiv.org/abs/1509.08275v2) states the ideal and quotient assertions separately in Conjecture 3.5, and Proposition 3.6 gives the equivalence with the general formulation. The preprint and [published article](https://armj.math.stonybrook.edu/pdf-Springer-final/016-0039-5.pdf) agree on those statements. Remark 2.5 explicitly distinguishes the already-known five-generator quotient case from the ideal result for at most four generators. Remark 3.7 states the known direction sdepth(I) <= sdepth(I:x6).

The [earlier five-generator computation](https://arxiv.org/abs/1408.4255v2), Theorem 1.2, concerns depth(S/I) = sdepth(S/I) < sdepth(I). Its ideal inequality does not alone prove Betti-poset invariance of ideal Stanley depth. Likewise lcm-lattice invariance is a stronger hypothesis than Betti-poset isomorphism. The audit accepts the creator's separation of these scopes.

The [Herzog-Vladoiu-Zheng computation theorem](https://arxiv.org/abs/0712.2308) is consistent with the interval-partition interpretation; the required squarefree specialization is also justified directly above. Public-source identity, PDF byte counts and hashes, and inspection coverage are recorded in SOURCE_METADATA.json. The audit bundle contains no copied source text or source documents.

## Reproduction and limits

The original audit ran against the unchanged creator evidence set using Python 3.12.14 and SymPy 1.14.0. The independently authored checker used explicit exceptions, not removable assertions. Its ordinary and optimized run records were retained separately. Runtime fields are nondeterministic; the mathematical checks and counts are deterministic. The checker read the creator inputs and wrote only its own result file.

Full reproduction requires the creator's complete exhaustive case and certificate files and the checker implementation, none of which is included in this public package. The public mathematical discussion proves the reduction and the soundness of the checking rules, while the aggregate records report the outcomes of applying those rules. Published hashes and byte counts establish identity only when the corresponding bytes are available; a digest is neither a mathematical proof nor a substitute for unavailable certificates.

This is an independent-code and mathematical-reduction audit, not a formal proof-assistant derivation or an exhaustive software verification of Python and SymPy. No unresolved gap was identified within the stated finite scope and retained evidence. The unrestricted conjecture, arbitrary ambient dimension, other generator counts, and novelty remain outside this acceptance. In particular, no present literature-wide assertion of open status or priority follows from this audit.

## Subsequent recheck and publication preparation

A subsequent recheck on October 11, 2026 matched every mathematical field of the original audit. It changed only an elapsed-time field in the regenerated result. The original result bytes were reconstructed from the unchanged sealed audit log and restored, and the recheck output was retained separately. Fresh preparation-time checks found all 18 creator manifest entries and all 8 audit manifest entries byte-for-byte intact. This records a restored runtime-output difference; it is not evidence that the input artifacts had drifted beforehand.

Preparation-time replays used copies of the sealed inputs and independently authored audit implementation, leaving the originals unchanged. The creator certificate checker and independent audit both passed under ordinary Python, Python -O, and Python -OO, with identical mathematical fields after removing only elapsed time and the audit optimization-level field. The independent audit rejected all five of its deliberate certificate mutations in each mode. Historical creator controls also rejected eight corruption types, including a missing case, altered Betti support, invalid atom permutation, incomplete partition, raised depth, missing obstruction child, incorrect homology rank, and a missing all-field flag. VALIDATION.json distinguishes recorded historical controls from fresh replays.

The public manifest is a closed allowlist of the authored report, this full mathematical acceptance account, an overview, editorial mapping, and aggregate source, integrity, and validation metadata. A separately stored external seal pins that manifest. The preparation verifier uses explicit failures and is tested in all three Python optimization modes, including rejection of altered content, missing or extra files, nonregular entries, a modified manifest, and a changed seal. These are packaging-integrity tests. They do not add new mathematical evidence beyond the replays above and do not make the excluded computation publicly reproducible.
