# Discovery 05 priority audit

Audit cutoff: **2026-07-22T02:42:05Z**.

This is a documented search, not a guarantee of worldwide priority. Public
work following the announced Jacobian counterexample is changing on an hourly
timescale; private, unindexed, or simultaneously released work may exist.

## Refresh: 9 August 2026

The refreshed exact-phrase, repository, arXiv, and Zenodo sweep found no
public explicit `SIC(n)` witness for `n <= 21` before this artifact's first
release on **22 July 2026 at 02:59:33 UTC**. The original priority conclusion
therefore remains source-bounded but unchanged.

The quantitative dimension headline is no longer current:

- Discovery 07 superseded it internally later on 22 July with an explicit
  `SIC(14)` obstruction at every positive exponent.
- Roy van Rijn's archival preprint, *A Four-Term Counterexample to the Special
  Image Conjecture in Three Pairs*, was deposited on Zenodo on **28 July 2026
  at 01:06:41 UTC** (DOI
  [`10.5281/zenodo.21634058`](https://doi.org/10.5281/zenodo.21634058)). It
  proves `SIC(3)` false with a four-term polynomial and a linear multiplier.
  This is later work, not prior art against the 22 July release, but it
  externally supersedes the dimension-21 benchmark.

The remaining historical content is the explicit 72-term certificate and the
nonhomogeneous scalar-parameter inversion lemma used to remove the earlier
homogenizing coordinate. Neither should be described as the current SIC
dimension record.

## Claim being audited

The construction supplies explicit rational polynomials in 42 indeterminates,

```text
A(xi,Z) = -sum_{j=1}^{21} xi_j g_j(Z),   b=Z_1,
```

such that every positive power of `A` belongs to `ker(E_21)`, while
`b*A^m` does not belong to `ker(E_21)` for infinitely many `m`. It is thus an
explicit counterexample to the Special Image Conjecture `SIC(21)`.

The audit searched specifically for any earlier:

- explicit characteristic-zero counterexample to `SIC(n)` at dimension 21 or
  below, in Zhao's polynomial/differential-operator form;
- numerical failing-dimension bound at or below 21;
- explicit pair `(A,b)` after the July 2026 Jacobian announcement; or
- nonhomogeneous scalar-parameter inversion lemma that immediately produces
  this pair.

The general existential implication “the all-dimensional Image Conjecture is
false” is not being claimed as new. Nor is the existence of an explicit SIC
counterexample: cubic homogeneous maps already public after the announcement
give such witnesses immediately by Zhao's Theorem 3.7.

## Immediate explicit predecessor: SIC(22)

Exploration 03 in this repository contains a noninjective cubic homogeneous
Keller map `I+h` in 22 variables, with nilpotent `Jh` and an exact collision.
Zhao's homogeneous theorem applied to

```text
A_22(xi,Z) = -sum xi_j h_j(Z),   b=Z_1
```

immediately gives an explicit counterexample to `SIC(22)`. The sign is
irrelevant to the power argument. Although Exploration 03 did not state this
corollary, it is mathematically available from its public certificate and must
be counted as prior art. Thompson's 24-variable and Harrison's 79-variable
cubic homogeneous maps similarly imply larger SIC witnesses.

- Exploration 03 source:
  <https://github.com/AlecKriebel/Math/tree/43447d229758c79cf5656195a275dc271147c232/discovery_03_small_vanishing_counterexample>
- Thompson snapshot:
  <https://github.com/wtho704/explicit-cubic-homogeneous-jacobian-counterexample/commit/45a7616fdf5a20c065564f2676190093722696b9>
- Harrison snapshot:
  <https://github.com/DrAlexHarrison/jacobian-anatomy/tree/7f56794da5f100dd729bd7d029a242ef17cbc5cb>

Discovery 05 saves exactly the one homogenizing coordinate from the
22-variable construction. That introduces a linear `BU` block, so Zhao's
homogeneous corollary no longer applies verbatim; the scalar-parameter lemma is
the conceptual ingredient that makes the 21-variable version work.

## Closest public sources

### Zhang's direct-consequences note

Zihan Zhang's 20 July note says explicitly that failure of the Image
Conjecture is known only “in some finite dimension” and that “this immediate
result is also only existential.” It gives no polynomial pair and no dimension
bound.

<https://zzhang-iu.github.io/papers/direct-consequences-jacobian/>

### CAOS_RESEARCH

The consequence manuscript inspected at commit
`74130c67513975fa24b27eddd3d0d15be007fdbf` states that the Image Conjecture is
false in some dimension. Its “What remains open” section lists the minimal
failing dimensions and every explicit witness as open/queued work. No SIC
certificate occurs in the repository.

<https://github.com/fsantibanezleal/CAOS_RESEARCH/tree/74130c67513975fa24b27eddd3d0d15be007fdbf>

### Harrison's anatomy project

The note inspected at commit
`7f56794da5f100dd729bd7d029a242ef17cbc5cb` records family-level falsity of
Zhao's Image Conjecture and says explicit related witnesses are in progress.
Its explicit certificate concerns the Mathieu conjecture for `SU(79)`, not
`SIC(n)`.

<https://github.com/DrAlexHarrison/jacobian-anatomy/tree/7f56794da5f100dd729bd7d029a242ef17cbc5cb>

### Guide to the Jacobian counterexample

The structured claim record inspected at commit
`d0b4e59c534ac44a3fc9311ad9d90f0dbc8ff1c8` states only that the
all-dimensional Image Conjecture is false in some finite dimension and
explicitly says it does not establish the least failing dimension.

<https://github.com/nmonson1/guide-to-jacobian-conjecture/blob/d0b4e59c534ac44a3fc9311ad9d90f0dbc8ff1c8/claims/JCG-CLAIM-0018.yml>

## Public-repository sweep

The GitHub repository API returned 29 projects created after 18 July 2026
whose indexed metadata contains “Jacobian Conjecture.” Every project was
cloned at the commit below. Across all nonbinary files, case-insensitive
searches were run for `Special Image Conjecture`, `SIC(n)`, `Image
Conjecture`, `Mathieu subspace`, `Mathieu-Zhao`, `ker E`, `Im Theta`, and
`Zhao`.

| Repository | Commit inspected |
|---|---|
| `Quantyra/jacobian-weyl-quantum-phase-space` | `358328123d565247f3bd2e506f75c7093ea79aa9` |
| `minustsquared/keller-quotient-deg4` | `d1891c3642a5eeb4fdf3c19ea0b0aa3f92d946aa` |
| `nmonson1/guide-to-jacobian-conjecture` | `d0b4e59c534ac44a3fc9311ad9d90f0dbc8ff1c8` |
| `fsantibanezleal/CAOS_RESEARCH` | `74130c67513975fa24b27eddd3d0d15be007fdbf` |
| `Muchmirul/jacobian-conjecture` | `1af839d5de65217d9f0dc9e00bb766ebc81602e4` |
| `sebmellen/jacobian-counterexample` | `fac5c7df05df6a6b2ba8d7901d4f0a9961fb853e` |
| `frozaken/dixmier3` | `8e0fcf0f3285b08f3aec6208349ea5b581fbf176` |
| `FeeJai/jacobian_conjecture` | `6029e216d466989933ebed9b6c0571c7a5bc7b9c` |
| `dasjoms/jacobian-conjecture-counterexample-exploration` | `46324c113d8b171bc63481c52c17cf48aae93034` |
| `TOTOGT/jacobian` | `48946e8950634672d2f1a550855c9c02044b2508` |
| `nasqret/jacobian-counterexample` | `a9c1695581b270bd73fc47a5ed917cac5bff8d76` |
| `FourPawnsAttack/jacobian-conjecture` | `2004bb9ef35ba5d14a582c5e08c5936d6ff0a0ba` |
| `tellurium587465/jacobian-c3-counterexample` | `36d726e8846a22b802632170946cbd00b8bcd502` |
| `toandreyras/jacobian-conjecture` | `190a830c55ab758693ef46e862c9e7603047e0ec` |
| `MikhailSzh/weighted-lift-galois` | `9193c66385ce390f61a4e25d3f5255435bfa056a` |
| `michaelmmarch/jacobian-conjecture-counterexample` | `4451ec14b99082c6f081ca23ef507a39a3ad07ad` |
| `KitaKen1/jacobian-conjecture-counterexample-lean` | `0748ab2a7e657c438eb42e653cb0917af4f1df6c` |
| `juanmgh3/quartic-resultant-keller-map` | `640322133fa4bbe172e0ac95f3c485f2c86d8cea` |
| `jzkay12/jacobian_conjecture` | `1ff68e870f66afec8c6611f910fcc8f5522fdbce` |
| `wmayner/dixmier-counterexample` | `475cea2a7449230e7d493ff29ea94fc22ce81e61` |
| `DrAlexHarrison/jacobian-anatomy` | `7f56794da5f100dd729bd7d029a242ef17cbc5cb` |
| `javieraragonmartinez/forever-was-too-optimistic` | `d4f2f58eb7dcb928e046af1aaf3a60275560b728` |
| `notactuallytreyanastasio/lol_jacobian_conjecture` | `239e881c47ba0d4f018eed32200723ddcab7215b` |
| `arnabmaiti-gif/jacobian-c4` | `7a7006b2f33a8f1364cf441433a6d68a40caa4c1` |
| `italian-brainrot/jacobian-conjecture` | `0a5d53b1687a027e8df2de68528530f8eaf5fe6a` |
| `NeilFoxAgency/jacobian-search` | `50c4b42862d905dface2f9e8c671b828269a475f` |
| `MMVFIRM/alpoge-fable-jacobian-counterexample` | `e33ba1994361d577bfa573116c17e691ddb68fef` |
| `headllesslulu/Constant-Jacobian-Noninjective-Polynomial-Map-in-Lean` | `8641448867c64f7ecd64841d64e3d5a8e54d0651` |
| `Radcliffe/jacobian-conjecture` | `d30e5a93c1b61e3a3261fd3b42557e98fa5fa616` |

Only the Harrison, CAOS_RESEARCH, nmonson guide, and a few consequence lists
mentioned the Image Conjecture explicitly. They recorded existential falsity.
Several repositories nevertheless contain cubic homogeneous Keller
counterexamples from which larger-dimensional SIC witnesses follow
immediately. None gave a dimension-21 theorem or a witness below dimension
22.

Repository searches with the metadata queries `"Image Conjecture"`,
`Mathieu Zhao`, and `SIC Jacobian`, restricted to creation after 18 July,
returned no additional repositories.

## Web, arXiv, MathOverflow, and code-index sweep

Exact and variant web searches included:

```text
"Special Image Conjecture" explicit counterexample
"Special Image Conjecture" SIC Jacobian counterexample 2026
"SIC(21)" polynomial Image Conjecture
"Image Conjecture is false" Jacobian 2026
"ker E" "Jacobian Conjecture" counterexample
"Im Theta" "Jacobian Conjecture" counterexample
"Mathieu subspace" Alpoge Jacobian counterexample
```

They surfaced the classical literature and Zhang's existential note, but no
competing characteristic-zero certificate in dimension 21 or below. GitHub's
indexed exact-phrase search for `Special Image Conjecture` likewise found only
background or consequence-tracking records.

The newest arXiv item found in the consequence literature was Christopher
Long's `arXiv:2607.18186`, which gives explicit counterexamples to the
*Gaussian Moments Conjecture*. It does not address SIC. The earlier
Discovery 04 arXiv sweep of the 100 newest “Jacobian conjecture” results had
found no other post-announcement consequence paper. Searches of MathOverflow
for `Image Conjecture`, `SIC`, and `Zhao` with the Jacobian counterexample
found no explicit pair.

## Primary-source check

Zhao's `arXiv:0902.0210`, inspected from the full PDF, proves
`ker(E)=Im(Theta)` in Theorem 3.1 and uses Abhyankar--Gurjar inversion in
Theorem 3.7. Corollary 3.8(b) treats homogeneous maps of degree at least two.
It does **not** cover the present nonhomogeneous `g` verbatim, because (5)
contains a linear `BU` block. The paper therefore proves and uses a separate
`t`-adic scalar-parameter lemma.

Derksen--van den Essen--Zhao, `arXiv:1506.05192`, Definition 2.6, calls the
assertion that `ker(E_n)` is an MZ space the “Special Image Conjecture
SIC(n).” Its Theorem 2.7 is global in dimension: if `SIC(n)` holds for every
`n`, then the Jacobian Conjecture holds in every dimension. It does not by
itself give the dimension 21 or this explicit pair.

## Permitted novelty language

Unless a later audit locates an earlier source, defensible wording is:

> We give an explicit rational 72-term counterexample to SIC(21), one
> dimension below the immediate SIC(22) consequence of Exploration 03. The
> saved homogenizing variable creates a linear block, handled by a
> scalar-parameter inversion lemma. No earlier SIC witness in dimension 21 or
> below was located.

Do not claim:

- guaranteed worldwide priority;
- the first proof that the all-dimensional Image Conjecture is false;
- the first explicit counterexample to the Special Image Conjecture;
- minimality of dimension 21 or of the 72-term support;
- that Zhao's homogeneous theorem applies verbatim to this nonhomogeneous
  map; or
- peer-reviewed or expert-verified status.
