document.addEventListener('DOMContentLoaded', function() {
    // 「重力」という単語の要素を取得
    const gravityWord = document.getElementById('gravity-word');

    if (gravityWord) {
        gravityWord.addEventListener('click', function() {
            // 現在のURLパスを取得
            const currentPath = window.location.pathname;

            // URLに '/blog' が含まれているかチェック
            if (currentPath.includes('/blog')) {
                // '/blog' を削除した新しいURLを生成
                const newPath = currentPath.replace('/blog', '');

                // 新しいURLにリダイレクト
                window.location.href = newPath;
            }
        });
    }
    
    // --- 以下は以前のクッキー関連のコード。今回は無効化 ---
    /*
    const hasCookie = document.cookie.split(';').some(item => item.trim().startsWith('yuki=True'));
    if (hasCookie) {
        console.log('クッキーが設定されており、ページが再読み込みされました。');
    }
    */
});
