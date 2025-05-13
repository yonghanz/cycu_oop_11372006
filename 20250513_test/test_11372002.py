from m11372002.ebus_map_hw1 import get_bus_info_go

if __name__ == "__main__":
    # Example bus IDs
    bus1 = '0161000900'  # 承德幹線
    bus2 = '0161001500'  # 基隆幹線

    bus_list = [bus1, bus2]

    for route_id in bus_list:
        try:
            # 呼叫 get_bus_info_go 並傳入 bus_id
            stop_ids = get_bus_info_go(route_id)
            print(f"Stops for bus {route_id}: {stop_ids}")

            # 模擬處理每個車站的資訊
            for stop_id in stop_ids:
                print(f"Processing stop ID: {stop_id}")

        except Exception as e:
            print(f"Error processing route {route_id}: {e}")
            continue