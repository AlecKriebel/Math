# Graph coloring game palette monotonicity: bounded partial results

Date: 2026-10-06. Problem: GRAPH-005 (1392).

**Status: partial.** This note does not prove or refute palette monotonicity for arbitrary finite graphs. It gives self-contained proofs for disjoint unions of complete multipartite graphs, an elementary sufficient condition for winning with a specified palette, and the exclusion of counterexamples on at most five vertices. These are elementary bounded results; no novelty or priority is claimed.

## 1. Exact game and question

Let $G=(V,E)$ be a finite simple undirected graph and let the common palette be $[q]=\{1,\ldots,q\}$, where $q\geq1$. Initially every vertex is uncolored. Alice starts. The players alternate; each move colors exactly one previously uncolored vertex. A move is legal precisely when its color differs from the colors of all already colored neighbors. Neither player passes or recolors a vertex. Bob wins when some uncolored vertex has neighbors of all $q$ colors. Alice wins when every vertex has been colored. The empty graph is an immediate Alice win.

Write $W_q(G)$ for the assertion that Alice has a winning strategy in this game. The question is whether $W_k(G)\Rightarrow W_{k+1}(G)$ for every such graph and every positive integer $k$. The usual game chromatic number is the least winning palette size; its definition alone does not establish that all larger palettes are winning.

This is the original Alice-first coloring game in Zhu's introduction, not the marking game used to define the game coloring number. The latter tracks earlier marked neighbors rather than color assignments. Bob-first, passing, ordered-vertex, connected-play, edge-coloring, and arboricity games change the rules and are not substituted for this question. The original source defines a move as coloring a vertex, so passing is not an available move. Its finite-game convention gives the same winner if play is allowed to continue after an uncolorable vertex first appears: colors are never removed, so that vertex remains uncolorable until play stops. See [Zhu, 1999, introduction](https://www.math.nsysu.edu.tw/~zhu/papers/game/planar.pdf).

Hollom's peer-reviewed 2024 paper explicitly leaves the unrestricted question open. Its positive arboricity result and negative ordered/connected-game results do not settle it. In particular, its ordered-game construction includes a three-to-four-color failure, so a transfer argument valid independently of vertex order cannot simply be assumed. See [Hollom, 2024, Question 1.1 and Section 3](https://doi.org/10.1016/j.dam.2024.01.007).

## 2. Elementary bounds and a high-degree reservation lemma

### Proposition 1

If $W_q(G)$, then $G$ admits a proper $q$-coloring. If $q>\Delta(G)$, Alice wins under every sequence of legal moves.

**Proof.** A successful play following a winning strategy ends in a proper $q$-coloring. For the second claim, an uncolored vertex has fewer than $q$ neighbors, hence sees fewer than $q$ colors. It can never be blocked. Every turn colors a vertex, so the finite game ends with all vertices colored. $\square$

Define $H_q=\{v\in V:\deg(v)\geq q\}$, and let $h_q=|H_q|$.

### Proposition 2 (reservation lemma)

If $2h_q-1\leq q$, then $W_q(G)$. In particular, the hypothesis holds when $h_q=0$.

**Proof.** If $h_q=0$, apply Proposition 1. Otherwise Alice gives priority to uncolored vertices in $H_q$, using any legal color. The set $H_q$ is exhausted no later than Alice's $h_q$-th turn, which is move $2h_q-1\leq q$; Bob's moves in $H_q$ can only make this happen earlier. Before that last required Alice move, at most $2h_q-2\leq q-1$ vertices have been colored. Thus every uncolored vertex still has a legal color, so Alice can carry out the priority strategy and Bob cannot already have blocked a vertex. After $H_q$ is exhausted, every remaining vertex has degree less than $q$, and so can never be blocked. $\square$

This proof is a vertex-selection argument and is valid for every palette size satisfying its displayed hypothesis. It does not infer a marking-game bound from an arbitrary coloring-game win.

### Corollary 3 (necessary conditions for a counterexample)

If $W_k(G)$ holds but $W_{k+1}(G)$ fails, then:

- $k\geq2$;
- $G$ is $k$-colorable;
- $\Delta(G)\geq k+1$;
- $ |\{v:\deg(v)\geq k+1\}|\geq\lfloor(k+2)/2\rfloor+1$.

**Proof.** A one-color winning graph is edgeless, so every positive palette wins. The second and third statements follow from Proposition 1. Apply the contrapositive of Proposition 2 with $q=k+1$ to obtain the last statement. $\square$

## 3. Palette monotonicity for unions of complete multipartite graphs

A complete multipartite graph has a partition into nonempty independent parts, with every possible edge between distinct parts. A part is **touched** once one of its vertices is colored. A component is **secured** when all its parts are touched. Here isolated vertices are complete multipartite components with one singleton part.

Two simple observations apply to a proper partial coloring of such a component:

1. Each used color occurs in only one part. Once a part is touched, every uncolored vertex in it can always reuse a color already in that part. A subsequent legal move in another part of the same component cannot use that color.
2. An untouched part is adjacent to every colored vertex of its component. If $s$ distinct colors have appeared there, every vertex of the untouched part has exactly $q-s$ available colors. Thus an unsecured component in a non-lost $q$-color game satisfies $s<q$, while a secured component can never cause a loss.

### Theorem 4

Suppose every connected component of $G$ is complete multipartite. For all positive integers $k\leq q$, $W_k(G)\Rightarrow W_q(G)$.

**Proof.** Fix an Alice winning strategy $\sigma$ with $k$ colors. Alice plays the real game with $q$ colors and maintains a shadow game with $k$ colors, using $\sigma$ for shadow Alice. In both games, exactly the same vertices will be colored on exactly the same turns. Hence the touched parts and secured components agree between the games.

For each unsecured component $C$, let $r_C$ and $s_C$ be the numbers of distinct colors used in $C$ in the real and shadow games. Maintain

$$
r_C\leq s_C<k\leq q.
$$

The invariant holds initially. Counts are deliberately not compared in secured components, where both games are permanently safe.

On Alice's turn, obtain the vertex $v$ and color prescribed by $\sigma$ in the shadow game and make that shadow move. In the real game, color the same vertex. If its part was already touched before the move, reuse any color already present in that part; this is legal by observation 1 and does not increase the component's real color count. If its part was untouched, choose a color not yet used in that component. The pre-move invariant guarantees that such a real color exists. In the latter case the shadow move must also introduce a color new to that component. Consequently the real count increases by no more than the shadow count. The shadow game cannot become lost on a move of its winning strategy. Thus, if the component is still unsecured, observation 2 gives $s_C<k$, preserving the invariant. If it has just become secured, no count comparison there is needed subsequently.

On Bob's turn, first observe his real move at vertex $v$. If $v$'s component was unsecured before this move, copy the vertex into the shadow game but give it any color not yet used in that shadow component. This is legal because $s_C<k$. The shadow count increases by exactly one, whereas the real count increases by at most one. This is a legal Bob reply against $\sigma$, so it cannot produce a lost shadow position. Again either the component becomes secured, or the invariant continues to hold. If $v$'s component was already secured, copy the vertex with any shadow color already in its part; this is legal, and both components remain secured.

The invariant and observation 2 ensure that no real unsecured component is blocked. Observation 1 gives the same conclusion in secured components. The construction specifies a legal Alice move after every real Bob play and synchronizes the complete global move order, including plays in different components. After finitely many moves all vertices are colored. Thus Alice wins the real game. $\square$

**Scope.** The proof allows singleton parts, disconnected graphs of the stated form, and arbitrary $q\geq k$. It does not give a formula for the least winning palette. It makes no use of the monotonicity conjecture. Its crucial structural premise, that a color belongs to a unique part inside a component, is false for general graphs.

The touched-part observation is standard background in the multipartite literature. Obszarski, Turowski, and Zięba discuss the stage when every part first contains a colored vertex and give much stronger numerical results when all parts are nonsingletons. This note claims no improvement to their formulas or priority for the above elementary transfer. See [their 2023 paper, Section 1.3](https://arxiv.org/abs/2304.12073v2).

## 4. No counterexample on at most five vertices

### Theorem 5

If $ |V(G)|\leq5$, then $W_k(G)\Rightarrow W_{k+1}(G)$ for every positive integer $k$.

**Proof.** The empty graph is immediate. Suppose $W_k(G)$.

- If $k=1$, Proposition 1 implies that $G$ is edgeless, and two colors suffice.
- If $k=2$, then $G$ is bipartite. Choose a bipartition $V=A\sqcup B$ with $ |A|\leq|B|$. Since $ |V|\leq5$, $ |A|\leq2$. Every vertex in $B$ has degree at most two, so every vertex of degree at least three is in $A$. Thus $h_3\leq2$, and Proposition 2 gives $W_3(G)$.
- If $k=3$ and $ |V|\leq4$, four colors exceed the maximum degree. If $ |V|=5$, each vertex of degree at least four is universal. There can be at most two such vertices: three universal vertices, together with any fourth vertex, form a clique of size four, contradicting the proper three-colorability supplied by Proposition 1. Hence $h_4\leq2$, and Proposition 2 gives $W_4(G)$.
- If $k\geq4$, then $k+1\geq5>\Delta(G)$, so Proposition 1 applies.

These cases exhaust all positive $k$. $\square$

This is a deductive statement for all graphs of the specified order, not an empirical enumeration. No game-state search, sampled play, or heuristic certificate supports or is needed for it.

## 5. Why the general argument is still missing

A fixed map from $k+1$ colors to $k$ colors must merge two colors. A properly colored edge carrying those two colors then maps to an improper coloring. Thus palette merging is not, by itself, a map of legal game states. Moreover, Bob's moves using the extra color need not belong to the $k$-color game tree at all. Merely telling Alice to ignore the extra color does not address those moves.

Theorem 4 succeeds because its explicitly maintained component counts and permanent safe parts make all shadow replies legal. Arbitrary graphs need a replacement invariant with those properties. Proposition 2 establishes a sufficient winning condition independent of a smaller-palette win, but it does not imply that an arbitrary $W_k(G)$ graph satisfies that condition at $q=k+1$. Theorem 5 and Corollary 3 are exclusions, not a construction or a universal solution.

The bounded literature check conducted on 2026-10-06 verified no later general resolution. That is a report of what was found, not a proof that no unindexed or later result exists. The general question remains unresolved by this note.
