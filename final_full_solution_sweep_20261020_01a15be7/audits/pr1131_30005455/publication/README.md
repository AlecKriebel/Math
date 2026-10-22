# A sharp forest bound and an improved whisker bound for finite WARM graphs

Alec Kriebel · ORCID https://orcid.org/0009-0001-9320-500X · Version1.0.0 ·21October2026 · Unrefereed preprint.

For a finite simple undirected loopless graph with positive vertex firing rates, power exponent alpha>1 and arbitrary fixed positive integer initial edge counts, the infinitely reinforced edges almost surely form a forest for alpha>4/3. The known equal-rate unit triangle shows that no smaller strict forest constant works. With equal rates every surviving component is a tree of diameter at most three for alpha>=17/4. The stochastic equality endpoint4/3 and the suggested sharp whisker interval4/3<alpha<17/4 are unresolved here. No loops, infinite-graph theorem or noninteger initialization extension is asserted.

The seven-page paper in main.tex and output/pdf/finite-warm-thresholds.pdf contains the complete analytic proof and every rational comparison. A weighted odd-cycle Hessian inequality treats arbitrary equilibria, unequal rates, chords and attachments. The separate equal-rate matching proof does not depend on that cycle theorem. A finite-path conditioning lemma supplies the positive-integer almost-sure extension, without reversing a stable-attainment implication.

## Prior work and target reconciliation

Kleptsyn's OWR12/2023 printed655 requests improvements of the finite forest bound2 and equal-rate whisker bound25. The following suggestion of sharpness at4/3 is a stronger target. The historical eight-file source calls the result partial because it required that sharper whisker interval. Original bytes remain in original/; audit/SCOPE_AND_CHANGES.md explicitly supersedes that eligibility interpretation and identifies the initialization and attribution additions.

The published HHK2023 finite convergence and support-identification theorems are imported at their hypotheses. The even-cycle method, VHHKR2016 uniform odd-cycle threshold and triangle obstruction, HK2017 least-weight/champion mechanism and earlier unequal-rate obstruction are credited. The HK2017 displayed proof already implies a weaker whisker bound at24; the paper gives a conservative >24 consequence with an exact rational exponential certificate. The claimed contribution is the stronger17/4 bound and arbitrary-rate forest result, not the first possible numerical improvement of25.

Two independent bounded priority approaches recovered no earlier theorem or full positive implication giving those substantive universal bounds. Their sources, source interfaces, versions, positive overlaps, access failures and search limits are recorded in audit/priority01 and audit/priority02. This does not certify exhaustive novelty, worldwide firstness, first public availability, causal independence or current global openness. Metadata and creation dates do not establish historical public visibility. The original source's graph convention is made explicit rather than broadened silently.

## Contents and integrity

- main.tex and output/pdf/finite-warm-thresholds.pdf: the operative paper and frozen PDF.
- original/: all eight unchanged actual submitted artifacts at head bacae693a1f2a33c89565b0bd716620885831289.
- audit/forest and audit/whisker: distinct mathematical reconstructions and newly authored exact finite controls.
- audit/priority01 and audit/priority02: independent priority/equivalence challenges, known-method credits and exact old-bound bridge.
- verification/: portable runner, three-mode control plan, complete expected JSON outputs and pure-mathematics forest wrapper.
- PROVENANCE.json and SOURCE_MANIFEST.json: exact original identity, scope/edition provenance and a closed archive inventory; the manifest hashes every other member.
- zenodo-metadata.json and zenodo-deposit.json: native metadata and two-file upload manifest; the separate upload kit has the same metadata and flat portable paths.

The audit manifests retain their original authored private-source hash references and historical paths. Those are custody observations, not claims that private bodies are included. The forest report's full custody entrypoint and priority02 verifier require the identified private primary captures. They are preserved for inspection but are not advertised as self-contained offline custody replays from this distribution. Third-party full bodies, extracted text, images, raw API/ledger/account responses and private operational receipts are excluded. Source identities and retrieval/access metadata are original authored records rather than copied source text. Original authored material is CC BY4.0; cited works retain their rights.

## Reproduce the finite controls

Python3.10 or later and the standard library suffice. In a new extracted copy run:

    python3 -B verification/run_checks.py

Optionally add --manifest-sha256 HASH using an independently obtained SOURCE_MANIFEST.json digest. The default verifies the closed source inventory, makes a temporary read-only mirror, and runs three suites in ordinary, -O and -OO modes. No network or primary-source download is used and no release input is modified.

The forest suite calls only the new verifier's finite_controls function, without its private-custody main. It recomputes weighted equilibrium/Jacobian/Hessian relations, cycle directions, chords and attachments, critical and boundary controls, and an exact positive-integer reachability example; six false alternatives are rejected in every mode. The whisker suite independently checks all five exact intervals, margins, fractional-power caps, polynomial identities, quadratic-field identity and exponential-tail certificate, rejecting seven mathematical/scope corruptions in every mode. The third suite recomputes the older >24 proof consequence and checks the priority report's bounded scope statements. All complete JSON values and recursive types are compared exactly; no mathematical or process fields are dropped or normalized. EXPECTED.json preserves outputs actually obtained in the root's independent copied replays.

These are finite arithmetic and integrity controls. Universal mathematical deductions are in the paper and written audits; imported stochastic foundations and absence of earlier literature are not certified by software or hashes. No exploratory numerical tree search is a proof dependency.

## Rebuild

In a disposable extracted copy run:

    python3 -B build_package.py

It verifies the package and controls, then reconstructs the closed source archive and five-member upload kit using fixed timestamps and sorted paths. The frozen PDF is an input: the builder does not silently recompile TeX. Same Python/zlib runtime gives identical ZIP bytes; different compression runtimes may preserve all members while changing ZIP bytes. To revise the paper, deliberately compile, render and inspect every page, then rebuild and independently review the changed release. The repository's top-level Zenodo tool stages, verifies and publishes separately; this builder and runner perform no publication.

AI tools were extensively involved in mathematical research, proof development, symbolic and computational verification, adversarial auditing, literature investigation and manuscript preparation. This paper and supporting materials are unrefereed and have not undergone formal independent human peer review, journal acceptance or proof-assistant certification. Internal independent AI reviews do not supply those certifications. Whole-package review decisions and later operational publication receipts are kept outside the fixed scientific archive to avoid self-referential hashes.
