# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 11:37:22 2025

@author: USER
"""

# 控制值
def ctrl_values(ip_format):
    # 判斷 IPv4 or IPv6
    if ip_format == "IPv4":
        name_list = ["Network ID", "Subnet Mask", "Dec"]  # 網路名稱, 子網遮罩, 二進位
        mask_ctrl = [32, 7, 7, 3]                         # 子網長度, 控制值, 固定值, 分號數
        str_length = 15
        
    elif ip_format == "IPv6":
        name_list = ["Prefix", "Prefix Length", "Hex"]  # 網路名稱, 前綴長度, 十六進位
        mask_ctrl = [128, 3, 3, 7]                      # 子網長度, 控制值, 固定值, 分號數
        str_length = 39
    
    return name_list, mask_ctrl, str_length

# 顏色設定
COLOR = {
         "title":        "\033[1;36m{}\033[0m",      # Cyan Bold      → 大標題
         "section":      "\033[1;33m{}\033[0m",      # Yellow Bold    → 小節標題

         "ip_mask":      "\033[32m{}\033[0m",        # Green          → IP、Mask
         "network":      "\033[35m{}\033[0m",        # Magenta        → 網段 Network
         "broadcast":    "\033[95m{}\033[0m",        # Light Magenta  → 廣播 Broadcast
         "usable":       "\033[1;34m{}\033[0m",      # Bright Blue    → 可用主機數/範圍
         
         "interface_id": "\033[96m{}\033[0m",        # Bright Cyan    → Interface ID (IPv6)
         "mac":          "\033[38;5;208m{}\033[0m",  # Orange         → MAC Address
         "fffe":         "\033[91m{}\033[0m",        # Red            → FFFE

         "label":        "\033[37m{}\033[0m",        # White          → 欄位名
         "line":         "\033[90m{}\033[0m",        # Gray           → 分隔線
         }

# 文字顏色設定
def text_color(key, text):
    return COLOR[key].format(text)