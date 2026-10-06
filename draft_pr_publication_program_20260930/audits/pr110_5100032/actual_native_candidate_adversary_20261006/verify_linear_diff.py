#!/usr/bin/env python3
"""Pure-data exact application of every complete diff; no native/source main execution."""
import pathlib,types,os,json,re,base64,hashlib,time,sys,random
W=pathlib.Path(__file__).resolve().parent
v=types.ModuleType('linear_diff_independent');v.__file__=str(W/'verify_actual_candidate.py');exec(compile(pathlib.Path(v.__file__).read_bytes(),v.__file__,'exec'),v.__dict__)
N='unsolved_math_prioritization/'
P=N+'attempts/5100032/'
checks=0
def need(x,m):
    global checks
    checks+=1
    if not x:raise ValueError(m)
def lines(b):
    # Independent scanner; retain exact byte terminators, splitting only LF.
    out=[];start=0
    while True:
        end=b.find(b'\n',start)
        if end<0:
            if start<len(b):out.append(b[start:])
            return out
        out.append(b[start:end+1]);start=end+1

def parsed_range(start,count):
    s=int(start);n=1 if count is None else int(count)
    need(s>=0 and n>=0,'nonnegative range')
    need(n==0 or s>=1,'nonempty ranges count from one')
    return (s if n==0 else s-1),n

def apply_all(diff,before,offers,cap=1048576):
    need(type(diff) is bytes and len(diff)<=cap,'complete bounded diff bytes')
    rows=lines(diff);pos=0;results=[]
    for path,want in offers.items():
        old=before.get(path[len(N):]) if path.startswith(N) else None
        need(pos<len(rows),'missing complete path entry')
        if rows[pos].startswith(b'Complete new binary addition '):
            need(old is None,'binary entry cannot replace native body')
            header=b'Complete new binary addition '+path.encode()+b' '
            need(rows[pos].startswith(header),'exact binary path/order')
            spec=json.loads(rows[pos][len(header):]);pos+=1
            need(pos<len(rows) and rows[pos].endswith(b'\n'),'full binary base64 line')
            decoded=base64.b64decode(rows[pos][:-1],validate=True);pos+=1
            need(spec==v.pin(decoded) and decoded==want,'exact full binary count/hash/body')
            try:decoded.decode('utf8')
            except UnicodeDecodeError:pass
            else:raise ValueError('UTF8 body falsely called binary')
            results.append({'path':path,'kind':'binary','after':v.pin(decoded)});continue
        need(rows[pos]==b'--- '+(b'/dev/null' if old is None else b'a/'+path.encode())+b'\n','exact old header/order');pos+=1
        need(pos<len(rows) and rows[pos]==b'+++ b/'+path.encode()+b'\n','exact new header/order');pos+=1
        need(pos<len(rows),'missing hunk')
        h=re.fullmatch(rb'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@\n',rows[pos]);need(h is not None,'strict complete hunk header');pos+=1
        os_,oc=parsed_range(h[1],h[2]);ns,nc=parsed_range(h[3],h[4]);previous=lines(b'' if old is None else old)
        need(os_==ns and os_+oc<=len(previous),'single-hunk global prefix/start/count')
        removed=[];added=[];tags=[]
        while len(removed)<oc or len(added)<nc:
            need(pos<len(rows),'hunk truncated');record=rows[pos];pos+=1
            need(record[:1] in [b' ',b'-',b'+'] and record.endswith(b'\n'),'body sign/terminator')
            tag=record[:1];body=record[1:]
            if pos<len(rows) and rows[pos]==b'\\ No newline at end of file\n':body=body[:-1];pos+=1
            if tag in [b' ',b'-']:removed.append(body)
            if tag in [b' ',b'+']:added.append(body)
            tags.append(tag)
            need(len(removed)<=oc and len(added)<=nc,'strict hunk count overflow')
        need(removed==previous[os_:os_+oc],'every removed/context byte matches actual full preimage')
        actual=b''.join(previous[:os_]+added+previous[os_+oc:])
        need(actual==want,'independent complete application reproduces actual offered body')
        # Shape of the specified single replacement hunk: context,-,+,context.
        state=0
        for tag in tags:
            if tag==b'-':need(state<=1,'replacement removal order');state=1
            elif tag==b'+':need(state<=2,'replacement addition order');state=2
            elif state>0:state=3
        lead=0
        for tag in tags:
            if tag!=b' ':break
            lead+=1
        tail=0
        for tag in reversed(tags):
            if tag!=b' ':break
            tail+=1
        need(lead<=3 and tail<=3,'bounded exact three-line context')
        results.append({'path':path,'kind':'text','global_old_start':os_,'old_count':oc,'global_new_start':ns,'new_count':nc,'after':v.pin(actual)})
    need(pos==len(rows),'no omitted/injected path/hunk/body after complete entries')
    return results

def main():
    began=v.now();suffix='optimized' if sys.flags.optimize else 'normal'
    hp=v.A/'native_post_assess_carryforward_v3_20261006/linear_full_diff.py';source=v.regular(hp)
    module=types.ModuleType('reviewed_linear_helper');module.__file__=str(hp);exec(compile(source,str(hp),'exec'),module.__dict__)
    need(b'SequenceMatcher' not in source and b'difflib' not in source,'No matching-algorithm dependency')
    pairs=[(b'',b'a'),(b'',b''),(b'a',b''),(b'a',b'b'),(b'a\n',b'a'),(b'a',b'a\n'),(b'a\r\n',b'b\r\n'),(b'a\r',b'b\r'),(b'\n',b''),(b'',b'\n'),(b'a\n\n',b'a\n'),(b'x\ny\nz\n'*20,b'x\ny\nz\n'*11+b'insert\n'+b'x\ny\nz\n'*9),(b'0\n1\n2\n3\n4\n5\n6\n7\n8\n9',b'0\n1\n2\n3\n4\n5\n6\n7\nchange\n9')]
    unique=0
    for i,(old,new) in enumerate(pairs):
        path=P+'edge'+str(i)+'.txt'
        if old==new:
            diff=module.full_diff({}, {path:new},P);apply_all(diff,{}, {path:new});continue
        before={'QUEUE.md':old};offers={N+'QUEUE.md':new};diff=module.full_diff(before,offers,P);apply_all(diff,before,offers);unique+=1
    # Whole-body UTF8, byte LF rather than Unicode separator line classification.
    for new in ['one\u2028two\u0085three\rtrail','--- path\n+++ path\n@@ -0,0 +1 @@\n\\ No newline at end of file','π\r\n😀'].copy():
        body=new.encode();diff=module.full_diff({}, {P+'unicode.txt':body},P);apply_all(diff,{}, {P+'unicode.txt':body});unique+=1
    # Exhaustive finite insert/delete/replace, repeated lines and missing final LF.
    rng=random.Random(5100032)
    for i in range(300):
        old=b''.join(rng.choice([b'a\n',b'b\r\n',b'\n',b'x\r',b'\xce\xbb\n']) for j in range(rng.randrange(25)))
        new=b''.join(rng.choice([b'a\n',b'b\r\n',b'\n',b'x\r',b'\xce\xbb\n']) for j in range(rng.randrange(25)))
        if new==old:new+=b'changed'
        before={'QUEUE.md':old};offers={N+'QUEUE.md':new};diff=module.full_diff(before,offers,P);apply_all(diff,before,offers);unique+=1
    additions={P+'a space.txt':b'',P+'binary.bin':b'\xff\x00\n\x80',P+'normal.txt':b'end'};diff=module.full_diff({},additions,P);apply_all(diff,{},additions)
    rejected=[]
    def reject(label,callback):
        try:callback()
        except (ValueError,TypeError,UnicodeDecodeError,KeyError,IndexError):rejected.append(label)
        else:raise ValueError('Mutant accepted '+label)
    base={N+'QUEUE.md':b'changed\n'};bfr={'QUEUE.md':b'old\n'};d=module.full_diff(bfr,base,P)
    for label,mut in [('wrongold',d.replace(b'--- a/',b'--- z/',1)),('wrongnew',d.replace(b'+++ b/',b'+++ z/',1)),('badcount',d.replace(b'@@ -1 +1 @@',b'@@ -1,2 +1 @@',1)),('badglobal',d.replace(b'@@ -1 +1 @@',b'@@ -2 +2 @@',1)),('wrongremoved',d.replace(b'-old\n',b'-evil\n',1)),('wrongadded',d.replace(b'+changed\n',b'+evil\n',1)),('truncated',d[:-1]),('duplicateentry',d+d),('falsemarker',d.replace(b'-old\n',b'-old\n\\ No newline at end of file\n',1))]:reject(label,lambda mut=mut:apply_all(mut,bfr,base))
    zero=module.full_diff({}, {P+'empty':b''},P)
    reject('omittedzero-count',lambda:apply_all(zero.replace(b'-0,0 +0,0',b'-0 +0'),{}, {P+'empty':b''}))
    reject('cap-one-byte',lambda:module.full_diff(bfr,base,P,cap=len(d)-1));need(module.full_diff(bfr,base,P,cap=len(d))==d,'exact cap accepted')
    for path in ['/abs','../escape',P+'../x',P+'double//x',P+'bad\npath','other/target.txt']:
        reject('badpath-'+repr(path),lambda path=path:module.full_diff({}, {path:b'x'},P))
    reject('unchangednative',lambda:module.full_diff({'QUEUE.md':b'x'},{N+'QUEUE.md':b'x'},P))
    reject('nativebinary',lambda:module.full_diff({'QUEUE.md':b'x'},{N+'QUEUE.md':b'\xff'},P))
    reject('capbool',lambda:module.full_diff({}, {P+'x':b'x'},P,cap=True))
    bin_d=module.full_diff({}, {P+'binary':b'\xff'},P)
    reject('wrongbinaryhash',lambda:apply_all(bin_d.replace(v.sha(b'\xff').encode(),b'0'*64),{},{P+'binary':b'\xff'}))
    reject('wrongbinarybase64',lambda:apply_all(bin_d[:-3]+b'??\n',{},{P+'binary':b'\xff'}))
    two={P+'first':b'a',P+'second':b'b'};two_d=module.full_diff({},two,P)
    reject('wrongpathorder',lambda:apply_all(two_d,{},dict(reversed(list(two.items())))))
    integration=v.obj(v.regular(v.A/'current_main_carryforward_input_20261006/CURRENT_INTEGRATION_INPUTS.json'));packet=v.obj(v.regular(v.PACKET));packet={**packet,'main_parent':integration['main_parent']};before={}
    for name,spec in integration['native_baseline'].items():
        body=v.git_blob(packet,name);need(v.pin(body)=={k:spec[k] for k in ['bytes','sha256']},'Full genuine current native preimage');before[name]=body
    stopped=v.A/'native_post_assess_carryforward_v2_20261006/workspaces/candidate_d9eb646c1dd70e89'
    offers={str(f.relative_to(stopped/'offer')):v.regular(f) for f in sorted((stopped/'offer').rglob('*')) if f.is_file()};need(len(offers)==84,'All84 actual stopped offer bodies')
    mono=time.monotonic();actualdiff=module.full_diff(before,offers,P);duration=time.monotonic()-mono
    mono=time.monotonic();application=apply_all(actualdiff,before,offers);application_duration=time.monotonic()-mono
    output=W/('PURE_LINEAR_STOPPED_OFFER_DIFF_'+suffix+'.txt');need(not output.exists(),'unique pure review output');output.write_bytes(actualdiff)
    result={'schema':'pr110-independent-pure-linear-diff-control/v1','UTC_start':began,'UTC_end':v.now(),'actual_reviewer_PID':os.getpid(),'optimized':bool(sys.flags.optimize),'checks':checks,'library_guards':v.checks,'helper_pin':{'path':str(hp.relative_to(v.A)),**v.pin(source)},'edge_and_seeded_bytecases':unique,'explicit_rejections':rejected,'all84_actual_stopped_offers_applied_exactly':True,'all84_entry_application':application,'full_current_native_preimage_pins':{n:v.pin(b) for n,b in before.items()},'pure_stopped_offer_diff_pin':{'path':str(output.relative_to(v.A)),**v.pin(actualdiff)},'actual_full84_generation_seconds':duration,'independent_full84_application_seconds':application_duration,'future_candidate_approved':False,'native_assess_calls':0,'native_source_main_execution':False,'Git_mutations':0,'service_calls':0,'verification_source_pin':v.pin(pathlib.Path(__file__).read_bytes())}
    v.save('LINEAR_DIFF_CONTROL_'+suffix+'.json',result);v.save('LINEAR_DIFF_GIT_JOURNAL_'+suffix+'.json',v.journal);print(json.dumps({k:z for k,z in result.items() if k not in ['all84_entry_application','full_current_native_preimage_pins']}))
if __name__=='__main__':main()
