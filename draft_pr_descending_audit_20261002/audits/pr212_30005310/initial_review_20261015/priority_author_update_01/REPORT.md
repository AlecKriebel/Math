# Independent same-author update audit: PR212 / 30005310

**Recommendation: do not promote the present literal negative answer as a newly solved mathematical problem or novel preprint result. Apply an `already_solved` prior-coverage/credit correction under the literal numerical interpretation, or hold that promotion until it is reframed.** The frozen proof may still be a correct expository source correction; its own no-novelty disclaimer is appropriate. This audit makes no provider, tracker, PR, repository, or publication change. The parent retains the disposition decision.

The decisive prior result is Proposition 3.26, p. 13, of Roser Homs, Olga Kuznetsova and Bernadette J. Stolz, [*A computational approach to maximum likelihood thresholds for colored Gaussian graphical models*, arXiv:2609.02382v1](https://arxiv.org/pdf/2609.02382v1#page=13). Its four-cycle specialization already gives a negative answer to the literal numerical scenario classification. It precedes the candidate's October 1 date. This is **theorem coverage of the target**, not a finding that the authors explicitly announced a refutation of their OWR Conjecture 4, and not a finding that their paper anticipates the candidate's exact K4,4 construction.

## 1. Independence, scope and exact target

I first read the two original sources and reconstructed the colored-four-cycle calculation. Only then did I read the frozen candidate's PROOF.md, source_record.json, metadata.json, README.md and PUBLICATION_STATUS.md. I did not read or run the candidate's inherited independent review, its PASS reports, its verifier, or any other audit family's report. The supplied candidate head is `c697b4a5cc62f3b8836d8c37d82b71a1d1c53fb7`; this audit does not independently certify that Git head or the entire frozen tree.

The original [Homs/Kuznetsova OWR contribution](https://ems.press/content/serial-article-files/46992), printed pp. 3146-3149, defines a general colored linear concentration model and the rank-indexed symmetric-minor elimination ideals. Proposition 3 assumes `I(G,n+1)=0` and `I(G,n) != 0`. Each displayed numerical scenario has `MLT=n+1`. Its second bullet additionally has `WMLT=n` when the elimination variety meets the positive-definite sufficient-statistics cone. Conjecture 4 calls these cases exhaustive. The frozen cleaned target retains these numerical conclusions (and makes the second weak/ordinary threshold separation strict).

The frozen candidate uses singleton-colored K4,4, and a genuinely colored variant with K11=K22, to establish `I3 != 0`, `I4=0`, `WMLT=2`; it credits the singleton model's `MLT=4` to earlier work. Thus it attacks the proposed weak-threshold lower bound at n=3. The prior four-cycle attacks the proposed ordinary-threshold equality at n=1. **Different counterexamples refute the same universal numerical classification.** Exact anticipation of the eight-vertex example is unnecessary for that theorem-to-target implication.

The candidate explicitly excludes a repaired Boolean statement that only asks whether a strict signed SOS separator exists or the elimination variety meets the PD cone. That exclusion is correct and remains essential.

## 2. Primary-source identity and reading coverage

- OWR primary PDF: SHA256 `56e4555409c330099d6ff15cdda3f8b3d5415af067c1800b0aac846ca5701b65`. Read the complete contribution, printed 3146-3149, including definitions, both proposition bullets, figures, conjecture and references; visually checked all four pages using existing private renders.
- Homs/Kuznetsova/Stolz v1 primary PDF: 5,540,856 bytes; SHA256 `29727f7143ce6a7a92cf15dc80882e74590b7a3de66c42b50c31a4d94737e48d`. Read sections 1-3 in full, pp. 1-13, including every theoretical definition, statement and proof there; also discussion pp. 22-23, availability/acknowledgments, references pp. 24-26 and the colored-cycle table p. 27. Visually checked pp. 7, 8 and 13. I read part of the TDA exposition but did not reproduce its experiments or verify its algorithms; nothing in this conclusion relies on TDA.
- The current [arXiv primary landing page](https://arxiv.org/abs/2609.02382) was checked on 2026-10-15 UTC. It lists only v1, submitted **2026-09-02 09:57:00 UTC**. The PDF's title-page date is September 3. The [MCML institutional listing](https://mcml.ai/publications/hks26/) identifies the same September 2026 preprint. Exact-title, author/threshold and v2 searches found no later same-author update in the bounded search. This is a dated search observation, not an exhaustive priority certificate.

The 2026 model is explicitly a centered Gaussian concentration model; its projection uses the trace pairing, and Example 2.7 gives twice the edge entries. Proposition 3.9 equates generic completion rank to the first index with zero elimination ideal. Proposition 3.26 states `gcr=2` for equally vertex-colored cycles with distinct edges, and `mlt=1` for even cycles. Table 1's G12 supplies the precise four-by-four concentration matrix. In addition, the prose after Example 3.10, p. 8, explicitly recognizes probability-one MLE existence while the elimination ideal is nonzero. These are mathematical coverage and explicit recognition of the relevant phenomenon. The paper does **not** cite the OWR report or explicitly label its result a correction of that Conjecture 4.

## 3. Independent specialization, without relying on GCR terminology

Take the connected four-cycle with edges 12,23,34,41. Give all four vertices one color and each edge its own color. This is genuinely colored, with concentration space

```text
        [ lambda   a       0       d    ]
L_G = { [ a        lambda  b       0    ] : lambda,a,b,c,d real }.
        [ 0        b       lambda  c    ]
        [ d        0       c       lambda]
```

The identity matrix is in its positive-definite part. In the trace-pairing convention, write

```text
pi(S) = (tr(S), 2s12, 2s23, 2s34, 2s41)
      = (t0,t12,t23,t34,t41).
```

### 3.1 The exact OWR elimination conditions hold at n=1

The nonzero polynomial

```text
f = t12*t34 - t23*t41
```

belongs to `I(G,1)`: after replacing statistics it is four times the 2-by-2 minor `s12*s34-s14*s23` (rows 1,3, columns 2,4) of the full symmetric matrix. The defining ideal uses all minors, so this is an exact ideal-membership witness, not just a PSD observation. The polynomial is nonzero, for example at edge coordinates (1,0,1,0).

For `I(G,2)=0`, consider the polynomial map `F(X)=pi(XX^T)` from real 4-by-2 data matrices to R5. At `X=[e1,e3]`, its Jacobian has rank five. Taking columns in the order `x11,x21,x22,x42,x41`, the five-by-five minor is diagonal with entries 2,2,2,2,2, determinant **32**. Hence its image contains a real open set. Every polynomial in the exact symmetric-minor elimination ideal vanishes on this Gram image, and therefore vanishes on an open set and is the zero polynomial. This proves the first-zero condition directly, with no assumption that a statistical threshold equals a generic completion rank.

### 3.2 The ordinary and weak thresholds are both one

For any symmetric K in this space and any x in R4, direct expansion gives

```text
x1*(Kx)1 - x2*(Kx)2 + x3*(Kx)3 - x4*(Kx)4
  = lambda*(x1^2-x2^2+x3^2-x4^2).
```

The edge terms cancel because every edge joins opposite parts of the cycle. Set `D(x)=x1^2-x2^2+x3^2-x4^2`. If `Kx=0` and `D(x) != 0`, then lambda is zero. A PSD K with zero diagonal must be zero, since its 2-by-2 principal minors give `|Kij|^2 <= Kii*Kjj=0`. Thus no nonzero PSD K in L_G annihilates x.

Here is why that implies PD completion. The image of the PSD cone under pi is closed: its trace coordinate bounds the trace of any PSD preimage, and hence bounds that preimage; a convergent sequence of statistics therefore has a convergent PSD subsequence of preimages. A boundary point of this full-dimensional closed cone has a nonzero supporting functional. Under the trace pairing this functional is a nonzero PSD K in L_G. For `S=xx^T` the supporting equality is `tr(KS)=x^T Kx=0`, which for PSD K is equivalent to `Kx=0`. The preceding identity rules this out when D(x) is nonzero. Thus `y=pi(xx^T)` is interior. For sufficiently small positive delta, `y-delta*pi(I4)` is still in the PSD image; add `delta*I4` to a PSD preimage to get a PD preimage of y. The standard Gaussian likelihood criterion then gives MLE existence.

D is a nonzero polynomial, so its zero set has Lebesgue measure zero. Every nondegenerate centered Gaussian has a density on R4; therefore the MLE exists almost surely for one observation. Since sample size/rank zero cannot yield a PD statistic, **MLT=WMLT=1**. This is the m=4 specialization of the prior proposition, independently checked.

The positive-probability conclusion can also be made directly quantitative. Near x=e1, use a symmetric completion Q with equal diagonal `||x||^2/4`, cycle entries `xi*xj`, and other entries zero. If each coordinate differs from e1 by less than 1/100, its diagonal exceeds each row's off-diagonal absolute sum by at least `8993/40000 > 0`. Q is PD throughout this open box, and x is nonzero there. This is a positive-probability success set, not an isolated rank-one witness.

An adversarial boundary control is x=(1,1,1,1). The nonzero cycle Laplacian has diagonal 2, edge entries -1, is PSD by `z^T K z=sum_edges(zi-zj)^2`, and annihilates x. Thus there really are exceptional failure samples; they do not invalidate almost-sure existence. No claim of existence for every rank-one sample is being made.

### 3.3 The bare PD-intersection case actually holds

Set `S=e1*e1^T` and `Q=I4/4`. Then S has rank one, Q is PD, and both statistics are `(1,0,0,0,0)`. Consequently `pi(Q)` lies in `V(I(G,1))`. Every ideal polynomial vanishes at this PD point, so no polynomial in that ideal can give an everywhere nonvanishing signed-SOS separator on the PD Cholesky domain.

The prior example satisfies B and fails its claimed threshold conclusion. It therefore refutes both **numerical** scenarios, since at n=1 they both demand MLT=2. It does **not** give a case where neither A nor B holds. This logical distinction is unaffected by choosing different generators or by the SOS representation's strictness.

## 4. Assumption and interpretation challenges

| Challenge | Check and consequence |
|---|---|
| GCR might not equal the first zero elimination index | Proposition 3.9 states that equality in the update, but the explicit minor and real submersion above independently prove the two exact OWR ideal conditions. No GCR/MLT equality is used. |
| Real PSD image versus complex symmetric determinantal variety | The nonzero ideal witness is a literal symmetric minor. The zero-ideal proof only uses that every eliminated polynomial vanishes on a real open Gram-statistics image; no claim that every real low-rank symmetric matrix is a Gram matrix is needed. |
| Fixed versus estimated mean | The update starts with a centered Gaussian and n independent observations, using S=(1/n)XX^T. All arguments use rank and positive scaling. Estimating an unknown mean changes the observation/rank relationship and would require restating the target; it does not rescue this rank-indexed statement. |
| OWR edge statistics omit the factor two | The conventions differ by an invertible diagonal transformation of output coordinates. Fibers, intersection, zero/nonzero ideal status, and thresholds are invariant. The unscaled-edge Jacobian minor is 2 rather than 32; both are nonzero. |
| General colored graph might exclude the example | This graph is connected, has a genuine four-way vertex equality, distinct edge colors, a feasible identity concentration matrix, and no shared vertex/edge colors. It fits both primary definitions. It also fits a restriction to colored four-cycles. |
| A special rank-one point might not establish WMLT | The open completion box and the Gaussian density argument establish positive probability, while the alternating identity proves almost-sure existence. |
| A published statement might contain a proof gap | The numerical conclusion is independently derived above. The ambiguous extracted inequality was checked in the PDF: it is the valid entrywise bound lambda_1 >= abs(lambda_i). The specialization does not rely on the paper's displayed general-cycle GCR construction. |
| The cleaned question might differ from the original | The cleaned second scenario has a strict threshold separation; the original already fixes MLT=n+1. Our example contradicts that original equality, so the negative answer does not depend on the cleaning. |

## 5. What is prior-covered, and what is not

1. **Literal universal numerical classification: covered negatively before the candidate.** The September same-author theorem supplies a genuinely colored four-cycle with `I1 != 0`, `I2=0`, `WMLT=MLT=1`. A general K4,4 counterexample is not required to settle this target. A four-cycle-only numerical interpretation is covered as well.
2. **Explicit earlier recognition: partly explicit, partly an independently supplied implication.** The update expressly recognizes nonzero elimination ideals alongside probability-one existence and proves its cycle family. I found no explicit OWR-Conjecture-4 citation, refutation claim, or replacement theorem formulated as a complete repair of the original dichotomy. Calling the original conjecture explicitly retracted would go beyond the read sources.
3. **An additional original-source warning:** the OWR Figure 2, printed 3147, already reports WMLT=MLT=1 for its all-vertices-same-color four-cycle after adding vertex symmetries. Its natural unchanged-edge reading appears to be this model, so the original report may already display the relevant threshold phenomenon. The audit does not rest a priority conclusion solely on a black-edge drawing convention; the 2026 explicit theorem, concentration matrix and independent ideal calculation suffice.
4. **Exact K4,4 / K11=K22 anticipation: not established here.** I found no such construction in the read same-author theory or conclusions. Section 3.2 mentions an older uncolored K5,5 gap, but this audit does not inspect or certify that separate literature family. The correctness and provenance of the candidate's exact eight-vertex construction remain separate questions.
5. **Repaired bare SOS-versus-PD-intersection question: not settled by either example.** Each has an actual PD intersection. A failure of the numerical threshold assertions is not a counterexample to the bare union A-or-B.
6. **Complete priority certification: not established.** This was a bounded same-author primary-source audit. No negative search result is promoted to a proof that no other earlier construction exists.

The frozen candidate already calls itself a source correction/classical consequence and disclaims novelty. That is consistent with this audit. What must change is any interpretation of `claimed_solved` as a new mathematical solution for this campaign and any stale statement that the literal numerical target remains open. The candidate's limited statement that its own eight-vertex example does not settle a four-cycle restriction is accurate; the literature context should add that the September theorem does settle that numerical restriction. A credit/provenance record can explain the prior counterexample and retain the elementary K4,4 exposition. If a genuinely new preprint is desired, an additional separately stated and verified contribution is needed. There is no remaining mathematical gap in the narrow prior-coverage implication proved here.

## 6. Checkable artifacts and seal

`CONTROL.py` is an independent Python-standard-library checker. It verifies the exact five-output Jacobian minor, unscaled-coordinate minor, PD witness, alternating polynomial identity, explicit open-box margin, and a balanced exceptional failure. `CONTROL_RESULTS.json` records PASS and binds the code hash. Its finite vector controls are sanity checks; the universal identity is checked symbolically, and the probability/null-set argument is in this report.

The authored manifest lists only this audit's report, code, results, source-verification receipt and research log, with relative path, byte count and SHA256. Private primary payloads and page renders are excluded and were not copied here. The final seal binds that manifest; the manifest and seal self-exclusions are explicit. All written files are inside the authorized `priority_author_update_01` directory. No external communication, outreach preparation, Git/index/ref, database, queue, PR, provider, deposit or tracker mutation occurred.
