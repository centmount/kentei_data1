# インポート
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import japanize_matplotlib

st.title('検定コーナーの正解率を取得')
st.write('ファイルをアップロードして、解答の割合を表示します')

files = st.file_uploader("データファイルをアップロード", type='csv', accept_multiple_files=True)
st.write('複数のファイルをアップロードできます')

button= st.button('処理を実行')

if button:
    for file in files:
        df = pd.read_csv(file, encoding='shift-jis')
        category = df.loc[0, '名称']
        date = df.loc[0, '登録日時'][2:12]
        df_color = round(df['解答色'].value_counts() / df['解答色'].count(), 4) * 100
        df_color = pd.DataFrame(df_color)
        df_color.index = ['青', '赤', '緑']
        df_color.columns = [category + '  ' + date]
        st.dataframe(df_color.T)
        fig = plt.figure(figsize=(8,8))
        labels = ["青", "赤", "緑"]
        colors = ["blue", "red", "green"]
        textprops = textprops = {'fontsize':16}
        plt.pie(df_color, labels=labels, colors=colors, counterclock=False, startangle=90, autopct="%.2f%%", textprops=textprops)
        plt.title(category + '  ' + date, fontsize=20)
        plt.show()
        st.pyplot(fig)
        st.write('処理を実行しました')
