"""Compile the unmodified production helper prefix with an independent rank oracle.
The prefix before int main() is copied verbatim into a disposable translation unit;
only a new test main is appended. This does not modify the frozen source.
"""
import json, subprocess, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
TEST=r'''
int oracle(array<int,7> cols){int a[7][7];for(int i=0;i<7;i++)for(int j=0;j<7;j++)a[i][j]=dig[cols[j]][i];int r=0;for(int j=0;j<7;j++){int p=r;while(p<7&&!a[p][j])p++;if(p==7)continue;for(int k=0;k<7;k++)swap(a[p][k],a[r][k]);int inv=a[r][j];for(int k=0;k<7;k++)a[r][k]=a[r][k]*inv%3;for(int i=0;i<7;i++)if(i!=r){int c=a[i][j];for(int k=0;k<7;k++)a[i][k]=(a[i][k]-c*a[r][k]+6)%3;}r++;}return r;}
int main(){pw[0]=1;for(int j=1;j<=7;j++)pw[j]=3*pw[j-1];for(int a=0;a<Q;a++)for(int j=0;j<7;j++)dig[a][j]=a/pw[j]%3;
for(int a=0;a<Q;a++)for(int b=0;b<Q;b++){int v=0;for(int j=0;j<7;j++)v+=((dig[a][j]+dig[b][j])%3)*pw[j];addt[a*Q+b]=v;}
// rk only multiplies by prime-field scalars; initialize these independently.
for(int a=0;a<3;a++)for(int b=0;b<Q;b++){int v=0;for(int j=0;j<7;j++)v+=(a*dig[b][j]%3)*pw[j];mult[a*Q+b]=v;}
unsigned int state=1;int cases=0;
for(int t=0;t<20000;t++){array<int,7> c{};for(int j=0;j<7;j++){state=1664525u*state+1013904223u;c[j]=(t%8>j)?int(state%Q):0;}if(rk(c)!=oracle(c))throw runtime_error("rank oracle mismatch");cases++;}
for(int mask=0;mask<128;mask++){array<int,7> c{};int expected=0;for(int j=0;j<7;j++)if(mask&(1<<j)){c[j]=pw[j];expected++;}if(rk(c)!=expected)throw runtime_error("basis rank mismatch");cases++;}
cout<<"{\"production_rank_cases\": "<<cases<<", \"independent_oracle\": \"passed\"}\n";
}
'''
def main():
    source=(ROOT/'finite_test.cpp').read_text()
    if source.count('int main(){')!=1:raise ValueError('unique production prefix boundary')
    derived=source.split('int main(){')[0]+TEST
    result=[]
    with tempfile.TemporaryDirectory(prefix='theta-rank-') as t:
        p=Path(t)/'rank.cpp';p.write_text(derived)
        for extra in ([],['-DNDEBUG']):
            flags=['-std=c++17','-O2','-Wall','-Wextra','-pedantic',*extra]
            proc=subprocess.run(['g++',*flags,str(p),'-o',str(Path(t)/'rank')],capture_output=True,text=True)
            if proc.returncode:raise RuntimeError(proc.stderr)
            out=subprocess.run([str(Path(t)/'rank')],capture_output=True,text=True)
            if out.returncode:raise RuntimeError(out.stderr)
            result.append({'flags':flags,'stdout':out.stdout,'stderr':out.stderr,'compiler_stdout':proc.stdout,'compiler_stderr':proc.stderr})
    print(json.dumps({'status':'PASS','runs':result},indent=2))
if __name__=='__main__':main()
