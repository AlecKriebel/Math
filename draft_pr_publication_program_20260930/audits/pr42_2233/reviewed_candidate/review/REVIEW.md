# Current source precision and historical qualifications

EP-653 / 2233 remains **UNSOLVED**. The valid scoped partial consists of the
generic-gluing deficit-spectrum identity and proper-polynomial open dense
complement, the sharp ceil(n/2) line/circle bound, its t=o(n) exception extension,
and the classical Erdős–Saldanha two-pin square-root defect. Their exact stated
hypotheses are essential. Finite controls supplement these proofs. They do not
solve the unrestricted asymptotic question, improve the reported historical
coefficients, or certify novelty, priority or best-known bounds.

The raw research-results object has **no EP-653 key**. `pinned_prior_report.json`
stores `{}` as a SQL fallback. This is neither a fetched prior result nor a
null-valued raw entry. The 2026-08-17 OPEN-TRIAGE text is dated background in the
problem record. The original source audit's “entry is null” sentence is corrected
in current presentation; its complete original body remains byte-exact in
`original_archive/SOURCE_AUDIT.md`.

Original head `099ae5e4d06d8789214cfaaece87309c87e914f9`, actual original base
`60292bed09f59236aa192cb17aa138f7b4750e1a`, original17 and full diff18 are retained.
The final mathematical file SHA256 is
`0b116a4593d84d7e9d02f635a080eb0e2242aaba66acfc8efeae74462ad89898`;
the reviewed file SHA256 is
`b51799d262ea7f633771128422708232c0522e7fddbaa5062a955911ed2e79f5`.
Only the review-status header replacement separates them. All mathematics is
unchanged. Saved author `check_results.json` binds the reviewed hash; ROOT's
genuine final-file replay differs only in `partial_sha256`. Reviewed author
and original independent saved FILE objects are byte-exact genuine replays.
The original mathematical/source/code/result/ledger files are retained exactly,
including this honest header-hash distinction and original source checksums.
Those checksums identify archived originals; the current packet's manifest
identifies every current derivative.

Historical model/reasoning/time-window, source access/search and review labels
inside original17 or closed families are attributed dated records, not a
certificate of genuine historic runtime. The 2026-09-30 original review remains
historical evidence; it does not approve the new current packet. Genuine ROOT
reproduction on 2026-10-02 records 18,306 current author checks, 18,306 reviewed
author checks, and 1,263 original independent checks with complete sources,
PIDs, argv/cwd, clocks, outputs, exits and full typed results. The whole raw
149,266,659 bytes and all 15,458 SQL joins were independently compared. The
wrong-base empty export and the guessed receipt-name failure occurred before
scientific execution and remain retained with their sources and full captures.

The new literal and exact families verify scoped original mathematics under
their disclosed independence and reading limits. Their closed manifests bind
the exact bodies. ROOT must author its own proof/source reading record and
scope certificate after personally reading the requisite evidence. The source
preparer's false/null drafts do not attest ROOT reading or approval.

The relevant 1995 manuscript pages14–15 establish the intended distinct-point
spectrum question and Saldanha credit. The exact 1997 article and complete
Erdős–Fishburn and Csizmadia–Ismailescu proofs remain unavailable/unverified as
recorded. The 2026 external preprints and Janzer input are reported source
claims with explicit reading limits; their proofs are not certified here and
none is an elementary-proof premise. No current absence-of-literature or
priority claim follows from the bounded searches.

Foreign primary PDFs, HTML, headers, extracted text, renderings and the named
`literal_geometry_family/controls/primary_pdf_extract.stdout.txt` derivative
are individually hash-bound dependencies, retained in their original audit
families, and excluded from copying/authorship in the current packet. This
preserves the full original extraction capture without republishing its paper
text. Other first-party source/capture/failure history is copied exactly with
appropriate attribution. Dependencies resolve from the repository-relative
PR42 audit root, including after canonical copying, never from scratch.

Current model, reasoning, deadline and whole verdict remain explicit nulls.
The **NEW whole-current source-first adversarial review is PENDING** even after
an actual administrative freeze. Original attempts are **2/5**, new substantive
attempts **0**, audit turns **0**. No paper, DOI, tracker entry, native/canonical/
shared/Git/remote write, release or external human communication is performed.

Historical body follows. Its model/reasoning, search/access and review labels are reported archival claims; this administrative packet does not certify genuine historic runtime or transfer old PASS to the NEW whole-current review. See SOURCE_PRECISION_QUALIFICATIONS.md.

# Independent adversarial review: EP-653 / 2233

**Verdict: PASS for the scoped partial obstruction package. The original asymptotic problem remains unresolved. No mandatory mathematical correction was found.**

- Reviewed: 30 September 2026
- Independent reviewer: gpt-6-astra, xhigh
- Artifact: `PARTIAL.md`
- Frozen SHA-256: `b51799d262ea7f633771128422708232c0522e7fddbaa5062a955911ed2e79f5`
- No edits were made to the author's mathematics or source files
- This is an adversarial AI review, not external peer review or a historical-priority certificate

## 1. Exact original target

The target counts the distinct **integer pinned-distance counts** attained by the points. It does not count the total set of distances and does not ask for many distances from one chosen pin. For n distinct planar points, the relevant values lie between 1 and n−1. The desired number of different values is n−o(n).

I checked the complete 1995 Erdős manuscript at Section III.1, manuscript pp. 14–15, and inspected the supplied rendering of p. 15. It expressly asks about the number of distinct values among the pinned counts and proposes n−o(n). Page 14 credits the two-pin product observation to Erdős and Saldanha. The publisher verifies the 1995 article's identity and journal pagination. The package correctly distinguishes this recovered source from the tracker's cited 1997 article, whose bibliographic entry is confirmed but whose full text was not recovered.

A fresh direct request to the official tracker again returned 403. The package's source audit accurately labels indexed evidence and does not claim a successful live tracker read.

Sources: [1995 full manuscript](https://www.ime.usp.br/~yoshi/resenhas/abstracts/Erdos.pdf), [1995 publisher record](https://revistas.usp.br/resenhasimeusp/en/article/view/74798), [1997 publisher contents](https://www.jams.jp/notice/mj/46-3.html).

## 2. Generic translation gluing

Lemma 1 and its four consequences are correct.

The density claim is a finite-dimensional algebraic genericity statement. I checked all cases of a forbidden distance equality:

- If the two comparison points lie in one external block, their difference is a fixed nonzero vector. Subtracting the squared distances cancels the quadratic terms and leaves a nonconstant affine polynomial in the relative translation.
- If they lie in different blocks, choose a block containing one comparison point but not the pin. Varying just that block leaves a nonzero quadratic term.
- This includes the case where the other comparison point belongs to the pin's own block. Equalities wholly internal to that block are intentionally allowed.
- A point coincidence between two distinct blocks is also a proper algebraic condition. Coincidences inside one seed cannot occur because each seed is a set of distinct points.

Each forbidden locus is closed with empty interior, and there are finitely many. Its complement is therefore open and dense. The case of one block has no forbidden cross-block constraints and causes no exception.

At an admissible pin, every external point contributes a new distance distinct from all the internal distances. Subtracting the resulting count from n−1 cancels the number of external points exactly. Thus each pin retains its seed deficit, and the deficit spectrum of the union is exactly the union of the seed spectra.

Singleton seeds have deficit zero. For maximum seed size M≥2, every seed deficit lies in 0 through M−2, so the total spectrum has at most M−1 elements. When M=1 it has one element. Applying the same identity at each finite level proves the hierarchical assertion; it requires every joining step to satisfy the stated admissibility, not merely a generic first level. The union of two unit segments into a unit square is a valid negative control: the internal deficit is zero, while the square's deficit is one. Nongeneric cross-block equalities are exactly where the identity need not hold.

No claim is made that arbitrary nongeneric gluings obey this obstruction, or that translations can encode a successful construction for the full problem.

## 3. Line and circle restrictions

The upper bound in Lemma 2, including its exact integer rounding, is correct. A positive distance circle centered at a pin meets a supporting line in at most two points. When the pin lies on a positive-radius supporting circle, the two circles have different centers and are distinct, so the same bound holds. This forces every pinned count to lie between ceil((n−1)/2) and n−1; that integer interval contains exactly ceil(n/2) values.

Both sharp constructions work for all n≥2. Consecutive equally spaced line points have pinned counts max(i,n−1−i). For the circular arc, the imposed total angular span below pi makes each chord length strictly increasing in the absolute index difference, yielding the identical count list. The circular argument would not be valid for unrestricted equally spaced points winding around the whole circle; the stated arc restriction prevents this issue.

Lemma 3 also survives the strongest simple exceptional case, an extra point at the center of the supporting circle. Such a pin can see very few distances, but it is one of the at most t exceptional pins. Every supported pin still sees at least ceil((m−1)/2) distances among the supported points. Their possible full counts occupy at most n−ceil((m−1)/2) integer values, and exceptions add at most t. The additional n−1 bound and the (1/2+o(1))n conclusion follow as written.

Here concentration means that n−t points lie **exactly** on the same line or circle. The package does not assert a theorem for arbitrary points merely close in Euclidean distance to such a support.

## 4. Classical two-pin estimate

For distinct pins p and q, every other point lies at an intersection of one circle centered at p and one centered at q. A pair of these circles has at most two intersections, giving n−2≤2r(p)r(q). Distinct centers prevent coincident circles, including when the two radii happen to be equal.

If the different pinned counts are a1<…<as, the bound aj≤n−s+j−1 follows from the number of remaining larger integers at most n−1. For s≥2, choose pins realizing a1 and a2. With h=n−s, the product estimate yields n−2≤2h(h+1). Solving the quadratic gives exactly the displayed expression with sqrt(2n−3). For s=1, h=n−1 makes the same inequality immediate. The n=2 boundary case is harmless.

This is correctly credited as a classical elementary bound, not a new improvement. Its sublinear deficit, and the stronger sublinear deficits reported in the source audit, are compatible with the desired asymptotic ratio one.

## 5. Literature and external-claim caveats

The source audit does not depend on the unavailable complete Erdős–Fishburn or Csizmadia–Ismailescu papers to prove its elementary lemmas. It treats their numerical historical bounds as reported literature, not fully re-audited results. The joint authorship and distinction between the 1997 volume and a later platform date are preserved.

I directly opened the two author-uploaded 2026 Bado preprints listed in the audit. The first states a 5/7 deficit exponent; the second states an exponent arbitrarily below approximately 0.8173595896. Both explicitly retain the original asymptotic question as open. Their hosting pages distinguish preprints from peer-reviewed publication. The Janzer–Janzer–Methuku–Tardos arXiv record and the named incidence input were checked for bibliographic scope. This review does **not** independently certify those newer arguments or all their cited inputs. None is a premise of `PARTIAL.md`, and the package appropriately avoids a best-known-bound or full-resolution claim.

Sources: [Bado incidence preprint](https://www.researchgate.net/publication/414001878_An_incidence_bound_for_distinct_pinned-distance_counts), [Bado Katz–Tardos preprint](https://www.researchgate.net/publication/414000090_A_Katz-Tardos_upgrade_for_planar_distance-count_spectra), [Janzer et al.](https://arxiv.org/abs/2411.07188).

## 6. Independent exact checks

The author's checker and frozen mathematical artifact were copied to the review directory before replaying the script, so its output-writing behavior did not modify the author directory. All **18,306** assertions passed; the replay receipt is byte-identical to the submitted one.

The independent script passes **1,263** exact assertions using SymPy 1.14.0 and rational arithmetic. It includes:

1. 162 symbolic checks that all forbidden-equality polynomials in a three-block control are nonzero and have the predicted degree
2. A deterministic grid of 121 two-block translations, with 37 admissible and 84 inadmissible cases, checking the exact count and deficit identities in every admissible case
3. The nongeneric square negative control
4. Exact rational-rotation circular arc constructions attaining the sharp bound for every n from 2 through 30, together with line attainment
5. Supported configurations with exceptional center pins and other off-support points, checking the exception bound and two-pin inequality
6. Independent integer-rounding and quadratic-root identities

These computations are finite diagnostics. The algebraic genericity and all-n geometric proofs were separately checked above; no experiment is being used as a substitute for the original asymptotic theorem.

## 7. Disposition

**Required mathematical corrections: none.** The scoped obstruction package is fit for a draft PR with an `unsolved` queue status and no new-discovery credit. The missing task is still a family with n−o(n) distinct pinned-count values, or a universal obstruction disproving that possibility. Generic small-seed gluing and near-total exact line/circle support do not deliver either outcome.

If the pending-review status sentence is updated, the final hash should be linked by an exact diff. New substantive mathematical changes would require re-review.

## Final publication snapshot

The final `PARTIAL.md` SHA-256 is `0b116a4593d84d7e9d02f635a080eb0e2242aaba66acfc8efeae74462ad89898`. Exact byte comparison confirms that replacing only the pending-review header sentence with the passed-AI-review sentence and report link produces this final file. All mathematical and source-scope text is unchanged. The verdict above applies to this final snapshot as well.
