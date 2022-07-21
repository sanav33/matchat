from app.app import app
from app.utils.constants import PORT

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=PORT)