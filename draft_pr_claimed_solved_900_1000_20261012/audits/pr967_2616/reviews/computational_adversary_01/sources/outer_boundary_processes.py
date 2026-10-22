"""New actual CLI trust-boundary negatives; no mocked child or remote state."""
from pathlib import Path
import datetime,hashlib,json,os,shutil,subprocess,sys,time

HERE=Path(__file__).resolve().parent.parent
PACK=HERE/'fixtures/replay_packet'
BPIN='128bfd14af0273eb4bd850ae95be8a0cbe908795c0032c003894809d733575b5'
AUTHOR_PIN='31bd2aed10d96d5ada5344531e2207dd4388c8cb1328e3c448ac89be5b78ec8c'

def sha(b):return hashlib.sha256(b).hexdigest()
def require(ok,msg):
    if not ok:raise RuntimeError(msg)

def main():
    require(sha((PACK/'BOOTSTRAP.py').read_bytes())==BPIN,'external bootstrap anchor')
    work=HERE/'fixtures/outer_cli_boundaries';work.mkdir()
    rows=[];env=dict(os.environ)
    env.update(TMPDIR=str(HERE/'tmp'),TMP=str(HERE/'tmp'),TEMP=str(HERE/'tmp'),PYTHONDONTWRITEBYTECODE='1')
    def run(label,argv):
        utc=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
        p=subprocess.run(argv,cwd=work,env=env,capture_output=True,timeout=60)
        row=dict(label=label,launch_utc=utc,elapsed_seconds=time.monotonic()-t,argv=argv,
                 cwd=str(work),returncode=p.returncode,stdout=p.stdout.decode(errors='replace'),stderr=p.stderr.decode(errors='replace'))
        rows.append(row)
        (HERE/'receipts/outer_cli_boundaries.json').write_text(json.dumps(rows,indent=2)+'\n')
        require(p.returncode!=0,'unexpected outer CLI acceptance: '+label)
    def repin(root):
        m=json.loads((root/'PUBLICATION_MANIFEST.json').read_bytes())
        for row in m['files']:
            raw=(root/row['path']).read_bytes();row.update(bytes=len(raw),sha256=sha(raw))
        (root/'PUBLICATION_MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
    targets={}
    for label in ['report_self_repin','wrapper_doc_self_repin','bootstrap_changed','oversized_wrapper']:
        root=work/label;shutil.copytree(PACK,root);targets[label]=root
        if label=='report_self_repin':
            p=root/'author/public/REPORT.md';p.write_bytes(b'X'+p.read_bytes()[1:]);repin(root)
        elif label=='wrapper_doc_self_repin':
            p=root/'README.md';p.write_bytes(p.read_bytes()+b'\nOwned changed metadata.\n');repin(root)
        elif label=='bootstrap_changed':(root/'BOOTSTRAP.py').write_text('print("forged")\n')
        elif label=='oversized_wrapper':(root/'verify_publication.py').write_bytes(b'x'*1000001)
    symlink=work/'linked_root';symlink.symlink_to(PACK,target_is_directory=True);targets['linked_root']=symlink
    external_root=work/'oversized_public';shutil.copytree(PACK/'author/public',external_root)
    (external_root/'REPORT.md').write_bytes(b'x'*1000001)
    for mode,flags in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
        for label,root in targets.items():
            run(mode+':'+label,[sys.executable,'-I','-S','-B',*flags,str(PACK/'BOOTSTRAP.py'),str(root)])
        run(mode+':external_bootstrap_actual_oversized_file',[sys.executable,'-I','-S','-B',*flags,
            str(PACK/'author/external/bootstrap.py'),str(external_root),str(PACK/'author/external/MANIFEST.json'),AUTHOR_PIN,mode])
    run('outer_bootstrap_missing_no_site_flag',[sys.executable,'-I','-B',str(PACK/'BOOTSTRAP.py'),str(PACK)])
    run('outer_bootstrap_missing_isolated_flag',[sys.executable,'-S','-B',str(PACK/'BOOTSTRAP.py'),str(PACK)])
    run('outer_verifier_missing_isolated_flag',[sys.executable,'-S','-B',str(PACK/'verify_publication.py')])
    run('mutation_harness_missing_isolated_flag',[sys.executable,'-S','-B',str(PACK/'mutation_tests.py')])
    print(json.dumps(dict(commands=len(rows),all_negative_exit_codes=True,actual_process_execution=True,
                         process_network_mutations='No remote requests or network tools; authenticated scripts only use local children and owned scratch.'),indent=2))

if __name__=='__main__':main()
