# sale per day
# sale per customer
# sale per item
# customer preference
import matplotlib.pyplot as plt
import pandas as pd
import merasql as sql


def g1(clm):
    data = sql.select(table="Sale", fields=f"{clm}, sum(Quantity*Rate_of_sale)", groupby=f"{clm}", orderby=f"{clm}")
    ind = []
    val = []
    for x in data:
        ind.append(x[0])
        val.append(int(x[1]))
    ser = pd.Series(val, index=ind)
    ser.plot(kind="bar")
    plt.xlabel(f"{clm}")
    plt.ylabel("Net Sale Amount")
    if clm == "Date":
        plt.title("Sale per Day")
    elif clm == "Item_id":
        plt.title(f"Sale per Item")
    elif clm == "Customer_id":
        plt.title("Sale per Customer")
    plt.show()


def g2():
    df1 = pd.DataFrame(sql.select(table="Sale, Customer", fields="distinct Sale.Customer_id, Customer.Customer_name",
                                  where="Sale.Customer_id = Customer.Customer_id"))
    if df1.empty:
        print("\n->No applicable data found.")
    else:
        df1.columns = ["Customer_id", "Customer_name"]
        print(f"\nCustomers are -: ")
        print(df1)
        cust = input("Enter Customer_id for which you want to view preference: ")
        data = sql.select(table="Item, Sale", fields="Item.Item_name, sum(Sale.Quantity)",
                          where=f"Item.Item_id = Sale.Item_id and Sale.Customer_id = {cust}",
                          groupby="Item.Item_name")
        ind = []
        val = []
        for x in data:
            ind.append(x[0])
            val.append(int(x[1]))
        ser = pd.Series(val, index=ind)
        ser.plot(kind="pie", autopct="%2.1f%%")
        plt.title("Customer Preference")
        plt.show()
