# Independent adversarial paper-only reconstruction —23578142

This substantive reconstruction follows personal reading of the complete actual seven-page PDF, all391 controlling TeX lines and all seven fresh individual page rasters. It precedes foreign scientific primary bodies, native scientific code/results, archive inventory, bundled opinions and current peer/root science. The source owner supplied sealed identity/path/hash metadata only. An early directory-creation failure caused no manuscript exposure; its history is separately preserved. The target's own description of computational/prior audits has necessarily been read as part of the paper, but none of those bodies has been opened. Root126's science gate is CLOSED; findings in this file are local and provisional until primary/code audits finish.

## Exact target and category

P is an ordinary unweighted r-differential poset: r is a positive integer; the poset is locally finite and N-graded with a global minimum0, finite ranks P_j, and ordinary0/1 incidence up/down operators over Q satisfying DU−UD=rI as an integer counting identity. Write p_j=|P_j|, d(x)=number of lower covers,u(x)=number of upper covers. Thus u=d+r and distinct same-rank pairs have equal numbers of common lower and upper covers. Weighted/multiple-edge or merely characteristic-modular versions are not the target.

For n≥2, Z=P_(n−2), X=P_(n−1), let S consist precisely of z with at least one a∈X having the WHOLE predecessor set{z}. This does not mean z has only one successor, or that a has degree1 only in a selected subgraph. H_S has vertices S⊔X, including all X isolates, and every incidence edge with its Z-end in S. Set q_n=β(H_S), β(H)=E−V+c. With B_j the entire consecutive-rank incidence graph and b_j=β(B_j), the target is0≤q_n≤b_(n−1),b_n≥q_n and the exact incidence-dependent refinement

p_n≤U_n−q_n,   U_n=1+rΣ_(k=0)^(n−2)p_k+(r−1)p_(n−1).

Equivalently p_n≤r p_(n−1)+p_(n−2)+b_(n−1)−q_n. The correction is computed before P_n is selected and is valid for every admissible next extension of the preceding data in an ordinary differential poset.

Additional full claims: if S=Z, the local recurrence follows; if n≥3 and EVERY z has at least two distinct singleton successors, equality in the local bound is equivalent to the exact Wagner reflection extension of the top rank, up to relabeling, not just equality of its size. Every rank-one element has two singleton successors (credited prior lemma), so the rank-three local bound and its equality classification follow for all r≥1. Two specified infinitely realizable reflected Young-prefix constructions attain U_n−q_n with q_n=1, proving a universal coefficient1 sharpness. The note does not prove unrestricted b_n≥b_(n−1), improve a rank-only global Fibonacci envelope, establish combinatorial strict growth or certify firstness/current worldwide openness. Those limitations remain part of the target, not defects to be repaired.

## Family1: exact operator/counting interface and forbidden4-cycles

With incidence matrix M_j rows P_(j−1), columns P_j, the commutator at rank j is M_(j+1)M_(j+1)^T−M_j^TM_j=rI. Its diagonal gives u−d=r, its off-diagonal gives common-cover equality. This is over integers/Q; characteristic reduction alone could erase a violation.

If distinct x,y in rank j have two common uppers, equality gives two distinct common lowers z,w in rank j−1. The pair z,w has x,y as two common uppers, so the argument descends. Eventually it requires two distinct rank-zero elements, impossible. Both common-cover counts are therefore0 or1. This needs the whole valid lower prefix and the unique minimum, not just two middle commutators of an arbitrary layered graph. A relaxed rooted layer whose rank-zero commutator fails is not a counterexample to the theorem.

Falsifiers: a hidden multi-edge convention, a minimum-degree assumption not forced by d+r, a truncated-prefix checker that omits rank-zero, or a descent using elements in the wrong rank. Primary standard definitions and the alleged OWR typo must be checked directly later.

## Family2: connectivity, boundary ranks and exact slack

B1 is the star from0 to r rank-one vertices. If B_j is connected, the graph on P_j whose adjacencies mean a shared predecessor is connected, including a one-vertex case. Each such pair has a common successor by the integer relation, so P_j lies in one component of B_(j+1). Every upper element has a predecessor, hence B_(j+1) is connected.

Summing u(x)=d(x)+r gives e_j=e_(j−1)+r p_(j−1),e0=0; therefore e_j=rΣ_(k=0)^(j−1)p_k. Since B_j is connected,

b_j=rΣ_(k=0)^(j−1)p_k−p_(j−1)−p_j+1.

Rearranging gives p_n=U_n−b_n and subtracting gives b_n−b_(n−1)=r p_(n−1)+p_(n−2)−p_n. In particular U_n−(r p_(n−1)+p_(n−2))=b_(n−1). The old cumulative inequality is exactly b_n≥0; local recurrence is the strictly stronger monotonicity b_n≥b_(n−1). The note does not infer monotonicity merely from nonnegativity.

No b0 is needed. At n2, b1=q2=0 and p2≤r²+1. For r1,n2 the sole witness tree has one terminal and no internal vertex. Finite positive ranks remain nonempty because r>0; no artificial empty-rank or rank-zero exception may be fed into the graph formulas.

## Family3: support graph and component bookkeeping

E(H_S)=Σ_(z∈S)u(z), V=|S|+|X|, hence q_n=Σ_(z∈S)(u(z)−1)−|X|+c(H_S). Retaining all X vertices matters to this displayed formula; deleting isolates would require changing V and c together. Cycle dimension is nonnegative and monotone under subgraph inclusion over any fixed cycle-space field, so q_n≤b_(n−1). The poset axioms themselves remain integer, regardless of this auxiliary cycle-space field.

If S is empty, H_S is precisely the isolated set X and q_n=0. If S=Z, H_S=B_(n−1), including its whole connected vertex set, so q_n=b_(n−1). A mere count of singleton vertices cannot replace the support-incidence graph; overlapping terminal neighborhoods determine cycles.

## Family4: local witness blocks and disjoint internals

Fix z∈S and choose a_z with pred(a_z)={z}. Set N_z=succ(z)⊆X. For each y∈N_z\{a_z}, common-cover equality gives exactly one rank-n vertex t_z(y) covering a_z and y. If t covers a_z and w, their common successor forces a common predecessor; because a_z has only z, w∈N_z. Thus every predecessor of such a nonsingleton t is in N_z.

The sets pred(t)\{a_z}, over nonsingleton t covering a_z, partition N_z\{a_z}. Existence covers every y, and uniqueness prevents overlap. Their stars share only a_z, so their union T_z is a tree with exactly N_z as the retained terminals and its nonsingleton rank-n vertices as internals. If |N_z|=1, this is the singleton tree.

For z≠w, witnesses a_z,a_w are distinct and have disjoint predecessor sets. They cannot share any successor. Hence no internal vertex of T_z can belong to T_w. Intersections between different trees occur only at old X terminals. This simultaneous disjointness is the load-bearing restriction; constructing each tree separately would not by itself justify a sum of cycle dimensions.

Falsifiers: an upper vertex omitted from a T_z though it covers the witness and another terminal; extra predecessors outside N_z; a terminal occurring twice within T_z; internal collisions across centers; or confusing whole predecessor singleton with degree1 inside H_S.

## Family5: Euler replacement and an independent common-contraction model

Let K be the union of all T_z and every X vertex, including isolates. Replacing center z and its |N_z| edges by a tree with k_z internals changes E and V by the same k_z−1 and preserves terminal connectivity. Disjoint internals allow all replacements simultaneously. Thus c(K)=c(H_S) and β(K)=β(H_S)=q_n. Since K⊆B_n, b_n≥q_n.

A separately derived structural model gives a more explicit verification. In H_S contract each witness edge z−a_z; these edges form a matching. In K contract every internal edge t−a_z for t∈T_z; these edges form disjoint rooted stars because internals are disjoint. Both resulting graphs have vertex set X and one edge a_z−y labelled(z,y) for every y∈N_z\{a_z}. A witness a_z cannot be a terminal of N_w for w≠z, so no unintended root identification occurs. Both contracted forests preserve cycle rank and induce the same graph. This validates arbitrary witness choices without a numerical cycle-count extrapolation.

The |N_z|=1,k_z=0 case deletes one pendant center/edge and preserves the component containing its terminal. It is not an exception to the ΔE=ΔV accounting.

## Family6: explicit linear injection of supported cycles

Orient H_S edges z→y. A cycle chain c has Σ_y c_(z,y)=0 at each z and Σ_z c_(z,y)=0 at each y. Since a_z has no other predecessor even in the whole graph, its witness-edge coefficient c_(z,a_z) is0. Orient K edges X→P_n. Send c to

Φ(c)=Σ_(z∈S) Σ_(y∈N_z\{a_z}) c_(z,y) ([a_z,t_z(y)]−[y,t_z(y)]).

The boundary of each bracketed path is y−a_z. The two cycle conditions make the total boundary zero. For each original nonwitness edge(z,y), the coefficient of the image edge[y,t_z(y)] is−c_(z,y); no other center contributes because internals are disjoint, and within one center y selects a unique edge. Therefore c can be recovered and Φ is injective over any field, including characteristic2. This is a direct map on cycle spaces, independently derived before any source code or claimed computational approach is read. It isolates exactly why weakening the singleton condition can destroy the proof.

## Family7: conditional local bound and equality rigidity

If every z is supported, q_n=b_(n−1), yielding the local bound for EVERY admissible next extension. A reflected rank n−1 contributes r singleton successors per old z, so this hypothesis holds even if rank n is selected differently.

For the equality theorem, the two-singleton hypothesis gives S=Z, so K is connected and spans X. Adding any unused rank-n vertex t with all its edges increases β by d(t)−1≥0. Equality b_n=b_(n−1)=β(K) forces every unused upper vertex to be singleton; every nonsingleton upper lies in K.

Fix z and two singleton successors a=a_z,b. A nonsingleton upper over b lies in some T_w and covers a_w. Common-cover equality for b,a_w forces w=z. Thus it covers a. Let h be the unique common successor of a,b. For every y∈N_z\{b}, the unique upper of b,y is nonsingleton, belongs to T_z and covers a; uniqueness of a,b forces that upper to be h. Hence pred(h)=N_z. Every other nonsingleton internal of T_z would share a pair a,y with h, impossible. There is one h_z over each N_z. They are distinct; each x belongs to exactly d(x) such neighborhoods. Since u(x)=d(x)+r, exactly r singleton uppers remain over x. This recovers the full reflection extension, not merely its rank size. Conversely reflection has |Z|+r|X| top elements and attains the local equality.

For n≥3, z has a predecessor and |N_z|≥r+1≥2. The theorem does not silently require r≥2. The second witness is essential to this rigidity argument; the one-witness corollary alone must not be promoted to the same equality classification.

## Family8: credited rank-one lemma and infinite extension

There are r rank-one elements. A fixed one z has r+1 successors. Each nonsingleton successor consumes a nonempty subset of the other r−1 rank-one elements, and distinct such successors consume disjoint subsets because common upper counts are≤1. At most r−1 successors are nonsingleton; at least2 are singleton. This proves the credited lemma directly. It makes n3 satisfy the two-witness hypothesis for every r≥1, so p3≤r p2+r with the stated reflection equality characterization. Primary attribution to GV Proposition3.4 must still be read, rather than treating this elementary proof as new.

For any valid prefix through rank m, reflection adds one top vertex for the full successor set of each rank-(m−1) z and r singleton tops over each rank-m x. Current x receives d(x)+r uppers; a current pair receives one new common upper for each common predecessor, preserving all integer commutators. Every new vertex has a predecessor and ranks stay finite. Repeating this provides an infinite ordinary differential poset. Sharpness cannot rest solely on a finite three-rank matrix without this realization step.

## Family9: exact sharp examples and limits of coefficient sharpness

For r3, use P1={a,b,c}, rank2 consisting of the3 pair-support vertices and2 singleton successors per rank-one element. Then p=(1,3,9), e2=12, B2 has12vertices and is connected, so b2=1. Every z is supported. Reflection gives p3=3+3·9=30,e3=12+3·9=39 and b3=1. U3=1+3(1+3)+2·9=31, q3=1, so the refined bound30 is attained. The finite prefix is precisely that of Y^3, and indefinite reflection proves realization.

For r1, Young ranks through5 are1,1,2,3,5,7. Reflecting gives p6=5+7=12,p7=7+12=19. e6=Σ0..5 p=19, so b6=19−7−12+1=1. Reflection at rank6 provides support of every rank5 element, q7=b6=1. Reflection at rank7 keeps b7=1. U7=1+Σ0..5 p=20, so equality19 is attained. Both examples have q=1; replacing the universal coefficient1 by any real c>1 gives a false inequality. This does not prove the correction is pointwise optimal among all functions of past incidences.

For Young's actual n6 layer, b5=1 and q6=0. The support S need not be empty: the extreme rank4 rows have singleton successors, but their supported stars are acyclic. The refined upper13, local upper12 and actual p6=11 distinguish the residual allowance from an actual recurrence failure. The unremoved quantity b_(n−1)−q_n can be positive; it cannot be discarded by assertion.

## Family10: falsifiable source, computation and priority interfaces

The exact original OWR improvement wording must be inspected: an explicitly rank-number-only or prove-the-entire-local-recurrence request would need a different interpretation from the stated incidence-dependent improvement. The alleged erroneous equality-to-one in OWR's common-cover wording must be compared with actual standard definitions, not used to change the theorem's ordinary-poset category. Byrnes Chapter5, Stanley's reflection and matrix identities, GV's credited lemma, and SZ Remark8 are load-bearing source interfaces. Older singleton/crown/cycle methods and upper-extremal results must remain credited; failure to locate a predecessor is not a priority proof.

The native checker claims labelled-prefix counts, not isomorphism counts. Its arbitrary-choice theorem cannot be inferred from5764 sampled witness selections or from first/last-only choices. Planned own diagnostics will use exact integer incidence matrices and independent GF2 boundary ranks, explicitly check all witness choices where small, compare an explicit cycle transfer map with the Euler/tree model, test equality by the actual multiset of predecessor blocks, and separately construct sharp examples/infinite reflection. Deliberate faults should include a missing root commutator, deletion of an upper vertex, an invalid singleton definition, isolate/component mishandling, non-tree replacement/internal collision, false equality with only one witness, and coefficient2 in an attained q1 case. Native code/results and all claimed expected outputs will be inspected only after this seal and campaign ownership coordination.

## Provisional status and exact remaining work

The paper-only derivations above supply a consistent universal mechanism and no substantive defect has yet been established. Actual primary wording/attribution, native source/certificate integrity and meaningful independent diagnostic controls remain to be audited. No inference to the unrestricted local recurrence, a stronger Fibonacci envelope, strict-growth proof, prime historical claim or machine certification is justified. If a substantive defect is found, record its precise evidence and stop that promotion; no extended repair or narrowed replacement is authorized. Root126 findings stay withheld until its explicit initial gate opens.
