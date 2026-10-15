# Independent audit of the reconstructed O7b findings

Audit date: 2026-10-09 (UTC).

Edition note, 9 October 2026: this is the complete written mathematical audit, with its original reasoning, qualifications, counterexamples, and supplementary-check discussion retained. The four reviewed reports below are distributed byte-for-byte. Two inventory-only references are edited: the non-distributed input inventory's identity is omitted, and the omitted independent checker is described without its local path. No checker, separate test result, or execution log accompanies this proof-only edition. The original and edited audit identities and the exact editorial scope are recorded in ACCEPTANCE.md and PROVENANCE.md. Historical pre-audit labels in the reports are not the present review determination.

## Determination

**ACCEPTED: the reconstructed restricted mathematical findings in both turn reports, under their stated hypotheses. No must-fix mathematical defect was found in the reviewed bytes.**

This is a fresh acceptance of the specifically hashed reconstruction, not recovery or authentication of the lost historical audit. Turn 1's former acceptance is background only. Turn 2 had not previously been independently accepted; this report now independently accepts its sign lemma, fixed-batch dependency theorem, and correctly restricted transporter theorem. It does not accept either approach as a solution of O7b.

**O7b / 8400008 / AMR-083-0008 remains unresolved after two approaches (2/5 turns).** The review is not a third approach, a new research turn, or an oracle lower bound. No publication, commit, push, queue change, or external sharing was performed by this audit.

The decisive transporter statement is

    gcd(c,n) = n/gcd(x*r' - x'*r,n),

under the stated odd-squarefree, equal-nonzero-norm, divisibility, and unit hypotheses. Replacing gcd(c,n) by c would be false. The reviewed turn-2 report does not make that replacement.

## 1. Reviewed objects and integrity

The four reports were read in full. The accompanying implementation and recorded results were inspected. All nine entries of the input packet's manifest were checked against their actual byte counts and SHA-256 hashes; all matched. The manifest's own SHA-256 also matched its sidecar.

Reviewed report identities:

- `reports/MODEL_AND_STATUS.md`: 3,381 bytes; SHA-256 `93214cb26eca4bf52ed8a116f67cbbee8c03a35a10526c17e3c8d6e85bd525a1`.
- `reports/TURN1_RECONSTRUCTED.md`: 9,221 bytes; SHA-256 `906baa8b7c6c5f960c2f89e13aaebce7705458a679e93e5664237871c403cb4d`.
- `reports/TURN2_CANDIDATE.md`: 11,602 bytes; SHA-256 `7d57ffaed0175c46b807c251c8615eaa0749b339f1f6580a4ad5c55a722b2468`.
- `reports/SOURCE_VERIFICATION.md`: 3,259 bytes; SHA-256 `76c23317c3b9283dcc0ecb72602881863f6d6ac9e77debf2757e7aa1ea155f7a`.

The reviewed reports are identified above. The auxiliary input inventory is not distributed in this proof-only edition, and its identity is omitted.

The source reports were left unchanged. Their historical labels such as “preliminary and unaccepted” describe their creation state, prior to this audit. They must not be silently relabeled while retaining the old hashes. This report records the new review determination separately.

## 2. Exact model

The supplied C7 convention is internally consistent: on a positive integer m it returns the unique positive pair (r,s) with m=r²s and s squarefree. Thus each prime valuation is sent to (floor(e/2), e mod 2). In particular C7(27)=(3,3); neither coprimality of r and s nor equality of s with rad(m) is part of the model.

The target requires complete factorization of every positive input, zero-error output or explicit failure on every allowed random tape, polynomial worst-case bit work/query sizes/query counts/tape length, and success on at least half the uniformly chosen allowed tapes. The empty factorization of 1 is included. A single correct factor, average-case input performance, or an expected-time unbounded rejection procedure does not satisfy the target.

Acceptance of this model means agreement with the stipulated assignment. The original historical problem document was not independently recovered in this audit. No claim is made that the model file is a quotation or authenticated transcription of that source.

## 3. Turn 1: accepted results and exact scope

### 3.1 Gcd-layer support projection

For squarefree n, each gcd(n,u) layer removes exactly one copy of every n-prime still dividing u. A prime p|n of valuation e in m therefore appears in the first e layers and in no later layer. The product A of all layers has valuation e, the product R of even-numbered layers has valuation floor(e/2), and S=A/R² has valuation e mod 2. Primes outside n never enter the layers. The remaining u=m/A is coprime to n.

The divisions are exact, every intermediate has O(log m) bits, and at most floor(log₂m) nontrivial layers occur. Computing gcds and exact divisions requires no factorization of n. This is a deterministic polynomial-bit construction in the explicit input lengths. Both n=1 and m=1 are covered by empty products.

**Accepted without amendment.** Squarefreeness of n is essential to this particular one-prime-copy layer analysis; the report does not claim the same construction for arbitrary n.

### 3.2 Coprime-query simulation

The n-supported squarefree part S and the squarefree part of u have disjoint prime support. Consequently, if C7(u)=(r_u,s_u), then (R*r_u,S*s_u) is exactly C7(m). Its uniqueness follows from the parity valuation formula.

On each fixed random tape, the simulator reconstructs the same answer to each virtual query. Induction then gives identical next queries, virtual transcripts, outputs, and success decisions even for an adaptive algorithm. Actual query values generally differ; only the simulated transcript is identical. Querying u=1 can be omitted. Query length does not grow, no extra random bits are needed, and preprocessing adds polynomial overhead to a polynomial-bounded computation.

**Accepted without amendment.** This removes n-supported query content from oracle access; it does not remove the oracle. The example C7(72)=(6,2), gcd(35,6−1)=5 correctly blocks an inference that coprime answers are useless under arbitrary subsequent arithmetic.

### 3.3 Recoverable valuation blocks and closure

For a tag z, successive gcd layers reveal the products of n-primes with valuation at least e. Exact layer quotients reveal the positive-valuation equality classes; n divided by the first layer reveals the zero class. Intersecting these partitions by gcd and splitting complements by exact division produces the joint valuation-vector partition. There are at most omega(n) nonempty prime blocks and a polynomial number of explicit layers. No oracle or factorization is needed for this computation.

For two primes whose valuations agree in every initialized integer, equality is preserved by addition/subtraction of valuations (multiplication/exact division), min/max (gcd/lcm), multiplication by a common exponent, exact integer roots, and the two C7 valuation maps. Selecting among already available integers does not change this. Every constant or newly supplied integer must be accounted for as a tag.

**Accepted without amendment.** If the output is a divisor of pq, equal p- and q-valuations exclude its being p or q. This conclusion is restricted to the listed closure. It says nothing comparable about addition, subtraction, modular reduction, or fresh bit-decoded integers. It is not an information-theoretic lower bound for unrestricted algorithms, nor does it limit what arbitrary bit computations might output as new tags.

### 3.4 Fresh normalized polynomial bound

For n=pq with distinct primes, gcd(n,all coefficients)=1 means that the polynomial is nonzero over each of F_p and F_q. A proper coefficient gcd already exposes a factor and must be treated separately. Repeatedly stripping a common factor n terminates for every nonzero explicit polynomial. The stripped n-powers change both relevant valuations equally. The identically zero polynomial is correctly excluded from this root argument.

Conditioned on the past, G is fixed before the fresh uniform X in {0,…,M−1}. There are at most d roots modulo p, and each residue has at most ceil(M/p) representatives in the interval. Thus

    Pr[p|G(X) | past] <= d(1/p + 1/M),
    Pr[gcd(G(X),n)>1 | past] <= d(1/p + 1/q + 2/M).

This includes zero evaluation values as hits. Degree zero with normalized coefficient gcd 1 gives no hits. The inequality remains valid if its right-hand side exceeds one.

For adaptive stages, activation and the chosen polynomial are determined by the prior history. If H_t denotes a hit at active stage t before any coefficient split, conditional expectation gives

    E[1_{H_t} | past] <= alpha * 1_{active t} * d_t,
    alpha = 1/p + 1/q + 2/M.

The union bound, tower property, and pathwise sum of degrees at most D therefore yield Pr(any such hit)<=alpha*D. If a specified scheme's success without a coefficient split implies a hit, the same upper bound applies to Pr(success AND no coefficient split). The report correctly leaves that success-implies-hit premise separate.

**Accepted without amendment.** The degree budget must hold on every path, and does not alone bound the number of degree-zero steps, coefficient lengths, or bit work. The displayed balanced-range constant 10 follows directly from the two inequalities supplied in the report.

The prohibition against conditioning on the future event “no coefficient split ever” is necessary. An independently checked example uses n=35, M=64, and first polynomial X. Choose the next polynomial to be constant 1 after a hit and constant 5 otherwise. Then no eventual coefficient split occurs exactly on first-stage hits. Their joint probability is 21/64, while the conditional probability given no split is 1. The otherwise tempting bound 419/1120 is less than 1 and cannot bound that conditional probability. This is an audit fixture for the existing scope limitation, not a new research approach.

### 3.5 Distinct-exponent prior result

The stated attribution is supported by the inspected versioned article: Section 5 defines the pairwise-distinct positive exponent class and Theorem 5.3 supplies a black-box full-factorization reduction with classical work outside its subroutine. An exact C7 oracle satisfies the relevant squarefree-decomposition capability. A composite squarefree integer has repeated exponent 1 and is outside the distinct-exponent class. No extension to that excluded case is supplied by the citation. [Kahanamoku-Meyer, Ragavan, Vaikuntanathan, and Van Kirk, arXiv:2412.12558v4, Section 5](https://arxiv.org/html/2412.12558v4#S5).

**Accepted as an attribution and restricted prior result, not a new contribution.**

## 4. Turn 2: accepted results and exact scope

### 4.1 Sign-blind modular-square relation

For independent uniform units x_i modulo odd squarefree n, conditioning on their squared residues leaves each x_i uniform on exactly 2^k roots, independently across i. CRT identifies each root fiber with k independent uniform signs. Deterministic C7 answers add no sign information because they are functions of the fixed residues.

After fixing the selector's independent randomness as well, a returned nonempty subset I, its positive h, and Y=h*product(r_i) are fixed. The relation implies X²=Y² mod n and Y is invertible. Multiplying the roots over any fixed nonempty I leaves a uniform vector of k signs. Thus X/Y is uniform among the 2^k roots of one. All-plus and all-minus are exactly the two trivial gcd outcomes; every other sign vector gives a proper factor. The exact conditional probability is 1−2^(1−k).

Conditioning further on the selector returning a relation is legitimate because that event is determined by the fixed residues and independent selector randomness. If the selector's success probability is rho, the resulting proper-factor probability is rho*(1−2^(1−k)); it is not automatically at least one half. Selection that sees x_i, any equivalent sign information, or prior sign-sensitive outcomes falls outside this proof.

The integer-exponent extension is valid when the proposed relation makes the comparison well-defined and at least one exponent is odd. Negative powers, if used, require interpreting the square root in the rational unit group and reducing its denominator modulo n; subset exponents avoid this issue entirely. All-even exponents eliminate the fresh sign argument and carry no such probability guarantee.

**Accepted without amendment for the precisely stated subset theorem.** The short general-integer-exponent sentence is accepted with the ordinary well-defined rational-unit interpretation for negative exponents; it is not a claim that a negative-exponent product is necessarily an integer square.

The ordinary congruence-of-squares method is credited to its classical literature, particularly Dixon. The inspected original paper presents residue collection, binary exponent dependencies, and a proof that conditions on squared-sample data. The present proof does not claim those ideas as novel. [Dixon, *Asymptotically Fast Factorization of Integers*, 1981, pp. 255–260, institutional PDF copy](https://pages.cs.wisc.edu/~cs812-1/dixon.pdf).

### 4.2 Sampling and acquisition remain open obligations

Uniform unit sampling is a mathematical hypothesis of the sign lemma. Straight rejection sampling without a cap does not supply a worst-case finite tape or runtime bound. A proposed reduction must explicitly budget sampling, failures, repeated trials, query sizes, and all later recursive factorization steps. None is established merely by a one-relation conditional success calculation.

Most importantly, no polynomial-bounded method to acquire a useful nonempty relation is proved here. The paper's statement of this gap is accurate. The audit does not fill it and does not infer from it an impossibility theorem.

### 4.3 Complete fixed-batch square-dependency computation

The gcd-free refinement is correct, including divisibility cases g=a or g=b and collisions among newly inserted or existing bases. Removing the two columns u,v and adding columns u,v,u+v to a/g,b/g,g preserves every original m_i exactly. Merging equal bases adds their exponents. Bases 1 may be discarded.

Let P be the product of distinct current bases. Before duplicate merging, each genuine refinement replaces ab by ab/g. Merging can only decrease the product further. Thus P falls by a factor at least two at every refinement. Initially log₂P<L, so fewer than L refinements occur. At every step there are at most L bases; every base has at most L bits, and each exponent is bounded by log₂m_i because its base is at least two and all exponents are nonnegative. Pair scanning, gcds, divisions, and exponent-column additions therefore give a deterministic polynomial-bit algorithm. This also covers m_i=1, duplicates, perfect powers, and the empty batch.

The final pairwise-coprime bases have disjoint prime supports. A nonsquare base has at least one odd prime valuation, so its E-th power is square exactly when E is even; a square base imposes no parity condition. Consequently the parity rows from exactly the nonsquare bases give precisely the entire dependency kernel. Gaussian elimination returns a basis of that space without enumerating it. Every binary subset product has at most O(L) bits, permitting exact integer square-root recovery and checking.

**Accepted without amendment.** Dropping the square tests would reject valid dependencies such as the singleton batch (4). Coprime refinement alone is not a prime factorization, and its final bases need not be squarefree. Neither property is needed for the stated kernel algorithm.

The prior gcd-free/coprime-basis work is correctly credited. The institutional Bernstein record identifies both his algorithm and the earlier work of Bach, Driscoll, and Shallit. Shallit's publication list confirms the 1993 *Factor refinement* citation. This audit validates the report's own elementary polynomial bound, not an implementation of the cited faster algorithms. [Bernstein institutional record](https://research.tue.nl/en/publications/factoring-into-coprimes-in-essentially-linear-time/); [Shallit publication list](https://cs.uwaterloo.ca/~shallit/papers.html).

Since each m_i differs from s_i by a square factor, both fixed batches have exactly the same binary dependency space. This establishes only that oracle normalization is unnecessary for finding dependencies in an already explicit batch. It does not provide a relation where the kernel is zero, show that a polynomial number of sampled residues will have a relation, reconstruct all C7 answers, or remove adaptive oracle-dependent choices of a future batch.

### 4.4 Equal-norm transporter with arbitrary valuations

Write A=x*x'−s*r*r' and B=x*r'−x'*r. In Q[T]/(T²−s), nonzero K makes z=x+rT invertible with inverse (x−rT)/K, including when s is a square and the algebra is not a field. Thus z'/z=(A+BT)/K is legitimate.

Dividing the common gcd of A,B,K and normalizing the denominator sign gives primitive a,b,c with c>0. Direct multiplication and the equal-norm identity prove all three equations displayed in the report:

    a²−s*b²=c²,
    a*x+b*s*r=c*x',
    b*x+a*r=c*r'.

Now fix p|n and put e=v_p(K)>0. The unit hypothesis implies that s,r,r',x,x' are all p-adic units. Because p is odd, the two local slope signs are distinct.

- Opposite slopes: B=2*x*r' mod p is nonzero. Therefore the common divisor h has p-valuation zero, so v_p(c)=e.
- Equal slopes: C=x*r'+x'*r is a unit mod p. The exact identity B*C=K*(r'²−r²) gives p^e|B. The exact identity r*A=−x*B+K*r' then gives p^e|A. Hence v_p(h)=e and v_p(c)=0. This remains valid when B=0; if r'²=r², the product identity and C≠0 force that case.

This is the required full-valuation cancellation argument. Merely proving A=B=0 mod p would not be sufficient when e>1.

As n is squarefree, gcd(c,n) is the product of the opposite-slope primes, whereas gcd(B,n) is the product of the equal-slope primes. They are complementary divisors of n, establishing the audited identity. The inverse transporter changes B's sign but not c. Conjugating a single supplied representation is a different operation and cannot be substituted without changing the local sign interpretation.

**Accepted without amendment.** The identity concerns gcd(c,n), not c. The supplied fixture n=15, s=1, (x,r)=(11,4), (x',r')=(−11,4) has K=105 and c=105, so c itself is not the corresponding divisor 15.

All three sign outcomes are legitimate: gcd(c,n)=1 when signs all agree, n when they all differ, and a proper divisor exactly when the pattern is mixed. A second useful representation is assumed supplied; no method to find one within the target bounds is proved.

The hypotheses cannot be silently dropped. K=0 makes the proposed inversion invalid. A nonunit counterexample is n=3, s=1, (x,r)=(−15,−6), (x',r')=(−15,6). It has K=189, B=−180, and c=21, so gcd(c,n)=3 but n/gcd(B,n)=1. It is excluded because gcd(2srr',n)=3. This fixture confirms the need for the restriction; it is not a defect in the stated theorem.

## 5. Independent verification performed

The unchanged recovery implementation was copied into the audit directory and rerun there so it could not overwrite the reviewed packet. Its regenerated result JSON matches the original recorded JSON byte-for-byte, SHA-256 `5c8f09afbe0880ac8d6f53b72343c17a0593fed644eca56913ab9cc74f7fc14e`.

A separate independent checker, not distributed in this edition, was written without importing the recovery code. It uses a different binary-kernel construction and additional boundary cases. All assertions passed:

- 80,161 support projections and C7 normal forms, including independently prescribed valuations.
- 1,280 eight-step adaptive oracle transcript simulations, over every 8-bit tape in each fixture.
- 1,200 joint valuation partitions and 392 arithmetic closure outputs.
- 3,882 explicit batches; exact dependency-space comparison against 94,549 subset square tests. Included duplicates, 1s, square-only bases, mixed prime powers, and a 998-step refinement stress case.
- 440 fixed selected relations over n=15,21,35,77,105, covering all 10,208 compatible root tuples; exact sign probabilities and uniform quotient distributions checked.
- 10,636 finite-interval root bounds, 138 coefficient splits, explicit repeated normalization, and zero-polynomial cases.
- A complete 32,768-tape adaptive experiment with pathwise degree budget 3, checking both the expected-active-degree and worst-case-budget bounds.
- Explicit counterexamples to root-aware relation selection and invalid future conditioning.
- 197,382 equal-norm transporter instances, including 122,642 with negative K, 27,504 mixed-sign cases, and both cancellation cases with repeated prime factors in K.
- Sixteen prescribed-high-valuation cases reaching v_3(K)=80 and v_5(K)=81, plus n=1, the c-versus-gcd distinction, and the excluded nonunit fixture.

The test program uses small trial factorizations or deliberately known factorizations to form reference answers. Those are test oracles and are not asserted to be polynomial-time factoring procedures. The finite tests detect errors; the mathematical arguments above establish the general results. Testing does not prove the missing relation-acquisition theorem or the original reduction.

## 6. Defect ledger and final disposition

### Must-fix mathematical defects

None found in the reviewed report bytes.

### Interpretive cautions, already respected by the main statements

1. “All dependencies” means a polynomial-size basis, not enumeration of an exponentially large set.
2. The sign probability is conditional on sign-blind acquisition and uniform independent units.
3. Negative integer relation exponents, if used, need a well-defined rational-unit square relation; the explicit subset theorem is unaffected.
4. Valuation closure and the degree bound have restricted operation/sampling models and cannot be promoted to general oracle lower bounds.
5. The transporter equality identifies the squarefree intersection of its denominator with n, not the entire denominator.
6. The new acceptance is tied to the reconstruction hashes; it does not authenticate missing historical files or imply a successful solution.

### Obligations still absent for a solution

- A uniform polynomial-bounded mechanism for obtaining useful relations or suitable second equal-norm representations.
- An end-to-end algorithm with verified worst-case query, arithmetic, and tape bounds, including bounded sampling and failure accounting.
- A complete-factorization guarantee on every positive integer, with at least half of allowed tapes successful and no erroneous success on any tape.

**Final disposition: accept the reconstructed restricted lemmas and their stated boundaries; retain unresolved status for O7b. No novelty is claimed for standard Dixon, gcd-free basis, valuation, or elementary root-bound techniques.**
