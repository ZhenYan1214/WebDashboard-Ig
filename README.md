# 📊 Instagram Analytics Dashboard

### **專案簡介**
這是一個基於 **Streamlit** 的數據分析應用，幫助用戶篩選和分析 Instagram 帳號數據。專案目標是通過互動式的篩選功能、數據摘要和視覺化工具，協助用戶快速了解數據中的趨勢和洞察。
![Demo GIF](Example.gif)
---

## 🔑 **專案功能**
1. **數據篩選與條件設置**：
   - 按照類別（Category）、國家（Country）、粉絲數範圍（Followers）及互動率範圍（Engagement Rate）篩選數據。
   - 提供動態更新篩選選項，篩選條件的選擇更精準。

2. **數據摘要**：
   - 篩選後自動計算總帳號數、總粉絲數及平均互動率，快速提供關鍵數據。

3. **視覺化展示**：
   - 條形圖展示 Top 10 高互動率帳號。
   - 散點圖顯示粉絲數與互動率之間的關係，並添加回歸線（OLS）分析。

4. **數據導出**：
   - 支持將篩選後的數據導出為 **CSV** 或 **Excel** 文件。

---

## 🛠️ 技術堆疊
- **後端數據庫**：Microsoft SQL Server
- **前端框架**：Streamlit
- **數據清洗與處理**：Pandas
- **數據視覺化**：Plotly Express
- **文件導出**：支持 Excel 和 CSV 格式

- ## 🔍 數據來源
數據集為 [https://www.kaggle.com/datasets/ramjasmaurya/top-1000-social-media-channels]

