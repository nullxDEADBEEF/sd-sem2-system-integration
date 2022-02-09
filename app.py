from bottle import route, run, template, error


@error(404)
def error404(error):
    return f"{error} Impossible. Perhaps the archives are incomplete."


@route("/hello/<name>")
def greet(name="Stranger"):
    return template("Hello {{name}}, how are you?", name=name)


@route("/")
def index():
    return "Index"


run(host="localhost", port=8080, debug=True, reloader=True)
