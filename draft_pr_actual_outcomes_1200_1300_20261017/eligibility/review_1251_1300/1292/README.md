# An L2 counterexample to unrestricted dyadic tail LIL bounds

Problem 30001617, reference OWR-4531-020. Prepared 11 October 2026 UTC.

The unrestricted assertion has a negative answer. A real L2 function on [0,1) has dyadic tail square sums Q_n that are positive at every finite index and tend to zero, while the absolute tail divided by sqrt(Q_n log log(1/Q_n)) has infinite limsup almost everywhere. The total realized square function is at most one on every binary path. Zero extension gives a globally integrable real-line counterexample to Artur Nicolau's question in Oberwolfach Report 49/2010, printed p. 2872.

This negative phenomenon is prior work of Santosh Ghimire, presented in 2011 and developed in his 2012 dissertation, Section 3.3. The full dissertation section has been inspected. This packet preserves a self-contained all-positive stopped-block reconstruction with explicit parameters and a summable future-error budget. It makes no novelty claim.

## Read the packet

- [Complete proof](PROOF.md)
- [Mathematical audit and exact source interpretation](AUDIT.md)
- [Acceptance scope and artifact bindings](ACCEPTANCE.json)
- [Scholarly-source identity and inspection metadata](SOURCE_PINS.json)
- [Aggregate verification summary](CHECK_SUMMARY.json)
- [Public file manifest](MANIFEST.json)

## Mathematical scope

The full proof establishes predictable block activation, L2 and almost-sure convergence to one terminal function, the identification of every martingale value with its terminal conditional mean, eventual block success, logarithmic denominator bounds, strict tail positivity at every finite index, and the exact dyadic-index and logarithm match under zero extension. The successful-block start indices are used only pathwise; they are not asserted to be stopping times.

The cited positive theorems assume a uniform within-atom comparison of square tails. The construction directly violates that hypothesis on positive-measure subevents. A positive statement along selected times does not imply a bound on the full limsup. No specialized positive LIL theorem is imported or certified here.

## Verification and limits

The entire accepted proof is preserved byte-for-byte. Every mathematical and source-analysis section of the accepted audit is also preserved byte-for-byte. Editorial changes only remove a non-public record name and clarify that the audit is AI-assisted, with no external human peer review or formal proof-assistant certification. The acceptance report and source metadata retain their original claims and limitations, with explicit preparation metadata added.

The accepted audit and exact finite checks were rerun in normal, -O and -OO Python modes, with byte-identical results. Each mode enumerates 1,608 finite paths across four exact models and rejects both nonstopped and anticipative mutations. The 21 upstream integrity-control runs passed. Frozen candidate, source, authored-artifact and validation-receipt hashes and byte counts were rechecked. These checks support the written argument; they do not replace its infinite analytical proof.

This directory contains authored mathematical exposition, audit and acceptance reports, plus source and aggregate verification metadata. Source PDFs, source text, rendered source pages, datasets, executable scripts and private coordination material are excluded. Hashes identify prepared bytes; they do not certify mathematical truth. Preparation itself performs no publication, repository operation or queue change.
