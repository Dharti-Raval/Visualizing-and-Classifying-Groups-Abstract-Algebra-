features = [c for c in df.columns if c.startswith('n_el_order_') or c.startswith('lap_eig_')] + \
           ['order','center_size','n_conjugacy_classes','avg_degree','mean_element_order','is_cyclic']

X = df[features].fillna(0)
y = df['is_abelian']

# If any class has <2 samples, do not stratify
y_counts = y.value_counts()
stratify_flag = True if y_counts.min() >= 2 else False

if stratify_flag:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
else:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

lr = LogisticRegression(max_iter=500)
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)

rf = RandomForestClassifier(n_estimators=300, random_state=42)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)

print("Logistic Regression accuracy:", accuracy_score(y_test, y_pred_lr))
print("Random Forest accuracy:", accuracy_score(y_test, y_pred_rf))
print("\nRandom Forest classification report:\n", classification_report(y_test, y_pred_rf))
print("Confusion matrix:\n", confusion_matrix(y_test, y_pred_rf))
