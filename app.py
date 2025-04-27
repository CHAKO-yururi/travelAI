import streamlit as st
import pandas as pd

# データ読み込み
routes = pd.read_csv('routes.csv', encoding='utf-8-sig')

# タイトル
st.title("🚃 旅の交通サポートチャット（バージョンアップ！）")

# 言語選択
language = st.selectbox(
    "言語を選んでください / Select your language",
    ("日本語", "English")
)
# 優先度の日本語→英語マッピング
priority_mapping = {
    "早い": "Speed",
    "安い": "Price",
    "楽": "Comfort"
}
# 出発地・到着地の日本語→英語マッピング
location_mapping = {
    "片瀬江ノ島駅": "Katase-Enoshima Station",
    "藤沢駅": "Fujisawa Station",
    "新宿駅": "Shinjuku Station",
    "渋谷駅": "Shibuya Station",
    "東京駅": "Tokyo Station",
    "品川駅": "Shinagawa Station",
    "小田原駅": "Odawara Station",
    "新大阪": "Shin-Osaka",
    "成田空港": "Narita Airport",
    "羽田空港": "Haneda Airport",
    "箱根": "Hakone",
    "富士山": "Mt. Fuji",
    "鎌倉駅": "Kamakura Station"
}

# 入力項目
if language == "日本語":
    departure_label = "出発地を選んでください"
    destination_label = "目的地を選んでください"
    priority_label = "一番優先したいのは？"
    priority_options = ("早い", "安い", "楽")
    button_label = "最適な交通手段を提案する！"
    result_prefix = "から"
    result_suffix = "までは、"
    result_suffix2 = "がおすすめです！"
else:
    departure_label = "Select your departure location"
    destination_label = "Select your destination"
    priority_label = "What do you prioritize?"
    priority_options = ("Speed", "Price", "Comfort") 
    button_label = "Suggest the best route!"
    result_prefix = "From "
    result_suffix = " to "
    result_suffix2 = ", the best way is "

# 出発地・到着地の選択肢を言語に合わせて変える
if language == "日本語":
    departure_options = routes['出発地'].unique()
    destination_options = routes['到着地'].unique()
else:
    departure_options = [location_mapping.get(loc, loc) for loc in routes['出発地'].unique()]
    destination_options = [location_mapping.get(loc, loc) for loc in routes['到着地'].unique()]

departure = st.selectbox(departure_label, departure_options)
destination = st.selectbox(destination_label, destination_options)
priority = st.radio(priority_label, priority_options)

# 「検索する」ボタン
if st.button(button_label):

    # 優先度・出発地・到着地を日本語に戻す（英語選択時だけ）
    search_priority = priority
    search_departure = departure
    search_destination = destination

    if language == "English":
        reverse_priority_mapping = {v: k for k, v in priority_mapping.items()}
        reverse_location_mapping = {v: k for k, v in location_mapping.items()}
        
        search_priority = reverse_priority_mapping.get(priority, priority)
        search_departure = reverse_location_mapping.get(departure, departure)
        search_destination = reverse_location_mapping.get(destination, destination)

    # 検索（ここで日本語に戻したあとにやる！）
    result = routes[
        (routes['出発地'] == search_departure) & (routes['到着地'] == search_destination)
    ]

    if not result.empty:
        suggestion = result.iloc[0][search_priority]
        st.subheader("🚀 提案結果")
        st.write(f"{departure}{result_prefix}{destination}{result_suffix}{suggestion}{result_suffix2}")
    else:
        st.subheader("😢 提案できるルートが見つかりませんでした。")
