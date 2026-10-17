# Four point quantum symmetrizer reader

13 October 2026. Bounded mathematical verification for queue row 1773, problem `/30004316`.

For the solution `X = Z/4`, `r(x,y) = (y,x+1)`, the accepted proof and independent audit establish the following over every field of characteristic different from 2:

- The signed quantum-symmetrizer image fails to be a bimodule resolution. This verifies the core of Ferudun's existing Theorem 1.3(a) and answers the precisely specified Farinati–García Galofre Question 44 negatively.
- For the character sending every generator to 0 (`k0`), no chain quotient through which the specified comparison factors can repair the comparison. This verifies the core of Ferudun's existing Theorem 1.3(b).
- For the character sending every generator to 1 (`k1`), this same example has an explicit chain quotient on which the comparison is a quasi-isomorphism: remove the all-sum tensor line in each degree at least 2. This is an authored all-degree proof for this example and this coefficient module.

The first two claims are credited to Ferudun. No novelty claim is made for any result. His pinned manuscript was dated 1 October 2026 and described itself as unrefereed and AI-assisted; its broader census is not certified here.

## Essential limits

The terse OWR Problem 2 still requires a source-scope qualification. Its omitted coefficient and quotient conventions have not been settled. This reader does **not** resolve a universal constant-character suitable-quotient question. In particular, failure for `k0` does not rule out every quotient for `k1`.

The positive quotient is a quotient of chain complexes after choosing `k1`. No algebra-ideal, Hopf-ideal, coefficient-independent, or universal construction is claimed. Characteristic 2 is excluded throughout.

There are at least two exhibited independent degree-2, weight-3 classes in all the permitted characteristics. **Exactly two** is the recorded rational result. The independent finite-field audit finds **dimension three in characteristic 3**, with `rank(Q3) = 46`; this is stated separately from the rational computation. Finite checks support the proofs and do not replace their all-degree arguments.

## Read the proof and audit

1. [Accepted proof](REPORT.md): definitions, signed comparison, obstruction, and explicit constant-character chain quotient.
2. [Independent mathematical audit](audit/AUDIT.md): accepted scope, sign and coefficient checks, and the characteristic-3 qualification.
3. [Proof check results](check_results.json) and [independent audit results](audit/independent_results.json): preserved original finite computation records.
4. [Proof source metadata](SOURCES.json) and [audit source pins](audit/source_pins.json): public URLs, retained PDF byte counts and SHA256 values, and the prior inspection scope.
5. [Portability record](PORTABILITY.md): the only changes made to the two checkers; the proof and audit text remain byte-for-byte unchanged.

This reader contains authored text, authored code, computed check results, and public source metadata. The source PDFs and source archives are not needed to run its checkers and are not included. The metadata records historical retrieval and inspection, not a new download or fresh literature review during packaging. The extra JKV and CJKV entries in the original proof metadata are provenance only; their theorems are not dependencies of these elementary arguments.

## Reproduce the finite checks

Tested with Python 3.12.14 and SymPy 1.14.0. The two mathematical checkers use the Python standard library and SymPy, with exact arithmetic. The manifest verifier uses only the standard library. [requirements.txt](requirements.txt) records the tested SymPy version; in an environment needing it, install with `python -m pip install -r requirements.txt`.

From this reader directory, use a separate output directory so the historical result records remain unchanged:

```sh
out="$(mktemp -d)"
for flag in '' -O -OO; do
  python $flag verify_manifest.py
  python $flag check_claim.py --output "$out/proof${flag:-normal}.json" > /dev/null
  cmp check_results.json "$out/proof${flag:-normal}.json"
  python $flag audit/independent_checks.py --output "$out/audit${flag:-normal}.json" > /dev/null
  cmp audit/independent_results.json "$out/audit${flag:-normal}.json"
done
```

Every command must exit successfully; each `cmp` is silent on a byte-identical match. Every mathematical check remains active under normal Python, `-O`, and `-OO`. Omitting `--output` prints JSON to standard output without writing a result file. Both checkers may also be invoked by absolute path from another working directory; `--output` is interpreted relative to the caller's working directory.

The scripts perform the same bounded computations as the accepted reports. They neither access the network nor run programs from a source archive. The independent checker does not import or execute the proof checker.

## File integrity

[MANIFEST.json](MANIFEST.json) lists every reader file except itself, with byte counts and SHA256 values. `verify_manifest.py` checks those bytes and the complete file inventory, using explicit checks that also remain active under optimization. Added output files inside the reader will correctly cause its inventory check to fail, so keep outputs elsewhere.

The separate packaging report pins the manifest itself. This is an ordinary reproducibility check against a trusted manifest, not an authenticity certificate or a guarantee about a hostile filesystem. No repository or queue changes are part of this reader.
