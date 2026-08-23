# Audit environment

- Audit start: 2026-08-22T21:59:04-07:00
- Host OS: macOS 26.5.2 (build 25F84), Darwin 25.5.0, arm64
- Shell: GNU Bash 3.2.57 available; command runner login shell is zsh
- Default `python` selected by the advertised wrapper: CPython 3.9.6 at `/Library/Developer/CommandLineTools/usr/bin/python` (invoked through `/usr/local/bin/python`), assertions enabled
- Separately installed `python3`: CPython 3.14.6 at `/opt/homebrew/bin/python3`; it has none of the manuscript's required scientific packages
- Bundled artifact-review Python: CPython 3.12.13; it has `numpy`, `pypdf`, `pdfplumber`, and `reportlab`, but lacks `matplotlib`, `pytest`, `scipy`, and `sympy`, so it cannot run the submitted replay by itself
- Git: 2.38.2
- Package release tag declared by provenance: `maximally-collective-stable-turing-v1.0.7`
- Tagged commit declared by provenance: `963594192a494421de6c5984c24d4a41e682da3f`
- Exact-version DOI declared by provenance: `10.5281/zenodo.22062080`

## Python packages visible to the advertised default `python`

| Package | Actual version/status | Packet minimum | Preflight consequence |
|---|---:|---:|---|
| matplotlib | 3.7.1 | 3.7 | satisfies |
| numpy | 1.24.3 | 1.24 | satisfies |
| pandas | 2.3.3 | 2.0 | satisfies |
| pypdf | **unavailable** | 6.0 | complete replay cannot pass dependency import |
| pytest | 8.4.2 | 8.0 | satisfies |
| scipy | 1.10.1 | 1.10 | satisfies |
| sympy | 1.14.0 | 1.12 | satisfies |

The repository supplies only lower-bound specifiers (`>=`) in `requirements.txt`; it has no lockfile and no hashes. The author-provenance environment records versions matching the available scientific stack except that `pypdf==6.10.0` is absent from the default interpreter.

## External commands

| Tool | Actual version/path/status | Consequence |
|---|---|---|
| `bash` | 3.2.57 at `/bin/bash` | available |
| `biber` | 2.22 at `/opt/homebrew/bin/biber` | available; author provenance used 2.17 |
| `pdflatex` | **not installed/on the base-host PATH** | the first literal wrapper invocation stopped at preflight; later disposable TinyTeX runs covered the stated document route |
| `tectonic` | 0.16.9 at `/opt/homebrew/bin/tectonic` | available but is not invoked by the supplied replay and is not a drop-in proof that the `pdflatex`/Biber route works |
| `pdffonts`, `pdftoppm`, `pdfinfo` | Poppler 26.08.0 | available |
| `sha256sum` | Darwin 1.0 at `/sbin/sha256sum` | available and accepted both supplied manifests |
| `awk` | 20200816 | available |
| BSD `grep`, `find`, `sort`, `xargs`, `tail`, `cp`, `cmp`, `mktemp` | system versions | available; GNU version pinning is absent |

No runtime network access is used by the verifier, replay, generators, tests, simulations, or document build. Network access would be needed only to install the missing dependencies or independently retrieve cited literature/release records. The source scan found no private user/home path. The only absolute-path sentinel in executable source is the portability audit that deliberately rejects `/mnt/data/` references.

## Disposable document environments used for route coverage

No system TeX or Python installation was changed. The following official
TinyTeX bundles and a temporary `pypdf==6.10.0` target under `/tmp` were put on
`PATH`/`PYTHONPATH` only for the recorded commands:

| Environment | Versions | Wrapper result |
|---|---|---|
| TinyTeX 2026.08 | pdfTeX 1.40.29; host Biber 2.22 | After installing the manuscript's required LaTeX packages into the disposable bundle, all repository build stages ran. The final PDF audit failed on a 19-page supplement and two version-sensitive extraction/layout probes. |
| Full TinyTeX 2022.08 | pdfTeX 1.40.24; Biber 2.18 | Both 18-page documents and all figures built. The final PDF audit failed only on the Latin-`u` phrase probe. |
| Full TinyTeX 2022.04 | pdfTeX 1.40.24; Biber 2.17, matching the recorded Biber generation | Both 18-page documents and all figures built. The final PDF audit again failed only on the Latin-`u` phrase probe. |

Under `pypdf==6.10.0`, both 2022 builds extract the visibly correct source
phrase `with $u$ the Latin letter` as `withu the Latin letter`. A disposable
change from literal membership to
`re.search(r"with\s*u\s+the\s+Latin\s+letter", supplement, re.I)` made that
audit pass. The submitted `audit_pdfs.py` was not changed in either packet copy.
The unmodified wrapper therefore remains exit 1/no completion marker, but
document generation itself is covered.

The 2022.04 regenerated PDFs use `pdfTeX-1.40.24`; the archived PDFs identify
`xdvipdfmx (0.1)` as producer. They are semantically comparable, not expected
to be byte-identical products of the same engine.
