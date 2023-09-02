import pandas as pd


xlsx_path_1 = "ETLprocess/ETLDataSource1.xlsx" 
xlsx_path_2 = "ETLprocess/ETLDataSource2.xlsx"
xls_1 = pd.ExcelFile(xlsx_path_1)
xls_2 = pd.ExcelFile(xlsx_path_2)

sheet_names_1 = xls_1.sheet_names
sheet_names_2 = xls_2.sheet_names

repositary = {}

for sheet_name in sheet_names_1:
    df = pd.read_excel(xls_1, sheet_name)
    repositary[sheet_name] = df

for sheet_name in sheet_names_2:
    df = pd.read_excel(xls_2, sheet_name)
    repositary[sheet_name] = df


product_order_1 = pd.merge(repositary["orderSource1"], repositary["productSource1"], on = "OrderID", how = "inner")
product_order_1["CustomerState"].replace(repositary["StateLookup"].set_index("Abbreviation")["State"], inplace = True)
product_order_1["CustomerFirstName"] = product_order_1["CustomerName"].str.split(" ").str[0]
product_order_1["CustomerLastName"] = product_order_1["CustomerName"].str.split(" ").str[1]
product_order_1.drop("CustomerName", axis = 1, inplace = True)
product_order_1.sort_index(axis = 1, inplace = True)

product_order_2 = pd.merge(repositary["orderSource2"], repositary["productSource2"], on = "OrderID", how = "inner")
product_order_2["OrderID"] = product_order_2["OrderID"].str.strip("A")
product_order_2["OrderID"] = product_order_2["OrderID"].astype(int)
product_order_2["CustomerStatus"] = product_order_2["CustomerStatus"].map({1: "Silver", 2: "Gold", 3: "Platinum"})
product_order_2["TotalDiscount"] = product_order_2["FullPrice"] * product_order_2["Discount"]

product_order = pd.concat([product_order_1, product_order_2])
product_order["CustomerName"] = product_order["CustomerFirstName"] + " " + product_order["CustomerLastName"]
product_order.drop("CustomerFirstName", axis = 1, inplace = True)
product_order.drop("CustomerLastName", axis = 1, inplace = True)
product_order.to_csv("ETLprocess/ETLprocess.csv", index = False)