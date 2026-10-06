# Independent adversarial priority and materiality review

Frozen submission: PR280 / problem30000156, original head `091bdecef6f84154f5d5c205a4b07eeb6391b8f8`.

This review finds **no verified earlier exact target-negative theorem or equivalent counterexample in the bodies actually read**. It does not certify novelty. A theorem note can pass scientific readiness under an expressly bounded, transparent historical application claim, subject to the attribution and wording below. The user's stronger desired framing as a first resolution of a previously unsolved problem remains **held**: the close four-author 2011 manuscript has not been recovered, and the search does not establish the problem's unsolved status through 2026. Failure to recover that manuscript is not evidence that someone previously solved the problem.

## Claim and success criteria

The accepted mathematical/source input is the frozen original `PROOF.md`, `SOURCE_AUDIT.md`, and `ROOT_MATHEMATICAL_AND_SOURCE_ACCEPTANCE_01.json`. The acceptance record is not a novelty authority. Input hashes and subsequent peer-report hashes are in `INPUT_PINS.json` and `PEER_INPUT_PINS.json`.

The target is the literal broad existence assertion recorded by Roberts and Vivaldi in the 2004 Oberwolfach report, pp2944–2945: an ordinary, unaveraged, point-weighted period CDF with period scaled by p. The candidate is

\[
L(u,v)=(u,(u^2+1)v),\qquad
D_p(x)=p^{-2}\#\{z\in\mathbb F_p^2:T_p(z)\le xp\},
\]

on all affine points, for primes p≡3 mod4. The accepted result is that for every fixed 1/2≤x<1,

\[
\limsup_{p\equiv3\ (4)}D_p(x)=1,
\qquad \liminf_{p\equiv3\ (4)}D_p(x)\le23/24.
\]

A prior collision need not use this exact map or constant. A verified earlier full-affine example in the same admitted broad class, with rigorous incompatible prime subsequences for the same ordinary statistic, would suffice. A new synthesis made in this audit from old ingredients is not itself a verified earlier publication of the target application. An averaged distribution over primes, a distribution across parameters at a fixed prime, a conditional fixed-base order conjecture, or a random-ensemble theorem does not alone meet the collision criterion.

The result does not refute a formal complex polynomial-automorphism conjecture, a genus-one foliation assertion, or a random-involution ensemble theorem. These class, phase-space, weighting, and limiting distinctions must remain explicit.

## Independence and method

`INDEPENDENT_FINDINGS_CHECKPOINT_01.md` was sealed before either peer priority draft was read (SHA256 `3ab333fd47b584fef96fa47cc8f287edb3d0ddd2405adf03124efbc2fd895a73`). It fixed the exact-equivalence test and distinguished historical priority from theorem readiness. Later peer findings were used as leads, with provenance pins, rather than as automatic body exclusions.

This audit independently pursued official repository bitstreams, MathNet original-text endpoints, the journal's historical AMS PDF route, actual Wayback capture indexes and original-host captures, and a second institutional mirror of Neumärker's thesis. Actual PDFs were extracted and read within the scopes recorded in `READING_RECEIPTS.json`; selected pages were visually checked. Downloading, extracting, term searching, and reading are separately identified. `DIRECT_FETCH_RECEIPTS_01.json` through `DIRECT_FETCH_RECEIPTS_10.json` preserve request/final URLs, HTTP outcomes, bytes, and hashes, including non-PDF access pages and failures. `SEARCH_RECEIPT_FINAL.json` records a final explicit exact-title/collision query batch; other raw search outputs are preserved locally. Search absence and archive incompleteness are not exclusions.

All work stayed in this dedicated folder on the observed main branch. No human was contacted, no outreach prepared, no Git/remote state changed, and no publication or promotion authorized. Completion percentages in `RESEARCH_LOG.md` describe completion of this bounded audit, not a probability of novelty.

## Actual recovered bodies and adverse findings

### Arnold2003: original-content gap closed

The actual Russian original was recovered from the [official MathNet full-text endpoint](https://www.mathnet.ru/php/getFT.phtml?jrnid=faa&paperid=132&what=fullt&option_lang=eng), despite the language parameter. Both English- and Russian-labelled endpoint requests returned the same Russian PDF: 221009 bytes, SHA256 `ffbeec54a5eea63a9d35ca6e25a797785a1b61ee1349a1d3eaef8858fc969e79`, all18 original printed pages read. This is the paper associated with English DOI10.1023/A:1022915825459, not Arnold's separate 2003 survey. The English translation was not recovered or read.

The paper treats fixed-multiplier dynamics (chiefly multiplier2) on residue classes and units. It gives arithmetic cycle/period relations and congruence classifications, then finite computations and empirical weak asymptotics for normalized periods. It does not construct the candidate varying-fiber affine map or establish a rigorous ordinary planar p-scaled CDF nonlimit. Its experimental mean or ratio statements cannot be silently upgraded to that theorem. The English-translation version gap remains; the actual original-content gap is closed.

### Arnold2005: actual final body recovered from an original-host capture

The current AMS route produced a LibLynx access page, and MathNet's full-text route produced an access notice, not a PDF. A fresh public CDX query identified a successful 2015 capture of the journal-hosted original. The [captured original AMS PDF](https://web.archive.org/web/20150922143618id_/http://www.ams.org/distribution/mmj/vol5-1-2005/arnold.pdf) is 258546 bytes, SHA256 `f33a35719b6adc35c9116f3b7c11162a9c4a7617d2cdf5823fa98d9479c34b91`. All18 PDF pages / MMJ5(1), printed5–22, were read. Identity and capture evidence are preserved in the direct receipts; the archive's compressed capture length is not presented as PDF length.

The body studies constant-multiplier residue dynamics, arithmetic orbit properties, and neighbor-spacing statistics. Its weak period means and arithmetic randomness discussion are largely empirical; its precise congruence classifications do not supply the required varying-prime planar CDF nonlimit. This is an actual original-body exclusion for the exact prior theorem, not a conclusion from the abstract. DOI10.17323/1609-4514-2005-5-1-5-22 is no longer an unresolved original-body lead in this audit.

### Jogia2008 and Siu2019: recovery closed, read coverage bounded

Fresh reads of the official handle pages exposed actual public bitstreams, independently of the peer recovery:

- [Jogia2008 official PDF](https://unsworks.unsw.edu.au/bitstreams/aff0cf7d-1349-41d4-af1d-9f19853d36d1/download), handle1959.4/40947, DOI10.26190/unsworks/17873, 248PDF pages. Selected scopes are in the receipts.
- [Siu2019 official PDF](https://unsworks.unsw.edu.au/bitstreams/1e1fbe86-f63a-428c-8a1e-f12a8980ae79/download), handle1959.4/63745, DOI10.26190/unsworks/21440, 191PDF pages. Selected scopes are in the receipts.

Jogia's printed47–48 treat genus-zero parameterized translation/multiplication. Printed70–75 and92–99 discuss integrability tests and period distributions, chiefly elliptic assumptions, plateaus, and finite examples. Printed182–183 and215–219 explicitly use denominators z²+1 and primes3 mod4 to obtain full-affine permutations. This is particularly adverse to a claim that the zero-free quadratic/suitable-prime device is new. The passages actually read do not prove the target nonconvergence result. A whole-thesis exclusion is not claimed.

Siu's printed54–71 include artificial parameter-coordinate integrals, foliations, and cat-map orbit orders. Corollary6.3.8 and Theorem6.3.9 describe periods and φ(t)/2 counts across parameters at fixedp, with a parameter-weighted CDF. Printed96–110 discuss experiments for fixed parameters and anomalous parameter sectors, explicitly distinguishing them from failure of the expected fixed-map prime limit. These are close arithmetic and dynamical ingredients, but the scopes read contain no rigorous target-negative theorem. A whole-thesis exclusion is not claimed.

### Roberts2011 and Neumärker2012: missing manuscript remains close

The actual [Roberts2011 proceedings PDF](https://www.dma.uvigo.es/~eliz/pdf/Roberts.pdf) was recovered (445755bytes; SHA256 `0b19e105ae8e8196cf9f0ac430e9892d49873eb9696cef22dcd00910e63dd8ac`). Printed217–221 were fully read. Page217 defines the CDF using periodic-point weighting and a normalization parameter; pp218–219 distinguish constrained reversible maps, specific-map evidence, and random-involution expected distributions. Reference9 on p220 names the four-author 2011 UNSW manuscript. The proceedings body is not that manuscript.

The fresh [Neumärker2012 institutional-mirror thesis](https://noah.nrw/ubbihs/download/pdf/5124915) is 3763519bytes, SHA256 `cbb1b9a04bfb1852628190eb5466e4a251d4fc7930a5e5fc46a8bb7e8534bb35`. Its introduction and conclusion, plus pp58,80–82 and90–92, were read. Page91 cites the same four authors with a rational-maps/experimental-results title variant and in-preparation status. Page82 describes numerical observations and an extension accounting for denominator singularities. This provides actual context and a bibliographic lead; it does not establish everything the unseen manuscript contains or prove the two citations refer to an identical final version.

Current/archived official author pages and actual prefix CDX rows yielded no recovered four-author body. The retrieved 2011 archived homepage has older selected-publication content. Missing archive rows, stale selected lists, failed index requests, and lack of search hits cannot establish that the manuscript was never released or contains no counterexample. A downloaded 87-page Vivaldi slide PDF was image-based and was not read; it provides no exclusion.

There is also a precise reason not to exclude this lead merely because the candidate is triangular: with a(u)=u²+1, the rational involution G(u,v)=(u,1/v) satisfies G L G=L⁻¹ on the rational function field. This is a direct algebraic deduction, not a claim about the missing manuscript. G is undefined on v=0, so it does not put the example within every later full-affine involution-permutation hypothesis. L also has extra commuting fiber scalings. Nonetheless, its rational reversibility makes the four-author subject a materially close priority lead. Genus-zero fibers or failure to be a complex polynomial automorphism are not enough to dismiss a manuscript about reversible birational/rational maps.

## Ingredient priority and the strongest attempted falsification

The peer mechanism audit, read after the independent checkpoint, identifies older triangular-map families (Ostafe–Shparlinski2009/2010), later explicit zero-free quadratic multiplier use (Roy–Steiner2023), primitive-value character machinery, totient-density variation (Aivazidis–Sofos2014), and the earlier mean attributed to Pillai1941. The present audit accepts these as adverse ingredient-priority evidence within that report's pinned scopes; it does not reclassify them as earlier exact target applications.

I independently checked the adopted actual Aivazidis–Sofos arXiv1308.5701v2 body at PDF1–3 and16–17. Equation1.1 and Theorem1.3 include normalized totient densities and a continuous limiting empirical distribution. Its proof first establishes the distribution along primes before comparing with prime powers. For n=1, a continuous proper empirical distribution is incompatible with an ordinarily convergent prime sequence φ(p−1)/(p−1): a convergent sequence would produce a point mass. That implication is my deduction from the theorem, not a new analytic result and not a statement specifically proved there about the p≡3 mod4 subsequence. The arithmetic nonconvergence mechanism is already established and must be attributed.

I also independently read the published Colón-Reyes–Jarrah–Laubenbacher–Sturmfels2006 paper, printed336–337: discrete logarithms conjugate monomial dynamics on the multiplicative torus to exponent-matrix dynamics over Z/(q−1), preserving cycles. This makes a primitive-order mechanism with a fiberwise multiplier very elementary. Combining such prior mechanisms with prior density results is an adverse materiality observation: the remaining possible contribution is a modest application to the precise broad question, not a new family or new order-density theory. The combination made here is not a verified earlier negative-answer publication; changing torus to full affine phase space also requires its own convention check. I have not promoted an alternative result.

These attempts falsify expansive construction/arithmetic novelty, but they have not falsified the exact claimed application by locating an earlier body that proves it. A literature audit should not use either conclusion as a substitute for the other.

## Gap classification and decision

| Lead / issue | Evidence status | Exact remaining gap | Materiality |
|---|---|---|---|
| Arnold2003 Russian original | Actual original fully read | English translation not read; no exact negative theorem in original | Original-content priority lead closed; version qualifier retained |
| Arnold2005 MMJ original | Actual final English original fully read | None for this body's exact-target comparison | Original-content priority lead closed |
| Jogia2008 / Siu2019 | Actual complete PDFs recovered, priority-relevant selected scopes read | Unread thesis pages are not exclusions | Recovery gap closed; bounded coverage uncertainty retained |
| Roberts2011 proceedings | Actual pp217–221 read | Cited four-author body is a different object | Bibliographic/context evidence, not manuscript exclusion |
| NRVV2011 four-author manuscript | Two actual-body citations; no body recovered | Its theorem/counterexample inventory and publication/version history unknown | Material blocker to first/current-unsolved priority certification |
| Broader earlier/later literature | Scoped searches and peer bodies | Search/citation/version coverage incomplete | No worldwide novelty certificate or current-open-status certificate |
| Accepted mathematical theorem | ROOT independent math/source acceptance plus frozen inputs | No new mathematical gap introduced by this priority review | Correct bounded negative theorem can be scientifically ready |
| Ingredient novelty | Several direct/peer prior mechanisms established | Particular question application priority unresolved | Broad ingredient novelty rejected; attribution required |

**Bounded readiness:** PASS-ELIGIBLE, conditional on a concrete rewrite that makes the precise negative theorem, old inputs, and historical uncertainty explicit. It can truthfully answer the literal assertion recorded in2004 without claiming that nobody else has answered it since. This readiness is not approval to promote or publish and does not certify a novel contribution for the project's goal.

**Desired unsolved/first-resolution readiness:** HOLD. Neither the recovered sources nor the unresolved manuscript establish an earlier exact solution, but they also do not establish continued unsolved status. Calling the issue still open in2026, claiming a first solution, or allowing the title/abstract to imply either would outrun the evidence. Narrowing a claim must be visible in the title/abstract/introduction, not buried in an audit footnote.

## Concrete framing

Acceptable title: **An explicit failure of ordinary prime-limit cycle distributions for a birational map**.

Acceptable abstract/introduction statement:

> We give an explicit birational map whose ordinary point-weighted, p-scaled period distributions fail to converge as p varies through primes congruent to3 modulo4. This provides a negative answer to the literal broad existence assertion recorded in the2004 Oberwolfach report of Roberts and Vivaldi. The triangular construction, suitable-prime device, and arithmetic inputs belong to established families. The historical priority of this particular application has not been established.

The paper should display the full-affine phase space and congruence subsequence, identify the exact2004 wording used, and separate it from restricted later statements. Cite the older triangular mechanism and zero-free device where the map is introduced, and cite primitive-value/totient inputs where used. Retain the exact strongest verified result and its elementary/non-new ingredients. A bibliographic note should disclose the cited unrecovered2011 four-author manuscript and the inability to certify current-open status; it must not characterize its unseen contents.

Rejected framing includes **first solution**, **resolution of an open problem still unsolved until2026**, **new triangular construction**, **new zero-free quadratic trick**, or **disproof of the reversible polynomial-automorphism/elliptic/random-ensemble conjecture**. A title saying merely that an open problem has been solved would also invite an unsupported first/current-open reading unless the bounded interpretation is unmistakable.

## Falsifiable conditions that would change this verdict

A recovered earlier manuscript/paper proving an admitted fixed-map ordinary CDF nonlimit would convert the application claim into prior-result reproduction or refinement, even with different constants. A recovered NRVV2011 body lacking such a theorem would close that specific gap, but would not prove worldwide novelty or current-open status. An explicit later source recognizing the broad question as solved would defeat a current-unsolved claim. A materially different application contribution, such as a verified sharper quantitative result absent from predecessors, would require a new comparison instead of reusing this verdict.

The strongest verified outcome remains: no exact earlier target-negative result was established by this audit; two important original-body access gaps were actually closed; historical first/current-unsolved claims remain unsupported; a transparent, modest application note is scientifically defensible on the independently accepted mathematics. No external input was sought. If the human later obtains the missing manuscript independently, its body is the most valuable next evidence to record.
