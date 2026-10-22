# Reduced powers on loop spaces: audited partial results

Problem **11100062 / AMR-110-0062**, catalogue rank 848. Disposition:
**unsolved, 5/5 substantive approaches**. This is an AI-assisted, unrefereed
research checkpoint. Independent internal audit accepted the scoped results;
it did not accept a solution to the original question.

For each fixed finite simply connected CW complex X, the original target asks
for a single sufficiently-large-prime threshold that makes every positive
reduced power vanish on H*(ΩX; F_p), uniformly over every input degree. That
fixed-X uniformity question remains unresolved by this work. P^0 and the
Bockstein are outside the target.

## Read the mathematics

- [Authored proofs and exact scope](author/RESULT.md)
- [Five substantive approaches and remaining gaps](author/APPROACHES.md)
- [Independent mathematical audit](independent_audit/INDEPENDENT_AUDIT.md)
- [Acceptance record](independent_audit/ACCEPTANCE.json)
- [Current publication verdict](VERDICT.json)

The accepted results are:

1. The homology-generator criterion: generator degrees strictly below 2p
   force every positive reduced power to vanish.
2. The sharp dimension-only suspension criterion dim(Y) < 2p for ΩΣY.
3. A credited consequence of Stanton–Vylegzhanin's January 2026 preprint:
   odd p >= m suffices for moment-angle complexes on m vertices, under the
   no-ghost-vertices convention. No Bockstein conclusion is asserted.
4. The actual Steenrod-stable Eilenberg–Moore filtration gives the strict
   degree-window condition 2(p−1) > (d−r−1) floor(N/r). When d−r−1 > 0,
   this bound depends on N and does not give one threshold for all degrees.
5. The family X_p = Σ²CP^p has vanishing positive-degree pth cup powers
   but nonzero P^1. The space varies with p, so this is not a fixed-X
   counterexample. It also verifies sharpness of the degree-window endpoint.

No correction was required. Both frozen archives and all their members are
preserved byte-for-byte. Historical fields saying review was pending or
publication had not occurred remain unchanged; the later acceptance and
publication records must be read alongside them.

## Source and status limits

The [author's source audit](author/SOURCE_AUDIT.md) and
[independent inspection record](independent_audit/PUBLIC_SOURCE_INSPECTION.json)
distinguish directly inspected material from restatements and inaccessible
sources. In particular, the complete 2025 thesis and the author's reported
indexed Conjecture 1.3 excerpt were not independently recovered during review.
The April 2026 follow-on paper received a bounded abstract/introduction/Steenrod
discussion check, not a full proof audit. The January 2026 generator theorem is
the cited inspected version, not a claim to be the latest work in the subject.
Deep external theorems are used as cited inputs. No novelty claim, exhaustive
priority search or certification of current global openness is made.

## Preservation and verification

- [Original author archive](frozen_author_11100062.zip): 13,840 bytes;
  SHA-256 `5de2a4ab509186a5fdc6929079c3b710b7760afc7d271a1884a1a6158e5fb4dd`.
- [Independent audit archive](UNSTABLE_HOMOTOPY_11100062_INDEPENDENT_AUDIT_SAFE.zip):
  26,412 bytes; SHA-256
  `a3b27780e8e533f1f8a6b450c817846b9316b91344313f0bea134c3c85c40a4f`.
- [Publication manifest](PUBLICATION_MANIFEST.json) binds the readable files,
  archives, receipts and verification metadata.
- [Publication checks](PUBLICATION_CHECKS.json) record strict data-only
  inventory/hash/size checks and replay under normal, optimized and relocated
  isolated Python modes. Each mode rejected 12 malformed controls and checked
  86,688 finite integer instances of the degree identity.

These finite tests check integrity and arithmetic consistency. They do not
prove the topological theorems. No executable checker is included, and no
archive member is executed. The proofs require mathematical review.

Only the selected row's Status and Turns cells change in QUEUE.md. Its other
cells and every unrelated byte are preserved. Corpus contents, downloaded
papers, source text, private coordination and private test code are excluded.
No merge, GitHub release, DOI creation or external outreach is part of this
draft publication.
