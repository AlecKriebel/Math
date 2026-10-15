# Independent maintained-source priority and exact-target audit

Audit completed 2026-10-12 UTC. Family: the maintained editors' primary-source chain and its cited earlier resolution. Scope: only PR436 / upstream 2569 / Kourovka 21.60 at frozen head `c7805ab0804f50c6f4b0d1dda99e433dbb702ae2`. The mathematical gate was accepted before this audit; it was not reopened for proof search. Author budget remains 5/5, with zero new proof-search responses.

**Verdict: the current exact target is already resolved negatively in the maintained primary source, and the cited order-twelve example is a genuine complete resolution. The saved order-120 counterexample passes mathematics but does not support a new resolution claim.** The exact first public upload time of the earlier proof is not established here. Its explicit author records precede the saved October 3 research record. Neither a different group nor the absence of an earlier search hit supplies a novelty certificate for a paper.

## Independence and method

`INITIAL_SEAL.json` was saved before reading any other current priority reports. Its SHA-256 is `b9fca631b87218934cb73f9705b4216827f5e87b75fc73a9132cc8800345c24b`. The parent supplied the accepted mathematics and URLs as unverified starting information. I read no other agent's current priority conclusions. I downloaded the cited source independently, extracted only relevant sections for mathematical reading, inspected the relevant rendered PDF pages, followed its primary author-repository link, and wrote a separate exact checker of the already existing example. Foreign PDFs, full text, rendered pages, HTML and raw API replies remain in `private_sources/current_source_priority`; they are not public deliverables.

## Exact claim and comparison

For a finite group `G` and prime `p`, set `R=Z_(p)` and `k=F_p`. Let `d` be the ordinary decomposition map from `G_0(QG)` to `G_0(kG)`, and let `M` be the nonnegative integer span of `d([W])` over simple rational `QG`-modules `W`. The target asks whether

`RG is semiperfect  <=>  [P] belongs to M for every indecomposable projective kG-module P`.

This is the full universal equivalence, with the prime field and rational localization specified. Its negative resolution needs one pair `(G,p)` satisfying the positive condition for every PIM while `RG` fails semiperfectness. Grothendieck equality is composition-factor equality; it does not assert an isomorphism to a rational lattice's reduction or projective lifting. Faithfulness of rational witnesses is not required. The problem imposes no normal Sylow subgroup condition.

| Comparison | Cited earlier resolution | Accepted saved result |
|---|---|---|
| Pair | `C3 semidirect C4`, inversion action, order 12; `p=2` | `SL(2,5)`, order 120; `p=2` |
| Central quotient | Central involution, quotient `S3` | Central involution, quotient `A5` |
| Exact modular field | `F2`; simple dimensions 1 and 2 | `F2`; simple dimensions 1, 4, 4, including the nonabsolute type with endomorphism field `F4` |
| Positive evidence | Every simple has a simple rational lift; hence every finite-dimensional module class satisfies the monoid condition | All three PIM classes have explicit rational witnesses, using the doubled quotient PIM classes |
| Actual PIM | Two PIMs of dimension 4; an explicit primitive `f` identifies a nonlifting one | The dimension-8 PIM has forced ordinary character `chi_+ + chi_-` |
| Obstruction | Quotient order in a rational division quaternion algebra, whose residue algebra is `M2(F2)` | A quaternionic constituent occurs with odd multiplicity in a hypothetical rational lift |
| Target strength | Full negative resolution; the positive condition is verified for all modular module classes | Full negative resolution for a different group, already accepted by the mathematical gate |

The arguments share a central involution, modular information passing through the quotient, and a rational quaternion obstruction invisible to positive composition classes. The earlier proof does not require a Schur-index table. The saved construction and character computation are additional checkable exposition and a different concrete example, but no claim of novelty for those additions is established by this audit.

## Why the earlier example is a complete resolution

The cited mathematical edition, §3.40, printed/PDF pages 55-56, supplies the explicit matrices, norm and radical argument. Its directly linked author proof and review provide the modular idempotents. The following is my independent verification of those objects, rather than reliance on a candidate label or a table.

In characteristic two, a central involution acts as identity on every simple module: its difference from identity squares to zero and has a nonzero invariant kernel. The quotient is `S3`. The central order-three averaging idempotent splits `F2 S3` into a dimension-2 local algebra and a dimension-4 algebra. For

`A=((0,1),(1,1)), B=((1,1),(0,1))`, the checker verifies the relations and that `I,A,B,AB` span all `M2(F2)`. Thus the exact prime-field simple list consists of the trivial module `k` and the natural 2-dimensional `V`. The integer matrices

`A_Q=((0,-1),(1,-1)), B_Q=((1,-1),(0,-1))`

give a stable rational lattice reducing to `V`. Rational simplicity follows because the order-three matrix has polynomial `t^2+t+1`, irreducible over `Q` (discriminant -3). Both simple types therefore have allowed rational witnesses. A composition series supplies the nonnegative witness for every finite module, including every PIM. This step uses no lifting of extensions.

For the negative condition, take `E=Q(omega)` with `omega^2+omega+1=0`, and `D=E+Ej` with `j^2=-1` and `ju=bar(u)j`. The norm on rational coordinates is

`x^2-xy+y^2+z^2-zt+t^2 = (x-y/2)^2+3y^2/4+(z-t/2)^2+3t^2/4`.

This is strictly positive for every nonzero rational coordinate vector; conjugation divided by this scalar gives an inverse. Hence division is a universal deduction, not a bounded numerical experiment. The order `O=R[omega]+R[omega]j` has an `R`-basis of four elements. The group map `a -> omega, b -> j` extends onto `O`. Modulo two its basis maps to `I,A,B,AB`, so `O/2O=M2(F2)`.

Conjugation preserves `O`. The norm of `1-2y` is a unit in `R` for every `y in O`, so every such element is a unit in `O`. Since `2O` is an ideal, the full Jacobson unit criterion applies; this verifies `2O <= J(O)`. Semisimplicity of the residue matrix algebra gives the reverse inclusion. Nontrivial residue idempotents cannot lift into the division algebra subring. Thus `O` is not semiperfect. Quotients of semiperfect rings are semiperfect: pass to the semisimple radical quotient, lift through its direct-factor quotient, then lift to the ring. The surjection `RG -> O` therefore proves that `RG` is not semiperfect.

The independent finite checker reproduces the two primitive projectives using `e=1+a+a^2`, `c=1-e`, `z=b^2` and `f=c(a+ab+1+z)` in `kG`. Their dimensions are both 4, and their corner/corner-radical dimensions are respectively `(4,3)` and `(2,1)`. The explicitly computed semisimple quotient is `F2 x M2(F2)`; its kernel powers have dimensions `7,2,1,0`. This proves primitivity without assuming the desired lifting conclusion. Their composition classes are `4[k]` and `2[V]`, witnessed by `4[Q]` and `2[W]`. The regular module dimension check is `4+2*4=12`.

There is also a direct actual-module check of the obstruction. The image of `f` in `O/2O` is `E22`. If `kGf` admitted a projective `RG`-lattice lift `L`, the base change `O tensor_RG L` would be a finite projective `O`-module whose reduction is `M2(F2)E22`, of dimension 2. It would therefore have `R`-rank 2. Its rational generic fiber is a vector space over the division algebra `D`, whose `Q`-dimension is divisible by 4. That is impossible. This verifies that the earlier example concerns actual PIM lifting as well as the Grothendieck monoid.

`verify_earlier_example.py` independently checks all 144 group products in the quaternion realization, 64 basis associativity identities, all 4096 modular elements for idempotence (52 idempotents), the radical powers and primitive corners, and the explicit nonlifting residue polynomial. These exact finite checks supplement the universal written argument; they do not replace positivity, the Jacobson criterion, or quotient closure. The checker uses explicit exceptions and passes under ordinary Python.

## Original source and possible apparent contradiction

Johnston-Rumynin arXiv `2507.21316v2` explicitly states the target as Conjecture 9 on printed/PDF page 3. Proposition 1.4 (pages 4-5) relates semiperfectness to actual projective/idempotent lifting. Proposition 3.1 (page 8) proves the necessary direction. Proposition 3.2 (pages 8-9) has a normal Sylow subgroup hypothesis, outside both examples. The cases `p` not dividing group order are also outside both examples.

Proposition 3.3 (pages 9-10) asserts a filtration sufficiency statement and invokes an unrestricted reduction isomorphism on `Ext^1`. This is not a valid reason to reject the explicit example: trivial `C2` actions yield `Ext^1_(RC2)(R,R)=0` but `Ext^1_(kC2)(k,k)=k`, since an extension generator `((1,t),(0,1))` must satisfy `2t=0` over `R` while `t=1` gives a nonsplit modular extension. The cited earlier resolution already records this obstruction. The saved fifth author response's Ext observation therefore cannot be promoted as an independently established new correction to that version. Neither counterexample relies on Proposition 3.3. The saved proof's credited `A5` inputs occur in Example 3.4, pages 10-11; their existence is distinct from the conjectural general implication.

## Maintained status and dated chronology

The October 6 update-2 post links the current main Notebook. Its printed page 186 marks **\*21.60** and records the negative answer with the exact words “AI solution confirmed by D. Rumynin”, crediting M. Kinyon and J. Urban and linking the source audited here. The update-only PDF repeats the entry on printed/PDF page 29. The preface on printed page 4 and the editor post distinguish unconfirmed AI proposals (sharp marker, still unsolved) from confirmed solutions (star marker). Thus treating current 21.60 as merely an unverified AI proposal contradicts the maintained source. This is an entry-specific editor attestation; it does not certify every candidate in the multi-problem report, our saved example, historical priority, or any new paper's novelty.

| Date and evidence | What is established | Boundary |
|---|---|---|
| July 28, 2025; October 9, 2025 v2, arXiv submission history | Exact retained original paper dates; v2 poses the modular criterion as a conjecture | Not a current openness certificate |
| September 1, 2026 editor update post | A maintained September revision was posted | Its linked old PDF now returns 404; no historical page body is inferred from that failed retrieval |
| September 11, 2026, author's `research/21.60-review.md` explicit audit date | The order-12 construction is documented by the authors as internally audited then | An author record date is not an independently established first public release time |
| September 11, 08:10:16 UTC, author proof commit; repository created September 11, 12:27:28 UTC | Repository technical chronology supports the dated author records | Commit/repository timestamps alone do not prove when a formerly private artifact became public; history was filtered |
| September 19, 2026, title page and author README | Version 4 of the audited cited edition is explicitly dated | No publication date is inferred solely from PDF creation metadata or the URL directory |
| October 3, 2026, saved selected PR research log | All five author attempts completed; saved publication checkpoint is 12:45 UTC | The saved historical source gate explicitly disclaims exhaustive novelty |
| October 6, 2026, maintained editor post (visible date and unmodified publication entry), plus linked current PDF | The maintained editor announces this revision and it records the confirmed negative resolution | This establishes maintained current status; a web archive proving the first appearance of the link was not obtained |
| October 12, 2026, this independent retrieval | Current source bytes, exact-target match, and validity of the earlier proof are independently checkable | Does not adjudicate personal discovery priority |

The earlier primary mathematical artifacts expressly predate the October 3 selected record. The maintained resolution was announced by October 6 according to the publisher's dated post and is present in the current October 12 retrieval. A precise first public upload date remains a chronology gap, explicitly preserved rather than guessed. That gap does not restore current unsolved status or support a novel solution claim.

## Strongest result and remaining gap

Strongest verified result: the current authoritative target is negative and confirmed, with a valid cited order-12 counterexample satisfying the exact base fields and all-PIM positive condition; the accepted order-120 counterexample is an additional example of the same failed implication. The cited source also predates the saved Ext correction in its explicit author records.

Remaining novelty gap: no independently verified new general statement, strict strengthening, or previously unrecorded mechanism has been identified in the selected saved claim. The exact first public-upload chronology of the earlier work is unestablished, so this report does not assign personal discovery priority. No new proof search, external communication, remote write, queue/status/PR mutation, publication, or release occurred. Completion toward this audit objective: 100%; completion toward a supported new publication claim: 0% on the evidence audited here.

## Primary source locators

1. [Maintained October 6 update-2](https://kourovkanotebookorg.wordpress.com/2026/10/06/october-2026-update-2-for-the-21st-edition/), links to main and update-only PDFs and states the marker policy. [Main PDF](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21tkt-1.pdf), printed page 186, exact entry 21.60; printed page 4, marker policy. [Update-only PDF](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21upd-1.pdf), printed page 29, exact entry.
2. [Cited mathematical edition](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/09/kourovka-mathematics.pdf), title page version/date; §3.40 pp55-56; reference [60], p84. PDF page numbers equal printed numbers for these locators.
3. [Author repository](https://github.com/JUrban/kour1), README explicit experiment and edition dates; [frozen exact proof](https://github.com/JUrban/kour1/blob/b567ffdaecf60466e1a8afd3e8dbac5f403c4e76/research/21.60-proof.md), sections 1-3 and relation to the original conjecture; [specific review](https://github.com/JUrban/kour1/blob/master/research/21.60-review.md), exact computations and explicit idempotents. The latter's retrieved bytes are pinned in the receipt manifest even though the URL is mutable.
4. [Original retained conjecture](https://arxiv.org/abs/2507.21316v2), submission history; PDF Conjecture9 p3, Proposition1.4 pp4-5, Propositions3.1-3.3 pp8-10, Example3.4 pp10-11.
5. [Author full account](https://github.com/JUrban/kour1/blob/master/paper/kourovka-experiment.pdf), §6.1.8 pp25-26, same exact proof; p129 review summary. Only relevant 21.60 text was mathematically inspected. Other entries and broad experimental claims were not audited.

Exact byte hashes and retrieval outcomes are recorded in `SOURCE_RECEIPTS.json` and `PRIMARY_QUERY_LOG.json`. No extended foreign text or foreign binary artifact is included in this public review directory.
