import merasql as sql
import pandas as pd
from datetime import date as dt


def view_data(table):
    flist = []
    for x in sql.desc(table=table):
        flist.append(x[0])
    df = pd.DataFrame(sql.select(table=table))
    if df.empty:
        return "-> Empty table."
    else:
        df.columns = flist
        return df


def insert_data(table):
    info = sql.desc(table=table)
    data = []
    try:
        for x in info:
            dtype = x[1]
            if dtype == "int" or dtype == "bigint":
                val = int(input(f"Enter {x[0]}(numeric): "))
            if dtype == "float(9,2)":
                val = float(input(f"Enter {x[0]}(numeric): "))
            if dtype == "date":
                val = f'{dt.today()}'
            if dtype == "varchar(30)" or dtype == "varchar(50)":
                val = f'{input(f"Enter {x[0]}: ")}'
            data.append(val)

            if x[0] == "Item_id":
                id = val
            if x[0] == "Quantity":
                qty = val
        if table == "Sale":  # yeh sab tamjham isliye taki jo item hai aur jitna hai utna hi sell ho
            df = view_data("Item")
            if type(df) is not str:
                if id in df["Item_id"].values:
                    aqty = df.loc[df["Item_id"] == id, "Quantity"].values
                    if qty <= aqty:
                        sql.insert(table=table, data=tuple(data))
                        sql.update(table="Item", field="Quantity", value=f"Quantity - {qty}", where=f"Item_id = {id}")
                        print("-> Data inserted successfully.")
                    else:
                        print(f"\n-> Entered quantity exceeds available quantity, please enter a valid value.\
                        \nAvailable quantity: {aqty}")
                        insert_data(table)
                else:
                    print("\n-> Specified item could not be found in the store. Please enter a valid value.")
                    insert_data(table)
            else:
                print("\n-> You have no items in the store to sell. Items table is empty.")
        else:
            if table == "Purchase":
                sql.update(table="Item", field="Quantity", value=f"Quantity + {qty}", where=f"Item_id = {id}")
            sql.insert(table=table, data=tuple(data))
            print("-> Data inserted successfully.")

    except ValueError or sql.mc.DataError:
        print("\n-> Please enter a valid value!")
        insert_data(table)
    except sql.mc.IntegrityError:
        print(f"\n-> Please do not enter duplicate value for {info[0][0]}!")
        insert_data(table)


def update_data(table):
    info = sql.desc(table=table)
    print("\nFields of the table are -: ")
    for x in info:
        print(x[0])
    clm = input("Enter field name for which you want to change data: ")
    dtype = ""
    for x in info:
        if x[0] == clm:
            dtype = x[1]
            break
    try:
        if dtype == "":
            print("\n-> Please enter column from given list!")
            update_data(table)
        if dtype == "int":
            val = int(input(f"\nEnter new {clm}(numeric): "))
        if dtype == "float(9,2)":
            val = float(input(f"\nEnter new {clm}(numeric): "))
        if dtype == "date":
            val = f'{input(f"\nEnter new {clm}(as yyyy-mm-dd): ")}'
        if dtype == "str":
            val = f'{input(f"\nEnter new {clm}: ")}'
    except ValueError:
        print("\n-> Please enter a valid value!")
        update_data(table)
    c = input('''\nDo you want to change it for all rows?
1. Yes
2. No
Enter choice: ''')
    if c == "1":
        cod = None
    elif c == "2":
        print("\n-> Please give the condition to be applied (Example condition-> Item_id = 5).")
        cod = input(f"Enter condition: ")
    else:
        print("\n-> Please enter a valid value!")
        update_data(table)
    sql.update(table=table, field=clm, value=val, where=cod)


def delete_data(table):
    info = sql.desc(table=table)
    id = int(input(f"\nEnter {info[0][0]} of the row you want to delete: "))
    c = input('''\n-> Are you sure you want to delete the data?
1. Yes
2. No
Enter choice: ''')
    if c == "1":
        sql.delete(table=table, where=f"{info[0][0]} = {id}")
        print("-> Data deleted successfully.")
    elif c == "2":
        print("\n-> Your data is safe.")
    else:
        print("\n-> Please enter a valid value!")
        delete_data(table)

