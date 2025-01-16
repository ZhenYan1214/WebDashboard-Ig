import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine


df = pd.read_csv(r'C:\Users\User\Desktop\Py\Pandas\archive\ig\social media influencers-instagram - -DEC 2022.csv')
#print(data.head())
#print(data.isnull().sum())

def convert_to_numeric(value):
    if isinstance(value, str):
        if 'K' in value:
            return float(value.replace('K', '')) * 1_000
        if 'M' in value:
            return float(value.replace('M', '')) * 1_000_000
    return float(value)

df['Followers'] = df['followers'].apply(convert_to_numeric).astype('int64')
df['Engagement Avg'] = df['Eng. (Avg.)'].apply(convert_to_numeric).astype('int64')

df.drop(['followers', 'Eng. (Avg.)', 'Category_2', 'Eng. (Auth.)', 'instagram name', 'Rank'], axis=1, inplace=True)
df.rename(columns={'Category_1': 'Category', 'name': 'Name', 'country': 'Country'}, inplace=True)


#print(df.isnull().sum())
df.fillna('None', inplace=True)
df['Engagement Rate'] = np.round((df['Engagement Avg'] / df['Followers']) * 100, 3)
df['Target'] = (df['Engagement Rate'] > 3.5).astype('int')

#clean_df = r'C:\Users\User\Desktop\Py\Pandas\archive\ig\clean_df.csv'
#df.to_csv(clean_df,index=False)
#print('成功')

server = 'LAPTOP-E5RI25OJ'  # 例如 'localhost\SQLEXPRESS'
database = 'InstagramAnalytics'  # 你的資料庫名稱
username = ''  # 如果使用 Windows Auth，留空
password = ''  # 如果使用 Windows Auth，留空

# 建立連接字符串
engine = create_engine(
    f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server'
)

# 將資料導入 SQL Server，建立新資料表
'''
try:
    df.to_sql('InstagramData', con=engine, if_exists='replace', index=False)
    print("✅ 資料已成功導入 SQL Server！")
except Exception as e:
    print(f"❌ 資料導入失敗: {e}")
'''


try:
    df_sql = pd.read_sql('SELECT * FROM InstagramData', con=engine)
    print('✅成功提取')
    #print(df_sql.head())
    top_engagement = df_sql.nlargest(10,'Engagement Rate')
    plt.figure(figsize=(10, 6))
    plt.barh(top_engagement['Name'], top_engagement['Engagement Rate'], color='skyblue')
    plt.xlabel('Engagement Rate (%)')
    plt.ylabel('Account Name')
    plt.title('Top 10 Instagram Accounts by Engagement Rate')
    plt.gca().invert_yaxis()
    plt.show()


except Exception as e:
    print(f'❌讀取失誤: {e}')













