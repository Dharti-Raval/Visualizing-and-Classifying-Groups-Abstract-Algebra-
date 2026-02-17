imp = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False)
imp.head(15)
