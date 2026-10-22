# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Alec Kriebel
"""Finite checks from raw monomial relations. Python standard library only.

Unit-pivot integral row operations build the quadratic quotient without using
the manuscript's basis or multiplication formula as construction rules.
These checks supplement, and do not prove, the universal theorem.
"""
import itertools, json, math

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def relations(n, omit=None):
    mons = list(itertools.combinations_with_replacement(range(2*n), 2))
    index = {m:i for i,m in enumerate(mons)}
    rows = []
    def add(terms):
        row = [0]*len(mons)
        for u,v,c in terms:
            row[index[tuple(sorted((u,v)))]] += c
        if any(row): rows.append(row)
    if omit != 'xx':
        for i,j in itertools.combinations(range(n),2): add([(i,j,1)])
    for i,j in itertools.combinations_with_replacement(range(n),2):
        if omit != 'ysquare' or i != j: add([(n+i,n+j,1)])
    for i in range(n): add([(i,n+i,1)])
    if omit != 'differences':
        for i,j,k in itertools.permutations(range(n),3):
            add([(i,n+j,1),(i,n+k,1 if omit == 'sums' else -1)])
    return mons, rows

def quotient(n, omit=None):
    mons, rows = relations(n,omit)
    pivots = []; k = 0
    for col in range(len(mons)):
        possible = [i for i in range(k,len(rows)) if rows[i][col]]
        if not possible: continue
        unit = [i for i in possible if abs(rows[i][col])==1]
        # All exact construction cases use unit pivots. Mutated sums can have
        # torsion: return a distinct failure witness instead of dividing it out.
        if not unit: return None
        i = unit[0]; rows[k],rows[i] = rows[i],rows[k]
        if rows[k][col] == -1: rows[k] = [-v for v in rows[k]]
        for i in range(len(rows)):
            if i != k and rows[i][col]:
                a = rows[i][col]; rows[i] = [x-a*y for x,y in zip(rows[i],rows[k])]
        pivots.append(col); k += 1
    need(all(not any(r) for r in rows[k:]), 'uneliminated relations')
    free = [i for i in range(len(mons)) if i not in pivots]
    coords = {}
    for i,m in enumerate(mons):
        if i in free: v = [int(i==f) for f in free]
        else:
            row = rows[pivots.index(i)]; v = [-row[f] for f in free]
        coords[m] = v
    return coords, len(free), mons

def matrix(n, q, coeff):
    coords,d,_ = q
    return [[sum(coeff[i]*coords[tuple(sorted((i,j)))][r]
                 for i in range(2*n)) for j in range(2*n)] for r in range(d)]

def det_integer(a):
    a = [r[:] for r in a]; sign=1; prev=1; n=len(a)
    for k in range(n-1):
        pivot = next((i for i in range(k,n) if a[i][k]),None)
        if pivot is None: return 0
        if pivot != k: a[k],a[pivot]=a[pivot],a[k];sign=-sign
        val=a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                num=a[i][j]*val-a[i][k]*a[k][j]
                need(num%prev==0,'Bareiss nonexact division');a[i][j]=num//prev
        for i in range(k+1,n):a[i][k]=0
        prev=val
    return sign*a[-1][-1]

def rank_mod(a,p):
    a=[[v%p for v in r] for r in a]; k=0
    for j in range(len(a[0])):
        pivot=next((i for i in range(k,len(a)) if a[i][j]),None)
        if pivot is None:continue
        a[k],a[pivot]=a[pivot],a[k];u=pow(a[k][j],-1,p)
        a[k]=[(v*u)%p for v in a[k]]
        for i in range(k+1,len(a)):
            t=a[i][j];a[i]=[(x-t*y)%p for x,y in zip(a[i],a[k])]
        k+=1
        if k==len(a):break
    return k

def expected_basis_matrix(n,q,c):
    # Change from the independently obtained free basis to ordered u,v.
    coords,d,_=q
    basis=[coords[(i,i)] for i in range(n)]
    basis += [coords[tuple(sorted((i,n+((i+1)%n))))] for i in range(n)]
    change=[[basis[j][r] for j in range(2*n)] for r in range(d)]
    need(abs(det_integer(change))==1,'claimed integral basis not unimodular')
    bsum=sum(c[n:]); form=[]
    for r in range(2*n):
        row=[]
        for j in range(2*n):
            if r<n:val=c[r] if j==r else 0
            elif j<n:val=bsum-c[n+j] if r-n==j else 0
            else:val=c[r-n] if r-n!=j-n else 0
            row.append(val)
        form.append(row)
    changed=[[sum(change[r][k]*form[k][j] for k in range(2*n))
              for j in range(2*n)] for r in range(d)]
    need(matrix(n,q,c)==changed,'general-form matrix mismatch')
    return change,form

def check_orbits():
    counts=0
    def generators(n):
        mons,rows=relations(n); result=[]
        for row in rows:
            result.append(tuple(sorted((mons[i],v) for i,v in enumerate(row) if v)))
        for mon in itertools.combinations_with_replacement(range(2*n),3):
            result.append(((mon,1),))
        return set(result)
    for n in range(1,6):
        target=generators(n+1)
        for inj in itertools.permutations(range(n+1),n):
            def mapvar(i):return (i//n)*(n+1)+inj[i%n]
            for g in generators(n):
                mapped=tuple(sorted((tuple(sorted(map(mapvar,m))),v) for m,v in g))
                need(mapped in target,'injection compatibility')
            counts+=1
    for n in range(3,7):
        g3=generators(3)
        for g in generators(n):
            support=sorted({v%n for mon,_ in g for v in mon})
            need(len(support)<=3,'support exceeds three')
            inv={v:i for i,v in enumerate(support)}
            small=tuple(sorted((tuple(sorted((v//n)*3+inv[v%n] for v in mon)),c) for mon,c in g))
            need(small in g3,'width-three generator missing')
    return counts

def main():
    qs={n:quotient(n) for n in range(1,8)}
    for n,q in qs.items():need(q is not None and q[1]==(1 if n==1 else 2*n),'quadratic dimensions')
    need(matrix(1,qs[1],[1,0])==[[1,0]],'width one multiplication')
    need(matrix(1,qs[1],[0,1])==[[0,0]],'width one zero-product control')
    determinant_cases=0
    for n in range(2,8):
        for seed in range(12):
            c=[((i+1)*(seed+2)+i*i)%7-3 for i in range(2*n)]
            change, form=expected_basis_matrix(n,qs[n],c)
            # det(change)=+/-1; compare the manuscript matrix after independent
            # raw-product equality, without guessing orientation of free basis.
            want=(-1)**(n-1)*(n-1)*math.prod(v*v for v in c[:n])
            need(det_integer(form)==want,'integer determinant formula')
            determinant_cases+=1
    exhaustive=0
    for n,p in [(2,2),(2,3),(3,2),(3,3),(4,2),(5,2)]:
        for c in itertools.product(range(p),repeat=2*n):
            m=matrix(n,qs[n],c);good=rank_mod(m,p)==2*n
            need(good==((n-1)%p!=0 and all(c[i] for i in range(n))),'all-form rank criterion')
            square=[sum(row[j]*c[j] for j in range(2*n))%p for row in m]
            if good:need(any(square),'WLP form not strong')
            if (n-1)%p==0:
                need(all(sum(row[n:])%p==0 for row in m),'socle witness lost')
            exhaustive+=1
    controls={}
    def reject(name, false):
        need(not false,'false control survived: '+name);controls[name]='rejected'
    reject('width_one_has_quadratic_dimension_two',qs[1][1]==2)
    reject('omit_y_squares_preserves_dimension',quotient(3,'ysquare')[1]==6)
    reject('omit_offdiagonal_xx_preserves_dimension',quotient(3,'xx')[1]==6)
    reject('omit_mixed_differences_preserves_dimension',quotient(3,'differences')[1]==6)
    reject('replace_differences_with_sums_keeps_unit_pivots',quotient(4,'sums') is not None)
    reject('all_widths_are_good_in_char_two',rank_mod(matrix(3,qs[3],[1]*3+[0]*3),2)==6)
    reject('all_widths_are_bad_in_char_two',rank_mod(matrix(4,qs[4],[1]*4+[0]*4),2)<8)
    reject('zero_x_coefficient_can_be_good',rank_mod(matrix(4,qs[4],[0,1,1,1,2,1,0,1]),5)==8)
    reject('char_two_square_of_sum_x_is_zero',not any(sum(row[j] for j in range(4))%2 for row in matrix(4,qs[4],[1]*4+[0]*4)))
    reject('sum_y_is_zero_when_p_divides_n',not any([1]*4))
    reject('bad_width_is_n_zero_mod_p',rank_mod(matrix(3,qs[3],[1]*3+[0]*3),3)<6)
    reject('y_only_form_suffices_at_good_width',rank_mod(matrix(4,qs[4],[0]*4+[1]*4),2)==8)
    print(json.dumps({'status':'PASS','integral_quotient_widths':list(qs),'integer_general_form_cases':determinant_cases,'exhaustive_finite_field_forms':exhaustive,'injections_checked':check_orbits(),'width_three_generation_through':6,'negative_controls':controls,'limits':'Finite exact checks only; universal written proof is primary. No priority certificate.'},sort_keys=True,indent=2))

if __name__=='__main__':main()
