# Independent review of the configuration-dependent Yamabe-cone partial

**Verdict: PASS_SCOPED_LOW_POINT_TOPOLOGY_AND_INERTIA_OBSTRUCTION. No mandatory mathematical correction.** The fixed-fiber descriptions, global p<=3 products, genuine four-point inertia change and credited p<=5 boundary consequence are correct in their declared scopes. The general total-space/relative-pair topology remains **unsolved, 2/5 approaches**.

Reviewed on 2026-09-30 by a separate GPT-6 Astra agent at xhigh reasoning. This is an independent adversarial AI audit, not human peer review or a priority certificate.

## 1. Frozen object and exact source scope

The reviewed `PARTIAL.md` has SHA-256
`60f6266dec816b00f7b4bf30f7e78cd1329d46313cbd669950198603aea591bd`.
The submitted verifier and receipt hashes are respectively
`69d0866e2211f0084ab1102063bc701004968c721cb9e0ca11975d7dd9bea5c9` and
`959814f0dca69c9c50359464cd4cdf0406e9e3ded94ae754ae6ddb860f0f2e6b`.

I read the complete contribution in [OWR 29/2005](https://ems.press/content/serial-article-files/46004), printed pp.1658–1660, and inspected its rendered pages. The interaction matrix depends on the ordered concentration points. The source first displays a strict negative cone over the ordered configuration space of S^3, then displays the nonpositive punctured set and the ambient relative pair. The package correctly keeps those two inequalities distinct and does not replace the total family by one fixed quadratic form. There is no permutation or antipodal quotient in the displayed base and pair.

The 2005 matrix display has positive reciprocal-distance entries. There is also a source inconsistency worth recording: later prose on p.1659 calls the quadratic value negative when all masses have one sign, which does not agree with that positive display. [Bahri's 2016 paper](https://www.numdam.org/item/10.1051/cocv/2016048.pdf), rendered p.949, explicitly uses the negative reciprocal-distance matrix. The submission chooses the positive 2005 display openly and states the effects of sign reversal; it does not claim to resolve this source convention for the entire Yamabe variational program.

The report also abbreviates the passage from Euclidean coordinates to the compactified S^3 configuration base. The p<=3 result is proved for any continuous positive off-diagonal weight family on that base. The four-point example uses actual Euclidean reciprocal distances and also actual round-sphere chord distances. The boundary consequence is explicitly restricted to the Euclidean model. Those qualifications prevent an unsupported change of kernel normalization.

## 2. Fixed fibers and the role of a zero eigenvalue

After real congruence, write the form as -|x|^2+|y|^2 with z in the kernel. For the weak cone, shrinking only y preserves the inequality and fixes the target y=0. The pair (x,z) cannot vanish on the original punctured cone: otherwise the inequality forces y=0 too. This is therefore a strong deformation retraction onto the punctured negative-plus-null subspace, with homotopy type S^(r_-+r_0-1).

For the strict cone, x is necessarily nonzero. Shrinking both y and z preserves strict negativity and retracts onto the punctured negative subspace, giving S^(r_--1). If the indicated subspace has dimension zero, the respective cone is empty, as already stated in the package. The explicit product homeomorphism for a nondegenerate form is understood in the nonempty case; the positive-definite case is the empty exception, not a nonempty negative-dimensional sphere.

These are fixed-matrix results. They do not provide a continuously chosen eigenspace decomposition when A varies through a singular locus. The submission does not make that inference.

## 3. Global products for p=2 and p=3

For p=2, multiplication by sqrt(a) sends the varying off-diagonal form to J_2-I_2. For p=3, the three positive diagonal factors sqrt(ab/c), sqrt(ac/b), sqrt(bc/a) have the required pair products a,b,c. All factors and their inverses vary continuously over any positive-weight base. Thus the displayed map (configuration,u)->(configuration,D*u) is an actual global homeomorphism over the base, with an explicit continuous inverse. No eigenvector-selection or triviality assumption is hidden in this step.

The fixed matrix J_p-I_p has one positive eigenvalue p-1 and p-1 negative eigenvalues. Its nonpositive cone is a sphere S^(p-2), a positive radial factor and a closed one-dimensional ball, up to the stated homeomorphism. This gives the two product descriptions exactly, including their interval boundaries. The p=1 zero-matrix exception is also correct.

The configuration-space simplification is global: left multiplication by the inverse of the first unit quaternion sends that first point to 1. Stereographic projection from 1 then sends the remaining distinct points to distinct points of R^3. Its inverse multiplies back by the first quaternion. For two remaining Euclidean points, midpoint and difference identify their configuration space with R^3 times (R^3 minus zero). These maps and inverses are continuous everywhere in their stated domains. The resulting homotopy types S^3 times S^0 for S_2 and S^3 times S^2 times S^1 for S_3 follow.

Replacing A by -A reverses the positive and negative inertia. In particular, the p=3 weak fiber then has type S^0. The stated sign warning is mathematically necessary.

## 4. Independent verification of the four-point change

The two rectangles have pairwise distances 2s, 2c and 2, with their advertised incidence pattern. Every point is distinct, and adding a fourth zero coordinate places them on the unit S^3 without changing their chord distances. They are therefore admissible geometric configurations, not arbitrary positive-entry matrices.

Besides checking the displayed eigenvalues, I independently reduced the matrix by a two-by-two Schur complement. Let

    B=[[0,a],[a,0]],  X=[[b,d],[d,b]],  E=B.

Eliminating the first two coordinates is an invertible congruence taking A to B direct-sum S, where

    S=[[-2bd/a, a-(b^2+d^2)/a],
       [a-(b^2+d^2)/a, -2bd/a]].

B has one eigenvalue of each sign. The two eigenvalues of S are

    (a^2-(b+d)^2)/a,   ((b-d)^2-a^2)/a.

The latter is negative on the rectangle interval. The former changes sign exactly with a-b-d. This gives inertia (r_-,r_+)=(3,1) at (c,s)=(4/5,3/5) and (2,2) at (12/13,5/13), independently of the submitted Hadamard basis. The exact four eigenvalues in both examples agree with the submission. Thus the weak fibers have different sphere homotopy types S^2 and S^1.

The proposed connecting interval contains no collision. Its crossing eigenvalue is strictly decreasing in theta, with opposite endpoint signs, and the other three eigenvalues retain their signs. Equivalently, under t=tan(theta/2), its sign is that of 1-4t-t^4 on [1/5,1/3], whose derivative is strictly negative. There is one simple crossing. At it the weak cone retains the one-dimensional kernel and has type S^2, while the strict cone has type S^1.

Different fiber homology rules out a locally trivial fiber bundle across this locus. It does not determine the topology of the total subset, nor prove that the total zero boundary is singular. At a kernel vector, the derivative in u vanishes while a configuration derivative can remain nonzero, so these two facts are fully compatible.

The stereographic chord formula is correct. Its reciprocal gives a positive diagonal congruence between the spherical chord and Euclidean matrices, with diagonal entries sqrt(1+|x_i|^2)/sqrt(2). Such a congruence preserves inertia and the corresponding cone, rather than preserving eigenvalues individually. That is exactly the property used here.

## 5. Credited regular-boundary consequence

I read the full published [Chen–Ge–Jia–Lu paper](https://lu.math.uci.edu/pdfs/publications/2021-2025/66.pdf), including inequality (1.2), the discussion of p<=3 and Theorem 3.3 on rendered p.1740. The theorem proves the relevant Bahri–Xu inequality for p=4,5 in arbitrary ambient dimension. No extension beyond that range is needed for this package.

For F(a,u)=u^T A(a)u, the differential in u is 2Au and each configuration differential is u^T(partial A)u. If the full differential vanished, the left side of the credited inequality would be zero. Its right side is strictly positive for any u not zero: a nonzero component u_j occurs in at least one summand with i different from j, and every distance is positive and finite. This contradiction proves regularity of the zero level for 2<=p<=5 in the Euclidean model.

On the unit-u link, constrained criticality gives Au=mu*u. Since |u|=1 and F=0, mu=0. The same contradiction applies. The regular-level theorem then supplies the smooth hypersurface, and the sublevel set is a manifold with boundary. This is a sound consequence of credited prior work, not a fresh proof of the discrete inequality or a classification of the total space.

## 6. Reproducibility and remaining problem

All **7,526 author assertions** replay byte for byte. The separate standard-library checker passes **2,528 independent exact assertions**. It reconstructs distance matrices and performs explicit block congruences on 25 rational rectangle configurations, checks the quaternion/stereographic product coordinates on 369 labelled triples, and tests nonorthogonal three-point congruences and weak/strict cone deformations with null directions retained correctly.

The finite checks supplement the proof; they do not calculate a configuration-space attachment map or the general relative topology. The source's whole family for general p still requires understanding how the fiber strata fit together across zero-eigenvalue loci and near collision ends. A smooth boundary and a list of fiber homotopy types do not supply those data.

Keep **unsolved, 2/5**, with the exact low-point results, four-point obstruction and published p<=5 consequence clearly separated. The 2007 monograph was not fully retrieved from a primary source, and the bounded literature audit is not proof that no later classification exists. No mathematical revision of the frozen partial is required.
