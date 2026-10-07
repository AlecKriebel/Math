# Fresh independent priority and attribution audit, 7 October 2026

Audit begun 2026-10-07 06:50 PDT (13:50 UTC). Primary-source and remote
version checks below were made on 2026-10-07, independently of the historical
`research/priority_alternatives.md` verdict. That file was read as a baseline,
not accepted as certification. The complete `research/PROJECT_BRIEF.txt` and
`/Users/alec/Documents/Math/AGENTS.md` were read. No external individual was
contacted, and no outreach was prepared. No Git state, manuscript, publication
service, or tracker was changed. The upstream clone remained read-only.

## Decision at this checkpoint

**Do not clear the current all-algebra manuscript as a new unconditional
solution on the strength of the priority search.** There is no identified
explicit duplicate full arbitrary-von-Neumann ordinary-distance theorem and
proof in the checked current corpus, but this does not establish novelty.
The source composition for algebras with separable predual is immediate from
two already public inputs. The exact predual/isometry equivalences and the
cohomological perturbation mechanism are older contributions, not independent
new results of this project.

The newly supplied primary Roydor PDF exposes a material difference from the
historical slide-based framing: **its Theorem 1.2 assumes that the fixed
algebra has separable predual**. Accordingly, the proposed all-algebra result
is not established merely by substituting family 295 into that theorem.
An independently checked extension beyond this restriction is needed to
support the original target. A general conditional formulation was already
announced in Roydor's public October 2020 slides; any extension proof must
acknowledge that announcement rather than claiming the general conditional
statement was previously undisclosed.

This verdict is neither a declaration that the all-algebra theorem is false
nor a declaration that a novel extension exists. The separate mathematical
scope audit must establish the actual result and proof before a final
publication candidate can receive a fresh priority judgment. A failed
keyword search cannot supply that missing mathematics or prove firstness.

## Exact claim being compared

For every complex von Neumann algebra \(M\), the target asks for
\(\varepsilon_M>0\) such that every complex von Neumann algebra \(N\)
satisfying either

\[
d_{BM}(M,N)<1+\varepsilon_M,
\qquad d_{BM}(M_*,N_*)<1+\varepsilon_M
\]

is Jordan \(*\)-isomorphic to \(M\). Distance is the infimum of
\(\|T\|\|T^{-1}\|\) over bounded bijective complex-linear Banach-space maps,
with infinity when none exist. No complete boundedness, normality, fixed
representation, or multiplicativity of the initial map is assumed.

Equivalent formulations searched or inspected include isolation modulo
linear isometry among von Neumann algebras; noncommutative Amir--Cambern or
Banach--Stone rigidity; local rigidity of canonical noncommutative
\(L^1\)-spaces; Jordan rigidity of almost isometric algebra maps; and
stability of multiplication from ordinary bounded Hochschild cohomology.
These are not interchangeable with completely bounded distance, two-matrix
level distance, Kadison--Kastler distance, exact sphere isometries, or
one-sided near inclusions without an additional proved bridge.

## Primary Roydor statement and its public versions

Source actually inspected: `sources/roydor/roydor2020_user_supplied.pdf`,
431,430 bytes, SHA-256
`2320e92723841bd9414c4d846a489bbe78d01a03403b8078ca43354407cfacb4`.
The PDF identifies Jean Roydor, the title *Banach--Mazur stability of von
Neumann algebras*, and
[DOI 10.1142/S1793525321500151](https://doi.org/10.1142/S1793525321500151).
It has publisher headers marked “2nd Reading,” dated 9 December 2020,
physical pages 1--26, and a first-page publication line of 11 December 2020.
The 2022 journal citation is *Journal of Topology and Analysis* 14(3),
767--792. This receipt describes the actual early publisher PDF version
supplied by the user; it does not silently equate its physical pagination
with final journal pagination or certify that a later typeset version has
no changes.

Theorem 1.2, physical page 2, was read in text and independently rendered
and visually checked. Its assumptions are:

- \(M\) is a von Neumann algebra **with separable predual** \(L^1(M)\);
- ordinary bounded \(H^2(M,M)=0\);
- \(B^3(M,M)\) is closed in \(Z^3(M,M)\).

Its conclusion gives a positive algebra-dependent threshold and, for every
von Neumann algebra \(N\), equivalence of Jordan \(*\)-isomorphism,
algebra-space linear isometry, canonical-predual linear isometry, and the
two strict distance conditions. The comparison algebra is not separately
assumed separable in the statement. Vanishing of \(H^3\) implies the stated
closedness because it gives \(B^3=Z^3\), but \(H^3=0\) is a sufficient
stronger input, not the theorem's exact assumption.

Physical pages 20--21 introduce all bounded multilinear cochains with
self-coefficients and actual-image cohomology, then attribute associative
multiplication correction to Johnson's Theorem 2.1. Theorem 4.5 requires
\(H^2=0\) and closed \(B^3\); Remark 4.6 identifies the older
Raeburn--Taylor variant requiring \(H^2=H^3=0\). Physical pages 21--23
contain the proof of Theorem 1.2. In the type-I step it explicitly indexes
homogeneous matrix sizes by \(\mathbb N\cup\{\infty\}\). Extending that
argument to arbitrary cardinal homogeneous ranks is a mathematical task,
not a citation substitution. I did not independently validate all of this
proof in this priority audit.

Corollary 1.3, physical page 3, already states ordinary Jordan rigidity for
algebras whose type-\(\mathrm{II}_1\) summand has property \(\Gamma\), a
Cartan MASA, or hyperfinite-factor absorption; its statement does not add
the separable-predual restriction. These are inherited subcases regardless
of any unresolved scope issue in the general cohomological theorem. They
must not be promoted as this project's new contribution.

The [October 2020 primary-author slides](https://www.cirm-math.fr/RepOrga/2169/Slides/Roydor_Slides.pdf),
Theorem 2 on physical pages 28--29 and repeated later, instead state the
general conditional implication assuming \(H^2=H^3=0\), without a
separability condition. The
[CIRM meeting record](https://conferences.cirm-math.fr/2169.html) dates the
conference 12--16 October 2020. This establishes an earlier public
announcement of the conditional ordinary and predual conclusions. It does
not identify the first possible disclosure anywhere, and the slide's
unrestricted formulation must not overwrite the supplied full article's
restricted theorem. The journal received/accepted dates alone also do not
establish public availability of its theorem.

The publisher's deposited Crossref metadata reports online publication
2020-12-11 and print publication 2022-09. Its DOI record creation date
2020-10-22 is a metadata event, not a proof-disclosure timestamp. The DOI
and CIRM PDF failed in the web-reading tool on this fresh audit (the CIRM
reader returned 403); the saved actual PDF and author slides were read
locally. No new access to the final journal layout is claimed.

## Public upstream version and attribution

The fresh read-only `git ls-remote https://github.com/openai/math.git`
returned exactly HEAD and `refs/heads/main` at
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`. The public
[GitHub commit API](https://api.github.com/repos/openai/math/commits/main)
independently returned the same hash, initial commit, no parents, and
author/committer timestamp 2026-10-06T21:58:50Z. The
[repository API](https://api.github.com/repos/openai/math) reported creation
2026-10-06T21:47:02Z and `pushed_at` 2026-10-06T22:01:11Z. The public web
page displayed one commit. These checks found no later correction on
advertised upstream main at the checkpoint. They do not prove that no
correction exists on another site, private branch, fork, or subsequently.

Raw pinned family-295 introduction, manuscript README, and PDF were
retrieved by authorized public HTTPS with HTTP 200; each SHA-256 matched
the read-only local clone. The public PDF hash is
`56ec913df9fbe4a2daf371eec1cb06ddc5b544cf9defc838aab540f33171f753`.
The source theorem states ordinary bounded complex multilinear
self-coefficient Hochschild vanishing for every complex von Neumann
algebra and every degree at least two, with the actual differential image.
It includes nonseparable scope. This priority audit verifies the public
assertion and version, not the validity of its proof or Lean declarations.

The source's manuscript date, 23 September 2026, is **not** evidence of
public disclosure on that date. The prior saved audit directly checked
public availability at the same hash on 6 October PDT; this audit rechecks
it on 7 October. Repository creation and commit metadata add chronology
evidence without proving the precise minute the public became able to
read it.

The [source manuscript README](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Vanishing-of-higher-bounded-Hochschild-cohomology-September-23-2026/README.md)
supplies author **OpenAI**, title *Vanishing of higher bounded Hochschild
cohomology*, and BibTeX key
`OAI:Vanishing-of-higher-bounded-Hochschild-cohomology-September-23-2026`.
Use that supplied attribution and a pinned version link. A consequence
note must not claim independent authorship of the base cohomology result
or the previously established geometric reduction.

## Fresh companion overlap search and inspected statements

The expanded case-insensitive search covered all **8,987** upstream
`.tex`, `.md`, and `.bib` files under `preprints/` at the checked commit.
Its pattern is recorded verbatim with every hit in the ignored receipt
`sources/priority/current_sources_20261007.json`. It covers ordinary
Banach--Mazur and Banach--Stone spellings, Roydor, Amir--Cambern, and
predual/Jordan stability combinations. Ten matching lines were returned;
the relevant ones are Ricard--Roydor's cb multiplication correction in
the strong Kadison--Kastler manuscript. False positives from unrelated
Jordan domains or predual modular recovery were checked. No explicit
ordinary algebra-plus-predual corollary was found.

Exact introduction/main statements and, where material, input sections
were freshly read for these closest companions:

| Public companion | Checked scope and mechanism | Priority effect |
| --- | --- | --- |
| Family 295, *Vanishing of higher bounded Hochschild cohomology* | All complex von Neumann algebras, ordinary bounded self-coefficient cochains, degrees \(k\ge2\). The introduction mentions multiplication perturbation but gives no ordinary geometric corollary. | Base claim already public; must be attributed. |
| Family 289, *Universal strong Kadison--Kastler stability* | Small two-sided common-representation unit-ball gap, all Hilbert spaces, small implementing unitary. Its UCP criterion assumes a UCP map close in cb norm to a faithful normal representation; its product correction is cb. | Does not explicitly state the target or prove the needed abstract ordinary-distance bridge. |
| Family 288, *Kadison's similarity theorem through uniform derivation estimates* | Bounded complex-linear unital **algebra homomorphism** into operators becomes a \(*\)-homomorphism by similarity, without separability. | Initial ordinary Banach-space near-isometry lacks exact multiplicativity, so no direct duplicate/bypass. |
| *A positive solution to Tingley's problem* | Exact onto sphere isometry for arbitrary nonzero **real** Banach spaces extends to real-linear isometry. | Fixed small ordinary distortion does not supply an exact sphere isometry, and complex linearity is not asserted. |
| Family 289, *Near Inclusions of von Neumann Algebras Without Small Spatial Embeddings* | One-sided gap tends to zero on separable Hilbert spaces; all embedding unitaries stay away from the identity. No reverse gap is supplied. | Does not refute the abstract Jordan target or duplicate its proof. |
| Family 289, *Close Separable C*-Algebras Without Spatial Conjugacy* | Close norm-separable C*-algebras in common representation with equal von Neumann closures, no ambient unitary conjugacy. | Explicitly makes no abstract nonisomorphism or von Neumann counterexample claim. |

These are semantic-overlap inspections, not independent proof validation
of those companion results. The general corpus text search is a bounded
screen: unrecognized equivalent wording or material only in figures/PDFs
could escape it. The operator-algebra catalog around families 286--299 was
also read to select these companions; factor classification, generation,
bicentralizer, and C*-regularity assertions do not state the ordinary
distance target.

## Older exact formulations that require attribution

[Ricard--Roydor, arXiv:1108.1970v2](https://arxiv.org/abs/1108.1970v2),
24 June 2013, Theorem A: for any von Neumann algebra \(A\) and any
C*-algebra \(B\), sufficiently small **cb** Banach--Mazur distance forces
\(*\)-isomorphism; the v2 constant is \(4\cdot10^{-6}\). The arXiv
version history records v1 on 9 August 2011. The
[Glasgow seminar notice](https://www.gla.ac.uk/schools/mathematicsstatistics/events/details/?id=8634)
announced the cb discretization on 24 May 2011, an earlier checked
announcement rather than an exact theorem/proof source. The published
article is JFA 267(4) (2014), 1121--1136,
[DOI 10.1016/j.jfa.2014.05.018](https://doi.org/10.1016/j.jfa.2014.05.018).

The exact v2 text also contains the cb-predual observation (Remark 3.4)
and conditional **two-matrix-level** stability under \(H^2=H^3=0\)
(Remark 3.7). Neither is the ordinary-distance target.
Since \(d_{BM}\le d_2\le d_{cb}\), these older theorems cannot be
invoked merely from small \(d_{BM}\).

For the predual transfer, any bounded complex isomorphism
\(S:M_*\to N_*\) has an adjoint \(S^*:N\to M\) with inverse
\((S^{-1})^*\) and exactly the same two operator norms. Thus
\(d_{BM}(M,N)\le d_{BM}(M_*,N_*)\), for arbitrary cardinalities.
This elementary deduction makes the same algebra threshold sufficient
for the predual target. It is standard Banach duality, not a separately
invented rigidity mechanism. Exact isometry/Jordan equivalences have
older primary formulations, and Roydor already includes them in his
conditional theorem.

Specifically, [David Sherman, *Noncommutative Lp structure encodes exactly
Jordan structure*, arXiv:math/0309365v2](https://arxiv.org/pdf/math/0309365v2),
Theorem 1.1, physical page 1, establishes the equivalence for arbitrary
von Neumann algebras and \(1\le p\le\infty\), \(p\ne2\). The proof of
the \(p=1\) implication on physical page 7 takes adjoints. Its corrected
v2 was submitted 2004-09-14 22:10:07 UTC; v1 was submitted 2003-09-22
20:48:15 UTC. The [arXiv version history](https://arxiv.org/abs/math/0309365)
notes a finite type-I issue in the earlier proof. Cite Theorem 1.1 for
\(p=1\): revised Theorem 1.2 is stated for \(1<p<\infty\). This exact
isometry theorem does not turn a small but positive distortion into an
isometry.

## Independent external citation-chain reconciliation

A separate internal auditor completed an initially independent external
primary-source search at 2026-10-07 13:56:36 UTC (06:56:36 PDT). The
auditor did not find an inspected unconditional ordinary complex-linear
all-von-Neumann theorem. Its primary statement checks agree with the
scope distinctions above and add these closest nonduplicates:

- [Kuznetsova--Roydor, arXiv:1706.00701v1](https://arxiv.org/pdf/1706.00701v1),
  Theorem 1.2, physical page 3, concerns surjective **algebra
  isomorphisms** of Fourier or Fourier--Stieltjes algebras under a
  universal ordinary distortion bound. Exact algebra preservation and
  those special spaces are extra assumptions absent from our target.
  The [arXiv history](https://arxiv.org/abs/1706.00701) gives first
  submission 2017-06-02 14:40:38 UTC.
- [Cameron et al., arXiv:1209.4116v3](https://arxiv.org/pdf/1209.4116v3),
  Theorems A/B, physical pages 1--2, concern specified crossed-product
  factors. Definition 2.1, physical page 3, uses Kadison--Kastler
  Hausdorff distance of represented unit balls. The inspected v3 is
  2014-02-26, following v1 2012-09-18 and v2 2012-11-30; the
  [version record](https://arxiv.org/abs/1209.4116) and the shorter
  [arXiv:1211.6963v1 exposition](https://arxiv.org/abs/1211.6963) identify
  the relationship. This is a different metric and restricted class.
- [Peralta's 2023 primary exposition](https://arxiv.org/pdf/2308.16788)
  treats exact metric isometries. The auditor's inspected text searches
  found no Roydor, Cambern, or distortion occurrence. This is a bounded
  exclusion, not a claim to have exhaustively classified its implications.

Forward chains for Roydor's DOI were checked in
[publisher-deposited Crossref](https://api.crossref.org/works/10.1142/S1793525321500151),
[OpenAlex](https://api.openalex.org/works/https://doi.org/10.1142/S1793525321500151),
and Semantic Scholar. Each returned zero indexed citations. Crossref is
primary publisher metadata; the other two indexes were used only to
discover candidate primary sources. These counts do not imply that no
citing source exists. The Semantic Scholar Ricard--Roydor chain found
Roydor 2020, *Almost contractive maps* (2017/2018), and the Cameron
papers above. A separate arXiv-ID citation request returned HTTP 429;
its result is inconclusive, not a negative citation search. The journal
full-text access attempts failed; exact Roydor scope comparison rests on
the supplied complete DOI-identified primary artifact.

The independent auditor additionally queried the arXiv API with
`all:"Banach-Mazur" AND all:"von Neumann"`, space and double-hyphen
variants, `all:"Banach-Mazur" AND all:"Jordan"`,
`all:"Jordan" AND all:"stability" AND all:"von Neumann"`,
`all:"Amir-Cambern"`, and `au:Roydor`. No unconditional-target candidate
appeared in these returned results. Exact-title and year 2024--2026
web queries likewise added no such primary statement. These are finite
search observations, not proof of novelty.

A closing primary-source chain check followed Roydor's reference 30 to
Ricard--Roydor, *Almost contractive maps between C*-algebras with
applications to Fourier algebras*, JFA 275(1) (2018), 196--210,
[DOI 10.1016/j.jfa.2017.11.012](https://doi.org/10.1016/j.jfa.2017.11.012).
The [institutional deposit record](https://oskar-bordeaux.fr/handle/20.500.12278/193224)
and [author's older publication page](https://www.math.u-bordeaux.fr/~jroydor/?onglet=Research)
identify this source. The deposit leads to
[HAL hal-01876526v1](https://hal.archives-ouvertes.fr/hal-01876526v1),
which returned an access-denied page in the web reader. Full-text access
to that additional article was not obtained here. In the supplied complete
Roydor article, Theorem 2.6 explicitly quotes its Theorem 2.5: a quantitative
near-Kadison--Schwarz estimate for unital self-adjoint linear maps. Roydor's
Corollary 2.7 then obtains near Jordan multiplicativity, before the separate
cohomological correction step. That checked dependency is not itself a
general ordinary-distance rigidity conclusion. The institutional abstract's
Fourier-algebra norm gap is not accepted as a full theorem/proof comparison.
Additional search strings were `Ricard Roydor "Almost contractive maps"
arxiv` and `"almost contractive maps" "Banach" "Jordan"`.

## Search record, limits, and publication duplication verdict

Fresh web queries on 7 October 2026 included the following exact strings
(both hyphen and en-dash spellings were used):

- `"Banach-Mazur" "von Neumann" stability Roydor`
- `"Banach–Mazur" "von Neumann" 2026`
- `"Hochschild" "Banach-Mazur" algebras`
- `"Banach-Mazur stability of von Neumann algebras"`
- `"Banach–Mazur" "Roydor" "2024"`
- `"Banach-Mazur" "Hochschild" "2026"`
- `"von Neumann" "Jordan" "Banach-Mazur" "predual"`
- `"Vanishing of higher bounded Hochschild cohomology"`
- `"Banach-Mazur" "von Neumann algebras" -site:researchgate.net -site:scribd.com -site:eurekamag.com`
- `"Banach–Mazur stability" "separable" Roydor`
- `"Banach-Mazur" "Jordan" "nonseparable"`
- `"Banach-Mazur" "JBW" stability`

Technical claims rely on primary texts or the explicit adjoint deduction.
Secondary indexes were discovery aids only. Exact Roydor-title matches
and abstracts cannot settle scope; the primary article does. Current
metadata and search coverage may omit unindexed work. The absence of a
result, zero indexed forward citations, or a manuscript date does not
prove novelty or lack of prior dissemination.

**Duplication verdict, separated by scope:**

1. **Separable-predual algebra and predual statement:** no new rigidity
   mechanism is added by composing family 295 with published Roydor
   Theorem 1.2. Once the upstream input is valid, this is an immediate
   already-available consequence of public inputs. If written, it must
   be labeled a consequence note with exact attribution; an independent
   “new solution” claim is unsupported.
2. **Arbitrary-predual statement:** no explicit full duplicate was
   identified in the bounded current search, but the general conditional
   statement was already publicly announced in Roydor's slides. The
   supplied full article's restriction leaves the proposed composition
   incomplete. A valid new extension proof may supply a contribution,
   but that contribution has not been established by this audit.
3. **Predual proof, cb result, special classes, or small associative
   multiplication perturbation alone:** these have established reductions
   or direct prior statements and must not be presented as newly invented
   mechanisms. They do not rescue a novel full-solution claim.
4. **Entire all-algebra result and proof already public:** this stronger
   duplication condition was **not verified**. No permission to publish
   follows from that negative search finding. If a subsequently inspected
   source gives the same full statement and proof, the user instruction
   requires withholding a duplicate preprint advertised as a new solution.

Final checkpoint 2026-10-07 07:01:33 PDT (14:01:33 UTC). This assigned bounded
priority audit is 100% complete; it makes no numerical assessment of the
still separate mathematical resolution or publication readiness. Its
strongest verified update is the exact separable-predual primary theorem
scope, inherited predual mechanism, and current public upstream version,
not a novelty certificate. The full-project completion estimates belong
in the parent research log.

## Final-candidate addendum — 2026-10-07 14:25:01 UTC (2026-10-07 07:25:01 PDT)

This addendum assesses the revised actual manuscript and preserves the initial
audit above as historical evidence. Its disposition is about priority and
attribution. It does not certify a mathematical proof, the upstream theorem,
a complete publication package, or a license choice.

### Exact candidate and evidence inspected

The complete revised `manuscript/main.tex`, titled *Ordinary Banach–Mazur
rigidity of von Neumann algebras*, was read in full. This addendum binds to
SHA-256 `46a02c0cd03f798459a9cfd8fb1cd5e03c4e599208a2a53750d3b218b7e96dc4` (22,215 bytes). The initial revised source
sent for this follow-up had SHA-256
`a7542b8b497c8eaff82fb560040d71e263c05bf4ea4d7c9c74f54ef4cd36d8ca`.
A subsequent source explicitly added Ricard–Roydor Proposition 3.2 attribution
and the final layout wording says that the first block nearly preserves
multiplication and the second nearly reverses it. These changes were read,
not assumed. Any later substantive source change requires a fresh comparison;
a date or layout change alone does not establish review of different proof text.

The following complete internal reports were also read, as evidence of the
candidate's intended mechanism, not as independent primary literature:

| Report | SHA-256 |
|---|---|
| `research/roydor_full_proof_scope_attack_20261007.md` | `399a86004e38f81325b4c29a3ab8e68ed9c8d113082f7b90c9fae555686544a2` |
| `research/nonseparable_typei_extension_20261007.md` | `dbf2f609cd9d27b45265af9951d0f058b05c9a9619b29d2a08245dfa36e465f3` |
| `research/involutive_deformation_adversary_20261007.md` | `e7111f5e42e134ea9ea16f6c55cc0db0a8c42d23ceff1931ea68ebfa014040b6` |

An independent external-source comparison was performed by a separate agent,
whose follow-up checkpoint was 2026-10-07 14:16:39 UTC. It likewise reported
no inspected complete duplicate and independently identified the old
involutive perturbation and full-carrier structure-theory ingredients.
No external individual was contacted. Only this report is modified by this
follow-up; no Git operation, manuscript edit, publication, or tracker action
is part of it.

### What the actual revised manuscript adds to the old composition draft

The candidate now supplies explicit proof text at the point the original audit
identified as a scope gap. It fixes the halving central summand `P` once,
fixes the single noncentral corner `E=eOe` once for the bounded central
product of all odd finite degrees, and uses the universal cohomology input on
those two algebras. It consolidates the target's multiplicative and opposite
orientations into one twisted product before correcting on the fixed source.
For the odd portion it proves preservation of full central carriers using
Roydor's center and approximate-order estimates, then reconstructs degree
`n` from `n−1` full-carrier abelian projections and the final abelian
complement. Arbitrary infinite type-I cardinal dimensions stay in the halving
part, so the proof does not try to enumerate or cancel them.

This is a materially different candidate from simply citing the published
Theorem 1.2 for every `M`. Accordingly, the original second disposition
above, which found that composition incomplete, must not be read as a verdict
that the current explicit proof text is absent. Whether this new text
actually closes every mathematical gap is the separate proof-review task.
Reading favorable internal reports does not turn this priority audit into
that certification.

### Exact inherited contributions and the possible remaining proof contribution

| Component of the revised note | Priority disposition |
|---|---|
| Ordinary algebra and predual conclusion for separable-predual `M` | Immediate consequence of published Roydor Theorem 1.2 and the newly public attributed vanishing input, subject to that input's validity. The reduction and predual conclusion are inherited. |
| Unrestricted conditional ordinary formulation | Already announced in Roydor's 2020 author slides, Theorem 2, under `H²=H³=0`. The note correctly disclaims priority for that formulation. The published Theorem 1.2 has the narrower hypothesis and must still be cited accurately. |
| All-algebra bounded Hochschild vanishing | OpenAI family 295 is the essential newly supplied external input. This follow-on must not claim to solve that cohomology problem. Its manuscript date alone is not evidence of the date of public disclosure. |
| Near-identity correction, symmetry, quadratic iteration and ordered-product limit | Established multiplication-stability mechanisms. The explicit signed-cochain proof and its fixed-algebra constants are useful exposition/verification details; they are not a newly invented deformation mechanism. |
| Roydor normalization, center/projection rounding, compressed maps, halving geometry and two orientations | Inherited geometric machinery. The one twisted target product consolidates the already used multiplication/reversed-multiplication construction. |
| Full-corner centers, equal-carrier abelian equivalence and finite homogeneous matrix reconstruction | Classical structure theory. In particular the final `n−1+1` rank count follows from established facts and is not a new matrix-classification theorem. Odd finite type-I rigidity itself lies within the previously stated type-I/special-class scope. |
| Adjoint inequality and exact predual/Jordan equivalences | Inherited: the same algebra threshold transfers by taking adjoints; Sherman Theorem 1.1 includes the predual endpoint. This is not a separate new predual rigidity mechanism. |
| Complete source-uniform assembly through fixed `P`, fixed `E`, quantitative full-carrier preservation and odd reconstruction | The potentially distinct proof contribution. No inspected predecessor was found containing this complete arrangement. That bounded finding permits only the description “explicit proof extension/arrangement of established ingredients,” not a priority claim or a claim that every ingredient is new. |

The distinction is substantive: once the unrestricted conditional statement
is taken from the prior public announcement, the all-algebra conclusion is a
consequence of that statement and the new universal vanishing input. The
candidate's possible independent value concerns the explicit proof and its
scope/constant bookkeeping, beyond the published restricted theorem, rather
than first formulation of the conditional result. The current manuscript's
consequence/extension framing and attributions express this distinction.

### Newly checked primary passages, versions and limits

The supplied Roydor primary PDF remains the complete 26-page December 2020
publisher proof identified above; it has not been byte-compared with a final
journal-issue file. Its Theorem 4.5 and Remark 4.6, physical page 21, explicitly
give ordinary bounded algebraic stability under `H²=0` and closed `B³`,
including self-adjoint correction for involutive multiplication; the remark
attributes the `H²=H³=0` version to Raeburn–Taylor. Its pages 21–22 already
pull multiplication back through the nearly multiplicative block and use
reversed multiplication on the other block. Its main Theorem 1.2 and the
unrestricted slides therefore cannot be interchanged.
[Article DOI](https://doi.org/10.1142/S1793525321500151);
[author slides](https://www.cirm-math.fr/RepOrga/2169/Slides/Roydor_Slides.pdf).

The complete relevant Proposition 3.2 in Ricard–Roydor, physical page 6 of
`arXiv:1108.1970v2`, was inspected again. It expressly preserves involution
for involutive perturbed multiplication and describes a quadratic iteration
and convergence of the ordered correcting maps. This operator-space
statement points to the bounded antecedents; its completely bounded
hypothesis must not be silently replaced by an ordinary one. Version dates
remain v1 9 August 2011 and v2 24 June 2013, with journal publication in 2014.
[Primary version](https://arxiv.org/pdf/1108.1970v2);
[version history](https://arxiv.org/abs/1108.1970).

For the carrier/matrix ingredients, a fresh primary check of Kadison's
*Normalcy in Operator Algebras*, printed page 460 (physical page 2), found
the explicit use of equivalent abelian projections with the same central
carrier and orthogonal full-carrier abelian families on homogeneous parts.
The first page records receipt on 3 September 1961 and presentation on
22 January 1962. The retrieved 743,045-byte PDF has SHA-256
`608cb78a06d6ac181532a4e580bbc54f0ded75d770914ab4b7cfb408fb895a88`.
These old structural facts are being used in the candidate, not invented
there.
[Primary article](https://www.isibang.ac.in/~soumyashant/misc/collected-works-of-kadison/1960s/1962_NormalcyInOperatorAlgebras.pdf).

Brent Nelson's author teaching notes *Math 209: von Neumann Algebras*, dated
26 April 2017, were additionally inspected at Lemmas 5.3.11–5.3.13 and
Theorem 5.3.17 (printed pages 55–59). They give full-corner center
identification, equal-carrier abelian equivalence and homogeneous
matrix representation for arbitrary abelian centers. This is an accessible
primary exposition confirming the structure-theory facts, not a claim to
their earliest origin or a duplicate Banach–Mazur theorem.
[Author notes](https://users.math.msu.edu/users/banelson/teaching/209/209_notes.pdf).

Johnson's [1977 paper](https://doi.org/10.1112/plms/s3-34.3.439) and
Raeburn–Taylor's [1977 paper](https://www.sciencedirect.com/science/article/pii/0022123677900726)
were followed through the citation chain. Full original text was not newly
obtained from their publisher endpoints. The old involutive-deformation
disposition here rests on the actually inspected Ricard–Roydor and Roydor
primary statements, not on an assumed reading of those inaccessible
original proofs. Their exact original proof text could further clarify
antecedents, but no outreach has been prepared.

### Fresh public upstream correction check and companion scope

A follow-up `git ls-remote https://github.com/openai/math.git` still returned
HEAD/main `adc7f1241b42e322a6451854ab7e4b4c146bf78a` and no later public
ref. A fresh GitHub API read at about 14:16–14:17 UTC likewise returned that
main commit, an empty parent list, the initial-commit message and commit time
2026-10-06T21:58:50Z. Repository metadata still gave creation
2026-10-06T21:47:02Z and push 2026-10-06T22:01:11Z. A changing repository
`updated_at` field alone is not evidence of a paper correction.
[Commit API](https://api.github.com/repos/openai/math/commits/main);
[repository API](https://api.github.com/repos/openai/math).

Thus no later public upstream correction was observed in this read-only
check. This is a time-bounded statement about visible refs/API state; it does
not exclude unpublished corrections or later changes. The original
full-source companion comparison remains applicable at the unchanged
commit. The universal strong Kadison–Kastler companion starts with
two-sided distance in a common representation; the similarity companion
starts with an actual algebra homomorphism; exact Tingley/isometry results
do not supply a positive ordinary-distortion threshold. None inspected
contained the missing complete abstract ordinary-algebra plus predual proof.
Their mathematical correctness is not certified here.

A further narrow local search within the pinned vanishing, universal
Kadison–Kastler and similarity source directories for
`full.?carrier|full.?central.?support|rank.*(n.?1|odd)|halv.*product|Newton.*(cohomolog|involut)|fixed.?source|opposite.*product`
found no matching complete arrangement. This supplements the earlier
8,987-file scan; it is not a proof that no equivalent proof exists.

### Additional current queries and publication duplication verdict

Additional web queries on 7 October 2026, approximately 14:13–14:17 UTC,
included:

- `"Banach-Mazur" "central support"`
- `"Banach-Mazur" "full" "projection" "Roydor"`
- `"Banach-Mazur" "involution" "perturbation"`
- `"Hochschild" "symmetric" "perturbations" "Banach"`
- `"Roydor" "separable" "Banach-Mazur" "corner"`
- `"Banach-Mazur" "odd" "von Neumann"`
- `"von Neumann" "Hochschild" "fixed" "stability" "Roydor"`
- `"Banach-Mazur" "opposite" "cohomology"`
- `"Roydor" "fixed source" Banach`
- `"Banach-Mazur" "full central carrier"`
- `"Banach-Mazur" "rank n" "corner"`
- `"Banach-Mazur" "multiplication" "nonseparable" "von Neumann"`

The independent follow-up additionally queried
`"Banach-Mazur stability" "Newton" Roydor`,
`"von Neumann" "Banach–Mazur" "nonseparable"`,
`"Banach–Mazur stability" "odd"`,
`"Banach-Mazur" "full" "carrier"`,
`"Banach-Mazur" "Hochschild" "2026"`, and
`"type I" "equivalent abelian projections" "matrix" von Neumann pdf`.
Search-result failure, lack of indexed citations, and recent manuscript
metadata cannot establish novelty. A very recent public consequence may
also be absent from indexes, and private or informal dissemination was not
audited.

**Final-candidate priority disposition:** no inspected current primary
source was found to duplicate both the complete unrestricted ordinary
complex algebra/predual result and the candidate's complete fixed-source
proof arrangement. The stronger “entire result and proof already public”
duplication condition has therefore **not been established** by this audit.
This is not the converse claim that the result/proof is first or new.

A preprint advertised as an independently new solution would be inconsistent
with the verified inherited statement, geometry, predual reduction and
deformation mechanisms. The actual source instead frames an attributed
consequence and an explicit proof extension. On the bounded evidence here,
there is no verified complete-duplication finding that rules out continuing
review of that accurately framed candidate. Mathematical validity,
adequacy as a publishable contribution, source/package consistency and the
publication decision remain separate gates. This audit provides no final
package or publication clearance.

Final checkpoint 2026-10-07 14:25:01 UTC (2026-10-07 07:25:01 PDT). This requested bounded
priority follow-up is 100% complete. No percentage is assigned here to
mathematical discovery or publication readiness; those are outside the
priority assignment. The initial audit text remains byte-for-byte preserved.
