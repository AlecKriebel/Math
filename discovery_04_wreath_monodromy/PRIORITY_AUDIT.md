# Discovery 04 priority audit

Audit cutoff: **2026-07-21T17:02:36Z**.

This is a documented search, not a guarantee of worldwide priority. The
counterexample literature is changing on an hourly timescale, some work may be
private or unindexed, and search engines lag. The defensible claim is therefore
limited to the sources and snapshots below.

**Level-three scope note.** The exact `W_3` certificate was added on 22 July,
after the displayed audit timestamp. The original sweep did include
`iterated monodromy`, `arboreal monodromy`, and composition terms and located
no competing `F^3` computation, but this document makes no stronger priority
claim for the extension than that source-bounded statement.

## Claim being audited

For the announced degree-three Keller map `F`, the exact geometric monodromies
of the second and third iterates are the full imprimitive wreath products

```text
Mon(F^2) = S_3 wr S_3,
Mon(F^3) = S_3 wr S_3 wr S_3.
```

Their degrees are nine and 27, and their orders are `6^4=1296` and
`6^13=13,060,694,016`.

The note also proves the narrower all-iterate statement that `Mon(F^m)`
contains a full `3^m`-cycle for every `m>=1`. The audit searched for iterated
or arboreal monodromy of this map as well; no such statement was located.

The audit is not searching for the general fact that a composite cover has
monodromy contained in a wreath product; that fact is classical. It is
searching for an earlier determination of equality for this map, or a theorem
that immediately implies it.

## Strongest affirmative priority evidence

The closest source is MikhailSzh and Claude, *The Antiderivative Resolvent of
the Weighted-Lift Family of Keller Maps*, inspected at commit
`9193c66385ce390f61a4e25d3f5255435bfa056a`.

- Section 4 states only the containment
  `Mon(F_0 o F_0) <= S_3 wr S_3`.
- Section 6 says that compositions contribute imprimitive groups and that
  which exact groups occur is unresolved.
- Section 8 calls the exact group of `F_0 o F_0` “a natural next computation.”

This is direct, source-specific evidence that the exact computation was open
in the nearest public monodromy project immediately before Discovery 04.

Permanent source target for citation:

<https://github.com/MikhailSzh/weighted-lift-galois/blob/9193c66385ce390f61a4e25d3f5255435bfa056a/note-weighted-lift.md>

## Important scope correction

Juan M. G. H.'s four-variable quartic-resultant construction already claims a
different imprimitive degree-eight monodromy group of order `192`, inspected at
commit `640322133fa4bbe172e0ac95f3c485f2c86d8cea`. Discovery 04 therefore must
not be advertised as the first non-symmetric or first imprimitive monodromy of
a post-announcement Keller map. Its narrower contribution is the exact group
of the canonical second and third iterates and the realizations of the
specific pairs `(9,W_2)` and `(27,W_3)`.

Source:

<https://github.com/juanmgh3/quartic-resultant-keller-map/tree/640322133fa4bbe172e0ac95f3c485f2c86d8cea>

## Public-repository sweep

GitHub repository search for projects created after 18 July 2026 with
“Jacobian conjecture” in their indexed metadata returned the projects below.
All were cloned at their displayed commit and 884 non-Git files were searched
for `wreath`, `monodromy`, `self-composition`, `iterated monodromy`,
`imprimitive`, and equivalent spellings. Duplicate local clones are omitted.

| Repository | Commit inspected | Relevant scope |
|---|---|---|
| `nasqret/jacobian-counterexample` | `a9c1695581b270bd73fc47a5ed917cac5bff8d76` | anatomy and `S_3` of `F` |
| `DrAlexHarrison/jacobian-anatomy` | `7f56794da5f100dd729bd7d029a242ef17cbc5cb` | anatomy and `S_3` of `F` |
| `MikhailSzh/weighted-lift-galois` | `9193c66385ce390f61a4e25d3f5255435bfa056a` | explicitly leaves exact composite group open |
| `tellurium587465/jacobian-c3-counterexample` | `36d726e8846a22b802632170946cbd00b8bcd502` | degree-three fibers and collisions |
| `michaelmmarch/jacobian-conjecture-counterexample` | `4451ec14b99082c6f081ca23ef507a39a3ad07ad` | exposition of `F` and its `S_3` group |
| `javieraragonmartinez/forever-was-too-optimistic` | `d4f2f58eb7dcb928e046af1aaf3a60275560b728` | anatomy and reductions |
| `Quantyra/jacobian-weyl-quantum-phase-space` | `ea0ced4434cf55fe243aceab5a7e6276f358c45f` | program plans; composite monodromy pending |
| `fsantibanezleal/CAOS_RESEARCH` | `272f2dcc883a801e3aa85894ddca41db57cbe7e2` | plane-search program |
| `Radcliffe/jacobian-conjecture` | `d30e5a93c1b61e3a3261fd3b42557e98fa5fa616` | no competing claim found |
| `FourPawnsAttack/jacobian-conjecture` | `2004bb9ef35ba5d14a582c5e08c5936d6ff0a0ba` | no competing claim found |
| `toandreyras/jacobian-conjecture` | `190a830c55ab758693ef46e862c9e7603047e0ec` | no competing claim found |
| `Muchmirul/jacobian-conjecture` | `b022709805f39346faa609479ca2d1c5e3dc0499` | visualization |
| `jzkay12/jacobian_conjecture` | `1ff68e870f66afec8c6611f910fcc8f5522fdbce` | no competing claim found |
| `italian-brainrot/jacobian-conjecture` | `0a5d53b1687a027e8df2de68528530f8eaf5fe6a` | no competing claim found |
| `FeeJai/jacobian_conjecture` | `c556f5649fc3156a1570ed201214b1b7a36e23dd` | no competing claim found |
| `notactuallytreyanastasio/lol_jacobian_conjecture` | `239e881c47ba0d4f018eed32200723ddcab7215b` | verification critique |
| `KitaKen1/jacobian-conjecture-counterexample-lean` | `0748ab2a7e657c438eb42e653cb0917af4f1df6c` | Lean verification of `F` |
| `arnabmaiti-gif/jacobian-c4` | `7a7006b2f33a8f1364cf441433a6d68a40caa4c1` | four-dimensional construction |
| `juanmgh3/quartic-resultant-keller-map` | `640322133fa4bbe172e0ac95f3c485f2c86d8cea` | different imprimitive order-192 group |
| `MMVFIRM/alpoge-fable-jacobian-counterexample` | `e33ba1994361d577bfa573116c17e691ddb68fef` | exact verification of `F` |
| `headllesslulu/Constant-Jacobian-Noninjective-Polynomial-Map-in-Lean` | `8641448867c64f7ecd64841d64e3d5a8e54d0651` | Lean verification of `F` |
| `wmayner/dixmier-counterexample` | `475cea2a7449230e7d493ff29ea94fc22ce81e61` | Dixmier consequence |
| `NeilFoxAgency/jacobian-search` | `50c4b42862d905dface2f9e8c671b828269a475f` | plane-search experiments |

Only the weighted-lift note and the quartic-resultant note contained relevant
composition/imprimitive-monodromy statements. Neither gives the exact group of
`F^2` or `F^3`.

## Web, arXiv, and MathOverflow sweep

Queries included exact and variant searches for:

```text
"S_3 wr S_3" Jacobian
"wreath product" "Jacobian conjecture" counterexample monodromy
Alpoge composition monodromy wreath product Keller map
"degree 9" monodromy Jacobian Keller map
"F_0 o F_0" monodromy Jacobian
"F₀∘F₀" monodromy
```

The arXiv API was queried for the 100 newest records matching “Jacobian
conjecture.” The only post-announcement record returned at the cutoff was
arXiv:2607.18186 on the Gaussian Moments Conjecture; no composite-monodromy
paper was indexed.

MathOverflow 513387 determines the original map's degree-three `S_3`
monodromy, not an iterate. MathOverflow 513390 concerns weighted-lift
constructions, not exact iterated monodromy. Zhang's *Direct Consequences of a
Counterexample to the Jacobian Conjecture*, Gallagher's weighted-lift page,
and the other public consequence notes inspected earlier do not state the
degree-nine wreath equality.

General papers on monodromy of composed univariate polynomials and Belyi maps
were also found. They explain why a wreath product is the natural upper bound,
but their hypotheses do not immediately determine the self-composition of this
multivariate nonproper Keller map.

## Permitted novelty language

Unless a later audit finds an earlier source, defensible wording is:

> We determine the exact geometric monodromy of the second and third iterates
> of the announced three-dimensional Keller map. They are the full imprimitive
> wreath products `W_2` and `W_3`, of orders `1296` and `13,060,694,016`.
> The level-two result answers a computation explicitly left open in the
> closest public monodromy study. We also exhibit full-cycle inertia of length
> `3^m` for every iterate `F^m`.

Do not claim:

- the first non-symmetric or imprimitive Keller monodromy;
- the first observation that compositions are contained in wreath products;
- guaranteed worldwide priority;
- an all-iterate arboreal theorem;
- any priority claim for the separately certified `W_4` upgrade without a
  new source audit specifically covering level four.
