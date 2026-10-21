# AI-assisted acceptance audit of Fuchs's additive intersection problem

**Review disclosure:** This authored exposition and audit are AI-assisted. There has been no external human review and no formal certification or proof-assistant verification. The word “independent” below describes direct derivation and checking apart from the cited manuscript; it does not mean independent discovery or external human validation.

**Audit date:** 11 October 2026 (UTC).  
**Target:** Hayman–Lingham Problem 7.73; problem 2307073, queue row 1664.  
**Decision:** ACCEPTED, limited to the general-domain assertion that no finite A(R) exists for any R>0.  
**Necessary corrections to the frozen argument:** None found.

## Evidence and meaning of acceptance

The preliminary authored argument was verified against SHA-256
`3c6995b8dbb6e76643f11d1c3da15995f90f2e34eef6b45db52e31aec387d3f5`
(3,015 bytes). The original problem and the relevant manuscript sections were read from the supplied, hash-pinned PDFs and text extractions. The original problem's printed page 183 / PDF page 184 and the manuscript's PDF pages 2, 3, 4, 5, and 10 were visually inspected. The manuscript's title, author names, v1 date, and submission history were checked against its current primary arXiv record.

There are two separate findings:

1. **Manuscript coverage:** He–Tang, arXiv:2603.16676v1, Theorem 1.2 (PDF p. 3) states exactly the general-domain negative conclusion. Section 3 (PDF p. 10) gives the symmetric-puncture obstruction. Its setup is on p. 2 and its needed elementary metric lemmas are on pp. 4–5.
2. **Independent mathematical acceptance:** Every step needed for that conclusion was checked by direct derivation. `PROOF.md` supplies a standalone exposition, including the covering calculation, automorphism derivatives, hyperbolicity and positivity argument, domain-monotonicity direction, full parameter quantifiers, and scaling to every radius. Acceptance is not based merely on the abstract or the existence of a preprint.

This credits an existing result and does not claim a new theorem, independent discovery, peer review, or formal proof-assistant verification. The standard mathematical foundations are universal covering theory, uniformization, Little Picard, and the disk Schwarz lemma; their applications and hypotheses are explicitly identified. No computer experiment is used as proof.

## Hypothesis-by-hypothesis audit

- **Original domain class: PASS.** The printed question admits arbitrary domains contained in the radius-R disk. There is no simple-connectivity or boundary-regularity restriction. Punctured disks are permitted.
- **Radius: PASS.** R is any fixed positive radius. The construction uses points of modulus strictly less than R and does not vary R to force divergence.
- **Domain topology: PASS.** Each disk with one puncture, and the disk with both punctures, is open, nonempty, and path connected. The proof gives an explicit polygonal-path justification.
- **Common evaluation point: PASS.** 0 lies in all constructed domains and is distinct from each puncture because 0<a<1/2.
- **Intersection component: PASS.** The constructed intersection is connected, so its density is unambiguous and equals the density of the component containing 0. No general theorem about connectedness of arbitrary intersections is assumed.
- **Hyperbolicity: PASS.** The bounded domains are hyperbolic. The comparison domain C minus {-1,1} has three excluded points on the sphere, including infinity, and is hyperbolic. Uniformization plus Little Picard supplies an independent justification of the latter fact.
- **Fixed positive constant: PASS.** m is the hyperbolic density of C minus {-1,1} at 0. The universal-cover formula shows 0<m<infinity, with m independent of a and R. No numerical value or asymptotic for m is assumed.
- **Normalization: PASS.** The disk density 1/(1-|z|^2) has curvature -4. The half-plane and punctured-disk calculations use the same normalization throughout. A common positive rescaling cancels in the quotient.
- **Covering formula: PASS.** exp maps the left half-plane onto the punctured unit disk, is unbranched and universal, and has derivative exp. The half-plane density is independently obtained with the Cayley map. This gives exactly 1/(2|z| log(1/|z|)).
- **Automorphism formula: PASS.** For real a, phi_a(z)=(z-a)/(1-az) has phi_a(0)=-a and phi_a'(0)=1-a^2. Replacing a by -a gives the same absolute values. There is no missing factor of two in the sum of densities.
- **Domain monotonicity: PASS.** The intersection is the smaller domain, hence its density is at least that on C minus {-a,a}. The direction is independently proved by lifting to the disk and applying Schwarz's lemma. Only non-strict monotonicity is required.
- **Scaling of the comparison domain: PASS.** C minus {-a,a} is a times C minus {-1,1}, and its density at 0 is m/a, not a times m.
- **Ratio and limit: PASS.** The lower bound is m log(1/a)/(1-a^2), with positive denominator. It diverges as a tends to zero through positive values.
- **Strict inequality: PASS.** For any finite A>0, selecting a<min(1/2,exp(-A/m)) makes the ratio strictly exceed A. There is no unexamined endpoint-attainment issue in this unbounded case.
- **All radii: PASS.** Dilating all three bounded domains by R multiplies all three densities by 1/R. The ratio is unchanged, so no finite A(R) works even for one fixed R>0.
- **No unnecessary dependency: PASS.** Nothing from the simply connected/capacity argument, the sharp lower-bound theorem, or their equality cases enters the proof.

## Credit and current source-status limits

Credit the general-domain theorem and punctured-disk construction to:

Yixin He and Quanyu Tang, *On Fuchs's additive intersection problem for the hyperbolic metric*, arXiv:2603.16676v1, 17 March 2026, Theorem 1.2 and Section 3. [Versioned primary record](https://arxiv.org/abs/2603.16676v1); [current primary record](https://arxiv.org/abs/2603.16676).

The current arXiv record, checked 11 October 2026, showed only v1, submitted 17 March 2026 at 15:41:23 UTC, and no journal-reference field. Two bounded searches, by exact title and by both authors plus “Fuchs journal,” did not identify a primary journal-publication record for this paper. Accordingly it should be described as an arXiv preprint; peer-reviewed publication was not verified. Absence of a journal reference is not proof that no referee has ever considered it. The independent mathematical acceptance above does not change that publication-status distinction.

The original problem is Walter K. Hayman and Eleanor F. Lingham, *Research Problems in Function Theory (New Edition)*, arXiv:1809.07200v2, Problem 7.73, printed p. 183 / PDF p. 184. The primary record identifies v2 as 21 September 2018. [Versioned primary record](https://arxiv.org/abs/1809.07200v2).

**Retrieval limitation retained:** An optional attempt on 11 October 2026 to freshly retrieve both versioned PDF binaries did not succeed because the retrieval route did not provide access. No retry was made. This audit uses the supplied pinned PDFs, their inspected content, prior supplied acquisition metadata, and separately retrieved current web metadata; a fresh byte-for-byte comparison against versioned downloads was not completed and is not claimed. No raw tool logs are included. This limit does not leave a mathematical gap in the reproduced argument.

## Explicit exclusions and preservation

This acceptance does not cover simply connected refinements, their strict endpoint, the sharp lower constant, equality characterizations, the paper's wider capacity claims, or any claim about priority beyond the cited preprint. No source-author software was run. At audit time, no source text, PDFs, or dataset contents were redistributed, and no repository publication or queue edit was performed. Hash checks confirmed that the audited mathematical input, source PDFs, and text extractions remained unchanged. This preservation statement applies only to those identified inputs; whole-directory immutability is not certified. The public packet contains only the authored exposition, authored audit, and public verification metadata; source materials, scripts, and non-public working records are excluded.
