"""

EUI-64 Calculate

Calculator veriosn 1.0.1

"""
import copy
from parser import input_normalization
from validator import validate_str, validate_mac
from converter import bin_to_dec, dec_to_hex, hex_to_bin

# Mac Address -------------------------------------------------------------------------
def mac_address_process():
    while True:
        try:
            mac_address = input("Mac Address = ")
            mac_address = input_normalization(mac_address)
            
            if not validate_str(mac_address, 17):
                raise
            
            if not validate_mac(mac_address):
                raise
            
            # 建立 分割 Mac Address 清單
            mac_address_list = []
            
            if ":" in mac_address:
                n = ":"
            
            elif "-" in mac_address:
                n = "-"
            
            elif "." in mac_address:
                n = "."
            
            # 分割 Mac Address
            X = mac_address.split(n)
            
            for i in X:
                for j in i:
                    mac_address_list.append(j)
            
            break
            
        except Exception:
            print("\nMac Address 解析錯誤，請重新輸入...\n")

    return mac_address_list

# Interface ID -------------------------------------------------------------------------
def interface_id_process(mac_address_list):
    interface_id_list = copy.copy(mac_address_list)
    
    # 反轉第 7 位
    inverting_7th = hex_to_bin([interface_id_list[1]])
    
    if inverting_7th[2] == 1:
        inverting_7th[2] = 0
    
    elif inverting_7th[2] == 0:
        inverting_7th[2] = 1
    
    # 二進位轉十六進位
    inverting_7th = dec_to_hex(bin_to_dec("IPv6", inverting_7th)) # [128, 3, 3, 0]
    
    # 覆蓋 Mac Address
    interface_id_list[1] = inverting_7th[0]
    
    interface_id_list = interface_id_list[:6] + ["f", "f", "f", "e"] + interface_id_list[6:]

    return interface_id_list

# 組合結果 -------------------------------------------------------------------------
def combine_prefix_mac(ip_bin, interface_id_list):
    # Prefix 去除後 64 bit
    eui64_full_ipv6 = dec_to_hex(bin_to_dec("IPv6", ip_bin[:64])) # [128, 3, 3, 3]
    
    # 組合成 EUI-64
    eui64_full_ipv6 += interface_id_list

    return eui64_full_ipv6