# NP-completeness of the initial odd-ear prefix

Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X.
Preprint 1.0.0, 22 October 2026.

The paper proves the full variable-threshold decision theorem for initial
consecutive odd OPEN ears, counting the first circuit and one-edge ears.
Hardness already holds on simple 2-vertex-connected cones over connected
bipartite bases. The proof is a polynomial explicit Set Cover reduction;
arbitrary partial blocks are handled by an exact loss inequality.
Fixed YES and NO outputs are triangle / threshold 1 and triangle / threshold 2.
No fixed-threshold, total-odd-ear, closed-ear or P!=NP theorem is asserted.

Read manuscript/main.tex or paper.pdf. The main proof imports the classical
Lovasz odd-open-ear characterization of 2-connected factor-critical graphs
and standard Set Cover NP-completeness. Everything specific to the new
reduction, including induced completion, cone equivalence, forward matching,
arbitrary partial-block converse, size bounds and NP certificates, is proved
in the paper. DEPENDENCIES.md gives precise source versions/read limits;
PRIORITY.md records the bounded priority challenge.

## Reproduction

Python >= 3.10, standard library only:

    python3 -I -S -B exact_checks.py > rerun.json
    cmp rerun.json CHECK_RESULTS.json
    python3 -I -S -B -O exact_checks.py > rerun_O.json
    cmp rerun_O.json CHECK_RESULTS.json
    python3 -I -S -B -OO exact_checks.py > rerun_OO.json
    cmp rerun_OO.json CHECK_RESULTS.json

The saved output has10 direct complete-ear/cone/factor-critical comparisons;
70 covered set systems and 194 thresholds, including 180 explicit full-actual-k
forward matching witnesses;142 preprocessing cases;9454 exact block omission
identities; and 7 falsifiable controls. The H3 boundary from Benchetrit--Sebo
has maximum initial prefix 2 versus maximum total-odd count 4 in the direct
search. Dropping one-edge ears changes a square-cone result 4 to 2; omitting
the first circuit changes it 4 to 3. The balanced nonmatchable control prevents
using bipartition equality as a replacement for a perfect matching.

These are finite debugging tests, not formal verification or a substitute
for any universal proof. The full-size checks construct YES witnesses;
they do not exhaust arbitrary subsets of the full hardness graphs. A
smaller k=2 example does exhaust its actual subsets. The k=3 connectivity
gap 27 versus 25 has an explicit 25-edge connected matching witness and the
written universal upper bound; the checker does not claim full k=3 subset
enumeration. Earlier audit code is not imported or executed.

To rebuild the EXACT six-file release in a NEW directory:

    python3 -I -S -B build_release.py --output /absolute/new/release

The builder uses the frozen paper.pdf and verifies every pinned source
member. It creates two scientific files (PDF and source/verification ZIP),
Zenodo metadata and deposit manifest, a five-member upload kit, and upload
instructions. It does not recompile TeX, allocate a DOI, access credentials,
contact a service or modify an existing output. To typeset separately, use
a standard LaTeX installation with geometry,amsmath,amssymb,amsthm,fontenc,
hyperref (e.g. tectonic --only-cached --outdir NEW_DIR manuscript/main.tex).
A new typesetting need not have the frozen PDF's identical bytes.

No third-party paper body, private account/sheet capture or publication
driver is included in the public source archive. Existing cited DOIs
identify sources, not publications of this reduction.

## AI and review status

AI tools were extensively involved in mathematical research, proof
development/reconstruction, computational verification, literature
investigation, manuscript preparation, editing and adversarial auditing.
Alec Kriebel is the named human author. This is a preprint without formal
independent human peer review, journal acceptance or proof-assistant
certification. Internal AI review does not supply those certifications.
Authored prose is CC BY 4.0; authored code is MIT licensed.

