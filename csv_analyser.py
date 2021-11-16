import sys
import pandas as pd


def read_csv(filepath):
    # df >> data frame
    return pd.read_csv(filepath)


def read_as_list(filepath):
    df = pd.read_csv(filepath)
    return df.values.tolist()


def analyse(filepath, return_type):
    df = read_csv(filepath)

    df["Date"] = pd.to_datetime(df["Date"])
    df["Date"] = df["Date"].dt.strftime('%d/%m/%Y')

    # Sum of the total sale value per day
    sum_sales_value = df.groupby(["Date"]).sum().reset_index()

    # Total amount of sales per day
    count_sales = df.groupby(["Date"]).count().reset_index()

    # Getting the highest sale of the day
    highest_sales = df.groupby(["Date"]).max().reset_index()

    # Getting the lowest sale of the day
    lowest_sales = df.groupby(["Date"]).min().reset_index()

    # Wrost sale day of the month
    min_value = sum_sales_value.min()["Sum Sales Value"]
    # Getting min_value completly row
    row_min_value = sum_sales_value[sum_sales_value["Sum Sales Value"] == min_value]

    # Better sale day of the month
    max_value = sum_sales_value.max()["Sum Sales Value"]
    # Getting max_value completly row
    row_max_value = sum_sales_value[sum_sales_value["Sum Sales Value"] == max_value]

    # Wrost quantity of the month
    min_qty = count_sales.min()["Sum Sales Value"]
    # Getting min_qty completly row
    row_min_qty = count_sales[count_sales["Sum Sales Value"] == min_qty]

    # Better quantity of the month
    max_qty = count_sales.max()["Sum Sales Value"]
    # Getting max_qty completly row
    row_max_qty = count_sales[count_sales["Sum Sales Value"] == max_qty]

    # Getting average and highest and lowest sale day
    sum_sales_value["Count Sale"] = count_sales["Sum Sales Value"]
    sum_sales_value["Average Sale"] = sum_sales_value["Sum Sales Value"] / sum_sales_value["Count Sale"]
    sum_sales_value["Highest Sale Day"] = highest_sales["Sum Sales Value"]
    sum_sales_value["Lowest Sale Day"] = lowest_sales["Sum Sales Value"]

    # Formating datas
    sum_sales_value["Sum Sales Value"] = sum_sales_value["Sum Sales Value"].map('R$ {:.2f}'.format)
    sum_sales_value["Average Sale"] = sum_sales_value["Average Sale"].map('R$ {:.2f}'.format)
    sum_sales_value["Highest Sale Day"] = sum_sales_value["Highest Sale Day"].map('R$ {:.2f}'.format)
    sum_sales_value["Lowest Sale Day"] = sum_sales_value["Lowest Sale Day"].map('R$ {:.2f}'.format)

    dict_result = {
        'min_value': {
            'data': row_min_value["Date"].values[0],
            'value': f'R$ {row_min_value["Sum Sales Value"].values[0]:.2f}'
        },
        'max_value': {
            'data': row_max_value["Date"].values[0],
            'value': f'R$ {row_max_value["Sum Sales Value"].values[0]:.2f}'
        },
        'min_qty': {
            'data': row_min_qty["Date"].values[0],
            'value': row_min_qty["Sum Sales Value"].values[0]
        },
        'max_qty': {
            'data': row_max_qty["Date"].values[0],
            'value': row_max_qty["Sum Sales Value"].values[0]
        }
    }

    if return_type == 'df':
        return sum_sales_value
    
    elif return_type == 'dict':
        return dict_result