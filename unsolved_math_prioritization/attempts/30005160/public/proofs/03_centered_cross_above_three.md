# Proof 03  Centered crosses for exponents at least three

This is a reading edition of an accepted authored proof. Its mathematical scope is unchanged. Source and reading-edition hashes are recorded in the [inventory](../CONTENT_AND_DEPENDENCIES.md). No novelty claim is made.

Public analytic inputs and exact attribution are listed in [References](../REFERENCES.md).

## Theorem

For every n>=1, the frequency set {0,+e_1,-e_1,...,+e_n,-e_n} subset Z^n has the full strict majorant property for real coefficients at every p>=3. All subsets do too, by setting coefficients to zero. The standard all-sets even-integer result also includes p=2. This supplement makes no claim about the interval 2<p<3 when n>=2.

## Scalar multiradius lemma

Let C_1,...,C_n be independent variables with the law of cos(theta), theta uniform on [0,2pi). For p>=3 define

G_p(s_0,s_1,...,s_n)=E |sqrt(s_0)+sum_{j=1}^n sqrt(s_j) C_j|^p,

for all s_j>=0. Then G_p is lattice-supermodular.

### Proof

Write g(x)=|x|^p. Its fourth distributional derivative is nonnegative:

- for p>3, g''''(x)=p(p-1)(p-2)(p-3)|x|^(p-4), a locally integrable nonnegative function;
- for p=3, g''''=12 delta_0.

Let rho_epsilon be a smooth, even, nonnegative approximate identity and set g_epsilon=g*rho_epsilon. Then g_epsilon is smooth and even; g_epsilon''''>=0. Thus g_epsilon''' is odd and nondecreasing.

Define T_s h(x)=E_theta h(x+sqrt(s) cos(theta)). View h as a function on R^2 depending only on the first coordinate, and apply the circle/disk mean differentiation identity. One obtains

partial_s T_s h = (1/4) Q_s h'',

where Q_s h(x)=E_D h(x+sqrt(s) D_1) and D is uniform in the unit disk of R^2. Both T_s and Q_s are convolutions by symmetric probability measures on R and commute with each other and with differentiation.

Put

`G_epsilon(s)=[T_{s_1}...T_{s_n} g_epsilon](sqrt(s_0)).`

For distinct random-radius indices i,j>=1,

partial_{s_i}partial_{s_j}G_epsilon
`= (1/16)[Q_{s_i}Q_{s_j} product_{k!=i,j}T_{s_k} g_epsilon''''](sqrt(s_0)) >=0.`

For a mixed derivative involving the deterministic-shift coordinate s_0 and j>=1,

partial_{s_0}partial_{s_j}G_epsilon
`= (1/(8 sqrt(s_0))) [Q_{s_j} product_{k!=j}T_{s_k} g_epsilon'''](sqrt(s_0)) >=0.`

The final inequality holds because convolution of an odd nondecreasing function with a symmetric probability measure remains odd and nondecreasing, so its value at sqrt(s_0)>0 is nonnegative. Hence all mixed partial derivatives are nonnegative on the positive orthant. This implies lattice supermodularity. Let epsilon decrease to zero; uniform convergence on bounded intervals of arguments yields the same inequality for G_p. Continuity extends it to coordinate boundaries.

## Projection reduction and majorant comparison

For every complex number z,

|z|^p = m_p^(-1) E_t |Re(e^(-it) z)|^p,

where t is uniform on [0,2pi) and m_p=E_t |cos(t)|^p>0.

Fix nonnegative coefficient magnitudes c,a_j,b_j. The positive-coefficient polynomial is

c+sum_j (a_j e^(i theta_j)+b_j e^(-i theta_j)).

Set A_j=a_j+b_j and B_j=|a_j-b_j|, so A_j>=B_j>=0. Independent changes theta_j->-theta_j can remove signs from a_j-b_j; these do not change the moment. Thus the positive polynomial has the same moment as

c+sum_j (A_j cos(theta_j)+i B_j sin(theta_j)).

For arbitrary real signs of coefficients, an overall sign and individual changes theta_j->theta_j+pi remove the center sign and common pair signs. Each opposite-sign pair interchanges the horizontal and vertical semiaxes A_j,B_j, up to harmless conjugation/reflection of that individual theta_j. Hence every sign pattern can be represented by sigma_j in {+1,-1}, indicating the ordering of the two semiaxes in each pair.

For fixed projection direction t, each independent scalar variable

A_j cos(theta_j) cos(t)+B_j sin(theta_j) sin(t)

has the same law as sqrt(A_j^2 cos^2(t)+B_j^2 sin^2(t)) C_j. If the semiaxes are interchanged, its squared amplitude has the sign of the cos(2t) term reversed. The deterministic projection is c cos(t), whose sign does not affect the scalar expectation because the sum of the C_j terms is symmetric. Therefore the pth moment for a sign pattern is

m_p^(-1) E_t G_p(alpha_0+beta_0 cos(2t), alpha_1+sigma_1 beta_1 cos(2t),...,alpha_n+sigma_n beta_n cos(2t)),

where

alpha_0=beta_0=c^2/2,
alpha_j=(A_j^2+B_j^2)/2,
beta_j=(A_j^2-B_j^2)/2=2a_jb_j>=0.

The all-positive pattern has every sigma_j=+1. For z>=0 apply lattice supermodularity to the two vectors

x=(alpha_0+beta_0 z, alpha_j+sigma_j beta_j z)_{j>=1},
y=(alpha_0-beta_0 z, alpha_j-sigma_j beta_j z)_{j>=1}.

Their coordinatewise join is alpha+beta z and their meet is alpha-beta z. Thus

G_p(alpha+beta z)+G_p(alpha-beta z) >= G_p(x)+G_p(y).

The law of cos(2t) is symmetric. Integrating this paired inequality proves sign domination at each fixed set of nonnegative magnitudes. For p>=1, convexity of the pth moment in the real coefficient vector then extends sign domination to all coefficients whose absolute values are bounded by those magnitudes.

## Scope

The use of g''''>=0 is essential to this proof. For 2<p<3, g'''' is not a nonnegative distribution; the mixed random-radius derivatives need not have the sign used above. Therefore no extension to that interval is justified by this supplement. The AP subcase n=1 has a different direct two-variable derivative argument covering every p>=2; see [Proof 05](05_arithmetic_progressions.md).
