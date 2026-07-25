# July 2026 literature audit for the H(668) program

## Status

Ramos, Hulak, and de Queiroz,
[Multiplier obstructions for Legendre pairs of length
333](https://arxiv.org/abs/2607.20765), submitted 22 July 2026, materially
changes attribution for the multiplier lanes but does not close the active
public order-three family.

Their theorem concerns pairs fixed by a common subgroup
`H <= (Z/333Z)^*`, without the prescribed length-37 compression used in
several local models here.  It proves:

```text
30 subgroups survive the necessary reduction modulo 3;
21 of those 30 are impossible;
all 19 subgroups of order at least 9 are impossible;
the nine unresolved subgroups have orders 1,2,3,3,3,3,6,6,6.
```

The result uses exact compression, row-sum certificates, value-set
enumeration, direct pseudo-Boolean bounds, and checked DRAT proofs.  It is not
a timeout report and it leaves unrestricted `LP(333)` and `H(668)` open.

A second 2026 source is directly relevant:
Kotsireas, Gallardo-Cava, Gómez, and Gómez-Pérez,
[On the search of binary Legendre pairs of length
`p q^2`](https://doi.org/10.1016/j.jsc.2026.102606).  Its proposed
`q^2`-uncompression starts from

```text
A(p,q) = [1, q chi],
B(p,q) = [1,-q chi],
```

where `chi` is the quadratic character modulo `p`.  At `(p,q)=(37,3)`,
this is exactly the prescribed length-37 compression underlying the local
`LP(333)` program.  The paper verifies its conjectured uncompression only
at smaller parameters; it does not construct `LP(333)`, classify the local
order-three Eisenstein profiles, or close `H(668)`.

## Exact correspondence

| Local lane | Paper ID and subgroup | Public status | Consequence here |
|---|---|---|---|
| column-only `h=18` | ID20, `<10,28>` | impossible | local fixed-compression proof is subsumed |
| quartic `h=9` | ID12, `<10,46>` | impossible analytically | local fixed-compression proof is subsumed |
| sextic `h=6` | ID8, `<10,64>` | impossible | local fixed-compression proof is subsumed |
| column-only `h=3`, with the local prescribed compression | ID3, `<10>` | open | public ID3 remains open; local results cover only a strict prescribed-compression slice |
| `<112>` | ID2 | open | only the prescribed fixed-compression branch is closed locally |
| `<121>` | ID4 | open | coupled 1,296-word boundary remains |
| `<211>` | ID5 | open | coupled 1,296-word boundary remains |

The public full-family conclusions for IDs 20, 12, and 8 are strictly
stronger than `LP333_MULTIPLIER_ROW_SUM.md`.  That local theorem is retained
as a compact independent proof and as the row-sum front end of the local
prescribed-compression slice of ID3, not as headline novelty.

The paper does not contain the following local results inside that
prescribed-compression slice of public ID3:

- the 1,756-word fixed-compression row-sum catalog;
- the 22 Eisenstein shards or primitive-nine labelled lift;
- the characteristic-37 and `F_729` decompositions;
- prime-167 exactness and the spectral-unit theorem;
- the exact shell exclusions `n_9=6,5,4,3`;
- the five exact `n_9=2` profile orbits;
- the eighteen-orbit classification of exact compressed profiles in the
  frozen dense `n_9=0` characteristic-two/modulo-nine search scope;
- the quadratic second-placement-digit pencil and ramified row-collapse
  theorem;
- the five-canonical-representative multiplicative class-by-row anti-tensor
  obstruction; or
- the 84-image action closure of the three nontrivial opposite structured
  families and the `F_27` minimal-submodule family.

These remain potentially novel but are restricted results within a
non-necessary fixed-compression slice of the public ID3 family.

## `q^2`-uncompression overlap

The fixed compression itself must now be attributed to the
`p q^2` paper.  It is not a local discovery.  The additional restriction by
the open order-three common multiplier `<10>` is also not a necessary
condition for an uncompression of that seed.

Within that restricted slice, the checked sources do not contain:

- the complete set of eighteen exact compressed-profile orbits found by the
  frozen 729-shard dense-`h=0` characteristic-two/modulo-nine census, all
  with shell `(0,18,6)`;
- their exact all-37-lag Eisenstein certificates and formal orbit
  distribution of twelve size-24 and six size-12 orbits;
- the half-turn splitting `36=21+15`;
- the twelve even quadrics and six odd bilinear equations;
- the complete 35-family nonidentity global fiber-twist exclusion; or
- the ternary `[27,15,4]` antisymmetric code and complete exclusion of its
  three projective minimum directions.

These are plausible new internal results about one open `p=37,q=3`
uncompression branch.  The eighteen-orbit statement is a complete
classification of the frozen `char2_mod9_intersection` compressed-profile
scope.  It is not a classification of every dense `n_9=0` labelled
placement, a complete uncompression theorem, an `LP(333)`, or an `H(668)`.

## Search consequence

The five minimal proper fixed common-multiplier supergroups of ID3 are paper
IDs

```text
8, 11, 12, 13, 14.
```

All five are publicly excluded.  Therefore any exact pair in the `<10>`
lane has fixed common-multiplier stabilizer exactly `<10>`.  A structured
search must break every proper supergroup; imposing another common
multiplier cannot produce a solution.  Additional useful structure would
have to be asymmetric between the channels, translation-twisted, or
unrelated to common multiplier invariance.

## Companion-release overlap

The paper's
[proof-artifact repository](https://github.com/Arthur742Ramos/hadamard-668-multiplier-obstructions)
contains two additional relevant notes.

Its
[mod-64 report](https://raw.githubusercontent.com/Arthur742Ramos/hadamard-668-multiplier-obstructions/main/mod64/report.md)
already states the basic exact-lift equivalence between Eliahou's special
form and `BS(84,83)`, proves a raw-distance lower bound of 64, and gives a
solver-backed distance-17 bound for a 128-modular lift.  The basic
Eliahou-to-base-sequence translation is therefore prior.  The local
adjacent-42 distance bound 80 is still a strict improvement; the companion
source does not contain the local special-distance-41 boundary, anti-fold
reduction, rank-21 lift, or certified anti-fold case.

Its
[fixed-field compression note](https://raw.githubusercontent.com/Arthur742Ramos/hadamard-668-multiplier-obstructions/main/compression_theorem/theorem_note.md)
publishes general totally real and quadratic fixed-field obstructions.  It
does not reach the local prescribed-compression ID3 profile algebra or
prime-167 exactness theorem, but generic novelty claims for fixed-field
compression must be avoided.

The April 2026 paper
[Determining the group that sends each Legendre pair to an equivalent
Legendre pair](https://arxiv.org/abs/2604.22423) must also be cited before
claiming priority for formal equivalence groups or lex-leader machinery.

The March 2026
[Ulam Frontier-HAD report](https://www.ulam.ai/research/frontier-had.pdf)
already uses `9 x 37` compression, multiplier-orbit search, SAT/SMT, and
decompression.  Those generic ingredients are prior.  No order-three
Eisenstein profile, half-turn algebra, or profile-specific fiber-twist
census was located there.

## Eliahou long-block exact-triage boundary

The companion release establishes priority for the basic translation from
Eliahou's special form to `BS(84,83)`.  The local
`eliahou_long_block_exact_triage/` artifact instead classifies the exact
search geometry and host-scale cost of canonical long cases 1 through 20.
It proves neither existence nor infeasibility of any case.

The checked companion material does not contain the local all-case
characteristic-two syndrome classification, the proof that the free
short-case reflection gauge disappears, the conditioned next-2-adic-digit
interaction theorem, or the complete `2^20` quadratic-Walsh pencils.  The
last calculation counts zeros in a 57-dimensional odd-weight affine
relaxation, not the exact weight-39 slice; its counts near `2^37` show no
low-rank mod-4 collapse.  The characteristic-three fixed-quotient graphs
still have worst treewidth 18, the naive global block table needs at least
8 TiB, and bounded exact-CRT/PB solver runs all ended `UNKNOWN`.

These are mechanically checked structural and feasibility results, not a
long-case exclusion, a construction, or evidence of convergence.  No
matching calculation was located in the checked sources, but that negative
search is not proof of priority.  The honest publication role is supporting
search-complexity analysis unless a broader theorem is extracted.

## Post-audit structured-family comparison

The anti-tensor family is a five-canonical-representative audit, not an
all-action-image theorem, and is not a fixed-common-multiplier family. Its
class-by-row term

```text
h_j F_X(j mod 6) G_X(s)
```

varies by channel and by the row law `G_X`; exact overlap replay shows that
514,912 of its 517,109 first-digit placements lie outside all five proper
fixed common-multiplier supergroups of ID3. The July multiplier theorem
therefore neither proves nor subsumes their digit-two failure. Conversely,
the anti-tensor census is much narrower than the paper's full-orbit
theorems: it excludes one explicitly parameterized placement ansatz inside
five canonical compressed-profile representatives, not any
common-multiplier subgroup or the complete ID3 lane.

The separate structured action closure repairs the corresponding scope gap
for three opposite families and the `F_27` minimal-submodule family.  It
exhausts all 84 labelled profile images and 5,900,019 attained first-digit
placements.  Its five digit-two points are five distinct verified
`C6`-rotation classes, all fixed by minimal proper multiplier supergroup
ID8, with digit-three defects `5,6,7,8,12`; zero reach digit three.  This is
consistent with the public exclusion of ID8 and supplies no surviving point
in the open exactly-`<10>` lane.  It is a mechanically useful scope
correction, not construction progress.

This comparison is based on the paper's stated limitation to untranslated
fixed common multipliers, its complete subgroup ledger, and its explicit
conclusion that nine subgroups of orders at most six remain open. No
similar multiplicative class×row placement family was found in the checked
paper or its artifact description. This is a novelty assessment, not proof
of priority across all literature.

## Conference-core and partial-difference-set comparison

The local `conference_333_group_obstruction/` theorem excludes every
normalized conference matrix of order 334 whose `333 x 333` core is
developed over a group of order 333.  Equivalently, no abelian or
nonabelian group of order 333 contains a Paley-type partial difference set
with parameters `(333,166,82,83)`.  This closes one clean conference-doubling
route to `H(668)`, but it says nothing about nongroup-developed conference
matrices, Legendre pairs, Eliahou repairs, or arbitrary Hadamard matrices.

The decisive linear-character eigenvalue identity is standard and prior.
[Nelson and Swartz](https://arxiv.org/abs/2507.23039) explicitly state it
for partial difference sets in nonabelian groups.  Moreover,
[Wang](https://arxiv.org/abs/1908.07055) already classifies the abelian
orders supporting Paley-type partial difference sets, so the abelian
order-333 exclusion is prior.  The genuinely relevant remaining context is
nonabelian: [Davis, Polhill, Smith, and
Swartz](https://doi.org/10.5802/alco.416) describe nonabelian Paley-type
partial difference sets as a recent and comparatively undeveloped area.

No explicit order-333 nonabelian statement or the local prime-quotient
corollary was located in the checked sources.  Nevertheless, the
nonexistence proof is an immediate application of the prior character
identity plus Sylow theory.  It is a useful exact route exclusion and a
natural appendix result, not a major standalone priority claim without a
broader review.  The independent 37,224-vector cyclic-quotient census and
96-profile affine-plane anatomy strengthen the certificate but are not
needed for the short proof.

## Near-Williamson comparison

Kharaghani, Mohammadian, and Tayfeh-Rezaie,
[A search for Hadamard matrices of Williamson
type](https://arxiv.org/abs/2605.08661), submitted 9 May 2026, introduces
near-Williamson matrices: one circulant block and three symmetric circulant
blocks satisfying the Williamson norm identity.  It classifies all odd
orders through 35 and gives examples through 63.  It does not give an
order-167 object or a route to one.

The local order-167 audit derives a one-defect binary reduction and an
exact gauge-fixed front-end count of about `10^48.73`.  Neither the
reduction nor that count was located in the checked paper.  This is useful
negative feasibility information, not a construction and not a
publication-level theorem by itself.  The public paper makes clear that
the family is active and should be cited if the order-167 route is ever
developed.

## Priority verdict

The five-orbit shell-two classification, the eighteen-orbit classification
in the frozen dense-`h=0` characteristic-two/modulo-nine compressed-profile
scope, the five-representative anti-tensor obstruction, the four-family
84-image action closure, and their second-digit algebra are not superseded
by the checked 2026 papers.  Their honest scope is now sharper:

```text
new-looking exact structure inside the p=37,q=3 q^2-uncompression
and a prescribed-compression slice of public open subgroup ID3,
not a classification of the complete ID3 family,
not an unrestricted Legendre-pair result,
and not an H(668) construction.
```

The former two-profile fragment is now a complete eighteen-orbit
classification of that frozen compressed-profile scope, with detached exact
certificates, so it has crossed the threshold for a scoped classification
manuscript.  The strongest paper package combines that theorem with the
all-orbit lift geometry, the complete six-profile half-turn low-shell
exclusion, and the rank-one conic-center obstruction.  A complete `3^14`
quadratic antipodal rank-two census on one priority orbit supplies an
additional finite-family theorem, with zero digit-two, margin-compatible, or
consecutive-digit survivors.  The package must be advertised as a
compressed-profile classification in the prescribed order-three
`q^2`-uncompression branch, not as a complete dense-shell classification or
as progress probability toward an unrestricted Legendre pair.

A construction claim still requires a row-margin-compatible lift through
two consecutive higher digits.  An even stronger obstruction paper would
require a whole-profile digit-three exclusion, rather than the finite
structured families presently closed.  In particular, the five
action-closure ID8-fixed digit-two points and zero digit-three points do not
change the construction verdict.

No external contact was made during this audit.
