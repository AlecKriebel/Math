# Support-slit verification package — preparation draft

Paper: **Nonmonotone Argument and Radial Angle of a Support Slit**, Alec Kriebel (ORCID 0009-0001-9320-500X), planned version 1.0, 13 October 2026. Unrefereed, extensively AI-assisted, no human peer review or formal proof certification. CC BY 4.0.

Every global maximizer of the real part of a2+i·10^-24(a4−3a3) in the full normalized schlicht class has an actual omitted slit with nonmonotone continuous argument, signed outward radial angle, and ordinary unsigned radial angle. Compactness supplies genuine extremizers; the area theorem bounds their actual tips; a controlled Schiffer natural coordinate identifies a subarc of each actual slit. Classical support-point and area-theorem results are explicit inputs. No converse sufficiency claim for arbitrary trajectories, numerical extremal solver, unique maximizing function, or continuity of slit tips is assumed.

The original question is Hayman–Lingham, Problem 6.72, printed p.143. The known support-slit geometry, Schiffer methods and Friedland–Schiffer coefficient/control framework are credited. CURRENT_PRIORITY_ASSESSMENT.json records the current publication hold. New complete Hibschweiler1996 and Friedland–Schiffer1977 comparisons close their earlier access/scope gaps; the older sealed reviews retain their historical unread status. Other specific full texts remain unread. No historical-first claim or assertion of continued open status in 2026 is made. This preparation draft is not an accepted publication package.

## Offline checks

Once frozen, extract the ZIP and use Python 3.10 or later without optimization:

```sh
python3 run_all.py
```

The offline runner needs no third-party Python packages or network access. It checks the strict outer inventory and every registered inner seal, then replays the jobs listed in JOBS.json in scratch copies. It compares all mathematical JSON output; only the source-bridge script's generated execution timestamp is ignored. The Hibschweiler1996 checker prints a summary and writes a full record: both are compared with their respective frozen records. Repeated runs leave the sealed payloads unchanged. Python cache and a virtual environment are not archived payloads. Hashes establish consistency, not authenticity, correctness or novelty.

The universal analytic argument is in support_slit.tex and the independent analytic and quantitative derivations in reviews/. Finite rational checks supplement that argument. Original authored input is preserved under its entire original repository path so independent checks resolve it correctly. Source-scope and priority evidence are authored audit records. Third-party full texts are omitted.

Optional retrieval, sealing and source-content inspection scripts are provenance helpers, not offline verification jobs unless explicitly listed in JOBS.json. Retrieval needs network access; some PDF inspection helpers need pypdf. In particular, reviews/priority05_friedland1977/verify_manifest.py additionally rechecks the separately cached original PDF at its recorded local path. That original is not archived, so this helper is optional and is not run by the offline runner. The runner itself verifies all ten of that family's authored sealed entries, and its pure algebra checker is an offline job. Run optional helpers on a separate copy with the required source files. Cached third-party papers and account data are not part of this package.

## PDF rebuild

Rebuild outside the extracted directory to preserve its strict inventory:

```sh
mkdir -p ../pdf-rebuild
SOURCE_DATE_EPOCH=1791892800 tectonic --outdir ../pdf-rebuild support_slit.tex
```

BUILD.json records the compiler and PDF digest; PDF_QA.json records visual inspection. Different compilers or fonts may change PDF bytes. metadata.json is the supplied deposit configuration; its file paths refer to the deposit directory containing the separate PDF and ZIP.

Fresh complete-package adversarial reports and eventual publication receipts will be recorded in the repository audit at https://github.com/AlecKriebel/Math/tree/main/draft_pr_claimed_solved_500_600_20261012/audits/pr563_2306072. Fresh reviews are outside the ZIP to avoid circular artifact/report digests. No DOI, tracker append or merge has been performed for this draft.
