# Source-first independent analytical baseline

UTC seal time: 2026-10-03T22:01:56.518962+00:00
Candidate access at this checkpoint: none. No sibling analysis, candidate proof, candidate program, or candidate verdict has been consulted.

## Exact source claim and scope
The Keller contribution in OWR 49/2009, pp. 2713–2715, credits Bardet–Keller–Zweimüller, Communications in Mathematical Physics 292 (2009), 237–270. Its conjecture is W0 = boundary_D(W+) = boundary_D(W−), where D is all nonnegative probability densities on X=[−1/2,1/2] in relative L1 topology, W0 is attraction to 1, and W± are attraction to u_(±r*). Parameters are 0<A<=2/5, 6<B<=16, G(m)=A tanh(Bm/A). It is not the distinct BKZ finite-system limiting-mixture conjecture alpha=1/2. The public report's known density of W+ union W− does not alone imply both basins touch every W0 point.

## Independently reconstructed equations
Let f_r(x)=((r+4)x+r+1)/(2rx+2), and alpha_r=−r/4. The two increasing full branches of T_r are f_r and f_r−1. Their inverses on X are
b_−(r,y)=(2y−r−1)/(r+4−2ry),
b_+(r,y)=(2y+1−r)/(4−r−2ry).
Each derivative in y equals 2(4−r²)/its denominator²; f'_r(x)=(4−r²)/(2(1+rx)²). Therefore P_r u(y)=u(b_−)b'_−+u(b_+)b'_+. The exact minimum branch expansion is 2(2−|r|)/(2+|r|), at least4/3 on |r|<=2/5. Differentiating an inverse and composing with its forward branch gives (4x²−1)/(4−r²), with negative interior sign. This sign must not be confused with forward sensitivity (1−4x²)/(4−r²).

On mixture densities w_y(x)=(1−y²/4)/(1−xy)², the induced dual branches and weights are
sigma_r(y)=2(y+r)/((r+1)y+r+4),
tau_r(y)=2(y+r)/((r−1)y−r+4),
p_r(y)=1/2−(r+y)/(4+ry).
Their common zero is −r, and their equal derivative there is2/(4−r²). On Y=[−2/3,2/3] and |r|<=2/5 they preserve Y and have derivative<=3/4. BKZ proves the boundary claim for W0 intersect the mixture class D0, whereas extension to every L1 density is the remaining original gap. D0 is highly regular; derivative/variation estimates proved for it do not automatically apply to arbitrary D.

## Prior results that must be credited and not assumed stronger
BKZ's full argument includes finite system expansion, the mixture IFS, strict order, contraction of support intervals near the zero, shadowing by mixture densities, convergence of arbitrary D, openness and Lyapunov stability of W±, and common-boundary contact on W0 intersect D0. Section5.3 expressly limits strong differentiability to C2 densities (BV to L1); using a stable-manifold theorem directly in L1 or at arbitrary rough densities requires justification. The paper's generic assumptions I and II include G'(m)<=25−50|G(m)| and S-shapedness of H(r)=G(phi(u_r)). The source tanh example uses B<=18, but the OWR conjecture asks B<=16. The arXiv item is0812.4040v1; variant typography/compilation date must not substitute for the cited 2009 article identity.

## Falsifiable audit plan
1. Derive candidate Möbius identities independently, especially parameter derivatives, moving branch effects, Jacobian cancellation, and mass preservation.
2. A finite parameter grid cannot certify uniform bounds. Any rational rectangle certificate needs domain coverage, positivity of denominators, correct derivative monotonicity or interval enclosure, and explicit handling of excluded endpoint/limit sets.
3. Test A tending to0, B approaching6 from above, B=16, r=0, and tanh saturation. No uniform Lipschitz constant for G'' follows from B<=16: its scale grows as1/A. Constants depending on a fixed A are acceptable if the theorem fixes A; a universal constant requires proof.
4. Differentiate fixed-point response carefully: H'(0)=B/6 but the nonlinear PFO's unstable eigenvalue at1 is1/2+B/12. These are distinct.
5. Verify exact claims using Fraction or available SymPy. Floating samples are empirical controls only. Replay every candidate program without changing original bytes and compare complete native stdout to saved receipts. A successful replay is no analytic proof.
6. If a route replaces the basin-boundary claim by an unsupported lifting/openness/contraction assertion of comparable difficulty, record it blocked with its exact gap.

## Status at source-first checkpoint
Mechanism: primary-source reconstruction plus independent exact branch inversion. Evidence: credited primary equations, full BKZ logical sections read, arXiv variant cross-check in progress. Strongest verified result: exact original target, inverse formulas, sensitivity sign, parameter regime, and distinction from limiting-mixture conjecture. Remaining work: all candidate comparison, native reproduction, controls and integrity checks. Best-guess completion of this audit:15%; no estimate of discovery completion is asserted.

Primary URLs: https://ems.press/content/serial-article-files/46250 ; https://mat.univie.ac.at/~zweimueller/MyPub/bkz.pdf ; https://arxiv.org/abs/0812.4040
