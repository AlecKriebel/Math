# Incident segments in the cofactor normal form

The [cofactor proof](COFACTOR_NORMAL_FORM.md) incorporates a mandatory correction accepted by the [independent audit](INDEPENDENT_COFACTOR_ACCEPTANCE.md). No numerical example or polynomial coefficient changes.

For an incident triangle T_i the formula is

    q_i-p_v = x_v s_i L_i L_(i+1)/a_i.

It follows that q agrees with p_v on each incident edge segment. Each of the two adjacent polynomial pieces also agrees with p_v on the entire supporting line by polynomial continuation. It does not follow that the piecewise function uses one of those pieces on the opposite ray. Thus the earlier statement of agreement on every full incident supporting line was false.

The four-star in the proof already demonstrates this: for 0<t<1,

    (-t,0)=(t/14)d_1+(5t/14)d_2,
    q(-t,0)-p_v(-t,0)=5t²/14.

The point lies in a different sector from the incident positive horizontal ray.

The corrected three-ray lemma requires three nondegenerate incident edge segments with distinct supporting lines on which q is zero. Since q=p_v on those segments and p_v has zero value and gradient at the vertex, p_v is a homogeneous quadratic vanishing on three distinct lines. Hence p_v=0, and q vanishes on every incident edge segment. No assertion about a nonincident opposite ray follows.

A second exact control in [THIRD_PASS_CERTIFICATES.json](THIRD_PASS_CERTIFICATES.json) has three full zero lines but is nonzero on the opposite ray of a fourth incident direction. This also refutes the literal whole-line conclusion, rather than merely showing that its old proof was incomplete.

In the direct macro-patch construction, this corrected lemma is applied only where there is an actual full even fan and the quartic proportionality is imposed. Three incident macro-edge segments on distinct supporting lines then force every neighboring micro-vertex value to vanish, so each incident patch amplitude is zero. An odd macro star or an invented exterior fan is not covered.

The [pencil-collapse proof](THIRD_PASS_CEVA_OBSTRUCTION.md) has a separate, non-substantive clarification: its lemma now repeats that all twelve vertices are distinct, as already required by the fixed conforming-realization model. This is essential when ruling out projectively coincident nonadjacent vertices, and does not impose a new generic-position assumption.
