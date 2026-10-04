# Independent preprint reviewer 02: PR356 / problem30001552

Review checkpoint: 4 October2026 UTC / 3 October2026 PDT. Mathematical and
publication-file review complete; one administrative closure awaits root approval.
Best-guess review completion:96%. No mandatory correction was found.

## Independent scientific verdict

The released preprint correctly proves the exact unnumbered alternating
antimorphic conjecture after Theorem23 on printed2220 of Nowotka's contribution,
joint with Bischoff, to OWR37/2010. For an arbitrary alphabet, an antimorphic
involution theta, positive alternating periods p,q of a finite word w, and
d=gcd(p,q), length at least p+q-d forces alternating period d. This does not
claim the different morphic Conjecture27. The convention that periods are positive
is explicit in the preprint and implicit in the original infinite nonempty-seed
definition. Fixed letters, a one-letter alphabet, nonminimal periods, equality,
divisibility, and a short final block are all covered. Empty w cannot meet the
positive threshold; an empty alphabet provides no nonempty witness.

I first read the complete official original contribution, printed2219–2222 /
PDF25–28, and visually inspected every page. The source-only baseline distinguishes
both source conjectures, all relevant definitions, and implicit conventions.
The original source alone does not map the external catalogue identifier to one
of those conjectures. Root subsequently supplied that mapping after fully reading
and validating my source gate. I then read every line of the complete released
TeX/PDF and visually inspected all three PDF pages. My independent analytic
verdict and falsifier design were frozen before ZIP-member, metadata, prior-audit,
control-code, or prior-reviewer exposure. These gate-time records remain immutable.

The decisive universal reasoning is independently checkable. An involutive
free-monoid antimorphism maps letters to letters: it fixes epsilon, cannot erase
a nonempty word, and a split image of a letter would split that letter on applying
theta again. Write its involutive letter permutation as sigma. The two-sided
repetition of u theta(u), |u|=p, satisfies s[-1-i]=sigma(s[i]); the reflected
residue 2p-1-r exchanges the two block halves. Therefore the restriction to
[-L,L-1] is exactly W=theta(w)w, with ordinary period2p. The q representation
gives ordinary period2q on that same finite W. The two infinite tails need not
be equal. Fine–Wilf gives ordinary period2d because |W|=2L meets exactly
2p+2q-2d. The hypothesis also gives L>=max(p,q)>=d. For each right-side index,
its residue modulo2d has a representative in [-d,d-1]; every step between the
positions stays in W. The center is theta(v)v, v=w[0:d], so negative residues
recover the appropriate reversed/sigma-transformed letters. This establishes
the required alternating phase, rather than merely an ordinary period2d on w.

The reversal witness abb at p2,q3 and length3 correctly obstructs a uniform
one-letter reduction. It establishes no optimum for every fixed numerical pair,
alphabet, or involution. The note makes this qualification consistently.

## Independent controls and actual native executions

I manually read all twelve package Python programs before executing any of them.
Their standard-library dependencies, preserved absolute-path historical checker,
portable dynamic execution boundary, assertions, input/output contracts and file
effects were inspected. Default public verification executes four read-only
audit verifiers. Explicit --full also executes six mathematical finite-control
programs. It never runs the old literal absolute-path reviewer program.

Before first execution I independently assembled every byte of both expected
wrapper streams from the read contract and saved child streams; I did not run or
import the wrapper to derive its expectations. I also assembled the entire own
control expectation, deriving its domain counts by finite sums and specifying
its hand-checked witnesses. The capture runner pinned candidate4, all69 ZIP
members, all six expected stdout/stderr files, three reviewer programs, the
interpreter binary/version, and exact argv before executing. All82 file pins
remain unchanged, and every before/after snapshot agrees. Assertions were enabled;
bytecode writes were disabled. No installation or network action occurred.

| Fresh run | Exit / stderr | Entire stdout bytes / SHA256 |
| --- | --- | --- |
| Default public wrapper | 0 / empty | 1586 / cef38ef1a41ebcd26f090f73ef2991e2dbf8d6022c68c0f202d0f959e675fd9e |
| Public wrapper --full | 0 / empty | 2960 / 9555386bf072f272e069bfec19c3cc665c9ace49486d6772069fc3a1171f73d4 |
| Reviewer02 own literal controls | 0 / empty | 1174 / 7c070f720d893b260e2a753cf6e7ba8685d3efd7cc0eeeb575f8207f942aac29 |

All three actual whole streams equal their pre-execution expectations, including
formatting and newline. The wrapper --full stream binds the genuine reproduced
child outputs for526887 author assertions,68408 portable assertions, and all four
other controls. Complete own native streams and execution metadata are at
`native_runs/{default,full,own}.{stdout,stderr,before.json,after.json}`. The genuine
capture-runner stream is `native_capture_runner.stdout`; its stderr is empty.
`native_runs/preexecution.json` records the actual binary, exact absolute argv,
timestamps and all input pins. These are this reviewer's executions, not adopted
historical/root/other-reviewer captures. No native mathematical run failed.

My controls were independently authored, without importing prior implementations.
They perform literal finite template comparisons and verify central coordinates
for qualifying p/q pairs. They record8619 finite words,76352 literal period
queries, and995 structured larger-template truncations. The five models are a
unary fixed letter, two fixed letters, a swapped pair, three fixed letters, and a
swapped pair with a fixed third letter. Larger seeds are explicitly structured,
not random. Equality, divisibility and partial-block cases are asserted, but
separate category counters proposed in my analytic design were not implemented
or reported as measurements. Finite checks do not replace the universal proof.

Five realistic mutations have concrete retained witnesses:

* Replacing theta(w)w by ww fails ordinary period4 for reversal, w=011,p2.
* Moving the reflection center from -1-i to -i fails at i1 in block0110.
* Applying sigma in forward order instead of reversing the second base block
  predicts0101 instead of the valid reversal block0110.
* Lowering the threshold by one fails at w=001,p2,q3 for reverse-complement.
* Replacing both input alternating-period premises by general arbitrary-block
  premises while **retaining the alternating gcd conclusion** fails at w=0000,
  p2,q3 for reverse-complement. This is a premise-only mutation. That word also
  has general theta-period1, so this is not a counterexample to general-gcd closure.

## Source, citation and bounded priority evidence

The sole original source in the source-first phase has463460 bytes and SHA256
e88f211c5be990a68a967f3a9549f5db042279e8473e2cb126ea1e3caaebf98c.
Only after analytic freeze did I inspect five previously cached primary PDFs.
`primary_source_pins.json` gives their exact hashes, external paths, actual read
levels/pages, and acquisition limitation. I made no fresh source download and do
not newly authenticate their old acquisition. Private extracts are direct local
read artifacts; they are omitted from this curated public review.

| Primary work actually inspected | Independent comparison |
| --- | --- |
| Fine–Wilf1965, PDF1–2, Theorem1 and both discrete-case proof arguments; PDF1 visually | The original title is plural, as the preprint cites it. Its agreement theorem for periodic sequences gives the standard finite-word statement by extending each finite period template; equality on h+k-gcd positions forces a common extension. This is credited prior mathematics. |
| Bischoff thesis, PDF25–28, Lemma3.9 and Satz3.11 statements/full proofs | Reflection and doubled ordinary periods are originating work; Satz3.11 gives n>=p+q, and its following discussion still leaves tightness unresolved. The candidate credits this related mechanism and does not claim reflection itself new. |
| CKS2010 journal-layout PDF6–8,11,13 | Theorems25/26 impose a theta-palindromic base word and conclude common theta-primitive roots. Their proofs and Theorem28's full short doubling proof were read. Corollary32's exact statement has2p+q-d for general powers. These differ in assumptions/conclusion from the candidate. I did not verify every proof in the whole paper. |
| Kari–Seki dated author PDF3,9,18,19 visually | Page19 Theorem8 explicitly has p>q>=2d and the improved general bound b'=2p+q-d-floor(d/2); its constructive proof is referenced there. Page9's q=2d boundary classification and the final proof segment were inspected. The OCR rendered >= misleadingly; the original pixels resolve it. I do not certify this author version identical to unavailable publisher full text or claim a full independent reproof of its long theorem. |
| Simpson2025 published PDF9–11, Theorems3.3/3.4 statements/full proofs | The bound is2h1+2h2-D, D=gcd(2(r2-r1),2h1,2h2), with ordinary-period conclusion D. Common phase gives h1=p,h2=q,D=2d, hence a threshold twice the candidate's on w. The candidate's extra common reflected extension is the essential deduction. |

The supplement contains53 dated query records and21 retrieval records, which I
parsed and inspected; I did not replay the searches or newly witness those source
acquisitions. Its bounded report identifies unavailable Kari–Seki publisher full
text, unrecovered earlier conference material, Simpson-v1 and other access gaps.
The preprint accurately says no earlier exact theorem was found in that inspected
scope, and explicitly disclaims universal novelty/first discovery. My primary
comparisons corroborate the named close comparisons. This review does not certify
global priority, absence of unpublished knowledge, or current exhaustive literature
status. AI use and unrefereed status are clearly disclosed; no external human peer
review is claimed or supplied. No individual was contacted.

## File, metadata and historical fidelity

All69 ZIP members were inspected as complete UTF8/structured bytes, all twelve
executable sources manually read, and all narrative reports read. The top manifest
checks68 payloads plus itself with no additional member. ZIP paths are safe;
all member bytes match fresh extraction. Member inspection and exact inventory
are retained in `member_inspection.json` and `package_members_inventory.json`.

The packaged TeX and deposit JSON are byte-identical to the corresponding released
files. All16 historical submitted files also match the retained original snapshot
disk bodies, and all7 author,15 publication and3 review manifest hashes recompute.
`original_candidate_fidelity.json` records those readbacks. This is disk/hash
verification; I did not independently inspect local Git history or API acquisition.
The four released pins were:

* TeX10658: ccf85ea52eb1d2003b69344e23e5c4641f851b22155bc95cbe01775ca41b2cab.
* PDF68077: 3ee2635930d4d107ff80cde1dfb7f8c57752fa833d0d212ba15c4ef7d4cdd81d.
* ZIP116605: 2e9137b22696a454bea1b48df1ebc732eb1c20b6950da55a983b3b593c7ab1c2.
* Deposit JSON2168: fa6d6889ec68a782650231ed86308b06957ac93993c437064af8612274eb73e1.

TeX and visible PDF content agree; every PDF page is readable, the index formulas
and page transitions are complete, references/hyperlinks display, and author Alec
Kriebel/ORCID0009-0001-9320-500X/date3 October2026 agree with deposit metadata.
The metadata correctly identifies a preprint/publication, version1.0 and CC-BY4.0,
with PDF+ZIP as the listed publication files. The description matches the exact
theorem, uniform sharpness, bounded priority, AI use and unrefereed status. Source
PDFs are excluded from the supplement and not relicensed by its own-materials
license. Current URL availability and the publisher's publication-date metadata
were not newly tested by this offline review.

The historical README/review's68413 assertions include five private source hashes.
This exact historical optional mode remains unreproduced; newly rendered or
re-extracted source bytes cannot establish those old bindings. The present
README/note/root report clearly distinguish it from the current68408 public run.
The literal absolute-path checker is retained as history and not called by the
public wrapper. Historical original AMS-retrieval failure is likewise preserved,
while the later bounded audit legitimately identifies a cached original AMS PDF.
Parent's export-stability race involved an earlier55628-byte PDF; its disclosed
repair is preserved in `provenance/PREPRINT_EXPORT_SEQUENCE_REPAIR.json`. It is
historical parent evidence, not my native execution. My released68077-byte PDF
and candidate4 remained stable throughout both fresh runs.

## Read-only closure and exact limitations

`public/verify_review.py` reads inventories, gate freezes, candidate4/ZIP members,
every retained pre/after stream, executed program/expected-stream pins, the full
capture-runner stream, and public-copy identities. It never invokes mathematical
programs, writes, installs or networks. Full mode checks private evidence; public
mode checks exactly the curated public files and declared whole-output receipts.
The explicit `--include-external-sources` option additionally hashes the five
cached primary PDFs, original OWR,16 original candidate files, parent candidate4,
and interpreter binary. Without the option no current external-body binding is
asserted. Public mode does not silently require private records.

Unsealed root-review commands are Python3.11 with -B, this verifier, `--root` this
review directory, `--proposal` its closure_plan.json, and `--mode full` or
`--mode public`; optionally add `--include-external-sources` in full mode. After
approved closure, omit `--proposal`. The exact one-time plan, including six tiny
terminal verifier captures and final log-only append, is supplied separately.
All preceding file paths/bodies/modes must remain unchanged except that declared
append. Existing writable modes are retained rather than retroactively altered;
the sealing commitment forbids further namespace writes. No final manifest or
seal exists at this checkpoint, and closure requires root's explicit approval.

One initial source-image lookup failed because it used025 instead of Poppler's25;
all four actual source page images were then inspected. Two broad combined tool
reads were truncated; the missing executable/report segments were re-read in
bounded calls. Kari–Seki rendering emitted nonfatal Type3-glyph warnings; its
pages were visually legible. No uncertain native run was overwritten or replaced.
No candidate alteration, dependency installation, Git mutation, publication,
upload, release, external contact, or outside-human review occurred.
