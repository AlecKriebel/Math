# Fresh independent complete-package review 02

Review checkpoint: 2026-10-06 21:30 PDT (2026-10-07 04:30 UTC).
Reviewer: independent AI subagent `whole_package_review02`.
Reviewed version: frozen candidate03, with the exact identities below.
This is automated adversarial review, not conventional human peer review.

## Verdict

**No substantive mathematical, semantic, novelty-framing, package, or
reproducibility defect found in candidate03.** The two fixed-binary
consequences meet the original target with cubic source-size loss. The
exponential engines are external, explicitly attributed OpenAI theorems;
the paper does not claim an independent proof of them or invented alphabet
reduction. My own reading of the original proof chains found no unsupported
mathematical obligation needed by the reduction.

There is one **minor bibliographic locator correction** (M1): the upstream
complementation result is numbered Theorem **1.1**, not Theorem 1. Correct
the two locators in `main.tex` before depositing the final bytes. This does
not change the theorem, proof, assumptions, or numerical formula. A precise
identity and locator recheck of the corrected frozen package is sufficient;
it does not call for revisiting the mathematics. Until that recheck, this
verdict applies to the exact candidate03 identities, not to later files.

I did not reproduce a Lean kernel build, print transitive axiom sets, or run
Comparator. The candidate expressly discloses the failed build attempt and
does not claim either reproduced formal verification or formalization of
the new binary result. This limitation remains real; source inspection and
finite tests are not kernel verification. The dependency validation basis
here is the independently checked handwritten proof, with actual formal
statements/semantics inspected for agreement. I found no actual
mathematical gap that would require withholding the consequence on that
basis.

## Independence and reviewed material

I began with the original target and frozen package, not a previous
favorable complete-package review. Before reading the upstream audit
reports' conclusions, I read all of `main.tex` and the full original
handwritten proof sections of both primary manuscripts. I then inspected
the actual theorem declarations and operational models, primary literature,
package code/data, and the recorded proof/audit artifacts. I have not used
`reviews/whole_package_review01.md` as evidence or as a source of reasoning.

The complete current manuscript, actual six-page deposited PDF, intended
metadata/file manifest, README, dependency ledger, current theorem,
approach table, bibliography, source manifest, binary compiler, independent
reduction checker, algebraic checkers, their data receipts, formal-scope
report, priority report, and the 28-member verification ZIP were reviewed.
The candidate's inherited lower bounds were checked against the original
primary sources in the read-only clone at
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`, not against the intentional
Comparator `sorry` templates. The clone's HEAD matched the pin and its
working tree was clean when inspected.

I performed no external contact, PR operation, commit, push, or deposit.
Read-only web accesses and local checks were the only external-source
operations. Frozen candidate files were not edited.

## Exact identities

| Intended artifact | Bytes | SHA-256 |
|---|---:|---|
| `main.tex` | 20422 | `effc61c3809b0290f4b9a063c7a7dbc389e512d38e81683d0bea0cee42f19aa5` |
| `paper.pdf` | 80290 | `8f068229d0f4222e3a46070f2e3db6ae7ce4194eb0a172696c0201f1beedeb56` |
| `README.md` | 5370 | `fca0eb6955d6c5794eaafcc132617a42706178fb16319bc1c4a6d75c3a8b3dd2` |
| `verification.zip` | 74536 | `98387ea3646a73c09db831269111e796e1ceded5a290cf518b8e140b09726a3b` |
| `zenodo-deposit.json` | 2427 | `fa6d151d0ce646e898cfb68ac7abb92c857c344488a593e138003e5cc290c5c0` |

All five identities matched `reviews/candidate03_hashes.json` exactly.
Every ZIP member's bytes and SHA-256 matched `PACKAGE_CONTENTS.json`;
every member also matched its live project counterpart at inspection.
No absolute/parent-traversal path, unexpected cache, credential, upstream
source copy, or third-party PDF is included. All 74 source entries in
`SOURCE_MANIFEST.json` matched their actual upstream bytes, sizes, and
SHA-256 values.

## Independent uniform binary-proof audit

### Exact language and source

For h>=2, b=h^2, the encoding is a bijection from relation words to
binary words of length divisible by b. Every block describes exactly one
relation; therefore there is no further malformed syntax to handle. The
language K_h is total on all binary words, rejects all nonmultiple lengths,
and contains the empty word because the empty relation product is identity.

The source's U states remember the preceding vertex and current phase
before choosing an edge. Their upper phase bound is the end of that
vertex's row. A skip is impossible at the last row bit, so every surviving
full-block branch chooses exactly one 1-bit in the correct row. After a
choice, a V state retains the endpoint through the rest of the block.
At offset ph+q the first V phase is ph+q+1>=q+1; every destination is in
its declared trimmed range. A new U(q,0) occurs only after a full block.
The right marker can accept only at these boundaries. This proves both
the path-product invariant and malformed rejection, with no alignment
assumption or promise.

The sums are |U|=(h^3+h^2)/2 and
|V|=h^3-(h^2+h)/2, giving exactly
N_h=(3h^3-h)/2+2 marked states. The ordinary epsilon-free construction
removes the two marker-specific states, adds one initial/final state whose
first-bit row is the union of the h boundary rows, and has N_h-1 states.
It accepts only after consuming the whole word. The empty-word cases and
positive marked acceptance are correct. The compiler is polynomial in h;
there is no unproved quadratic-size claim for this strict language.

### Cubic source lower bound

The h^3 pairs formed from a singleton diagonal relation, a split identity
block, and another singleton diagonal relation are a genuine fooling set.
Every diagonal has product P_p I P_p=P_p. If offsets differ, the crossed
length is 3b+t-u and is not divisible by b, since 0<|t-u|<b. At equal
offsets but distinct vertices, the crossed product P_p I P_r is empty.
All off-diagonal crosses reject, not just one of each symmetric pair.

The cut-state splice proves the bound for ordinary NFAs. For a marked
no-left source with arbitrary accepting positions, an accepted well-formed
word cannot have an accepting run before reaching its right marker: that
same finite computation would accept the word extended by one bit, which
is malformed for h>=2. Thus the chosen accepting runs cross the nonempty
prefix/suffix cut, and no-left motion permits splicing. Stays do not
consult the discarded prefix. This is a valid extension of the ordinary
fooling-set argument, with no hidden halting assumption.

### Exact target pullback

Q times b phases gives exactly sb states, all counted. The phase table
simulates each binary transition by one real transition: interior bit
motion becomes a stay with a phase change, while movement across a block
boundary changes the real input cell. The marker rows ignore phase and
reset it only on reentry to a body cell. Nonunique marker phases cause no
problem: each simulated transition projects correctly and each original
transition lifts from every configuration with the matching image.

The position map (j-1)b+t+1 on body cells, with all phases identified on
each corresponding marker, yields step-for-step correspondence from the
actual initial states. Hence finite runs, zero-step acceptance,
positive-run acceptance, partial rows, interior stays, leftward crossings,
marker loops, and infinite nonaccepting runs are preserved. Empty input
has two adjacent distinct markers in both tapes. Disabled outward entries
can be deleted without states; the README correctly documents this
normalization for the executable, which asserts legal marker rows.
Determinism is preserved because a single successor remains a single
successor.

### Full complement and quantitative loss

The complement identity in the manuscript is a disjoint union of all
nonmultiple-length strings and encodings of every empty relation product.
Its pullback is the entire upstream complement in Sigma_h*, including
the exclusion of the empty word. Restricting the pullback's image to valid
encodings does not weaken recognition on its own all-word universe.

Substitution s'=sh^2 gives exactly
2^floor((h-2)/31)<=4(sh^2+2)^2 and
2^floor((h-2)/127)<=2(sh^2+1). The rearrangements are correct. The positive
complement variant first adds one nonaccepting initial copy with the old
row and old destinations; that models exactly a required positive first
step, and gives the stated s+1 variant. Since h^3<=N_h<=2h^3, polynomial
denominators and constant subtractions are absorbed only asymptotically,
yielding 2^Omega(N_h^(1/3)). The argument does not yield a linear source
exponent or a uniform L versus NL separation. Those limits are stated in
the paper, README, and metadata.

## Independent scrutiny of pivotal upstream dependencies

I read the full deterministic proof in its introduction, matching, rank,
machines, and separation sections, and the full complementation proof in
its introduction, diagrams, nesting, amplification, and automata sections.
I also checked the actual PDFs' central theorem text against the source:
the deterministic PDF has SHA-256
`612819217a2929102a0e55c00cc4fb606b733d1f90dda513d42bf47783e0a92e`;
the complementation PDF has SHA-256
`302292b182622e126913eaa4ee8d73ecdd98b148e3364028a7cb9dfa6ac897b4`.

For determinization, the partial-functional graph's terminal component
is exactly its reachability basin and is a tree, even if unrelated
components contain cycles. The candidate-slot completion adds only fresh
leaves to that graph: target attachments are unconditional, source
attachments depend only on the source symbol, and unused slots get
distinct leaves. Thus local symbol independence is justified, rather than
assumed. Two lanes and local cyclic joins yield perfect matching diagrams
of degree 4(s+1)^2, or 4(s+2)^2 for positive acceptance. Opening the two
test leaves in the terminal tree proves the recognition criterion,
including empty input. Singleton identity contexts then distinguish every
ordered relation pair, giving the required full, unital relation-monoid
quotient.

The arbitrary-idempotent matching corner reduction deletes only its fixed
caps and uses its connector to number retained ports. Idempotence makes
the connector the inverse transversal map. This verifies multiplication
and absolute-rank preservation, including the degree-zero corner.
The bound on idempotent support and the common-support sandwich bound
follow from disjoint connector paths and preserved middle identity edges.
The minimum-rank idempotent lift is genuinely needed and is supplied;
it forces unit lifts to full-rank permutation diagrams. The 32 conjugates
have common support at most 64c. The 256 additions each retain a full
relation corner on h-31 points, after the second minimum-rank reduction,
and each costs at least half the smaller inductive bound. Comparing the
same absolute rank losses yields c>=2L(h-31), with correct base range
2..32 and recurrence threshold h=33. I found no circularity or unsupported
unit-lift assumption.

For complementation, stay closure followed by one exit move exactly
represents every finite local visit; the fresh accepting exit state can
first be entered only after original finite acceptance. Repeated cell
crossings and nonaccepting infinite runs cause no extra accepting path.
Diagram inclusion gives context-monotone acceptance, and singleton
contexts convert this to the required order-reversing full relation image.
The empty product and entire word universe agree with the new language.

Idempotent through edges are covered by recurrent-class rectangles;
corner returns persist, and a surviving recurrent loop preserves its
rectangle. The transport argument crosses witness prefixes/suffixes
through a shared rectangle. Because orientation is fixed by the old
class's sign, both crossed paths are valid even with a backward middle
edge or repeated crossings. Two target classes of one sign sharing that
rectangle must coincide. This supplies one common budget, with factor two
for the two target signs. Under nesting, the explicit absorption
identities and two through-edge factorizations place either a nonmissing
old class or two old classes inside every new class. Protected initial
labels remain recurrent, so the weighting argument charges total loss at
most twice the initial budget; it does not confuse nesting with inclusion.

The 128 conjugates, common budget <=8*64*c after transport, chain budget
<=16*64*c, and 4096 pair additions are consistent. Minimal idempotent
corners inside each current corner supply actual unit lifts and a full
relation image on h-127 retained points. Each step costs at least half
the smaller bound, yielding c>=2D(h-127) with base range 2..128 and first
inductive instance h=129. All needed structural lemmas are proved in
this manuscript rather than imported from the other headline theorem.

Actual source declarations checked include
`OAI.OneWayLiveness.main_theorem`, `deterministic_lower_bound`, both
Model modules' transition/run/acceptance definitions, and
`OAI.TwoWayComplementation.complementation_lower_bound`,
`explicit_complementation_family`, and the Transport/Nesting/ImageBound
proof code. The DMachine boundary fields prohibit outward transitions;
TwoNFA's finite head positions disable them operationally. Deleting
outward table entries makes these presentations agree. The first family
uses both reflexive and positive finite closure; the second uses reflexive
finite closure. Their source languages and state offsets match the exact
formulas cited in the note. Source-level proof bodies are real and the
operational definitions do not impose totality, global halting, a length
promise, or nonempty-input restriction. These observations are not an
elaborated axiom audit.

## Independent priority and attribution check

I consulted current primary pages on October 6, 2026 PDT:

* Kapoutsis's [2011 author PDF](https://www.andrew.cmu.edu/user/cak/reads/2011-ICALP/main.pdf),
  Section 5, and [2013 author PDF](https://www.andrew.cmu.edu/user/cak/reads/2013-IAC/main.pdf),
  Section 8: adjacency-bit reduction is older machinery; their exponential
  deterministic conclusion restricts reversals. The binary paragraph does
  not specify incomplete-block behavior. The paper's cubic claim therefore
  concerns its own explicitly total language; it does not assert that older
  authors proved or intended the same strict language.
* [Adeogun--Kapoutsis v2](https://arxiv.org/html/2602.24279v2),
  Section 4.4, Theorem 1: the unrestricted liveness bound is quadratic,
  h(h+1)/4. The comparison in the new note is accurate.
* [Their later v2 limitation](https://arxiv.org/html/2609.13793v2),
  Theorems 2.1 and 5.1: the ceiling concerns their property-chain method.
  The text defers the general-property proof while proving its
  connectivity special case. The new note cites it only as a method
  limitation, and does not invoke it as a dependency or claim it rules out
  other exponential mechanisms.
* [Guillon--Prigioniero--Taheri STACS 2026](https://drops.dagstuhl.de/storage/00lipics/lipics-vol364-stacs2026/LIPIcs.STACS.2026.48/LIPIcs.STACS.2026.48.pdf),
  introduction/Table 1 and theorem scope: same-model read-only
  complementation is described as open there; the polynomial result uses
  1-limited rewriting. The new paper does not conflate these models.
* [TheoremDB R816](https://www.theoremdb.org/records/R816/): its public
  record gives existing binary coding/macro machinery and imports only
  the quadratic theorem. It is properly identified as a public antecedent,
  not peer-reviewed certification or the source of an exponential bound.
  The note attributes it without inventing a named author or priority.

Additional searches for the exact proposed title and unrestricted
exponential binary liveness/complementation combinations did not locate a
duplicate full result. This is limited negative evidence, not proof of
priority. The actual exponential source manuscripts explicitly disclaim a
fixed-alphabet theorem. The checked sources therefore support presenting
this note as an explicit binary consequence with exact strict-language
source analysis, not a first or independently solved base-conjecture claim.

Read-only GitHub repository/commit API checks were also made to look for
later source corrections. No correction to the pinned input was observed
in the checked current repository. Internal September manuscript dates
and verified October public-release dates are distinguished in the note.
The deposited bibliography retains the upstream manuscript-specific
BibTeX entries verbatim in the supplement and uses pinned manuscript URLs
in the paper. The only locator issue found is M1 below.

## Exact-ZIP clean reproduction and PDF inspection

I independently extracted the exact frozen ZIP into a newly created
review-owned directory, verified every archive/content hash and live
counterpart, and ran its four documented check programs with Python
3.14.6. All completed successfully:

| Check | Independently reproduced result |
|---|---|
| binary compiler | 1,534 exhaustive source words; 288 partial deterministic tables; 128 seeded NFA tables; 227,136 pullback comparisons; 100 fooling pairs |
| independent reduction implementation | 16,382 ordinary source-word tests; 32,764 marked convention tests; 20,515 fooling crosses; 8,192 raw NFA tables; 4,472,832 pullback comparisons; 4,369 complement identities |
| Brauer algebra | degrees 0..4 exhaustive, including 105 degree-4 diagrams, 40 idempotents, 11,304 corner products, 7,520 supported sandwiches |
| path-diagram algebra | width-one exhaustive and reproducible seeded width-two tests, matching the supplied results |

These tests falsify finite cases and help check compiler/proof agreement;
they do not prove the exponential obstructions or replace the uniform
arguments. No test failure was hidden or repaired during this review.

Tectonic 0.16.9 built the extracted standalone `main.tex` successfully
without stderr. The resulting PDF had identical extracted text to the
deposited `paper.pdf`; its byte count differed by one because build
metadata differed, as the README allows. The actual deposited PDF was
rendered afresh with Poppler and all six pages were visually inspected.
Formulas, phase table, citations, ORCID, margins, page breaks, and references
were legible and complete, with no clipped/overlapping content or missing
reference. `pdfinfo` confirms the intended title/author, six letter-size
pages, no encryption, forms, or JavaScript. `pdffonts` reports all fonts
embedded.

The independent machine-readable receipt is
`reviews/whole_package_review02_receipt.json`; raw reproduction and page
renders are in the review-owned `reviews/review02_work/` directory.
Those scratch extraction/build/render products are not intended deposit
files and need not be committed.

## Metadata, disclosure, and licensing

The manifest lists exactly `paper.pdf`, `main.tex`, `README.md`, and
`verification.zip`, corresponding to the reviewed files above. The title,
author Alec Kriebel, ORCID, October 6 date, subject keywords, and pinned
derived-from identifiers agree with the manuscript and README. The
description accurately states the cubic source loss and inherited
exponential inputs, and discloses extensive AI use, lack of conventional
human refereeing, and nonreproduced formal validation. No unverified DOI
or publication claim is asserted in these intended metadata.

The CC BY 4.0 metadata agree with the README's license for the new note and
original supplements. Upstream retained local source copies are not in
the deposit archive, so their separate Apache license is not silently
replaced by the new license. The ZIP contains original proof/audit/code
artifacts and source fingerprints rather than third-party PDFs or caches.
No credential or fabricated coauthor/affiliation was found.

## Findings and exact remaining obligations

**M1 (minor, actionable): precise complementation theorem locator.**
In `main.tex`, the Section 4 citation after equation (2) uses
`[Theorem~1]`; the corresponding bibliography entry ends `Theorem 1.`
The original source begins its pivotal theorem with `Theorem 1.1` in
the actual PDF (and section-numbered TeX). Replace both with `1.1`.
The theorem statement, numeric dependence n=h+2, acceptance conventions,
and imported bound are otherwise correct. This is bibliographic precision,
not an unsupported dependency or proof defect.

No substantive issue is open within the reviewed scope. Publication,
remote file/metadata/checksum inspection, DOI resolution verification,
tracker insertion/readback, and final owned-file publication remain the
lead researcher's operations; I have not certified them as performed.
After the M1 correction, verify the new exact file identities, build and
ZIP integrity, and corrected rendered locators. A material mathematical
or metadata change beyond that correction would require renewed review.

Completion estimates for this review task: mathematical review 100%;
candidate-package review 100% with the minor locator correction recorded.
These are planning estimates, not mathematical evidence, and do not mean
the persistent publication/tracker objective is complete.

## Final candidate04 identity and correction recheck

Checkpoint: 2026-10-06 21:32 PDT. The lead researcher corrected M1 and froze
candidate04. I independently extracted that exact ZIP into a second clean
review-owned directory, verified the actual source diff against my saved
candidate03 extraction, checked every archive-member hash, rebuilt the
source, compared rebuilt/deposited PDF text, and rendered/inspected both
affected PDF pages (4 and 6).

The source diff consists **exactly** of the two complementation locators
changing `Theorem 1` to `Theorem 1.1`. Among ZIP members, only `main.tex`
and its entry in `PACKAGE_CONTENTS.json` changed. All proof text, compiler
code, dependency evidence, README, and intended metadata are byte-identical
to the completely reviewed candidate03 files. Every candidate04 identity
matches `reviews/candidate04_hashes.json`:

| Intended artifact | Bytes | SHA-256 |
|---|---:|---|
| `main.tex` | 20426 | `b6aa5b342c1b4a919d1f938f26f0b5f5242d7bbaac9e74540899621ff6441910` |
| `paper.pdf` | 80290 | `fc8fe182d3fc92cd61607e514cd811b268e0ab56cd84f170c6fb0f689980e215` |
| `README.md` | 5370 | `fca0eb6955d6c5794eaafcc132617a42706178fb16319bc1c4a6d75c3a8b3dd2` |
| `verification.zip` | 74534 | `6169f978956c923664207e274f93ab2c13042965206f9bb17cd1f35869794ac1` |
| `zenodo-deposit.json` | 2427 | `fa6d151d0ce646e898cfb68ac7abb92c857c344488a593e138003e5cc290c5c0` |

The independent Tectonic 0.16.9 build succeeded with empty stderr, and
its PDF's extracted text exactly matches the current deposited PDF. The
freshly rendered pages show both corrected 1.1 locators, with no changed
formula, omitted content, or layout defect. Because every executable and
data member remained byte-identical, the full candidate03 clean test
results above remain applicable; redundant mathematical test reruns were
not used as extra evidence.

A separate read-only retrieval of
`https://api.github.com/repos/openai/math/commits?per_page=1` confirmed that
the currently returned upstream head remains the pinned commit
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`. Its returned committer timestamp
is retained in `whole_package_review02_candidate04_receipt.json`.

**Final verdict for the exact candidate04 package: PASS. No substantive
issue or known remaining bibliographic/package concern was found. M1 is
resolved.** This verdict incorporates the full independent review above
and the exact correction recheck; it does not certify a future changed
package, human peer review, formal kernel reproduction, or publication/
tracker actions. The nonreproduced Lean-build limitation remains expressly
disclosed and is not converted into a claim of verified formalization.
The final independent receipt is
`reviews/whole_package_review02_candidate04_receipt.json`.
