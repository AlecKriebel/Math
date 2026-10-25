# Complete independent adversarial review — Zenodo 23333046

**Disposition: the full original mathematical theorem is supported; no central gap, counterexample or required source correction was identified.** This is an AI research review with no publication authority. The complete custom object is `VERDICT.json`; neither this result nor any historical object has been normalized into a generic PASS.

The reviewed paper is *A characteristic-two counterexample to dévissage for local deformation functors*, Alec Kriebel, actual five-page reader, API version 1.0. The manuscript prints “12 October 2026 (research note)” without a printed version. Zenodo declares 12 October and records creation at 13 October 2026, 05:43:05.275367 UTC. Those are distinct fields and have not been conflated.

## Exact claim and outcome

For k=F4, G=(F4,+), N=F2 and rho(a)(t)=t/(1+at), the theorem excludes every prorepresentable functor F and every choice of natural maps from the actual fixed subfunctor D_N^Q and quotient deformation functor D_Q to F that could make restriction–induction into their fibre product formally smooth. The exclusion is independent of the recipient's tangent dimension. It includes the originally prescribed one-dimensional tangent-space formulation.

The coefficient category is local Artinian W(k)-algebras with identified residue k, and equivalence is by all coordinate changes reducing to the identity. Nilpotent constant terms are permitted. This is the original category, not a framed or zero-section-preserving variant. The statement does not claim to refute the separate variant assuming D_N and D_Q prorepresentable. This example has the exceptional nonprorepresentable involution component.

## Independent mechanism and universal proof

The entire actual reader and all 285 controlling TeX lines were read before foreign primary bodies, mathematical source code, historical proof-review narratives or current opinions. The immutable early reconstruction already contains the exact theorem, falsification targets, a separate ring-injection route and a full rank-two formal-series calculation. Its seal is `7c40942626ed92dd3bb9190d187cf1f470c60e2782a43c57daefa89d85336cc8`. No sibling/root final report or verdict was used in this review.

`DERIVATION.md` gives a checkable proof of the entire original assertion. Its essential steps are:

1. The N-invariant parameter is y=t²/(1+t); the induced quotient involution is y/(1+y). Exact invariant-ring bases prove these identifications.
2. Restriction of integral N-invariant derivations is precisely M=y k[[y]]d/dy, by unique extension and a sharp valuation calculation. The lift of y d/dy is (1+t)d/dt, so omitting constant coefficients would change the calculation.
3. Put z=y²/(1+y), R0=k[[z]]. On the complete free module M=yR0⊕y²R0, the characteristic-two cohomology differential has matrix [[0,0],[1,0]]. Its kernel equals its image on all formal series, with explicit primitives. Thus H¹(Q,ThetaN)=0. A direct cocycle argument then proves tangent restriction injective on the actual deformation functor.
4. The nonzero quotient tangent v is represented by (y+e)/(1+y) over A=k[e]/e². No arbitrary identity-reducing first-order coordinate can remove its nonzero constant perturbation.
5. The injective coefficient map A→B=k[w]/w³, e↦w², kills v in the actual quotient deformation functor. The explicit allowed conjugacy is proved by M_(w²) C=(1+w) C M_0, C=[[1+w,w],[0,1]]. A represented Hom-functor preserves injections. Naturality therefore forces every map D_Q→F to kill v, including maps with mixed-characteristic representing rings and without any prescribed tangent formula.
6. For any proposed f,g, the point (0_N,v) belongs to the actual fibre product at A. Formal smoothness over A→k would lift it to a G-tangent with zero restriction. Injectivity makes that tangent zero, whose induction cannot equal nonzero v. This is the required universal contradiction.

This route does not infer recipient collapse from mere nonprorepresentability. It does not use universality of a Klein-four deformation ring or replace the fixed deformation subfunctor by a hull. The proof is about every permitted natural transformation, not finitely many guessed formulas. It already fails at the first small extension.

For the auxiliary identification, the full module ThetaSharp has differential z[[1,1],[1,1]] in basis (1,y), giving H¹(Q,ThetaSharp)=k. The quotient ThetaSharp/ThetaN is the trivial module k, so the original prescribed H¹ is one-dimensional. These computations are exact over the complete coefficient ring; finite-jet rank experiments are not their proof.

## Exact diagnostics and attempted falsification

`exact_adversarial.py` was independently written from the sealed mechanism. It uses the existing mathematical runtime and exact symbolic polynomial reduction over F4, plus separately implemented finite Artinian arithmetic. It verifies the action, quotient and derivative identities, module basis transformations, all pairs for the injection and cubic automorphism, fixed ring, matrix involution and both conjugacies. All predicates use explicit guards.

Two pristine runs, ordinary and optimized Python, passed. Seven deliberately changed formulas or assumptions rejected in each mode: quotient action, zero-section module restriction, derivation weight, false vanishing of full quotient H¹, a false coefficient-ring embedding, false fixed ring, and omitted conjugator translation. These fourteen controls detect the intended failures. One fully inspected original explicit-guard arithmetic program was also run once and passed; no package builder/finalizer, historic permission harness, compiler or full portable suite was executed.

An initial own diagnostic wrongly expected the injection conjugacy to fail over the quartic truncation. Exact multiplication rejected that expectation: the injection identity is polynomially valid there too. The cubic parameter-shift identity is the one with a w³ residual. The unsealed diagnostic was corrected and the failed development expectation retained in `EXACT_RESULTS.json`; no source or early sealed object was changed. This is not a defect in the manuscript.

The computations corroborate identities and control sensitivity. The complete formal-series argument, arbitrary-coordinate nonvanishing and all-natural-map quantifier are justified by the written derivation, not by the finite runs. `PROOF_BOUNDARIES.md` records the hidden-hypothesis and limiting-case challenges individually.

## Primary attribution and limits

Actual OWR contribution pages, arXiv:1112.0352v1 interfaces, published Byszewski–Cornelissen pages, and the official 104-page thesis's question/conditional-theorem interface were directly read after the early seal. `PRIMARY_LEDGER.md` gives exact page coordinates, supported imports, edition/access limits and predecessor credit; `PRIMARY_CUSTODY.json` binds actual cached bytes and raw acquisition receipts. Critical category/question/Proposition 6.1 pixels were inspected too. This does not claim a read of every page in all four foreign works or a re-proof of the long conditional obstruction theorem.

The [published Byszewski–Cornelissen paper](https://www.numdam.org/item/10.5802/aif.2450.pdf) already supplies the involution pathology, parameter-shift conjugacy and injection collision. Those are established ingredients. The [original OWR question](https://ems.press/content/serial-article-files/46200), [specified arXiv v1](https://arxiv.org/pdf/1112.0352v1) and [official thesis](https://dspace.library.uu.nl/server/api/core/bitstreams/6c6ba94b-6588-4c8d-a2de-050faf43aea7/content) support the distinction between the unrestricted question and conditional component-prorepresentability results. The checked contribution assembles the known collision with the computed zero restriction kernel. No later journal version of the arXiv source is invented.

Two focused web queries and these primary interfaces are a bounded literature check, described in `SEARCH_LEDGER.md`. They certify neither novelty, priority, firstness nor continued openness until 2026. The first official thesis URL returned retained 403 HTML; that response is not counted as a PDF. A subsequent official direct bitstream yielded the actual 104-page PDF and the cited interfaces. Historical source-package search/review counts were read only after our own mechanism and controls and are not claimed as this lane's work or authority.

## Original custody and review completeness

The selected reader has 72,991 bytes and SHA256 `206114a917235504567f9f8487023c284aebacef00440e3c5bebfed98639d8cb`. The whole controlling TeX has 13,594 bytes and SHA256 `6c35823d8c64fbc3383dd04497a8bdfcffb80e32786b4f4cb54d5cc4a9cf61b1`. The original ready seal is `0b47008701fdf09019ae4ae87a09d648c90992ab4253b67481ec7bd7b36d355d`.

All 163 original ready-manifest files plus its manifest and seal were rehashed. The complete ZIP was CRC-read, all 154 regular member hashes/extracted bytes matched, and expanded size was 884,320 bytes. There are no nested archives. Its embedded reader equals the actual standalone five-page reader byte for byte. The identical review-copy TeX is not treated as a competing edition.

The literal source schema is `all_assets_in_original_order` with whole `original_api_file_object` objects. ZIP-before-PDF order, native checksum spelling/case, complete raw metadata, original API objects, actual paths and full transport headers/fields remain unchanged. This lane reuses the source owner's fresh authentication receipts and does not claim to have made those requests itself. `INPUT_BINDINGS.json` also binds the four actual primary bodies, two raw primary receipts and nine ignored derived cache files. All borrowed bodies and derived text/pixels stay in ignored caches; no full borrowed text is incorporated in public outputs.

`verify_review.py` is read-only and checks exact source/primary/cache/early/final bytes, original schemas/native objects/order, recorded transports, actual five-page reader and every ZIP payload. Six in-memory changed-custody controls reject in both ordinary and optimized Python. It neither executes source programs nor proves the mathematics. `SOURCE_PRESERVATION.json`, `READ_LEDGER.md` and the research log make those boundaries explicit. Future additive source envelopes may be separately authenticated without changing this immutable historical packet.

The bounded adversarial assignment is complete at 100%. No source, prior packet, sibling review, shared/core/site/config/native/UI/Git state was modified by this lane. No outreach was prepared or initiated. Extensive AI use and unrefereed status remain explicit; conventional human peer review, formal certification and publication clearance are false. Root retains disposition/publication authority. The overall 203-paper programme remains ongoing; no follow-up is scheduled.
