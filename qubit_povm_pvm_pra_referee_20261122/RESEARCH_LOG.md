# Independent referee log

Review date: 22 November 2026. Times in UTC. Percentages estimate progress toward a manuscript ready to submit to Physical Review A.

| Time | Completion | Checkpoint |
| --- | ---: | --- |
| 21:38 | 15% | Read pull request 1451 and the full revised manuscript and appendices. Checked each proof step by hand, including both POVM strategies, the Bell-operator expansion and the scalar certificates. Found no error in a stated result. |
| 21:41 | 30% | Started four independent sub-reviews: bibliography and prior art, Lean statement audit, adversarial proof reading, and numerical falsification. Rebuilt the PDF with Tectonic 0.16.9 and reran the exact artifact suite and the earlier review's checker. All passed. |
| 21:50 | 45% | Lean audit returned: the formal statements match the three claims, with no vacuity or forbidden construct. Corrected three wording errors in the verification appendix. |
| 21:57 | 60% | Bibliography audit returned: all entries exist with correct metadata. The description of Cerf and Ollivier was inaccurate, and the manuscript did not say that Navascués et al. state the CGLMP case as a conjecture or that Zhu et al. leave the two-setting program open. Verified each point against the source text and rewrote the introduction and related work. Added nine verified references. |
| 22:04 | 80% | Adversarial reading returned: no false statement; stationarity and the second derivative along curved feasible curves were asserted without derivation. Wrote both derivations into Sections 7 and 8 and repaired the smaller imprecisions. |
| 22:32 | 92% | Numerical falsification returned: sum-of-squares identity exact; both witness values exact; largest projective value found 28.8877 against the bound 28.9; no positive POVM-over-PVM gap in 7,845 two-setting functionals. Wrote the referee report. |
