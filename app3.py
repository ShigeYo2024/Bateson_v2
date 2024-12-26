import streamlit as st
import openai
from textblob import TextBlob  # 感情分析に使用
import matplotlib.pyplot as plt  # グラフ描画用
import random  # シミュレーション用の仮データ生成

# OpenAI APIキーの設定
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# セッション状態の初期化
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": """あなたはグレゴリー・ベイトソンの教育モデルに基づいた教育コーチです。以下を行います：\n1. 感情状態を分析。\n2. 学習段階に応じた対話を提供。\n3. 内省を促進。"""}
    ]
if "progress" not in st.session_state:
    st.session_state["progress"] = {"zero_learning": 0, "first_learning": 0, "second_learning": 0, "third_learning": 0}

# 感情分析関数
def analyze_emotion(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.5:
        return "ポジティブ"
    elif polarity < -0.5:
        return "ネガティブ"
    else:
        return "ニュートラル"

# 学習段階ごとのメッセージを生成する関数
def generate_stage_message(stage, user_input):
    if stage == "zero_learning":
        return f"あなたの基本知識を確認します: {user_input}"
    elif stage == "first_learning":
        return f"新しい方法について考えてみましょう: {user_input}"
    elif stage == "second_learning":
        return f"あなたの考え方やパターンに焦点を当てます: {user_input}"
    elif stage == "third_learning":
        return f"より大きな視点であなたの世界観を再構築してみましょう: {user_input}"

# 学習進捗を更新する関数
def update_progress(stage):
    if stage in st.session_state["progress"]:
        st.session_state["progress"][stage] += 1

# 学習進捗の可視化
def visualize_progress():
    progress = st.session_state["progress"]
    stages = list(progress.keys())
    values = list(progress.values())

    plt.figure(figsize=(8, 6))
    plt.bar(stages, values, color='skyblue')
    plt.title("学習進捗の可視化")
    plt.xlabel("学習段階")
    plt.ylabel("対話数")
    st.pyplot(plt)

# シミュレーション機能
def interactive_simulation():
    st.write("### インタラクティブシミュレーション")
    scenario = random.choice([
        "チームでの意見交換を円滑に進める方法を考える",
        "新しいプロジェクトの計画を立てる",
        "お客さまからのフィードバックに対応する",
        "経営陣向けの説明を円滑に進める方法を考える",
        "対立する意見を持つ人々の対立状態を解消する"
    ])
    st.write(f"シナリオ: {scenario}")
    user_action = st.text_input("この状況でどう対応しますか？")

    if user_action:
        st.write("🤖 コーチのフィードバック: よい視点です。さらに考えるべきポイントは...")

# 推薦エンジン
def personalized_recommendation():
    st.write("### あなたにおすすめの提案")
    progress = st.session_state["progress"]
    if progress["third_learning"] > 3:
        st.write("おすすめの提案: 高度なケーススタディ")
    elif progress["second_learning"] > 3:
        st.write("おすすめの提案: 思考パターンを深めるための読書")
    elif progress["first_learning"] > 3:
        st.write("おすすめの提案: 新しいスキルを学ぶためのオンライン講座")
    else:
        st.write("おすすめの提案: 基礎知識を復習するための教材")

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    # ユーザーのメッセージを追加
    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    # 感情分析の結果を追加
    emotion = analyze_emotion(st.session_state["user_input"])
    messages.append({"role": "assistant", "content": f"感情分析結果: {emotion}"})

    # 学習段階の判定 (仮のロジック)
    if "基礎" in st.session_state["user_input"]:
        stage = "zero_learning"
    elif "方法" in st.session_state["user_input"]:
        stage = "first_learning"
    elif "パターン" in st.session_state["user_input"]:
        stage = "second_learning"
    else:
        stage = "third_learning"

    # 学習進捗を更新
    update_progress(stage)

    # 学習段階に基づくメッセージ生成
    stage_message = generate_stage_message(stage, st.session_state["user_input"])
    messages.append({"role": "assistant", "content": stage_message})

    # OpenAI API呼び出し
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages
        )
        bot_message = response["choices"][0]["message"]
        messages.append(bot_message)
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")

    st.session_state["user_input"] = ""

# ユーザーインターフェイスの構築
st.title("AI Coach べいとそん: 学びの段階・シミュレーション・次のステップに向けたおすすめの提案")

user_input = st.text_input("今の気持ちと学びたいことを教えてください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]
    for message in reversed(messages[1:]):
        speaker = "🙂" if message["role"] == "user" else "🤖"
        st.write(f"{speaker}: {message['content']}")

# サマリー表示
if st.button("学びの段階を見える化する"):
    visualize_progress()

if st.button("シミュレーションにより学ぶ"):
    interactive_simulation()

if st.button("次のステップに向けたおすすめ提案を確認する"):
    personalized_recommendation()
