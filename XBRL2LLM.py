import os
import configparser
from arelle import Cntlr
from bs4 import BeautifulSoup
import re

# iniファイルの読み込み
config = configparser.ConfigParser()
config.read('keys.ini')

yearly_data = {
    2024: {  # 年をキーとして使用する
        '売上高': 0, '売上原価': 0, '販売費及び一般管理費': 0, '営業利益': 0, '従業員数': 0,
        '平均年間給与': 0, '売上総利益': 0, '売上総利益率': 0, '売上高営業利益率': 0,
        '短期借入金': 0, '長期借入金': 0, '総資産': 0, '純資産': 0, '自己資本比率': 0,
        '流動資産': 0, '流動負債': 0, '流動比率': 0, '完成工事高': 0, '完成工事原価': 0,
        '未成工事支出金': 0, '未成工事受入金': 0, '一人当たり売上高': 0, '一人当たり人件費': 0,
        '役員報酬': 0, '経営方針': "", '経営環境及び対処すべき課題': "", '経営上のリスク': "", '従業員情報': ""
    }
}

"""
# 処理する年のリストを作成
years = list(range(2015, 2025))  # 2015年から2024年まで
years.reverse() # 降順にソート

# 全ての年の結果を格納するリスト
all_results = []

# 各年のデータを保持する辞書
yearly_data = {}
for year in range(2015, 2025):
    yearly_data[year] = {  # 年をキーとして使用する
        '売上高': 0, '売上原価': 0, '販売費及び一般管理費': 0, '営業利益': 0, '従業員数': 0,
        '平均年間給与': 0, '売上総利益': 0, '売上総利益率': 0, '売上高営業利益率': 0,
        '短期借入金': 0, '長期借入金': 0, '総資産': 0, '純資産': 0, '自己資本比率': 0,
        '流動資産': 0, '流動負債': 0, '流動比率': 0, '完成工事高': 0, '完成工事原価': 0,
        '未成工事支出金': 0, '未成工事受入金': 0, '一人当たり売上高': 0, '一人当たり人件費': 0,
        '役員報酬': 0, '経営方針': "", '経営環境及び対処すべき課題': "", '経営上のリスク': "", '従業員情報': ""
    }
"""

def load_xbrl_file(file_path):
    ctrl = Cntlr.Cntlr(logFileName='logToPrint')
    try:
        model_xbrl = ctrl.modelManager.load(file_path)
        return model_xbrl
    except Exception as e:
        print(f"ファイルの読み込みに失敗しました。: {file_path}: {e}")
        return None

#"""  
# 2024年のみ
year = 2024
xbrl_file = config['FILE_PATH'][f'XBRL_FILE_{year}']
model_xbrl = load_xbrl_file(xbrl_file)
if model_xbrl is None:
    exit()
#"""

"""
# ループ処理
for year in years:
    xbrl_file = config['FILE_PATH'][f'XBRL_FILE_{year}']
    model_xbrl = load_xbrl_file(xbrl_file)
    if model_xbrl is None:
        continue
"""

data = yearly_data[year]  # 年をキーとしてデータを取得
processed_contexts = set()

for fact in model_xbrl.facts:
    key = fact.concept.qname.localName  # key=要素ID
    if key == "NetSalesSummaryOfBusinessResults" and fact.context.id == "CurrentYearDuration_NonConsolidatedMember":
        data['売上高'] += int(fact.value) if fact.value else 0
    elif key == "CostOfSales" and "CurrentYearDuration_NonConsolidatedMember" in fact.context.id:
        data['売上原価'] += int(fact.value) if fact.value else 0
    elif key == "SellingGeneralAndAdministrativeExpenses" and "CurrentYearDuration" in fact.context.id:
        data['販売費及び一般管理費'] += int(fact.value) if fact.value else 0
    elif key == "OperatingIncome" and "CurrentYearDuration_NonConsolidatedMember" in fact.context.id:
        data['営業利益'] += int(fact.value) if fact.value else 0
    elif key == "NumberOfEmployees" and fact.context.id == "CurrentYearInstant" and fact.context.id not in processed_contexts:
        data['従業員数'] += int(fact.value) if fact.value else 0
        processed_contexts.add(fact.context.id) # context.id を集合に追加
    elif key == "AverageAnnualSalaryInformationAboutReportingCompanyInformationAboutEmployees" and fact.context.id == "CurrentYearInstant_NonConsolidatedMember" in fact.context.id:
        data['平均年間給与'] += int(fact.value) if fact.value else 0
    elif key == "ShortTermLoansPayable" and "CurrentYearInstant" in fact.context.id:
        data['短期借入金'] += int(fact.value) if fact.value else 0
    elif key == "LongTermLoansPayable" and "CurrentYearInstant" in fact.context.id:
        data['長期借入金'] += int(fact.value) if fact.value else 0
    elif key == "TotalAssetsSummaryOfBusinessResults" and "CurrentYearInstant" in fact.context.id:
        data['総資産'] += int(fact.value) if fact.value else 0
    elif key == "NetAssetsSummaryOfBusinessResults" and "CurrentYearInstant" in fact.context.id:
        data['純資産'] += int(fact.value) if fact.value else 0
    elif key == "CurrentAssets" and "CurrentYearInstant" in fact.context.id:
        data['流動資産'] += int(fact.value) if fact.value else 0
    elif key == "CurrentLiabilities" and "CurrentYearInstant" in fact.context.id:
        data['流動負債'] += int(fact.value) if fact.value else 0
    elif key == "NetSalesOfCompletedConstructionContractsCNS" and "CurrentYearDuration" in fact.context.id:
        data['完成工事高'] += int(fact.value) if fact.value else 0
    elif key == "CostOfSalesOfCompletedConstructionContractsCNS" and "CurrentYearDuration" in fact.context.id:
        data['完成工事原価'] += int(fact.value) if fact.value else 0
    elif key == "CostsOnUncompletedConstructionContractsCNS" and "CurrentYearInstant" in fact.context.id:
        data['未成工事支出金'] += int(fact.value) if fact.value else 0
    elif key == "AdvancesReceivedOnUncompletedConstructionContractsCNS" and "CurrentYearInstant" in fact.context.id:
        data['未成工事受入金'] += int(fact.value) if fact.value else 0
    elif key == "DirectorsCompensationsSGA" and "CurrentYearDuration" in fact.context.id:
        data['役員報酬'] += int(fact.value) if fact.value else 0
    # テキスト部
#'''    
    elif fact.concept.qname.localName == "BusinessPolicyBusinessEnvironmentIssuesToAddressEtcTextBlock":
        data['経営方針'] = fact.value if fact.value else ""
        business_policy = fact.value
    elif fact.concept.qname.localName == "BusinessRisksTextBlock":
        data['経営上のリスク'] = fact.value if fact.value else ""
        business_risks = fact.value
    elif fact.concept.qname.localName == "ManagementAnalysisOfFinancialPositionOperatingResultsAndCashFlowsTextBlock":
        data['経営分析'] = fact.value if fact.value else ""  
        management_analysis = fact.value
    elif fact.concept.qname.localName == "InformationAboutEmployeesTextBlock":
        data['従業員情報'] = fact.value if fact.value else ""
        employee_information = fact.value
#'''
'''
        elif key == "BusinessPolicy" and "CurrentYearInstant" in fact.context.id:
            print(fact.value)
            # BeautifulSoupを使ってHTMLタグを除去
            soup = BeautifulSoup(fact.value, "html.parser")
            BusinessPolicy_cleaned = soup.get_text()
            print(BusinessPolicy_cleaned)
            # 空白や改行を取り除く
            BusinessPolicy_cleaned = re.sub(r'\s+', ' ', BusinessPolicy_cleaned).strip()
            data['経営方針'] = BusinessPolicy_cleaned if BusinessPolicy_cleaned else ""
        elif key == "BusinessEnvironmentAndIssuesToBeAddressed" and "CurrentYearInstant" in fact.context.id:
            soup = BeautifulSoup(fact.value, "html.parser")
            BusinessEnvironmentAndIssuesToBeAddressed_cleaned = soup.get_text()
            BusinessEnvironmentAndIssuesToBeAddressed_cleaned = re.sub(r'\s+', ' ', BusinessEnvironmentAndIssuesToBeAddressed_cleaned).strip()
            data['経営環境及び対処すべき課題'] = BusinessEnvironmentAndIssuesToBeAddressed_cleaned if BusinessEnvironmentAndIssuesToBeAddressed_cleaned else ""
        elif key == "BusinessRisksTextBlock" and "CurrentYearInstant" in fact.context.id:
            soup = BeautifulSoup(fact.value, "html.parser")
            BusinessRisksTextBlock_cleaned = soup.get_text()
            BusinessRisksTextBlock_cleaned = re.sub(r'\s+', ' ', BusinessRisksTextBlock_cleaned).strip()
            data['経営上のリスク'] = BusinessRisksTextBlock_cleaned if BusinessRisksTextBlock_cleaned else ""
        elif key == "InformationAboutEmployeesTextBlock" and "CurrentYearInstant" in fact.context.id:
            soup = BeautifulSoup(fact.value, "html.parser")
            InformationAboutEmployeesTextBlock_cleaned = soup.get_text()
            InformationAboutEmployeesTextBlock_cleaned = re.sub(r'\s+', ' ', InformationAboutEmployeesTextBlock_cleaned).strip()
            data['従業員情報'] = InformationAboutEmployeesTextBlock_cleaned if InformationAboutEmployeesTextBlock_cleaned else ""
'''

# 計算
if data['売上高'] > 0:
    data['売上総利益'] = data['売上高'] - data['売上原価']
    data['売上総利益率'] = (data['売上総利益'] / data['売上高']) * 100
    data['売上高営業利益率'] = (data['営業利益'] / data['売上高']) * 100

if data['従業員数'] > 0:
    data['一人当たり売上高'] = data['売上高'] / data['従業員数']
    if data['平均年間給与'] + data['役員報酬'] > 0:
        data['一人当たり人件費'] = (data['平均年間給与'] * data['従業員数'] + data['役員報酬']) / data['従業員数']

if data['総資産'] > 0:
    data['自己資本比率'] = (data['純資産'] / data['総資産']) * 100

if data['流動負債'] > 0:
    data['流動比率'] = data['流動資産'] / data['流動負債']

# 結果の出力
#print(f"{year}年 ({xbrl_file}) の分析結果: {data}")


#'''

# 言語処理部分
import os
import google.generativeai as genai

# iniファイルからAPIキーを取得
GEMINI_API_KEY = config['API']['GEMINI_API_KEY']
# APIキーを設定
genai.configure(api_key=GEMINI_API_KEY)

## 財務分析

# 既存のdata辞書をpartsキーを持つ形式に変換
formatted_data = {
    "parts": [
        {
            "text": f"売上高: {data['売上高']}\n"
                     f"売上原価: {data['売上原価']}\n"
                     f"販売費及び一般管理費: {data['販売費及び一般管理費']}\n"
                     f"営業利益: {data['営業利益']}\n"
                     f"従業員数: {data['従業員数']}\n"
                     f"平均年間給与: {data['平均年間給与']}\n"
                     f"売上総利益: {data['売上総利益']}\n"
                     f"売上総利益率: {data['売上総利益率']}\n"
                     f"売上高営業利益率: {data['売上高営業利益率']}\n"
                     f"短期借入金: {data['短期借入金']}\n"
                     f"長期借入金: {data['長期借入金']}\n"
                     f"総資産: {data['総資産']}\n"
                     f"純資産: {data['純資産']}\n"
                     f"自己資本比率: {data['自己資本比率']}\n"
                     f"流動資産: {data['流動資産']}\n"
                     f"流動負債: {data['流動負債']}\n"
                     f"流動比率: {data['流動比率']}\n"
                     f"完成工事高: {data['完成工事高']}\n"
                     f"完成工事原価: {data['完成工事原価']}\n"
                     f"未成工事支出金: {data['未成工事支出金']}\n"
                     f"未成工事受入金: {data['未成工事受入金']}\n"
                     f"一人当たり売上高: {data['一人当たり売上高']}\n"
                     f"一人当たり人件費: {data['一人当たり人件費']}\n"
                     f"役員報酬: {data['役員報酬']}"
        }
    ]
}

# Create the model
generation_config = {
  "temperature": 0.2,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction="与えられた財務データを一覧化した後、XBRLから抽出された財務データを用いて、企業の流動性、収益性、安全性、成長性を分析してください。データが存在する場合、主要な財務指標を用いて過去3年間のデータと比較してトレンドを分析してください。異常値があれば指摘し、その原因を考察してください。結論として、企業の財務状況の健全性についてまとめてください。",
)

chat_session = model.start_chat(
  history=[
  ]
)

response_data = chat_session.send_message(formatted_data)

print(f"\n\n[[財務分析]]\n\n {response_data.text}")

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
  system_instruction="提供されたデータ（経営方針、戦略説明など）を分析し、主要な方針や目標を特定してください。財務データと経営方針の整合性を評価し、実現可能性を考察してください。経営方針の強みと弱み、リスクを分析してください。\n\n入力データ\n経営方針に関するテキストデータ\n\n関連する財務データ（XBRLから抽出）\n\n出力形式\n経営方針の主要なポイント\n\n財務データとの整合性分析\n\n経営方針の評価（強み、弱み、リスク）\n\n注意点\nテキストデータから重要な情報を正確に抽出してください。\n\n財務データと経営方針の関連性を論理的に説明してください。\n\n現実的かつ具体的な評価を行ってください。",
)

chat_session = model.start_chat(
  history=[
  ]
)
response_business_policy = chat_session.send_message(f"[財務状況]{formatted_data}\n\n[経営基本方針]{business_policy}")

print(f"\n\n[[経営基本方針]]\n\n {response_business_policy.text}")

# リスク分析

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
  system_instruction="提供された情報（リスク分析に関するテキスト、財務データ）から潜在的なリスク要因を特定してください。各リスク要因の影響度と発生可能性を財務データとの関連を含めて評価してください。リスク対策の提案を行ってください。\n\n入力データ\nリスクに関連するテキストデータ\n財務データ\n\n出力形式\n特定されたリスク要因\n\nリスクの評価（影響度、発生可能性）\n\nリスク対策の提案\n\n注意点\n多角的な視点からリスクを洗い出してください。\n\n評価基準を明確にし、客観的な評価を行ってください。\n\n実効性の高いリスク対策を提案してください。",
)

chat_session = model.start_chat(
  history=[
  ]
)

response_risks = chat_session.send_message(f"[財務状況]{formatted_data}\n\n[リスク分析]{business_risks}")

print(f"\n\n[[リスク分析]]\n\n {response_risks.text}")

# 経営環境分析

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
  system_instruction="与えられた経営環境に関するデータと財務データ（市場動向、競合状況、法規制など）の情報を分析してください。経営環境が企業に与える影響を財務データも参考にしつつ評価してください。経営戦略への示唆を提供してください。\n\n入力データ\n経営環境に関するテキストデータ\n\n関連する財務データ\n\n出力形式\n環境の主要な特徴\n\n企業への影響評価\n\n経営戦略への示唆\n\n注意点\n多面的かつ詳細な分析を行ってください。\n\n実践的な示唆を提供してください。",
)

chat_session = model.start_chat(
  history=[
  ]
)

response_management_analysis = chat_session.send_message(f"[財務状況]{formatted_data}\n\n[経営環境分析]{management_analysis}")   

print(f"\n\n[[経営環境分析]]\n\n {response_management_analysis.text}")

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
  system_instruction="従業員数、平均給与、離職率などについて企業がまとめ発表したデータや財務データから従業員状況を分析してください。従業員の生産性や満足度を評価してください。人材管理の課題と改善策を提案してください。\n\n入力データ\n従業員に関するデータ（従業員数、平均給与、離職率など）\n\n出力形式\n従業員状況の分析結果\n\n生産性や満足度の評価\n\n人材管理の課題と改善策\n\n注意点\n多角的な視点から分析を行ってください。\n\n具体的な改善策を提案してください。",
)

chat_session = model.start_chat(
  history=[
  ]
)

response_employee_information = chat_session.send_message(f"[財務状況]{formatted_data}\n\n[従業員情報]{employee_information}")

print(f"\n\n[[従業員情報]]\n\n {response_employee_information.text}")

# 総合分析

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
#  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction="与えられた「財務状況」、「財務分析」、「経営方針分析」、「リスク分析」、「経営環境分析」、「従業員情報」の各分析者の分析結果報告に基づき、総合的な経営判断と改善提言を行ってください。各部門の分析を統合し、短期、中期、長期の戦略に分けて提言します。\n\nステップ\n\n各分析者の報告内容を詳細に検討し、主要な問題点と強みを特定します。\n\n各分析結果間の関連性と矛盾点を洗い出し、総合的な視点から分析します。\n\n特定された問題点に対し、「なぜ」を繰り返し問い、根本原因を追求します。\n\n短期、中期、長期の戦略を策定し、具体的な改善策を提案します。\n\n提案する改善策が企業にどのような利益をもたらすかを明確に説明します。\n\nアウトプットフォーマット\n総合経営判断\n\n[総合的な経営判断を記述。例: 企業の現状評価、主要な課題と強み]\n\n改善提言\n短期戦略 (1年以内)\n\n[具体的な改善策とその実施計画。例: コスト削減、業務効率化]\n\n中期戦略 (1-3年)\n\n[成長戦略と組織改革。例: 新市場開拓、人材育成]\n\n長期戦略 (3年以上)\n\n[持続的成長のための戦略。例: 技術革新、企業文化の醸成]\n\n結論\n\n[総合的な結論と最終的な提言。例: 企業が目指すべき方向性]\n\n例\n総合経営判断\n\n財務分析では流動比率の低下が見られ、資金繰りに課題があると判断します。[財務状況]の報告によると、売上は安定しているものの、営業キャッシュフローの減少が懸念されます。経営方針分析では、新規事業への投資が積極的ですが、[リスク分析]によると市場リスクの評価が不十分です。従業員情報からは、離職率の上昇が確認され、[経営環境分析]では競合他社の動向が企業に影響を与えていることが示されています。\n\n改善提言\n短期戦略 (1年以内)\n\nまず、資金繰りの改善を目指し、在庫管理の最適化と売掛金の回収期間短縮を実施します。(実際には、具体的な数値目標と実施手順を含める必要があります)\n\n中期戦略 (1-3年)\n\n新規事業のリスク管理体制を強化し、市場調査とリスク評価を徹底します。また、従業員のスキルアップとモチベーション向上のための研修プログラムを導入します。\n\n長期戦略 (3年以上)\n\n持続的な成長を目指し、技術革新への投資を拡大します。特に、デジタル技術を活用した業務効率化と新サービス開発に注力します。企業文化の改革を進め、従業員が働きやすい環境を整備することで、長期的な成長基盤を構築します。\n\n結論\n\n企業が持続的な成長を遂げるためには、短期的な資金繰りの改善だけでなく、中長期的な視点での戦略的な取り組みが必要です。特に、リスク管理の強化と人材育成、技術革新への投資が重要となります。\n（各分析は実際にはもっと長く詳細な物となります）",
)

chat_session = model.start_chat(
  history=[
  ]
)

response = chat_session.send_message(f"[財務状況]{formatted_data}\n[財務分析]{response_data}\n[経営基本方針]{response_business_policy}\n[リスク分析]{response_risks}\n[経営環境分析]{response_management_analysis}\n[従業員情報]{response_employee_information}")

print(f"\n\n[[総合分析]]\n\n {response.text}")

#'''

'''
# 各年の結果を辞書として保存
year_result = {
    "year": year,
    "data": data,
    "financial_analysis": response_data, # Geminiからの財務分析結果
    "business_policy": response_business_policy, # Geminiからの経営基本方針結果
    "risk_analysis": response_risks, # Geminiからのリスク分析結果
    "management_analysis": response_management_analysis, # Geminiからの経営環境分析結果
    "employee_information": response_employee_information # Geminiからの従業員情報結果
    }
all_results.append(year_result)

# 全ての年の処理が完了したら、all_results を使用して統合処理を行う
combined_financial_data = {}
for result in all_results:
    for key, value in result['data'].items():
        combined_financial_data[key] = combined_financial_data.get(key, 0) + value

print("全ての年の財務データを統合しました:", combined_financial_data)
'''