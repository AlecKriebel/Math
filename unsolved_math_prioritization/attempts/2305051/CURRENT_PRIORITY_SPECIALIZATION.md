# Credited prior resolution of Holland Problem 5.51

This is a source audit and checked specialization of prior work, not a new paper or a claim of earliest recognition.

## Exact target and historical evidence

Holland's question asks for an explicit construction of a Blaschke product B on the unit disc, B(0)=0, for which F=(1+B)/(1-B) is a Bloch function. Existence is already assumed in the question. The required product is pure Blaschke, not merely an inner function with an uncontrolled singular factor. The Bloch condition is a global derivative bound, not a numerical sample.

Hayman-Lingham, Research Problems in Function Theory, Fiftieth Anniversary Edition (Springer2019), printed121-122 / supplied PDF127-128, prints the original question and credits Aleksandrov-Anderson-Nicolau [21] with an explicitly constructed inner function satisfying a stronger vanishing hyperbolic-derivative estimate. This supersedes the genuine no-progress wording in the retained arXiv1809.07200v2,21September2018, printed105 / PDF106. The2018 statement was accurately quoted as a dated report; using it after reading2019 to assert continuing open status would be materially incomplete. The adjacent2019 no-progress update is5.52, not5.51.

The2019 update alone speaks of an inner I, so pure Blaschke and B(0)=0 are checked from its cited primary source rather than silently inferred from the book.

## Exact target from AAN1999

Aleksandrov, Anderson and Nicolau, Inner functions, Bloch spaces and symmetric measures, Proc. London Math. Soc.(3)79(1999),318-352, Theorem2 printed320 and proof326-327, states: for every positive continuous phi on(0,1] with phi(0+)=0, an interpolating Blaschke product A exists with

    (1-|z|^2)|A'(z)| <= phi(1-|A(z)|^2),  z in D.

Its construction takes a holomorphic universal covering A:D -> D\Lambda, with Lambda countable, cluster points confined to the unit circle and 0 excluded from Lambda. The proof establishes innerness and excludes the singular factor; this is a pure Blaschke product. Because0 belongs to the covered domain, a preimage p with A(p)=0 exists.

Choose phi(t)=t^2. Let psi(z)=(p+z)/(1+conj(p)z), so psi(0)=p, and set B=A composed with psi. The automorphism identity

    (1-|z|^2)|psi'(z)|=1-|psi(z)|^2

preserves the estimate, giving B(0)=0 and

    (1-|z|^2)|B'(z)| <= (1-|B(z)|^2)^2.

B remains a covering of the same domain, so the source's purity argument applies to it. Independently, purity under precomposition follows from the Blaschke Green identity: for each zero a, the factor modulus at psi(z) equals that of the factor with zero psi^{-1}(a) at z; transformed zeros satisfy the Blaschke sum since (1-|psi^{-1}(a)|^2)/(1-|a|^2) is bounded above and below for fixed p. No singular harmonic defect is introduced. This is precomposition, not an arbitrary target-value Frostman shift.

For F=(1+B)/(1-B), the exact derivative identity and elementary modulus inequality yield

    (1-|z|^2)|F'(z)|
      =2(1-|z|^2)|B'(z)|/|1-B(z)|^2
      <=2(1-|B(z)|^2)^2/|1-B(z)|^2
      <=2(1+|B(z)|)^2 <=8.

The denominator is nonzero inside the disc because B is a nonconstant disc map. Also F(0)=1. Thus the exact stated target is fulfilled by the earlier theorem and its covering construction. The source itself prints the quadratic-weight Cayley application for every unimodular alpha on328-329 with Bloch seminorm bound8c. The choice of a zero and the displayed normalization are our checked specialization, distinguished from a literal printed B(0)=0 formula.

The published problem does not formally define 'explicit' as a finite algebraic recursion with a specified error modulus. Its2019 update explicitly credits AAN's construction. Adopting a narrower operational meaning for a present algorithm does not establish that the original historical question remained open or that PR65 newly resolved it. AAN's covering method differs from PR65's finite-stage algebraic recipe; identical-method priority is not asserted.

## Earlier mechanism and PR65's distinct ordering

Piranian, Two monotonic, singular, uniformly almost smooth functions, Duke Math.J.33(1966),255-262, printed260-261, credits Kahane and prints the fixed absorbed four-adic rule: start at height1; replace a positive height M by(M-1,M+1,M+1,M-1); replace0 by four0s. It excludes finite positive ordinary derivatives at every point. This is an earlier inspected printed antecedent than Kahane1969. Duren-Shapiro-Shields, Singular measures and domains not of Smirnov type, Duke Math.J.33(1966),247-254, printed248-250, defines the affine-periodic primitive and proves its Zygmund condition equivalent to F'(z)=O((1-|z|)^-1) for the Herglotz transform. Their primary application uses exp(-aF), not the Cayley Blaschke answer. Neither complete1966 paper is described here as literally printing Holland's exact application.

PR65's first-stage heights are(2,0,2,0), whereas the fixed old rule gives(0,2,2,0). The measures differ, including first-quarter mass1/2 versus0. The submitted neighbor-directed sign choices are a modified deterministic ordering of an old absorbed-walk mechanism. No necessary new benefit of those choices has been established. Independent checks prove that the old fixed rule has the same mass consistency, atomlessness, singularity, all-point ordinary-density obstruction, circular neighbor bound and effective midpoint approximation modulus. This supports mechanism attribution, not an assertion of literal copying.

## Supported disposition and limits

The exact source problem has an earlier sufficient construction credited as explicit by the2019 problem update. This positive prior evidence is enough to withdraw a newly-solved-open-problem claim. It does not identify the earliest solution, first target-specific articulation, identical algorithm, a complete world-wide priority chain, or the novelty of every quantitative detail in PR65. None of those stronger absence/earliest claims is required to classify the original question as already resolved for this program.

The separately audited PR65 theorem remains mathematically verified. It can be accepted as attributed progress/exposition with status already_solved, not promoted as a novel open-problem solution. Original two proof-search turns out of five stay unchanged. The prior work and this newly written normalization deduction are distinguished. All copyrighted supplied PDFs, full text and rendered pages stay in the private cache; public findings reproduce only the necessary authored mathematical deductions and bibliographical evidence. AI tools were used extensively; this audit is unrefereed and has no conventional human peer-review or formal proof-assistant certification.
