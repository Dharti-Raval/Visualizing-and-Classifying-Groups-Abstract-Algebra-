# cyclic C_n (represented as integers 0..n-1 under addition mod n)
def make_Cn(n):
    elems = list(range(n))
    def op(a,b): return (a + b) % n
    return FiniteGroup(f"C{n}", elems, op, 0)

# symmetric S_n using permutation tuples
def compose_perm(p, q):
    return tuple(p[i-1] for i in q)  # q then p; using 1-based elements in representation

def make_Sn(n):
    perms = [tuple(p) for p in itertools.permutations(range(1,n+1))]
    def op(a,b): return compose_perm(a,b)
    return FiniteGroup(f"S{n}", perms, op, tuple(range(1,n+1)))

# dihedral D_n as permutations of n points: rotation r and reflection s
def make_Dn(n):
    # represent permutations as tuples of images 0..n-1
    def rot(k):
        return tuple((i + k) % n for i in range(n))
    def refl(k):
        return tuple((( -i ) % n + k) % n for i in range(n))
    elems = [rot(k) for k in range(n)] + [refl(k) for k in range(n)]
    elems = list(dict.fromkeys(elems))
    def op(a,b): return tuple(a[b[i]] for i in range(n))
    return FiniteGroup(f"D{n}", elems, op, tuple(range(n)))

# quaternion Q8 with explicit multiplication
def make_Q8():
    elems = ['1','-1','i','-i','j','-j','k','-k']
    def mul(a,b):
        sign = 1
        if a.startswith('-'): sign *= -1; a = a[1:]
        if b.startswith('-'): sign *= -1; b = b[1:]
        table = {
            ('1','1'):'1', ('1','i'):'i', ('1','j'):'j', ('1','k'):'k',
            ('i','1'):'i', ('j','1'):'j', ('k','1'):'k',
            ('i','i'):'-1', ('j','j'):'-1', ('k','k'):'-1',
            ('i','j'):'k', ('j','k'):'i', ('k','i'):'j',
            ('j','i'):'-k', ('k','j'):'-i', ('i','k'):'-j'
        }
        out = table[(a,b)]
        if out.startswith('-'):
            sign *= -1
            out = out[1:]
        return ('' if sign==1 else '-') + out
    return FiniteGroup("Q8", elems, mul, '1')

# direct product G x H
def direct_product(G, H):
    elems = [(a,b) for a in G.elements for b in H.elements]
    def op(x,y):
        return (G.op(x[0], y[0]), H.op(x[1], y[1]))
    return FiniteGroup(f"{G.name}x{H.name}", elems, op, (G.e, H.e))
