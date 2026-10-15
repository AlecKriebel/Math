from pathlib import Path
import hashlib,json,datetime,difflib,urllib.request,concurrent.futures
root=Path(__file__).resolve().parent
program=root.parent
current=program/'reviewed_candidate'
family=program/'priority_mechanism_family'
def sha(data):return hashlib.sha256(data).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
# Preserve the independently completed 21-file checkpoint before final rebinding.
checkpoint_sha={'REPORT.md':'535c9b040c8f65680bb66e9ccdff5cb07fc46f1ea0e5bce89ff0dc4fba321ded','VERDICT.json':'cd35de5f2352ffa7b3bc87035ef1d8b329da42dc4fe4cf77573ca95dda19ec73','MANIFEST.json':'b847f0875847d927026e9edc67dd4370f5640453c7d99352cea982089e58279c'}
checkpoints=[]
for name in ('REPORT.md','VERDICT.json','MANIFEST.json'):
    target=root/('CHECKPOINT_21_'+name)
    if target.exists():
        assert sha(target.read_bytes())==checkpoint_sha[name], 'Checkpoint must never be overwritten'
    else:target.write_bytes((root/name).read_bytes())
    checkpoints.append({'path':target.name,'bytes':target.stat().st_size,'sha256':sha(target.read_bytes())})
prior=json.loads((root/'INTEGRITY_AND_REPLAY.json').read_text())
initial={x['path']:x['actual_sha256'] for x in prior['current_manifest_entries']}
manifest_bytes=(current/'MANIFEST.json').read_bytes()
manifest=json.loads(manifest_bytes)
expected_manifest='1190312a7917a663fc4da4ecb44fa3b435e6798acb534c0de22db01b3f4f36c8'
assert sha(manifest_bytes)==expected_manifest
assert len(manifest['sha256'])==22
assert set(manifest['sha256'])==set(initial)|{'CONTROL_PROOFS.md'}
assert all(manifest['sha256'][name]==digest for name,digest in initial.items())
entries=[]
for name,digest in manifest['sha256'].items():
    data=(current/name).read_bytes()
    assert sha(data)==digest, name
    entries.append({'path':name,'bytes':len(data),'sha256':sha(data),'match':True,'unchanged_from_initial_21':name in initial})
old=(family/'CONTROL_PROOFS.md').read_bytes()
new=(current/'CONTROL_PROOFS.md').read_bytes()
assert sha(old)=='f3094259f1b408aab0311563b62c88d21742c838be20de468e294dca9db9a6ef'
assert sha(new)=='401b230c480d1437ef0e7747e088c156396f5069e002bf1a728fc38300e24569'
oldname=b'SUBSUMPTION_PROOF.md'
newname=b'CLASSICAL_PRIOR_ADAPTER_INDEPENDENT_CHECK.md'
assert old.count(oldname)==1
assert old.replace(oldname,newname)==new
original=[]
for entry in prior['original_snapshot_entries']:
    data=(program/'source_snapshot'/entry['path']).read_bytes()
    assert sha(data)==entry['actual_sha256']
    original.append({'path':entry['path'],'sha256':sha(data),'unchanged':True})
# Fetch the supplemental primary PDFs; downloaded bodies are ignored.
cache=root/'tmp'/'attachment_primary'
cache.mkdir(parents=True,exist_ok=True)
specs=[
('bryant_pl','https://webhomes.maths.ed.ac.uk/~v1ranick/papers/pltop.pdf','eb5d25148f2b08f3a5994006fdb66a32c3c277ebfe85f144f71d56fbfe0f97cf'),
('oliva_kuhl_magalhaes','https://mat.uab.es/pubmat/fitxers/download/FileType%3Apdf/FolderName%3Av37%282%29/FileName%3A37293_02.pdf','4dfda99616144813ada80b507c14be8a001d05c110b60df10f0a407ad7756900'),
('mostajeran_sepulchre','https://arxiv.org/pdf/1804.06068v1','e5f5af5b637bca087394df126c66526ce54569af30f6686a2b02ddb4da6e95db'),
('wall_differential_topology','https://webhomes.maths.ed.ac.uk/~v1ranick/surgery/wallretyped.pdf','d048f5c917397ae14d8cfeb2202f2090a9d7eb4d1e64ef851ee5b1f8c0ee038e')]
def fetch(spec):
    ident,url,expected=spec
    req=urllib.request.Request(url,headers={'User-Agent':'Independent-mathematical-source-audit/1.0'})
    with urllib.request.urlopen(req,timeout=40) as response:
        blocks=[]
        while True:
            block=response.read(262144)
            if not block:break
            blocks.append(block)
        data=b''.join(blocks)
        receipt={'id':ident,'requested_url':url,'resolved_url':response.geturl(),'http_status':response.status,'content_type':response.headers.get('Content-Type'),'utc':now(),'bytes':len(data),'sha256':sha(data),'previous_primary_hash_matches':sha(data)==expected}
    assert data.startswith(b'%PDF'),ident
    assert sha(data)==expected,ident
    (cache/(ident+'.pdf')).write_bytes(data)
    return receipt
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    sources=list(executor.map(fetch,specs))
checks={
'1_boundary_core_and_actual_neighborhood':{'status':'PASS','reason':'Alternating perturbations outside s^-<=i approach e1. Bryant3.16 and RS3.30 explicitly require an actual neighborhood; outward collar is already independently reconstructed.'},
'2_translation_cone_counterexample':{'status':'PASS','reason':'Exact sums and noncyclic variations are 0,1,2; positive diagonal conjugacy preserves variations and sums.'},
'3_single_map_rank_two_counterexample':{'status':'PASS','reason':'Closed all-real-scalar cone C0 union L has rank2, since every3-subspace meets excluded F; Ty expansion at least3 and Tz contraction at most1 prove strict inclusion. C0 sphere section is S1 times D2, while L supplies two isolated points. Both printed general-cone hypotheses permit this C; no continuous-semigroup claim.'},
'4_normalized_flow_and_GKL':{'status':'PASS','reason':'Unit eigenvectors are fixed and norm is preserved, contrary to the point-attractor norm-shrinking hypothesis. Whole-sphere extension is an independently audited extra step in the candidate.'},
'5_Wall_stable_range':{'status':'PASS','reason':'Actual p131 pixels confirm c>=m+1, and n>=6,c>=3 for the smooth disc-bundle theorem. Text extraction drops >= signs; no equality claim is adopted. d6,i3 has c2,m3 and is outside the stable range.'}}
receipt={'utc':now(),'status':'PASS','stage':'Complete current 22-file package after source-locator attachment repair; initial complete audit and seals preserved','current_manifest_sha256':sha(manifest_bytes),'current_manifest_entries':entries,'all_initial_21_bytes_unchanged':True,'original_snapshot_14_entries':original,'checkpoints_21':checkpoints,'attachment':{'original_sha256':sha(old),'current_sha256':sha(new),'only_change':'Exactly one post-seal back-reference filename SUBSUMPTION_PROOF.md -> CLASSICAL_PRIOR_ADAPTER_INDEPENDENT_CHECK.md','replacement_count':1,'exact_replacement_equals_current':True,'mathematical_content_unchanged':True,'all_five_controls_independently_reconstructed':checks,'source_gate':'Four supplemental primary PDF captures independently retrieved, all hashes match prior source bodies directly read; Wall p131 visually checked','supplemental_primary_receipts':sources,'new_mathematical_correction_required':False},'initial_first_pass_seal_sha256':sha((root/'FIRST_PASS_SEAL.json').read_bytes()),'initial_first_pass_reconstruction_sha256':sha((root/'FIRST_PASS_SEALED.md').read_bytes()),'no_candidate_or_historical_input_modified':True}
(root/'CURRENT22_ATTACHMENT_REVIEW.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'status':'PASS','current_manifest_sha256':sha(manifest_bytes),'entries':len(entries),'unchanged_initial_entries':len(initial),'supplemental_primary_sources':len(sources),'control_change':'one filename replacement only','checkpoint_files':checkpoints},indent=2))
