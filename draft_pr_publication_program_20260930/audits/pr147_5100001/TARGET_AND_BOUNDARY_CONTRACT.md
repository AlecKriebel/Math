# Exact claim, boundary cases and acceptance conditions for PR147

Original PR: https://github.com/AlecKriebel/Math/pull/147
Original immutable head: 502de2f863a63ca205814da4194411847797a7c3.
Original QUEUE status: claimed_solved; author effort:2/5 (two recorded approaches).
Problem5100001 / AMR-050-0001: the literal printed k107 assertion.

The assertion is universal: for every noncircular ellipse and every fixed confocal elliptical caustic giving a Poncelet N-periodic billiard family with N divisible by4, K=(A'/A) product sin(theta_i/2) is constant over that family. Here P' is formed from consecutive tangent intersections at the original orbit vertices on the outer ellipse, A and A' are signed shoelace areas, and theta_i are the original polygon's internal angles. The source Table2 gives k103=A'/A and k105=product sin(theta_i/2), then k107=k103*k105 with an unproved mark at N=0mod4. ROOT read the primary definitions and inspected both complete rendered table pages, arXivv11 p5 and journal p345.

Success by counterexample requires two actual primitive four-period trajectories in one continuous fixed-caustic family, with all objects finite and unambiguous and different exact values of K. A repeated orbit, changed caustic, changed reflection convention, self-intersection/zero area, outer-tangent singularity, angle-sign trick, or numerical approximation alone would not suffice.

For a=4,b=3 the submitted diamond and rectangle meet these requirements under ROOT's initial analytic review. The family map with Delta=sqrt(a^4 sin²t+b^4 cos²t) connects them, has T²=-id and positive cross product. Its denominator never vanishes since a>b>0. The caustic has squared semiaxes256/25 and81/25, so lambda=144/25 is strictly between0 and b²=9. ROOT independently checked the support and physical normal-projection identities in the mathematical proof. The returned exact values288/625 and625/1152 differ by58849/720000. Independent preparatory reviewers must still close their complete reports before the mathematics gate.

Boundary cases: a=b gives the circular coincidence K=1/2 and is excluded by the source a>b>0. For every b>0 the ellipse and caustic remain nonsingular; the limit b->0 is outside the admissible nondegenerate hypotheses. Scaling both axes does not change the dimensionless quantity. The ordinary internal angles lie strictly in(0,pi), hence each half-angle sine is positive; reversing both polygon orders changes both signed areas together and leaves the ratio unchanged. Primitive N=4 is permitted by the printed parity entry; no N>4 restriction appears there.

This audit does not substitute a quotient for the printed product, claim a corrected identity at all periods, or establish historical priority merely from verifying the mathematics. A period-four quotient identity can be explained as a diagnostic if independently proved and credited appropriately, but is not needed to refute the literal universal assertion.

Verification guards in the submitted scripts relied on Python assertions. ROOT reproduced both original receipts byte-for-byte in normal Python and observed a deliberately false checker accepted under -O. The candidate repair changes only these guards to explicit RuntimeError conditions and preserves every calculation, case and receipt. Repaired normal/-O runs and deliberate wrong-value rejection both pass. Frozen originals are unchanged.

The next gate is a bounded primary-source priority audit after independent mathematical acceptance. No paper, new Zenodo record, tracker row, PR merge or native status promotion is authorized by this preliminary checkpoint alone. The persistent user goal remains ACTIVE.
