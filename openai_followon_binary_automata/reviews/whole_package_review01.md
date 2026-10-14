# First independent complete-package adversarial review

Reviewer: independent AI subagent `whole_package_review01`.
Date: October 6, 2026, America/Los_Angeles.
Original target: explicit ordinary binary 1NFA families of polynomial source
size with unrestricted 2DFA lower bounds (2^{n^{\Omega(1)}}), and the analogous
read-only binary 2NFA complementation lower bound, with exact full-word
semantics, independently audited dependencies, priority attribution, and a
complete reproducible publication package.

## Verdict and exact reviewed version

**No substantive mathematical, semantic, attribution, disclosure, licensing,
PDF, or final-package defect was found in candidate03.** This verdict is
based on the independent proof reading and checks recorded below, not on
the existence of Lean directories or earlier favorable agent verdicts.
It is an automated review, not conventional human peer review or a claim
of infallibility. A second fresh complete-package reviewer is still required
by the human publication protocol; this review does not authorize describing
a draft deposit as published or claiming that the tracker has been updated.

The five frozen candidate03 identities are:

| File | Bytes | SHA-256 |
|---|---:|---|
| main.tex | 20422 | effc61c3809b0290f4b9a063c7a7dbc389e512d38e81683d0bea0cee42f19aa5 |
| paper.pdf | 80290 | 8f068229d0f4222e3a46070f2e3db6ae7ce4194eb0a172696c0201f1beedeb56 |
| README.md | 5370 | fca0eb6955d6c5794eaafcc132617a42706178fb16319bc1c4a6d75c3a8b3dd2 |
| verification.zip | 74536 | 98387ea3646a73c09db831269111e796e1ceded5a290cf518b8e140b09726a3b |
| zenodo-deposit.json | 2427 | fa6d151d0ce646e898cfb68ac7abb92c857c344488a593e138003e5cc290c5c0 |

`whole_package_review01_hashes.json` additionally records the reviewed ZIP
contents and independently read primary-source identities. Candidate01 had
the same paper/source/README/metadata but an older supplement. During this
review the root repaired the supplementary clean-reproduction helper, included
the standalone manuscript in the ZIP, and obtained an explicit historical-audit
clarification. Candidate03 is the version covered by this final verdict.

## Independent mathematical scrutiny

I read the entire standalone main.tex and the actual six-page paper.pdf.
I checked the source compiler, ordinary-NFA conversion, fooling set, target
compiler, complement identity, numerical rearrangements and asymptotics
directly, then read both original primary proof mechanisms independently.

1. **Total language and source.** Every (h^2)-bit block codes exactly one
   relation. The source's (U(p,t)) states retain the incoming vertex until
   one edge in row p is selected; the last row position has no skip rule.
   Afterwards (V(q,t)) retains the selected endpoint until the full block
   ends. Every destination is in its declared range. The ranges yield
   (|U|=(h^3+h^2)/2), (|V|=h^3-(h^2+h)/2), and exactly
   ((3h^3-h)/2+2) marked states. Only boundary states can accept at the
   right marker. Thus incomplete blocks reject, the empty input accepts
   through two legal transitions, and complete blocks accept precisely the
   nonempty relation product. The ordinary source removes the two marked
   special states and adds one accepting initial state whose consuming bit
   rows are their explicitly specified unions. It uses one fewer state,
   one initial state, no markers and no epsilon transitions.
2. **Cubic lower bound.** The (h^3) displayed pairs have accepted diagonals.
   Unequal cut phases give a nonmultiple length (3b+t-u); equal cut phases
   with unequal vertices give (P_pI_HP_r=\varnothing). The cut-state
   splicing proof is valid for ordinary NFAs. In the right-only marked
   model, an accepting run cannot accept before reaching the right marker,
   since that same finite run would accept a one-bit extension of an
   accepted, complete-block word. Every chosen suffix is nonempty and
   suffix runs cannot inspect the discarded prefix, so stays do not defeat
   the cut argument. The cubic order is specific to this strict total
   language and is not asserted for alternative encodings.
3. **Exact target pullback.** The (sh^2) states correctly track the target
   state and virtual bit position. Internal target left/right moves become
   real stays; block-crossing moves update the real head and reset phase.
   At markers the target row ignores phase; entry into a body block resets
   it as required. Projection at a marker intentionally identifies phases,
   and every outgoing original step lifts from each phase. Therefore the
   proof is not assuming a false unique marker phase. Finite and infinite
   runs correspond transition by transition, and acceptance and positive
   run length are preserved. Partial rows remain partial and determinism
   is preserved. The empty input still has two adjacent distinct markers.
   Disabled outward entries can be removed at zero state cost, matching
   the executable interface's legal-row assertions.
4. **Complement and quantitative loss.** The full complement is the disjoint
   union of malformed lengths and encodings of the full relation-word
   complement. Pullback restriction to valid codewords therefore recognizes
   product emptiness on every relation word, including epsilon, which is
   absent from both complements. Substitution (s'=sh^2) gives exactly
   the displayed deterministic and nondeterministic inequalities. Square
   roots and constant subtractions are correct. Polynomial denominators
   are absorbed only asymptotically. Since (h^3\le N_h\le2h^3), the
   exponent is proportional to (N_h^{1/3}), and the ordinary source has
   the same order. The positive-run initial-copy variant is valid. No
   (2^{\Omega(n)}), L versus NL, uniform small transition-table theorem,
   or stronger complexity-class separation is claimed.

The lower-bound inputs themselves were scrutinized, not merely quoted.
For determinization I read the original manuscript's introduction,
matching.tex, rank.tex, machines.tex and separation.tex. The terminal's
functional-graph component is a tree; unused candidate slots introduce
leaves without creating nonlocal symbol dependence. Local tour contraction
supplies the quadratic matching degree and correct acceptance test. Singleton
relation contexts give a well-defined unital surjection onto the entire
relation monoid, including the empty product. The idempotent corner reduction
preserves absolute rank; its common support set is justified by disjoint
transversal paths. Minimum-rank idempotents provide actual permutation
lifts, and the second local reduction verifies the smaller induction
hypotheses. All 256 additions spend the same 64c support budget, while
each loses at least half the (h-31) instance. The recurrence and its
base interval (2\le h\le32) are consistent.

For complementation I read the original introduction, diagrams.tex,
nesting.tex, amplification.tex and automata.tex. The path-diagram model
uses finite local stay closures and supports arbitrary repeated crossings.
Its added exit is only a representation device. Singleton contexts establish
the full order-reversing relation image. Recurrent rectangles cover all
idempotent through edges; crossing witnesses sharing one rectangle merges
target recurrent classes of the same sign. This yields one common transport
budget, including backward middle edges. The nested-class dichotomy and
protected-label weight argument compare losses while identities change.
Minimal idempotent corners supply unit lifts without an unsupported general
lifting assumption. Each smaller relation corner is the full monoid on
(h-127) points and retains order reversal. The 4096-step budget gives
(c\ge2D(h-127)=D(h)), with base interval (2\le h\le128), and
(D(h)\le2m) at (m=s+1). I found no circular central replacement claim
or hidden target restriction in these arguments.

I also read the actual Automata/Main.lean, Model.lean and Recognition.lean,
and TwoWayAutomata/Main.lean, Model.lean and ExplicitFamily.lean statements
and bodies. The models and numerical hypotheses agree with the cited
mathematical theorems. Comparator placeholders were not proof evidence.
All 74 entries of SOURCE_MANIFEST.json were independently matched against
the source clone's bytes and SHA-256 values. This is source validation;
I did not run the upstream Lean build, #print axioms or Comparator. The
published disclosure of that failed reproduction is accurate. The explicit
supplementary addendum correctly separates a successful formal-verification
claim from the independently inspected handwritten proof.

## Priority and claim scope

I independently opened and inspected the primary Kapoutsis 2011 Section 5
and expanded 2013 Section 8 binary paragraphs, the exact Adeogun–Kapoutsis
2026 Theorem 1 and later property-chain Theorem 2.1, and the STACS 2026
Guillon–Prigioniero–Taheri target model and Theorem 4.1. I inspected the
public R816 coding explanation and the original Sakoda–Sipser technical
report record, and checked current version histories. The manuscript's
distinctions are appropriate: established adjacency coding, previously
restricted targets or quadratic bounds, and stronger rewrite/annotation
targets are not recast as unrestricted exponential read-only results.
The R816 record is a relevant coding antecedent, not an exponential
input or independent priority certification.

Searches for the exact title and for binary liveness/unrestricted exponential
automata results did not reveal the entire proposed result already public.
That negative search is not a proof of global novelty. The note makes
no first claim and clearly frames its result as an explicit consequence of
the two OpenAI theorems, with strict-block source accounting. No inspected
antecedent makes that attribution false or requires withholding this
consequence as an advertised independent base breakthrough.

Fresh read-only `git ls-remote` and the GitHub commit API returned
adc7f1241b42e322a6451854ab7e4b4c146bf78a for both upstream HEAD and main,
and one Initial commit dated 2026-10-06T21:58:50Z. Thus no later upstream
correction was present at this review. The September manuscript dates are
correctly kept distinct from verified October public availability.

Primary online locations inspected on October 6, 2026:

- https://www.andrew.cmu.edu/user/cak/reads/2011-ICALP/main.pdf
- https://www.andrew.cmu.edu/user/cak/reads/2013-IAC/main.pdf
- https://arxiv.org/html/2602.24279v2 and its submission-history page
- https://arxiv.org/html/2609.13793v2 and its submission-history page
- https://drops.dagstuhl.de/storage/00lipics/lipics-vol364-stacs2026/LIPIcs.STACS.2026.48/LIPIcs.STACS.2026.48.pdf
- https://www.theoremdb.org/records/R816/
- https://www2.eecs.berkeley.edu/Pubs/TechRpts/1978/28933.html
- https://api.github.com/repos/openai/math/commits?per_page=3

## Executed checks and package inspection

I independently reran all four advertised scripts. Every run exited zero.
The compiler run reproduced 1,534 source words and 227,136 target comparisons;
the independent adversary run reproduced 16,382 ordinary source words,
32,764 marked-source comparisons, 20,515 fooling crosses, 4,472,832 target
comparisons and 4,369 complement identities. The Brauer check reproduced
all degrees 0 through 4, including degree-4's 105 diagrams, 40 idempotents
and 11,304 corner products. The path-diagram check reproduced exhaustive
width one and seeded width two, including all 65,536 width-two diagrams
and 12,821 idempotents. These are finite falsification checks, not uniform
lower-bound certificates.

I verified the exact candidate03 ZIP's CRC, safe member paths, every one
of its 27 listed content hashes/byte counts, matching included main.tex,
and presence of the clarified dependency-audit addendum. I extracted that
ZIP into a fresh project-local temporary directory and ran its own
code/clean_reproduction.py. It recreated its temporary directory, reran
all four scripts and compiled the standalone source successfully. The ZIP
hash was unchanged before and after this final test. The complete output
is in whole_package_review01_artifacts/exact_zip_reproduction.json;
the earlier candidate02 extraction is separately labeled rather than
misrepresented as the final candidate.

I rendered and visually inspected all six PDF pages, extracted the text,
and checked pdfinfo and pdffonts. The source/PDF agree, the title and author
metadata are correct, all fonts are embedded, references resolve in the
rendered text, and no clipped formula, overlapping element, missing glyph
or unreadable page was found. The final exact-extraction build supplies an
actual PDF, not just a preview. Build timestamps may alter PDF bytes.

The README, theorem ledger, dependency ledger, approach table, priority
audit, all dependency audits, compiler notes, earlier reduction review,
recorded test receipts, bibliography and deposit metadata/file list were
checked. The four upload files match the stated title, sole author, ORCID,
October 6 date and CC BY 4.0 declaration. No affiliation or coauthor is
invented; the AI and no-conventional-human-peer-review disclosures are
explicit. The original exponent and machinery are attributed. The deposit
ZIP excludes upstream source copies and caches; the retained local upstream
copies have separate notices and licensing. No credential or secret was
found in the intended upload contents.

## Findings, repair record and remaining limits

There is no unresolved substantive finding in the latest exact package.
The older reproduction helper assumed tmp existed and the older ZIP did
not include main.tex. Root repaired those before candidate03, and the exact
extraction run independently verified the repair. The old complementation
audit's wording about a prospective formal rebuild was clarified by its
original auditor in a preserved addendum; this review independently finds
no handwritten mathematical obligation resting only on that prospective
build. No mathematical claim, manuscript text, PDF or publication metadata
was changed during those repairs.

This review does not reproduce kernel verification, prove globally earliest
priority, validate future remote deposit metadata, verify DOI resolution, or
check a future spreadsheet mutation. Those remain distinct evidence scopes.
This review's mathematical-checking and package-checking tasks are complete;
their completion does not mark the parent publication objective achieved.
I edited only this review and its private evidence artifacts, made no commits,
and contacted no external individual.

## Addendum: candidate04 bibliographic correction review

Timestamp: 2026-10-06T21:33:37.926976-07:00 (America/Los_Angeles).

A fresh reviewer found two bibliographic locator errors in candidate03 that
my first review did not catch. The original complementation result is
**Theorem 1.1**, rather than Theorem 1. Root corrected the inline citation
at main.tex:253 and the bibliography locator at main.tex:355. The original
candidate03 verdict and its evidence remain preserved above.

I independently verified that reversing exactly these two locator strings
reconstructs the candidate03 main.tex SHA-256
`effc61c3809b0290f4b9a063c7a7dbc389e512d38e81683d0bea0cee42f19aa5`.
Thus no mathematical text, transition, proof, quantitative bound, attribution
claim or convention was changed. The pinned original paper.pdf explicitly
labels the result Theorem 1.1 on page 1, and its build/paper.tex uses theorem
numbering by section. The corrected locator is therefore verified directly
against the primary source.

The current four publication files and manifest were all hash-checked
against reviews/candidate04_hashes.json:

| File | Bytes | SHA-256 |
|---|---:|---|
| main.tex | 20426 | b6aa5b342c1b4a919d1f938f26f0b5f5242d7bbaac9e74540899621ff6441910 |
| paper.pdf | 80290 | fc8fe182d3fc92cd61607e514cd811b268e0ab56cd84f170c6fb0f689980e215 |
| README.md | 5370 | fca0eb6955d6c5794eaafcc132617a42706178fb16319bc1c4a6d75c3a8b3dd2 |
| verification.zip | 74534 | 6169f978956c923664207e274f93ab2c13042965206f9bb17cd1f35869794ac1 |
| zenodo-deposit.json | 2427 | fa6d151d0ce646e898cfb68ac7abb92c857c344488a593e138003e5cc290c5c0 |

I independently rendered and visually inspected affected PDF pages 4 and 6,
then checked their extracted text. Both locators now read Theorem 1.1;
formulas, line breaks, margins and references are intact. The PDF still has
six pages and correct title/author metadata. README and deposit metadata
are byte-identical to candidate03.

I verified all 27 ZIP content hashes and CRC, compared the current member
manifest with the one in my original review, and confirmed that **only
main.tex changed inside verification.zip**. In a fresh extraction of the
exact candidate04 ZIP, I ran code/clean_reproduction.py successfully: all
four verification scripts passed and the corrected standalone source built
an actual PDF. The ZIP hash was unchanged before and after this check.
Evidence: whole_package_review01_artifacts/candidate04/checks.json and
whole_package_review01_candidate04_hashes.json.

**No unresolved substantive or bibliographic issue was found in candidate04
within this change review.** The earlier full mathematical and dependency
review continues to apply because the exact source comparison establishes
that its proof text and all supplementary code/audit content are unchanged.
The formal-verification and publication/tracker limitations from the original
review remain unchanged. This addendum is an automated review, not human
peer review. No candidate file or external publication state was changed
by this reviewer.
