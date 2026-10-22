# Acceptance of the polynomial lemniscate inradius reconstruction

## Decision and theorem

**Accepted as a complete conventional mathematical proof. No mathematical correction patch is required.**

This acceptance concerns database problem 2450 / Erdős problem 1039, as of October 11, 2026. The complete candidate reconstruction and independent audit have both been read. All mathematical proof steps in the frozen candidate and the audit are accepted. The complete mathematical sections and all section headings of both documents are preserved in this packet.

For every integer n >= 1, let F_n be the monic degree-n polynomials whose roots, counted with multiplicity, lie in the closed unit disk. Define

rho(f) = sup {r > 0 : some open disk of radius r is contained in {z : |f(z)| < 1}},
R_n = inf {rho(f) : f in F_n}.

The accepted conclusions are

(log 2)/n <= R_n <= rho(z^n - 1) <= pi/(2n),
and max {rho(f) : f in F_n} = 1.

Every f in F_n also has an open disk of radius (log 2)/n centered at one of its listed roots and contained in the strict lemniscate. The original strict lower-bound wording R_n > c/n follows for any fixed 0 < c < log 2.

## Mathematical acceptance basis

The standalone audit provides all seven parts of the proof:

1. The finite Szego-kernel estimate, with the conjugation convention fixed and repeated roots allowed.
2. The off-diagonal product bound on the entire closed polydisk, derived on the torus and extended by coordinatewise maximum modulus. The invalid all-pairs extension is explicitly excluded.
3. The exact scaled quadratic-separation bound, including cancellation of all exponential factors.
4. The perturbed-root product inequality, derived from the exact complex pairing identity and nonnegative scalar identity, then elementary calculus.
5. The compact-maximizer contradiction and the finite-root subsequence argument for the open endpoint disk.
6. The root-of-unity witness, bounding distance to the actual complement of the strict lemniscate in both radial cases.
7. The exact maximum inradius, from Cauchy's leading-coefficient estimate and the polynomial z^n.

The audit also expressly checks repeated roots, boundary roots, n=1, empty pair products, all denominator and logarithm domains, strict endpoints, independent disk maximizers, and attainment issues. These arguments, rather than finite diagnostics or a software claim, establish the theorem.

## Exact scope and unresolved questions

The original uniform positive-constant-over-n question is resolved affirmatively, and the sharp order of the worst-case inradius is 1/n. No exact value of R_n, exact limiting constant, or existence of a limit of n R_n is established. There is no assertion that every individual polynomial has inradius of order 1/n; z^n has inradius 1 for every n. The open endpoint disk assertion does not assert containment of the corresponding closed endpoint disk in the strict lemniscate.

This is acceptance of the supplied mathematical argument. It is not external journal acceptance, an assertion of current problem-website status, or Lean compilation or axiom certification.

## Attribution and source limits

Credit for the reconstructed method belongs to Liam Price's May 2026 GPT-assisted proposed proof and Kenta Kitamura's corresponding 2026 Lean development, as documented by the inspected public README/source. No novelty is claimed.

The original problem is Problem 3 on printed page 134 of P. Erdős, F. Herzog, and G. Piranian, Metric Properties of Polynomials (1958). Physical pages 1 and 10, printed pages 125 and 134, were visually inspected; the entire 24-page paper was not read. Public sources are recorded in SOURCE_PINS.json and cited in the complete proof and audit.

The Lean source was only selectively inspected as text. No source-author program, Lean source, imported code, build system, or axiom-reporting command was executed. The frozen local capture has 282,106 bytes and SHA-256 f53e12d1c52e6a28e89298eafed24b878f79b1a9c531425c87522a762c10719e. Removing exactly one terminal LF byte, with no source-line content changes, gives 282,105 bytes and SHA-256 0d643fc771036648cc05476ef1688eee02285b4cb7dbb092072a055e72d034d0, whose Git-blob SHA-1 is efc244f5d31674970b4ea0370b20c31955c779ea. The literal unnormalized capture has Git-blob SHA-1 15f64ac6954408f2866cb82866da1673e64a3b2e. The capture is therefore not literally byte-identical to that stated upstream blob without the one-byte qualification.

On October 11, 2026, direct reads of the EP1039 problem page and forum returned HTTP 403, and the advertised Overleaf project was inaccessible. The live forum and Overleaf proof PDF were not independently read, and their current contents and the website's current status are unverified. The README's status statement is dated May 16, 2026 and is not a current-status certification.

## Preservation and diagnostics

LEMNISCATE_INRADIUS.md retains the candidate's historical sentence saying that it was awaiting independent audit. That sentence describes the frozen candidate's original stage; the completed independent audit and the present acceptance supersede that historical status. The candidate's static-source identification must be read with the exact single-terminal-LF qualification above and in AUDIT.md. Neither qualification changes a mathematical argument.

The only document changes remove private packaging identifiers, executable invocation syntax, and private coordination history, with complete text preservation verified against an exact editorial mapping. Every section remains, and the mathematical sections are byte-for-byte identical to their accepted originals. PRESERVATION.json supplies aggregate verification results and original/public hashes.

The independently authored exact rational diagnostic checker produced 39,357 checks per run in normal Python mode and both optimization modes (-O and -OO), including three negative controls. Fresh preparation runs matched the three audited receipts. These are bounded corroborative diagnostics only, not a substitute for proof, a Lean execution, or a continuum-wide exhaustive check. CHECKS.json contains only aggregate results.

## Public packet boundary

The public packet contains the complete authored reconstruction, complete authored audit, this acceptance, navigation, public-source verification metadata, aggregate diagnostic results, preservation metadata, and a closed manifest. It contains no third-party source copies or extracts, source images, dataset contents, scripts, raw computational data, or private coordination material.
