# KP-4.69: audited pseudo-isotopy partial results

**Problem 2945, queue rank 1047: unsolved, five of five mathematical approaches completed.**

The unchanged candidate and independent audit accept a zero Casson–Sullivan representative for the named Friedman–Witt–Kwasik–Schultz endpoint and a smooth extension of its prescribed boundary map after finitely many interior S²×S² stabilizations. This does **not** give a smooth pseudo-isotopy of the original, unstabilized cylinder. The proof uses identified imported geometric theorems; no novelty, human peer review, or global openness certification is claimed.

## Read the result

- [Full mathematical report](original/public/MATHEMATICAL_REPORT.md)
- [Full independent mathematical audit](audit/AUDIT.md)
- [Publication acceptance and limits](ACCEPTANCE.md)
- [Five-approach ledger](original/public/APPROACH_LEDGER.json)
- [Independent audit disposition](audit/AUDIT_RESULT.json)

The five approaches concern the endpoint derivative, split-filling extension, the explicit finite cover, marked mapping tori, and relative Casson–Sullivan cancellation. The degree-144 cover is a connected sum of 121 copies of S²×S¹; the lifted twist is isotopic to identity **non-equivariantly**. The endpoint problem downstairs remains unresolved.

## Source boundary

The original KS96 full text was not obtained. Its topological pseudo-isotopy input is accepted via the specifically identified K3 and Galvin-thesis statements. Galvin's relative realization conclusion is obtained by tracing the boundary markings in Proposition 4.10, not by silently replacing a closed-manifold theorem with a compact-relative one. The audit explains the source's notation issues, the supported excision map, the composition pullback, and preservation of boundary values during stabilization. No good-group assumption on the free product is used.

All source and corpus verification records in `original/` and `audit/` are historical, immutable evidence. A fresh source-free replay reports fresh PDF/source verification and fresh corpus verification as **NOT_RUN**. It does not download papers or datasets. The older author-site Galvin PDF is recorded separately and is superseded for theorem numbering.

## Immutable layout

- `original/CANDIDATE_FREEZE.json` and the eight files in `original/public/` are unchanged.
- The twelve files in `audit/` are unchanged, including the copied original freeze.
- This directory adds an acceptance report, this guide, a strict verifier, a mutation driver, a manifest, and an externally anchored bootstrap.
- No corrected candidate or proof patch is required.

Only authored mathematics, audit work, reproducibility code, and permitted verification metadata are included. Source papers/text/images, dataset contents, and private coordination files are excluded.

## Authenticate before executing

Obtain the **bootstrap SHA-256 from an independently trusted release/PR record**, not a hash freshly computed from the same untrusted download. Authenticate `BOOTSTRAP.py` against that external value before executing it. The bootstrap pins the publication manifest and verifier bytes; the verifier additionally hard-pins all 21 accepted historical files and rejects every unexpected file or directory, symlink, special file, duplicate JSON key, nonfinite number, unsafe path, and inexact integer type.

With Python 3 and an ordinary Unix account whose real and effective UID are both 1000, run:

```sh
python -I -S -B /trusted/path/BOOTSTRAP.py /path/to/packet
python -I -S -B -O /trusted/path/BOOTSTRAP.py /path/to/packet
python -I -S -B -OO /trusted/path/BOOTSTRAP.py /path/to/packet
```

The trusted bootstrap must be byte-identical to the packet's bootstrap. Run the authenticated mutation driver in each optimization mode as well:

```sh
python -I -S -B mutation_tests.py --root /path/to/packet --bootstrap-sha256 EXTERNALLY_TRUSTED_SHA256
```

Add `-O` or `-OO` before the script name for the other modes. The mutation driver must itself come from the authenticated packet. It tests integrity, exact schemas, external anchoring, relocation, hostile import environments, and actual read-only write denial. It never mutates the supplied packet.

The native harness prepares mutations using a separate authenticated disposable writable staging copy, then makes all executed specimens read-only and proves write denial. The supplied packet remains read-only; see the acceptance report.

The replay executes the unchanged candidate, independent arithmetic, audit verifier, and full 36-process native audit with its 30 semantic negative controls. Finite arithmetic and byte integrity do not certify smooth or topological existence. See the acceptance report for the precise normalization of historical runtime metadata.
