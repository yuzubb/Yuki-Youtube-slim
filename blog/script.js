document.addEventListener('DOMContentLoaded', function() {
    // 「重力」という単語の要素を取得
    const gravityWord = document.getElementById('gravity-word');

    // クッキーに特定の情報（yuki=True）があるか確認
    const hasCookie = document.cookie.split(';').some(item => item.trim().startsWith('yuki=True'));

    // もしHTML要素が存在するなら、イベントリスナーを追加
    if (gravityWord) {
        gravityWord.addEventListener('click', function() {
            // クッキーがない場合のみ処理を実行
            if (!hasCookie) { 
                // クッキーを設定
                document.cookie = "yuki=True; max-age=31536000; path=/";
                
                // ページを再読み込み
                location.reload();
            }
        });
    }

    // 再読み込み後に実行したい処理
    if (hasCookie) {
        console.log('クッキーが設定されており、ページが再読み込みされました。');
        // 必要に応じて、ここに再読み込み後の特別な動作を追加できます
        // 例：alert('再読み込みが完了しました！');
    }
});
