# Mutual multiphase domination does not force deterministic transport

Problem 30003386, corpus identifier OWR-15212-005, asks whether mutual componentwise domination of atomless vector measure spaces entails deterministic componentwise maps in both directions. The answer is negative. The interval/square example here has common probability kernels in both directions and a deterministic reverse projection, but no deterministic forward map.

This packet gives a checked rederivation of Alper Ferudun's prior interval/square counterexample, Theorem 3.1(1), pp. 4-5, in his unrefereed preprint dated 2 October 2026, DOI [10.5281/zenodo.23107180](https://doi.org/10.5281/zenodo.23107180). No novelty claim is made. His component densities (x,1-x) and this presentation's normalized densities (1,2x) are equivalent under an invertible component change, as detailed in the proof.

## Read the argument

- [PROOF.md](PROOF.md) contains the self-contained proof, source notation corrections, normalization, atomlessness argument, and normalized everywhere-positive density variant.
- [AUDIT.md](AUDIT.md) records the mathematical and source-scope checks.
- [ACCEPTANCE.md](ACCEPTANCE.md) states the accepted conclusion, hypotheses, qualifications, and review limits.
- [SOURCE_METADATA.json](SOURCE_METADATA.json) records public source locations, PDF hashes and sizes, retrieval and inspection history, and publicly stated manuscript status.
- [ARTIFACT_MANIFEST.json](ARTIFACT_MANIFEST.json) records the byte counts and SHA-256 hashes of the five preceding files. It excludes itself to avoid a circular checksum.

## Essential scope qualification

Mutual probability-kernel domination is proved on the compact standard Borel spaces [0,1] and [0,1]^2 with their Borel sigma-algebras. The obstruction to deterministic maps persists for completed-source-measurable maps into the Borel target, and maps into a fully completed planar target cannot evade that obstruction. The forward kernel is not claimed to extend simultaneously to every set in the fully completed planar target sigma-algebra. See the proof's completion section.

The original question appears in Gershon Wolansky's *Multiphase Optimal Transport*, Oberwolfach Report 7/2017, printed p. 388, [DOI 10.4171/OWR/2017/7](https://doi.org/10.4171/OWR/2017/7). The report's reverse-space and component-index notational slips are explicitly identified in the proof; no additional equal-dimension, continuity, invertibility, or component-independence hypothesis is imposed on the question.

## Review disclosure

This exposition, audit, acceptance report, and packet preparation are AI-assisted. No external human review, journal peer review, or formal proof-assistant certification of this packet has occurred. The audit's use of “independent” means a separate check of the displayed argument; it does not describe external human refereeing. The cited preprint is publicly described as unrefereed and AI-assisted, and this packet does not change that status. The source review covers the relevant interval/square construction, definitions, and manuscript-status evidence, not every result in the preprint.

The packet includes authored exposition and public bibliographic and verification metadata only. It includes no third-party source documents, copied source extracts, source images, datasets, arithmetic output, or executable programs. All mathematical details needed for the counterexample are in the written proof.
