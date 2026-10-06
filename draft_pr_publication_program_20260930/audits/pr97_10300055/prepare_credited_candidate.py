from pathlib import Path
import datetime, hashlib, json, os

A=Path(__file__).resolve().parent
old=A/'repaired_verification_candidate_v1'
new=A/'credited_verification_candidate_v2'
new.mkdir(exist_ok=False)
proof=(old/'CANDIDATE.md').read_text()
require=lambda c,m: None if c else (_ for _ in ()).throw(RuntimeError(m))
require(hashlib.sha256(proof.encode()).hexdigest()=='393241cc6299a7a8e7b9a2d72c22e48f574702e0f3c822e0310647a16e0ff4c7','Frozen mathematical candidate differs')
header='**Problem 10300055, AMR-102-0055, Calegari Question 13.2. Verified conditional argument with mathematical-audit repairs incorporated; priority and publication-package reviews pending.** This is an application of classical contact-topology theorems. Historical priority is unconfirmed, and this document has not undergone human peer review.'
replacement='**Problem 10300055, AMR-102-0055, Calegari Question 13.2. Mathematically verified classical argument, with the covering affine-deformation antecedent now credited.** Historical priority and the novelty of the explicit application or regularity extras remain unestablished. This document has not undergone human peer review, and no PR97 publication clearance has been granted.'
require(proof.count(header)==1,'Header anchor differs')
proof=proof.replace(header,replacement)
anchor='The source\'s conditional tightness question is fully addressed by this candidate. The construction or existence of any contact Godbillon–Vey form on a given foliation remains a separate question. We make no historical-priority claim. A related closed-defining-form deformation argument already appears in [DR, Proposition 3.4]; that proposition does not directly apply here because $\\alpha$ need not be closed.'
paragraph='''The source's conditional tightness question is addressed by this candidate under its standard smooth contact-form interpretation. The construction or existence of a contact Godbillon–Vey form remains a separate question. We make no historical-priority claim.

The affine contact mechanism is already covered by Dathe–Khoule [DK, Definition 2.1 and Theorem 2.2, pp.102–103]. In dimension three their criterion is $\\alpha\\wedge d\\omega+\\omega\\wedge d\\alpha\\geq0$; here it vanishes term by term. Their allowed choice $C(t)=1$, $B(t)=t$ gives $\\alpha+t\\omega$ and contact volume $t^2\\omega\\wedge d\\omega$. This is the same plane-field family as (3), after positive scaling and $s=1/t$. Their original proof is available as an author-uploaded full article transcription and the criterion is reproduced with explicit historical $C^1$ attribution in [KMNW, Theorem 6.2, pp.32–33]. We do not present this pencil as a new construction.

Ordinary smooth tightness is our stated corollary of the known affine mechanism, the Eliashberg–Thurston neighborhood theorem, and finite smooth Gray stability. The narrower near-foliation/isotopy argument already appears in [DR, Proposition 3.4], with a closed defining form. Neither inspected [DK] nor the relevant [KMNW] text explicitly states the exact conditional answer to Calegari Question 13.2. That bounded absence does not establish firstness. The exact extra $C^1$/$C^2$-disk conclusion checked here also has no established historical novelty. The final 2003 published Calegari chapter and other identified literature gaps remain unread; no equality with the 2002 source, current openness, exhaustive novelty or newly discovered historical resolution is claimed.

The normalized-equality display following [KMNW, Eq.(62)] drops a nonnegative mixed term in the general case; the correct general relation is an inequality. In our zero mixed-term specialization its equality is valid, independently confirmed by (3) and [DK]'s expansion. We use only this verified specialization, not an endorsement of the later preprint's unrelated results.'''
require(proof.count(anchor)==1,'Priority anchor differs')
proof=proof.replace(anchor,paragraph)
proof+='''
- **[DK]** H. Dathe and C. Khoule, *Sur les déformations d'un feuilletage de codimension 1 en structures de contact*, African Diaspora Journal of Mathematics **13**(2) (2012), 100–107. Definition 2.1 and Theorem 2.2, pp.102–103. [Public author-uploaded article transcription](https://www.researchgate.net/publication/258228980_Sur_les_deformations_d%27un_feuilletage_de_codimension_1_en_structures_de_contact); the original PDF pixels were not locally obtained. Publication year and author upload date (21 August 2026) are distinct.
- **[KMNW]** C. Khoule, M. Manso, A. Ndiaye and K. War, *C0-Contact Anosov flows*, arXiv:2503.00454v1 (1 March 2025), relevant Section 6, Theorem 6.2 and its proof, pp.32–33. [Primary preprint](https://arxiv.org/pdf/2503.00454v1). Only the relevant deformation/regularity statements are used; its unrelated main dynamical results were not audited.
'''
(new/'CANDIDATE.md').write_text(proof)
for rel in ['verify.py','review/independent_checks.py','review/author_replay/verify.py']:
    p=new/rel; p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((old/rel).read_bytes())
(new/'review/author_replay/CANDIDATE.md').write_text(proof)
record={'schema':'pr97-credited-candidate-preparation/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'operator_PID':os.getpid(),'parent_candidate_sha256':hashlib.sha256((old/'CANDIDATE.md').read_bytes()).hexdigest(),'candidate_sha256':hashlib.sha256((new/'CANDIDATE.md').read_bytes()).hexdigest(),'changes':['Covering Dathe–Khoule2012 criterion and 2025 primary reproduction credited','Known construction and our classical tightness corollary separated from an exact prior printed answer','Priority/access limitations made explicit; no novel historical resolution asserted'],'mathematical_derivation_changed':False,'verifier_sources_changed':False,'originals_or_v1_mutated':False,'priority_clearance':False,'publication_clearance':False,'new_central_proof_search_turns':0,'workflow_estimate_percent':30}
(A/'ROOT_CREDITED_CANDIDATE_PREPARATION_20261006.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))
