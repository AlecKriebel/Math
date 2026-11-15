UTC: 2026-11-14T23:52:42.430658+00:00

# Independent initial reconstruction and falsification ledger

This ledger was written after my personal complete reading of the actual four-page PDF, full controlling TeX (150 lines,11262 bytes) and visual inspection of all four freshly rendered pages. Before this initial seal I have read no foreign primary body, supplied code/data, native record-description body, inventory triage, archived/current review opinion, source-owner scientific finding or analytic-family opinion for this paper. The raw SOURCE_READY custody fields and the assignment's literal title/hash fields were read. Earlier unrelated 108/109 assignments are not claimed as readings or scientific evidence for this paper. This is a new independent adversarial reconstruction.

## Literal quantified claim and metrics

Fix n>=2,N>=1,p in the unit-round geodesic sphere S^(n-1). The norm nu is either the UNNORMALIZED Hilbert–Schmidt norm sqrt(tr X*X) or operator norm, with its induced intrinsic length metric on U(N). The map space consists of all, possibly nonsmooth, Phi with intrinsic Lipschitz constant L<=1/2 and has the uniform topology. Put A=Phi(p),W(x)=A*Phi(x), and

    H_t(Phi)(x)=A(W(x)+tI)(I+tW(x))^-1, 0<=t<=1.

The claimed strong deformation retraction fixes each constant map, starts at Phi and ends at the constant Phi(p), with Lip H_t(Phi)<=q_t L, q_t=(1-t²)/(1+t²). It preserves both closed and strict1/2 sublevels, remains in the SAME U(N), and is jointly continuous in the entire map and t. It is a retraction onto a copy of U(N), not a contraction of the unbased space to one global point. The based subspace Phi(p)=I contracts. The separate S^0 claim uses angular distance pi, not a disconnected path metric. Continuous families over arbitrary parameter spaces and constant two-sided frame equivariance are also claimed. No nontrivial sphere-fibration or arbitrary-bi-invariant-metric theorem is claimed. The weak principal-logarithm deformation is additionally claimed for every fixed L<1 without preservation of a Lipschitz sublevel. Classical Cayley/log mechanisms and priority limits are explicit.

The original question and its exact sphere/target metric convention still need independent primary-interface inspection AFTER this seal. The manuscript prints23September2026/version1.1, while READY reports creation24September2026 and later update10October2026; neither archive dates nor latest version are silently substituted.

## Mechanism A: spectral containment and noncommuting resolvents

For an eigenvector Wv=e^(i theta)v, every unitary path U(s) from I to W gives a real-unit-sphere path U(s)v, whose length is at least |theta| and whose speed is bounded by ||U'||op<=||U'||HS. Thus each principal eigenangle is bounded by intrinsic d_nu(I,W). Since d(I,A*Phi(x))<=L d(p,x)<=pi/2, every W(x) has nonnegative Hermitian real part. The proof does not assume that close matrices commute or that the image is in a scalar subgroup.

For B=I+tW, B*B=(1+t²)I+t(W+W*)>=(1+t²)I. This yields invertibility uniformly THROUGH t=1, operator inverse norm<=(1+t²)^(-1/2), and is stronger than just avoiding -1. The equal Gram matrices of W+tI and B give unitarity of F_t(W). F_0(W)=W,F_1(W)=I,F_t(I)=I.

The alleged noncommutative identity can be checked by sandwiching:

    (I+tU)[F_t(U)-F_t(V)](I+tV)
     =(U+tI)(I+tV)-(I+tU)(V+tI)
     =(1-t²)(U-V).

The tUV terms cancel in their original order, so no U,V commutation is used. Differentiating gives DF_t(W)[E]=(1-t²)B^-1 E B^-1. The two-sided ideal inequality for HS and op yields q_t. A possible falsification route is a wrong resolvent ORDER in a noncommuting example; I will construct exact rational unitary examples to test that explicitly, rather than trust scalar or random commuting tests.

## Mechanism B: intrinsic geometry, nonsmooth curves and sharp boundary

A chordal matrix inequality alone would not give an intrinsic Lipschitz constant. Here every chosen spherical minimizing geodesic gamma maps under W into the same closed semicircle domain S, and the input curve is absolutely continuous in matrix coordinates and intrinsic length. The finite-dimensional chain rule along that actual curve gives length(F_t o W o gamma)<=q_t length(W o gamma)<=q_t L length(gamma). Taking the intrinsic endpoint distance below this curve length yields the required inequality. This avoids any assumption that S is geodesically convex, or that a U(N) minimizing geodesic between arbitrary image pairs stays in S. The original-domain geodesic remains available even at sphere antipodes and for arbitrary nonsmooth Lipschitz input.

A strong edge test is the scalar map Phi(x)=exp(i d(p,x)/2). Its argument lies in[0,pi/2] and its intrinsic Lipschitz constant is1/2. The scalar transformed argument is g_t(theta)=2 arctan(k tan(theta/2)),k=(1-t)/(1+t). Direct differentiation gives g'_t=(1-t²)/(1+t²+2t cos theta). As theta approaches pi/2 from below this tends to q_t. Thus the universal q_t is plausibly tight even on scalar maps; a claimed stronger coefficient such as q_t² would fail for0<t<1. This is a checkable analytic boundary family, not numerical evidence.

At t=0 the estimate is equality; at t=1 the map is constant and the inverse bound is still finite, including W with eigenvalue ±i. The proof excludes W=-I. At L=0 it fixes every constant. At N=1 it reduces to the scalar formula. At L=1 the identity circle map S1->U1 is a noncontractible example; the weak L<1 logarithm threshold is not carelessly closed.

UNNORMALIZED HS is load-bearing. Under a normalized HS norm divided by sqrt(N), the loop diag(e^(i theta),1,...,1) would have Lipschitz constant1/sqrt(N)<=1/2 forN>=4 but nonzero determinant winding. It could not deform to a constant in U(N). That is an outside-hypothesis counterexample to an illicit normalization generalization, not a defect of the stated theorem. Similarly S^0 with path-distance infinity would permit unrelated values with zero formal Lipschitz cost; angular pi is essential and explicitly stated.

## Mechanism C: map-space topology, changing base value and families

For two eligible maps with delta=sup||Phi-Psi||nu, their base values A,B differ by at most delta and their normalized images differ by at most2delta. Unitarity and the chordal q_t estimate yield sup||H_t(Phi)-H_t(Psi)||nu<=(1+2q_t)delta<=3delta. The rational formula is uniformly continuous on compact[0,1]xS. This gives joint uniform-topology continuity; finite-dimensional intrinsic and matrix metrics induce the same compact-group topology, so their uniform mapping topologies agree. The claim is not continuity in a stronger Lipschitz-norm topology.

For any topological Y with continuous Phi(y,x), A(y)=Phi(y,p) is continuous and the rational expression is a direct continuous composition in(y,x,t). No local compactness or metrizability of Y is needed for that pointwise formula. For constant Q,R, the new base is QAR and normalized image is R*WR. Conjugation covariance of the rational expression gives H_t(QPhiR)=QH_t(Phi)R. All constants remain fixed because their W equalsI. This proves the strong, rather than merely weak, retraction endpoints if the length and continuity details stand.

For S^0, only the second endpoint changes after fixing p. Diagonalization reduces its distance-to-I contraction to the scalar angle formula; the usual principal-angle HS/op distance formulas are an imported finite-dimensional geometric fact. I will verify that interface or supply the needed direct path argument, rather than infer it from a chordal bound. The full connected-sphere proof does not need the exact distance formula, only the eigenvector lower bound and length characterization.

## Mechanism D: literal question, classical credit and bounded diagnostics

The main finite-dimensional proof appears internally coherent on a first independent reconstruction. No atomic counterexample to its stated full metric/quantifier/topological claim is yet identified. Still pending are actual Gromov pp35–36 (question number, normalization, dimension and continuity scope), Neretin's Cayley interface, rigorous curve-length facts and source-code/static-certificate inspection. The manuscript's historical search statement is bounded; no firstness or continued-worldwide-openness conclusion follows. Exact algebra and adversarial noncommuting cases can confirm transcription, but sampled numerical stress tests cannot prove the full claim.

After this seal I will inspect only relevant deposited support, derive exact rational noncommuting checks and hostile boundary controls, and verify primary interfaces. If a substantive defect appears, its exact evidence will be recorded and the repair route stopped. Root scientific delivery remains withheld pending its own111 initial seal. The original full claim will not be replaced by a narrower supported result.
