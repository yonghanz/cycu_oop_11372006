# homework 1 
def get_bus_info_go(bus_id):
    """
    根據 bus_id 回傳該路線的所有車站 id (去程)
    """
    # 在這裡實作邏輯，根據 bus_id 查詢車站資訊
    # 假設回傳一個範例清單
    
    stop_ids = ["Stop1", "Stop2", "Stop3"]
    return stop_ids


if __name__ == "__main__":
    stop = get_bus_info_go("m11372006")
    print(f"Stops for bus m11372006: {stop}")