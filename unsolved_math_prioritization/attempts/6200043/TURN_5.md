# Recovery proof turn 5: finite-state hole certificates

2026-10-03. Recovery turn 5/5; historical count unknown. Original unresolved. Completion estimate 20%, subjective route coverage. This final proof attempt asks whether boundary self-similarity and automatic descriptions can turn a single omitted region into uniform porosity. We obtain a checkable sufficient criterion and prove why finite-state structure alone is insufficient. No sixth author search follows.

## Geometric certificate

Let (X,d) be compact. Suppose there are nested cells C_w indexed by a rooted finite-alphabet tree, with depth |w|, satisfying:

- Every x∈Y⊂X has an infinite chain of cells containing x.
- diam C_w≤Aρ^|w|, where A>0 and 0<ρ<1.
- There is a finite state attached to each cell in such a chain. From every reachable safe state, some word of length at most N leads to a rejected descendant v.
- Each such rejected descendant of depth |w|+l has a certified ball B(z,c0ρ^(|w|+l))⊂C_v⊂C_w disjoint from Y, with c0>0 independent of w.

The last hypothesis is about an actual ambient metric ball, not merely an absent symbolic address. Boundary coding can be many-to-one, so a missing address by itself does not prove it.

Then Y is uniformly porous. Given y∈Y and sufficiently small r>0, choose the least k≥0 with Aρ^k≤r/2 and a chain cell C_w of depth k containing y. Minimality gives ρ^k>ρ r/(2A) whenever k≥1. The certified rejected descendant has l≤N, so its ball radius is at least c0ρ^(k+N)>[c0ρ^(N+1)/(2A)]r. Its containing parent has diameter at most r/2 and contains y, so the ball lies in B(y,r)\Y. Thus c=c0ρ^(N+1)/(2A), or any smaller positive constant, is a porosity constant at small scales. Compact scale adjustment as in turn 1 extends the conclusion if desired.

It follows from turn 1's credited attained-dimension obstruction that no QS self-image of the source Loewner boundary can satisfy this certificate. Equivalently, any attempted proper self-embedding constructed with these uniformly escaping cells is excluded.

## Finite-state decision and counting

Let S be a finite set of safe states, with |S|=m, an alphabet of b≥2 letters, a total deterministic transition function δ:S×{1,...,b}→S∪{⊥}, and absorbing rejected state ⊥. A word survives when its path never reaches ⊥. Restrict attention to safe states reachable from the initial state.

There is a uniform escape length from all reachable safe states if and only if each has a directed path to ⊥. Reverse breadth-first search computes the shortest distances exactly. Whenever a path exists, a shortest path repeats no safe vertex, so its length is at most m. The maximal shortest distance N is therefore an explicit uniform certificate. This is an elementary directed-graph argument; no floating-point spectral approximation is needed.

If N is finite, from each safe state at most b^N−1 words of length N survive: at least one shortest rejected word can be padded to length N because ⊥ is absorbing. Iterating blocks, the number a_{kN+r} of surviving words satisfies

  a_{kN+r} ≤ (b^N−1)^k b^r,   0≤r<N.

Thus the exponential growth rate is at most (b^N−1)^(1/N)<b. This is a symbolic growth deficit only; converting it to a boundary dimension bound would require verified coding geometry. The actual ball criterion above already provides the geometric implication needed here.

## Why a proper finite-state image is not enough

Consider binary sequences whose first symbol is 0, with all subsequent symbols unrestricted. Three states suffice: initial, unrestricted safe, and reject. The accepted set is proper, but after entering the unrestricted state no word reaches reject. Under the usual binary coding into [0,1], its image is the whole half interval [0,1/2], including its nonempty relative interior. It is not porous there. Address ambiguity at the midpoint is harmless for this example's image but illustrates why actual metric balls must be checked separately.

Hence neither 'proper regular language' nor 'finite automaton' implies uniform escape from every reachable safe state. Nor does the automatic structure of a hyperbolic group automatically give a finite-state description of an arbitrary QS self-image. Both missing claims would need independent proofs; neither is established by the source's Loewner hypothesis.

## Final endpoint

The five recovery routes produce: a precise porosity obstruction; a finite-quasiconvex-cover positive class; necessary iterate collapse/summability; a critical-modulus shortcut countermodel; and a finite-state metric-hole certificate. They do not prove or disprove the original general conjecture. These are scoped deductions and method obstructions, with substantial classical credit, not a replacement target or a verified new theorem claim.
