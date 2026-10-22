# Independent source, model, and hypothesis audit

PR 908; problem 30006191 / OWR-14299085-005. Review date: 14 October 2026 UTC (13 October 2026 in the workspace timezone). Frozen candidate: `bounded_region_v2` at commit `a35667b1bb0bafed69916709997a4684223ecc93`.

**Family verdict: PASS for source/model alignment of the stated existential, dimension-three bounded-region claim.** No fatal model, topology, ordering, state, or potential-class mismatch was found. This family does not certify the complete proof, historical priority, present openness, or final promotion. The mathematical gate must also receive the independent analytic families' verdicts.

## 1. Independence, binding, and scope

The original problem record and authentic primary sources were examined before the author proof, package README, or any historical acceptance summary. The exact public clean statement is bound by SHA-256 `b1dbb64893b3d9001bde17e483192efb5cc7463cf06335aed11447a4c0fb55fe`; the supplied source review identity is `f23bfd4c411aac7c668dc28faa80b7ad4dd4393047c4ea03801bc3e6d82093a2`. The local private source-record wrapper separately hashes to `4f4ee09ed2e8b385c86dec6c96c895b62f653da676ec1eab5e1ddb31c978bfc3`; these identify different objects and are not interchangeable.

The author proof was then read in full and independently fingerprinted: 12,771 bytes, SHA-256 `2b7c22cfc54049a9e51fe5eb4eb283ba911e6f27e8b6e4dc9557927bc04d7350`. The package manifest is 3,790 bytes, SHA-256 `828280cc131c38e1f651b48b655dff177f880ba3505bba54e049510d81827795`. The package README was read only after source binding. It contains descriptions of old acceptances; those descriptions were not used as mathematical evidence. No historical audit body was read. No earlier `already_solved` packet was processed.

The full mathematical target is an example of an unregularized continuum fermion Hamiltonian and states witnessing failure of pointwise operator-norm continuity of the Heisenberg orbit of a fixed annihilation operator. The authoritative model locator is OWR 7/2025, printed p. 371, subsection 2.2 and equation (1), with the topology clarified on printed p. 365. The private extraction of the originally curated statement has interleaved neighboring paragraphs; their physical and asymptotic assumptions cannot be imported into this question.

## 2. Primary-source evidence and current versions

The official [EMS PDF](https://ems.press/content/serial-article-files/51350) was obtained directly, fingerprinted, extracted for search, and visually inspected on complete PDF pages 26, 27, and 33, corresponding to printed pages 364, 365, and 371. The [official landing page](https://ems.press/journals/owr/articles/14299085) authenticates DOI [10.4171/owr/2025/7](https://doi.org/10.4171/owr/2025/7), volume 22, issue 1, pp. 339-374, publication 29 August 2025, and the same PDF.

The relevant source evidence is precise: printed p. 365 distinguishes norm continuity from the weaker strong operator topology. Printed p. 371 separates the boson Hartree problem in subsection 2.1 from the fermion problem in subsection 2.2. The latter displays the all-space kinetic operator and a pair-density interaction over `Lambda x Lambda`, then asks for a particular potential and states for the unregularized `H_Lambda`. The smeared comparison orbit uses full-space notation after the thermodynamic limit. The requested counterexample is expressly phrased for `H_Lambda`.

The current official [arXiv 2409.10495 page](https://arxiv.org/abs/2409.10495), retrieved during this review, lists v2 (24 February 2025) as its latest version and records *Letters in Mathematical Physics* 115, article 33 (2025), DOI [10.1007/s11005-025-01919-y](https://doi.org/10.1007/s11005-025-01919-y). Its v2 PDF matches the supplied reference fingerprint exactly. The [publisher article](https://link.springer.com/article/10.1007/s11005-025-01919-y) and published PDF were also authenticated and inspected on the relevant model and main-result sections. The journal body is separately fingerprinted; its typography and PDF length differ from the arXiv body. Both contain the same relevant full-space, continuous-even-decaying pair-potential model, sector-continuous extended algebra theorem, and norm-continuous time-averaged subalgebra conclusion.

The current official [arXiv 2609.34402 page](https://arxiv.org/abs/2609.34402), also retrieved during this review, lists only v1, submitted 28 September 2026 at 06:15:26 UTC. The full PDF title page says 29 September 2026; these are different date fields, not a version discrepancy. Its fingerprint matches the supplied v1 exactly. Its arXiv-issued DOI is [10.48550/arXiv.2609.34402](https://doi.org/10.48550/arXiv.2609.34402); no journal reference or journal DOI was listed on that retrieved official page.

No access gap remains for the primary bodies used here. The web browsing tool's DOI redirects initially failed; direct retrieval from official EMS, arXiv, and Springer succeeded. This report does not infer body contents from metadata alone. Latest-version statements are point-in-time observations, not promises about subsequent changes.

## 3. Exact target and candidate model

Let `h = L^2(R^3)`, `F = direct_sum_n wedge^n h`, `Lambda = B(0,4)`, and `L = dGamma(1_Lambda)`. The candidate chooses one real, even, nonnegative `V` in `C_c^infinity(R^3)` satisfying `0 <= V <= 1` and `V = 1` on `Lambda - Lambda`. It sets

\[
H^{(\sigma)}=d\Gamma(-\Delta)+L(L-\sigma),\qquad \sigma\in\{0,1\}.
\]

The two values encode respectively inclusion and exclusion of diagonal pairs. The kinetic energy acts on all of `R^3`. `Lambda` restricts the interaction only; it is not a Dirichlet box or a confining kinetic boundary. The region, potential, and normalized `f` are fixed independently of particle number. A family of unit Slater vectors `Xi_N` and times

\[
t_N^{(\sigma)}=\frac{\pi}{2N+1-\sigma}\longrightarrow0
\]

is used to test one fixed annihilation operator. The claimed conclusion is

\[
\left\|\left(e^{it_N^{(\sigma)}H^{(\sigma)}}a(f)e^{-it_N^{(\sigma)}H^{(\sigma)}}-a(f)\right)\Xi_N\right\|\longrightarrow2,
\]

and therefore the corresponding ambient operator norm also tends to 2.

The target is existential. The supplied clean statement contains no universal dimension quantifier, and the original subsection uses generic `R^d` notation without stating a requirement to produce an example in every fixed dimension. A valid dimension-three instance answers that existential request. It must not be promoted to an all-dimensional theorem: nonrelativistic dimensions one and two remain outside the candidate's estimate. If the human elects a stronger goal requiring an example for each arbitrary fixed `d`, this package would be a partial result with that exact missing target. The report preserves this boundary rather than silently rewriting the source as a universal theorem.

Likewise, no part of the displayed fermion question asks for every potential, every bounded region, a fixed-density thermodynamic state sequence, or a fixed normal state. The neighboring boson subsection's `N/|Lambda|`, high-density scaling, zero-temperature class, and Hartree approximation are separate questions. The generic full-space discussion on p. 365 motivates the issue but does not erase the explicit bounded-interaction model on p. 371.

## 4. Independent ordering and Hamiltonian checks

The formal field expression requires a rigorous interpretation; `a_x` is an operator-valued distribution and cannot be multiplied pointwise without explanation. On the `n`-particle sector write

\[
L_n(X)=\sum_{j=1}^n1_\Lambda(x_j).
\]

The density product interpreted with its diagonal contribution gives the multiplication operator

\[
\sum_{i,j=1}^n1_\Lambda(x_i)1_\Lambda(x_j)V(x_i-x_j)=L_n(X)^2.
\]

The equality is exact for every configuration away from irrelevant boundary null sets: every difference of two points in `Lambda` lies in the plateau. Omitting `i=j` gives

\[
\sum_{i\ne j}1_\Lambda(x_i)1_\Lambda(x_j)V(x_i-x_j)=L_n(X)(L_n(X)-1).
\]

The same distinction follows formally from the CAR contraction of `a_x^* a_x a_y^* a_y`: its normal-ordered pair term is supplemented by `delta(x-y) a_x^* a_y`, whose integral is `V(0)L`. Here `V(0)=1`, so the supplement is exactly `L`, consistent with `L^2 = L(L-1)+L`. The candidate uses rigorous sector multiplication operators rather than treating this distribution manipulation as a construction.

There is no factor `1/2` in the displayed source formula or in the candidate. The pair term is an ordered sum; a convention using an unordered sum would change the coupling. This is not a flaw in the reviewed coefficient-one claim. More generally a fixed positive overall coupling `c` only changes the selected times to `pi/[c(2N+1-sigma)]` and the error constants; the frozen example already uses the source's displayed coefficient.

For every fixed `n`, `0 <= L_n <= n` and each `L_n(L_n-sigma)` is real bounded multiplication with norm at most `n^2`. It is therefore a bounded self-adjoint perturbation of the all-space sector kinetic operator `T_n = sum_j(-Delta_j)`, on `D(T_n)`. Exchange symmetry preserves the antisymmetric subspace. The maximal direct sum is self-adjoint; the vacuum term is zero. The perturbation is unbounded across particle sectors, which is precisely compatible with the source's unregularized continuum setting. A bounded spatial interaction region does not make the full-Fock perturbation bounded.

## 5. Potential, state, and quantifier tests

The explicit bump quotient has denominator

\[
b(81-|x|^2)+b(|x|^2-64),\qquad b(s)=e^{-1/s}\ (s>0),\quad b(s)=0\ (s\le0).
\]

Both denominator terms could vanish only if `|x|^2 >= 81` and `|x|^2 <= 64` simultaneously; this is impossible. Flatness of `b` at zero gives smoothness through the transition radii. The quotient is radial, real, even, nonnegative, at most one, equal to one for `|x| <= 8`, and zero for `|x| >= 9`. These are exact checks. It is bounded, integrable, square-integrable, continuous, and vanishes at infinity.

No positive-type or Fourier-positivity requirement is stated in the original fermion subsection. The Fourier-transform restriction discussed on p. 364 concerns a one-body potential called `V` there, whereas the pair potential is called `W`; the notation is reused for the pair potential on p. 371. The candidate's external one-body potential is zero, so it also meets that one-body restriction if the older regularized comparison class is consulted. Spatial nonnegativity of the candidate pair potential must not be confused with positivity of its Fourier transform, which this package does not claim. A new Fourier-positive assumption would require a new audit and cannot be silently added.

The related 2409.10495v2 and published model requires a real continuous even pair potential vanishing at infinity. The candidate `V` meets these regularity and decay properties, although its spatially cut off kernel is a different Hamiltonian. In 2609.34402v1, Hypothesis B allows measurable real even `W` in `L^2+L^infinity`, bounded below; the candidate potential also meets that class. There is no small coupling, small norm, or fixed-density bound in those pair-potential hypotheses. Its Laplacian and zero external field meet that paper's Hypotheses A, C, D in dimension three. These compatibility observations do not permit applying a full-space theorem directly to a non-translation-invariant kernel.

The `N` packet orbitals have mutually disjoint supports in one fixed cube contained in `B(0,3)` and are normalized. The fixed `f`, supported in `B(0,1/2)`, is disjoint from that cube. Orthogonality and the normalized Slater convention therefore give unit `Psi_N` and `Xi_N = a^*(f)Psi_N`, with `a(f)Xi_N = Psi_N`. For each finite `N`, these smooth compactly supported vectors belong to the relevant kinetic and full Hamiltonian domains and have finite kinetic energy. Their energy and local particle density need not be uniformly bounded in `N`; neither source target nor candidate claims such a bound. There is no violation of Pauli exclusion: infinitely many different modes are available in a continuum region.

The state family is essential, rather than an illicit variation of the observable. It is legitimate to choose a different unit vector for each operator norm lower bound. The positive bounded test operator `D_N^*D_N` then has vector-state expectation tending to 4. In a number eigenstate the expectation of the odd operator `a(f)` itself is zero; the positive test measures its action and is a valid norm witness. The states do not establish a fixed normal-state scalar discontinuity.

## 6. Independent topology and representation tests

For self-adjoint `H`, bounded `B`, and a fixed vector `eta`, the following exact estimate proves strong operator continuity:

\[
\|(e^{itH}Be^{-itH}-B)\eta\|
\le \|B\|\|(e^{-itH}-1)\eta\|+\|(e^{itH}-1)B\eta\|\longrightarrow0.
\]

This is independent of the number of particles in `eta` or its membership in `D(H)`. It also implies continuity in every fixed normal state: write a positive trace-class density operator as `rho = sum_j p_j |eta_j><eta_j|`. The summands in

\[
\operatorname{Tr}(\rho D_t^*D_t)=\sum_jp_j\|D_t\eta_j\|^2
\]

converge to zero and are dominated by `4||B||^2 p_j`, a summable bound. Thus the claimed varying-state lower bound is compatible with ordinary Schrödinger and strong operator continuity. Any reinterpretation of the problem as requiring failure on one fixed Fock vector would be impossible for the displayed self-adjoint implementation and would contradict the report's explicit topology clarification.

The CAR algebra in the standard Fock representation is the norm-closed algebra generated by these bounded creation and annihilation operators. Its faithful representation preserves the intrinsic norm. The candidate compares the implemented Heisenberg orbit with `a(f)` in `B(F)`, which remains meaningful even without CAR invariance. If this implementation were a pointwise norm-continuous automorphism group of the CAR algebra, that fixed orbit would necessarily be norm continuous in this same faithful norm. A norm discontinuity rules out the asserted continuity property without needing a separate non-invariance theorem.

The candidate does not assert that its dynamics preserves the CAR algebra. It also does not derive non-invariance. Those are distinct questions; the source asks for a discontinuous fixed field orbit, so failure of that necessary continuity property is enough for the stated counterexample target. Faithfulness and ambient bounded-operator comparison do not justify any unproved preservation or non-invariance claim.

## 7. Current related-theorem scope

The actual body of 2609.34402v1, section 2.2 and Theorem 2.4, uses an ordered full-space sum of a translation invariant kernel `W(x_i-x_j)`. It treats a pair potential with two nonzero continuity points at which its values differ, compatible dispersion, and local external-field propagation. It gives fixed-observable norm discontinuity and, by a separate automatic-continuity argument, CAR non-invariance. Its Laplacian example includes `d >= 2`; its relativistic example includes every `d >= 1`. This difference does not extend the present nonrelativistic candidate to dimensions one and two.

Its Proposition 2.6 treats the full-space constant interaction `c N(N-1)` with arbitrary self-adjoint one-particle dynamics. That result directly concerns the candidate's reference-phase mechanism, but not the candidate's interacting Hamiltonian: `L = dGamma(1_Lambda)` is not the total number `N` once particles move outside `Lambda`, and `L` does not commute with the all-space Laplacian. The cutoff kernel

\[
K_\Lambda(x,y)=1_\Lambda(x)1_\Lambda(y)V(x-y)
\]

is not translation invariant and cannot be represented by a function of `x-y` alone on all of space. Two pairs with the same difference can have different membership in `Lambda x Lambda`. The current theorem's hypotheses therefore do not literally include the cutoff example, even though locally the plateau suggests related phase arguments.

The candidate supplies additional leakage and comparison estimates to handle that difference. Its kinetic packing exponent `N^(5/3)` gives the reference-comparison errors `O(N^(-1/6)+N^(-1/3))` at `t=O(1/N)`. Algebraically, the corresponding general-dimension exponents are `-1/2+1/d` and `-1+2/d`, both strictly negative precisely for `d>2`. This independently confirms why the written candidate has the stated dimension boundary; it is not a proof in `d=2` with a hidden logarithmic improvement.

These two inspected sources do not supply a literal theorem for the spatially cut off pair kernel as displayed above. This is a theorem-scope finding, not a claim that no earlier exact bounded-region result exists. No priority search was conducted, and no discovery status is inferred from an author's historical introduction.

## 8. Mathematical idealization and exact remaining limits

The construction is a mathematical model with the constants in the kinetic operator and evolution absorbed into units. One may read `hbar = 1` and `hbar^2/(2m) = 1`, together with the chosen interaction energy unit. Restoring fixed positive physical constants rescales the short times and comparison constants, without adding an empirical assertion. The radii 4, 8, 9 are dimensionless choices in those units. No measured force, material parameter, experimental density, or real-world time discontinuity is asserted.

The strongest result this family verifies is that the frozen theorem's model and quantifiers genuinely furnish an admissible instance of the bound existential source target, and its norm conclusion would answer that target if its independent analytic proof checks pass. Ordering identities, self-adjoint model construction, potential admissibility, fixed-observable versus varying-state logic, automatic SOT continuity, fixed-normal-state continuity, and the related-theorem scope distinctions have been checked analytically here.

The exact remaining gates are the complete continuum leakage/Duhamel/Slater/matrix-element proof verification by the independent analytic families, and only afterward any authorized priority review. This family has neither requested nor performed candidate revisions, PR or Sheet edits, publication, Git commits or pushes, outreach, or communication with individuals. All primary raw material, extraction text, HTML bodies, and screenshots remain in ignored private storage and are excluded from the public intentional-file manifest.

## 9. Falsification outcomes

| Attempted mismatch | Outcome | Exact boundary |
| --- | --- | --- |
| Strong operator continuity substituted for C*-strong continuity | Rejected by source and direct estimate | All fixed-vector and fixed-normal-state continuity survives |
| Neighboring Hartree density restrictions imported | Rejected by complete page layout | Separate boson subsection 2.1 |
| Dirichlet box substituted for all-space kinetic operator | Not present in candidate | `Lambda` cuts only the interaction |
| Normal ordering or diagonal term silently changed | Both conventions expressly treated | `L^2` and `L(L-1)` differ by `L` |
| Ordered pair coefficient doubled or halved | No mismatch at displayed coefficient one | A half convention needs rescaled times |
| Fourier-positive interaction silently assumed | No such target assumption found | Spatial positivity is not Fourier positivity |
| N-dependent potential, region, or test observable | Not present | Only vectors, particle number, and times vary |
| Packed states excluded by finite density or energy rule | No applicable source rule | Not a fixed-density thermodynamic construction |
| Full-space theorem invoked as exact cutoff theorem | Candidate does not do this | Cutoff leakage estimates are substantive new obligations |
| Dimension three relabeled as every fixed dimension | Candidate expressly excludes this | `d=1,2` remain beyond this mechanism |
| Norm failure used to assert CAR preservation | Candidate makes no preservation claim | Compare the orbit in faithful `B(F)` norm |
| Norm failure used to claim historical novelty or current openness | Excluded from this family | Later priority gate required |

The public `RESULT.json` and `SOURCE_MANIFEST.json` record the machine-readable verdict, fingerprints, primary identities, version observations, and locators. `MANIFEST.json` freezes only this family's intentional public files, excluding itself and all raw sources.
