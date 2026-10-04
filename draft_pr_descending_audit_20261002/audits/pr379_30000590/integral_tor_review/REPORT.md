# Integral coefficient, Tor and flat quotient audit — PR379

Audited frozen head: `90794508688ec07f598e0871bbd1eb38aaf466ce`.
Target: `problems/30000590_group_ring_cohomology`.
Primary focus: complete Turns 3–4 proofs, integral products, coefficient
connecting maps, exact support, and flat duality quotient extensions.

**Conclusion:** no mandatory mathematical correction found in this assigned
scope. The strongest verified statements are the conditional integral product
Tor criterion, fixed-modulus coefficient criterion, flat-product and PD-factor
cases, and normal-extension closure with the explicit integral flat-duality
quotient hypothesis and full right action. The proposed **unsolved, 5/5**
disposition is consistent with these results. This is an AI-assisted audit,
not a full solution, historical novelty determination, human peer review, or
merge certificate. No broader verdict about every approach family is inferred
from this audit alone.

## Independence and exact source gate

The task instruction exposed mechanism names, source locators, and author /
historical control counts. That limited exposure is disclosed rather than
described as blind independence. Before any candidate proof, checker,
historical verdict, root verdict, or sibling verdict was read, I independently
fetched the literal EMS OWR PDF and companion published AGT PDF; read the
complete OWR contribution on printed 2588–2590; visually inspected those
pages; reconstructed the exact claim and integral controls; and sealed the
complete reconstruction, code and output at **2026-10-03T04:02:51.348311Z**.
The seal is `independent_pre_candidate_seal.json`.

After sealing I read the frozen manifest, all five complete proof files,
RESULT, complete author and historical checker/verifier code, source indexes,
relevant nested manifests, the historical review, and publication wrappers.
No root or sibling verdict was read. A later file inventory showed sibling
filenames only, with no sibling content inspection.

The literal question is total integral H*(Gamma;ZGamma), finite generation as
a **right ZGamma-module**, for Gamma virtually type FP. The regular coefficient
action used by cohomology is left; the right action commutes and descends.
Finite generation over Z or a cup algebra would be different statements.
The FP convention is a finite-length augmented resolution of the trivial
integral module by finitely generated projectives, not FP-infinity.

Source locators checked semantically:

| Source | Checked material | Meaning for this audit |
|---|---|---|
| EMS 46073 / OWR 43/2006 | Printed 2588–2590, PDF 10–12; visual inspection | Literal question and preceding right-module Coxeter filtration |
| AGT 6 (2006) 1289–1318 | Introduction; §§2–5 proof components; §7 base change | Left coefficients/right residual action; integral coefficient-system argument; associated graded, without right-module splitting |
| Sharifi Homological Algebra | Theorem 4.3.12 and actual proof, printed/PDF 97 | Additive Hochschild–Serre, functorial quotient action; old page 86 is incorrect |
| Brown's own group cohomology lectures | Definition 2.8 printed/PDF 11; dual-complex construction 25–27 | FP versus FP-infinity; commuting right action and duality mechanism |
| Davis Poincare duality survey | Printed/PDF 4–6 | Finite-resolution convention and finite-cd/filtered-colimit FP criterion used in Turn 4 |
| Davis–Okun published 2012 paper | Printed 529 / PDF 45, §9 | Integral duality convention includes torsion-free cohomology |

All six candidate-bound primary PDF byte hashes were independently fetched and
matched. This count is a byte verification count, not a claim to have read all
pages of all six PDFs. Davis's large 2024 book was byte-verified here; its
semantic locator correction is outside the core integral-Tor proof obligations
and is covered by the other assigned source audit. The original OWR/AGT and
Sharifi hashes match the pre-candidate downloads exactly.

The Sharifi statement and proof were inspected before candidate access, with
the printed/PDF 97 image checked subsequently. Its proof correctly uses the
N-invariants right adjunction to exact inflation. The printed proof has an
incidental domain notation slip in its first functor sentence; the adjunction
and intended quotient-invariants composition are unambiguous. The candidate
uses the actual theorem, not that slip. No new mathematical theorem is claimed
from this locator verification.

## Turn 3: exact integral criteria

At TURN_3 lines 15–68 the product resolution, finite projective dual model,
integral cohomological Kunneth sequence and right naturality are correct.
The tensor diagonal is i+j=n; the Tor diagonal is i+j=n+1. Each input has
finite cohomological support under the finite-length FP hypothesis, so every
sum and the total support are finite. The noncanonical abelian splittings
used to explain the formula are not promoted to right-module splittings.

The finite-generation equivalence assumes both factor cohomologies already
have the desired property. Under this assumption tensor terms have finite
pairwise generators. A finitely generated product module gives a finitely
generated **quotient** Tor term. Conversely, generators of tensor and Tor
terms lift to generators of the product module. This is the correct direction
and never assumes that an arbitrary submodule of a finitely generated group-
ring module is finitely generated. The missing general Tor finiteness claim
is explicitly retained at lines 70–72 and 194–202.

The fixed-field theorem at lines 76–108 includes its necessary nonzero-factor
detection. The bounded dual projective complex cannot be acyclic, because a
bounded acyclic projective complex splits and double duality would contradict
the trivial module's nonzero homology. A nonzero vector space then detects
the first-coordinate quotient. The theorem is for one fixed field and is
not used as an integral certificate.

The PD-factor shift at lines 112–125 is valid over Z, including the orientation
sign action. It gives finite-generation equivalence, not an integral-PD
recognition theorem from field coefficients.

At lines 129–163 the coefficient short exact sequence is integral and right
equivariant. The adjacent-degree kernel M_(i+1)[m] is the correct connecting
term. Reduction of the augmented integral resolution remains exact because
its abelian resolution of the Z-flat trivial module splits. The claimed
finite-generation equivalence assumes M_i is finitely generated, so M_i/mM_i
is finitely generated; it does not infer global integral finiteness from
every residue field or from every fixed modulus. The formula for a module N
killed by p, Tor^Z_1(M,N)=M[p] tensor_Fp N, is natural for both actions and
is correctly limited to the prime-annihilated case.

## Turn 4: quotient flatness, right action and support

The bounded Hochschild–Serre spectral sequence and exact filtered-colimit
comparison at TURN_4 lines 36–44 prove FP for the extension. Finite projective
resolutions of kernel and quotient make the two cohomology functors commute
with filtered colimits, including the quotient action. The uniform finite
rectangle is what permits passing this comparison to the abutment; finite
generation of arbitrary kernels is not assumed.

The cochain conjugation action at lines 48–81 gives a right G-action extending
the natural right N-action. The prism has the correct sign. The inner
coefficient action is retained: C_n induces right multiplication by n^{-1},
so C_{n^{-1}} induces the required right multiplication by n.

The bimodule identification at lines 85–115 is balanced, invertible and lift
independent. Changing a lift to n tilde(q) cancels by balancing. The left Q
action is regular on the first tensor factor, and the commuting right G
action is the displayed diagonal action. No homomorphic section is needed.

At lines 119–135 the correct integral cochain UCT is used: the additional
term would be Tor^Z_1(H^{p+1}(Q;ZQ),M_q). The explicitly assumed Z-flat D
kills it. Concentration without this flatness would not justify that step.
There is then exactly one occupied spectral column, hence one associated
graded term per total degree and no unproved splitting of a multi-piece
right-module filtration. The tensor map's naturality gives the full action
through the resulting isomorphism.

The split-tail argument at line 139 proves D finitely generated over ZQ,
without asserting that it is finitely generated over Z. The diagonal
generator calculation at lines 141–147 is correct: lift q, transport the
M_q coordinate by g^{-1}, express it using right N-generators, then multiply
by g. Finite support in q follows from cd(N)<infinity. These checks validate
the stated extension theorem with all of its hypotheses retained.

## New independent exact controls

`independent_controls.py` imports and reads no candidate code. Its complete
pre-candidate stdout has 281 JSONL records, including the final summary:

| Control family | Cases | Checkable evidence |
|---|---:|---|
| Integral tensor / Smith / Tor connecting | 144 | Integer differential matrices, unimodular V and V^{-1}, determinant -1, d1 V=(g,0), V^{-1}d0=(0,g), explicit Tor connecting class |
| Integral Bockstein | 96 | Actual lift d(1)/p and its order; p-square torsion distinguishes integral and reduced connecting maps |
| Shifted free flat factor | 36 | Explicit diagonal Smith matrices and degree shift, zero Tor |
| Noncommutative S3 residual action | 1 | Full left/right regular matrices; differential commutes with right action and fails the wrong left action/composition |
| Genuine C2 augmentation boundary | 1 | Full periodic maps, augmentation and nonzero top truncation kernel |
| Support / detection boundaries | 2 | Lower Tor degree and Prüfer p-kernel versus rational/mod-p quotient invisibility |

`post_candidate_mutant_controls.py` adds 262 full JSONL records: nine explicit
mutant rejections, 192 actual field-reduced differential/rank computations,
60 prime-annihilated Tor controls on mixed cyclic sums, and a summary. The
rejected mechanisms are zero Tor, wrong Tor diagonal, flat cochains implying
flat cohomology, rational tensor as an integral certificate, concentration
without dualizing flatness, substituting reduced for integral Bockstein,
support from only the tensor diagonal, treating a truncated periodic complex
as a finite augmentation resolution, and rational/mod-p quotient detection
of integral finite generation.

The scalar cochain and Prüfer controls are expressly algebraic models. They
are not claimed as H*(Gamma;ZGamma) realizations and give no original group
counterexample. In particular, their role is to falsify shortcuts without
transferring the central group-realization difficulty to an unsupported
claim.

## Frozen binding and full replay

All **56** frozen paths (55 target paths plus QUEUE) match the supplied head
manifest, by size and SHA-256. Relevant nested manifests verify, including
all 28 historical author bindings and the previous-manifest chain, the 40
final author entries, the additive correction, the seven historical review
entries, and the 54 publication entries. The review verifier also recomputes
all 43 recorded Git blob hashes directly from bytes; no Git command, index,
branch or remote operation was used by this audit.

All five author scripts were read completely and replayed, with full stdout
and stderr saved individually and stdout compared **byte for byte** with
each frozen receipt. Their counts are 300681, 46264, 79346, 83797, and 237015,
total **747103**. The historical independent script was also read completely
and replayed with full byte-exact stdout, **23463** assertions. Packet,
review and publication verifiers all completed with exit code 0; their full
streams are preserved. The portable historical review verifier truthfully
prints source_pdfs_reverified=false because it performs no source fetch;
the separate packet replay here uses the six freshly matched private sources
and prints source_files_checked=6.

These assertion counts are finite identity / support / normal-form controls,
not a measure of proof strength, novelty, or coverage of infinite groups.
Some author checks intentionally repeat simple identities. Their deterministic
replay supports reproducibility; the written arguments supply the infinite
claims. `full_replay_comparison.json` contains the complete parsed receipts
and exact stdout bindings, not just counts.

## Strongest result and exact gap

The integral criteria and the flat quotient extension theorem survive the
independent checks. They cannot be promoted to the original unrestricted
statement by dropping actual Tor, flatness, finite-length, or support
hypotheses. The final Turn 5 matrix is a bad finite matrix over a genuine
positive FP group ring, while its ambient group's own regular cohomology is
positive. It is not shown to arise as a differential in that group's dual
augmentation resolution.

The exact remaining gap is still to realize a non-finitely-generated
cohomology module in a genuine finite projective augmentation resolution of
an FP group, or prove that the augmentation constraints rule out all such
failures. A bounded literature search cannot establish the current global
status of the historical question or novelty. The packet's unsolved 5/5
label means that this packet supplies neither a general proof nor a genuine
cohomological counterexample. No extra author proof-search turn was taken.

All writes were confined to this audit's dedicated folder. Raw PDFs, text
extractions and renders are under ignored `private/`. No external individual
was contacted; no service, candidate file, repository index, branch or remote
was modified.
