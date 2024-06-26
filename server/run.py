import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('SERVER_PORT')), host=os.environ.get('SERVER_HOST'))

