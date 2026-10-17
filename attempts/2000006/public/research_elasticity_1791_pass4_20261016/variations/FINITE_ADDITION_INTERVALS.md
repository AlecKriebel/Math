# Pass 4: finite inverse-addition intervals and an isolated finite amplitude

E-6322, 2026-10-16. The accepted compact-addition theorem identifies genuine inverse competitors whenever the resulting V energy is finite. This note proves a sufficient finite-energy interval criterion, and gives an exact obstruction showing why such intervals cannot be assumed from the baseline energy.

## 1. Baseline and notation

Let y be any admitted primal map, v its actual Sobolev a.e. inverse on D, F=Dy, J=det F, H=Dv, K=det H. The identity

H(z)=F(v(z))^{-1}

is established. The inverse energy is

V(H)=a|cof H|^6/K^5+b|H|^3/K^2+c/K+dK^3.

For compactly supported W^{1,9/4} additions zeta, the accepted pass-3 theorem states that finite integral V(H+Dzeta) implies membership in the exact inverse class. It does not assert that any nonzero amplitude is finite.

## 2. A sufficient relative-derivative condition

Let zeta be compactly supported and in W^{1,9/4}(D). Suppose

M(z)=Dzeta(z)F(v(z))

is essentially bounded, with norm at most L. For |t|L<1/2, put Q_t=I+tM. Then

H+tDzeta=Q_t H,
K_t=det Q_t K>0,
(H+tDzeta)^{-1}=F(v)Q_t^{-1}.

The matrices Q_t and Q_t^{-1}, and their determinants and reciprocal determinants, are bounded uniformly for t in a smaller fixed interval. Consequently

V(H+tDzeta)
=det Q_t K W(F(v)Q_t^{-1})
<=C V(H),

where C is independent of z. Every such amplitude has finite inverse energy, hence is a genuine inverse competitor by the accepted class theorem. This proves a two-sided finite-energy interval without a lower bound on the primal determinant.

In particular, compact smooth inverse tests have such an interval if the primal gradient is essentially bounded on the preimage of the support of their derivative. Global boundedness of Dy is a sufficient special case.

## 3. Why this safe criterion reduces to known material compositions for smooth tests

When zeta is C_c^1, define xi(x)=zeta(y(x)). The Sobolev chain rule gives

Dxi(x)=Dzeta(y(x))F(x)=M(y(x)).

Thus the relative bound makes xi a Lipschitz vector field with zero full boundary trace. Its support is compact in Omega, since y is continuous on the closure and maps its boundary to partial D. For sufficiently small |t|, phi_t=Id+t xi is a bi-Lipschitz material diffeomorphism fixing the boundary, and

v+t zeta=phi_t composed with v a.e.

Therefore these bounded-relative-derivative additions coincide with the already legitimate material-composition comparisons. They ensure admissibility, but do not themselves add a new comparison mechanism that truncates unbounded gradients or a vanishing determinant infimum.

This last composition argument is stated for smooth zeta so that no unproved Sobolev-composition theorem for a merely W^{1,9/4} zeta is imported. The finite-energy estimate in Section 2 does not require that extra composition argument.

## 4. A one-sided structured rank-one interval

There is also a useful sufficient condition which permits a degenerate endpoint. Let u=v+zeta, where zeta is compactly supported and W^{1,9/4}. Write H_e=Du, C=cof H, C_e=cof H_e, and K_e=det H_e. Suppose, for some M>=1,

rank(H_e-H)<=1 a.e.,
|H_e|<=M|H|,
|C_e|<=M|C|,
0<=K_e<=MK.

For 0<=t<1 set v_t=(1-t)v+tu. Every minor of a rank-one matrix segment is affine, so

H_t=(1-t)H+tH_e,
cof H_t=(1-t)C+tC_e,
K_t=(1-t)K+tK_e>=(1-t)K.

Hence

V(H_t)<=C_M(1-t)^{-5}V(H).

In particular the entire one-sided interval t in [0,1) consists of actual finite-energy inverse competitors, even if the endpoint K_e vanishes and its energy is infinite. This conclusion uses the compact-addition theorem after proving the displayed energy estimate.

The additional relative minor bounds are important: K_e>=0 alone is insufficient to control the two perspective terms with denominators K^5 and K^2.

For a minimizer this interval gives a justified one-sided derivative inequality. Let

X(H)=a|C|^6/K^5+b|H|^3/K^2+c/K.

All derivative terms are dominated by C_M V(H), because each of H, C and K changes by at most M+1 times its original size. If zeta vanishes off E, differentiating at zero and bounding the positive-part derivative above gives

3d integral_E K^2(K-K_e) <=11(M+1) integral_E X(H).

For example the a-term derivative is

6a|C|^4 C:(C_e-C)/K^5
 -5a|C|^6(K_e-K)/K^6,

bounded above by 11(M+1)a|C|^6/K^5; the b- and c-term bounds have smaller constants. The d-term is exactly 3dK^2(K_e-K).

This is a real comparison estimate under explicit verified hypotheses. It becomes a high-K estimate only if an endpoint with appropriate K_e and controlled relative minors is actually constructed. No such endpoint for arbitrary low-J sets has been supplied. A compact determinant change also has to compensate its volume change elsewhere, as explained in the companion note.

## 5. An inverse direction with no nonzero finite-energy amplitude

Use the established anisotropic admissible map on B_1:

y_alpha(x)=(r^{-alpha}x_1,r^{-alpha}x_2,r^{5alpha}x_3),
1/3<=alpha<1/2,
r=|x|.

Its trace is the identity, all target energy terms are finite, and

J=r^{3alpha}(1-alpha+6alpha n_3^2),
F_{11}=r^{-alpha}(1-alpha n_1^2).

In particular,

J is comparable to r^{3alpha},
F_{11}>=(1-alpha)r^{-alpha}.

Let v be its actual a.e. inverse on D=B_1. Choose chi in C_c^infinity(B_1) equal to one near zero, and define

zeta(z)=-chi(z) z_1 e_1.

This is one fixed smooth compactly supported inverse addition. Because y_alpha is continuous and y_alpha(0)=0, all sufficiently small primal balls map into the region chi=1. In that region

H_t=H-t e_1 tensor e_1,
K_t=K(1-t F_{11}),

by the rank-one determinant identity.

### Positive amplitudes

For every t>0, F_{11} tends uniformly to infinity as r tends to zero. Hence 1-tF_{11}<0 throughout a sufficiently small punctured primal ball. Its image has positive target measure by the area formula and J>0. Thus K_t<0 on a set of positive measure and

integral_D V(H_t)=infinity.

### Negative amplitudes

For every t<0, put tau=|t|. On the same core,

K_t=K(1+tau F_{11})>0.

Regardless of what happens outside the core, the dK_t^3 contribution is bounded below by

d tau^3 integral_core K^3 F_{11}^3 dz
=d tau^3 integral_primal_core J^{-2} F_{11}^3 dx
>=c tau^3 integral_primal_core r^{-9alpha} dx
=infinity,

since alpha>=1/3. Thus the inverse energy is infinite for every negative amplitude as well.

We have proved

integral_D V(Dv)<infinity,
but integral_D V(Dv+tDzeta)=infinity for every t not equal to zero.

The addition is smooth and hence satisfies every Sobolev regularity requirement of the accepted comparison-class theorem. The obstruction is exactly the sign/energy requirement, not a missing inverse-class theorem.

This example is not a minimizer: its identity boundary trace has the affine minimizer. It does not refute E-6322, and it does not show that an actual minimizer has such an isolated amplitude. It proves that a nonzero finite-energy interval cannot be inferred from the stated full admissible class alone, even for a smooth single-component direction.

## 6. Consequence for the attempted inverse cutoff route

The existence of every compact smooth comparison as an extended-valued competitor does not license differentiation through it. The example above has an extended-valued comparison energy finite only at zero along one such line.

To obtain new estimates by inverse additions, one therefore needs a structured sign/energy argument for the particular additions, or an independently stronger integrability/relative-derivative estimate. The bounded-relative criterion supplies one such argument but reduces smooth tests to material compositions. No reverse-Holder gain or inverse determinant upper bound has been obtained from it.
