# Explicit interpretation amendments and independent obstruction checks

Status: audit memorandum, 2026-10-16. These amendments preserve the original formulation gate as history. They do not alter its exact finite polynomial, the CK Ramanujan arithmetic profile, its sharp-kernel functional Q, or its aggregate prime-power target.

## 1. Nonvacuous parameter subrange

The explicitly adopted amended witness range is

0 < psi <= phi < 1,
1 < lambda < min(2, 1/phi, 1/(1-psi)).

This is a restriction, not a proof that the unchanged conjecture is plausible throughout the original range. The interval is nonempty for every such (phi,psi). For example (phi,psi,lambda)=(3/4,1/4,6/5) works. All earlier strict endpoint inequalities remain strict.

The restriction is necessary for this particular cumulative CK density and uniform complex polydisc hypothesis. Indeed, suppose psi>phi. Choose phi<theta<min(psi,1), even h comparable to N^theta, and a small fixed b>0 with r=b/log N lying in the interior of the polydisc centered at zero. Both center zero and center r have interior Cauchy circles of radius comparable to 1/log N. Two numerator derivatives of the assumed coefficient correlations therefore give cumulative Lambda-pair formulas with errors O(x^phi (log N)^2), uniformly on N/2<=x<=N. The differentiated CK density is S(h)x^(-2r).

At center zero the differentiated cumulative sum has density S(h). Exact coefficient reweighting at common shift r is [n(n+h)]^(-r). Partial summation on (N/2,N] consequently gives density S(h)[x(x+h)]^(-r), with total error O(N^phi (log N)^2). Applying the assumed center-r formula on the same interval instead gives S(h)x^(-2r). Their difference is

S(h) integral_(N/2)^N x^(-2r) [1-(1+h/x)^(-r)] dx.

For this even h, S(h) is bounded below by a fixed positive constant. Since h/N tends to zero and r=b/log N, the displayed difference is bounded below by a constant times h/log N. This exceeds N^phi (log N)^2, a contradiction. Endpoint conventions in the interval subtraction only enter the existing error term. This argument also applies when a0=0: positive common r is already inside the complex polydisc about zero. No unproved prime-pair asymptotic is invoked outside the hypothesized consequence.

## 2. Corrected CK displacement

The locally inspected CK2016 v2 PDF prints B_{-beta,-alpha,gamma,delta}(1+s) in Theorems 1 and 2. With the paper's explicit definition of B, this cannot be the literal finite-ratio identity. At all four shifts zero, I_{0,0}(n)=1_{n=1}, so the finite mean is exactly its diagonal. But the printed B is identically one; its one-swap Perron term adds the integral over t<2 pi N. This is an order-T discrepancy for a positive test weight, not a power-saving remainder. The supplied page-4 image was inspected, so this is not an OCR inference.

The independently verified displacement associated with the unchanged CK density is

B_{-beta,-alpha-s,gamma+s,delta}(1),

with k=alpha+beta+s. Equivalently the s allocation can be exchanged between the two shifted coefficient pairs. The density identity is

chi(1-k) J_z(k) = B_{-beta,-alpha-s,gamma+s,delta}(1),

where J_z(k) is the Dirichlet series in h of the explicit Ramanujan density. This statement is meromorphic continuation of an Euler-product identity, not an assertion of absolute convergence of B's original coefficient series in the displayed parameter region.

For a local check set d=alpha+beta, u=gamma-alpha, v=delta-beta. Multiplying the Euler factors gives numerator

1-p^(-1-u)-p^(-1-v)+p^(-1-gamma-delta-s)

and denominator 1-p^(-1+d+s), exactly the local factor of the displaced B. In particular the corrected expression vanishes on the simultaneous pair-collision locus, as the off-diagonal density must.

## 3. Whole-line weight endpoint

For the allowed arbitrary real Schwartz band-limited weight, w(0) need not vanish. Let

W(v)=hat w(v)+hat w(-v),
M_W(k)=integral_0^infinity W(v)v^(k-1)dv,
H_w(k)=integral_R w(t)|t|^(-k)dt.

The ordinary Fourier-Mellin identity M_W(k)=chi(1-k)H_w(k) holds in 0<Re k<1. The absolutely convergent h-Dirichlet-series derivation starts to the right of k=1. Shifting the contour to Re k=1/2 crosses the pole of J_z at k=1. Its residue contributes

2 pi w(0) N^(1-alpha-beta) / [(1-alpha-beta) zeta(1+gamma-alpha) zeta(1+delta-beta)].

This term must remain in the corrected zero/one-swap correspondence. It is generally of order N times the two reciprocal-zeta factors. It is zero when w(0)=0, but that optional specialization does not replace the arbitrary-weight theorem. The prime mixed derivative of this endpoint is 2 pi w(0) N^(1-2r)/(1-2r), so omitting it would also change the prime statistic materially.

The contour shift is legitimate once the normal Euler-product region and rapid vertical decay of M_W are proved. On Re k=1/2, H_w is an ordinary convergent integral, with the entire real line handled by |t|. There is no need to discard low times or negative times.

## 4. GRH scope and acceptance consequence

An independent Euler-factor derivation starting with the explicitly assumed CK density does not need GRH. It does not remove GRH from the source's separate identification of additive-twist residues with that density. Any use of that original twisted-residue identification must retain its GRH qualification. The complete witness may be stated conditional only on the explicit arithmetic hypothesis if all density-to-main-functional calculations are independently proved.

The amended witness can answer the declared existential reading of AIM Problem 6.2. It is not a verification of the source's literal printed Theorems 1/2, an unrestricted answer about full zeta ratios, an individual fixed-shift Hardy-Littlewood result, or a novelty claim. Final acceptance requires a separate audit of frozen proof files and independent controls; this memorandum alone does not grant it.
