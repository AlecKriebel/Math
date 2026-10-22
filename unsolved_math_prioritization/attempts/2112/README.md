# EP423 / 2112: fourth-power Hofstadter plateau bound

This prose-only edition contains a complete elementary partial proof and its
full independent audit. For the classical seed (1,2), with natural logarithms,

    a_n-n >= (log(log(n))-log(log(5)+log(2)/3))/log(4), for every n>=2.

The fourth-power finite plateau bound improves the specific double-logarithmic
coefficient displayed in Tang arXiv:2603.09939v2 Theorem 1.4. It is an elementary
modification of Tang's plateau and threshold-function strategy, which is
credited explicitly. No exact asymptotic, deviation upper bound, b_n=o(n),
a_n=O(n), global novelty, priority, or optimality is established. Synthetic
prefix obstructions are not asserted to be actual greedy-sequence prefixes.

## Contents

- PROOF.md: complete authored proof and remaining problem
- AUDIT.md: complete independent mathematical audit and scope qualifications
- ACCEPTANCE.md: decision, identity bindings and verification interpretation
- ACCEPTANCE.json: original acceptance fields with an editorial scope note
- SOURCES.json: public bibliographic, retrieval and inspection metadata
- VERIFICATION.json: historical finite-check counts, hashes and limitations
- MANIFEST.json: exact member list and hashes of the other seven files
- README.md: this scope and navigation guide

The source comparison is specifically with [Tang v2](https://arxiv.org/abs/2603.09939v2).
Original formulations were historically checked in [Erdős 1977, printed
p. 71](https://www.renyi.hu/~p_erdos/1977-27.pdf) and [Erdős–Graham 1980,
printed p. 83](https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf).
Complete file retrieval is distinguished from text-reading and visual
inspection scope. No newly verified live problem-tracker status is claimed.

Historical independent checks remain active under normal Python, -O and -OO
and produced identical reports. The candidate's assertion-based verifier now
rejects optimized modes rather than silently skipping assertions. This
edition does not include either executable checker; its verification summary
is historical metadata, not a claim that the programs can be rerun from these
eight files. Mathematical inspection uses the full written proof and audit.

## Edition and review statement

This prose-only edition preserves the complete substantive mathematical argument
and its qualifications. The AI-assisted work is unrefereed. Acceptance refers
only to the independent internal AI audit of this partial theorem; no external
human peer review, journal acceptance, or formal proof-assistant certification
is claimed. No mathematical correction was required.

The historical finite checks and scholarly-source inspection are described
for provenance. Preparing this edition added no mathematical test execution
and no scholarly-source retrieval or inspection. The original sealed candidate
and audit are unchanged. Programs, raw datasets, detailed execution receipts,
full computational certificates, copied source documents/text/images, and
private coordination material are not distributed. This is a mathematical
prose and verification-metadata edition, not an executable reproduction package.
