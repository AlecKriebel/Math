# Attempt 1: equivariant presentation quotients

## Target and outcome

The target is the assertion that every infinite Coxeter group of finite rank has an automorphism group with a finite-index subgroup admitting an epimorphism onto an infinite Coxeter group. This attempt establishes sufficient conditions, not the full assertion. No novelty claim is made.

We use the finite-edge graph convention: an edge labelled m records (st)^m=1, including edges labelled 2; no edge means m=∞.

## Input theorem

Let C(W) be the subgroup of Aut(W) whose restriction to each maximal complete special subgroup is conjugation by an element of W (the element may depend on the complete subgroup). This subgroup has finite index. This is Mihalik–Tschantz, Theorem 28, also explicitly stated as Theorem 2.7 in Varghese's published 2026 paper.

## Lemma 1: invariant normal closures

Let R be any set of words such that each r∈R belongs to a complete special subgroup. Put N=⟨⟨R⟩⟩_W. Then N is C(W)-invariant.

Proof. If f∈C(W) and r belongs to W_Δ, choose a maximal complete subgroup containing W_Δ. There is g with f(r)=grg⁻¹. Thus f(R)⊆N, hence f(N)⊆N. Applying the same argument to f⁻¹ gives equality. ∎

This includes killing chosen generators and adding (st)^d=1 whenever {s,t} is already a finite-labelled edge. In particular d=1 permits contraction of such an edge. No analogous assertion is made for a missing edge.

## Lemma 2: finite-Out quotient lifting

Suppose q:W↠Q is an epimorphism onto an infinite finite-rank Coxeter group, ker(q) is C(W)-invariant, and Out(Q) is finite. Then the target conclusion holds for W.

Proof. The induced homomorphism ψ:C(W)→Aut(Q) has image containing Inn(Q), since ψ(ι_w)=ι_q(w), and q is onto. Hence H=ψ⁻¹(Inn(Q)) has finite index in C(W), and ψ|_H maps onto Inn(Q). Decompose Q as a product of irreducible standard factors and choose an infinite factor Q₀. Infinite irreducible Coxeter groups have trivial center, so the factor projection Q/Z(Q)↠Q₀ is well defined and surjective. Composing H↠Inn(Q)≅Q/Z(Q)↠Q₀ gives the required epimorphism. ∎

For a centerless Q the output is Q itself. It is important that the proof uses the actual finite-index preimage of Inn(Q), rather than claiming that ψ is onto Aut(Q).

## Corollary 3: separated odd components

Let Γ_odd be obtained by discarding all even-labelled edges. Suppose two distinct connected components A and B of Γ_odd have no finite-labelled edge between them. Then Aut(W) virtually surjects onto D∞=C₂*C₂.

Proof. First add st=1 for every odd-labelled edge and (st)²=1 for every even-labelled edge. Lemma 1 makes their normal closure invariant. The resulting presentation has one involution for each odd component; two of these involutions commute exactly when there is at least one finite-labelled edge joining the corresponding components. This is a right-angled Coxeter presentation. In the original group, also kill each generator outside A∪B; the additional relations again satisfy Lemma 1. The complete quotient presentation is precisely ⟨a,b | a²=b²=1⟩ because there are no finite edges between A and B. The quotient has trivial center and finite outer automorphism group, so Lemma 2 applies. ∎

This recovers the nonadjacent-even-vertices mechanism but does not require A or B to be a singleton. A complete odd-component quotient gives only a finite elementary abelian quotient, which does not suffice.

## Corollary 4: common-divisor cycle quotient

Suppose Γ is connected and contains a cycle, and every finite edge label is divisible by a fixed integer d≥3. Then Aut(W) virtually surjects onto the rank-three triangle Coxeter group

Q_d=⟨a,b,c | a²=b²=c²=(ab)^d=(bc)^d=(ca)^d=1⟩.

Proof. Partition V(Γ) into three nonempty connected sets A,B,C with at least one edge between each pair. Such a partition exists: choose a simple cycle, divide its vertices into three consecutive nonempty arcs, and attach every vertex outside the cycle by a rooted spanning forest. A tree within each part gives edge relations st=1 identifying that part to one vertex. Also impose (st)^d=1 on each finite-labelled edge of Γ. All newly imposed relators belong to complete special subgroups, so Lemma 1 applies. The original relators follow from these because d divides each original label. After eliminating repeated generators, the quotient presentation has exactly three involutions with pairwise product orders d, namely Q_d. No original missing edge contributes a relation.

For d=3 this is the Euclidean triangular reflection group. For d>3 it is the hyperbolic triangular reflection group. Thus Q_d is infinite, irreducible, and centerless. Its defining graph is complete, so its outer automorphism group is finite by the 2-spherical finite-Out theorem. Lemma 2 now gives a virtual epimorphism onto Q_d. ∎

Example: a five-cycle with successive labels 3,6,9,12,15 has such a quotient with d=3. Choose parts {v₁,v₂,v₃}, {v₄}, {v₅}; contract the first two cycle edges and reduce the three remaining labels to 3.

## Exact gap

The method does not show that every infinite W has a C(W)-invariant presentation quotient which remains infinite and has finite Out. Killing generators propagates across odd-labelled edges; arbitrary label contractions can collapse the quotient to a finite group. In particular, neither the separated-component criterion nor a common label divisor is universal. Replacing the missing argument by the assertion that such a quotient always exists would simply introduce a new unsupported reduction theorem.

## Sources

- M. Mihalik and S. Tschantz, Visual decompositions of Coxeter groups, Groups Geom. Dyn. 3 (2009), 173–198, Theorem 28. https://doi.org/10.4171/GGD/53
- O. Varghese, Coxeter quotients of the automorphism group of a Coxeter group, Algebraic & Geometric Topology 26 (2026), 2353–2362, Lemma 1.3 and Theorem 2.7. https://doi.org/10.2140/agt.2026.26.2353
- R. B. Howlett, P. J. Rowley and D. E. Taylor, On outer automorphism groups of Coxeter groups, Manuscripta Math. 93 (1997), 499–513. Primary author repository: https://www.maths.usyd.edu.au/u/ResearchReports/Algebra/HowRowTay/1996-26.html
