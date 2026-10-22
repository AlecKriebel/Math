"""Final reviewer-owned seal; run only after every public payload is settled."""
import hashlib,importlib.util,json,stat,sys
from pathlib import Path
from datetime import datetime,timezone
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;A=R.parents[1];P=R.parents[3];D=A/'publication'
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text())
spec=importlib.util.spec_from_file_location('review_acceptance_schema',P/'accept_pr938.py');ac=importlib.util.module_from_spec(spec);spec.loader.exec_module(ac)
prior=[]
for num,pin in [(1,'37feff8cb31bbef2b7f41b98d8f34571923e7a89cb4c8f53226ccd2adf388a91'),(2,'36a69cb090d28f33be92963bcf7a62ed2ce756d653c44f07d2f37cb468290716')]:
 f=A/'reviews'/('full_package_'+str(num).zfill(2));raw=(f/'MANIFEST.json').read_bytes()
 if sha(raw)!=pin:raise RuntimeError('Prior external review seal drift')
 records=ac.authenticate_review_records(f,json.loads(raw));prior.append(dict(round=num,external_manifest_sha256=pin,authenticated_payloads=len(records),adverse_verdict_preserved=True))
(R/'SEALED_HISTORY_CHECK.json').write_text(json.dumps(dict(utc=datetime.now(timezone.utc).isoformat(),status='PASS',prior_reviews=prior),indent=2)+'\n')
search=dict(utc=datetime.now(timezone.utc).isoformat(),queries=['"pure braids" "derived" "solvable" signature','"P_m" "n+2" "solvable" braid','"homogeneous" "quasimorphism" "derived" "signature" braids','"Pure braids, Whitney towers, and 0-solvability"'],primary_metadata=[dict(url='https://ems.press/journals/owr/articles/15955',verified='Corrected report container title, DOI10.4171/OWR/2017/50, volume14(2017), pages2987–3033, published19December2018 on article page'),dict(url='https://www.numdam.org/item/BSMF_2005__133_4_541_0/',verified='GG2005 identity/DOI/pages and ordinary link-signature subject')],primary_actual_bytes='SOURCE_PINS.json and ADDITIONAL_SOURCE_PINS.json',related_primary_checks=['CHH arXiv1003.4977v3 Example2.4/Proposition7.1','Kawasaki etal2025Lemma7.12 stronger general theorem','BK2015Proposition3.6 and pure example','Kuzbary2009.04641v2 Theorem1.1','DiPrisa–Framba published2025Theorem4.7/proof'],secondary_search_results_used_as_mathematical_proof=False,access_limits=['MSP XHTML metadata unsupported by web browser tool; actual primary PDF authenticated and inspected','Published CHH2012 bytes not newly authenticated; version-specific arXivv3 actual bytes checked','No exhaustive literature or forward-citation graph repeated; earlier broader search ledgers remain historical bounded evidence'],historical_conclusion='No complete predecessor established in inspected primary evidence; firstness/current-openness unverified and not asserted.')
(R/'SOURCE_SEARCH.json').write_text(json.dumps(search,indent=2)+'\n')
# Put actual recorded checkpoints in timestamp order; completion estimates may move.
p=R/'RESEARCH_LOG.md';parts=[x.strip() for x in p.read_text().split('\n\n') if x.strip()];events=sorted(x for x in parts if x[:4]=='2026');other=[x for x in parts if x[:4]!='2026'];p.write_text(other[0]+'\n\n'+('\n\n'.join(events))+'\n\n'+('\n\n'.join(other[1:]))+'\n')
freeze=load(D/'PREPUBLICATION_FREEZE.json');result=load(R/'RESULT.json');ac.validate_review_evidence(R,result,freeze,D)
allowlist=['RESULT.json','FULL_AUDIT.md','RESEARCH_LOG.md','AUTHENTICATION_START.json','AUTHENTICATION_END.json','COLD_REPLAY.json','INDEPENDENT_RECONSTRUCTION.md','SOURCE_PINS.json','ADDITIONAL_SOURCE_PINS.json','SOURCE_SEARCH.json','SEALED_HISTORY_CHECK.json','PACKAGE_AND_METADATA.json','PACKAGE_GUARD_CHALLENGES.json','COPY_GUARD_CHALLENGE.json','HELPER_MODE_SUMMARY.json','HELPER_CONTROLS_normal.json','HELPER_CONTROLS_O.json','HELPER_CONTROLS_OO.json','HELPER_CONTROLS_env2.json','ADDITIONAL_HELPER_CONTROLS.json','authenticate.py','cold_replay.py','run_replays.py','source_auth.py','additional_sources.py','render_sources.py','helper_controls.py','run_helper_modes.py','additional_helper_controls.py','package_evidence.py','finish_review.py','seal_review.py']
records={}
for n in allowlist:
 p=R/n
 if not stat.S_ISREG(p.lstat().st_mode):raise RuntimeError('Nonregular reviewer payload')
 raw=p.read_bytes();records[n]=dict(bytes=len(raw),sha256=sha(raw))
mapping=dict(utc=datetime.now(timezone.utc).isoformat(),pr=938,problem_id='30003634',candidate_revision=3,files=records,explicit_public_allowlist=allowlist,excluded=['MANIFEST.json (self)','private/**','raw third-party PDF/text/rendered source bodies','private target source body','unlisted scratch/log/output files','initial superseded unsealed HELPER_CONTROLS.json'],status='SEALED_REQUIRED_R6',subsequent_mutations_permitted=False)
# This final write settles the seal. No public or private mutations follow.
(R/'MANIFEST.json').write_text(json.dumps(mapping,indent=2)+'\n')
ac.authenticate_review_records(R,mapping)
print(json.dumps(dict(status='SEALED',manifest_sha256=sha((R/'MANIFEST.json').read_bytes()),public_payloads=len(records),required_issues=['R6'],optional_issues=[],all_prior_issues_resolved=True,mathematical_gap=None)))
