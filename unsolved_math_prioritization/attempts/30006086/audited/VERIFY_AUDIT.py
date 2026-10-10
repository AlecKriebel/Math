"""Verify sealed artifact integrity and consistency of all saved audit evidence."""
import hashlib,json,pathlib,zipfile
ROOT=pathlib.Path(__file__).resolve().parent

def require(ok,message):
    if not ok:raise RuntimeError(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def get(name):return json.loads((ROOT/name).read_text())

def main():
    manifest=get('AUDIT_SHA256SUMS.json')
    for name,meta in manifest['files'].items():
        p=ROOT/name
        require(p.is_file(),f'Missing file: {name}')
        b=p.read_bytes();require(len(b)==meta['bytes'] and sha(b)==meta['sha256'],f'Hash mismatch: {name}')
    am=(ROOT/'author/SHA256SUMS.json').read_bytes()
    require(sha(am)=='bc12e0df09d9093b25b8786640bc9b38876e9949e80b07837afc48b64e1208ff','Author freeze mismatch')
    for name,meta in json.loads(am)['files'].items():
        b=(ROOT/'author'/name).read_bytes();require(len(b)==meta['bytes'] and sha(b)==meta['sha256'],f'Author mismatch: {name}')
    az=ROOT/'AUTHOR_PACKET.zip';require(sha(az.read_bytes())=='cfdcd3b660c0e835fd4006a2e88e01b42ded92e177319fc2d5a4b9b38f4a1d55','Original ZIP mismatch')
    with zipfile.ZipFile(az) as z:
        require(set(z.namelist())==set(json.loads(am)['files'])|{'SHA256SUMS.json'},'Author ZIP inventory mismatch')
        for name in z.namelist():require(z.read(name)==(ROOT/'author'/name).read_bytes(),f'ZIP member mismatch: {name}')
    require((ROOT/'author/EXPECTED_RESULTS.json').read_bytes()==(ROOT/'audit/AUTHOR_REPLAY.json').read_bytes(),'Replay differs')
    expected=get('author/EXPECTED_RESULTS.json');ind=get('audit/INDEPENDENT_RANK_RESULTS.json')
    require(ind['status']=='PASS','Independent ranks not passed')
    ref={(g,tuple(x['content'])):x for g in ('multilinear','binary') for x in expected[g]};seen=set()
    for x in ind['cases']:
        key=x['group'],tuple(x['content']);require(key in ref and key not in seen,'Independent rank coverage error');seen.add(key)
        require(all(x[k]==ref[key][k] for k in ('content','V','bracket_rank','cyclic_rank','loop_quotient')),'Independent rank mismatch')
    require(seen==set(ref) and len(seen)==109 and expected['rank_cases']==109,'Rank count mismatch')
    require(sum(expected['explicit_control_counts'].values())==2137,'Author control count mismatch')
    extra=get('audit/SUPPLEMENTAL_RESULTS.json');require(extra['status']=='PASS_SUPPORTING_FINITE_CONTROLS' and extra['total_controls']==sum(extra['counts'].values())==319,'Supplemental count mismatch')
    require(len(extra['matrix_controls'])==48 and len(extra['paths'])==3,'Supplemental coverage mismatch')
    guards=get('audit/OPTIMIZED_MODE_CHECKS.json');require(len(guards)==3 and all(x['exit_code']!=0 and x['stdout_bytes']==0 for x in guards),'Optimized mode result mismatch')
    acc=get('audit/ACCEPTANCE.json');require(acc['target_status']=='unsolved' and acc['turns']=='5/5' and acc['author_correction_required'] is False,'Acceptance scope mismatch')
    print(json.dumps({'status':'PASS_INTEGRITY_AND_SAVED_EVIDENCE','sealed_files':len(manifest['files']),'rank_cases':109,'author_controls':2137,'supplemental_controls':319,'target_status':'unsolved','turns':'5/5'},sort_keys=True,indent=2))
if __name__=='__main__':main()
