# Counterexample constructions: diagonal, marked-limit, and algebraic routes

Research effort: Kourovka 21.144, standard Thompson group F with finitely many dyadic breakpoints and slopes in 2^Z. Author metadata for the encompassing project: Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X.

## Exact target and scope

Find a subgroup H <= F such that (i) H is not elementary amenable (EA), and (ii) H contains no subgroup isomorphic to F. Both clauses require proof. Abstract group constructions, arbitrary homeomorphism actions, infinite-piece PL actions, and marked limits do not establish H <= F. Because EA is closed under directed unions, a counterexample must already occur in a finitely generated subgroup.

This note records three distinct construction families and elementary deductions. No counterexample or resolution is claimed. Literature summaries are identified below; the proofs of the construction obstructions are supplied explicitly. No outside contact was initiated or prepared.

## Research log

- **2026-10-17 20:59:41 UTC — 5% toward an actual counterexample.** Opened the isolated counterexample route. Preserved independence from the orbital/dynamics and current-priority investigations. Planned to test infinite diagonal products, finite subdirect products, and marked limits rather than infer non-EA from nonsolvability.
- **2026-10-17 21:00:18 UTC — 7%.** Located primary sources showing that very high EA complexity and free marked limits already occur among subgroups of F. This defeats both naive ordinal-complexity and marked-limit membership arguments. Found Lodha's just-infinite quotient restriction, which is a necessary restriction rather than an EA criterion.
- **2026-10-17 21:01:19 UTC — 8%.** Proved the finite-breakpoint obstruction to infinitely many nontrivial fixed cells; proved that being F-less is closed in each finite-rank space of marked groups; proved that every full subdirect subgroup of a finite power of F contains F. Requested independent adversarial checks from the residual-properties agent. All three checks passed, with the hypotheses and infinite-product boundary recorded below.
- **2026-10-17 21:04:35 UTC — 8%; this construction audit 100%.** Independently verified the residual agent's stronger wreath-limit obstruction and its exact base-inclusion orientation in the published Bleak manuscript. Residually finite candidates must be solvable; residually solvable candidates must be locally solvable and EA. Exact rational checks passed for the finite F certificate and diagonal breakpoint growth. The primary Cannon–Floyd–Parry PDF was accessed and its proper-quotient theorem checked directly. No actual counterexample has been produced.

Percentages estimate progress toward constructing and proving an actual counterexample, not the fraction of this note that is written. Excluding tempting constructions does not mean the original conjecture is close to settled.

## Family A: diagonal products on disjoint intervals

### Intended mechanism

Diagonal products of an infinite sequence of solvable or EA marked groups can have much more complicated behavior than any factor. In the abstract product, a generator may have nontrivial coordinates in infinitely many factors. A natural attempt places those coordinates on shrinking pairwise disjoint subintervals of (0,1).

### Lemma A1: finite-breakpoint budget

Let f be an orientation-preserving PL homeomorphism of [0,1] with finitely many slope breakpoints. Let (I_j) be pairwise disjoint nonempty open intervals whose endpoints f fixes. Then f is nontrivial on at most as many I_j as it has breakpoints.

**Proof.** If f has no slope breakpoint in I_j, its restriction there is affine. Its continuous extension fixes both endpoints, so the affine map is the identity. Consequently every interval on which f is nontrivial contains an interior slope breakpoint. Distinct intervals contain distinct breakpoints. This proves the bound, including intervals that accumulate at 0, 1, or an interior point. Endpoint breakpoints cannot replace the required interior breakpoint. The identity has zero active intervals. QED.

This argument does not depend on dyadic arithmetic. In particular, an infinite diagonal sum of nonidentity interval maps cannot belong to standard F, even if every individual coordinate is an element of a dyadic copy of F.

### Proposition A2: fixed-cell EA obstruction

Let H <= PL_+([0,1]) fix the complement of a union of pairwise disjoint open intervals I_j pointwise. Suppose the restriction image H_j on each I_j is EA. Then H is EA.

**Proof.** Each h fixes every endpoint and, by A1, is nontrivial on finitely many cells. Restriction is an injective homomorphism

    H -> direct_sum_j H_j.

Injectivity uses the pointwise fixed-complement assumption. A finite product of EA groups is EA, by repeated extensions. The direct sum is the directed union of its finite subproducts and is EA. Subgroup closure gives the assertion. QED.

**Quantifiers.** H need not be finitely generated. There need not be a uniform bound on the number of cells used by elements of H. Arbitrarily high EA ranks across the coordinate groups do not defeat directed-union closure. We do not assert that a restriction at arbitrary nondyadic fixed endpoints, extended by identity, is itself an element of F; no such assertion is used.

### Corollary A3: adding an EA cell permutation cannot repair the construction

Suppose H permutes a family of pairwise disjoint open cells whose union is dense. Let Q be its permutation image and K its kernel. If Q and every restriction image of K on a cell are EA, then H is EA.

**Proof.** K preserves every cell, hence fixes its endpoints. Density of the union implies that the endpoints are dense in the complement (including any isolated complementary points); continuity therefore makes K fix that complement pointwise. Apply A2 to K, then use 1 -> K -> H -> Q -> 1. QED.

The dense-union hypothesis can be replaced by directly requiring that K fix the complement pointwise. Without one of those conditions the restriction map could miss an action on an open complementary interval.

**Status / exact gap.** The fixed-cell route is blocked. An infinite active diagonal violates finite-breakpoint membership, while finite-active coordinates with EA factors remain EA. A permutation/recycling extension with EA quotient is also blocked under A3's exact hypotheses. To reopen this family requires a new mechanism outside those hypotheses; merely adding an EA shift or increasing coordinate complexity does not suffice.

## Family B: finite fiber products and full subdirect products

### Intended mechanism

F^n embeds in F by using n disjoint dyadic intervals. One might try a fiber product H <= F^n that retains a nonelementary quotient but suppresses the visible copies of F in the factors.

### Proposition B1

Every full subdirect subgroup H <= F^n, for a positive finite integer n, contains an isomorphic copy of F.

Here "full subdirect" means that every coordinate projection H -> F is surjective.

**Proof.** Induct on n. The case n=1 is immediate. Project onto the first n-1 factors and call the image P. It is a full subdirect subgroup, so contains F by induction. The kernel K of H -> P identifies with a subgroup N of the last F. Surjectivity of H onto the last factor implies N is normal in F: conjugate an element of K by an element of H lifting any prescribed element of that F. If N is nontrivial, the normal-subgroup theorem for F gives F' <= N, and F' contains a dyadically supported copy of F. Thus H contains F. If N is trivial, H -> P is an isomorphism and the copy of F in P pulls back to H. QED.

**Boundary cases.** The proof is for finitely many full F factors. It does not assert that arbitrary subgroups of F^n with proper coordinate images contain F, or that surjecting abstractly onto F alone forces a copy of F. Those would require additional arguments. Infinite products cannot be reduced by this finite induction.

**Status / exact gap.** All full finite subdirect/fiber-product constructions are blocked. Replacing coordinates by arbitrary proper subgroups returns the unresolved subgroup problem to the coordinate images; this is not progress by itself.

## Family C: marked limits of EA subgroups

### Proposition C1: a finite algebraic certificate for containing F

Use a fixed finite presentation of F with its standard generators a,b. A pair u,v in a group G generates an isomorphic copy of F if both defining relators vanish on u,v and [u,v] != 1.

**Proof.** The relations define a homomorphism F -> G sending a,b to u,v. Every nontrivial normal subgroup of F contains F', so every proper quotient of F is abelian. The image here is nonabelian. The kernel must therefore be trivial. QED.

For example one standard presentation is

    <a,b | [a b^-1, a^-1 b a] = [a b^-1, a^-2 b a^2] = 1>.

Changing the convention for composing maps requires using a consistently corresponding marking; the abstract proof above is independent of that choice.

### Proposition C2: F-less is closed in the space of k-marked groups

Fix a finite k. If (G_n,S_n) converges to (G,S) in the usual space of k-marked groups and no G_n contains F, then G contains no F.

**Proof.** Suppose G contains F. Express the images u,v of a standard generating pair of that copy by two fixed words in S. The finitely many presentation relators in u,v hold in G, while [u,v] is nontrivial. Marked convergence says that each of these finitely many fixed word equalities and inequalities eventually has the same truth value in G_n. The corresponding pair in every sufficiently large G_n satisfies C1 and gives a copy of F, contradiction. QED.

Thus containing F is an open property in each fixed finite-rank marked-group space. This is a short deduction from known finite presentation and normal-subgroup structure, with no novelty claim.

### Consequence for the intended construction

Marked limits can preserve absence of F and lose EA. They do not preserve membership in standard F. A sharp warning is that markings of F itself can converge to nonabelian free groups: Akhmedov, Stein and Taback construct limits of rank n >= 3. F has no nonabelian free subgroup, so that limit cannot embed back into F. This primary example directly falsifies the proposed general inference "limit of subgroups of F is a subgroup of F."

Bleak, Brin and Moore additionally remark that certain two-generator EA subgroups in their hierarchy converge to the rank-two free group. Since their specific remark is stated without proof, it is treated here as a literature observation; the rigorous rank-at-least-three warning already suffices. Their proven hierarchy gives EA classes cofinal below epsilon_0, so high nonsolvable or ordinal complexity alone is also no non-EA certificate.

### Algorithmic consequence, with an explicit limitation

For a finitely generated subgroup H of F supplied by exact dyadic maps, one can enumerate word pairs u,v and test C1 with exact composition. This semidecides that H contains F. Failure of a bounded search proves nothing about all word pairs. C2 likewise supplies no procedure deciding whether a marked limit embeds into F.

**Status / exact gap.** The route remains possible only if one can separately exhibit an exact finite dyadic action for a specific non-EA F-less limit. No such embedding is supplied. Treating the marked limit as already inside F transfers the central difficulty to an unsupported assertion and is blocked.

## Family D: residual and automaton constructions

The independently delegated algebraic investigation is recorded, with full proofs, in [residual_obstructions.md](residual_obstructions.md). Its strongest construction filters were independently audited here:

1. Every residually finite subgroup of PL_+([0,1]) is solvable. Bleak's universal nonsolvable subgroup contains W_3=(Z wr Z) wr Z, and any finite quotient of A wr Z with nonabelian A kills the derived subgroup of each lamp. Thus W_3 is not residually finite.
2. Every subgroup with no nontrivial perfect subgroup is locally solvable and EA. In particular, every residually solvable subgroup is locally solvable and EA, and a finitely generated one is solvable.
3. Any faithful group of automorphisms of a locally finite rooted tree is residually finite, by its finite-level actions. Thus a non-EA group of that type, including a torsion-free example, cannot embed in standard F. Removing torsion does not evade item 1.

The exact orientation needed for item 2 was checked rather than inferred from the presence of arbitrarily large solvable wreath products. Every finitely generated nonsolvable PL subgroup contains Brin's B by [Bleak–Brough–Hermiller, Corollary 1.1](https://arxiv.org/pdf/1507.06908). In [Bleak, Section 1.2.4](https://arxiv.org/pdf/math/0608182), the consecutive generators beta_0,...,beta_(n-1) give W_n, and adjoining beta_n adds the outer shift. Thus the positive-index union is the **base-inclusion** limit L=union W_n with W_(n+1)=W_n wr Z. It is not the opposite limit with stage retractions.

For completeness, the essential new calculation within this audit is elementary. In A wr Z use distinct lamp positions 0,1,2. The elements u=x_0 x_1^-1 and v=y_0 y_2^-1 are in the derived subgroup, and their commutator is [x,y] in position 0 and identity elsewhere. Hence A_0' <= (A wr Z)''. Along the base inclusions this implies L'=L'' != 1. A group with no perfect subgroup therefore cannot have a finitely generated nonsolvable PL subgroup. L itself is locally solvable and EA, so its perfect subgroup L' does not certify non-EA.

**Status / exact gap.** Residually finite and residually solvable non-EA constructions are blocked inside finite PL. Residual EA remains a valid no-F certificate because every homomorphism F' -> an EA group is trivial; unlike a solvable target, an EA target can contain a nontrivial perfect subgroup such as L'. Neither this broader certificate nor absence of infinite simple subgroups comes with a constructed non-EA subgroup of F here.

## Exact computational artifacts

[verify_counterexample_filters.py](verify_counterexample_filters.py) uses only rational arithmetic and implements composition by taking the union of one map's breakpoints with the preimages of the other's. The saved output is [counterexample_filter_checks.json](counterexample_filter_checks.json).

- The ordinary dyadic maps x_0 and x_1 satisfy the two finite relators and have a nontrivial commutator. The commuting pair x_0,x_0^2 is rejected by the commutator condition. This checks the presentation/composition convention used by the displayed certificate.
- Put rescaled copies of x_0 on I_j=(2^(-j-1),2^(-j)), 1 <= j <= N, and use the identity elsewhere. The exact reduced breakpoint counts for N=1,2,3,8,16,32 are 4,7,10,25,49,97. In general the count is 3N+1: two internal breaks per cell, N-1 shared cell boundaries, and two boundaries with the identity region. Consequently the infinite diagonal has infinitely many breaks. The finite counts only support this explicit example; Lemma A1 proves the general obstruction without a finite bound.

## Primary literature used, with limited scope

- [Cannon, Floyd and Parry, Introductory notes on Richard Thompson's groups](https://www.imo.universite-paris-saclay.fr/~emmanuel.breuillard/Cannon.pdf), 1996, Section 3, Theorem 4.3, and Lemma 4.4. These provide the finite presentation, proper-quotient theorem, and interval copies used in B1 and C1–C2. The primary PDF was accessed directly; the proofs of our deductions are supplied above.
- [Bleak, Brin and Moore, Complexity among the finitely generated subgroups of Thompson's group](https://arxiv.org/html/1711.10998v2), 2021, Theorem 1 and the remark following Theorem 4. Its established EA hierarchy and stated marked-limit observation have the restricted uses above.
- [Akhmedov, Stein and Taback, Free limits of Thompson's group F](https://arxiv.org/abs/0908.1268), revised 2010. Its free marked limits refute closure of abstract subgroup membership under marked convergence.
- [Brin, Elementary amenable subgroups of R. Thompson's group F](https://arxiv.org/abs/math/0501085), 2005. Provides the EA-construction context; no claim here that nonsolvable wreath constructions are non-EA.
- [Lodha, Just infinite quotients of finitely generated subgroups of PL^+[0,1]](https://arxiv.org/html/2503.13523v1), 2025 preprint, Theorem 0.1. Every finitely generated subgroup of PL^+[0,1] has only virtually abelian just-infinite quotients. This can reject candidates having a prohibited quotient; it cannot imply EA, since F itself has this quotient restriction and is not EA.

## Adversarial review

The separately tasked residual-properties agent independently checked A1–A2, C2, and B1. Its report confirmed the fixed-complement hypothesis in A2, fixed finite rank in C2, coordinate surjectivity and finite n in B1, and the need to keep the infinite-product boundary open. No counterexample to these elementary deductions was found. A3 was proved after that report and is kept with its dense-union/kernel hypothesis explicitly stated.

## Strongest result and remaining gap at this checkpoint

The verified output is a set of construction filters, not a solution: naive infinite coordinate diagonals fail finite-PL membership; their finite-active EA versions remain EA; full finite subdirect products already contain F; marked limits need a separate embedding theorem; and residually finite/solvable non-EA groups cannot provide that embedding. The remaining central task is an explicit finitely generated non-EA group with a faithful finite dyadic PL action and a global proof excluding F. None has been found here. These deductions are not asserted to be novel.
