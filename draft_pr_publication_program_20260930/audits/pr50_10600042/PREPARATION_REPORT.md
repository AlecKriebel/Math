# PR50 /10600042: bounded original mathematical preparation

The original candidate gives a sound explicit reformulation of classical and
virtual Markov equivalence using only even-strand states, conditional on the
credited foundational theorems. I found no missing edge type, support error,
closure substitution or circular applicability condition. Both original
verification outputs reproduced byte for byte. This is preparation for fresh
independent mathematical review, not an acceptance or publication certificate.
Historical priority and current open-problem status remain unresolved.

## Exact original source and accounting

The actual draft is PR50, “10600042: reviewed even-strand classical and virtual
Markov reformulation,” branch `dot/math-10600042`, head
`7260315f8b8b193020c09d4ef6df9d943a3a13ff`. The GitHub-reported base is
`c6975ca76f9f667f1250ba403d0e6da2aafe14d0`; its actual merge base is separately
`01358d66fc67d1c462bddf31c0d4ee5b120e6737`. The actual comparison is diverged,
five commits ahead and two behind. Neither identity is future merge authority.

`ORIGINAL_MANIFEST.json` binds all15 selected original files by full length,
SHA256, canonical Git blob SHA1 and literal Git mode, the target/root trees and
actual snapshot PID40885. These files were retrieved through read-only GitHub
Git-object APIs without fetching or changing local refs. Every original snapshot
file is full0444. Actual metadata,66360-byte diff,99419-byte comparison and
individual tree/blob command captures remain complete with full streams. The
changed scope is these15 files and one QUEUE row. The original patch sets
`claimed_solved`,1/5 and a qualified Findings cell. Its literal proof hash is
`749f55ab651476c5f3c7868fed2b9f06809a38518057e33414966cb6f4f253bc`.

The original ledger has one substantive turn in one family, “canonical positive
padding and explicit lifting of every Markov edge.” That historical entry remains
unchanged, including its then-pending independent review field. No new proof
search response, audit turn, native queue mutation or accounting event was
created by this preparation. The current native row is still queued0/5 as a
dated observation. The existing prior AI review is a historical artifact and
provides no fresh independent acceptance decision.

Actual selected-source child45403 read only one SQL record and reconciled both
of its complete typed problem/report objects with the original source record
and selected raw JSON entries. The immutable dataset revision and raw file
length/hash pins match the local manifest. No unrelated SQL rows were audited;
no raw-cache or foreign PDF bodies were copied. The current selected catalog,
assessment and exact-ID related-group lookup were recorded; no exact-ID group
was found. Imported placeholder arXiv identifiers remain untrusted triage text,
not proof citations or a current status audit.

Earlier own child44934 failed because I incorrectly assumed the reported GitHub
base equalled the merge base. Its actual prelaunch child/operator sources, full
1132-byte stderr, empty stdout and failure are preserved. The narrow source
reconciliation repair distinguishes those identities; it does not alter any
original artifact or mathematical statement.

## Source question and foundational inputs

The target source asks for a reformulation of Markov's theorem involving only
even-strand braids. The same item42 occurs on printed p34 of the
[2014 preprint](https://arxiv.org/pdf/1409.2823v1) and p37 of the
[published survey](https://www.impan.pl/shop/publication/transaction/download/product/86155).
The checked item states no minimality or uniformly bounded-support requirement.
The survey contains classical and virtual questions, so giving both readings
avoids dropping the virtual case. These are checked text locations; this
preparation does not claim new whole-PDF pixel inspection or verification of
the old stored PDF-byte identities. The browser reports66 pages for the
preprint; the original research log's “65-page” description is a retained
historical page-count error, with no mathematical consequence.

[Kamada, Proposition3.1 and Theorem3.2](https://arxiv.org/pdf/math/0008092v1)
provide ordinary oriented virtual braid representatives and the unrestricted
equivalence moves. The definitions on printed pp5–7 explicitly include
positive, negative and virtual right stabilizations, both exchange directions
and the left inclusion shifting every old generator index by one. The
candidate's formulas match these definitions. Kamada's Proposition3.3 also
prevents dropping virtual exchanges without justification.

[Kauffman–Lambropoulou, Section5, p30](https://arxiv.org/pdf/math/0507035v3)
independently spells out the same right/left exchange patterns, negative crossing
before the second block and positive crossing after it. Their Section4 threaded
formulation is a different presentation and is not silently substituted.

The publisher's classical article returned an internal error during text search.
The primary author preprint
[Gorsky–Kivinen–Simental, Theorems2.1–2.2](https://arxiv.org/pdf/2108.10356)
supplies the classical Alexander/Markov statements with ordinary closure,
conjugation and both stabilization signs. Those existing results remain inputs;
the candidate does not reprove them. External text access errors and failed
publisher screenshot access are recorded as limitations rather than visual
verification passes. No foreign source body is redistributed here.

## Independent reconstruction of the mathematical mechanism

Let the unrestricted word graph have vertices `(m,b)` with positive strand count
and edges given by its usual Markov moves and defining word relations. Let E
be the graph whose vertices have even tags and whose generating edges are the
candidate's explicit patterns. Define P to fix even vertices and send each odd
vertex to its positive right stabilization. There are three separate proof
obligations: P preserves closure; every unrestricted edge has its endpoints
joined by a specified E edge or word relation; and every specified E edge
preserves closure. Once checked, any unrestricted equivalence chain maps to an
E chain with the original even endpoints fixed exactly. This graph retraction
argument needs no group-homomorphism claim for P.

For conjugation at m, both words use indices at most m−1. Even m gives C;
odd m gives BC at N=m+1, where that bound is N−2 and the retained positive
crossing has index N−1. Thus there is no misplaced suffix or conjugator crossing
on the extra strand.

For stabilization of the smaller m-strand word by g at index m, even m produces
the N=m to N+2 pattern D, with new suffix g followed by the positive crossing
at index m+1. Odd m produces two words at N=m+1, the positive padded suffix
and the arbitrary allowed stabilization suffix, exactly T. Reversing these
edges covers destabilizations. Positivity of the chosen padding is fixed in
both formulas, while T and D retain every sign/type permitted by the input.

For exchange at total strand count m, unshifted blocks use indices at most m−2.
Even m gives R or L at N=m. Odd m gives BR or BL at N=m+1: the original bound
becomes N−3 and the retained suffix index is N−1. In the left case, shifting
the block raises its largest index to N−2; the explicit exchange crossings
stay at index1. All letters are valid even-endpoint letters, including the
smallest buffered case N=4. Both directions are retained.

Every defining braid relation at an odd count acts within the old prefix; the
new terminal crossing remains a context suffix at the even count. Relations at
an even count stay unchanged. Word-level formulation therefore avoids an
assumption that padding must be independent of a chosen group representative.
This exhausts the generator list. Identical successive padded vertices can be
deleted; there is no unbounded hidden-path condition used as an applicable move.

Soundness is independently checked by short unrestricted witnesses: C is
conjugation; BC and buffered exchanges remove and restore their retained
positive stabilization around the corresponding legitimate edge; T removes one
positive stabilization and adds the permitted other type; D is two permitted
stabilizations; direct exchanges are the established exchanges. Each support
cutoff makes those witnesses legitimate. Auxiliary odd vertices belong to a
proof of soundness, not the allowed-state graph E, whose patterns are defined
in advance. Consequently no circular equivalence oracle is used.

Alexander representation and one application of P give even representatives of
all nonempty oriented links. The one-strand empty word pads to sigma1 at two
strands, not the two-strand empty word. The latter has two closure components;
strand tags cannot be erased. A zero-strand empty-link state may remain isolated.
No theorem about framed, transverse, plat or uniformly bounded geometric moves
has been deduced. A certificate whose maximum tag is M has padded maximum at
most2ceil(M/2); this is certificate conversion, not a search complexity bound.

## Actual reproduction and adversarial boundary check

Actual author child42536 passed3219 assertions and emitted748 bytes exactly
equal to `even_move_verification.json`; prior independent child42537 passed6641
assertions and emitted1872 bytes exactly equal to `review/independent_results.json`.
Both exited0 with empty stderr, under private replay wrapper child42535. All15
original bodies were read and remained unchanged. Full actual PID/UTC/argv/cwd,
prelaunch sources and streams are retained. These finite checks corroborate the
symbolic proof; their count does not prove the target, unrestricted theorems or
historical priority. They cover sampled syntax and necessary component counts,
not a braid-word or link-equivalence oracle.

An additional small exact countercontrol under actual child46233 checks why T's
support restriction matters. Illegally allowing prefix sigma1² at N=2 would
relate sigma1³ to sigma1² sigma1⁻¹. Both closures have one permutation component,
but Fox3 closure coloring counts are9 and3, respectively. The allowed T has
maximum prefix index0 here and rejects the prefix before applicability. Its
empty-prefix positive/negative boundary yields3 colorings on either side.

The coloring obstruction is algebraic: with x▷y=2y−x modulo3, idempotence,
involutivity and `(x▷y)▷z=(x▷z)▷(y▷z)` give bijections of colorings under the
three Reidemeister moves. Both sides of the last identity are x−2y+2z. The
crossing propagation map `(x,y)↦(2x−y,x)` is invertible; closing means taking
its fixed points. Thus the differing counts genuinely rule out the enlarged
rule, while not challenging the actual restricted rule. This also falsifies
the idea that the earlier component-count diagnostics alone establish soundness.

## Strongest verified claim, exact gap and next independent families

Strongest verified claim: the specified four classical/eight virtual schemes
give a full ordinary-oriented even-state reformulation, conditional only on the
explicit credited unrestricted Alexander/Markov theorems. No mathematical repair
is currently identified. A materially independent adversary should try to
falsify virtual exchange orientation/index conventions, group-word passage,
minimal strand boundaries and the source interpretation before promotion.

The original draft is `claimed_solved`; its status also says
`new_discovery_claim:false` and `novelty:unestablished`. This combination requires
an explicit publishing disposition. Being an elementary consequence of known
theorems is not evidence that the exact source question had a prior published
resolution. No verified prior exact four/eight-pattern answer was identified in
the bounded searches. Conversely, a source problem listing and unproductive
search do not establish current openness or priority. Classification as
`already_solved` therefore needs a concrete prior resolution, not the existing
Markov inputs alone.

Priority preparation searched the exact problem phrase, even-strand Markov and
ordinary/virtual parity reformulations, then read the relevant primary inputs.
Plat presentations, transverse statements, free-link and bonded-braid theorems
concern different closure/category scopes; none encountered settles this exact
ordinary classical-plus-virtual formulation. This is bounded qualification,
not the extensive priority audit required before publishing a claimed solution.
A distinct priority family should seek earlier parity presentations and updated
problem-list status while preserving the narrow ordinary-closure target.

Remaining gap: fresh independent full-scope adversarial review and extensive
priority/current-status decision. A preprint, its repeated independent reviews,
Zenodo upload, tracker row and acceptance remain future ordered work. No paper,
DOI, tracker action, ROOT certificate, native state change, Git stage/ref/commit
or remote mutation occurred here. Earlier PRs46→47→48→49 remain prerequisites
for any PR50 integration. Bounded original preparation95%; overall mathematical
verification provisional pending independent challenge; novelty/discovery credit
unestablished; acceptance0%.
