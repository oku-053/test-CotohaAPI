import os
import configparser
from cotoha_api_client import CotohaAPIClient
import json

def convertClassToJp(resultObjects):
    with open('class.json') as f:
        classObjects = json.load(f)
    
    with open('extended_class.json') as f:
        exClassObjects = json.load(f)
    
    
    convertResult = []
    
    for resultObject in resultObjects["result"]:
        print(resultObject)
        for classObjectKey in classObjects:
            if resultObject["class"] == classObjectKey:
                resultObject["class"] = classObjects[classObjectKey]
                
        for exClassObjectKey in exClassObjects:
            if resultObject["extended_class"] == exClassObjectKey:
                resultObject["extended_class"] = exClassObjects[exClassObjectKey]
        
        convertResult.append(resultObject)
    
    return convertResult

if __name__ == '__main__':
    # ソースファイルの場所取得
    APP_ROOT = os.path.dirname(os.path.abspath( __file__)) + "/"
    
    with open('payload.json') as f:
        config = json.load(f)

    # 設定値取得
    CLIENT_ID = config["ClientId"]
    CLIENT_SECRET = config["ClientSecret"]
    DEVELOPER_API_BASE_URL = config["APIBaseURL"]
    ACCESS_TOKEN_PUBLISH_URL = config["AccessTokenPublishURL"]

    # COTOHA APIインスタンス生成
    cotoha_api_client = CotohaAPIClient(CLIENT_ID, CLIENT_SECRET, DEVELOPER_API_BASE_URL, ACCESS_TOKEN_PUBLISH_URL)

    # 固有表現抽出対象文
    target = open('targetSentence.txt', 'r', encoding='UTF-8')
    sentence = target.read()
    target.close

    # 固有表現抽出API実行
    resultJson = cotoha_api_client.ne(sentence)

    # 結果を日本語に変換
    convertResult = convertClassToJp(resultJson)

    #結果をファイルに書き込み
    with open('result.json', 'w') as f:
        json.dump(convertResult, f, ensure_ascii=False, indent=4)
    
    # 結果表示
    print(resultJson)