from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def read(p): return (ROOT/p).read_text(encoding='utf-8')

def test_postgres_only_server():
    db=read('app/db.py')
    assert 'postgresql' in db
    assert 'SQLite is not supported' in db

def test_idempotent_offline_sales():
    models=read('app/models.py'); main=read('app/main.py')
    assert 'client_id' in models and 'unique=True' in models
    assert 'select(Sale).where(Sale.client_id' in main
    assert 'with_for_update()' in main

def test_offline_queue_and_service_worker():
    pos=read('app/templates/pos.html'); sw=read('app/static/service-worker.js')
    assert 'indexedDB' in pos and 'api/sync/sales' in pos
    assert 'offline-pos' in sw and 'serviceWorker' not in sw


def test_render_port_and_healthcheck():
    main=read('app/main.py'); docker=read('Dockerfile')
    assert 'os.getenv("PORT"' in main or 'PORT' in docker
    assert '/healthz' in main


def test_render_postgres_url_compatibility():
    db=read('app/db.py')
    assert 'postgres://"' in db or "postgres://" in db
    assert 'postgresql://"' in db or "postgresql://" in db
    assert 'postgresql+psycopg://"' in db or "postgresql+psycopg://" in db
