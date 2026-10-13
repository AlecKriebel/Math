# Independent fixed-alpha transport and full gauge flux

For a chosen smooth oriented volume mu on M define W by i_W mu=d alpha. Since alpha wedge d alpha=0, W is tangent to the foliation. Since d2alpha=0, div_mu W=0. Write omega wedge d omega=b mu. For fixed alpha and omega'=omega+g alpha, the transgression is

    b'=b+W(g).

This identifies the precise constrained range of the fixed-alpha gauge: a derivative along one divergence-free leafwise vector field, not an arbitrary exact3-form. Zeros of W and integrals against W-invariant measures give potential fixed-alpha obstructions. For a closed periodic orbit of W, the time integral of W(g) vanishes. Such an obstruction is not a full-gauge or Q13.1 counterexample: rescaling alpha also changes W and may remove it.

In oriented Euclidean coordinates write alpha=A dot dx and omega=Omega dot dx. Then curl A=A cross Omega by the defining equation, and alpha wedge d omega=0 says A dot curl Omega=0. Set W=curl A. Full gauges have Omega'=Omega-grad f+g A and A'=e^f A, so

    b'-b=grad g dot W-grad f dot curl Omega
          -grad f dot(grad g cross A)-g grad f dot W.

The exact flux vector representing the primitive T from INDEPENDENT_CORE.md is

    J=g W-f curl Omega+g(grad f cross A),
    b'-b=div J.

This provides a materially distinct coordinate/vector-calculus sign check of the exterior-algebra expansion, and shows where integration cancels while pointwise density need not. Orientation reversal negates the volume coefficient b but not the3-form itself. No physical units or numerical tolerances enter these purely geometric identities.
