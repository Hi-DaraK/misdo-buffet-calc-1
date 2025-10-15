import streamlit as st

donut_menu = {
    "ポン・デ・リング": 140,
    "エンゼルクリーム": 151,
    "オールドファッション": 140,
    "ゴールデンチョコレート": 151,
    "フレンチクルーラー": 140,
    "チョコファッション": 151,
    "ハニーディップ": 140,
    "ストロベリーリング": 151
}

def main():
    st.title("🍩 ミスド食べ放題カリキュレーター")

    buffet_price = st.number_input("食べ放題の料金（円）", value=1500, step=10)

    st.markdown("---")
    st.header("🍩 食べたドーナツを記録")

    donut = st.selectbox("ドーナツの種類を選んでください", list(donut_menu.keys()))
    quantity = st.number_input("個数", min_value=1, value=1, step=1)

    if "eaten" not in st.session_state:
        st.session_state.eaten = []

    if st.button("追加"):
        st.session_state.eaten.append({"name": donut, "price": donut_menu[donut], "qty": quantity})

    if st.session_state.eaten:
        st.subheader("✅ 食べたドーナツ一覧")
        total = 0
        for item in st.session_state.eaten:
            item_total = item["price"] * item["qty"]
            total += item_total
            st.write(f"{item['name']} × {item['qty']}個 → {item_total} 円")

        st.markdown("---")
        st.subheader("☁️ 結果")
        st.write(f"合計金額: {total} 円")

        diff = total - buffet_price
        if diff > 0:
            st.success(f"{diff} 円お得でした！")
        elif diff == 0:
            st.info("ちょうど元が取れました！")
        else:
            st.warning(f"あと {-diff} 円で元が取れました。")

    if st.button("リセット"):
        st.session_state.eaten = []

if __name__ == "__main__":
    main()
