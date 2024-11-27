from arelle import Cntlr, ModelXbrl

# XBRLデータのファイルパス
xbrl_file = "L:\ダウンロード\Xbrl_Search_20241127_161643\S100UA2W\XBRL\PublicDoc\jpcrp030000-asr-001_E00059-000_2024-05-31_01_2024-08-27.xbrl"  # ファイルパスを適切なものに置き換える

# arelle ControllerとModelXbrlのインスタンスを作成
cntlr = Cntlr.Cntlr()
modelxbrl = ModelXbrl.load(cntlr, xbrl_file)

# 要素名とラベルのリストを格納する辞書
element_labels = {}

# conceptsはタクソノミに定義された概念のリストです。
for concept in modelxbrl.qnameConcepts.values():
    # 要素名を取得
    qname = concept.qname
    
    # ラベルを取得。多言語対応している場合、言語を指定する必要がある。
    # ここでは、日本語ラベルを取得する例を示す。
    label = concept.label(lang="ja")  # lang="en" で英語ラベルを取得

    # 要素名とラベルを辞書に追加
    element_labels[str(qname)] = label


# 結果を出力
for qname, label in element_labels.items():
    print(f"要素名: {qname}, ラベル: {label}")


# 後処理
modelxbrl.close()
cntlr.close()