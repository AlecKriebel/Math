# Equivariant critical group torsor prior proof audit

## Publication edition and historical evidence

This prose-only edition preserves the complete substantive authored proof audit,
source-hypothesis audit and scope clarifications. Acceptance is limited to the
minimum full-Aut(G)-equivariant critical-group torsor existence formulation,
its cohomology-class and actual-action counts, and the stated simple
generalized-theta and cactus family theorems. Stronger unspecified naturality,
a uniquely preferred general action, efficient algorithms and historical
priority remain unestablished. No mathematical correction is required.

The prior manuscript is anonymous, AI-assisted and unrefereed. This acceptance
is an independent internal AI audit, not external human peer review, journal
acceptance or formal proof-assistant certification. “Independent” describes a
separate proof reconstruction and separately authored checks, not independent
human validation. The finite checks and scholarly-source retrieval/inspection
statements below are historical records of the accepted audit on 10 October
2026. Preparing this edition performed no new mathematical test execution or
scholarly-source retrieval/inspection. The complete written arguments supply
the universal mathematical justification; finite tests do not prove it.

Executable code, raw test outputs, certificates, source documents and excerpts
are omitted. This is a prose-only edition, not an executable reproduction
package. The original audit remains unchanged; the editorial changes affect
framing and historical/distribution descriptions only.

## Decision and exact scope

The mathematical claims in Anonymous, *An exact criterion for symmetry-respecting critical-group torsors*, version 0.2.0-candidate, pass this independent audit. In particular, accept Theorem 2.1 and its effective evaluation and action-count formula, Theorems 5.1 and 6.1 on simple generalized theta graphs, and Theorem 7.1 on simple cactus graphs. No substantive mathematical defect was found. The assessment is an AI-assisted mathematical audit with independently authored computations, not a human referee report or formal proof-assistant verification.

Acceptance has a precise boundary: it establishes the existence and counting of simply transitive critical-group actions compatible with the full prescribed graph-automorphism action. It does not establish a uniquely preferred action on every admissible graph, compatibility with unspecified non-isomorphism maps, deletion-contraction consistency, or a useful complexity bound. Nor does it establish historical priority, journal acceptance, or correctness of source-repository software that was not run.

The exact audited manuscript is 28,223 bytes, SHA-256 `43d033dafb5568ce4d01b54171c0ff9d8f4fd7740b1ac9164d21dc4256796645`. A new retrieval on 10 October 2026 matched the supplied bytes exactly. Public source: [candidate manuscript](https://raw.githubusercontent.com/ipitchford/symmetry-respecting-tree-torsors/main/PAPER.md).

## The original problem and the naturality boundary

The recorder's 2013 AIM list, Problem 8, asks for a spanning-tree torsor without the chosen sink and ribbon structure used in rotor-routing. The recorded clarification makes respecting graph automorphisms a minimum requirement. Problem 8 and its remarks occur on physical PDF page 4. The preface explains that the recorded remarks are summaries, not verbatim quotations of speakers. [AIM workshop list, recorder copy](https://www.samuelfhopkins.com/docs/aim_chip-firing_problems.pdf).

For a fixed graph G the precise minimum is

    g(alpha(a,T)) = alpha(g_*a,gT)

for every graph automorphism g, Jacobian element a, and spanning tree T. Here g_* is induced on degree-zero divisors modulo principal divisors; it is not a representation chosen to make a result work. Simply transitive means that for any two trees exactly one a takes the first to the second.

Four logically separate questions must be kept apart:

1. Without any equivariance, cardinality equality always gives an action by transporting translations through an arbitrary bijection.
2. For the given induced module and tree actions, does at least one compatible torsor exist? The candidate supplies a complete finite criterion.
3. Can one select such actions functorially under graph isomorphisms? Once an equivariant action is selected on one representative of each admissible isomorphism class, transport is independent of the isomorphism chosen. This is a valid consequence of the criterion. A finite canonical-labelling-and-search convention could make that selection algorithmic.
4. Is the action uniquely preferred, intrinsically characterized by additional axioms, efficient, or consistent under other graph operations? The general criterion does not answer these questions. The cactus construction has more intrinsic choice independence than the general existence construction.

Question 3 does not imply uniqueness in Question 4. Conversely, unspecified stronger requirements cannot be silently added as hypotheses that make a correct solution to Question 2 disappear. The honest disposition is a complete answer to the explicit minimum, with the broader informal word “natural” still requiring a specified meaning.

## Graph actions and the critical group

For a connected finite graph, let A = Div^0(G)/L Z^V and X = T(G). A graph automorphism permutes vertices and edges preserving incidence. Its vertex permutation commutes with the Laplacian and preserves degree, hence descends to A; its edge permutation sends a spanning tree to a spanning tree. These are the actions that enter every theorem below. The matrix-tree theorem gives |A| = |X|.

Choosing a sink for coordinates does not add a sink to the theorem. In the basis e_v-e_q of Div^0, the image of the Laplacian is the lattice of the reduced Laplacian L_q. If g moves q, the matrix representing g on these coordinates has column i equal to the nonsink coordinates of e_{g(i)}-e_{g(q)}. It is generally wrong merely to delete a row and column from the vertex-permutation matrix. The independent tests use the full degree-zero divisor, permute all its coordinates, and then return to reduced coordinates. Every induced module action is checked for additivity and the group law.

For a multigraph, retain edge permutations in Aut(G), even when they act trivially on vertices and hence trivially on A. Loops affect neither the spanning-tree set nor the incidence/Laplacian quotient, but removing them may enlarge the automorphism group. One must retain the original prescribed group rather than substitute the automorphism group of the simplified graph. The abstract theorem is valid under this convention; the candidate's graph-family theorems assume simple graphs.

## Affine reduction and the cohomology parameter

Let Gamma be a finite group, A a finite abelian Gamma-module, and X a Gamma-set of cardinality |A|. Assume a compatible torsor action and choose x_0 in X. Define c(g) by gx_0 = alpha(c(g),x_0). Applying gh to x_0 in two ways yields

    c(gh) = c(g) + g c(h).

The coordinate bijection a -> alpha(a,x_0) identifies X with the affine Gamma-set A_c, whose action is a -> ga+c(g). Conversely, translations on A_c satisfy the compatibility law and can be transported through any equivariant bijection A_c -> X.

Changing the origin to alpha(b,x_0) replaces c(g) by c(g)+gb-b. Thus H^1(Gamma,A) classifies equivariant A-torsors, where an isomorphism preserves the label a in A as well as the Gamma-action. No quotient by Aut(A) is taken. The candidate uses this convention consistently.

For H <= Gamma, an affine fixed point a satisfies c(h)=a-ha for all h in H. Such a point exists exactly when the restricted class res_H[c] is zero. If a is one solution, all solutions are a+A^H. Consequently the H-mark of A_c is either zero or d_H=|A^H|, with the latter case occurring exactly on

    K_H = ker(H^1(Gamma,A) -> H^1(H,A)).

The sign convention for coboundaries is immaterial: the subgroup generated by hb-b is the same as that generated by b-hb. The candidate's changes of origin and fixed-point equations are consistent.

## Why all subgroup marks give sufficiency

Every finite Gamma-set is a disjoint union of transitive sets Gamma/K. An H-fixed coset in Gamma/K exists only if H is conjugate to a subgroup of K. Order subgroup conjugacy classes by decreasing size. The resulting mark matrix is triangular, with positive diagonal |N_Gamma(H):H|. Its columns are linearly independent, and descending subtraction recovers the orbit multiplicities. Thus equality of every subgroup mark implies isomorphism of finite Gamma-sets.

This argument justifies the exact sufficiency step; matching elementwise fixed points alone would only match permutation characters. Conjugacy-class representatives suffice because fixed-point counts and affine fixed-point existence are invariant under subgroup conjugacy.

Let P be the representatives with t_H=|X^H|>0 and Z those with t_H=0. If any t_H is neither zero nor d_H, no class can work. Otherwise set V_0=intersection of K_H for H in P. The compatible classes are precisely

    V_0 minus the union, over H in Z, of (V_0 intersection K_H).

Ordinary finite inclusion-exclusion gives the candidate's nu. It is a nonnegative integer counting these classes. If nu>0, their affine marks equal the marks of X, so an equivariant bijection exists and translation supplies the desired action. Necessity follows from the affine reduction. This proves both directions without appealing to a conjectural graph-specific input.

An orbit matching can be made explicit. Pair orbits with conjugate stabilizers, move one representative so the stabilizers agree exactly, and send ga to gT. Equality of stabilizers proves the map is well-defined and bijective. Transporting translations through this map gives the stated action formula.

## Counting actual action maps

Fix one admissible class [c]. Equivariant bijections A_c -> X form a principal homogeneous set for Aut_Gamma(X). Two bijections give the same action map precisely when their relative permutation of A commutes with every translation. Such a permutation is a translation by b, as is seen by evaluating it at zero. It also commutes with the affine Gamma-action exactly when gb=b for every g. Therefore the fiber has size |A^Gamma|.

Different cohomology classes cannot produce the same action map: choosing origins in that map changes its cocycle only by a coboundary. If X has m_H orbits of type Gamma/H, the equivariant automorphisms on those orbits form a wreath-product group of order m_H! |N_Gamma(H)/H|^{m_H}. Multiplication over types gives

    number of action maps = nu * product_H(m_H! |N_Gamma(H):H|^{m_H}) / |A^Gamma|.

This is valid even when the fraction as written is not visibly integral; the free translation action on the bijections proves the required divisibility for each admissible class. Boundary checks agree: for Gamma trivial the count is (|A|-1)!, and for |A|=1 it is one.

## Finite evaluation versus tautological search

Finite decidability already follows by enumerating normalized bijections A -> X. The candidate acknowledges this and does not establish new decidability in that bare sense. Its additional content is a complete cohomological obstruction with simultaneous feasibility, an explicit arithmetic formula, class and action counts, and structural graph-family results.

Here is the arithmetic verification. Write A as a product of cyclic groups with moduli d_i and retain integral matrices M_g representing the induced module action. For a family F of subgroups, introduce c_g in A for each g and b_H in A for H in F. Impose the cocycle equations and c_h=(I-M_h)b_H for h in H. These equations define a homomorphism between finite products of cyclic groups, with kernel E_F.

For any cocycle whose restrictions are trivial, the choices of b_H form an independent product of torsors for A^H. Thus the number of such cocycles is |E_F|/product_{H in F}|A^H|. Quotienting by global coboundaries divides by |A|/|A^Gamma|, giving the claimed intersection-kernel formula.

For an integer matrix M from a finite cyclic-product domain to a target with modulus matrix D_out, well-definedness means M D_in Z^p is contained in D_out Z^q. The integer lifts used above have this property. The target modulo the image has order

    I_M = [Z^q : D_out Z^q + M Z^p].

Smith normal form of [D_out M] computes this finite index because D_out already has full rank. The kernel therefore has size |domain| I_M / |target|. Applying the same construction to the blocks M_h-I computes |A^H|. No unknown mathematical existence assertion remains hidden inside these finite operations.

This does not give polynomial or practically competitive complexity. Enumerating graph automorphisms, spanning trees, subgroups, cocycles, or subsets of zero-mark subgroups can be prohibitive. “Effective finite criterion” is justified; “efficient classification algorithm” is not.

## Generalized theta proof audit

Let B(l_1,...,l_k), k>=3, be a simple graph consisting of internally disjoint paths between two terminals. There is at most one path of length one. Orient each path from the first terminal to the second.

The incidence map gives a natural isomorphism

    Z^E / (ker boundary + im boundary^t) = Div^0 / im L.

Surjectivity uses connectivity. If boundary(z)=Lf, then z-boundary^t(f) lies in ker boundary, proving the kernel identity. Internal vertex cuts identify consecutive edges on each path. The terminal cut gives sum_i x_i=0, and the k-1 cycles comparing path 1 with each other path give l_1 x_1=l_i x_i. These cycles are an integral basis of the cycle lattice: a flow has a constant integer coefficient on each path, with the sum of those coefficients zero. Thus the presentation has no hidden missing relations.

A spanning tree keeps exactly one whole path and deletes one edge from each other path. Two whole paths would make a cycle, and two deletions on the same path would isolate a nonempty internal segment. It follows that tau=sum_i product_{j!=i} l_j.

For pairwise distinct lengths the full automorphism group has order two. The terminals are the only degree-k vertices; an automorphism either fixes them and fixes each length-distinguished path pointwise, or interchanges them and reverses every path. On the critical group this reversal is inversion, because every oriented-edge generator changes sign.

Write e for the number of even path lengths. A reversed tree can omit only a central edge on an odd path. Thus its fixed-tree count is k if e=0, one if e=1, and zero if e>=2.

Reduction of the presentation modulo 2 gives the other count. If e=0, all x_i are equal and kx_1=0, so |A/2A| is one for odd k and two for even k. Both are less than k. If e>=1, the common value l_i x_i is zero, odd-path generators vanish, and the e even-path generators have their single sum relation. Hence |A/2A|=|A[2]|=2^{e-1}.

For inversion by an involution s, every b=c(s) in A satisfies the cocycle relation. Classes are A/2A. The affine involution a -> -a+b has fixed points exactly when b is in 2A, and then has |A[2]| of them. A finite involution set is determined by its cardinality and number of fixed points. Therefore the admissible class count is zero for e=0, one for e=1, and 2^{e-1}-1 for e>=2. Its action count follows from the general theorem: one singleton plus (tau-1)/2 pairs in the middle case, and tau/2 pairs in the last case.

If two paths have equal length a, exchange only those two while fixing the terminals and all other paths. Let the other lengths be b_1,...,b_r and P=product b_j. A fixed tree must keep an unexchanged path intact and omit matching-position edges from the exchanged paths, so

    t_sigma = a * sum_j product_{h!=j} b_h > 0.

Coinvariants identify the two exchanged generators. Their presentation has relations 2x+sum y_j=0 and ax-b_j y_j=0. The absolute determinant, using the diagonal block with entries -b_j, is

    2P + a * sum_j product_{h!=j} b_h = 2P+t_sigma.

For an endomorphism of a finite abelian group, kernel and cokernel have equal order. Thus |A^sigma|=2P+t_sigma>t_sigma>0, contradicting the necessary fixed-point condition. This remains an obstruction inside any larger automorphism group.

This verifies the full criterion “distinct lengths and at least one even length.” The k=3 theorem is exactly its specialization. The two-generator Smith presentation there has gcd of entries gcd(a,b,c), determinant ab+ac+bc, and the stated invariant factors. The examples Theta(1,2,3) and Theta(2,4,6), including the former's 3,840 action maps and the latter's three nonzero torsor classes, are correct.

## Subdivision consequences

Uniform subdivision multiplies each length by the same integer. Distinctness is unchanged. Odd scaling preserves parity; even scaling makes every path even. Thus the claimed existence changes and the count 2^{k-1}-1 after even subdivision follow directly.

Starting from distinct odd lengths and then doubling gives homeomorphic graphs with the same abstract automorphism group C2 and opposite existence answers. Contracting one edge from each new two-edge segment recovers the negative graph from the positive one, so the positive class is not minor-closed. Oddly scaling first makes the girth arbitrarily large. These are valid consequences of the audited theorem, not new computations or an assertion about every possible minor-consistency axiom.

## Cactus construction audit

A connected simple cactus has cycle blocks and bridge blocks. Its edge lattice splits as the direct sum of the block edge lattices. The cycle lattice splits because every cycle belongs to one block. The cut lattice also splits: remove an end block with attachment vertex v; cuts at its other vertices are supported in that block, their negative sum is its local cut at v, and subtracting that local cut from the whole-graph cut at v leaves the cut of the remaining graph. Induction handles every block. A bridge quotient is trivial, and a coherently oriented m-cycle quotient has one generator with relation m times that generator equals zero.

This yields a direct sum of the cycle critical groups in a way respected by block permutations. A spanning tree contains every bridge and omits exactly one edge from each cycle, yielding the corresponding product of omitted-edge sets.

For one temporarily oriented cycle, let x be the class of an oriented edge and let edge j be omitted. Define kx to move the omitted edge to j+k modulo m. A different starting edge adds a constant to both input and output indices. Reversing orientation negates x, sends k to -k, and changes an edge index j to a constant minus j; the resulting physical output edge is unchanged. Thus both temporary choices disappear. The product action over blocks is free and transitive. An automorphism permutes blocks and preserves or reverses their cycle orientations, so the same formulas establish compatibility with its actual induced Jacobian action.

The proof is complete. In particular, automorphisms exchanging isomorphic cycle blocks are covered; treating the blocks as individually fixed would have been insufficient. The tree case, with no cycle blocks, gives the unique action of the trivial group.

## Prior obstructions and what is not new here

Wagner's Theorem 8.1 concerns the ordinary complex permutation representations on trees and critical-group elements. His cyclic-vertex-permutation example has no fixed spanning tree, while the linear critical-group action fixes zero. This prevents a natural linear intertwiner, hence an equivariant bijection to the untwisted critical-group set; it does not exclude an affine torsor. A cycle graph already illustrates the distinction. [Wagner, Section 8, PDF pages 15–16](https://arxiv.org/pdf/math/0010241).

Chan–Church–Grochow give a genuine obstruction to a universal bare-graph torsor using parallel edges. For two vertices with n>=3 parallel edges, a transposition of edges acts trivially on the cyclic critical group but fixes n-2 trees, a positive number smaller than n. Their root-independence theorem retains a ribbon graph and says that root independence is equivalent to planarity of that ribbon structure. It is not a full-automorphism classification of abstract graphs. [Chan–Church–Grochow, introduction and Theorem 2](https://arxiv.org/pdf/1308.2677).

The candidate explicitly acknowledges earlier machine-generated claims of the affine reduction, fixed-point obstruction and unicyclic construction. These are not new contributions of this audit. The earlier complete-graph obstruction also checks: a transposition on K_n fixes (n-2)^{n-3} trees and n^{n-3} critical-group elements, so n>=4 is excluded even after allowing affine twists. The tree count follows by attaching the swapped vertices as leaves to one vertex of a tree on the other n-2 vertices. In the model {x in (Z/n)^n : sum x_i=0}/<1>, the unchanged coordinates force x_1=x_2, giving the stated critical count. Both are positive and unequal.

The unicyclic construction is the one-cycle case of the cactus argument. Neither its earlier presence nor Wagner's different obstruction invalidates the candidate's exact simultaneous criterion. They do limit claims of novelty. Historical priority for the criterion or family classification has not been established by this bounded audit.

## Historically recorded independent finite verification

Only locally authored audit programs were executed. No candidate checker, source-repository script, or supplied executable was run. The programs use Python and the already installed SymPy integer-algebra routines. The original census was reconstructed by enumerating labeled simple graphs through five vertices and quotienting by all vertex permutations, without importing a graph atlas.

The historically recorded independent results are:

- All 31 connected simple graph types through five vertices were processed. Positive counts by number of vertices are 1, 1, 2, 4, 12, exactly as in the candidate.
- On all 19 census graphs with critical-group order at most eight, normalized-bijection enumeration independently agrees with the actual-action-count formula.
- For every computed positive case, an explicit equivariant orbit bijection was constructed and the resulting full action table was tested for identity, composition, simple transitivity and equivariance.
- Eleven additional theta/generalized-theta instances cover three through six paths, distinct and repeated lengths, all-odd obstructions, one-even cases and nonzero affine classes. Every result agrees with the theorem. These are not claimed to reproduce the candidate's separate 123-case checker run.
- Twelve direct graph-edge/divisor-lattice mark checks independently verify the reversal counts and every equal-path swap count in those cases plus a six-distinct-path graph. This route uses integer lattice indices rather than enumerating critical-group elements.
- The V4 regular-set / trivially acted-on Z/4 negative control has four cohomology classes and satisfies every isolated zero-or-fixed-size condition, yet has zero jointly admissible classes and zero direct actions.
- Five explicit cacti test the stated construction directly, including cycle-block permutations, a connecting bridge, unequal cycles, pendant branches and three equal cycle blocks. All action axioms, all combinations of cycle-orientation reversals, and a generating origin shift on every cycle pass.
- Forty-four subgroup-family cases compare the integer Smith-form kernel formula with direct cohomology enumeration. Modules include Z/4 with trivial and inversion actions, (Z/2)x(Z/22) with inversion, and trivial Z/4 under V4. All match.

Finite tests support the audit and test implementation details; the universal acceptance rests on the complete mathematical arguments above. This remains a bounded source-and-proof audit, with no new general-graph conjecture search.

## Final disposition

Accept the existing candidate as a rigorous prior answer to the minimum full-automorphism-equivariant existence problem, including its counts and stated graph families. Preserve its unrefereed, AI-assisted status and the absence of a historical-priority determination. Do not report an unrestricted solution of every possible interpretation of the 2013 naturality question. No proof correction is necessary for acceptance; the companion corrections note records scope and implementation clarifications that prevent overstatement.
