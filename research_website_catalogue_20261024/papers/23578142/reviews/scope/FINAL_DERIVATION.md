# Complete independent derivation and exact boundary controls

The initial substantive eight-family reconstruction was sealed before foreign scientific bodies or supplied programmes/results. This final derivation uses that reconstruction and the frozen independent predecessor/minor controls. All assertions concern ordinary unweighted r-differential posets, positive integer r, finite ranks and exact integer cover identities. Native enumeration is not a proof premise.

Let e_j be the number of incidences between P_(j−1) and P_j. Summing u=d+r gives e_j=e_(j−1)+r p_(j−1), hence e_j=rΣ_(k<j)p_k. Distinct same-rank elements have at most one common cover in either direction: a minimal-rank pair with two common covers descends to a lower such pair, contradicting the unique root. Incidence graphs B_j are connected by induction: B1 is a star; a path in the common-predecessor projection of B_j lifts via common successors to B_(j+1), and every upper vertex has a predecessor. Consequently

b_j=e_j−p_(j−1)−p_j+1,
p_n=U_n−b_n,
b_n−b_(n−1)=r p_(n−1)+p_(n−2)−p_n.

Fix n≥2, Z=P_(n−2), X=P_(n−1), and S the z having at least one upper a_z∈X with pred(a_z)={z}. H_S contains S and all X, including isolates. It is a subgraph of B_(n−1), so 0≤q_n=β(H_S)≤b_(n−1). Its explicit formula follows from E=Σ_(z∈S)u(z), V=|S|+|X|.

For each z∈S let N_z=succ(z). Each y∈N_z\{a_z} shares exactly predecessor z with a_z, so they have exactly one common upper t. Every lower cover w of t must belong to N_z: otherwise the pair w,a_z would have a common upper but no common lower. Every nonsingleton upper t covering a_z has all its lower covers in N_z. Two such t share no other terminal besides a_z. They therefore form a tree T_z connecting precisely N_z, with all incidence edges retained. The singleton-terminal case is the single vertex a_z. An internal t cannot belong to T_z and T_w for distinct z,w because it would cover a_z,a_w, which have disjoint predecessor sets. The trees can overlap only at X terminals.

Here is an independent graph-minor proof of the simultaneous transfer. Contract z−a_z in each source star of H_S. Separately, in K=the union of all T_z and all X, contract t−a_z for every internal t of T_z. The chosen witnesses are distinct and every internal t has exactly one assigned z, so no two X terminals are identified. Both operations yield the same graph M on X with edges a_z−y for y∈N_z\{a_z}. Neighborhoods N_z,N_w intersect in at most one terminal, so no duplicate pair is introduced by different z. Each contracted edge is a nonloop edge of a tree, hence β is preserved. Thus

q_n=β(H_S)=β(M)=β(K)≤β(B_n)=b_n.

Equivalently, replacing a |N_z|-edge source star by a tree with k internal vertices changes E and V by k−1 each and preserves terminal connectivity. Shared terminals are harmless because internal vertex sets are disjoint. Adding X isolates consistently preserves the component accounting. These are simultaneous constructions for any choice of the a_z, not a selected finite witness search.

Substituting b_n≥q_n in exact slack gives p_n≤U_n−q_n. Since U_n−(r p_(n−1)+p_(n−2))=b_(n−1), this is precisely the stated residual form with allowance b_(n−1)−q_n. The input q_n is computed entirely from the two preceding ranks; constructing K in an arbitrary admissible extension proves validity but is not used to determine the correction.

If S=Z, q_n=b_(n−1), so local recurrence follows for any admissible next extension. A reflection-created preceding rank supplies at least r≥1 singletons over every z, regardless of how the following rank is chosen.

For the full equality statement assume n≥3 and at least two singleton successors for every z. Then H_S and K are connected and K contains all X. Each unused top t contributes d(t) edges and one vertex, preserving connectedness and increasing β by d(t)−1≥0. Equality with the local bound forces every unused top to be singleton. For z choose singleton witnesses a=a_z,b. Every nonsingleton top over b belongs to K and specifically T_z: membership in T_w would force b and a_w to have common predecessor, requiring w=z. Each such top covers a. The unique common upper h of a,b must also cover every y∈N_z\{b}, since the common upper of b,y is in T_z and hence also covers a,b. Thus h covers all N_z. A second nonsingleton internal vertex would share a terminal pair with h, impossible. Each z has |N_z|≥r+1≥2 because n≥3, so this gives exactly one nonsingleton h_z for each z. The h_z are distinct. Each x belongs to d(x) of these neighborhoods and needs u(x)=d(x)+r uppers, leaving exactly r singleton uppers. This is reflection-extension up to top-rank relabeling. Conversely reflection has p_(n−2)+r p_(n−1) tops, giving equality. No equality theorem with only one singleton was substituted.

For rank one, each of the r vertices has r+1 uppers. Its nonsingleton uppers use pairwise disjoint nonempty subsets of the other r−1 rank-one vertices, so at most r−1 can be nonsingleton. At least two are singleton. Therefore p3≤r p2+r and equality is reflection-only. This lemma is prior Gaetz–Venkataramana Proposition3.4, not a new contribution.

Reflection extends any valid finite prefix by one block N_z for each penultimate z and r singleton blocks per current x. It enforces the exact Gram difference at the current rank, preserves earlier constraints, and can be iterated indefinitely. The two finite sharp examples therefore occur in genuine infinite differential posets. The r=3 prefix with3 pair blocks and2 singleton blocks per rank-one element has ranks1,3,9; reflection gives30, b2=b3=q3=1, U3=31. A Young prefix through rank5 reflected twice has ranks1,1,2,3,5,7,12,19; b6=b7=q7=1, U7=20. Any coefficient c>1 in U_n−c q_n fails in either example. This is coefficient sharpness, not optimality among every function of preceding incidence.

INDEPENDENT_MINOR_CONTROLS.json supplies every predecessor set for five bounded examples, ordinary integer Gram differences, all13 possible supported-witness products in those examples, actual K and common-contracted-minor edges, component lists and independent GF(2) incidence-column cycle dimensions. It also verifies:

- n=2,r=1: q2=0 and the replacement has one terminal and no internal vertex.
- Young n=6: b5=1,q6=0,refined RHS13,local RHS12,actual p6=11. The residual allowance can be positive.
- Coefficient2 is false in both sharp examples.
- The relaxed layers1,3,3,7 have exact middle Gram differences I,I but root difference3I. Their β2=1 and β3=0 are not an ordinary differential-poset counterexample. Modulo2 the root discrepancy disappears, and p2=3 would exceed the r=1 cumulative bound2. This independently exposes the essential exact-integer/full-prefix category.

The graph-contraction/GF(2) controls are materially different from the deposited edge-clique partition enumeration. They were frozen before native code/results were opened. The deposited exact checker and portable runner were subsequently read completely but not executed/imported here; another independent lane owns their bounded reproduction. Finite examples do not establish the universal theorem, which is proved above.

The full original mathematical claim is supported with no substantive gap found. General b_n≥b_(n−1), global-envelope improvement and combinatorial strict growth are not established or asserted. Fully reflected Fibonacci prefixes already have all b_j=0, illustrating why this correction need not improve the global extremal envelope. No narrowed repair or speculative follow-up is proposed.
