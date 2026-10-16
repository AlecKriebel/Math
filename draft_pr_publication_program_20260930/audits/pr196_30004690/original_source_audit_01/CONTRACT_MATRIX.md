# Primary-source contract matrix and page map

The source-problem freeze preceded candidate access. Page numbers below are printed journal/report pages; PDF numbers are one-based. The journal PDF is controlling; arXiv is a version cross-check. Statements are mathematical restatements, not reproduced prose.

| Input | Precise contract needed | Candidate match and limit | Locator |
|---|---|---|---|
| Original global Dirichlet setting | Smooth boundary f; fiberwise omega+dd_z^c f >= 0; continuous relatively psh solution; locally bounded Bedford-Taylor equation | Candidate asks for strictly positive boundary slices, which meet this weaker setting | OWR 1322; PDF32 |
| Original interior objective | Exhibit failure of C^2 inside P^1 x D | Candidate's tau*=exp(G_Omega(w*,0)/2) has 0<tau*<1 | OWR 1323-1324; PDF33-34 |
| Original provenance | Interior construction announced and sketched; smoothness of inverse density receives tentative discussion with vanishing density permitted | Curation's world-open interpretation is not certified by this report | OWR 1321,1323-1324; PDF31,33-34 |
| Flow definition | phi smooth; omega_phi>epsilon*omega; normalized area(P^1)=1; dd^c log|z|^2=delta_0; envelopes with Lelong >=t | Compact strict positivity supplies uniform epsilon. T is area time, not arbitrary shape time | AIF 7; PDF8 |
| Proposition 2.5 | t in (0,1), smooth strictly positive obstacle; Omega_t connected; boundary zero area; psi_t C^{1,1} away from pole; omega_psi_t=1_(Omega_t^c)*omega_phi+t*delta_0 | Applicable at T and T+h. Equality on a zero-area contact arc adds no area measure. No regular post-contact boundary is assumed | AIF 8; PDF9; proof source IHES 319-320, PDF5-6 |
| Definition 1.2 and Proposition 3.4 | S finite union of points and nonintersecting smooth embedded segments disjoint from 0; T in (0,1); pre-T smooth simply connected domains; terminal boundary locally immersed with tangencies along S; resulting global omega_phi strictly positive | Choose one nontrivial segment. Use the particular construction, not an arbitrary degenerate terminal domain. Cover projection is injective on the chosen open lifted domain; closure injectivity is not required | AIF 4,15-16; PDF5,16-17 |
| Strong/weak identification and normalization | Strong flow grows from point 0, simply connected, area-time parametrization; modification can be joined to a standard short-time family | These are built into Proposition 3.4 through Theorem 3.1/Remark 3.2 and Proposition 2.12. The constructed form has total mass one | AIF 9-16; PDF10-17 |
| Two-sided smooth lifted flow | Smooth Jordan lifted domain, fixed injection point, smooth positive area form near boundary; allow interior modification of area form | AIF Theorem 2.15 supplies a two-sided interval; Proposition 3.4 uses its backward part. Plain forward short-time existence alone would be insufficient | AIF 12,15-16; PDF13,16-17; precursor arXiv1212.2337v2 Theorem2.2 p3 versus Remark7.1 p23 |
| Limiting velocity | For the Proposition 3.4 construction, lifted strong flow gives nonvanishing limiting normal velocity at T | Growth and nonvanishing imply outward scalar velocity >0. Smooth positivity of permeability and Hopf also give the sign | AIF proof of Theorem6.2, 24; PDF25 |
| Appendix A | Smoothly varying smoothly bounded simply connected planar domains on an open time interval; pole fixed inside. Pullback operators uniformly elliptic on a compact time subinterval | Apply in a fixed conformal coordinate on the covering surface near compact lifted domains. Never apply directly at the singular projected contact boundary. Remove time-independent log pole before differentiating | AIF TheoremA.1/CorollaryA.2, 26-28; PDF27-29 |
| Proposition 4.2 | Smooth global strictly Kähler phi; two envelopes defined in Section4.1; nonzero disc coordinate | On P^1 x D^x, (z,tau)->(tau*z,tau) is biholomorphic and corrections are smooth. Its infinity-chart formulation is regular as well | AIF 16-17; PDF17-18; original proof IHES Prop2.3/Remark2.4, 323-324; PDF9-10 |
| Duality | Same phi and envelopes; psi_t concave in t; dual supremum over t in [0,1] suffices | Gives candidate F(kappa)=kappa+sup_t(a(t)-t*kappa). No smoothness after T or global strict concavity is required | AIF Theorem4.4, 18; PDF19; full original proof IHES Theorem2.7, 325-326; PDF11-12 |
| Existing boundary theorem | Non-twice-differentiability at (tau^{-1}z,tau), z in S, |tau|=1 | Existing statement concerns the outer boundary. It does not itself state the candidate's interior point conclusion | AIF Theorems1.1/1.3/6.2, 2,4,24; PDF3,5,25; arXiv1509.02665v3 TheoremB, pp17-18 |
| Earlier harmonic-disc result | Smooth strictly Kähler phi on P^1; entire holomorphic graph discs classified using simply connected flow domains and two exceptional types | Explains original report's mechanism. Candidate relies on duality instead; it does not need a regular foliation through a rank-zero point | IHES Theorem3.1, 327-329; PDF13-15 |
| Earlier non-maximal-rank result | Smooth strictly Kähler phi with a prescribed terminal arc contact set; solution current vanishes on a nonempty open set | This is a rank assertion, insufficient by itself to prove failure of C^2. Later discussion conjectures/anticipates stronger regularity behavior | APDE Theorem1.1, 494 (PDF3); Theorem2.1, 495 (PDF4); Section3B, 501-502 (PDF10-11) |

## Literal-formula cautions

1. In the OWR report, the planar phi includes log(1+|z|^2); in AIF, phi is the global P^1 potential. Their symbols cannot be identified without this correction.
2. OCR drops closure bars in the covering construction. Visual review confirms that the punctures are chosen in components of the complement of the closure of Omega_T. A smooth cover boundary separates the two sides of a contact arc even when their projections coincide.
3. The local coordinate expression in Proposition 4.2 has logarithmic terms that separately diverge at z=infinity. Their difference extends smoothly. Use that difference, or a local chart, at infinity.
4. Pressure normalizations involving a displayed Laplacian and Euclidean constants should not be imported blindly. The candidate explicitly normalizes its negative Green function by the coefficient of log|w|^2, which is exactly the envelope's Lelong normalization. Smoothness and sign arguments survive any positive convention factor.
5. The AIF appendix's uniform ellipticity is needed only after restricting to a compact time interval around the lifted contact time. It is not a claim of a uniform bound across arbitrary noncompact parameter intervals.

## Main primary links

- [OWR report, DOI 10.4171/owr/2021/25](https://ems.press/content/serial-article-files/46904)
- [Published AIF paper, DOI 10.5802/aif.3237](https://www.numdam.org/item/10.5802/aif.3237.pdf)
- [Author version, arXiv:1509.02665v3](https://arxiv.org/abs/1509.02665v3)
- [Harmonic discs, DOI 10.1007/s10240-015-0074-0](https://www.numdam.org/item/10.1007/s10240-015-0074-0.pdf)
- [Maximal rank, DOI 10.2140/apde.2019.12.493](https://msp.org/apde/2019/12-2/apde-v12-n2-p07-s.pdf)
- [Smooth-flow precursor, arXiv:1212.2337v2](https://arxiv.org/abs/1212.2337v2)
