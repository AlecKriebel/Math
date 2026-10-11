# Independent audit of the multiphase domination counterexample

## Verdict

ACCEPTED as a complete negative answer to the mutual-domination question in Wolansky's 2017 report, with the precise Borel-space formulation in PROOF.md. This is a verification and rederivation of a prior public counterexample. It is not a novelty claim, a formal proof-assistant certificate, a review of every theorem in the prior preprint, or a statement of peer-reviewed acceptance.

The two necessary presentation clarifications have been incorporated in PROOF.md:

1. Nonexistence of a deterministic map survives completion of the source sigma-algebra. This does not, by itself, assert that the explicit forward kernel extends to the entire completed planar target sigma-algebra. Mutual domination is established on the Borel spaces specified in the construction.
2. The vector-atomlessness argument explicitly splits a set of positive first-component measure and uses absolute continuity of the second component. A blanket statement that any vector atom must be an atom of an arbitrarily chosen scalar component would be too broad.

## Source scope check

The original report's printed p. 388 was inspected as text and as a rendered page. Physical PDF pages 50 and 51 were visually inspected; printed pp. 388-390 were extracted to check the surrounding definitions and references.

The question follows a definition of componentwise transport by a common measurable family of measures. It assumes positive atomless vector measures on measurable spaces. Its additional optimal-transport discussion on the following page does not add hypotheses to the earlier open question. There is no equal-dimension, continuity-of-map, invertibility, or independent-component requirement in the question. The exhibited spaces are compact metric Borel spaces and the transport families are probability kernels, so they satisfy the relevant requirements in a particularly regular setting.

The printed reverse-domination expression repeats Y at its end although the reverse deterministic map is from Y to X. Its index range uses N after defining k components. The audit treats these as the evident notational slips and addresses mutual domination with the same two components on each space.

## Mathematical checks

- Measures and masses: all four components are finite atomless probabilities; both vector masses are (1,1).
- Scalar and vector atomlessness: verified by measurable cuts and absolute continuity, rather than by a point-mass test on arbitrary spaces.
- Forward kernel: P_x = delta_x tensor lambda is a countably additive probability measure on Borel Y for every x. Measurability in x follows from the rectangle case and a monotone class argument.
- Common transport: Tonelli verifies that the same P transports both components; no separately selected componentwise kernels are used.
- Reverse kernel: Q_(u,v) = delta_u is a Borel probability kernel, induced by the continuous projection S(u,v) = u. It transports both components.
- Common reference normalization: using the sum of the components gives reference masses two and density vectors with entries summing to one. Dividing the reference measures by two gives probability references. Neither convention changes the direct kernel proof.
- Moment rigidity: testing the first pushforward against u^2 and the second against u forces integral(a-x)^2 dx = 0. All tests are bounded Borel functions.
- Measurable graph: for Borel b, G_b is a Borel zero set of the Borel function (u,v) -> v-b(u). Its vertical sections are singletons; Tonelli gives area zero. The pushforward of lambda gives that same graph mass one, a contradiction.
- Almost-everywhere changes: both source components vanish on lambda-null sets. Borel coordinate versions preserve the required Borel pushforward identities for completed-source-measurable maps.
- Strictly positive variant: replacing second densities by (2/3)(1+x) and (2/3)(1+u) preserves normalization, kernels, and the contradiction. This eliminates any concern about the zero density at the endpoint.
- Logical scope: failure of the forward map alone disproves the asserted existence of both maps. The reverse map actually exists; no inverse relationship is assumed or needed.

## Prior work and attribution

The actual ten-page PDF of Alper Ferudun's *A Negative Answer to Wolansky's Question on Mutually Dominating Multiphase Measure Spaces* was inspected. Its Theorem 3.1(1), on p. 4, and proof on p. 5 give the interval/square example with components (x dx,(1-x) dx) and (u du dv,(1-u) du dv). The proof uses the same fiber kernel and projection; its rigidity lemma on p. 4 is followed by a Borel-graph contradiction on p. 5. Theorem, kernels, and graph argument were checked visually against the PDF.

The present components are an invertible linear repackaging of those components: (alpha,beta) becomes (alpha+beta,2alpha). Consequently a single map or kernel transports the present pair if and only if it transports the earlier pair. The present elementary moment calculation is a self-contained specialization of the same obstruction.

The PDF's title page dates the manuscript 2 October 2026 and labels it unrefereed. The linked Zenodo record gives version 1.0, publication date 2026-10-02, and DOI 10.5281/zenodo.23107180. Page 9 discloses AI assistance and says the note has not been peer reviewed. The audit does not upgrade these self-described status claims. It does not certify the preprint's other examples, classification claims, numerical verifications, or literature-priority discussion. No author-supplied program or archive was run.

## Evidence and reproducibility limits

SOURCE_METADATA.json records public bibliographic details, PDF SHA-256 hashes, byte counts, retrieval timestamps, inspection locations, and stated manuscript status. ARTIFACT_MANIFEST.json identifies this packet's authored files by byte count and SHA-256. Exact rational checks covered the displayed arithmetic and the linear component conversion. Those checks support bookkeeping; the countable-additivity, measurability, atomlessness, almost-everywhere, and graph-null assertions are established by the written arguments, not by numerical experiments.

The packet consists of README.md, PROOF.md, AUDIT.md, ACCEPTANCE.md, SOURCE_METADATA.json, and ARTIFACT_MANIFEST.json. It contains authored mathematical exposition and public bibliographic and verification metadata. Third-party source documents, source extracts, rendered source pages, arithmetic data, and executable programs are not included.
