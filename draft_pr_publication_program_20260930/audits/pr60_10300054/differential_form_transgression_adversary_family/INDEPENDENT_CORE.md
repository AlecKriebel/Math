# Differential-form core derived before candidate/checker

Derivation recorded from the literal problem and ordinary exterior algebra, before candidate or historic/fresh reviewer bodies. Assume global sufficiently regular forms on an oriented3-manifold: alpha nowhere zero and d alpha=alpha wedge omega. The pointwise sign target requires an orientation; integrated/cohomological claims require appropriate closedness/boundary hypotheses. No minimality, tautness or atoroidality is used in these identities; those are crucial to the unsolved geometric question, not consequences of algebra.

Applying d twice gives alpha wedge d omega=0. For a transverse vector field X normalized by alpha(X)=1, contraction gives d omega=alpha wedge eta with eta=i_X d omega. Consequently d omega wedge d omega=0 and omega wedge d omega is closed even without using the ambient3-dimensional top-degree shortcut.

All global coorientation-preserving defining forms are alpha'=e^f alpha: a nowhere-zero scalar multiple with positive ratio has a global logarithm. The defining equation then forces omega'=omega-df+g alpha for a global scalar g, because alpha wedge (omega'-omega+df)=0. A coorientation-reversing ratio is constant-sign on each connected component, and -e^f alpha obeys the same omega formula. No positive factor varying through zero is allowed.

Write GV=omega wedge d omega. Direct expansion gives

    GV'-GV = -df wedge d omega + dg wedge d alpha
              -df wedge dg wedge alpha -g df wedge d alpha.

Thus the exact2-form primitive is

    T = g d alpha -f d omega +g df wedge alpha,
    GV'-GV = dT.

Equivalently T'=df wedge omega +g alpha wedge (omega-df); T'-T=d(f omega). All signs follow from d(a wedge b)=da wedge b+(-1)^degree(a) a wedge db. If g is instead the coefficient of alpha', substitute g=e^f h before differentiating: the two parameterizations are not interchangeable without this factor.

For fixed alpha (f=0), the entire ambiguity is omega->omega+g alpha and the defect is d(g d alpha). A closed M then has unchanged total integral by Stokes; a region with boundary has boundary term integral_boundary T, and arbitrary boundary terms must not silently be discarded. On a saturated smooth boundary where alpha pulls back to zero, the primitive T pulls back to zero, as do d alpha and d omega there; this explains a special boundary invariance, not arbitrary regional integral invariance.

Successive gauges have composition (f1,g1) then (f2,g2) = (f1+f2,g1+e^f1 g2) relative to the original alpha. This independently controls global parameter normalization.

Useful honest smooth controls: on R3, alpha=dz, omega=0, f=x, g=y gives alpha'=e^x dz, omega'=-dx+y dz, GV'=-dx wedge dy wedge dz. This local exact3-form is not a closed-manifold example with nonzero evaluatedGV. On T3 take f=sin x, g=sin y and alpha=dz; then GV'=-cos x cos y dx wedge dy wedge dz changes sign and has zero total integral. This is a gauge diagnostic on a toroidal nonminimal zero-GV product foliation, not a counterexample to Q13.1. Irrational closed alpha can make a linear torus foliation minimal/taut, but atoroidality and nonzeroGV still fail; no target counterexample follows.

Exact remaining geometric gap: the image of the gauge map (f,g)->GV+dT is constrained. A positive top-degree representative of the same nonzero cohomology class on a closed connected oriented manifold need not be shown to arise from this gauge map. Establishing that constrained pointwise sign realization is the central unsolved step. No abstract DGA identity, local contact example, exactness or nonzero total integral resolves it.

Regularity qualification: the displayed pointwise calculations require enough regularity to define omega and d omega as ordinary forms and the displayed primitives/derivatives. Calegari states C2 suffices for the invariant; its precise relationship to these chosen global form regularities needs primary/convention checking, not an automatic extra smoothness assumption. Smooth controls verify signs but cannot settle a C2-to-smooth reduction.
