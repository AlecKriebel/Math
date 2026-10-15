# Independent source, credit and priority alignment audit

UTC 2026-10-13. The mathematical conclusion in INDEPENDENT_DERIVATION.md was reached first, without consulting the earlier PR254 audit verdicts. This source audit then challenged the frozen note's claims against primary definitions, actual predecessor statements and the included priority reports.

## Source invariant and canonical input

I independently hashed the original local primary reading PDFs against the distributed provenance pins:

| Source | Independently confirmed SHA256 | Checked content |
| --- | --- | --- |
| Reznik–Garcia–Koiller, arXiv:2004.12497v11 | c56bb4ea29734ed04ee153206bb8619286df544714fd3f77fe97bdc945dfe1da | Table 5, printed p. 7, visually inspected; odd N, center O, unprimed pedal times unprimed antipedal, proof unknown. |
| Published Fifty New Invariants | c2a2e644521fd03a15833a23bd57c2498b5644036f6bc8fe682c40581f640d42 | Signed area definition, original-side foot definition in §3.3, original antipedal definition in §3.5, and Table 5 printed p. 348 visually inspected. |
| Stachel, On the Motion of Billiards in Ellipses | 9121028d7295435740cebb25ec60abe1a0dcc4e96686c226b1b6533bd49515d8 | Published Theorem 4.3 and (4.9), printed p. 1614, visually inspected with the complete surrounding derivation. |

Primary URLs: [RGK v11](https://arxiv.org/pdf/2004.12497v11), [published RGK](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf), [Stachel](https://doi.org/10.1007/s40879-021-00524-2).

The note identifies the right unprimed polygons, not outer tangents or caustic-contact polygons. Its signed-area convention agrees with the published source and the explicit self-crossing antipedal footnote. The bibliography gives the exact authenticated v11 PDF title, Eighty New Invariants in the Elliptic Billiard. The arXiv landing-page title includes of N-Periodics, but this does not warrant changing the correct PDF-title citation.

Stachel explicitly uses the caustic numerical eccentricity as modulus and includes coprime turning number tau. His symbol m means k in the note; mpmath's parameter is k^2. The note's formulas correctly maintain that distinction. An earlier displayed real-shift line in the Stachel reading text gives an erroneous sign for dn; the note uses the correct dn(z+2K)=dn(z), independently confirmed by DLMF. The canonical theorem itself is accurately transcribed and provides actual reflected trajectories, not merely inscribed tangent polygons.

## Jacobi, cyclic and prior pedal methods

I directly reopened [DLMF 22.4](https://dlmf.nist.gov/22.4), including Tables 22.4.1–3, and [DLMF 22.8](https://dlmf.nist.gov/22.8), including (22.8.1–3). The shifts, simple pole/zero classes, p-shift chart and addition formulas in the note agree. The current DLMF page identifies version 1.2.8, release 2026-09-15; access was 2026-10-13 UTC, consistent with the bibliography. Section 22.9 is an appropriately cited background cyclic-identity source; its formulas are not required to fill a proof gap here.

I fetched the actual KLS and Landen primary PDFs independently. Their hashes match the older classical audit's reading-copy pins:

- [Khare–Lakshminarayan–Sukhatme, Cyclic Identities II, v2](https://arxiv.org/pdf/math-ph/0207019v2), SHA256 c9977e124bfdbf34030eb1b4fbb0d1f2a51827b65c823b5670ea70a435d25a66. Section 2.1.1, (17)–(20), supplies the dn archetypal sum and reductions through the aggregate principal parts; the simple-pole character is established prior technique.
- [Khare–Sukhatme, Generalized Landen Transformation Formulas, v1](https://arxiv.org/pdf/math-ph/0312074v1), SHA256 d3b24f90d25347818874415e571d965b1c92a54f36c4a6202b8bd2bc9767ad2b. Equations (13)–(15) give the uniformly shifted dn trace as a rescaled transformed-modulus dn. The note cites the correct equations and 2003 version date. It does not depend on adopting that transformed-modulus formula or claim to discover it.

The direct immutable [PR204 proof](https://raw.githubusercontent.com/AlecKriebel/Math/551a524e2db65fec90684485ef676d0b4179378d/unsolved_math_prioritization/attempts/5100012/PROOF.md) is 11,083 bytes with SHA256 d1e04cf42d4358243365969487348887f3451f9b3fcef63b5215e7389af0e039, matching the included public source pins. I read the full document. Its origin-pedal two-pole cancellation, trace uniqueness and half-shift mechanism are precisely the mechanism explicitly credited and restated in the note. Its target is original-area times origin-pedal area, including odd periods; it does not include an origin-antipedal theorem. The preserved candidate/pending-review label in that immutable historical proof is not a claim of human peer review or a contradiction of its later campaign review status. The current note calls the present work unrefereed.

I also directly inspected [Akopyan–Schwartz–Tabachnikov](https://arxiv.org/pdf/2001.02934), including the odd original/outer-tangent area ratio (Theorem 3 in that arXiv version) and the complete final proof section. It is genuine prior complex/grid technique. Its actual tangent line at P is (P_x/a^2,P_y/b^2) dot X=1; the present antipedal line is P dot X=P dot P. They cannot be equated by simply reusing the named area functional. For example at a=2,b=1,P=(6/5,4/5), their normal determinant is -18/25. The supplied construction checkset independently confirms this and the inverse-ellipse quartic. A different proved bridge could in principle matter; no such bridge is supplied by the checked predecessor theorem.

## Fresh challenge to the adjacent focal product

The strongest contemporary covering route is an earlier all-odd theorem A*_O=r A, combined with the already credited PR204 constant A A_O. It would cover this target even under another code or title. The note's priority claim must therefore not be based only on searching k403,a literally.

I independently reopened [Ferudun's Focal Pedal-Antipedal Area Products](https://eulersolve.org/papers/amr-050-0021/paper.pdf?v=34ff068237a7), especially the construction definitions, equation (16), Lemma 4 and its complete opposite-edge proof. Lemma 4 is broader than the title's N divisible by four statement, but requires centrally paired vertices and a fixed focus. An odd primitive set on the nondegenerate ellipse cannot be centrally paired, since origin negation has no fixed ellipse vertex and partitions such a set into pairs. Setting focal displacement to zero makes the ellipse circular, not an arbitrary noncircular origin case. These are substantive failed hypotheses, not just a code mismatch.

Equation (16) in that neighboring paper is the same elementary generic antipedal edge-area expression as F after translating its focus. Thus F by itself must not be advertised as a new general formula. The current note makes no such claim: it identifies the additional step as the construction-specific divisor analysis, especially the distinct opposition pole and odd real-lattice alignment, and expressly disclaims method/invariant novelty. This observation does not block the stated theorem or its current framing. Citing the nearby focal result as additional related work would be optional, not a repair of an originality claim the note actually makes.

## Bounded search and included audit alignment

Fresh object-based searches used k403,a; pedal plus antipedal plus area plus elliptic billiard; pedal-antipedal invariant; AMR-050-0020; and origin-antipedal odd area-ratio variants. I relied on primary papers for mathematical scope, not search snippets. These searches rediscovered the source table, AST, triangle-only formulas, the contemporary EulerSolve catalogue and the neighboring focal result, but no earlier covering odd-original-origin theorem. Direct access to EulerSolve AMR-050-0020 failed, as it did in the recorded earlier audit; that failure is not absence evidence.

After recording the independent mathematical conclusion, I read the complete included geometric and meromorphic reports, classical and recent priority reports, root mathematical and priority acceptance, route notes and source-pin ledgers. The historical reports bind the original proof hash ff2b1d78a1b94997d366d5173243ea95b949d5ae24574471639740b35cf2c16e; they do not purport to bind the later TeX hash. The note reproduces the same theorem and the originally required opposition/N3/pedal-cancellation details. Its new KLS/Landen references meet the classical audit's credit recommendation.

The current note says bounded audits found no earlier covering proof, without certifying historical firstness. The included authored reports substantiate that limited statement and explicitly acknowledge their query bounds, access failures, original versus revised records, and the distinction between recorded chronology and certified causal discovery. The metadata repeats that bounded framing. Neither a search no-result nor a prior PASS flag was used as the universal mathematical proof.

No worldwide-firstness or exhaustive-current-openness certificate is produced by this review. Such a certificate is neither claimed nor needed for the carefully credited result. An authenticated earlier all-odd origin-antipedal/original-area relation would reopen the priority assessment. I found no current source or framing correction required. Whole third-party PDFs, extracted source text and rendered source pages used for reading are removed from this owned review's final authored evidence; URL/byte/hash pins remain.
