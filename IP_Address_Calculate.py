"""

IP Address Calculate

find IPv4 Network ID, Broadcast address

find IPv6 Prefix, Prefix Length

find Available IP, IP Range

"""

import os
import sys

# 讓 Python 找得到套件資料夾
current_dir = os.path.dirname(os.path.abspath(__file__))
package_path = os.path.join(current_dir, "IP_packages")
sys.path.append(package_path)

# 工具套件
from main import network, subnetting, supernetting, eui64, clear_screen

# 主程式 -------------------------------------------------------------------------
if __name__ == "__main__":
    while True:
        # 清除畫面
        clear_screen()
        
        print("=======================================")
        print("        IPv4 / IPv6 工具選單")
        print("=======================================")
        print("1. 計算 網段 (Network Calculator)")
        print("2. 計算 子網切割 (Subnetting)")
        print("3. 計算 超網合併 (Supernetting)")        
        print("4. 計算 EUI-64 位址 (EUI-64 Generator)")
        print("0. 離開程式")
        print("=======================================")
        
        choice = input("\n請輸入選項編號：").strip()

        if choice == "1":
            print("\n[執行] 網段計算中...\n")
            network()
        
        elif choice == "2":
            print("\n[執行] 子網切割計算中...\n")
            subnetting()
        
        elif choice == "3":
            print("\n[執行] 超網合併計算中...\n")
            supernetting()
        
        elif choice == "4":
            print("\n[執行] EUI-64 計算中...\n")
            eui64()
            
        elif choice == "0":
            print("\n程式結束，再見！")
            break
        
        else:
            print("\n輸入錯誤，請重新選擇。\n")

        input("按下 Enter 鍵回主選單...\n")