import streamlit as st
import pandas as pd

st.set_page_config(page_title="ドーナツ食べ放題計算機", page_icon="🍩")
# ---------------------------------------
# 🔗 外部CSVのURL → 🔽 リポジトリ内のローカルファイルに変更
# ---------------------------------------
CSV_PATH = "data/menu.csv"  # ← 相対パスで指定

@st.cache_data
def load_menu(path):
    df = pd.read_csv(path, encoding="utf-8-sig")  # ← url → path に変更
    df["価格"] = pd.to_numeric(df["価格"], errors="coerce").fillna(0).astype(int)
    return df

df = load_menu(CSV_PATH)  # ← CSV_URL → CSV_PATH に変更

# ---------------------------------------
# 📊 カテゴリ分割
# ---------------------------------------
df[["大カテゴリ", "サブカテゴリ"]] = df["カテゴリ"].str.split("：", expand=True)

# ---------------------------------------
# 🖼️ UI 表示
# ---------------------------------------
# st.title("🍩食べ放題計算機") ← この行をコメントアウト or 削除
st.markdown("### 🍩 食べ放題calculator")  # 小見出しサイズ（h3相当）

# 第1フィルター：大カテゴリ（定番 / 期間限定 / ザクもっち etc）
main_categories = ["すべて"] + sorted(df["大カテゴリ"].dropna().unique())
selected_main = st.selectbox("📌 大カテゴリを選んでください：", main_categories)

# 第2フィルター：サブカテゴリ（ポンデ系、ハロウィン、パイなど）
if selected_main == "すべて":
    filtered_df = df.copy()
    subcats = sorted(df["サブカテゴリ"].dropna().unique())
else:
    filtered_df = df[df["大カテゴリ"] == selected_main].copy()
    subcats = sorted(filtered_df["サブカテゴリ"].dropna().unique())

selected_sub = st.selectbox("📂 ジャンルを選んでください：", ["すべて"] + subcats)

# 最終フィルター
if selected_sub != "すべて":
    filtered_df = filtered_df[filtered_df["サブカテゴリ"] == selected_sub]

# タイトル表示
#st.header(f"カテゴリ：{selected_main if selected_main != 'すべて' else '全体'} / ジャンル：{selected_sub if selected_sub != 'すべて' else '全体'}")
st.markdown(f"### カテゴリ：{selected_main if selected_main != 'すべて' else '全体'} / ジャンル：{selected_sub if selected_sub != 'すべて' else '全体'}")

# 個数入力欄
filtered_df["個数"] = filtered_df["商品名"].apply(
    lambda name: st.number_input(name, min_value=0, max_value=20, step=1, key=name)
)

# 合計金額計算
subtotal = (filtered_df["価格"] * filtered_df["個数"]).sum()
# ------------------------------
# 🏷 食べ放題価格の入力欄
# ------------------------------
st.markdown("### 🧾 食べ放題コースの金額を入力してください")
buffet_price = st.number_input("💰 食べ放題の価格（円）", min_value=0, max_value=10000, step=100, value=1800)

# ------------------------------
# 💡 損得計算
# ------------------------------
diff = subtotal - buffet_price

st.markdown("---")
if buffet_price == 0:
    st.info("※ 食べ放題の金額が未入力です")
elif diff > 0:
    st.success(f"🎉 元を取りました！ **¥{diff:,}** お得です！")
elif diff == 0:
    st.info("🟰 ちょうど元を取りました！ナイス！")
else:
    st.warning(f"📉 あと **¥{abs(diff):,}** で元が取れます！がんばれ！")


# 合計表示
st.markdown("---")
st.subheader(f"🍽 合計金額：¥{int(subtotal):,}")
st.caption("※ 価格はすべてイートイン・税込価格です")
