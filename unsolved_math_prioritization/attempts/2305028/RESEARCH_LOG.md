# Research log

## Turn 1: exact-source recovery and complete prior-proof verification

1. Attempted the exact catalogue URL, then read its pinned record for
   bibliographic identification. The record's generated open-status claim
   was contradicted by the actual primary update.
2. Read Hayman–Lingham Problem 5.28 and Update 5.28. The update identifies
   a negative answer and gives the precise 1975 reference.
3. Retrieved the full Rubel–Shields–Taylor article from its university
   repository. Read the relevant complete proof, Lemmas 4.1 and 4.2 and
   Proposition 4.3, including page images where extraction was incomplete.
4. Verified the half-plane boundary maximum, the bounded cutoff,
   expanding-circle transfer, and summable perturbation construction.
   The source proves a single-function limsup obstruction, which is enough
   to refute the proposed limit.
5. Wrote a full verification with explicit arithmetic constants and a
   detailed limit argument, reconciled the open-disk numerator, and ran
   the exact standard-library verifier.

## Outcome and stopping condition

The exact problem already has a published negative solution. This first
source-verification turn establishes that prior resolution, so no new
five-attempt sequence is represented as having occurred. The appropriate
outcome is `already_solved`, with one completed turn and no novelty claim.

The full analytic proof is in PROOF.md. Machine checks certify the stated
rational constants and error budget; they do not substitute for mathematical
review of the analytic steps.
