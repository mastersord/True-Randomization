from System import *
import Manager
import Utility
import Item

def init():
    global price_skip_list
    price_skip_list = [
        "Potion",
        "Ether",
        "Alkhahest",
        "Waystone"
    ]

def set_shop_price_weight(weight):
    global shop_price_weight
    shop_price_weight = Utility.weight_exponents[weight - 1]

def randomize_shop_prices(scale):
    Manager.write_file("Spoiler", f"\nItem prices: \n")
    Manager.write_file("Spoiler", f"Item | Buy Price | Sell Price\n")
    for entry in datatable["PB_DT_ItemMaster"]:
        if datatable["PB_DT_ItemMaster"][entry]["buyPrice"] == 0 or entry in price_skip_list:
            Manager.write_file("Spoiler", f"{entry} | {datatable["PB_DT_ItemMaster"][entry]["buyPrice"]} | {datatable["PB_DT_ItemMaster"][entry]["sellPrice"]}\n")
            continue
        #Buy
        buy_price = datatable["PB_DT_ItemMaster"][entry]["buyPrice"]
        sell_ratio = datatable["PB_DT_ItemMaster"][entry]["sellPrice"]/buy_price
        multiplier = Utility.random_weighted(1.0, 0.01, 100.0, 0.01, shop_price_weight, False)
        datatable["PB_DT_ItemMaster"][entry]["buyPrice"] = int(buy_price*multiplier)
        datatable["PB_DT_ItemMaster"][entry]["buyPrice"] = max(datatable["PB_DT_ItemMaster"][entry]["buyPrice"], 1)
        if datatable["PB_DT_ItemMaster"][entry]["buyPrice"] > 10:
            datatable["PB_DT_ItemMaster"][entry]["buyPrice"] = round(datatable["PB_DT_ItemMaster"][entry]["buyPrice"]/10)*10
        #Sell
        if not scale:
            multiplier = Utility.random_weighted(1.0, 0.01, 100.0, 0.01, shop_price_weight, False)
        datatable["PB_DT_ItemMaster"][entry]["sellPrice"] = int(buy_price*multiplier*sell_ratio)
        datatable["PB_DT_ItemMaster"][entry]["sellPrice"] = max(datatable["PB_DT_ItemMaster"][entry]["sellPrice"], 1)
        Manager.write_file("Spoiler", f"{Item.get_real_item_name(entry).ljust(25, ' ')} | {datatable["PB_DT_ItemMaster"][entry]["buyPrice"]} | {datatable["PB_DT_ItemMaster"][entry]["sellPrice"]}\n")