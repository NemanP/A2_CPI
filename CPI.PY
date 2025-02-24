import pandas as pd

#part 1
# Read each CSV file add "Jurisdiction" column
df_canada = pd.read_csv("CANADA.CPI.csv")
df_canada["Jurisdiction"] = "Canada"

df_ab = pd.read_csv("AB.CPI.csv")
df_ab["Jurisdiction"] = "Alberta"

df_bc = pd.read_csv("BC.CPI.csv")
df_bc["Jurisdiction"] = "British Columbia"

df_mb = pd.read_csv("MB.CPI.csv")
df_mb["Jurisdiction"] = "Manitoba"

df_nb = pd.read_csv("NB.CPI.csv")
df_nb["Jurisdiction"] = "New Brunswick"

df_nl = pd.read_csv("NL.CPI.csv")
df_nl["Jurisdiction"] = "Newfoundland and Labrador"

df_ns = pd.read_csv("NS.CPI.csv")
df_ns["Jurisdiction"] = "Nova Scotia"

df_on = pd.read_csv("ON.CPI.csv")
df_on["Jurisdiction"] = "Ontario"

df_pei = pd.read_csv("PEI.CPI.csv")
df_pei["Jurisdiction"] = "Prince Edward Island"

df_qc = pd.read_csv("QC.CPI.csv")
df_qc["Jurisdiction"] = "Quebec"

df_sk = pd.read_csv("SK.CPI.csv")
df_sk["Jurisdiction"] = "Saskatchewan"

# Combine all datasets into one DataFrame
final_df = pd.concat([
    df_canada, df_ab, df_bc, df_mb, df_nb, df_nl, 
    df_ns, df_on, df_pei, df_qc, df_sk
])

# Convert from wide to long format to make it look like the example
final_df_long = final_df.melt(id_vars=["Item", "Jurisdiction"], var_name="Month", value_name="CPI")

# Ensure CPI column is numeric
final_df_long["CPI"] = pd.to_numeric(final_df_long["CPI"])

# Print first 12 rows
print("First 12 rows of the transformed CPI data:")
print(final_df_long.head(12))

#part 2
# Compute monthly percentage change
final_df_long["Monthly Change"] = (
    final_df_long.groupby(["Jurisdiction", "Item"])["CPI"].pct_change() * 100
)

# Compute average month-to-month change 
# the line below calculates the average month-to-month change for the items of interest
items_of_interest = ["Food", "Shelter", "All-items excluding food and energy"]
avg_monthly_change = (
    final_df_long[final_df_long["Item"].isin(items_of_interest)]
    .groupby(["Jurisdiction", "Item"])["Monthly Change"]
    .mean()
    .reset_index()
    .round(1)
)

# Print average month-to-month change
print("\nAverage Month-to-Month Change:")
print(avg_monthly_change)

#part 3
# Find the province with the highest average monthly CPI change
highest_change = avg_monthly_change.loc[avg_monthly_change.groupby("Item")["Monthly Change"].idxmax()]

# Print result
print("\nProvince with Highest CPI Change:")
print(highest_change)

# Compute annual CPI change for Services
services_df = final_df_long[final_df_long["Item"] == "Services"]

# Pivot table for annual CPI change
services_annual_change = services_df.pivot(index="Jurisdiction", columns="Month", values="CPI")

services_annual_change["Annual CPI Change (%)"] = (
        (services_annual_change["24-Dec"] - services_annual_change["24-Jan"])
        / services_annual_change["24-Jan"]
    ) * 100

# Reset index to make it a dataframe
#ervices_annual_change = services_annual_change[["Annual CPI Change (%)"]].reset_index()

# Print annual CPI change for services
print("\nAnnual CPI Change for Services:")
print(services_annual_change)

# Find the region with the highest annual service inflation
highest_services_inflation = services_annual_change.loc[services_annual_change["Annual CPI Change (%)"].idxmax()]

print(f"\nRegion with the highest inflation in services: {highest_services_inflation['Jurisdiction']} ({highest_services_inflation['Annual CPI Change (%)']:.1f}%)")


