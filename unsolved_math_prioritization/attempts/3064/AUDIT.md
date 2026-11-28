# Independent mathematical audit of the matroid base weight report

Problem 3064 / OPG-369. Audit date: 2026-10-11 UTC.

## Verdict and exact target

**ACCEPT the report as a correct partial mathematical investigation. The unrestricted conjecture remains unresolved in this investigation. No mathematical correction is required in the audited report.** This is an independent review of the actual arguments, not a formal proof-assistant certificate, an independent human referee report, a novelty certificate, or an acceptance of a solution of the full conjecture.

The reviewed authored proof report is 13,481 bytes, SHA-256 `9ba11ec39c74cd9c4a03e2502b15d31a447f8182677ba6643a5b7e17433dac4c`. Its closed 28-member evidence package has manifest SHA-256 `ee2bb288d6fb28334b94740be84b5738b355939298fa01e42dcbf957aa92fc9b`. The public PROOF.md is its complete mathematical prose edition. VERIFICATION.json records original and distributed identities; original evidence and identity-check records are not distributed.

Write M for a finite matroid on E, R for its rank, w:E→G for an arbitrary labeling to an additive abelian group, S for the set of weights of all bases, and H for the translation stabilizer of S. The target is

    |S| ≥ |H| (1 − R + Σ_{Q∈G/H} r(w^{-1}(Q))).

The ground set is finite; the ambient abelian group need not be finite, cyclic, torsion-free, or finitely generated. Bases form a nonempty family, including the empty basis when R=0. Labels need not be distinct or nonzero. Loops, parallel elements, coloops, and zero-rank fibers are allowed. Every sum over fibers has finite support. These are the hypotheses used by the proofs and match the intended finite-matroid problem in the sources. No stronger representability or exchange assumption is imported.

## Source fidelity and imported results

The exact target agrees with the main conjecture on the [Open Problem Garden page](https://www.openproblemgarden.org/op/bases_of_many_weights), DeVos–Goddyn–Mohar Conjecture 1.13, and Conjecture 1.2 in the [ICALP 2025 article](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICALP.2025.85). The latter article explicitly starts with a finite ground set. OPG's later displayed prime-order background theorem omits the term −R+1; the main target does not have that defect. The rank-two free matroid with weights 0 and 1 in C3 has one base weight and fiber-rank sum two, directly disproving that background display while satisfying the correct target.

The report correctly distinguishes its elementary derivations from prior literature. The prime-order contraction mechanism already occurs in DeVos's [section 8 notes](https://www.sfu.ca/~mdevos/notes/comb_numb/notes7.pdf), Theorem 8.1. The authored report supplies its own complete ordered-group argument rather than claiming the mechanism as novel. Standard matroid facts and the finitely generated abelian-group structure theorem remain foundational dependencies.

Kneser's theorem is the only additional substantial theorem needed for Section 5. Its exact imported form is the finite, nonempty sumset statement for an arbitrary abelian group in [DeVos–Goddyn–Mohar Theorem 1.2](https://www.sfu.ca/~mohar/Reprints/2009/BM09_AM220_DeVos_KneserAdditionTh.pdf). Its proof was not independently audited here. The same source identifies uniform matroids with parallel extensions as a proved case, and Theorem 1.14 covers groups of order pq for primes p,q and cyclic groups of prime-power order. These are prior results, not results established by the present computation or audit; in particular, arbitrary abelian prime-power groups are not silently included.

The 2025 article calls the exact cardinality bound a conjecture and proves results about the separate proximity conjecture. Those statements support the report's distinction between the two problems. They do not certify exhaustive openness as of the audit date. No independent comprehensive literature search or novelty review was performed for this audit.

## Section 1 audit of the actual stabilizer quotient

The subgroup argument is valid. Translation by h maps S bijectively to itself for h∈H; inverses and sums consequently remain in H. For fixed s0∈S, the map h↦s0+h is injective into the finite set S, so H is finite without any finiteness hypothesis on G. H-invariance makes S a union of complete H-cosets.

For π:G→G/H and T=π(S), the identity S=π^{-1}(T) is exact because every fiber meeting S is one of those full cosets. Therefore |S|=|H||T|. If q∈G/H stabilizes T and g lifts q, then S+g=π^{-1}(T+q)=S, so g∈H and q=0. This proves aperiodicity of the quotient base-weight set, rather than assuming that a quotient automatically removes every period. The new label fibers are exactly the old H-coset fibers, so division by |H| gives the displayed aperiodic inequality with unchanged fiber ranks.

The deletion and translation statements are also valid. Loops belong to no basis and contribute no rank. Every basis contains a coloop c, giving S(M)=w(c)+S(M\c); a coloop contributes one to the rank of every set containing it, so global rank and exactly one stabilizer-coset fiber rank decrease by one. The stabilizer and the numerical deficit are preserved. Adding c to all element labels translates every base weight by Rc and permutes the label cosets. None of these operations needs c to be invertible as a scalar or needs the labels to generate G.

This section makes no assertion that an arbitrary subset or intermediate sumset inherits aperiodicity from S. The report appropriately reserves a distinct, valid inheritance argument for actual summands in Section 5.

## Section 2 audit of the finite model

This is an exact instance-by-instance reduction, including periods and fiber partitions; merely preserving the distinct base weights would have been insufficient.

Let A=⟨w(E)⟩. Since S⊆A and, for any h∈H, h=(s0+h)−s0∈S−S, one has H⊆A. Computing stabilizers in G or in A consequently gives the same subgroup, and replacing G by A changes neither side of the inequality.

Use A≅Z^d⊕K, with K finite. The set

    F=(S+S−S) ∪ (W+H) ∪ H ∪ {0},  W=w(E),

is finite. Choose positive N larger than every free-coordinate range on F. If two elements of F have the same image under reduction of free coordinates modulo N and the identity on K, every coordinate difference has absolute value less than N and is divisible by N, hence is zero; the torsion coordinates also agree. Thus q is injective on F. When d=0, N=1 causes no problem because the K-coordinate map is still the identity. When E is empty, the inclusion of {0} makes the construction unambiguous.

Here is the decisive full stabilizer check. Every q(h), h∈H, stabilizes q(S). Conversely, let k stabilize q(S), fix s0∈S, and select s1∈S with q(s0)+k=q(s1). Set d0=s1−s0. For each s∈S, q(s+d0)∈q(S), so some t∈S has q(s+d0)=q(t). Both s+d0 and t belong to S+S−S: the first by its definition, and the second because S is nonempty. Injectivity on F forces s+d0=t∈S. Hence S+d0⊆S; translation is injective and both sets have the same finite size, so equality holds. Therefore d0∈H and k=q(d0). This proves stab(q(S))=q(H), including the exclusion of newly created quotient periods.

Also S⊆S+S−S, so |q(S)|=|S|, and injectivity on H gives |q(H)|=|H|. For a,b∈W,

    q(a)−q(b)∈q(H) ⇔ q(a)=q(b+h) for some h∈H.

Both a and b+h lie in W+H, so the latter equality is equivalent to a=b+h. Thus two ground elements belong to the same stabilizer-coset label fiber in the finite model exactly when they did before. The ground-set partition, all its ranks, and both sides of the target are unchanged. This argument covers loops and repeated labels as well as arbitrary torsion in A.

The conclusion is not a reduction to cyclic groups, a group-size bound uniform over all instances, or a finite decision procedure for the entire conjecture. The report expressly avoids those overclaims.

## Section 3 audit of the torsion-free quotient theorem

After the exact quotient reduction, it suffices to work with labels in a torsion-free abelian group. The subgroup generated by the finitely many labels is free abelian of finite rank. Lexicographic order supplies a translation-invariant total order there, which is all the proof requires. The monotone chain listed in the report contains |A|+|B|−1 distinct sums. A finite nonempty set in such a group cannot have a nonzero period, since its least element would move.

The rank induction is complete. Rank zero gives one empty-basis weight and zero fiber ranks. At positive rank a nonloop x exists. If F_g=w^{-1}(g) and A_x={g:x∈cl(F_g)}, then A_x contains w(x) and is finite: an empty fiber cannot span the nonloop x. The contracted matroid N=M/x has rank R−1 and a nonempty basis family.

For any basis D of N, D∪{x} is a basis of M, so x∉cl_M(D). If a fiber F_g spans x, it cannot be contained in cl_M(D), because monotonicity and idempotence of closure would then imply x∈cl_M(D). There is therefore y∈F_g outside cl_M(D); D∪{y} is independent of size R and hence a basis. This justifies every sum in A_x+w(N), including the case y=x, with no assumed simultaneous choice of y across different fibers or different bases.

For each g the contraction formula is applied to the correct ground-set subset F_g\{x}:

    r_N(F_g\{x}) = r_M(F_g∪{x})−1
                 = r_M(F_g)−1_{g∈A_x}.

This handles the fiber containing x, fibers containing only loops, and empty fibers. Summing it and applying the rank R−1 induction bound gives |w(N)|≥2−R+Σ_g r_M(F_g)−|A_x|. The ordered-group sumset estimate then supplies precisely 1−R+Σ_g r_M(F_g). No periodic-sumset estimate is being smuggled into this step. The transfer back to G by multiplication by |H| is justified by Section 1.

## Section 4 audit of two classes and the boundary cases

Loops can first be removed, preserving all relevant quantities. Zero or one quotient label class gives a single quotient base weight and right side one. For two distinct quotient labels a,b on X,Y, every basis meets X in between l=R−r(Y) and u=r(X) elements. Extending a basis of Y attains l; extending a basis of X attains u. These extensions cannot add more elements from the already spanned side. The usual basis exchange axiom connects the endpoint bases while reducing their difference by one element at each step. Each exchange changes the X-count by at most one, so all integers in [l,u] occur.

Consequently T=Rb+{kd:l≤k≤u}, d=a−b≠0. The interval length is m=r(X)+r(Y)−R+1≥1. Infinite order of d makes all m weights distinct. For finite order t, m<t also gives m distinct weights, while m≥t makes the progression an entire coset of ⟨d⟩. The last case contradicts the already proved aperiodicity of T because d≠0. Thus |T|=m. This establishes exact equality in the original target, not only a lower bound. It does not assume a potentially problematic converse about every proper progression having trivial stabilizer.

The unrestricted-label rank-one argument is exact: every nonloop is a singleton basis, and each nonloop label fiber in the quotient has rank one. Rank zero and the loop-coloop case have already been covered.

For corank one, dual rank one gives a nonempty set C of possible omitted elements, so the bases are E\{c}, c∈C. It follows directly that r(F)=|F|−1 exactly when C⊆F and otherwise r(F)=|F|. If k distinct quotient labels occur on C, then the quotient base-weight set has k elements. Exactly one fiber contains C when k=1, and no fiber contains C when k≥2. Summing ranks therefore produces right side one or two, respectively, bounded by k. This remains correct when C is a singleton loop and the remaining elements are coloops. The report claims only the inequality in the corank-one case, as required; equality need not hold for k>2.

## Section 5 audit of conditional direct sum closure

The hypothesis must mean that each fixed summand M_i satisfies the target for every labeling into every abelian group. With that natural quantification, the statement is valid. It does not infer an unrestricted result for connected matroids from checked small or special examples.

A direct sum has base-weight set S=S_1+⋯+S_k and additive rank on every subset. After quotienting by the actual stabilizer of S, let A_i be the quotient weight sets. They are finite and nonempty, and T=A_1+⋯+A_k is aperiodic. Any period of an A_i or of an actual partial sum also translates T to itself, so every such stabilizer is trivial. This inheritance is valid because these sets are summands of T; it is not the invalid subset inheritance illustrated in Section 6.

The assumed conjecture for each M_i is legitimately available over G/H with its induced labeling. Kneser's theorem applies to successive finite nonempty partial sums and, because their stabilizers are trivial, yields |T|≥Σ_i |A_i|−k+1. Inserting the individual lower bounds cancels k−1 and, by direct-sum rank additivity, yields the desired quotient bound. The one-summand case is immediate; an empty direct sum, if admitted, is the rank-zero case. This proof is accepted conditional on the explicitly named Kneser theorem, whose source proof was not audited.

## Section 6 audit of the induction obstruction

The specified rank-two matroid has parallel class {x,y} and singleton parallel classes {u},{v}, so its bases are exactly xu,xv,yu,yv,uv. In C6 with labels (0,3,1,4), the corresponding weights are 1,4,4,1,5. Thus S={1,4,5}. Its only possible nonzero stabilizer would have order three, since a stabilizer size divides |S|, but {1,4,5} is not a coset of the subgroup {0,2,4}; directly translating also confirms H={0}. All four label fibers have rank one, giving target right side three and equality.

Contracting x turns y into a loop and leaves u,v as rank-one nonloops. The labels whose fibers span x are exactly 0,3, and contraction base weights are 1,4. Their sumset is {1,4}, stabilized by {0,3}, with size two rather than the proposed aperiodic lower bound three. The omitted basis uv contributes weight five and destroys that period. This is a valid counterexample to the naive intermediate aperiodicity step and is not a counterexample to the target conjecture. Kneser's periodic estimate gives exactly two here, so the missing contribution cannot be recovered by simply naming that theorem without an additional argument.

## Exact inspection and computational scope

The complete 149-line authored mathematical report was read and every mathematical claim was checked as above. The source/dependency ledger, acceptance report, computational audit, finite verifier, control harness, and integrity verifier were also read. No source-author executable code was run. The finite verifier was not rerun by this mathematical auditor, so the full-run total of 669,782 instances per mode and the 21 computational negative-control outcomes remain results of the separately retained computation, not independent reruns certified by this report. They are unnecessary to the proof acceptance above.

An independently written input-identity checker verified the exact report pin, all 28 manifest members and the closed file inventory, and every source-ledger hash and byte count. Its normal, -O, and -OO runs all passed and produced identical records after excluding only their verification timestamps. These are byte-identity checks, not additional mathematical verification or source-proof audits.

Source inspection was bounded as follows:

- S1: complete retained mathematical page text, including main target and defective prime-order background display; matched to the live OPG page during this audit.
- S2: retained cover/title metadata and the relevant statements and surrounding passages for Theorems 1.2, 1.3, 1.14 and Conjecture 1.13. PDF pages 3, 8, and 9 (one-based file pages, printed pages 2, 7, and 8) were visually inspected. The public author-hosted PDF was also opened. The full source proof, later sections, and equivalence proofs for prior special cases were not audited.
- S3: retained PDF pages 1–2 read as text; page 2 visually inspected, including the complete proof of Theorem 8.1. The audit checked the nonloop contraction argument and the correct −R+1 term. The source's informal contraction description is used only in the nonloop situation where it is valid. Later notes sections were not audited.
- S4: abstract and introductory context, the finite-ground-set convention, the separate proximity conjecture, Conjecture 1.2, and its adjacent prior-case discussion. PDF page 3 was visually inspected. The official publisher page verified bibliographic metadata and publication date 2025-06-30; its bibliography also confirms the journal citation for S2. The full 2025 proof and its source-code supplement were not audited or executed.

The live DOI-open attempts were not used as proof of byte identity: the S4 DOI route returned a tool error, after which its official publisher landing page was opened successfully. Local source pins identify the exact retained versions inspected. Public URL availability and local-byte integrity are distinct checks.

The report's bounded-search limitation is appropriate. This audit neither turns an unsuccessful search into a certificate of current openness nor treats known cases as newly proved by the computational scan. The accepted outcome is the exact reductions, complete partial-case proofs, conditional closure statement, and explicit failed-induction diagnosis. The finite aperiodic theorem for arbitrary matroids remains the missing general mathematical step.

## Distribution and review status

This AI-assisted manuscript is unrefereed. Acceptance refers to an internal AI mathematical audit, not external human peer review, journal acceptance, or formal proof-assistant certification. This is not a computational reproduction package. No novelty or exhaustive current-openness claim is made.

The full mathematical review above is retained in this public prose edition. Original inspection evidence is not distributed. Source documents and rendered source pages are inspection material, not authored publication content. The audit does not establish the unrestricted Schrijver–Seymour conjecture.

## Supplementary historical computational audit

The following records the creator's bounded computation. The mathematical auditor and this edition preparer did not rerun it. The complete proofs above do not depend on it.

## What was checked

The independently authored finite verifier checks the exact stabilizer-corrected inequality. All arithmetic is exact finite-group arithmetic. Every basis family is validated by nonemptiness, equal basis sizes and the full basis exchange axiom; all subset ranks are computed. No authors' code, third-party matroid datasets, solver, numerical approximation or random acceptance rule is used.

For each of C2×C2×C2 and C2×C4:

- All labelled matroids on 0, 1, 2, 3 and 4 elements are generated by considering every nonempty equicardinal subset family and checking basis exchange. The counts are respectively 1, 2, 5, 16 and 68. All normalized labelings are checked, totaling respectively 1, 2, 40, 1,024 and 34,816 instances.
- All 32,768 normalized labelings of the explicitly constructed cycle matroid of K4 are checked.
- All 262,144 normalized labelings of the explicitly constructed Fano matroid are checked.
- A deterministic sample of 4,096 distinct normalized labelings of the explicitly constructed Vámos matroid is checked. This last scope is a sample, not exhaustive.

Normalization sets the first element's label to 0; global translation invariance, proved in Section 1 of the report, covers every unnormalized labeling for the exhaustive portions. The zero-element case is handled separately.

Total: **669,782 distinct normalized test instances** per complete run. No counterexample was found. This is not a proof for other matroids, larger ground sets, other groups, or the full conjecture. It also makes no novelty claim for these finite cases.

## Optimization and true negative controls

The entire 669,782-instance run was executed in fresh Python interpreters in normal, `-O` and `-OO` modes. All mathematical outputs and canonical per-family transcript hashes agree. Elapsed times and the explicit optimization-mode field are excluded from the cross-mode comparison.

For each of those three modes, seven genuine rejection tests are run as separate subprocesses:

1. A nonmatroid basis family {01,23} violates exchange.
2. An out-of-range group label is supplied.
3. A correct certificate's stabilizer is corrupted.
4. Its fiber-rank sum is corrupted.
5. A base weight is omitted from the certificate.
6. Its claimed right-hand side is increased.
7. A real valid matroid is tested against the false background formula that omits −rank+1: the rank-two free matroid with labels 0,1 in C3 has one base weight but that false bound asks for two.

All 21 tests must exit nonzero with an explicit `VerificationError`; the harness rejects a spurious successful return, an unrelated exception, or a failure that merely comes from the negative-control sentinel. Three positive quick scans ensure the verifier is not simply rejecting every input. No check uses Python `assert`, so optimization cannot silently remove validation.

The seventh test checks the same inequality rejection gate used by the actual finite scan on a mathematically false bound. It is a control against the defective background formula, **not a counterexample to the target conjecture**.

## Historical reproduction limits and record identity

The historical runs used Python 3.12.14 and only its standard library. The retained original reports contain the explicit basis lists for the named matroids. For sampled labelings, Python's random.Random with seed 16183064 generated candidate tuples; duplicates were removed and selected tuples sorted. This identifies the historical sampling method, but the code, labels, raw output reports, and reproduction commands are outside this prose edition.

Each historical per-family transcript hash commits, in loop order, to the exact basis-mask list, normalized labeling, base-weight set, stabilizer, fiber-rank sum, and both sides of the inequality. These checksum commitments are supplementary and do not replace the omitted algorithm or supply a formal proof. VERIFICATION.json supplies the original run-report byte identities and the exact limitation on independent reruns.
