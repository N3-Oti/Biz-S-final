from arelle import Cntlr

xbrl_file = r"L:\TMP\KIC\bizs\analyzee\yuuka\Xbrl_Search_20241127_161643\S100UA2W\XBRL\PublicDoc\jpcrp030000-asr-001_E00059-000_2024-05-31_01_2024-08-27.xbrl"

# Arelleのコントローラーオブジェクトを初期化し、XBRLファイルからデータを読み込む
ctrl = Cntlr.Cntlr(logFileName='logToPrint')
model_xbrl = ctrl.modelManager.load(xbrl_file)

# 変数の初期化
company_name = None
netsales = None
risks = None

# forループを使ってXBRLに含まれる全てのFactを調査
# if文で特定の要素を抽出し、それぞれの変数に代入する
for fact in model_xbrl.facts:
    if fact.concept.qname.localName == "CompanyNameCoverPage":
        company_name = fact.value
    elif fact.concept.qname.localName == "NetSales":
        netsales = fact.value
    elif fact.concept.qname.localName == "BusinessRisksTextBlock":
        risks = fact.value

print("会社名：" + company_name)
print("売上高：" + netsales)
print("経営リスク：" + risks)
