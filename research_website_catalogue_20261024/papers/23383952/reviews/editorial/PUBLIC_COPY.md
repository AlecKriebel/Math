# A finite counterexample to the weighted Yamabe heat trace comparison

By Alec Kriebel, independent researcher. [ORCID](https://orcid.org/0009-0001-9320-500X).

Manuscript and declared publication date: 13 October 2026 · Version 1.0.0 · **Unrefereed preprint**

[Read the paper (PDF, 4 pages)](weighted-yamabe-heat-trace-note.pdf) · [Download PDF](weighted-yamabe-heat-trace-note.pdf) · [Complete source and verification materials (ZIP)](weighted-yamabe-heat-trace-verification.zip) · [Zenodo record](https://doi.org/10.5281/zenodo.23383952) · [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

## Original abstract

Morpurgo’s volume-normalized weighted Yamabe heat trace comparison, stated for every dimension at least three, is false in dimension three. We specify one smooth positive conformal weight on the round three-sphere whose scaled heat trace exceeds 13/20 at a specified positive time, whereas the round maximum is less than 321/500. The argument applies classical cylindrical conformal geometry and Dirichlet min–max estimates. A finite cylinder length, explicit smooth caps, and exact rational certificates give quantitative separation.

## The idea in plain English

A heat trace adds together the decaying contributions of all the vibration modes of an operator. The Yamabe operator combines the Laplacian with a curvature term. Multiplying its heat trace by a power of time lets us compare the largest value reached by different conformal weights while keeping the volume normalization fixed.

Morpurgo’s comparison asks whether the round sphere gives the largest such value for every smooth positive normalized weight, in every dimension at least three. This note gives a counterexample on the three-sphere.

The construction stretches a region into a very long round cylinder and closes it with smooth caps. It fixes the cylinder length at 10000 and rescales the resulting metric to the round sphere’s volume. The resulting weight stays smooth and strictly positive everywhere.

At a specified positive time, its scaled heat trace is greater than 13/20. The round sphere’s value is less than 321/500 at every positive time. Since 13/20 is larger than 321/500, the weighted example has a strictly larger time maximum. Both maxima occur at finite positive times.

## The precise result

Let g₀ be the unit round metric on S³, let Δg₀ be the positive Laplacian, and define Y₀ = Δg₀ + 3/4 and YW = W^(-1/2) Y₀ W^(-1/2) on L²(dVg₀). There is one specified smooth strictly positive weight W with ∫S³ W^(3/2) dVg₀ = 2π² and an explicitly defined t* > 0 such that (t*)^(3/2) Tr(exp(-t* YW)) > 1106714561/1700054750 > 13/20, while max over t > 0 of t^(3/2) Tr(exp(-t Y₀)) < 321/500.

For the paper’s capped cylinder gL = WL g₀ with L = 10000 and VL = vol(gL), set a = (2π²/VL)^(2/3), W = aWL and t* = 4a. The paper defines WL by an explicit flat smooth cutoff and a convergent volume integral. These expressions specify one finite weight and time.

Both the weighted and round scaled heat traces attain their maxima at positive finite times. The dimension-three example refutes the comparison quantified over all dimensions n ≥ 3.

## Why the result holds

Classical cylindrical conformal geometry supplies the long product region. The explicit caps extend smoothly over both poles, and the final constant rescaling gives the exact volume normalization. Conformal covariance identifies the geometric Yamabe operator with the stated symmetric weighted operator.

Dirichlet sine functions on the cylinder, extended by zero, belong to the global quadratic-form domain. The min–max principle bounds every eigenvalue needed for an infinite heat-trace lower sum. A Gaussian integral and the finite cap-volume estimate give the displayed weighted lower bound.

The round sphere has an explicit spectrum. Gaussian Poisson summation controls small times, analytic interval and infinite-tail estimates control the middle range, and monotonicity controls large times. Exact rational inequalities complete the bound for every positive time.

The common small-time limit and decay at infinity, together with continuity and values above the small-time limit, ensure that both maxima are attained. The finite arithmetic certificates support these analytic arguments.

## Scope and limitations

The example is in dimension three. The comparison restricted to n ≥ 4 and the separate monotonicity conjecture for n ≥ 4 remain unaddressed.

The theorem uses the specified finite length, smooth caps, exact normalization and witness time. It makes no assertion that the witness time is a maximizing time, that a maximizing time is unique, or that the estimates are uniform over a degenerating family.

The cylindrical geometry, conformal covariance, Dirichlet trial spaces, min–max principle and Gaussian heat estimates are classical. The contribution presented here is a specified finite quantitative application to the historical comparison, with checkable bounds.

The historical source comparison is bounded. The inspected author versions and selected transformed-trace interfaces do not establish exhaustive coverage of the literature. Historical priority, worldwide firstness and continued worldwide openness remain unestablished.

The final 2011 Ammann–Jammes publisher chapter and complete final 2002 Morpurgo journal PDF were not authenticated in the underlying source comparison. The exact author editions and selected web interfaces used are distinguished in the accompanying materials.

## Status and AI use

OpenAI tools were used extensively in mathematical development, derivation, writing, coding, literature research and internal adversarial checking. This is an unrefereed preprint. Internal AI review is not external human or journal peer review, and no formal proof-assistant certification is claimed. The named author is responsible for the claims, materials and citations.

The manuscript and Zenodo’s declared publication date are 13 October 2026, version 1.0.0. Zenodo created the record on 15 October 2026 UTC. These edition dates do not establish historical priority.

## Read the paper

Read the complete four-page paper in the on-page PDF reader.

[Open PDF in a full window](weighted-yamabe-heat-trace-note.pdf) · [Download PDF](weighted-yamabe-heat-trace-note.pdf) · [Zenodo original PDF](https://zenodo.org/records/23383952/files/weighted-yamabe-heat-trace-note.pdf)

## Supporting materials

[Download the complete manuscript source and verification materials (ZIP)](weighted-yamabe-heat-trace-verification.zip) · [Zenodo original complete ZIP](https://zenodo.org/records/23383952/files/weighted-yamabe-heat-trace-verification.zip)

## Collaborate on this result

Substantive collaboration on independent verification of the finite construction and analytic estimates, a meaningful extension supported by proof, or development of a journal submission is welcome. Authorship and responsibilities would be discussed by mutual agreement and would reflect actual research and writing contributions.

## Cite this paper

Alec Kriebel. (2026). *A finite counterexample to the weighted Yamabe heat trace comparison* (Version 1.0.0, 13 October 2026) [Preprint]. Zenodo. [doi:10.5281/zenodo.23383952](https://doi.org/10.5281/zenodo.23383952).

[Download BibTeX](citation.bib)

## Background and prior work

[Morpurgo, Oberwolfach Report 6/2009, item (16), printed pages 421–422](https://doi.org/10.4171/OWR/2009/06). Records the original volume-normalized weighted Yamabe time-maximum comparison for n ≥ 3, and the separate monotonicity conjecture for n ≥ 4.

[Ammann and Jammes, The supremum of first eigenvalues of conformally covariant operators in a conformal class](https://doi.org/10.1017/CBO9780511863219.002). Classical conformally covariant spectral geometry and long-cylinder/Pinocchio constructions, with earlier constructions credited there. The note cites the 2011 chapter and identifies its inspected author manuscript dated 8 December 2008.

[Morpurgo, Sharp inequalities for functional integrals and traces of conformally invariant operators](https://doi.org/10.1215/S0012-7094-02-11433-1). Related classical transformed-trace inequalities. The inspected interfaces have a different stated functional class; that bounded comparison does not certify the absence of other relevant results.

[Research home](/research/) · [Blog](/blog/)
