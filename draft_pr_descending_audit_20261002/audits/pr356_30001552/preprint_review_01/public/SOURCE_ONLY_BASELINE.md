# Source-only baseline: first new preprint reviewer

Dated UTC: 2026-10-04T01:43:07+00:00

Status: source-first gate ready; candidate/package exposure forbidden until an explicit release from root. Overall review completion estimate: 15% (source gate complete; package review not started).

## Provenance and scope

The actual official source file is `/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr356_30001552/root_sources_private/owr2010-37.pdf`, 463460 bytes, SHA256 `e88f211c5be990a68a967f3a9549f5db042279e8473e2cb126ea1e3caaebf98c`. Official URL: https://ems.press/content/serial-article-files/46296. A byte-identical private copy is preserved in `source_private/owr2010-37.pdf`. This reviewer extracted and read the full contribution on PDF pages 25–28, printed pages 2219–2222, and visually inspected every one of those pages. The speaker/contribution author is Dirk Nowotka, with joint work credited to Bastian Bischoff. The contribution characterizes its material as work in progress.

The PDF does not encode the identifiers PR356 or problem30001552. Therefore the index-to-conjecture mapping remains unverified at this gate. It contains two distinct open conjectures; their scopes are pinned below so a later release cannot silently substitute one for the other.

## Definitions and deductions required by either target

A word is a finite element of the free monoid A*. A morphic involution respects concatenation in order; an antimorphic involution reverses that order; applying either involution twice returns the word. Such involutions preserve length and act on letters by an involutive permutation (a deduction from invertibility in the free monoid, not an extra source assumption). For a positive integer p, an alternating theta-period means that the word is a prefix of the infinite concatenation of u, theta(u), u, theta(u), ... with |u|=p. A general theta-period permits each successive p-block to be chosen independently between u and theta(u). The former implies the latter, while the reverse implication needs separate proof and must not be used as a definition.

For n=|w|>=p the root u is necessarily w's p-letter prefix. The final observed block may be partial; a check only on complete blocks is insufficient. Periods p>n are possible under the source definition by extending w to u. At either positive-length threshold below, p and q are automatically <=n, because gcd(p,q)<=min(p,q). This justifies prefix-root checks under those thresholds but not unrestricted oracle shortcuts. Letter fixed points, identity morphisms, and reversal with identity letter map are not excluded by the source's conjectures. An arbitrary alphabet can be reduced to the finite theta-closed support of each individual word.

## Target A: antimorphic alternating Fine–Wilf threshold

Printed page 2220 states Theorem 23 with a sufficient length n>=p+q for positive alternating theta-periods p and q and conclusion that d=gcd(p,q) is itself an alternating theta-period. The following unnumbered conjecture proposes the stronger sufficient length n>=p+q-d for exactly that same antimorphic setting and alternating-period conclusion. There is no source restriction p>q, p!=q, binary alphabet, fixed-point-free theta, or coprime periods for this conjecture. The p>q condition in the preceding general-antimorphic theorem belongs to a different statement.

Success criterion: a complete proof for every antimorphic involution and finite nonempty word with p,q>0 and n>=p+q-d, yielding membership of d in the alternating period set, or a fully checked counterexample to that exact assertion. A theorem restricted to general theta-periods, weak theta-periods, ordinary periods, common primitive roots, or morphic involutions would leave the original claim unresolved unless a valid implication back to the exact conclusion is supplied.

Boundary and falsification checks: p=q (the conclusion is given); p or q equal to 1; p dividing q; scaled noncoprime periods; quotient parities p/d and q/d; equality n=p+q-d; lengths immediately below it; longer words with incomplete final blocks; fixed letters; involutions with no fixed letters; alphabets with multiple two-cycles and mixtures of fixed and exchanged letters. A sharpness claim must produce failures at the claimed preceding length for its stated parameter range; degenerate pairs must be separated from a uniform worst-case claim. A signed-constraint construction must derive actual prefix compatibility for both original periods and explicitly disprove alternating d-periodicity, not merely produce an unlabelled disconnected graph. Every equivalence between graph connectivity and word realizability needs a proof addressing forced fixed points or incompatible sign cycles.

## Target B: morphic unbordered-factor Conjecture 27

Printed pages 2221–2222 define theta-bordering by a proper prefix u whose theta-image is a suffix. Under the usual nonempty-border convention, tau_theta(w) is the largest length of a theta-unbordered contiguous factor. Conjecture 27 is: for a morphic involution, n>=3 tau_theta(w) should imply tau_theta(w)=the shortest alternating theta-period of w. The source does not explicitly redefine tau_theta after introducing tau for ordinary unbordered factors; its use and the surrounding paragraph determine this theta-factor meaning. This is separate from Target A.

The preceding source family is w_i=(ab)^i abb (ab)^i aab (ab)^i a, i>=2, with theta exchanging a and b. It reports n=6i+7, tau_theta=2i+4, and shortest alternating theta-period 4i+5. Thus n/tau approaches 3 from below; this alone is not a proof of the upper implication. Any later treatment must independently validate the stated parameter formulas and avoid claiming the displayed family already proves the conjecture.

Boundary and falsification checks: the identity morphism, fixed letters, one-letter words, exchanged pairs and larger alphabets; all proper nonempty border lengths, including overlaps; all contiguous factors rather than only prefixes/suffixes; exact equality n=3 tau; and the displayed family. The source writes w in A* without giving an empty-word convention. If epsilon has tau=0 while its least positive alternating period is 1, the literal unrestricted implication fails on epsilon. A defensible statement must explicitly handle or exclude epsilon rather than hide that convention. Allowing an empty border would also trivialize the definition, so that convention must be stated.

## Attribution and presentation controls

Both original conjectures should credit Nowotka's contribution and its joint-work attribution to Bischoff. A numbered source theorem, preceding work in the bibliography, and an original conjecture must not be collapsed into one credit. The source's cited Kari/Mahalingam and Czeizler/Kari/Seki works should be checked when priority or definitions matter after release. No claim of present-day open status, global novelty, or external human review follows from this 2010 report. This gate makes no such claim.

## Exposure declaration

Read: parent task instructions; supplied source path/hash/URL; PDF skill and runtime documentation; filesystem listing restricted to locating the named original source; the byte-bound source PDF, its private four-page extraction, and the four rendered pages. The retained source-only derivations and checks above are this reviewer's own.

Not read: candidate snapshot; preprint note, manuscript, PDF or ZIP; parent's proof; prior reviewers' reports; priority audits; prior code or outputs; any package-specific mathematical claim. No internet priority search has occurred. No external-person communication, Git/index/branch operations, installs, or parent-file writes have occurred. All review artifacts are confined to this folder.
