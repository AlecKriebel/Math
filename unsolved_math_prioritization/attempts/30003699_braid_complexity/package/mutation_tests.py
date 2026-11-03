#!/usr/bin/env python3
"""Negative controls using writable disposable copies only; no sockets."""
import ast, contextlib, io, json, os, shutil, sys, tempfile
from pathlib import Path
from unittest.mock import patch
sys.dont_write_bytecode=True
from validate import validate, require
ROOT=Path(__file__).resolve().parent

def fixture(destination):
    shutil.copytree(ROOT,destination)
    destination.chmod(0o700)
    for p in destination.iterdir():p.chmod(0o600)
    return destination

def main():
    validate(ROOT)
    source=(ROOT/'check_coefficients.py').read_text()
    results=[]
    # These single-expression changes alter mathematical values, not validation.
    edits=[('reflection_subtraction','r[n-1-i]-r[i]','r[n-1-i]+r[i]'),
           ('stirling_multiplier','+k*s[n-1][k]','+(k+1)*s[n-1][k]'),
           ('characteristic_block_factor','[-(n-1),1]','[-n,1]'),
           ('associated_stirling_multiplier','(n-1)*(d[n-2][k-1]+d[n-1][k])','n*(d[n-2][k-1]+d[n-1][k])'),
           ('labeled_component_factor','math.comb(n-1,j-1)','math.comb(n,j)'),
           ('odd_rank_leading','m=n//2;return Fraction(dfact(2*m-3)*(2*m-1)**(m-2))','m=n//2;return Fraction(dfact(2*m-3)*(2*m-1)**(m-2)+1)'),
           ('even_rank_leading','-Fraction(m-2)*','+Fraction(m-2)*')]
    with tempfile.TemporaryDirectory(prefix='braid-controls-') as t:
        tmp=Path(t)
        for name,old,new in edits:
            require(source.count(old)==1,'unique mutation target '+name)
            mutant=source.replace(old,new)
            ast.parse(mutant)
            path=tmp/(name+'.py');path.write_text(mutant)
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    exec(compile(mutant,str(path),'exec'),{'__name__':'__main__'})
            except ValueError as exc:
                results.append({'name':name,'rejected':True,'reason':str(exc)})
            else:raise ValueError('undetected mathematical mutation '+name)
        # Require zero reads for bad inventory, including a poisoned manifest.
        for name in ['payload_symlink','manifest_symlink','directory','fifo','hardlink','manifest_hardlink']:
            root=fixture(tmp/name)
            if name=='payload_symlink':
                (root/'AUDIT.md').unlink();(root/'AUDIT.md').symlink_to(tmp/'missing')
            elif name=='manifest_symlink':
                (root/'MANIFEST.json').unlink();(root/'MANIFEST.json').symlink_to(tmp/'missing')
            elif name=='directory':(root/'unexpected').mkdir()
            elif name=='fifo':os.mkfifo(root/'unexpected')
            elif name=='hardlink':os.link(root/'AUDIT.md',root/'unexpected')
            else:os.link(root/'MANIFEST.json',root/'unexpected')
            with patch.object(Path,'read_text',side_effect=RuntimeError('premature content read')),patch.object(Path,'read_bytes',side_effect=RuntimeError('premature content read')):
                try:validate(root)
                except ValueError:results.append({'name':name,'rejected':True,'content_reads':0})
                else:raise ValueError('accepted bad inventory '+name)
        for name in ['boolean_byte_count','boolean_schema','float_problem_id','duplicate_json_key','hash_change','unexpected_regular']:
            root=fixture(tmp/name);p=root/'MANIFEST.json';m=json.loads(p.read_text())
            if name=='boolean_byte_count':m['files'][0]['bytes']=True
            elif name=='boolean_schema':m['schema_version']=True
            elif name=='float_problem_id':m['problem_id']=30003699.0
            elif name=='hash_change':(root/'AUDIT.md').write_bytes(b'changed')
            elif name=='unexpected_regular':(root/'unexpected').write_bytes(b'x')
            if name=='duplicate_json_key':p.write_text('{"schema_version":1,'+p.read_text()[1:])
            else:p.write_text(json.dumps(m))
            try:validate(root)
            except ValueError:results.append({'name':name,'rejected':True})
            else:raise ValueError('accepted malformed fixture '+name)
    print(json.dumps({'status':'PASS','mathematical_controls':len(edits),'all_controls':len(results),'results':results,'actual_sockets_created':False,'fixtures':'writable disposable copies'},indent=2))
if __name__=='__main__':main()
