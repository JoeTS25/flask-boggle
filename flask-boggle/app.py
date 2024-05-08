from flask import Flask, request, render_template, jsonify, session
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = "ssddffgg"

boggle_game = Boggle()

@app.route('/')
def begin_game():
    # displays board on homepage
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    return render_template("boggle.html", board=board,
                           highscore=highscore,
                           nplays=nplays)


@app.route('/check-valid')
def valid_word():
    word = request.args["word"]  
    board = session["board"]
    # get a response from the check_valid_word function in boggle.py and jsonify its result
    response = boggle_game.check_valid_word(board, word)
    return jsonify({'result': response})

@app.route("/post-score", methods=["POST"])
def post_score():
    """Posts new high score if achieved, and tells how many plays."""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)


