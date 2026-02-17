groups = []

# cyclic groups
for n in range(1,11):            # C1 .. C10
    groups.append(make_Cn(n))

# dihedral groups D3..D8
for n in range(3,9):
    groups.append(make_Dn(n))

# symmetric S2, S3, S4
for n in [2,3,4]:
    groups.append(make_Sn(n))

# quaternion
groups.append(make_Q8())

# direct products: C2xC2 (Klein 4), C2xC3, C3xC3, C2xC4
groups.append(direct_product(make_Cn(2), make_Cn(2)))
groups.append(direct_product(make_Cn(2), make_Cn(3)))
groups.append(direct_product(make_Cn(3), make_Cn(3)))
groups.append(direct_product(make_Cn(2), make_Cn(4)))

# Deduplicate by name
byname = {g.name: g for g in groups}
groups = [byname[name] for name in sorted(byname.keys(), key=lambda s: (len(s), s))]

len(groups)
