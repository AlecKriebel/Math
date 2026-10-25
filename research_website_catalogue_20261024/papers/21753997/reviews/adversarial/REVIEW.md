# Independent adversarial review of Zenodo 21753997

Completed: 2026-10-25 UTC. Review assignment: 100% complete.

**Verdict: PASS for the stated mathematical theorems, with a nonblocking wording clarification.** The main construction, complete constrained rate family, generic geometric coprimality, two radical decompositions, fixed-support integer optima, frozen-example transverse classification, and structural lower bounds survived the independent checks below. No substantive theorem-level defect was demonstrated. This is an AI mathematical review, not human peer review, a universal novelty certificate, or authorization to publish.

## 1. Exact object and review independence

The reviewed named release is Zenodo **21753997, v2.0.0, 2 August 2026**, “A four-parameter family of reversible three-species mass-action continua without a common factor.” Its single public asset is a complete repository archive; only the named work's 126 extracted files were accessed for this review. The current manuscript is the 14-page `releases/v2.0/output/pdf/manuscript-v2.0.0.pdf`, SHA256 `fe429cf073b30cacfe1ba75624236cda2545c44076f711d4319dcb22ff79512b`. The whole 180,108,207-byte public ZIP is SHA256 `d92c83fd79fc1a723bcaa3fd0674f9fcf04dec18bb6a220c583f6bef4cbdc9fd`, MD5 `4d4c43174a28c17a82b8365ead817975`.

I read all 14 current PDF pages and the complete current mathematical source, all eight frozen-v1 pages, and the one-page specialist statement. The duplicate current PDF and duplicate handout are byte-equivalent reader copies, not additional works. Necessary support read includes the family derivation, clean-rate/stability note, minimality analysis, current principal verifiers, and the central radical/Sturm portions of the supplementary audit checker. The latter checker was also replayed in full; this does not imply that every line of every redundant checker received a separate code audit.

Before reading or running submitted mathematical helpers, I wrote and ran fresh reaction reconstruction, quotient-ring linear algebra, positivity, GCD, radical, integer-search and normal-coordinate controls. Those controls use only the manuscript's displayed data and this review's preceding outputs. No sibling review or dedicated historical opinion body was consulted. Required manuscript/handout/support text contained incidental claims about prior checking and priority; these were not used as evidence. An initial inventory exposed unrelated archive filenames but no unrelated mathematical work was opened.

All source bytes were preserved. Replay used an isolated copy under this review's ignored cache. Final source/reader/primary bindings and selected-member integrity checks are in `evidence-bindings.json`; fresh scripts, exact outputs and eight submitted logs are retained outside the cache.

## 2. Exact claim and hypotheses

The network has three species, ten listed complexes, ten reversible pairs (twenty directed reactions), one linkage class and stoichiometric rank three. Every strictly positive rate vector in the displayed four-parameter **conic-preserving** family has the same positive equilibrium ellipse in its single positive stoichiometric class. The four-dimensional family has codimension sixteen in the full twenty-rate space. The coordinate polynomials are geometrically coprime on a nonempty Zariski-open part of that family; coprimality is not claimed for every positive parameter.

The conic is

\[
L=z-x-y+1=0,\qquad Q=7x^2-2xy-16x+7y^2-16y+16=0.
\]

The free rates are \((a,b,c,d)=(k_{29},k_{43},k_{95},k_{98})\). All twenty rates are positive exactly when

\[
a,b,c,d>0,\quad b<c,\quad 192a+221c<154d.
\]

The complete-family theorem is written over the rationals. Its rational matrix/kernel calculation also extends directly to real parameters. The two specified integer examples have radical steady ideals consisting of the conic and fifteen reduced isolated complex points. The clean example simultaneously minimizes maximum rate and total rate **within this fixed-support positive integral family**. The transverse stability theorem concerns the frozen example, not all four-parameter members.

“Reversible” refers to the presence of both directed reactions in each pair. It does not mean detailed balance, thermodynamic reversibility, or complex balance at the conic equilibria. The construction concerns algebraic mass-action kinetics with positive rate constants; no physical realizability premise beyond that model is proved.

## 3. Independent reconstruction of the family and continuum

The ten complex vectors are `(0,0,0), (0,0,1), (0,0,3), (0,1,1), (0,3,0), (1,0,1), (1,1,0), (1,1,1), (2,1,0), (3,0,0)`. The undirected pairs are `(0,1), (0,4), (0,6), (1,7), (2,4), (2,7), (2,9), (3,4), (5,9), (8,9)`. Tracing these pairs connects all ten complexes. The reaction vectors from complex 0 to complexes 1, 4 and 6 have determinant of absolute value three; therefore the stoichiometric subspace is all of \(\mathbb R^3\). Positive rates preserve this support and its sole positive class.

I reconstructed each vector-field contribution as source monomial times target-minus-source stoichiometric vector. Reduction modulo \((L,Q)\) gives a 21-by-20 rational matrix. Its rank is exactly sixteen; the specified 16-by-16 minor equals \(7255941120/823543\). Substitution of the displayed family produces zero normal forms and four independent parameter columns. This proves exhaustiveness, not just that four examples work. The independently reconstructed matrix is retained as `family-matrix-fresh.csv`.

Necessity of the strict positive cone follows from the four free rates and the two entries \((c-b)/3\), \((154d-192a-221c)/64\). Under \(c=b+h\), \(d=(192a+221(b+h)+s)/154\), every rate is a nonzero linear form with nonnegative rational coefficients in positive \(a,b,h,s\). I checked those coefficient arrays symbolically, which proves sufficiency for the whole cone. Setting \(h=0\) or \(s=0\) makes a required arrow vanish; these faces are correctly excluded.

For \(d(t)=t^2-t+1\), the parametrization

\[
x=\frac{t^2+3}{2d(t)},\qquad y=\frac{3t^2+1}{2d(t)},\qquad
z=\frac{t^2+t+1}{d(t)}
\]

annihilates both conic equations exactly. All coordinates are positive for real \(t\), and \(z'=2(1-t^2)/d(t)^2\) is positive on \((-1,1)\), giving a genuine nonconstant continuum. The projective conic matrix has determinant \(-256\), so the conic is nonsingular and geometrically irreducible. In coordinates \(u=x-y\), its equation is \(4(u^2+(z-1)^2)=(z+1)^2\). Thus \(1/3\le z\le3\) and \(|u|\le(z+1)/2\); the complete real conic is a compact strictly positive ellipse. The missing affine-parameter limit is \((1/2,3/2,1)\). It is included when the parameter is viewed projectively. There is no hidden boundary concentration on the coordinate axes.

## 4. Generic GCD statement and its limits

Theorem 4.2 uses the projective multiplication map for a degree-\(e\) common factor, \(e=1,2,3\), of three homogenized cubics. Its source is projective, hence its image is closed. Taking affine cones includes the zero triple; pulling back the finite union along the linear four-rate map produces a closed bad locus. An affine common factor homogenizes to a homogeneous one. Possible extra factors of the homogenizing variable at degree-drop limits only enlarge this excluded locus and do not invalidate the sufficient open set.

The clean rational witness lies outside all these loci: I computed pairwise affine GCDs equal to one, and the GCD of the homogenized triple equal to one. A normalized common factor over the complex numbers would have algebraic coefficients; the product of distinct Galois conjugates would give a rational common divisor. Thus rational GCD one suffices here for geometric GCD one. This validates the scalar-extension interface rather than treating a rational computation alone as a geometric proof.

For parameters in the resulting open set, the nonzero steady ideal is contained in the height-two prime \((L,Q)\) and in no height-one prime. Therefore that conic prime is minimal. This proves a genuine irreducible equilibrium component. It does not prove a radical ideal for every family member, nor the same residual component count for every member.

A negative control increases only \(k_{01}\) by one at the clean example. Restriction of the new field to the old conic becomes \((0,0,1)\), so the continuum is immediately destroyed by this off-family perturbation. The family is not an open robustness assertion in ambient rate space.

## 5. Two explicit specializations and radical geometry

The clean parameters are \((653,1,70,915)\), with positive orthant coordinates \((653,1,69,64)\). Its primitive rate vector has maximum 10,296 and sum 52,464. The frozen parameters are \((3920,3920,15680,658560)\), with positive orthant coordinates \((3920,3920,11760,97200320)\). Independent mass-action reconstruction reproduces both displayed fields, their conic restrictions vanish identically, their pairwise affine GCDs are one, and their homogenized triple GCDs are one. Both Jacobians have rank two at \((3/2,1/2,1)\).

I independently recomputed lexicographic Gröbner bases over \(\mathbb Q\). With

\[
D=y^2-yz-y+7z^2/16-z/8+7/16,
\]

each steady ideal \(K\) has the form generated by \(g_0,DH,DR\), where \(g_0\) is linear in \(x\), \(H\) linear in \(y\), and the eliminant \(R(z)\) has degree fifteen. The conic prime \(P=(L,D)\) and triangular maximal ideal \(J=(g_0,H,R)\) are comaximal. Six product-generator reductions vanish modulo \(K\), and the three field coordinates reduce to zero modulo each of \(P,J\). Therefore

\[
K=PJ=P\cap J.
\]

The eliminant is irreducible over \(\mathbb Q\); separate finite-field irreducibility checks use prime 23 for the clean case and prime 19 for the frozen case. Its derivative is coprime to it. Consequently \(J\) is a degree-fifteen maximal ideal over \(\mathbb Q\), splitting into fifteen reduced isolated points over \(\mathbb C\), disjoint from the conic. This establishes radicality and the absence of hidden embedded components for these two specializations. Exact bases, maximal ideals and reductions are retained.

The presence of fifteen complex points does not assert fifteen real or positive points. A fresh exact real-root isolation check finds one real residual root for each eliminant. Rational interval Horner evaluation of its triangular coordinate expressions certifies that the corresponding point is positive and off the conic. Approximate coordinates, only for readability, are

- clean: \((15.84835305,44.52195624,52.76930053)\);
- frozen: \((53.74363502,141.80296725,171.22239893)\).

These facts agree with the radical theorems and delimit the wording issue in Section 9 of this report.

## 6. Fixed-support integer optimum

Because the free coordinates are themselves entries, integral rates imply integral \(a,b,c,d\). Integrality of two further entries forces \(15\mid d\), \(14\mid c\). A strict improvement over the clean maximum would imply \(d<1755\); a strict improvement over the clean sum implies \(d<2714\). Positivity gives safe bounds \(c<d\), \(1\le b<c\), \(1\le a<d\).

My fresh rational-arithmetic search separates the \(a\)-dependent and \(b\)-dependent entries at each \((c,d)\), rather than importing the submitted search output. It checks 17,358 candidate \((c,d)\) pairs under the larger bound, of which sixteen pass the fixed-entry integrality/positivity conditions and have feasible parameters. Independent minimization returns maximum 10,296 and sum 52,464, both attained by the clean vector. Another maximum-rate optimizer is found, so this is not a uniqueness claim. The finite computation is justified by the exact preceding bounds; it is not an unbounded search extrapolation.

This proves Proposition 5.2 in its stated family. It gives no optimum over other graphs, other equilibrium varieties, real rate scalings, or all reversible reaction networks.

## 7. Frozen-example transverse stability

I used a different linearization route from the submitted three-by-three characteristic-polynomial calculation. Polynomial division gives \(F=UL+VQ\). The induced two-by-two normal matrix is

\[
A=\begin{pmatrix}\nabla L\\\nabla Q\end{pmatrix}[U\ V]
\]

restricted to the parametrized conic. Nonsingularity of the conic makes these legitimate transverse coordinates. Its trace, determinant and discriminant independently reproduce

\[
\tau=-8T/d(t)^2,\qquad \pi=-6272N/d(t)^4,\qquad
\Delta=64E/d(t)^4.
\]

Exact Sturm counts are zero real roots for \(T\), two for \(N\), and zero for \(E\). Values at zero determine \(T,E>0\). The two roots of \(N\) lie respectively in \((-4,-3)\) and \((9/10,1)\), and exact signs on either side reproduce the stated classification. Thus the frozen ellipse has a normally attracting open arc between the two transitions, saddle-type transverse behavior outside, and a vanishing transverse eigenvalue at each transition. The missing projective parameter point has negative normal determinant and is saddle-type. These checks are exact global real-polynomial sign checks, not a sampled numerical plot.

The result describes transverse eigenvalues and normal behavior along the specified frozen ellipse. It does not assert a global basin of attraction, asymptotic stability of individual equilibria along a continuum, or the same classification for the clean example or all parameters.

## 8. Structural lower bounds and primary interfaces

I reconstructed the manuscript's elementary lower-bound arguments rather than relying solely on the arithmetic helper:

- In one species a positive-dimensional polynomial zero set forces the field to vanish identically. In rank one, all field coordinates are multiples of a single scalar polynomial. In two species and full rank, a positive-dimensional equilibrium set forces a height-one component and hence a common divisor in a polynomial UFD. Thus three species are necessary for this phenomenon.
- In a three-species, one-linkage, rank-two network, an integer vector \(w\) normal to the stoichiometric subspace assigns the same weight to every complex. The corresponding multiplicative scaling sends equilibria to equilibria, and its tangent has dot product \(\sum w_i^2p_i>0\) with the class normal at a positive point. A curve in one class sweeps out a surface of equilibria, forcing a height-one common factor. The one-linkage hypothesis is essential to this argument and is retained.
- At deficiency zero, injectivity of the complex matrix on the linkage-zero-sum subspace forces every positive equilibrium to be complex-balanced. Weak reversibility gives a one-dimensional positive Laplacian kernel on each linkage class. Two positive equilibria in one class have log difference in \(S^\perp\), whereas their concentration difference is in \(S\). Strict monotonicity of the logarithm makes them equal. Therefore a target continuum needs deficiency at least one.
- With \(m=\ell+s+\delta\), four complexes would force \((m,\ell,s,\delta)=(4,1,2,1)\), excluded above. Five complexes are a lower bound, not an attained optimum. The actual network has ten complexes and deficiency six. The support note's elementary reaction and degree lower bounds are consistent with these arguments.

The construction is self-contained apart from standard algebra and linear algebra; the literature interfaces are chiefly attribution and scope. I read the primary [Boros–Craciun–Yu manuscript](https://pollyyu.web.illinois.edu/manuscripts/2020-WR%20systems%20with%20infinitely%20many%20steady%20states.pdf), including its exact concluding questions. Its common-factor-free continuum question is distinct from its question about persistence for an ambient open set of rates. The present construction addresses the former, not the latter. BCY had already supplied continuum examples and rate flexibility with a common scalar factor; those broader ingredients are not credited as new here.

I also read the relevant statements and examples in the primary [Feliu–Henriksson–Pascual-Escudero manuscript](https://arxiv.org/abs/2412.17798), including Theorem A, Theorems 3.1/3.4, Corollary 3.5 and the fine-tuned examples in Section 3. These concern generic behavior in ambient rate/total spaces and allow exceptional algebraic loci. A codimension-sixteen constrained family is compatible with them. I did not independently reprove that thirty-page paper or perform an exhaustive literature search. Primary-source hashes, versions, reading extents and access limits are recorded separately. The manuscript's historical firstness sentence is not certified by this review.

## 9. Identified clarification, negative controls and exact remaining limits

Current v2 Section 8, PDF page 11, source line 750 says “the vector fields are nonzero off the conic.” If read as a pointwise nowhere-zero assertion on the complement, this is false, even in the positive orthant: the exact residual-point certificates above give counterexamples. `off_conic_control.py` independently isolates the real root, proves coordinate positivity by rational interval arithmetic, and proves \(L\ne0\) by an interval exclusion. The earlier `off-conic-boundary-check.json` is preserved alongside the reproducible strengthened check.

This is **not** a refutation of Theorems 5.1 or 6.1: they explicitly assert the isolated residual points. The frozen-v1 discussion instead establishes that the field is *not identically zero*, for example by evaluating it at an off-conic point. That context supports the intended nonzero-polynomial reading of the abbreviated v2 sentence. I classify it as a nonblocking wording clarification, not a missing construction proof. No source repair was made. A downstream presentation should say the field is not identically zero and should not claim every off-conic point is non-equilibrium.

Other falsification controls delimit the claims: strict-cone faces lose required arrows; the all-zero parameter is excluded; changing one unconstrained rate destroys conic invariance; detailed balance fails already on the first reversible pair at \((3/2,1/2,1)\), with net fluxes −9,136 and −6,886,754 in the clean and frozen cases. None contradicts the hypotheses. Boundary cases were not silently promoted into the theorem.

No substantive unresolved mathematical gap was found in the reviewed theorem scope. Remaining limitations are external to that conclusion: no comprehensive priority certification, no human peer review, no all-parameter radical/residual or stability classification, no ambient-rate robustness, no global complex/reaction optimum, and no independent second implementation of every computer-algebra primitive. Fresh checks and submitted replay both ultimately use SymPy's exact arithmetic/Groebner/root tools; their different reconstruction routes reduce, but do not eliminate, shared-library risk.

## 10. Reproduction and strongest supported result

Fresh scripts are `fresh_controls.py`, `fresh_radical_optimum.py` and `off_conic_control.py`. They retain exact matrices, ideals, rational intervals and result JSON. `replay_submitted.py` copies the v2 release into an isolated cache and runs all eight checks listed by the published reproduction workflow, using Python 3.9, SymPy 1.14.0 and mpmath 1.3.0 already installed at `/Users/alec/Documents/Math/.venv/bin/python`. It does not invoke package installation or alter the source tree. All eight exited zero; individual command timing, input hashes, stdout and stderr are retained. The first attempted runtime lacked SymPy, so the verified project environment was used; this was an environment selection issue, not a failed mathematical test.

The strongest supported result is an explicit reversible three-species mass-action construction with a positive one-dimensional equilibrium component in one compatibility class and geometric coordinate GCD one, together with a complete positive four-parameter conic-preserving family having generic geometric coprimality. The two explicit examples and their additional stated exact properties are supported as detailed above. The only identified text issue is the pointwise interpretation of the Section 8 phrase; no stronger conclusion about publication readiness or priority follows from this review alone.
