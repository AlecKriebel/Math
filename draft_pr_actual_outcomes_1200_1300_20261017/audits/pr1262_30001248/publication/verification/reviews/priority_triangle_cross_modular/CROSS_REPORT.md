# Detached reverse cross-challenge: priority family A checks family B

Reviewer: `/root/pr1262_priority_triangle`. PR1262 / problem30001248. Performed 17 October 2026 UTC. The initial A seal `9d13033d6c5e0a4fb2a7aee0988457c6cdb5427f7b00dbdc385010bf4c7dd789` and B seal `cbf895a625d7773ba2e165933625bba98336acb24981ee45f1c69701e86f50b3` remain immutable. This detached review reads B only after both initial priority passes were sealed. The separate fresh Fourier adversary's outputs were not read before this cross-review seal.

**Decision: PASS, with required integration of the stronger historical credit into the final publication.** No mathematical or priority-framing defect was found in B's sealed report or its complete `OLD_IMPLICATIONS.md`. The twelve declared authored members authenticate exactly. B correctly distinguishes a full implication derived today from earlier estimates from an earlier explicitly printed modular iff theorem, which its bounded search did not locate. This is a cross-review of priority findings and a source-lemma reduction, not a whole-preprint review or a certification of every imported deep proof.

## Main finding: the 2014 Fourier estimates already suffice

I independently read the exact Gilmer–Kopparty source statements on author-PDF pp.5–6, visually inspected p.6, and checked the p.13 restatement. The PDF is401,939 bytes, SHA-256 `fd7578b138e1e29b01dcd2cc12a6e4e19150cf2bf1e71bc7f934568c175c9eaa`; it is the author manuscript internally dated 6 December 2014. Lemma 4 gives uniform polynomial decay with exponent 1+delta0 for positive frequencies up to n^0.55; Lemma 5 gives exponent50 from there through pi sigma. Constants depend on fixed p, not n or a chosen modulus. The text itself combines them into a common integrable envelope. [Primary author manuscript](https://sites.math.rutgers.edu/~sk1233/triangles.pdf).

Let Z=(T−mu)/sigma, psi_n(t)=E exp(itZ), and choose eta=min(delta0,1)>0. On 1<=|t|<=pi sigma, both lemmas imply |psi_n(t)|<=D|t|^(-1−eta), after increasing a fixed D. There is no gap at n^0.55, no missing factor of sigma, and no division by a zero variance in the eventual n>=3 range. The source counts ordinary triangles, with sigma the true standard deviation of order n².

For q>=2, the roots-of-unity filter gives

    q P(T=a mod q)−1 = sum_(j=1)^(q−1) exp(−2pi ija/q) E exp(2pi ijT/q).

For j>q/2, subtracting q from j leaves exp(2pi ijT/q) unchanged because T is integer. Centering multiplies by a phase. Negative frequencies have the same characteristic-function modulus as their positive partners because Z is real. Thus with j*=min(j,q−j), the modulus is |psi_n(2pi sigma j*/q)|. The fractional value of mu causes no lattice or phase error.

If q=o(sigma), then d=2pi sigma/q tends to infinity. Eventually all the nonzero reduced frequencies are at least1 and at most pi sigma. The even-q endpoint is included and occurs only once; counting every positive j* at most twice is a valid upper bound. Therefore

    max_a |q P(T=a mod q)−1|
      <= 2D d^(-1−eta) sum_(j>=1) j^(-1−eta)
      <= 2D(1+1/eta)(q/(2pi sigma))^(1+eta) -> 0.

The p-series comparison is valid for every eta>0. The identity for q=1 is exact. On sequences that take q=1 infinitely often, apply the bound on the other indices. Composites, bounded q, oscillation, and arbitrarily slow q/sigma->0 introduce no additional hypothesis. The root's independently checked CLT/Fourier converse provides necessity; Scott–Tateno already states the standard-deviation obstruction. This validates the whole mathematical content of B's first derivation, including its quantifiers and endpoint handling.

The deep proofs of the imported source lemmas were **not** reconstructed in full here. B also does not claim that reconstruction. Its direct modular proof is an implication written on 17 October 2026; it must not be described as a modular corollary printed in 2014 without a matching primary passage.

**Required final integration F01.** Name Gilmer–Kopparty's actual characteristic-function lemmas as already sufficient for the complete sharp modular range. Do not imply that a new analytic estimate, the 2016 polynomial LLT rate, or the 2020 general theorem was first necessary to obtain this range. The initial A report had not inspected the decisive p.6 envelope, so this detached finding supplements that earlier pass without changing its seal. A's narrower warning remains correct: an unspecified qualitative LLT conclusion alone does not justify the chosen growing-window summation.

## Weber mechanism comparison

The freshly retrieved 2022 preprint matches B's pin `89f4a8210a8a0b7f7c18a806029492cf6901bd6ab44be09de1bd4808a838bbf8`. I read pp.1–6 and visually inspected p.5. Theorem 1.4 is explicitly about sums of independent integer-valued variables. Its proof uses a finite central window, a pointwise local approximation, a tail term, and Gaussian Poisson summation. That is an earlier mechanism precedent for the candidate's transfer argument. It is **not** a theorem applicable to the dependent triangle count merely by renaming its variables. [Versioned preprint](https://arxiv.org/abs/2209.12228v1).

B's caution about the cardinality estimate is justified. On p.4, the number of members of one residue in a closed interval of length2B/sqrt(epsilon) is bounded without the possible extra endpoint term. For example, B=6, epsilon=1, h=100 and integer mean0 give one central member of residue0, while2B/(h sqrt(epsilon))=0.12. This is a counterexample to that intermediate count bound, not a demonstrated counterexample to the source theorem. The candidate's retained `+1` avoids the issue. Other printed constants and algebra in Weber's proof were not imported or globally repaired by B or this cross-review.

Fresh archive and publisher-index metadata support the journal title *A strengthened asymptotic uniform distribution property*, Probability and Mathematical Statistics 43(2)(2023),263–285, published online 15 April 2024, DOI10.37190/0208-4147.00147. The 2022 archive preserves the longer title and its spelling. The differing titles and issue/online dates are not a reason to invent a revised proof or treat 2024 as the preprint date. B honestly states its own published-body access failure and uses the preprint for mechanism comparison. This cross-pass used the publisher's indexed metadata, without certifying equality of final and preprint theorem/proof bodies. [Publisher record](https://www.math.uni.wroc.pl/~pms/publicationsArticle.php?doi=10.37190%2F0208-4147.00147).

**Required final integration F02.** If the paper discusses the finite-window/Poisson route, credit its classical nature and the Weber precedent. Keep the dependence restriction and avoid importing the source constants. The direct GK route itself requires neither Weber's theorem nor any independent-sum identification.

## Modular scope, source history and current versions

Fresh Kolaitis–Kopparty PDF p.10 explicitly says its graph-copy equidistribution theorem holds for arbitrary integers q, not necessarily prime. The copy count is a set of subgraph edges, whereas the labeled frequency equals the automorphism factor times that count. The exponential constant is indexed by q,p,d. The prime restriction in its logic convergence theorem on PDF p.7 is a different statement. B's distinction is correct. [Primary preprint](https://arxiv.org/abs/0904.2436).

Fresh DeMarco–Kahn–Redlich PDF pp.1–3 likewise fixes q, uses unlabeled copies, and expressly allows the exponential constant to depend on q and the graph family. Its sparse extension cannot by itself be quoted as a bound uniform in q growing near n². B has not made that substitution. [Version2](https://arxiv.org/abs/1402.2264v2).

My independent initial pass had already visually checked the Loebl primary Theorem 1.2: the prime range is logarithmic for p=1/2. Both A and B correctly prefer that actual source over Gilmer–Kopparty's smaller logarithmic-power historical summary. The Scott–Tateno2009 statement, all-integer o(n²/log n) range, and preexisting necessary scale also agree across the independently sealed passes. No first sharpness idea is available for the new note.

The current Sah and Sawhney author-list HTML was freshly retrieved here and matches B's byte pins. Sah lists the joint paper as a preprint, while Sawhney lists *Annals of Probability*, to appear. The IMS future-papers indexed result independently lists its title and authors. These labels do not establish a new theorem version, final journal coordinates, or equality to a future published body. B's archive/author-mirror match to 2024 v1 is a proper version pin, and its anti-bot warning does not treat a challenge page as an article. Cite the inspected v1 if this optional context is retained.

B's uncertainty about precise Araújo–Mattos journal metadata was an honest limitation of that run. Initial A separately obtained the 2025 online/2026 issue metadata from a primary publisher record and depositor metadata, while explicitly keeping its 2023 v1 body distinct from B's 2025 v3 body. Neither audit imports a new sparse-density theorem into the fixed-p claim. The final short note can omit this peripheral reference or use a verified versioned citation without making a current-openness inference.

## Evidence counts and provenance checks

All 12 B authored files were read and authenticated under the supplied manifest SHA. I additionally matched all 20 successful retained-byte records from its 24 retrieval attempts to files actually present in B's ignored scratch. The eleven distinct article/report bodies counted by B are consistent after excluding author mirrors, metadata, HTML author lists and the anti-bot page. A failed request is not counted as a source body. Exact checks are recorded in `B_EVIDENCE_RECHECK.json`.

The public query ledger has 52 entries with IDs 1 through 52 and 52 distinct literal strings. They equal the query array in B's retained raw web log, which holds 15 response strings. Thirteen batches of four queries is arithmetically consistent with that ledger. The raw log does not preserve each structured request, so this cross-review checks the internal record rather than claiming an independent service-history reconstruction or request-to-result ranking audit. Neither the 52 count nor unrelated negative search previews establish exhaustive priority clearance.

The twelve B authored members and both original A/B seals were checked again at this cross-review's seal. Original missing research packages remain historical. No source-author program, outreach, repository branch/index operation, service mutation, or other fresh-family read was performed.

## Minimal final-paper credit and disposition

The main paper should cite Scott–Tateno for the historical question, smaller positive range, already stated triangle LLT and scale obstruction; Gilmer–Kopparty for the prior triangle result **and its directly sufficient Fourier bounds**; Berkowitz for the earlier quantitative triangle input; and Sah–Sawhney for the operative clean quantitative theorem. Add Weber as a transfer-mechanism precedent if that route is discussed. Cite Loebl if its earlier logarithmic prime range is described. KK/DKR, sparse and joint results are optional context, with their hypotheses kept separate. The known 2K2 supplement, if retained, belongs explicitly to Sah–Sawhney Theorem 1.3 and overlaps the adjacent general-subgraph target.

The note may decisively prove the historical fixed-p modular equivalence as an attributed consequence. It should describe its contribution as a complete explicit reduction and verification, not a first resolution of a presently open LLT problem. Extensive AI use, unrefereed status, and lack of external human review/formal certification should be present throughout the publication metadata. No blocking defect was found in B; the two framing integrations above should be propagated globally before the whole-package review rounds.
