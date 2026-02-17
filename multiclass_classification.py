from sklearn.utils.multiclass import unique_labels

# Prepare data for multiclass classification on 'group_type'
ym = df['group_type']
le = LabelEncoder()
ym_encoded = le.fit_transform(ym)

# Split data for multiclass classification
# Removed 'stratify' argument as some classes have only one member
X_train_mc, X_test_mc, ym_train, ym_test = train_test_split(X, ym_encoded, test_size=0.3, random_state=42)

# Train a RandomForestClassifier for multiclass
rf_mc = RandomForestClassifier(n_estimators=300, random_state=42)
rf_mc.fit(X_train_mc, ym_train)
ym_pred = rf_mc.predict(X_test_mc)

# Evaluate multiclass model safely
print("Multiclass accuracy:", accuracy_score(ym_test, ym_pred))

# Identify which classes are actually present in y_test/y_pred
labels_present = unique_labels(ym_test, ym_pred)
label_names_present = [le.classes_[i] for i in labels_present]

# Generate the classification report only for present labels
print(classification_report(ym_test, ym_pred,
                            labels=labels_present,
                            target_names=label_names_present, zero_division=0))