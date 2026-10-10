# Separate corrections to the preserved author freeze

These are editorial corrections only; no frozen file was changed.

## S1. 2008 theorem concerns the closure

In `STATEMENT_AND_SOURCES.md`, replace the paragraph beginning “The 2008 report uses a strict cone” with:

The 2008 report defines the strict cone C_d by scal(R)>d||R_W||, but its displayed preservation theorem is for the closure, overline(C_d). This closure is the target closed cone after setting c=2n(n-1)/d^2. The report states PDE sufficiency, with necessity for PDE preservation separately conjectural. It must not be silently substituted for the closed-cone ODE equivalence in the 2007 target.

Evidence: Christoph Böhm, joint with Burkhard Wilking, “Ricci flow in higher dimensions,” OWR 34/2008, p. 1942. https://ems.press/content/serial-article-files/46179 . The overbars were visually checked on the hash-matched PDF. This clarification does not alter any proved partial mathematical result.

The accompanying `corrections.patch` applies this change to an extracted working copy. Keep the author freeze untouched. A new corrected release would require its own new manifest and transport hash.
