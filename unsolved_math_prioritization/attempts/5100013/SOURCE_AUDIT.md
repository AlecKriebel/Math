# Exact source, prior-work and contribution audit

Target 5100013 / AMR-050-0013, source code k204, original queue rank270.
Both full source PDFs were read and Table3 was rendered and visually inspected:
arXiv2004.12497v11 p6 and the final Arnold Mathematical Journal article p346.
The row is stable across these editions: A/A_M, N=2 modulo4, all M, with a
question mark in the proof column. Section3.3 defines the pedal of the original
orbit side lines; the preliminary signed shoelace convention covers stars.
The source's ellipse pair is strictly nondegenerate and confocal, with a>b.

The row is interpreted on its natural quotient domain. The proof supplies
a global proportionality first, a positive denominator for convex families,
and an exact primitive-star family with identically zero pedal area on a
circle of fixed M. It does not promote those undefined quotients to finite
values, identify them as removable0/0 values, or call them a disproof of
invariance where the quotient exists. Least period is explicit. Repeating
an odd primitive orbit does not create the source parity property.

## Gate and primary access

- Complete pinned source record and previous third-party report were recovered
  from revision37e53eabe540fb458758e198be61634bd02ee008. Their hashes are in
  TARGET.json. The old report supplies no proof and consumes no author turn.
- All-state GitHub PR search for5100013/k204, branch search, and exact attempt-path
  main commit history found no prior exact campaign target. The related-target
  group file contains no5100013 entry. This is not a historical novelty guarantee.
- Related reviewed campaign PR203/k203,a and PR204/k203,b were inspected rather
  than ignored. PR203's remote head8edca9d773c085adb4ed0611357a7a2957e3395d
  carries the earlier arbitrary-M proof. Its SHA256 is pinned in source_manifest.
- Full Stachel published Theorem4.3/(4.9), printedp1614, supplies the canonical
  coordinates, period/turning-number convention and contact phase. The university
  archive filename mislabels the journal; the PDF/header and DOI give European
  Journal of Mathematics8(2022),1602–1622. The adjacent printed dn-shift typo
  is not used.
- NIST DLMF22.4 and22.8 were opened for the exact real/imaginary periods,
  poles, zeros, quarter shifts and addition identities. The modulus convention
  is k; mpmath receives k².
- A bounded current search found the source row and related pedal literature,
  but no exact published k204 theorem beyond the already inspected mechanism.
  Absence from that search is not a priority or novelty certificate.

## Shared-author and classical credit

This proof deliberately reuses the reviewed k203,a radial and two-pole lemma,
including the central-pedal author contribution originating in k203,b. The
proof is repeated here with general even-period hypotheses so that the new
N=2mod4 alignment can be independently audited. That alignment is a corollary
of the existing method, rather than an independent discovery. The exact
convex positivity and star denominator qualifications were checked in the
current substantive turn. Stachel, classical Jacobi theory, and classical
compact-torus pole cancellation retain their full credit. The prior
Chavez-Caliz area-product theorem is not required for this ratio target.

One substantive author turn covers the parity proof and complete domain
analysis. Source retrieval alone was not counted. A separate uninvolved
review is required before any PR or final status promotion. Proposed
post-review disposition is a credited already_solved1/5 consequence, not
a novelty claim. No person was contacted and no external executable was run.
