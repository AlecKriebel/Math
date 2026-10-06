# Independent adversarial audit: problem 30001176

Date: 2026-10-06. Target: rank 823, OWR-3392-002.

## Disposition

**ACCEPTED: the precise canonical-filtration and prescribed-singleton obstruction.**

**NOT ACCEPTED: an unqualified claim that the original Conjecture 5 is resolved.**

The frozen argument supplies a valid infinite, minimal, exchangeable, tail-trivial tracial W*-probability sequence. Its canonical local algebras fail the meet identity, already on three sites. No factorization retaining the given singleton image algebras can exist. No mathematical correction to these claims was found. The separately stated eight-dimensional singleton enlargement is also valid and is decisive for the source-scope qualification.

This is an independent AI-assisted mathematical and artifact audit, not human refereeing, formal proof verification, or a historical-priority determination. The reviewer was not involved in the author construction. No remote mutation or publication was performed.

## 1. Source-scope finding

The official 2009 report states Conjecture 5 on printed p. 522, following the generated-algebra example in Theorem 4. Its phrase “gives rise” does not explicitly require preserving singleton algebras or rule out enlargement. Definition 1 on p. 521 includes the meet, join, disjoint independence, and increasing-exhaustion requirements. Its hypotheses include faithful normal state and separable predual, but no ambient-factor assumption. The factor hypothesis in Question 3 must not be imported into Conjecture 5. [Official report](https://ems.press/content/serial-article-files/46209)

Definition 1.6 of the cited de Finetti paper explicitly defines the canonical filtration, minimality, and tail. This supports the canonical reading but does not eliminate the ambiguity in the report's implication. [Cited preprint](https://arxiv.org/abs/0806.3621)

Therefore use the accepted theorem's exact scope in titles, abstracts, and status records. A permissible summary is: “A canonical-filtration counterexample, with no singleton-preserving factorization.” Whether that is the intended complete resolution of the historical conjecture is not established by this audit. There is no claim here that the broader formulation is presently open or solved in the literature.

## 2. Infinite mathematics checked

### Group and exact site algebras

The multiplication is a genuine central extension: the map F is bilinear, its cocycle identity holds coordinatewise, and the written inverse works on both sides. Finite support is preserved. The set of triples is countable. The commutator formula [p_i,q_j] = z_i for i != j, and identity for i = j, follows directly. Distinct z_i are distinct nonidentity central involutions. This is a class-two group, with exponent at most four.

A singleton generated subgroup has order four, with zero central coordinate. Any index set of size at least two contains enough cross-site commutators to obtain every central generator on that set. Its generated subgroup is exactly the group of triples supported there. This reasoning holds for infinite sets because every individual word and coordinate vector is finitely supported. The full set of sites generates the whole group, so minimality is exact.

### Von Neumann realization and all state assumptions

The left regular representation yields a unital von Neumann algebra with faithful normal tracial state. Countability gives a separable representation Hilbert space and separable predual. Each site's four group elements give an injective, normal, unital and state-preserving copy of L(C2 x C2). The state is faithful on every image. Trace-preserving subgroup expectations exist. Equivalently, the trace's modular group is trivial, so the conditioning and modular covariance requirements are automatic. The construction requires neither a nonfaithful state nor unbounded random variables.

The short conditional-expectation paragraph in the author proof is correct but condensed. INDEPENDENT_LEMMAS.md spells out compression, the right-coset amplification, and the Fourier-support criterion so that no intersection conclusion rests on an unproved passage from groups to von Neumann algebras.

### Exchangeability, injections, and stationarity

Every relabeling permutation preserves F and defines a trace-preserving normal automorphism. This proves equality of all joint moments, including repeated site indices and arbitrary elements of the common four-dimensional domain. Any injection preserves the same law. The one-sided shift is a normal injective endomorphism onto the tail subgroup algebra. It need not be onto the whole algebra: one-sided stationarity does not require an automorphism. A two-sided variant is available, but is not a missing hypothesis.

This is ordinary permutation exchangeability. The site involutions are not CAR generators: cross-site commutators are independent central group elements, not imposed scalar anticommutation signs. No CAR hypothesis appears in the target statement.

### Infinite tail and meet

For any subgroup H, membership in L(H) is equivalent to Fourier support in H. Hence arbitrary intersections of group von Neumann subalgebras agree with the von Neumann algebra of the group intersection. Every tail subgroup consists of triples supported entirely in that tail. Intersecting all tails leaves the identity alone. The faithful trace then forces every element of the von Neumann tail to be scalar. This is a genuine infinite argument, not extrapolation from a finite test.

The witness lambda(z_0) belongs to the algebras on {0,1} and {0,2}, but its Fourier projection onto the original singleton algebra is zero. In fact their intersection is L(K_{0}), of dimension eight, whereas the original singleton has dimension four. The product of the two subgroup expectations fixes this witness; expectation onto the canonical meet annihilates it. Thus the failure is exactly the required meet identity, despite the two subgroup expectations commuting.

The impossibility for prescribed singletons is immediate and robust: the binary join axiom forces both two-site algebras, and the meet axiom would force their intersection to be the prescribed four-dimensional singleton. The contradiction does not depend on continuity at infinite sets.

### Remaining axioms and the enlargement

Disjoint supports imply trivial subgroup intersection. The subgroup expectation of the other algebra is scalar, giving tau(xy) = tau(x)tau(y) for arbitrary bounded elements, including infinite index sets. Canonical joins and increasing exhaustions hold by generation. P(N0) is atomic. No extra nonatomic continuity condition applies.

Replacing each singleton by L(K_i), of dimension eight, gives a valid factorization C_I = L(K_I) with the same state and ambient algebra. It has exact meets, joins, disjoint scalar independence and increasing exhaustions. It is permutation covariant as well. Thus even allowing an exchangeably covariant enlargement is a materially different question; this example satisfies that enlarged version.

## 3. Compatibility with related results

The cited extended de Finetti theorem yields conditional full independence, which becomes scalar independence when the tail is trivial. It is not a universal Boolean-meet theorem. Its definitions of probability space, random variable, canonical filtration and exchangeability agree with the construction. [Köstler](https://arxiv.org/abs/0806.3621)

Quantum-permutation symmetry is stronger. The present site algebras are not free: the alternating centered word (p_i q_j)^4 has trace one for i != j. Therefore the quantum-exchangeability/free-independence equivalence does not contradict this example. [Köstler–Speicher](https://arxiv.org/abs/0807.0677)

The symmetric-group-character theorem has additional representation hypotheses and identifies special fixed-point and tail algebras. Those hypotheses are not supplied merely by an external permutation action on the present group. [Gohm–Köstler, Theorem 5.2](https://arxiv.org/abs/1005.5726)

The July 2026 preprint's block-singleton property is also compatible with the example: traciality and disjoint scalar independence give tau(xyz) = tau(y)tau(zx) when the middle block is disjoint from the outer blocks. Its factorization terminology therefore cannot be substituted for the Boolean meet axiom. [Del Vecchio–Rossi, Definitions 5.1 and 6.1; Theorems 5.3 and 6.3](https://arxiv.org/abs/2607.20342)

## 4. Intake and artifact audit

All three complete corpus files were read and their byte counts and SHA-256 hashes independently recomputed. The full target problem record and catalog entry were inspected; the research-results map has no target entry. Reconstructing the complete-review binding using that absent-entry convention and hashing the exact statement reproduces both intake hashes. No corpus content or extracted record is included here.

The author ZIP SHA-256 and external manifest trust anchor match the assignment. All twelve ZIP members are unique, flat regular files, with no unsafe paths. Frozen member bytes match both the original release and the authenticated manifest. The author source and all executables were read before replay. The author checks report 2,900,842 finite checks.

Independent replay passed normal Python, optimized Python, relocation with spaces, and the author's eight mutation classes in both modes. The new finite-set implementation imports no author code and separately exercises the multiplication, regular representation, subgroup lattice, enlarged repair, expectation support masks, noncontiguous labels, and selfadjoint encoding. Both sets of checks are supplementary. They do not certify the infinite mathematics by computation.

The audit package has its own manifest, code pins and fail-closed verifier. Its independent mutation campaign also checks empty directories, a regular file named __pycache__, symlink replacement of a manifested file, a changed result with its manifest updated, and changed code with its manifest updated. Creating an actual Unix-domain socket is prohibited in this execution environment; that mutation is explicitly recorded as not run, not passed. The verifier rejects every nonregular node via lstat, and directories, symlinks and FIFOs are dynamically tested. See the machine-readable receipts for actual outcomes.

## 5. Required disposition language and limits

- Accept the scoped canonical/prescribed-singleton theorem and its enlargement qualification.
- Do not replace the original problem's status by an unqualified “solved” solely on this audit.
- Do not describe this audit as a formal certificate, human peer review, or a novelty search.
- The author freeze remains unchanged. This separate report adds detailed justification; it does not silently patch the frozen argument.
- Public literature searches were bounded. No inspected item resolved the source-intent ambiguity. The audit did not exhaust literature or repository history and did not independently rerun the author's repository searches.

No mandatory mathematical correction was identified within the accepted theorem. The remaining blocker to a full historical-conjecture resolution is source scope, not an alleged flaw in the explicit construction.
