def extract_features(group, max_order_feature=10):
    feat = {}
    feat['name'] = group.name
    feat['order'] = group.order
    feat['is_abelian'] = int(group.is_abelian())
    feat['is_cyclic'] = int(group.is_cyclic())
    feat['center_size'] = len(group.center())
    conj = group.conjugacy_classes()
    feat['n_conjugacy_classes'] = len(conj)
    orders_map = group.element_orders()
    counts = Counter(orders_map.values())
    for k in range(1, max_order_feature+1):
        feat[f'n_el_order_{k}'] = counts.get(k, 0)
    normals = group.normal_subgroups()
    feat['num_normal_subgroups'] = len(normals) if normals is not None else -1
    simple = group.is_simple() if hasattr(group, 'is_simple') else None
    feat['is_simple'] = int(simple) if isinstance(simple, bool) else -1
    feat['is_solvable'] = int(group.is_solvable())
    gens = default_generators(group)
    G = group.cayley_graph(gens)
    degs = [d for _,d in G.degree()]
    feat['avg_degree'] = float(np.mean(degs)) if degs else 0.0
    # Laplacian eigenvalues (first 6)
    try:
        L = nx.laplacian_matrix(G).todense()
        eigs = np.linalg.eigvalsh(np.array(L))
        eigs_sorted = sorted(eigs)
        for i in range(6):
            feat[f'lap_eig_{i+1}'] = float(eigs_sorted[i]) if i < len(eigs_sorted) else 0.0
    except:
        for i in range(6):
            feat[f'lap_eig_{i+1}'] = 0.0
    orders_list = list(orders_map.values())
    feat['mean_element_order'] = float(np.mean(orders_list)) if orders_list else 0.0
    feat['median_element_order'] = float(np.median(orders_list)) if orders_list else 0.0
    feat['std_element_order'] = float(np.std(orders_list)) if orders_list else 0.0
    return feat

dataset = [extract_features(g) for g in groups]
df = pd.DataFrame(dataset)
df = df.sort_values('order').reset_index(drop=True)
df.head(20)
