"""Meaningful copied-input/output guards for the exact frozen source builder/verifier."""
from pathlib import Path
import argparse, hashlib, json, os, shutil, stat, subprocess, tempfile, time
PIN='32d7a891fa5ad3ff49269865e122f5ed3327da4fe83b3344738d958130bcf38b'
RUNTIME='/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
def need(x,m):
    if not x: raise ValueError(m)
def digest(raw): return hashlib.sha256(raw).hexdigest()
def snap(root):
    out={}
    if not root.exists(): return out
    for f in root.rglob('*'):
        st=f.lstat();kind=stat.S_IFMT(st.st_mode)
        out[f.relative_to(root).as_posix()]=[kind,digest(f.read_bytes()) if stat.S_ISREG(st.st_mode) else os.readlink(f) if stat.S_ISLNK(st.st_mode) else None]
    return out
def rebind(src):
    m=json.loads((src/'MANIFEST.json').read_text())
    for row in m['files']:
        f=src/row['path']
        if f.is_file() and not f.is_symlink():
            raw=f.read_bytes();row.update(bytes=len(raw),sha256=digest(raw))
    (src/'MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
    return digest((src/'MANIFEST.json').read_bytes())
def main(a):
    source,pdf,scratch=Path(a.source).resolve(),Path(a.pdf).resolve(),Path(a.scratch).resolve()
    controls=['wrong_pin','source_tex_bytes','source_archive_bytes','full_record_bytes','missing_source',
      'extra_source','empty_source_directory','source_symlink','source_fifo','manifest_fifo',
      'helper_fifo','pdf_fifo','pdf_bytes','manifest_duplicate_rebound','gate_priority_rebound',
      'builder_output_inside_source','builder_output_equals_source','builder_output_symlink',
      'builder_ancestor_symlink','builder_destination_fifo','builder_destination_directory',
      'builder_source_hardlink','builder_pdf_hardlink','builder_unrelated_multilink',
      'builder_parent_regularfile','builder_pdf_symlink']
    results=[]
    with tempfile.TemporaryDirectory(prefix='guard02-',dir=scratch) as tmp:
      root=Path(tmp)
      for opt in (False,True):
        cmd0=[RUNTIME,'-I','-B']+(['-O'] if opt else [])
        for control in ['positive']+controls:
          case=root/'case'
          if case.exists(): shutil.rmtree(case)
          src=case/'source';shutil.copytree(source,src)
          localpdf=case/'input.pdf';shutil.copyfile(pdf,localpdf)
          out=case/'outputs';pin=PIN
          isbuilder=control.startswith('builder_')
          if control=='wrong_pin':pin='0'*64
          elif control=='source_tex_bytes':(src/'paper.tex').write_bytes((src/'paper.tex').read_bytes()+b'\n')
          elif control=='source_archive_bytes':
            f=src/'audit/intake/original/unsolved_math_prioritization/attempts/30001223/archives/YOUNG_TOPS_30001223_AUTHOR_SAFE_FREEZE.zip';f.write_bytes(f.read_bytes()+b'\n')
          elif control=='full_record_bytes':
            f=src/'audit/intake/SELECTED_PUBLIC_RECORD.json';f.write_bytes(f.read_bytes()+b' ')
          elif control=='missing_source':(src/'paper.tex').unlink()
          elif control=='extra_source':(src/'unlisted').write_text('extra')
          elif control=='empty_source_directory':(src/'empty').mkdir()
          elif control=='source_symlink':(src/'paper.tex').unlink();(src/'paper.tex').symlink_to(pdf)
          elif control in ('source_fifo','manifest_fifo','helper_fifo'):
            key={'source_fifo':'paper.tex','manifest_fifo':'MANIFEST.json','helper_fifo':'build_package.py'}[control]
            (src/key).unlink();os.mkfifo(src/key)
          elif control=='pdf_fifo':localpdf.unlink();os.mkfifo(localpdf)
          elif control=='pdf_bytes':localpdf.write_bytes(localpdf.read_bytes()+b'\n')
          elif control=='manifest_duplicate_rebound':
            f=src/'MANIFEST.json';raw=f.read_text();f.write_text(raw[:-2]+',"schema":"pr786-closed-source/v1"}\n');pin=digest(f.read_bytes())
          elif control=='gate_priority_rebound':
            f=src/'audit/root-receipts/PRIORITY_GATE.json';v=json.loads(f.read_text());v['historical_first_priority_certified']=True;f.write_text(json.dumps(v)+'\n');pin=rebind(src)
          elif control=='builder_output_inside_source':out=src/'bad-output'
          elif control=='builder_output_equals_source':out=src
          elif control=='builder_output_symlink':
            target=case/'link-target';target.mkdir();out.symlink_to(target,target_is_directory=True)
          elif control=='builder_ancestor_symlink':
            target=case/'ancestor-target';target.mkdir();link=case/'link';link.symlink_to(target,target_is_directory=True);out=link/'child'
          elif control in ('builder_destination_fifo','builder_destination_directory','builder_source_hardlink','builder_pdf_hardlink','builder_unrelated_multilink'):
            out.mkdir();target=out/'paper.tex'
            if control=='builder_destination_fifo':os.mkfifo(target)
            elif control=='builder_destination_directory':target.mkdir()
            elif control=='builder_source_hardlink':os.link(src/'paper.tex',target)
            elif control=='builder_pdf_hardlink':
                target=out/'output/pdf/paper.pdf';target.parent.mkdir(parents=True);os.link(localpdf,target)
            else:
                other=case/'unrelated';other.write_text('original other file');os.link(other,target)
          elif control=='builder_parent_regularfile':
            parent=case/'regular-parent';parent.write_text('not a directory');out=parent/'child'
          elif control=='builder_pdf_symlink':
            link=case/'pdf-symlink';link.symlink_to(localpdf);localpdf=link
          before=snap(src)
          if isbuilder:
            cmd=cmd0+[str(src/'build_package.py'),'--expected-manifest-sha256',pin,'--pdf',str(localpdf),'--output-dir',str(out)]
          else:
            cmd=cmd0+[str(src/'verify_bundle.py'),'--expected-manifest-sha256',pin,'--pdf',str(localpdf)]
          started=time.monotonic()
          r=subprocess.run(cmd,capture_output=True,text=True,timeout=5)
          elapsed=time.monotonic()-started
          if control=='positive':
            need(r.returncode==0 and json.loads(r.stdout)['result']=='PASS','Positive copied baseline failed')
          else:
            need(r.returncode!=0,'Accepted bad control '+control)
            if not isbuilder:
                need(json.loads(r.stdout).get('result')=='FAIL','Verifier failure not structured')
          need(snap(src)==before,'Rejected command mutated copied closed source')
          results.append({'control':control,'optimized':opt,'tool':'builder' if isbuilder else 'verifier',
              'expected':'PASS' if control=='positive' else 'REJECT','exitcode':r.returncode,
              'elapsed_seconds':round(elapsed,4),'stdout_sha256':digest(r.stdout.encode()),
              'stderr_sha256':digest(r.stderr.encode()),'source_unchanged_after_command':True,
              'diagnostic':(r.stderr if isbuilder else r.stdout)[-400:]})
          shutil.rmtree(case)
    return {'status':'PASS','positive_cases':2,'negative_cases':len(controls)*2,
      'distinct_negative_controls':len(controls),'all_mutations_on_owned_copies':True,
      'nonregular_timeout_seconds':5,'results':results,
      'limits':'Static guard controls and exact source binding; no hostile concurrent filesystem race or sandbox security certification.'}
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for x in ('source','pdf','scratch'):p.add_argument('--'+x,required=True)
    print(json.dumps(main(p.parse_args()),indent=2,sort_keys=True))
