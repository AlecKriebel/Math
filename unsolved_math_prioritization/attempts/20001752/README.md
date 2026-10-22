# Problem 20001752: E8 and Leech midpoint Mellin values

This draft research packet received an independent **PASS_PARTIAL** audit.

- The normalized E8 midpoint value is proved to be **1/15** through a universal radial-Schwartz sampling identity.
- A separate Leech weighted-tail functional is proved to be **20/91**. It is not the Leech midpoint moment.
- The original combined question remains **unsolved**, with **5/5** substantive approaches completed. No priority or novelty claim is made.

Read [the proof](public/PROOF.md), [the complete independent audit](audit/AUDIT_REPORT.md), [source checks](public/SOURCE_GATE.md), and [the research log](public/RESEARCH_LOG.md).

The frozen author packet and full independent audit are preserved byte for byte. Their references to a pending audit or an exhausted approach budget record earlier stages. The current audit verdict is PASS_PARTIAL and the canonical queue status is `unsolved`, not `exhausted`. The source-version and numerical qualifications in the audit accompany the result. No human peer-review claim is made.

## Reproduce

From this directory, run `python audit/audit_controls.py`. Its default mode uses only the standard library and checks the frozen inputs and exact controls. Add `--numeric` for optional mpmath diagnostics. The audit records 331 exact-mode assertions and 344 numeric-mode assertions, with eight and nine rejected mutations respectively. Floating-point quadrature is not certified interval arithmetic.

The author scripts in `public/` require SymPy/mpmath as described there. They write diagnostic output, so run them in a copy if preserving the frozen byte-level manifest matters.

`PORTABLE_ALLOWLIST.json` lists the exact distributable files and hashes. Complete papers, source PDFs, source-corpus extracts, cached prior reports, private work files, and coordination records are excluded.
