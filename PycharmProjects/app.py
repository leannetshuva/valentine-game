from flask import Flask, render_template, request, session, redirect, url_for
from datetime import timedelta


# -------------------------
# יצירת אפליקציה, משתנים והגדרות בסיס
# -------------------------
app = Flask(__name__)
app.secret_key = "replace-this-with-a-secure-random-key"
app.permanent_session_lifetime = timedelta(minutes=60)

DEFAULT_WELCOME = "יום אהבה שמח אהובי💖<br> מוכן למשחק קטן?"
MATH_RIDDLE_ANSWER = "042"
MAP_RIDDLE_ANSWER = 6
FINAL_DATE = "2026-02-18"
PIC_RIDDLE_ANSWER = "ליאן"
TEXT_RIDDLE_ANSWER = "חופשה"
MAX_ATTEMPTS = 3
# -------------------------

# הודעות בעת ניסיונות
FAIL_MESSAGES = {
    "math": {
        2: "מזל שאני החכמה בקשר... נשארו 2 ניסיונות",
        1: "שגיאה 404: מדובר במטומטם. ניסיון אחרון.",
        0: "נשלח דיווח למחלקת שיפור ביצועים💖"
    },
    "map": {
        2: "תשמע אתה נרקומן... נשארו 2 ניסיונות",
        1: "אעמיד פנים שלא ראיתי את זה, נסה שוב",
        0: "לא חשבתי על מה לכתוב כאן כי חשבתי שתצליח, מסתבר שלא"
    },
    "pic": {
        2: "יא באשל, עוד 2 ניסיונות",
        1: "ניסיון יפה, כמעט כמו השקר שלך שהתחלתי איתך...",
        0: "אפילו צ׳יקו היה מצליח."
    },
    "text": {
        2: "נו מה?! שיקחו אותך כל השדים והשדות...",
        1: "שוב טעות? העיקר אתה ״מהנדס״",
        0: "GirlfriendOS: תשובה לא תואמת את הנתונים. דרוש להחליף חבר."
    },
    "date": {
        2: "אין תחושות בטן... רק בטן. 2 ניסיונות נשארו",
        1: "אתה מתיש, ניסיון אחרון",
        0: "יותר גרוע משון"
    }
}

# איתחול משחק חדש / ריסט
def init_game():
    session.clear()
    session.permanent = True
    session['step'] = 0
    session['success_next_step'] = None
    session['attempts'] = MAX_ATTEMPTS
    session['message'] = ""
    session['progress'] = []
    session['final_date'] = FINAL_DATE
    session['pic_images'] = ["pic1.jpg", "pic2.jpg", "pic3.jpg"]

# כישלונות ומעבר אוטומוטי
def fail_and_maybe_pause(riddle_key, skip_text, next_step):
    session['attempts'] -= 1

    if session['attempts'] <= 0:
        session['progress'].append(skip_text)
        session['message'] = FAIL_MESSAGES[riddle_key][0]
        session['failed_next_step'] = next_step
        session['step'] = "failed"
    else:
        session['message'] = FAIL_MESSAGES[riddle_key][session['attempts']]


# ------------ ROUTE -------------
@app.route("/", methods=["GET", "POST"])
def index():

    # ריסט ידני
    if request.args.get("reset") == "1":
        init_game()
        return redirect(url_for("index"))

    if 'step' not in session:
        init_game()

    if request.method == "POST":
        action = request.form.get("action")

        # מסך פתיחה / הוראות
        if action == "start_game":
            session['step'] = 0.5
            return redirect(url_for('index'))

        if action == "start_after_instructions":
            session['step'] = 1
            session['attempts'] = MAX_ATTEMPTS
            return redirect(url_for('index'))

        # ---- חידה מתמטית ----
        if action == "math_submit":
            guess = request.form.get("math_guess", "").strip()
            if guess == MATH_RIDDLE_ANSWER:
                session['progress'].append("פתרת את החידה המתמטית✅")
                session['message'] = "יותר מזל משכל... אבל למזלך אני עדיין אוהבת אותך💖"
                session['success_next_step'] = 2
                session['unlock_math'] = True
            else:
                fail_and_maybe_pause("math", "דילגת על החידה המתמטית ⏭️", 2)
            return redirect(url_for('index'))

        # ---- מעבר אחרי הצלחה ----
        if action == "continue_after_success":
            session.pop('unlock_math', None)  # ⭐️ חשוב – מנקה את המנעול
            session['step'] = session.pop('success_next_step')
            session['attempts'] = MAX_ATTEMPTS
            session['message'] = ""
            return redirect(url_for('index'))

        # ---- חידת מפה ----
        if action == "map_pick":
            if request.form.get("map_choice") == str(MAP_RIDDLE_ANSWER):
                session['progress'].append("מצאת את המספר על המפה✅")
                session['message'] = "פששש אתה מפתיע💖"
                session['success_next_step'] = 3
                session['step'] = "success"
            else:
                fail_and_maybe_pause("map", "דילגת על חידת המפה ⏭️", 3)
            return redirect(url_for('index'))

        # ---- חידת תמונות ----
        if action == "pic_submit":
            if request.form.get("pic_guess","").lower() == PIC_RIDDLE_ANSWER:
                session['progress'].append("פתרת את חידת התמונות✅")
                session['message'] = "רמז קשה, אני יכולה להיות קשורה להרבה דברים😈💖"
                session['success_next_step'] = 4
                session['step'] = "success"
            else:
                fail_and_maybe_pause("pic", "דילגת על חידת התמונות⏭️", 4)
            return redirect(url_for('index'))

        # ---- חידה טקסטואלית ----
        if action == "text_submit":
            if request.form.get("text_guess","").lower() == TEXT_RIDDLE_ANSWER:
                session['progress'].append("פתרת את החידה הטקסטואלית✅")
                session['message'] = "הפתעת אותי ממש אבל אל תתלהב, אפילו צ׳יקו היה מצליח קודם💖"
                session['success_next_step'] = 5
                session['step'] = "success"
            else:
                fail_and_maybe_pause("text", "דילגת על החידה הטקסטואלית ⏭️", 5)
            return redirect(url_for('index'))

        # מעבר אחרי כישלון
        if action == "continue_after_fail":
            session['step'] = session.pop('failed_next_step')
            session['attempts'] = MAX_ATTEMPTS
            session['message'] = ""
            return redirect(url_for('index'))

        # ---- ניחוש תאריך ----
        if action == "date_pick":
            if request.form.get("date_choice") == session['final_date']:
                session['progress'].append("ניחשת את התאריך הנכון💕")
                session['end_result'] = "success"
                session['step'] = 999
                session['message'] = ""
            else:
                session['attempts'] -= 1
                if session['attempts'] <= 0:
                    session['end_result'] = "fail"
                    session['message'] = FAIL_MESSAGES["date"][0]
                    session['step'] = 999
                else:
                    session['message'] = FAIL_MESSAGES["date"][session['attempts']]
            return redirect(url_for('index'))

        # מעבר אחרי הצלחה
        if action == "continue_after_success":
            session['step'] = session.pop('success_next_step')
            session['attempts'] = MAX_ATTEMPTS
            session['message'] = ""
            return redirect(url_for('index'))

    # מיקומי הכפתורים שעל המפה
    map_positions = [
        (6, "60%", "16%"), (7, "45%", "22%"), (8, "42%", "31%"),
        (5, "58%", "30%"), (9, "37%", "33%"), (4, "48%", "39%"),
        (3, "62%", "53%"), (2, "41%", "55%"), (1, "43%", "87%")
    ]

    return render_template(
        "game.html",
        step=session['step'],
        message=session.get('message', ""),
        pic_images=session.get('pic_images', []),
        map_positions=map_positions,
        final_date=session.get('final_date'),
        welcome_text=DEFAULT_WELCOME
    )


if __name__ == "__main__":
    app.run(debug=True, port=5004, host="0.0.0.0")

# --- כתובת ריסט לאתר ---
# http://localhost:5004/?reset=1
