# Independent historical and explicit-match audit: PR1261 / problem30003990

Sealed-audit cutoff: 2026-10-17 UTC. This family worked independently of the other new priority family. It used the original submitted AUDIT.md and SOURCE_VERIFICATION.json as bounded prior context. It did not inspect the other new family's files.

The inspected primary bodies did not yield an earlier explicitly printed theorem matching the complete target. This is a bounded search outcome, **not** novelty clearance, a firstness claim, or a statement that the problem remains open worldwide.

A stronger positive finding is available: the full target follows by a deduction assembled during this audit from Totik–Varga's2012 endpoint polynomial theorem, the already published quadratic-proxy reduction, Markov's inequality, and an elementary convex-body homothety estimate. Every external theorem hypothesis and each measure, degree, normalization, and quantifier interface is checked in DERIVATION.md. This assembled implication has not yet received the parent's planned independent adversarial cross-challenge. It does not show that any earlier author printed, discovered, or disclosed the target theorem.

## Exact question and original source

For fixed compact convex full-dimensional K⊂R^d and fixed real polynomial f, define
H_r=inf{∫K f q dx : q globally SOS, deg q≤2r, ∫Kq dx=1}.
The target is 0≤H_r−minKf≤C(K,f)/r² for every integer r≥1. One global square is enough; constants need not be uniform in dimension or bodies. A minimizer-dependent existence proof is allowed. No arbitrary reference measure or restriction q=s(f) is assumed.

The original [Laurent contribution, joint with de Klerk, OWR50/2018](https://ems.press/journals/owr/articles/16633), printed2991–2993, was read completely (S01). Its probability formulation defines the intended hierarchy; displays3/4 visibly omit a unit-mass equality. The allconvex Lebesgue rate question is the natural normalized interpretation, confirmed by the full papers' explicit unit-mass definitions. An unnormalized literal infimum would be a different, usually degenerate problem.

The statement is an upper/worst-case rate claim. A constant objective has zero error, so there is no assertion that each objective has Theta(r^-2). The classical worst-case example is supported by [de Klerk–Laurent, Th3.1/Cor3.2](https://doi.org/10.1287/moor.2018.0983), PDF8, using Jacobi α=β=0, K=[−1,1], f=x. Its endpoint-zero asymptotics give the matching Theta(r^-2) example for Lebesgue measure.

## Four separate priority categories

**Earlier explicit printed resolution.** None was located in the body passages specified in SOURCE_RECORDS.json. This is a statement about this inspected corpus only. The closest same-scope primary theorem remains [Slot–Laurent, arXiv1905.08142v2, Th11](https://arxiv.org/abs/1905.08142v2), with O(log²r/r²); its p29 explicitly asks about removing the logarithm for all convex bodies. The proof pp22–24 was inspected: its absolute small-core lower bound and total-volume tail control create a logarithmic balance. That is materially different from canceling relative shell mass against the same local core mass.

**Now-assembled deduction from older ingredients.** [Totik–Varga2012, Th2.1](https://doi.org/10.1016/j.jmaa.2012.03.006), PDF2/printed379, permits ψ(v)=sqrt(v), a=0. Its hypotheses, including the integral condition, are all verified. It supplies degree-m polynomials equal to1 at0, bounded by2 on[0,1], with decay Aexp[−c(m²t)^(1/4)]. Markov yields a positive core of scale m^-2. If a pushed-forward measure has cumulative growth F(t)≤(t/h)^dF(h), dyadic shell contributions divided by the same core mass have a summable stretched-exponential factor. The normalized first moment is therefore O(m^-2).

For arbitrary f, use the prior Taylor upper proxy g(x)=∇f(z)·(x−z)+γ||x−z||² at a minimizer z. This proxy already appears in [de Klerk–Laurent's2017 preprint, Cor4.3](https://arxiv.org/abs/1703.00744v1) and S02. Its sublevel sets satisfy the required cumulative growth by contraction toward z. Composing P_m with u=g/maxKg gives one global square. Choosing m=floor(r/2) verifies degree≤2r, and constant density handles r=1. No zero-spacing theorem or unverified general-doubling hypothesis is used. DERIVATION.md contains the complete checkable proof.

**Mechanism overlap.** Endpoint localization on the degree^-2 scale, squared-polynomial localization, Taylor/quadratic proxy reduction, and relative shell/core mass arguments all have substantial prior literature. Totik–Varga pp7–9 already compare shells to local mass in a Christoffel-function proof. It would be unsupported to assign broad originality to those devices. The audit's mathematical assembly concerns their application to the exact normalized allconvex hierarchy. Even this application is not certified historically new by the search.

**Bounded absence.** Exact identifier searches, author pages, current preprint records, broad equivalent-wording searches, and selected citation threads found no explicit full-target match. The source-access and search limits below remain material. No inference about historical lineage, disclosure, independent discovery, or worldwide current openness is promoted.

## Current and adjacent literature checks

The [final2026 Laurent–Slot overview](https://ir.cwi.nl/pub/36052/36052.pdf), DOI10.1007/978-981-95-1446-5_8, still gives the log²/r² bound in Table1 (S04, PDF11, visually checked). More current primary evidence was found independently: [Gribling–Klep–Kumar, arXiv2610.22030v1](https://arxiv.org/abs/2610.22030v1), submitted15 Oct2026. Its p2 also reports the convex-body Lebesgue log²/r² baseline. Its own theorem concerns Gaussian measure on R^d, with O1/r under attainment, and does not settle the compact target. These two statements are evidence about their authors' printed accounts, not an exhaustive openness certificate.

The recent [Gribling–de Klerk–Vera hypercube kernel preprint](https://arxiv.org/abs/2605.31496v1), Proposition14, does provide a global-SOS upper O1/r² statement at order rn, but for a hypercube with product Chebyshev measure. Slot's Christoffel–Darboux work gives ball/simplex statements with preordering and special-measure interfaces. De Klerk–Hess–Laurent uses a box, Chebyshev reference measure, and a wider weighted-SOS density class. Magron's2026 set-products results concern positivity/lower hierarchies on bispheres. Recent de Finetti and polarization papers use different outer approximations. Their titles or rates alone are not positive matches.

The [Slot–Laurent objective-pushforward paper](https://arxiv.org/abs/2001.11289) was read at the hierarchy definitions, degree scaling, theorem/proof, and conclusion. A density constrained to s(f) is a different approximation space. The present assembled witness uses s(g) for a quadratic proxy; it does not establish the stronger original-objective restriction at the same rate.

The older convergence, annealing, measured-cone, and distributionally robust density sources were checked at their actual theorem interfaces. CLAIM_MATRIX.md records exact K, measure, SOS category, order, conclusion, and missing interface for each retained source. Generic kernel implications were not promoted without a correct admissible kernel.

## Search and reading coverage

QUERY_LEDGER.json retains all26 web invocations:19 search invocations with76 literal search expressions,6 open invocations with22 open requests, and1 find invocation with4 find requests. These are actual invocation/request counts, not distinct-source counts. W001's exact UTC timestamp and raw response were not retained; its literal queries and the limitation are recorded.

There were35 additional program-level HTTP GET attempts:21 source retrieval attempts and14 metadata/archive/author-page attempts. Twenty retrieved source files were valid PDFs; one apparent PDF was HTML. Twelve of the14 extra GETs succeeded and two failed. Redirect-level network requests are not counted as separate invocations. HTTP_LEDGER.json records this accounting. Repeated arXiv/publisher/author-page visits do not inflate the source total.

SOURCE_RECORDS.json contains21 source records:20 PDFs with specified passages read and one missing body. No complete reading of all20 papers is claimed. Selected arXiv metadata screens covered56+15+16+10 title occurrences across four queries (with duplicates); the broad4037-result 'measure-based' search returned only its first100 and was machine-filtered. ARXIV_SCREEN.json preserves the distinction. Zenodo results were metadata screens, not audits of all attached papers.

Searches included exact problem identifiers and question wording, full-convex/global-SOS/rate variants, author/research pages, recent arXiv listings, Zenodo, EulerSolve's public index, and French/German/Russian/Chinese phrase variants. Literal expressions, UTC times where captured, source titles, actions, and scopes are retained. Repeated search hits were followed into selected primary bodies rather than counted as confirmations.

## Material limits and remaining checks

Kroo2015, DOI10.1007/s10474-015-0507-8, is an important needle-polynomial predecessor cited by S02. The publisher PDF endpoint returned HTML, and a repository restricted access. Only metadata/abstract were inspected. An exact or equivalent theorem in that unread body has not been excluded. No outreach was prepared or initiated.

EulerSolve's public index was searched for exact identifiers and Lasserre; its roughly300 listed preprints were not all read, and the bonus problem endpoint was not obtained. Zenodo metadata searches are incomplete discovery tools. Author publication pages can lag: the inspected Gribling page did not display all separately found2026 preprints. Cross-language phrase searches are limited and no global citation graph was exhausted. Metadata-only kernel/perturbative leads and unread proof sections remain outside the positive-match comparison.

Independent cross-challenge should inspect DERIVATION.md's endpoint theorem specialization, relative normalization, quadratic proxy, homothety inequality, and all-integer degree handling. Its result is a verified assembly within this family, pending that later challenge. Broader historical searching could obtain the missing Kroo body and follow additional approximation-theory citations. No theorem date alone determines discovery or communication priority.

This report is a priority/literature audit. It does not approve a final paper, public package, submission, or publication claim.

