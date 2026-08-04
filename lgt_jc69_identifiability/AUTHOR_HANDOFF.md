# Author handoff: three-taxon LGT-JC69 identifiability

**Version 0.2 — prepared for author audit — August 2026**

## 1. Principal process theorem

Fix a known substitution rate μ > 0. Consider one sampled ortholog from each taxon on the rooted clocklike species tree `((1,2),3)`, with `0 < t1 < t2`, no incomplete lineage sorting, constant ordered-pair transfer-rate parameter λ > 0, donor retention, recipient replacement, and the backward-lineage convention stated in the manuscript. Under JC69, the exact population site-pattern distribution uniquely determines `(t1,t2,λ)`.

The result is global on the full open domain: the corrected process map `F_proc` is injective, its Jacobian has rank three everywhere, there is no exceptional interior set, and there is no second interior preimage. The proof holds for every fixed known μ > 0, not only μ = 4/3.

The theorem is specifically about the exhaustively summed ordered-pair Poisson process. It should not be paraphrased as an unqualified proof of the conjecture attached to the distributed formula map. The latter is a different map and first requires reconciliation with the process definition.

## 2. Concrete omitted-history mechanism

Choose `0 < u < v < t1`.

At time `u`, branch 1 transfers into branch 2. Traced backward, the sampled lineage from taxon 2 jumps to branch 1 and coalesces with lineage 1. The sampled cherry is now `(1,2)`. The surviving sampled ancestral lineages occupy branches 1 and 3; branch 2 carries no currently traced sampled ancestry, although it still carries a population gene copy.

At time `v`, branch 2 transfers into branch 3. Traced backward, lineage 3 jumps from recipient branch 3 to donor branch 2. This event does not immediately coalesce the two surviving sampled lineages. It does, however, move them onto branches 1 and 2, so they coalesce vertically at `t1`. Without this second transfer, they remain on branches 1 and 3 and do not coalesce at `t1`.

Thus the second transfer changes the second gene-tree coalescence time and JC69 branch lengths without changing the already formed cherry. This explains why gene-tree topology probabilities can remain correct while site-pattern probabilities change.

## 3. Exhaustive CTMC correction

After the first sampled-gene coalescence, the state is the identity of the species branch carrying no currently traced sampled ancestry. Conditional on no second transfer-coalescence, this three-state chain has generator

```text
Q = (λ/2) [ -2  1  1
             1 -2  1
             1  1 -2 ].
```

The second transfer-coalescence has hazard λ. Conditional on survival for elapsed time `s`,

```text
P_same(s) = 1/3 + (2/3) exp(-3λs/2),
P_other(s) = 1/3 - (1/3) exp(-3λs/2).
```

This sums any number of noncoalescing movements. The resulting genealogy measure is disjoint, exhaustive, and normalized, and it recovers

```text
P(T1) = 1/3 + (2/3) exp(-3λt1),
P(T2) = P(T3) = 1/3 - (1/3) exp(-3λt1).
```

## 4. Compact map and global proof

Use

```text
q = λ/(λ+μ),
x = exp(-(λ+μ)t1),
y = exp(-(λ+μ)(t2-t1)),
r = q + (1-q)y^2,
X = x^(2-q),
Z = x^3,
D = A-B,
M = (A+2B)/3.
```

The exhaustive process map is

```text
D = (1-r)x^(2+q/2),
M = q(1-X)/(2-q) + (1+2r)X/3,
C = q^2((q-2)Z+3X-(q+1))/((q-2)(q+1))
    + rZ + q(1+2r)(X-Z)/(q+1).
```

For fixed observed `(D,M)` and each `q in (0,1)`, a strictly increasing scalar equation has exactly one formal solution `X(q)`, hence unique `x(q),r(q)`. Writing `h=(1-r)/(1-q)`, physical feasibility is exactly `0<h<1`. The proof shows `dh/dq>0` whenever `h<=1`, so every crossing of `h=1` is upward and the feasible q-set is a nonempty interval.

The minor

```text
det ∂(D,M)/∂(x,r) = x^(3-q/2)[2-q(1+r)]
```

is strictly positive. An exact determinant factorization plus a convexity argument proves

```text
det ∂(D,M,C)/∂(q,x,r) < 0
```

throughout the physical domain. Consequently `C` is strictly decreasing along the entire physical fixed-`(D,M)` branch, giving a unique `q` and then a unique original parameter triple.

## 5. Joint topology-and-parameter corollary

For species topology `((1,2),3)`,

```text
A-B = (1-q)(1-y^2)x^(2+q/2) > 0
    = (4/3)(p12-p13).
```

Hence `p12 > p13 = p23`. After relabeling, the uniquely largest matching-pair aggregate identifies the rooted species-tree cherry. The principal theorem then identifies `(t1,t2,λ)`.

If μ is unknown, the common-scale transformation

```text
(t1,t2,λ,μ) -> (c t1,c t2,λ/c,μ/c)
```

leaves `q,x,y` unchanged. A time or rate scale therefore must be fixed.

## 6. Precise three-map distinction

- **`F_proc`** — the exhaustive process map above. It is globally injective and regular everywhere in the interior.
- **`F_table`** — the auxiliary fourteen-history map obtained by distinguishing the two one-transfer density types and treating the displayed transfer variables as absolute gene-tree times. It is internally normalized but omits the repeated noncoalescing movements under the manuscript’s backward-lineage convention.
- **`F_src`** — the formula/code map distributed with the frozen source versions listed below. It differs algebraically from both other maps.

### `F_table` regular double point

The exact first point is `(q,x,y)=(1/2,1/10,3/5)`. A 384-bit outward-rounded Krawczyk certificate proves a unique second root in the rational box stored in `verifier/certificate.json`. Both Jacobian determinant intervals exclude zero. The inverse function theorem therefore gives a nonempty open set of regular observed distributions, each with at least two distinct `F_table` preimages. No stronger claim is made about almost every point in the full image.

### `F_src` exact diagnostic

At `(q,x,y)=(1/2,81/100,1/10)`, the source formula gives a positive normalized aggregate distribution but

```text
A_src-B_src = -57472173/800000000,
p12-p13     = -172416519/3200000000.
```

Under the source aggregate convention,

```text
p0  = p_xxx,
p12 = p_xxy,
p13 = p_xyx,
p23 = p_yxx,
pD  = p_xyz.
```

The class multiplicities are `4,12,12,12,24`. Thus the exact diagnostic reverses the strict matching-pair inequality of `F_proc`.

## 7. Frozen source identifiers

- arXiv: `2607.14653v1`, submitted July 16, 2026.
- Audited repository: `https://github.com/lkubatko/LGT-Model`
- Audited commit: `1954b2ab92525dfdaf43b50f97dcf46658cab6c9`
- R formula: `LGT-SimulationStudy.Rmd`, function `GetSitePatternProbs`, lines 32–64.
- Notebook history definitions: `KubatkoLinzWicke-LGT-2026.nb`, text lines 430–749.
- Notebook site-pattern integrations: cell headed `Pxxx`, lines 1308–1489, with analogous later cells.

`SOURCE_SNAPSHOT.md` records SHA-256 hashes, retrieval dates, PDF page references, and the exact limitation concerning the arXiv source archive.

## 8. Reproduction

From the package root:

```bash
make verify-exact
```

The final line is:

```text
ALL EXACT CHECKS PASSED
```

The exact target runs symbolic history normalization and integration, all 64 direct JC69 pattern checks, the global-univalence algebra, topology and scale identities, the exact source diagnostic, and the directed-rounding Krawczyk certificate. It does not run Monte Carlo.

Run the numerical sanity check separately with:

```bash
make audit-simulation
```

The interval certificate is logically independent of the numerical root search: it reads only an exact target, a rational box, and a rational-decimal preconditioner, and evaluates all transcendental functions with outward MPFR rounding.

## 9. Natural collaborative follow-ups

1. Reconcile the intended transfer convention with the backward-lineage interpretation and revise the genealogy derivation accordingly.
2. Implement the corrected exact likelihood from `F_proc` and rerun the simulation study.
3. Quantify conditioning across the parameter domain, especially near `t2-t1=0` and extreme-rate regimes.
4. Compare corrected LGT site-pattern distributions with joint LGT–ILS or multispecies-coalescent models.
5. Extend the occupancy-state Markov-chain method to four or more taxa, branch-specific transfer rates, and alternative transfer conventions.
