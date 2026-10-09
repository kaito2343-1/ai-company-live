# ai-company-live
AI経営チームの活動を可視化する、2事業対応の経営シミュレーション型ダッシュボード。
AI COMPANY LIVE v0.1

スマホ向けの「AI会社 経営シミュレーションゲーム型」試作品です。すべて静的ファイルなので、初期費用は0円です。アニメーションはゲーム演出であり、ChatGPT / Workの実際の動作を取得していません。

使い方

1. index.html をChromeまたはSafariで開きます。iPhoneの「ファイル」アプリ内プレビューはJavaScriptを制限することがあります。その場合は下記の無料公開手順を利用します。
2. 「交渉文庫」「かけまる研究所」で事業を切り替えられます。キャラクターをタップすると仮想担当の仕事の説明が見られます。
3. 「演出停止」「速度」で画面のアニメーションを操作できます。演出ログと実績ログは別です。
4. 「＋ 実績を記録」で手入力した事実の記録を端末内に保存できます。根拠URLは任意です。入力の真偽はシステムで保証されません。
5. 「JSON保存」で実績データをバックアップできます。「JSON取込」で別端末のログを取り込めます。

GitHub Pagesで無料公開

1. GitHubで新規の公開リポジトリ（例 ai-company-live）を作ります。ログイン情報や売上の機密データはアップロードしないでください。
2. このフォルダにある index.html と data/activity.json をリポジトリのルートに配置します。
3. GitHubのリポジトリの Settings → Pages → Build and deployment → Deploy from a branch → main / (root) を指定します。
4. 公開されたPagesのURLをSafariで開き、「共有 → ホーム画面に追加」を選べばアプリのように使えます。

※GitHubの公開リポジトリ内の data/activity.json は全世界に公開されます。顧客名・非公開の売上・内部原稿・個人情報・パスワード・APIキー等を記録しないことを強く推奨します。

実データにする方法（次の段階）

GitHub Actions、許可されたAPIや明示的な手動記録から data/activity.json を更新できれば、この画面はページを開いている間、60秒ごとに更新を確認します。静的サイトだけではAIの進捗は自動取得できません。

JSONの形式

{
  "schemaVersion": 1,
  "records": [
    {
      "id": "public-post-001",
      "business": "bunko",
      "role": "CMO",
      "summary": "実際に確認済みの公開内容（例）",
      "at": "2026-10-10T12:00:00+09:00",
      "source": "json",
      "evidence": "https://example.com/verified-page"
    }
  ],
  "metrics": {
    "bunko": {"posts": 2, "articles": 1, "sales": null, "revenue": null, "updatedAt": "2026-10-10の記録"},
    "kakemaru": {"posts": null, "articles": null, "sales": null, "revenue": null, "updatedAt": "未取得"}
  }
}

上は仕様説明の例であり、実績を表していません。JSON取り込み後もデータが真実かどうかを自動検証する仕組みはありません。

現在の制限

• GitHub Pagesへの公開は未実施。公開URLはまだありません。
• ChatGPT Work、note、X、Threads等の実APIとは未連携。
• ブラウザのローカル保存は端末ごとで、同期されません。
• AI役員が動き回る・ゲーム内の時間が進む・会話する挙動はすべて演出です。
• data/activity.json の自動再取得は画面を開いている間だけ。iOSがバックグラウンドにしたタブは動作が止まる場合があります。
