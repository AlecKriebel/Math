# Multipeaked alignment states: physical-kernel scope and a credited monochromatic diagnostic

**30001251 / OWR-3474-001. Scoped partial; original physical-kernel conjecture unresolved.** Recommended status **unsolved, 2/5**. The pure-harmonic minimizers below are prior generalized-Kuramoto phenomena, not a new discovery or a counterexample within the source's physical sign restriction.

## 1. The exact question and two different kernel classes

Primi's [OWR24/2009 contribution, printed pp.1356–1359](https://publications.mfo.de/bitstream/handle/mfo/3125/OWR_2009_24.pdf?isAllowed=y&sequence=1) considers mass-one densities on the circle R/Z and the Fokker–Planck approximation

$$ f_t=D f_{xx}+\partial_x(f(V*f)),\qquad D=\sigma^2/2>0. \tag{1} $$

The orientational angle V is smooth, odd and 1-periodic. The physical discussion additionally requires a z in (0,1/2) with

$$V>0\text{ on }(0,z),\qquad V<0\text{ on }(z,1/2),\qquad V(0)=V(z)=V(1/2)=0.\tag{2}$$

The report conjectures instability of the small-noise, equal-height, equally spaced N-peak steady states for N>=3, based on four-peak numerical evidence. It does not fix a precise stability norm. Because rotations produce a continuum of equilibria, orbital stability must be distinguished from convergence to a specific unshifted density. This attempt addresses equation (1), not the original nonlocal kinetic turning equation before its diffusion approximation.

The full [Primi–Stevens–Velazquez preprint, revised June2007](https://webdoc.sub.gwdg.de/ebook/serien/e/MPI_Math_Nat/preprint2007_34.pdf), published in *Comm. PDE*34(2009),419–456, DOI[10.1080/03605300902797171](https://doi.org/10.1080/03605300902797171), separates assumptions. Its Theorem7.1 assumes only smooth periodicity, oddness, and conditions (35),(36). With

$$V_N(x)=\frac1N\sum_{i=0}^{N-1}V(x-i/N),\quad W_N(x)=\int_0^xV_N(s)\,ds,$$

these require sum_i V'(i/N)>0 and strict positivity of W_N uniformly on every closed interval [delta,1/(2N)] with delta>0. They do **not** include the physical condition (2), although the latter remains part of the motivating model. Consequently an example satisfying Theorem7.1's formal assumptions alone cannot silently refute the physical conjecture. The report's displayed first-order stationary equation omits D; the full paper's Lemma2.1 retains it. We use the correct equation D f'+f(V*f)=0 throughout.

## 2. Prior literature and a useful relaxed-class example

[Carrillo–Gvalani–Pavliotis–Schlichting, *Arch. Ration. Mech. Anal.*235(2020),635–690](https://doi.org/10.1007/s00205-019-01430-4), Section6.1, studies the generalized Kuramoto potential -cos(kx). Its nonuniform branch is a free-energy minimizer and tends to equally weighted peaks at low temperature. This is restated in [Bertoli–Goddard–Pavliotis, Proposition2.1](https://doi.org/10.1093/imamat/hxaf001), published13January2025 in the October2024 issue. [Bertini–Giacomin–Pakdaman](https://arxiv.org/abs/0911.1499) supplies earlier noisy-rotator stationary and spectral theory. These works are credited; the elementary computations below make the comparison with the source explicit.

There is a relevant [June2025 correction](https://doi.org/10.1093/imamat/hxaf014) to Bertoli–Goddard–Pavliotis. It clarifies that an operator in that paper freezes the convolution at an invariant measure, rather than taking the full nonlinear McKean–Vlasov derivative. We do not use its frozen-convolution spectrum to conclude nonlinear stability. The full Hessian below retains the perturbation of the interaction.

Fix N>=3 and a>0, and set

$$ V(x)=a\sin(2\pi Nx),\quad c=\frac{a}{2\pi N},\quad \kappa=\frac cD=\frac{a}{\pi N\sigma^2}.\tag{3}$$

This V meets every formal hypothesis of Theorem7.1: V_N=V,

$$W_N(x)=c(1-\cos(2\pi Nx)),\qquad \sum_iV'(i/N)=2\pi aN^2>0.$$

But V has N-1 distinct interior zeros on (0,1/2), with alternating signs. For N>=3 it violates (2). This exclusion is essential.

## 3. Exact branch, normalization and energy minimum

Define

$$I_0(b)=\int_0^1e^{b\cos(2\pi x)}dx,\quad I_1(b)=I_0'(b),\quad r(b)=I_1(b)/I_0(b).$$

If kappa>2, equivalently sigma²<a/(2pi N), there is a unique b>0 solving b=kappa r(b). The corresponding orbit is

$$f_{b,\theta}(x)=\frac{e^{b\cos(2\pi Nx-\theta)}}{I_0(b)}.\tag{4}$$

It has exactly N equal maxima in one unit period. Its convolution with V is a r(b) sin(2pi Nx-theta), while D f'/f=-2pi N D b sin(2pi Nx-theta), proving the stationary equation.

For completeness, uniqueness follows from a positive-series argument, avoiding any numerical Bessel estimate. With t=b²/4,

$$I_0(b)=\sum_{j\ge0}\frac{t^j}{(j!)^2},\qquad I_1(b)/b=\frac12\sum_{j\ge0}\frac{t^j}{j!(j+1)!}.$$

The numerator/denominator coefficient ratios are 1/[2(j+1)], strictly decreasing. Differentiating the quotient and pairing indices i>j gives coefficients proportional to (i-j)(a_i d_j-a_j d_i)<0. Thus r(b)/b strictly decreases from 1/2 to zero; the latter limit follows from 0<r(b)<1. This proves existence and uniqueness. Also r'(b)=Var_b(cos)>0 and kappa r'(b)<1 at the nonzero root.

Let m(f)=(integral f cos(2pi Nx), integral f sin(2pi Nx)). A primitive of V is -c cos(2pi Nx); the free energy is

$$\mathcal F(f)=D\int f\log f-\frac c2|m(f)|^2.\tag{5}$$

For z=kappa m(f), write f_z=e^{z\cdot(\cos(2pi Nx),\sin(2pi Nx))}/I_0(|z|). Direct substitution gives the exact identity

$$\frac{\mathcal F(f)}D=\operatorname{KL}(f\Vert f_z)+E(|z|),\qquad E(\rho)=\frac{\rho^2}{2\kappa}-\log I_0(\rho).\tag{6}$$

Since E'(rho)=rho[1/kappa-r(rho)/rho], its unique radial global minimum is b. Nonnegativity of relative entropy therefore proves that (4) is the complete family of global minimizers among **all** probability densities, not just 1/N-periodic perturbations. Equality requires f=f_z and |z|=b, and the self-consistency equation verifies these conditions for every phase. This recovers the credited generalized-Kuramoto minimizer statement.

As sigma tends to zero, kappa tends to infinity and the root b tends to infinity (otherwise r(b)/b could not tend to zero). Elementary Laplace concentration in (4) then gives the equally weighted sum of the N point masses at its maxima.

## 4. Full interaction Hessian and an orbital Lyapunov statement

At phase zero, let h=f_b u with integral h=0. The second variation, divided by D, is

$$Q(u)=\mathbb E_{f_b}u^2-\kappa\big[(\mathbb E_{f_b}u\cos)^2+(\mathbb E_{f_b}u\sin)^2\big].\tag{7}$$

The trigonometric arguments here are 2pi Nx. Put C=Var_b(cos)=r'(b), S=E_b sin². Integrating the derivative of sin(t)e^{b cos(t)} over a period gives S=r(b)/b=1/kappa. The mean-zero functions cos-r and sin are orthogonal. Decompose

$$u=\alpha(\cos-r)+\beta\sin+u_\perp.$$

Then

$$Q(u)=\alpha^2 C(1-\kappa C)+\|u_\perp\|_{L^2(f_b)}^2\ge0.\tag{8}$$

The kernel consists exactly of the translation direction f_b sin. No restriction to periodic perturbations was imposed. In particular this is not the spectrum of the frozen-convolution operator.

There is also a precise nonlinear statement requiring no numerical spectral approximation. For smooth nonnegative mass-one solutions of (1), the gradient-flow identity gives

$$\frac{d}{dt}\mathcal F(f)=-\int f\left|\partial_x(D\log f-c\,m(f)\cdot(\cos,\sin))\right|^2\le0.\tag{9}$$

For t>0 positivity permits the calculation; initial densities with zeros are treated by positive-time regularization and continuity. Smooth periodic kernels and D>0 give global smooth solutions: convolution and its first derivative are uniformly bounded by a and 2pi Na from mass conservation; the parabolic maximum principle prevents finite-time blowup, and the usual heat-semigroup iteration gives existence and smoothing.

Small excess energy forces small L1 distance to the orbit. Indeed |z|<=kappa. If F(f)-F_min tends to zero, (6) implies KL(f||f_z) tends to zero and E(|z|)-E(b) tends to zero. Pinsker's inequality gives ||f-f_z||1 tending to zero. Strict radial minimality on the compact interval [0,kappa] implies |z| tends to b. The smooth radial family f_z then approaches the phase orbit in L1. This argument also gives an epsilon-delta statement by compactness.

Consequently, for every epsilon>0 there is eta>0 such that any smooth mass-one initial density with F(f_0)-F_min<eta has L1 distance less than epsilon from the orbit at **all** nonnegative times. In particular sufficiently small L-infinity perturbations of any member of (4) satisfy this conclusion, since entropy and m vary continuously there and f_b is bounded away from zero. This is an orbital energy/L-infinity-to-L1 Lyapunov statement. We do not claim here an L1-to-L1 basin theorem, asymptotic phase selection, or uniform-in-noise decay rate.

## 5. What is still open in this attempt

Route1 reconstructed the relaxed monochromatic branch and its full Hessian/energy coercivity, while checking published generalized-Kuramoto credit. Route2 attempted to bring that mechanism into the physical class (2). It fails at a concrete hypothesis: the additional sign changes of the pure Nth harmonic. No admissible replacement kernel with a certified stable physical N-peak branch was established, and no instability proof for every physical kernel was obtained.

Thus the formal existence assumptions alone are insufficient for a blanket instability inference, but the motivating physical source question is not resolved. The two statements must stay separate. The zero-diffusion multipeak results of [Geigant–Stoll, EJDE2012/157](https://ejde.math.txstate.edu/Volumes/2012/157/geigant.pdf) likewise cannot automatically settle the positive-noise problem. No claim that all remaining literature has been exhaustively classified is made.
