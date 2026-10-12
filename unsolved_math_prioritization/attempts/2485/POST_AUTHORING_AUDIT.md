# Post-authoring audit supplement

Date: 2026-10-12. This is a separate supplement to the mathematical audit. Its original reviewed proof bytes remain frozen; this public edition applies only the distribution edits recorded in EDITION_MAP.json.

## Finding

**PASS on the final authored versions.** The final authored versions of ACTUAL_MINIMUM_PARTIALS.md, SOURCE_CORRECTION.md and COMPUTATIONAL_CERTIFICATE.md were read in full. Their exact original byte pins are recorded below and in ORIGINAL_INPUT_PINS.json. This acceptance applies to these bytes, not to unspecified later revisions.

- The finite construction correctly retains the strict inequality T>B_y/(1-D_y), every leading-digit filter, and n>k+1. The statement L_k is divisible by k(k-1) holds because k and k-1 are coprime, so its domain proof works even at k=3.
- The asymptotic proof now explicitly fixes epsilon, takes a limsup, and only then allows epsilon to approach zero. The PNT partial-summation calculation and polynomial choice of T are valid. The claimed scale and prior-art limitations are accurate.
- The prime-transport theorem uses a separate A_k notation allowing trivial n values, but its explicit n>q+1 hypothesis restores exactly the correct domain for the conclusion about g. The equivalence and actual-minimum inequality are correct.
- The printed-lemma counterexample satisfies all candidate conditions. Its uniform extension to n=k+L_k is correct, and the implementation caveat is preserved.
- The computational certificate document correctly explains the search jump, finite termination, independent local-period verifier and complete-coverage proof. It explicitly restricts the independently certified scope to k<=46.

## Repaired full-density calculation

SOURCE_CORRECTION.md Section 2 is correct. For any prime p<q, p does not divide q, so d_p=(q-1) mod p lies in [0,p-2]. Incrementing q-1 changes exactly the units digit. The leading positions do not change: crossing a p-power at q would require q=p^a, impossible for p<q and prime q. Therefore the full local density ratio is (p-d_p-1)/(p-d_p), with all higher-digit factors cancelling legitimately.

The new prime q contributes precisely (q-1)/q, because the base-q digits of q are 10. CRT independence applies to the pairwise coprime prime-power moduli, yielding the stated exact product identity. Each units-digit ratio is at most (p-1)/p, and the remaining factor (q-1)/q is below 1. Thus the displayed weaker upper bound by the product over p<q is valid; the slightly stronger product over p<=q is also valid. Mertens's theorem then supplies a logarithmic lower bound for the reciprocal-density model's prime-step ratio. None of this transfers a ratio theorem to the first admissible integer g(k).

An independent exact-Fraction check reconstructed both densities from all digits and confirmed the identity and inequality at all 45 primes from 3 through 199. This is a regression check supplementary to the proof.

## Negative-control replay

The separately retained authored negative-control program was inspected and rerun without altering the original author packet. All five results agree with the original report and the aggregate record in VERIFICATION.json: missing initial coverage, inclusion of an admissible integer, an incorrect rejecting prime, an incorrect alleged minimum, and a stale checksum are rejected. The first four tests reseal their mutated metadata to reach semantic checks; the fifth deliberately preserves a stale checksum. Thus they should not be described as five resealed semantic tests. No source-author code was executed.

## Final editorial review

The two earlier editorial qualifications have been resolved. The composite-parameter sentence now states the valuation identity with a clearly defined general parameter K and the correct subtraction of v_p(K). Public mathematical status and computation-scope qualifications are preserved. Both changed documents were reread in full; SOURCE_CORRECTION.md remains byte-identical. No mathematical objection remains within this audit's stated scope.

## Exact original authored-file pins

- ACTUAL_MINIMUM_PARTIALS.md: 6,120 bytes; SHA-256 3742a96b89aa3cfa856a294533eec47135e9684506bde87d92241ccf35d8e827.
- SOURCE_CORRECTION.md: 3,897 bytes; SHA-256 86e83da6a5824f67060b6a77d6577108abe7d22060f7ea4c8cf0f2224936dd79.
- COMPUTATIONAL_CERTIFICATE.md: 4,059 bytes; SHA-256 570eb2bcf33853235b48e9c456fbb7c8f9cfccb2a6cc90863795c5255322cd58.

Additional historical verifier, manifest, negative-control and comparison identities are summarized in ORIGINAL_INPUT_PINS.json and VERIFICATION.json. The original audit's mathematical conclusions and limitations remain unchanged.
