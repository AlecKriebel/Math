# Independent integration review: proof-first pivot

Date: 2026-07-26 (PDT)

## Verdict

**REVISE.**

The frozen mathematics and archive binding for C-058--C-062 otherwise pass
this integration audit.  Every artifact hash in
`results/universal_proof_pivot_acceptance.json` matches the current byte
stream.  The acceptance record explicitly preserves the one-guard model,
states that the universal conjecture is unresolved, starts no order-14 work,
and makes no novelty or priority claim.  The two lightweight Schläfli
replays reproduce the frozen output hashes
`d50d01db...` and `7c1af42d...`.

The public workstream page correctly identifies Alec Kriebel in the HTML
author metadata, structured data, byline, and disclosure.  It prominently
and repeatedly says that the universal conjecture remains unresolved,
defines attacks as unoccupied and exactly one adjacent guard moving along
one edge, distinguishes clique cover from the Lovász theta function, and
does not present C-058--C-062 as a conjecture resolution or counterexample.

## Required defects

1. **C-058 overstates the Hall certificate without its necessary
   hypothesis.**  In `CLAIMS.md`, the sentence “A Hall violation is
   therefore a compact static certificate that
   \(\gamma^\infty(G)\geq\alpha(G)+1\)” follows a theorem stated for an
   arbitrary independent \(k\)-set.  This conclusion is valid only when
   \(k=\alpha(G)\), equivalently when the reference \(S\) is maximum.  The
   frozen source note states this correctly in Corollary 4.2.  Amend the
   registry sentence to say, for example, “When \(k=\alpha(G)\) (so \(S\)
   is maximum), a Hall violation ...”.  Make the same qualification in the
   current `STATE.md` sentence, which presently repeats the unqualified
   implication.

2. **The current state file uses novelty-suggestive wording inconsistent
   with its own archive boundary.**  The heading “C-058 is a new universal
   Hall obstruction” can naturally be read as a literature-novelty claim,
   while the acceptance JSON sets `novelty_priority_claimed=false` and the
   targeted audit remains search-limited with the directly relevant 2018
   manuscript unavailable.  Replace “new” with “campaign-derived” or
   “proved” (or explicitly “new to this campaign”).  The claim registry,
   literature ledger, README, acceptance JSON, and public page otherwise
   preserve the no-priority boundary correctly.

No mathematical defect was found in C-059--C-062, no complement/model
confusion was found, and no website-attribution or unresolved-status defect
was found.

## Final addendum after correction

The two required defects above have been corrected and this review's final
verdict is now **ACCEPT**.

- C-058 now observes from the existence of both an eternal \(k\)-family and
  an independent \(k\)-set that
  \(k=\alpha(G)=\gamma^\infty(G)\), and it expressly conditions the Hall
  certificate on \(k=\alpha(G)\).
- `STATE.md` now calls the result “campaign-proved” and repeats the
  \(k=\alpha\) qualification.
- The public page now frames the statement inside a candidate with
  \(k=\alpha\), fixes a maximum independent \(k\)-guard state, and conditions
  the Hall conclusion on existence of an eternal \(k\)-family.

These edits resolve the logical qualification and literature-priority
wording without altering the frozen theorem artifacts or their acceptance
hashes.
