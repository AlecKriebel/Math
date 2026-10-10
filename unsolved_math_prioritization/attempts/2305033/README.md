# Function Theory 5.33: prior-literature attribution

Rank 680; upstream ID 2305033; AMR-022-5033.

**Disposition: `already_solved`; campaign ledger: `1/5`. No new solution is claimed.**

For the holomorphic universal covering projection from the disk onto the
complement of a regular triangular lattice, Hayman and Lingham's
[Problem/Update 5.33](https://arxiv.org/pdf/1809.07200v2#page=98)
reports coefficient decay and the stronger fixed-map estimate
`a_n = O((log n)^(-1/2))`. It attributes the result to W. K. Hayman,
S. J. Patterson and Ch. Pommerenke, *On the coefficients of certain
automorphic functions*, Math. Proc. Cambridge Philos. Soc. 82(3) (1977),
357–367, [DOI 10.1017/S0305004100054013](https://doi.org/10.1017/S0305004100054013).

The independent audit verifies this attribution and the exact reported scope.
**The original 1977 full proof was not obtained or inspected.** The historical
estimate is imported, not reconstructed or independently certified by this
package. The result is not extended to arbitrary holomorphic subordinates or
to every analytic function merely omitting the lattice.

## Files and interpretation

- [author/README.md](author/README.md) and all eight files under `author/`
  preserve the exact frozen author packet. Its historical audit-pending and
  zero-new-proof-search statements describe its preparation stage.
- [audit/INDEPENDENT_AUDIT.md](audit/INDEPENDENT_AUDIT.md), with all five
  audit files, preserves the complete subsequent independent review.
- [LEDGER_GUIDE.md](LEDGER_GUIDE.md) explains why zero author-local proof-search
  turns and one substantive campaign literature response are compatible.
- [BINDING.json](BINDING.json) and `PUBLICATION_MANIFEST.json` bind the frozen
  identities, allowed inventory, public queue observation and disposition.
- `verify_publication.py` provides strict, portable integrity checks, finite
  replay and rejection tests. This is a publication check, not another
  mathematical proof audit.

## Reproduce

Python 3.10+ and the standard library suffice. From this directory run:

```sh
python3 -B verify_publication.py --replay --selftest
python3 -O -B verify_publication.py --replay --selftest
```

The wrapper checks the complete inventory and immutable author/audit manifests,
rejects symlinks, unsafe paths, duplicate JSON keys and duplicate manifest paths,
then runs the frozen author checks with assertions enabled in a fresh temporary
directory. The 162 finite exact checks comprise 72 affine/rotation evaluations,
24 translation controls, 44 finite lacunary Bloch controls, and 22 sparse
coefficient controls. They do not establish the infinite historical theorem;
the elementary infinite arguments are separately written and audited.

## Remaining limits

The raw upstream statement/report corpus was unavailable, its imported hashes
were not independently reproduced, and the upstream AI report was uninspected.
No prior attempt was found in the documented bounded repository searches;
the searches are not an exhaustive historical guarantee. The source PDF hash
describes an existing local copy; it is not fresh remote-byte provenance.
Hayman–Lingham arXiv v2 is an authors' draft, not claimed to be a final edition.

Only authored analysis, code, audits and permitted public verification metadata
are included. Source documents, extracted source text, source screenshots,
dataset contents and private coordination records are excluded.
