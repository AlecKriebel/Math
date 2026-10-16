# PR880 / 9700026: structural priority audit

Family: weighted-cell dynamics, spatial competition, reinforcement, and classical permanence. Frozen target head: `fba74a301786f9648e48722e76f440097b0746c2`. Audit conducted 15 October 2026 UTC. This report concerns priority and transfer, not a replacement proof audit.

## Decision

**Bounded review complete, with material required credits and a current overlapping result.** No prior source located in this structural search states or implies, with all hypotheses already discharged, the full all-finite-site, all-positive-initial-state quantitative persistence theorem for `p=2alpha/beta<1`. This is a bounded search outcome, not a novelty, firstness, worldwide-absence, or current-openness certificate.

The protected-neighborhood mechanism and its area exponent already appear in Aldous's own 2007 notes. Classical weighted Voronoi geometry and the subsequent scalar differential inequality are standard. A current Ferudun preprint explicitly discusses Conjecture 32, gives related counterexamples, and contains proved lemmas implying a qualitative two-city counterexample even in the present parameter range. It must be discussed rather than dismissed because its main title concerns the stochastic model. The parent's authenticated 6 October PR chronology predates its claimed 14 October release; this family does not independently certify historical firstness.

The unchanged author proof claims no literature novelty. Its mathematical correction can be evaluated independently of whether the application, quantitative strengthening, or exposition is historically new. A public update must not advertise a new capture mechanism or an absence of related resolutions.

## Scope, independence, and search boundary

`INDEPENDENT_SCOPE.md` was written before reading `source/author/SOURCE_AUDIT.md`, the author's proof, or inherited priority verdicts. The independent scope fixed the mechanism and three search families first. The exact source-scope report supplied the model boundary, not a novelty verdict. Only afterward were the author's two files read. Their negative-search wording is appropriately cautious and has not been used as evidence of absence.

The precise target is `z_i'=A_i(z)-z_i` on the positive probability simplex, with fixed distinct interior sites in the unit square and hard cells maximizing `z_i^alpha |y-x_i|^-beta`. Write `q=alpha/beta` and `p=2q`. The cells are exactly multiplicatively weighted Voronoi cells for distances `|y-x_i|/w_i`, with `w_i=z_i^q`; taking a positive common power causes no time change. The target conclusion for `p<1` is a positive lower bound along every positive-initial solution, and a positive asymptotic bound independent of its initial state. A local stable equilibrium or an open basin disproves generic collapse but is weaker than that theorem.

Forty-five recorded search queries covered equivalent weighted-distance notation, cell area/population ODEs, territory/coverage models, retail gravity dynamics, spatial reinforcement/urn terminology, and permanence. Plausible hits were checked in primary bodies. Search-engine snippets were used only to select sources. `QUERY_LEDGER.json`, `SOURCE_LEDGER.json`, and `TRANSFER_LEDGER.json` record coverage, exact reading, and mapping status. The direct-author family supplied the Ferudun lead after this scope and initial search were fixed. No other family's verdict was substituted for source reading.

## Required geometric and source credit

[Aurenhammer and Edelsbrunner (1984)](https://doi.org/10.1016/0031-3203(84)90064-5), printed pp.251–252, define precisely the weighted distance used here, give pairwise Apollonius disks, explain the importance of weight ratios, and discuss local attraction near a small shop. The author's copy was read in rendered form and OCR. Setting their weight to `z_i^q` is an exact geometry mapping. These static facts do not supply the population ODE or persistence theorem; they do rule out presenting weighted cells, circular ties, or the local dominance idea as new geometry.

[Aldous's 2007 notes](https://www.stat.berkeley.edu/~aldous/Research/OP/cities-notes.pdf), §6.1, printed p.36, already take a city-centered captured disk with radius proportional to `N^(alpha/beta)` and an area/growth lower bound proportional to `N^(2alpha/beta)`. The full surrounding pp.35–37 were read, and p.36 rendered and inspected. This is within the unfinished Proposition 30 argument, with explicit gaps and a different stochastic target. Its coefficient and probabilistic conclusion were not adopted as proved. Separately, Lemma 3 on p.9 supplies an upper area estimate with the same exponent. Mandatory credit is for the local capture/scaling mechanism, not an assertion that the notes already prove normalized finite-site persistence.

The useful distinction is the rigorously uniform bound against every competing weight in the simplex, for every separated fixed configuration. Once `A_i>=K_i z_i^p` is available, setting `u_i=z_i^(1-p)` gives `u_i'>=(1-p)(K_i-u_i)`. Integrating this scalar inequality is the usual Bernoulli substitution and integrating-factor argument. Neither operation supports a claim of a new ODE technique.

## Classical permanence: exact map and exact gap

The [Hofbauer–Sigmund chapter (1987), pp.70–73](https://homepage.univie.ac.at/josef.hofbauer/87iiasa_HS.pdf) treats replicator permanence; its Theorem 1, credited there to Hofbauer (1981), requires a continuous boundary Lyapunov rate. The neighboring Hutson–Pym chapter, pp.39–43, Theorem 1, allows upper-semicontinuous solution funnels but still requires a forward-invariant excluded set and a repulsion ratio condition. Both theorem bodies and hypotheses were read; the former theorem page was also rendered.

The target has the exact interior replicator representation

`f_i(z)=A_i(z)/z_i`, `sum_i z_i f_i(z)=1`, `z_i'=z_i(f_i-1)`.

This is not a reason to reject the connection by terminology. It also does not discharge the boundary hypotheses. For the conventional `P=product_i z_i`,

`P'/P=sum_i A_i(z)/z_i-n`.

The verified target area bound makes this expression tend to positive infinity when a coordinate vanishes and `p<1`; it has no finite continuous boundary extension. More fundamentally, the target lower estimate at any fixed `t>0` remains positive as `z_i(0)` decreases to zero. Consequently a selection of interior solutions cannot extend continuously to an invariant zero-coordinate face. A funnel including limits of such solutions cannot preserve that face; restricting it to sticky boundary solutions loses the needed upper semicontinuity. Thus these cited theorems do not give a direct ready-made instantiation on the natural closed simplex. A different compactification or theorem is not excluded, but must be specified and checked. The direct scalar barrier already proves what is needed without importing an unverified boundary-flow assertion.

The inaccessible Butler–Freedman–Waltman 1986 article was retained as an access gap, not treated as a checked theorem or a negative result. No general permanence citation was found that removes the model-specific capture estimate.

## Dynamic near-hits: explicit non-transfers

The [Osawa–Akamatsu–Takayama revised preprint (26 April 2016)](https://mpra.ub.uni-muenchen.de/70969/8/MPRA_paper_70969.pdf), §§3.1–3.4, pp.6–9, is a particularly close algebraic hit. Its Harris–Wilson adjustment is `h_i'=S_i(h)-kappa_i h_i`; taking all costs one and total demand one preserves the normalized simplex. But its demand is a finite-origin **soft** gravity sum, `S_i=sum_j O_j h_i^a exp(-b t_ji)/sum_l h_l^a exp(-b t_jl)`. It is not the hard area functional. Sending the exponent scale to infinity could produce argmax allocation after replacing origins by a continuum and using logarithmic distances; transferring long-time persistence through both singular limits is an additional unsupported theorem. The read source studies local bifurcations and does not supply that transfer. Different vocabulary alone was not used as a dismissal.

[Pierson et al. (2017)](https://sites.bu.edu/pierson/files/2021/05/pierson2017ijrr.pdf), model and theorem/proof pp.339–345, use squared-distance **power** cells, moving site positions, and a weight update driven by neighboring health differences. Their Theorems 1–2 concern convergence toward weighted centroids. No substitution `w_i=g(z_i)` changes those additive squared distances into the required multiplicative distance ratios for arbitrary states, or turns their update into `A_i-z_i`. Hence the theorem's stronger-sounding convergence conclusion is for another vector field.

[Abellanas et al. (2016)](https://doi.org/10.5424/fs/2016252-08021), pp.4–7, are a closer biological mechanism: fixed tree locations, genuinely multiplicatively weighted regions, size-dependent weight feedback, and resource area affecting growth. Actual equations [1]–[6] were read. The weight depends on diameter and local/global diameter averages; occupied area is clipped by a potential-crown radius; growth is a discrete Chapman–Richards increment modified by occupied/potential area; a mortality threshold deletes trees. Normalizing these increments does not yield `A_i-z_i`. Eliminating these factors would define a different specialization for which this paper provides no persistence theorem. This source confirms a well-established modeling family, not an exact target theorem.

## Current direct overlap: do not dismiss an omitted quantitative strip argument

[Ferudun (2026), version 1, 14 October](https://eulersolve.org/papers/amr-096-0023/paper.pdf?v=319a8f49e0c4), §4 pp.6–9 and §8 p.13, explicitly treats Conjecture 32. Its `k` is our `p`. With `n=2`, `z_2=1-z`, its share map is exactly `f_x(z)=A_1(z,1-z)`; thus `z'=f_x(z)-z` is the target without time change. It proves open-data trapping for `1<=p<sqrt(3)`, states the same exponent-ratio inconsistency, and labels its `p<1` quantitative strip extension a sketch.

There is nevertheless a stronger qualitative transfer from its proved Lemma 4.1(iii): for **every** `p>0`, `f'(.5)=p(a+1/(12a))`. For `p<1`, take `a=1/4`, giving slope `7p/12<1`. Differentiability supplies strict inward signs at `.5±delta`; Lemma 4.3/continuity preserves them under small site perturbations. The scalar interval is invariant. Thus the written lemmas already imply an open-basin two-city refutation in the present range. They do not imply all-site/all-initial uniform persistence. Only this deterministic implication was checked here; the paper's full stochastic claims were not audited.

The root reports an authenticated public PR dated 6 October, earlier than the preprint's claimed date. Record both dates and the overlap. An unrefereed current preprint is neither ignorable nor evidence sufficient to certify firstness for either author.

## Claim boundary and disposition

The strongest independently verified mathematical result remains the separately audited all-finite-site quantitative persistence theorem under the stated assumptions. This priority family identifies classical ingredients and current overlapping qualitative conclusions; it does not replace the independent analytic verification or upgrade the original `claimed_solved, 2/5` queue state.

Safe present claims are: a rigorous correction of the literal 2007 ODE collapse clause; a specified quantitative finite-site persistence theorem; explicit attribution of Aldous's geometric mechanism, standard ODE comparison, and related literature. Unsafe claims are: first solution, a new geometric or permanence method, no identified related correction as of today, a complete city-growth solution, or globally open status for parameter regimes outside this theorem. Removing an unrestricted `alpha>1` disjunct does not by itself settle the corrected alternatives, and the current preprint addresses some additional regimes.

The bounded audit is complete (100%). Historical priority and absence of a full earlier theorem remain uncertified. No contact, outreach, Git operation, PR mutation, release, Zenodo operation, sheet edit, candidate edit, or central new proof search was performed. The PDF authoring marker was not run.

## Public allowlist and private evidence

Only `REPORT.md`, `INDEPENDENT_SCOPE.md`, `RESEARCH_LOG.md`, `DECISION.json`, `QUERY_LEDGER.json`, `SOURCE_LEDGER.json`, `TRANSFER_LEDGER.json`, `PUBLIC_MANIFEST.json`, and the authored `.gitignore` exclusion are candidates for publication, subject to the parent's artifact review. They contain authored prose and authored bibliographic/audit metadata only. The explicit manifest controls membership; it is not a glob. Everything under `private/`, all downloaded primary PDFs, OCR/text extracts, rendered pages, third-party corpora, raw records, and the shared private source paths are excluded. No third-party content or corpus is authorized for publication by this report.
