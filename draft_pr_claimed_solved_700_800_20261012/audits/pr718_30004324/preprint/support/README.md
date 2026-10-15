# Source and verification for the tangent-Seshadri research note

**Paper:** Positive tangent-bundle Seshadri constants characterize projective space.
**Author:** Alec Kriebel, ORCID 0009-0001-9320-500X. **Version:** 1.0, 12 October 2026.

The theorem addresses Fulger–Murayama Conjecture 4.9 and OWR-17296-007
(repository problem 30004324): positivity at one arbitrary closed point on a
smooth integral projective variety over an algebraically closed field of any
characteristic forces projective space. The five-page paper is the governing
mathematical presentation. Its proof imports explicit established theorems;
the numerical-generation principle and earlier special cases are credited.

AI tools were used extensively to develop, check, internally review, and prepare
the result. This is an unrefereed preprint. Internal AI-assisted reviews are not
external human peer review, and the package is not a formal proof certificate.

The archive contains:

- `paper.tex`: standalone manuscript with embedded bibliography.
- `historical_candidate/`: all 49 exact frozen attempt files from PR718 head
  `8edfe0bf37d07814c5503107b9029e506b6046ea`, including original and revised
  ZIPs and the preserved adverse historical integrity finding.
- `audit/`: fresh independent mathematical mechanism reviews, root reproduction
  receipts, finite countercontrols, and the documented priority audit and ledgers.
- `MANIFEST.json` and `verify_bundle.py`: exact support-file inventory and replay.
- `zenodo-metadata.json`: the same metadata object used in the upload kit and deposit.

Historical candidate files retain their original candidate-only/pending wording
byte for byte. Those statements describe their historical stages, not a different
scope or a mathematical objection to the present note. The later paper and authored
reviews document the checked presentation. Final preprint-readiness reviews and
publication receipts are maintained outside this fixed archive in the repository
audit folder, so their recording does not change the reviewed archive bytes.

To reproduce, extract the archive into a clean directory and run:

```sh
python3 verify_bundle.py
```

Python 3.10 or later and a system `patch` command supporting `--batch`, `--fuzz=0`
and `-p1` are required. All Python checks use the standard library. For a quick
inventory check, use `python3 verify_bundle.py --integrity-only`. The complete run
reproduces normal and optimized historical replays, relocated and patched
reconstructions, integrity mutations and finite controls, then the fresh
independent boundary controls. The universal geometric implications must be checked
in the paper and referenced theorems; finite enumeration does not prove them.

Compile `paper.tex` with a standard LaTeX installation supporting the listed AMS,
geometry, microtype and hyperref packages, or run `tectonic paper.tex`. Recompilation
may change PDF timestamps and metadata; exact PDF-byte identity is not a theorem
test. The distributed PDF is separately bound by the upload package inventory.

The priority audit found no earlier full resolution in its bounded 64-query search,
but does not certify first historical priority. It credits standard methods and
records source-access limits. Third-party source PDFs, extracted texts, private
data, credentials, and coordination material are excluded. Citations and retrieval
hashes point to the primary sources without redistributing those source documents.

The deposit's authored paper and supporting materials are licensed CC BY 4.0.
Referenced third-party works retain their own rights.
