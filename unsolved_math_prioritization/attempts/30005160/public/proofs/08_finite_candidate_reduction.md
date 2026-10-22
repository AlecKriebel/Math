# Proof 08  Finite rational affine candidate lists

This odd-m reduction is retained as optional background. [Proof 29](29_uniform_mass_and_finite_shapes.md) establishes finite rational-affine candidate lists for every prescribed positive noneven exponent.

This is a reading edition of an accepted authored proof. Its mathematical scope is unchanged. Source and reading-edition hashes are recorded in the [inventory](../CONTENT_AND_DEPENDENCIES.md). No novelty claim is made.

Proof dependencies included in this package: [Finiteness at each prescribed noneven exponent](06_fixed_exponent_finiteness.md).

Public analytic inputs and exact attribution are listed in [References](../REFERENCES.md).

Fix an odd positive integer m and an augmented affine rank r. Consider finite configurations Gamma of distinct integer frequencies such that every primitive affine circuit passes the leading-binomial tests for p in (2m,2m+2). Then Gamma belongs, up to rational-affine equivalence, to a finite explicit list.

Indeed, choose the minimum-volume augmented basis B from the proof. Every circuit has mass at most 2m. Every augmented point therefore has its B-coordinate vector in

    G_(m,r) = {x in Q^r: sum_j x_j=1,
                  x_j=-lambda_j/t for every j,
                  1<=t<=2m, lambda_j in Z, |lambda_j|<=2m}.

This finite set has at most 2m(4m+1)^r points and contains the standard basis vectors e_1,...,e_r. The coordinate map is a rational-affine isomorphism from the affine span of Gamma to the hyperplane sum x_j=1 and sends Gamma into G_(m,r). Thus the finite collection of subsets of G_(m,r) that contain the standard basis supplies an explicit, possibly highly redundant list of candidates. If labelled configurations are wanted, add all labellings of these finite subsets by 1,...,N; there are still finitely many after the number of points N is bounded.

One can make every candidate an integer-frequency set: project the sum-one hyperplane onto coordinates x_2,...,x_r and multiply by lcm(1,...,2m). This is an injective rational-affine change and clears every denominator.

The actual strict-majorant property is invariant under these labelled rational-affine changes. One way to see this is to adjoin a common independent uniform phase to all characters: the integer affine relation lattice is then the annihilator of their joint compact-subgroup Haar law. Rational-affine equivalence preserves exactly that relation lattice, so the joint law and every absolute-value norm function coincide. The common phase does not change absolute values. This is the same affine-relation-lattice transfer used in the earlier circuit and block results.

Consequently, for any one prescribed p with odd m=floor(p/2), the classification problem reduces to finitely many explicit rational-affine candidates. This is only a finite candidate reduction. It does not assert an algorithm deciding the universal coefficient inequality for any candidate, nor decidability of the signs of the resulting integrals. It does not supply a corresponding finite-shape claim when m is even; the high-mass line parameters in that case remain unbounded in the proof.
