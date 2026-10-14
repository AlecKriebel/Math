# PR263 independent broad primary priority audit

Audit cutoff: 2026-10-11 UTC. Reviewer: independent broad-literature subagent. This report is separate from the Cross thesis/talk audit. No outside person was contacted, and no outreach was prepared. Copyrighted reading copies and extracted source text are confined to ignored `private_reading/`.

## Decision

**Priority: HOLD.** In the primary bodies and sections actually read below, I did not locate a theorem asserting the exact accepted complex-quadratic projection conclusion or the exact whole-abscissa-epigraph obstruction. That is a bounded audit finding, not evidence of firstness or present-day openness. Several materially relevant original sources remain unread, and Cross's 2010 thesis is being audited independently. The foundational stability-boundary cusp mechanism is already classical.

**Research-note framing: qualified GO.** A self-contained proof note may state the accepted mathematical result, identify the precise complex convention of the historical question it answers, and explicitly credit the prior stability geometry and projection theorem. It should omit “new,” “first,” “previously unknown,” and any claim that the question remained open through 2026. This is not a priority clearance and does not override the root's mathematical/source-scope acceptance or administrative requirements.

**Already-known assessment:** the underlying Whitney-umbrella stability geometry, first-order polynomial root/normal calculus, and the prox-regularity/local-single-valued-projection equivalence are known ingredients. Exact theorem overlap for the final accepted claim is **not established by this broad audit**. A discovery that an older body already contains the required ambient normal-support argument or projection-tie theorem would change the priority decision.

## Exact target and exclusions

The target is the root-accepted statement: for each fixed SPD real inner product on complex quadratic coefficient space, every neighborhood of `z²` contains an unstable polynomial with at least two distinct attained global nearest polynomials whose roots lie in the closed left half-plane. The monic and full exact-degree coefficient spaces are both included. The other accepted statement is failure of **set** prox-regularity of the whole polynomial-abscissa epigraph at `(z²,0)`.

The normal mechanism in the submitted proof is

\[
p_t(z)=z^2+t^2z+t^2+it^3=(z+it)(z+t^2-it),\qquad
n_t=(-t,-t^2/2,-t/2,1)\longrightarrow(0,0,0,1).
\]

Comparison with `p_{√2 t}` gives positive normal support of order `t³` against squared coefficient distance of order `t⁴`. The limiting direction is horizontal in the epigraph. It therefore does not resolve the separate finite-subgradient function-prox-regularity conjecture. The audit also excludes a real-only classification, an all-degree classification, and an explicit input together with its two minimizers.

Inputs read: `ROOT_SCOPED_MATH_SOURCE_ACCEPTANCE.json`; the frozen `original_submission/files/attempts/30000170/PROOF.md` and `SOURCE_SCOPE.md`; and `source_alignment/SOURCE_ALIGNMENT_AUDIT.md`. The scoped author's revised file was not substituted for the frozen submission during the independent comparison.

## Primary-body comparison

“Read” means the stated substantive body extent, not merely an abstract or search hit. Full-text term scans supplement those reads; they do not certify every unexamined proof. Each technical conclusion below is supported by an author-hosted paper, publisher body, or primary preprint. Sources recovered only as records/abstracts are listed separately as unknown.

| Primary source and version | Substantive extent read | Exact relevance and boundary |
|---|---|---|
| [Burke–Overton, *Stable Perturbations of Nonsymmetric Matrices* (1992)](https://sites.math.washington.edu/~burke/papers/reprints/16-stable-perturb.pdf), LAA 171, 249–273 | Introduction, pp. 249–252, and opening polynomial perturbation discussion; whole-body term scan | Complex matrix/root perturbations and necessary/sufficient first-order stability directions. A precursor to root-splitting calculus; the read results do not assert uniform quadratic normal support or tied nearest complex quadratics. |
| [Burke–Overton, *Variational Analysis of the Abscissa Mapping for Polynomials* (2001)](https://sites.math.washington.edu/~burke/papers/reprints/37-va-abs-poly.pdf), SICON 39, 1651–1676 | Introduction; Thm. 1.2, p. 1654; opening normal characterization, Thm. 2.1; Thm. 3.2, p. 1673, and its proof; concluding application/references; whole-body term scan | Complex coefficient spaces. Thm. 3.2 establishes subdifferential/epigraph Clarke regularity. The tangent/normal descriptions are classical ingredients. Clarke regularity does not supply the uniform curvature bound required for local unique projection. |
| [Lewis, *The Mathematics of Eigenvalue Optimization* (2003)](https://people.orie.cornell.edu/aslewis/publications/03-mathematics.pdf), MP 97, 155–176 | Entire §8, pp. 166–168 | Explicitly uses complex monic polynomial coefficients. Thm. 8.1 gives Clarke regularity; Thm. 8.3 describes partial smoothness. Page 168 asks whether the stable monic set is prox-regular, explaining its implication for nearby unique projections. This is an exact historical set-question antecedent, not its solution. |
| [Burke–Lewis–Overton, Gauss–Lucas note (2004)](https://sites.math.washington.edu/~burke/papers/reprints/48-Gauss-Lukas.pdf), JGO 28, 259–268 | Introduction/§2, including Thm. 2.1, pp. 259–261; whole-body term scan | An alternative proof of complex polynomial-abscissa Clarke regularity and its normal formula. The stated stronger projection obstruction is not the theorem being proved. |
| [Burke–Lewis–Overton, *Variational Analysis of Functions of the Roots of Polynomials* (2005)](https://sites.math.washington.edu/~burke/papers/reprints/53-va-polys-GL.pdf), MP 104, 263–292, DOI 10.1007/s10107-005-0616-1 | Introduction/domain; entire §6 conclusion, p. 291; surrounding root-radius material; whole-body term scan | First- and second-order root-function calculus. The concluding conjecture cites RW Definition 13.27 for function prox-regularity. It must not be treated as the same as whole-epigraph set prox-regularity in all normal directions. |
| [Lewis, *Eigenvalues and Nonsmooth Optimization*, author-posted chapter](https://people.orie.cornell.edu/aslewis/publications/focm-paper.pdf) | §§1.4–1.5 and §1.7, including pp. 7–9 and 15 | Complex stable monics, Clarke regularity, and the stronger projection/epigraph question. This author's posted chapter corroborates the historical distinction; precise publication metadata was not independently settled here. |
| [Lewis, *Nonsmooth Optimization and Robust Control* (2007)](https://people.orie.cornell.edu/aslewis/publications/07-nonsmooth.pdf), Annual Reviews in Control 31, 167–177 | Entire p. 172, §7 and Thm. 7.1 | States the complex monic regularity theorem, describes prox-regularity using unique nearest epigraph points, and describes abscissa prox-regularity as apparently open at that time. This is evidence about 2007, not evidence of current openness. |
| [Burke–Eaton, *On the Subdifferential Regularity of Max Root Functions for Polynomials* (2012)](https://sites.math.washington.edu/~burke/papers/reprints/69-polys-Julie.pdf), NA 75, 1168–1187 | Introduction; Prop. 5.5, p. 1181; Thm. 6.2 and opening proof, p. 1183; root-radius theorem; whole-body term scan | Complex coefficients with real inner products. Includes horizon/recession subdifferentials and regularity under convex-generator conditions. The theorem identifies regular and limiting subdifferentials; it does not assert prox-regularity or local unique metric projection. |
| [Burke–Eaton, *Variational Analysis of Convexly Generated Spectral Max Functions*](https://sites.math.washington.edu/~burke/papers/reprints/88-va-cvx-max.pdf), DOI 10.1007/s10107-016-1088-1; accepted 25 October 2016, MP 168 (2018), 63–92 | Introduction; Thm. 6, Lemma 7, Thm. 11; concluding discussion; whole-body term scan | Matrix spectral max functions. Regularity is linked to nonderogatory active eigenvalues. This strengthens subdifferential characterization, not the accepted coefficient-space projection property. The 2016 DOI/copyright date and 2018 volume date are distinct. |
| [Overton, author-posted 2014 book chapter](https://cs.nyu.edu/~overton/papers/pdffiles/banff_paper.pdf), *Nonlinear Physical Systems* | §16.1.6, p. 360, and §16.3, p. 372; surrounding root optimization and references; whole-body term scan | Reviews polynomial-root and matrix spectral optimization, crediting the 2001/2005/2012 regularity chain. The relevant read body supplies optimization background, not an exact projection-tie result. |
| [Mailybaev–Seyranian, *On Singularities of a Boundary of the Stability Domain* (1999)](https://alexei.impa.br/data/_uploaded/file/papers/1999%20SIAM%20J.%20Matrix%20Anal.%20Appl.%2021%281%29%2C%20106-128.pdf), SIMAX 21, 106–128 | Primary parsed PDF: pp. 106–107; selected §4 classification/tangent-cone passages; §6 example introduction; selected §7 polynomial transfer and derivative formulas, eqs. (7.6)–(7.11); conclusion | Real parameter families, generic low-dimensional stability-boundary singularities, and transfer from matrices to polynomials. Derivative/root-splitting formulas are relevant classical ingredients. The inspected results are tangent-cone/singularity statements, not the exact complex-quadratic nearest-point theorem. |
| [Kirillov–Overton, *Robust Stability at the Swallowtail Singularity* (2013)](https://cs.nyu.edu/~overton/papers/pdffiles/swallowtail.pdf), Frontiers in Physics 1:24, DOI 10.3389/fphy.2013.00024 | Entire pp. 1–2, especially eqs. (4), (6), and (10) | Real quartic stability region and its Whitney-umbrella boundary. This is material geometric overlap, detailed below. It precludes describing the stability cusp itself as a newly discovered phenomenon. |
| [Poliquin–Rockafellar–Thibault, *Local Differentiability of Distance Functions* (2000)](https://sites.math.washington.edu/~rtr/papers/rtr170-LocalDiffDistance.pdf), TAMS 352, 5231–5249 | Definition 1.1, Prop. 1.2, Thm. 1.3, pp. 5233–5235 | Classical uniform quadratic normal-support characterization and, in finite dimension, Thm. 1.3(k)'s equivalence with local single-valued projection. This is the accepted proof's bridge from support failure to projection ties, not a novel ingredient. |
| [Cruces–Pérez-González–Docampo, *Determination of the Optimal Stable Projection for AR Systems*, author-hosted COST94 copy](https://personal.us.es/sergio/PAPERS/COST94.pdf) | Introduction, stability-region section, conclusion/references; whole-body term scan | Discrete AR/unit-circle coefficient projection algorithms, including second-order convex updates and local behavior. The read domain and algorithmic conclusion differ from ambient complex quadratic half-plane projection. Full proceedings metadata was not checked. |
| [Gillis–Sharma (2017)](https://orbi.umons.ac.be/bitstream/20.500.12907/42022/1/26%20On%20computing%20the%20distance%20to%20stability%20for%20matrices%20using%20linear%20dissipative%20Hamiltonian%20systems.pdf), Automatica 85, 113–121, DOI 10.1016/j.automatica.2017.07.047 | Introduction/domain, p. 114; DH formulation/Remarks 4–6; conclusion | Real matrix Frobenius algorithms. Its stable domain includes semisimplicity of imaginary eigenvalues and is not closed; the relaxed DH formulation is discussed separately. Nonuniqueness of a DH factorization is not nonuniqueness of nearest polynomial coefficients. |
| [Noferini–Poloni (2021), primary arXiv v2](https://arxiv.org/pdf/2002.07052v2), revised 7 February 2021; [published body](https://link.springer.com/article/10.1007/s00211-021-01217-4), Numerische Mathematik 148, 817–851 | §3 complex Schur reformulation, Thm. 3.2; §5.1, Lemmas 5.4–5.5, Example 5.6 and Remark 5.7; §7.6 | Frobenius matrix nearness to a prescribed closed spectral region. Explicit candidates for real 2×2 matrices and a complex-versus-real matrix discussion. Polynomial coefficient distance and full matrix Frobenius distance are different optimization problems. |
| [Kuo–Cheng–Syu–Shieh (2021), published body](https://www.aimsciences.org/data/article/export-pdf?id=2eaa1e6a-c5e2-423b-a60d-6c108b26f615), DCDS-B 26, 2025–2035, DOI 10.3934/dcdsb.2020358 | Domain/summary, pp. 2025–2026; Thms. 3.4–3.5 and proof portions, pp. 2031–2034; conclusion | Closed-half-plane stability for real 2×2 matrices; formulas distinguish unique, two, and infinitely many minimizers under stated hypotheses. The conclusion leaves the complex matrix problem for later work. Multiple matrices may have identical characteristic polynomial; see the boundary check below. |
| [Drusvyatskiy–Ioffe–Lewis (2015)](https://people.orie.cornell.edu/aslewis/publications/15-clarke.pdf), MOR 40, 328–349, DOI 10.1287/moor.2014.0672 | Introduction; positive-reach attribution on p. 336; Remark 3.6 and surrounding geometry; Thm. 3.10 proof/discussion; whole-body term scan | General stratifiable, directionally Lipschitzian subdifferential representation. Positive reach is cited as a hypothesis of other results. No polynomial-abscissa example appears in the term scan; the read theorem does not establish reach for the target epigraph. |
| [Heß–Henrion–Lasserre–Pham, primary arXiv 1507.08463 copy](https://arxiv.org/pdf/1507.08463), related published SICON 54 (2016), 1633–1656, DOI 10.1137/15M1033198 | Introduction, §2 domain, conclusion; whole-body term scan | Real polynomial parameter families and convergent semidefinite approximations to abscissa. The retrieved PDF bears arXiv v1's 2015 identifier and an internal draft date 26 May 2022; no new edition date is inferred. The read object is approximation, not nearest stable coefficients. |
| [Liu–Davanloo Tajbakhsh (2024)](https://proceedings.mlr.press/v238/liu24e/liu24e.pdf), PMLR 238 | §2 equations (3)–(6), projection discussion; §3 equation (12) and projection implementation | Real ARMA/unit-circle domains. Explicitly allows nonunique projections in general, without a local theorem at the complex quadratic half-plane cusp. “Proximal” in its title concerns its algorithm and is not a claim of set prox-regularity. |
| [Mehrmann–Mengi, primary arXiv 2409.04297 v3](https://arxiv.org/pdf/2409.04297v3), 1 September 2025 | Introduction, eqs. (1.1)–(1.7), nondegeneracy/smoothness setup in §2, discussion comparing linearization | Positive-tolerance pseudospectral-abscissa optimization for parameterized quadratic matrix polynomials. Its uniqueness hypotheses concern the rightmost pseudospectral point. This is distinct from nearest scalar stable polynomial projection and the zero-tolerance whole epigraph. |

## Material classical geometric overlap

The 2013 quartic paper studies

\[
\lambda^4+a_1\lambda^3+a_2\lambda^2+a_3\lambda+1,
\quad a_1,a_3>0,
\quad a_2>2+\frac{(a_1-a_3)^2}{a_1a_3}.
\]

It identifies a Whitney-umbrella boundary at `(a₁,a₃,a₂)=(0,0,2)`. Its attribution reaches earlier Bottema/Arnold work; those originals have not been independently read here. [Primary equations and discussion](https://cs.nyu.edu/~overton/papers/pdffiles/swallowtail.pdf).

**Own algebraic comparison, not a theorem claimed from that source:** let `x=(a₁+a₃)/2`, `v=(a₁−a₃)/2`, `u=a₂−2`. The strict stability inequality becomes

\[
u x^2>(u+4)v^2.
\]

Near the singular point, the smooth coordinate `V=v√(u+4)` gives the positive solid `V²<x²u`, with `x,u>0`. Independently, for the complex monic quadratic `z²+(x+iy)z+(u+iv)`, the shift `z=w−iy/2` gives coordinates

\[
U=u+y^2/4,\qquad V=v-xy/2,
\]

and the full closed stable set is `x≥0, U≥0, V²≤x²U`, with `y` free. These are genuine ambient coefficient coordinates. The shape generating the accepted support-ratio obstruction is consequently a classical stability singularity. This comparison does not by itself establish the all-metric nearest-point theorem: one still needs normal/support control, metric handling, and global attainment/localization. A nonproximal slice alone would not suffice.

## Adversarial boundary checks

1. **Clarke/partial smoothness versus prox-regularity.** The 2001/2003/2012/2018 theorems identify first-order normal geometry or regular/limiting subdifferentials. They do not provide a bounded quadratic support constant near the cusp. The accepted positive `t³` versus `t⁴` quotient is compatible with those older regularity theorems.
2. **Whole epigraph versus finite-subgradient function condition.** The accepted scaled graph normals approach `(n₀,0)`. A theorem or conjecture formulated for `(v,−1)` with finite `v` cannot be ruled out by this horizontal limiting normal alone. The note must preserve this scope distinction.
3. **Matrix ties versus polynomial ties.** In Kuo et al., Thm. 3.5(ii)'s real matrix minimizers in equation (3.18) both have trace and determinant zero; thus they both have characteristic polynomial `z²`. Their matrix multiplicity is not distinct polynomial multiplicity. Moreover, for the real Jordan block `J=[[0,1],[0,0]]`, inputs in a sufficiently small real matrix neighborhood have `b−c≠0` and the uniqueness parameters in the paper stay nonzero. Its unique-projection cases therefore do not contradict the complex coefficient result. [Primary theorem/domain](https://www.aimsciences.org/article/doi/10.3934/dcdsb.2020358).
4. **Fixed inner product versus a pulled-back nonlinear distance.** A matrix characteristic map or Cayley transform can preserve spectral stability while changing the optimization metric. A polynomial theorem valid for every fixed SPD coefficient inner product still needs an argument if the transformation induces a variable metric. Such a transfer was not assumed in this audit.
5. **Closed versus strict/semisimple stability.** Nonexistence of a minimizer in an open stable set, or in the nonclosed Lyapunov-stable matrix set, is different from multiple attained nearest points in the accepted closed polynomial set.

## Unknown primary bodies and material follow-up

The following are not cleared by abstracts, metadata, later summaries, failed access, or search-term absence.

| Source | Access/read status | Material question still requiring its body |
|---|---|---|
| Cross, 2010 thesis/talk | Excluded from this broad audit; root reports a full open-access thesis recovered and being read independently | Does it already prove the exact complex quadratic obstruction, or a theorem that directly includes it? Reconcile the separate audit before any novelty decision. |
| [Orban de Xivry–Nesterov–Van Dooren, *Nearest Stable System Using Successive Convex Approximations* (2013)](https://research.dial.uclouvain.be/entities/publication/b08eabfd-86fc-4be9-bcbb-56231630e414), Automatica 49, 1195–1203, DOI 10.1016/j.automatica.2013.01.053 | Primary repository record/abstract read; file is restricted; publisher full body not recovered | Determine coefficient field/metric and whether theoretical examples or global-nearest assertions contain the target local nonuniqueness. An algorithm abstract cannot settle this. |
| Orban, *Nearest Stable System*, doctoral thesis, July 2013 | [Primary supervisor's thesis list](https://perso.uclouvain.be/paul.vandooren/students.html) read; full body not recovered; CiteSeer mirror failed | Thesis may include broader polynomial geometry, nonuniqueness, or statements omitted from the article. |
| Moses–Liu, *Determining the Closest Stable Polynomial to an Unstable One* (1991), IEEE TSP 39, 901–906, DOI 10.1109/78.80912 | Cited by audited primary algorithm papers; original full body not recovered | Exact real/complex domain, unit-circle/half-plane transfer, uniqueness and boundary cases must be checked in the original. |
| Fam, *On the Geometry of Stable Polynomials of One and Two Variables* (1979); Combettes–Trussell, *Best Stable and Invertible Approximations for ARMA Systems* (1992) | Original bodies not recovered; titles located in primary later reference lists | Could contain coefficient-space examples or a nearest-point theorem stronger than later algorithm summaries. Original bibliographic pages and actual bodies still require verification before promoting exact theorem attribution. |
| Levantovskii, original stability-boundary singularity work (1980); Bottema (1956); Arnold (1971) | Original bodies not read; attributions visible in audited primary papers | Settle original provenance of cusp/tangent geometry and whether a stronger local metric statement already follows explicitly there. Do not cite the originals as independently audited. |
| [Colombo–Marigonda–Wolenski, *The Clarke Generalized Gradient for Functions Whose Epigraph Has Positive Reach* (2013)](https://pubsonline.informs.org/doi/abs/10.1287/moor.1120.0580), MOR 38, 451–468 | Primary abstract/repository records read; body not recovered | Read examples and precise reach assumptions. It would be invalid to infer from its title or search aggregation that the abscissa epigraph has positive reach. The later 2015 primary paper cites it as a general representation result, not a verification for abscissa. |

Public access routes were used; restricted files were not requested from their authors. If an original cannot be recovered publicly, record that access limitation. Only the human may decide whether to seek outside input.

## Search scope and limits

Families searched independently: foundational polynomial variational geometry; later max-root/spectral regularity; nearest-stable matrix/polynomial algorithms and examples; cusp/Whitney-umbrella/positive-reach geometry; recent root-abscissa and projection continuations. Search combinations included `stable monic set`, `polynomial abscissa`, `max root functions`, `prox-regular`, `positive reach`, `nearest stable polynomial`, `complex quadratic`, `nonunique projection`, the principal author names, and year-targeted 2022–2026 queries. Author publication pages and reference chains were used to locate actual primary bodies. Searches recovered substantive bodies through September 2025 and were run at the October 2026 cutoff; no claim of exhaustive 2026 coverage is made.

Results from aggregators and search summaries were discovery leads only. The report does not infer that a theorem is absent from an inaccessible body. It does not infer novelty from failure to locate a match. Body versions, read extents, local private-copy hashes, and access failures are recorded in `SOURCE_PROVENANCE.json`.

## Permissible author-note language

Suggested factual framing, pending root reconciliation:

> We give a direct coefficient-space proof that, for every fixed positive-definite real inner product, complex quadratic stability projection has multiple attained global nearest points arbitrarily close to `z²`. The proof also exhibits failure of set prox-regularity of the whole abscissa epigraph. The mechanism uses classical stability-boundary cusp geometry and the standard normal-support/projection characterization of prox-regular sets. This addresses the complex convention of the historical set question; priority and the separate finite-subgradient function conjecture are not claimed here.

If Cross or another recovered primary body contains the conclusion, revise this to an independently verified exposition or alternative proof and cite that exact theorem. Do not call such a verification a novel resolution.
