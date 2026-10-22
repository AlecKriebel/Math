# Independent mathematical and reproducibility audit

## Verdict

**The mathematical counterexample and minimally hardened verifier are accepted. All 687 independently run controls passed.** No mathematical correction is required. The original frozen certificate was already a valid, exactly verified witness. A narrow input-schema weakness was found in the standalone verifier and corrected in a separate copy; the original freeze was preserved.

The claim is exactly this: a rational polynomial of actual degree 200000000000000000100 has strictly positive coefficients, at least four distinct negative roots, and exactly three distinct corners of the binomial-multiplication tropical polynomial. This is not a claim about conventional slope-jump multiplicities, an exact total real-root count, simplicity of every root, smallest degree, novelty, or priority.

The complete PROOF.md and all verifier, replay, bootstrap, manifest, certificate, and release-description files were read. The mathematical reconstruction and first parser exploits were completed independently before reading the separate scope review. Its eventual conclusions agree with this audit. The author's freeze-and-test script was inspected but was not executed, since executing it would rewrite the original freeze.

## 1. Independent arithmetic reconstruction

The independent program `independent_math.py` does not import or execute the author's mathematical verifier. It hard-codes the displayed witness and reconstructs its degree-100 seed in scaled integer arithmetic.

The sixteen subset sums of 5, 15, 25, and 55 are distinct. Scaling coefficients by S=10^72 makes the full seed integral. The three corrections are added with their explicitly expanded integer coefficient vectors. This independently verifies the constant coefficient C=1+v^2+v^6+v^12, the leading coefficient 1, and the bounds 0<=q_j<=1 at every interior index, for v=10^(-6).

For each of the five displayed sample points t=A/D, the program computes S D^100 Q(t) in two separate ways:

1. A homogeneous sum of all 101 scaled coefficients, using integer powers of A and D.
2. The product S times the four factors D^e+A^e, followed by three separately homogenized correction terms.

These agree as integers and have signs +,-,+,-,+. The independent check uses neither floating-point evaluation nor the author's Horner implementation. It records short hashes and bit lengths of the signed integers rather than publishing thousands of digits. The points are strictly increasing, negative, and have absolute value between 1/2 and 2.

The factor H(-r) is independently evaluated as a product of positive geometric sums at all five points. The analytic uniform estimate is also valid: the product of the four exponents is 103125, their reduced degrees sum to 96, and 103125/(1-96v)<200000. The factorizations and four signed bracket inequalities in the proof have the correct exponents and signs. In particular the term -H v^4 at the third bracket and -H v^9 at the fourth bracket have the correct sign.

The independent program computes the actual 99 rational ratios binom(N,K+j)/binom(N,K), using the exact recurrence with factor (K+101-j)/(K+j). It checks every individual weighted-coefficient majorant against L=1+v^2/200. At all seventeen nonzero interior seed positions it also verifies the stronger direct power-form chord comparison, raising both positive sides to power 100. No logarithm, fractional-power approximation, huge binomial coefficient, degree-N expansion, or enormous denominator for delta is formed.

## 2. Root persistence and full support

The coefficient denominators divide 10^72, and sample denominators divide 10^42. Consequently the denominator of every Q(t) divides 10^4272. The integer nonvanishing therefore gives |Q(t)|>=10^(-4272). Since |t|>1/2 and 10<16, the unperturbed value has absolute value greater than 2^(-K-17088).

The filler E has absolute value at most delta(N+1)2^N<=2^(-N^2+2N), using binom(N,i)>=1 and N+1<=2^N. Omitting the two distinguished indices cannot increase the estimate. The exact positive exponent gap is

40000000000000000039499999999999999992712.

Thus E cannot reverse any sample sign. K is even, so multiplication by t^K also preserves signs. The intermediate value theorem gives a root in each of four disjoint negative intervals. This is enough for four distinct roots; no claim that there are exactly four roots or that every root is simple is needed.

At the two omitted filler indices K and K+100 the coefficients remain C and 1. At every other index the filler contributes a positive rational number to a nonnegative seed coefficient. At indices 0 and N it contributes exactly delta. Hence every coefficient is positive, the actual degree is N, and zero is not a root. This argument covers the entire enormous support symbolically, rather than relying on a finite program pretending to enumerate it.

## 3. Exact three-corner conclusion

Let B=binom(N,K). The symmetry binom(N,K+100)=B follows from N=2K+100. The two distinguished weighted coefficients are CB and B. The filler cancels its reciprocal binomial weights exactly, so all weighted coefficients outside the seed block equal delta.

For every interior block index the ratio bound and delta/B<v^2/1000 give a strict margin below L. The uniform margin is exactly

19/5000000000000000.

The independent check establishes L^100<C. Therefore every central interior height is strictly below the chord from (K,log(CB)) to (K+100,log B). This includes both the original zero coefficients and the original unit coefficients. There is no unexamined interior equality case.

The first of the three proposed hull-edge slopes is positive. The middle one is -log(C)/100<0. The last equals (log(delta)-log B)/K and is strictly smaller than the middle one because B>=1, C<2, and 100N^2>K. All outside-block nonvertices have height log(delta) and are strictly below the corresponding outer chord. Thus the upper hull has exactly the four stated vertices and three edges.

Consequently the maximum of the coefficient lines has exactly three distinct corners, with precisely two maximizing terms at each one. Conventional slope-jump multiplicities are K,100,K and sum to N. Those multiplicities are explicitly outside the audited target. The ordinary-corner conclusion is obtained directly and does not rely on confusing essential tropical roots with all corners.

## 4. Standalone parser defect and minimal correction

The original scalar integer fields already excluded booleans using exact type checks. However four array-valued fields were checked through Python equality alone. Since True equals 1 and 1.0 equals 1, several malformed certificates were accepted by the direct mathematical interface:

- Boolean entries in expected_signs.
- Floating-point entries in expected_signs.
- Boolean entries in sample_offsets.
- A Boolean correction degree.
- Non-ASCII decimal characters in the K string, permitted by str.isdigit and Python integer conversion.

The first four are a genuine schema inconsistency. They do not invalidate the fixed original witness or its mathematical calculations. The non-ASCII string represents the same integer, but accepting it is unnecessarily permissive for the intended integer-string interchange format. All five original acceptances and all five corrected rejections are explicitly reproduced in normal, -O, and -OO execution.

The patch adds exact integer-vector and integer-pair-vector validation, requires ASCII decimal integer strings, and rejects named nonfinite JSON constants explicitly. It makes no arithmetic changes. Ordinary JSON overflow literals such as 1e999 and -1e999 are tested separately: Python's JSON parser converts them to infinities without calling parse_constant, but the exact integer schema rejects them. Every scalar numeric field and both integer-string fields are tested with both overflow signs; all four nested numeric arrays are also tested with overflow.

Only verify_math.py differs between the original and corrected seven-file public slices. The six remaining public files, including PROOF.md and certificate.json, are byte-identical. A new external manifest and bootstrap pin the corrected verifier. The original and corrected pins are both recorded in EXTERNAL_PINS.json; PARSER_HARDENING.patch is the actual unified diff. The original public RESULT.json retains its historical audit-pending value; this external acceptance report records the subsequent audit rather than silently rewriting that frozen history.

## 5. Reproducibility and integrity controls

`run_audit.py` independently constructs the corrected manifest, checks the original externally supplied pins, executes the controls, and verifies that every original input file remains unchanged. It never invokes the author's freeze generator. CONTROL_REPORT.json records 687 passing controls, 229 per interpreter mode, including 78 explicit overflow-literal rejection controls. The actual UID and EUID were both 1000. The final acceptance metadata records these totals.

Coverage includes:

- Independent integer reconstruction in normal, -O, and -OO modes.
- Original and corrected pinned bootstrap replay in all three modes.
- All known old-parser acceptances and corrected rejections in every mode.
- Boolean, floating, null, string, malformed list/pair, nonfinite, overflow, duplicate-key, malformed-JSON, oversized, missing, and symlinked certificate inputs.
- Wrong degree, odd/small K, weak denominator and filler bounds, incorrect signs and target counts, and low H bounds.
- Deliberately corrupted arithmetic implementations, including reversed exact evaluations, a reversed direct correction, and a corrupted seed.
- Individual tampering of every one of the seven frozen public files.
- Extra/missing files, symlinked files, root directories, and manifests, changed manifests, rehashed changed content, and a self-consistent forged replay/manifest pair checked against the trusted bootstrap.
- Direct replay tests of malformed or incorrect external digests, noninteger manifest byte counts, duplicate manifest paths/keys, path traversal, absolute paths, and bad hashes.
- Real relocation through paths containing spaces and a non-ASCII character.
- Genuine nonroot execution with UID=EUID=1000, mode-0444 input files, and a mode-0555 slice directory. Separate write probes actually fail for existing files, new files, the bootstrap, and the manifest.
- Hostile working-directory modules and hostile PYTHONPATH, PYTHONHOME, and PYTHONSTARTUP settings. Isolated startup prevents their execution. File inventory and contents remain unchanged; no bytecode cache appears in either slice.

The original author's 93 reported controls were inspected as historical evidence, but their report was not substituted for these independent runs. Optimized execution does not disable any check: neither mathematical verifier relies on assert.

The trust boundary is an independently obtained bootstrap or replay hash plus the pinned manifest. A manifest supplied by an attacker together with an arbitrary matching digest is not an authenticity guarantee. Bootstrap and replay were inspected for this distinction. The tested contract assumes a trusted Python standard library/interpreter and stable files during a run. It is not a sandbox against a concurrently malicious filesystem administrator, nor a proof-assistant kernel. File hashes establish byte identity; the mathematical review supplies the argument's validity.

## 6. Source and status reconciliation

The source text already retrieved for Shapiro 2015, Section VII, was inspected independently. It specifies positive coefficients, binomial multiplication, and a count of tropical corners. The witness meets precisely those conditions. [Shapiro, arXiv:1503.05295v1](https://arxiv.org/abs/1503.05295v1).

FNS's tropical multiplicity definition, Theorem 11, Lemma 27, and the theorem's proof were inspected. The theorem already supplies the small-curvature obstruction. For binomial weights its curvature is log((1+1/j)(1+1/(N-j))), which tends uniformly to zero on a fixed central block. That establishes the prior-obstruction classification. The unspecified constant in that theorem alone does not certify this particular K; the independently checked finite construction does. [FNS, arXiv:1510.03257v1](https://arxiv.org/abs/1510.03257v1).

The 2024 Section 5 repeats the target as its Conjecture 1 and directs its counterexamples to Conjectures 2 and 3. It does not announce a disproof of Conjecture 1. The later printed status is therefore disclosed as a discrepancy, without speculation about why it arose. [Katkova–Shapiro–Vishnyakova, arXiv:2403.12200v1](https://arxiv.org/abs/2403.12200v1).

SOURCE_METADATA.json independently recomputes the byte counts and hashes of all four already-retrieved PDFs. This is local byte verification, not a new independent network retrieval. The two catalog hashes reproduced in the original public source metadata were not independently re-retrieved in this audit, and no dataset contents are included here.

## 7. Release boundary and conclusion

The release allowlist includes only authored proof/audit text, original or corrected verifier code, certificates for this authored witness, exact-check output, patches, public citation metadata, and integrity/control metadata. It excludes third-party source text/PDFs, dataset contents, private sources, personal information, and private coordination material. The actual output file list and hashes are recorded in the audit manifest. To reproduce, run `python -I -B run_audit.py --original ORIGINAL_PACKET_DIRECTORY`, then `python -I -B seal_audit.py` to reseal the resulting control report; independent_math.py also runs on its own. No publication, queue modification, external outreach, or child task was performed by this auditor.

Accept the witness as a literature-derived negative resolution with an explicit reconstruction. Accept the corrected, independently pinned verifier as the release candidate after the narrow schema hardening. Preserve the original freeze and both sets of hashes for the audit trail. No further mathematical gap is identified.
