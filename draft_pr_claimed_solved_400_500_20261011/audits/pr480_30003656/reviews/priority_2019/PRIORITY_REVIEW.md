# Independent priority review: PR480 / problem30003656

Reviewer assignment completed 2026-10-11, America/Los_Angeles
(2026-10-12 UTC). Frozen target: `EXACT_CLAIM.md` and the author-stage
`PROOF.md` / `SOURCE_GATE.md` for problem30003656. I did not read other new
priority-review conclusions. This report evaluates priority and scope, rather
than independently replacing the mathematical review families.

## Result and publication gate

**The full published Bezem–Coquand (2019) text has been obtained and read.
It does not explicitly give the candidate sentence or an explicit resolution
of the purely equational refinement.** Its detailed negative example uses a
binary relation and an existential axiom; its field and local-ring examples
also have non-equational axioms.

**Nevertheless, a claim that this is a first or newly established negative
resolution of the literal displayed algebraic question fails this priority
audit.** The already established excluded-middle argument applies immediately
to an equality formula in the purely equational pointed-object theory. A
checkable specialization is given below. It uses the prior general result,
not this PR's nonclassically valid sentence. Finding a paper explicitly
announcing the algebraic refinement settled is not necessary to recognize
this routine prior corollary.

The strongest narrower result available from this bounded review is:

* The candidate `alpha = not forall x notnot(x=c)` is not found in the primary
  full texts checked here, and is not the 2019 Skolem-choice counterexample.
* Its redundancy mechanism is already known: a model complete for geometric
  consequences may validate more first-order sentences than the generic
  model. The 2018 forcing machinery also already supplies the relevant
  all-maps versus injections setting and equality-completeness machinery.
* The candidate supplies a nonclassically valid equality-only sentence,
  conditional on the independent mathematical audits. Exact anticipation of
  that stronger particular statement was not located. **That absence does
  not certify novelty.**

Consequently this review does **not** authorize publication of a paper framed
as newly solving the literal open problem. A possible contribution consisting
of this particular nonclassically valid example would require an explicitly
different, narrower contribution claim, full credit to the prior machinery,
and the remaining independent checks. This conclusion does not claim that a
precisely formulated stronger version of the source question was previously
resolved.

## Exact target and candidate

The 2018 primary preprint, §7, internal p.26, asks whether every T-redundant
sentence is true in the generic model when T is algebraic, expressly meaning
purely equational. The preceding definition is preservation of all geometric
consequences after adding the sentence. It contains no displayed requirement
that the sentence fail classically. The 2017 OWR source was separately checked
by the parent; I rely here on my own full 2018 source, not on any other
reviewer's conclusions.

The candidate T has one sort, one constant c and no nonlogical axioms.
Write beta = forall x notnot(x=c), alpha = not beta. In the proposed genuine
generic model U on finite pointed sets with all pointed maps, beta and not
alpha hold. In the proposed model V on finite pointed sets with pointed
injections, alpha holds. Geometric reflection or the syntactic finite-quotient
argument establishes redundancy. A singleton pointed Set-model refutes
alpha, so alpha is not classically valid. These are the mathematical claims
audited by the other families, not assumed to imply historical novelty.

## Full published 2019 source: identity and provenance

Marc Bezem and Thierry Coquand, *Skolem's Theorem in Coherent Logic*,
Fundamenta Informaticae **170**(1–3) (2019), 1–14,
[DOI 10.3233/FI-2019-1853](https://doi.org/10.3233/FI-2019-1853).
Publisher metadata reports first online publication 2019-10-18. Thorsten
Altenkirch and Aleksy Schubert are special-issue editors, not additional
authors of this article.

The version of record is available in the author's public repository as
[`fi-170(1-3)02.pdf`, pinned to its 2019 commit](https://raw.githubusercontent.com/marcbezem/skolem/0b31294a66f90c3071d9f128e0e3972ce404bab3/fi-170%281-3%2902.pdf).
The [commit record](https://github.com/marcbezem/skolem/commit/0b31294a66f90c3071d9f128e0e3972ce404bab3)
is dated 2019-10-04T11:37:24Z and identifies the file as the PDF sent by
Fundamenta Informaticae. The PDF header has the correct volume, pagination
and DOI. The pinned PDF and current repository PDF have identical bytes:

`SHA256 5b040c354408db36489a72f6fccb1ef607f4d6ad97fed08bff96bf5f4cabc93a`

Size: 226247 bytes. First current-file retrieval:
2026-10-12T03:50:27.223236+00:00. Historical-pin retrieval and all response
details are recorded in `private_sources/retrieval_receipts_ninth.json`.

The earlier `FIversion.pdf` author draft has placeholder volume167 and
DOI ending1800. It is not the correct bibliographic version of record, even
though its mathematical text is closely aligned. The actual published PDF,
not that placeholder header, governs this review. Full text was read for all
14 pages; published pp.11–12 were additionally rendered and inspected.

Publisher requests originally returned403; the later browser publisher view
displayed restricted access. The institutional NVA record supplied metadata
but no associated source artifact. This access limitation was overcome by
the author's published-file deposit; no contact, login, purchase or outreach
was undertaken.

## Page and theorem comparison

| Primary result | Exact location | Scope and implication for this candidate |
| --- | --- | --- |
| Elimination of Skolem functions without equality | 2019 Theorem4.4, p.7 | Coherent conservativity machinery; no assertion about the equality-only algebraic refinement or this alpha. |
| Elimination of Skolem functions with equality | 2019 Theorem5.5, p.11 | Coherent conservativity after adding Skolem functions and equality congruence. Does not itself identify a purely equational T for the present target. |
| Four known redundancy mechanisms | 2019 §6.1, p.11 | Includes classically provable sentences and sentences true in another complete model. The candidate is an instance of the latter mechanism; it cannot claim the mechanism as new. |
| Propositional excluded-middle counterexample | 2019 §6.1, p.11 | Empty theory with propositional P and P or not P. Not an equality-only formula as written, but the stated general classical-conservativity principle immediately applies to equality formulas. |
| Skolem-choice counterexample | 2019 §6.1, p.12; also introduction formula(3), p.2 | T has binary P and forall x exists y P(x,y). Its noncoherent choice-coherence formula is classically valid but not generic. This T is not purely equational and the formula differs from alpha. |
| Algebraically closed fields | 2019 §6.2, p.12 | Equational rings plus field and closure axioms; not purely equational despite the word “algebraically.” Does not resolve the exact restriction. |
| Local rings | 2019 §6.3, p.13 | Equational rings plus nontriviality and local invertibility disjunction. Again not purely equational. |
| Equality-completeness of syntactic forcing models | BBC2018 Theorem5.11 and Remark5.12, pp.22–23 | Established machinery. With one constant and no operations, the listed constructor restrictions add no nontrivial axioms. The PR's proof should credit this route even if it supplies a self-contained proof. |
| Equality decidable in the renaming/injection model | BBC2018 paragraph after Remark5.12, p.23 | The text explicitly notes forcing of forall x,y (x=y or (x=y implies false)). This gives prior structural context for equality excluded-middle examples. |
| All-maps versus injections example | BBC2018 Example6.1, p.23 | Inhabited empty-signature example, with the Schanuel topos on the injections side. It is not the candidate pointed theory as stated, but the category comparison and mechanism are prior. |
| Generic double-negation identification | BBC2018 Example6.2, pp.23–24 | Empty theory with two constants; its generic bipointed object forces notnot(0=1). It is not the candidate quantified formula, but already exhibits the collapse-map mechanism. |
| Algebraic restriction explicitly left open | BBC2018 §7, p.26 | Defines algebraic as purely equational. Must distinguish the published wording from later observations that its literal reading permits excluded-middle answers. |

The 2019 p.12 sentence, in its two-variable context, is

    exists y1,y2 [P(x1,y1) and P(x2,y2)
                  and (x1=x2 implies y1=y2)].

Its universally closed version is displayed in the introduction. T' supplies
the witnesses yi=f(xi). A finite-graph site with relation-preserving maps
models the generic T and refutes the sentence. Neither this relational theory
nor its cover freely adjoining a P-successor is the pointed-object theory.

Simple substitutions do not recover the candidate: P(x,y) = (x=y) gives
constructive witnesses yi=xi, and P(x,y) = (y=c) gives yi=c. Thus the exact
alpha is not a routine substitution instance of this particular 2019
Skolem-choice counterexample. This is different from whether the underlying
complete-model method is already known: it is.

## Checkable prior corollary for the literal question

Take exactly the candidate purely equational T, and instead use

    epsilon = forall x [(x=c) or not(x=c)].

1. Classical logic proves epsilon. The known conservativity of classical
   logic for geometric consequences implies that epsilon is T-redundant:
   if T+epsilon intuitionistically proves geometric sigma, then T
   classically proves sigma, and hence T intuitionistically proves sigma.
   This mechanism is expressly recorded in 2019 §6.1 p.11, point2; the
   geometric/coherent relation is noted in its footnote2. Blechschmidt's
   independent primary treatment also expressly states the geometric-sequent
   version and the excluded-middle observation.
2. In the proposed genuine generic pointed object on finite pointed sets and
   all maps, choose A={c,a}, a distinct from c. At the identity arrow, a=c
   is not forced. The collapse A→{c} makes a=c true, so A does not force
   not(a=c) either. Since the presheaf coverage is trivial, A does not force
   their disjunction. Therefore the generic model does not validate epsilon.
3. T is purely equational and has a constant, so no issue about allowing empty
   Set-domains is involved. Epsilon is an original-language sentence using
   equality and c. There is no added predicate or relation axiom.

This is a routine specialization of an established general principle to the
same target class. It establishes why the bare yes/no question cannot be
advertised as newly settled by alpha. It is not evidence that the exact alpha
was previously written down, and it does not answer a strengthened question
requiring the redundant sentence to fail in some classical model. A claimed
solution to that stronger question would need its own precise statement and
priority assessment.

The 2018 authors' decision to display the algebraic question as open is a
real historical scope tension. It is not a reason to suppress the later
primary excluded-middle observation or to silently add a missing restriction.
The manuscript must make the tension explicit if it mentions the source
question.

## Later primary checks and exact remaining gaps

* Ingo Blechschmidt, [*A general Nullstellensatz for generalised spaces*,
  CT2019 slides](https://conferences.inf.ed.ac.uk/ct2019/slides/74.pdf),
  title page dated July9,2019. Notes to slide6 (PDFp.16) explain that excluded-middle
  instances in the language give trivial negative examples, and attribute
  the nontrivial negative general-coherent answer to BBC. They do not give
  the pointed alpha or explicitly classify the purely equational refinement.
* Blechschmidt's [current author-hosted rough draft](https://rawgit.quasicoherent.io/iblech/internal-methods/master/paper-qcoh.pdf),
  Introduction p.3, expressly applies classical conservativity to geometric
  sequents and says signature-level excluded-middle instances are redundant
  but typically not generic. It then distinguishes the BBC result excluding
  those trivial answers. The nearby paragraph supplies no precise additional
  restriction for the algebraic question. Current draft retrieval establishes
  present contents, not the date of every sentence; the dated 2019 slides are
  the historical corroboration used here.
* Henri Lombardi and Assia Mahboubi, [*Valuative Lattices and Spectra*,
  arXiv:2210.16558v3](https://arxiv.org/abs/2210.16558), revised2023-09-02,
  English §3.3, E19–E23, especially Theorem3.3.8 on E23 (PDFp.25): cites
  Bezem–Coquand2019 for Skolemized dynamical-theory conservativity. The
  relevant section was read in full; text searches locate no Wraith or
  pointed-object refinement claim. It supplies later use of the theorem,
  not an explicit resolution of this problem.
* Gilles Dowek and Benjamin Werner, [*A constructive proof of Skolem
  theorem for constructive logic*, arXiv:2305.10016v1](https://arxiv.org/abs/2305.10016),
  all four PDF pages read; Theorem1 on p.3 treats Skolem conservativity.
  There is no Wraith/algebraic-refinement discussion. The 2019 paper already
  cites its 2004 manuscript, so the2023 upload is not automatically evidence
  of a new post2019 discovery.
* Marc Bezem's [public site-model slides](https://marcbezem.github.io/CL-PC22/Site_CL.pdf),
  p.12, recap redundancy and known complete-model arguments and discuss
  Kock's local-ring property. No exact alpha was located. The related
  [Skolem slides](https://marcbezem.github.io/CL-PC22/Skolem_CL.pdf) have a
  title page dated Dagstuhl January8–12,2024 even though the repository is
  named CL-PC22; a repository name must not be used as a historical date.
  These slide checks are corroborative and bounded, not exhaustive paper
  reviews.
* The retrieval lead [*Geometrisation of First-Order Logic*](https://unige.iris.cineca.it/bitstream/11567/995798/4/Geometrisation-FOL.pdf)
  is by Roy Dyckhoff and Sara Negri. Introduction and reference/keyword
  screening show it concerns coherent conservative extensions and cites
  earlier Automating Coherent Logic work, not the2019 Skolem article. It is
  not an exact later algebraic-Wraith resolution; no conclusion of novelty
  is drawn from this limited screen.

Crossref, OpenAlex and Semantic Scholar citation retrievals were also saved.
Their citing-work lists are small and disagree. They are discovery aids,
not complete citation censuses. OpenAlex's two returned records were the
Lombardi–Mahboubi work and a classical-calculus normalization paper; the
latter has not been independently validated as a relevant2019 citation and
is not used for any mathematical or priority conclusion.

Recorded final queries include exact titles and combinations of Wraith,
algebraic, purely equational, redundant, generic model and pointed. The
queries `"Wraith" "algebraic" "redundant"`, `"Wraith" "purely equational"`,
`"Skolem’s Theorem in Coherent Logic" Wraith`, and
`"Wraith" "pointed" "generic"` were run2026-10-12UTC. No searched primary
full text explicitly gave alpha. Unindexed literature, unpublished work,
different notation, other stronger intended formulations and additional
citing papers remain genuine priority gaps. No person was contacted.

## Evidence custody and permitted conclusions

Private PDFs, extracted text, rendered pages, metadata responses and dated
retrieval receipts reside in this review's `private_sources/`. The generated
`SOURCE_MANIFEST.json` maps each retrieval to its URL, date, size and SHA256.
They are research evidence only and must not be copied into the public paper
or commit package. No Git, queue, PR, publication or spreadsheet mutation was
performed in this review.

**Established classification:** 2019 full-text gate resolved; no direct
anticipation of exact alpha found in the checked texts; general mechanism
already established; literal negative algebraic answer a routine prior
corollary; first-resolution publication framing rejected. **Remaining gap:**
novelty and significance of the stronger particular nonclassically valid
example, plus independent mathematical and precise-scope validation. A
bounded search is not a certificate of originality.

## Independent recommendation on repository classification

Using the human user's definition of `already_solved` to include a target
that was not actually open or a priority-audit issue, a **qualified status
repair to `already_solved` is justified for this literal target**. The
qualification must say that the displayed yes/no problem is already answered
by a routine consequence of published classical-conservativity and generic
model methods, with the explicit equality specialization proved in this
audit. It must **not** assert that an earlier publication explicitly printed
the exact pointed counterexample, recognized the algebraic refinement as
settled, or anticipated this nonclassically valid alpha; those historical
claims were not established.

This recommendation follows my own primary-text comparison and the
epsilon derivation above. The distinction matters because preserving
`claimed_solved` for an ostensibly new resolution and merely deleting
“first” would still misrepresent the novelty of the target outcome. The
stronger example may deserve separate research notes, but it is not a basis
for publishing this target as a newly solved open problem. I performed no
status repair or other repository mutation. Once the parent makes the
qualified classification repair, the user's rule requires skipping further
paper, merge, closure or comment processing for this PR.
