# Independent initial source/scope reconstruction — record 22929857

This initial follows personal reading of the complete actual four-page published PDF and the complete 11,262-byte controlling TeX, plus inspection of all four actual rendered pages. It precedes foreign mathematical bodies, deposited code/data, archived audits, triage, current reviewer/root opinions and author priority notes. Native API metadata descriptions were necessarily encountered during custody acquisition; they are not proof or review authority. ZIP names/checksums were inspected structurally without reading audit/code/research bodies.

## Literal claim and exact success criterion

For every n>=2,N>=1, use the unit-round sphere S^(n-1) with geodesic distance and U(N) with the length metric of either the unnormalized Hilbert–Schmidt norm or operator norm. On maps with Lipschitz constant <=1/2, equipped with uniform topology, fix p in the sphere and define A=Phi(p), W=A*Phi, H_t(Phi)=A(W+tI)(I+tW)^(-1), 0<=t<=1. The claim is an explicit strong deformation retraction onto the entire constant-map copy of U(N), fixing every constant at every time and ending at the input-dependent constant A. It restricts to the strict sublevel and has Lip(H_t Phi)<=(1-t^2)/(1+t^2) Lip(Phi). It stays in the same U(N), without stabilization.

The claim includes nonsmooth Lipschitz maps, continuity simultaneously in t and the entire input map, based-space contractibility, arbitrary continuous parameter families, and constant left/right frame equivariance. For n=1 the separate S^0 statement assumes angular distance pi between its two points; it does not use disconnected intrinsic path distance. No arbitrary bi-invariant metric follows from the shortest-geodesic normalization alone. No nontrivial sphere-fibration theorem is claimed. The printed Gromov question and Neretin attribution remain primary-source obligations; no first-publication guarantee is claimed.

## Independent proof mechanism

A target point W within intrinsic pi/2 of I has each principal eigenangle |theta|<=pi/2: act with an arbitrary unitary path on an eigenvector; its real-sphere endpoint distance is |theta| and its speed is <=operator-norm speed<=HS speed. Thus Re W>=0. The domain diameter pi and L<=1/2 place every normalized value W_Phi(x) in the closed right semicircle set S.

For W in S, D=I+tW satisfies D*D=(1+t^2)I+t(W+W*) >=(1+t^2)I. Its inverse therefore exists uniformly even at t=1, with operator norm <=1/sqrt(1+t^2). The numerator N=W+tI has N*N=D*D, implying F_t(W)=ND^-1 is unitary. Endpoints and fixed identity are direct: F0=W,F1=I,F_t(I)=I.

For noncommuting U,V, left/right multiplication by their own denominators reduces the difference formula to (U+tI)(I+tV)-(I+tU)(V+tI)=(1-t^2)(U-V); the UV terms cancel without commuting U and V. Hence the ideal norm inequality gives chordal factor q_t=(1-t^2)/(1+t^2). Differentiation gives DF_t(W)[E]=(1-t^2)D^-1 E D^-1. This follows either by product/inverse differentiation or by the resolvent difference. It does not require W and E to commute.

A chordal contraction alone would not establish intrinsic distance contraction for arbitrary endpoint pairs. Instead, each minimizing domain geodesic has image contained in S; the original Lipschitz image is absolutely continuous, with norm-speed integral <=L times domain length. The differential bound contracts that particular curve's length. Its transformed curve is an admissible intrinsic target path, proving the required Lipschitz estimate. The proof does not need S to be geodesically convex or a minimizing target geodesic inside S.

Changing the input changes its anchor as well. With delta=sup||Phi-Psi||, anchor difference <=delta and normalized difference <=2delta. Thus H_t has map-space chordal difference <=(1+2q_t)delta<=3delta. Joint t continuity follows from the uniformly invertible rational formula on compact [0,1]xS. Compact finite-dimensional U(N) has equivalent norm/intrinsic uniform topologies, so this is the requested uniform topology. Direct joint substitution also handles arbitrary topological parameter spaces.

For Q,R unitary, normalized W for Q Phi R is R* W R, and rational functional calculus commutes with conjugation, so H_t(Q Phi R)=Q H_t(Phi) R. On based maps A=I, the end constant is I and all times stay based, proving contractibility.

## Boundary and falsification plan

Test t=0,1, t approaching1, Re W=0, eigenangles +/-pi/2, mixed multiplicity, N=1 and noncommuting N=2, constant maps, sharp L=1/2, the strict sublevel, and n=1 with its expressly stipulated distance. At t=1 the numerator factor 1-t^2 vanishes and invertibility remains bounded; there is no singular endpoint. For scalar angles in [-pi/2,pi/2], angle derivative is (1-t^2)/(1+t^2+2t cos theta)<=q_t and fixes theta0=0. The S0 HS claim additionally uses the standard principal-angle Euclidean distance formula; the operator claim uses the maximum formula. These exact metric facts should be independently justified or checked against a primary source.

A scalar boundary family Phi(x)=exp(i d(p,x)/2), N=1, is admissible at L=1/2 and approaches the q_t differential factor near the antipode. This can diagnose an accidental replacement of q_t by the smaller factor (1-t)/(1+t); it is not an additional novelty claim.

The principal-log comparison for L<1 uses normalized radius <pi, excluding eigenvalue -1; it gives a continuous ordinary deformation without claiming the same Lipschitz bound. Neretin's Cayley transform should support classical attribution, not be assumed to prove this quantitative map-space theorem. Gromov's actual pages35–36 must be read for exact question, target metric convention and the distinction between bounds1 and1/2.

## Remaining gates at initial seal

1. Read exact primary Gromov question and metric context, including adjacent clauses; confirm that the paper answers the literal printed assertion and does not imply resolution of a stronger geometric programme.
2. Read Neretin's actual cited Cayley chart and theorem to verify attribution/normalization. No priority conclusion from the author's search notes or from an unsuccessful new search.
3. Inspect and run bounded meaningful deposited exact/numeric diagnostics read-only after checking for source writes; construct independent exact noncommutative and scalar endpoint checks. Finite diagnostics do not replace the above universal analytic proof.
4. Record strongest verified claim, any exact source-scope gap, and final boundaries. No substantive defect currently follows from this independent reconstruction; all conclusions remain hypotheses until the primary and check interfaces are completed.

Review completion estimate 30%: custody and full target reading, complete literal claim extraction and independent analytic mechanism are done; primary-source interpretation, diagnostics and final adversarial boundary verification remain.
