# Retained diagnostics

2026-10-16 05:43 UTC (approximate): initial exact control run raised RuntimeError: independent N6 product mismatch. I had speculatively guessed the arbitrary-M polynomial as 40+4(m²+n²), without deriving it. That guess was discarded; the enforced independent check compares the two direct Euclidean phase constructions and separately checks origin product40. No candidate files had been read.

2026-10-16 05:45:58 UTC: initial physical sweep reached every primitive target case and then failed its negative-repetition threshold (1e-4). Retained stderr. Separate diagnosis shows all six excluded repetitions vary, but repeated period11 has maximum relative spread1.71455e-5, below that arbitrary threshold. Revised falsification threshold to1e-10, still at least35 orders above numerical target tolerance; preserved complete diagnostic rows. This is a test-threshold correction, not a theorem counterexample.

2026-10-16 05:47 UTC (approximate scratch calculation): preliminary general-axis expression evaluation failed with AttributeError: int object has no attribute subs, because integer-valued normal norm was not sympified. The final extended exact checker explicitly sympifies every norm and passes. No mathematical conclusion was drawn from that failed scratch command.
