Editorial note: Complete authored proof or audit prose is preserved below. Only operational artifact identities, byte counts, locations and obsolete replay directions have been replaced; all mathematical arguments, finite scopes and limitations remain. The public manifest identifies the actual distributed edition.

# Independent acceptance: sharp chromatic order and clique-cutset barriers

## Verdict and exact frozen scope

**ACCEPTED as a partial mathematical continuation. No mathematical correction is required. The unrestricted odd-hole-free 2-divisibility conjecture and general clique-cutset exclusion remain unresolved.**

The final author snapshot consists of exactly nine files, including its manifest. The author directly supplied the manifest pin after freezing. The complete authored proof and checker were checked against the supplied frozen identities before review. Omitted working-artifact identities are retained in the private preservation record; the distributed prose is inventoried by this edition's public manifest.

All original payload lengths and hashes match the direct pin, the complete inventory is exact, and the frozen proof is the same proof that received the mathematical review. An unchanged copy of those nine files was retained for the review. The earlier accepted five-file input, external pin, and complete acceptance report were preserved separately as explicit dependencies. Neither author original was modified. This review performed no remote or queue mutation and opened no additional literature-research round.

The graph universe throughout is finite simple graphs. A division means a two-coloring with no monochromatic maximum-cardinality clique, for graphs with clique number at least two. The theorem concerns this property, not perfect divisibility. Edgeless graphs are excluded from the indivisibility definition but are included and handled in the computational enumeration.

## 1. Universal chromatic-order theorem

The claim is valid without connectedness, criticality, minimality, or an odd-hole-free hypothesis:

- If q = chi(H) > r = omega(H), then n >= 2q-r+1.
- Equality holds exactly for the complete join of K_(r-2) and C5.
- Thus equality has q=r+1. If q>=r+2, or if H has no induced C5, then n>=2q-r+2.

### Counting and the first strict inequality

In an optimal proper coloring, singleton vertices form a clique; otherwise two singleton colors merge. Let s count the singletons and e be the sum of class-size excesses beyond two over nonsingleton classes. Then n=2q-s+e with s<=r and e>=0.

For a pair color class {a,b}, both endpoints cannot have a nonneighbor in the singleton clique. If the chosen nonneighbors coincide, a stable triple replaces two classes. If they differ, two stable pairs replace three classes. Either operation reduces the total number of colors. The proof correctly uses that a and b were in one stable class; no additional cross-adjacency assumptions are needed.

At n=2q-r, there are r singleton vertices and every remaining class is a pair. Neither endpoint of a pair can be complete to a maximum singleton clique. This contradicts the exchange property. Hence the inequality is strict by at least one.

### Equality classification

At n=2q-r+1, exactly the two displayed cases occur: (s,e)=(r,1) or (r-1,0). There is no missing coloring configuration because both numbers are integers and e>=0.

In the first case, every nonsingleton class except one would be a pair, which the preceding contradiction forbids. The remaining stable triple can be distributed among singleton colors using each vertex's nonneighbor. Several vertices may use the same singleton color because the triple is stable. Thus the graph would be r-colorable, contradicting q>r.

In the second case, there are t=q-r+1>=2 pairs and r-1 singleton vertices S. Choose in each pair an endpoint a_i complete to S. All a_i are mutually nonadjacent, because an edge between them would enlarge S to an (r+1)-clique. If every other endpoint b_i were also complete to S, the entire outside set would be stable, again giving an r-coloring.

Therefore some b_i misses some x in S. The exchange replacing {a_i,b_i},{x} with {b_i,x},{a_i} preserves the optimal number of colors and makes (S minus {x}) union {a_i} the singleton clique. Each a_j, j!=i, misses a_i, so the exchange property forces b_j to be complete to this new singleton clique. It must miss x, since otherwise S union {a_i,b_j} is an (r+1)-clique. Repeating with j also forces b_i complete to S minus {x}. Repeating over the indices supplies all cross edges a_i b_j for i!=j and shows that every b_i misses exactly x within S. This repetition is legitimate because t>=2 and the same nonneighbor x has now been established for every pair.

For t>=3, an edge b_i b_j together with a third a_l and S minus {x} would make an (r+1)-clique. Thus B is stable, and A together with B union {x} supplies two stable classes, plus r-2 singleton classes, contradicting q>r. Hence t=2. The edge b_1 b_2 must exist to prevent the same recoloring. The five vertices x,a_1,b_2,b_1,a_2 have exactly the C5 edges, and all remaining r-2 singleton vertices are universal. This proves the claimed graph isomorphism, not merely the presence of a C5.

The converse clique and chromatic counts for the join are immediate and correct. The condition q>r already rules out r<2, so the empty-clique join at r=2 is the only small-boundary case needed. The argument does not silently assume connectedness. In fact the equality classification itself implies connectedness. Disconnected graphs and isolated-vertex additions were also included in the exact checks.

The seven-antihole example correctly attains n=2q-r+2 in the induced-C5-free class, with (n,q,r)=(7,4,3). It does not establish sharpness for the substantially larger chromatic gaps required of forcing sides; the author explicitly avoids that claim.

## 2. Indivisibility and separator arithmetic

The clique-precolor grouping lemma is correct at a fixed threshold k. In a proper coloring using at most 2k-2 stable classes, the precolored clique occupies distinct classes. If a are already red and b blue, the remaining capacities are k-1-a and k-1-b, and their sum accommodates all unassigned classes. Admissibility supplies the nonnegative capacities. No hidden hypothesis omega(H)=k is required for that lemma.

Consequently every indivisible graph of clique number k has chi>=2k-1. For k>=3, this gives chi>=k+2, so the strengthened theorem yields n>=2(2k-1)-k+2=3k. **This bound needs neither induced-subgraph minimality nor odd-hole-freeness.** The k>=3 condition is necessary for this deduction; C5 has k=2 and five vertices.

For a clique cutset C in a minimal indivisible graph, let D_i be the components after removing C and H_i=G[C union D_i]. A maximum clique cannot meet two distinct components, so compatible side colorings glue exactly when their boundary restrictions have a common element. Each side's restriction set is nonempty by minimality. Removing D_i supplies a boundary coloring admitted by all other sides and excluded by side i. This witness is admissible, including when |C|=k, because a monochromatic C would already violate the threshold on the remaining graph.

Thus every side excludes an admissible boundary coloring. The precolor lemma forces chi(H_i)>=2k-1. A side with omega(H_i)<k would permit every boundary coloring, so in fact omega(H_i)=k. The order theorem applies to each side and proves |H_i|>=3k.

Writing s=|C| and t for the number of components, the sides count C exactly t times, so

    |G| >= s + t(3k-s).

The existing swap-orbit argument is unchanged and valid: the excluded witnesses for different sides have different swap orbits. It gives t<=2^(s-1) for s<k and t<=2^(k-1)-1 for s=k. At s=1 it rules out a cutset. At s=2<k, t=2 and the two nonempty feasible sets consist of opposite single orbits, namely equal and different boundary colors.

Therefore an edge cutset implies |G|>=6k-2, giving **22 at k=4**. For an arbitrary clique cutset, s<=k and t>=2 imply |G|>=6k-s>=5k, giving **20 at k=4**. Each side at k=4 has at least **12 vertices**. These replace the prior accepted bounds of 18, 16, and 10 respectively. They are necessary lower bounds; no existence or optimality statement follows.

## 3. Maximum-clique locations and forcing endpoints

For any indivisible graph with clique number k>=2 and any vertex v, the open neighborhood has clique number at most k-1. If the open antineighborhood also had clique number below k, then N(v) and {v} union M(v) would form a division. The latter part has clique number max(1,omega(M(v))), since v is anticomplete to M(v). Hence M(v) contains a maximum k-clique. **This conclusion is valid for every indivisible graph, with no minimality or forbidden-hole assumption.**

Minimality is used only to obtain a division after deleting v and hence two disjoint (k-1)-cliques in its neighborhood, one blocking each insertion color. These and the anticomplete k-clique are disjoint from one another and from v. The degree sandwich 2k-2<=degree(v)<=n-k-1 and the elementary n>=3k-1 count are correct; the chromatic argument then strengthens the latter to 3k for k>=3.

For an equal-only forcing edge xy, absence of a maximum clique in M(x) would produce the canonical neighborhood/antineighborhood division, in which adjacent x,y receive different colors. Thus both endpoint antineighborhoods contain maximum cliques. In an equal-boundary division, recoloring one endpoint must fail and yields an opposite-color (k-1)-clique in its neighborhood. It excludes the other endpoint because that endpoint still has the original color.

For a different-only edge, if H-{x,y} contained no maximum clique, coloring x,y one color and all other vertices the other would divide H. This uses k>=3 so that the two red vertices cannot themselves form a monochromatic k-clique. The recoloring witnesses are valid here as well, but may contain the other endpoint, exactly as stated.

Accordingly both components of a two-vertex clique cutset contain a maximum clique wholly inside the component. On the equal-only side the stronger anticompleteness to each individual cutset endpoint holds. These conclusions do not rule out either forcing type.

The odd-hole localization statement is correct: an induced cycle of length at least four contains at most two vertices of a clique; if it contains two they are consecutive. Its remaining path therefore lies inside one component. Thus gluing odd-hole-free sides along a clique cannot create a cross-side odd hole. No missing cross-side contradiction completes clique-cutset exclusion.

## 4. Comparison with the accepted prior audit and cited source

The previous accepted continuation and its complete acceptance report were verified as exact dependencies before the new checker did mathematics. Their intended companion editions are [the earlier structural proof](../3251_divisibility_partials_20261012/STRUCTURAL_PROOFS.md) and [the earlier audit](../3251_divisibility_partials_20261012/STRUCTURAL_AUDIT.md). The prior separator equivalence, orbit count, and chromatic forcing deductions agree with this review; the new ingredient is the sharpened order theorem and its equality classification.

The separately supplied elementary source audit of Hu, Xu and Zhuang, *Some properties of minimally nonperfectly divisible graphs*, [arXiv:2603.01967v2](https://arxiv.org/html/2603.01967v2#S4), was read in full. Its Section 4 concerns minimally non-2-divisible graphs and already contains no-basin/minimum-degree reductions, retention of clique number in cutset pieces, incompatible division traces, and minimum-disagreement blocking cliques. The author correctly credits this overlap and makes no novelty claim. The source's restricted clique-cutset theorem for minimally nonperfectly divisible graphs is a different statement and is not imported as an unrestricted non-2-divisibility theorem.

The inspected Hoang [arXiv:2506.12660v2](https://arxiv.org/abs/2506.12660v2) remains a frontier marker for Conjecture 4.7, not a proof of general clique-cutset exclusion. The [K4-free odd-hole-free four-color theorem](https://thomas.math.gatech.edu/PAP/k4free.pdf) is needed only to place the original target's unresolved range at k>=4. The elementary results audited here do not depend on its decomposition proof. This audit does not independently re-audit the complete external theorem proofs or certify novelty or current publication status beyond the supplied source audit.

## 5. Exact computational verification and its limits

The independent checker imports no author or prior mathematical checker. It computes invariants by bitmask dynamic programming and, for every graph in the exhaustive universe, independently cross-checks clique number by direct pair tests over all vertex subsets and chromatic number by enumerating set partitions into stable classes. It directly enumerates all two-colorings, endpoint patterns, and the necessary antineighborhood clique numbers.

Both independent and exact frozen-author programs pass in normal Python, `-O`, and `-OO`. Each program's three output files are byte-identical. The author replay also exactly matches the frozen expected-results record.

The exhaustive universe contains all **33,868 labeled simple graphs of orders zero through six**, with these matching counts:

- 696 graphs with chi>omega.
- 84 equality graphs: 12 labeled C5s and 72 labeled joins K1 with C5.
- 624 indivisible graphs, all of clique number two in this universe.
- 3,732 vertex antineighborhood instances in those indivisible graphs.
- 12 minimal indivisibles, all the labeled five-cycles.
- 219,764 edge-boundary instances with k>=3 and at least one division.
- Zero equal-only or different-only edges with k>=3.

The author additionally verifies 11 named graphs and 1,972 separator-arithmetic instances. The independent checker verifies 181 benchmark instances: six joins K_u with C5 for 0<=u<=5; every one-edge toggle of each such graph; disconnected clique additions; odd antiholes of orders 7, 9 and 11; four joins of K_u with the seven-antihole; and the join of two C5s, which tests chromatic gap two. Its separate arithmetic check covers 1,449 triples with 3<=k<=20, 1<=s<=k, and 2<=t<=8.

The universal equality classification has nonvacuous small cases. By contrast, the k>=3 indivisible, forcing-side, and minimal-indivisible-cutset bounds have no nonvacuous example in the exhaustive universe. Their acceptance rests on the written proofs. None of these finite checks resolves the unrestricted conjecture, establishes that forcing sides exist, or proves that the numerical barriers are best possible.

## 6. Fail-closed controls and separate review seal

The independent frozen-input verifier hardcodes the exact manifest digest supplied after freeze. It requires an external pin, exactly nine entries including the manifest, regular nonsymlink files, safe directory ancestors, exact payload sizes and hashes, exact stored scope and counts, and assertion-free mathematical scripts. It rejects missing, unexpected, altered and substituted inputs rather than silently narrowing the checked universe.

There are **37 independent controls per interpreter mode**, comprising two pristine positive controls and 35 required failures. They cover missing required arguments, same-size proof and manifest mutations, extra files and directories, missing files, ordinary and dangling symlinks, root and ancestor symlink substitutions, missing/wrong/duplicate-key pins, altered or missing prior acceptance, and injected false mathematical obligations in both programs. Mathematical negative controls fail without creating a result artifact in all three modes. No correctness condition relies on Python `assert`.

All mutations used disposable copies. A preliminary control-harness injection marker was updated to match the final frozen checker before all complete final control runs were performed; this changed no author input and no mathematical claim.

The review is separately inventoried in an external seal. Its verifier checks the caller-supplied seal SHA-256, exact full file and directory inventory, regular file types and ancestors, and every size and digest. Post-seal verification and hostile-control receipts are external to the sealed review directory. This avoids altering the reviewed bytes after the review pin is issued.

**Final acceptance is limited to the exact frozen authored proof, its stated partial consequences, and the explicitly bounded checks above. General odd-hole-free 2-divisibility, unrestricted clique-cutset exclusion, and novelty remain unclaimed.**
