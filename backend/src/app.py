from flask import Flask
from flask_cors import CORS
from routes.users import users_bp
from routes.llm import llm_bp
from routes.leaderboard import leaderboard_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(users_bp, url_prefix="/api/users")
app.register_blueprint(llm_bp, url_prefix="/api/llm")
app.register_blueprint(leaderboard_bp, url_prefix="/api/leaderboard")



@app.route('/favicon.ico')
def favicon():
    # Browsers automatically request /favicon.ico. Return 204 No Content
    # to avoid 404s or noisy logs when you don't have an icon to serve.
    return ('', 204)

if __name__ == '__main__':
    app.run(debug=True)
