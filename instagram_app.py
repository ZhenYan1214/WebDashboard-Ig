import streamlit as st
import pandas as pd
import plotly.express as px
import io
import xlsxwriter
from sqlalchemy import create_engine

# 📊 1. SQL Server 連接
server = 'LAPTOP-E5RI25OJ'
database = 'InstagramAnalytics'
engine = create_engine(f'mssql+pyodbc://@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server')


#提取數據
@st.cache
def fetch_data():
    query = 'SELECT * FROM InstagramData'
    return pd.read_sql(query,con=engine)

df = fetch_data()

# 標題
st.markdown(
    """
    <style>
        .title {
            font-size: 2.5rem;
            font-weight: bold;
            text-align: center;
            color: #004e89;
            margin-bottom: 10px;
        }
        .subtitle {
            font-size: 1.2rem;
            text-align: center;
            color: #555555;
        }
        .divider {
            border-top: 2px solid #004e89;
            margin: 20px 0;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="title">📊 Instagram 數據分析儀表板</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">深入洞察您的數據，輕鬆篩選並進行可視化分析</div>', unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


# 篩選條件
st.sidebar.header("篩選條件")

# 初始化國家選項
countries = []
categories =[]
# 計算可用的類別選項
available_categories = (
    df['Category'].unique() if not countries
    else df[df['Country'].isin(countries)]['Category'].unique()
)

# 計算可用的國家選項
available_countries = (
    df['Country'].unique() if not categories
    else df[df['Category'].isin(categories)]['Country'].unique()
)

# 設定預設值
default_categories = ["Music", "Sports with a ball"]
default_countries = ["United States", "Argentina"]

# 顯示類別選項
categories = st.sidebar.multiselect(
    "選擇類別（Category）：", 
    options=available_categories, 
    default=default_categories if not categories else categories  # 預設為最常用
)

# 顯示國家選項
countries = st.sidebar.multiselect(
    "選擇國家（Country）：", 
    options=available_countries, 
    default=default_countries if not countries else countries  # 預設為最常用
)




# 增加提示信息
if not categories:
    st.sidebar.info("請選擇至少一個類別")
if not countries:
    st.sidebar.info("請選擇至少一個國家")


min_followers = st.sidebar.slider(
    "最少粉絲數（Followers）", 
    int(df['Followers'].min()), 
    int(df['Followers'].max()), 
    value=int(df['Followers'].min()),  # 確保默認值為最小值
    step=1000
)
max_followers = st.sidebar.slider(
    "最多粉絲數（Followers）", 
    int(df['Followers'].min()), 
    int(df['Followers'].max()), 
    value=int(df['Followers'].max()),  # 確保默認值為最大值
    step=1000
)

min_engagement = st.sidebar.slider(
    "最少互動率（Engagement Rate %）", 
    float(df['Engagement Rate'].min()), 
    float(df['Engagement Rate'].max()), 
    value=float(df['Engagement Rate'].min()),  # 確保默認值為最小值
    step=0.1
)
max_engagement = st.sidebar.slider(
    "最多互動率（Engagement Rate %）", 
    float(df['Engagement Rate'].min()), 
    float(df['Engagement Rate'].max()), 
    value=float(df['Engagement Rate'].max()),  # 確保默認值為最大值
    step=0.1
)


#過濾
# 過濾數據
def filter_data(df, categories, countries, min_followers, max_followers, min_engagement, max_engagement):
    return df[
        (df['Category'].isin(categories)) & 
        (df['Country'].isin(countries)) & 
        (df['Followers'].between(min_followers, max_followers)) & 
        (df['Engagement Rate'].between(min_engagement, max_engagement))
    ]


# 檢查篩選條件是否足夠
if not categories or not countries:
    st.warning("⚠️ 請選擇篩選條件以查看結果")
else:
    # 過濾數據
    filtered_df = filter_data(df, categories, countries, min_followers, max_followers, min_engagement, max_engagement)

    if filtered_df.empty:
        st.warning("⚠️ 沒有符合條件的數據，請嘗試放寬篩選條件！")
    else:
        # 篩選結果展示
        st.subheader(f"篩選結果：類別-{', '.join(categories)}   國家-{', '.join(countries)}")
        st.write(f"共有 {len(filtered_df)} 筆符合條件")
        st.dataframe(filtered_df)

        # 匯出數據
        export_format = st.radio('選擇匯出格式', options=['CSV', 'Excel'])
        if st.button('匯出數據'):
            filename_categories = "_".join(categories) if categories else "所有類別"
            filename_countries = "_".join(countries) if countries else "所有國家"

            if export_format == 'CSV':
                filtered_df.to_csv(f'{filename_categories}_{filename_countries}_data.csv', index=False)
                st.success(f'數據已匯出為 {filename_categories}_{filename_countries}_data.csv 文件！')
            elif export_format == 'Excel':
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    filtered_df.to_excel(writer, index=False, sheet_name='Filtered Data')
                st.download_button(
                    label='下載Excel文件',
                    data=output.getvalue(),
                    file_name=f'{filename_categories}_{filename_countries}_data.xlsx',
                    mime="application/vnd.ms-excel"
                )

        # 圖表展示
        st.subheader('Top10 互動率帳號')
        top_engagement = filtered_df.nlargest(10, 'Engagement Rate')
        st.bar_chart(top_engagement[['Name', 'Engagement Rate']].set_index('Name'))

        fig = px.scatter(
            filtered_df,
            x="Followers",
            y="Engagement Rate",
            color="Category",
            size="Engagement Rate",
            hover_data=["Name", "Followers", "Engagement Rate"],
            trendline="ols",
            title=f"粉絲數 vs. 互動率（類別：{', '.join(categories)}   國家：{', '.join(countries)}）"
        )
        st.plotly_chart(fig, use_container_width=True)

        # 數據摘要
        total_filtered_accounts = len(filtered_df)
        total_filtered_followers = filtered_df['Followers'].sum()
        avg_filtered_engagement_rate = filtered_df['Engagement Rate'].mean()

        st.write("### 篩選後數據摘要")
        st.markdown(
            f"""
            - 📊 **篩選後總帳號數：** {total_filtered_accounts}
            - 👥 **總粉絲數：** {total_filtered_followers:,}
            - ✨ **平均互動率：** {avg_filtered_engagement_rate:.2f}%
            """
        )