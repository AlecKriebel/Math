# Support-slit verification package

Paper: **Nonmonotone Argument and Radial Angle of a Support Slit**, Alec Kriebel (ORCID 0009-0001-9320-500X), version 1.0, 14 October 2026. Unrefereed, extensively AI-assisted, no human peer review or formal proof certification. CC BY 4.0.

Every global maximizer of the real part of a2+i·10^-24(a4−3a3) in the full normalized schlicht class has an actual omitted slit with nonmonotone continuous argument, signed outward radial angle, and ordinary unsigned radial angle. Compactness supplies genuine extremizers; the area theorem bounds their actual tips; a controlled Schiffer natural coordinate identifies a subarc of each actual slit. Classical support-point and area-theorem results are explicit inputs. No converse sufficiency claim for arbitrary trajectories, numerical extremal solver, unique maximizing function, or continuity of slit tips is assumed.

The original question is Hayman–Lingham, Problem 6.72, printed p.143. Classical support-slit geometry, Schiffer methods and the Friedland–Schiffer coefficient/control framework are credited. Complete comparisons include Hibschweiler (1996), Friedland–Schiffer (1977), Zemyan (2003, 2005, 2007), Duren–Leung–Schiffer (1983), Zhang–Ma (1991), Brickman (1984), and Goh (1992, 1994). Goh's two-functional hypotheses require a second independent extremal or critical equation, which is absent here. No earlier exact-target negative answer was verified in the inspected corpus.

The later Duren commentary and Hibschweiler (1995) could not be inspected. **Priority therefore cannot be fully cleared.** The human expressly accepts publication with these disclosed limitations. No historical-first claim or assertion of continued open status in 2026 is made. CURRENT_PRIORITY_ASSESSMENT.json records the precise scope and additional unread leads. Historical sealed reports retain their earlier holds; the current assessment and USER_PRIORITY_LIMIT_AUTHORIZATION_20261014.json explain the changed source coverage and human acceptance policy. Those historical reports are not final acceptance of this revised package.

## Offline checks

Once frozen, extract the ZIP and use Python 3.10 or later without optimization. Install the single pinned dependency from a package index or a separately prepared local wheel cache, then run the checks:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python run_all.py
```

The runner itself needs no network access after installation. mpmath 1.4.1 supplies directed interval arithmetic for the independently derived Zemyan (2003) comparison; the main theorem's rational checks use the Python standard library. The runner checks the strict outer inventory and every registered inner seal, then replays all 17 jobs listed in JOBS.json in scratch copies. It compares all mathematical JSON output; only the source-bridge script's generated execution timestamp is ignored. The Hibschweiler (1996) checker prints a summary and writes a full record: both are compared with their respective frozen records. The supplied-primary wrapper compares the complete records from five new source-comparison and adjudication families, including the exact rational controls and directed interval controls. Repeated runs leave the sealed payloads unchanged. Python cache and a virtual environment are not archived payloads. Hashes establish consistency, not authenticity, correctness or novelty.

The universal analytic argument is in support_slit.tex and the independent analytic and quantitative derivations in reviews/. Finite rational checks supplement that argument. Original authored input is preserved under its entire original repository path so independent checks resolve it correctly. Source-scope and priority evidence are authored audit records. Third-party full texts are omitted.

Optional retrieval, sealing and source-content inspection scripts are provenance helpers, not offline verification jobs unless explicitly listed in JOBS.json. Retrieval needs network access; some PDF inspection helpers need pypdf. The Friedland–Schiffer (1977) custody helper additionally rechecks its separately cached source PDF. The Zemyan source-custody helpers also refer to external PDFs and the earlier compared manuscript. Those PDFs are not archived. The two historical manuscripts are preserved byte for byte as root_reproduction/PRIMARY_AUDIT_BASELINE.tex and root_reproduction/PRE_GOH_MANUSCRIPT.tex. Their mathematical bodies, delimited by the first and attribution section headings, are byte-identical to the current manuscript; the date, attribution, bibliography and footer changed. MANUSCRIPT_GOH_REVISION.json records this mapping. The two new Goh checkers are portable standard-library controls; their custody records bind the exact historical pre-Goh manuscript. The historical independent input seals are preserved rather than rewritten to match the revision. The offline runner verifies the authored seals and replays the mathematical components without consulting those external paths. Run optional custody helpers only on a separate copy with their recorded historical inputs. Such helpers are not a promise of portable source retrieval or priority clearance. Cached third-party papers and account data are not part of this package.

## PDF rebuild

Rebuild outside the extracted directory to preserve its strict inventory:

```sh
mkdir -p ../pdf-rebuild
SOURCE_DATE_EPOCH=1791892800 tectonic --outdir ../pdf-rebuild support_slit.tex
```

BUILD.json records the compiler and PDF digest; PDF_QA.json records visual inspection. Different compilers or fonts may change PDF bytes. metadata.json is the supplied deposit configuration; its file paths refer to the deposit directory containing the separate PDF and ZIP.

Fresh complete-package adversarial reports and eventual publication receipts will be recorded in the repository audit at https://github.com/AlecKriebel/Math/tree/main/draft_pr_claimed_solved_500_600_20261012/audits/pr563_2306072. Fresh reviews are outside the ZIP to avoid circular artifact/report digests. At this archive freeze, production publication, tracker append and merge remain subsequent actions; repository receipts record their eventual outcome.
