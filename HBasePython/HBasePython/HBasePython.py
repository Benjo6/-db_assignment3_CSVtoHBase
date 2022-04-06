import happybase
import csv
import time
import logging
logging.basicConfig(level=logging.DEBUG)

batch_size = 1000
host = "localhost"
file_path = "myfoodapediadata\Food_Display_Table.csv"
namespace = "hw"
row_count = 0
start_time = time.time()
table_name = "food"


def connecttohbase():
    conn = happybase.Connection(host = host, autoconnect=False ,port =9095,table_prefix=namespace,table_prefix_separator = ",", timeout=86400, protocol="compact", transport="framed" )
    conn.open()
    table = conn.table(table_name)
    batch = table.batch(batch_size= batch_size)
    return conn,batch

def insertrow(batch, row):
    """ Insert a row into HBase.
    Write the row to the batch. When the batch size is reached, rows will be
    sent to the database.
    Rows have the following schema:
        [ Food_Code, Display_Name, Portion_Default, Portion_Amount, Portion_Display_Name, Factor, Increment,'Multiplier,
          Grains, Whole_Grains, Vegetables, Orange_Vegetables, Drkgreen_Vegetables,Starchy_vegetables, Other_Vegetables, Fruits, Milk, Meats
          Soy,Drybeans_Peas, Oils, Solid_Fats, Added_Sugars, Alcohol, Calories, Saturated_Fats ]
    """
    batch.put(row[0],{"data:Food_Code": row[0], "data:Display_Name": row[1], "data:Portion_Default": row[2],
        "data:Portion_Amount": row[3], "data:Portion_Display_Name": row[4], "data:Factor": row[5],
        "data:Increment": row[6], "data:Multiplier": row[7], "data:Grains": row[8],
        "data:Whole_Grains": row[9], "data:Vegetables": row[10], "data:Orange_Vegetables": row[11], "data:Drkgreen_Vegetables": row[12], "data:Starchy_vegetables": row[13]
        , "data:Other_Vegetables": row[14], "data:Fruits": row[15], "data:Milk": row[16], "data:Meats": row[17], 
       "data:Soy": row[18], "data:Drybeans_Peas": row[19], "data:Oils": row[20], "data:Solid_Fats": row[21], "data:Added_Sugars": row[22], "data:Alcohol": row[23]
       , "data:Calories": row[24], "data:Saturated_Fats": row[25] })
def readcsv():
    csvfile = open(file_path,"r")
    csvreader = csv.reader(csvfile)
    return csvreader,csvfile

conn, batch = connecttohbase()
print ("Connect to HBase. table name: %s, batch size: %i" % (table_name, batch_size))
csvreader, csvfile = readcsv()
print ("Connected to file. name: %s" % (file_path))


try:

    for row in csvreader:
        row_count+=1
        print("Completed row: %s" % (row))
        if row_count==1:
            pass
        else:
            insertrow(batch,row)

    batch.send()

finally:
    csvfile.close()
    conn.close()

duration = time.time() - start_time
print("Done. row count: %i, duration: %.3f s" % (row_count, duration))