# Source versions, inspection, and reproduction

All fetches were read-only and occurred on 2026-10-17 UTC. The ignored paths
`sources/private/` and `tmp/` were created and ignored before retrieval.
Third-party full bodies, extracted text, source images, HTML and dependency
packages remain under those paths. Public files contain only this reviewer's
proof/code/results, fingerprints, and bibliographic/fetch notes.

| Source | Exact fetched identity | Inspection |
| --- | --- | --- |
| Stubborn Polynomials v1 | arXiv:2602.01191v1; 648190 bytes; SHA256 `c91b217bbe413cb934822be9c5f364c75739b38b7bdf178bbf2b764af6ecd0b9` | Definitions 2.1,6.3; Thm1.2; Section6.1 including Example6.1, Lemma6.2 and full Thm6.4 proof. Visual pp.2,19,20,21. |
| OWR 14/2023 | EMS PDF47007; 734622 bytes; SHA256 `5a9bdc9f9daa12ef35185ceae208c0f2f75e191875827f78b7b6ad0f5cdbf240` | Reznick contribution and exact two target clauses, printed p.780 / physical40 visually. |
| BKR publisher PDF | DOI10.1017/fms.2026.10221; 666704 bytes; SHA256 `f4058ac7b54e498c5b639eb21bf54973b421a9fc7b5ed301b1053e0e594078bb` | Thms5.2,5.3,6.3, mixed proof, classification acknowledgement and retained limit question. Visual pp.22,23; text pp.21-24. |
| Demazure III | Numdam `SSS_1976-1977____A6_0`; 1368115 bytes; SHA256 `795915f97ce143af01fb6c1328a0988b3db5a380a5e7af3c0f13429ed5c5854a` | Almost-general-position definition and equivalent nefness condition, physical7 visually. |
| Demazure IV | Numdam `SSS_1976-1977____A7_0`; 1146080 bytes; SHA256 `3f5ae21bce8d837fdd298bc85da1de68cb194324dfec4821c67c45de3d4f32ca` | Corollary1 after Prop2 on fundamental-cycle containment, physical7 visually. |
| Demazure V | Numdam `SSS_1976-1977____A8_0`; 969013 bytes; SHA256 `b417b7b0418bbadd61f1c9994c730e3284fb729ac394f088279d5ea837b529ff` | Thm2 contraction/canonical-sheaf identities and Cor3 ampleness, physical7-8 visually. |

Each successful fetch has its own small `*_fetch_metadata.json` containing URL,
final URL, status, length, hash and timestamp. The arXiv abstract record was
also read live: v1 submission 2026-02-01 12:30:43 UTC; no journal reference was
displayed. The fixed PDF date is 2026-02-03. Numdam supplies the original
1976-1977 seminar editions; these are not falsely represented as the exact
typeset 1980 Springer volume cited by Stubborn. Their directly inspected
theorem statements match the anticanonical facts being checked.

The fresh BKR PDF is **not byte-identical** to the input metadata's historical
630710-byte / `24de6d87101b210f717e050a82d87e3a29a30b02213cf88899b7872e4b6f490d`
PDF. Both the current publisher HTML and the freshly fetched PDF were inspected
for the needed formulas. No explanation of the binary difference is asserted;
no historical file was silently relabeled as the fresh one. The fresh PDF's
embedded creation and modification dates are in April2026; those metadata alone
do not prove immutability. The old hash is not used as the identity of a newly
inspected BKR body.

The author-hosted Dolgachev `https://dept.math.lsa.umich.edu/~idolga/CAG-2.pdf`
could not be fetched directly (HTTP403). A newer author-site path suggested by
the search result returned HTTP404. Search snippets were not used as theorem
premises. The primary Demazure III/IV/V texts above supplied the needed checks.

Focused discovery queries were about the exact Motzkin threshold and the
Stubborn classification. They located the primary BKR and Stubborn records
but no inspected explicit sentence giving the full limit. This is a bounded
search note, not evidence of nonexistence or a priority premise. No secondary
article was used to support a mathematical conclusion.

## Reproducing the exact checks

The successful run used Python3.14.6 with SymPy1.14.0 and mpmath1.3.0. This
workspace's default Python and bundled Python lacked SymPy, so packages were
installed only under this audit's ignored `tmp/python_packages/`.

From this audit directory, run with any Python having SymPy1.14.0 available:

```sh
python3 check_bridge.py
```

For the isolated installed packages here, run:

```sh
PYTHONPATH="$PWD/tmp/python_packages" python3 check_bridge.py
```

The script writes `CHECK_RESULTS.json` with timestamp and exact-check names.
Its checks use explicit exceptions rather than Python `assert`, so optimization
flags cannot remove them. Full source bodies are not inputs to the checker.

`INPUT_PINS.json` records the verified frozen original proof and appendix
hashes and the supplied head identity. It does not claim a new network fetch
of that PR head. `ARTIFACT_SHA256.json` fingerprints every public audit file
except itself and the separately supplied input-pin file; ignored source and
temporary files are excluded.
