# Source/prior-attempt gate: 30005240 / OWR-11101924-003

**Gate checkpoint, zero substantive author turns.** The direct UnsolvedMath page was inaccessible. The complete pinned problem record at dataset revision 37e53eabe540fb458758e198be61634bd02ee008 was read; no matching prior research-results entry exists. The primary source controls the mathematical target rather than the imported title alone.

## Exact source and scope

Fatih Ecevit, *A survey on high-frequency scattering relating to smooth convex scatterers*, [OWR 43/2022](https://ems.press/content/serial-article-files/46980), printed pp. 2545–2548, was read in full. All four contribution pages were rendered and visually inspected, including the displayed rate on p. 2547. The report's publication label is 2023; the workshop/report year is 2022.

The setting is time-harmonic exterior Helmholtz scattering by a finite disjoint collection of smooth compact convex obstacles, with wavenumber k tending to infinity. The density eta_m is the normal derivative of the m-th total field on the current obstacle for Dirichlet scattering, and the total boundary field for Neumann scattering. The extracted phase is the optical path length after m reflections. The Airy transition coordinate is k^(1/3) Z_m. The source already records high-frequency expansions for fixed multiple-scattering iterations.

The selected open question concerns the **actual-density periodic-orbit convergence rate**, presented in the Dirichlet discussion. It is not merely the existence of those fixed-iteration expansions. It must distinguish high frequency k, reflection count m, a period n, leading amplitudes and actual densities. The source's displayed positive two-period number suppresses the optical phase; the cited analysis instead uses the complex multiplier

    R_(n,k)=(-1)^n exp(i k Phi_n) product_(r=0)^(n-1) L_r^(-1/2).

The primary continued-fraction definition of L_r and the printed special-case simplification must be reconciled before that simplified number is used as a proof target. No silent normalization or phase correction is adopted at this gate. In particular an editorial prefactor issue, if confirmed, would not by itself settle the intended actual-density remainder problem.

## The exact known conditional result

Ecevit–Reitich, *Analysis of multiple scattering iterations for high-frequency scattering problems. I: The two-dimensional case*, Numerische Mathematik 114 (2009), 271–354, DOI [10.1007/s00211-009-0249-z](https://doi.org/10.1007/s00211-009-0249-z), was checked through the author-provided full manuscript text and the complete [MPI preprint 137/2006](https://files-www.mis.mpg.de/mpi-typo3/preprints/2006/preprint2006_137.pdf). The latter is an earlier version, not silently treated as the published pagination. The publisher PDF route returned HTML rather than a PDF; the published-manuscript text and preprint are distinguished in the retrieval record.

The published manuscript's Section 3 assumes disjoint compact strictly convex C-infinity boundaries, visibility of successive obstacles, no occlusion relative to the incident direction, and its explicit Assumption C extending the single-scattering expansion to smooth convex wavefront incidence with a classical slow-symbol expansion. The curvature lower bounds used in its ray estimates must not be silently dropped. Its Section 4 proves convergence rates for approximate optical currents through dispersing-ray estimates and continued fractions.

For actual currents it writes eta_m=(1+k^(-1)P_m)2ik eta_m^A on compact illuminated subsets. Corollary 4.1 (earlier preprint Corollary 4.14) is conditional on

    S_(m,n)=(P_(m+n)-P_m)/(k+P_m)=O(k^(-1)),
    T_(m,n)=(k+P_(m+n))/(k+P_m)=O(1),

**uniformly in m**. Then, on compact subsets of the jointly illuminated regions and for m>2n, the relative estimate has the form

    |eta_(m+n)-R_(n,k)eta_m|
      ≤ [O(k^(-1)delta^n)+O(k delta^(m+n))+O(delta^(m-n))]|eta_m|,

for a geometric delta in (0,1). Fixed-m P_m=O(1) does not imply these uniform hypotheses. The published numerical section treats extension of the estimate to the whole boundary as a heuristic supported by experiments, not a completed proof. Pointwise ratios additionally need denominator/nonvanishing control, especially in shadow and transition regions. A proof on a compact illuminated subarc must not be relabeled as the global-boundary statement.

The three-dimensional analysis, Anand–Boubendir–Ecevit–Reitich, Numerische Mathematik 114 (2010), 373–427, DOI 10.1007/s00211-009-0263-1, was read in the [author-hosted earlier preprint](https://web.njit.edu/~boubendi/highfreq1.pdf). Its scalar rate involves principal curvature matrices and their relative rotation. Its actual-current corollary also has explicit uniform-in-m remainder hypotheses. A two-dimensional recurrence calculation would not resolve the three-dimensional version.

## Current primary literature check

Boubendir–Ecevit's [arXiv:2208.06257v1](https://arxiv.org/abs/2208.06257) was downloaded and its setup, statements and remainder/derivative estimates were inspected. It became *High-frequency asymptotic expansions for multiple scattering problems with Neumann boundary conditions*, JMAA 544 (2025), article 129047, DOI [10.1016/j.jmaa.2024.129047](https://doi.org/10.1016/j.jmaa.2024.129047), as confirmed by the author's institutional publication record. These results concern fixed-iteration expansions and wavenumber-explicit derivative estimates. They do not state the missing uniform periodic-orbit actual-density theorem. The introduction explicitly presents rate analysis as a further application.

Targeted searches of the exact target, the source author's later work and periodic convergence-rate terms found no verified complete resolution of that missing step. An April 2025 author seminar advertises preliminary developments on the infinite tail, not a checked full periodic-rate theorem. This is a bounded literature gate, not a novelty certificate. The neighboring target 30005241 concerns collective returns and the possibly divergent infinite tail; it is distinct and is not being attempted here.

## Prior-attempt gate

Live all-state PR searches for 30005240, OWR-11101924-003, the title and multiple-scattering aliases returned no matching PR. Exact attempt-path histories in both repository locations were empty. Matching-ref/branch and commit searches for the ID returned no hits. The read-only local mirror audit covered 374 refs and found no target path or matching target/title/rate-density commit history. The live checks supplement that earlier mirror; no claim is made that its ref inventory itself was refreshed.

The target is eligible for a first genuine proof attempt, with a fresh five-turn budget. Source retrieval, version comparison, formula-fidelity checks and this gate do not count as author turns. No theorem for actual densities has yet been derived in this attempt.
