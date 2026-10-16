# Independent probability derivation (written before reading the submission)

Status at creation: the submitted `PROOF.md` has not been opened. This derivation uses only the task's specified model and hypotheses.

## Model and claim

Write `T = 1/(2 lambda)` for `lambda > 0`. The offspring law satisfies `P(xi >= m) = m^(-1/4)` for integer `m >= 1`. In particular, `xi >= 1` almost surely and `xi < infinity` almost surely. Label vertices by finite words in positive integers. Assign independent offspring variables, independent rate-`lambda` arrow processes to ordered parent/child edges, and independent rate-one recovery processes to vertices.

The graphical process consists of vertices reachable from the initially infected root by a finite time-ordered path of arrows and vertical segments without recovery marks. This definition is retained even if finite-path reachability is infinite at a finite time. The target is

`P(|X_T| = infinity) >= (7/30) exp(-3T)`.

## A summable-window forward-ray mechanism

Define thresholds `k_n = 256^(2^n) = 2^(8 * 2^n)` for `n >= 0`. Define times `s_0 = 0` and `s_n = T (1 - 2^(-n))` for `n >= 1`, and windows `I_n = (s_(n-1), s_n]`. Their lengths are `Delta_n = T 2^(-n)` and their scaled lengths are `lambda Delta_n = 2^(-(n+1))`.

First require `xi(root) >= k_0 = 256`, an event of probability `1/4`. Given a current vertex `v_(n-1)` with at least `k_(n-1)` children, inspect its first `k_(n-1)` children. A child passes when:

* it has at least `k_n` children; and
* the parent-to-child arrow process has at least one mark in `I_n`.

Choose the first passing child as `v_n`. The probability for one fresh child to pass is

`p_n = k_n^(-1/4) (1 - exp(-2^(-(n+1))))`.

For `0 <= x <= 1/4`, the elementary bound `1 - exp(-x) >= x - x^2/2 >= (3/4)x` gives

`k_(n-1) p_n >= a_n := (3/4) 2^(4 * 2^(n-1) - n - 1)`.

Here `a_1 = 3` and `a_(n+1)/a_n = 2^(4 * 2^(n-1) - 1) >= 8`. Consequently `a_n >= 3n` for all `n >= 1`. The conditional chance of having no passing child is at most

`(1 - p_n)^(k_(n-1)) <= exp(-a_n) <= exp(-3n)`.

This bound is valid under adaptive selection. The prior exploration has revealed the chosen current vertex's own offspring count, but has not revealed its children's offspring variables or its outgoing arrows in the next window. All these child pairs are independent fresh data. The first-passing-child rule biases the selected child's own offspring count, which is harmless because the next stage uses only its guaranteed lower bound and fresh grandchildren data. Distinct inspected sibling counts do not expose grandchildren counts.

A conditional union bound at the first failing stage now gives

`P(all stages succeed | xi(root) >= 256) >= 1 - sum_(n>=1) exp(-3n) = 1 - 1/(exp(3)-1) > 14/15`.

The final strict inequality is elementary: the first five terms of the exponential series give `exp(3) > 1+3+9/2+27/6+81/24 = 131/8 > 16`. Thus the arrow-and-tree event `G` producing an infinite forward ray has probability at least `7/30`.

## Recoveries and simultaneous infection

The ray selection does not inspect recovery marks. Conditional on all tree and arrow data, on `G`, require:

* no recovery at `v_0` during `[0,T]`;
* no recovery at `v_n` during `[s_(n-1),T]` for every `n >= 1`.

These concern distinct vertices, so their probability is

`exp(-T - sum_(n>=1) (T-s_(n-1))) = exp(-T - T sum_(n>=1) 2^(-(n-1))) = exp(-3T)`.

This infinite product is positive because the exposure lengths are summable. The countable intersection follows by continuity from above applied to the finite intersections. A common incorrect alternative would demand every ray vertex be recovery-free on all of `[0,T]`; that alternative has probability zero and is not used here.

For each fixed `n`, use one arrow in each of `I_1,...,I_n`. The windows are in chronological order. Each arrow's target has no recovery from the start of its window until `T`, and each source has the preceding survival condition. Therefore this is a finite valid graphical infection path from `(root,0)` to `(v_n,T)`. Every `v_n` belongs to `X_T`; hence `|X_T| = infinity`. This proves the claimed annealed bound with the exact exponent `3/(2 lambda)`.

No infection path from the root to an infinite endpoint is invoked. Only countably many ordinary finite-path membership statements are used at the common time `T`.

## Quenched amplification

Fix a rate `r > 0` and let `h_r(tau)` be the graphical probability, on a subtree `tau` started with its root infected, that infinitely many vertices are infected at `1/(2r)`. The annealed result gives `E h_r > 0`. Thus `rho_r := P_tree(h_r > 0) > 0`.

Let `Z_n` be the finite size of generation `n`. Since every vertex has at least one child, `Z_n` is nondecreasing. It tends to infinity almost surely. To check this without a finite-mean assumption, if it stayed bounded it would eventually equal some integer `k >= 1` forever. Conditional on a generation of size `k`, keeping that size for the next `j` generations requires all `kj` offspring counts to equal one, with probability `q^(kj)`, where `q = P(xi=1) = 1-2^(-1/4) < 1`. Letting `j` increase and then taking the countable union over starting generation and `k` proves that bounded growth has probability zero.

Conditional on the tree above generation `n`, the `Z_n` forward subtrees rooted there are independent copies of the original Galton–Watson tree. Therefore

`P(no vertex at generation n has h_r > 0) = E[(1-rho_r)^(Z_n)] -> 0`.

The event that no vertex anywhere has `h_r > 0` is contained in each of these events. Its probability is zero. Almost every tree consequently has a vertex `w` at a finite depth whose forward subtree has positive `h_r`.

On such a fixed tree, force infection along the finite root-to-`w` path during `[0,1]` by requiring no recovery on its finitely many vertices and at least one arrow on each path edge in successive disjoint subintervals. For depth `d >= 1` this event has probability at least

`exp(-(d+1)) (1-exp(-r/d))^d > 0`.

For `d=0`, retaining root infection until time one has probability `exp(-1) > 0`. The graphical randomness after time one is independent of this access event and has its original law. Start the successful subtree event from `(w,1)` and concatenate each finite subtree path with the finite access path. It follows that, on almost every tree, rate `r` has positive quenched probability of infinitely many infections at the deterministic finite time `1+1/(2r)`.

Intersect these full-measure tree sets for `r = 1/m`, `m >= 1`. For any `lambda > 0`, choose `m` with `1/m <= lambda`. Superpose extra rate-`lambda-1/m` arrows while retaining the same recoveries. Every finite infection path at rate `1/m` remains valid at rate `lambda`. The probability of infinitely many infections at the finite time `1+m/2` is therefore positive at rate `lambda` on this single full-measure set of trees. This establishes the required order of quantifiers: **almost every tree, every positive rate**.

## Measurability and boundary checks

All potential vertices lie in the countable Ulam–Harris word set. Membership in the random tree is a finite condition on ancestral offspring variables. Each selected child is defined by a finite scan and the first-success rule. Success for every stage and each required recovery-free interval form countable intersections of measurable events. Conditional recovery probabilities are valid because selection uses only tree and arrow data and all chosen vertices are distinct.

Finite-path reachability is a countable union over finite vertex paths of measurable finite-clock events. The event of infinitely many reachable vertices at a fixed time is measurable on this countable vertex set. Integrating its indicator over graphical randomness makes `h_r` a measurable tree function; thus the subtree amplification uses measurable events. No infinite endpoint or undefined infinite sequence of jumps is needed.

The statement is restricted to `lambda > 0`; the construction and its final time do not extend to `lambda=0`. Large and small positive rates merely change the final time and the positive recovery factor. Local finiteness and the absence of leaves follow from the specified offspring law, not from a finite offspring mean (which is infinite here). The argument does not assert explosion on every deterministic locally finite tree: an infinite degree-one ray is an immediate counterexample to that stronger claim and has probability zero under this law.

## Independent conclusion

Both supplied hypotheses follow from the checkable mechanism above. This is a mathematical validation of the stated hypotheses for the explicitly specified finite-path process, before any comparison with the submission. It does not establish novelty or publication priority.
