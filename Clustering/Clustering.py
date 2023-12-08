from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.impute import SimpleImputer
import pandas as pd

# Load data
data = pd.read_csv("Clustering/Chapter06Exercise.csv")
data = data.drop(["First_Name", "Last_Name", "Student_ID", "Gender", "Grade"], axis=1)

# Define preprocessing pipeline
pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="mean")),
    ("kmeans", KMeans(n_init=10, max_iter=300, random_state=42))
])

# Define GridSearchCV
param_grid = {"kmeans__n_clusters": range(1, 8)}
grid_clf = GridSearchCV(pipeline, param_grid, cv=5)
grid_clf.fit(data)

# Find the best number of clusters
# print("Best number of clusters: ", grid_clf.best_params_['kmeans__n_clusters'])

# Fit the model with 3 clusters
pipeline.set_params(kmeans__n_clusters=3)
data["cluster"] = pipeline.fit_predict(data)

# Get centroids of each cluster
centroids = pd.DataFrame(pipeline.named_steps["kmeans"].cluster_centers_, columns=data.columns[:-1])
print("Centroids of Each Cluster (Use 3 Cluster):")
print(centroids)
