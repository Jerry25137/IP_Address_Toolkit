"""

IP Address Calculate

Converter veriosn 1.0.1

"""

from setting import ctrl_values

# 進位轉換 --------------------------------------------------------------------------------
# 十進位轉二進位
# 將每個十進位整數（IP位元組）轉換為8位的二進位，並平鋪成32位的list
def dec_to_bin(dec_list):
    bin_list = []
    for i in dec_list:
        X = bin(i)[2:]  # 去掉開頭的 '0b'
        
        if len(X) < 8:
            for j in range(8 - len(X)):  # 補足前綴0使其成為8位
                bin_list.append(0)
        
        for k in X:  # 將字元逐一轉成int加進list中
            bin_list.append(int(k))
        
    return bin_list

# 十進位轉十六進位
def dec_to_hex(dec_to_hex_list):
    for i in range(len(dec_to_hex_list)):
        dec_to_hex_list[i] = hex(dec_to_hex_list[i])[2:]
        
    return dec_to_hex_list

# 十六進位轉二進位
def hex_to_bin(hex_list):
    bin_list = []
    for i in hex_list:
        if isinstance(i, int):
            X = bin(i)[2:]
            
        else:
            X = bin(int(i, 16))[2:]  # 去掉開頭的 '0b'

        if len(X) < 4:
            for j in range(4 - len(X)):  # 補足前綴0使其成為4位
                bin_list.append(0)
        
        for k in X:  # 將字元逐一轉成int加進list中
            bin_list.append(int(k))
        
    return bin_list

# 二進位轉十進位
def bin_to_dec(ip_format, bin_list):
    # 設定值
    name_list, mask_ctrl, str_length = ctrl_values(ip_format)
    
    dec_list = []
    n = mask_ctrl[1]
    y = mask_ctrl[2]
    
    x = 0
    for i in range(len(bin_list)):
        x += bin_list[i] * 2**n

        if n > 0:
            n -= 1
            
        else:
            dec_list.append(x)
            n = y
            x = 0
            
    return dec_list

# 子網遮罩值轉二進位 -------------------------------------------------------------------------
def mask_to_bin(ip_format, subnet_mask):
    # 設定值
    name_list, mask_ctrl, str_length = ctrl_values(ip_format)
    
    # 取得遮罩最大值
    max_mask = mask_ctrl[0]
    
    mask_bin = []
    prefix_len = int(subnet_mask)
    
    if prefix_len >= 0 and prefix_len <= max_mask:
        for i in range(max_mask):
            if i < prefix_len:
                mask_bin.append(1)
                
            else:
                mask_bin.append(0)
    
    else:
        raise ValueError(f"CIDR遮罩長度必須在 0 ~ {max_mask} 之間！")
    
    return mask_bin