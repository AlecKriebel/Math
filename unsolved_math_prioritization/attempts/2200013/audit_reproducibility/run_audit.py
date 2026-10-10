#!/usr/bin/env python3
"""Independent audit and narrow parser regression suite; no network/publication.

Supply the frozen author directory with --original. Writes only in the audit
folder and temporary copies. Never invokes the author's freeze-and-test script.
"""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

FILES = {'PROOF.md','README.md','RESULT.json','certificate.json','replay.py','sources.json','verify_math.py'}
ORIGINAL_PINS = {'verification/MANIFEST.json':'3453f9b0764e9a4296257226dd4629959781867f0cf5827cd2929da259af9125',
                 'verification/bootstrap.py':'3de2f4468273603ee0ed27326653f33f10a268021024be7d7c4e15631087ff46',
                 'public/replay.py':'3445d032b94e7da0cc9f48daa1b7cf290e29ca62d780cb7684e448d6e296ddac'}
MODES = (('normal',[]),('O',['-O']),('OO',['-OO']))


def digest(data):
    return hashlib.sha256(data).hexdigest()


def must(condition, message):
    if not condition:
        raise RuntimeError(message)


def inventory(directory):
    return [{'path':p.name,'bytes':len(p.read_bytes()),'sha256':digest(p.read_bytes())}
            for p in sorted(directory.iterdir()) if p.is_file()]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--original',type=Path,required=True)
    args=parser.parse_args()
    original=args.original.resolve()
    here=Path(__file__).resolve().parent
    corrected=here/'corrected'
    before={p.relative_to(original).as_posix():digest(p.read_bytes()) for p in original.rglob('*') if p.is_file()}
    for name,pin in ORIGINAL_PINS.items():
        must(before.get(name)==pin,'original external pin mismatch: '+name)
    must({p.name for p in (original/'public').iterdir()}==FILES,'original seven-file allowlist')
    must({p.name for p in (corrected/'public').iterdir()}==FILES,'corrected seven-file allowlist')
    for name in FILES-{'verify_math.py'}:
        must((original/'public'/name).read_bytes()==(corrected/'public'/name).read_bytes(),'unexpected corrected file: '+name)
    manifest={'schema':'authored-slice-manifest-v1','files':inventory(corrected/'public')}
    mp=corrected/'verification/MANIFEST.json'
    mp.write_text(json.dumps(manifest,indent=2)+'\n')
    manifest_pin=digest(mp.read_bytes())
    boot=(original/'verification/bootstrap.py').read_text().replace(ORIGINAL_PINS['verification/MANIFEST.json'],manifest_pin)
    bp=corrected/'verification/bootstrap.py'; bp.write_text(boot)
    pins={'original':{key:{'sha256':value,'bytes':len((original/key).read_bytes())} for key,value in ORIGINAL_PINS.items()},
          'corrected':{key:{'sha256':digest((corrected/key).read_bytes()),'bytes':len((corrected/key).read_bytes())}
                       for key in ['verification/MANIFEST.json','verification/bootstrap.py','public/replay.py','public/verify_math.py']}}
    (here/'EXTERNAL_PINS.json').write_text(json.dumps(pins,indent=2)+'\n')
    rows=[]

    def command(script,flags,*arguments):
        return [sys.executable,'-I','-B',*flags,str(script),*map(str,arguments)]

    def run(name,cmd,expected='PASS',mode=None,**kwargs):
        cp=subprocess.run(cmd,capture_output=True,text=True,timeout=60,**kwargs)
        try:
            result=json.loads(cp.stdout)
            status=result.get('status') if isinstance(result,dict) else None
        except (ValueError,TypeError):
            status=None
        if expected=='PASS':
            passed=cp.returncode==0 and status=='PASS'
        elif expected=='REJECT_JSON':
            passed=cp.returncode==2 and status=='REJECT'
        elif expected=='REJECT':
            passed=cp.returncode!=0 and status!='PASS'
        elif expected=='PROBE':
            passed=cp.returncode==0 and cp.stdout.strip()=='NONROOT_WRITES_DENIED'
        else:
            raise RuntimeError('unknown expectation')
        row={'name':name,'mode':mode,'expected':expected,'passed':passed,'returncode':cp.returncode,
             'observed_status':status,'stdout_sha256':digest(cp.stdout.encode()),
             'stderr_empty':not bool(cp.stderr)}
        if status=='REJECT' and isinstance(result.get('reason'),str) and '/' not in result['reason']:
            row['reason']=result['reason']
        rows.append(row)
        return cp

    certificate=json.loads((original/'public/certificate.json').read_text())
    acceptance_changes=[('boolean signs',{'expected_signs':[True,-1,True,-1,True]}),
                        ('float signs',{'expected_signs':[1.0,-1.0,1.0,-1.0,1.0]}),
                        ('boolean sample entries',{'sample_offsets':[[-1,True],[-1,3],[-1,5],[-1,7],[True,7]]}),
                        ('boolean correction degree',{'corrections':[[3,2],[2,6],[True,12]]}),
                        ('non-ASCII integer string',{'K':''.join(chr(0x660+int(c)) for c in certificate['K'])})]
    invalid=[]
    integer_fields=['problem_id','v_denominator_power10','coefficient_denominator_power10','point_denominator_power10',
                    'evaluation_denominator_power10','H_upper_bound','delta_comparison_power2',
                    'required_distinct_negative_roots','expected_distinct_corners']
    for field in integer_fields:
        for label,value in [('boolean',True),('float',float(certificate[field])),('NaN',float('nan')),
                            ('Infinity',float('inf')),('negative Infinity',float('-inf')),('null',None),('string','1')]:
            invalid.append((field+' '+label,{field:value}))
    for field in ['K','N']:
        for label,value in [('boolean',True),('integer',int(certificate[field])),('float',float(certificate[field])),
                            ('empty',''),('plus prefix','+'+certificate[field]),('minus prefix','-'+certificate[field]),
                            ('whitespace',' '+certificate[field]),('decimal point',certificate[field]+'.0'),
                            ('exponent form','1e20'),('oversize','1'*100),('superscript digit','²'),('NaN',float('nan'))]:
            invalid.append((field+' '+label,{field:value}))
    for field in ['factor_exponents','corrections','sample_offsets','expected_signs']:
        for label,value in [('null',None),('object',{}),('boolean',True),('string','1'),('empty',[])]:
            invalid.append((field+' '+label,{field:value}))
    for field in ['factor_exponents','expected_signs']:
        for value_name,value in [('bool',True),('float',1.0),('NaN',float('nan')),('Infinity',float('inf'))]:
            z=copy.deepcopy(certificate[field]); z[0]=value
            invalid.append((field+' nested '+value_name,{field:z}))
    for field in ['corrections','sample_offsets']:
        for value_name,value in [('bool',True),('float',1.0),('NaN',float('nan')),('Infinity',float('inf')),('null',None)]:
            z=copy.deepcopy(certificate[field]); z[0][0]=value
            invalid.append((field+' nested '+value_name,{field:z}))
        for value_name,value in [('wrong pair width',[1]),('null pair',None),('object pair',{})]:
            z=copy.deepcopy(certificate[field]);z[0]=value
            invalid.append((field+' '+value_name,{field:z}))
    mathematical=[('odd K',{'K':str(10**20+1),'N':str(2*(10**20+1)+100)}),
                  ('insufficient K',{'K':'100','N':'300'}),
                  ('wrong degree',{'N':str(2*10**20+102)}),
                  ('insufficient H bound',{'H_upper_bound':100000}),
                  ('insufficient coefficient denominator',{'coefficient_denominator_power10':71}),
                  ('insufficient point denominator',{'point_denominator_power10':41}),
                  ('bad denominator derivation',{'evaluation_denominator_power10':4271}),
                  ('weak filler comparison',{'delta_comparison_power2':49}),
                  ('wrong root target',{'required_distinct_negative_roots':5}),
                  ('wrong corner target',{'expected_distinct_corners':4}),
                  ('wrong sign',{'expected_signs':[-1,-1,1,-1,1]}),
                  ('wrong problem',{'problem_id':2200014}),
                  ('extra key',{'unexpected':1})]

    with tempfile.TemporaryDirectory(prefix='tropical-independent-audit-') as td:
        temp=Path(td)
        for mode,flags in MODES:
            run('independent integer reconstruction',command(here/'independent_math.py',flags),mode=mode)
            for label,root in [('original',original),('corrected',corrected)]:
                run(label+' frozen bootstrap',command(root/'verification/bootstrap.py',flags,'--root',root/'public','--manifest',root/'verification/MANIFEST.json'),mode=mode)
            mutant=temp/'certificate.json'
            for label,changes in acceptance_changes:
                modified=copy.deepcopy(certificate);modified.update(changes);mutant.write_text(json.dumps(modified))
                run('original permissive parsing: '+label,command(original/'public/verify_math.py',flags,mutant),mode=mode)
                run('corrected rejects: '+label,command(corrected/'public/verify_math.py',flags,mutant),expected='REJECT_JSON',mode=mode)
            for label,changes in invalid+mathematical:
                modified=copy.deepcopy(certificate);modified.update(changes);mutant.write_text(json.dumps(modified))
                run('corrected rejects: '+label,command(corrected/'public/verify_math.py',flags,mutant),expected='REJECT_JSON',mode=mode)
            # JSON overflow literals parse as infinities without invoking
            # parse_constant; exact integer schema checks must reject them too.
            canonical_raw=json.dumps(certificate)
            for field in integer_fields+['K','N']:
                token=json.dumps(field)+': '+json.dumps(certificate[field])
                must(token in canonical_raw,'overflow mutation target absent')
                for literal in ['1e999','-1e999']:
                    mutant.write_text(canonical_raw.replace(token,json.dumps(field)+': '+literal,1))
                    run('corrected rejects overflow literal '+literal+' in '+field,command(corrected/'public/verify_math.py',flags,mutant),expected='REJECT_JSON',mode=mode)
            for field in ['factor_exponents','corrections','sample_offsets','expected_signs']:
                modified=copy.deepcopy(certificate)
                if field in ['corrections','sample_offsets']:
                    modified[field][0][0]='OVERFLOW_SENTINEL'
                else:
                    modified[field][0]='OVERFLOW_SENTINEL'
                mutant.write_text(json.dumps(modified).replace('"OVERFLOW_SENTINEL"','1e999'))
                run('corrected rejects nested overflow literal in '+field,command(corrected/'public/verify_math.py',flags,mutant),expected='REJECT_JSON',mode=mode)
            for label,raw in [('duplicate key','{"schema":0,'+(original/'public/certificate.json').read_text().lstrip()[1:]),
                              ('top-level NaN','NaN'),('top-level Infinity','Infinity'),('top-level negative Infinity','-Infinity'),
                              ('top-level list','[]'),('trailing data',(original/'public/certificate.json').read_text()+'0'),
                              ('malformed JSON','{'),('certificate size cap',' '*100001)]:
                mutant.write_text(raw)
                run('corrected rejects: '+label,command(corrected/'public/verify_math.py',flags,mutant),expected='REJECT_JSON',mode=mode)
            symlink=temp/'link.json'
            if symlink.exists():symlink.unlink()
            symlink.symlink_to(original/'public/certificate.json')
            run('corrected rejects symlink certificate',command(corrected/'public/verify_math.py',flags,symlink),expected='REJECT_JSON',mode=mode)
            run('corrected rejects missing certificate',command(corrected/'public/verify_math.py',flags,temp/'missing.json'),expected='REJECT_JSON',mode=mode)
            # Author arithmetic mutations must still be caught, without relying on assert.
            text=(corrected/'public/verify_math.py').read_text()
            for label,old,new in [('reversed direct correction','direct += v**2','direct -= v**2'),
                                  ('reversed seed evaluation','values = [evaluate(q,t) for t in points]','values = [-evaluate(q,t) for t in points]'),
                                  ('wrong leading seed','q = [F(1)]','q = [F(2)]')]:
                must(old in text,'mutation target absent')
                script=temp/'arithmetic_mutant.py';script.write_text(text.replace(old,new))
                run('arithmetic corruption rejected: '+label,command(script,flags,original/'public/certificate.json'),expected='REJECT_JSON',mode=mode)
            for label,root in [('original',original),('corrected',corrected)]:
                # Real relocation includes spaces and non-ASCII text, read-only inputs,
                # a hostile current directory and poisoned startup environment.
                stage=temp/(label+' '+mode+' relocated Ω');stage.mkdir()
                public=stage/'public';shutil.copytree(root/'public',public)
                manifest=stage/'manifest.json';manifest.write_bytes((root/'verification/MANIFEST.json').read_bytes())
                bootstrap=stage/'bootstrap.py';bootstrap.write_bytes((root/'verification/bootstrap.py').read_bytes())
                hostile=stage/'hostile';hostile.mkdir()
                marker=stage/'shadow-executed'
                for name in ['json','fractions','math','pathlib','hashlib','subprocess','argparse','sitecustomize','usercustomize','verify_math']:
                    (hostile/(name+'.py')).write_text('open('+repr(str(marker))+',"w").write("bad")\nraise RuntimeError("SHADOW_EXECUTED")\n')
                for p in public.iterdir():p.chmod(0o444)
                public.chmod(0o555);manifest.chmod(0o444);bootstrap.chmod(0o444)
                probe='import os,sys\nif os.getuid()==0 or os.geteuid()==0:sys.exit(1)\nfor p in sys.argv[1:]:\n try:\n  with open(p,"a") as f:f.write("bad")\n except PermissionError:pass\n else:sys.exit(2)\nprint("NONROOT_WRITES_DENIED")'
                run(label+' actual nonroot write-denial probe',command('-c',flags,probe,public/'certificate.json',public/'new-file',manifest,bootstrap),expected='PROBE',mode=mode)
                env=os.environ.copy();env.update(PYTHONPATH=str(hostile),PYTHONHOME=str(hostile),PYTHONSTARTUP=str(hostile/'sitecustomize.py'),PYTHONDONTWRITEBYTECODE='0')
                run(label+' relocated read-only hostile replay',command(bootstrap,flags,'--root',public,'--manifest',manifest),cwd=hostile,env=env,mode=mode)
                rows.append({'name':label+' no shadow import or replay writes','mode':mode,'passed':not marker.exists() and inventory(public)==inventory(root/'public') and {p.name for p in public.iterdir()}==FILES})
                public.chmod(0o755)
                for p in public.iterdir():p.chmod(0o644)
                manifest.chmod(0o644);bootstrap.chmod(0o644)
            # Every frozen slice file is individually corrupted in its own copy.
            for target in sorted(FILES):
                stage=temp/('tamper '+mode+' '+target);stage.mkdir()
                public=stage/'public';shutil.copytree(corrected/'public',public)
                file=public/target;file.write_bytes(file.read_bytes()+b'\n')
                run('frozen integrity rejects changed '+target,command(bp,flags,'--root',public,'--manifest',mp),expected='REJECT',mode=mode)
            for kind in ['extra file','missing file','symlink file','symlink root','symlink manifest','changed manifest','rehashed content','self-consistent forged gate']:
                stage=temp/('integrity '+mode+' '+kind);stage.mkdir()
                public=stage/'public';shutil.copytree(corrected/'public',public)
                manifest=stage/'manifest.json';manifest.write_bytes(mp.read_bytes())
                if kind=='extra file':(public/'EXTRA.txt').write_text('extra')
                elif kind=='missing file':(public/'README.md').unlink()
                elif kind=='symlink file':
                    (public/'README.md').unlink();(public/'README.md').symlink_to(corrected/'public/README.md')
                elif kind=='symlink root':
                    shutil.rmtree(public);public.symlink_to(corrected/'public',target_is_directory=True)
                elif kind=='symlink manifest':
                    manifest.unlink();manifest.symlink_to(mp)
                elif kind=='changed manifest':manifest.write_bytes(manifest.read_bytes()+b'\n')
                elif kind in ['rehashed content','self-consistent forged gate']:
                    (public/'PROOF.md').write_text('forged proof')
                    if kind=='self-consistent forged gate':
                        (public/'replay.py').write_text('print(\'{"status":"PASS"}\')\n')
                    changed={'schema':'authored-slice-manifest-v1','files':inventory(public)}
                    manifest.write_text(json.dumps(changed))
                run('bootstrap rejects '+kind,command(bp,flags,'--root',public,'--manifest',manifest),expected='REJECT',mode=mode)
            for pin in ['0'*64,manifest_pin.upper(),'not-a-digest']:
                run('replay rejects untrusted or malformed pin',command(corrected/'public/replay.py',flags,'--root',corrected/'public','--manifest',mp,'--manifest-sha256',pin),expected='REJECT_JSON',mode=mode)
            # Direct replay schema checks use explicitly supplied matching test
            # digests. These cannot pass the independently pinned bootstrap.
            base=json.loads(mp.read_text())
            manifests=[]
            for label,entry_changes in [('boolean byte count',{'bytes':True}),('float byte count',{'bytes':9287.0}),
                                        ('negative byte count',{'bytes':-1}),('nonfinite byte count',{'bytes':float('nan')}),
                                        ('path traversal',{'path':'../PROOF.md'}),('absolute path',{'path':'/PROOF.md'}),
                                        ('malformed digest',{'sha256':'bad'})]:
                mm=copy.deepcopy(base);mm['files'][0].update(entry_changes);manifests.append((label,json.dumps(mm)))
            mm=copy.deepcopy(base);mm['files'][1]=copy.deepcopy(mm['files'][0]);manifests.append(('duplicate manifest path',json.dumps(mm)))
            manifests.append(('duplicate manifest JSON key','{"schema":0,'+mp.read_text().lstrip()[1:]))
            for label,raw in manifests:
                malformed=temp/'malformed_manifest.json';malformed.write_text(raw)
                run('replay rejects '+label,command(corrected/'public/replay.py',flags,'--root',corrected/'public','--manifest',malformed,'--manifest-sha256',digest(raw.encode())),expected='REJECT_JSON',mode=mode)

    after={p.relative_to(original).as_posix():digest(p.read_bytes()) for p in original.rglob('*') if p.is_file()}
    must(before==after,'original freeze or source material was altered')
    report={'schema':'independent-tropical-reproducibility-audit-v1','uid':os.getuid(),'euid':os.geteuid(),
            'python':sys.version.split()[0],'original_preserved':True,'proof_bytes_unchanged':True,
            'corrected_public_files_changed':['verify_math.py'],'external_pins':pins,
            'control_count':len(rows),'passed_count':sum(row['passed'] for row in rows),
            'all_passed':all(row['passed'] for row in rows),'controls':rows}
    (here/'CONTROL_REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['control_count','passed_count','all_passed','uid','euid','original_preserved','proof_bytes_unchanged']},sort_keys=True))
    return 0 if report['all_passed'] else 1


if __name__=='__main__':
    sys.exit(main())
