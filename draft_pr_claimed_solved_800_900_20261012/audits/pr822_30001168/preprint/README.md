# A finite counterexample to the weighted Yamabe heat trace comparison

Alec Kriebel, independent researcher. ORCID: https://orcid.org/0009-0001-9320-500X.
Version 1.0.0, October 13, 2026. Problem 30001168 / OWR-3389-021; original PR #822 at c9fd5a0462d1fa98f21aa7037f7a5e061fbbee9c, exactly claimed_solved, original proof effort 1/5.

The four-page note gives a full negative answer to the assertion over all n >= 3 in Morpurgo's Conjecture 1, OWR 6/2009, printed pp. 421-422. One specified smooth positive weight on S^3 has conformal volume 2 pi^2 and scaled heat trace > 13/20 at t*=4(2 pi^2/V_L)^(2/3), L=10000. The round maximum is < 321/500; both maxima are attained. This does not decide the comparison restricted to n >= 4 or adjacent problem 30001169.

The qualitative result is an assembled classical corollary: cylindrical conformal geometry of Ammann--Jammes and its earlier ancestry, a chosen fixed rescaled cap, Dirichlet min--max, and an elementary round trace bound. The contribution recorded here is the explicit finite quantitative application to the historical question. No new geometric or spectral mechanism, historical priority, worldwide firstness or current-openness certificate is claimed. See CURRENT_PRIORITY.md and the complete bounded source audit.

## Files and reproduction

The standalone deposit files are the note PDF and verification.zip. Extract the latter into a new directory. It contains:
- note.tex, note.pdf, metadata.json, this README and CURRENT_PRIORITY.md;
- source/: all 42 original files unchanged, including three frozen ZIPs containing 32 exact corresponding members;
- geometry_audit_01/ and trace_audit_01/: new independent reconstructions, reports, checks and receipts;
- priority_audit_01/: authored source/search ledgers, historical, broader-theorem and adversarial lanes, deduction and disposition; downloaded primary works are excluded;
- root_evidence/: exact-target criteria, frozen-source inventory and independent reproduction/priority receipts;
- package_index.json and verify_package.py: closed file inventory and the portable check entry point.

Obtain the trusted SHA-256 of package_index.json from the independently retrieved Git release metadata or reviewed package seal. The archived index binds every other member; its authenticity must be established separately. Run in the intact extracted directory:
    python3 -I -B verify_package.py TRUSTED_INDEX_SHA256 --full
Repeat using:
    python3 -I -B -O verify_package.py TRUSTED_INDEX_SHA256 --full

Only the Python standard library is needed, with no network, third-party package or Git requirement. The check is relocatable, including paths with spaces, and verifies the closed inventory before and after execution. It replays the original publication and 34 audit controls, the 20 original outer controls, the new exact six-interval trace bound plus the small-time region, and independent geometry arithmetic. It checks all seven rational upper enclosures printed in the note. The writing geometry checker and fresh semantic-control harness run only in disposable copies. Fresh controls include 16 expected semantic rejections and two expected acceptances of deliberately wrong analytic prose after rehashing: that boundary demonstrates why arithmetic and integrity cannot certify the analytic proof.

Analytic obligations (smooth cap extension, covariance, form domains, min--max, Gaussian/Poisson identities and heat asymptotics) were checked by independent adversarial mathematical AI reviews. They are not proved by these programs. The preserved scripts and ledgers outside the documented entry point are dated audit tools: some reference the original working checkout or private primary-source corpus. In particular priority_audit_01/verify_audit_receipt.py is an audit-time source-receipt checker, not a portable priority theorem or completeness test. Source locators, byte hashes, inspected passages and retrieval limits are provided for independent source inspection.

build_verification.py, retained in the Git preprint folder rather than inside this archive, deterministically assembles the same archive from the sealed audit inputs. Do not regenerate the PDF while reproducing archive identity; PDF compilation timestamps can change its bytes. Tectonic and the built-in LaTeX editor independently compiled note.tex. Final package review receipts on main bind the finished PDF, source, metadata, index, ZIP and outer repository assembly.

## Status, tools and reuse

OpenAI tools were used extensively in development, solving, drafting, coding and adversarial checking. This is unrefereed work: no completed external human peer review or formal proof-assistant verification is claimed. Mathematical acceptance and historical priority are separate. The original 1/5 proof-effort count is preserved; no additional central proof search was needed.

The authored note and supporting authored materials are released under CC BY 4.0: https://creativecommons.org/licenses/by/4.0/. Dated source citations and imported standard results retain their attribution. Downloaded primary publications and private credentials/state are not distributed.
