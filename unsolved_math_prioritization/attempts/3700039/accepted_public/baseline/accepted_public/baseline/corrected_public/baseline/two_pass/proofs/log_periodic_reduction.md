# A sufficient finite-dimensional route to a genuine counterexample

This is an exact reduction and search specification, not a counterexample.

Fix rho>0 and omega>0. Let H_j(s,theta) be real functions, 2*pi-periodic in both variables. Suppose

((omega partial_s+rho)^2 + partial_theta^2) H_j >= 0.

Then

u_j(r exp(i theta)) = r^rho H_j(omega log r,theta), u_j(0)=0

are whole-plane subharmonic if the H_j are continuous. Define

M(s)=integral_0^{2*pi} median(H_1(s,theta),H_2(s,theta),H_3(s,theta)) dtheta,
C(s)=max_{j,theta} H_j(s,theta).

At every radius with C(omega log r)>0, the exact normalized median ratio is M(s)/C(s). If continuous H_j satisfy M(s)<0 for every phase s, compactness gives max_s M(s)<0, C(s)>0, and max_s C(s)<infinity. Therefore the supremum over all radii is strictly negative. Such a certificate would refute the full target, not merely its stronger local variant.

One exact way to enforce subharmonicity is to choose real trigonometric polynomials P_j and put F_j=P_j^2. In the Fourier convention exp(i(m*s+n*theta)), solve

Hhat_j(m,n)=Fhat_j(m,n)/((rho+i*omega*m)^2-n^2).

For rho>0, omega>0, every multiplier is nonzero if rho is not an integer. Indeed, its imaginary part is 2*rho*omega*m; vanishing therefore requires m=0 and rho=|n|. Thus these H_j are exact finite trigonometric polynomials, and L H_j=F_j>=0 everywhere.

A numerical negative sample is not enough: one must certify the inequality M(s)<0 for every phase and control angular integration errors. No such certificate was found in the exploratory probes accompanying this note. Discrete Fourier evaluation of these small-bandwidth polynomials is a computational convenience, not a mathematical counterexample certificate.
