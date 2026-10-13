# Independent audit: extension, restriction, and the actual independence relation

Target: PR 533, problem 30001182 / OWR-3392-009, original claimed-solved head `135911efff1ad14314f0506b0d5f158ba986426f`.

**Disposition: no mathematical gap found in this approach family.** The finite-dimensional example changes the truth of the independence relation under a state-preserving ambient inclusion; it does more than show loss of extremality for a selected witness. The algebraic Laurent example establishes the source's separate literal non-lifting concern. The C*-extension observation is correct and does not invalidate the finite example. The original claim excludes modified categories in which the argument would fail. This audit assesses mathematics and source scope, not historical priority.

I read only the frozen authored `public/PROOF.md` and `public/SOURCE_GATE.md`, the intake identity, and the official source. I did not read the original `audit/AUDIT.md` or prior audit conclusions. This report independently reconstructs the mechanisms and attempts to falsify the conclusions.

## 1. Exact claim and source convention

Let F(A) be the countable unital algebraic free product of a unital complex *-algebra A, with canonical injections j_i. Let K_A be all positive unital functionals on F(A) invariant under finitely supported permutations of the copies. For unital *-subalgebras B,C of A and a state phi, the tested relation is:

    There exists omega in ext(K_A) such that
    omega o ((j_1|B) * (j_2|C)) = phi o (i_B * i_C)
    as entire states on B*C.

The original [official OWR 09/2009 report](https://publications.mfo.de/bitstream/handle/mfo/3111/OWR_2009_09.pdf?isAllowed=y&sequence=1), Liebscher's complete contribution on printed pp.540–541, was downloaded independently, text-extracted, and visually read, including both diagrams. The subscript 1 on the coproduct confirms unit amalgamation. The first diagram places both subalgebras in the original ambient algebra. The second places them in distinct free-product copies. Extremality is stated for exchangeable states, without specifying a full marginal slice. The definition states no faithfulness, normality, traciality, distinctness, or scalar-intersection requirement. The main example's distinctness and scalar intersection are stronger optional properties.

Using finitely supported permutations causes no ambiguity if S-infinity is instead read as all permutations of N: each algebraic word involves finitely many indices, and any permutation agrees on those indices with a finitely supported permutation. For C*-states, equality on these dense words extends by continuity.

Item (1) concerns a possible shortage of extreme-state lifts under an ambient embedding. Item (6) separately asks about C*-algebras and von Neumann algebras with normal states. The source's comment about the classical case does not replace its explicit free-product diagrams by a tensor product or impose global commutativity on the exchangeable free-product algebra. A convention that does so would be a separate relation.

Success criterion: an explicit state-preserving unital inclusion A into A' and fixed B,C for which the entire-state relation is false in A and true in A'. Failure criteria: an alternative extreme downstairs witness, an impure upstairs witness, failure to preserve a word of the joint law, a noninjective inclusion, or a source requirement excluding the examples. None was found.

## 2. Actual downstairs nonexistence, independently derived

Take A=C({00,01,10,11}), p(s,t)=s, q(s,t)=t, B=span{1,p}, C=span{1,q}, and phi=(delta_00+delta_11)/2. The functions 1,p,q,pq are a basis. Evaluating a+bp=c+dq at 00,10,01 shows that B and C intersect in scalars; they are distinct proper subalgebras.

Assume a candidate omega in K_A satisfies the entire joint-state identity. In its algebraic GNS representation put P_i=pi(j_i(p)), Q_i=pi(j_i(q)), with cyclic vector Omega. These operators are projections. From the specified joint law and exchangeability, for every i distinct from j,

    omega(P_i)=omega(Q_j)=omega(P_i Q_j)=omega(Q_j P_i)=1/2.

Thus the squared norm of (P_i-Q_j)Omega is zero. Since there are at least three copies, a third index connects every two P vectors; the same equation connects every Q vector. All P_i Omega and Q_i Omega coincide with one vector v. For every generator R among these projections, R Omega=v and Rv=R^2 Omega=v. Every nonempty word in these generators therefore sends Omega to v, and its expectation is 1/2.

Every element of every copy of A is a linear combination of 1,p,q,pq, so these words span the entire algebraic free product. Let chi_0 and chi_1 evaluate every copy at 00 and 11 respectively. The calculation forces the identity of whole states

    omega = (chi_0 + chi_1)/2.

Both characters are positive, normalized, and exchangeable; they differ on p in any copy. Consequently the forced omega is not extreme in K_A. This covers **every** candidate, rather than ruling out only the natural folded candidate. The same calculation applies to the universal C*-free product, where the algebraic words are norm-dense.

No projection-commutativity assumption was made for different copies. Within a copy p and q commute, but the collapse derives from positivity and the joint law. The algebraic GNS null space is a left ideal: if eta(x*x)=0, Cauchy–Schwarz applied to x and a*a x gives eta(x*a*a x)=0, so ax is null. This validates the representation calculation even before completion. In this finite-dimensional example each copy acts boundedly as well.

## 3. An upstairs extreme state and equality for every word

Embed A diagonally in M_4 in the order 00,01,10,11. For v=(e_00+e_11)/sqrt(2), let phi'(T)=v*T v. Its diagonal restriction is exactly phi. The density matrix vv* is a rank-one projection, so phi' is pure: if phi' is a convex combination of states, the positive projection 1-vv* has zero expectation in each constituent. Cauchy–Schwarz kills every matrix block outside vv*, leaving the same vector state.

The folding homomorphism f:F(M_4) -> M_4 sends every copy to the same matrix. It is surjective and permutation invariant. A pure state pulled back along a surjective *-homomorphism remains pure: each constituent of a convex decomposition vanishes on x*x for x in the kernel, hence on the kernel itself, and descends to a state of the quotient. Purity on the quotient makes the decomposition trivial. This proof works for positive algebraic states, not only continuous states.

Therefore omega'=phi' o f is pure among all states and in particular extreme among exchangeable states. For any word w in B*C, f sends the B letters in copy 1 and C letters in copy 2 to the original diagonal matrices in their original order. Their product lies in A, so its phi' value is its phi value. Linearity proves equality on every element of B*C. This is the required full joint-state identity. Every entire copy also has marginal phi'.

Thus the relation is **false downstairs and true upstairs**. The upstairs state restricts to the unique nonextreme downstairs state, which explains the mechanism but is not a substitute for the nonexistence proof in Section 2.

## 4. Free-product injection and category compatibility

In the algebraic category, for each unital inclusion D_i into E_i choose vector-space complements D_i=C1 plus D_i^0 and E_i=C1 plus E_i^0 with D_i^0 contained in E_i^0. The unital free product has the normal-form vector space consisting of the scalars and alternating tensor products of these complements, with adjacent copy indices distinct. The induced map on each summand is a tensor product of injections and is injective. Thus F(A) -> F(A') is genuinely an embedding, including for the polynomial/Laurent example.

There is also an injective map of the universal unital C*-free products. Here is a derivation from the ordinary C*-state extension theorem rather than assuming the statement. Given a representation pi of F(A) on H, consider its copy representations pi_i of A. Decompose pi_i into cyclic reducing representations. Extend each cyclic vector state from A to A' and use its A'-GNS representation: the closure of the A-orbit of the cyclic vector reproduces the original cyclic representation and reduces A. This extends pi_i to a representation of A' on H plus K_i. Pad all the countably many extension spaces, using direct sums of any nonzero representation of A', to a common larger Hilbert space while fixing H pointwise. The universal property now gives a representation of F(A') that restricts on H to pi on F(A). Taking the supremum over pi proves preservation of the universal norm, hence injection. No faithful conditional expectation is being assumed.

For the finite-dimensional A and M_4 in the main example, positive algebraic states on their free products are automatically continuous in the universal C*-norm. Indeed, in each copy, c=||a||^2 1-a*a has a positive square root b, and for every GNS vector [x], eta(x* c x)=eta((b x)*(b x)) is nonnegative. This bounds each represented a by ||a||. Completion produces a bounded representation of each copy, hence of the universal free product. Therefore the finite example has compatible algebraic and C* interpretations; it does not silently use an algebraic discontinuous state as a C*-state.

## 5. Extreme C*-invariant extensions exist; restrictions need not stay extreme

For an equivariant unital C*-inclusion D into E under the finitely supported permutation group G, let lambda be an extreme invariant state of D. First extend it to an ordinary state eta of E. Average eta over the finite symmetric subgroups S_n. Each average still restricts to lambda; a weak-* convergent subnet exists by compactness. For any g in G, all sufficiently late averages are g-invariant, so the limit is invariant. This proves nonemptiness of the invariant extension fiber.

Let K_E and K_D be the invariant state spaces and r the restriction map. The fiber L=r^{-1}({lambda}) within K_E is compact and convex. It is a face: if an element of L is a nontrivial convex combination of eta_1,eta_2 in K_E, the extremality of lambda forces r(eta_1)=r(eta_2)=lambda. An extreme point of L exists by the compact-convex extreme-point theorem, and being extreme in a face makes it extreme in K_E. Thus every extreme invariant state downstairs has an extreme invariant lift upstairs.

Applying this to the injected free products proves that the tested independence relation is preserved from smaller to larger C*-ambient algebras. The finite counterexample shows that the converse fails. There is no contradiction: r(ext(K_E)) can contain nonextreme elements of K_D while also containing every extreme element of K_D.

Consequently the *specific proposed missing-lift mechanism* in source item (1) is unavailable in this C*-setting, while *ambient dependence of the actual relation* still occurs there. The authored proof explicitly distinguishes these statements; this audit confirms the distinction.

## 6. Literal algebraic nonextension and its limits

Let R=C[x] with x*=x and S=C[x,x^{-1}] with self-adjoint inverse. The inclusion is unital and injective. Evaluation at zero gives a character chi of F(R), obtained by setting x to zero in every copy. Characters are pure: their quotient is C with its unique state, and the quotient-purity proof applies. They are exchangeable under uniform evaluation.

If a positive unital extension eta to F(S) existed, X=j_1(x) and Y=j_1(x^{-1}) would satisfy X*=X, Y*=Y, XY=1, and eta(X*X)=0. Cauchy–Schwarz gives

    |eta(Y*X)|^2 <= eta(X*X) eta(Y*Y),
    so 1 <= 0.

This rules out every positive extension, with no exchangeability or extremality hypothesis needed upstairs. Both original ambient algebras have states, for example evaluation at 1. For a state-preserving probability-space inclusion based on evaluation at 1, the forbidden chi is not the specified full marginal; that is legitimate for the source's unrestricted invariant state sets, but must not be sold as failure to extend that prescribed marginal. The finite matrix example separately provides the actual state-preserving independence counterexample.

The Laurent construction is not a C*-counterexample. Its evaluation-zero state cannot be continuous on a C*-algebra in which the represented x is invertible. The argument exploits absence of the ordinary C*-state extension theorem for arbitrary algebraic *-algebras. This category distinction is explicit in the original claim and causes no mismatch.

## 7. Boundary cases and falsification results

The C^2 diagonal inclusion into M_2 works with B=C=A, state phi(a,b)=(a+b)/2, and the pure vector extension associated with (1,1)/sqrt(2). The same-copy multiplication of the repeated subalgebra forces cross-copy moments of the projection r to equal 1/2; the GNS argument again gives the unique two-character mixture. The lower state is faithful since both point masses are strictly positive. The source does not require B and C to be distinct. The M_4 example removes their coincidence at the cost of lower nonfaithfulness. The upper vector states are not faithful, which is allowed by the actual definition.

Merely adding the condition omega o j_i=phi for every whole copy while retaining extremality in K_A does not invalidate the example: the forced downstairs mixture has exactly those marginals, and the upstairs witness has marginals phi'.

Changing the *set in which extremality is evaluated* does invalidate this example. In fact the downstairs mixture is extreme in the set of all states with the prescribed full marginal, even before demanding exchangeability. To see this, let h:F(A)->C^2 evaluate uniformly at 00 and 11. The mixture is the faithful half-half state pulled back by h. Any positive convex decomposition factors through h, because every kernel element has zero squared norm in both constituents. The prescribed marginal value on p forces each constituent's weight to be 1/2, so both constituents equal the mixture. Thus a fixed-full-marginal-extremality reformulation makes this example independent downstairs too. The author only warns that its proof cannot be reused; the stronger statement here is an independently proved scope boundary, not a repair requirement.

The example does not establish ambient dependence with faithful states on all ambient algebras, tracial witnesses, von Neumann free products with normality conventions, or globally commutative ambient extensions. These are excluded modifications, not hidden assumptions in the printed definition. No unsupported de Finetti theorem or tail-algebra classification is needed.

## 8. Artifacts, evidence, and remaining gap

`verify_extension.py` is a new standard-library-only exact rational control, independent of the author's checker. It verifies the algebra and subalgebra dimensions, scalar intersection, matrix density purity data, restriction, endpoint law, finite word identities through length 12, representative multi-copy collapse identities, and the minimal faithful C^2 variant. Its output is `CHECKS.json`. These computations do not prove any all-state or infinite-copy quantifier; Sections 2–7 give the mathematical proofs.

`SOURCE_RECEIPT.json` pins the frozen authored inputs and independently downloaded official PDF. Full source text and renders are under ignored `tmp/`, so only hashes and the audit's own paraphrases remain in the public artifact set. `RESEARCH_LOG.md` records timestamped checkpoints with completion estimates. `MANIFEST.json` seals the reviewer-created records, with its own self-hash excluded.

Strongest verified result: the stated finite matrix inclusion is a complete counterexample to ambient invariance for the unrestricted whole-state, extreme-exchangeable free-product definition, in both algebraic and universal C* categories. The independent polynomial example also proves the literal unrestricted algebraic non-lifting obstruction. **Exact remaining mathematical gap in this assigned approach family: none found.** Historical priority is outside this subtask; the source-category modifications listed above are not claimed solved.
