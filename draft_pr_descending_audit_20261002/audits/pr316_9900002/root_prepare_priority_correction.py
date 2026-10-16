"""Prepare a reviewable correction only; perform no remote or Git mutation."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json

A = Path(__file__).resolve().parent
M = json.loads((A / 'snapshot_manifest.json').read_bytes())
T = M['target_prefix']
D = A / 'priority_correction_packet'
D.mkdir(exist_ok=False)
stamp = datetime.now(timezone.utc).isoformat()
sha = lambda b: hashlib.sha256(b).hexdigest()
pin = lambda b: dict(bytes=len(b), sha256=sha(b),
                     git_blob_sha1=hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest())
original = {}
for e in M['files']:
    b = (A / 'snapshot' / e['path']).read_bytes()
    if len(b) != e['bytes'] or sha(b) != e['sha256']:
        raise RuntimeError('Original changed: ' + e['path'])
    if e['path'].startswith(T + '/'):
        original[e['path'][len(T) + 1:]] = b
if len(original) != 18:
    raise RuntimeError('Unexpected original artifact count')
note = '''# Current priority correction for Thorisson Problem 1.2

Operational outcome: **already_solved by an exact corollary of classical renewal theory**. The submitted lacunary counterexample is mathematically valid, but the general negative answer should not be promoted as a novel resolution of an unsolved problem. No earlier author has been authenticated as explicitly announcing an answer to Thorisson's later named question. This classification records the checkable old-theorem implication, not a claim that Erickson explicitly discussed that question.

For ordinary renewal S_0=0, positive iid increments, N(t)=max{k:S_k<=t}, total life D_t=S_{N(t)+1}-S_{N(t)}, renewal function U(t)=sum_{k>=0}P(S_k<=t), and survival r(x)=P(X>x), the exact identity is

    P(D_t>x) = U(t) r(x),  x>=t.

Indeed the event is the disjoint union of {S_k<=t, X_{k+1}>x}. Each such jump passes strictly beyond t, including a jump starting at t. Independence and Tonelli yield the identity.

Erickson1970, Theorem5 (printedp265) and equation2.2 (p266), explicitly include the regular-variation index alpha=0. For a slowly varying tail r(t)->0 they give U(t)r(t)->1. The theorem uses U on [0,t] and includes the renewal at zero. Consequently, for every fixed M>=1, P(D_t>Mt)->1, so D_t/t diverges in probability.

If D_t/phi(t) has a proper finite weak limit for any eventually finite positive deterministic phi, tightness forces phi(t)/t->infinity. Otherwise a sequence with phi(t)<=Ct gives escape to infinity along that sequence. For any fixed positive a,b, eventually a phi(t),b phi(t)>t, and

    P(D_t>a phi(t))/P(D_t>b phi(t))
        = r(a phi(t))/r(b phi(t)) -> 1.

Since each probability is at most one, their difference tends to zero. The limiting survival probabilities therefore agree at every positive continuity point. Properness at infinity forces their common value to be zero. The limit is nonnegative, so it is zero almost surely. This covers atoms at zero, other atoms, every real inspection time tending to infinity, and oscillating positive scales; monotonicity of phi is unnecessary.

A completely elementary admissible example uses the continuous survival r(t)=1 for 0<=t<=1 and r(t)=1/(1+log t) for t>=1. It has density 1/[x(1+log x)^2] on x>1, is finite almost surely and non-lattice, and has infinite mean. Its truncated expectation M(t)=E[X 1_{X<=t}] obeys

    M(t) <= sqrt(t) + t/(1+(log t)/2)^2,
    M(t)/(t r(t)) -> 0.

For the first increment strictly exceeding t, its start T satisfies E[T]=M(t)/r(t) by geometric stopping and Tonelli. Markov gives P(T>t)->0, and on T<=t that increment is the straddling interval. Thus P(D_t>t)->1 and the exact identity establishes U(t)r(t)->1 for this example without invoking a Tauberian theorem. The proposed scale E[min(X,t)] is asymptotic to t r(t) and is eventually smaller than t, so this example also rejects that scale. Alternatively this follows directly from the submitted lacunary proof.

The submitted law remains a separate independently verified irregular example outside the regularly varying tail class. Its atoms have p_n=2^(-2^n) at a_n=2^(4^n). With q_n=sum_{k>=n}p_k, r(a_n/2)=q_n and r(a_n)=q_{n+1}, and q_{n+1}/q_n->0. A regularly varying tail would instead have a strictly positive finite factor-two ratio. Its construction and every-scale proof are valid; exact historical priority of this specific construction is unestablished. No assertion of firstness is made for it.

The independent current audits include the submitted Tonelli/Markov proof, a separate geometric count-of-failures argument, and a separate bounded-transform variance proof of the proper-limit obstruction. Root reproduced the author7852 and inherited646 exact controls, its separate6124 controls, and fresh263/1773 controls. These finite checks supplement the analytic infinite-quantifier proofs. The source-first priority audit and fresh adversarial classical-corollary reviews support the priority correction; their final bound reports must be accepted before this prepared packet is published to the PR.

Primary references: K. B. Erickson, *Strong renewal theorems with infinite mean*, Transactions of the AMS151 (September1970),263–291, https://doi.org/10.1090/S0002-9947-1970-0268976-9; Hermann Thorisson, *Open problems in renewal, coupling and Palm theory*, Queueing Systems68 (2011),313–319, https://doi.org/10.1007/s11134-011-9241-2. Original Erickson article pages were read and visually checked; the binary was obtained from a mirror after the official AMS endpoint returned403. The exact Thorisson definitions and Problem1.2 were checked in indexed institutional primary text; full original PDF binary/visual access remains unavailable. No copyrighted source PDFs are redistributed.

Bibliographic correction to the immutable historical SOURCE_GATE.md: the Angus–Ding2020 relative-age article is108745, DOI10.1016/j.spl.2020.108745, rather than108747. It addresses the relative-age ratio under regular-variation assumptions and is not itself the all-scale total-life theorem. The2015 three-page ratio preprint is by Blanchet, Glynn and Thorisson; Bingham, Goldie and Teugels wrote the separate1987 regular-variation monograph.

This is extensively AI-assisted research and independent AI-assisted verification, not human peer review or formal verification. Under the user's current claimed_solved-only workflow, after the operational status is corrected to already_solved this draft is left unmerged and no paper, Zenodo upload, DOI, tracker row or release is made. Historical author/review files and the1/5 author-turn count are preserved.
'''
(D / 'CURRENT_PRIORITY_NOTE.md').write_text(note)
status = json.loads(original['CURRENT_STATUS.json'])
status.update(utc=stamp, status='already_solved', original_submitted_status='claimed_solved',
              disposition='General negative answer follows from authenticated classical renewal asymptotics; valid independent lacunary construction retained',
              independent_review='Submitted mathematics PASS; operational classical-corollary priority correction awaiting final bound acceptance before branch publication',
              historical_novelty='General negative answer is an elementary consequence of Erickson1970 alpha0 theorem; no earlier explicit announcement answering the later named question authenticated; exact construction priority unestablished',
              current_priority_note='CURRENT_PRIORITY_NOTE.md', mathematical_acceptance=True,
              new_resolution_claim=False, preprint_ready=False,
              current_workflow_disposition='Leave draft unmerged after correction under current claimed_solved-only scope',
              paper=False, zenodo_upload=False, doi=None, tracker_row=False,
              fresh_probability_controls=263, fresh_normalization_controls=1773,
              root_independent_geometric_controls=6124,
              original_submitted_head=M['head'],
              historical_files='All15 original author and review artifacts byte-preserved; only three current presentation wrappers updated, with one additive priority note')
(D / 'CURRENT_STATUS.json').write_text(json.dumps(status, indent=2) + '\n')
readme = '''# Independent lacunary counterexample and classical priority correction

**9900002 / AMR-098-0002: already_solved by a classical-corollary priority audit; author1/5. Submitted counterexample mathematics PASS.**

The general negative answer to Thorisson Problem1.2 is an exact elementary consequence of the alpha-zero renewal theorem published by Erickson in1970. No earlier author has been authenticated as explicitly announcing the answer to the later named problem; the operational status records the proved implication. Read [the current priority note](CURRENT_PRIORITY_NOTE.md) for the complete proof, exact scope and source-access qualifications. [Current status](CURRENT_STATUS.json) is authoritative for this audited outcome.

The submitted [lacunary construction and complete proof](TURN_1.md) remain valid and byte-preserved. Their non-lattice infinite-mean law defeats every positive deterministic scale through asymptotic concentration at one atom along a deterministic time subsequence. The proposed truncated-mean scale escapes to infinity along that subsequence. The law is outside the regularly varying tail class, but historical priority of this specific example is unestablished. It is not presented as a new resolution of a genuinely open general question.

Root and distinct source-first independent reviewers checked the renewal probability proof, every-scale proper-limit argument, endpoint convention, arbitrary oscillating scales and possible limit atoms. Author7852 and inherited646 controls, root6124 checks, and fresh263/1773 controls passed; finite controls supplement the analytical proof. Historical [source gate](SOURCE_GATE.md), [author log](RESEARCH_LOG.md), [turn manifest](TURN_1_MANIFEST.json), and [inherited review](review/ADVERSARIAL_REVIEW.md) retain their original labels and bytes. The current note corrects the historical Angus–Ding article-number typo without rewriting that record. [Publication manifest](PUBLICATION_MANIFEST.json) binds all current accompanying files and records the original submitted hashes of these presentation wrappers.

This is extensively AI-assisted research and independent AI-assisted review, unrefereed and without human peer review or formal verification. Exact primary Thorisson Section1 text was checked in the indexed institutional source; full original binary/visual access was unavailable. Erickson's decisive primary article pages were visually verified using original-article mirror binaries. Raw source records and copyrighted PDFs are not redistributed.

The current workflow processes only claimed_solved PRs. After this priority correction changes the status to already_solved, the draft remains unmerged and receives no paper, Zenodo upload, DOI, tracker row or release. The adjacent relative-age, conditional joint-limit and coupling problems are unchanged.
'''
(D / 'README.md').write_text(readme)
manifest = json.loads(original['PUBLICATION_MANIFEST.json'])
manifest.update(current_status='already_solved', priority_classification='Exact classical-corollary implication; no authenticated prior explicit named-problem announcement',
                original_submitted_head=M['head'], utc=stamp,
                historical_author_review_files_preserved=15,
                original_current_wrapper_pins={n: pin(original[n]) for n in ['CURRENT_STATUS.json', 'README.md', 'PUBLICATION_MANIFEST.json']},
                current_wrappers=['CURRENT_STATUS.json', 'README.md', 'PUBLICATION_MANIFEST.json'],
                additive_files=['CURRENT_PRIORITY_NOTE.md'],
                claimed_only_scope_disposition='Leave draft unmerged after correction; no paper/publication/tracker')
for name in ['CURRENT_STATUS.json', 'README.md', 'CURRENT_PRIORITY_NOTE.md']:
    manifest['files'][name] = pin((D / name).read_bytes())
(D / 'PUBLICATION_MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
body = '''## Priority-corrected outcome: already_solved, author1/5

The submitted non-lattice infinite-mean lacunary counterexample and its every-scale proof passed extensive independent mathematical review. The current priority audit found that the general negative answer to Thorisson Problem1.2 is already an exact elementary corollary of Erickson's1970 alpha-zero renewal theorem. No earlier author has been authenticated as explicitly announcing the answer to Thorisson's later named question; this classification records the verified implication rather than such a historical claim.

For slowly varying tails r, the classical relation U(t)r(t)->1 and the exact identity P(D_t>x)=U(t)r(x), x>=t, show D_t/t diverges. Proper scaled convergence forces phi(t)/t->infinity; slow variation makes all positive limiting survival probabilities equal, and properness forces the limit to be zero. This excludes every positive deterministic scale, including nonmonotone ones and limits with an atom at zero. The current note also gives an elementary continuous-tail proof independent of Tauberian theory.

The specific submitted irregular lacunary example is valid and outside the regularly varying class; its exact historical priority remains unestablished. It is retained as an independent construction rather than promoted as a novel resolution of the general question. All15 historical author/review files and the1/5 author-turn count are preserved. Current README/status/manifest and one additive priority note make the correction visible throughout current presentation; the note corrects the historical Angus–Ding article-number typo.

Author7852, inherited646, independent root6124, and fresh263/1773 exact controls passed. Infinite-law and every-normalizer claims are supported by analytical proofs, not those finite controls alone. Original Thorisson hypotheses and Problem1.2 were checked in indexed institutional primary text; full original PDF binary/visual access remains unavailable. Erickson's relevant original article pages were independently visually verified, with mirror provenance disclosed.

Extensively AI-assisted research and independent AI-assisted verification; unrefereed, without human peer review or formal verification. Under the user's current claimed_solved-only scope, this priority-corrected already_solved draft is left unmerged, with no paper, Zenodo upload, DOI, tracker row or release. The distinct adjacent questions are not resolved.
'''
(D / 'PR_BODY.md').write_text(body)
(D / 'PR_TITLE.txt').write_text('9900002: verified lacunary counterexample; classical priority correction (already_solved1/5)\n')
receipt = dict(utc=stamp, status='PREPARED_REVIEWABLE_PRIORITY_CORRECTION_NO_REMOTE_MUTATION',
               pr=316, original_head=M['head'], packet=str(D),
               prepared_files={q.name: pin(q.read_bytes()) for q in sorted(D.iterdir())},
               changed_current_wrappers=['CURRENT_STATUS.json', 'README.md', 'PUBLICATION_MANIFEST.json'],
               additive_target_files=['CURRENT_PRIORITY_NOTE.md'],
               all15_historical_author_review_files_preserved=True,
               author_turns='1/5', proposed_status='already_solved',
               full_priority_acceptance_pending=True, corrected_packet_review_pending=True,
               branch_push_performed=False, paper=False, merge=False, publication=False)
(A / 'PRIORITY_CORRECTION_PREPARATION.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt, indent=2))
