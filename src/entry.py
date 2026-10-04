import os
import sys
from django.core.wsgi import get_wsgi_application
from a2wsgi import WSGItoASGI

# プロジェクトルートをPythonパスに追加
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Djangoの環境変数をセット
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Djangoの初期化
application = get_wsgi_application()

# Workers（ASGI/Async）環境で動かすための変換アダプター
asgi_app = WSGItoASGI(wsgi_app)

# Cloudflare WorkersからのHTTPリクエストをDjangoで処理するハンドラー
async def on_fetch(request, env, ctx):
    # Cloudflareの環境変数をPython側で読み込めるようにセット
    for key, value in env.items():
        if isinstance(value, str):
            os.environ[key] = value

    return await asgi_app(request, env, ctx)