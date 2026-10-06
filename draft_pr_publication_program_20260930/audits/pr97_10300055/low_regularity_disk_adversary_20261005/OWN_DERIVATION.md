# Independent analytic derivation

This derivation was formed without reading the old review/REVIEW.md or any new reviewer's findings. Original author effort is 2/5; this document records verification, with zero additional central proof-search turns.

## Distributional differentiation at C1

Work in a smooth chart. For a C1 one-form alpha, its exterior derivative is a continuous two-form, and d(d alpha)=0 as a distribution because mixed distributional derivatives commute. The assumed equation identifies d alpha with the C1 two-form alpha wedge omega. Consequently its distributional exterior derivative is the ordinary continuous three-form

    d alpha wedge omega - alpha wedge d omega.

The first term is (alpha wedge omega) wedge omega=0. Thus alpha wedge d omega is the zero distribution. Its coefficients are continuous, so they vanish at every point. No second classical derivative of alpha, smooth foliation, or low-regularity flow is needed.

The other vanishing terms in the constant pencil are omega wedge d alpha=omega wedge alpha wedge omega=0 and alpha wedge d alpha=0. Therefore beta_s=omega+s alpha has precisely the contact three-form of omega for every *constant* real s. A variable function would add omega wedge dh wedge alpha, which is not generally zero.

## Compact interval, approximation, and smooth Gray

A global contact form orients the manifold; on a connected component its contact volume has constant sign. Reverse the chosen ambient orientation on the negative components. A compact smooth manifold has finitely many components, so a common set of finite bounds suffices. Fix a Riemannian norm and positive volume form. Since alpha is nowhere zero, m=min ||alpha|| is positive. The normalized covector alpha+omega/S converges uniformly to alpha and defines the same cooriented planes as omega+S alpha for S>0. This proves uniform convergence of the pencil endpoint to the original foliation.

Let U be the C0 neighborhood provided by the imported taut-foliation theorem, in the chosen positive orientation. Pick a finite S with ker(beta_S) strictly inside U. Compactness of M times [0,S] gives finite bounds B for ||beta_s|| and ||d beta_s|| and a minimum c0>0 for the original contact volume. If e_s=(eta-omega)+s(a-alpha), then C1 approximation errors below delta/(1+S) make both ||e_s|| and ||d e_s|| at most delta. The wedge estimate

    ||(beta_s+e_s) wedge d(beta_s+e_s) - beta_s wedge d beta_s||
        <= 2 B delta + delta^2

holds uniformly. Choose delta so this is below c0/2, and shrink the approximation errors again to keep the endpoint in U. Smooth forms a and eta can be chosen by ordinary chartwise smoothing of C1 sections and a smooth partition of unity. The form a need not be integrable and need not obey the original relation; the quantitative estimate replaces that identity for the smoothed path.

The family eta+s a is a smooth family of smooth contact forms on the finite closed interval. Smooth Gray stability on the closed manifold relates all its plane fields. Its endpoint is tight by U, so eta is tight. This proves the following strong fact without giving any definition to tightness of a rough distribution:

**Every sufficiently C1-close smooth contact form eta has the usual smooth tightness property.**

In particular, if omega itself is smooth, choose eta=omega. Only alpha needs smoothing. The usual tightness conclusion follows even when the foliation and alpha are not smooth.

## Simultaneous disk and contact-form smoothing

Suppose theta is C1 and f:closed D2 -> M is a C2 embedding whose boundary gamma is Legendrian and whose disk planes are distinct from ker(theta) along the boundary. Approximate f in C2 by smooth embeddings f_j. Compact-domain C1 embedding openness preserves embedding for sufficiently close approximations. One can obtain the approximation by local smoothing in an ambient Euclidean embedding and a smooth tubular retraction to M. This is ordinary approximation of an embedding; it is not approximation of the foliation or a Legendrian-preserving embedding theorem.

Let sigma be a fixed smooth knot sufficiently C1 close to gamma. The oriented ambient three-manifold gives its oriented rank-two normal bundle, which is trivial over S1. Pick a smooth tubular map H:S1 times B_R -> M. If sigma was chosen sufficiently close, the projection of gamma onto S1 has positive derivative and degree one. The same holds for gamma_j. Reparametrize each boundary by this projection. In this *fixed* chart the boundaries are graphs gamma=(t,U(t),V(t)) and gamma_j=(t,U_j(t),V_j(t)); the graph functions converge in C2. This follows from C2 convergence and continuity of inverse/reparametrization on the set with projection derivative bounded away from zero.

Choose smooth theta_j -> theta in C1 and let q_j(t)=theta_j(gamma_j'(t)). In chart coefficients A_j,k, differentiation gives

    q_j' = sum_(k,l) partial_l A_j,k(gamma_j) gamma_j,l' gamma_j,k'
           + sum_k A_j,k(gamma_j) gamma_j,k''.

C1 convergence of the coefficient functions, C2 convergence of the graphs, and uniform continuity of D theta make this tend uniformly to the derivative of theta(gamma'), which is the derivative of the identically zero function. Thus q_j -> 0 in C1. Only C1 graph convergence would not suffice: for theta=du-v dt and gamma_n=(t,n^-2 sin(nt),0), q_n'= -sin(nt) has supremum one, despite gamma_n converging in C1. The candidate uses exactly the needed C2 approximation.

Choose a smooth cutoff chi supported in B_(R/3), equal to one near its center, with all graph centers in B_(R/3). Then the translated supports lie in B_(2R/3), at a fixed positive distance from the tubular boundary. The correction

    C_j = q_j(t) chi(u-U_j(t),v-V_j(t)) dt

is a smooth one-form supported strictly inside the fixed tubular chart and extends smoothly by zero. The symbol dt is the global smooth angular one-form on S1, so a globally single-valued real angular coordinate is unnecessary. Its derivatives include

    partial_t C_j coefficient = q_j' chi
        - q_j (U_j' partial_1 chi + V_j' partial_2 chi),
    partial_u C_j coefficient = q_j partial_1 chi,
    partial_v C_j coefficient = q_j partial_2 chi.

Since the first graph derivatives stay uniformly bounded, there is a constant K independent of j for which ||C_j||_C1 <= K ||q_j||_C1. Therefore hat(theta_j)=theta_j-C_j tends to theta in C1 and is contact for large j. Along gamma_j, chi=1 and dt(gamma_j')=1, so the boundary is exactly Legendrian for the corrected form.

The plane-separation angle between TD and ker(theta) has a positive minimum on the compact boundary. C1 convergence of f_j and uniform convergence of theta_j-C_j preserve that separation for the new disk. Hence f_j(D2) is an overtwisted disk for the *smooth* corrected contact form by the verified smooth criterion. Any C2 boundary-criterion disk for the original C1 theta therefore yields arbitrarily C1-close smooth overtwisted forms.

Combining this lemma with the close-smooth-form tightness fact excludes every such embedded C2 disk for omega. This argument does not establish or need a theorem stating that every overtwisted C1 distribution has a C-infinity Legendrian-boundary disk. It also does not use C1 Gray stability or C1 Darboux coordinates.

## Strongest directly established scope

1. Smooth omega: usual tightness, under the original closed, cooriented, taut C2-foliation assumptions and the C1 relation with nonzero alpha.
2. C1 omega: no embedded C2 disk with Legendrian boundary and everywhere distinct boundary tangent/contact planes.
3. C1 omega: all sufficiently C1-close smooth contact forms are tight in the usual smooth sense.

There is no identified gap in answering Calegari Question 13.2 under the usual smooth contact-form interpretation. The extra C1 extension should state its disk-based meaning explicitly rather than assert an unverified equivalence with every possible low-regularity formulation of overtwistedness. Neither result constructs the assumed contact connection form or settles Question 13.1.
