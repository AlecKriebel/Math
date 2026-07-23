# Primary-Source Baseline and Imported Hypotheses

Last updated: 2026-07-23T18:39:53Z

## Bachoc--Vallentin three-point bound

C. Bachoc and F. Vallentin, *New upper bounds for kissing numbers from
semidefinite programming*, J. Amer. Math. Soc. 21 (2008), 909–924.

- DOI: <https://doi.org/10.1090/S0894-0347-07-00589-9>
- arXiv: <https://arxiv.org/abs/math/0608426>

Imported mechanism:

- normalized Jacobi/Gegenbauer polynomials satisfy \(P_k^n(1)=1\);
- positive-semidefinite matrix-valued kernels \(S_k^n(u,v,t)\) encode
  three-point positivity;
- the relevant triple domain includes
  \(-1\leq u,v,t\leq1/2\) and
  \(1+2uvt-u^2-v^2-t^2\geq0\);
- a dual feasible solution gives a universal upper bound for spherical codes,
  without symmetry assumptions on the code.

Audit still required before reuse in a final proof:

- transcribe the exact primal and dual with every factor and symmetrization
  convention;
- confirm whether the enlarged domain used for SOS certification loses
  strength or only simplifies sufficient conditions;
- independently verify all endpoint conventions (\(\leq1/2\), not \(<1/2\));
- reconstruct exact or directed-interval PSD and polynomial certificates.

## Mittelmann--Vallentin high-accuracy computation

H. D. Mittelmann and F. Vallentin, *High accuracy semidefinite programming bounds
for kissing numbers*, Experimental Mathematics 19 (2010), 174–178.

- DOI: <https://doi.org/10.1080/10586458.2010.10129070>
- arXiv: <https://arxiv.org/abs/0902.1105>

Imported statement:

- the reported three-point SDP computation narrows the integer range in
  dimension 5 from 40–45 to 40–44.

Important limitation:

- the published numerical result is baseline context, not a certificate for
  \(\tau(5)\leq40\);
- this project will not infer exact dual feasibility merely from printed
  decimal output.

## Non-isometric 40-point configurations

F. Szöllősi, *A note on five dimensional kissing arrangements*,
<https://arxiv.org/abs/2301.08272>.

H. Cohn and I. Rajagopal, *Variations on Five-Dimensional Sphere Packings*,
<https://doi.org/10.1007/s00454-026-00841-x>.

Imported statements:

- there are at least four pairwise non-isometric 40-point kissing
  configurations \(D_5,L_5,Q_5,R_5\);
- some are non-antipodal and have much smaller symmetry groups than \(D_5\);
- therefore uniqueness, antipodality, and large symmetry cannot be assumed in
  an upper-bound proof.

## Literature status as of 2026-07-23

The 2026 Cohn--Rajagopal paper states that 40 appears to be the answer while 44
is the best proved upper bound.  This is used only for context and novelty
tracking, never as evidence for either exact conclusion.
