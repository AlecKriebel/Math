# PR255 / 5100022 / k404: independent meromorphic adversarial review

**Verdict: PASS for the exact claimed mathematical theorem. No actionable mathematical finding and no remaining proof gap were found in this review family. Estimated completion: 100% of the assigned mathematical audit, not of publication or historical priority clearance.**

Reviewed source PROOF.md SHA256:

    b8edd78d03dac33a7be77837649eef7a8558900b3499774725174836fa54d462

The frozen proof is 14,220 bytes. It was read in full before author checkers or any prior/new reviewer report. The source target was checked against both rendered Table 5 pages and the surrounding primary definitions. The review applies to signed area of the **original orbit's** focal antipedal divided by the **original side-line** focal pedal, primitive least period N=2 modulo 4, all allowed primitive star classes, both original foci, and strict noncircular, nondegenerate confocal elliptical caustics.

## Strongest independently verified result

The all-period claim follows from the independently reconstructed meromorphic proof in INDEPENDENT_DERIVATION.md, with algebra/Laurent certificates in fresh_meromorphic_checks.py. It establishes:

1. Every real focal antipedal intersection is finite.
2. The original focal antipedal area B(w) has the correct elliptic lattice <h,4iK'>, character under 2iK', and at most two simple poles on that torus.
3. The comparison trace S(w)=sum dn(w+j delta) has nonzero residue -2i at iK'. Exactly two original summands contribute there, with equal signs.
4. Matching residues and the shared anti-period proves B(w)=bS(w), including b=0.
5. The original focal pedal area equals p0S(w) for the requested primitive parity, with p0>0.
6. Hence the literal target quotient is defined and constant at every real phase, with the same constant at the two foci.

This is an analytic proof for arbitrary admissible N, not an extrapolation from numerical samples.

## Distinct independent mechanism and certificates

I independently rationalized the antipedal formula in the imaginary-shift chart u=iK'+x. Its only denominator is sn²(x)-sn²(v). I computed the residue vectors R+,R- at x=+/-v and those of their central translates. The two adjacent singular edge pairs have opposite double Laurent coefficients:

    det(R-,R+)+det(-R+,-R-)=0.

This provides a direct local cancellation certificate independent of merely restating the submitted odd-Laurent symmetry argument. I also independently checked the latter argument and its reflection/traversal signs.

For the focal pedal, I derived the quarter-period Laurent chart, its leading double-pole vector (2/k)(1,i), the absence of a simple-pole vector term, and the incident-edge residue. This gives the explicit positive coefficient

    p0=b0² sn(delta)[dn(delta)-k² cn(delta)-b0²]/
       [k²(cn(delta)-dn(delta))²].

The exact identity

    dn²(delta)-(k² cn(delta)+b0²)²
      =k²b0²(1-cn(delta))²

proves its numerator factor is positive for every strict real 0<delta<2K. This is a second proof of the nonzero denominator independent of the submitted lifted-normal positivity argument. The latter also checks out.

## Adversarial checks and resolutions

| Potential failure | Independent resolution |
|---|---|
| Wrong antipedal object or outer-polygon substitution | Both actual focal line equations are exact-certified; both primary table editions and definitions match. |
| False real intersection finiteness for stars | The exact focal-ray determinant has only strictly positive real factors, including 1+k sn u and L. |
| Treating U itself as elliptic on too small a lattice | Pole counting uses the scalar L on <2K,2iK'>; complete area sums descend to <h,4iK'>. The function/divisor distinction is made explicitly. |
| Missing poles at common sn/cn/dn poles | Their numerator and denominator orders give removable singularities; all nonremovable possibilities are counted by L's two-zero divisor. |
| Coincident or multiple L zeros | 0<v<K gives distinct +/-v classes; sn'(+/-v)=CD!=0 gives simple zeros. |
| Hidden double area poles | Direct residue-pair cancellation is certified; global oddness supplies a second argument. |
| Incorrect reflection or focus-swap sign | Central inversion relabels the even orbit; y-reflection reverses its index and area sign twice; imaginary reflection negates area once. |
| Zero comparison residue | The only contributing indices are j=0,m, and dn's real 2K period makes both residues -i. |
| Missing additive constant after residue matching | The holomorphic difference is constant on the compact torus; its nontrivial imaginary anti-period forces zero. |
| Importing a related pedal theorem without domain checks | The actual focal foot, its poles and residue, and its positive coefficient are reproduced directly. |
| Pedal double poles multiplying each other | Adjacent poles cannot coincide because 0<delta<2K; the quarter chart is even and the incident neighbor difference is odd. |
| Erasing the primitive parity | K+v is an integer multiple of h exactly when m,tau are odd. The stated result does not extend this alignment to N divisible by four. |
| Denominator vanishing on highly winding stars | The explicit p0>0 and S(real)>0 prove all-phase positivity; direct high precision controls include near-maximal allowed winding. |
| Extending singular boundary cases by continuity | k=0, k=1, v=0, and v=K remain excluded. No circular, hyperbolic, or degenerate claim is accepted here. |
| Confusing numerical agreement with proof | The report and verifier label diagnostics separately; the all-N proof is the meromorphic derivation. |

## Reproduction results

The fresh verifier has no campaign-code imports. Final run: **PASS**.

- 25 exact symbolic controls, including both defining line equations, original chord tangency, direct projection, residue-vector pairing, paired double-pole cancellation, quarter-chart Laurent coefficients and derivatives, trace coefficient and sign identity.
- 2,275 exact finite primitive-parity arithmetic families, N=6 through 298. These test the generic integer argument but are not its proof.
- 39 independently generated real/complex diagnostic families at 90 decimal digits, with N in {6,10,14,18,22,26,50}, simple and highly winding primitive classes, and k in {0.02,0.71,0.999999}.
- Each family has three real phases and one complex phase. Both focus areas, the explicit p0 coefficient, trace proportionality, and target ratio were checked using actual line intersections and actual perpendicular projection formulas.
- Six additional near-complex-pole cases for (N,tau)=(6,1),(14,5),(26,11), at epsilon=1e-4 and 1e-7, verify pole oddness, trace agreement, and both area anti-periods.
- The final maximum scaled numerical discrepancy is **2.93265196296804787e-69**, including near-pole ill conditioning, below the stated 1e-65 tolerance. The initial non-pole matrix alone had discrepancy 1.25747027857108722e-83. Both run receipts are retained, and neither is presented as an exact proof.

FRESH_CHECK_RESULTS.json is the final complete receipt; run_02.stdout.txt and run_02.stderr.txt preserve its execution. The exact runtime used was the supplied Python environment with SymPy and mpmath. The derivation and script are portable and impose no Git or network mutation.

## Source checks, attribution, and bounded scope

Primary DLMF Tables 22.4.1–3 and addition equations 22.8.1–3 confirm the actual periods, pole/zero locations, quarter-period charts, and addition signs. Stachel's published Theorem 4.3 and equation (4.9) match the canonical coordinates and primitive rotation step. The rendered arXiv v11 and published Table 5 pages both show k404 as the focal antipedal/pedal ratio with N=2 modulo 4. Primary equation (1) specifies signed area.

Stachel's printed claim that dn changes sign under a real 2K shift is a source typo. The submitted proof uses the correct real 2K period, independently confirmed in DLMF. This discrepancy is not a defect in the present proof; the preprint should continue citing DLMF for function characters.

The canonical coordinates, compact-torus residue uniqueness argument, and earlier campaign pedal-trace mechanism remain credited inputs. My explicit p0 and residue certificates are verification artifacts, not claims of mathematical priority. I have not performed the root's separate extensive historical priority audit or the later publication-package reviews. Passing this mathematical review does not itself clear those stages.

No submitted source file was changed. No prior/new reviewer report was read before reaching the independent derivation. After that derivation I read the author checker to confirm that its stated construction and separation of algebra from floating diagnostics are consistent; I did not rely on it to establish the theorem. All owned artifacts and source pins are recorded in FROZEN_HASHES.json.
