# Acceptance report for problem 30003386

Assessment date: 11 October 2026.

## Accepted conclusion

The written argument establishes a complete negative answer to the mutual-domination question in Gershon Wolansky's *Multiphase Optimal Transport*, Oberwolfach Report 7/2017, printed p. 388. Two positive atomless vector measures on measurable spaces can admit common componentwise probability-kernel transports in both directions while failing to admit the requested pair of deterministic componentwise maps. In this construction the reverse map exists and the forward map does not; the question does not require inverse maps.

The construction uses two scalar probability components on each of the compact standard Borel spaces [0,1] and [0,1]^2. Each scalar component and each vector measure is atomless. The common forward fiber kernel and reverse projection kernel meet the transport requirements directly. The second-moment calculation forces the first coordinate of any putative forward map to equal its input almost everywhere. A Borel-graph null-set contradiction then rules out that map. The same reasoning applies to the normalized continuous everywhere-strictly-positive second-density variant in PROOF.md.

The source question assumes positive atomless vector measures and a common measurable transport family for all components. Its later optimal-transport discussion does not impose extra restrictions on this earlier question. The construction uses probability kernels, so no relaxation to unrelated componentwise kernels is needed. The evident repeated-space typo in the reverse-domination expression and the N/k component-index mismatch are disclosed and interpreted consistently with the stated question.

## Completion qualification

The mutual-domination claim is established on the specified Borel spaces. Nonexistence of deterministic forward transport remains valid if the source sigma-algebra is completed, using Borel versions of the coordinates and absolute continuity of the source components. Maps into a fully completed planar target would also have to satisfy the contradicted Borel transport identities. No simultaneous extension of the forward kernel to every set of the completed planar target sigma-algebra is asserted.

## Attribution and status

This is a verification and rederivation of the interval/square example in Alper Ferudun's *A Negative Answer to Wolansky's Question on Mutually Dominating Multiphase Measure Spaces*, unrefereed preprint dated 2 October 2026, Theorem 3.1(1), pp. 4-5, [DOI 10.5281/zenodo.23107180](https://doi.org/10.5281/zenodo.23107180). The earlier density pair (x,1-x) is transformed to (1,2x) by (alpha,beta) -> (alpha+beta,2alpha), with inverse alpha = sigma_2/2 and beta = sigma_1-sigma_2/2. Applying this invertible linear change to both spaces preserves simultaneous map and kernel transport. No novelty or priority claim is made.

PROOF.md preserves the accepted mathematical exposition byte-for-byte. AUDIT.md preserves the mathematical argument and source assessment; its closing nonmathematical file-inventory and workflow references have been adapted to this packet. SOURCE_METADATA.json retains the public source evidence, with administrative queue-position metadata omitted. The artifact manifest identifies the exact public file bytes.

## Review and evidence limits

The proof, audit, acceptance report, and packet preparation are AI-assisted. There has been no external human review, journal peer review, or formal proof-assistant certification of this packet. “Accepted” records this mathematical assessment, not an external referee decision. The cited preprint's own unrefereed status is retained.

Exact rational checks support the displayed arithmetic and invertible component conversion. They are not a machine formalization of the measure-theoretic argument. Countable additivity, kernel measurability, atomlessness, almost-everywhere substitutions, and the graph contradiction are justified in the written proof. No source-author code was executed. Source inspection covers the original question and the relevant prior construction and status evidence; it does not certify all claims in the prior preprint or exhaust the literature.
