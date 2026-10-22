# Exact moment formulation at a non-simple boundary vertex

This example checks that the theorem applies beyond local affine cube/simplex models. It is not the proof of the general theorem, and a numerical SDP is not used as a certificate.

## Square pyramid and objective

Let

    K = {(x,y,z) : 0<=z<=1, -z<=x<=z, -z<=y<=z},
    f(x,y,z)=z.

K is a compact convex body in R^3. Its unique minimizer is the apex (0,0,0), incident to four facets, with four extreme rays in its tangent cone. A cube or simplex vertex in dimension three has three incident facets and three tangent-cone extreme rays. An invertible affine change preserves these incidences. Thus the apex is not locally affine-equivalent to any boundary point of a three-dimensional cube or simplex. In particular a local cube/simplex argument does not directly settle this vertex.

For integers a,b,c>=0, direct integration gives

    mu(a,b,c) = integral_K x^a y^b z^c dx dy dz
              = 0, if a or b is odd;
              = 4/((a+1)(b+1)(a+b+c+3)), otherwise.

Indeed, for even a,b the integrals over x and y are 2z^(a+1)/(a+1) and 2z^(b+1)/(b+1), after which the remaining z integral is elementary. In particular vol(K)=4/3.

## Full hierarchy: an exact generalized eigenvalue

Let I_r={alpha in N^3 : |alpha|<=r} and v_r=(x^alpha)_{alpha in I_r}. Define rational matrices

    H_r[alpha,beta] = mu(alpha_1+beta_1,alpha_2+beta_2,alpha_3+beta_3),
    Z_r[alpha,beta] = mu(alpha_1+beta_1,alpha_2+beta_2,alpha_3+beta_3+1).

H_r is positive definite: a nonzero real polynomial cannot vanish on the interior of K, so its squared integral over K is positive. For every nonzero coefficient vector c,

    integral_K z(c^T v_r)^2 / integral_K (c^T v_r)^2
       = (c^T Z_r c)/(c^T H_r c).

Any SOS q of degree<=2r is a sum of squares p_j^2 with each degree(p_j)<=r, because top-degree squares cannot cancel. Its objective divided by its normalization is a weighted average of these single-square Rayleigh quotients. Conversely every single square is feasible after normalization. Therefore

    f^(r) = lambda_min(Z_r,H_r),

exactly, with no numerical approximation. This is the general moment/eigenvalue formulation already described in the source literature, specialized here to fully explicit rational entries.

## A certified feasible witness

Since f=z itself is affine and nonnegative on K, it may be used directly in place of the quadratic proxy. For L=5 and m>=1 set

    Q_m(x,y,z)=A_m(z)^10,

with A_m defined in the proof. It is a single square, of degree 10m, feasible at hierarchy order r=5m after normalization. Its objective is exactly

    integral_0^1 z^3 A_m(z)^10 dz / integral_0^1 z^2 A_m(z)^10 dz.

The omitted factor 4 cancels. The sublevel-volume function is F(t)=(4/3)t^3 for 0<=t<=1, so the general dyadic estimate applies directly with dimension three. All mass in the whole pyramid is included. The finite rational checks accompanying this document confirm selected coefficient identities and exact witness integrals, but the all-order theorem is proved by the analytic argument, not by those finite tests.
