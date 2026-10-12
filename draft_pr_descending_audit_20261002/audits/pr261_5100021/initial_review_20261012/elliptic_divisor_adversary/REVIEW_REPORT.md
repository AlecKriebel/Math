# PR261 / 5100021 — independent elliptic divisor adversary

Verdict: **PASS for the stated noncircular ellipse, strictly nested nondegenerate confocal elliptical caustic, primitive least period N divisible by four, including every allowed star winding.** No proof-level analytic gap or counterexample was found. This is a verification verdict, not a novelty or priority certification. Completion estimate: 100% for this assigned analytic/divisor audit.

## Independence and exposure order

1. At 2026-10-12 09:33 UTC the pre-exposure plan was sealed after reading only the task and the two applicable AGENTS.md files. SHA256: `e01758f43f05db3e6a0988a5a609701894ba0c8ca8ac11c1771287942a90a872`.
2. Then TARGET.json and source_manifest.json were read for the exact original constructions/source locations; their earlier-campaign filenames/hashes were seen, but no earlier-campaign proof was read. The original arXiv PDF definitions and Table 5, and NIST DLMF §§22.4,22.8,22.13, were inspected.
3. The direct line/intersection derivation, complete pole support, explicit local residues, N=4 double-coefficient check, and a product proof using complementary zero/pole supports were saved and sealed at 09:41 UTC **before** candidate PROOF.md or checker exposure. Current SHA256: `bfa2840c3b0933f54de35c6d557b103943cbfa7663c507b8e65408b908dbf1d9`. A typed future time was corrected before candidate exposure; the earlier hash and correction are preserved in RESEARCH_LOG.md.
4. Complete candidate PROOF.md first read at 09:42 UTC. Complete check_exact.py and check_numeric.py were then read at approximately 09:43 UTC. Neither candidate receipts nor earlier reviews, verdicts, or research logs were read at any point.
5. Stachel's published Theorem 4.3 and equation (4.9) were checked directly. The standalone checkers here were written from the sealed independent derivation, after candidate exposure, and do not import any submitted checker or receipt.

No outside individual was contacted. No remote write, branch/ref mutation, queue edit or change outside this assigned folder was performed. The local .venv is ignored and dependencies are pinned for reproducibility.

## Strongest independently verified result

Using t as the chord/contact midpoint parameter, define p=sn(v), q=cn(v), r=dn(v), l=k', s=sn(t), c=cn(t), E=1-k²p²s², B=l²+k²q⁴, C=l²-k²q⁴. Direct original-focus line algebra gives

    pedal Q(t)=((k-s)/(1-ks), l c/(1-ks));
    antipedal R_x(t)=(k r²s²-Bs-kq²)/(q²E);
    antipedal R_y(t)=c(C-kBs)/(l q²E).

The candidate's H is exactly B. Both submitted vertex formulas and the determinant of its actual antipedal line normals match these independently derived expressions. The determinant is 2bpr dn(t)(1+k sn(t))/E and is strictly positive on the real line, establishing finite intersections for the entire real family.

On the valid reduced torus Lambda=<h,4iK'> with h=4K/N=2K/(N/2), the contact-phase pedal trace has only possible simple poles at iK',3iK'. Its double vertex pole cancels because the neighboring difference is odd around K+iK'. The contact-phase antipedal trace has only possible simple poles at h/2+iK',h/2+3iK'. The underlying intersection denominators have **complete** support E=0; dn(t)=0 and 1+k sn(t)=0 are removable, and the common sn/cn poles are removable.

All area traces are even and anti-periodic under 2iK'. Thus each is zero wherever the other has a possible pole. Their product is holomorphic on the compact torus and hence constant. This independently proves the target without assuming a nonzero area, residue, or constant and without dividing by either signed area. The submitted trace proof is consistent with this separate mechanism.

## Local multiplicities and the N=4 challenge

The independent artifact gives explicit residues U_epsilon and W_epsilon of antipedal intersections at epsilon*v+iK' and epsilon*v+2K+iK'. Their two ordinary singular-edge wedge coefficients are

    det(U_-,U_+)=-i B/(l p r q²),
    det(W_-,W_+)=+i B/(l p r q²).

They cancel. Extra adjacent singular pairs occur only when 4v=2K, which primitivity forces to N=4,tau=1. In that case W_-=-U_+ and W_+=-U_-, so both extra wedge coefficients vanish. All four cyclic edges were included. This explicitly validates the candidate's global odd-germ cancellation, including the collision case.

There are no missing residue cancellations in T(w)=sum dn(w+j delta): at iK' precisely j=0,N/2 are singular and each has residue -i, so Res(T)=-2i. At3iK' its residue is +2i. Hence T has exactly two simple poles on Lambda and is nonzero. Evenness and imaginary anti-periodicity place its two distinct simple zeros at h/2+iK',h/2+3iK', proving T(w)T(w+h/2) constant. T is strictly positive on the real line, so that trace product is positive.

## Focus equality, stars, and zero constants

Antipodality exchanges the two original foci. The shift by N/2 is a cyclic relabeling because tau is odd. Applying X->-X to either focus construction preserves every determinant, so the two **same-family areas** agree. No false pointwise same-focus antipodality was used. The actual winding tau and cyclic order are preserved throughout; no convex-only relabeling was substituted.

The proof genuinely needs its allowance for zero antipedal area. An additional exact N=8,tau=1 check provides opposite signs at two admissible moduli:

| k² | Pedal area | Antipedal area | Product |
| --- | --- | --- | --- |
| 175/256 | 27 sqrt(6)/28 | 245 sqrt(6)/864 | 105/64 |
| 20111/20736 | 125 sqrt(30)/459 | -139009 sqrt(30)/162000 | -40885/5832 |

The accompanying checker verifies all original vertices, confocal caustic tangencies, actual specular reflections and original-focus constructions exactly. The antipedal coefficient is continuous between these parameters: real intersections stay finite and the dn trace is positive. Therefore an intermediate admissible parameter has coefficient zero by the intermediate value theorem. At that parameter antipedal signed area and the target constant vanish identically in phase. This deduction uses the independently verified trace proportionality; the sign witnesses themselves use exact geometry, not floating-point signs.

## Validation and limits

- `verify_analytic.py`: PASS, 31,982 exact assertions. These include symbolic original line incidences, focal determinant, independent residues, exact opposite double coefficients and all N=4 extra-edge coefficients. The 6,391 finite primitive period controls through N=500 are sanity checks of universal arithmetic already proved symbolically; they are not a finite substitute for the analytic argument.
- The same standalone program: PASS, 76 families at 90 decimal digits, all primitive windings for N=4,8,12,16,20,28 and k=.0001,.51,.97,.9999. Direct original line intersections and side projections were used. Worst relative real-product discrepancy 1.29e-86; worst complex near-pole discrepancy 2.70e-52. Half-period trace product, both focus equalities, residue limits and pole oddness were also checked. These are noninterval diagnostics only.
- `verify_zero_cases.py`: PASS, exact opposite sign witnesses and the genuine-zero deduction above.
- Standard analytic facts were checked against [NIST DLMF periods/shifts](https://dlmf.nist.gov/22.4), [addition laws](https://dlmf.nist.gov/22.8), and [differential identities](https://dlmf.nist.gov/22.13). Coverage of elliptical-caustic families and primitive winding classes agrees with [Stachel, Theorem 4.3 and (4.9), published p.1614](https://repositum.tuwien.at/bitstream/20.500.12708/136087/1/Stachel-2022-European%20Journal%20of%20Applied%20Mathematics-vor.pdf). Original signed-area and original-focus definitions are in [Reznik–Garcia–Koiller, arXiv v11, pp.3–7](https://arxiv.org/pdf/2004.12497v11).

Exact remaining gap in the assigned analytic review: **none**. This verdict does not extend to degenerate or hyperbolic caustics, k=0 or1 endpoints, repeated lower-period traversals, unsigned lobe areas, outer/inner constructions, or novelty assessment. Source/novelty audit and repository-level promotion are parent responsibilities.
