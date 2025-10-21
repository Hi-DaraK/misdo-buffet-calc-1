import streamlit as st
import pandas as pd

st.set_page_config(page_title="ドーナツ食べ放題計算機", page_icon="🍩")

# ---------------------------------------
# 🔗 ローカルCSVファイルを読み込み
# ---------------------------------------
CSV_PATH = "data/menu.csv"

@st.cache_data
def load_menu(path):
    df = pd.read_csv(path, encoding="utf-8-sig")
    df["価格"] = pd.to_numeric(df["価格"], errors="coerce").fillna(0).astype(int)
    return df

df = load_menu(CSV_PATH)

# 📊 カテゴリ分割
df[["大カテゴリ", "サブカテゴリ"]] = df["カテゴリ"].str.split("：", expand=True)

# 🧠 セッションステート初期化（累計用）
if "saved_items" not in st.session_state:
    st.session_state.saved_items = []

# 🖼️ ヘッダー
st.markdown("### 🍩 食べ放題calculator")

# 🔽 フィルター：大カテゴリ
main_categories = ["すべて"] + sorted(df["大カテゴリ"].dropna().unique())
selected_main = st.selectbox("📌 大カテゴリを選んでください：", main_categories)

# 🔽 フィルター：サブカテゴリ
if selected_main == "すべて":
    filtered_df = df.copy()
    subcats = sorted(df["サブカテゴリ"].dropna().unique())
else:
    filtered_df = df[df["大カテゴリ"] == selected_main].copy()
    subcats = sorted(filtered_df["サブカテゴリ"].dropna().unique())

selected_sub = st.selectbox("📂 ジャンルを選んでください：", ["すべて"] + subcats)

if selected_sub != "すべて":
    filtered_df = filtered_df[filtered_df["サブカテゴリ"] == selected_sub]

# 🎯 選択中カテゴリ表示
st.markdown(f"### カテゴリ：{selected_main if selected_main != 'すべて' else '全体'} / ジャンル：{selected_sub if selected_sub != 'すべて' else '全体'}")

# 🍩 個数入力欄
filtered_df["個数"] = filtered_df["商品名"].apply(
    lambda name: st.number_input(name, min_value=0, max_value=20, step=1, key=name)
)

# 💴 合計金額計算
subtotal = (filtered_df["価格"] * filtered_df["個数"]).sum()

# 💰 食べ放題価格入力
st.markdown("### 🧾 食べ放題コースの金額を入力してください")
buffet_price = st.number_input("💰 食べ放題の価格（円）", min_value=0, max_value=10000, step=100, value=2000)

# 💾 セーブボタン
if st.button("➕ この組み合わせを追加する"):
    selected_items = filtered_df[filtered_df["個数"] > 0].copy()
    if not selected_items.empty:
        st.session_state.saved_items.append(selected_items)
        st.success("✅ 累計に追加しました！")
    else:
        st.warning("⚠ 商品を1つ以上選んでください")

# 🔄 リセットボタン
if st.button("🗑 累計をリセットする"):
    st.session_state.saved_items = []
    st.info("🧹 累計をリセットしました")

# 📊 通常の合計表示（今回の組み合わせ）
st.markdown("---")
st.subheader(f"🍽 今回の合計金額：¥{int(subtotal):,}")
diff = subtotal - buffet_price

if buffet_price == 0:
    st.info("※ 食べ放題の金額が未入力です")
elif diff > 0:
    st.success(f"🎉 元を取りました！ **¥{diff:,}** お得です！")
elif diff == 0:
    st.info("🟰 ちょうど元を取りました！ナイス！")
else:
    st.warning(f"📉 あと **¥{abs(diff):,}** で元が取れます！がんばれ！")

# 📋 累計表示
if st.session_state.saved_items:
    st.markdown("---")
    st.markdown("### 🧾 累計した注文一覧")
    combined_df = pd.concat(st.session_state.saved_items, ignore_index=True)
    combined_df_summary = combined_df.groupby("商品名", as_index=False).agg({
        "価格": "first",
        "個数": "sum"
    })
    combined_df_summary["小計"] = combined_df_summary["価格"] * combined_df_summary["個数"]
    st.dataframe(combined_df_summary[["商品名", "価格", "個数", "小計"]])

    # 累計合計金額と判定
    total_saved = combined_df_summary["小計"].sum()
    diff_saved = total_saved - buffet_price
    st.subheader(f"🧮 累計合計金額：¥{int(total_saved):,}")
    if buffet_price > 0:
        if diff_saved > 0:
            st.success(f"🎊 累計で元を取りました！ **¥{diff_saved:,}** お得です！")
        elif diff_saved == 0:
            st.info("🟰 累計でちょうど元を取りました！")
        else:
            st.warning(f"📉 累計であと **¥{abs(diff_saved):,}** 必要です")

# フッター署名
st.markdown("---")
st.markdown("<div style='text-align: right; font-size: 12px; color: gray;'>Presented by 原田くん🐧</div>", unsafe_allow_html=True)
