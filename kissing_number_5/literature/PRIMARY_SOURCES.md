# Primary-Source Baseline and Imported Hypotheses

Last updated: 2026-07-24T03:34:00Z

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

## Second-level spherical Lasserre bound

D. de Laat, N. M. Leijenhorst, and W. H. H. de Muinck Keizer,
*Optimality and uniqueness of the \(D_4\) root system*,
<https://arxiv.org/abs/2404.18794>.

Imported statements from the primary paper:

- the second level of the spherical Lasserre hierarchy is a universal
  four-point bound;
- the authors computed the truncation \(d_1=14\),
  \(d_2=\delta=16\) in dimensions \(5,6,7,10,12,16\);
- at these degrees it improves the integer kissing bound only in dimension
  six, and does not improve the dimension-five bound 44;
- their dimension-four sharp computation required roughly two weeks on eight
  cores with 128 GB memory, so low-degree exploratory runs are not a proxy for
  the published high-degree calculation.

The associated public code and exact-verification data are archived at
<https://doi.org/10.4121/74ce1c25-6fca-4680-8a36-e9c18e7e9594>.
Our local degree-4, 6, and 8 trials are discovery computations only and are
recorded separately in the research log.

## 2025 dissertation audit of three- and four-point computations

N. M. Leijenhorst, *On the computation of three and four-point bounds in
discrete geometry and analytic number theory*, TU Delft dissertation (2025).

- DOI:
  <https://doi.org/10.4233/uuid:91af805a-376c-4ef8-aec5-e6ce08ae20a7>

Primary-source findings relevant here:

- the reported degree-20 three-point bound in dimension five is
  \(44.970252\), so it still rounds only to 44;
- the second Lasserre step was computed in dimensions
  \(4,5,6,7,10,12,16\) with \(d_1=14\) and \(d_2=\delta=16\);
- the text reports a sharp dimension-four result and the rigorous
  dimension-six improvement \(77.85<78\), but no dimension-five
  improvement below 44;
- the public 4TU archive above contains exact dimension-four and
  dimension-six certificates and source code, but no exact
  dimension-five certificate approaching 41.

This rules out treating a straightforward reproduction of that released
truncation as a hidden 40/41 separator.  It does not rule out a stronger
four-point truncation or a different exact dual.

## Exact eight-point Tammes result

K. Schütte and B. L. van der Waerden,
*Auf welcher Kugel haben 5, 6, 7, 8 oder 9 Punkte mit Mindestabstand eins
Platz?*, Math. Ann. **123** (1951), 96--124,
<https://doi.org/10.1007/BF02054944>.

Imported statement used in `proofs/local_link_geometry.md`:

- every eight points on \(S^2\) contain a pair with inner product at least
  \((2\sqrt2-1)/7>1/4\).

Together with the exact rational seven-point witness in the local-link
verifier, this establishes \(A(3,1/4)=7\).

## Literature status as of 2026-07-23

The 2026 Cohn--Rajagopal paper states that 40 appears to be the answer while 44
is the best proved upper bound.  This is used only for context and novelty
tracking, never as evidence for either exact conclusion.
