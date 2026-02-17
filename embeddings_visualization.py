embed_cols = ['order','center_size','n_conjugacy_classes','avg_degree','mean_element_order'] + [f'lap_eig_{i}' for i in range(1,7)]
E = df[embed_cols].fillna(0).values

pca = PCA(n_components=2, random_state=42)
E_pca = pca.fit_transform(E)

tsne = TSNE(n_components=2, random_state=42, perplexity=6, init='pca')
E_tsne = tsne.fit_transform(E)

plt.figure(figsize=(12,5))
plt.subplot(1,2,1)
for i, label in enumerate(df['name']):
    plt.scatter(E_pca[i,0], E_pca[i,1], s=40)
    plt.text(E_pca[i,0]+0.01, E_pca[i,1]+0.01, label, fontsize=8)
plt.title("PCA embedding")

plt.subplot(1,2,2)
for i, label in enumerate(df['name']):
    plt.scatter(E_tsne[i,0], E_tsne[i,1], s=40)
    plt.text(E_tsne[i,0]+0.01, E_tsne[i,1]+0.01, label, fontsize=8)
plt.title("t-SNE embedding")
plt.show()
