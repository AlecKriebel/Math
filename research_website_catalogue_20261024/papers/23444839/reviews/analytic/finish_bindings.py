from pathlib import Path
import hashlib,json,zipfile,datetime,sys
b=Path(__file__).resolve().parent;p=b.parent.parent;s=p/'sources'
def pin(f):return {'path':str(f),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()}
receipt=json.loads((s/'receipt.json').read_text());entries=[]
for item in receipt['files']:
    v=pin(s/item['name'])
    if v['sha256']!=item['sha256'] or v['bytes']!=item['bytes']:raise RuntimeError(v)
    entries.append(v)
members=[]
for archive in receipt['archives']:
    with zipfile.ZipFile(s/archive['name']) as z:
        if z.testzip() is not None:raise RuntimeError('CRC failure')
        for item in archive['members']:
            f=s/'published-source'/item['member'];v=pin(f)
            if v['sha256']!=item['sha256'] or v['bytes']!=item['bytes']:raise RuntimeError(v)
            if hashlib.sha256(z.read(item['member'])).hexdigest()!=v['sha256']:raise RuntimeError('ZIP member mismatch')
            members.append(v)
if len(members)!=120:raise RuntimeError('wrong member count')
if (s/'published-source/output/pdf/spherefree-doubly-cm.pdf').read_bytes()!=(s/'spherefree-doubly-cm.pdf').read_bytes():raise RuntimeError('main mismatch')
if pin(s/'record.json')['sha256']!=receipt['record_sha256']:raise RuntimeError('metadata mismatch')
(b/'source-integrity.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','receipt':pin(s/'receipt.json'),'record':pin(s/'record.json'),'assets':entries,'member_count':len(members),'members':members,'zip_crc':'PASS','embedded_main_identical':True,'all_originals_unchanged':True},indent=2)+'\n')
sc=p/'reviews/scope';r=json.loads((sc/'primary-source-receipts.json').read_text())
scopes={
'lsv-v2':{'lines':[[87,618]],'pdf_pages':'2–13 (Sections2–4; exact import statements and proofs read)','role':'Load-bearing building/lattice/conjugation representation: Section2; Section3center/splitting and adjoint embedding; Equation9, Corollary4.6, Definition4.7, Proposition4.8. Later Ramanujan assertions not imported.'},
'nevo-published':{'lines':[[174,350]],'pdf_pages':'4–7; printed414–417','role':'Exact 2-CM definition, Theorem3.4 including full proof and reordering/overlap quantifiers, Problem3.7.'},
'nevo-owr-2005':{'lines':[[1882,1942]],'pdf_pages':'Printed960–961','role':'Theorem7 and original Problem8 exact formulation; no changed modern question presumed.'},
'swartz-v1':{'lines':[[475,590]],'pdf_pages':'12–14','role':'Section4explicit local-link/Gorenstein-star homology-sphere convention and surrounding decomposition context; no extra theorem imported.'},
'lm-author-alt':{'lines':[[150,306]],'pdf_pages':'4–8','role':'Section3.1/3.2, Claim3.1, Theorem3.2 and Proposition3.3 proof: classical degree-versus-congruence method. Its irreducible-polynomial quotient not invoked for t^9.'},
'ballmann-swiatkowski':{'lines':[[45,95],[598,725]],'pdf_pages':'1–2,11–13','role':'Theorem1/trivial-group finite case and general Section2 proof interface. Current paper independently proves its exact finite 2D lemma.'},
'januszkiewicz-swiatkowski':{'lines':[[80,120],[276,355],[410,488]],'pdf_pages':'2–3,7–12','role':'Definitions of local largeness and Example1.8(5), classical surface curvature attribution. General systolic contractibility theorem is not needed.'}}
checks=[]
for name,scope in scopes.items():
    e=next(e for e in r if e['name']==name);pdf=Path(e['path']);v=pin(pdf)
    if v['sha256']!=e['sha256']:raise RuntimeError('primary source mismatch')
    checks.append({'name':name,'url':e['url'],'fresh_acquisition_receipt_utc':e['retrieved_utc'],'pdf':v,'text':pin(pdf.with_suffix('.txt')),'read_scope':scope,'interface_result':'MATCH','not_a_full_primary-paper_recertification':True})
(b/'primary-source-checks.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'primary_bodies_acquired_by':'scope agent; independently read and rehashed here','scope_receipt':pin(sc/'primary-source-receipts.json'),'sources':checks,'web_verification':{'lsv':'https://arxiv.org/abs/math/0406217 confirms v2 dated5January2005','nevo_doi':'Web tool DOI open failed; complete fresh Springer PDF successfully available and read locally.'},'limits':'No novelty certification or complete literature search. Historical paper audit bodies and current sibling mathematical findings were not read.'},indent=2)+'\n')
print(json.dumps({'assets_verified':len(entries),'members_verified':len(members),'primary_bodies_rehashed':len(checks),'receipt_sha256':pin(s/'receipt.json')['sha256']},indent=2))
