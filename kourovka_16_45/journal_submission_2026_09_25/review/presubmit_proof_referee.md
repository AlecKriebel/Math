# Final independent adversarial proof review

**Verdict: no substantive mathematical defect found. No mathematical correction is required by this review.**

The manuscript proves the stated exact values

\[
G=\mathbf F_{29}^{,2}\rtimes\langle A,B\rangle,
\qquad |G|=100920,
\qquad b_{\mathrm f}(G)=b(G)=3<4=\mu'(G),
\]

under its explicit conventions: bases are inclusion-minimal, they are taken for the permutation image, and arbitrary intransitive and nonfaithful actions are allowed. I found no missing class of actions or subgroups in the universal upper bounds.

## Identity and independence of this review

- Reviewed file: `manuscript/kourovka_16_45.tex` in this submission folder.
- Current source SHA-256: `98c5263a75670d694009a566b2b4578ee42fc579c854e3fecf18f88b05e88fd3`.
- Current mathematical payload SHA-256: `edd472fbabb18b1c07e1fba088a39eccf0656dfe2d32baf7835cdc4268514fd4`.
- Baseline source SHA-256: `88127081c7f705d5099cfc2b95680cee9a52e187acd3df75712d829663797606`.
- Baseline mathematical payload SHA-256: `f183c53d8126b0ac23af28675ad24bae5619221b000e802479dfadb1520ffaf2`.
- Payload convention: exact UTF-8 bytes from `\begin{abstract}` inclusive to the heading `\section*{Reproducibility and use of artificial intelligence}` exclusive. This includes the abstract, introduction, theorem, and every mathematical proof. Byte-for-byte copies are retained in `tmp/presubmit/proof/reviewed_mathematical_payload.tex` (baseline) and `reviewed_mathematical_payload_current.tex` (current). The reviewed delta is documented below.
- The manuscript was read before any other mathematical material. No earlier review, existing verification implementation, supplementary proof, or external source was used to derive the structural verdict.
- A separate agent independently transcribed the concrete witnesses into fresh exact arithmetic code. Its work corroborated, rather than supplied, the structural upper-bound arguments.
- No manuscript edit, commit, push, submission, or external contact was made.

## Claim, success criterion, and boundary cases

The target conclusion was treated as a hypothesis. Success required independent checks of (i) the matrix complement and its invariants; (ii) every possible subgroup missing the translation subgroup; (iii) every possible action kernel; (iv) universal bounds applying to independent subsets that need not generate the ambient group; and (v) concrete lower-bound witnesses. A check only of the displayed affine action, only of faithful actions, or only of irredundant generating sets of the whole group would have been insufficient.

The boundary cases checked include the trivial group and trivial action, empty and singleton subgroup families, the identity subgroup and odd prime-order subgroups of the complement, a trivial scalar complement, subgroups with zero or one-dimensional translation intersection, repeated or identity images in the central quotient, and infinite permutation domains for a finite group. None introduces an exception to the stated bounds.

## Re-derived dependency chain

### 1. Bases, kernels, restriction, and monotonicity

For point stabilizers of an inclusion-minimal base, their total intersection equals the action kernel and omission of any one stabilizer strictly enlarges it. Conversely, the action on the disjoint union of the coset spaces has kernel

\[
\bigcap_i\operatorname{Core}_X(L_i)
=\operatorname{Core}_X\!\left(\bigcap_iL_i\right).
\]

When the intersection is normal this is exactly that intersection; the selected identity cosets give a minimal base. Thus the normality requirement in Proposition 2 is justified rather than assumed. For a trivial action the empty family has ambient intersection \(X\), giving base size zero; for a nontrivial group the singleton family \(\{1\}\) gives a faithful base of size one. Passing to the action kernel proves the maximum-over-quotients formula.

If a family is meet-irredundant, witnesses \(x_i\in\bigcap_{j\ne i}L_j\setminus L_i\) are independent because every other witness belongs to \(L_i\). Conversely, deleting one generator of an independent set gives the requisite subgroup family. This handles independent sets in proper subgroups as well as generating sets of the ambient group.

On restriction to \(L_i\), the witness for \(L_j\), for every \(j\ne i\), still belongs to \(L_i\). Hence the restricted family remains irredundant, and its total intersection is unchanged. For \(t=1\), the restricted family is empty and its ambient intersection is \(L_i\), exactly as required; if the original intersection was trivial then \(L_i=1\). There is no lost boundary case in either restriction inequality.

Subgroup monotonicity of \(\mu'\) follows directly from independence. Subgroup monotonicity of \(b_{\mathrm f}\) follows by viewing a family with trivial total intersection as the same family of subgroups in a larger group. For a singleton, the deletion intersection only becomes larger, so this also causes no exception. The zero value at the trivial group handles an empty family. No unsupported monotonicity assertion about the all-actions invariant is used later.

The stated Boolean map preserves meets since complementing an intersection of index sets forms their union. Each witness distinguishes images with different index sets; the empty ambient intersection ensures that the top maps to \(X\). A normal bottom therefore gives exactly a family of the kind covered by the base bound, without a join-preservation assumption.

A minimal base on an infinite domain is still finite: for each nonidentity element of the finite permutation image, choose a point moved by that element **from the given base**. The finite selected subset is itself a base, so minimality forces equality. This validates the finite-family arguments for all permitted domains.

### 2. The matrix complement and the \(A_5\) inputs

The matrices have determinant one; \(A^2=B^3=(AB)^5=-I\) puts \(Z=\{I,-I\}\) inside \(H\). The displayed spherical triangle presentation gives a surjection from \(A_5\) to \(H/Z\). Since \(A\notin Z\), that quotient is nontrivial, and simplicity forces it to be \(A_5\). Thus \(|H|=120\). These deductions do not assume the sought order in advance.

The proper-subgroup argument for \(A_5\) is complete. An intransitive subgroup either fixes a letter or preserves a partition of type \(2+3\); it then lies in \(A_4\) or \((S_2\times S_3)\cap A_5\cong S_3\). A proper transitive subgroup has order \(5,10,15,20\), or \(30\). Orders \(15\) and \(20\) force a normal Sylow 5-subgroup and contradict its order-ten normalizer; index two rules out order \(30\). The remaining possibilities lie in that normalizer. In particular, there is no unhandled proper subgroup carrying a larger independence invariant.

For \(A_4\), any generating family of the whole group includes a 3-cycle and an element outside its cyclic subgroup; these generate because there is no subgroup of order six. Its proper subgroups have independence invariant at most two. The prime-rotation dihedral argument handles both \(S_3\) and \(D_{10}\), including their proper subgroups. Deleting one element of an independent set in \(A_5\) generates a proper subgroup, and hence gives the bound three. Fixing three points in the natural five-point action gives trivial stabilizer while fixing two leaves a subgroup of order three, proving equality.

### 3. All three invariants of \(H\)

In odd characteristic, a matrix squaring to the identity is diagonalizable with eigenvalues in \(\{1,-1\}\). In determinant one and dimension two, a nonidentity such matrix must be \(-I\). Thus every even-order subgroup of \(H\) contains \(Z\); a subgroup omitting \(Z\) is odd and projects injectively into \(A_5\), so it is trivial, cyclic of order three, or cyclic of order five.

For an independent indexed set \(S\subseteq H\), dependence of its images modulo \(Z\) means that one \(s\) lies in \(KZ\), where \(K=\langle S\setminus\{s\}\rangle\). Independence in \(H\) excludes \(s\in K\); hence \(Z\not\subseteq K\). The preceding classification makes \(\mu'(K)\le1\), giving \(|S|\le2\). This also covers coincident quotient images and an identity quotient image. If the images are independent, the \(A_5\) bound gives \(|S|\le3\). No unjustified lifting of independence from a quotient is being used.

The pullback of the natural \(A_5\) action supplies a minimal base of size three with kernel \(Z\). Together with the independent-set bound this gives \(b(H)=\mu'(H)=3\).

For a family in \(H\) with trivial total intersection, some member must have odd order. If that member is trivial, an irredundant family has size one. If it has odd prime order, intersection with some other member is already trivial; irredundancy limits the whole family to two members. Subgroups of orders three and five exist by Cauchy's theorem and give a two-member irredundant family. Thus \(b_{\mathrm f}(H)=2\), with no assumption that the associated action is transitive.

### 4. Scalar lemma and subgroups missing \(V\)

In the scalar lemma, a subgroup intersecting \(P\) trivially injects into the cyclic 2-group, so a largest-order element of any generating set already generates it. A subgroup containing \(P\) is the full preimage \(P\rtimes D\) of its projection; the standard copy of \(D\) is present because any translation component can be removed using \(P\).

When \(D\ne1\), its unique maximal subgroup ensures that a generating set contains an element whose projection generates \(D\). Its scalar \(\lambda\ne1\) has geometric sum zero over its order, so the element has precisely the order of \(D\) and generates a complement. Any second generator outside that complement must, together with it, generate a subgroup meeting \(P\) nontrivially; otherwise projection would be injective and force the same complement. Since \(|P|\) is prime, this yields all of \(P\rtimes D\). When \(D=1\), the group is cyclic of prime order. The argument therefore proves the bound for **every subgroup**, which is what \(\mu'\) requires.

For a line stabilizer in \(H\), the kernel of scalar restriction consists of unipotent matrices \(\left(\begin{smallmatrix}1&u\\0&1\end{smallmatrix}\right)\). A nonidentity such matrix has order 29, impossible in \(H\). Restriction is injective, and its order divides both 120 and 28, hence divides four. This proves irreducibility of \(H\) and the faithful cyclic 2-group action needed by the scalar lemma.

Every additive subgroup of \(\mathbf F_{29}^2\) is a subspace because 29 is prime. Thus if \(K\not\supseteq V\), its intersection with \(V\) is either zero or a line; there is no third case. In the zero case, projection embeds \(K\) in \(H\), so \(b_{\mathrm f}(K)\le2\) and \(\mu'(K)\le3\). In the line case, \(\pi(K)\) has order dividing four. A Sylow 2-subgroup of \(K\), including the trivial one when appropriate, projects isomorphically onto \(\pi(K)\) and complements the order-29 subgroup. Its scalar action is faithful by the injectivity just proved. The scalar lemma gives \(\mu'(K)\le2\), and hence \(b_{\mathrm f}(K)\le2\).

### 5. Universal faithful and nonfaithful upper bounds

A subgroup family with trivial intersection cannot have every member containing the nontrivial subgroup \(V\). Selecting one member missing \(V\) and restricting to it yields

\[
t-1\le b_{\mathrm f}(K_i)\le2.
\]

This proves the faithful upper bound for every permitted action. It does not presume the stabilizers are complements, maximal subgroups, or conjugate to one another.

If \(N\lhd G\), then \(N\cap V\) is an \(H\)-invariant subspace. If it is trivial, normality of both groups gives \([N,V]\le N\cap V=1\). Faithfulness of the displayed matrix action gives \(C_G(V)=V\), so \(N\le V\), forcing \(N=1\). Consequently every nontrivial normal subgroup contains \(V\). Every nonfaithful action, including a trivial action, factors through \(G/V\cong H\); since the invariant \(b(H)\) already allows every further kernel, its bound three applies. This closes the all-actions gap without assuming that a quotient preserves independence bounds.

For the upper bound on \(\mu'(G)\), if every subgroup in a meet-irredundant family contains \(V\), the subgroup correspondence with \(H\) preserves strictness and irredundancy, giving size at most three. Otherwise restriction to a member missing \(V\) gives \(t-1\le\mu'(K_i)\le3\). These are exhaustive cases. The argument applies to arbitrary total intersection and to independent sets generating proper subgroups.

### 6. Lower bounds and the explicit nonnormal bottom

The fresh arithmetic check confirms both word identities for \(R_2,R_3\), all three squares \(-I\), product orders \(4,3,10\), and projective product orders \(2,3,5\). The respective pair subgroups have orders \(8,12,20\). Their least common multiple is 120, so the three elements generate \(H\); every pair is proper, proving independence. The first two pair subgroups intersect in \(\langle R_3\rangle\) by the order-four lower bound and the greatest-common-divisor upper bound. The third contains \(Z\) but not \(R_3\), so the triple intersection is exactly \(Z\).

Projection prevents any displayed linear generator of \(G\) from being generated by the other three displayed generators, and the nonzero translation lies outside the zero-translation complement. Thus the displayed four-set is independent. The orbit-span argument then proves generation of \(G\); as an additional check, \(Ae_1=e_2\) already supplies both translation directions once \(H\) is generated.

The three affine subgroups used for the faithful lower bound have the explicit forms

\[
\begin{aligned}
L_1&=\{(te_1,I),(te_1,-I):t\in\mathbf F_{29}\},\\
L_2&=\{(te_2,I),(te_2,-I):t\in\mathbf F_{29}\},\\
L_3&=\{(t(e_1+e_2),I),(2e_1+t(e_1+e_2),-I):t\in\mathbf F_{29}\}.
\end{aligned}
\]

Their translation lines meet pairwise only at zero. Their negative-linear-part cosets meet at the three respective vectors \(0,2e_1,-2e_2\). These give exactly the stated order-two pair intersections and trivial triple intersection. The assumption that the characteristic is odd is respected: \(2\ne0\) in this field is essential and satisfied. Their orders are 58, and the disjoint coset action has degree \(3\cdot100920/58=5220\). This is a genuine faithful inclusion-minimal base of size three.

For the four subgroups obtained by deleting one element of the independent four-set, each matrix pair of order greater than four acts irreducibly: a preserved line would put it in a line stabilizer of order at most four. Therefore the translation orbit spans \(V\) and the three subgroups involving the translation are exactly the claimed preimages under projection. Intersecting them with the complement gives exactly \(Z_0\). Conjugation by \((e_1,I)\) sends \((0,-I)\) to \((2e_1,-I)\), proving nonnormality.

Each proper matrix pair contains \(Z\), and its quotient is proper in simple \(A_5\); its core is therefore exactly \(Z\). Taking preimages gives core \(V\rtimes Z\). The complement has trivial core by the established normal-subgroup argument. Thus the four-core calculation is also correct and does destroy irredundancy.

## Adversarial route ledger

| Potential failure mechanism | Check and evidence | Status / remaining gap |
|---|---|---|
| Intransitive or infinite actions evade the subgroup family bound | Disjoint-coset equivalence and finite subbase argument checked directly | Closed within the manuscript's definitions |
| Restriction loses a witness or fails for a singleton | Each remaining witness lies in the restricted ambient subgroup; empty intersection checked | Closed |
| Faithful invariant is not subgroup-monotone | The same nonempty trivial-intersection family works in the larger group; zero boundary handled separately | Closed |
| An independent set in \(H\) loses independence modulo \(Z\) while retaining large size | Such loss forces the other generators into a subgroup omitting \(Z\), which is cyclic of odd prime order or trivial | Closed |
| The scalar proof only covers generating sets of the whole scalar group | It classifies an arbitrary subgroup first and proves the two-generator bound there | Closed |
| A subgroup missing \(V\) has an unclassified translation intersection or nonsplit extension | Prime-field subspace classification and Sylow complement give exhaustive alternatives | Closed |
| A nontrivial kernel avoids \(V\) | Irreducibility plus the centralizer identity forces that kernel to be trivial | Closed |
| \(\mu'(G)\) upper bound silently requires generation of \(G\) | Meet-irredundant formulation is valid for every independent subset | Closed |
| Displayed witnesses or word identities contain arithmetic errors | Fresh exact check of 29 named assertions; small closures only | Closed for the displayed finite data |
| The rank-four intersection is actually normal, or normal cores retain its rank | Direct conjugation and core computations contradict those alternatives | Closed |

No route in this proof transfers the central difficulty to an equivalent unsupported upper-bound assertion. The key reductions terminate in cyclic prime-power groups, the elementary subgroup structure of \(A_5\), and explicitly verified finite arithmetic.

## Arithmetic artifacts and reproduction

The independent exact arithmetic audit passed all 29 named assertions. It enumerated only the 120-element matrix group, the three named matrix pair subgroups, and the three order-58 affine subgroups. It did not enumerate \(G\) or any subgroup lattice, and no large search was repeated.

Artifacts, relative to this submission folder:

- `tmp/presubmit/proof/arithmetic/check_witnesses.py`
- `tmp/presubmit/proof/arithmetic/results.json`
- `tmp/presubmit/proof/arithmetic/REPORT.md`
- `tmp/presubmit/proof/reviewed_mathematical_payload.tex`
- `tmp/presubmit/proof/reviewed_mathematical_payload_current.tex`
- `tmp/presubmit/proof/final_hash_check.json`
- `tmp/presubmit/proof/review_log.md`

The arithmetic script uses only Python's standard library and exact arithmetic modulo 29. From the repository root it can be run with:

```sh
python3 kourovka_16_45/journal_submission_2026_09_25/tmp/presubmit/proof/arithmetic/check_witnesses.py
```

## Required fixes and scope limitations

**Required mathematical fixes: none found.** I do not recommend adding manuscript qualifications to repair any of the attempted counterexamples above, because the present arguments already cover them.

This review is a proof audit by AI agents, not external peer review or formal proof-assistant certification. Standard elementary finite-group facts used in the proof include Lagrange's theorem, Sylow theory, Cauchy's theorem, the spherical triangle presentation of \(A_5\), and its simplicity. The review re-derived the applications and checked their hypotheses; it did not formalize those standard theorems from axioms. It does not establish novelty, priority, the current status or wording of the notebook problem, bibliographic accuracy, journal eligibility, or correctness of the separate supplementary software. Those matters require their own scoped checks. The verdict applies to the exact mathematical payload identified above; a substantive later change needs renewed review.

## Reviewed source delta

While this review was being completed, the parent agent made a small historical-wording update: the introduction now says the question is posed in the cited sources, without asserting a current unsolved status from the absence of a printed solution comment. The reproducibility section identifies the archived document as an earlier version and notes its hosting in the notebook's online repository. I read the full source diff independently. These changes alter no definition, hypothesis, claim, construction, or proof. An exact comparison confirms that the byte sequence from the main theorem through the end of the mathematical sections is unchanged. The only change inside the hashed mathematical payload is the introductory historical sentence. The current source and payload hashes above were independently recomputed; the verdict therefore also applies to the current file. The external hosting claim itself belongs to source verification, outside this mathematical review's scope.

Final recorded checkpoint, verified with `clock__curr_time`: **2026-09-26 05:04:18 UTC** (2026-09-25 22:04:18 America/Los_Angeles). This is the recording time of the completed review and timestamp audit, not an estimate of the precise instant the mathematical reasoning ended. Best-guess completion toward the assigned final independent mathematical review: **100%**. Strongest verified result: the full stated theorem and normality-obstruction explanation, with no substantive defect found. Exact remaining mathematical gap identified by this audit: **none**; the scope limitations above remain.
