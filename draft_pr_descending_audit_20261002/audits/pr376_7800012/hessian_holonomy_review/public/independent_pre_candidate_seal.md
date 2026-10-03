# PR376 independent pre-candidate mechanism seal

UTC checkpoint: 2026-10-03 05:47 UTC. Completion estimate: 18% of this family audit. Candidate files, root/sibling findings, and prior verdicts have not been accessed. This file fixes the independent mechanisms and failure tests before such access.

## Exact claim under test

On a simple nearest-neighbor square torus Lx,Ly >= 3, with unit complex hopping magnitudes, n=Lx Ly divisible by four, minimize E_k(T)=sum of its k=n/4 least eigenvalues over every oriented edge phase. A finite 4x4 result, a uniform-flux-only comparison, local phase stability, an all-size theorem, and a thermodynamic statement are distinct claims. The source's word 'large' leaves the size/asymptotic interpretation material.

## Gauge and topology mechanism

Choose one orientation on each of 2n edges. Vertex phase changes add exact edge cochains and are diagonal unitary conjugacies. Their real tangent rank is n-1. The quotient dimension is 2n-(n-1)=n+1. Plaquette curl has rank n-1 (the sum of all oriented faces is zero); two independent noncontractible loop phases remain. Equality of elementary plaquette flux alone therefore does not imply gauge equivalence or equal spectra. Equality on a spanning cycle basis does: fix a spanning tree and use vertex phases to remove every tree difference; the remaining n+1 chord differences are precisely the cycles. Flux pi/2 is feasible only if n*pi/2 is zero modulo 2pi. The gauge with horizontal phases zero and vertical phases x*pi/2 is periodic without a seam when Lx is a multiple of four. General admissible dimensions need a seam construction. For lengths 1 or 2, the simple-edge convention collapses the expected 2n edges and must be excluded or treated explicitly.

Control: zero plaquettes with different loop phases have spectra 2cos((2pi r+alpha)/Lx)+2cos((2pi s+beta)/Ly). Their top eigenvalue changes, so no 'plaquettes determine spectrum' statement on a torus is accepted literally.

## Uniform pi/2 holonomy mechanism, independently derived

For a 4x4 torus, use T_(x,y),(x+1,y)=exp(i alpha/4), T_(x,y),(x,y+1)=i^x exp(i beta/4), plus conjugate entries. Fourier transform y, then gauge horizontal interior phases onto the closing edge. For each of four y momenta, the resulting 4x4 Harper determinant is

p(lambda)=lambda^4-8lambda^2+4-2cos(alpha)-2cos(beta).

The four blocks are unitarily equivalent (cyclic x translations). Put D=sqrt(12+2cos(alpha)+2cos(beta)), a=sqrt(4+D), b=sqrt(4-D). Spectrum is {-a,-b,b,a}, each multiplicity four, counting coincident zero bands at alpha=beta=0. Thus E_4=-4a. Monotonicity proves the global minimum **inside this fixed uniform-flux class** at alpha=beta=0 modulo 2pi, with value -8sqrt(2). The occupied-unoccupied gap is a-b>0, including where middle bands merge. At the optimum, spectrum is {-2sqrt(2)}^4,{0}^8,{2sqrt(2)}^4, gap 2sqrt(2). The two-loop Hessian is diagonal with both entries sqrt(2)/8. No sampled twist mesh can replace this all-holonomy proof. For larger dimensions the allowed momentum set changes; the 4x4 proof cannot be silently extrapolated.

## Full phase derivative mechanism

For a phase direction z, define A=T'(0), B=T''(0) by A_uv=i z_e t_uv, A_vu=conjugate(A_uv), B_uv=-z_e^2 t_uv and conjugate reverse. Let P be the spectral projector onto the first k states and suppose lambda_k < lambda_(k+1). Then E is analytic near the base matrix despite degeneracies strictly inside occupied or unoccupied clusters. In any orthonormal eigenbasis,

E'=Tr(P A),
E''=Tr(P B)+2 sum_(i<=k,j>k) |<j|A|i>|^2/(lambda_i-lambda_j).

The cross-cluster denominators are negative; dropping B changes the answer. Degenerate occupied eigenvectors individually need not be differentiable. At a gap closure, smoothness and this Hessian require a separate argument; generic E_k is only piecewise analytic and can have a cusp.

At the 4x4 zero-loop point let s=2sqrt(2), Pminus=(T^2-sT)/16, Pzero=I-T^2/8, Pplus=(T^2+sT)/16. These exact polynomial projectors avoid choosing degenerate eigenvectors. For edge directions e,f,

H_ef=delta_ef Tr(Pminus Q_e) -(2/s) Re Tr(Pminus D_e Pzero D_f) -(1/s) Re Tr(Pminus D_e Pplus D_f),

where Q_e=-the edge's Hermitian hopping contribution. Check every gradient component equals zero. Check the exact Hessian, its inertia and nullspace, every gauge direction, both holonomy directions, and the curl quotient. A PSD Hessian proves at most second-order stability. A strict positive Hessian modulo gauge gives a strict local minimum modulo gauge; additional non-gauge kernel directions need higher-order analysis. Neither establishes global optimality.

## Falsifiable controls and boundary cases

Reproduce exact matrix characteristic polynomials, all projector identities, derivatives, and Hessian signs with independent symbolic algebra. Test the derivative formula by central differences away from a cluster crossing. Verify gauge curves are exactly isospectral, so stationary Hessians annihilate n-1 gauge directions. Manufacture a wrong sign in the virtual-transition term, a missing Q_e term, and a missing holonomy to ensure controls fail. Check occupation multiplicities and Fermi gaps; compare edge conventions for length 2. Distinguish finite computations from all-size assertions. Compare any finite lower energy against the **optimized** uniform pi/2 class at that same size, not a chosen holonomy only.

## Primary source scope and research gap

Lieb 1994's reflection argument is a half-filling, particle-hole/grand-canonical mechanism. A quarter-filled spectral sum is not supplied by that theorem. Lieb-Loss 1992 proves determinant/trace-function results under graph and filling assumptions, and explicitly distinguishes unrestricted fluxes from constant fluxes. These do not automatically establish quarter-filling on a torus. The central unverified gap is global comparison against every phase configuration and, separately, extension beyond a specifically proved finite size.

Sources accessed first: https://web.math.princeton.edu/~aizenman/OpenProblems_MathPhys/9802.OptFlux.html ; https://arxiv.org/pdf/cond-mat/9410025 ; https://arxiv.org/pdf/cond-mat/9209031. No contact or outreach.
