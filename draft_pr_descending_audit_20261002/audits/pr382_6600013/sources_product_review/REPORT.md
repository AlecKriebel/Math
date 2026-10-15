# PR382 source/product family audit report

Verdict: PASS for the source normalization and the scoped mathematical results in TURN_1 and TURN_2. No mandatory mathematical repair was found in this assigned family. These results do not settle Julien's arbitrary higher-dimensional implication. The audit is complete for this family; it does not independently certify the later three mathematical turns or historical novelty.

Frozen subject: head421c6aa90eace49c8659f9a96e83c24fe1b5b901,57 target files under unsolved_math_prioritization/attempts/6600013 plus QUEUE. The independent source reconstruction and proposed falsifiers were sealed before reading candidate conclusions; the finished proof reconstruction and controls were sealed before consulting RESULT, old reviews or sibling/root verdicts. See PRE_CANDIDATE_SEAL.json and INDEPENDENT_SEAL.json.

## Source target

The literal source is Problem2.5.1, arXiv1604.06280v2 p8 and journal p587: repetitive, completely translation-aperiodic tilings in dimension d with patch complexity O(n^d), targeting finite total rational hull cohomology. The Cech interpretation follows the source's cited inverse-limit theory. Integral non-finite-generation, finite-rank high-complexity examples, rotation hulls, and periodic directions cannot supply a counterexample. [Original problem](https://arxiv.org/pdf/1604.06280), [published journal source](https://oro.open.ac.uk/48876/1/open%20problems%20adiceam%20et%20al%202016.pdf).

The one-dimensional implication is credited work. Its Rauzy inverse-limit theorem, connected graph formula and cofinal small-rank lemma were read in Julien0804.0145v1 pp23-27, where the linear-growth proposition is5.16; the published proposition cited by the original is6.7. The packet records this distinction correctly. [Julien source](https://arxiv.org/pdf/0804.0145).

The2017 definitions use absence of every nonzero translational period, syndetic repetition of each finite patch, and the translational orbit closure; symbolic finite-alphabet suspensions satisfy FLC automatically. Pointing, bounded collar changes and equivalent norms preserve growth exponents, while the numerical box-complexity coefficient need not equal the radius coefficient. [Julien2017](https://www.numdam.org/item/10.5802/aif.3091.pdf).

The Koivusalo-Walton qualification is correct: almost-canonicity does not generally identify acceptance-domain and hyperplane-cut topology; quasicanonicity suffices, and canonical windows meet that condition. This published correction is credited and not promoted as a new finding. [Koivusalo-Walton](https://doi.org/10.1017/etds.2020.10).

The four primary PDFs were independently downloaded. Three exactly match SOURCE_MANIFEST. The Cambridge response regenerates a download stamp: the fresh file has485595 bytes and SHA5046fbc65c23ff0ac0e20610f13128e1edd6a874c4c6fcaaa14be17ff12cf477, unlike the historical packet's485567 bytes and098e4c... hash. The cited mathematical pages agree; source_receipts.json records the actual fresh object and does not claim a false match. Relevant local PDF pages were visually checked. The journal page was confirmed through the primary web PDF text; direct local retrieval returned403, recorded in journal_source_receipt.json.

## Verified early claims

1. For Cartesian products, p_i(n)>=n+1 and the exact box language product imply every factor has finite liminf linear coefficient when the product coefficient C is finite. Cofinal Rauzy rank control then gives finite factor cohomology. Persistent classes imply the simultaneous eventual lower bounds p_i(n)>=max(1,r_i-1)n-B_i. These yield product_i max(1,r_i-1)<=C. Finite graph Kunneth plus Cech continuity gives total rank product_i(1+r_i)<=3^d C. The proof correctly uses eventual bounds, avoiding an invalid product of unrelated liminf subsequences. Sturmian equality is proved at the direct limit by integration of the constant and indicator cochains, with values1 and irrational frequency; it does not merely assume that stage cycles survive.
2. The two-block shear z(i,j)=(t(i+j),t(i+j+1),y(j)) has an invertible integer coordinate action and an invertible recoding. Independent minimal aperiodic factors therefore give a fully aperiodic repetitive finite-alphabet source-admissible tiling. Every box recovers a TM word of length n+m and a Sturmian word of length m, so P(n,m)=p_TM(n+m)(m+1) and square growth is O(n^2). Its real suspension is homeomorphic to a product suspension, with finite rational cohomology.
3. The TM alignment argument gives all-scale even/odd complexity recurrences. The signed rectangular mixed difference is chi=(m+2)(s(n+m+1)-s(n+m))+s(n+m). The proved increment recurrences give2n+6 and-2n on the stated cofinal square scales. Connected cellular complexes then force unbounded beta2 and beta1. This valid obstruction concerns raw finite approximants; it supplies no persistent infinite-rank hull group.

Full first-principles derivations, boundary cases and dependency discussion are in INDEPENDENT_RECONSTRUCTION.md. No empirical extrapolation is used for all-scale conclusions.

## Actual reproduction and independent falsifiers

| Check | Actual result | Evidence |
|---|---|---|
| Outer snapshot versus exact Git head |58/58 files match size, SHA and Git bytes |snapshot_binding_receipt.json |
| Private verify_turn1 replay |1435 assertions; output bytes match TURN_1_CHECKS |verify_turn1.py.stdout and receipt |
| Private verify_turn2 replay |418 assertions; output bytes match TURN_2_CHECKS |verify_turn2.py.stdout and receipt |
| New independent controls |18432 assertions; all pass |independent_controls.py, full stdout/stderr and receipt |
| New indexing/scope negative controls |466 assertions; all pass |negative_controls.py, full stdout/stderr and receipt |

The new18432-control script imports no candidate code. It obtains complete TM factors through length257 from binary digit parity and an aligned-block completeness proof. It uses a rational isolating interval for sqrt2-1 and certifies every floor/cut order for its Sturmian words. The signed cellular matrices are rebuilt separately and ranked with SymPy DomainMatrix over QQ. Extra examples include square(4,4), cells(110,264,168), Betti(1,5,18), chi14; asymmetric(1,4) and(4,1) both have Betti(1,7,10), chi4. Euler controls run through the negative scale n96.

The negative controls remove the two-block recoding and correctly get P(n,m)=p_TM(n+m-1)(m+1), detecting the otherwise concealed indexing shift; for example square n2 changes chi10 to-4. Removing the independent y coordinate gives the actual diagonal period(1,-1) at all sites, so that tempting low-complexity example fails the exact source hypothesis. These controls confirm that recoding and full aperiodicity are substantive parts of the written construction.

Initial missing-SymPy runtime attempts and an initially reversed convergent enclosure were caught immediately and preserved under named failure receipts. Successful runs use private SymPy1.14.0; no system package or frozen candidate file was modified. The main controls, successful receipts and seal hashes were verified after the historical comparison. The final SHA manifest binds all nonprivate audit outputs; source page-image hashes are recorded separately.

## Remaining gap and promotion limit

No repair is mandatory for this family's proofs, source scope, or finite arithmetic. Publication must preserve the restricted product class, the raw-approximant scope of the obstruction, credited one-dimensional theorem, rational coefficients, and unproved arbitrary target.

The exact unsolved gap is a bound on persistent rational classes for every repetitive fully aperiodic O(n^d) hull, or an actual admissible such hull carrying infinitely many persistent independent rational classes. Neither Cartesian product Kunneth nor the growing Euler examples establish that. The old review agrees with this early-family conclusion; reading it after sealing caused no revision of the independent verdict. The later cover/profinite claims require their own family audits. No worldwide novelty or current-open-status certification is made.

Assigned-family audit completion:100%. This percentage measures completed audit work, not progress toward solving the original problem. No external communication, Git mutation, publication service, or shared queue edit was performed.
