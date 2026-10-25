from pathlib import Path
import json,hashlib,zipfile,zlib,datetime
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024'); B=P/'papers/23441617'; R=B/'reviews/root'
sha=lambda b:hashlib.sha256(b).hexdigest()
def info(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':sha(b)}
def load(p):return json.loads(p.read_text())
bindings={}
def check(p,v):
 p=p.resolve();a=info(p)
 assert a['sha256']==v['sha256'] and a['bytes']==v['bytes'],str(p)
 bindings[str(p.relative_to(P))]=a
manifests=[(B/'sources/SOURCE_MANIFEST.json','files',B/'sources'),(B/'reviews/scope/MANIFEST.json','files',None),(B/'reviews/analytic/MANIFEST.json','portable_files',P),(B/'reviews/adversarial/FINAL_MANIFEST.json','files',B/'reviews/adversarial')]
for m,k,base in manifests:
 for v in load(m)[k]:
  p=Path(v['path']);check(p if p.is_absolute() else base/p,v)
 bindings[str(m.relative_to(P))]=info(m)
seal_expected={'sources/SOURCE_SEAL.json':'24ae37faf178b1fbc08883239d2470c27d219e65f234bffa52f33bcf0616c5bb','reviews/scope/SEAL.json':'07bc10be743457c0d7c89c8d8949472e5a18c8b7d996251e528ea951131fca32','reviews/analytic/FINAL_SEAL.json':'23a03d6e909f92f03bf2a21aa095e85d9e64b9b20f9ec80a6aaf4733ed5072cf','reviews/adversarial/FINAL_SEAL.json':'04d5755dcf9bda962894efc17c6768f4b5dfb87ad6cc4aa7f7898887b295bc48'}
for r,h in seal_expected.items():
 p=B/r;assert info(p)['sha256']==h;bindings[str(p.relative_to(P))]=info(p)
s=load(B/'sources/SOURCE_READY.json');raw=load(B/'sources/record.raw.json')
assert s['record_id']==23441617 and s['version']=='1.0'
assert len(s['all_assets'])==2
for a in s['all_assets']:
 p=Path(a['path']);b=p.read_bytes();assert len(b)==a['bytes'] and sha(b)==a['sha256'] and hashlib.md5(b).hexdigest()==a['md5']
 assert a['original_api_file_object'] in raw['files'];assert a['original_api_file_object']['checksum']=='md5:'+a['md5']
arc=load(B/'sources/archive-members.json'); members={x['member']:x for x in arc['members']}
assert len(members)==118 and arc['nested_archive_count']==0
zpath=next(Path(x['path']) for x in s['all_assets'] if x['path'].endswith('.zip'))
with zipfile.ZipFile(zpath) as z:
 zi=[x for x in z.infolist() if not x.is_dir()];assert len(zi)==118 and len({x.filename for x in zi})==118
 for x in zi:
  assert not x.filename.startswith('/') and '..' not in Path(x.filename).parts
  assert not x.flag_bits&1 and (x.external_attr>>16)&0o170000!=0o120000
  b=z.read(x);m=members[x.filename];assert len(b)==m['bytes'] and sha(b)==m['sha256'] and f'{zlib.crc32(b)&0xffffffff:08x}'==m['CRC32']
  assert Path(m['extracted_path']).read_bytes()==b
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
receipt={'utc':utc,'status':'ROOT_RECHECKED_ALL_CURRENT_SOURCE_FINAL_FAMILY_AND_PRIOR_BOUND_CUSTODY','unique_bindings':len(bindings),'bindings':bindings,'known_final_seals':seal_expected,'actual_public_API_assets':2,'original_archive_member_occurrences_compared':118,'source_schema':'all_assets/original_api_file_object/lowercase md5 and sha256; original objects preserved','originals_modified':False,'overall203_goal_complete':False}
cp=R/'custody-recheck-20261025.json';assert not cp.exists();cp.write_text(json.dumps(receipt,indent=2)+'\n')
text='''# Root scientific disposition: real-complement modulus

The complete original seven-page v1.0 theorem is supported under the manuscript's explicit whole-plane, pointwise-Borel, every-curve convention. This is a bounded AI-assisted mathematical review; it is not human peer review or formal certification. No substantive proof gap was found. The only confirmed error is the noncentral citation-volume typo in reference [4]: Heinonen–Koskela is Acta Math. **181** (1998), not 180. Its title, authors and DOI identify the correct credited source. The archived PDF and ZIP remain unchanged.

I read the actual full seven-page published manuscript and controlling TeX and sealed my substantive reconstruction before current reviewer opinions and foreign primary bodies. I have now read all three complete final family reports and their custom verdicts, together with the analytic full derivation. My own early proof remains in initial-reconstruction.md. The universal claim, not a narrower substitute, is adopted: for every compact E in [0,1], with F the real complement, positive planar 2-modulus of every connector to the radius-two circle implies infinite modulus to F. Both consistently local-off-endpoint and globally rectifiable conventions survive; intermediate plate contacts are allowed.

The pointwise lsc majorant preserves infinite null-set values. Weighted-length compactness uses its lower bound one, compact E and bounded path lengths. The actual potential is Borel, ACL and Sobolev; its actual trace is the characteristic function of E. A Fourier trace estimate without zero-frequency division and the telescoping translation argument force length(E)=0. This is not a capacity conclusion. The separate polar-circle argument works at every fixed actual endpoint, obtains a liminf subsequence of radii, uses first exits and localization to obtain finite arclength, and contradicts finite separator cost without discarding any null endpoint or exceptional curve. Scaling the infinite-cost outer separator establishes the contrapositive. Empty, singleton, positive-length-without-interval and null positive-capacity cases are retained.

I read the actual critical Hayman–Lingham Problem 7.58 interface at PDF179, actual Brezis pages1–3, DNPV's relevant Fourier/Gagliardo/trace statement contexts, Heinonen–Koskela's first-page and all-curve/majorant/weighted-potential interfaces and Hesse's Theorem5.5 and proof context. The exact raw images inspected are retained in tmp/pdfs/root-primary-interfaces-20261025. These reads authenticate classical context and the minor volume defect. I do not claim to have read entire long primary books/papers, the full 2019 Springer problem page, the original 1982 Goldstein–Jackson talk body, or the entire historical alternative condenser argument. Hesse's compact-plate continuity is not extended to a touching open complement. The current direct proof avoids that import.

The mathematical mechanisms receive classical credit, including Gonchar via Vuorinen/Hayman–Lingham, Fourier/Sobolev trace and critical rigidity via DNPV/Brezis and mediated predecessors, and upper-gradient/potential background. An authenticated 1982 title and a finite 2021 update list cannot establish priority or present openness. No historical firstness, current worldwide openness, independent-discovery or new-mechanism claim is approved. No follow-up meets the programme's high bar on this evidence.

The accompanying root custody receipt independently rehashes every bound current source/final family object and fixed prior object in those manifests, all original API file objects and both actual assets, and compares all118 original ZIP members/CRCs/extracted bytes. This does not turn the archive integrity replay into a theorem certificate. No source repair occurred. The minor citation defect belongs in the native notes and any public prior-work reference should use the authenticated volume181. Scientific review is complete; editorial, rendered, deployment, browser/download and native URL gates remain separate. Overall203-paper goal remains active.
'''
rp=R/'ROOT_REVIEW.md';assert not rp.exists();rp.write_text(text)
reviews={}
for lane in ['scope','analytic','adversarial']:
 d=B/'reviews'/lane;reviews[lane]={'report':str((d/'REPORT.md').relative_to(P)),'report_sha256':info(d/'REPORT.md')['sha256'],'verdict':str((d/'verdict.json').relative_to(P)),'verdict_sha256':info(d/'verdict.json')['sha256']}
out={'utc':utc,'record_id':'23441617','status':'PASS_WITH_NONCENTRAL_BIBLIOGRAPHIC_DEFECT','disposition_by':'root','reviewed_zenodo_version':'1.0','publication_date':'2026-10-17','record_created_utc':s['created'],'actual_complete_published_manuscript_read':True,'all_complete_final_family_reports_and_verdicts_read':True,'approved_scope':'Complete original all-compact, all-endpoint, all-curve real-complement modulus theorem under both consistent stated curve conventions. Direct majorant/potential/trace/rigidity plus separate null-endpoint circle proof; no touching-plate identity, firstness or present-openness certification.','root_review':str(rp.relative_to(P)),'root_review_sha256':info(rp)['sha256'],'root_custody_receipt':str(cp.relative_to(P)),'root_custody_receipt_sha256':info(cp)['sha256'],'reviews':reviews,'source_receipt_path':str((B/'sources/SOURCE_READY.json').relative_to(P)),'source_receipt_sha256':info(B/'sources/SOURCE_READY.json')['sha256'],'source_receipt_schema':receipt['source_schema'],'metadata_path':str((B/'sources/normalized-metadata.json').relative_to(P)),'metadata_sha256':info(B/'sources/normalized-metadata.json')['sha256'],'raw_record_path':str((B/'sources/record.raw.json').relative_to(P)),'raw_record_sha256':info(B/'sources/record.raw.json')['sha256'],'source_tex_path':str((B/'sources/published-source/manuscript/main.tex').relative_to(P)),'source_tex_sha256':info(B/'sources/published-source/manuscript/main.tex')['sha256'],'pdf_sha256':s['all_assets'][0]['sha256'],'supplement_sha256':s['all_assets'][1]['sha256'],'seal_bindings_rehashed':len(bindings),'original_archive_member_occurrences_compared':118,'substantive_mathematical_defect':False,'noncentral_bibliographic_defect':{'location':'PDF7 reference[4]; controlling TeX442','printed':'Acta Math.180','correct':'Acta Math.181(1998),1–61','DOI':'10.1007/BF02392747','effect':'No mathematical gap; correct title/authors/DOI identify credited source','source_repaired':False},'source_repair':False,'human_peer_review':False,'formal_machine_verification':False,'follow_up':None,'rendered_live_browser_native_gates_passed':False,'completion_estimate_percent_this_scientific_review':100,'overall_goal_complete':False}
op=P/'verification/root-clearance-23441617-20261025.json';assert not op.exists();op.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':'PASS_WITH_NONCENTRAL_BIBLIOGRAPHIC_DEFECT','bindings':len(bindings),'archive_members':118,'root_clearance_sha256':info(op)['sha256']}))
