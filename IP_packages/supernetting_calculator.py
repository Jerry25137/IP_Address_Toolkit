"""

IP Address Calculate

Supernetting Calculator veriosn 1.0.1

"""

from net_calculator import ip_and_mask, net_and_bcast, find_first_and_last_ip, bitlist_offset, find_broadcast_address_bin
from converter import mask_to_bin, bin_to_dec, dec_to_hex
from setting import ctrl_values, text_color
from display import show_info_full, show_info_abbr

# 子網切割 IP / Mask 輸入
# ipv4_table = {mask1:[[N1, B1, IP1], [N2, B2, IP2]], 
#               mask2:[[N1, B1, IP1], [N2, B2, IP2]]}
def supernetting_ip_and_mask():
    # 初始化
    ipv4_table = {}
    ipv6_table = {}
    
    while True:
        # IP / Mask 輸入
        ip_format, ip_bin, mask_bin = ip_and_mask(func = "supernetting")
        
        # 取得子網遮罩 CIDR
        mask = mask_bin.count(1)
        
        # 取得網段 / 廣播
        network_id, broadcast_address = net_and_bcast(ip_format, ip_bin, mask_bin)
        
        # 儲存清單
        if ip_format == "IPv4":
            if mask not in ipv4_table:
                ipv4_table[mask] = []
            
            ipv4_table[mask].append([network_id[0], broadcast_address[0], ip_bin])
        
        elif ip_format == "IPv6":
            if mask not in ipv6_table:
                ipv6_table[mask] = []
            
            # 網段
            ipv6_table[mask].append([network_id[0], broadcast_address[0], ip_bin])
        
        # 繼續或跳出
        ans = input("\n繼續輸入下一組？(Enter 繼續 / q 結束)：").strip().lower()
        print(text_color("line", "\n" + "─" * 45 + "\n"))
        
        if ans == "q":
            # 退出輸入後，依網段排序，方便超網合併
            if len(ipv4_table) > 0:
                for mask in ipv4_table:
                    ipv4_table[mask].sort(key = lambda x: x[0])
            
            if len(ipv6_table) > 0:    
                for mask in ipv6_table:
                    ipv6_table[mask].sort(key = lambda x: x[0])
                
            break

    return ipv4_table, ipv6_table

# 超網合併
def get_supernetting(ipv4_table, ipv6_table):
    # 相同網段合併
    def merge_same_network(table):
        # 初始化
        new_table = {}
    
        # 迴圈處理每個子網遮罩對應的資料
        for mask, entries in table.items():
            # 初始化，key 不存在就設定預設值
            new_table.setdefault(mask, [])
    
            # entry 包含三個元素：[Network ID, Broadcast, IP]
            for net_id, broadcast, ip in entries:
                
                # 檢查 new_table[mask] 是否已有相同 Network ID 的 entry
                for existing in new_table[mask]:
                    # 如果已有相同 Network ID
                    if existing[0] == net_id:
                        existing[2].append(ip)
                        break
                    
                else:
                    # for 迴圈沒有 break，新增一個新的網段
                    new_table[mask].append([net_id, broadcast, [ip], mask])
    
        return new_table
    
    
    # 超網合併
    def merge_network(ip_format, table):
        while True:
            # 初始化
            merge_table = {}
            merge_state = False
        
            # 迴圈處理每個子網遮罩對應的資料
            for mask, entries in table.items():

                n = 0
                while (n + 1) < len(entries):
                    n1, b1, ip1, origin_mask1 = entries[n]
                    n2, b2, ip2, origin_mask2 = entries[n + 1]
                    
                    if bitlist_offset(b1, 1) == n2:
                        # 取得新 Mask
                        new_mask = mask - 1
                        new_mask_bin = mask_to_bin(ip_format, new_mask)

                        # 初始化，key 不存在就設定預設值
                        merge_table.setdefault(new_mask, [])
                        
                        new_b1 = find_broadcast_address_bin(n1, new_mask_bin)
                        
                        # 儲存結果
                        merge_table[new_mask].append([n1, new_b1, ip1 + ip2, origin_mask1])
                        
                        # 迴圈狀態
                        merge_state = True
                        
                        # 序號間格
                        n += 2
                    
                    else:
                        # 初始化，key 不存在就設定預設值
                        merge_table.setdefault(mask, [])
                        
                        # 儲存結果
                        merge_table[mask].append([n1, b1, ip1, origin_mask1])

                        # 序號間格
                        n += 1
                        
                # 儲存最後一個結果
                if n < len(entries):
                    # 初始化，key 不存在就設定預設值
                    merge_table.setdefault(mask, [])

                    merge_table[mask].append(entries[n])
            
            if merge_state:
                table = merge_table
            
            else:
                break
                        
        return merge_table
    
    # 轉換成顯示值
    def tranfer_to_show(ip_format, table):
        # 取得控制值
        name_list, mask_ctrl, str_length = ctrl_values(ip_format)
        
        # 迴圈處理每個子網遮罩對應的資料
        for mask, entries in table.items():
            mask_bin = mask_to_bin(ip_format, mask)
            
            for i in range(len(entries)):
                net_id, br, ip, origin_mask = entries[i]
                
                # 取得網段 / 廣播
                network_id, broadcast_address = net_and_bcast(ip_format, net_id, mask_bin)
                
                # 儲存網段 / 廣播值
                entries[i][0] = network_id
                entries[i][1] = broadcast_address
                
                # IP 轉換顯示值
                for j in range(len(ip)):
                    entries[i][2][j] = bin_to_dec(ip_format, ip[j])
                    
                    if ip_format == "IPv4":
                        entries[i][2][j] = show_info_full(ip_format, ip[j])
                        
                    elif ip_format == "IPv6":
                        entries[i][2][j] = dec_to_hex(ip[j])
                        entries[i][2][j] = show_info_abbr(ip[j])
                
                # 可用範圍數計算  / 第一 / 最終 IP
                ip_n, first_ip, last_ip = find_first_and_last_ip(ip_format, mask_bin, network_id, broadcast_address)
                
                # 儲存結果
                entries[i] = [
                              network_id,
                              broadcast_address,
                              entries[i][2],   # ip list
                              origin_mask,
                              ip_n,
                              first_ip,
                              last_ip
                              ]
                
        return table
    
    
    # 網段資料整理            
    ipv4_table = merge_same_network(ipv4_table)
    ipv6_table = merge_same_network(ipv6_table)
    print("網段資料整理 ")
    print(ipv4_table)
    print(ipv6_table)
    
    # 超網合併
    ipv4_supernetting_table = merge_network("IPv4", ipv4_table)
    ipv6_supernetting_table = merge_network("IPv6", ipv6_table)
    print("超網合併")
    print(ipv4_supernetting_table)
    print(ipv6_supernetting_table)
    
    # 顯示值轉換
    ipv4_supernetting_table = tranfer_to_show("IPv4", ipv4_supernetting_table)
    ipv6_supernetting_table = tranfer_to_show("IPv6", ipv6_supernetting_table)
    print("顯示值轉換")
    print(ipv4_supernetting_table)
    print(ipv6_supernetting_table)
    
    return ipv4_supernetting_table, ipv6_supernetting_table
