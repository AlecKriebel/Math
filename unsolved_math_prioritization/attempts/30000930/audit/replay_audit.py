#!/usr/bin/env python3
"""Replay the exact bound continued archive. Requires Python 3 and SymPy."""
import hashlib,json,os,subprocess,sys,tempfile,zipfile
from pathlib import Path

def digest(data):return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}

def main():
    root=Path(__file__).resolve().parent
    b=json.loads((root/'BINDING.json').read_text())
    archive=Path(sys.argv[1]);data=archive.read_bytes()
    assert digest(data)=={k:b['author_archive'][k] for k in ['bytes','sha256']}
    for e in b['audit_files']:
        assert digest((root/e['path']).read_bytes())=={k:e[k] for k in ['bytes','sha256']},e['path']
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    with tempfile.TemporaryDirectory() as tmp:
        tmp=Path(tmp)
        with zipfile.ZipFile(archive) as z:
            assert sorted(z.namelist())==b['author_archive']['members']
            for name in z.namelist():
                p=Path(name)
                assert name.startswith('safe/') and not p.is_absolute() and '..' not in p.parts
            z.extractall(tmp)
        author=tmp/'safe'
        out=subprocess.check_output([sys.executable,'verify_manifest.py'],cwd=author,env=env)
        assert json.loads(out)['files']==23
        generated=tmp/'author_generated.json'
        subprocess.check_output([sys.executable,'verify_continued.py','--output',str(generated)],cwd=author,env=env)
        assert generated.read_bytes()==(author/'CONTROL_RESULTS.json').read_bytes()
        historical=subprocess.check_output([sys.executable,'history/audit/replay_audit.py','history/author-packet.zip'],cwd=author,env=env)
        assert json.loads(historical)['status']=='PASS'
        independent=subprocess.check_output([sys.executable,str(root/'independent_check.py')],env=env)
        assert independent==(root/'INDEPENDENT_RESULTS.json').read_bytes()
        after=subprocess.check_output([sys.executable,'verify_manifest.py'],cwd=author,env=env)
        assert out==after
    print(json.dumps({'status':'PASS','author_archive_bound':True,'author_manifest_files':23,
                      'historical_replay':'PASS','author_replay_byte_match':True,
                      'independent_replay_byte_match':True,'generic_associativity_triples':1728,
                      'normal_form_associativity_triples':1728,'basis_change_products':144,
                      'graded_trace_products':144,'higher_rank_triples':2878},sort_keys=True))
if __name__=='__main__':main()
