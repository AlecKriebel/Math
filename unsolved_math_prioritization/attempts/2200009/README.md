# Mesh-preserving constant-coefficient difference operators

Rank 1030 / 2200009 / AMR-021-0009: **already_solved, 0/5**.

The prior solution is credited to Jonathan Leake and Nick Ryder, *Connecting the q-Multiplicative Convolution and the Finite Difference Convolution*, [arXiv:1712.02499v1, Theorem 1.4](https://arxiv.org/abs/1712.02499v1), published in [Advances in Mathematics 374 (2020), 107334](https://doi.org/10.1016/j.aim.2020.107334).

For each nonnegative integer m, a finite real constant-coefficient backward-shift operator preserves real-rooted polynomials of degree at most m with mesh at least 1, allowing the zero polynomial as an output, if and only if its image of F_m(x) = x(x-1)...(x-m+1) is admissible under the same convention. Constants are admissible. If every nonzero input must instead have a nonzero admissible output, additionally require degree(T(F_m)) = m. The report proves the algebraic normalization and translation bridge, closure and lower-degree extension, and the nonzero-output convention. The universal convolution theorem is an explicitly credited import, not an independently reproved universal result.

## Reading order and status

- [Original mathematical report](original/freeze/packet/REPORT.md)
- [Full independent audit](independent_audit/public/AUDIT.md)
- [Current acceptance record](PUBLICATION_ACCEPTANCE.json)
- [Original public allowlist](independent_audit/public/PUBLIC_ALLOWLIST.json)

The 13 original author files and 13 audit files are retained byte-for-byte, including both freeze archives. Historical pending-review, publication-performed and queue-mutation flags remain unchanged. The separate current acceptance records the accepted disposition. No correction to the frozen mathematical report was needed. The independent audit explains a harmless omitted scalar normalization in a cited direct proof.

This is AI-assisted, unrefereed mathematical verification and exposition. No novelty, priority, formal-proof certification, independent universal-theorem proof, conventional human peer review, or new discovery is claimed. The 8,829 author and 12,339 independent exact checks (including 35 nontrivial Sturm certificates) are finite diagnostics, not a proof of the universal theorem.

## Reproduction and trust

Use a trusted Python 3 interpreter and a genuinely nonroot account. Obtain the publication manifest and verifier SHA-256 pins separately from the reviewed PR description or another trusted channel. A co-shipped manifest cannot authenticate itself. Before executing either script, authenticate its bytes with a trusted hashing tool against the externally supplied pins; test_publication.py is bound by the authenticated publication manifest.

Run, replacing the placeholders with the external pins:

```
python3 -I -S -B verify_publication.py --manifest-sha256 EXTERNAL_MANIFEST_SHA256
python3 -I -S -B -O verify_publication.py --manifest-sha256 EXTERNAL_MANIFEST_SHA256
python3 -I -S -B -OO verify_publication.py --manifest-sha256 EXTERNAL_MANIFEST_SHA256
python3 -I -S -B test_publication.py --manifest-sha256 EXTERNAL_MANIFEST_SHA256 --verifier-sha256 EXTERNAL_VERIFIER_SHA256
```

The wrapper rejects missing/extra files or directories, symlinks and special files, malformed or duplicate-key JSON, nonfinite numbers including exponent overflow, unsafe/duplicate paths, non-exact-integer schema fields, wrong external pins, modified frozen artifacts and nonidentical archive contents. It authenticates the complete exact inventory before invoking frozen code using isolated normal, -O and -OO child interpreters. Original controls reproduce 99 integrity and 111 semantic rejections plus actual nonroot read-only write-denial probes. Independent diagnostics and the independent nonroot read-only replay must match their preserved receipts, except numeric uid/euid may differ across hosts.

The separate test driver executes the complete wrapper under normal, -O and -OO from an unrelated hostile-import directory, including a relocated read-only packet with actual failed writes; rejection controls test both external authentication and separately reanchored malformed schemas. It verifies unchanged bytes and inventory after execution. It writes results to stdout, never into this packet.

Source documents, source text, dataset contents, private material and coordination records are excluded. Historical public retrieval/inspection metadata is preserved but is not a fresh retrieval. Missing source PDFs and corpora default to NOT_RUN. Hosted CI is evaluated separately after publication; zero checks/runs means NOT_RUN, not PASS. Local replay is not hosted CI.

Draft publication only; no merge, release, DOI issuance or outreach.
