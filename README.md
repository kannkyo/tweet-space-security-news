# tweet-space-security-news

## 設定項目

事前に設定しておくべき項目を以下に示す。

## AWS Lambda

AWS Lambda に以下の値を設定しておくこと。

### 環境変数

![env](README.assets/env.png)

- TWITTER_SECRET_NAME
  - 意味：twitter の API キーなどを格納したシークレットの名前
  - 例：`secrets/twitter`
- LOG_LEVEL
  - 意味：ログレベル `CRITICAL, ERROR, WARNING, INFO, DEBUG` から選択
  - 例：`DEBUG`

### Secrets

### Twitter

- api_key
  - 意味：Basic 認証用の API key
  - 例：`21afjlij4224`
- api_secret_key
  - 意味：api_secret_key
  - 例：`hoge`
- bearer_token
  - 意味：bearer_token
  - 例：`fajlfaiwejf239340`
- access_token
  - 意味：access_token
  - 例：`fajlfaiwejf239340`
- access_token_secret
  - 意味：access_token_secret
  - 例：`fajlfaiwejf239340`

## 使い方

### ソースコードのアップロード

まず、aws-cli を事前に設定しておくこと。

```bash
aws configure
```

次に、アップロードスクリプトを実行すること。

```bash
./upload.sh
```
