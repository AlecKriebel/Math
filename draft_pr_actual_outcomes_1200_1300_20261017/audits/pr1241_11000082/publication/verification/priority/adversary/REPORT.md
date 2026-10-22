# Independent general-theory priority adversary: PR 1241 / problem 11000082

## Verdict and its limits

**Substantive implication from older general theory found and written out now. No earlier explicit printed resolution of this exact Johnson-filtration question was identified among the older bodies inspected. Neither statement certifies novelty or worldwide openness.**

The clean additional old theorem is Kapovich's existence of a rank-two subgroup malnormal in a torsion-free hyperbolic ambient group. Applied inside the index-six free subgroup of a modular overgroup of the full affine disk stabilizer, it supplies a constant ambient-conjugacy fusion bound of six. Horowitz's trace families then imply the exact fixed-genus, fixed-depth theorem. DERIVATION.md gives every interface and the quantifier order. This is **NOW-ASSEMBLED (17 October 2026)**, not an earlier printed Johnson theorem.

There is also a positive exact-target public source dated **11 October 2026**: Alper Ferudun's 13-page unrefereed EulerSolve note, Theorem 1.1 on PDF 2. Its current primary PDF asserts a stronger version for every k>=1, up to inversion and extended mapping-class conjugacy. This is an actual theorem body, not a keyword-only hit. Its priority relationship and independence from the submitted candidate remain unresolved here. Same problem identifier, same date as candidate source-check metadata, and closely related proof mechanisms prohibit silently counting it as an independent historical resolution. A currently accessible PDF's internal date is not independently verified evidence of when its present bytes first became public.

The submitted proof already credits the underlying sources and expressly makes no firstness claim. This audit does not identify a false priority assertion in that text and does not reverse the mathematical PASS gate. It provides a stronger literature/dependence account and an exact contemporary source requiring provenance reconciliation.

## Scope and independence

The target is: for every fixed closed genus g>=2 and every fixed k>=3, arbitrarily large sets of pseudo-Anosov elements in that fixed I_g(k) have identical logarithmic dilatation and distinct orientation-preserving **ambient Mod_g** conjugacy classes. Proper powers are allowed. The value may change with family size. Simple Teichmüller loops and one value of infinite multiplicity are separate statements.

Permitted candidate inputs read: repository AGENTS.md, submitted PROOF.md and SOURCES.json, MATH_GATE.json and ROOT_ANALYTIC_REVIEW.md. The remaining submitted files were authenticated by hashes for provenance but not substantively read. No other ongoing priority-family, source-question-family, analytic-adversary artifact, or root source-search ledger was read. Listing filenames during the initial scoped inventory was not reading those contents.

No source-author code, submitted diagnostic, PR/Git-index/commit/push/release operation, subagent creation, external individual's communication, or outreach was performed. Local code was used only for downloading, extracting/rendering PDFs and recording evidence metadata. Raw source bodies, excerpts, rendered pages and search outputs are in ignored _local/. This authored report and its ledgers are the durable checkable outputs.

## Why the old general theorem matters

The submitted construction's hard priority interface is not equality of free-word traces. It is retaining arbitrarily many distinct ambient mapping-class classes after placing all words inside one fixed Johnson depth. The following old ingredients suffice:

| Interface | Actual inspected old source | Scope check |
|---|---|---|
| Every-genus separating filling seed | Aougab-Taylor Lemma 2.2, PDF 3-4; alternatively FLM section 2.3, PDF 12-13, using separating multicurves | Genus fixed first; g=2 included |
| Faithful two-parabolic affine free group and dilatation | Leininger sections 5.1/6.1/6.2, PDF 19-21,23,26 | Shear >2; cusp exceptions excluded inside commutator subgroup |
| Fixed-depth containment | FLM Proposition 4.8 proof, PDF 20; Aougab-Taylor Theorem 5.1 proof, PDF 10 | gamma_k(F) <= I_g(k), with explicit indexing |
| Entire affine derivative overgroup | Hubert-Lelièvre Lemmas 2.1/2.3, PDF 7-8, after the elementary orientation-double-cover lift in DERIVATION.md | Applies to every affine conjugator, not just the two twist generators |
| Old ambient fusion mechanism | Kapovich original preprint Theorem 7.7, PDF 29-30 | Ambient group is free, torsion-free hyperbolic; the deep subgroup need not be finitely generated |
| Universal equal traces | Horowitz Example 8.2, PDF 14-15, universal convention PDF 2 | Substitute free generators already inside fixed depth |
| Mapping-class conjugator preserves the disk | Leininger Theorems 3.1/3.2, PDF 14-15 | Uniqueness reduces all ambient conjugators to the full affine stabilizer |

Using the conservative single-curve seed, these are old theorems available before this audit. FLM's multitwist seed allows the theorem ingredients to be taken from publications dated at latest 2008. This availability date is **not a historical solution date**. The cover-lifting, group-theoretic matching and final combination are supplied in the present deduction.

The older Anderson survey already explains the ambient-fusion obstruction and describes both malnormality and bounded-fusion approaches. Its Theorem 5.3 cites precisely the Kapovich mechanism. Thus it would be misleading to describe the *idea of controlling Horowitz families by a malnormal ambient free subgroup* as newly discovered here. That general mechanism was explicitly discussed in print well before 2026.

## The inspected candidate leads, with exact non-implications

### Horowitz, Randol, Masters, Anderson

Horowitz's 1972 Example 8.2 is the actual universal trace construction. It makes no Johnson-filtration or mapping-class statement. Naively applying its words to the full two-twist group does not place them in the commutator subgroup: in its printed recurrence W_m has abelianization b^(6m-1). The repair is to substitute a basis of a fixed deep free subgroup first.

The direct Randol 1980 AMS PDF returned HTTP 403. I do **not** claim to have inspected Randol's authentic primary body. Masters' authentic primary paper reproduces a proof of the finite-volume surface theorem as Theorem 3.1, PDF 5-6. That theorem counts classes in the hyperbolic surface group; on an infinite normal cover, deck translates can be intrinsically distinct while all becoming one ambient class. It therefore cannot simply be transplanted as an ambient Johnson answer.

Masters' primary Theorem 1.1, PDF 2, says a finitely generated group with an infinite irreducible SL_2(C) representation has unbounded stable trace multiplicities. Theorem 1.2 transfers this to Kleinian groups, with parabolic exclusions handled in Lemma 2.1. This is genuine older general theory, but applying it only to a deep subgroup gives intrinsic classes; the ambient-fusion bridge is still required. Applying it to the full stabilizer does not ensure the words lie in the chosen depth.

Anderson's primary author-hosted survey, section 5, printed 487-489 / PDF 18-20, openly identifies this issue and proposes malnormal free subgroups. His Lemma 5.4 is phrased for maximal cyclic subgroups and has stronger uniformity language than its displayed compact-core argument transparently supplies for varying free subgroups; the printed proof also refers to an infinite-volume quotient as compact where its convex core is evidently intended. I do not rely on that lemma's strongest formulation. Original Kapovich plus the elementary six-coset argument avoids these issues and handles proper powers directly. Pignataro-Sandler's underlying original chapter was not retrieved; Anderson's bibliography also prints 1974 for a volume associated with 1994. That lead remains unverified at the original-body level.

### Leininger and the square-tiled/pillowcase route

Leininger 2004 supplies exactly the geometric representation and disk-uniqueness imports. It does not itself assert the target unbounded multiplicity statement at fixed Johnson depth in the inspected relevant bodies.

Hubert-Lelièvre's general period-lattice lemmas and Appendix C give an older published form of the affine-integrality/arithmetic mechanism for translation surfaces. Original q need not be a translation surface; applying a homological argument directly on S would be invalid for Torelli pseudo-Anosovs. The canonical orientation double cover supplies the exact missing interface. We need containment of the full derivative group in an integral-lattice automorphism group, not finite index of the two-twist subgroup in that group. No finite-index claim about a Johnson term is made.

The original Gutkin-Judge 2000 full body was not retrieved. Its arithmeticity theorem is stated and independently proved in the inspected Hubert-Lelièvre paper; this report relies on that latter actual primary proof for the required period-lattice assertion. Schmithüsen's origami algorithms and later general-origami papers were source leads, not executed or imported.

### FLM, Aougab-Taylor, Malestein-Putman

FLM 2008 proves least-dilatation bounds and the lower-central construction. Its Theorem 1.2 is not a multiplicity theorem. Its explicit affine seed and depth containment are nevertheless enough inputs for the present combination. The generic sparse cyclic matrix display must not be read literally in the one- and two-component cases without adding coincident incidences; the actual shear-8 construction and the single-curve alternative avoid relying on that notational shortcut.

Aougab-Taylor Theorem 1.1 (PDF 2; proof section 4, PDF 8-9) gives infinitely many primitive ambient classes associated to a disk, and Theorem 1.2/5.1 gives ratio optimizers arbitrarily deep in Johnson filtration. Neither says those infinitely many elements share a dilatation at one fixed depth. The section 4 argument proves finiteness of fusion for a chosen reference class, with quantities depending on that class; the needed uniform control across the later trace-family sizes is supplied explicitly by our Kapovich reduction.

Malestein-Putman, actual Theorems A/B on PDF 2-3, gives quantitative lower bounds for least dilatation and for intersection of curves with identical nilpotent-quotient conjugacy classes. The introduction's word-length improvement improves least-dilatation upper bounds. It supplies no fixed-depth equal-dilatation multiplicity conclusion.

### Jeffreys, including both versions

Theorem 1.4 in Jeffreys v1 (20 October 2022) and v2 (25 February 2026), PDF 4 in each, asserts infinitely many ratio-optimizing pseudo-Anosovs lying arbitrarily deep in the Johnson filtration and stabilizing a disk associated to the specified hyperelliptic component. Section 5.3/5.4, v2 PDF 25-26, reduces this to separating filling pairs and Aougab-Taylor. It does not equate their dilatations, prove a fixed-depth multiplicity conclusion, or supply a different ambient-fusion theorem.

Both actual bodies were downloaded and inspected at their relevant statements; v1 has 26 pages and v2 has 29. The arXiv record says v2 added section 6 and clarified geometric constructions. Its journal reference is Geom. Dedicata 218,93 (2024), although v2 was posted in 2026. Those are separate dates. The search engine's relative “years ago” labels and PDF regeneration dates were not treated as publication dates.

### Dahmani-Mj and arithmetic class numbers

Their primary v4 Definition 1.1/Theorem 1.2 and introduction, PDF 2-4, bound the number of Aut(pi_1(S))-conjugacy classes in one **commensurated-conjugacy** class by a constant depending only on genus. Same stretch factor is a necessary invariant of that equivalence relation, not a sufficient characterization of it. Therefore this is neither a bound on the full equal-dilatation multiplicity nor a counterexample to unbounded multiplicity. The genus-three example in Theorem 1.3 distinguishes homological actions; it does not supply arbitrary Johnson depth or arbitrarily many classes.

Their appendix's matrix ideal-class theory and section 6.5, PDF 19, explicitly leave the higher-genus realization/fiber questions unresolved. Importing unbounded GL_2(Z) class numbers would require proving that relevant classes lift to the same fixed surface and fixed Johnson depth with the required dilatation and nonconjugacy; that transfers the central difficulty into an unsupported realization claim. This route is **blocked as an implication**, pending a materially new realization theorem.

### Normal all-pseudo-Anosov subgroups

Whittlesey's primary Theorems 1.1/1.2, PDF 2, concern Brunnian punctured-sphere groups and a nontrivial normal all-pseudo-Anosov subgroup in closed genus two. They do not assert all genera, arbitrary Johnson depth, or an SL_2 derivative representation tying trace to dilatation. General pure/normal subgroup existence, by itself, cannot convert trace-equivalent abstract words into equal entropies. The mechanism is blocked unless that missing representation/geometric compatibility is established. Later normal-generation/rotating-family leads were not promoted from search snippets to theorem dependencies.

Leininger's 2003 Theorem 1.4 and Bankovic's 2013 Theorem 5.1, actually inspected in their introductions, concern equal lengths of surface-group curve classes across hyperbolic or flat metrics. Their objects are curves on S, not pseudo-Anosov maps. Lawton–Louder–McReynolds's published 2017 Lemma 4.1 explicitly uses malnormality to transfer trace-equivalent pairs into another group. Its citation supports the age of that general mechanism; this deduction uses Kapovich's original torsion-free hypotheses and does not assume Mod_g is word-hyperbolic.

## Positive contemporary exact source

[Primary EulerSolve PDF](https://eulersolve.org/papers/amr-109-0082/paper.pdf?v=f04bac1ae0f6) currently has SHA-256 f04bac1ae0f63f083777008c50442fa97fc9edc3659b35b789343e017a73d0ed, 167507 bytes, 13 pages. PDF 2 Theorem 1.1 explicitly quantifies every g>=2,k>=1,N>=1, equal dilatation, and pairwise nonconjugacy even up to inversion in Mod_g^±. The same page explicitly supplies the full affine-stabilizer/modular-overgroup/finitely-generated-subgroup fusion mechanism.

Only PDF 1-3 theorem/introduction material was substantively inspected here; the entire paper's proof is **not** independently certified by this audit. Its displayed timestamp and online-release label say 11 October 2026. This is affirmative exact-target *printed-claim* evidence, with current bytes authenticated; mathematical validation of its complete proof and chronology/provenance comparison remain separate. This family does not decide whether it is independent prior work, a parallel presentation, or related provenance. No inference about copying is made.

## Search and evidence limits

The literal query ledger records 15 batches (at most four queries each), covering general trace equivalence, length-spectrum multiplicity in normal/deep subgroups, affine arithmeticity, Veech/pillowcase groups, class numbers, Johnson constructions, normal pure subgroups, and exact target phrases. Every search output and metadata result is preserved locally. Search hits were used as leads; conclusions above depend on actual identified theorem bodies.

SOURCES.json records individual PDF hashes, sizes, page counts, metadata dates, inspection pages and whether inspected pages were complete or partial. Fetching whole bytes is not reading every page. No source in this audit was read in full. PDF render/inspection was restricted to the eight listed critical pages. Some source-level backgrounds, original Bers, original Gutkin-Judge, original Randol, original Pignataro-Sandler and possible non-indexed/inaccessible work remain outside the verified corpus.

This is a substantial bounded adversarial search and an explicit old-theorem derivation. It authorizes **no worldwide openness/firstness clearance** and no unsupported historical “already solved” status. The durable conclusion is the checked dependence chain plus the separately flagged exact 2026 printed claim. Any later comparison with other families must occur after the authored freeze.

