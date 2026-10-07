# Independent audit of family 113's approximation and sampling mechanism

Auditor: independent internal AI research subagent `upstream_proof`.
Checkpoint: 2026-10-06 22:12 PDT (2026-10-07 05:12 UTC).
Completion estimates: manuscript dependency audit 100%; new-project publication package 0% reviewed by this audit. Percentages describe work coverage, not proof evidence.

## Scope, sources, and result

I read the original request in `research/USER_REQUEST.txt` before auditing. I read the entire approximation manuscript, including its central proofs, explicit deletion sampler, bit arithmetic, and bibliography. I also read the entropy companion's introduction, weighted interface, and singleton-loop appendix. I did not contact an external individual, modify the upstream clone, or modify Git.

The source clone `/Users/alec/Desktop/math` reports HEAD `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. The copied approximation manuscript and upstream file have identical SHA-256 `dcf28553d442dfc53a9f90f7c52bd48c9e2e7e5e27b197aa7ca4be1c8daed703`.

Relevant entropy companion hashes:

| File | SHA-256 |
| --- | --- |
| `build/sections/01-introduction.tex` | `b5dac47840e40de4d2b31a3cbe326544fcb0612d33625676b5c632837ec435ce` |
| `build/sections/05-weighted.tex` | `9b993d9ea79e7d692f604be3748eed0cd432700adfd86ac9e1eacdc0dbd250b1` |

**Verdict:** I found no substantive mathematical gap in the manuscript proof after independently reconstructing its mechanisms and checking their interfaces. This is a manuscript-level mathematical audit, not a claim that the entire theorem has been machine checked or experimentally implemented. Genuine Lean declarations/builds are the responsibility of a separate auditor; the scope document `lean/docs/113.md` was read only as context and not treated as proof.

**Strongest checked statement.** The argument supports the following theorem in its actual input model: for every explicitly encoded finite simple undirected unweighted graph, and rational `0 < ε < 1`, `0 < δ < 1/2`, a uniform classical randomized algorithm returns a nonnegative rational relative-ε approximation to the perfect-matching count with probability at least `1−δ`, returns zero certainly if no perfect matching exists, and has polynomial bit running time on every execution in full input length, `ε⁻¹`, and `log δ⁻¹`. The empty graph is assigned count one. This is an existence/complexity theorem with exceptionally large fixed polynomial degrees, not a practical implementation benchmark.

The manuscript does not directly state this result for compressed multiplicities or binary rational weights. Its intermediate weighted colored spaces are explicit constructed graphs with separately controlled activities. The proposed compact gadget reduction is an additional interface requiring independent proof, even though it can invoke the checked unweighted theorem.

## Dependency reconstruction

The dependency chain is:

1. alternating-path injections → two/four-hole estimates and strong-path relocation;
2. relocation plus a finite-polynomial homotopy → logical pairing-capacity bound;
3. odd subdivision plus deterministic hole accounting → lifted capacity bound and bounded inflation;
4. fixed-label quadrangulation plus two-matching repairs → additive two-coordinate energy inequality;
5. replicated adjacent tiers plus uniquely assigned ANOVA residuals → arbitrary-function product spectral gap;
6. unit-activity tree dynamic programming and finite-state spectral mixing → bag sampler;
7. marked observables, adaptive scale restoration, and bounded-bit choices → unweighted FPRAS;
8. count-based deletion self-reduction → total-variation approximate uniform sampler.

No entropy-companion theorem is needed in that chain. The principal outside ingredients are deterministic polynomial matching feasibility (Edmonds), Hoeffding's inequality, elementary finite-dimensional spectral diagonalization, and exact integer/rational arithmetic. The count-to-sample reduction is explicit, so its applicability does not rest solely on citing Jerrum–Valiant–Vazirani.

## 1. Logical hole bound (manuscript lines 447–707)

I checked the injections rather than accepting theorem labels. For the four-hole comparison, the distinguished-hole path in the overlay of a four-hole matching and a perfect matching ends at exactly one of the other three holes. Switching is weight preserving and reversible after specifying its endpoint. This yields the three-term product bound for arbitrary positive activities.

For relocation, overlay a matching missing `S` with one missing `{z,p}`, where `g(zp)=r_z`. Inserting the strong edge gives `g(az)≤1/B<1/8`, hence `p≠a`. The three listed path-endpoint cases exhaust the degree-one vertices, including `p∈S`, in which case `p` is isolated. In the two insertion cases, the inverse first removes the newly inserted `az` before reversing the switch. The edge was absent from both inputs because one missed `a` and the other missed `z`. The bracket is at most `48+3·16=96`; dividing by row maxima at least `1/8` gives additive `6144/B` error. Normalization makes errors add along the path rather than multiply. The final adjacent-hole term is at most `32/B`; multiplying by `r_i≤4` gives the stated loose `10⁵n/B`. The case `n=2` requires no unavailable four-hole set.

For `μ(t)=λ+tB/D₀`, derivatives are finite-polynomial derivatives with positive denominator. There are at most `binom(n,2)` terms bounded by `10⁵n`, and `D₀=10⁸(n+1)⁴` makes the derivative bound smaller than `10⁻³`. Continuity keeps initially balanced row maxima strictly inside `[1/8,4]` and closes the first-exit argument. Distinguished added copies make the final pairing insertion injective even if an original edge has the same endpoints. This capacity bound uses no sampling oracle.

## 2. Subdivision and inflation (lines 708–1260)

The two intact odd-path tilings use both terminals or neither, with weight ratio exactly `λ_uv` because noncentral factors occur in equal adjacent pairs. A noncentral edge's effective strength equals its activity: an avoiding path must use its equal-activity twin at a degree-two internal endpoint. The central strength equals original `B_uv`; the proof separately covers strict bottleneck improvement and the floor-at-one case. Activities below one are allowed.

Deleted-vertex accounting follows from the direct prefix ratio. A first even hole consumes its terminal, with ratio `1` on its home side and `λ/T` on the opposite side. An odd/even neutral pair has factor `1/T_j`, `1/T_k`, or `λ/(T_jT_k)`. These factors and terminal consumption depend only on the hole set. Explicitly deleted terminals enter `R`; feasibility forbids double consumption and consuming a deleted terminal. Broken logical edges remain forbidden in the exact identity before relaxing to an inequality. Parity gives even `R`, with `|R|≤|U|`.

For the threshold pairing formula, bottom-up pairing in the laminar threshold family attains every class floor simultaneously. Internal vertices are isolated below their `T_j` threshold and connect to home above it. A same-side neutral pair costs at most one class floor; a cross pair costs the two active-hole indicators minus the connecting-λ indicator. If `λ<1`, replacing `log λ` by `log max(1,λ)` improves the charge in the correct direction. Away-home consumed holes are discarded only when not connected to their destination. The charge inequality does not silently assume all activities exceed one.

A virtual edge's height is at most its endpoints' bottleneck similarity. Thus a virtual partial matching of `a` edges contributes at most `2(D₀/D)^a`; at most `N^(2a)` choices exist because each pair shares at most two labels. The geometric sum gives `I≤1+2/99<2`. Marked identities require arbitrary positive activities; only inflation needs balance. Probe mass equals `C₀ Z_λ(-uv)/D`: the forced outer legs consume both original terminals with their baseline product weight.

## 3. Fixed-label cells and additive energy (lines 1261–2136)

The quadrangulation uses arcs of the original full cycle and fixed endpoint label sets after every recursive split or reversal. I checked each split case, strict index inequalities, parity, and admissibility. In the exterior-not-good branch, a leaf lacking the chosen label orients the subproblem to start with that label. Tree-walk avoidance then forces the repeated neighbor label. This handles recursive exteriors instead of assuming all diagonal exteriors are good.

A boundary-edge label is at distance at most one from its chord, and a leaf repair at most two. The four chords have label diameter at most two; the total collection therefore has diameter at most six. Its activity ratio is at most `192D≤1000D`; common clamping contracts logarithmic ratios.

The signed identity holds for arbitrary matching functions. The first conversion has canonical gain; the second has canonical gain plus its defined context error. Complementary arcs have the same converted matching, so each interior diagonal contributes one whole-cycle difference rather than zero. One more cell than diagonals yields the global identity with the stated signs. Canceling those complementary gains to zero would have been false; the pinned manuscript does not do that.

Switch-demand repairs of a good opposite pair cover every corner once and every internal vertex. Error guides remain legal and contain the closed `X` pattern. Interchanging `Y` patterns preserves the multiset union. Added and dropped lists have equal size at most four and all belong to one comparable edge collection, giving the `A₀⁴` product-weight bound.

The tag inverse reconstructs the original colored multiset union and its active discrepancy cycle. The orientation bit determines original layers on that cycle; other components retain their input layers. Four corners, padded edge-occurrence lists, and flags have fewer than `(10N)³⁰` possibilities. Multiplicities of coincident colored edges are retained, so the inverse does not lose doubled edges.

Rare-guide conditioning is handled correctly: summing only over guides containing `C_X` produces `p_X` in the demand mass. Jensen introduces `1/p_X`, which cancels exactly. No polynomial lower bound on that rare event is assumed. `T_X∪C_X` covers the same vertex set and is an entire fresh-pair discrepancy cycle. Its identity is specified by the closing edge in the second layer and a direction, so at most `2N` identities charge each cycle; there is no exponential path-count loss.

Toggling all earlier cycles in both demand layers preserves product weight, union, active cycle, and order, and is its own inverse. Variance and Cauchy–Schwarz sums therefore use the right demand distribution. The final bound `1000N⁴A₀⁶𝒯≤(10⁴ND)¹⁰⁰` is valid.

## 4. Arbitrary-function product gap (lines 2137–2420)

The product gap is not inferred from the additive inequality alone. Adjacent normalized laws have pointwise ratio in `[1/2,2]`, so their unequal-tier Metropolis capacities dominate half the equal-tier capacities. The pair inequality applies conditionally on fixed predecessors.

I rederived the residual assignment explicitly. Order slots high-to-low; each guide `y` follows its upper slot `x`. A residual for conditional expectation onto `U_x∪{x,y}` consists exactly of ANOVA components `f_S` with `x,y∈S` and all other coordinates before `x`. Hence `y` is last and `x` penultimate in `S`, uniquely. Distinct pairs cannot contain the same component even if they share a slot. Thus `Σ_xy ||r_xy||²≤Var f`; the argument uses orthogonality, not independence.

Conditional expectation decreases pair energy by Jensen because the kernel depends only on that pair. `E(r)≤2||r||²` holds for any stationary kernel. Averaging over `q=32L` guides gives absorbable residual coefficient `8L/q=1/4`. The remaining coefficients are `1/6` for pair energies and `4/3` for refresh energies, so `Var f≤(8M/3)E(f)`. The all-functions gap is proved rather than inserted as an unsupported oracle.

## 5. Sampler, statistics, and bit costs (lines 2166–3080)

The unit-activity dynamic program assigns vertices to matched-edge colors. Incident interfaces are disjoint; vertices in a fixed selected interface subset are exchangeable within a clique, so only its size matters. Convolutions evaluate the recurrence without exponentially enumerating all child-size tuples. Intermediate counts are at most `2^N N!`, with polynomial bit length. Sequential subset/pairing choices avoid exponential output lists.

The lazy spectral mixing bound uses the actual gap and product minimum mass. A logical pairing expands to a deterministic initial colored matching. All transitions/revelations use rational ratios with cancelling normalizers. Across unequal tiers cycle swaps correctly use Metropolis acceptance, not the acceptance-one rule for identical laws.

Balance is not presumed on failed tapes. The one-pass scaling procedure preserves every pair-product constraint and decreases coordinates only. A tight neighbor visited later cannot decrease; every row retains a final equality. On successful estimates, `g⁺≤G≤g⁺+2α` and row maxima at least `1/8` imply each updated coordinate at least `1/16`; a tight pair gives new row maximum at least `1−512α>1/4`. Unconditional clipping bounds failed-history scale multipliers in `[α/2,2]`, enough for construction and arithmetic.

The marked observables have the stated exact means in `[0,1]`. Balance gives all-real mean at least `1/2` and reweighted mean at least `1/4`, explicitly protecting ratio denominators. Independent fresh sampler runs at each adaptive stage can be coupled separately to ideal samples. Conditional Hoeffding and coupling failures sum to `13/(1000K)` per stage. Products of ratio errors and final padding bias give relative ε error. The median repetition count is odd and its tail gives logarithmic confidence cost.

Adaptive rational sizes are controlled concretely: observations share denominator `(n+1)^(n/2)` independent of scales. Every update expression follows a strictly decreasing dependency chain of at most `n` earlier updates. Across `K` stages, scale bit lengths grow linearly in `K`, not by recursive doubling. Bottleneck/profile values select activities and powers of two. Ladder powers have polynomial bit lengths. Fixed-grid categorical choices never choose a zero-mass option, have bounded coin count, and their conditional errors sum by coupling. No rejection or convergence stopping loop exists. The every-execution complexity proof is not restricted to successful tapes; the enormous numerical parameters still have fixed polynomial exponents.

## Exact scope of the unweighted sampling consequence

Lemma `lem:deletion-sampler` (lines 3203 onward) states exact infeasibility reporting, feasible perfect-matching output on every execution when feasible, TV error at most rational `0<τ<1` from uniform, and every-execution bit time polynomial in full explicit graph input length and `τ⁻¹`. It does not state exact sampling, pointwise almost-uniform probabilities, or time polynomial in `log τ⁻¹`.

I reconstructed the reduction independently. At edge `uv`, inclusion/exclusion counts are `Z(H−u−v)` and `Z(H−e)`. Exact feasibility tests remove zero branches and preserve support regardless of count failures. If both counts are positive, and relative errors `a,b` satisfy `|a|,|b|≤η`,

`|p̂−p| = z₊z₋|a−b| / [(z₊+z₋)(z₊(1+a)+z₋(1+b))] ≤ η/[2(1−η)]`.

Fresh count randomness gives conditional failure at most `2γ`; flooring costs at most `2^(−t)`. With `η=γ=τ/(8 max(1,|E|))` and `2^(−t)≤η`, branch error is at most `4η`. At most `|E|` decisions cost at most `τ/2<τ`. Ideal branch ratios telescope to uniform. Every decision removes at least one edge; feasibility forces the final edgeless residual to have no vertices. Bad estimate bit lengths are bounded by the every-execution FPRAS theorem, preserving exact ratio/floor complexity.

For the weighted project, apply this sampler to the independently proved compact graph and push forward (TV contracts under deterministic maps), or provide a separately analyzed self-reduction. The word FPRAS alone is insufficient sampling justification.

## Finite falsification attempt: label cells and repair legality

I executed an independent pure-Python reconstruction of the splitting rule without importing upstream code. It enumerated every closed label walk allowing stays, on three tree topologies and cycle lengths 4,6,8,10. For each recursive cell it asserted odd admissible sides, correct cell count, the two good-opposite-pair requirements, legality of both chord cell matchings, and legality of every good-pair repair. All passed. These are finite falsification attempts, not certification of the all-size theorem.

| Label tree | Cycle length | Closed walks | Cells checked | Repairs checked |
| --- | ---: | ---: | ---: | ---: |
| 3-node path | 4 | 35 | 35 | 70 |
| 3-node path | 6 | 199 | 398 | 796 |
| 3-node path | 8 | 1,155 | 3,465 | 6,638 |
| 3-node path | 10 | 6,727 | 26,908 | 50,397 |
| 4-node star | 4 | 58 | 58 | 116 |
| 4-node star | 6 | 418 | 836 | 1,672 |
| 4-node star | 8 | 3,106 | 9,318 | 17,652 |
| 4-node star | 10 | 23,170 | 92,680 | 170,555 |
| 5-node fork | 4 | 77 | 77 | 154 |
| 5-node fork | 6 | 565 | 1,130 | 2,260 |
| 5-node fork | 8 | 4,421 | 13,263 | 25,189 |
| 5-node fork | 10 | 35,373 | 141,492 | 260,326 |

Tree edge sets were `{01,12}`, `{01,02,03}`, and `{01,12,13,24}`. Distinct cycle vertices had membership sets `{previous edge label,current edge label}`. No density or balance condition was added. Final output: `ALL QUADRANGULATION AND REPAIR CHECKS PASSED`.

## Entropy companion and duplication boundaries

The companion allows binary integer pair multiplicities and proves deterministic `N/512^n≤A≤N`; its weighted variational interface gives an additive binary-log bracket of width `(2m−2)/ln 2`. Neither is a relative-error FPRAS for arbitrary ε. Its introduction distinguishes its compressed-multiplicity model from the simple-graph FPRAS. The singleton-loop appendix changes covering convention and proves another exponential-factor estimate, not the target weighted rational hafnian result.

No compact integer-weight path gadget, weighted rational FPRAS, or weighted approximate sampler appeared in the companion sections inspected. This is a limited direct-source duplication check, not a literature novelty verdict.

## Remaining gaps and limits

No substantive mathematical gap was found in the required manuscript dependency. This audit does not certify Lean semantics/builds, implement/run the enormous full upstream algorithm, establish external literature priority, verify the new compact weight gadget, or review the final new manuscript/publication package. Those remain separate tasks and cannot be reported complete from this document. No conjectural replacement of the central difficulty was introduced.

## Reproducer for the finite cell/repair check

Executed with Python 3.14.6, standard library only. Save the following block as a temporary `.py` file inside this project, then run `python3` on it. The assertions and printed table reproduce the finite computational claims above. The code works with uncolored endpoint pairs solely to test coverage; admissibility and repair label intersections are tested separately against the original fixed label sets.

```python
from collections import Counter

# Independent reconstruction; no source code imported.
def certify(tree, m):
    labs = tuple(sorted(tree))
    cnt = Counter()

    def check(labels):
        S = [frozenset((labels[(i - 1) % m], labels[i])) for i in range(m)]

        def good(J):
            return len(J) == 2 or bool(S[J[1]] & S[J[-2]])

        def ext(J):
            d = 1 if (J[1] - J[0]) % m == 1 else -1
            x = J[-1]
            E = [x]
            while x != J[0]:
                x = (x + d) % m
                E.append(x)
            return E

        cells = []

        def rec(J):
            s = len(J) - 1
            assert s % 2 == 1 and S[J[0]] & S[J[-1]]
            if s == 1:
                return
            P = min(S[J[0]] & S[J[-1]])
            a = [labels[J[i]] if (J[i + 1] - J[i]) % m == 1
                 else labels[J[i + 1]] for i in range(s)]
            E = ext(J)
            if good(E):
                if P not in a:
                    assert a[0] == a[-1]
                    P = a[0]
                odd = [i for i, v in enumerate(a) if v == P and i % 2]
                pos = [i for i, v in enumerate(a) if v == P]
                if odd:
                    p1, p2 = odd[0], odd[0] + 1
                elif pos[0] > 0:
                    p1, p2 = pos[0] - 1, pos[0]
                elif pos[-1] < s - 1:
                    p1, p2 = pos[-1] + 1, pos[-1] + 2
                else:
                    p1, p2 = 1, s - 1
            else:
                if P in S[E[-2]]:
                    assert P not in S[E[1]]
                    J = list(reversed(J))
                    E = ext(J)
                    a = [labels[J[i]] if (J[i + 1] - J[i]) % m == 1
                         else labels[J[i + 1]] for i in range(s)]
                assert a[0] == P
                if a[-1] == P:
                    p1, p2 = 1, s - 1
                else:
                    t = max(i for i, v in enumerate(a) if v == P) + 1
                    if t % 2 == 0:
                        p1, p2 = 1, t
                    else:
                        p1, p2 = t, s - 1
            assert 0 < p1 < p2 < s and p1 % 2 and not p2 % 2
            arcs = [J[:p1 + 1], J[p1:p2 + 1], J[p2:], E]
            assert all((len(X) - 1) % 2 and S[X[0]] & S[X[-1]]
                       for X in arcs)
            gs = [good(X) for X in arcs]
            lng = [len(X) > 2 for X in arcs]
            assert (gs[0] and gs[2]) or (gs[1] and gs[3])
            assert not (lng[0] and lng[2]) or (gs[1] and gs[3])
            assert not (lng[1] and lng[3]) or (gs[0] and gs[2])
            cells.append(arcs)
            for X in arcs[:3]:
                rec(X)

        rec(list(range(m)))
        assert len(cells) == (m - 2) // 2
        cnt['walks'] += 1
        cnt['cells'] += len(cells)

        def pat(X):
            T = [tuple(sorted((X[i], X[i + 1])))
                 for i in range(0, len(X) - 1, 2)]
            N = [tuple(sorted((X[i], X[i + 1])))
                 for i in range(1, len(X) - 1, 2)]
            chord = tuple(sorted((X[0], X[-1])))
            C = N + [chord]
            return T, N, C, chord

        def pm(edges):
            degrees = Counter(v for edge in edges for v in edge)
            assert len(edges) == m // 2 and all(degrees[v] == 1
                                               for v in range(m))

        for arcs in cells:
            patterns = [pat(X) for X in arcs]
            for pair in [(0, 2), (1, 3)]:
                pm([e for q, (_, N, _, chord) in enumerate(patterns)
                    for e in N + ([chord] if q in pair else [])])
            for pair in [(0, 2), (1, 3)]:
                if all(good(arcs[q]) for q in pair):
                    B = [e for T, _, _, _ in patterns for e in T]
                    for q in pair:
                        X = arcs[q]
                        T = patterns[q][0]
                        if len(X) == 2:
                            B.remove(T[0])
                        else:
                            B.remove(T[0])
                            B.remove(T[-1])
                            B.append(tuple(sorted((X[1], X[-2]))))
                    pm(B)
                    cnt['repairs'] += 1

    def walk(prefix):
        if len(prefix) == m:
            if prefix[-1] == prefix[0] or prefix[0] in tree[prefix[-1]]:
                check(prefix)
            return
        for nxt in (prefix[-1], *tree[prefix[-1]]):
            walk(prefix + [nxt])

    for first in labs:
        walk([first])
    return dict(cnt)


trees = {
    'path3': {0: (1,), 1: (0, 2), 2: (1,)},
    'star4': {0: (1, 2, 3), 1: (0,), 2: (0,), 3: (0,)},
    'fork5': {0: (1,), 1: (0, 2, 3), 2: (1, 4), 3: (1,), 4: (2,)}
}
for name, tree in trees.items():
    for m in [4, 6, 8, 10]:
        print(name, m, certify(tree, m))
print('ALL QUADRANGULATION AND REPAIR CHECKS PASSED')
```
