from effect import ComposedDispatcher, Effect, base_dispatcher
from effect.do import do
from flask import redirect, render_template, url_for
from flask import g

from src.core import move, take
from src.fpflask import FunctionalFlask
from src.setup import initial_state
from src.storage import LoadGame, SaveGame, connect_db, initialize, sqlite_dispatcher

app = FunctionalFlask("the_game")

@app.before_request
def before_request():
    g.conn = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.conn.close()

def get_conn():
    return g.conn

@app.route("/")
def root(request):
    return Effect(LoadGame()).on(
        lambda state: render_template("game.html", state=state)
    )


@app.route("/move", methods=["POST"])
@do
def handle_move(request):
    exit_name = request.form["exit_name"]
    state = yield Effect(LoadGame())
    new_state = move(state, exit_name)
    if new_state is not None:
        yield Effect(SaveGame(state=new_state))
    return redirect(url_for("root"))


@app.route("/take", methods=["POST"])
@do
def handle_take(request):
    item_name = request.form["item_name"]
    state = yield Effect(LoadGame())
    new_state = take(state, item_name)
    if new_state is not None:
        yield Effect(SaveGame(state=new_state))
    return redirect(url_for("root"))


if __name__ == "__main__":
    conn = connect_db()
    initialize(conn, initial_state)
    dispatcher = ComposedDispatcher([base_dispatcher, sqlite_dispatcher(get_conn)])
    app.flask.config.update(PROPAGATE_EXCEPTIONS=True)
    app.run(dispatcher=dispatcher)
