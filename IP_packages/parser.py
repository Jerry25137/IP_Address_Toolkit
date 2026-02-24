"""

IP Address Calculate

Parser veriosn 1.0.0

"""

# 資料正規化 -------------------------------------------------------------------------
# 輸入資料正規化
def input_normalization(ip_address):
    ip_address = normalize_to_halfwidth(ip_address)  # 全形轉半形
    ip_address = ip_address.lower()                  # 大寫轉小寫
    ip_address = ip_address.replace(" ", "")         # 移除空格
    
    return ip_address

def normalize_to_halfwidth(text: str) -> str:
    """將字串中的全形字元轉成半形字元"""
    result = []
    for char in text:
        code = ord(char)
        
        # 全形空白 (U+3000) → 半形空白 (U+0020)
        if code == 0x3000:
            result.append(chr(0x0020))
            
        # 全形英數符號 (U+FF01 ~ U+FF5E) → 減去 0xFEE0
        elif 0xFF01 <= code <= 0xFF5E:
            result.append(chr(code - 0xFEE0))
        else:
            result.append(char)
            
    return "".join(result)

# IPv6 轉換 -------------------------------------------------------------------------
# IPv6
def ipv6_normalization(ip_addr_list):
    new_ip_addr_list = []
    
    # 情境 ::
    if ip_addr_list.count("") == 3 and len(ip_addr_list) == 3:
        # 補 0
        z = 3
        new_ip_addr_list = fill_zero(ip_addr_list, new_ip_addr_list, z)
    
    # 情境 ::xxxx
    elif ip_addr_list.count("") == 2 and ip_addr_list[0] == "" and ip_addr_list[1] == "":
        # 補 0
        z = 2
        new_ip_addr_list = fill_zero(ip_addr_list, new_ip_addr_list, z)
        
        # 補內容
        new_ip_addr_list = fill_value(ip_addr_list, new_ip_addr_list)

    # 情境 xxxx::
    elif ip_addr_list.count("") == 2 and ip_addr_list[-1] == "" and ip_addr_list[-2] == "":
        # 補內容
        new_ip_addr_list = fill_value(ip_addr_list, new_ip_addr_list)
        
        # 補 0
        z = 2
        new_ip_addr_list = fill_zero(ip_addr_list, new_ip_addr_list, z)
    
    # 情境 xxxx::xxxx
    elif ip_addr_list.count("") == 1:
        # 補內容
        new_ip_addr_list = fill_value(ip_addr_list, new_ip_addr_list)
        
        # 補 0
        z = 1
        zero_list = []
        zero_list = fill_zero(ip_addr_list, zero_list, z)
        
        # 組合內容
        x = ip_addr_list.index("")
        n = x * 4
        
        for i in zero_list:
            new_ip_addr_list.insert(n, i)
        
    # 情境 xxxx:xxxx:xxxx
    elif "" not in ip_addr_list and len(ip_addr_list) == 8:
        # 補內容
        new_ip_addr_list = fill_value(ip_addr_list, new_ip_addr_list)

    return new_ip_addr_list

# 補 0
def fill_zero(ip_addr_list, new_ip_addr_list, z):
    n = (8 - (len(ip_addr_list) - z)) * 4
    
    for i in range(n):
        new_ip_addr_list.append(0)
        
    return new_ip_addr_list

# 補內容
def fill_value(ip_addr_list, new_ip_addr_list):
    for i in ip_addr_list:
        if i == "":
            continue
        
        elif len(i) < 4:
            for j in range(4 - len(i)):
                new_ip_addr_list.append(0)
        
        for k in i:
            try:
                new_ip_addr_list.append(int(k))
                
            except Exception:
                new_ip_addr_list.append(k)
            
    return new_ip_addr_list