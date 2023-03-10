# インポート
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import japanize_matplotlib
import numpy as np
from io import BytesIO

# パスワードはstreamlitのシークレットに保存
# パスワード入力
def login():
    value = st.sidebar.text_input('パスワードを入力してください:', type='password')
    if value == st.secrets['password']:
        st.sidebar.write('パスワードを確認しました！')
    else:
        st.stop()

login()

st.title('検定コーナーの正解率を取得')
st.write('ファイルをアップロードして、解答の割合を表示します')

files = st.file_uploader("データファイルをアップロード", type='csv', accept_multiple_files=True)
st.write('複数のファイルをアップロードできます')

button= st.button('処理を実行')

if files and button:
    for file in files:
        try:
            df = pd.read_csv(file, encoding='shift-jis')
            category = df.loc[0, '名称']
            date = df.loc[0, '登録日時'][2:12]
            df_color = round(df.groupby('解答色').count()['番組識別文字列'] / len(df), 4) * 100
            df_color = pd.DataFrame(df_color)
            df_color['count'] = df.groupby('解答色').count()['番組識別文字列']
            df_color.reset_index(inplace=True, drop=True)
            df_color.index = ['青', '赤','緑']
            df_color.rename(columns={'番組識別文字列': f'{category} {date}'}, inplace=True)
            st.dataframe(df_color.T.style.format('{:.0f}'))
            fig = plt.figure(figsize=(3,3))
            labels = ["青", "赤", "緑"]
            colors = ["blue", "red", "green"]
            textprops = textprops = {'fontsize':8}
            x = df_color.iloc[:,0].to_numpy().reshape(-1)
            plt.pie(x, labels=labels, colors=colors, counterclock=False, startangle=90, autopct="%.2f%%", textprops=textprops)
            plt.title(category + '  ' + date, fontsize=10)
            plt.show()
            buf = BytesIO()
            fig.savefig(buf, format="png")
            st.image(buf, width=300)
        except Exception as e:
            st.write('ファイルが正しくない可能性があります')                       
    st.write('処理を実行しました')
