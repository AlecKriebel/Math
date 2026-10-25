from pathlib import Path
import json,hashlib,zipfile,datetime,shutil
r=Path(__file__).resolve().parent;p=r.parent.parent;s=p/'sources'
def pin(f):return {'path':str(f),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()}
receipt=json.loads((s/'receipt.json').read_text());assets=[];members=[]
for e in receipt['files']:
    f=s/e['name'];q=pin(f)
    if q['sha256']!=e['sha256'] or q['bytes']!=e['bytes']:raise RuntimeError(q)
    assets.append(q)
for a in receipt['archives']:
    with zipfile.ZipFile(s/a['name']) as z:
        if z.testzip() is not None:raise RuntimeError('CRC')
        for e in a['members']:
            f=s/'published-source'/e['member'];q=pin(f)
            if q['sha256']!=e['sha256'] or q['bytes']!=e['bytes'] or hashlib.sha256(z.read(e['member'])).hexdigest()!=q['sha256']:raise RuntimeError(q)
            if pin(r/'replay-copy'/e['member'])['sha256']!=q['sha256']:raise RuntimeError('replay input changed')
            members.append(q)
if len(members)!=45:raise RuntimeError('member count')
if (s/'finite-warm-thresholds.pdf').read_bytes()!=(s/'published-source/output/pdf/finite-warm-thresholds.pdf').read_bytes():raise RuntimeError('PDF copy')
if pin(s/'record.json')['sha256']!=receipt['record_sha256']:raise RuntimeError('record')
(r/'source-integrity.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','receipt':pin(s/'receipt.json'),'record':pin(s/'record.json'),'assets':assets,'zip_crc':'PASS','member_count':45,'members':members,'embedded_main_identical':True,'replay_inputs_also_unchanged':True,'source_modified':False},indent=2)+'\n')
sc=p/'reviews/scope';receipts=json.loads((sc/'primary-source-receipts.json').read_text())
scopes={
'hhk-2023-published':{'text_line_ranges':[[70,310],[480,525],[611,769],[1060,1350],[1452,1508]],'printed_pages':'3014–3017,3021,3023–3025,3029–3033,3036','scope':'Exact process, Conditions1/3, Theorem1 and full relevant Section5 proof including Proposition8, Proposition1 and its Lemma1/proof, Lemma2 even-cycle proof. No inference from merely an ODE or simulation.','interface':'Finite graph, alpha>1, positive rates and unit counts; convergence a.s. to equilibria with no positive eigenvalue, stable-point attainment with positive probability; E_infinity=E_plus from Proposition1.'},
'warm-2016-published':{'text_line_ranges':[[130,191],[285,420],[430,489],[504,735],[1325,1400]],'printed_pages':'2495–2502,2503–2506,2515–2516','scope':'Original WARM normalization and unit start; Theorem1(ii) and Section2.1 proof interface for stable attainment; Proposition2(iv),(v) and their full proofs; Theorem4(ii) attribution.','interface':'Uniform odd-cycle threshold already known; triangle strict stability below4/3 and criticality at equality; no need to import the 2016 conjectural full convergence statement.'},
'hk-2017-author':{'text_line_ranges':[[277,405],[918,1092]],'printed_pages':'7–10,21–24','scope':'Theorem2(a), Example1, Theorem3/Corollary1; complete Section5.1 proof of Lemmas5–8 and its matching conclusion.','interface':'Classical whisker/least-weight/champion argument and unequal-rate limitation; actual displayed inequalities support the manuscript alpha>24 prior-method comparison.'},
'owr-2023-12':{'text_line_ranges':[[607,724]],'printed_pages':'653–656','scope':'Kleptsyn contribution model, finite-graph setting and exact OpenProblems1/2, distinct sharpness suggestion.','interface':'Requests improvement of >2 forest and >25 equal-rate whisker bounds; >4/3 suggested separately for both, not an assertion proved here.'}}
raw=[]
for name,scope in scopes.items():
    e=next(e for e in receipts if e['name']==name+'.pdf');f=sc/'cache/primary-sources'/e['name'];q=pin(f)
    if q['sha256']!=e['sha256']:raise RuntimeError('primary pin')
    raw.append({'name':name,'url':e['url'],'retrieved_utc':e['retrieved_utc'],'pdf':q,'text':pin(f.with_suffix('.txt')),'read_scope':scope,'interface_result':'MATCH'})
(r/'primary-source-checks.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'acquisition':'Fresh raw primary PDFs supplied by scope agent; only paths, versions and hashes shared. Independently read and rehashed here.','scope_receipt':pin(sc/'primary-source-receipts.json'),'sources':raw,'recursive_background_proof_certification':False,'priority_certification':False},indent=2)+'\n')
shutil.rmtree(r/'replay-copy')
(r/'temporary').rmdir()
print(json.dumps({'receipt_sha256':pin(s/'receipt.json')['sha256'],'assets':len(assets),'members':len(members),'primary_sources':len(raw)},indent=2))
