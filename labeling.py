def label_group_type(name):
    if name.startswith('C') and 'x' not in name:
        return 'cyclic'
    if name.startswith('D'):
        return 'dihedral'
    if name.startswith('S'):
        return 'symmetric'
    if name == 'Q8':
        return 'quaternion'
    if 'x' in name:
        return 'direct_product'
    return 'other'

df['group_type'] = df['name'].apply(label_group_type)
df['group_type'].value_counts()
