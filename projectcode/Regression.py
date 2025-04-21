import pandas as pd
import numpy as np
from sklearn.linear_model import RidgeCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import seaborn as sns




merged_df = pd.read_csv("/Users/karlyjae/Documents/25-spring-kiriarte/datasets/mergedf.csv")
#rename columns please

merged_df.rename(columns={'Number_of_Parks': 'Parks #', 'Percent Families in Poverty': 'Poverty %', 'TOTAL Publicly Owned': 'Public (Acres)', 'Total Population': 'Population',
'All races/ ethnicities (aggregated)': 'Activity %', 'Black or African American Non-Hispanic/Latino':'Activity % (Black)', 'White Non-Hispanic/Latino':'Activity %(White)', 'Percent Walked':'Walked %',
'Percent Civilian Population w/ Health Ins. Cov.':'% w/ Health Ins.', 'Median Household Income ($)': 'MHI (Income)', "accessibility_score":"Accessibility score",
"num_trails":"Number of Trails"

}, inplace=True)
target = "Activity %" 

features = [
    "Parks #", "Amount", "MHI (Income)",
    "Poverty %", "Population",
    "Public (Acres)",
    "Walked %", "Unemployment Rate",
    "% w/ Health Ins.",
    "Bachelor's degree", "Accessibility score", "Number of Trails"
]


# Drop rows with missing values
df_clean = merged_df.dropna(subset=features + [target])
X = df_clean[features]
y = df_clean[target]

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Tune Ridge regression
alphas = np.logspace(-3, 3, 50)
ridge_cv = RidgeCV(alphas=alphas, scoring='r2', store_cv_values=True)
ridge_cv.fit(X_scaled, y)

#plots
print(f"Best alpha: {ridge_cv.alpha_}")
print(f"R² score: {ridge_cv.score(X_scaled, y):.4f}")

#Coefficients for presentation 
for feature, coef in zip(X.columns, ridge_cv.coef_):
    print(f"{feature}: {coef:.4f}")



ridge = RidgeCV(alphas=np.logspace(-3, 3, 50), scoring='r2')
ridge.fit(X_scaled, y)

coef_df = pd.DataFrame({
    "Feature": X.columns,
    "Coefficient": ridge.coef_
}).sort_values(by="Coefficient", ascending=False)

top_custom_features = coef_df[~coef_df["Feature"].isin(["Public (Acres)"])]["Feature"].head(2).tolist()

# Always include accessibility_score
if "accessibility_score" not in top_custom_features:
    top_custom_features.append("Accessibility score")

if "num_trails" not in top_custom_features:
    top_custom_features.append("Number of Trails")

# --- Plot each feature ---
for feature in top_custom_features:
    plt.figure(figsize=(6, 4))
    sns.scatterplot(data=df_clean, x=feature, y=target)
    sns.regplot(data=df_clean, x=feature, y=target, scatter=False, color="green")
    plt.title(f"{feature} vs {target}")
    plt.xlabel(feature)
    plt.ylabel("Physical Activity Level (%)")
    plt.tight_layout()
    plt.show()