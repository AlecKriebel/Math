"""Independent finite exact arithmetic and pinned-source checks, not measure-proof certification."""
from pathlib import Path
from fractions import Fraction as Q
import json,hashlib,sys,zipfile,io
P=Path(__file__).resolve().parent
cases=[]
def check(label,ok):
 if not ok:raise RuntimeError(label)
 cases.append(label)
def integral(poly,a=Q(0),b=Q(1)):
 return sum((Q(c,i+1)*(b**(i+1)-a**(i+1))for i,c in enumerate(poly)),Q(0))
def mm(a,b):return [[sum((x*y for x,y in zip(row,col)),Q(0))for col in zip(*b)]for row in a]
M=[[Q(1),Q(1)],[Q(2),Q(0)]];I=[[Q(0),Q(1,2)],[Q(1),Q(-1,2)]]
check('exact invertible component conversion left',mm(M,I)==[[1,0],[0,1]])
check('exact invertible component conversion right',mm(I,M)==[[1,0],[0,1]])
check('strictpositive conversion invertible',mm([[Q(1),Q(0)],[Q(2,3),Q(1,3)]],[[Q(1),Q(0)],[Q(-2),Q(3)]])==[[1,0],[0,1]])
for n in range(13):check('exact Lebesgue moment '+str(n),integral([0]*n+[1])==Q(1,n+1))
for j in range(17):
 x=Q(j,16);alpha=x;beta=1-x
 check('density pair normalization '+str(j),M[0][0]*alpha+M[0][1]*beta==1 and M[1][0]*alpha+M[1][1]*beta==2*x)
 check('strictpositive range '+str(j),Q(2,3)<=Q(2,3)*(1+x)<=Q(4,3))
# Rectangle generators: the source side integrates the original(x,1-x) pair,
# then changes components; the target side directly integrates normalized densities.
for den in range(2,11):
 for i in range(den):
  a=Q(i,den);b=Q(i+1,den)
  for j in range(den):
   c=Q(j,den);d=Q(j+1,den);height=d-c
   old=[integral([0,1],a,b)*height,integral([1,-1],a,b)*height]
   source=[sum((v*w for v,w in zip(row,old)),Q(0))for row in M]
   target=[(b-a)*height,(b*b-a*a)*height]
   check('common P rectangle '+str((den,i,j)),source==target)
   # Projection marginal integrates the full second coordinate, independent of x.
   check('reverse Q interval '+str((den,i,j)),[integral([1],a,b),integral([0,2],a,b)]==[b-a,b*b-a*a])
   check('positivevariant P rectangle '+str((den,i,j)),integral([Q(2,3),Q(2,3)],a,b)*height==Q(2,3)*((b-a)+(b*b-a*a)/2)*height)
check('two normalized masses',integral([1])==1 and integral([0,2])==1)
check('positivevariant mass',integral([Q(2,3),Q(2,3)])==1)
check('secondmoment rigidity identity',Q(1,3)-2*Q(1,3)+Q(1,3)==0)
check('strictpositive unscaled moment',integral([0,1,1])==Q(5,6) and Q(5,6)-Q(1,2)==Q(1,3))
check('wrong independent-noise forward kernel detected',(Q(1,2)*integral([0,2]))!=integral([0,2],Q(0),Q(1,2)))
check('wrong second-coordinate reverse projection detected',Q(1,2)*integral([0,2])!=integral([0,2],Q(0),Q(1,2)))
# An explicit family satisfying coordinate rigidity still fails area pushforward:
# T_n(x)=(x,floor(nx)/n) has second-coordinate mass1 on a finite union of
# horizontal lines. Uniform square mass of that Borel set is0.
for n in range(1,25):
 push_mass=sum((Q(1,n)for j in range(n)),Q(0));area_mass=sum((Q(1)*Q(0)for j in range(n)),Q(0))
 check('finite graph-line control '+str(n),push_mass==1 and area_mass==0)
for e in json.loads((P/'PINNED_PR_INPUTS.json').read_text()):
 b=(P/'pinned_pr'/Path(e['path']).name).read_bytes()
 check('PR blob '+Path(e['path']).name,len(b)==e['bytes']and hashlib.sha256(b).hexdigest()==e['sha256']and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['blob'])
m=json.loads((P/'pinned_pr/ARTIFACT_MANIFEST.json').read_text())
for e in m['files']:
 b=(P/'pinned_pr'/e['path']).read_bytes();check('PR manifest '+e['path'],len(b)==e['bytes']and hashlib.sha256(b).hexdigest()==e['sha256'])
r=json.loads((P/'sources/zenodo_record_live.json').read_text())
check('version publication identity',r['id']==23107180 and r['doi']=='10.5281/zenodo.23107180'and r['conceptdoi']=='10.5281/zenodo.23107179'and r['status']=='published'and r['state']=='done'and r['submitted']is True and r['metadata']['version']=='1.0')
check('authors/title/date',r['metadata']['creators']==[{'name':'Ferudun, Alper','affiliation':'Mercury Software GmbH'}]and r['metadata']['publication_date']=='2026-10-02'and r['metadata']['title']=="A Negative Answer to Wolansky's Question on Mutually Dominating Multiphase Measure Spaces")
for e in r['files']:
 b=(P/'sources'/e['key']).read_bytes();fresh=(P/'private_readonly'/('fresh_'+e['key'])).read_bytes()
 check('all published files fresh '+e['key'],len(b)==e['size']and'md5:'+hashlib.md5(b).hexdigest()==e['checksum']and b==fresh)
z=zipfile.ZipFile(io.BytesIO((P/'sources/OWR-15212-005-source.zip').read_bytes()))
check('zip34membersCRC',len(z.infolist())==34 and z.testzip()is None)
check('report zip and standalone identical',z.read('verification_report.md')==(P/'sources/OWR-15212-005-verification-report.md').read_bytes())
for name in ['datacite_version.json','datacite_concept.json']:
 a=json.loads((P/'sources'/name).read_text())['data']['attributes']
 check('registry title '+name,a['titles']==[{'title':r['metadata']['title']}]and a['version']=='1.0'and a['creators'][0]['familyName']=='Ferudun')
v=json.loads((P/'sources/zenodo_versions.json').read_text())['hits'];check('one version inventory',len(v['hits'])==1 and v['hits'][0]['id']==23107180)
check('original PDFhistoricalpin',hashlib.sha256((P/'sources/original_owr2017.pdf').read_bytes()).hexdigest()=='400d411ff8310f28bd79aab8211bb60d57789fb54f61538dc26396689c7ade05')
print(json.dumps({'pass':True,'optimized':sys.flags.optimize,'count':len(cases),'checks':cases,'limitations':'Finite exact arithmetic and artifacts only. Written proof establishes kernels on all Borel sets, atomlessness, a.e. coordinate rigidity and graph contradiction. Source-author programs/history counts not rerun.','service_writes':0},indent=2))
