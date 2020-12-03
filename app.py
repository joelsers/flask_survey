from flask import Flask, request, render_template, redirect, flash, session

from flask_debugtoolbar import DebugToolbarExtension

from surveys import satisfaction_survey as survey

RESPONSES_KEY = 'responses'

app = Flask(__name__)

app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def show_home():
    return render_template('home.html', survey = survey)

@app.route('/start', methods=['POST'])
def start_survey():

    session[RESPONSES_KEY] = []

    return redirect('/questions/0')

@app.route('/answer', methods = ["POST"])
def answer():

    choice = request.form['answer']

    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")

@app.route('/questions/<int:num>')
def show_question(num):
    responses = session.get(RESPONSES_KEY)
    if (responses is None):
        # trying to access question page too soon
        return redirect("/")
    if (len(responses) == len(survey.questions)):
        return redirect("/complete")

    if (len(responses) != num):
        return redirect(f"/questions/{len(responses)}")

    question =  survey.questions[num] 
    return render_template('question.html', question_num = num, question = question)


@app.route("/complete")
def survey_complete():
    return render_template('complete.html')
