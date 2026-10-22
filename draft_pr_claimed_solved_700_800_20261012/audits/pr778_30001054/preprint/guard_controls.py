"""Corruption controls for the actual source inventory parser; no files are mutated."""
from pathlib import Path
import copy,json,sys
sys.dont_write_bytecode=True
from verify_bundle import validate_closed_map,read_closed
ROOT=Path(__file__).resolve().parent
payload=read_closed(ROOT)
cases=[]
def run(name,change,reject=True):
    data=dict(payload)
    change(data)
    try:
        validate_closed_map(data)
        failed=False
    except (ValueError,KeyError,TypeError,UnicodeError):
        failed=True
    if failed!=reject:
        raise RuntimeError('Wrong guard result: '+name)
    cases.append({'case':name,'rejected':failed})
def edit(change):
    def apply(data):
        m=json.loads(data['MANIFEST.json'])
        change(m)
        data['MANIFEST.json']=(json.dumps(m)+'\n').encode()
    return apply
run('baseline',lambda d:None,False)
run('altered_tex',lambda d:d.update({'paper.tex':d['paper.tex']+b'changed'}))
run('missing_tex',lambda d:d.pop('paper.tex'))
run('extra_hidden_file',lambda d:d.update({'.extra':b'extra'}))
run('duplicate_path',edit(lambda m:m['files'].append(dict(m['files'][0]))))
run('parent_path',edit(lambda m:m['files'][0].update(path='../outside')))
run('absolute_path',edit(lambda m:m['files'][0].update(path='/outside')))
run('noncanonical_path',edit(lambda m:m['files'][0].update(path='./paper.tex')))
run('backslash_path',edit(lambda m:m['files'][0].update(path='a\\b')))
run('self_manifest',edit(lambda m:m['files'][0].update(path='MANIFEST.json')))
run('boolean_length',edit(lambda m:m['files'][0].update(bytes=True)))
run('negative_length',edit(lambda m:m['files'][0].update(bytes=-1)))
run('bad_digest',edit(lambda m:m['files'][0].update(sha256='g'*64)))
run('duplicate_json_key',lambda d:d.update({'MANIFEST.json':b'{"schema":1,"schema":2}'}))
run('nonfinite_json',lambda d:d.update({'MANIFEST.json':b'{"schema":NaN}'}))
print(json.dumps({'status':'PASS','positive_controls':1,'negative_controls':14,
                  'scope':'Actual manifest parser and exact byte mapping, tested in RAM; physical filesystem guards and mathematical proof are separate.',
                  'authored_files_not_written':True,'cases':cases},sort_keys=True,indent=2))
