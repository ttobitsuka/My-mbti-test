import streamlit as st
import time
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="WAIS風知能測定アプリ", layout="centered")

# =========================
# 問題データ（32問）
# 方式B：領域ごとにまとめて出題
# =========================
QUESTIONS = [
    # ================= VCI（1〜8） =================
    {
        "id": 1,
        "domain": "VCI",
        "domain_label": "言語理解",
        "subtype": "類似",
        "difficulty": 1,
        "weight": 1,
        "q": "「自由」と「規律」の共通点は？",
        "options": [
            "反対の意味",
            "社会生活における個人のあり方",
            "法律の別名",
            "感情の種類"
        ],
        "answer": "社会生活における個人のあり方",
        "expl": "抽象概念の共通点を見抜く問題です。"
    },
    {
        "id": 2,
        "domain": "VCI",
        "domain_label": "言語理解",
        "subtype": "語彙",
        "difficulty": 1,
        "weight": 1,
        "q": "「杞憂」の正しい意味は？",
        "options": [
            "無意味な心配",
            "深い悲しみ",
            "災難",
            "計画的な行動"
        ],
        "answer": "無意味な心配",
        "expl": "語彙の意味を正確に把握できているかを見ます。"
    },
    {
        "id": 3,
        "domain": "VCI",
        "domain_label": "言語理解",
        "subtype": "ことわざ",
        "difficulty": 2,
        "weight": 2,
        "q": "「情けは人のためならず」の正しい意味は？",
        "options": [
            "人に親切にしても無駄",
            "甘やかすのはよくない",
            "人への親切は巡って自分に返る",
            "情けをかけてはいけない"
        ],
        "answer": "人への親切は巡って自分に返る",
        "expl": "ことわざ・慣用句の正確な理解を測ります。"
    },
    {
        "id": 13,
        "domain": "VCI",
        "domain_label": "言語理解",
        "subtype": "類似",
        "difficulty": 1,
        "weight": 1,
        "q": "「希望」と「不安」の共通点は？",
        "options": [
            "どちらも食べ物",
            "どちらも未来に関する感情",
            "どちらも病気の名前",
            "どちらも法律用語"
        ],
        "answer": "どちらも未来に関する感情",
        "expl": "抽象語どうしの共通点を見抜く問題です。"
    },
    {
        "id": 14,
        "domain": "VCI",
        "domain_label": "言語理解",
        "subtype": "語彙",
        "difficulty": 2,
        "weight": 2,
        "q": "「本末転倒」の正しい意味は？",
        "options": [
            "大事なこととそうでないことを取り違えること",
            "物事が順調に進むこと",
            "意見が一致すること",
            "最初からやり直すこと"
        ],
        "answer": "大事なこととそうでないことを取り違えること",
        "expl": "ことわざ・四字熟語の意味理解を測ります。"
    },
    {
        "id": 15,
        "domain": "VCI",
        "domain_label": "言語理解",
        "subtype": "ことわざ",
        "difficulty": 2,
        "weight": 2,
        "q": "「石の上にも三年」が最も伝えたいことは？",
        "options": [
            "石は三年で壊れる",
            "つらくても続ければ成果が出ることがある",
            "冷たい場所に座ってはいけない",
            "時間は無駄にしてはいけない"
        ],
        "answer": "つらくても続ければ成果が出ることがある",
        "expl": "ことわざの本来の意味を理解できるかを見る問題です。"
    },
    {
        "id": 16,
        "domain": "VCI",
        "domain_label": "言語理解",
        "subtype": "概念理解",
        "difficulty": 2,
        "weight": 2,
        "q": "「教師」と「医師」の共通点として最も適切なのは？",
        "options": [
            "どちらも学校にいる",
            "どちらも専門知識を使って人を支える職業",
            "どちらも同じ資格でなれる",
            "どちらも必ず白衣を着る"
        ],
        "answer": "どちらも専門知識を使って人を支える職業",
        "expl": "表面的ではなく、本質的な共通点を捉える問題です。"
    },
    {
        "id": 17,
        "domain": "VCI",
        "domain_label": "言語理解",
        "subtype": "語彙",
        "difficulty": 3,
        "weight": 3,
        "q": "「示唆」に最も近い意味は？",
        "options": [
            "明確な命令",
            "それとなく気づかせること",
            "強く反対すること",
            "失敗を責めること"
        ],
        "answer": "それとなく気づかせること",
        "expl": "語彙の精密な理解を測るやや難しめの問題です。"
    },

    # ================= PRI（9〜16） =================
    {
        "id": 4,
        "domain": "PRI",
        "domain_label": "知覚推理",
        "subtype": "数列",
        "difficulty": 1,
        "weight": 1,
        "q": "1, 3, 7, 15, 31, (?) 次の数字は？",
        "options": ["62", "63", "46", "55"],
        "answer": "63",
        "expl": "前の数を2倍して1を足す規則です。"
    },
    {
        "id": 5,
        "domain": "PRI",
        "domain_label": "知覚推理",
        "subtype": "数列",
        "difficulty": 1,
        "weight": 1,
        "q": "1, 1, 2, 3, 5, 8, (?) 次の数字は？",
        "options": ["11", "13", "15", "10"],
        "answer": "13",
        "expl": "前2つの数を足すフィボナッチ型の数列です。"
    },
    {
        "id": 6,
        "domain": "PRI",
        "domain_label": "知覚推理",
        "subtype": "論理",
        "difficulty": 2,
        "weight": 2,
        "q": "A > B、B > C のとき、必ず言えることは？",
        "options": ["A > C", "A < C", "A = C", "判断できない"],
        "answer": "A > C",
        "expl": "大小関係の推移性を使う問題です。"
    },
    {
        "id": 18,
        "domain": "PRI",
        "domain_label": "知覚推理",
        "subtype": "数列",
        "difficulty": 1,
        "weight": 1,
        "q": "2, 4, 6, 8, (?) 次の数字は？",
        "options": ["9", "10", "11", "12"],
        "answer": "10",
        "expl": "2ずつ増える単純な等差数列です。"
    },
    {
        "id": 19,
        "domain": "PRI",
        "domain_label": "知覚推理",
        "subtype": "数列",
        "difficulty": 2,
        "weight": 2,
        "q": "2, 5, 10, 17, 26, (?) 次の数字は？",
        "options": ["35", "36", "37", "38"],
        "answer": "37",
        "expl": "差が 3, 5, 7, 9 と増えているので、次は +11 です。"
    },
    {
        "id": 20,
        "domain": "PRI",
        "domain_label": "知覚推理",
        "subtype": "論理",
        "difficulty": 2,
        "weight": 2,
        "q": "すべての赤い箱は大きい。ある箱Aは赤い。必ず言えることは？",
        "options": [
            "箱Aは小さい",
            "箱Aは大きい",
            "箱Aは赤くない",
            "判断できない"
        ],
        "answer": "箱Aは大きい",
        "expl": "条件文から確実に導ける結論を選ぶ問題です。"
    },
    {
        "id": 21,
        "domain": "PRI",
        "domain_label": "知覚推理",
        "subtype": "規則発見",
        "difficulty": 2,
        "weight": 2,
        "q": "3, 6, 12, 24, (?) 次の数字は？",
        "options": ["36", "42", "48", "54"],
        "answer": "48",
        "expl": "前の数を2倍していく規則です。"
    },
    {
        "id": 22,
        "domain": "PRI",
        "domain_label": "知覚推理",
        "subtype": "論理",
        "difficulty": 3,
        "weight": 3,
        "q": "AはBより重い。BはCより軽い。このとき必ず言えることは？",
        "options": [
            "AはCより重い",
            "AはCより軽い",
            "AとCの重さ関係は確定しない",
            "Bが最も重い"
        ],
        "answer": "AとCの重さ関係は確定しない",
        "expl": "A>B と C>B は分かりますが、AとCの大小関係は確定しません。"
    },

    # ================= WMI（17〜24） =================
    {
        "id": 7,
        "domain": "WMI",
        "domain_label": "ワーキングメモリ",
        "subtype": "逆唱",
        "difficulty": 1,
        "weight": 1,
        "q": "「8-2-5-9」を後ろから言うと？",
        "options": ["9-5-2-8", "9-2-5-8", "8-5-2-9", "2-5-8-9"],
        "answer": "9-5-2-8",
        "expl": "保持した情報を逆順に操作する問題です。"
    },
    {
        "id": 8,
        "domain": "WMI",
        "domain_label": "ワーキングメモリ",
        "subtype": "並べ替え",
        "difficulty": 3,
        "weight": 3,
        "q": "「6」「2」「9」を小さい順に並べ、そのあと逆から読むと？",
        "options": ["9-6-2", "9-2-6", "6-2-9", "2-6-9"],
        "answer": "9-6-2",
        "expl": "一度並べ替えてから、さらに逆転操作をする問題です。"
    },
    {
        "id": 9,
        "domain": "WMI",
        "domain_label": "ワーキングメモリ",
        "subtype": "暗算",
        "difficulty": 3,
        "weight": 3,
        "q": "8に4を足し、2倍して、最後に6を引くと？",
        "options": ["18", "20", "22", "24"],
        "answer": "18",
        "expl": "複数手順を保持しながら処理する暗算課題です。"
    },
    {
        "id": 23,
        "domain": "WMI",
        "domain_label": "ワーキングメモリ",
        "subtype": "逆唱",
        "difficulty": 1,
        "weight": 1,
        "q": "「4-1-7」を後ろから言うと？",
        "options": ["7-1-4", "7-4-1", "1-7-4", "4-7-1"],
        "answer": "7-1-4",
        "expl": "短い数列を逆順に保持・操作する問題です。"
    },
    {
        "id": 24,
        "domain": "WMI",
        "domain_label": "ワーキングメモリ",
        "subtype": "並べ替え＋操作",
        "difficulty": 3,
        "weight": 3,
        "q": "「3・7・1」を小さい順に並べ、その後すべてに2を足すとどうなる？",
        "options": ["5-9-3", "3-5-9", "5-3-9", "9-5-3"],
        "answer": "3-5-9",
        "expl": "並べ替えと同時に計算処理を行う複合的なワーキングメモリ課題です。"
    },
    {
        "id": 25,
        "domain": "WMI",
        "domain_label": "ワーキングメモリ",
        "subtype": "暗算",
        "difficulty": 2,
        "weight": 2,
        "q": "12から4を引いて、その結果に6を足すと？",
        "options": ["12", "13", "14", "15"],
        "answer": "14",
        "expl": "途中結果を保持しながら処理する問題です。"
    },
    {
        "id": 26,
        "domain": "WMI",
        "domain_label": "ワーキングメモリ",
        "subtype": "逆唱",
        "difficulty": 2,
        "weight": 2,
        "q": "「3-9-2-6」を後ろから言うと？",
        "options": ["6-2-9-3", "6-9-2-3", "3-2-9-6", "2-6-9-3"],
        "answer": "6-2-9-3",
        "expl": "保持量が少し増えた逆唱課題です。"
    },
    {
        "id": 27,
        "domain": "WMI",
        "domain_label": "ワーキングメモリ",
        "subtype": "暗算",
        "difficulty": 3,
        "weight": 3,
        "q": "5を2倍して、3を足して、最後に4を引くと？",
        "options": ["8", "9", "10", "11"],
        "answer": "9",
        "expl": "複数手順を頭の中で順番に処理する問題です。"
    },

    # ================= PSI（25〜32） =================
    {
        "id": 10,
        "domain": "PSI",
        "domain_label": "処理速度",
        "subtype": "照合",
        "difficulty": 1,
        "weight": 1,
        "time_limit": 8,
        "q": "次のうち、他と異なるものはどれ？",
        "options": ["AB12", "AB12", "AB21", "AB12"],
        "answer": "AB21",
        "expl": "素早く違いを見つける力を測る問題です。"
    },
    {
        "id": 11,
        "domain": "PSI",
        "domain_label": "処理速度",
        "subtype": "比較",
        "difficulty": 1,
        "weight": 1,
        "time_limit": 8,
        "q": "次のうち、最も大きい数は？",
        "options": ["98", "89", "108", "99"],
        "answer": "108",
        "expl": "単純な比較を素早く正確に行う問題です。"
    },
    {
        "id": 12,
        "domain": "PSI",
        "domain_label": "処理速度",
        "subtype": "照合",
        "difficulty": 2,
        "weight": 2,
        "time_limit": 6,
        "q": "次のうち、完全に同じ並びはどれ？  『K7M2』",
        "options": ["K7N2", "K7M2", "KM72", "K2M7"],
        "answer": "K7M2",
        "expl": "視覚的な照合の正確さを測る問題です。"
    },
    {
        "id": 28,
        "domain": "PSI",
        "domain_label": "処理速度",
        "subtype": "照合",
        "difficulty": 1,
        "weight": 1,
        "time_limit": 8,
        "q": "次のうち、他と異なるものはどれ？",
        "options": ["XZ31", "XZ31", "XZ13", "XZ31"],
        "answer": "XZ13",
        "expl": "すばやく並びの違いを見つける問題です。"
    },
    {
        "id": 29,
        "domain": "PSI",
        "domain_label": "処理速度",
        "subtype": "比較",
        "difficulty": 1,
        "weight": 1,
        "time_limit": 8,
        "q": "次のうち、最も小さい数は？",
        "options": ["71", "17", "27", "70"],
        "answer": "17",
        "expl": "単純な数の比較を正確に行う問題です。"
    },
    {
        "id": 30,
        "domain": "PSI",
        "domain_label": "処理速度",
        "subtype": "照合",
        "difficulty": 2,
        "weight": 2,
        "time_limit": 6,
        "q": "次のうち、完全に同じ並びはどれ？ 『R4T8』",
        "options": ["R4T8", "R4T6", "RT48", "R8T4"],
        "answer": "R4T8",
        "expl": "視覚的な照合を素早く行う問題です。"
    },
    {
        "id": 31,
        "domain": "PSI",
        "domain_label": "処理速度",
        "subtype": "比較",
        "difficulty": 2,
        "weight": 2,
        "time_limit": 6,
        "q": "次のうち、最も大きい数は？",
        "options": ["209", "290", "192", "220"],
        "answer": "290",
        "expl": "桁を見落とさずに比較できるかを測ります。"
    },
    {
        "id": 32,
        "domain": "PSI",
        "domain_label": "処理速度",
        "subtype": "照合",
        "difficulty": 3,
        "weight": 3,
        "time_limit": 5,
        "q": "次のうち、他と異なるものはどれ？",
        "options": ["M2Q7", "M2Q7", "M2O7", "M2Q7"],
        "answer": "M2O7",
        "expl": "似た文字列の中から1文字違いを見抜くやや難しめの問題です。"
    },
]

DOMAINS = ["VCI", "PRI", "WMI", "PSI"]
DOMAIN_LABELS = {
    "VCI": "言語理解",
    "PRI": "知覚推理",
    "WMI": "ワーキングメモリ",
    "PSI": "処理速度",
}

DOMAIN_NORMS = {
    "VCI": {"mean": 8.0, "sd": 2.5},
    "PRI": {"mean": 8.0, "sd": 2.5},
    "WMI": {"mean": 8.0, "sd": 2.5},
    "PSI": {"mean": 8.0, "sd": 2.5},
}

DEBUG_MODE = True

# =========================
# ユーティリティ
# =========================
def fill_debug_answers(mode="all_correct"):
    import random

    st.session_state.answers = []
    st.session_state.raw_scores = {domain: 0 for domain in DOMAINS}

    for q in QUESTIONS:
        if mode == "all_correct":
            user_answer = q["answer"]
        elif mode == "all_wrong":
            wrong_options = [opt for opt in q["options"] if opt != q["answer"]]
            user_answer = wrong_options[0]
        elif mode == "random":
            user_answer = random.choice(q["options"])
        else:
            user_answer = q["answer"]

        is_correct = user_answer == q["answer"]

        st.session_state.answers.append(
            {
                "id": q["id"],
                "domain": q["domain"],
                "domain_label": q["domain_label"],
                "question": q["q"],
                "user_answer": user_answer,
                "correct_answer": q["answer"],
                "is_correct": is_correct,
                "weight": q["weight"],
                "expl": q["expl"],
                "elapsed_time": None,
                "time_limit": q.get("time_limit"),
                "is_timeout": False,
            }
        )

        if is_correct:
            st.session_state.raw_scores[q["domain"]] += q["weight"]

    st.session_state.started = True
    st.session_state.current_index = len(QUESTIONS) - 1
    st.session_state.finished = True
    st.session_state.question_start_time = None


def get_domain_max_scores(questions):
    max_scores = {domain: 0 for domain in DOMAINS}
    for q in questions:
        max_scores[q["domain"]] += q["weight"]
    return max_scores


def convert_domain_score(raw_score, mean_score, sd_score):
    raw_score = float(raw_score)
    mean_score = float(mean_score)
    sd_score = float(sd_score)

    if sd_score == 0:
        return 100

    z = (raw_score - mean_score) / sd_score
    index_score = round(100 + 15 * z)

    return max(55, min(145, int(index_score)))


def calc_fsiq(domain_indices):
    composite = (
        float(domain_indices["VCI"]) +
        float(domain_indices["PRI"]) +
        float(domain_indices["WMI"]) +
        float(domain_indices["PSI"])
    )

    mean_sum = 400.0
    sd_sum = 30.0

    z = (composite - mean_sum) / sd_sum
    fsiq = round(100 + 15 * z)

    return max(55, min(145, int(fsiq)))


def get_iq_band_comment(iq):
    if iq >= 130:
        return "非常に高い"
    if iq >= 120:
        return "高い"
    if iq >= 110:
        return "やや高い"
    if iq >= 90:
        return "平均域"
    if iq >= 80:
        return "やや低い"
    return "低い"


def get_domain_comment(domain, score):
    if domain == "VCI":
        if score >= 120:
            return "言語理解・語彙・抽象化が強い傾向があります。"
        elif score >= 100:
            return "言語理解はおおむね安定しています。"
        else:
            return "語彙や概念理解の問題で伸びしろがあります。"

    if domain == "PRI":
        if score >= 120:
            return "法則発見や非言語推理が強い傾向があります。"
        elif score >= 100:
            return "パターン認識は標準的です。"
        else:
            return "数列や規則発見を鍛える余地があります。"

    if domain == "WMI":
        if score >= 120:
            return "情報保持と脳内操作が得意です。"
        elif score >= 100:
            return "ワーキングメモリは標準的です。"
        else:
            return "頭の中での保持や並べ替え課題で伸びしろがあります。"

    if domain == "PSI":
        if score >= 120:
            return "視覚探索や単純処理の速さ・正確さが高いです。"
        elif score >= 100:
            return "処理速度は標準的です。"
        else:
            return "素早い比較や照合課題で伸びしろがあります。"

    return ""


def handle_timeout_submission(q, q_idx, total_questions):
    elapsed_time = time.time() - st.session_state.question_start_time
    time_limit = q.get("time_limit", 8)

    st.session_state.answers.append(
        {
            "id": q["id"],
            "domain": q["domain"],
            "domain_label": q["domain_label"],
            "question": q["q"],
            "user_answer": "時間切れ",
            "correct_answer": q["answer"],
            "is_correct": False,
            "weight": q["weight"],
            "expl": q["expl"],
            "elapsed_time": round(elapsed_time, 2),
            "time_limit": time_limit,
            "is_timeout": True,
        }
    )

    st.session_state.question_start_time = None

    if q_idx < total_questions - 1:
        st.session_state.current_index += 1
    else:
        st.session_state.finished = True

    st.rerun()


# =========================
# セッション初期化
# =========================
if "started" not in st.session_state:
    st.session_state.started = False

if "current_index" not in st.session_state:
    st.session_state.current_index = 0

if "answers" not in st.session_state:
    st.session_state.answers = []

if "raw_scores" not in st.session_state:
    st.session_state.raw_scores = {domain: 0 for domain in DOMAINS}

if "finished" not in st.session_state:
    st.session_state.finished = False

if "question_start_time" not in st.session_state:
    st.session_state.question_start_time = None


# =========================
# 開始画面
# =========================
if not st.session_state.started:
    st.title("🧠 WAIS風知能測定アプリ")
    st.subheader("4領域プロフィール版（32問）")

    st.write("""
このアプリでは、以下の4領域を簡易的に測定します。

- **VCI**：言語理解
- **PRI**：知覚推理
- **WMI**：ワーキングメモリ
- **PSI**：処理速度
""")

    st.warning("※ 本アプリは正式な臨床用知能検査ではありません。WAISを参考にした独自の簡易推定モデルです。")
    st.info("PSIのみ自動時間切れ対応です。")

    if st.button("開始する"):
        st.session_state.started = True
        st.session_state.question_start_time = None
        st.rerun()

    if DEBUG_MODE:
        st.write("---")
        st.subheader("デバッグ用ショートカット")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("全問正解で結果へ"):
                fill_debug_answers("all_correct")
                st.rerun()

        with col2:
            if st.button("全問不正解で結果へ"):
                fill_debug_answers("all_wrong")
                st.rerun()

        with col3:
            if st.button("ランダム回答で結果へ"):
                fill_debug_answers("random")
                st.rerun()

# =========================
# 問題画面
# =========================
elif not st.session_state.finished:
    q_idx = st.session_state.current_index
    q = QUESTIONS[q_idx]
    total_questions = len(QUESTIONS)

    if st.session_state.question_start_time is None:
        st.session_state.question_start_time = time.time()

    elapsed_time = time.time() - st.session_state.question_start_time
    is_psi = q["domain"] == "PSI"
    time_limit = q.get("time_limit", 20)
    remaining_time = max(0, int(time_limit - elapsed_time))

    st.title("📝 問題に回答してください")
    st.progress(q_idx / total_questions)

    st.caption(f"領域: {q['domain']} / {q['domain_label']}")
    st.subheader(f"問 {q_idx + 1} / {total_questions}")
    st.write(f"**問題タイプ:** {q['subtype']}")
    st.write(f"**難易度:** {q['difficulty']}")
    st.write(f"**配点:** {q['weight']}点")
    st.write("---")
    st.write(q["q"])

    if is_psi:
        st_autorefresh(interval=1000, limit=time_limit + 2, key=f"psi_timer_{q_idx}")
        st.warning(f"PSI制限時間: {time_limit} 秒")
        st.caption(f"残り時間: {remaining_time} 秒")
    else:
        st.caption("この問題は手動で次へ進みます。")

    choice = st.radio(
        "答えを選んでください",
        q["options"],
        index=None,
        key=f"question_{q_idx}"
    )

    if is_psi and elapsed_time >= time_limit:
        handle_timeout_submission(q, q_idx, total_questions)

    if st.button("次へ"):
        elapsed_time = time.time() - st.session_state.question_start_time
        is_timeout = is_psi and elapsed_time > time_limit

        if choice is None and not is_timeout:
            st.warning("回答を選んでください。")
        else:
            if is_timeout:
                user_answer = "時間切れ"
                is_correct = False
            else:
                user_answer = choice
                is_correct = choice == q["answer"]

            st.session_state.answers.append(
                {
                    "id": q["id"],
                    "domain": q["domain"],
                    "domain_label": q["domain_label"],
                    "question": q["q"],
                    "user_answer": user_answer,
                    "correct_answer": q["answer"],
                    "is_correct": is_correct,
                    "weight": q["weight"],
                    "expl": q["expl"],
                    "elapsed_time": round(elapsed_time, 2) if is_psi else None,
                    "time_limit": time_limit if is_psi else None,
                    "is_timeout": is_timeout,
                }
            )

            if is_correct:
                st.session_state.raw_scores[q["domain"]] += q["weight"]

            st.session_state.question_start_time = None

            if q_idx < total_questions - 1:
                st.session_state.current_index += 1
            else:
                st.session_state.finished = True

            st.rerun()

# =========================
# 結果画面
# =========================
else:
    st.balloons()
    st.title("🏁 測定完了")
    st.subheader("結果レポート")

    domain_max_scores = get_domain_max_scores(QUESTIONS)

    domain_indices = {}
    for domain in DOMAINS:
        raw_score = st.session_state.raw_scores[domain]
        mean_score = DOMAIN_NORMS[domain]["mean"]
        sd_score = DOMAIN_NORMS[domain]["sd"]

        domain_indices[domain] = convert_domain_score(
            raw_score,
            mean_score,
            sd_score
        )

    fsiq = calc_fsiq(domain_indices)
    band = get_iq_band_comment(fsiq)

    st.metric("総合推定IQ", f"{fsiq}")
    st.write(f"判定：**{band}**")

    st.write("---")
    st.subheader("4領域指数")

    for domain in DOMAINS:
        label = DOMAIN_LABELS[domain]
        raw = st.session_state.raw_scores[domain]
        raw_max = domain_max_scores[domain]
        index_score = domain_indices[domain]

        st.markdown(f"### {domain} / {label}")
        st.write(f"- 素点: **{raw} / {raw_max}**")
        st.write(f"- 領域指数: **{index_score}**")
        st.write(f"- コメント: {get_domain_comment(domain, index_score)}")

    strongest = max(domain_indices, key=domain_indices.get)
    weakest = min(domain_indices, key=domain_indices.get)

    st.write("---")
    st.subheader("認知プロフィールまとめ")
    st.write(f"- 最も高い領域: **{strongest} / {DOMAIN_LABELS[strongest]}**")
    st.write(f"- 最も低い領域: **{weakest} / {DOMAIN_LABELS[weakest]}**")

    st.write("---")
    st.subheader("答え合わせ")

    for i, ans in enumerate(st.session_state.answers, start=1):
        mark = "✅" if ans["is_correct"] else "❌"
        with st.expander(f"問{i} {mark} {ans['question'][:24]}..."):
            st.write(f"**領域:** {ans['domain']} / {ans['domain_label']}")
            st.write(f"**あなたの回答:** {ans['user_answer']}")
            st.write(f"**正解:** {ans['correct_answer']}")
            st.write(f"**配点:** {ans['weight']}点")

            if ans.get("elapsed_time") is not None:
                st.write(f"**回答時間:** {ans.get('elapsed_time')} 秒")
            if ans.get("time_limit") is not None:
                st.write(f"**制限時間:** {ans.get('time_limit')} 秒")
            if ans.get("is_timeout") is not None:
                st.write(f"**時間切れ:** {'はい' if ans.get('is_timeout') else 'いいえ'}")

            st.info(ans["expl"])

    st.write("---")
    if st.button("もう一度受ける"):
        st.session_state.started = False
        st.session_state.current_index = 0
        st.session_state.answers = []
        st.session_state.raw_scores = {domain: 0 for domain in DOMAINS}
        st.session_state.finished = False
        st.session_state.question_start_time = None
        st.rerun()
