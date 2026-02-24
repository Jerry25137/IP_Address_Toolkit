"""

IP Address Calculate

Subnetting Calculator veriosn 1.0.1

"""

import copy

from net_calculator import ip_and_mask, net_and_bcast, find_first_and_last_ip, bitlist_offset
from validator import validate_sites
from converter import mask_to_bin
from setting import ctrl_values

# 子網切割 IP / Mask 輸入
def subnetting_ip_and_mask():
    while True:
        ip_format, ip_bin, mask_bin = ip_and_mask(func = "subnetting")
        
        # 設定值
        name_list, mask_ctrl, str_length = ctrl_values(ip_format)
        
        # 取得子網遮罩
        mask      = mask_bin.count(1)
        max_mask  = mask_ctrl[0]
        mask_name = name_list[1]
        
        if mask == max_mask:
            print(f"\n{mask_name} 為 /{max_mask}，主機位為 0，無法借位進行子網切分。")
            continue
        
        elif mask == max_mask - 1:
            print(f"\n注意：切分 /{max_mask - 1} 網段會產生 /{max_mask}，通常僅用於 point-to-point。")
            break
        
        else:
            if ip_format == "IPv6":
                mask = mask_bin.count(1)
                
                if mask >= 65 and mask <= 127:
                    input("\n注意：IPv6 /65～/127 雖然可正常運算，但在實務上不建議用於一般網路介面（建議介面使用 /64）。")
            
            break
    
    return ip_format, ip_bin, mask_bin


# 分割段數
def sites(ip_format, mask_bin):
    # 初始值
    new_mask_bin = None
    
    # 設定值
    name_list, mask_ctrl, str_length = ctrl_values(ip_format)
    
    # 取得子網遮罩
    mask = mask_bin.count(1)
    max_mask = mask_ctrl[0]

    while True:
        # 輸入分割段數
        while True:
            print()
            new_sites = input("請輸入分割段數 = ")
            
            if validate_sites(new_sites):
                new_sites = int(new_sites)
                break
            
            else:
                print("輸入錯誤，請重新輸入分割段數！\n")
        
        # 確認 2**n 次方
        n = 0
        while True:
            if 2 ** n >= new_sites:
                break
            n += 1
        
        # 確認切分後子網遮罩
        if (mask + n) <= max_mask:
            new_mask_bin = mask_to_bin(ip_format, mask + n)
            break
            
        else:
            print("\n輸入錯誤：超出可用範圍，請重新輸入分割段數！")
    
    if new_sites == 1:
        input("\n注意：切分 1 段等同未切分，將直接回傳原始網段。")
    
    return new_sites, new_mask_bin
    
# 取得切分的每一段資訊
def get_subnetting(ip_format, ip_bin, new_mask_bin, new_sites):
    # 初始化
    all_sites = []
    
    # 設定值
    name_list, mask_ctrl, str_length = ctrl_values(ip_format)
    
    # 取得子網遮罩
    new_mask = new_mask_bin.count(1)
    max_mask = mask_ctrl[0]
    n = max_mask - new_mask

    # 儲存計算資料
    for i in range(new_sites):
        if i == 0:
            Bin = ip_bin

        # 網段與廣播
        network_id, broadcast_address = net_and_bcast(ip_format, Bin, new_mask_bin)
        
        # 可用範圍數計算 / 第一 / 最終 IP
        ip_n, first_ip, last_ip = find_first_and_last_ip(ip_format, new_mask_bin, network_id, broadcast_address)
        
        # 儲存結果
        result = [network_id, broadcast_address, ip_n, first_ip, last_ip]
        all_sites.append(result)
        
        Bin = copy.deepcopy(network_id[0])
        Bin = bitlist_offset(Bin, 2**n)
    
    #print(all_sites)
    return all_sites
    