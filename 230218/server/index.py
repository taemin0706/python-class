from flask import Flask

# Flask 클래스 생성
# __name__ : 파일의 이름
app = Flask(__name__)

# @ 네비게이터 : 바로 아래에 있는 함수를 실행하겠다.
# route(주소) : 주소에 요청을 하면 아래의 함수를 실행
# @app.route("/") : 127.0.0.1:5000/ 요청 하는 경우 아래의 함수를 실행
@app.route("/")
def index() :
    return "Hello World"

app.run
