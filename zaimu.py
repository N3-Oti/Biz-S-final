from arelle import Cntlr
import os
import configparser

# configparserを使用してiniファイルを読み込む
config = configparser.ConfigParser()
config.read('keys.ini')

# iniファイルからXBRLファイルのパスを取得
xbrl_file = config['FILE_PATH']['XBRL_FILE']

# Arelleのコントローラーオブジェクトを初期化し、XBRLファイルからデータを読み込む
ctrl = Cntlr.Cntlr(logFileName='logToPrint')
model_xbrl = ctrl.modelManager.load(xbrl_file)

# 変数の初期化
company_name = None
netsales = 0
risks = None
number_of_employees = 0

# forループを使ってXBRLに含まれる全てのFactを調査
# if文で特定の要素を抽出し、それぞれの変数に代入する
for fact in model_xbrl.facts:
    if fact.concept.qname.localName == "CompanyNameCoverPage":
        company_name = fact.value
    elif fact.concept.qname.localName == "NetSales":
        netsales = fact.value
    elif fact.concept.qname.localName == "NumberOfEmployees":
        if fact.context.id == "CurrentYearInstant":
            number_of_employees = fact.value
    elif fact.concept.qname.localName == "BusinessPolicyBusinessEnvironmentIssuesToAddressEtcTextBlock":
        business_policy = fact.value
    elif fact.concept.qname.localName == "BusinessRisksTextBlock":
        risks = fact.value
    elif fact.concept.qname.localName == "ManagementAnalysisOfFinancialPositionOperatingResultsAndCashFlowsTextBlock":
        management_analysis = fact.value
    elif fact.concept.qname.localName == "InformationAboutEmployeesTextBlock":
        information_about_employees = fact.value
    elif fact.concept.qname.localName == "ConstructionCompleted":
        construction_completed = fact.value

print("会社名：" + company_name)
print("売上高：" + netsales)
print("従業員数：" + number_of_employees)
print("一人当売上高：" + str(float(netsales) / float(number_of_employees)))
print("完成工事高：" + construction_completed)


#print("経営政策：" + business_policy)
#print("経営リスク：" + risks)
#print("経営分析：" + management_analysis)
#print("従業員情報：" + information_about_employees)

'''
# 言語処理部分
import os
import google.generativeai as genai

# iniファイルからAPIキーを取得
GEMINI_API_KEY = config['API']['GEMINI_API_KEY']
# APIキーを設定
genai.configure(api_key=GEMINI_API_KEY)

## 経営基本方針

# Create the model
generation_config = {
  "temperature": 0.5,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction="企業の経営方針、特に「中期経営計画2024」とそれに関連する取り組みに焦点を当て、経営改善点を見つけるための情報を抽出するプロンプト。\n\n抽出対象:\n\n経営理念と長期ビジョン: 企業の核となる価値観と、将来目指す姿を把握する。\n\n対処すべき課題: 現在直面している問題と、それに対する具体的な対策を特定する。\n\n特に土木・建築事業の業績悪化とその改善策に焦点を当てる。\n\n資本コストや株価に対する意識と、その改善に向けた取り組みを把握する。\n\n中期経営計画の進捗: 目標達成に向けた具体的な取り組みとその現状を把握する。\n\n「建設を『人』から『機械』へ」の取り組みとその進捗状況。\n\n「新たな事業領域を構築する」取り組みとその具体例。\n\n計数目標の見直しとその理由。\n\n推論の順序: まず、テキストから関連情報を抽出し、次にそれらの情報に基づいて経営改善点を推論する。\n結論の順序: 経営改善点の提案は、すべての情報抽出と推論の後に行う。\n\n経営方針分析プロンプト\n\n提供されたテキストから、企業の経営方針、特に「中期経営計画2024」とその関連情報、対処すべき課題を抽出し、経営改善点を見つけるための情報を整理してください。\n\n抽出項目\n\n経営理念と長期ビジョン:\n\n経営理念\n\n長期ビジョン（2030年までの目標）\n\n長期ビジョンで設定された社会課題\n\n対処すべき課題:\n\n経営環境の認識（経済全体、建設業界）\n\n土木・建築事業の業績に関する課題とその原因\n\n土木・建築事業の業績改善策\n\n体制整備\n\n管理体制の見直し\n\n現場管理の強化\n\n資本コストと株価に関する課題\n\n現状の認識（PBR、ROEなど）\n\n資本コストと株価に対する目標\n\n市場評価と資本収益性改善に向けた取り組み\n\n中期経営計画2024の進捗:\n\nミッション\n\n主要な取り組み\n\n「建設を『人』から『機械』へ」の具体策とその進捗\n\n機械化の具体策とその進捗\n\nDXの具体策とその進捗\n\n「新たな事業領域を構築する」具体策とその進捗\n\n新規事業の具体例\n\n第3の柱となる事業の具体例とその進捗\n\n計数目標の見直しとその理由\n\n見直しの背景\n\n見直された目標\n\n推論ステップ\n\n抽出された情報に基づき、以下の点を推論します。\n\n課題の深刻度: 各課題が経営に与える影響の大きさを評価します。\n\n対策の妥当性: 提示された対策が課題解決に効果的かどうかを評価します。\n\n目標達成の可能性: 中期経営計画の目標達成に向けた進捗状況と、残された課題を評価します。\n\n結論\n\n推論結果に基づき、経営改善点を具体的に提案します。改善点は、以下の観点を含めてください。\n\n戦略の妥当性: 長期ビジョンや中期経営計画の戦略が適切かどうかを評価し、必要に応じて修正案を提示します。\n\n実行体制の強化: 課題解決に向けた実行体制やリソース配分について、改善案を提示します。\n\nリスク管理の強化: 潜在的なリスクを洗い出し、それに対する予防策や対応策を提示します。\n\n新たな成長機会の探索: 既存事業の強化だけでなく、新たな成長機会を探るための提案を行います。\n\n出力フォーマット\n\nJSON形式で出力します。各抽出項目、推論結果、結論は以下のキーに格納します。\n\n{\n  \"経営理念と長期ビジョン\": {\n    \"経営理念\": \"[経営理念]\",\n    \"長期ビジョン\": \"[長期ビジョン]\",\n    \"社会課題\": \"[社会課題]\"\n  },\n  \"対処すべき課題\": {\n    \"経営環境\": {\n      \"経済全体\": \"[経済全体の認識]\",\n      \"建設業界\": \"[建設業界の認識]\"\n    },\n    \"土木・建築事業\": {\n      \"課題\": \"[課題]\",\n      \"原因\": \"[原因]\",\n      \"改善策\": {\n        \"体制整備\": \"[体制整備の内容]\",\n        \"管理体制の見直し\": \"[管理体制の見直しの内容]\",\n        \"現場管理の強化\": \"[現場管理の強化策]\"\n      }\n    },\n    \"資本コストと株価\": {\n      \"現状\": {\n        \"PBR\": \"[PBRの現状]\",\n        \"ROE\": \"[ROEの現状]\",\n        \"その他\": \"[その他の現状認識]\"\n      },\n      \"目標\": {\n        \"ROE\": \"[ROE目標]\",\n        \"その他\": \"[その他の目標]\"\n      },\n      \"取り組み\": \"[取り組み内容]\"\n    }\n  },\n  \"中期経営計画2024の進捗\": {\n    \"ミッション\": \"[ミッション]\",\n    \"主要な取り組み\": {\n      \"建設を『人』から『機械』へ\": {\n        \"機械化\": \"[機械化の具体策と進捗]\",\n        \"DX\": \"[DXの具体策と進捗]\"\n      },\n      \"新たな事業領域を構築する\": {\n          \"新規事業\": \"[新規事業の具体例]\",\n          \"第3の柱\": \"[第3の柱となる事業の具体例と進捗]\"\n      }\n    },\n    \"計数目標の見直し\": {\n        \"背景\": \"[見直しの背景]\",\n        \"目標\": \"[見直された目標]\"\n    }\n  },\n  \"推論\": {\n    \"課題の深刻度\": \"[各課題の深刻度の評価]\",\n    \"対策の妥当性\": \"[各対策の妥当性の評価]\",\n    \"目標達成の可能性\": \"[目標達成の可能性の評価]\"\n  },\n  \"結論\": {\n      \"戦略の妥当性\": \"[戦略の妥当性の評価と修正案]\",\n      \"実行体制の強化\": \"[実行体制とリソース配分の改善案]\",\n      \"リスク管理の強化\": \"[リスクに対する予防策と対応策]\",\n      \"新たな成長機会の探索\": \"[新たな成長機会の提案]\"\n  }\n}\ncontent_copy\nUse code with caution.\nJSON\nExamples\n\n入力:\n[提供されたテキストデータ] (例: 上記の１【経営方針、経営環境及び対処すべき課題等】のテキストデータ)\n\n出力:\n\n{\n  \"経営理念と長期ビジョン\": {\n    \"経営理念\": \"わが社はもっと豊かな社会づくりに貢献する\",\n    \"長期ビジョン\": \"社会課題を解決する『先端の建設企業』\",\n    \"社会課題\": [\"気候変動問題\", \"2030年問題\"]\n  },\n  \"対処すべき課題\": {\n    \"経営環境\": {\n      \"経済全体\": \"雇用・所得環境の改善、各種政策の効果により景気は回復傾向。ただし、海外景気の下振れリスクあり。\",\n      \"建設業界\": \"公共投資、民間設備投資により受注環境は底堅いが、資材価格高騰、労務需給逼迫による厳しい事業環境。\"\n    },\n    \"土木・建築事業\": {\n      \"課題\": \"大型建設工事での赤字発生による業績低迷\",\n      \"原因\": \"資機材調達遅れ、品質不良、材料費・労務費高騰\",\n      \"改善策\": {\n        \"体制整備\": \"業績管理対策本部設置\",\n        \"管理体制の見直し\": \"施工支援・技術指導部署新設、業務プロセス見直し、管理基準平準化\",\n        \"現場管理の強化\": \"重点管理現場の工程・原価進捗モニタリング強化\"\n      }\n    },\n    \"資本コストと株価\": {\n      \"現状\": {\n        \"PBR\": \"1倍を下回る\",\n        \"ROE\": \"低下傾向\",\n        \"その他\": \"成長戦略の提示不足\"\n      },\n      \"目標\": {\n        \"ROE\": \"2030年に10%以上\",\n          \"その他\": \"株主資本コスト6.0%程度\"\n      },\n      \"取り組み\": \"安定性・収益性・将来性・関係性の観点から市場評価と資本収益性の改善\"\n    }\n  },\n  \"中期経営計画2024の進捗\": {\n    \"ミッション\": \"『独自の強み』を創る\",\n    \"主要な取り組み\": {\n      \"建設を『人』から『機械』へ\": {\n        \"機械化\": \"自動化施工システム導入、自走型破砕\ncontent_copy\nUse code with caution.\nJson",
)

chat_session = model.start_chat(
  history=[
  ]
)

response_business_policy = chat_session.send_message(business_policy)

print(response_business_policy.text)

#　リスク分析

# Create the model
generation_config = {
  "temperature": 0.5,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction="指定された経営リスクに関する記述から、企業の経営方針分析に必要なデータを抽出します。\n\nSteps\n\n各リスク項目を特定する。\n\n各リスク項目に対する企業の対応策や取り組みを抽出する。\n\n抽出した情報を整理し、経営方針の分析に役立つデータとしてまとめる。\n\nOutput Format\n\n抽出したデータはJSON形式で出力します。各リスク項目をキーとし、その対応策や取り組みを値とします。\n\nExamples\n\nInput:\n\n(1) 事業環境について\n①建設市場の動向\n国内外の景気後退や国及び地方公共団体の公共投資予算の削減等により、建設市場が著しく縮小した場合や今後競合他社との競争が激化し、民間工事における受注価格が下落する場合には、当社グループの業績に影響を及ぼす可能性があります。\nこのリスクに対応するため、建設事業においては、ICT施工やDX戦略による省力化技術の確立により、市場の縮小にも柔軟に対応できる事業体質の構築に取り組んでおります。不動産開発事業・再生可能エネルギー事業を主とする関連事業による安定収益の拡大にも引き続き注力しており、直近３ヵ年においては当社利益の中核となっております。また、今後のさらなる市況の変化に備えR&D及び新規事業への投資も強化しており、持続的な成長を可能とする収益基盤の変革を推進してまいります。\n\nOutput:\n\n{\n  \"事業環境\": {\n    \"建設市場の動向\": {\n      \"リスク\": \"国内外の景気後退や公共投資予算の削減等による建設市場の縮小、競合他社との競争激化による受注価格の下落。\",\n      \"対応策\": \"ICT施工やDX戦略による省力化技術の確立、関連事業による安定収益の拡大、R&D及び新規事業への投資強化。\"\n    }\n  }\n}\ncontent_copy\nUse code with caution.\nJson\nNotes\n\nリスク項目は 複数の大項目があり、それぞれに小項目が存在する場合があります。\n対応策は各リスクに対する企業の具体的な取り組みを記述しています。",
)

chat_session = model.start_chat(
  history=[
  ]
)

response_risks = chat_session.send_message(risks)

print(response_risks.text)

# 経営分析

# Create the model
generation_config = {
  "temperature": 0.5,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction="与えられた経営分析テキストから、企業の財政状態、経営成績、キャッシュフローの状況を抽出し、構造化されたJSON形式で出力するプロンプトを作成します。\n\n経営分析テキストから、以下の情報を抽出し、JSON形式で出力してください。\n\n当期の経営成績：売上高、売上総利益（損失）、営業利益（損失）、経常利益（損失）、親会社株主に帰属する当期純利益（損失）とその増減率\n\nセグメント別経営成績：各セグメント（土木事業、建築事業、関連事業）の売上高とその増減率、セグメント利益（損失）\n\n地域別業績：各地域（日本、アジアなど）の売上高と営業利益（損失）\n\n受注実績：各セグメントの当期受注高、前期受注高、受注残高\n\nSteps\n\nテキストから当期の経営成績に関する情報を抽出します。\n\nテキストからセグメント別の経営成績に関する情報を抽出します。\n\nテキストから地域別の業績に関する情報を抽出します。\n\nテキストから受注実績に関する情報を抽出します。\n\n抽出した情報をJSON形式に変換します。\n\nOutput Format\n\nJSON形式で出力します。各数値は[数値]百万円の形式で記述し、増減率は%で記述します。\n\n{\n  \"経営成績\": {\n    \"売上高\": \"[数値]百万円\",\n    \"売上高増減率\": \"[数値]%\",\n    \"売上総利益\": \"[数値]百万円\",\n    \"営業利益\": \"[数値]百万円\",\n    \"経常利益\": \"[数値]百万円\",\n    \"親会社株主に帰属する当期純利益\": \"[数値]百万円\"\n  },\n  \"セグメント別経営成績\": {\n    \"土木事業\": {\n      \"売上高\": \"[数値]百万円\",\n      \"売上高増減率\": \"[数値]%\",\n      \"セグメント利益\": \"[数値]百万円\"\n    },\n    \"建築事業\": {\n      \"売上高\": \"[数値]百万円\",\n      \"売上高増減率\": \"[数値]%\",\n      \"セグメント利益\": \"[数値]百万円\"\n    },\n    \"関連事業\": {\n      \"売上高\": \"[数値]百万円\",\n      \"売上高増減率\": \"[数値]%\",\n      \"セグメント利益\": \"[数値]百万円\"\n    }\n  },\n  \"地域別業績\": {\n    \"日本\": {\n      \"売上高\": \"[数値]百万円\",\n      \"営業利益\": \"[数値]百万円\"\n    },\n    \"アジア\": {\n      \"売上高\": \"[数値]百万円\",\n      \"営業利益\": \"[数値]百万円\"\n    },\n   \"その他地域\": {\n      \"売上高\": \"[数値]百万円\",\n      \"営業利益\": \"[数値]百万円\"\n    }\n  },\n  \"受注実績\": {\n    \"土木事業\": {\n      \"当期受注高\": \"[数値]百万円\",\n      \"前期受注高\": \"[数値]百万円\",\n      \"受注残高\": \"[数値]百万円\"\n    },\n    \"建築事業\": {\n      \"当期受注高\": \"[数値]百万円\",\n      \"前期受注高\": \"[数値]百万円\",\n      \"受注残高\": \"[数値]百万円\"\n    },\n    \"関連事業\": {\n      \"当期受注高\": \"[数値]百万円\",\n      \"前期受注高\": \"[数値]百万円\",\n      \"受注残高\": \"[数値]百万円\"\n    }\n  }\n}\ncontent_copy\nUse code with caution.\nJson\n",
)

chat_session = model.start_chat(
  history=[
  ]
)

response_management_analysis = chat_session.send_message(management_analysis)   

print(response_management_analysis.text)

# 従業員情報

# Create the model
generation_config = {
  "temperature": 0.5,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction="与えられた従業員情報を分析に適したJSON形式に変換する。\n\nSteps\n\n従業員状況（連結会社）の抽出と整形:\n\nセグメントごとの従業員数（正社員と臨時従業員）を抽出する。\n\n数値を文字列ではなく数値として解釈する。\n\n従業員状況（提出会社）の抽出と整形:\n\n従業員数、平均年齢、平均勤続年数、平均年間給与を抽出する。\n\n数値を文字列ではなく数値として解釈する。\n\n注釈情報の抽出:\n\n従業員数に関する注釈（就業人員の定義、臨時従業員の定義、再雇用社員数、契約社員数）を抽出する。\n\nJSON 形式への変換:\n\n抽出した情報をJSON構造にマッピングする。\n\n連結会社情報は、セグメント名をキーとし、従業員数と臨時従業員数を値とするオブジェクトの配列にする。\n\n提出会社情報は、従業員数、平均年齢、平均勤続年数、平均年間給与をキーとするオブジェクトにする。\n\n注釈情報は、注釈番号をキーとし、注釈内容を値とするオブジェクトにする。\n\nOutput Format\n\n出力は以下の形式のJSONとする。\n\n{\n  \"連結会社\": {\n    \"日付\": \"[日付]\",\n    \"従業員状況\": [\n      {\n        \"セグメント\": \"[セグメント名]\",\n        \"従業員数\": [従業員数],\n        \"臨時従業員数\": [臨時従業員数]\n      },\n      {\n        \"セグメント\": \"[セグメント名]\",\n        \"従業員数\": [従業員数],\n        \"臨時従業員数\": [臨時従業員数]\n      },\n      ...\n    ],\n    \"合計\": {\n         \"従業員数\": [従業員数の合計],\n         \"臨時従業員数\": [臨時従業員数の合計]\n    }\n  },\n  \"提出会社\": {\n    \"日付\": \"[日付]\",\n    \"従業員数\": [従業員数],\n    \"平均年齢\": [平均年齢],\n    \"平均勤続年数\": [平均勤続年数],\n    \"平均年間給与\": [平均年間給与]\n  },\n   \"注釈\": {\n    \"1\": \"[注釈1の内容]\",\n    \"2\": \"[注釈2の内容]\",\n    \"3\": \"[注釈3の内容]\",\n    \"4\": \"[注釈4の内容]\"\n     }\n}\ncontent_copy\nUse code with caution.\nJson",
)

chat_session = model.start_chat(
  history=[
  ]
)

response_employee_information = chat_session.send_message(employee_information)

print(response_employee_information.text)
'''