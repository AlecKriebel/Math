# Reproduction

Extract the ZIP, then run from its top-level folder with Python 3.9 or later:

```
python3 -B tools/reproduce.py .
python3 -O -B tools/reproduce.py .
```

Only the Python standard library is required. The wrapper makes no network requests and writes no bundle files. It checks every manifest record's exact integer types, canonical relative path, byte length and SHA256, rejects missing or extra files and symlinks, and checks the complete inventory before running programs. The manifest itself is excluded from its own hash entries. It is not an authenticated signature; compare the externally supplied archive/PDF hashes where available.

The eleven originals are unchanged. `original/verify_public_packet.py` verifies ten historical manifested payloads and invokes the 4,240-identity script. Both historical scripts use assertions; optimized execution removes their guards. The new wrapper closes that limitation by removing PYTHONOPTIMIZE from the child environment, starting a fresh interpreter with `-E -B`, without `-O`, checking that `__debug__` is true, and only then running the original verifier. Removing the environment variable also protects the density-check subprocess started by that original verifier. Thus both original programs' assertions execute even if the outer new wrapper is optimized or PYTHONOPTIMIZE was set in the environment.

Next, the independently authored explicit-guard scripts in the measure/ordinal and continuity/core families run in normal and optimized modes. Their complete JSON outputs must be byte-identical between modes, agree with the sealed expected records, and satisfy separately specified exact integer counts. The measure family has 10,128 bounded exact checks. The continuity/core family has finite partition/support controls, 7,203 adjoint identities and the stated finite properness-bound checks. Their reports describe meaningful deliberate failures and exact mathematical limits. These computations do not prove the infinite measure theory or full theorem.

To repeat the new manifest negative controls, provide a writable directory **outside the extracted bundle**, so the exact inventory remains unchanged:

```
python3 -B tools/test_integrity_controls.py /absolute/path/to/disposable-directory
python3 -O -B tools/test_integrity_controls.py /absolute/path/to/disposable-directory
```

They check valid nonempty and zero-byte files and reject mutations of bytes, inventory, symlinks, exact schema/length types (including bool versus int), duplicate keys/paths, noncanonical and escaping paths, and malformed digests. Temporary fixture trees are removed automatically.

The paper is standalone TeX. Build `manuscript/main.tex` using a TeX engine supporting the listed standard packages; the retained preparation used official Tectonic 0.17.0. The published PDF is separately hashed because build timestamps may make byte-for-byte PDF regeneration differ. Actual compilation, PDF text/page checks and full-page visual QA are recorded in the preparation receipts. A successful compilation or finite replay is not mathematical proof certification.
