"""

IP Address Calculate

Veriosn 1.0.2

"""

import os
import sys

# 讓 Python 找得到套件資料夾
current_dir = os.path.dirname(os.path.abspath(__file__))
package_path = os.path.join(current_dir, "network_packages")
sys.path.append(package_path)

from net_calculator import ip_and_mask, net_and_bcast, find_first_and_last_ip
from subnetting_calculator import subnetting_ip_and_mask, sites, get_subnetting
from supernetting_calculator import supernetting_ip_and_mask, get_supernetting
from eui64_calculator import mac_address_process, interface_id_process, combine_prefix_mac

from display import show_network_result, show_subnetting_result, show_supernetting_result, show_eui64_result

# 網段計算
def network():
    try:
        # IP & Mask 輸入
        ip_format, ip_bin, mask_bin = ip_and_mask()
    
        # 網段與廣播
        network_id, broadcast_address = net_and_bcast(ip_format, ip_bin, mask_bin)

        # 可用範圍數計算 / 第一 / 最終 IP
        ip_n, first_ip, last_ip = find_first_and_last_ip(ip_format, mask_bin, network_id, broadcast_address)

        # 清除畫面
        clear_screen()
        
        # 顯示結果
        show_network_result(ip_format, ip_bin, mask_bin, network_id, broadcast_address, ip_n, first_ip, last_ip)

    except Exception:
        return

#network()

# 子網切割
def subnetting():
    try:
        # IP & Mask 輸入
        ip_format, ip_bin, mask_bin = subnetting_ip_and_mask()
            
        # 切分段數 輸入
        new_sites, new_mask_bin = sites(ip_format, mask_bin)
        
        # 子網切割
        all_sites = get_subnetting(ip_format, ip_bin, new_mask_bin, new_sites)

        # 清除畫面
        clear_screen()
        
        # 顯示結果
        show_subnetting_result(ip_format, ip_bin, mask_bin, new_sites, new_mask_bin, all_sites)
        
    except Exception:
        return

#subnetting()

# 超網合併
def supernetting():
    try:
        # IP & Mask 輸入 (多組)
        ipv4_table, ipv6_table = supernetting_ip_and_mask()
        
        # 執行超網合併
        ipv4_supernetting_table, ipv6_supernetting_table = get_supernetting(ipv4_table, ipv6_table)
        
        # 清除畫面
        clear_screen()

        # 顯示結果
        show_supernetting_result(ipv4_supernetting_table, ipv6_supernetting_table)
    
    except Exception:
        return

#supernetting()

# EUI-64
def eui64():
    try:
        # IP & Mask 輸入
        ip_format, ip_bin, mask_bin = ip_and_mask(func = "eui64")
        
        # Mac Address 輸入
        mac_address_list = mac_address_process()

        # 7th 倒置 Mac Address
        interface_id_list = interface_id_process(mac_address_list)

        # Prefix + Mac Address 合併 EUI-64
        full_ipv6_list = combine_prefix_mac(ip_bin, interface_id_list)

        # 清除畫面
        clear_screen()

        # 顯示結果
        show_eui64_result(ip_bin, mac_address_list, interface_id_list, full_ipv6_list)
                
        
    except Exception:
        return

#eui64()




# 清除畫面
def clear_screen():
    # Works on both Windows and Unix-like systems
    os.system('cls' if os.name == 'nt' else 'clear')


