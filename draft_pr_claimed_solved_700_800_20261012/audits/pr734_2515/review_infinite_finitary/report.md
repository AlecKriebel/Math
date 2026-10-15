# Independent adversarial review: infinite finitary construction for Problem 21.6

## Verdict and review boundaries

**PASS for mathematical validity.** The frozen proof gives a counterexample on a countably infinite domain to the stated universal assertion. The bottom-block obstruction survives arbitrary transitive subgroups and arbitrary outside action of lifts. There is no essential remaining mathematical gap in the reviewed argument.

Review target: claimed PR734 head `7a00d71fdf01ffb785863c859d75e88f943d38cf`, frozen `original/unsolved_math_prioritization/attempts/2515/author/PROOFS.md`, SHA-256 `e3eb35d6d94a9a28d14ef03ba3780b9da9d4195f8cfa45f780afbc6f0e602fc9`. This reviewer inspected the frozen proof and the independently obtained primary source; no earlier audit, other reviewer's findings, or author computation was consulted. No Git, checkout, PR, publication, or external-contact action was taken. PASS does not certify novelty, editorial acceptance, or exhaustive priority clearance.

## Source and exact claim

The editor homepage currently links the [October 2026 update-2 notebook](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21tkt-1.pdf). The supplied `21tkt.pdf` URL returns 404. Printed page 177, Problem 21.6, asks about a transitive finitary G and transitive Sylow p-subgroups **of G**. Its desired subgroup must be transitive, totally imprimitive, and have each individual cycle support as a subgroup block. Printed page 89, Problem 15.23, defines total imprimitivity by containment of every finite point subset in a finite group block. Problem 21.6 has no solution annotation on the inspected page. These source findings and hashes are in `source_metadata.json`.

The exact falsifiable counterclaim proved here is: there exists a countably infinite set Omega and a transitive locally finite 2-group G <= FSym(Omega), such that for every transitive H <= G there are h,k in H and a two-cycle support C of h with `0 < |C intersection k(C)| < |C|`. Such C is not an H-block. Setting S=G then disproves the requested existence statement, regardless of the extra total-imprimitivity condition.

## Independently verified finite dependency

Identify V with the additive group F2^2 and E with the four-dimensional function space V -> F2. Write tau_t f(v)=f(v+t), sigma(f)=sum_v f(v), and use the permutation

`(f,t): (v,e) -> (v+t, e+f(v+t))`.

Direct composition gives `(f,t)(g,u)=(f+tau_t(g),t+u)`, and inversion gives `(tau_t(f),t)`. Since sigma is invariant under translations, `sigma(f)+t_1` is a homomorphism E semidirect V -> F2. Its kernel P has order 32, projects onto V, and has base kernel E0=ker(sigma) of dimension 3. Even indicators of two chosen fibres flip a point in any chosen fibre, so P is transitive on D=V x F2.

For a transitive Q<=P, projection onto the four fibres is the full regular translation group V. Select q1=(f,e1), q2=(g,e2) in Q. Necessarily sigma(f)=1 and sigma(g)=0. Put D_i=1+tau_ei. The square q1^2 has base h=D1 f. On the two e1-pairs, h has constant values whose sum is 1. Thus h is the indicator of one such pair. Its q2-conjugate is the complementary pair indicator tau_e2 h. They span L=ker D1 of dimension 2.

The commutator q1 q2 q1^-1 q2^-1 has base c=D2 f+D1 g. Here c belongs to E0, while D1 c=D1D2 f=1_V, since each output is the sum of f over all four V points. Therefore c is outside L. The three base vectors generate E0 inside Q; the full projection gives Q=P. This argument does not presuppose minimal transitivity or a classification theorem.

Take b=(0,e2) and z=(delta_e1+delta_e2,0). Both satisfy the kernel equation. The b-cycle C={(0,0),(e2,0)} has z-image {(0,0),(e2,1)}, a distinct set sharing one point. Hence P fails the individual-cycle block requirement. In the proof's one-based labelling these are C={1,5} and z(C)={1,6}.

The independently authored checker also enumerates the complete subgroup lattice: 50 subgroups, only P transitive. All 64 possible pairs of q1/q2 lifts generate P and satisfy the square/commutator identities. These finite checks support, but are not needed for, the finite deductive proof.

## All-level construction and embedding invariant

For n>=0, let I_n={0,...,2^n-1} and Omega_n=D x I_n. A convenient independent description is

`G_n = P^(I_n) semidirect T_n`,

where T_n is the finite permutation group on I_n obtained recursively from T_0=1 and T_(n+1)=(T_n x T_n) semidirect C2, with the top involution exchanging the two halves coordinate by coordinate. Equivalently, every element of G_n sends a bottom fibre D x {i} to D x {t(i)} and uses some p_i in P on its D-coordinate. This description follows by induction from the two independent base copies and the top swap. It agrees with the candidate's G_(n+1)=G_n wr C2.

Embed G_n in the first base factor of G_(n+1). As an actual permutation, this preserves its action on Omega_n and fixes the second copy. Extend by the identity to Omega=D x N_0. These are injective embeddings of the stated permutation actions, and their images form a nested chain. The distinction matters: a diagonal embedding would repeat old movement into the new copy, and would not give these finite-support inclusions on the same domain.

Each G_n is finite with order a power of 2: `|G_0|=32`, `|G_(n+1)|=2|G_n|^2`. Every finite set of elements of G=union_n G_n lies in some G_n, so G is locally finite and is a 2-group. Every g lies in a finite stage and fixes Omega\Omega_n, so G is finitary. Its action is faithful because the inclusions are inclusions of actual permutations.

Transitivity is inductive: G_0 is transitive; the two copies are transitive in their own halves and the top swap interchanges halves. Any two points of Omega lie in a common Omega_n, so G is transitive on the infinite domain. No infinite product or unrestricted permutation is silently introduced.

## Blocks, proper blocks, and total imprimitivity

For every m>=n, T_m preserves the partition of I_m into aligned intervals of length 2^n. Its two base factors preserve the internal partitions and the top swap exchanges corresponding members. Consequently G_m preserves the corresponding point partition into copies of Omega_n. For m<n, G_m acts inside Omega_n and fixes its complement, so it stabilizes Omega_n. Thus each Omega_n is a G-block at **every** stage, including after arbitrary future swaps.

The Omega_n are finite, proper, strictly increasing, and cover Omega. Any finite subset has finitely many second coordinates, bounded by some integer less than 2^n, and therefore lies in Omega_n. This proves the exact primary-source definition of total imprimitivity directly.

Additional proper-block deduction: if A is an infinite proper block of a transitive finitary group, choose x in A and y outside A, and choose g sending x to y. The block axiom forces g(A) to be disjoint from A, because equality is excluded by y. Every x' in A is then moved by g, contradicting finite support. Thus every proper block is finite. In this particular action any proper block is strictly contained in a larger proper finite block: if x in A, use a translate of the displayed chain based at x, enclose the finite A in a member, and then take a larger member. This validates the candidate's no-maximal-block observation. It is not necessary to equate that observation with the source's definition; the covering chain already proves the definition.

Further strengthening: a G-block is automatically an H-block for every subgroup H<=G. Therefore **every transitive H<=G is totally imprimitive**, using exactly the same Omega_n chain. The counterexample has no hidden escape through a transitive H that lacks total imprimitivity.

## Fixed bottom restriction and the unrestricted H quantifier

Let B=D x {0}=Omega_0. The all-level fibre invariant shows that every g stabilizing B restricts there to an element of P. Conversely the original first-factor copy P realizes every such restriction. Hence the induced setwise-stabilizer action is exactly `G_B^B=P` at every stage and in the union.

Now let H<=G be any transitive subgroup. For any x,y in B, transitivity gives h in H with h(x)=y. Since h(B) intersects B and B is a G-block, h(B)=B. Thus H_B acts transitively on B and its induced image is a transitive subgroup of P. Minimal transitivity forces `H_B^B=P`.

Choose h_b,h_z in H_B restricting to b,z. The orbit of (0,0) under h_b is exactly the two points C: its first iterate is (e2,0), its second iterate returns, and no iterate can exit the setwise invariant B. Thus C is an individual cycle in the global permutation h_b even if h_b has larger order, other cycles, or arbitrary support outside B. The restriction of h_z carries C to the crossing image from the finite witness. Therefore C is not an H-block.

This uses surjectivity of the restriction image, never injectivity of restriction or containment of the first-factor P inside H. There is no assumption that H is finitely generated, is a union of selected stage subgroups, is normal, or contains the chosen finite-stage generators. The two required elements exist in H and independently lie in some finite stages, which is enough.

An equivalent independent deduction is a hereditary property: for any group with individual cycle supports as blocks, the induced action of the stabilizer of any block has the same property. Lift an element of that induced action; each of its block-internal cycles is an entire global cycle, and global blockhood implies blockhood for the induced stabilizer. Transitive subgroup restriction to a block is transitive. The finite P obstruction therefore rules out every transitive H in any extension whose bottom stabilizer image is P. This is a general block argument, rather than an inference from a bounded wreath computation.

## Sylow and domain boundary cases

S=G is a Sylow 2-subgroup of G under the maximal-2-subgroup definition, since G itself is a 2-group. If one instead requires compatibility with finite Sylow subgroups, every finite subgroup is a 2-group and its own Sylow subgroup, giving the same conclusion. A distinction between finite and infinite Sylow conventions cannot defeat this example. The source asks for Sylow subgroups of G; it does not demand that S be Sylow in all of FSym(Omega).

The action is genuinely infinite, countable, transitive, faithful, finitary, and locally finite. Fixed points outside a stage do not prevent transitivity of the union. Fixed-point one-cycles are singletons and always blocks; the failure uses a nontrivial two-cycle. A cycle support is not being confused with the support of the whole element. Regular actions on an infinite domain would have nonidentity fixed-point-free elements and fail the finitary hypothesis, but no regular infinite action is used here. Allowing the full symmetric group would still include this particular finitary example; broadening the ambient category cannot repair the universal statement.

## Controls and falsification attempts

`verify_independent.py` is independently authored and uses only Python's standard library, run with bundled Python 3.12.14. It produces `control_receipts.json` and checks the following, without importing the author verifier:

- Complete finite parity construction, product/inverse laws, subgroup enumeration, all 64 fibre-projection lift pairs, and the crossing cycle.
- Complete first wreath group of order 2048. Its bottom stabilizer has order 1024 and restriction image P. All 1024 pairs of b/z lifts with independent outside P-components retain the entire two-cycle and crossing translate.
- Diagonal(P) x C2, a transitive proper subgroup of order 64 in the first wreath group. It does not contain the original first-factor P, yet its bottom restriction is P and it fails the cycle property.
- Untwisted regular C2^3 control, which does have all individual cycle supports as blocks; identity-translate control, which does not create a crossing witness.
- Recursive random permutation checks at levels 0,1,2,3,6,9, including aligned partitions, bottom-fibre restrictions, and first-factor inclusions. These are bounded implementation controls, not proofs about the union.

The diagonal finite control has an infinite version: start J_0=diagonal(P) x C2 on Omega_1, then recursively set J_(k+1)=J_k wr C2, embedded in G_(k+2), and take first-factor inclusions. The union J is a transitive finitary subgroup of G preserving the requirement that paired bottom fibres receive identical P-components. It excludes the original first-factor P except for the identity. It still inherits the obstruction through restriction to B. Thus even an explicit infinite subgroup without the proposed base copy cannot escape.

## Nonessential corrections and exact remaining scope

1. Replace the dead controlling-source URL with the current editor-linked `21tkt-1.pdf` URL and retain retrieval metadata.
2. Cite the finite-subset containment definition of total imprimitivity directly, and state that Omega_n proves it. The no-maximal-proper-block argument is sound here but is an unnecessary detour.

No proof repair is required for these points. The strongest verified result is the negative mathematical answer, including the universal transitive-H obstruction on an infinite finitary domain. The remaining gap is scholarly: exhaustive priority and external mathematical/editorial confirmation were outside this review. No outreach was prepared or attempted. Temporary primary-source PDF, extracted text, rendering images and HTTP headers are removed from this deliverable package after metadata capture.
