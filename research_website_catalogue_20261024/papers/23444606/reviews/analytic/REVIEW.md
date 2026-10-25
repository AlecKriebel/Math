# Independent analytic review — Zenodo 23444606

**Disposition: PASS at the manuscript's stated hypotheses.** I found no substantive mathematical defect in Theorem 1, Lemmas 2–3, or the appendix's sufficiency proposition. The strongest supported result is the full ordered-additive-group assertion for every discrete initial subgroup of the surreal numbers, including proper classes in NBG with global choice. This is an AI mathematical review, not external human peer review, a formal proof-assistant certificate, or a novelty/priority certificate.

## Exact reviewed object and independence

The reviewed work is **Initial omnific models of discrete initial surreal groups**, Alec Kriebel, Zenodo **23444606**, DOI `10.5281/zenodo.23444606`, metadata version **1.0.0**, published **17 October 2026**. The manuscript prints that date but no separate version label. The complete seven-page public PDF and its current `main.tex` were read, including the appendix and all qualification/attribution text. The source archive has 145 regular files, one embedded reader PDF identical to the public PDF, and no nested archives.

- Public PDF SHA-256: `fa8c48fc0ec1c98b05ca4bf91cba37de86b91393f4085554bdecf87905bbb8d5`.
- Public ZIP SHA-256: `0830837e89037ee9c92e1d28f8fa8e30e95a86aa2878abf5176c314f155132b3`.
- Fresh Zenodo record SHA-256: `81bdd978e1cb80efb50b3d8b9ce39bc0acebc8890a0f2c505ff0b00cece66c44`.

The published mathematical support `FINAL_PROOF.md` and `pr_repair_candidate/DEPENDENCY_PROOF.md` was also read. These necessary proof files incidentally contain statements about earlier AI acceptance, repaired dependency steps, and bounded priority searches. I did not treat those statements as evidence of correctness. The manuscript itself also discloses historical internal reviews. Dedicated historical opinion/priority files and sibling/scope review bodies were not read. The source inventory and wrapper authenticate such files by bytes without adopting their contents. Raw primary PDFs/text and their acquisition receipt were used from the scope agent's cache; no scope conclusions were used.

The independent reconstruction and fresh control program preceded inspection of the submitted checker. Interrupted turns were resumed from the saved checkpoint; the completed fresh run was confirmed to have exited successfully, and no live verifier remained. An interruption was not treated as mathematical failure.

## Claim, assumptions, and success criterion

Let `G` be an actual additive subgroup of `No`, with its inherited order. “Initial” means that every proper ordinal-length sign prefix of every member belongs to `G`; it does **not** mean numerical convexity. “Discrete” means that a nonzero group has a least positive element. The zero group is included separately. Every surreal has its canonical, set-supported normal form with real coefficients.

The theorem constructs an order-preserving additive isomorphism `T:G→H`, where `H⊆Oz` and `H` is initial **in No**. The assertion concerns the actual image of `G`, not an enlarged Hahn completion. `T` need not preserve simplicity, multiplication, or a specified embedding into `No`. No claim about arbitrary discrete ordered groups lacking an initial surreal realization follows.

In a nonzero case, the least exponent is `m=−α`, with α a set ordinal; its coefficient group is `R_m=2^(−n) Z`, for a nonnegative integer n. Write `a=−^α`. The exponent map is

```
f(a) = empty,
f(s) = +s                         if s>a and a is not a prefix of s,
f(a(+)t) = +at                    when (+) is the first sign after a.
```

In the last line, the source is the concatenation `a`, one plus, and `t`. The normalization is `c_m=2^n`, with `c_y=1` elsewhere, and

```
T(sum r_y ω^y) = sum c_y r_y ω^(f(y)).
```

Success requires all ordinal lengths, all actual set-sized reverse-well-ordered supports, and both set and proper-class groups. Finite computations alone cannot meet that criterion.

## Independent proof reconstruction

### 1. The bottom exponent and coefficient group

Let `g>0` be least in `G`, with leading term `rω^m`, `r>0`. Truncation closure and subtraction put the leading term and residual tail in `G`. If the tail is nonzero, its absolute value is positive and strictly smaller than `g`, contradicting least positivity. Thus `g=rω^m`.

The initial subgroup `R_m` of the reals has least positive member `r`. Ehrlich–Kaplan's real-coefficient classification gives `R_m=2^(−n)Z` and `r=2^(−n)`; the alternative containing all dyadics cannot be discrete. If an occurring exponent `y<m` existed, cross sectionality would give `0<ω^y<rω^m=g`. Hence `m` is the minimum exponent. If `m` contained a plus sign, its prefix immediately before the first such sign would be an exponent below `m`. Therefore `m` consists entirely of minus signs and is `−α`. No finiteness or successor assumption on α was used.

This proof does not assume that the original `G` already lies in `Oz`. In particular, the familiar initial real group `(1/2)Z` is legitimately included and maps to `Z`.

### 2. Ordinal sign rotation

I checked the two nonminimum cases directly using sign order, with an undefined next sign compared as zero. Within each case the common block replacement preserves order and proper prefixes. Across cases, a case-A sequence either is `−^β`, `β<α`, or first differs from `a` with a plus before α. In the first situation it is a proper prefix numerically above the case-B sequence; in the second the two sequences are incomparable as prefixes and ordered by their first differing sign. Prepending the common plus preserves these distinctions. The cases cannot collide.

For every `s>a`, the exact prefix identity is

```
P(f(s)) = {empty} ∪ {f(v): v∈P(s), v≠a}.
```

For case B, the proper prefixes of `+at` are: the empty sequence; `+−^β` for `β<α`; and `+av` for proper prefixes `v` of `t`. If `t` is empty, `+a` is the entire image and must not be counted as an additional proper prefix. All source prefixes in this identity stay in the ray above `a`. Consequently an initial `Γ` maps to an initial `Δ`, whose minimum is zero.

The map preserves and reflects proper prefixes away from `a`. An image right predecessor cannot equal zero, since zero is the image minimum; therefore every image right-predecessor obligation reflects back to a source obligation at an exponent other than the bottom. This is precisely the condition needed after replacing the bottom coefficient group by `Z`.

The formula and its inverse are valid for ordered concatenations at limit ordinals. They do not cancel ordinal lengths or assume `1+α>α`. For positive `z=+v`, the inverse inserts a plus after `a` if `v` has prefix `a`, and otherwise returns `v`; zero returns `a`. The argument is a block partition argument even when `1+ω=ω`. At `α=0`, the map is the identity on the nonnegative ray. No class recursion is present.

### 3. Transport of the actual group

Increasing exponent relabeling preserves the reverse well-order type of each support; its image is a set. Positive fixed coefficient scalings preserve the leading sign. The displayed map therefore preserves addition, cancellation and strict order and is injective. Surjectivity onto the defined `H=T[G]` is automatic; no arbitrary series outside `G` have been added.

Truncations commute with `T`. For nonbottom exponents, source monomials map to image monomials. At the bottom the source element `2^(−n)ω^m` maps to `1`, proving cross sectionality there. An image containing exactly one nonzero term can only have a one-term preimage, so the pure coefficient groups are exactly

```
R'_0=Z,      R'_(f(y))=R_y  (y≠m).
```

These are initial real groups. Every right-predecessor requirement in the image reflects to a nonbottom source exponent, so the necessary dyadics remain present. Applying the independently checked sufficiency argument makes `H` initial in `No`. All its exponents are nonnegative. Every actually occurring zero coefficient is integral, because adjacent truncations isolate that coefficient into `R'_0`. The normal-form criterion for omnific integers then gives `H⊆Oz`.

### 4. The appendix really supplies sufficiency

This dependency is substantive: it cannot be replaced by citation alone when the two source proof steps identified in the paper require care. I reconstructed all four appendix subsections.

**Option covering and additive adjunction.** If `q={L|R}` and `z` is a proper prefix of `q`, then on the relevant side there must be an option between `z` and `q`; otherwise `z` itself separates the cut, contrary to the simplicity of `q`. A sequence between a prefix and its extension extends that prefix, by first-difference comparison. Thus `z` is a prefix of, or equal to, an option.

For initial sets `S,U`, recursive addition and induction on the **natural/Hessenberg sum of the two operand birthdays** show `S+U` is initial. Decreasing either operand decreases this measure, even when the birthday of the sum itself is unsuitable for induction. The prefixes of every recursive option are already in `S+U`; option covering then gives the prefixes of the sum. Negation preserves prefix relations, so finite additive closure of an initial set containing zero is initial. If an initial set subgroup `M` contains all options of a cut defining `b`, then `M∪{b}` is initial and `M+Zb` is initial. This derives the needed additive adjunction directly rather than assuming a stronger module theorem.

**Finite-support stage.** For a set exponent domain `E`, all actual series form a set. Order exponents by birthday, breaking ties by choice. Proper exponent prefixes precede each exponent. The monomial cut for `ω^y` has its left options among integer multiples at earlier exponents and its right options among dyadic multiples at earlier right predecessors, supplied by the hypotheses. After adjoining the leader, all its integer multiples exist. Noninteger pure coefficients can then be adjoined by increasing real birthday. Initiality of `R_y` provides their real predecessors. The two cases of the primary pure-multiple cuts, including the extra `±kω^(y^L)` terms in the dyadic case, all use previously admitted elements. Unions at limit stages are initial. The resulting group is exactly the finite-support subgroup of the actual `A`.

**Limit supports and exhaustion.** For an actual series `x` of infinite limit support length λ, let `s_η` be its η-term prefix. The options

```
l_μ=s_(μ+1)−ω^(y_μ),       u_μ=s_(μ+1)+ω^(y_μ)
```

belong to `A` by truncation closure and cross sectionality; no division of an actual coefficient is required. Their leading difference from `x` is `−1` or `+1` at exponent `y_μ`, so they bracket `x`. Given a standard dyadic-cut option at μ, choose `ν>μ`, possible because λ is limit. At the earlier exponent `y_μ`, the unit option at ν agrees with `x`, whereas the dyadic option differs by `±2^(−k)`. This proves the displayed cofinal/coinitial inequalities, regardless of later coefficients or cancellation of an option's final coefficient. The simplest separator of the legal unit cut is consequently `x`. The argument does not incorrectly require every option to be a prefix of `x`.

Well-order all actual infinite-limit-support members by support length, with a tie-breaking well-order inside a length. At a series of length λ, every shorter series is already generated: every ordinal ρ is uniquely `δ+j`, where δ is zero or limit and j is finite. Such a series is its δ-prefix plus finitely many pure terms. Every unit option has support length at most `μ+1<λ`, so additive adjunction applies. The same decomposition proves exhaustion of **all actual members**, including supports cofinal in the exponent enumeration. No false union of bounded exponent stages is used.

**Proper-class exponents.** Given any actual `x`, let `E` be its support together with all prefixes of its exponents. It is a set by replacement and union, is initial, and lies in `Γ`. The subgroup of actual series in `A` supported in `E` is a set; it inherits truncation closure, cross sectionality, the same pure coefficient groups at its exponents, and the right-predecessor condition. The set proof makes this subgroup initial and puts every prefix of `x` back in `A`. This local argument suffices for a proper-class `A` and requires neither a class well-ordering of its actual series nor a class-sized cut.

For necessity, the primary normal-form predecessor results give truncations, leader/exponent prefixes and real coefficient predecessors. Adjacent truncations isolate coefficients, and dyadic multiples at a right-predecessor exponent are simpler than the corresponding monomial. These are exactly the explicitly imported interfaces, not a hidden assumption that all possible supports occur.

## Primary theorem interfaces and attribution

The ledger `primary-interface-ledger.json` records exact fresh raw bytes, URLs, editions, text hashes and reading scope. Relevant findings from the primary bodies are:

1. **Ehrlich–Kaplan, 16-page author manuscript.** Read definitions and the normal-form/monomial interfaces, Lemma 3.1, Proposition 3.2, Proposition 3.3, Lemma 5.1, Theorem 5.1 with its proof, Proposition 5.2, §6.2's omnific criterion and Question 9.1. The canonical rather than arbitrary Hahn representation, initial exponent domain, initial real coefficient groups and dyadic right-predecessor requirement match the paper. The published appendix avoids the two literal support-exhaustion/option-legality issues in the author proof; neither issue is a counterexample to the characterization. The author body is a primary source, but its bytes were not authenticated against the final JSL publisher body. Standard underlying surreal normal-form theory is accepted as the stated foundation, not rederived back to the original monographs.
2. **Kaplan's April 2015 thesis, §7.1, Question 1, printed p.47.** The question is the additive-group question. The preceding `(1/2)Z` example explicitly distinguishes being an initial subgroup of `Oz` from being isomorphic to one. The current theorem addresses that exact distinction.
3. **Published OWR 60/2016, Kaplan's joint-work contribution, printed pp.3354–3356.** Its group definitions, theorem context and Question 1 agree with the target. No multiplicative closure is imposed on the group question.
4. **Ehrlich–Kaplan arXiv:1512.04001v1.** The corresponding question is numbered Question 2 in this earlier version. This edition was used to check attribution/numbering, not substituted silently for the inspected author numbering.
5. **Aschenbrenner–van den Dries–van der Hoeven, arXiv:1512.02267v3, Lemma 3.2 and proof.** An initial exponent set with a least element has a negative-ordinal least element. This is credited background and independently reproved in the current bottom lemma. Its Hahn-field context is not imported as an extra hypothesis on `G`.
6. **Kaplan–Krapp–Serra, arXiv:2509.22374v3, Proposition 3.9 and Construction 3.10, including the proof and explicit transport formula.** Exponent order relabeling and positive coefficient scaling are established Hahn-group operations. Their presentation involves automorphisms of the full group; the current proof checks its restricted actual-image construction directly. The new claimed bridge is the particular sign map/right-prefix control, not invention of Hahn transport. This source does not by itself establish the target image's initiality.
7. **Bagayoko–van der Hoeven, arXiv:2305.02001v1, Theorem 6.7 and Proposition 7.1 with proofs and hypotheses.** Thin partitions give surreal substructures, and the translation construction in §7.2 has a fixed set-sized additive subgroup assumption. These background constructions are not an automatic solution for every actual initial `G`. The fresh body is the May 2023 arXiv edition, not the separate April 2022 author edition mentioned by the paper; no identity of those editions is claimed.

The 2024 handbook chapter and the full 2001 predecessor were not independently read here. I make no absence-of-prior-work statement about them, no worldwide openness finding, and no firstness claim. Those limitations concern historical coverage; they are not an unfilled new lemma in the proof reconstructed above.

## Fresh controls and submitted reproduction

The fresh `fresh_controls.py` used a distinct exact ordinal-block representation before any packaged helper was read or replayed. It represents finite runs whose lengths are `ωk+n`, uses ordinal rather than commutative addition, retains nonempty blocks even when lengths absorb, and samples limit prefixes. It also uses exact rational coefficient vectors and lexicographic comparisons.

The completed run made **1,206,538 checked assertions**, including 496,136 strict-order checks, 493,209 prefix-reflection checks, 11,667 right-predecessor reflections, 500 exact Hahn-additivity controls, 500 order/cancellation controls, 2,513 truncation controls, and 16,800 unit-cut cofinal comparison controls. Nine bottom lengths include `0,1,2,3,4,ω,ω+2,2ω,2ω+3`. Countercontrols show that omitting the deletion can destroy initiality and an incorrect bottom scaling can leave a noninteger zero coefficient. The arithmetic check on dyadic perturbations illustrates why an integer coefficient group alone need not admit them.

These counts are operations within a finite diagnostic, not independent proofs or independent reviewers. The program's one `finite_stage_exhaustion_does_not_give_limit` assertion is only a finite illustration and is not evidence for an infinite exhaustion theorem. The actual transfinite exhaustion justification is the written ordinal argument above. Sampled blocks below `ω²` do not prove arbitrary ordinal or proper-class claims.

After those controls, I read the submitted `verify_finite_signs.py`, `verification/verify_all.py`, `package_common.py`, control plan and packaging self-test source. The selected mathematical replay ran the **unmodified** `verify_all.py` in an isolated copy inside this review folder:

- Both ordinary and optimized mathematical runs returned exit 0, empty stderr and the complete expected 319-byte output, not merely a `PASS` token.
- Each checked 1,538 nodes, 350,548 ordered pairs, 1,538 complete finite prefix sets, 4,374 right predecessors, 896 finite-support additions and 28 bottom generators, with minima 0–6 and signs through length 7.
- All four actual construction mutations failed at the expected computed mathematical property in each mode: omitted deletion, retained minimum, appended rather than prepended plus, and omitted normalization. Thus there were eight expected nonzero exits.
- The wrapper authenticated 128 authored audit members and the 144-member package manifest, and checked the embedded PDF/TeX pins.
- Full stdout, empty stderr and a timestamped process receipt are retained. The copied source files and original 145 extracted files were rehashed after replay.

The packaging builder and synthetic packaging self-test were **not executed**; neither is needed to establish the mathematical theorem or the selected published diagnostic claim. Historical family programs were not counted as reproduced. Authentication of archived opinion bytes is not adoption of the opinions. No downloaded primary PDF contains executable mathematics that was run.

## Boundary assessment and precise remaining scope

| Case or possible overclaim | Assessment |
|---|---|
| Zero group | Identity gives the stated result. |
| Bottom exponent zero | Rotation is the identity on the nonnegative ray; coefficient normalization still applies. |
| Bottom exponent a limit negative ordinal | Ordered-block argument handles ordinal absorption and does not cancel lengths. |
| Empty tail immediately after the deleted plus | The full image `+a` is not accidentally counted as a proper prefix. |
| Infinite support of limit or successor length | Legal unit cuts handle limit length; `δ+j` decomposition handles finite successor tails and exhaustion. |
| Support cofinal in the exponent enumeration | Actual-series induction covers it; bounded-stage union is not used. |
| Non-dyadic, dyadic and negative real coefficients | Pure-multiple cut cases and coefficient-group initiality cover them; signs and cancellation do not affect leading-order transport. |
| New bottom dyadic obligation | Excluded because zero cannot be an image right predecessor; nonbottom obligations reflect. |
| Proper-class `G` or exponent class | Every individual support and prefix closure remains a set; class formulas and local set restrictions suffice. |
| Full Hahn completion, ring embedding or simplicity-preserving isomorphism | None is claimed or needed. |

**Exact remaining mathematical gap:** none identified for the stated theorem using the explicitly cited standard surreal foundations. The review does not claim to reprove all foundational normal-form theory, verify every historical source, authenticate unread publisher editions, certify global novelty, or constitute formal/human peer review. Finite controls are supplemental evidence only.

**Recommended scientific disposition:** the exact theorem is eligible for the parent's remaining independent review and publication gates. This review performs no publication, source correction, website, spreadsheet, Git, deployment or outreach action. No follow-up conjecture is proposed from this review alone.
