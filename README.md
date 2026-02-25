# IP Address Toolkit

這是一個獨立的 Python 工具專案，提供 IPv4 與 IPv6 網路地址處理與分析功能。
專注於網段計算、子網切分、超網合併以及 EUI-64 生成。

## 主要功能

### 1. 網段計算 (Network Calculator)
- 計算指定 IP 與子網遮罩對應的網段 (Network ID) 與廣播地址 (Broadcast)
- 支援 IPv4 與 IPv6
- 可取得可用 IP 範圍及主機數量
- 自動處理 IPv6 縮寫與補零

### 2. 子網切分 (Subnetting)
- 根據指定網段切分多段子網
- 自動計算每個子網的網段、廣播、可用 IP 範圍
- 支援 IPv4 與 IPv6
- 檢查借位限制與可用子網範圍
- 可針對實務建議提示不建議的 IPv6 子網長度

### 3. 超網合併 (Supernetting)
- 合併多組網段，生成最小的網段集合
- 自動排序並合併相鄰網段
- 支援 IPv4 與 IPv6
- 轉換成可讀顯示格式，包含網段、廣播、可用範圍與原始 IP

### 4. EUI-64 生成 (EUI-64 Generator)
- 從 MAC Address 生成 IPv6 Interface ID
- 自動反轉第 7 位並插入 FFFE
- 驗證 MAC Address 格式合法性
- 支援多種 MAC Address 格式（`:`、`-`、`.`）

## 輔助功能

- **資料正規化**
  - 將全形字元轉半形
  - 統一大小寫並移除空白
  - IPv6 地址自動展開與補零

- **驗證**
  - 驗證 IP、子網遮罩、MAC Address、Offset、Sites
  - 驗證子網遮罩連續性與 EUI-64 子網遮罩合法性

- **命令列顏色顯示 (CLI)**
  - 不同顏色標示 IP、網段、MAC、Interface ID 等資訊
  - 提升命令列可讀性與使用體驗
