# PR582 complete publication-package adversarial review 01

Reviewed 15 October 2026 UTC. The assigned review is complete. Mathematical,
source-scope, reproduction, artifact-integrity and PDF-layout checks pass.
**One minor citation-locator correction remains (F01 below).** No mathematical
repair or further priority clearance is required by this review before the
qualified note can proceed. After the correction, rebuild the affected files
and package and obtain the requested new comprehensive adversarial review.

This report binds to original PR head
`e4b27ac757babc1aea75149ea986ed2beea438f9`. The four-page PDF reviewed is
63,716 bytes, SHA256
`66d272a26ba0e667164aac8516b03eb0e1a78ecb4a832a20df677004d4f88346`.
The verification ZIP is 193,829 bytes, SHA256
`284975424a97eb0ad7e454b77c309e3d86d8009a5d2957a4f6ab407bcf4a5c0d`.
`INPUT_FREEZE.json` records every current publication-file fingerprint.

## Independence and constraints

Before opening the paper or older verdicts, I reconstructed the original OWR
question from its primary text and independently derived the torus-bundle
obstruction, including the exact reduced word. The machine-generated
`EARLY_INDEPENDENT_CHECKPOINT.json` records this at
2026-10-15T05:50:05.490728+00:00. The assignment supplied the proposed mechanism;
this is an independent reconstruction, not a claim of blindness to it.

Only this review directory and its ignored `.cache` were written. Main was
observed and no Git mutation, branch/index action, external publication,
tracker or PR action, person-to-person outreach, other-shard communication,
editor change or new tab was made. Primary webpages were read through ordinary
public access. No restricted full text was bypassed or requested from anyone.
No further agents were needed for this assigned adversarial scope.

## Exact theorem and universal proof

The OWR source is Motegi's contribution with Ito and Teragaito, printed
pp.491–493 in OWR8/2020, DOI
[10.4171/OWR/2020/8](https://doi.org/10.4171/OWR/2020/8).
Printed p.491 fixes the standard meridian–longitude convention and identifies
the slope normal closure with the filling kernel. The final question on p.493
fixes an arbitrary hyperbolic knot without finite surgery and asks for
`H ≅ F2` avoiding the **union** of the normal closures over `r ∈ Q`.
The printed question was visually checked in PDF page29. Zero is included;
meridional infinity is excluded. No exceptional-slope deletion is printed.

Avoiding that union is equivalent to requiring every restriction `q_r|H`
to be injective. Joint injectivity into a product, trivial intersection of
all kernels, individual generator survival and cyclic persistence are weaker
or different conditions. The paper preserves these distinctions.

For every actual embedded subgroup `H ≅ F2`, choose a free basis `a,b` and set
`c=[a,b]`, `d=aca^-1`, `w=[c,d]`. Normality of `H'` puts both `c,d` in `H'`.
Thus `w ∈ H''`. Independently reducing the expanded word gives
`xyXYxxyXYXyxxYXX`, with 16 letters and no adjacent inverse pair. By free
normal form it is nonidentity in the chosen free subgroup and in the ambient
group. Under a homomorphism into a metabelian group it dies. The choice of
word depends legitimately on the subgroup's basis; the filling slope can
remain zero for all subgroups. No arbitrary ambient generators are substituted
for a basis, and no freeness of particular knot generators is assumed.

For a torus bundle, the homotopy sequence gives an abelian kernel `Z²` and
abelian quotient `Z`. The left injection uses `π2(S1)=0`; the quotient
surjection uses the connected fiber. Its commutator subgroup lies in `Z²`,
so its second derived subgroup is trivial. The same sequence proves its
fundamental group infinite. No monodromy convention, linearity assertion,
division by `A-I` or faithful finite matrix representation is needed.

Therefore a single rational zero filling with this group defeats every `F2`.
The proof is unconditional group theory applied to credited classical
topology; finite tests below only supplement it.

## Complete no-finite-surgery hypothesis

I checked the precise primary statements and the all-rational partition:

| Rational slope | Imported classical topology | Check proving infinite group |
| --- | --- | --- |
| Outside `{0,±1,±2,±3,±4}` | Closed hyperbolic | Finite fundamental group would make its noncompact universal cover `H³` a finite cover of a compact manifold. |
| `0,±4` | Toroidal | An essential incompressible torus injects `Z²`. |
| `±1` | Seifert base `S²(2,3,7)` | Surjects onto an infinite hyperbolic triangle group; characteristic `-1/42`. |
| `±2` | Seifert base `S²(2,4,5)` | Same argument; characteristic `-1/20`. |
| `±3` | Seifert base `S²(3,3,4)` | Same argument; characteristic `-1/12`. |

This exhausts all rationals of arbitrarily large denominator, rather than a
finite sample of integral coefficients. Meridian filling gives `S³` but lies
outside the target's rational index. Being Seifert fibered alone would not
prove infinitude; the actual three negative orbifold characteristics and
triangle quotients supply the necessary step. Finite first homology is never
used as evidence of finite fundamental group.

The sources are correctly credited and versions distinguished:

- Thurston's electronic v1.1 Chapter4 supplies the figure-eight hyperbolic
  construction and Theorem4.7, printed p.61, including sign symmetry. The
  latter page was independently read and visually checked. This review does
  not re-prove the full geometric construction.
- Brittenham–Wu's inspected author preprint is headed 1995. Its pp.1–2 fix
  the framing and give Theorem1.1(4), crediting figure-eight to Thurston.
  Lemmas2.1–2.2 exclude reducing fillings and give the toroidal cases. Both
  pages were visually checked. Journal pagination is not substituted for
  the inspected preprint pagination.
- Khoi's explicit zero torus-bundle statement is in Section3's unnumbered
  figure-eight example, printed p.524. The old Section3.1 locator has been
  corrected in current presentations and remains historical only in frozen
  originals. This page was read and visually inspected.
- Gukov–Manolescu Section9.4, printed p.71, supplies the positive Seifert
  base orders. The actual printed positive2/negative3 comparison is erroneous;
  the note expressly does not use it. Negative slopes instead use Thurston's
  independent symmetry. The source display was visually checked.
- Thurston's D-shaped surgery glyph is not used as the sole zero-slope
  identification. Khoi's explicit statement removes that ambiguity.

Consequently the figure-eight knot satisfies both original hypotheses and
has `H ∩ N0 ≠ {1}` for every rank-two free subgroup. No mathematical gap was
found in the claimed negative universal answer.

## Scope, attribution and bounded priority

The current paper, README and deposition metadata all say that the result
refutes the universal affirmative assertion and leaves unresolved the search
for a positive example among other hyperbolic knots. They also leave out of
scope variants allowed to discard finitely many slopes. The printed 2026
Question7.1 remains arbitrary-`K` wording; its adjacent positive-example
motivation is described without inventing the authors' intended quantifier
or an unprinted zero exclusion. Even inheriting its no-torsion-surgery focus
does not remove figure-eight, since no finite or reducing surgery occurs.

Boden–Friedl arXiv1208.1708v1 §4.6, proof of Proposition24 p.17, equation5
explicitly supplies the free genus-one fiber, commutator longitude and
metabelian-representation relationship. I read the local statement and proof
and visually checked p.17. That ingredient is credited without attributing
the later persistent-free-subgroup answer to them.

IMT arXiv2303.15738v1 p.37 explicitly discusses the zero torus bundle and
its abelian commutator subgroup. I read and visually checked the whole page.
It is within the old Claim6.3 proof; the paper cites it only as historical
ingredient evidence. The mathematical proof uses independent classical
sources instead. The v2 record does acknowledge a gap and replacement lemma;
the one remaining correction concerns the exact metadata field, not whether
the warning exists (F01).

Both completed priority-family reports and their detailed source/version
scopes were read. The first family's timestamp correction honestly preserves
its early content and explains the ahead-of-machine handwritten label.
The full 2024 cyclic-persistence and 2019 vanishing-elements bodies remain
unread. Some longer precursors were scanned and selectively read; Bart was
compared only through relevant public indexed text. These limits are disclosed
in the paper, README and metadata. The actual 2024 title/date/article number
and subscription limit were independently rechecked on the publisher page.
No explicit earlier full target resolution was found by those bounded
families; that does not establish firstness, absence of an unindexed remark,
current worldwide open status or editorial novelty. The user explicitly
accepts candid incomplete priority, so these disclosed limits are not a new
blocker. No further clearance or human input is requested here.

## Every artifact, manifest and original binding

All 104 archive members were read, checked for duplicate paths and forbidden
raw/cache/private output classes, and reconciled against the outer manifest's
103 payload entries. Every length and SHA256 agrees. The metadata embedded
in the archive equals the complete external configuration, and the embedded
TeX equals the actual paper source. The PDF is intentionally the separate
deposit file. The archive contains no third-party PDF, OCR source text,
rendered page, account file or this live self-referential review.

All 22 original bytes were independently read through `git show` at the pinned
head and compared to the archive. Every one equals the snapshot, with no
substitution or rewrite. The current pinned snapshot hash is
`3be36a104aef0cd87652ec12ed0b12fafc2a907cd302edd2abc2667b81e439c2`.
Ten nested seals verify 90 entries, including overlapping entries: three
original JSON manifests, four family seals, the algebra child seal and two
early checkpoint seals. Current root receipts and the four closed review
families retain their historical seals. Old pending-stage/locator/flag wording
is explicitly reconciled by current correction documents; no old report is
used as proof authority. All current program sources were read.

Source-cache bytes were independently matched against 35 first-priority-family
PDF/web/text ledger entries and 12 second-family PDF/web entries. This checks
source identity and version receipts, not truth or completeness of historical
searches. The precise package-review read scopes and fresh primary webpage
rechecks are recorded in `SOURCE_RECHECK.json`.

## Actual replay, R1 and tamper tests

`review_controls.py` executes the actual current driver with a macOS sandbox
profile denying all networking. A real socket probe fails with permission
denied under the same profile. All seven registered programs then execute
successfully. Their complete resulting JSON objects match, with no normalized
fields. The child semidirect result-file comparison uses its full generated
JSON, not merely stdout. The old release and topology programs really rerun
historical tests; the README correctly calls these overlapping replays rather
than seven independent proofs. The entire frozen extraction is unchanged
afterward, and optimized Python is rejected before assertions can disappear.

The old R1 limitation was independently reproduced in two actual copied
fixtures, one synthetic PDF-named sentinel and one synthetic corpus-named
sentinel. After extending the old outer manifest, the historical verifier
passes its full mathematical replays and self-tests while reporting the
constant exclusion flag false. No third-party content is involved in these
fixtures. The actual preserved inventory remains clean.

The current snapshot-pinned gate rejects both manifested sentinels after the
new outer manifest is resealed, and rejects a changed original verifier even
when the acquisition snapshot and outer manifest are resealed. Its literal
snapshot digest is an effective extra binding. This is consistency with a
known captured inventory, not semantic authorship classification.

Ten actual current-driver tamper cases reject: unlisted added file, changed
outer payload, changed nested payload with resealed outer manifest, changed
original with resealed outer, changed acquisition snapshot with resealed outer,
both manifested R1 sentinels, changed original plus resealed snapshot, changed
nested checksum file with resealed outer, and a real leaf symlink. Thus nested
and pinned checks are exercised beyond failures at the first outer hash.

The real producer rebuilds the byte-identical ZIP in three relocated audit
trees beneath ordinary, literal `.cache`, and `scratch` external ancestors.
All original input bytes remain unchanged. Its actual local `add` function,
extracted without edits from its parsed source, rejects 29 cases involving
lexical, resolved and archive excluded components, malformed/absolute/traversal
names, private names, source escape, leaf symlinks and duplicates. Checkout
ancestors outside the audit do not affect eligibility. A further actual
producer run with six unselected benign raw/cache/private fixtures still
rebuilds the exact ZIP and includes none of them. These are operational
controls, not checklist assertions.

Independently authored `fresh_algebra.py` reconstructs the 16-letter word,
checks all 729 pairs of the nonabelian metabelian unitriangular group over
`F3`, and evaluates all 576 pairs in `S4`, finding 168 nonidentity values as
a negative control. Exact characteristic values include Euclidean and
spherical boundary controls. These finite checks supplement, and do not
replace, the universal proof or source-supported slope classification.

## PDF and metadata

I rebuilt the exact PDF in this review's cache using Tectonic0.16.9,
`SOURCE_DATE_EPOCH=1792022400` and cached resources. It is byte-identical,
63,716 bytes with the hash above, and has no compiler warning. All four
pages were independently rendered at 100dpi and visually inspected: readable
math and table, intact bibliography/links and page numbers, no clipped text,
overlap or missing citation. The fixed epoch is correctly disclosed as a
reproducibility setting rather than discovery evidence. No editor was opened
or changed and no replacement deliverable PDF is proposed.

The complete Zenodo metadata agrees with the qualified theorem, classical
credit, priority limits, extensive AI use and unrefereed status. Author,
ORCID, independent affiliation, English, CC-BY4.0, date and two actual deposit
files are coherent. It claims neither human peer review nor proof-assistant
certification. It requests no automatic GitHub release. Publication and remote
state verification remain the parent's separate lifecycle actions.

## F01 — minor current citation locator

Severity: **P3**, citation precision only. Current locations:

- `publication/zero_filling.tex:213`: says the v2 abstract reports Claim6.3's gap.
- `CURRENT_PRIORITY_ASSESSMENT.json:32`: calls the same notice the v2 abstract.

The independently opened versioned primary record
[arXiv:2303.15738v2](https://arxiv.org/abs/2303.15738v2) puts the gap warning
and Lemma6.6 replacement in **Comments**. The mathematical Abstract field
does not contain that notice. Saying “abstract” is a small locator error.

Fix both mutable occurrences to “the v2 arXiv record's Comments field” or
equivalent precise wording. Preserve the frozen originals and family seals;
none of them needs editing for this finding. Rebuild the paper and archive,
refresh build/visual/integrity receipts and the current package fingerprints,
then obtain a new comprehensive review of that revised freeze. The underlying
warning, historical attribution and independence of the present proof are
already correct. No other actionable issue was found.

## Decision and limits

**Mathematics: PASS. Priority: appropriately bounded and explicitly incomplete.
Package operation/integrity and exact PDF reproduction: PASS. Submission
readiness: one minor current locator correction remains.**

This review does not authorize a remote publication itself, certify historical
firstness, re-prove the full classical surgery classification or replace
human peer review. The exact mathematical gap for the literal universal
counterexample is none under the credited classical topology. The positive
hyperbolic-example problem and stronger historical clearance remain outside
the verified result. Final completion estimate: 100% of this assigned
adversarial review, not 100% confidence of worldwide priority.
