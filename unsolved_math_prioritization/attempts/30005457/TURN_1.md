# Author turn 1: test the direct tree-transfer mechanism

**Partial obstruction only. The WARM lattice question, including existence and uniqueness, is unresolved.**

The first attempted route was to embed the published crystallization tree in a lattice while keeping its independent successful-block argument. The obstruction is stronger than merely a drawing problem.

## 1. Bounded-length tree embeddings are impossible

Suppose an n-ary rooted tree with n≥2 is injected into the nearest-neighbor lattice Z^d, and every tree edge is represented by a lattice path of length at most L. Every image of a vertex at tree depth at most k is then within lattice distance Lk of the root image. There are at least n^k such distinct images, while the lattice ball has at most (2Lk+1)^d vertices. Since exponential growth exceeds every fixed polynomial, this is impossible for all k.

This applies even if the representing paths are allowed to intersect. For an actual topological embedding the stronger requirement of internally disjoint paths does not improve the situation. Any faithful subdivision embedding must have unbounded edge lengths. More quantitatively, if every root-to-depth-k path uses at most R_k lattice edges, then n^k≤(2R_k+1)^d, hence R_k≥(n^(k/d)-1)/2.

## 2. Uniform independent thinning fails on every lattice tree

Let T be any fixed nearest-neighbor tree subgraph of Z^d. Keep each edge independently with probability at most rho<1, allowing inhomogeneous probabilities. For a fixed root o, every tree vertex at graph distance r has a unique root path of r edges. Thus

P(o connects through retained edges to distance r) ≤ |{v:d_T(o,v)=r}| rho^r ≤ (2r+1)^d rho^r →0.

Consequently the retained root cluster is finite almost surely. There are countably many possible roots, so there is almost surely no infinite retained component anywhere in T. This elementary argument is the branching-number-one obstruction, proved directly rather than used as a black-box percolation theorem.

The same conclusion holds for dependent retention under the explicit stronger hypothesis that along every simple root path, each next edge has conditional survival probability at most rho given all previous edges survived. The product bound then follows from the chain rule. A corresponding site version loses at most one factor rho.

This lemma does **not** apply automatically to WARM. Its eventual survival events are strongly dependent and no such conditional upper bound has been established. Nor does it rule out random lattice forests with infinite components. It rules out only the proposed direct transfer that replaces lattice tree edges or uniformly sized independent blocks by uniformly imperfect successful local trials.

## 3. Why the source theorem does not bypass this obstruction

The published tree construction obtains a supercritical Galton–Watson subtree from independent local blocks. Its ambient tree has exponentially many available sites, so a fixed failure probability is compatible with survival. In a lattice subdivision, long degree-two corridors have to be accounted for. Applying the same fixed-success trial at every corridor vertex falls under the lemma above. Skipping those vertices and treating an arbitrarily long corridor as one reliable edge would require a new, length-uniform WARM transmission theorem, absent from the cited source.

The source's finitely-joined extension also does not cover a lattice embedding: a sparse infinite subgraph usually has infinitely many lattice edges leaving it. Suppressing all those contacts is another unproved infinite-event requirement, not a finite conditioning event.

## 4. Outcome and next route

This closes the bounded-subdivision/independent-thinning transfer route, not the original problem. A successful construction would need cycles and merging, increasingly reliable long-range blocks, or a mechanism that defeats the uniform conditional-failure premise. Conversely, proving that premise for actual WARM would be substantial new work and is not claimed.

Next substantive route: test whether the lattice geometry itself prevents a percolating stable deterministic equilibrium, or whether stochastic attainability is the real missing step. Completion estimate for the original target: 10%. One substantive author turn used; four remain unless a full resolution is found sooner.
