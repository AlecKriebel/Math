UTC: 2026-11-14T23:59:59.407377+00:00

# Independent adversarial derivation

This complete derivation continues the paper-only INITIAL_RECONSTRUCTION.md, sealed before any target foreign body, support code/data, triage or archived/current opinion. No sibling/source-owner scientific assessment has been read. The later deposited code and two actual primary interfaces are evidence with bounded roles, not the proof authority.

## 1. Exact finite-dimensional metric identities

Let nu be the unnormalized HS norm or op norm, and d_nu its intrinsic path metric on U(N). Both matrix norms are invariant under unitary left/right multiplication. For every piecewise C1 curve U(s), the norm of U'(s) is its prescribed length integrand. The ambient chord obeys ||U(b)-U(a)||nu <= integral ||U'||nu, hence <= every such path length and therefore <=d_nu.

Here is an elementary independent derivation of the principal-angle distance formulas, including the separate S0 boundary claim. Diagonalize W with an orthonormal eigenbasis v_j and principal eigenangles theta_j in[-pi,pi]. Any path U from I to W produces real-unit-sphere curves U(s)v_j. Each has endpoint spherical distance |theta_j| and length l_j >= |theta_j|.

For op, speed_j<=||U'||op, giving length(U)>=max|theta_j|. For HS, sum_j ||U'v_j||²=||U'||HS². Minkowski's integral inequality for the nonnegative speed vector gives

    integral sqrt(sum speed_j²) >= sqrt(sum (integral speed_j)²)
                                  >= sqrt(sum theta_j²).

The diagonal path exp(s log W), using these principal eigenangles, attains the respective lower bound. Thus

    d_op(I,W)=max_j |theta_j|,
    d_HS(I,W)=sqrt(sum_j theta_j²).

This argument uses fixed target eigenvectors and avoids any unproved differentiability of moving eigenvectors or eigenangle branches. Left translation gives the general endpoint formula. It confirms both stated metrics and the exact S0 formula without importing a broader geodesic theorem.

It also gives the length characterization used for nonsmooth maps. The corresponding chordal norms are max_j2|sin(theta_j/2)| and sqrt(sum_j4sin²(theta_j/2)). As the endpoints approach each other, intrinsic/chordal ratios tend uniformly to1, since |theta|/(2|sin(theta/2)|)->1 uniformly over a shrinking principal-angle interval. A continuous curve on a compact parameter interval has arbitrarily fine partitions with all increments in that interval. Triangle inequality permits refinement of any coarse partition. Consequently intrinsic curve length equals matrix-norm curve length. For an absolutely continuous matrix curve, that length is integral ||U'||nu, an elementary finite-dimensional normed-space fact. No chordal-pair estimate is silently called an intrinsic-pair estimate.

For a closed one-parameter subgroup exp(sX), parameterized over one period, its eigenangles traverse2pi integer multiples. The shortest nonconstant such length is2pi under either norm, attained by a single rank-one phase. For the usual bi-invariant HS Riemannian metric this also is the shortest nonconstant closed geodesic length. No arbitrary normalized bi-invariant metric is inferred from this one scalar normalization.

## 2. Anchor containment and endpoint safety

Fix n>=2,N>=1, basepoint p and a map Phi with intrinsic Lipschitz constant L<=1/2 on the unit-round geodesic sphere. A=Phi(p),W(x)=A*Phi(x) has

    d_nu(I,W(x))<=L d(p,x)<=L pi<=pi/2.

Either the above exact distance formula, or the simpler one-eigenvector path lower bound, implies that every eigenangle is in[-pi/2,pi/2]. By unitary spectral calculus Re W>=0. This conclusion is valid on the CLOSED sublevel, including eigenvalues i and -i.

For 0<=t<=1 and B=I+tW,

    B*B=(1+t²)I+t(W+W*)>=(1+t²)I.

Hence B is invertible with ||B^-1||op<=(1+t²)^(-1/2). At t=1 this is still a uniform bound; the forbidden eigenvalue -1 never occurs. The equality

    (W+tI)^*(W+tI)=(I+tW)^*(I+tW)

(with * denoting the adjoint) yields F_t(W)*F_t(W)=I for F_t(W)=(W+tI)B^-1. Direct substitution gives F_0(W)=W,F_1(W)=I,F_t(I)=I. No stabilization or limiting unitary group is used.

## 3. Noncommuting algebra and norm estimate

For arbitrary U,V in the closed right semicircle domain S, multiply F_t(U)-F_t(V) on the left by I+tU and on the right by I+tV. Each matrix commutes with its OWN polynomial/resolvent. The numerator is

    (U+tI)(I+tV)-(I+tU)(V+tI)=(1-t²)(U-V).

The tUV terms retain their order and cancel; U and V need not commute. Inverting both external factors gives

    F_t(U)-F_t(V)=(1-t²)(I+tU)^-1 (U-V)(I+tV)^-1.

For op, submultiplicativity gives the ideal estimate. For HS, positivity of B*B<=||B||op²I gives ||BX||HS<=||B||op||X||HS; applying the analogous right bound yields ||BXC||HS<=||B||op||X||HS||C||op. Therefore

    ||F_t(U)-F_t(V)||nu<=q_t||U-V||nu,
    q_t=(1-t²)/(1+t²).

Differentiating on the open invertibility domain independently gives DF_t(W)[E]=(1-t²)B^-1 E B^-1. In particular its norm is at most q_t||E||nu. This validates the published chain-rule route for absolutely continuous curves.

There is also a partition-only route that checks the same analytic obligation independently. For ANY continuous rectifiable curve C contained in S, apply the chordal estimate to every consecutive pair of a partition. Matrix-norm curve length contracts by q_t. Section1 identifies matrix-norm and intrinsic lengths of each of these curves, so intrinsic curve length contracts by q_t as well. This does not require geodesic convexity of S and does not infer an intrinsic arbitrary-pair bound just from chordal contraction.

## 4. Full intrinsic Lipschitz statement and deformation properties

For x,y on the connected sphere, take a minimizing spherical geodesic gamma. Its image under W stays in S because the anchor containment holds for EVERY point of the domain. The input image curve has intrinsic length at most L length(gamma), by applying the Lipschitz inequality to partitions; it is also matrix absolutely continuous. The preceding curve-length estimate and unitary left invariance give

    d_nu(H_t(Phi)(x),H_t(Phi)(y))
      <=length(H_t(Phi) o gamma)
      <=q_t L length(gamma)=q_t L d(x,y).

This proves the full claimed constant for all nonsmooth Lipschitz maps, all n>=2 and all finite N>=1. At antipodal x,y one simply chooses any minimizing geodesic. No target minimizing geodesic is required to remain in S. The estimate preserves the closed 1/2 and strict 1/2 sublevels because 0<=q_t<=1.

H_0 is the identity, H_1(Phi) is the constant A=Phi(p), and every constant map stays fixed, since its W is I. Also H_t(Phi)(p)=A for all t. Thus this is a strong deformation retraction onto the constant-map copy of U(N); on the based subspace A=I it is a contraction. It is not a contraction of the full unbased mapping space to one universal constant.

For S0 assigned angular distance pi, only its second value changes. Its principal-angle scalar transformation is

    g_t(theta)=2 arctan(((1-t)/(1+t))tan(theta/2)).

For |theta|<=pi/2 its derivative is (1-t²)/(1+t²+2t cos theta), between0 and q_t, with g_t(0)=0. Therefore |g_t(theta)|<=q_t|theta|. Applying the proved l2/max principal-angle distance formulas gives d_nu(I,F_t(W))<=q_t d_nu(I,W), hence exactly the two-point Lipschitz estimate. This covers the printed all-dimensions interpretation without using a path metric on disconnected S0.

## 5. Uniform topology, all parameter spaces and frames

For eligible Phi,Psi set delta=sup_x||Phi(x)-Psi(x)||nu and A=Phi(p),B=Psi(p). Then ||A-B||nu<=delta and

    ||A*Phi(x)-B*Psi(x)||nu
       <=||Phi(x)-Psi(x)||nu+||A-B||nu<=2delta.

Using unitarity and the proven chordal estimate gives

    sup_x||H_t(Phi)(x)-H_t(Psi)(x)||nu<=(1+2q_t)delta<=3delta.

For time continuity, compactness of[0,1]xS and inverse safety suffice. An optional explicit independent bound is partial_tF_t(W)=(I-W²)(I+tW)^-2. Its op norm is at most2 and HS norm at most2sqrt(N). Hence the same matrix-uniform metric has a time modulus at most c_N|t-s|. Combined with the preceding3delta bound this proves joint continuity. The exact principal-angle/chord formulas also show the matrix/intrinsic metrics induce the same compact-group topology and uniformly equivalent uniform mapping topologies. No stronger Lipschitz-norm topology is claimed.

For an arbitrary topological space Y and continuous Phi:YxS^(n-1)->U(N), evaluation at p gives a continuous A(y). Multiplication and inversion in the displayed formula are continuous at every admissible(y,x,t), proving continuity of the family directly. No local compactness, metrizability or compactness of Y is needed. For constant Q,R inU(N), the new normalized image is R*WR and the new anchor QAR. Conjugation covariance gives H_t(QPhiR)=QH_t(Phi)R. These conclusions concern trivial product families with fixed frames; no nontrivial sphere-fibration theorem is imported.

## 6. Adversarial boundary families and rejected generalizations

For N=1, Phi(x)=exp(i d(p,x)/2) has Lipschitz constant1/2 and argument range[0,pi/2]. The scalar derivative g'_t(theta) increases up to q_t as theta approaches pi/2 for0<t<1. Along a minimizing radial geodesic near the antipode, output/input local Lipschitz ratios approach q_t. Thus replacing q_t by a strictly smaller factor such as q_t² would be false. This is a direct analytic attack family; it supports the size of the claimed constant without adding a sharpness theorem to the paper's claimed contribution.

At W=-1,t=1/2 the angular derivative is3, while q_t=3/5; at t=1 the denominator vanishes. These outside-S examples show why the right-semicircle hypothesis is load-bearing. They are not counterexamples to eligible inputs.

For the NORMALIZED HS norm divided bysqrt(N), the loop diag(e^(i theta),1,...,1) has Lipschitz constant1/sqrt(N)<=1/2 when N>=4, but its determinant has winding one and cannot be deformed to a constant. The manuscript expressly uses unnormalized HS, so this normalization counterexample does not apply to it. It rejects an illicit metric generalization.

The weak logarithm observation for L<1 is also correct: anchor distance is at mostLpi<pi, so the spectrum avoids-1. The principal logarithm is continuous on that open matrix domain, and A exp((1-s)log W) continuously deforms to A. A fixed input map has positive spectral-cut margin by compactness. No single uniform margin as L approaches1 is needed for continuity on the union. At L=1 the scalar identity loop is noncontractible, so closing that weak threshold is unjustified. No preservation of a given Lipschitz sublevel is asserted for the logarithm route.

## 7. Actual primary interfaces and source scope

After INITIAL_SEAL, ordinary HTTPS fetched the actual 103-page Gromov author PDF, internal title/date October 1, 2017, and actual 572-page Neretin author-hosted2011 book. The locally authenticated source receipts retain exact status, ordered headers, bytes and hashes. Full bodies and selected extracts/pixels remain ignored under private-primary; no whole-book reading is claimed.

Gromov physical/printed 35 gives the unit sphere and stated standard bi-invariant target normalization, and physical/printed 36 contains the literal [?24](i) small-map question with bound 1/2 and continuity in the input. The nearby Lip<1 discussion and separate nontrivial-fibration question are distinct. These complete selected pages were read as text and pixels. The paper's two explicit metrics are compatible with its claimed normalization; no uniqueness of a metric from that normalization is assumed.

Neretin physical 54/printed 42, Subsection 1.7.9/Theorem 7.5, supplies the classical unitary/self-adjoint Cayley chart. Its signs were checked in pixels because extraction has legacy-font control characters. On the matrix chart where I+W is invertible, C(W)=(I-W)(I+W)^-1 obeys C(F_t(W))=((1-t)/(1+t))C(W), by single-matrix rational algebra. The manuscript claims no novelty for this chart or logarithm contraction, and does not depend on a chart parametrizing matrices with eigenvalue-1. No broader source theorem or priority judgment is inferred from these inspected interfaces.

## 8. Exact reproducibility and status

The independent read-only check_exact_readonly.py uses exact rational-function 2x2 calculations, an explicitly noncommuting boundary pair with one nontrivial principal phase each, independent product-rule and time derivatives, anchoring/frame covariance, Cayley algebra and scalar margin identities. It rejects a wrongly ordered product, a stronger q_t² factor and outside-domain endpoint invertibility. These 26 exact checks passed. They test algebra/transcription and boundary behavior; Sections 1–6 supply the universal proof for all dimensions/maps.

Both deposited diagnostic program bodies were fully inspected only after the initial seal. verify_exact.py was run once with an explicit previously absent own-lane --output destination; its 10 ordered-word algebra checks passed. Its default source-adjacent output was never used. The numerical program was not executed: its ordinary floating-point checks are optional diagnostics and cannot establish the universal metric/topological theorem. No copied fixture, source builder/finalizer, environmental setup, old audit programme or archived conclusion was needed. All 45 source files and the original source manifest remain byte-identical.

No substantive defect or unresolved central mathematical gap is identified. The complete original theorem and stated auxiliary boundaries/families/weak-logarithm observation survive these attacks. The standard finite-dimensional spectral theorem, elementary normed-space length facts and basic topology remain ordinary mathematical inputs, not proof-assistant certification. No external human peer review, historical-firstness or current-worldwide-openness clearance is claimed. Follow-up is null; public/editorial authority belongs to root and the full catalogue remains ongoing.
