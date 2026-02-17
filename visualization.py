def cayley_table_matrix(group):
    elems = group.elements
    idx = {e:i for i,e in enumerate(elems)}
    n = group.order
    mat = np.zeros((n,n), dtype=int)
    for i,a in enumerate(elems):
        for j,b in enumerate(elems):
            prod = group.op(a,b)
            mat[i,j] = idx[prod]
    return mat, elems

def plot_cayley_table(group, figsize=(6,6)):
    mat, elems = cayley_table_matrix(group)
    plt.figure(figsize=figsize)
    plt.imshow(mat, interpolation='nearest', cmap='viridis')
    ticks = list(range(len(elems)))
    labels = [str(e) for e in elems]
    plt.xticks(ticks, labels, rotation=90, fontsize=8)
    plt.yticks(ticks, labels, fontsize=8)
    plt.title(f"Cayley table: {group.name} (n={group.order})")
    plt.colorbar(label='element index')
    plt.show()

def default_generators(group):
    if group.name.startswith("C") and all(isinstance(x,int) for x in group.elements):
        return [1 % group.order]
    if group.name.startswith("D"):
        orders = group.element_orders()
        max_ord = max(orders.values())
        rot = next(a for a,o in orders.items() if o==max_ord)
        refl = next((a for a,o in orders.items() if o==2 and a!=group.e), None)
        gens = [rot] + ([refl] if refl else [])
        return gens
    if group.name.startswith("S"):
        orders = group.element_orders()
        n = int(group.name[1:])
        cycle = next((a for a,o in orders.items() if o==n), None)
        trans = next((a for a,o in orders.items() if o==2 and a!=group.e), None)
        gens = []
        if cycle: gens.append(cycle)
        if trans: gens.append(trans)
        return gens if gens else [group.elements[1]]
    if group.name == "Q8":
        return ['i','j']
    return [a for a in group.elements if a!=group.e][:2]

def plot_cayley_graph(group, generators=None, figsize=(6,6)):
    if generators is None:
        generators = default_generators(group)
    G = group.cayley_graph(generators)
    plt.figure(figsize=figsize)
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=False, node_size=250)
    for node, (x,y) in pos.items():
        plt.text(x, y, str(node), fontsize=8, ha='center', va='center')
    plt.title(f"Cayley graph: {group.name} — generators: {generators}")
    plt.axis('off')
    plt.show()
