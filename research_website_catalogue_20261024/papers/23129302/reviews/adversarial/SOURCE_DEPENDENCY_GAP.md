# Exact source-statement versus proof-coverage distinction

This finding concerns validation of an external mathematical dependency. It is not a counterexample to the submitted theorem, and no repair was attempted.

## A. Exact unconditional published assertion exists

Keller's [OWR contribution, primary publisher body](https://ems.press/content/serial-article-files/46250), printed p.2714, Theorem2, unconditionally states the three-fixed-point, all-density L1 convergence and open noncentral basins result for precisely 0<A<=0.4, 6<B<=16. The full density space and the formulas for T and tanh feedback are specified on that page. The next page states the common-boundary conjecture. I read the whole contribution pp.2713–2715 and visually verified pp.2714–2715.

Accordingly, it is correct to say that the exact global assertion is an independently citable published theorem **statement**. There is no discovered range mismatch or smooth-density restriction in that statement. The OWR contribution gives no detailed proof; it credits the 2009 BKZ journal paper.

## B. The inspected detailed proofs have an additional hypothesis whose specialization is numerical

Both independently downloaded [BKZ arXiv:0812.4040v1](https://arxiv.org/pdf/0812.4040v1) and [BKZ author manuscript](https://mat.univie.ac.at/~zweimueller/MyPub/bkz.pdf) contain:

- §2.2: G is odd, increasing, real analytic and strictly concave on the positive half of its field domain.
- AssumptionI, (2.8): G'(x)<=25−50|G(x)|.
- §2.5, AssumptionII, (2.12): H(r)=G(phi(u_r)) is S-shaped. The authors explicitly say S-shape of G does not itself suffice. They explain that II is used through the fixed-point dichotomy for H.
- Theorem2, p.8: all-D L1 convergence and basin assertions **assuming I and II**. Example1 on that page asserts that tanh with 0<A<=0.4, 0<=B<=18 satisfies the assumptions and hence both theorems apply.
- AppendixA.2, p.35: the inequalities for psi(r)=phi(u_r), including psi(r)>=r/6 and psi''/(psi')^2<=(189/5)r on [0,0.4], are justified by numerical evidence and plots. The tanh specialization of the displayed sufficient conditions is then described as numerically checkable. No validated interval enclosure, remainder-controlled analytic inequality, or exact uniform parameter proof of this step was found in these bodies.

The tanh odd/increasing/concave hypotheses are immediate for the target range. AssumptionI also has an exact elementary verification here: with a=|G(x)| and g=G'(x), g<=16−100a^2, and

    (25−50a)−(16−100a^2)=100(a−1/4)^2+11/4>0.

This does not certify AssumptionII or the sufficient fixed-point dichotomy. The new paper's rigorous inverse-contraction polynomial solves a different estimate.

The final journal proof was not obtained. A bounded direct publisher-PDF request returned HTTP200 but delivered HTML with no proof text; its file signature was rejected and a receipt retained. It was never treated as a PDF or as evidence of the final proof. The accessible versions and final journal version have not been silently identified. It is unknown here whether the final journal supplies a stronger, rigorous specialization proof.

## C. Current submitted packet does not close this point

The entire current paper and TeX were read, together with the author SOURCE_SCOPE, SOURCE_ADDITION_T3, FINAL_RESULT, README and the relevant algebra/topology/backward programs. The packet imports the global result and seed; it does not give an exact uniform proof of II. Its exact interval/Bernstein and sharper polynomial certificates concern the self-consistent inverse norm, its rational identities concern the maps, kernels and AssumptionI, and its rough-density controls concern transport. None verifies H-shape or the required fixed-point dichotomy over the full rectangle. Searching all distributed Python, JSON, TeX and CSV files for the shape/AssumptionII/curvature terms yielded no such certificate. No historical/current review opinion was used to reach this finding.

## D. Strongest conclusion warranted by this adversarial review

The new all-density proof mechanisms withstand independent reconstruction. Without accepting the unconditionally stated external global theorem as a black-box import, this lane verifies F is an open continuous surjection on all D and

    union_n F^(-n)({1}) subset W subset closure_D(union_n F^(-n)({1})).

The second inclusion is the substantive arbitrary-integrable-density backward approximation, not merely an analytic-core or positive-density result. W's closedness is not established just by the definition of a basin. The submitted equality and both boundary identities additionally use the imported global partition/open-basins theorem and the boundary seed. The seed is proved in inspected BKZ Proposition4 on the invariant analytic class (which contains1), with the same source assumptions in force.

Accepting the exact OWR assertion as an established theorem gives a valid conditional deduction of the full submitted result. A claim of a fully independently certified unconditional proof across the entire rectangle remains unwarranted in this lane until the source-specialization proof is supplied or independently checked. This is a material external-dependency **proof-validation gap**, not a demonstrated false parameter, a false OWR quotation, or an internal flaw in the new transport proof.
