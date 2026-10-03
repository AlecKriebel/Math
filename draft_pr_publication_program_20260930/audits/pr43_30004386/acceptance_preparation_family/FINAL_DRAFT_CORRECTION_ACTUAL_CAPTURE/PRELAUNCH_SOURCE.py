"""Own literal newline drafting repair and actual predecessor clock field correction."""
from pathlib import Path
import json,re,hashlib,datetime,os,difflib
H=Path(__file__).resolve().parent;records=[];diff=[];old=H/'preserved_before_final_draft_correction';old.mkdir(exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest()
for name in ['integrate_reviewed_partial.py','pr43_guards.py']:
    p=H/name;before=p.read_bytes();text=before.decode();(old/name).write_bytes(before)
    if name=='integrate_reviewed_partial.py':
        for variable in ['BODY','PRESENT_SCOPE']:
            pattern=r'^'+variable+r" = '([^\n]*)\n'"
            match=re.search(pattern,text,re.M)
            if not match:raise ValueError('Exact initial escaped newline drafting form required')
            text=re.sub(pattern,lambda m:variable+' = '+repr(m.group(1)+'\n'),text,count=1,flags=re.M)
    else:
        token="utc_clock(rootpost['created_utc'],'ROOT predecessor postUTC')"
        if text.count(token)!=1:raise ValueError('One prior ROOT post timestamp token')
        text=text.replace(token,"utc_clock(rootpost['utc'],'ROOT predecessor postUTC')")
    after=text.encode();p.write_bytes(after);records.append({'path':name,'before_bytes':len(before),'before_sha256':sha(before),'after_bytes':len(after),'after_sha256':sha(after)})
    diff+=list(difflib.unified_diff(before.decode().splitlines(True),text.splitlines(True),fromfile='before/'+name,tofile='prepared/'+name))
(H/'FINAL_DRAFT_CORRECTION.patch').write_text(''.join(diff))
record={'schema':'pr43-own-source-literal-and-actual-prior-clock-correction/v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_child_pid':os.getpid(),'changed_files':records,'reason':'Initial regex replacement interpreted backslash-newline escape; final literal uses callable replacement. Existing genuine predecessor ROOT post schema uses utc, not whole-review created_utc. Both fixes are source only.','production_sources_imported_compiled_executed':False}
(H/'FINAL_DRAFT_CORRECTION.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record))
