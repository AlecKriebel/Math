# Fresh adversarial audit of the 21.139 partial results

Audit completed: **2026-10-24 16:37:09 UTC**. Scope: the exact problem in `PROBLEM.md`, Section 6 of `approach_geometry.md`, the amplification and right-angled Coxeter arguments in `approach_counterexamples.md`, the existing independent cover computation, the proposed retract obstruction, and the subsequently requested degree-seven coefficient check. This is a bounded mathematical audit, not a new solution or a novelty/priority determination.

**Verdict:** PASS for the stated conditional equivalence **(K) iff (Z2)**, with the cutting convention made precise below; PASS for amplification and the restricted RACG deduction; PASS for malnormality of retracts in torsion-free hyperbolic groups. **The unrestricted problem remains unresolved.** Treating (Z2), or virtual second-homology positivity for one-ended groups, as proved would be a fatal gap. Malnormality obstructs the specified conjugate-copy construction only inside a retraction host.

Audit completion estimate: **100% of this assigned audit**. Best-guess completion toward solving the full problem: **18%**, retaining the geometric checkpoint estimate; this is a planning estimate, not a probability that the conjecture is true.

No external person was contacted; no outreach was prepared. No Git operation, queue edit, release, or publication was performed. Only this separate review file was added.

## 1. Exact claims and pass criteria

All homology is over Q, and

    vb2(G) = sup{b2(L) : L <= G, [G:L] < infinity}.

(K) is the original implication: hyperbolic and virtually compact special, with finite vb2, implies virtually free or virtually a closed surface group. Finite groups and virtually cyclic groups belong to the virtually free conclusion.

(Z2) is the universal assertion that a hyperbolic compact special group with rational cohomological dimension at most two and vb2 = 0 is free. It is an additional hypothesis in the forward reduction, not an established theorem in the package.

The audit passes an equivalence only if it preserves the all-finite-index quantifier, provides the geometric hierarchy without assuming the desired classification, and does not descend a finite two-dimensional classifying space through a finite extension without proof.

## 2. Cutting lemma: PASS with a coherent cut model

The claim is: if a finite NPC special cube complex X has embedded two-sided hyperplanes, all with free fundamental groups, then pi1(X) has a finite classifying complex of dimension at most two. No finite-index descent is required for this lemma.

Here is a precise convention under which the proposed mechanism works. Subdivide as necessary to handle cubes as embedded cells. Retain the specified original mid-hyperplanes as the cutting loci. Cut a complex at a mid-hyperplane by duplicating its two boundary sides. For the graph of spaces, replace the identification of these sides by a hyperplane times an interval; a product collar identifies this model up to homotopy with the original gluing. Convexity is checked for the zero-width midplane cut, not for arbitrary shapes of a removed collar. A global subdivision makes the half-cube corners into subcomplexes. Subdivision is a change of cell structure; it does not change the dimension or fundamental group. If instead a full open cubical carrier is removed, the terminal pieces may be smaller than the truncated chambers described in Section 6. These two descriptions should not be silently identified. The midplane convention supplies the stated chamber proof.

The following checks establish the group-theoretic conclusion independently of that terminology.

1. **Subsequent pieces and cut groups inject.** Upstairs, after any collection of the specified cuts, a lift of a current piece is the intersection of chosen closed halfspaces. It is convex. A lift of a component of a subsequent cut is its intersection with an elevation of the next original hyperplane. That intersection is convex both in the ambient CAT(0) space and in the elevation. Local isometry, or the resulting convex lift, proves pi1-injectivity into the original hyperplane group. This applies to each component, including disconnected cuts and cuts that meet previous boundary faces. The cut spaces are finite, so their fundamental groups are finitely generated. A subgroup of a free group is free, and here its rank is finite. No assumption that a later cut remains an entire original hyperplane is needed.

2. **The hierarchy terminates in trivial groups.** There are finitely many original hyperplanes and finitely many components at each cut. After all cuts, each terminal chamber is obtained by gluing the compatible corners incident to one vertex. The contractions of these corners to that vertex agree on common faces. Alternatively, this conclusion can be checked without a cone description: any two distinct original vertices upstairs are separated by a hyperplane, so a terminal convex lift contains at most one original vertex. Every chamber contains such a vertex. A deck transformation stabilizing the chamber therefore fixes that vertex and is the identity. Since the chamber injects on pi1, its group is trivial. This also covers a loop edge downstairs: its two corner ends are separated upstairs, and no spurious terminal loop remains.

3. **Reverse the hierarchy in dimension two.** Start with points for terminal vertex groups. For each finite-rank free edge group use a finite graph as its classifying space. At a reverse step use the previously built finite classifying spaces for the vertex groups, choose maps realizing the specified injective edge homomorphisms, and attach edge graphs times intervals. The maps need not be embeddings or local isometries. Van Kampen gives exactly the original graph of groups. In its universal cover the vertex and edge spaces are contractible and the incidence graph is the Bass–Serre tree. A finite subtree gives a contractible homotopy pushout, by removing leaves. Every sphere maps into such a finite subtree of spaces and hence is null-homotopic. Thus the universal cover is contractible. Each reverse step has dimension at most max(2, 1+1) = 2, and remains finite.

This proves a finite two-dimensional K(pi1(X),1), and therefore cd_Z(pi1(X)) <= 2. No hyperbolicity is needed in the cutting lemma itself. Hyperbolicity enters later to supply quasiconvexity and the virtual retractions used to inherit vb2 = 0.

**Adversarial cases checked:** crossing hyperplanes; nonseparating cuts/HNN edges; disconnected later cuts; trivial hyperplane groups; loop edges and multiple corner incidences before subdivision; graph pieces of dimension zero; and arbitrary graph maps at the reconstruction stage. None invalidates the conclusion with the convention above.

## 3. Dimension induction and both directions of the equivalence: PASS

Assume (Z2), and induct on the dimension d of a finite compact special model X with hyperbolic fundamental group and vb2 = 0.

- At d <= 1 its group is free.
- For d > 1, an original hyperplane J is compact NPC and has dimension at most d-1. Its locally convex realization after subdivision inherits specialness. Its group is quasiconvex in the ambient hyperbolic group: its universal cover is convex, its action is cocompact there, and ambient word and CAT(0) orbit metrics are quasi-isometric.
- Rational virtual-Betti bounds pass to J by a virtual retraction. Crucially, for every finite-index T in the retract, the preimage of T under the retraction is finite-index in the host and retracts to T. Thus this is a bound on all covers of J, not a chosen collection.
- The induction hypothesis makes each hyperplane group free. The cutting lemma then gives cd_Q <= 2 for the ambient group under consideration, allowing the actual application of (Z2).

Under the older convention for specialness, a finite two-sided special cover can be chosen first, without increasing d. This only changes the eventual conclusion from free for that cover to virtually free for the original group. A torsion-free virtually free group is free: it acts on a tree with finite vertex stabilizers, which must be trivial. Consequently the induction closes. This argument does not claim that a finite two-dimensional classifying complex descends to the original finite extension.

For **(Z2) implies (K)**, pass first to a torsion-free compact special finite-index S. Unless S is free or a surface group, the checked [Wilton Theorem A](https://arxiv.org/html/2406.02121v3) supplies a one-ended infinite-index quasiconvex A. Amplification forces vb2(A) = 0 under boundedness of vb2(S). The compact special core theorem, after a finite-index passage if needed, supplies a finite-dimensional compact special model for A. The induction makes A virtually free. Ends are invariant under finite-index passage, and an infinite virtually free group has two or infinitely many ends. This contradicts one-endedness.

For **(K) implies (Z2)**, apply (K) directly. A virtually closed hyperbolic surface group has a finite-index orientable surface group, with b2 = 1, contradicting vb2 = 0. Thus the group is virtually free, and its torsion-freeness makes it free. This direction does not even use the dimension bound.

Rational virtual-Betti suprema are commensurability invariant: if S <= G has finite index, intersect an arbitrary finite-index L <= G with S, then use transfer to obtain b2(L) <= b2(L intersect S). This covers nonnormal finite-index subgroups too. The surface alternative includes a further orientation cover. These are the necessary bookkeeping steps, and they are present.

**Fatal gap if promoted beyond its scope:** neither the hierarchy nor the induction proves (Z2). The induction invokes it precisely after constructing the two-dimensional model. No class in H2 of a finite cover has thereby been produced. The equivalent one-ended virtual-positivity statement is likewise the remaining central difficulty, not a lemma available for completing the proof.

## 4. Amplification and RACGs: PASS

### Amplification

The hypotheses on Arzhantseva's Theorem 1 are all met after the stated passage: the ambient group is torsion-free, non-elementary and hyperbolic; A0 is infinite-index and quasiconvex. Non-elementarity follows already from b2(A0) > 0. The theorem supplies both the free product and quasiconvexity; merely exhibiting an abstract free product would not suffice.

For K = A0 * <t>, use one finite-index retraction host G' -> K. The kernel of K -> Z/n killing A0 is the free product of n conjugates of A0 and <t^n>. Its second Betti number is n b2(A0). Pullback through the retraction has index n in G' and retracts onto that kernel. Hence the displayed lower bound and index formula are correct for every n >= 1. A finite-index subgroup of A with positive H2 stays quasiconvex and infinite-index after the intersections used in the proof. Rational transfer preserves positivity. The finite-index host does not have to be changed separately for every n.

Removing the infinite-index hypothesis would be fatal: an orientable closed hyperbolic surface group is a counterexample to the purported amplification with A = G. Residuality of the constructed sequence is neither claimed nor needed. The construction supplies no first two-class when vb2(A) = 0.

### Hyperbolic right-angled Coxeter groups

For a finite defining graph Gamma with no induced square, the two cases exhaust all possibilities.

- A chordal Gamma has a simplicial vertex. The presentation decomposes W_Gamma as W_(Gamma-v) *_(W_link(v)) W_star(v), with the last two indicated clique groups finite. Iterating gives a virtually free group. Empty, complete, and disconnected graphs are included.
- Otherwise Gamma has an induced m-cycle C; absence of induced squares gives m >= 5. Its special subgroup is the compact right-angled hyperbolic polygon reflection group, hence has a finite-index orientable closed surface subgroup S. The standard-generator inclusion is isometric, because the retraction killing outside generators is 1-Lipschitz. Therefore W_C is undistorted and quasiconvex in the hyperbolic ambient group, and so is S.
- If an outside vertex v misses u in C, the retraction to the two nonadjacent generators u,v maps W_C into <u> in D_infinity. The cosets (vu)^j<u> are distinct. Thus [W_Gamma:W_C] is infinite, and amplification applies after the torsion-free passage.
- If every outside vertex sees every vertex of C, two nonadjacent outside vertices together with two nonadjacent cycle vertices would induce a square. Therefore the outside graph is a clique and W_Gamma = W_C times a finite elementary abelian 2-group. It is virtually a closed surface group.

Finite-index S inside W_C remains infinite-index in the third case. Commensurability invariance extends this restricted-class result to groups commensurable with these RACGs. Nothing in this graph argument classifies arbitrary compact special subgroups of RAAGs. That extension would be an unsupported new step.

## 5. Retracts are malnormal: PASS, with exact obstruction scope

Let r:G -> A be a retraction and G torsion-free hyperbolic. If z^k is in A for k > 0, then r(z)^k = z^k, and unique roots imply z = r(z) in A. For nontrivial x in A, write C_G(x) = <c> and x = c^m. Root closure implies c in A, hence C_G(x) <= A.

Write g = n r(g), with n in ker r. Then gAg^-1 = nAn^-1. If nontrivial x in A intersect nAn^-1, write x = nyn^-1 with y in A. Applying r gives x = y, so n centralizes x. Therefore n is in A intersect ker r = {1}, and g is in A. This is precisely malnormality.

The lemma is established background: [Myasnikov–Shpilrain, *Combinatorics over free groups*, p.70, Corollary 20](https://web.stevens.edu/algebraic/alexeim/Teaching/Math627_Fall_2005/Sections/book/ALLBOOK.pdf); see also [Goswami–Verma, Lemma 5.3](https://arxiv.org/html/2508.18223v1). The proof above explicitly uses a generator of the full centralizer; an element centralizing x need only be a power of its maximal root, not necessarily an integer power of x itself.

**Valid obstruction:** in a torsion-free finite-index host G' retracting onto A, two genuinely distinct conjugates A and gAg^-1 with g in G' cannot share a nontrivial cyclic group. If g is in A they are the same subgroup, so the proposed map of a proper amalgam to these coincident copies cannot be injective. Thus a retraction does not furnish the overlapping conjugate copy needed by the suggested commutator-double mechanism.

**Limits:** malnormality in G' says nothing by itself about conjugators outside G', nor about two embeddings of the same abstract group whose images are not conjugate. In particular it does not forbid every double construction. A concrete check is

    G = <a,b,c,d | [a,b] = [d,c]>.

This is the genus-two orientable surface group, a double of two rank-two free groups over their boundary commutator subgroups. The homomorphism fixing a,b and sending c to b, d to a retracts G onto A = <a,b>. Its other vertex group <c,d> has nontrivial intersection with A and is not a distinct conjugate of A. The example verifies the scope distinction without disputing malnormality.

Torsion-freeness is essential to the stated general lemma: projection F2 times C2 -> F2 is a retraction in a hyperbolic group, and its nontrivial finite central factor violates malnormality. Hyperbolicity/cyclic-centralizer control is essential too: the direct factor Z in Z squared is a nonmalnormal retract.

## 6. Existing exact-cover computation: inspected; no unnecessary replay

`reviews/partial_adversary01_checks.json` records completion at **2026-10-17T21:42:40.207541+00:00**. It did finish before the interrupted work stopped. The independent verifier rebuilds the 8-vertex, 24-edge characteristic mod-2 cover, chooses a spanning tree, and computes an integral 17-dimensional fundamental-cycle basis. It checks the automorphism and inverse, the cellular chain-map identity, reconstruction of cycles from the non-tree coordinates, and equality between homology-fixed-space and stacked-chain ranks.

| Monodromy power | Ambient subgroup index | Rank on H1 minus identity | b2 |
| --- | --- | --- | --- |
| 1 | 8 | 17 | 0 |
| 2 | 16 | 16 | 1 |
| 7 | 56 | 17 | 0 |
| 14 | 112 | 10 | 7 |

The JSON records successful replay of the separate root determinant certificate. Its saved root-script SHA-256 still equals the current root script. The code and result expose no unresolved concern requiring another execution, so I did not rerun either verifier or overwrite the old evidence. These checks certify the selected covers only; unboundedness for this free-by-cyclic family comes from the separate structural argument, not extrapolation of this table.

## 7. Additional degree-seven coefficient check: PASS

The coordinator subsequently requested an independent check of `root_artifacts/coefficient_change_degree7.json`. Direct integer multiplication of the original 3-by-3 monodromy matrix M gives

    M^7 - I = [[0,2,2],[2,2,4],[2,2,2]] = 2 M^4,
    M^4     = [[0,1,1],[1,1,2],[1,1,1]],
    det(M^4) = 1.

Thus M^4 is unimodular, and multiplying by its integral inverse identifies the cokernel of M^7-I with (Z/2)^3. The determinant is 8 and the Smith factors are (2,2,2). This independently verifies the Smith conclusion without a Smith-form library or reliance on the saved minors.

For the degree-seven cyclic cover G7 = F3 semidirect_(phi^7) Z, the integral Wang sequence gives H2(G7;Z) = ker(M^7-I) = 0 and a split exact sequence with coker(M^7-I) and Z, giving

    H1(G7;Z) = Z plus (Z/2)^3.

Over Q the same matrix is invertible, so b2(G7;Q) = 0. Over F2 it is zero, so the field Wang sequence gives b2(G7;F2) = 3. Equivalently, integral UCT gives the three mod-2 classes from Tor(H1(G7;Z),F2), rather than from integral H2. The integral and field calculations are consistent.

**Exact limitation:** this disproves a local implication from rational H2-vanishing to mod-2 H2-vanishing for one finite cover. The ambient free-by-cyclic example has unbounded rational second Betti numbers over all finite-index subgroups. It therefore does not refute an implication carrying the additional all-cover boundedness hypothesis from 21.139, and supplies no counterexample to that problem.

## 8. Checkpoint log and input pins

- **2026-10-24 16:27:46 UTC:** exact target and current geometry/counterexample files read; existing successful cover receipt located. Audit approximately **35%**; full-problem estimate **18%**.
- **2026-10-24 16:31:29 UTC:** cutting model, induction, amplification, RACG exhaustion, and retract algebra checked; source provenance and input hashes inspected. Audit approximately **85%**; full-problem estimate **18%**.
- **2026-10-24 16:33:28 UTC:** mathematical verdict reached. Conditional reduction passes; unproved (Z2) remains blocked as a completion route without a new mechanism. Audit approximately **95%**, pending review-file verification; full-problem estimate **18%**.
- **2026-10-24 16:36:10 UTC:** review file, source links, and evidence pins checked; bounded audit complete. Audit **100%**; full-problem estimate **18%**.
- **2026-10-24 16:37:09 UTC:** requested extra coefficient calculation independently verified by the unimodular identity and Wang/UCT; review supplemented. Expanded audit **100%**; full-problem estimate **18%**.

SHA-256 pins of reviewed inputs. The final pin check detected the coordinator's concurrent official-source addendum to `PROBLEM.md`; I reread that version and confirmed the target statement is unchanged. Its updated hash is recorded below. The other six pinned inputs were unchanged at the final check.

| Input | SHA-256 |
| --- | --- |
| PROBLEM.md | f39b986bec79c701278e573d9e99078fe1ea08f281a5c6c685d197191754a590 |
| approach_geometry.md | 2fda89a7b8cff6cbb4a3f21969b7d9078e2340e51fd5e0f28b8682b70e8e2abc |
| approach_counterexamples.md | bde8fa34fe2f476b14aa3e3c91b7f2a67a3384b70458f88481d336c50fca4abf |
| reviews/verify_partial01.py | a74deb9dc749992ea62fd42281f95b1ee4676fa7a26817d99a86f800d0e94e7f |
| reviews/partial_adversary01_checks.json | fe81dd0a99c3036ef83eb339246b6ac1c4ddc2371cca2665beea0942ad1cfd6e |
| root_artifacts/verify_mod2_cover.py | 814e6723d3351eddd198195a88370c0b37e257e788d6b04099746711097693e8 |
| root_artifacts/coefficient_change_degree7.json | f30b2aec458e04d64454c2ca7e6c0aa8299cc02e7219c02922464b1f9e2f5273 |

The strongest accepted outcomes here are the audited reductions and obstructions above. There is no verified proof or counterexample for unrestricted 21.139 in this review.
