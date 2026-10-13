# Independent invariant derivation (written before reading submitted checker)

Let S be a closed connected smooth hyperbolic surface, pi:M->S a connected smooth covering of degree two, and e:S->R^p an injective smooth isometric embedding. Put f=0 and h=e composed with pi. Assume T>0.

1. **Flow and linearization.** The unique solution of dx/dt=0 with initial x is x(t)=x for every real t. The flow phi_t=id_M has tangent map d(phi_t)_x=id_(T_xM). In a fixed state chart containing x, F(t)=D f(x)=0 and the fundamental matrix solves dPhi/dt=0 with Phi(0)=I; hence Phi(t)=I. This assertion uses the same chart/frame at initial and final time. A time-dependent external frame may display a different matrix, but the intrinsic map remains identity.

2. **History-map differential and Gramian.** Define Y_T:M->L2([0,T],R^p) by Y_T(x)(t)=h(phi_t(x)). Here Y_T(x) is the constant function h(x). Thus dY_T(x)v is the constant function dh_x(v). By the L2 inner product,

   P_T(x)(v,w)=<dY_T(x)v,dY_T(x)w>_(L2)
   =integral_0^T <dh_x(v),dh_x(w)> dt
   =T<de_(pi(x)) d pi_x(v),de_(pi(x)) d pi_x(w)>
   =T g_(pi(x))(d pi_x(v),d pi_x(w))=T(pi^*g)_x(v,w).

   This agrees with the source matrix integral. The chain rule and e's isometry, not a sampled matrix or an arbitrary chosen metric, are the exact links from observations to geometry.

3. **Exact fibers and local injectivity.** Equality Y_T(x)=Y_T(x') in L2 is equivalent to h(x)=h(x') for T>0 because the squared L2 distance is T times |h(x)-h(x')|^2. Injectivity of e makes this equivalent to pi(x)=pi(x'). Every history in Y_T(M) consequently has exactly two preimages. Histories outside Y_T(M) have no preimages. Around each x choose one sheet above an evenly covered neighborhood U of pi(x). On that sheet pi is a diffeomorphism; composing with e makes h and Y_T injective there. Its tangent map has rank dim(M) because d pi is invertible and de is injective.

4. **Metric positivity and fixed background bounds.** pi^*g is positive definite because d pi is invertible. It is smooth. On compact M, relative to any fixed smooth positive definite background q, the continuous generalized Rayleigh quotient on the q-unit tangent bundle attains a strictly positive minimum c and finite maximum C. Thus c q<=P_1<=C q. This is an exact compactness proof and is independent of any finite grid.

5. **Poincare chart bounds for all points.** In any sufficiently small hyperbolic isometric disk chart centered at 0,

   P_T=4T/(1-u^2-v^2)^2 I_2.

   On r^2=u^2+v^2<=1/4, 3/4<=1-r^2<=1, so 4T<=4T/(1-r^2)^2<=64T/9. This establishes the sharp weak bounds on a closed radius-1/2 disk. Charts are open and can be restricted to r<1/2 (or to a smaller radius); the same weak bounds hold. Each point has such a restricted chart around its origin. A finite subcover exists by compactness. There is no claim that every radius-1/2 hyperbolic disk embeds in M or that bounds survive arbitrary coordinate rescaling.

6. **Curvature and completeness.** pi is a local isometry for pi^*g, so its Gaussian curvature is -1. Equivalently, for lambda=4T/(1-r^2)^2 and metric lambda(du^2+dv^2), the conformal formula K=-(1/(2lambda))Delta(log lambda) gives K=-1/T: Delta(log lambda)=8/(1-r^2)^2. In 2D Gaussian and sectional curvatures agree. For a constant scaling T g, the Levi-Civita connection and affinely parameterized geodesic equation are unchanged; hence geodesic completeness persists. Compactness already ensures completeness for each T>0.

7. **Boundary cases.** T=0 gives a zero Gramian and loses distinguishability even locally, so is excluded by positive definiteness. T approaching 0 has no common positive lower bound across all T; T approaching infinity has no common finite upper metric bound or fixed negative curvature constant across all T. The problem fixes a positive interval length, and the submission's 'any fixed T>0' statement is correct. Changing the observation units by scalar a scales the Gramian by a^2 and curvature by a^-2; no invariant global-fiber conclusion follows from such scaling.

These deductions are conditional only on the stated standard existence inputs (hyperbolic compact surface, degree-two covering, smooth isometric embedding). Independent exact computational tests should exercise coordinate invariance, upper half-plane curvature, connection/curvature scaling, metric compatibility, nonorthogonal chart changes, and failed hypotheses at T=0, instead of only repeating the submission's sampled disk grid.
