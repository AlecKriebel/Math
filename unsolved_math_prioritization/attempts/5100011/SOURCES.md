# Source, contribution, and prior-work audit

## Identity and scope

Numeric upstream ID5100011, AMR-050-0011, original queue rank219.
Both source editions retain k203,a in Table3: A A_M, period0mod4, all M.
The arXiv table is printedp6; the final table is printedp346. The source
introduces a confocal ellipse pair and defines every polygon area by signed
shoelace sum. The relevant pedal is to the original orbit's side lines.
The formula's punctuation is not read as a simultaneous assertion for a
moving M: M is any chosen fixed point while the orbit phase varies.
Primitive period and admissible star turning numbers are explicit in the
candidate. Hyperbolic/degenerate caustics and unsigned filled-lobe area are
not silently substituted. Related k203,b restricts M=O but adds odd periods;
it is a different target, with an overlapping0mod4 central case.

## Inputs actually read

- Reznik, Garcia, Koiller: full arXiv2004.12497v11 and full final2021 PDF.
  Table3 and the source area/pedal definitions were read; finalTable3 was
  rendered and visually inspected.
- Stachel: full published *On the motion of billiards in ellipses*, European
  Journal of Mathematics8(2022),1602–1622. Theorem4.3/(4.9), p1614, and
  contact-phase interpretation. The university catalogue misnames the
  journal; the PDF/publisher title is used. The adjacent printed dn-shift
  sign typo is not used; DLMF gives the correct real and imaginary shifts.
- NIST DLMF22.4 and22.8: the specific sn,cn,dn poles, quarter shifts,
  imaginary/real period signs, and addition identities were opened and read.
- Chavez-Caliz: full published *More About Areas and Centers of Poncelet
  Polygons*, ArnoldMath.J.7(2021),91–106. Signed area definitionp93,
  complex-projective general positionp94, Theorems3 and6, complete proofp104.
  The latter page was rendered and visually inspected.

Exact source URLs, PDF hashes, and pinned dataset hashes are in the source
manifest. Full PDFs/images/text remain local ignored reading copies.

## Shared-author mechanism and campaign reuse

The central-pedal simple-pole cancellation and two-pole uniqueness were
shared by the parallel author of target5100012/k203,b. Its frozen initial
checkpoint is target5100012’s `TURN_1_CHECKPOINT.md`,
SHA2565d83783e146fc840c374b81b94554900543f6447c7bbafc32485914222822ba3.
That checkpoint is author input, not independent review. The present
turn1 supplied the radial-in-M signed-area lemma; turn2 extended the
meromorphic symmetries and pole argument to every fixed M, then linked the
pedal area to the contact-polygon area.

The published even-period area-product theorem belongs to Chavez-Caliz.
The elementary polarity transfer to A A_inner is reproduced in full and
was also used in the campaign's k110/5100004 work. No private Stachel
communication is needed for that transfer. The general pole-cancellation
method is classical. These dependencies are not presented as separate new
discoveries. The assigned independent reviewer must be uninvolved in either
author's shared mechanism.

## Prior attempts and bounded literature check

2026-10-01 04:48–04:50 UTC: local all-ref commit-message and path checks,
GitHub all-state PR searches for5100011 andk203, remote branch search,
target-attempt-directory commit history, and the related-target ledger
found no earlier Alec attempt on this exact target. Generic pedal PR search
returned no match. Related k107/k108 counterexamples, k110 polarity proof,
k114, k115, k117, and k120 work is not counted as this target's attempt.
The old upstream OPEN-TRIAGE report is third-party literature triage and
has consumed none of this author's five-turn budget.

Focused current searches of pedal-area/Poncelet literature found source
conjectures and adjacent known area/perimeter results, not an exact prior
all-N/arbitrary-M proof. That bounded search cannot certify historical
novelty. No person was contacted and no external code was downloaded or run.

## Budget

Turn1 proved the radial reduction and explored exact remaining coefficients.
Turn2 supplied the full meromorphic proportionality and completed the product
via the credited published theorem. queue.py recorded the first turn in an
isolated faithful single-record runtime; turn2 is recorded as candidate on
freeze. The runtime is local tooling, not a replacement of the shared full
queue. Two substantive turns, one elementary approach followed by a shared
complex-analytic mechanism. No need to consume five turns after full resolution.
