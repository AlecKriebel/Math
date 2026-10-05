# Independent reconstruction before reading ROOT gates or prior reviews

This artifact was written after reading the frozen TeX/code, submitted original proof, original Krener pp. 674–675, Nash printed p. 59 and Hatcher printed pp. 51, 61, 66–67. No earlier review report or ROOT gate was used to establish this reconstruction.

## Claim and assumptions

Fix one T>0. The history uses the actual unweighted Euclidean output on [0,T), and the metric is its differential L2 pullback. The permitted domain is a smooth connected state manifold; output dimension is any finite p. A meaningful fixed chart normalization or a fixed positive background metric is used for uniform state bounds. This does not assert constants uniform in T. The two-dimensional example avoids sectional-two-plane vacuity.

## Geometry reconstructed

Take an oriented regular hyperbolic octagon with angle pi/4. Opposite-side boundary directions reverse under orientation-preserving plane isometries: [v_i,v_(i+1)] maps to [v_(i+5),v_(i+4)]. Endpoint equivalence generated this way has one class. The oriented link continuation follows addition by 5 modulo 8, so visits all corners. Developing eight wedges has total angle 2pi. The closing hyperbolic isometry fixes their common vertex; its derivative is identity after the complete angular turn. A point and oriented tangent frame determine a hyperbolic isometry, so the closing isometry is identity, not a nontrivial rotation. Thus the developed neighborhood is a disk, not a cone or branched vertex. Interior-edge neighborhoods glue from two half disks. No polygon-side letters are needed for the abstract standard surface presentation. V=1,E=4,F=1 gives chi=-2, and orientation gives genus 2.

The center–vertex–midpoint triangle has angles pi/8,pi/8,pi/2, yielding cosh R=cot(pi/8)^2=3+2sqrt(2). Disk radius r=tanh(R/2) satisfies r^2=(cosh R-1)/(cosh R+1)=1/sqrt(2), hence r=2^(-1/4). This checks the concrete radius against the angle specification.

A character from the genus-two group onto Z/2, a1->1 and b1,a2,b2->0, is well-defined since the relator is a product of commutators. Its kernel has index 2. S is path connected, locally path connected and semilocally simply connected, so Hatcher supplies a connected covering; sheet count is the index. Smooth base charts lifted to sheets define the smooth structure with projection a local diffeomorphism. Pulling back orientation and metric is legitimate. A finite family of compact coordinate neighborhoods contained in evenly covered open sets covers the compact base; their preimages are two compact copies apiece. Thus M is compact. Lifted cells give chi=-4, hence genus 3. No branched points or disconnected double copy occurs.

Nash Theorem 2 printed p.59 explicitly covers C^k positive metrics for 3<=k<=infinity, gives dimension (n/2)(3n+11), and nearby text explicitly prevents self-intersections. Its smooth compact input applies to S and gives a globally injective C^infinity isometric embedding e:S->R17. The global injectivity imported here is essential to exactly two, as opposed to at least two, histories.

## Exact dynamics and metric

f=0 is complete on all real times. Its flow and tangent map are identities; in any fixed chart around the constant trajectory Df=0, Phi=I, H=Dh. Therefore
P_T(v,w)=T<d(e o pi)v,d(e o pi)w>=Tg(dpi v,dpi w)=T pi*g(v,w).
This uses the actual output and exact forward time integral; it is not an auxiliary negatively curved metric or an empirical Gramian. Removing the endpoint T changes no integral.

A local isometry preserves curvature, so K(pi*g)=-1. Constant positive metric scaling leaves the connection unchanged and scales sectional curvature by 1/T, hence K(P_T)=-1/T. Compactness gives geodesic completeness: each fixed-energy sphere bundle is compact, and the smooth geodesic vector field can be continued for all time on it. Zero energy is constant. This argument does not assume simple connectivity.

## Bounds and boundaries

For any fixed smooth positive q, the q-unit tangent bundle is compact. The positive continuous pi*g(v,v) on it has min c>0 and max C<infinity. By homogeneity Tcq<=P_T<=TCq; c,C depend on q, not T. Center local isometry charts at 0 in the Poincare disk and restrict them to some open radius <=1/2. They need only be sufficiently small to inject, not all have radius 1/2. A finite subcover exists. Writing s=u^2+v^2<=1/4 gives [P_T]=4T/(1-s)^2 I. Since 3/4<=1-s<=1, 4T I<=P_T<=64T/9 I. Independently, lower difference is 4s(2-s)/(1-s)^2, upper difference 4(1-4s)(7-4s)/(9(1-s)^2); every factor has the claimed sign. The upper bound may be attained only on a chart boundary if its image is open, which is harmless for a weak bound.

The conformal formula independently verifies curvature: lambda=4T/(1-s)^2, phi=(1/2)log lambda, Delta phi=4/(1-s)^2, K=-lambda^(-1)Delta phi=-1/T. At T=0, P is zero and no Riemannian curvature is defined; the theorem explicitly excludes it. As T->infinity K approaches 0, so no uniform negative constant is asserted across all T. Arbitrary rescaling z->az yields coefficient matrix a^(-2)P, ruling out one nonzero universal lower bound over every chart normalization.

## Histories

For T>0, constant histories are equal iff their values at t=0 are equal. Since e is injective, h(x)=h(x') iff pi(x)=pi(x'). Each fiber has exactly two distinct states. The equivalence relation persists for all real times. On a sufficiently small single covering sheet, pi and e are injective, so h and histories are locally injective. Histories outside the attained image have no preimages. No condition of the original two-page Krener conjecture excludes the construction; its output-normalization parenthesis imposes no additive noise requirement. The printed some-T>0 quantifier is satisfied at T=1.

## Adversarial attempts and exact gap

Tried failure modes: opposite-side orientation and disconnected link; nontrivial vertex holonomy; incompatible standard presentation; trivial character/disconnected cover; compact-base versus nonproper infinite cover; merely C1 Nash immersion; Gramian/auxiliary-metric confusion; changed curvature under constant scaling; T=0 and all-T uniformity; noninjecting fixed radius chart; histories outside image; continuous map with additional non-cover collisions; simple-connectivity silently assumed. The analytical argument above resolves each. The strongest verified result is exactly the printed theorem, under the disclosed fixed-normalization meanings. No mathematical gap identified in this independent reconstruction. Novelty and source equivalence remain a separate audit; no historical conclusion follows from the proof or finite code.
