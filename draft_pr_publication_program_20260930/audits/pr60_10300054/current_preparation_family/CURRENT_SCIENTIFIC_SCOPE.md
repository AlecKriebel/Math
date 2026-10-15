# PR60 current qualified partial result

**Disposition: unsolved, original 1/5; new attempts 0, audit increment 0, novelty credit 0.** The accepted deliverable is a qualified smooth gauge/form/transport partial result. Calegari Question 13.1 is unresolved by this candidate. No preprint, DOI, claimed solution, or eligible counterexample is prepared.

## Literal target and conventions

Calegari's 2002 Question 13.1, printed p29, asks whether a minimal taut C² foliation of an atoroidal 3-manifold with nonzero Godbillon–Vey pairing has a defining pair with omega wedge d omega everywhere nonnegative or everywhere nonpositive. Zero loci are allowed. The adjoining four remarks distinguish excluded torus/nonminimal splicing examples and the stronger contact condition from this target. The global defining-pair analysis assumes coorientation and a closed oriented manifold; it does not use those conventions to assert a solution of the original C² question.

The original source_record and all17 science/support bodies are retained byte-for-byte at original_preparation_family/original, authenticated at head 1e762651b698c1fb519901bd924c5bd3717cc5ef. The original frozen SOURCE has170 indexed bodies plus itself171; both fresh families are bound separately. This folder copies no original science, queue row, bulk corpus, full primary paper, or family index.

## Verified smooth deductions

For a smooth nowhere-zero global alpha and smooth omega with d alpha=alpha wedge omega, differentiation gives alpha wedge d omega=0. All smooth defining forms with the same coorientation are alpha_f=exp(f)alpha. Their auxiliaries are beta=omega-df+h alpha_f. The original coefficient convention is beta=omega-df+g alpha, where g=exp(f)h; mixing these conventions would change the apparent mixed term.

The exact transgression is

    beta wedge d beta
      =omega wedge d omega-df wedge d omega+dh wedge d alpha_f
      =omega wedge d omega+d(-f d omega+h d alpha_f).

Equivalently, its primitive in the original-coefficient convention is g d alpha-f d omega+g df wedge alpha. Stokes preserves the total integral on a closed oriented manifold. Boundary terms require separate treatment; an arbitrary exact top-degree representative is not automatically realizable by this constrained gauge map.

Choose a smooth positive volume form nu and define v, Y and X_f by omega wedge d omega=v nu, i_Y nu=d omega, and i_X_f nu=d alpha_f. Both fields are tangent and divergence-free. The operative explanation is d(d omega)=0 for Y and **d(d alpha_f)=0 for X_f**. In the global family's fixed-alpha notation, i_W nu=alpha wedge omega=d alpha, so **d(alpha wedge omega)=d(d alpha)=0**. The frozen global proof's phrase d(d omega) in that W explanation is superseded by the exact standalone PROOF_PRECISION_QUALIFICATION.md copied here, SHA ca2aab8ea6ee158fe562963abe48bb031e00377a21088fc38a693685575db141. Frozen historical bytes and their controls remain unchanged; this correction changes no resulting identity.

The density becomes v-Yf+X_f(h). For a fixed smooth f, every X_f-invariant probability annihilates X_f(h). A necessary weak-sign condition is that every such measure integrate v-Yf nonnegatively. Positive normalized-volume average checks only one invariant measure.

For any smooth complete flow on a closed manifold and smooth forcing b, strict positivity of every invariant-probability average is equivalent to existence of a smooth correction u with b+X(u)>0. Compactness of all invariant probabilities yields a uniformly positive finite time average. The explicit weighted integral u_T=(1/T) integral_0^T (T-t)b(Phi_t x)dt has X(u_T)=-b+A_T b. Nonnegative averages are equivalently sufficient for every approximate inequality b+X(u_delta)>=-delta. They do not establish exact weak-sign attainment.

The abstract Liouville-flow examples demonstrate failure of unrestricted attainment inference, including a variant with no distributional solution. They are torus transport diagnostics with zero mean, not realizations of the minimal taut atoroidal nonzero-GV target. Fixed-gauge negative invariant averages do not prove failure of every rescaling. Strict positivity would force a nowhere-zero tangent field and vanishing Euler class; zeros leave the weak-sign target open.

## C² regularity and exact gap

The fresh form family proves a controlled weak extension for alpha C¹, continuous omega with continuous weak d omega, and C¹ gauge functions. A cooriented C² foliation atlas admits such a pair by patching local transverse differentials and continuous auxiliaries. This does not classify every admissible low-regularity auxiliary or reduce the entire original question to smooth gauges. A nonnegative density with zeros need not survive approximation. No smoothing or sign-preserving upgrade is assumed.

No proof selects f globally from minimality, tautness, atoroidality and nonzero GV so that all required invariant inequalities hold. Even nonnegative averages require an additional exact weak-attainment argument. No actual target foliation defeating every gauge is constructed. The original C² pointwise question therefore remains unresolved. These are the exact gaps, not a presumed absence of a later literature result.

## Evidence, attribution and reading limits

ROOT's actual scientific adjudication,17370B SHA f3c4abd127129cb2488921b23f95afe504791f6908c713cfd7d04fda34b1a0d5, written by PID67075 at 2026-10-03T18:30:14.586276+00:00, accepts the qualified partial result and expressly preserves unsolved1/5/new0/audit0. ROOT personally read the original OBSTRUCTION/verify source, both fresh universal reports/derivations/regularity and the literal primary Q13.1 plus all four remarks. Separate genuine SOURCE custody does not itself constitute mathematics approval.

Fresh forms: universal PROOF/REGULARITY plus78 independent coordinate assertions and an actual61-check author replay. Fresh global: universal transport/small-divisor derivation plus76 corrected exact Fraction assertions. Historical original61/reviewer209, earlier float-promoted transport run and failed bookkeeping capture remain preserved. This preparation reruns none and earns no new mathematical review credit. Finite controls are evidence of finite identities; the universal deductions rest on the written proofs, with the gaps above retained.

Primary attribution: Calegari2002 Q13.1 ([official arXiv](https://arxiv.org/abs/math/0209081)); Hurder–Langevin and Hurder–Katok bounded regularity passages were read by the fresh form family. This preparer reread Q13.1/all4 remarks at existing private extracted-text LF1377–1413, printed29, not the entire paper or the full regularity literature. No new primary download, exhaustive priority certificate or earliest-solution claim is made. Raw prior is PRESENT, direct upstream OPEN-TRIAGE dict, SQL TEXT988B; it is not ABSENT or literal{}. Full raw/PDF/text remain private in place; current helpers need no corpus or private primary cache.

Extensive AI assistance; unrefereed and without human peer review or formal verification. Prose CC-BY4.0, authored verification code MIT. Current folder readiness is source preparation only; current ROOT custody/readback remains pending, with no native/Git/PR/remote acceptance mutation.
