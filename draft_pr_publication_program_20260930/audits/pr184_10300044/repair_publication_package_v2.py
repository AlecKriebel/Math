"""Additive publication correction; never rewrite the bound v1 or old reviews."""
from pathlib import Path
import datetime,hashlib,json,zipfile
A=Path(__file__).resolve().parent;OLD=A/'publication_package_v1';NEW=A/'publication_package_v2';NEW.mkdir(exist_ok=False)
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,j):p.write_text(json.dumps(j,indent=2)+'\n')
stamp=datetime.datetime.now(datetime.UTC).isoformat()
for n in ['taut_godbillon_vey.pdf','taut_godbillon_vey.tex','zenodo-deposit.json']:(NEW/n).write_bytes((OLD/n).read_bytes())
S=NEW/'supplement';S.mkdir();manifest=json.loads((OLD/'supplement/SHA256SUMS.json').read_text())
for x in manifest['files']:
 b=(OLD/'supplement'/x['path']).read_bytes()
 if len(b)!=x['bytes'] or sha(b)!=x['sha256']:raise RuntimeError('Old bound payload drift '+x['path'])
 p=S/x['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
readme=S/'README.md';text=readme.read_text();wrong='Mather--Moussu--Tsuboi 1981';right='Mizutani--Morita--Tsuboi 1981 (Annals of Mathematics 113(3), 515--527; DOI 10.2307/2006995)'
if text.count(wrong)!=1:raise RuntimeError('Expected unique current README correction')
readme.write_text(text.replace(wrong,right)+'\n\n## Version 2 bibliographic correction\n\nThe previous candidate expanded the initials MMT incorrectly in this README. The correct authors of the unread 1981 Annals paper are Tadayoshi Mizutani, Shigeyuki Morita and Takashi Tsuboi. See PRIORITY_CORRECTION.md for publisher metadata and the exact correction scope. The primary body remains unread; this metadata correction does not complete priority. The theorem, paper PDF/TeX, all executable controls and intended deposit metadata are unchanged. The first two whole-package reports and earlier candidate/native snapshots are preserved as dated custody history; their earlier PASS/pending statements do not override the required correction and subsequent fresh review. The corrected current package requires a new independent whole-package review before publication.\n')
correction='''# Priority-gap bibliographic correction

The unread 1981 Annals paper is by Tadayoshi Mizutani, Shigeyuki Morita and Takashi Tsuboi, *The Godbillon-Vey classes of codimension one foliations which are almost without holonomy*, Annals of Mathematics 113(3) (1981), 515--527, DOI https://doi.org/10.2307/2006995. Primary publisher metadata: https://annals.math.princeton.edu/1981/113-3/p04 (its page heading spells the title "Goldbillon-Vey"). Only publisher metadata was checked for this correction; no access to or reading of the article body is asserted.

The version1 current supplement README mistakenly expanded MMT as Mather--Moussu--Tsuboi. Version2 corrects that expansion to Mizutani--Morita--Tsuboi and provides the exact DOI. This is distinct from the correctly credited classical Mather--Thurston realization theory used in the proof. The archived suspension-priority report/addendum had already identified the correct authors. Unexpanded MMT1981 references in dated audit snapshots refer to this Mizutani--Morita--Tsuboi article. Historical candidate and reviewer snapshots are not silently rewritten.

This corrects one unread-source identification; it neither establishes historical firstness nor fills the article-body priority gap. The theorem, proof/PDF/source, code and exact deposit metadata are unchanged. All other version/access qualifications remain. A new whole-package adversary must review this corrected package before publication.
'''
(S/'PRIORITY_CORRECTION.md').write_text(correction)
entries=[{'path':str(p.relative_to(S)),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(S.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.json'];save(S/'SHA256SUMS.json',{'schema':'pr184.supplement.hashes.v2','self_excluded':True,'files':entries})
with zipfile.ZipFile(NEW/'verification-package.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
 for n in sorted([x['path'] for x in entries]+['SHA256SUMS.json']):
  info=zipfile.ZipInfo(n,(2026,10,13,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,(S/n).read_bytes())
(NEW/'README.md').write_text((OLD/'README.md').read_text().replace('# PR184 research-note publication candidate','# PR184 corrected research-note publication candidate v2')+'\nVersion2 corrects the supplement\u2019s unread1981Annals author identification to Mizutani--Morita--Tsuboi, DOI10.2307/2006995; no primary-body access or new priority clearance is claimed. The manuscript PDF/TeX, code and exact intended Zenodo metadata are byte-identical to v1. Earlier bound v1/native/reviewer snapshots remain historical. A new whole-package review of v2 is required before publication.\n')
outer=['taut_godbillon_vey.pdf','taut_godbillon_vey.tex','verification-package.zip','zenodo-deposit.json','README.md'];save(NEW/'REVIEW_PACKET_MANIFEST.json',{'schema':'pr184.whole-publication-candidate.v2','created_utc':stamp,'original_head':'fbd6561971368a0867df83453454427863d7f910','historical_priority':'unresolved','publication_ready':False,'files':[{'path':n,'bytes':(NEW/n).stat().st_size,'sha256':sha((NEW/n).read_bytes())} for n in outer],'supplement_payload_files_excluding_manifest':len(entries),'supersedes_packet_v1':sha((OLD/'REVIEW_PACKET_MANIFEST.json').read_bytes())})
repair={'UTC':stamp,'issue':'Wrong expansion of authors for unread1981Annals priority source','correct_authors':['Tadayoshi Mizutani','Shigeyuki Morita','Takashi Tsuboi'],'DOI':'10.2307/2006995','primary_metadata_checked':'https://annals.math.princeton.edu/1981/113-3/p04','primary_body_read':False,'v1_candidate_preserved':True,'v2_packet_manifest_sha256':sha((NEW/'REVIEW_PACKET_MANIFEST.json').read_bytes()),'unchanged':['paper PDF','paper TeX','all4 current controls','intended Zenodo metadata'],'changed':['current supplement README author identification','added current source correction','supplement hash manifest and ZIP','outer README and bound packet manifest'],'new_whole_package_review_required':True}
save(A/'GLOBAL_PUBLICATION_REPAIRS_01.json',repair);print(json.dumps(repair))
