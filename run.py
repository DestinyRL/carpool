import os
import sys
import subprocess
import multiprocessing
import time

BASE_DIR = os.path.join(os.path.dirname(__file__), 'carpool_django')


def run_django():
    env = os.environ.copy()
    if 'CARPOOL_SECRET_KEY' in os.environ:
        env['CARPOOL_SECRET_KEY'] = os.environ['CARPOOL_SECRET_KEY']

    try:
        subprocess.check_call([sys.executable, 'manage.py', 'migrate'], cwd=BASE_DIR, env=env)
    except subprocess.CalledProcessError:
        print('Failed to run migrations for Django')

    subprocess.check_call([sys.executable, 'manage.py', 'runserver', '0.0.0.0:8000'], cwd=BASE_DIR, env=env)


def run_fastapi():
    import uvicorn

    env = os.environ.copy()
    if 'CARPOOL_SECRET_KEY' in os.environ:
        env['CARPOOL_SECRET_KEY'] = os.environ['CARPOOL_SECRET_KEY']

    uvicorn.run('fastapi_app.main:app', host='0.0.0.0', port=8080, reload=False)


if __name__ == '__main__':
    print('Starting Carpool backend: Django (8000) + FastAPI (8080)')
    p1 = multiprocessing.Process(target=run_django, name='django')
    p2 = multiprocessing.Process(target=run_fastapi, name='fastapi')

    p1.start()
    time.sleep(1)
    p2.start()

    try:
        p1.join()
        p2.join()
    except KeyboardInterrupt:
        print('Shutting down...')
        p1.terminate()
        p2.terminate()
