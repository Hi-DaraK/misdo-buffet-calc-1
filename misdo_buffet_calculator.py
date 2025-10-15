import streamlit as st
import pandas as pd

st.set_page_config(page_title="ミスド食べ放題計算機", page_icon="🍩")

# ------------------------
# 外部CSVからメニュー読み込み
# ------------------------
CSV_URL = "https://raw.githubusercontent.com/あなたのユーザー名/あなたのリポジトリ名/main/data/menu_202510.csv"

@st.cache_data
def load_menu(url):
    df = pd.read_csv(url, encoding="utf-8-sig")
    df["価格"] = pd.to_numeric(df["価格"], errors="coerce").fillna(0).astype(int)
    return df

df = load_menu(CSV_URL)

# ------------------------
# UI 表示
# ------------------------

st.title("🍩 ミスタードーナツ 食べ放題計算機")

# カテゴリとサブカテゴリを分割抽出
df["カテゴリ名"] = df["カテゴリ"].str.split("：").str[0]
df["サブカテゴリ"] = df["カテゴリ"].str.split("：").str[1]

# カテゴリ選択バー
unique_categories = df["カテゴリ名"].dropna().unique().tolist()
selected_category = st.selectbox("カテゴリを選んでください：", ["すべて"] + unique_categories)

# サブカテゴリ選択バー（絞り込み付き）
if selected_category != "すべて":
    filtered_df = df[df["カテゴリ名"] == selected_category].copy()
else:
    filtered_df = df.copy()

unique_subcats = filtered_df["サブカテゴリ"].dropna().unique().tolist()
selected_subcat = st.selectbox("サブカテゴリを選んでください：", ["すべて"] + unique_subcats)

# 最終フィルタリング
if selected_subcat != "すべて":
    filtered_df = filtered_df[filtered_df["サブカテゴリ"] == selected_subcat]

st.header(f"カテゴリ：{selected_category if selected_category != 'すべて' else '全体'}"
          f" / サブカテゴリ：{selected_subcat if selected_subcat != 'すべて' else '全体'}")

# 商品と個数入力
filtered_df["個数"] = filtered_df["商品名"].apply(
    lambda name: st.number_input(name, min_value=0, max_value=20, step=1, key=name)
)

# 合計金額計算
subtotal = (filtered_df["価格"] * filtered_df["個数"]).sum()

# 合計表示
st.markdown("---")
st.subheader(f"🍽 合計金額：¥{int(subtotal):,}")
st.caption("※ 価格はすべてイートイン・税込価格です")
