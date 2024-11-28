import os
import configparser
from arelle import Cntlr
from bs4 import BeautifulSoup
import re

# iniファイルの読み込み
config = configparser.ConfigParser()
config.read('keys.ini')

# XBRLファイルのパスを取得 (複数年対応)
xbrl_files = {}
for year in range(2015, 2025):  # 2014年から2024年まで
    key = f'XBRL_FILE_{year}'
    if key in config['FILE_PATH']:
        xbrl_files[year] = config['FILE_PATH'][key]

# 各年のデータを保持する辞書  リストではなく辞書に変更
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


def load_xbrl_file(file_path):
    ctrl = Cntlr.Cntlr(logFileName='logToPrint')
    try:
        model_xbrl = ctrl.modelManager.load(file_path)
        return model_xbrl
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

# 各XBRLファイルを処理
for year, xbrl_file in xbrl_files.items():  # 年をキーとして使用する
    model_xbrl = load_xbrl_file(xbrl_file)
    if model_xbrl is None:
        continue

    data = yearly_data[year]  # 年をキーとしてデータを取得
    # XBRLデータの抽出
    for fact in model_xbrl.facts:
        key = fact.concept.qname.localName  # 要素IDの取得
        if key == "NetSales" and "CurrentYearDuration" in fact.context.id:
            data['売上高'] += int(fact.value) if fact.value else 0
        elif key == "CostOfSales" and "CurrentYearDuration" in fact.context.id:
            data['売上原価'] += int(fact.value) if fact.value else 0
        elif key == "SellingGeneralAndAdministrativeExpenses" and "CurrentYearDuration" in fact.context.id:
            data['販売費及び一般管理費'] += int(fact.value) if fact.value else 0
        elif key == "OperatingIncome" and "CurrentYearDuration" in fact.context.id:
            data['営業利益'] += int(fact.value) if fact.value else 0
        elif key == "NumberOfEmployees" and "CurrentYearInstant" in fact.context.id:
            data['従業員数'] += int(fact.value) if fact.value else 0
        elif key == "AverageAnnualSalaryInformationAboutReportingCompanyInformationAboutEmployees" and "CurrentYearInstant" in fact.context.id:
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
        elif fact.concept.qname.localName == "BusinessPolicyBusinessEnvironmentIssuesToAddressEtcTextBlock":
            data['経営方針'] = fact.value if fact.value else ""
        elif fact.concept.qname.localName == "BusinessRisksTextBlock":
            data['経営上のリスク'] = fact.value if fact.value else ""
        elif fact.concept.qname.localName == "ManagementAnalysisOfFinancialPositionOperatingResultsAndCashFlowsTextBlock":
            data['経営分析'] = fact.value if fact.value else ""  
        elif fact.concept.qname.localName == "InformationAboutEmployeesTextBlock":
            data['従業員情報'] = fact.value if fact.value else ""

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
    if data['販売費及び一般管理費'] + data['役員報酬'] > 0:
        data['一人当たり人件費'] = (data['販売費及び一般管理費'] + data['役員報酬']) / data['従業員数']

if data['総資産'] > 0:
    data['自己資本比率'] = (data['純資産'] / data['総資産']) * 100

if data['流動負債'] > 0:
    data['流動比率'] = data['流動資産'] / data['流動負債']

    # 結果の出力
print(f"{year}年 ({xbrl_file}) の分析結果: {data}")


'''

# 言語処理部分
import os
import google.generativeai as genai

# iniファイルからAPIキーを取得
GEMINI_API_KEY = config['API']['GEMINI_API_KEY']
# APIキーを設定
genai.configure(api_key=GEMINI_API_KEY)

## 各種数値分析

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
  "temperature": 0.5,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction="与えられた財務データに基づき、企業のその年の財務状況を分析し、整理し、改善点を指摘します。\n\n# 手順\n\n1. データの整理：与えられたデータを項目ごとに整理します。\n2. 財務状況の分析：整理されたデータを基に、収益性、安全性、効率性などの観点から財務状況を分析します。\n3. 改善点の指摘：分析結果に基づき、具体的な改善点を指摘します。\n\n# 出力フォーマット\n\n分析結果を以下の形式で出力します。\n\n
\n## 財務分析\n\n[財務状況の分析結果を記述]\n\n## 改善点\n\n* [改善点1]\n* [改善点2]\n* [改善点3] \n...\n
\n\n# 例\n\n## 入力データ\n\n
\n売上高: 100000000\n売上原価: 60000000\n販売費及び一般管理費: 20000000\n営業利益: 20000000\n従業員数: 100\n平均年間給与: 6000000\n短期借入金: 5000000\n長期借入金: 20000000\n総資産: 150000000\n純資産: 100000000\n流動資産: 80000000\n流動負債: 30000000\n完成工事高: 0\n完成工事原価: 0\n未成工事支出金: 0\n未成工事受入金: 0\n役員報酬: 5000000\n
\n\n## 出力\n\n
\n## 財務分析\n\n売上高は1億円であり、売上原価と販売費及び一般管理費を差し引いた営業利益は2000万円です。営業利益率は20%であり、良好な収益性を維持しています。従業員一人当たりの平均年間給与は600万円で、平均的な水準です。短期および長期借入金の合計は2500万円であり、総資産1億5000万円に対して低い比率です。流動資産は8000万円で、流動負債3000万円を大きく上回っており、短期的な支払い能力に問題はありません。完成工事関連のデータは全て0であり、建設業ではない可能性があります。役員報酬は500万円で、売上高に対する比率は低く、適切な水準です。\n\n## 改善点\n\n* 営業利益率が高い水準を維持しているため、さらなる事業拡大のための投資を検討することが望ましいです。\n* 短期借入金と長期借入金の比率が低く、財務レバレッジを活用することで、さらなる収益向上が期待できます。\n* 完成工事関連のデータが全て0であるため、業種に特化した財務指標を追加することで、より詳細な分析が可能になります。\n
\n",
)

chat_session = model.start_chat(
  history=[
  ]
)

response_data = chat_session.send_message(formatted_data)

print(response_data.text)

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
  system_instruction="以下の項目から得られた情報について、要点を整理し、経営改善につなげる提言を行ってください。\n\n[項目]\n\nSteps\n\n項目で指定された情報を分析し、要点を整理します。\n\n整理した要点に基づき、経営改善につながる提言を検討します。\n\n検討した提言をまとめ、出力します。\n\nOutput Format\n\n300文字程度の文章で、要点の整理と提言を記述します。\n\nExamples\n\n[項目] = 経営方針\n\n[入力]\n[経営方針の情報]\n\n[出力]\n経営方針の要点は[要点]です。この方針に基づき、[提言]を行うことで、経営改善につなげられると考えます。\n\n（実際には経営方針の情報はより長く詳細なものになります。例: 今期の売上目標、具体的な施策、経営理念など）\n\n[項目] = 経営環境等の課題\n\n[入力]\n[経営環境等の課題の情報]\n\n[出力]\n経営環境等の課題の要点は[要点]です。この課題に対応するために、[提言]を行うことで、経営改善につなげられると考えます。\n\n（実際には経営環境等の課題の情報はより長く詳細なものになります。例: 市場動向、競合状況、法規制の変更など）\n\n[項目] = 経営上のリスク\n\n[入力]\n[経営上のリスクの情報]\n\n[出力]\n経営上のリスクの要点は[要点]です。このリスクを軽減するために、[提言]を行うことで、経営改善につなげられると考えます。\n\n（実際には経営上のリスクの情報はより長く詳細なものになります。例: 資金繰り、人材流出、自然災害など）\n\n[項目] = 従業員情報\n\n[入力]\n[従業員情報]\n\n[出力]\n従業員情報の要点は[要点]です。従業員がより活躍できる環境を作るために、[提言]を行うことで、経営改善につなげられると考えます。\n\n（実際には従業員情報はより長く詳細なものになります。例: 平均年齢、勤続年数、スキル分布、満足度調査など）\n\nNotes\n\n[項目]には、「経営方針」「経営環境等の課題」「経営上のリスク」「従業員情報」のいずれかが入ります。\n\n出力する提言は、具体的かつ実現可能なものにしてください。",
)

chat_session = model.start_chat(
  history=[
  ]
)

response_business_policy = chat_session.send_message(BusinessPolicy_cleaned)

print(response_business_policy.text)

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
  system_instruction="以下の項目から得られた情報について、要点を整理し、経営改善につなげる提言を行ってください。\n\n[項目]\n\nSteps\n\n項目で指定された情報を分析し、要点を整理します。\n\n整理した要点に基づき、経営改善につながる提言を検討します。\n\n検討した提言をまとめ、出力します。\n\nOutput Format\n\n300文字程度の文章で、要点の整理と提言を記述します。\n\nExamples\n\n[項目] = 経営方針\n\n[入力]\n[経営方針の情報]\n\n[出力]\n経営方針の要点は[要点]です。この方針に基づき、[提言]を行うことで、経営改善につなげられると考えます。\n\n（実際には経営方針の情報はより長く詳細なものになります。例: 今期の売上目標、具体的な施策、経営理念など）\n\n[項目] = 経営環境等の課題\n\n[入力]\n[経営環境等の課題の情報]\n\n[出力]\n経営環境等の課題の要点は[要点]です。この課題に対応するために、[提言]を行うことで、経営改善につなげられると考えます。\n\n（実際には経営環境等の課題の情報はより長く詳細なものになります。例: 市場動向、競合状況、法規制の変更など）\n\n[項目] = 経営上のリスク\n\n[入力]\n[経営上のリスクの情報]\n\n[出力]\n経営上のリスクの要点は[要点]です。このリスクを軽減するために、[提言]を行うことで、経営改善につなげられると考えます。\n\n（実際には経営上のリスクの情報はより長く詳細なものになります。例: 資金繰り、人材流出、自然災害など）\n\n[項目] = 従業員情報\n\n[入力]\n[従業員情報]\n\n[出力]\n従業員情報の要点は[要点]です。従業員がより活躍できる環境を作るために、[提言]を行うことで、経営改善につなげられると考えます。\n\n（実際には従業員情報はより長く詳細なものになります。例: 平均年齢、勤続年数、スキル分布、満足度調査など）\n\nNotes\n\n[項目]には、「経営方針」「経営環境等の課題」「経営上のリスク」「従業員情報」のいずれかが入ります。\n\n出力する提言は、具体的かつ実現可能なものにしてください。",
)

chat_session = model.start_chat(
  history=[
  ]
)

response_risks = chat_session.send_message(BusinessRisksTextBlock_cleaned)

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
  system_instruction="以下の項目から得られた情報について、要点を整理し、経営改善につなげる提言を行ってください。\n\n[項目]\n\nSteps\n\n項目で指定された情報を分析し、要点を整理します。\n\n整理した要点に基づき、経営改善につながる提言を検討します。\n\n検討した提言をまとめ、出力します。\n\nOutput Format\n\n300文字程度の文章で、要点の整理と提言を記述します。\n\nExamples\n\n[項目] = 経営方針\n\n[入力]\n[経営方針の情報]\n\n[出力]\n経営方針の要点は[要点]です。この方針に基づき、[提言]を行うことで、経営改善につなげられると考えます。\n\n（実際には経営方針の情報はより長く詳細なものになります。例: 今期の売上目標、具体的な施策、経営理念など）\n\n[項目] = 経営環境等の課題\n\n[入力]\n[経営環境等の課題の情報]\n\n[出力]\n経営環境等の課題の要点は[要点]です。この課題に対応するために、[提言]を行うことで、経営改善につなげられると考えます。\n\n（実際には経営環境等の課題の情報はより長く詳細なものになります。例: 市場動向、競合状況、法規制の変更など）\n\n[項目] = 経営上のリスク\n\n[入力]\n[経営上のリスクの情報]\n\n[出力]\n経営上のリスクの要点は[要点]です。このリスクを軽減するために、[提言]を行うことで、経営改善につなげられると考えます。\n\n（実際には経営上のリスクの情報はより長く詳細なものになります。例: 資金繰り、人材流出、自然災害など）\n\n[項目] = 従業員情報\n\n[入力]\n[従業員情報]\n\n[出力]\n従業員情報の要点は[要点]です。従業員がより活躍できる環境を作るために、[提言]を行うことで、経営改善につなげられると考えます。\n\n（実際には従業員情報はより長く詳細なものになります。例: 平均年齢、勤続年数、スキル分布、満足度調査など）\n\nNotes\n\n[項目]には、「経営方針」「経営環境等の課題」「経営上のリスク」「従業員情報」のいずれかが入ります。\n\n出力する提言は、具体的かつ実現可能なものにしてください。",
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
  system_instruction="以下の項目から得られた情報について、要点を整理し、経営改善につなげる提言を行ってください。\n\n[項目]\n\nSteps\n\n項目で指定された情報を分析し、要点を整理します。\n\n整理した要点に基づき、経営改善につながる提言を検討します。\n\n検討した提言をまとめ、出力します。\n\nOutput Format\n\n300文字程度の文章で、要点の整理と提言を記述します。\n\nExamples\n\n[項目] = 経営方針\n\n[入力]\n[経営方針の情報]\n\n[出力]\n経営方針の要点は[要点]です。この方針に基づき、[提言]を行うことで、経営改善につなげられると考えます。\n\n（実際には経営方針の情報はより長く詳細なものになります。例: 今期の売上目標、具体的な施策、経営理念など）\n\n[項目] = 経営環境等の課題\n\n[入力]\n[経営環境等の課題の情報]\n\n[出力]\n経営環境等の課題の要点は[要点]です。この課題に対応するために、[提言]を行うことで、経営改善につなげられると考えます。\n\n（実際には経営環境等の課題の情報はより長く詳細なものになります。例: 市場動向、競合状況、法規制の変更など）\n\n[項目] = 経営上のリスク\n\n[入力]\n[経営上のリスクの情報]\n\n[出力]\n経営上のリスクの要点は[要点]です。このリスクを軽減するために、[提言]を行うことで、経営改善につなげられると考えます。\n\n（実際には経営上のリスクの情報はより長く詳細なものになります。例: 資金繰り、人材流出、自然災害など）\n\n[項目] = 従業員情報\n\n[入力]\n[従業員情報]\n\n[出力]\n従業員情報の要点は[要点]です。従業員がより活躍できる環境を作るために、[提言]を行うことで、経営改善につなげられると考えます。\n\n（実際には従業員情報はより長く詳細なものになります。例: 平均年齢、勤続年数、スキル分布、満足度調査など）\n\nNotes\n\n[項目]には、「経営方針」「経営環境等の課題」「経営上のリスク」「従業員情報」のいずれかが入ります。\n\n出力する提言は、具体的かつ実現可能なものにしてください。",
)

chat_session = model.start_chat(
  history=[
  ]
)

response_employee_information = chat_session.send_message(employee_information)

print(response_employee_information.text)
'''
