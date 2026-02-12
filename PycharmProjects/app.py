from flask import Flask, render_template, request, session, redirect, url_for
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "replace-this-with-a-secure-random-key"
app.permanent_session_lifetime = timedelta(minutes=60)

# -------------------------
# CONFIG
# -------------------------
DEFAULT_WELCOME = "יום אהבה שמח אהובי💖 מוכן למשחק קטן?"
MATH_RIDDLE_ANSWER = 3
MAP_RIDDLE_ANSWER = 9
FINAL_DATE = "2026-02-18"
PIC_RIDDLE_ANSWER = "ליאן"
TEXT_RIDDLE_ANSWER = "חופשה"
MAX_ATTEMPTS = 3
# -------------------------


def init_game():
    session.clear()
    session.permanent = True
    session['step'] = 0
    session['attempts'] = MAX_ATTEMPTS
    session['message'] = ""
    session['progress'] = []
    session['final_date'] = FINAL_DATE
    session['pic_images'] = ["pic1.jpg", "pic2.jpg", "pic3.jpg"]


@app.route("/", methods=["GET", "POST"])
def index():
    # -- Restarting the web --
    if request.args.get("reset") == "1":
        init_game()
        return redirect(url_for("index"))

    if 'step' not in session:
        init_game()

    if request.method == "POST":
        action = request.form.get("action")

        # --- start game ---
        if action == "start_game":
            session['step'] = 1
            session['attempts'] = MAX_ATTEMPTS
            return redirect(url_for('index'))

        # --- math riddle ---
        if action == "math_submit":
            guess = request.form.get("math_guess", "").strip()
            if guess == str(MATH_RIDDLE_ANSWER):
                session['progress'].append("פתרת את החידה המתמטית✅")
                session['message'] = ""
                session['attempts'] = MAX_ATTEMPTS
                session['step'] = 2
            else:
                session['attempts'] -= 1
                if session['attempts'] <= 0:
                    session['progress'].append("דילגת על החידה המתמטית⏭️")
                    session['message'] = ""
                    session['attempts'] = MAX_ATTEMPTS
                    session['step'] = 2
                else:
                    session['message'] = f"לא נכון — נשארו {session['attempts']} ניסיונות."
            return redirect(url_for('index'))

        # --- map riddle ---
        if action == "map_pick":
            picked = request.form.get("map_choice")
            if picked == str(MAP_RIDDLE_ANSWER):
                session['progress'].append("מצאת את המספר על המפה ✅")
                session['message'] = ""
                session['attempts'] = MAX_ATTEMPTS
                session['step'] = 3
            else:
                session['attempts'] -= 1
                if session['attempts'] <= 0:
                    session['progress'].append("דילגת על המפה ⏭️")
                    session['message'] = ""
                    session['attempts'] = MAX_ATTEMPTS
                    session['step'] = 3
                else:
                    session['message'] = f"לא זה — נשארו {session['attempts']} ניסיונות."
            return redirect(url_for('index'))

        # --- picture riddle ---
        if action == "pic_submit":
            guess = request.form.get("pic_guess", "").strip().lower()
            if guess == PIC_RIDDLE_ANSWER:
                session['progress'].append("פתרת את חידת התמונות ✅")
                session['message'] = ""
                session['attempts'] = MAX_ATTEMPTS
                session['step'] = 4
            else:
                session['attempts'] -= 1
                if session['attempts'] <= 0:
                    session['progress'].append("דילגת על חידת התמונות ⏭️")
                    session['message'] = ""
                    session['attempts'] = MAX_ATTEMPTS
                    session['step'] = 4
                else:
                    session['message'] = f"לא נכון — נשארו {session['attempts']} ניסיונות."
            return redirect(url_for('index'))

        # --- text riddle ---
        if action == "text_submit":
            guess = request.form.get("text_guess", "").strip().lower()
            if guess == TEXT_RIDDLE_ANSWER:
                session['progress'].append("פתרת את החידה הטקסטואלית ✅")
                session['message'] = ""
                session['attempts'] = MAX_ATTEMPTS
                session['step'] = 5
            else:
                session['attempts'] -= 1
                if session['attempts'] <= 0:
                    session['progress'].append("דילגת על החידה הטקסטואלית ⏭️")
                    session['message'] = ""
                    session['attempts'] = MAX_ATTEMPTS
                    session['step'] = 5
                else:
                    session['message'] = f"לא נכון — נשארו {session['attempts']} ניסיונות."
            return redirect(url_for('index'))

        # --- date pick ---
        if action == "date_pick":
            chosen = request.form.get("date_choice")
            if chosen == session['final_date']:
                session['progress'].append("ניחשת את התאריך הנכון 💕")
                session['step'] = 999
            else:
                session['message'] = "אין תחושות בטן... רק בטן.😘"
            return redirect(url_for('index'))

        # --- restart ---
        if action == "restart":
            init_game()
            return redirect(url_for('index'))

    # --- positions numbers ---
    map_positions = [
        (1, "65%", "18%"), (2, "50%", "20%"), (3, "47%", "28%"),
        (4, "63%", "29%"), (5, "42%", "33%"), (6, "49%", "43%"),
        (7, "67%", "57%"), (8, "45%", "65%"), (9, "47%", "93%")
    ]

    return render_template(
        "game.html",
        step=session['step'],
        message=session.get('message', ""),
        attempts=session.get('attempts', MAX_ATTEMPTS),
        progress=session.get('progress', []),
        pic_images=session.get('pic_images', []),
        map_positions=map_positions,
        final_date=session.get('final_date'),
        welcome_text=DEFAULT_WELCOME
    )


if __name__ == "__main__":
    app.run(debug=True, port=5004, host="0.0.0.0")
