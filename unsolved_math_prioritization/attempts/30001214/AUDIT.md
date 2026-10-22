# Mathematical audit: local closedness of symplectic cores

## Review status of this edition

This is an AI-assisted mathematical exposition accompanied by an independent internal AI mathematical and source audit. These authored documents are unrefereed. Acceptance means the source-credited, theorem-dependent conclusion of that audit, not external human peer review, journal acceptance of this exposition or audit, or formal proof-assistant certification. Bell, Launois, León Sánchez, and Moosa's differential-algebraic existence theorem is imported prior mathematics; no new counterexample or novelty is claimed.

## Decision

Accept a source-credited prior negative resolution of problem 30001214 / OWR-3397-002, with a prominent qualification on one clause of the inspected LWW manuscript. For each Krull dimension d≥4, BLLSM's Poisson domain has a non-locally-closed symplectic core in its maximal spectrum. The accepted argument is detailed in [PROOF_OF_IMPLICATION.md](PROOF_OF_IMPLICATION.md).

This is an implication audit of known results. It does not claim a new counterexample, a new solution date, or an independent reproof of the deep differential-algebraic construction.

## Critical source qualification

The inspected mathematical body of LWW is arXiv:1908.06542v2, not the journal PDF. Its p.22 definition of a prime core and p.23 Theorem 6.7(ii) really quantify over all ordinary prime ideals. The zero bracket on C[x] satisfies PDME and has closed singleton maximal cores, but its generic prime core is the non-locally-closed singleton {0} in Spec C[x]. Thus that all-prime clause is too broad in the inspected version. This conclusion follows from the source's actual definitions, not from a change of terminology.

The needed equivalence between PDME and local closedness of maximal-spectrum cores remains sound: Proposition 5.3 restricts its statements to primitive ideals, and Lemma 6.5 supplies the closure formula. The accepted proof reconstructs that route algebraically and does not use Theorem 6.7(ii). No claim is made that the published journal text has the same issue or that an official correction has been issued. Publisher metadata confirms the article's 2021 publication, volume and pages; it does not expose the full journal body.

## Obligations checked

1. **Question and topology.** Brown's original 2009 report, printed pp.783–784, asks about fibers of the Poisson-core map on the maximal ideal spectrum over C. It does not add a finite-leaf, algebraic-leaf, smoothness, or torus-action assumption. Later discussion of algebraic leaves is a sufficient special case.
2. **Counterexample input.** BLLSM Corollary 5.3, publisher PDF p.16 / printed p.2034, gives integral complex affine Poisson examples in every dimension at least four with rational, non-locally-closed zero prime. Theorem 4.1 supplies the differential domain; Proposition 5.2 converts it to R[t].
3. **Exact bracket.** The coefficientwise derivation δ and d/dt commute. The bracket δ(u)∂(v)−∂(u)δ(v) is a Poisson bracket. Its fraction-field center is the δ-constant field C. Extended nonzero differential primes remain Poisson prime and retain zero intersection coefficientwise.
4. **Primitivity.** Rational⇒primitive is not assumed from ordinary noncommutative Dixmier–Moeglin folklore. BLLSM Theorem 3.2 applies over C. Its finite-dimensional lemma, countability argument, and localization step are reconstructed. The resulting maximal ideal m satisfies P(m)=0.
5. **Implication directions.** Locally closed⇒primitive and primitive⇒rational are checked independently. Over complex affine algebras, rational⇔primitive holds; rational⇒locally-closed is precisely what fails in the counterexample.
6. **Density of the maximal core.** Every nonempty principal open in Max(A/P) contains a core-zero maximal ideal: localize, retain rationality, and apply rational⇒primitive. Hence closure(C_P)=V_max(P). This avoids imposing algebraicity of an analytic leaf.
7. **The topological bridge.** For primitive P, C_P is locally closed iff the intersection J_P of strictly larger Poisson primes strictly contains P. The forward direction uses the closed complement and Nullstellensatz; the reverse direction proves C_P=V_max(P) minus V_max(J_P). This is an explicit bridge between a fiber in Max A and a point in PSpec A, not an identification of the two.
8. **LWW hypotheses.** A is noetherian, dim_C A≤aleph_0<|C|, and finitely many Hamiltonian derivations suffice. The Proposition 5.3 closure hypothesis is supplied by Lemma 6.5 and verified algebraically. No hypothesis about finiteness or algebraicity of leaves is borrowed from adjacent corollaries.
9. **Integral convention.** BLLSM uses “affine” to mean finitely generated integral. Its negative examples already belong to the broader class in Brown's question. For implications at a Poisson prime in a nonintegral algebra, the quotient A/P is integral. There is no narrowing of the target sufficient to evade a counterexample.
10. **Dimension.** Theorem 4.1 gives dim R=d−1≥3; polynomial extension gives dim A=d. Theorem 7.3's dimension≤3 positive result is contextual and not needed for the negative implication.
11. **Adjacent problem.** The unrestricted PDME question represented by 30001215 / OWR-3397-003 and the maximal-core question are reconciled through the proved equivalence. A negative universal answer does not provide a classification of all positive subclasses or reopen a separate research project.

## Dependency and reproof boundaries

Imported essential input: BLLSM Theorem 4.1's existence of the differential domains. Its §4 construction and declared dependence on Manin kernels, nonisotrivial simple abelian varieties, and differential-algebraic/model-theoretic results were inspected. Those background results are not independently reproved here, and no explicit presentation or computational construction of the domain is asserted.

Checked and reconstructed: the finite-dimensional lemma behind BLLSM Theorem 3.2; rational⇒primitive; primitive⇒rational; locally-closed⇒primitive; the polynomial Poisson conversion and intersection calculation; density of a primitive core; and the local-closedness equivalence for that core. Standard imported algebraic facts include characteristic-zero primeness of Poisson cores, Poisson stability of minimal primes over Poisson ideals, affine noetherianity and finite Krull dimension, Hilbert Nullstellensatz/Jacobsonness, and extension of derivations to localizations.

Historical cross-check: Brown–Gordon §§3.2–3.6 provides the original definitions and core/leaf closure arguments. LWW Proposition 5.3 and Lemma 6.5 give the matching route. The alternate algebraic proof makes the accepted implication independent of the overbroad prime-core clause and of any unstated regularity of analytic leaves.

## Adverse mathematical checks

- **Wrong ambient spectrum:** C[x] with zero bracket separates the valid maximal-core statement from the invalid all-prime-core clause.
- **Rationality omitted:** A non-locally-closed prime alone does not suffice. In that same example zero is not primitive and has no corresponding nonempty maximal core. The accepted counterexample explicitly invokes rational⇒primitive.
- **Polynomial center substituted for fraction-field center:** This is invalid. For C[x,y,z] with {x,z}=x, {y,z}=y, {x,y}=0, the polynomial Poisson center is C, but x/y is a nonconstant central rational function. The accepted construction computes the fraction-field center.
- **Closure assumed without proof:** Local closedness only means open in one's own closure. The necessary equality with V_max(P) is separately proved before taking complements.
- **All primes substituted for primitive primes:** The restriction in Proposition 5.3 is retained throughout.
- **Zero derivation:** It would not have constant field C in the positive dimensions used, and would destroy the center calculation. The imported construction has nonzero derivation.
- **Dimension three claimed as a counterexample:** The construction produces dimension at least four; Theorem 7.3 is a contrary check in lower dimensions.
- **Algebraic or finite leaves silently required:** Neither occurs among the accepted assumptions. Those assumptions would instead lead to positive special cases.

## Source authentication and integrity

All four full PDFs were independently fetched from public primary-source URLs on 10 October 2026 and exactly matched the authenticated supplied bytes. Their identities, version labels, retrieval history, and inspection pages are recorded in [SOURCES.json](SOURCES.json). Decisive theorem pages were visually inspected, including the overbars in the closure formulas that text extraction can omit. Whole-PDF retrieval is not represented as proof-by-proof inspection of each paper.

The public payload consists only of authored proof/audit/acceptance text and public bibliographic/verification metadata. It contains no source PDFs, extracted source bodies, dataset contents, private coordination material, or raw source-search output. The exact files in this publication edition are listed in MANIFEST.json.

The integrity verifier is fail-closed and uses byte counts, SHA-256, an exact file inventory, and an external manifest/verifier pin. A disposable fixture passed the clean case and rejected 13 adverse mutations under normal Python, -O, and -OO: 42 checks in total. These include altered/missing/extra files, same-size tampering, symlinks, altered or missing manifests, verifier replacement, unsafe or duplicate manifest paths, invalid sizes, and an invalid seal. The controls validate artifact integrity, not mathematical truth.
