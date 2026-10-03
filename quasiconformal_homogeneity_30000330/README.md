# Audited partial research on quasiconformal homogeneity

Problem 30000330 / OWR-1106-004, rank 497.

**Unresolved, five substantive attempts out of five.** The independent review passes the partial reductions and their stated limitations. Neither a universal ordinary-homogeneity gap nor a counterexample is claimed. This is AI-assisted, unrefereed research, with no novelty or first-resolution claim.

Read the [clarifications](CLARIFICATIONS.md) together with the [frozen research report](public/REPORT.md). The clarifications address all four precision notes in the [independent audit](independent-audit/AUDIT.md). The six originally frozen author files and both original manifests are preserved byte for byte; historical references to a pending review describe the author freeze, not the current reviewed status.

## Packet contents

- [Author report and attempt log](public/README.md)
- [Full independent mathematical audit and controls](independent-audit/README.md)
- [Publication clarifications](CLARIFICATIONS.md)
- [Publication manifest](PUBLICATION_MANIFEST.json)

The author script passes 915 exact algebra cases. The independent script separately passes 915 rational parameter cases, five incorrect-formula controls, and an integral intersection-form check. Its approximate strong-homogeneity constant is a floating-point diagnostic, not an unrestricted bound. These computations do not establish the imported analytic theorems or the conjecture.

From this directory, run:

```
python3 verify_packet.py
python3 independent-audit/verify_audit.py --author-dir public --replay-author
python3 -O independent-audit/verify_audit.py
```

The public packet contains no source PDFs, copied corpus, source-page images, or private context. The proposed queue change only sets this problem's Status to `unsolved` and Turns to `5/5`; no other queue fields are part of this research contribution.
