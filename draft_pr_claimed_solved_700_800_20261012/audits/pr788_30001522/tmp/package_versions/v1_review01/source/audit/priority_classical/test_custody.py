"""Owned-copy normal/optimized custody controls for the classical-priority packet."""
from pathlib import Path
import argparse,ast,hashlib,json,os,shutil,subprocess,sys,tempfile,time
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(p,v):put(p,(json.dumps(v,indent=2,sort_keys=True)+'\n').encode())
def put(p,b):
    q=p.with_name(p.name+'.owned-temp')
    q.write_bytes(b);os.replace(q,p)
def editjson(p,f):
    d=json.loads(p.read_text());f(d);dump(p,d)
def manifest(w):
    rows={p.name:{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}for p in sorted(w.iterdir())if p.name!='MANIFEST.json'}
    dump(w/'MANIFEST.json',{'schema':'pr788-priority-classical/v1','head':'3412d5a074c3f3a03f75735a9ccf1755e172204a','exceptions':{'MANIFEST.json':'Only self-hash exception; caller-held external SHA256 required.'},'files':rows})
    return sha((w/'MANIFEST.json').read_bytes())
def tamper(p):put(p,p.read_bytes()+b'\nOWNED COPY TAMPER\n')
def main(a):
    w=Path(a.packet).absolute();inp=Path(a.input_root).absolute();scratch=Path(a.scratch).absolute()
    original_manifest=sha((w/'MANIFEST.json').read_bytes());checker_pin=sha((w/'custody_check.py').read_bytes())
    external=json.loads((w/'SOURCE_LEDGER.json').read_text())['external_scratch_files']
    firstpdf='kuhn_lloyd_v1.pdf'
    original_inputs={n:sha((inp/n).read_bytes())for n in json.loads((w/'INPUT_BINDINGS.json').read_text())['files']}
    original_sources={n:sha((scratch/n).read_bytes())for n in external}
    controls=['positive','wrong_manifest_pin','wrong_checker_pin','changed_checker_valid_comment','changed_report','missing_report',
      'extra_file','extra_empty_directory','report_symlink','report_fifo','manifest_fifo','external_pdf_fifo','external_pdf_changed',
      'original_changed','original_ledger_rebound','selected_record_rebound','input_fifo','input_extra','input_empty_directory','input_symlink',
      'initial_rebound','provisional_rebound','widen_exception_rebound','widen_input_exception_rebound','duplicate_json_rebound',
      'nonfinite_json_rebound','boolean_size_rebound','unsafe_name_rebound','novelty_flag_rebound','source_body_ledger_rebound',
      'critical_source_pin_rebound','query_count_rebound','required_file_removed_rebound']
    results=[]
    with tempfile.TemporaryDirectory(prefix='priority-classical-controls-',dir=scratch) as td:
      base=Path(td)
      for opt in [False,True]:
       for control in controls:
        case=base/'case';case.mkdir();cw=case/'packet';ci=case/'inputs';cs=case/'sources'
        shutil.copytree(w,cw);shutil.copytree(inp,ci);cs.mkdir()
        for n in external:os.link(scratch/n,cs/n)
        mp=original_manifest;cp=checker_pin
        if control=='wrong_manifest_pin':mp='0'*64
        elif control=='wrong_checker_pin':cp='0'*64
        elif control=='changed_checker_valid_comment':
            put(cw/'custody_check.py',(cw/'custody_check.py').read_bytes()+b'\n# changed owned checker\n')
            ast.parse((cw/'custody_check.py').read_text())
        elif control=='changed_report':tamper(cw/'REPORT.md')
        elif control=='missing_report':(cw/'REPORT.md').unlink()
        elif control=='extra_file':(cw/'EXTRA').write_text('owned')
        elif control=='extra_empty_directory':(cw/'empty').mkdir()
        elif control=='report_symlink':
            (cw/'REPORT.md').unlink();(cw/'REPORT.md').symlink_to(w/'REPORT.md')
        elif control=='report_fifo':
            (cw/'REPORT.md').unlink();os.mkfifo(cw/'REPORT.md')
        elif control=='manifest_fifo':
            (cw/'MANIFEST.json').unlink();os.mkfifo(cw/'MANIFEST.json')
        elif control=='external_pdf_fifo':
            (cs/firstpdf).unlink();os.mkfifo(cs/firstpdf)
        elif control=='external_pdf_changed':tamper(cs/firstpdf)
        elif control in ['original_changed','original_ledger_rebound']:
            bn=next(n for n in original_inputs if n.endswith('/author/PROOF.md'));tamper(ci/bn)
            if control=='original_ledger_rebound':
                def bind(d):
                    d['files'][bn]['bytes']=(ci/bn).stat().st_size;d['files'][bn]['sha256']=sha((ci/bn).read_bytes())
                editjson(cw/'INPUT_BINDINGS.json',bind);mp=manifest(cw)
        elif control=='selected_record_rebound':
            editjson(ci/'SELECTED_PUBLIC_RECORD.json',lambda d:d['problem'].__setitem__('title','owned changed title'))
            def bind(d):
                r=d['files']['SELECTED_PUBLIC_RECORD.json'];r['bytes']=(ci/'SELECTED_PUBLIC_RECORD.json').stat().st_size;r['sha256']=sha((ci/'SELECTED_PUBLIC_RECORD.json').read_bytes())
            editjson(cw/'INPUT_BINDINGS.json',bind);mp=manifest(cw)
        elif control=='input_fifo':
            (ci/'SELECTED_PUBLIC_RECORD.json').unlink();os.mkfifo(ci/'SELECTED_PUBLIC_RECORD.json')
        elif control=='input_extra':(ci/'EXTRA').write_text('owned')
        elif control=='input_empty_directory':(ci/'empty').mkdir()
        elif control=='input_symlink':
            (ci/'SELECTED_PUBLIC_RECORD.json').unlink();(ci/'SELECTED_PUBLIC_RECORD.json').symlink_to(inp/'SELECTED_PUBLIC_RECORD.json')
        elif control=='initial_rebound':tamper(cw/'INITIAL_PRIORITY_POSITION.json');mp=manifest(cw)
        elif control=='provisional_rebound':tamper(cw/'PROVISIONAL_FINDING.json');mp=manifest(cw)
        elif control=='widen_exception_rebound':
            editjson(cw/'MANIFEST.json',lambda d:d['exceptions'].__setitem__('REPORT.md','unbound'));mp=sha((cw/'MANIFEST.json').read_bytes())
        elif control=='widen_input_exception_rebound':
            editjson(cw/'INPUT_BINDINGS.json',lambda d:d['exceptions'].append('all sources'));mp=manifest(cw)
        elif control=='duplicate_json_rebound':
            p=cw/'VERDICT.json';put(p,p.read_bytes().replace(b'{',b'{"status":"duplicate",',1));mp=manifest(cw)
        elif control=='nonfinite_json_rebound':
            p=cw/'VERDICT.json';put(p,p.read_bytes().replace(b'{',b'{"unused":NaN,',1));mp=manifest(cw)
        elif control=='boolean_size_rebound':
            editjson(cw/'MANIFEST.json',lambda d:d['files']['REPORT.md'].__setitem__('bytes',True));mp=sha((cw/'MANIFEST.json').read_bytes())
        elif control=='unsafe_name_rebound':
            editjson(cw/'MANIFEST.json',lambda d:d['files'].__setitem__('../outside',{'bytes':0,'sha256':sha(b'')}));mp=sha((cw/'MANIFEST.json').read_bytes())
        elif control=='novelty_flag_rebound':
            editjson(cw/'VERDICT.json',lambda d:d.__setitem__('firstness_certified',True));mp=manifest(cw)
        elif control=='source_body_ledger_rebound':
            editjson(cw/'SOURCE_LEDGER.json',lambda d:d['full_primary_bodies'][0].__setitem__('body_sha256','0'*64));mp=manifest(cw)
        elif control=='critical_source_pin_rebound':
            def change(d):
                e=next(e for e in d['full_primary_bodies']if e['id']=='kuhn_lloyd_v1')
                e['body_sha256']='0'*64;d['external_scratch_files'][e['body_file']]['sha256']='0'*64
            editjson(cw/'SOURCE_LEDGER.json',change);mp=manifest(cw)
        elif control=='query_count_rebound':
            editjson(cw/'QUERY_LEDGER.json',lambda d:d.__setitem__('query_count',0));mp=manifest(cw)
        elif control=='required_file_removed_rebound':(cw/'REPORT.md').unlink();mp=manifest(cw)
        args=[sys.executable,'-B']+(['-O']if opt else [])+[str(cw/'custody_check.py'),'--packet',str(cw),'--input-root',str(ci),'--expected-manifest-sha',mp,'--expected-checker-sha',cp,'--source-root',str(cs)]
        start=time.monotonic();c=subprocess.run(args,capture_output=True,timeout=5)
        positive=control=='positive'
        diagnostic=c.stderr.decode().strip()
        if positive:
            if c.returncode!=0 or json.loads(c.stdout)['status']!='PASS':raise ValueError('Positive control failed: '+diagnostic)
        elif c.returncode==0 or not diagnostic.startswith('CUSTODY_FAIL:'):raise ValueError('Bad negative control '+control+': '+diagnostic)
        if control=='changed_checker_valid_comment' and 'External checker pin'not in diagnostic:raise ValueError('Checker tamper did not exercise external pin')
        results.append({'control':control,'optimized':opt,'expected':'PASS'if positive else'REJECT','exitcode':c.returncode,'diagnostic':diagnostic,'elapsed_seconds':round(time.monotonic()-start,4),'stdout_sha256':sha(c.stdout),'stderr_sha256':sha(c.stderr)})
        shutil.rmtree(case)
    if sha((w/'MANIFEST.json').read_bytes())!=original_manifest:raise ValueError('Original packet changed')
    for n,h in original_inputs.items():
        if sha((inp/n).read_bytes())!=h:raise ValueError('Original input changed')
    for n,h in original_sources.items():
        if sha((scratch/n).read_bytes())!=h:raise ValueError('External source changed')
    result={'status':'PASS','positive_cases':2,'negative_cases':2*(len(controls)-1),'distinct_negative_controls':len(controls)-1,'nonregular_timeout_seconds':5,'testing_manifest_sha256':original_manifest,'checker_sha256':checker_pin,'original_packet_inputs_sources_unchanged':True,
     'mutation_scope':'Temporary owned paths only. External baseline files are read-only hardlinks; every mutation uses atomic replacement/unlink, never writes linked original inodes. All original input/source hashes rechecked after controls.','results':results}
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__)
 for n in ['packet','input-root','scratch']:p.add_argument('--'+n,required=True)
 main(p.parse_args())
