import urllib.request
import json

class CotohaAPIClient:
    """
    COTOHA API クライアントクラス
    """
    def __init__(self, client_id, client_secret, developer_api_base_url, access_token_publish_url):
        """
        イニシャライザ

        Parameters
        ----------
        client_id : str
            Client ID
        client_secret : str
            Developer Client Secret
        developer_api_base_url : str
            Developer API Base URL
        access_token_publish_url : str
            Access Token Publish URL
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.developer_api_base_url = developer_api_base_url
        self.access_token_publish_url = access_token_publish_url
        self.get_access_token()


    def get_access_token(self):
        """
        Access Token を取得し設定する
        """
        # アクセストークン取得 API URL 指定
        url = self.access_token_publish_url
        # ヘッダ指定
        headers={
            'Content-Type' : 'application/json;charset=UTF-8'
        }
        # リクエストボディ指定
        data = {
            'grantType' : 'client_credentials',
            'clientId' : self.client_id,
            'clientSecret' : self.client_secret
        }
        # リクエストボディ指定をJSONにエンコード
        data = json.dumps(data).encode()

        # リクエスト生成
        req = urllib.request.Request(url, data, headers)
        # リクエストを送信し、レスポンスを受信
        res = urllib.request.urlopen(req)

        # レスポンスボディ取得
        res_body = res.read()
        # レスポンスボディをJSONからデコード
        res_body = json.loads(res_body)
        # レスポンスボディからアクセストークンを取得
        self.access_token = res_body['access_token']


    def get_response(self, url, data, headers) :
        """
        API を呼び出すテンプレートの private メソッド

        Parameters
        ----------
        url : url
            エンドポイント
        data : dict
            リクエストボディ
        headers : dict
            リクエストヘッダ

        Returns
        -------
        res_body : dict
            レスポンスボディ
        """        
        # リクエストボディ指定をJSONにエンコード
        data = json.dumps(data).encode()

        # リクエスト生成
        req = urllib.request.Request(url, data, headers)

        # リクエストを送信し、レスポンスを受信
        try:
            res = urllib.request.urlopen(req)
        # リクエストでエラーが発生した場合の処理
        except urllib.request.HTTPError as e:
            # ステータスコードが401 Unauthorizedならアクセストークンを取得し直して再リクエスト
            if e.code == 401:
                print ('get access token')
                self.get_access_token()
                headers['Authorization'] = 'Bearer ' + self.access_token
                req = urllib.request.Request(url, data, headers)
                res = urllib.request.urlopen(req)
            # 401以外のエラーなら原因を表示
            else:
                raise Exception(e.reason)

        # レスポンスボディ取得
        res_body = res.read()
        # レスポンスボディをJSONからデコード
        res_body = json.loads(res_body)

        return res_body



    def parse(self, sentence, type='default'):
        """
        構文解析 API を呼び出す (https://api.ce-cotoha.com/contents/reference/apireference.html#parsing)

        Parameters
        ----------
        sentence : str
            構文解析対象の文字列
        type : str
            通常文なら 'default', SNS などの崩れた文なら 'kuzure' を指定

        Returns
        -------
        result : dict
            構文解析結果
        """
        # 構文解析API URL指定
        url = self.developer_api_base_url + 'nlp/v1/parse'
        # ヘッダ指定
        headers={
            'Authorization' : 'Bearer ' + self.access_token,
            'Content-Type' : 'application/json;charset=UTF-8',
        }
        # リクエストボディ指定
        data = {
            'sentence' : sentence,
            'type' : type
        }

        # API を呼び出して結果取得
        result = self.get_response(url, data, headers)

        return result


    def ne(self, sentence, type='default'):
        """
        固有表現抽出 API を呼び出す (https://api.ce-cotoha.com/contents/reference/apireference.html#entity)

        Parameters
        ----------
        sentence : str
            固有表現抽出対象の文字列
        type : str
            通常文なら 'default', SNS などの崩れた文なら 'kuzure' を指定

        Returns
        -------
        result : dict
            固有表現抽出結果
        """
        # 固有表現抽出API URL指定
        url = self.developer_api_base_url + 'nlp/v1/ne'
        # ヘッダ指定
        headers={
            'Authorization' : 'Bearer ' + self.access_token,
            'Content-Type' : 'application/json;charset=UTF-8',
        }
        # リクエストボディ指定
        data = {
            'sentence' : sentence,
            'type' : type
        }

        # API を呼び出して結果取得
        result = self.get_response(url, data, headers)

        return result


    def coreference(self, document, type='default', do_segment=False):
        """
        照応解析 API を呼び出す (https://api.ce-cotoha.com/contents/reference/apireference.html#correspond)

        Parameters
        ----------
        document : Union[str, list[str]]
            照応解析対象の文字列または文字列のリスト
        type : str
            通常文なら 'default', SNS などの崩れた文なら 'kuzure' を指定
        do_segment : bool
            文区切りを実施するか否かを指定 (document が list のときは無効)

        Returns
        -------
        result : dict
            照応解析結果
        """
        # 照応解析API URL指定
        url = self.developer_api_base_url + 'nlp/v1/coreference'
        # ヘッダ指定
        headers={
            'Authorization' : 'Bearer ' + self.access_token,
            'Content-Type' : 'application/json;charset=UTF-8',
        }
        # リクエストボディ指定
        data = {
            'document' : document,
            'type' : type,
            'do_segment' : do_segment
        }

        # API を呼び出して結果取得
        result = self.get_response(url, data, headers)

        return result


    def keyword(self, document, type='default', do_segment=False, max_keyword_num=5) :
        """
        キーワード抽出 API を呼び出す (https://api.ce-cotoha.com/contents/reference/apireference.html#keyword)

        Parameters
        ----------
        document : Union[str, list[str]]
            キーワード抽出対象の文字列または文字列のリスト
        type : str
            通常文なら 'default', SNS などの崩れた文なら 'kuzure' を指定
        do_segment : bool
            文区切りを実施するか否かを指定 (document が list のときは無効)
        max_keyword_num : int
            抽出するキーワードの上限個数

        Returns
        -------
        result : dict
            キーワード抽出結果
        """
        # キーワード抽出API URL指定
        url = self.developer_api_base_url + 'nlp/v1/keyword'
        # ヘッダ指定
        headers={
            'Authorization' : 'Bearer ' + self.access_token,
            'Content-Type' : 'application/json;charset=UTF-8',
        }
        # リクエストボディ指定
        data = {
            'document' : document,
            'type' : type,
            'do_segment' : do_segment,
            'max_keyword_num' : max_keyword_num,
        }

        # API を呼び出して結果取得
        result = self.get_response(url, data, headers)

        return result


    def similarity(self, s1, s2, type='default'):
        """
        類似度算出 API を呼び出す (https://api.ce-cotoha.com/contents/reference/apireference.html#similarity)

        Parameters
        ----------
        s1 : str
            類似度計算対象の文字列1
        s2 : str
            類似度計算対象の文字列2
        type : str
            通常文なら 'default', SNS などの崩れた文なら 'kuzure' を指定

        Returns
        -------
        result : dict
            類似度算出結果
        """
        # 類似度算出API URL指定
        url = self.developer_api_base_url + 'nlp/v1/similarity'
        # ヘッダ指定
        headers={
            'Authorization' : 'Bearer ' + self.access_token,
            'Content-Type' : 'application/json;charset=UTF-8',
        }
        # リクエストボディ指定
        data = {
            's1' : s1,
            's2' : s2,
            'type' : type,
        }

        # API を呼び出して結果取得
        result = self.get_response(url, data, headers)

        return result


    def sentence_type(self, sentence, type='default'):
        """
        文タイプ判定 API を呼び出す (https://api.ce-cotoha.com/contents/reference/apireference.html#sentence)

        Parameters
        ----------
        sentence : str
            文タイプ判定対象の文字列
        type : str
            通常文なら 'default', SNS などの崩れた文なら 'kuzure' を指定

        Returns
        -------
        result : dict
            文タイプ判定結果
        """
        # 文タイプ判定API URL指定
        url = self.developer_api_base_url + 'nlp/v1/sentence_type'
        # ヘッダ指定
        headers={
            'Authorization' : 'Bearer ' + self.access_token,
            'Content-Type' : 'application/json;charset=UTF-8',
        }
        # リクエストボディ指定
        data = {
            'sentence' : sentence,
            'type' : type,
        }

        # API を呼び出して結果取得
        result = self.get_response(url, data, headers)

        return result


    def user_attribute(self, document, type='default', do_segment=False):
        """
        ユーザ属性推定 API を呼び出す (https://api.ce-cotoha.com/contents/reference/apireference.html#user)

        Parameters
        ----------
        document : Union[str, list[str]]
            キーワード抽出対象の文字列または文字列のリスト
        type : str
            通常文なら 'default', SNS などの崩れた文なら 'kuzure' を指定
        do_segment : bool
            文区切りを実施するか否かを指定 (document が list のときは無効)

        Returns
        -------
        result : dict
            ユーザ属性推定結果
        """
        # ユーザ属性推定API URL指定
        url = self.developer_api_base_url + 'nlp/beta/user_attribute'
        # ヘッダ指定
        headers={
            'Authorization' : 'Bearer ' + self.access_token,
            'Content-Type' : 'application/json;charset=UTF-8',
        }
        # リクエストボディ指定
        data = {
            'document' : document,
            'type' : type,
            'do_segment' : do_segment
        }

        # API を呼び出して結果取得
        result = self.get_response(url, data, headers)

        return result


    def remove_filler(self, text, do_segment=False) : 
        """
        言い淀み除去 API を呼び出す (https://api.ce-cotoha.com/contents/reference/apireference.html#filler)

        Parameters
        ----------
        text : str
            言い淀み除去対象の文字列
        do_segment : bool
            文区切りを実施するか否かを指定 (document が list のときは無効)

        Returns
        -------
        result : dict
            言い淀み除去結果
        """
        # 言い淀み除去 API URL指定
        url = self.developer_api_base_url + 'nlp/beta/remove_filler'
        # ヘッダ指定
        headers={
            'Authorization' : 'Bearer ' + self.access_token,
            'Content-Type' : 'application/json;charset=UTF-8',
        }
        # リクエストボディ指定
        data = {
            'text' : text,
            'do_segment' : do_segment
        }

        # API を呼び出して結果取得
        result = self.get_response(url, data, headers)

        return result


    def detect_misrecognition(self, sentence) :
        """
        音声認識誤り検知 API を呼び出す (https://api.ce-cotoha.com/contents/reference/apireference.html#detect)

        Parameters
        ----------
        sentence : str
            音声認識誤り検知対象の文字列

        Returns
        -------
        result : dict
            音声認識誤り検知結果
        """
        # 音声認識誤り検知 API URL指定
        url = self.developer_api_base_url + 'nlp/beta/detect_misrecognition'
        # ヘッダ指定
        headers={
            'Authorization' : 'Bearer ' + self.access_token,
            'Content-Type' : 'application/json;charset=UTF-8',
        }
        # リクエストボディ指定
        data = {
            'sentence' : sentence
        }

        # API を呼び出して結果取得
        result = self.get_response(url, data, headers)

        return result


    def sentiment(self, sentence) :
        """
        感情分析 API を呼び出す (https://api.ce-cotoha.com/contents/reference/apireference.html#sentiment)

        Parameters
        ----------
        sentence : str
            感情分析対象の文字列

        Returns
        -------
        result : dict
            感情分析結果
        """
        # 感情分析 API URL指定
        url = self.developer_api_base_url + 'nlp/v1/sentiment'
        # ヘッダ指定
        headers={
            'Authorization' : 'Bearer ' + self.access_token,
            'Content-Type' : 'application/json;charset=UTF-8',
        }
        # リクエストボディ指定
        data = {
            'sentence' : sentence
        }

        # API を呼び出して結果取得
        result = self.get_response(url, data, headers)

        return result
