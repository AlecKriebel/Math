# Attempt2 — Gaussian moment positivity

**Outcome: complete real-coefficient subcase; complex case unresolved.**

The missing H2 coefficient when n>=3 gives Gaussian moments 1,1,1/2 for P,xP,x²P.
Assuming a zero-free real polynomial makes it positive and yields the impossible
negative integral of (x-1)²P. The remaining n=2 cases are resolved by odd degree
or the even-part bound E(x)>2|x|. Full proof and all degree-drop cases are in
`PROOF.md` §1.

For complex a,b only Re P is a real polynomial to which positivity applies.
A real zero of Re P does not imply a zero of P. The later exact complex
triple-zero construction rules out extending this argument by equating those
notions. No positivity assumption on a complex measure is made.

Completion estimate toward the unrestricted target: 15%, heuristic only.
