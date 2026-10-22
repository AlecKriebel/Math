# Independent physical/geometry audit outcome

2026-10-16 16:03:17 UTC. Planned independent reproduction audit: complete (100%). Best-guess progress toward an independent universal proof by this family's mechanism: 30%; the global sum identity remains open.

## Verdict and strongest verified result

No counterexample to the odd-period focal complete-line-distance product was found in independent physical propagation. This family has **not proved** universal invariance. It independently establishes exact local geometry, exact single-orbit calibrations, and a finite high-precision reproduction with meaningful negative controls. It does not promote PR205 or make a priority claim.

The exact geometric results are q+,i q−,i=beta² for every caustic tangent, q+,i−1 q+,i=beta² d+,i/d−,i at each specular bounce, and the reversal/repetition/scaling rules. An independently derived isosceles three-period configuration a=sqrt(2),b=1 has alpha=sqrt(2)(sqrt(3)-1), beta=2-sqrt(3), and I=3. An exact four-period diamond at a=2,b=1 has I=12.8. Full derivations and the precise blocked route are in geometry_findings.md.

## Mechanism and independence

Plan and attack cases were frozen in research_log.md at 2026-10-16 15:54:41 UTC, before reading any submitted proof/checker/review/other-family report. After freezing, only the parent-named published primary source was opened to confirm the Table7/§3.7 distance semantics. No Stachel canonical closing formula, Jacobi orbit formula, submitted PR205 artifact, checker, review, or other family report was read or used.

Every closing pair was selected by bisection on accumulated ordinary ellipse angle under Euclidean physical reflection. The initial caustic tangent is obtained by affine scaling and elementary circle tangency. Propagation uses the forward root of the line/outer-ellipse quadratic and reflection about the gradient normal. No point is projected back onto either conic. Every support distance is computed from the original propagated chord by a Euclidean cross product, and every orbit must pass closure, winding, tangency, reconstructed reflection, boundary, focal-product, and optical-identity checks. Primitive periods are independently checked against all shorter return lengths. Repetitions skip only the primitive-period rejection; they retain all geometric residual checks.

## Coverage and receipts

Three full runs used Python3.14.6 and read-only mpmath1.3.0 with -E -S -B -P: ordinary90 requested/140 working digits, optimized(-O)90/140 digits, and ordinary130/180 digits. A fifty-digit guard addresses cancellation when beta is tiny. No package installation/copying or bytecode writes occurred.

Each run used54 configurations:34 odd and20 even. Aspect ratios:1.0001,1.1,2,10,100. For each ratio the selected odd N=3,5,7 cover EVERY coprime winding0<m<N/2. The even controls are N4,m1;N6,m1;N8,m1,m3. Four additional odd cases use N31,m1 and N101,m1 at aspect ratios1.0001 and2. The smallest lambda/b²≈.00096729815 probes a caustic close to the outer ellipse; the smallest beta/b≈3.12539066e-14 probes a near-degenerate caustic.

Eight phases and two directions give864 primitive traversals. Independently propagated repetitions r3 andr5 add108, giving972 core trajectories per run. Five exact/scaling calibrations add5. Across the three final full runs:2931 valid trajectories. Invalid negative-control trajectories are excluded from that count.

Normal and optimized receipts are byte-for-byte equivalent after removing the timestamp. All54 invariant values agree to the32 printed significant digits at the higher precision. Final high-precision maximum odd I relative spread is2.51422e-150; maximum repetition relative error is8.15180e-154. These are finite NONINTERVAL diagnostics, not certified error bounds.

At180 working digits, worst residuals are:

| Check | Maximum |
|---|---:|
| position/direction closure |3.85924e-150|
| winding lift |5.19051e-152|
| caustic tangency |3.25275e-180|
| reconstructed specular reflection |3.50718e-178|
| outer boundary |4.81984e-180|
| focal local product |3.49369e-180|
| optical adjacent identity |1.55997e-176|

Closure is max(position discrepancy/a,direction discrepancy). Tangency, focal-product, and optical residuals are normalized by a²; boundary, specular, and winding residuals are dimensionless. These normalizations and full receipts are specified in physical_audit.py.

## Falsification and calibration controls

Explicit guards reject four nonfinite/improper geometries, a deliberately rotated reflection, and a deliberately wrong caustic. No bare assert controls correctness. Code was rerun under -O.

EvenN4 at a2,b1 has target I relative spread .3584469568, so the procedure does not manufacture invariance for every closed orbit. In the oddN3,a2,b1 family, replacing complete-line distances with segment distances gives relative spread .2386912678, while vertex-distance products give .0452682823. The semantic controls distinguish the specified target.

The exactI=3 triangle andI=12.8 diamond pass to relative errors1.60662e-181 and4.51860e-181. Scaling all axes by1e-20 and1e20 gives relative I/k² discrepancies below3.86e-178.

An early90-WORKING-digit run correctly failed closed in the extreme a100,N7,m3 reversed orbit:2.23518e-60 closure residual exceeded the original1e-65 threshold. This failure was not suppressed or treated as a mathematical counterexample. Fifty additional working digits were added while retaining the requested-precision tolerance, and the180-working-digit full run independently confirmed convergence. See the research log.

## Adversarial self-review and exact remaining gap

The physical checker never assumes closure, caustic preservation, primitive period, the target invariant, or its intended parity. Closure shooting alone is insufficient; all trajectories are separately checked. The target is evaluated only after these geometric checks. Wrong semantics and even-period controls are required to vary, which guards against a checker that merely returns an input-dependent constant.

The local q+q− lemma does not establish the global sum product. Solving the odd optical cyclic relations only rewrites the same difficulty in vertex-distance variables. That local-elimination route is blocked until a new global identity or mechanism is supplied. Finite noninterval numerical checks, even with repeatable precision convergence and adversarial controls, cannot quantify over all confocal pairs, starting phases, periods, and coprime winding classes.

No Git/index/ref/service writes, promotion, releases, or external human communication occurred. All created artifacts are inside the assigned family folder.

## Reproduction

Use the Python executable and flags above to run physical_audit.py90 physical_receipt.json, physical_audit.py90 physical_receipt_optimized.json under-O, and physical_audit.py130 physical_receipt_high_precision.json. Then run compare_receipts.py. The script refuses receipt destinations outside its own folder and imports the preexisting read-only sibling runtime. Exact shell invocations are preserved in the research log below.
