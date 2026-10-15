# Authored source ledger

Inspection date: 12 October 2026, America/Los_Angeles.
Only bibliographic descriptions, authored relevance assessments, URLs, and checksums are intended for publication. Full text and screenshots remain in ignored `sources.private/`.

## S01: Exact target

Oliver Knill, *Some intriguing open problems in Hamiltonian dynamics*, talk of 19 October 2000, item 10. [Primary HTML](https://people.math.harvard.edu/~knill/seminars/intr/), [two-page list](https://people.math.harvard.edu/~knill/seminars/bozeman/intr-l.pdf), target p. 2. HTML and visually rendered page inspected. Exact source copy acquired from the author's abel.math.harvard.edu mirror; SHA-256 matches the candidate's pinned HTML and PDF hashes. The question is positive Liouville measure; weak mixing/genericity occur in its separate guess. No standard phase-space restriction is printed.

## S02: Exact discrete-time dynamics

Hirotada Anzai, *Ergodic skew product transformations on the torus*, Osaka Mathematical Journal **3** (1951), 83-99. [Primary repository](https://doi.org/10.18910/11966), [primary article](https://ir.library.osaka-u.ac.jp/repo/ouka/all/11966/omj03_01_08.pdf). Section 6, Theorem 6 and Corollary, pp. 91-92; these pages visually inspected. The irrational base rotation with cocycle `m*x`, with `m=1`, is exactly the candidate map. The Fourier shift/orthogonality calculation and continuous spectrum on the complement of the circle factor are old. It is a map theorem, not by itself a Hamiltonian volume theorem.

## S03: Compact ambient geometry

William P. Thurston, *Some simple examples of symplectic manifolds*, Proceedings of the AMS **55** (1976), 467-468. DOI [10.1090/S0002-9939-1976-0402764-6](https://doi.org/10.1090/S0002-9939-1976-0402764-6). [Primary article scan mirrored at Edinburgh](https://www.maths.ed.ac.uk/~v1ranick/papers/thurstonsimple.pdf), p. 467 visually inspected. The article's unipotent torus bundle over a two-torus, with the descended fiber form plus base area, is the classical topology underlying the candidate. The audit explicitly identifies the affine mapping torus with this topology; it does not assert identity of all symplectic forms.

## S04: Pre-2000 Hamiltonian realization

Manuel de Leon and Martintxo Saralegi, *Cosymplectic reduction for singular momentum maps*, Journal of Physics A: Mathematical and General **26** (1993), 5033-5043. DOI [10.1088/0305-4470/26/19/032](https://doi.org/10.1088/0305-4470/26/19/032). [Primary author-hosted article](https://www.mesa-lml.fr/Articulos/Cosymplectic.pdf). Lemma 3.2, p. 5036: the form `Omega+eta wedge ds` on `M x R` is symplectic exactly when the original pair is cosymplectic. Section 6.1, p. 5042: when the original Hamiltonian is zero, the extended Hamiltonian is the real added coordinate and its vector field is the lifted Reeb field. Both exact pages visually inspected. These are the same Hamiltonian extension used in the audit's finite energy band deduction.

## S05: Exact continuous-time classical identification

Artur Avila, Giovanni Forni, Corinna Ulcigrai, *Mixing for time-changes of Heisenberg nilflows*, Journal of Differential Geometry **89** (2011), 369-410. [Published article scan](https://archive.ymsc.tsinghua.edu.cn/pacm_download/21/903-JDG-89-3-A1-avila.pdf), [author preprint](https://arxiv.org/abs/1003.4636). Published Sections 2.1-2.2, Theorems 1-2 and Lemma 1, pp. 375-377, directly inspected; published Lemma 1 must not be cited using the preprint's p. 7. Their parameter choice `E=1, w_y=1, w_x=a, w_z=-a/2` gives exactly the candidate's return map and constant return time. Classical ergodicity and mixed toral/Lebesgue spectrum are recalled here and credited to Green (1961) and Auslander-Green-Hahn (1963). Theorem 4, p. 381, concerns nontrivial roofs and does not turn this constant-roof candidate into a weakly mixing flow.

## S06: Closest source-author Hamiltonian result

Oliver Knill, *Weakly mixing invariant tori of Hamiltonian systems*, Communications in Mathematical Physics **204** (1999), 85-88. DOI [10.1007/s002200050638](https://doi.org/10.1007/s002200050638). [Primary author offprint](https://people.math.harvard.edu/~knill/offprints/mixingtori.pdf). Lemma 3.1 and Theorem 3.3, pp. 87-88, inspected in full and visually rendered. They provide Hamiltonian time change and weakly mixing dynamics on an invariant torus, not a full phase-volume band. Cite as related context, never as a sufficient positive-volume resolution.

## S07: Author's integrability convention

Oliver Knill, *On a spectral notion of integrability*, UAB talk, 28 March 2002; header revision 29 March 2002. [Primary slides](https://people.math.harvard.edu/~knill/seminars/integrable/birmingham.pdf). All four pages visually inspected because text extraction is defective. Page 1 defines spectral integrability through ergodic invariant measures and explains why varying integrable frequencies can give continuous spectrum for a nonergodic measure. Page 2 gives compactness of Koopman orbits as a test. It supports explicitly separating per-energy ergodic behavior from energy averaging. It does not contain an inspected direct solution of item 10.

## S08: Later author discussion

Oliver Knill, *Measure and Category*, 2 July 2023. [Primary author article](https://www.quantumcalculus.org/measure-and-category/). Inspected paragraphs defining classes A-D and the coexistence discussion. It distinguishes ergodic discrete-spectrum behavior, positive exponents, zero-exponent singular-continuous behavior, and mixed spectral type. It discusses genericity questions and does not supply a checked direct resolution statement for item 10. The candidate has mixed spectral type and need not satisfy the narrower purely singular-continuous class.

## S09: Fayad's Hamiltonian mixing tori

Bassam R. Fayad, *Analytic mixing reparametrizations of irrational flows*, Ergodic Theory and Dynamical Systems **22** (2002), 437-468. DOI [10.1017/S0143385702000214](https://doi.org/10.1017/S0143385702000214). [Primary author article](https://webusers.imj-prg.fr/~bassam.fayad/mixing.pdf). Introduction, Corollary 2, p. 442, inspected. The Hamiltonian is `phi(theta)(|r|^2-1)` and the mixing tori are stated for a dense uncountable set on the zero energy hypersurface. That does not imply positive full six-dimensional Liouville volume. No such implication is used by this audit.

## S10: Standard product and mapping-torus background

Beniamino Cappelletti-Montano, Antonio De Nicola, Ivan Yudin, *A survey on cosymplectic geometry*, Reviews in Mathematical Physics **25** (2013), 1343002. DOI [10.1142/S0129055X13430022](https://doi.org/10.1142/S0129055X13430022), [author manuscript](https://arxiv.org/abs/1305.3704). Proposition 2.3, manuscript p. 5, gives the exact product form and explicitly cites de Leon-Saralegi (1993). Theorem 3.44, manuscript p. 25, recalls Li's mapping-torus existence characterization. These are background theorem references; one must not infer periodicity of a given Reeb flow merely from a diffeomorphism type.

Hongjun Li, *Topology of co-symplectic/co-Kahler manifolds*, Asian Journal of Mathematics **12** (2008), 527-544, DOI [10.4310/AJM.2008.v12.n4.a7](https://doi.org/10.4310/AJM.2008.v12.n4.a7). Primary abstract/introduction inspected through indexed publisher content; direct PDF acquisition returned 403. The ledger does not claim complete direct inspection of Li's proof.

## S11: Exact compact thickening precedent before this candidate

Eva Miranda and Pablo Nicolas, *Hamiltonian group actions in cosymplectic geometry*, [arXiv:2607.05231v1](https://arxiv.org/abs/2607.05231v1), submitted 6 July 2026. Proposition 4.1, pp. 8-9, directly inspected: compact `M x S1` with `beta+dtheta wedge alpha`. It is a preprint and its broad group-action assertions are not audited here. Only the elementary thickening proposition is used as a same-formula precedent; the original target already follows using [S04] on an energy interval.

## S12: Classical Anosov-Katok family

Dmitry V. Anosov and Anatole B. Katok, *New examples in smooth ergodic theory. Ergodic diffeomorphisms*, Trudy Moskovskogo Matematicheskogo Obshchestva **23** (1970), 3-36 (Russian). [Primary metadata](https://www.mathnet.ru/php/archive.phtml?jrnid=mmo&option_lang=eng&paperid=237&wshow=paper). English translation usually cited as Trans. Moscow Math. Soc. **23**, 1-35; this audit does not conflate the two page ranges. Original metadata checked; weak mixing is independently credited to the original Section 5 by the original coauthor's later paper [S13]. Full original theorem pages were not directly inspected.

## S13: Original coauthor's confirmation

Bassam Fayad and Anatole Katok, *Constructions in elliptic dynamics*, Ergodic Theory and Dynamical Systems **24** (2004), 1477-1520. DOI [10.1017/S0143385703000798](https://doi.org/10.1017/S0143385703000798). [Primary author paper](https://webusers.imj-prg.fr/~bassam.fayad/herman.pdf). Section 2.4.1, p. 1483, recalls weak mixing as generic in the relevant closure of conjugates and credits original Anosov-Katok Section 5; the basic disk, sphere and annulus settings are discussed. This is checked evidence for a distinct classical approach family. It is not an assertion of strong mixing, and the constant suspension still has clock eigenfunctions.

## S14: Modern disk Hamiltonian suspension and entropy context

Barney Bramham, *Periodic approximations of irrational pseudo-rotations using pseudoholomorphic curves*, Annals of Mathematics **181** (2015), 1033-1086. [Primary article](https://annals.math.princeton.edu/wp-content/uploads/annals-v181-n3-p04-p.pdf). Introduction pp. 1034-1035 recalls zero-entropy disk maps and weak mixing; Section 7, especially pp. 1062-1065, displays Hamiltonian mapping-torus structures. Also inspected his [2012 primary preprint](https://arxiv.org/abs/1205.6243), whose abstract explicitly credits weakly mixing zero-entropy Hamiltonian disk maps to 1970. These concern return maps or stable Hamiltonian energy structures. The full phase-volume conclusion still needs the extra real energy coordinate.

## S15: Katok's Hamiltonian perturbations: an exact limit on inference

Anatole B. Katok, *Ergodic perturbations of degenerate integrable Hamiltonian systems*, Mathematics of the USSR-Izvestiya **7** (1973), 535-571. DOI [10.1070/IM1973V007N03ABEH001958](https://doi.org/10.1070/IM1973V007N03ABEH001958). [Primary indexed abstract/introduction](https://www.mathnet.ru/php/getFT.phtml?jrnid=im&option_lang=eng&paperid=2279&what=fullteng) checked. Full PDF download failed with a TLS timeout, so theorem pages are not independently verified here. The primary retrospective *Anatole Katok*, [Cambridge article](https://www.cambridge.org/core/journals/ergodic-theory-and-dynamical-systems/article/anatole-katok/D0699E98CA8951FD35A8D8879E449837), explicitly states discrete spectrum for his related weak-oscillator construction. Accordingly, ergodic per-energy behavior is not used as an automatic non-almost-periodicity theorem. This remains a bounded source-access gap, not a hidden premise.

## Additional checked context, without promotion to a target theorem

- Avila-Fayad-Le Calvez-Xu-Zhang, [primary manuscript](https://webusers.imj-prg.fr/~bassam.fayad/AFLXZ.pdf), introduction: weakly mixing disk/sphere constructions from approximation by conjugation; no automatic ambient-volume claim.
- Bochi-Katok-Rodriguez Hertz, *Flexibility of Lyapunov exponents*, [primary journal article](https://www.cambridge.org/core/journals/ergodic-theory-and-dynamical-systems/article/flexibility-of-lyapunov-exponents/C17B9DA4A5ACE2AD95F83765E62ABB78), introduction: old zero-exponent ergodic disk/sphere constructions. Not used to turn ergodicity into weak mixing.
- Green (1961), DOI [10.1090/S0002-9904-1961-10650-2](https://doi.org/10.1090/S0002-9904-1961-10650-2), and Auslander-Green-Hahn (1963), *Flows on homogeneous spaces*: bibliography and later primary theorem attribution checked; full originals not acquired.

Public `SOURCE_MANIFEST.json` records checksums for the successfully acquired documents. No third-party full text is redistributed.
