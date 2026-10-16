# Separate normalization addendum

UTC: 2026-10-15T13:25:55.236743+00:00

This additional convention audit was requested after the original nine safe audit files were sealed. Those nine files and their manifest are unchanged. Completion of this additional normalization check: 100%.

## Printed formula and mathematical issue

Visual inspection of the published AIF printed page7 (PDF page8) confirms the displayed formula

    d^c = i/(2*pi) * (bar_partial - partial),

followed immediately by dd^c log|z|^2=delta_0 and the assertion that dd^c log(1+|z|^2) is the Fubini-Study form of total area1. The author-version arXiv1509.02665v3 manuscript page5 has the same prefactor. There is no alternative definition of the exterior derivative on that page that reconciles the assertions.

With ordinary d=partial+bar_partial and the usual real Dirac measure, the displayed prefactor gives dd^c=(i/pi)*partial*bar_partial. Since Delta log|z|^2=4*pi*delta_0 and i*partial*bar_partial f=(Delta f/2)*dx*dy, this gives dd^c log|z|^2=2*delta_0. It also gives total Fubini-Study area2. The three assertions therefore cannot all hold literally under conventional differential operators. The prefactor is best treated as an apparent factor-two typographical inconsistency, rather than evidence for an undeclared convention. This diagnosis is mathematical, not an author-confirmed erratum.

The earlier IHES paper's printed318 (PDF page4) specifies its normalization directly by FS area1, FS potential log(1+|z|^2), and dd^c log|z|^2=delta_0. Those statements are mutually consistent and are the conventions used by the candidate.

## Consistent convention and candidate effect

Use explicitly

    d^c = i/(4*pi) * (bar_partial - partial),
    dd^c = i/(2*pi) * partial*bar_partial,
    dd^c log|z|^2 = delta_0,
    omega_FS = dd^c log(1+|z|^2),
    omega_FS = dx*dy/[pi*(1+|z|^2)^2],
    integral_(P^1) omega_FS = 1.

Let every Green function G_Omega be negative, vanish at regular boundary points, and have singular part log|w|^2 at the pole. Then dd^c G_Omega=delta_0 inside Omega; envelope Lelong coefficient t equals its current mass t, and area time is t. All current, concavity, Legendre, and twisting identities used in the candidate retain exactly the displayed coefficients. In particular partial_t psi_t=G_Omega_t has coefficient1 at its pole. The AppendixA smoothness argument is unaffected by positive normalization constants; differentiating the Dirichlet boundary condition and using Hopf gives the same strict sign.

The disc radius relation comes from kappa=log|tau|^2, so for the candidate's unit-log-squared Green function

    tau_star = exp(G_Omega(w_star,0)/2)

remains exactly correct. A Euclidean fundamental-solution convention with Delta g=delta_0 would instead use g=G/(4*pi), and its equivalent radius would be exp(2*pi*g); mixing these conventions would be incorrect. No such mixing occurs in the candidate, which states its logarithmic coefficient explicitly.

This is a presentation clarification. It does not require changing the candidate's mathematics or the audit's PASS verdict. A public mathematical writeup should state the coherent unit-log-squared convention above rather than reproduce the inconsistent printed d^c prefactor. This check does not provide historical or publication clearance.

## Checkable custody

Published PDF: https://www.numdam.org/item/10.5802/aif.3237.pdf ; 3158845 bytes; SHA256724e742d033b3401b6938011cf07ee4faf79a7d13b14d22bb9ca1a90969cc0e2. Visual source is excluded shared private_primary_sources/aif_normalization-08.png. Earlier IHES PDF: https://www.numdam.org/item/10.1007/s10240-015-0074-0.pdf ; 744427 bytes; SHA256e5aa2b340ad496ff462fc71d227e7df1bbada01067304d38325e514c95d132d0. No new source PDFs were downloaded.
