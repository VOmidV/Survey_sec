from flask import Flask, render_template, request, redirect, flash, session
from surveys import satisfaction_survey as survay
app = Flask(__name__)

RESPONSES_KEY = "responses"

@app.route('/')
def home():
  title = survay.title
  instruction = survay.instructions
  return render_template('home.html', title=title, inst=instruction)

@app.route("/start", methods=["POST"])
def start_survey():
    session[RESPONSES_KEY] = []
    return redirect("/questions/0")

@app.route('/questions/<num>')
def question(num):
  number = int(num)
  responses = session.get(RESPONSES_KEY)

  if(number == len(responses)):
    return render_template('questions.html', question=survay.questions[number].question, choice=survay.questions[number].choices)
  
  if(number != len(responses)):
    flash(f'Wrong URL')
    return redirect(f'/questions/{len(responses)}')
  
  if (responses is None):
    return redirect("/")

@app.route('/ans', methods=["POST"])
def answer():
  responses = session.get(RESPONSES_KEY)
  answ = request.form['choices']
  responses.append(answ)
  session[RESPONSES_KEY] = responses
  if(len(responses) < len(survay.questions)):
    return redirect(f'/questions/{len(responses)}')
  else:
    return redirect('/complite')

@app.route('/complite')
def comp():
  return render_template('complite.html')
