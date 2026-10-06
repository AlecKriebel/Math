# Weighted Yamabe heat-trace monotonicity: partial result

Target: 30001169 / OWR-3389-022 (rank 822), n≥4. **Unresolved after five approaches.** See proof.md for the exact proved scope and gaps. This packet contains only authored analysis/code/results and public-source verification metadata.

## Replay

- Exact checks: `python -I -B certificate.py`
- Complete inventory/hash and result replay: `python -I -B verify.py`
- Optimized replay: `python -I -B -O verify.py`
- Optional floating-point research scan: `OPENBLAS_NUM_THREADS=1 python -B exploratory.py` (NumPy/SciPy required; not a proof)

Run from this directory or pass an absolute script path. The exact verifier needs only the Python standard library. It reads the sibling claim.json using the script path, not a fixed working directory. No bytecode, compiled binaries, symlinks, nested directories, datasets, copied papers, source extracts, or private coordination belong in the package. The verifier rejects them.

The mathematical acceptance claims require review of the arguments and public references, not merely a passing script. The script certifies rational inequalities and the finite cover. It does not formalize elliptic theory, heat asymptotics, geometry, or a full solution. The numerical exploration is expressly uncertified.

## Independent review requests

Check the positive-Laplacian convention, U=W^(n/4) unitary conjugacy, n/2 normalization, and constant-rescaling time change. Re-derive the dimension-four coefficient and differentiated asymptotic. Check the min–max interval method including ordered multiplicities and the sign of the entire omitted tail. Audit the rational exponential enclosures and all 750 time intervals. Check Poisson summation and both cylinder derivative ranges. Confirm the abstract spectral construction is not represented as an admissible W. Treat numerical Galerkin signs as observations only. Do not import any conclusion from the neighboring dimension-three comparison investigation.

The envelope manifest is for accidental/mutation detection; its outer archive SHA-256 must be pinned independently. Normal, optimized, relocation, extra-node, content-tamper, and semantic-claim mutations are recorded separately in the author freeze receipt.
