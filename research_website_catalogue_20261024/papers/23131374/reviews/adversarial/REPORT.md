# Independent adversarial review:23131374

**The full stated mathematical construction is supported; a material direct prior-work omission was identified.** I found no counterexample or substantive gap in the six-page proof for either surface or any fixed finite integer endpoint. A previously published fourteen-page preprint contains a stronger stated theorem and an inspected proof of the current positive-background cases, using the same spiral/logarithm/convex-radius architecture. Mathematical correctness and a claim of a new geometric resolution must therefore be assessed separately.

The actual reviewed note is *Integer endpoint discontinuity of normalized uniformization for positively curved surfaces*, version1.0, manuscript dated3October2026. The complete six-page PDF and complete19,942-byte TeX were read before research or opinions. All six actual PDF pages were subsequently visually inspected. PDF SHA256:`f900d86763266c73a5886df7edd194d275a25c31d55755c00716860d2e46e4a9`; TeX:`818f5ebb96328c2cdf418b05ff34bc5bbec5943ef508c798c715dc1fca4a7114`. Raw Zenodo metadata declares publication4October2026 and creation`2026-10-04T05:04:33.302140+00:00`; these are distinct from the manuscript date. The original sources were not changed.

## Exact scope and independence

For each fixed finite integer r>=0, the theorem constructs smooth complete strictly positive-curvature metrics on C and S2 converging to their positive background in ordinary compact-open Cr, while the unique specified point-normalized orientation-preserving uniformizing maps fail compact-open C(r+1) convergence. The inverse of this particular normalized parametrization is discontinuous, including its positive-curvature restriction. It does not claim a single sequence for all r, failure in noninteger Holder or Cinfinity topologies, a result on RP2, a uniform positive lower curvature bound on the plane, or an obstruction to unrelated abstract homeomorphisms.

The independent early ledger was sealed at`2026-10-25T06:49:44.376891+00:00`, SHA256`400568e76c3e7f7f6309f608b08cbfa43b7918d1c11e958e7c08ccca80df29ae`. It records seven independent attack mechanisms before primary browsing, the earlier14-page body, supplied code or historical/current opinions. Current sibling scope/analytic reports and current root scientific opinions were never opened. Root supplied the raw earlier primary body only after this seal. A fresh search independently returned its public page after the seal too; no conclusion was based on its abstract alone.

The own exact/numerical controls preceded supplied-checker reading. Later the distributed README, SOURCE_QUALIFICATIONS and complete finite-check source were read as documentation. Their historical review statements were not treated as proof, and no provided program or PASS wrapper was run or imported. No children, source repairs, new research programme, git/publication/UI/Sheet action or external communication occurred.

## Checkable mathematical reconstruction

### Normalization, backgrounds, completeness and global maps

The plane background b=log(1+|z|^2)/2 gives Delta b=2/(1+|z|^2)^2 and Gaussian curvature2/(1+|z|^2)>0. Its radial length bound is arsinh|z|, so every escaping curve has infinite length. The sphere background b=log(1+|z|^2)-log2 gives the unit round metric. Both have positive minima of Delta b and curvature on the fixed closed perturbation disk.

A smooth positive metric equal to its complete background outside that disk is globally comparable to it, with comparison constants allowed to depend on n. Thus each perturbed metric is complete. No uniform comparison over the sequence or lower curvature bound at infinity is needed. The conformal target is complete because the explicitly constructed coordinate map is an onto isometry.

For r>=1, the universal first derivative estimate gives ||D(f-id)||infinity<1 for all sufficiently large n. The all-plane Lipschitz lower bound proves injectivity. For each target y, z -> y-(f-id)(z) is a contraction of the complete plane, so f is onto. I+Dw has positive determinant: the straight matrix path I+tDw stays invertible and starts at I. The smooth inverse theorem supplies a global orientation-preserving smooth inverse. Identity outside the disk plus injectivity ensures that the disk maps to itself. The maps fix0,1 and extend by identity near spherical infinity.

Two decompositions of the same metric give a conformal automorphism psi composed with f inverse. It fixes both plane points, or the three sphere points, and is therefore identity. This is a direct uniqueness argument, with no endpoint continuity of Beltrami solutions assumed. No derivative is normalized at0.

### The zero endpoint survives the main normalization attack

The radial twist is constant rotation in the shrinking inner disk and identity outside R. Smoothness at0 follows from constant rotation there; smooth flat transitions of eta handle both radial boundaries. Its inverse subtracts the radial angle and fixes the same points. In orthonormal polar frames its differential is a shear with q=t theta'(t)=O(1/n). The exact relative metric is [[1+q^2,q],[q,1]], including the unchanged tensor at0. Hence metrics converge in C0 while Dphi_n(0)=Rot(theta0) stays different from I. A conformal rotational ambiguity cannot remove this derivative obstruction because the second fixed plane point, and the sphere triple, remove that ambiguity. Both positivity and completeness are retained by isometry.

### All finite derivative orders are justified by an actual induction

For L=log sqrt(x^2+y^2+rho^2), an ordered jth derivative has form P_j/s^(2j), where P_j is homogeneous of degree j. The recurrence replaces P by s^2 partial_i P-2j x_i P. Multiplication by s^2 contributes at most3j times the coefficient l1 norm and the second term at most2j times, giving the stated5j bound. Since each coordinate is bounded by s, this proves the arbitrary-order estimate C_j s^(-j), not just its finite test range.

Leibniz's rule gives derivatives of z^(r+1)L through order r+1 bounded by C s^(r+1-k)(1+|log s|). For positive exponent the power absorbs the logarithm. At exponent0, epsilon(1+|log s|)<=epsilon(1+n)<=2. On the fixed cutoff annulus the regularized denominator is bounded away from zero, so all needed fixed-order cutoff derivatives are O(epsilon).

Direct Wirtinger differentiation gives f_barz=epsilon z^(r+2)/(2s^2) in the inner disk; the factor1/2 is correct. After k real derivatives the numerator has degree r+2+k over denominator s^(2k+2), yielding O(epsilon s^(r-k)) for k<=r. The f_z derivatives need only remain bounded in Cr; they converge to1 in C(r-1). With |f_z|>=1/2, finitely differentiated reciprocals remain bounded in Cr, so mu=f_barz/f_z is O(epsilon) in Cr. No unsupported convergence of f_z in Cr is used.

At each fixed n, L=log rho+O(|z|^2) near0, and epsilon log rho=-1. Therefore the displacement's first nonzero jet is exactly -z^(r+1), giving partial_x^(r+1)(f-id)(0)=-(r+1)!. This persists after discarding an initial finite sequence. The argument covers each fixed finite r with r-dependent constants and thresholds, as stated.

### Exact reconstruction and the higher endpoints

The tensor |dz+mu dbarz|^2 has eigenvalues(1+-|mu|)^2, so it is positive for sufficiently large n. The identity df=f_z(dz+mu dbarz) gives exactly

    g_n=f*(exp(-2U)|dw|^2),
    U=(b+a+log|f_z|) composed with f inverse.

The plus sign on log|f_z| cancels its squared differential factor. On the plane the conformal parameter is U; on the sphere it is U-b(w), not U alone. It vanishes near infinity and extends smoothly. The log modulus is smooth because f_z never vanishes; a global complex logarithm is unnecessary.

For r>=2, a=0 and mu ->0 in Cr imply g_n ->g_* in Cr, hence C2. Positive-definite background2-jets on the closed disk form a compact set; curvature is a continuous function of those2-jets. The positive background minimum gives curvature positivity there for the tail. Outside the disk it is unchanged. This does not attempt the invalid C1-curvature-continuity argument.

### The critical curvature correction controls the full operator

For r=1, D^2f=O(epsilon ell) and D^3f=O(epsilon/s), with ell=1-log s. Differentiating h=log|f_z| gives Dh=O(epsilon ell) and D^2h=O(epsilon/s+epsilon^2 ell^2)=O(epsilon/s), using s ell^2<=4/e. This includes quadratic derivative terms.

I independently differentiated the inverse-map identity. With J_ai=partial_i f_a and H=J inverse, the pulled-back Euclidean Laplacian has principal matrix **HH transpose** and drift B^i=-H_ia(partial_jk f_a)A^jk. It is not the reversed matrix and cannot discard the drift. The exact formula gives A-I=O(epsilon), A>=I/2, B=O(epsilon ell). It follows on the inner disk that L_n(b+h)>=Delta b-C0 epsilon/s, including the background error and the drift on h.

The regularized radius has positive semidefinite Hessian with radial eigenvalue rho^2/s^3 and tangential eigenvalue1/s, and Delta s>=1/s. Thus trace(A Hess s)>=Delta s/2 even though Hess s is far from uniformly isotropic. The drift error is at most C epsilon ell. Bounded s ell permits one threshold N for which L_n s>=1/(4s) everywhere in the inner disk. Choosing **one fixed K>4C0 first**, and then taking n sufficiently large, gives positivity for a=K epsilon chi s there.

The fixed annulus R/2<=|z|<=R is separately covered: all f-id, h and a derivatives required by L_n are O_K(epsilon), so L_n(b+h+a) tends uniformly to Delta b there. The positive minimum handles every transition point. Outside support it is exactly Delta b. This is a uniform proof across core, annulus and exterior, not a substitution of finite samples. The correction is O_K(epsilon) in C1 while its Hessian may become large, which is exactly what is needed. Finally curvature is the positive factor exp(2U(f(z))) times this operator value, and the fixed second jet -2 prevents C2 convergence of the maps.

## Source applicability and the pushforward formulation

The actual two-page [Belegradek-Hu erratum](https://doi.org/10.1007/s00208-015-1354-1) was freshly acquired and read completely. It explicitly changes the incorrectly claimed integer continuity theorem to noninteger Holder norms with a one-derivative shift on the diffeomorphism and reports no counterexample then. The actual published [Banakh-Belegradek body](https://www.jstage.jst.go.jp/article/jmath/70/2/70_733/_pdf/-char/en), full relevant Section2 and Sections8-9, fixes smooth objects, compact-open topology, sphere triple/plane pair, continuous bijections and the shifted derivative order. Only the nonnegative-curvature, simply connected plane/sphere interfaces are used here.

The whole relevant workshop contribution on printed pp148-151 was read in the [actual OWR body](https://publications.mfo.de/bitstream/handle/mfo/3566/OWR_2017_03.pdf?isAllowed=y&sequence=1); p149 was also visually checked. Its map uses **pushforward**, while the submitted note uses pullback. This does not invalidate the endpoint answer: replace f by its inverse. For these sequences this can be checked directly, without a general noncompact group theorem. For r=0 the inverse derivative is Rot(-theta0). For r>=1 the inverse first nonlinear jet is +z^(r+1), so its (r+1)st derivative also stays nonzero. The external historical question is therefore matched exactly; the note does not prove a false result about arbitrary homeomorphisms between the parameter spaces.

The complete Section7 of [MSS22 v1](https://arxiv.org/pdf/2208.02551v1) was read. Its Example5 supports the credited classical continuous-Beltrami/non-C1 logarithmic mechanism, without supplying the current global positive-curvature realization. The two historical books were not directly read and no additional theorem was imported from their indirect attribution. Current mathematical correctness does not depend on proving a negative literature search.

## Material identified prior theorem and exact overlap

The complete **fourteen-page** primary preprint by Alper Ferudun, [*The Conformal Parametrization of Nonnegatively Curved Surfaces Is Not a Homeomorphism at Integer Smoothness*](https://doi.org/10.5281/zenodo.23062867), was read after the early seal, including all proof sections and disclosed finite-computation limitations. PDF SHA256:`d9a2c57a8a267370df199f7923434998e1d670d4add13d80fcc335bdf606291c`. Its critical construction and nonflat proof were also checked in the supplied raw TeX, lines674-914. This is an unrefereed primary preprint, not a claimed refereed established theorem or an abstract-only source.

| Current mechanism/claim | Earlier actual body | Comparison |
|---|---|---|
| Every finite endpoint, C and S2, strictly positive complete metrics | Theorem1.1, pp1-2 | Earlier statement is stronger: inverse discontinuity at every nonnegative and every positive base point, with further conformal-factor conclusions |
| Slow compactly supported radial twist at r=0 | Section3, Proposition3.1, p5 | Same endpoint mechanism; earlier proof even treats nonradial conformal backgrounds |
| Small regularized z^(r+1) logarithmic displacement, exponentially small scale, fixed high jet and small Beltrami Cr norm | Section4, Lemmas4.1-4.5, pp5-7 | Same architecture, with an integrated cutoff and log(|z|^2+delta^2) rather than the current product cutoff and half-log; numerical jet coefficients differ accordingly |
| r>=2 curvature from C2 convergence | Section5.1, p8 | Same argument |
| r=1 C1-small radial correction with large positive inner curvature and controlled negative/transition annulus | Section5.2, Lemmas5.2-5.3 and Proposition5.1 proof, pp8-9 | Earlier inner correction is16 epsilon sqrt(|z|^2+delta^2)+constant, extended through a compensated radial integral. Current K epsilon chi s and inverse-coordinate estimate are a different implementation, not a new covered theorem scope |
| Complete positive plane/round-sphere examples, normalized maps and exterior fixed metric | Section6.2, p10, with Sections2-5 | Earlier pertinent proof applies to both current positive backgrounds; no flat-case assertion is needed for this containment conclusion |

I reconstructed the pertinent earlier proof, rather than accepting the stronger statement uncritically. Its curvature linearization has remainder O(|mu||D2mu|+|Dmu|^2), and the Laplacian error is O(|mu||D2v|+|Dmu||Dv|). The exact polynomial in Lemma5.3 provides a positive margin for the16-radius correction. The fixed annulus errors are O(epsilon), and Section6.2 localizes inside a positive-curvature disk and preserves completeness/normalization. No substantive defect was found in this route covering the current theorem. The earlier flat-case extras, other topology statements and all numerical reports are not certified as a separate full-paper acceptance here.

Actual prior raw metadata declares version1.0, publication30September2026, creation`2026-09-30T14:01:44.407539+00:00`; the manuscript also prints30September. These precede both the current3October manuscript and4October declared publication/creation. This is a direct identified prior-work relation, not a worldwide firstness conclusion for either author.

The submitted bibliography and source qualifications omit this materially relevant preprint. Their bounded-negative-search sentence is not a logical assertion of exhaustive absence, so I do not call it a disproved firstness claim or infer copying/intent. Nevertheless a presentation of the **full geometric realization** as the potential new contribution now requires this explicit attribution and containment qualification. No distinct new theorem scope has been verified in the current note. A different concise correction/estimate may have expository or proof value; its own priority has not been established. No source repair was attempted.

## Independent controls, exact gap and disposition

Own `independent_checks.py` imports no supplied source. It checks ordered logarithm recurrences through order6, origin endpoint jets for r1-8, Wirtinger factors, the twist shear, convex-radius Hessian identities, and the pertinent prior polynomial identity. A nonlinear triangular shear gives a direct inverse-coordinate Laplacian check and detects reversed matrix order and omitted drift; a linear test already detects drift omission.

Eighteen inner-disk r1 controls use both actual backgrounds, n8/12/20 and z/rho=(-2,0),(0,1),(2,0), with identical32-digit values at85 and125 digits. All corrected K32 operator values are positive. Omitting correction is negative, e.g. plane n20,z=-2rho gives about-4.8128e7 versus+3.6846e8 with correction. These are local corroboration and negative controls, **not** a global certificate for K32, an annulus test, a universal-order proof or a priority argument.

One initial local harness failure constructed empty mpmath matrices using the wrong constructor; the exact code, traceback and bounded receipt are preserved under `failed-run-1/`. It was not a mathematical singular-Jacobian counterexample. Explicit row construction corrected that harness. The final isolated25-second run completed in1.195seconds, return0, empty stderr, with process-group SIGKILL attempted in finally. Its stdout SHA256 is`ccfa43592c83796ebb97abbfb157e88f4b55d011c4fab730e9f51877da031e10`.

**Strongest verified current result:** the entire stated all-fixed-finite-endpoint construction, including the critical correction, smoothness, complete positive geometry, normalized factors and both plane/sphere cases. **Exact remaining mathematical gap:** none found in this adversarial audit. **Material defect/context classification:** uncredited direct earlier preprint with stronger relevant theorem/proof; current theorem scope is contained. **Novelty disposition:** no new theorem contribution verified; explicit prior-work qualification is needed before presenting this as a new resolution. No formal certification, independent human review or exhaustive historical priority claim is made. Parent must read the actual paper and all final independent reports before promotion.
