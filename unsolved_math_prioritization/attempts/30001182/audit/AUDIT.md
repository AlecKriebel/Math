# Independent adversarial audit: 30001182

Date: 2026-10-04. Target: OWR-3392-009, rank 559.

## Verdict

**PASS. No blocking mathematical defect found.** The frozen proof gives a complete counterexample to ambient invariance under the printed extremal-exchangeable definition. Its four-point example works with distinct proper subalgebras having scalar intersection, for both algebraic and universal unital C*-free products. The separate Laurent-polynomial argument correctly establishes non-lifting in the unrestricted algebraic category.

The candidate disposition **claimed_solved, 1/5 substantive author turns** is supported. No additional author turn or repair is required by this audit. This is an independent AI-assisted mathematical review, not formal certification or human peer review. No historical novelty is certified.

Audited author manifest SHA-256:

`b021e926e34ae33bfb761b158d69d18355eddaad87331e2585d0e4977b971a90`

All seven author files matched their recorded lengths and hashes before and after review. They were not changed. The accompanying receipt records the individual checks.

## Source and interpretation gate

The [official OWR report](https://publications.mfo.de/bitstream/handle/mfo/3111/OWR_2009_09.pdf?isAllowed=y&sequence=1) was independently downloaded, hash-checked, and visually inspected at printed pp. 540-541. The contribution uses the unital free product and ordinary finite-permutation invariance. Independence requires equality of the entire induced states on B*C. The printed definition does not prescribe extremality in a fixed-marginal slice, faithfulness, traciality, or a trivial tail algebra. Item (1) motivates ambient dependence through a possible failure to lift extreme invariant states; those two issues need not be equivalent. The adjacent questions are not automatically resolved by this counterexample.

The [DKW version-3 preprint](https://arxiv.org/pdf/1305.7293v3) was also independently downloaded and hash-checked. Proposition 8.7 and its proof, Theorem 8.1 and its proof, and the adjacent fixed-marginal Theorem 8.9 were inspected. The proposition explicitly supplies the folding/maximal-amalgamation construction; Theorem 8.1 relates the relevant ordinary and quantum symmetric extremality. The packet credits this established mechanism appropriately, and its elementary proof does not rely on the classification machinery.

Both freshly downloaded PDF lengths and SHA-256 values agree with SOURCE_HASHES.json. Third-party PDFs, page images, and extracted text are not part of the audit deliverables. Historical novelty, exhaustive literature coverage, and the reported repository search history are not certified by this mathematical audit.

## 1. Exhaustion of every downstairs witness

This is the decisive point: showing only that the obvious folded state is nonextremal would be insufficient. The submitted proof does more.

Let p(s,t)=s and q(s,t)=t in A=C({0,1}^2), with the state assigning mass 1/2 to 00 and 11. Suppose omega is any exchangeable state satisfying the required joint-law equality. In its algebraic GNS representation, write P_i and Q_i for the copies of p and q, and Omega for the cyclic vector.

The joint-law equality supplies both ordered mixed moments from the two designated copies, as well as the single-letter moments. A finite permutation carries the ordered pair of designated indices to any ordered pair i,j with i unequal to j. Thus

- omega(P_i)=omega(Q_j)=1/2;
- omega(P_i Q_j)=omega(Q_j P_i)=1/2 whenever i is unequal to j.

Consequently the squared norm of P_i Omega minus Q_j Omega is zero for every such pair. No commutation between different copies is assumed here: both ordered moments have been justified separately.

For any i,k, choose j outside {i,k}. This gives P_i Omega=Q_j Omega=P_k Omega. Each Q_j Omega also equals this same vector, say v. The availability of a third copy is essential and is justified by the infinite-copy setting.

Every generator R among the P_i and Q_i satisfies R Omega=v and Rv=R^2 Omega=R Omega=v. Starting at the rightmost letter, induction therefore gives

R_1 ... R_m Omega=v

for every nonempty finite generator word, regardless of repeated indices, order, or alternating pattern. Every such moment is 1/2. Since 1,p,q,pq span each individual copy of A, the identity and these words span its entire algebraic free product. Hence this determines the state on every element, not merely on a tested truncation.

Let chi_0 and chi_1 evaluate every copy at 00 and 11 respectively. They are distinct positive unital exchangeable characters. The forced state is exactly

omega=(chi_0+chi_1)/2.

The two components differ on the first-copy p, so this decomposition is genuinely nontrivial in the convex set of all exchangeable states. This excludes every possible extreme witness. In the C*-completion, equality extends from the dense algebraic free product by continuity.

### Algebraic GNS domain check

The proof is not silently invoking a bounded-operator GNS theorem for arbitrary *-algebras. For a positive functional eta, Cauchy-Schwarz shows that eta(x*x)=0 implies eta(y*x)=0 for every y. Taking y=a*a x gives eta(x*a*a x)=0, so the null space is a left ideal. Left multiplication is therefore well defined on the quotient pre-Hilbert space. Every vector and product used in the argument belongs to that invariant algebraic domain. The projection identities and the induction are legitimate there; no completion, faithfulness, or unbounded-domain interchange is needed.

## 2. Upstairs witness and full ordered joint law

The diagonal inclusion into M_4 is unital and injective. The vector state of v=(e_00+e_11)/sqrt(2) restricts to the specified four-point state, including on every function in A. Its rank-one density projection has the claimed off-diagonal coherence and is not the diagonal mixture.

The matrix vector-state purity lemma is correct. If its state is a proper convex combination, each component vanishes on 1-vv*. Cauchy-Schwarz kills the off-corner terms, and the rank-one corner identity forces both components to equal the original state.

The quotient lemma is also valid for arbitrary unital *-algebras. In a convex decomposition of the pullback of a pure state through a surjective *-homomorphism, each component vanishes on every kernel element by positivity and Cauchy-Schwarz. Each component therefore descends to a positive unital functional on the quotient. Purity there makes the decomposition trivial. In particular the folded matrix state is pure among all states of the free product, a stronger conclusion than extreme exchangeability.

The folding homomorphism is surjective because any one canonical copy maps identically onto M_4. Relabeling the copies leaves folding unchanged, proving exchangeability for every finite permutation and every word. It also gives exactly the prescribed matrix-state marginal on each entire copy.

For an arbitrary element of B*C, each B-letter is placed in copy 1 and each C-letter in copy 2. Folding multiplies those original matrices in the same order. Restriction of the vector state then gives the original phi-law. This verifies the full state identity, including adjoints, arbitrary coefficients, and all word lengths. A second-moment calculation alone is not being substituted for the required law.

The coordinate subalgebras are distinct and proper: each has dimension 2, while their linear span has dimension 3 inside the four-dimensional ambient algebra. Their intersection is precisely the scalars. These facts and the inclusion/state restriction also reproduce directly in the exact controls.

## 3. Ambient dependence versus non-lifting

The main example changes independence from false downstairs to true upstairs. Its upstairs witness restricts to the unique nonextremal downstairs state. This is a loss of extremality under restriction, not an example of failure to extend an extreme downstairs state. The proof labels that distinction correctly.

The independent algebraic example has R=C[x] contained in S=C[x,x^-1], with x and x^-1 self-adjoint. Evaluation at zero on every R-copy is an exchangeable character, hence pure. Any positive extension to the S-free product would have, in its first copy, eta(X^2)=0 and eta(XY)=eta(1)=1. Cauchy-Schwarz gives 1 <= eta(X^2)eta(Y^2)=0, an immediate contradiction. The functional is defined on the whole algebra, so eta(Y^2) is a finite scalar; there is no hidden integrability exception.

This proves no positive extension exists, even without asking for exchangeability. The polynomial inclusion is not a C*-inclusion. Both algebras have other states, for example evaluation at one, but the nonextendible character is not that common ambient marginal. The packet expressly acknowledges this and does not claim a fixed-marginal extension counterexample.

The contextual C*-extension argument is sound: extend a state, average over the increasing finite symmetric groups, and take a weak-* cluster point. The invariant extension fiber is compact and nonempty. If its restriction is extreme invariant, that fiber is a face of the full invariant state space; an extreme point of the fiber is therefore extreme in the full invariant state space. This does not prevent the opposite-direction restriction failure shown by the main example.

## 4. Scope and adversarial variants

- **Infinite quantifiers:** The universal GNS argument covers every candidate state and every finite word in arbitrarily many copies. It is not an inference from the finite verifier.
- **Extremality set:** The conclusion is for extremality among all exchangeable states, exactly as used in the proof. Requiring the correct full marginal while retaining that extremality set does not invalidate the counterexample.
- **Fixed-marginal extremality:** Changing the convex set is substantial. In fact the folded state with marginal phi is extreme in the fixed-marginal state set: a decomposition must descend through folding, and both descended marginals are then forced to be phi. This reinforces, rather than repairs, the submitted warning not to claim the same result for that alternate definition.
- **Faithful, tracial, or normal variants:** No conclusion for faithful-only or tracial-only definitions follows. The witnesses are normal in their finite-dimensional ambient algebras, but that does not specify a normal W*-free-product theory.
- **Known mechanism:** Pure folding is established prior work. Neither the proof nor this audit supports claiming a historically new solution.
- **Smaller example:** The stated C^2-in-M_2 variant also works when coincident subalgebras are allowed. It is not needed to validate the distinct-subalgebra theorem.

No blocking repair or author-file edit is requested.

## 5. Reproduction and integrity

The frozen standard-library verifier was read and executed unchanged. Its output matched checks.json byte-for-byte: **14,944 exact rational assertions passed**. In particular the 5,461 pair-word controls and 9,330 projection-model controls are finite, supplementary checks. The latter explicitly instantiate already-collapsed projections, so they cannot establish the all-candidate GNS collapse by themselves. The report and author proof correctly reserve that conclusion for the argument above.

REPLAY_CHECKS.json records that deterministic output. AUDIT_RECEIPT.json records source-byte checks, author-file integrity, and review scope. AUDIT_MANIFEST.json pins the audit deliverables without modifying the author freeze. No remote repository state was changed during this audit.
