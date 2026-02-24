"""

IP Address Calculate

Display veriosn 1.0.2

"""

# 導入套件
from converter import bin_to_dec, dec_to_hex
from setting import ctrl_values, text_color

# 顯示資訊
def show_information(ip_format, bin_list):
    # IPv6 專用縮寫
    show_ip_abbreviation = ""      
    
    # 2 進位 -> 10 進位        
    show_ip_list = bin_to_dec(ip_format, bin_list)
    
    # 10 進位 -> 16 進位
    if ip_format == "IPv6":
        show_ip_list = dec_to_hex(show_ip_list)

        # 顯示處理 (縮排)
        show_ip_abbreviation = show_info_abbr(show_ip_list)
    
    # 顯示處理 (完整)
    show_ip_full = show_info_full(ip_format, show_ip_list)
    
    return show_ip_full, show_ip_abbreviation


# 顯示處理 (完整)
def show_info_full(ip_format, ip_list):
    # 設定值
    name_list, mask_ctrl, str_length = ctrl_values(ip_format)
    
    show_ip = ""
    s = mask_ctrl[3]
    
    for i in range(len(ip_list)):
        show_ip += str(ip_list[i])
        
        if ip_format == "IPv4" and s > 0:
            s -= 1
            show_ip += "."
        
        elif ip_format == "IPv6" and (i + 1) % 4 == 0 and s > 0:
            s -= 1
            show_ip += ":"
    
    return show_ip

def show_info_abbr(ip_list, mode = None):
    # 補冒號
    def add_colon(show_ip_list):
        for i in range(7):
            show_ip_list[i] += ":"
        
        if show_ip_list[7] == "":
            show_ip_list[7] += ":"
        
        return show_ip_list
    
    end = 3  # 控制值
    gap = 4  # 固定值
    
    show_ip = ""
    show_ip_list = ["", "", "", "", "", "", "", ""]
    
    # 忽略 0 處理
    n = 0
    for i in range(len(show_ip_list)):
        while n <= end:
            if ip_list[n] == "0" and show_ip_list[i] == "":
                show_ip_list[i] += ""
                
            else:
                show_ip_list[i] += ip_list[n]
            
            n += 1
        
        end += gap

    # 找出 0 的位置
    zero_pos = [i for i, val in enumerate(show_ip_list) if val == ""]
    
    # 分類 0 的位置 (位置, 位置, 位置, 位置, 連續數量, 補 "", 刪除)
    zero_class = [[], [], [], [],  
                  [], []]
    

    if len(zero_pos) > 1:
        # 分類
        n = 0
        for i in range(len(zero_pos) - 1):
            if i == 0:
                zero_class[n].append(zero_pos[i])
            
            if zero_pos[i] + 1 == zero_pos[i + 1]:
                zero_class[n].append(zero_pos[i + 1])
            
            else:
                n += 1
                zero_class[n].append(zero_pos[i + 1])
        
        # 計算連續數
        for i in range(4):
            if len(zero_class[i]) != 0:
                zero_class[4].append(len(zero_class[i]))
        
        # 取得最大連續位置段
        for i, val in enumerate(zero_class[4]):
            if i == 0:
                max_index = i
            
            if zero_class[4][max_index] < val:
                max_index = i

        # 補 0 位置
        for i in range(4):
            if i != max_index:
                for j in zero_class[i]:
                    show_ip_list[j] = "0"
        
        # 補冒號
        show_ip_list = add_colon(show_ip_list)

        # EUI-64 顏色處理
        if mode == "eui64":
            show_ip_list = eui64_color(show_ip_list)
        
        # 刪除位置
        for i in range(1, len(zero_class[max_index])):
            zero_class[5].append(zero_class[max_index][i])
        
        if 7 in zero_class[5] and len(zero_class[5]) == 7:
            zero_class[5].remove(7)

        elif 1 in zero_class[5]:
            zero_class[5].remove(1)
        
        
        zero_class[5].reverse()
        for i in zero_class[5]:
            del show_ip_list[i]
    
    else:
        # 補冒號
        show_ip_list = add_colon(show_ip_list)
        
        # EUI-64 顏色處理
        if mode == "eui64":
            show_ip_list = eui64_color(show_ip_list)

    # 顯示處理
    for i in range(len(show_ip_list)):
        show_ip += show_ip_list[i]

    return show_ip

# EUI-64 顏色替換
def eui64_color(show_ip_list):
    # 處理序列 1 ~ 4
    for i in range(4):
        show_ip_list[i] = text_color("ip_mask", show_ip_list[i])
    
    # 處理序列 5
    show_ip_list[4] = text_color("interface_id", show_ip_list[4])
    
    # 處理序列 6
    x = show_ip_list[5]
    show_ip_list[5] = ""
    
    if len(x) > 3:
        for i in range(len(x) - 3):
            show_ip_list[5] += text_color("interface_id", x[i])
    
    for i in range(len(x) - 3, len(x)):
        show_ip_list[5] += text_color("fffe", x[i])
        
    # 處理序列 7
    x = show_ip_list[6]
    show_ip_list[6] = ""
    
    for i in range(2):
        show_ip_list[6] += text_color("fffe", x[i])  
    
    if len(x) > 3:
        for i in range(len(x) - 3, len(x)):
            show_ip_list[6] += text_color("interface_id", x[i])
    
    # 處理序列 8
    show_ip_list[7] = text_color("interface_id", show_ip_list[7])
    
    return show_ip_list

# 顯示處理 (Mac Address)
def show_mac_address(mac_address_list):
    mac_address = ""
    mac_ctrl = [1, 5]  # 控制值, 分隔數
    
    for i in mac_address_list:
        mac_address += i
        
        if mac_ctrl[0] > 0:
            mac_ctrl[0] -= 1
        
        else:
            mac_ctrl[0] = 1
            mac_ctrl[1] -= 1
            
            if mac_ctrl[1] >= 0:
                mac_address += "-"  # Windows 樣式
            
    return mac_address


# 顯示處理 (Interface ID )
def show_interface_id(interface_id_list):
    interface_id = ""
    mac_ctrl = [3, 3]  # 控制值, 分隔數
    n = 1
    
    for i in range(len(interface_id_list)):
        if i >= 6 and i <= 9:
            key = "fffe"
            
        else:
            key = "interface_id"
            
        interface_id += text_color(key, interface_id_list[i])
        
        if mac_ctrl[0] > 0:
            mac_ctrl[0] -= 1
        
        else:
            mac_ctrl[0] = 3
            mac_ctrl[1] -= 1
            
            if mac_ctrl[1] >= 0:
                if n == 2:
                    key = "fffe"
                
                else:
                    key = "interface_id"
                
                interface_id += text_color(key, ":")
                
                n += 1

    return interface_id

# ---------------------------------------------------------------------------------------------------------------

# IP / 子網
def display_ip_and_mask(ip_format, ip_bin, mask_bin):
    # 設定值
    name_list, mask_ctrl, str_length = ctrl_values(ip_format)
    
    # 取得子網遮罩
    mask = mask_bin.count(1)
    
    # IP / 子網遮罩
    # IPv4
    if ip_format == "IPv4":
        space1 = "      "
        show_ip   = show_info_full(ip_format, bin_to_dec(ip_format, ip_bin))
        show_mask = show_info_full(ip_format, bin_to_dec(ip_format, mask_bin))
        
    # IPv6
    elif ip_format == "IPv6":
        space1 = "        "
        show_ip   = show_info_abbr(dec_to_hex(bin_to_dec(ip_format, ip_bin)))
        show_mask = show_info_abbr(dec_to_hex(bin_to_dec(ip_format, mask_bin)))
    
    print(f"{ip_format} Address {space1}= {text_color("ip_mask", show_ip)}")
    print(f"{name_list[1]} ({name_list[2]})  = {text_color("ip_mask", show_mask)}")
    print(f"{name_list[1]} (CIDR) = {text_color("ip_mask", f"/{mask}")}")


# 網段 / 廣播
def display_net_and_br(ip_format, mask, network_id, broadcast_address, addr = None, f_type = None):
    # 設定值
    name_list, mask_ctrl, str_length = ctrl_values(ip_format)
    
    # 縮排
    if addr:
        space0 = " - "
    
    else:
        space0 = ""
    
    # 網段 / 廣播
    if ip_format == "IPv4":
        if f_type is None:
            space1 = "        "
            space2 = " "
            
        elif f_type == "subnetting" or f_type == "supernetting":
            space1 = "       "
            space2 = ""

        print(f"{space0}{name_list[0]} {space1}= {text_color("network", f"{network_id[1]}/{mask}")}")
        print(f"{space0}Broadcast Address {space2}= {text_color("broadcast", f"{broadcast_address[1]}/{mask}")}")
        
    elif ip_format == "IPv6":
        if f_type is None:
            space1 = "              "
        
        elif f_type == "subnetting" or f_type == "supernetting":
            space1 = "           "
        
        print(f"{space0}{name_list[0]} {space1}= {text_color("network", f"{network_id[2]}/{mask}")}")

# 可用數量 / 可用範圍
def display_ip_range(ip_format, mask, ip_n, first_ip, last_ip, addr = None, f_type = None):
    # 設定值
    name_list, mask_ctrl, str_length = ctrl_values(ip_format)
    
    # 縮排
    if addr:
        space0 = " - "
    
    else:
        space0 = ""
    
    # 空格排版
    if ip_format == "IPv4":
        if f_type is None:
            space1 = "    "
            space2 = " "
        
        elif f_type == "subnetting" or f_type == "supernetting":
            space1 = "   "
            space2 = ""
    
    elif ip_format == "IPv6":
        if f_type is None:
            space1 = "      "
            space2 = "   "
    
        elif f_type == "subnetting" or f_type == "supernetting":
            space1 = "   "
            space2 = ""
    
    # 可用數量 / 可用範圍
    if mask == mask_ctrl[0]:
        ip_range = f"{text_color("usable", first_ip)} (Single {ip_format} address.)"
        
    elif mask == mask_ctrl[0] - 1:
        ip_range = f"{text_color("usable", first_ip)} ~ {text_color("usable", last_ip)} (Point-to-point {ip_format} network.)"
    
    else:
        ip_range = f"{text_color("usable", first_ip)} ~ {text_color("usable", last_ip)}"
    
    print(f"{space0}Available Host {space1}= {text_color("usable", ip_n)} addresses")
    print(f"{space0}Usable Host Range {space2}= {ip_range}")

# ---------------------------------------------------------------------------------------------------------------

# Network 顯示結果
def show_network_result(ip_format, ip_bin, mask_bin, network_id, broadcast_address, ip_n, first_ip, last_ip):
    # 設定值
    name_list, mask_ctrl, str_length = ctrl_values(ip_format)
    
    # 取得子網遮罩
    mask = mask_bin.count(1)
    
    # 標題
    print(f"{text_color("title", "- Network Calculator Result -")}")
    print(text_color("line", "─" * 52 + "\n"))

    # IP / 子網遮罩
    display_ip_and_mask(ip_format, ip_bin, mask_bin)
    print()
    
    # 網段與廣播
    display_net_and_br(ip_format, mask, network_id, broadcast_address)
    print()
    
    # 可用數量 / 可用範圍
    display_ip_range(ip_format, mask, ip_n, first_ip, last_ip)
    
    # 顯示分隔線
    print(text_color("line", "\n" + "─" * 52 + "\n"))

# Subnetting 顯示結果
def show_subnetting_result(ip_format, ip_bin, mask_bin, new_sites, new_mask_bin, all_sites):
    # 設定值
    name_list, mask_ctrl, str_length = ctrl_values(ip_format)
    
    # 標題
    print(f"{text_color("title", "- Subnetting Result -")}")
    print(text_color("line", "─" * 45 + "\n"))
    
    # IP / 子網遮罩
    display_ip_and_mask(ip_format, ip_bin, mask_bin)
    
    # 取得新子網遮罩
    new_mask = new_mask_bin.count(1)  # 切分
    
    # 顯示分割段數
    print(f"\n>>>　New Sites = {text_color("usable", new_sites)}")
    print(text_color("line", "\n" + "─" * 45 + "\n"))
    
    # 顯示網段 / 廣播
    for i in range(len(all_sites)):
        # 取得資料
        network_id        = all_sites[i][0]
        broadcast_address = all_sites[i][1]
        ip_n              = all_sites[i][2]
        first_ip          = all_sites[i][3]
        last_ip           = all_sites[i][4]
        
        # 顯示段落
        print(f"{text_color("section", f" * No.{i + 1} *")}")
        
        # 網段與廣播
        display_net_and_br(ip_format, new_mask, network_id, broadcast_address, addr = True, f_type = "subnetting")
        print()
        
        # 可用數量 / 可用範圍
        display_ip_range(ip_format, new_mask, ip_n, first_ip, last_ip, addr = True, f_type = "subnetting")
        
        # 顯示分隔線
        print(text_color("line", "\n" + "─" * 45 + "\n"))


# Supernetting 顯示結果
def show_supernetting_result(ipv4_supernetting_table, ipv6_supernetting_table):
    
    def show_table(ip_format, table):
        # 設定值
        name_list, mask_ctrl, str_length = ctrl_values(ip_format)
        
        # 標題
        print(f"{text_color("title", f"- Supernetting Result ({ip_format}) -")}")
        print(text_color("line", "─" * 45 + "\n"))
        
        for mask, entries in table.items():
            for i in range(len(entries)):
                network_id, broadcast_address, ips, origin_mask, ip_n, first_ip, last_ip = entries[i]

                print(f"{text_color("section", " Original inputs:")}")
                
                # 列出輸入的 IP
                for i in range(len(ips)):
                    print(f" - {text_color("ip_mask", f"{ips[i]}/{origin_mask}")}")
                print()
                
                # 網段與廣播
                if len(ips) == 1:
                  print(f"{text_color("section", " Unmerged Network:")}")
                
                else:
                    print(f"{text_color("section", " Merged Network:")}")
                
                display_net_and_br(ip_format, mask, network_id, broadcast_address, addr = True, f_type = "supernetting")
                
                # 可用數量 / 可用範圍
                display_ip_range(ip_format, mask, ip_n, first_ip, last_ip, addr = True, f_type = "supernetting")
                
                # 顯示分隔線
                print(text_color("line", "\n" + "─" * 45 + "\n"))
    
    if len(ipv4_supernetting_table) > 0:
        show_table("IPv4", ipv4_supernetting_table)
    
    if len(ipv6_supernetting_table) > 0:
        show_table("IPv6", ipv6_supernetting_table)


# EUI-64 顯示結果
def show_eui64_result(ip_bin, mac_address_list, interface_id_list, full_ipv6_list):
    # 覆蓋 64 bit 之後的內容
    for i in range(64, len(ip_bin)):
        ip_bin[i] = 0
    
    # 轉換顯示內容
    prefix       = show_info_abbr(dec_to_hex(bin_to_dec("IPv6", ip_bin)))
    mac_address  = show_mac_address(mac_address_list)
    
    # 顏色轉換 interface_id 
    interface_id = show_interface_id(interface_id_list)
    
    # 顏色轉換 full_ipv6
    full_ipv6 = show_info_abbr(full_ipv6_list, mode = "eui64")
    
    # 顯示標題
    print(f"{text_color("title", "- EUI-64 Conversion Result -")}")
    print(text_color("line", "─" * 45 + "\n"))
    
    # 顯示前綴
    print(f"Prefix       = {text_color("ip_mask", prefix)}")
    
    # 顯示 Mac Address
    print(f"MAC Address  = {text_color("mac", mac_address)}")
    
    # 顯示 Interface ID
    print(f"Interface ID = {interface_id}")
    
    # 顯示完整 IPv6 地址
    print(f"IPv6 Address = {full_ipv6}")
    
    # 顯示分隔線
    print(text_color("line", "\n" + "─" * 45 + "\n"))
