# Independent early derivation — package 03

Frozen before reading candidate mathematical text or prior reviewer reasoning.
Target hypothesis: independent standard equal-H fBm components, the canonical
integral X = integral B1 dB2 on [0,T], H in (1/4,1), and every L2 estimator
measurable with respect to both complete uniform grids satisfy
RMS >= c_H T^(2H) n^(1/2-2H), with c_H > 0 independent of n,T.
No assertion at H=1/4 or H=1, no uniformity in H, and no assertion about
correlated components, unequal H, adaptive information, or nonuniform grids.

## Independent reduction

Use the real Hilbert space of deterministic fBm integrands, with
<f,g> = C_H integral fhat(xi) conjugate(ghat(xi)) |xi|^(1-2H) dxi.
For independent isonormal processes, the mixed double integral is isometric
to the tensor Hilbert space, with no factor 2. On [0,1], the target kernel is
h(u,v)=1_{0<u<v<1}. Its canonical meaning must be justified for H>1/4,
separately by Young integration above 1/2 and canonical Gaussian rough
integration in (1/4,1/2]; existence alone is not a lower-bound proof.

Let V span the n cell indicators (equivalently the complete n+1 grid values,
including the deterministic zero). With P its orthogonal projection,
E[X | both grids] corresponds to (P tensor P)h. This follows by splitting
each independent Gaussian process into its V and V-perpendicular parts.
Every square-integrable grid estimator has error at least the distance to
that conditional expectation. This establishes the universal estimator
quantifier, provided the exact kernel and isometry have been established.

## A possible localized dual mechanism

Choose a nonzero real smooth bump phi compactly supported in (0,1). Put
w(u,v)=phi'(u) phi''(v). Every cell-rectangle integral of a rescaled copy is
zero, while its triangle integral is -integral(phi')^2, which is nonzero.
For k=0,...,n-1 place w_k,n(u,v)=n^2 w(nu-k,nv-k) in the kth diagonal
cell and sum them. If qhat equals the Fourier transform of this sum divided
by C_H^2 |xi|^(1-2H)|eta|^(1-2H), its pairing with every tensor grid
indicator vanishes, and its pairing with h is -n integral(phi')^2.
Fourier conjugation must be checked: use the real symmetry
qhat(-xi,-eta)=conjugate(qhat(xi,eta)), not an unqualified complex pairing.

Each individual q has squared norm proportional to n^(4H). To obtain
the desired exponent the sum must have squared norm O_H(n^(4H+1)),
not the crude O_H(n^(4H+2)). A sufficient check is summability of the
translation Gram coefficients. With the product bump they factor into
Fourier coefficients of |phihat(xi)|^2 |xi|^(2H+1) and
|phihat(xi)|^2 |xi|^(2H+3). Vanishing moments remove the origin
singularity, rapid decay handles infinity, and an explicit integration or
fractional-kernel argument should prove summable off-diagonal products.
This is an independent mechanism sketch, not a claimed completed proof:
its exact remaining gap is a quantitative uniform-in-n Gram bound and
the normalization needed to obtain an explicit c_H.

If that bound holds, dual Cauchy-Schwarz yields MSE >= const_H n^(1-4H).
Self-similarity of the entire signal and information gives T^(4H) for
MSE and T^(2H) for RMS. The n=1 case must remain included in the bound.
At H=1/2 the weight is constant and disjoint cell supports are orthogonal;
the Brownian bridge contribution already gives a positive n^-1 RMS lower
bound. This is compatible with a sharp Brownian optimum but does not
claim its constant. As H approaches 1 the constants may vanish, which is
allowed; as H approaches 1/4 the canonical-existence boundary is excluded.

## Falsification conditions

A valid proof fails if its witness is not a real Hilbert vector, if the
kernel represents a different area convention, if grid orthogonality only
covers one component, if it supplies only a linear-estimator bound, if
off-diagonal terms accumulate faster than n, or if the variance/isometry
has an unaccounted factor. Numerical checks cannot prove general-H
integrability, universal quantifiers, or an interval-certified constant.
Priority, novelty, and worldwide openness remain unknown until source
work and cannot be inferred from this derivation.
