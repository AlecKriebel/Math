# Independent differential-form verification

This verifies the smooth gauge reduction, not Calegari Question 13.1. Let M be a smooth manifold, alpha a nowhere-zero smooth 1-form, and omega a smooth 1-form satisfying d alpha=alpha wedge omega. Pointwise signs below use an orientation; integrated claims use a closed oriented3-manifold unless a boundary term is explicitly retained. The identities themselves do not require minimality, tautness or atoroidality.

## All smooth gauges and closedness

Differentiating the defining equation gives

    0 = d alpha wedge omega - alpha wedge d omega
      = -alpha wedge d omega.

Choose a smooth transverse vector field N with alpha(N)=1. Contracting alpha wedge d omega=0 gives d omega=alpha wedge i_N(d omega). It follows that d omega wedge d omega=0, and hence d(omega wedge d omega)=0 in any ambient dimension. In dimension 3 this also follows from top degree, but that shortcut does not explain the foliation identity.

Every smooth defining form with the same coorientation is alpha'=e^f alpha with a globally defined smooth real f. A positive nowhere-zero ratio has a global logarithm. If alpha' wedge omega'=d alpha', then

    alpha wedge (omega'-omega+df)=0.

For a nowhere-zero alpha, this forces omega'-omega+df=g alpha for a global smooth scalar g. Thus all such pairs are

    alpha'=e^f alpha,  omega'=omega-df+g alpha.

On a connected component a negative ratio has the form -e^f; reversing coorientation leaves the same parameterization of the auxiliary 1-form after absorbing the sign into its scalar coefficient. Ratios through zero are inadmissible.

## Exact transgression, including the mixed term

Write B=omega-df+g alpha. Since dB=d omega+dg wedge alpha+g d alpha, expand B wedge dB. The terms omega wedge g d alpha and g alpha wedge d omega vanish, as does every term containing alpha twice. The remaining change is

    B wedge dB - omega wedge d omega
      = -df wedge d omega + dg wedge d alpha
        -df wedge dg wedge alpha -g df wedge d alpha.

The signs are checked by differentiating the actual 2-form

    T = g d alpha -f d omega +g df wedge alpha.

Indeed dT is exactly the displayed change. A second primitive is

    T_alt = df wedge omega +g alpha wedge (omega-df),
    T_alt-T = d(f omega).

For the author's coefficient h of the NEW defining form, put g=e^f h and alpha_f=e^f alpha. Since d alpha_f=e^f(d alpha+df wedge alpha), substitution gives

    T = -f d omega +h d alpha_f,
    B wedge dB = omega wedge d omega-df wedge d omega+dh wedge d alpha_f.

This proves the author's formula(2.3), including its normalization. Constant h has no effect on this 3-form. A constant coefficient of the ORIGINAL alpha after a nonconstant rescaling need not have that property. Successive original-coefficient gauges compose as

    (f1,g1) followed by (f2,g2)
       = (f1+f2, g1+e^f1 g2).

On a closed oriented M, Stokes gives equality of total integrals. On an arbitrary region U, the integral changes by integral_boundary(U) T. For a smooth saturated boundary, pullback alpha=0, pullback d alpha=0 and pullback d omega=0, so pullback T=0. This special case does not justify dropping arbitrary boundary terms.

## Vector-field interpretation and the strict-sign boundary

Fix a smooth positive volume form nu on a closed3-manifold. Define v, Y and X_f by

    omega wedge d omega=v nu,
    i_Y nu=d omega,  i_X_f nu=d alpha_f.

Cartan's formula gives L_Y nu=L_X_f nu=0 because the contracted 2-forms are closed. The identity lambda(V) nu=lambda wedge i_V nu shows alpha_f(Y)=alpha_f(X_f)=0. Also df wedge d omega=(Yf)nu and dh wedge d alpha_f=(X_fh)nu. Therefore

    B wedge dB = (v-Yf+X_fh) nu.

For fixed f, an invariant probability measure mu of the complete X_f flow satisfies integral X_fh dmu=0. A necessary condition for nonnegativity is consequently integral(v-Yf) dmu>=0 for EVERY such measure. The normalized volume is only one of these measures. Rescaling f changes X_f and the other invariant measures, so a failure for one fixed f is not a counterexample to the full problem.

At a zero of X_f, d alpha_f=0 and alpha_f wedge(omega-df)=0. Thus omega-df is proportional to alpha_f there. Since alpha_f wedge d omega=0, the base density (omega-df) wedge d omega vanishes at that point; the X_fh term also vanishes. Strict positivity would force the tangent vector field X_f to be nowhere zero and thus the Euler class of the oriented tangent 2-plane bundle to vanish. Nonnegative forms with zero loci are not excluded by this argument.

## Regularity and the exact unresolved step

These statements classify all SMOOTH gauges of a smooth defining pair. REGULARITY.md separately proves a valid distributional extension for alpha C¹, omega continuous with continuous weak d omega, and C¹ gauge functions. It does not show that every auxiliary choice admitted by the original C² problem is captured by smooth gauges, or that a semidefinite representative survives a smooth approximation.

The exact smooth existence question is whether the geometric hypotheses supply f,h with v-Yf+X_fh>=0 everywhere after orienting M so its total Godbillon-Vey number is positive. A volume-form representative of the same top-degree cohomology class does not establish that it belongs to the constrained image of this gauge map. Neither an abstract exterior identity, a local contact calculation, nor a fixed-flow obstruction supplies the missing global gauge choice. The original C² question remains unresolved by the candidate and this verification.
