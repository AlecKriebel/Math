#!/usr/bin/env python3
"""Independent explicit-failure publication integrity checks, not a proof certificate."""
PINS={'packs': [{'tag': 'VERIFIED_PRIOR', 'folder': 'original_author', 'archive': {'name': 'DENSE_CYCLES_2193_VERIFIED_PRIOR_SAFE.zip', 'bytes': 6084, 'sha256': '0d9ca1f554cab84136aa76a88ace9c8c6864d1d5786724ab51d3531fa56c95b7'}, 'manifest': {'name': 'DENSE_CYCLES_2193_VERIFIED_PRIOR_EXTERNAL_MANIFEST.json', 'bytes': 1207, 'sha256': '538b980ffa106490ff105a5007c945f7953402b06f1164b302bccc180c323f56'}, 'members': 5}, {'tag': 'CLARIFIED', 'folder': 'accepted_author', 'archive': {'name': 'DENSE_CYCLES_2193_CLARIFIED_SAFE.zip', 'bytes': 6548, 'sha256': 'ebab33c6fba460c05265df0c79e8a711fe8a36650026578fcbd46b52a89a60b7'}, 'manifest': {'name': 'DENSE_CYCLES_2193_CLARIFIED_EXTERNAL_MANIFEST.json', 'bytes': 1209, 'sha256': 'a707dffc5f07b8e3f4ed62bd5e00766017904e6c43f9ed875d85253806323c4b'}, 'members': 5}, {'tag': 'INDEPENDENT_AUDIT', 'folder': 'independent_audit', 'archive': {'name': 'DENSE_CYCLES_2193_INDEPENDENT_AUDIT_SAFE.zip', 'bytes': 32009, 'sha256': '7a3d477e3b26d3fde048cf37d8062aa3ed0ff3abf521f3885664e1f174bde391'}, 'manifest': {'name': 'DENSE_CYCLES_2193_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json', 'bytes': 2575, 'sha256': 'c2e4e925afa9d04ea3c7777e56a632cba2967a4fbc6135477a14fa5e9bc4aaab'}, 'members': 12}, {'tag': 'EXACT_ACCEPTANCE', 'folder': 'exact_acceptance', 'archive': {'name': 'DENSE_CYCLES_2193_EXACT_ACCEPTANCE_SAFE.zip', 'bytes': 6018, 'sha256': 'b3528c5e3fdf0ce372846c1918b8b1e7ec0d5dd6b743fad7dfc18957004849db'}, 'manifest': {'name': 'DENSE_CYCLES_2193_EXACT_ACCEPTANCE_EXTERNAL_MANIFEST.json', 'bytes': 1301, 'sha256': 'e1d2990838587b747f162566d577a9210cf8fa8ac2e179c04a46d9da74e8a177'}, 'members': 4}], 'receipt': {'bytes': 1788, 'sha256': 'e1d510e6df361385246c58756dc430f693426812ef23a13a24a6ff5831e98455'}}
import argparse, hashlib, io, json, stat, subprocess, sys, tempfile, zipfile
from fractions import Fraction
from pathlib import Path, PurePosixPath
H=lambda b:hashlib.sha256(b).hexdigest()
def need(ok,why):
    if not ok: raise ValueError(why)
def pin(data,entry,label):
    need((len(data),H(data))==(entry['bytes'],entry['sha256']),label+' byte/hash mismatch')
def safe_name(n):
    p=PurePosixPath(n)
    need(n and not p.is_absolute() and '..' not in p.parts and '.' not in p.parts and '\\' not in n and ':' not in n and not n.endswith('/'),'unsafe member path')
    return p
def inspect(ab,mb,ap,mp,count):
    pin(ab,ap,'archive');pin(mb,mp,'manifest');m=json.loads(mb)
    need(m['archive']==ap and m['problem_id']==2193,'manifest binding');es=m['members'];names=[e['path'] for e in es]
    need(len(names)==count==len(set(names)),'manifest inventory');out={}
    with zipfile.ZipFile(io.BytesIO(ab)) as z:
        need(len(z.infolist())==count and set(z.namelist())==set(names),'archive inventory');need(z.testzip() is None,'archive CRC')
        for e in es:
            n=e['path'];p=safe_name(n);need(len(p.parts)==1,'unexpected directory');i=z.getinfo(n);mode=i.external_attr>>16
            need(stat.S_IFMT(mode) in (0,stat.S_IFREG) and not mode&0o111 and not i.flag_bits&1,'unsafe member mode')
            need(p.suffix in ('.md','.json','.py','.patch','.zip'),'unexpected member format');b=z.read(n);pin(b,e,'member '+n)
            if p.suffix!='.zip':
                b.decode('utf-8')
                if p.suffix=='.json':json.loads(b)
            out[n]=b
    return out

def replay(original,accepted,patch):
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)/'relocated'/'nested';root.mkdir(parents=True)
        for n,b in original.items():(root/n).write_bytes(b)
        p=subprocess.run(['patch','--batch','--forward','--fuzz=0','-p1'],cwd=root,input=patch,capture_output=True,timeout=30)
        need(p.returncode==0 and not p.stderr and b'fuzz' not in p.stdout.lower() and b'offset' not in p.stdout.lower(),'patch application')
        need({x.name:x.read_bytes() for x in root.iterdir() if x.is_file()}==accepted,'exact patch replay')
        need(all(x.is_file() and not x.is_symlink() for x in root.iterdir()),'patch unexpected output')
    return {'passed':True,'all_five_files_byte_equal':True,'fuzz':0,'offset':0,'changed_files':[n for n in sorted(original) if original[n]!=accepted[n]]}

def inputs(a,meta,source):
    out={'corpus_checks':{'performed':False},'source_checks':{'performed':False}}
    if any((a.catalog,a.problems,a.reports)):
        need(all((a.catalog,a.problems,a.reports)),'all three complete corpora are required');objs=[]
        for path,e in zip((a.catalog,a.problems,a.reports),meta['corpora']):
            b=Path(path).read_bytes();pin(b,e,'complete corpus '+e['label']);objs.append(json.loads(b))
        c,rs,reports=objs;c=[v for v in c if str(v.get('id'))=='2193'];rs=[v for v in rs if str(v.get('id'))=='2193'];need(len(c)==len(rs)==1,'unique exact ID');r=rs[0]
        need(c[0]['rank']==898 and r['problem_number']=='EP-584','target identity');need('EP-584' not in reports,'absent report key');need(H(r['statement'].encode())==meta['statement_sha256'],'statement pin')
        need(H(json.dumps([r,reports.get('EP-584',{})],sort_keys=True).encode())==meta['pair_sha256'],'complete pair pin');need(c[0]['statement_hash']==meta['statement_sha256'] and c[0]['review_hash']==meta['pair_sha256'],'catalog identity hashes')
        out['corpus_checks']={'performed':True,'all_three_complete_pins_match':True,'exact_id':2193,'rank':898,'report_key_present':False,'complete_pair_hash_match':True,'statement_hash_match':True,'dataset_contents_emitted':False}
    if a.sources_directory:
        found={H(f.read_bytes()):f.stat().st_size for f in Path(a.sources_directory).glob('*.pdf')}
        need(len(source['sources'])==5,'five source metadata entries')
        for s in source['sources']:need(found.get(s['sha256'])==s['bytes'],'source PDF byte/hash match')
        out['source_checks']={'performed':True,'all_five_public_pdf_pins_match':True,'source_contents_emitted':False,'fresh_retrieval_during_publication':False}
    return out

def verify(root,a):
    packs={};expected={};summary=[]
    for p in PINS['packs']:
        ab=(root/'archives'/p['archive']['name']).read_bytes();mb=(root/'archives'/p['manifest']['name']).read_bytes();pack=inspect(ab,mb,p['archive'],p['manifest'],p['members']);packs[p['tag']]=pack
        for n,b in pack.items():
            rel=p['folder']+'/'+n;f=root/rel;need(not f.is_symlink() and f.read_bytes()==b,'loose member equality');expected[rel]=b
        actual={x.relative_to(root).as_posix() for x in (root/p['folder']).rglob('*') if x.is_file()};need(actual=={p['folder']+'/'+n for n in pack},'loose inventory')
        summary.append({'archive':p['archive'],'members':len(pack)})
    original=packs['VERIFIED_PRIOR'];accepted=packs['CLARIFIED'];audit=packs['INDEPENDENT_AUDIT'];acceptance=packs['EXACT_ACCEPTANCE']
    for tag in ('VERIFIED_PRIOR','CLARIFIED'):
        p=next(p for p in PINS['packs'] if p['tag']==tag)
        for e in (p['archive'],p['manifest']):need(audit[e['name']]==(root/'archives'/e['name']).read_bytes(),'nested archive/manifest equality')
    need(all(audit[n]==b for n,b in acceptance.items()),'separate acceptance exact equality')
    acc=json.loads(audit['EXACT_ACCEPTANCE.json']);need(acc['decision']=='ACCEPT_SCOPED_PRIOR_NEGATIVE' and acc['problem_id']==2193 and acc['rank']==898 and acc['problem_number']=='EP-584','acceptance target/scope');need(acc['new_mathematical_approaches']==0 and len(acc['excluded_claims'])==8,'scope exclusion inventory')
    for key,n in [('actual_patch','CLARIFICATIONS.patch'),('audit_report','INDEPENDENT_AUDIT.md'),('full_local_replay_result','REPLAY_RESULTS.json'),('replay_program','replay_audit.py')]:pin(audit[n],acc[key],'acceptance '+key)
    for key,tag in [('original_payload','VERIFIED_PRIOR'),('preferred_clarified_payload','CLARIFIED')]:need(acc[key]==next(p['archive'] for p in PINS['packs'] if p['tag']==tag),'accepted archive binding')
    for key,tag in [('original_external_manifest','VERIFIED_PRIOR'),('clarified_external_manifest','CLARIFIED')]:need(acc[key]==next(p['manifest'] for p in PINS['packs'] if p['tag']==tag),'accepted manifest binding')
    need({e['path'] for e in acc['exact_accepted_clarified_members']}==set(accepted),'accepted member list')
    for e in acc['exact_accepted_clarified_members']:pin(accepted[e['path']],e,'exact acceptance member')
    rb=(root/'INDEPENDENT_AUDIT_RECEIPT.json').read_bytes();pin(rb,PINS['receipt'],'independent receipt');r=json.loads(rb);need(r['decision']==acc['decision'] and r['original_preserved'] and r['derivative_replayed'],'receipt decision')
    for key,tag,kind in [('audit_archive','INDEPENDENT_AUDIT','archive'),('audit_external_manifest','INDEPENDENT_AUDIT','manifest'),('acceptance_external_manifest','EXACT_ACCEPTANCE','manifest'),('separate_acceptance_archive','EXACT_ACCEPTANCE','archive'),('original_archive','VERIFIED_PRIOR','archive'),('preferred_clarified_archive','CLARIFIED','archive'),('clarified_external_manifest','CLARIFIED','manifest')]:need(r[key]==next(p[kind] for p in PINS['packs'] if p['tag']==tag),'receipt binding '+key)
    meta=json.loads(audit['INPUT_VERIFICATION.json']);need(meta['statement_sha256']=='b28737a9849838c6181d10b15f85a2d8e4eadce8040f8c437d8dbd8b06db485b' and meta['pair_sha256']=='e1601693f7c82888489d082791d70f661cbeb1cdb3bf38c03ebc0927279b48d7','input identity pins')
    need(acc['accepted_target']['statement_sha256']==meta['statement_sha256'] and acc['accepted_target']['complete_record_report_pair_sha256']==meta['pair_sha256'],'acceptance input identity')
    source=json.loads(audit['SOURCE_AUDIT.json']);proof=replay(original,accepted,audit['CLARIFICATIONS.patch']);need(proof['changed_files']==['PROOF_SCOPE.md','README.md','VERIFICATION_LOG.md'],'exact patch changed files')
    for q in (2,3,5,7,11,101,1009):
        n=2*q**5;m=q**6;d=Fraction(m,n*n);need(2*m==n*q and d==Fraction(1,4*q**4) and d*d*n*n==Fraction(q*q,4) and d**3*n*n==Fraction(1,16*q*q),'arithmetic consistency')
    pub=json.loads((root/'PUBLICATION_METADATA.json').read_bytes());need(pub['queue_status']=='unsolved' and pub['turns']=='0/5' and not pub['intended_sparse_internal_strong_C6_resolved'] and not pub['H1_only_refutation'] and not pub['fixed_density_refutation'] and not pub['novelty_claimed'] and not pub['Li_manuscript_certified'],'publication scope gate')
    if (root/'PUBLICATION_MANIFEST.json').exists():
        mf=json.loads((root/'PUBLICATION_MANIFEST.json').read_bytes());names=[e['path'] for e in mf['files']];need(len(names)==len(set(names)),'publication manifest duplicates')
        actual={x.relative_to(root).as_posix() for x in root.rglob('*') if x.is_file()};need(actual==set(names)|{'PUBLICATION_MANIFEST.json'},'complete publication inventory')
        for e in mf['files']:
            n=e['path'];safe_name(n);f=root/n;need(not f.is_symlink() and f.resolve().is_relative_to(root.resolve()),'publication path');pin(f.read_bytes(),e,'publication '+n)
    result={'status':'PASS','optimization_level':sys.flags.optimize,'archives':summary,'top_level_archive_member_occurrences':sum(len(p) for p in packs.values()),'exact_loose_members':len(expected),'acceptance_and_receipt_bindings':True,'patch_replay':proof,'arithmetic_consistency':True,'historical_audit_program_executed':False,'historical_audit_optimized_integrity_valid':False,'mathematical_certification':False,'scope':'Exact byte identity, provenance, patch replay and finite arithmetic consistency; no machine proof of the external girth theorem.'}
    result.update(inputs(a,meta,source));return result
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent);p.add_argument('--catalog');p.add_argument('--problems');p.add_argument('--reports');p.add_argument('--sources-directory');a=p.parse_args()
    print(json.dumps(verify(a.root,a),sort_keys=True,indent=2))
