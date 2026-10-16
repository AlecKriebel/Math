# Independent stationary control for the source convention

Checked 2026-10-13 UTC. This derivation is independent of the candidate's nonstationary construction.

Take S = P^1, E = O(1) + O(1), X = P^1_s x P^1_z and L = O_E(2) = O(2,2), using f_*O_E(1) = E. In affine compatible frames set

Phi(s,z) = b(s) + 2 log(1 + |z|^2),  b(s) = 2 log(1 + |s|^2).

It is the product positive metric on L. With any fixed positive area convention dA_z,

I(s) = integral exp(-Phi(s,z)) dA_z
     = C exp(-b(s)).

The normalized fiber curvature measure and exp(-Phi)dA_z/I(s) are the same Fubini-Study probability measure. Consequently the right hand side of Naumann's published (13) is identically zero: Phi_t = Phi for every t. Its horizontal geodesic curvature is

c(Phi) = b_{s bar s} = 2/(1 + |s|^2)^2 > 0.

Its mixed derivatives vanish, its horizontal lift is partial_s, its Kodaira-Spencer tensor A is zero, and c is constant along each fiber. Therefore

Delta_fiber c = 0,
partial_s partial_bar_s log I = -c,
partial_t c = 0.

The right side of published (14), with its printed r c term and the Section 3.3 declaration that exp(-Phi_t) is the metric on O_E(r), instead becomes

r c - c = (r - 1)c = c   (r = 2).

This contradicts the actual zero derivative. The contradiction is insensitive to the Laplacian sign, to normalization constants, and to the fiber-volume convention. With the report's unnormalized MA numerator the metric weight changes by a function of time only, leaving c unchanged.

In compatible frames, the defining equation (13) in fiber dimension one is

Phi_t = log(Phi_{z bar z}) + Phi + log I + C_0.

The coefficient of Phi is one. At a stationary central fiber where first base derivatives vanish, its horizontal second derivative w obeys

w_t = Delta_F w + w - integral w dmu_F.

A factor r can arise when one passes to the O_E(1) weight psi = Phi/r and also rescales time. However then the Laplacian, the evolution variable, and the exponent in I must be changed consistently. A bare substitution of r for one in the O_E(r)-weight equation is not such a change of convention.

Audit implication: the published defining equation (13) and printed Proposition 4/(14) cannot both hold literally under the notation explicitly stated in Section 3.3. The candidate's direct differentiation of (13) is the appropriate route for its declared theorem. This control does not establish all details of the candidate's nonstationary example.

