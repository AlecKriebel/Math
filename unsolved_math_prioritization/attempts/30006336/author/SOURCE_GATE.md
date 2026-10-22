# Source and scope gate

## Exact source

The investigation started at https://www.unsolvedmath.com/problems/30006336;
that endpoint returned HTTP 403 to the direct retrieval and was unavailable to
the web reader. The selected pinned catalogue record was therefore compared
with the official report, rather than treating its shortened question as primary.

The source is Hélène Esnault's contribution, joint work with Mark Kisin and
Alexander Petrov, in *Non-Archimedean Geometry and Applications*, Oberwolfach
Report 29/2025, pp. 1530–1534, DOI
[10.4171/OWR/2025/29](https://doi.org/10.4171/OWR/2025/29).
Section 4, pp. 1533–1534, asks for the analogue of Theorem 2 in the maximal-ideal
separated quotient of prismatic cohomology over Z_p[[u]]. It reports a computation
modulo (I²,pⁿ) and says that the general extension suggested by Scholze had not
yet been checked. Theorem 2's hypotheses are smooth proper X/Z_p,
H⁰(X_Fp,Ωⁱ)=0, and a dense affine open U⊂X.
This is not an unrestricted claim about all cohomology classes at a generic point.

## Working formulation and conventions

We make the base convention explicit, since the short report does not spell out
its Frobenius: use the standard Breuil–Kisin prism
A=Z_p[[u]], φ(u)=u^p, I=(d), d=u−p, m=(p,u)=(p,d), A/I≅Z_p.
This is a concrete standard interpretation of the report's Z_p[[u]] base.
The desired statement is

    image[Hⁱ_Δ(X̂/A) → Hⁱ_Δ(Û/A)] ⊂ ⋂_{n≥1} mⁿ Hⁱ_Δ(Û/A).

Here X̂ and Û are p-adic formal completions; Δ means relative prismatic
cohomology with its integral structure-sheaf coefficients. The target quotient
is M_sep=M/(⋂mⁿM), where M=Hⁱ_Δ(Û/A). No rationalization, passage to absolute
prismatic cohomology, or replacement of the module quotient by a derived inverse
limit is implicit. We work on the Zariski site after pushing forward from the
relative prismatic site; equivalent étale-local comparisons are used only where
specified. Density is the source condition on U⊂X; no extra density condition
on the special fibre or H¹(Ωⁱ⁻¹) vanishing is imposed. Empty formal pieces
contribute zero.

## Current literature and attribution

The [Strasbourg seminar of 2 October 2025](https://www.math.unistra.fr/seminaires/seminaire-arithmetique-et-geometrie-algebrique-2025.html)
announces, under the three authors' names, a separated integral prismatic
restriction-vanishing theorem for smooth proper p-adic schemes over a prism.
The [20 October 2025 IAS/Princeton announcement](https://www.math.princeton.edu/events/restriction-map-cohomology-2025-10-20t193000)
also states a prismatic separated-quotient result and distinguishes stronger
conclusions with extra assumptions. These are strong affirmative prior-result
signals, not proof artifacts inspected here.

The current public lists of Esnault, Kisin, and Petrov were checked, including
Petrov's 2026 teaching notes. No full joint proof was located. Caro–D'Addezio's
[arXiv:2511.11444](https://arxiv.org/abs/2511.11444), bibliography [EKP], cites
*Restriction in cohomology and differential forms* as in preparation. Their
Theorem 1.3.2 credits the crystalline/de Rham separated theorem; their negative
comparison results concern a different question. They do not supply a verified
replacement proof of the present full relative-prismatic statement in this packet.
Thus `unsolved` is a **local verification outcome**, with a prior-announcement
hold on novelty, not a categorical claim that the literature remains unsolved.

## Duplication and success criteria

The live repository queue still showed this exact numeric ID at rank 629,
queued, 0/5; there was no state entry. ID and title PR searches, a matching branch
search, code search, and the expected attempt README lookup found no existing
attempt/PR. The related-target groups did not list this ID. These bounded searches
do not prove there is no unindexed work. The pinned prior-report corpus had no
matching key or matching title text for this target.

Adjacent ID 30006335 concerns strongly p-divisible classes and the good-
compactification comparison map. It must not be counted as the present problem
or changed on the strength of this attempt. No adjacent record was edited.

Success would require a fully checked proof of the displayed inclusion for all
stated X,U,i,p, a counterexample satisfying those hypotheses, or a proof-bearing
prior theorem verified to cover the same coefficient and topology conventions.
Five approaches were exhausted without that success. Source copies and raw
catalogue records are excluded from the public-safe packet.
