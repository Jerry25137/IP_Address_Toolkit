"""

IP Address Calculate

Validate veriosn 1.0.1

"""


# 驗正輸入字串長度
def validate_str(ip_address, str_length):
    # 必定要有值
    if ip_address is None or ip_address == "":
        return False
    
    # 依樣式限制字串長度
    if len(ip_address) > str_length:
        return False
    
    return True

# 驗證 IP 或 子網遮罩 數目 / 進位值 是否為合法
def validate_ip(ip_format, ip_address, ip_list):
    # IPv4
    if ip_format == "IPv4":
        if len(ip_list) != 4:  # 驗證格式數量
            return False
        
        for n in ip_list:  # 驗證 10 進位數值
            try:
                if not (0 <= n <= 255):
                    return False
            
            except Exception:
                return False
            
    # IPv6
    elif ip_format == "IPv6":
        # 使用 : 分割，進行驗證 (粗分)
        ipv6_address_list = list(ip_address.split(":"))
        
        if len(ipv6_address_list) > 8:
            if len(ipv6_address_list) == 9 and ipv6_address_list.count("") == 2:
                if ipv6_address_list[0] == "" and ipv6_address_list[1] == "":
                    ""
                
                elif ipv6_address_list[-1] == "" and ipv6_address_list[-2] == "":
                    ""
                
                else:
                    return False   
                
            else:
                return False
        
        for i in ipv6_address_list: # 驗證每段由 4 bits 組成
            if len(i) > 4:
                return False
        
        # 使用 ip_list 驗證 (細分)
        if len(ip_list) != 32:  # 驗證格式數量
            return False
        
        for x in ip_list:  # 驗證 16 進位
            try:
                int(str(x), 16)
            
            except Exception:
                return False
        
        # 使用 ip_address 驗證 (原始字串)
        if ip_address.count("::") > 1:
            return False
        
        elif ip_address.count("::") == 0:
            if len(ipv6_address_list) != 8:
                return False
        
        if ip_address.count(":::") > 0:
            return False
        
    return True

# 驗證 EUI-64 子網遮罩數值
def validate_cidr(subnet_mask, mask_length, func):
    try:
        if int(subnet_mask) >= 0 and int(subnet_mask) <= mask_length:
            # EUI-64
            if func == "eui64" and int(subnet_mask) != 64:
                raise
            
        else:
            raise
        
        # 驗證成功
        return True
    
    except Exception:
        # 驗證失敗
        return False
    
# 驗證 子網遮罩 是否連續為 1
def validate_mask(mask_bin, func):
    o = mask_bin.count(1)
    n = 0
    
    for i in mask_bin:
        if i == 1:
            n += 1
            
        elif i == 0:
            break

    if func == "eui64":
        if o == 64:
            return True
        
        else:
            return False
    
    else:
        if n == o:
            return True
        
        else:
            return False

# 驗證 Offset 值
def validate_offset(ip_bin, offset):
    try:
        if abs(int(offset)) < 2**len(ip_bin):
            return True
        
        else:
            return False
        
    except Exception:
        return False

# 驗證 Mac Address 格式
def validate_mac(mac_address):

    if ":" in mac_address:
        n = ":"
        s = [2, 5, 8, 11, 14]
        max_length = 17
    
    elif "-" in mac_address:
        n = "-"
        s = [2, 5, 8, 11, 14]
        max_length = 17
    
    elif "." in mac_address:
        n = "."
        s = [4, 9]
        max_length = 14
    
    else:
        return False
    
    # 驗證字串長度
    if len(mac_address) > max_length:
        return False
    
    # 驗證分隔符號數量
    if mac_address.count(n) != len(s):
        return False
    
    # 驗證分隔符號位置
    for i in s:
        if mac_address[i] != n:
            return False
    
    # 驗證 16 進位
    X = mac_address.split(n)
    for i in X:
        for j in i:
            try:
                int(str(j), 16)
            
            except Exception:
                return False
    
    return True

# 驗證 正整數
def validate_sites(new_sites):
    return new_sites.isdigit() and new_sites[0] != "0"