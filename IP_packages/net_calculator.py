"""

IP Address Calculate

Calculator veriosn 1.0.4

"""

from parser import input_normalization, ipv6_normalization
from validator import validate_str, validate_ip, validate_mask, validate_cidr, validate_offset
from converter import dec_to_bin, hex_to_bin, bin_to_dec, mask_to_bin
from setting import ctrl_values
from display import show_information, show_info_full

# IP Address & Subnet mask -----------------------------------------------------------
def ip_and_mask(func = "network"):
    while True:
        # IP 輸入
        ip_format, ip_bin, subnet_mask, ip_val = ip_address_process(func)
        
        if ip_val:
            # 子網遮罩
            mask_bin, mask_val = subnet_mask_process(ip_format, ip_bin, subnet_mask, func)
            
            if mask_val:
                break
        
        print("\n請重新輸入...\n")

    return ip_format, ip_bin, mask_bin

# IP Address -------------------------------------------------------------------------
def ip_address_process(func):
    # IP 輸入顯示        
    if func == "eui64":
        ip_show = "IPv6"
    
    else:
        ip_show = "IP"
    
    # 初始值
    ip_format   = None
    ip_bin      = None
    subnet_mask = None
    validate    = False
    
    try:
        ip_address = input(f"{ip_show} Address = ")  # 例："192.168.1.70"
        ip_address = input_normalization(ip_address)
        
        # 判斷 IPv4 or IPv6
        if "." in ip_address and ":" not in ip_address:
            ip_format = "IPv4"
            str_length = 30
            
            # EUI-64 處理 (不支援 IPv4)
            if func == "eui64":
                raise
            
        elif "." not in ip_address and ":" in ip_address:
            ip_format = "IPv6"
            str_length = 79
        
        elif "." in ip_address and ":" in ip_address:
            ip_format = "IPv4-mapped IPv6"
        
        else:
            raise
        
        # 驗正輸入字串長度
        if not validate_str(ip_address, str_length):
            #print("字串長度不合法")
            raise

        # 判斷 CIDR 格式，例如 "192.168.1.70/26"
        if "/" in ip_address:
            X = ip_address.split("/")
            ip_address  = X[0]
            subnet_mask = X[1]
            
        # IP 轉換 --------------------------------------------------------------------------------
        # IPv4
        if ip_format == "IPv4":
            ip_address_list = list(map(int, ip_address.split(".")))  # 拆成 list: [192,168,1,70]
        
        # IPv6
        elif ip_format == "IPv6":
            ip_address_list = ipv6_normalization(list(ip_address.split(":"))) 

        # IP 格式檢查
        if not validate_ip(ip_format, ip_address, ip_address_list):
            raise
        
        # IPv4 to bin
        if ip_format == "IPv4":
            ip_bin = dec_to_bin(ip_address_list) # IP 轉為二進位 32 位元格式
        
        # IPv6 to bin
        elif ip_format == "IPv6":
            ip_bin = hex_to_bin(ip_address_list) # IP 轉為二進位 128 位元格式
        
        # 驗證成功
        validate = True    
        
    except Exception:
        print("\nIP 解析錯誤！\n")
    
    if ip_bin is None:
        validate = False    
    
    return ip_format, ip_bin, subnet_mask, validate

# Subnet Mask -------------------------------------------------------------------------
def subnet_mask_process(ip_format, ip_bin, subnet_mask, func):
    # 初始值
    mask_bin = None
    validate = False
    
    # 取得控制值
    name_list, mask_ctrl, str_length = ctrl_values(ip_format)
    
    # 子網遮罩轉換 ----------------------------------------------------------------------------   
    try:
        # 手動輸入 Subnet mask
        if subnet_mask is None:
            subnet_mask = input(f"{name_list[1]} ({name_list[2]}) = ")  # 例："255.255.255.192"
        
        # 正規化
        subnet_mask = input_normalization(subnet_mask)
        
        # 驗正輸入字串長度 (避免過長)
        if not validate_str(subnet_mask, str_length):
            raise
        
        # CIDR 判斷
        if len(subnet_mask) <= 4:
            if "/" in subnet_mask:
                X = subnet_mask.split("/")
                subnet_mask = X[-1]
            
            if not validate_cidr(subnet_mask, mask_ctrl[0], func):
                raise
            
            mask_bin = mask_to_bin(ip_format, subnet_mask)
        
        # 標準格式
        else:
            # IPv4
            if ip_format == "IPv4" and "." in subnet_mask:
                subnet_mask_list = list(map(int, subnet_mask.split(".")))
                
                # EUI-64 處理 (不支援 IPv4)
                if func == "eui64":
                    raise
            
            # IPv6
            elif ip_format == "IPv6" and ":" in subnet_mask:
                subnet_mask_list = ipv6_normalization(list(subnet_mask.split(":")))
                    
            # 不相符
            else:
                raise
            
            # Subnet mask 格式檢查
            if not validate_ip(ip_format, subnet_mask, subnet_mask_list):
                raise
            
            # IPv4 mask to bin
            if ip_format == "IPv4":
                mask_bin = dec_to_bin(subnet_mask_list) # Subnet Mask 轉為二進位 32 位元格式
            
            # IPv6 mask to bin
            elif ip_format == "IPv6":
                mask_bin = hex_to_bin(subnet_mask_list) # Prefix Length 轉為二進位 128 位元格式

            # Subnet mask 驗證排序
            if not validate_mask(mask_bin, func):
                raise
        
        # 二進位 -> CIDR
        #mask = mask_bin.count(1)
        
        # 驗證成功
        validate = True
         
    except Exception:
        print(f"\n{name_list[1]} 解析錯誤！\n")
    
    if mask_bin is None:
        validate = False
    
    return mask_bin, validate

# Network ID & Broadcast Address -------------------------------------------------------------------------
# 找 Network ID、Broadcast Address
def net_and_bcast(ip_format, ip_bin, mask_bin):
    # 計算 Network ID
    network_id_bin = find_network_id_bin(ip_bin, mask_bin)
    show_network_id_full, show_network_id_addr = show_information(ip_format, network_id_bin)
    network_id = [network_id_bin, show_network_id_full, show_network_id_addr]
    
    # 計算 IPv4 Broadcast Address / IPv6 Last IP
    broadcast_addr_bin = find_broadcast_address_bin(network_id_bin, mask_bin)
    show_broadcast_addr_full, show_broadcast_addr = show_information(ip_format, broadcast_addr_bin)
    broadcast_address = [broadcast_addr_bin, show_broadcast_addr_full, show_broadcast_addr]
    
    return network_id, broadcast_address

# 找 Network ID
# 將 IP 和 subnet mask 做 bitwise AND，並組合回四個十進位數字
def find_network_id_bin(ip_bin, mask_bin):
    network_id_bin = []  # 網段二進位
    
    # 合併成 Network ID
    for i in range(len(ip_bin)):
        network_id_bin.append(ip_bin[i] * mask_bin[i])
     
    return network_id_bin

# 找 Broadcast Address
# 將 Network ID 的 host bits 全部補 1，得到廣播位址
def find_broadcast_address_bin(network_id_bin, mask_bin):
    broadcast_addr_bin = []       # 廣播位址二進位
    ip_range = mask_bin.count(1)  # 網路位元數
    
    # 廣播二進位生成
    for i in range(len(network_id_bin)):
        if i < ip_range:
            broadcast_addr_bin.append(network_id_bin[i])  # 網路部分保留
        else:    
            broadcast_addr_bin.append(1)  # 主機部分補 1
    
    return broadcast_addr_bin


# IP 位移運算 -------------------------------------------------------------------------
# IP 加減位移
def bitlist_offset(ip_bin, offset):
    try:
        if not validate_offset(ip_bin, offset):
            raise Exception("位移值超出範圍！")
            
        # str to int
        offset = int(offset)
        
        # 無位移
        if offset == 0:
            return ip_bin
        
        # 將偏移值轉換成二進位
        offset_bin = [int(i) for i in list(bin(abs(offset))[2:])]
    
        # 初始化
        n = len(ip_bin) - 1
        mode = False
        
        for i in range(len(offset_bin) - 1, -1, -1):
            # 二進位相加
            if offset > 0:
                bin_value = ip_bin[n] + offset_bin[i]
            
            # 二進位相減
            elif offset < 0:
                bin_value = ip_bin[n] - offset_bin[i]

            # 判斷處理
            if bin_value == 0:
                ip_bin[n] = 0
    
            elif bin_value == 1:
                ip_bin[n] = 1
    
            elif bin_value == 2:
                ip_bin[n] = 0
                mode = True
            
            elif bin_value == -1:
                ip_bin[n] = 1
                mode = True
            
            # 進位 / 借位處理
            if mode:
                x = n - 1
                while True:
                    if x >= 0:
                        if offset > 0:
                            # 加法進位
                            if ip_bin[x] == 0:
                                ip_bin[x] = 1
                                break
                            
                            else:
                                ip_bin[x] = 0
                                x -= 1
                        
                        else:
                            # 減法借位
                            if ip_bin[x] == 1:
                                ip_bin[x] = 0
                                break
                            
                            else:
                                ip_bin[x] = 1
                                x -= 1
                                
                    else:
                        raise Exception("溢位或借位超出範圍！")
                        
                mode = False
             
            n -= 1
        
        return ip_bin
    
    except Exception as e:
        print(f"[錯誤] {e}")

# 第一 / 最終 IP / 可用範圍數計算 ----------------------------------------------------------------------------
# 計算可用 IP 數量 / usable IP 範圍
def find_first_and_last_ip(ip_format, mask_bin, network_id, broadcast_address):
    # 取得控制值
    name_list, mask_ctrl, str_length = ctrl_values(ip_format)
    
    # 取得子網遮罩
    mask = mask_bin.count(1)
    
    if ip_format == "IPv4":
        # 第 1 個可用 IP
        first_ip = network_id[1]
        
        # 最後 1 個可用IP
        last_ip  = broadcast_address[1]
        
        # 可用 IP 數量
        if mask == mask_ctrl[0]:
            ip_n = 1
            
        elif mask == mask_ctrl[0] - 1:
            ip_n = 2
            
        else:
            ip_n = 2**(mask_ctrl[0] - mask) - 2
        
            # 第 1 個可用 IP
            first_ip = show_info_full(ip_format, bin_to_dec(ip_format, bitlist_offset(network_id[0], 1)))
            
            # 最後 1 個可用IP
            last_ip = show_info_full(ip_format, bin_to_dec(ip_format, bitlist_offset(broadcast_address[0], -1))) 
    
    elif ip_format == "IPv6":
        # 可用 IP 數量
        ip_n = 2**(mask_ctrl[0] - mask)
        
        if ip_n < 10**6:
            ip_n
            
        elif ip_n < 10**12:
            ip_n = f"{ip_n:,}"
            
        else:
            ip_n = f"{ip_n:.2e}"
        
        # 第 1 個可用 IP
        first_ip = network_id[2]
        
        # 最後 1 個可用IP
        last_ip = broadcast_address[2]
    
    return ip_n, first_ip, last_ip