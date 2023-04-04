from flask import Flask,render_template,jsonify,request

import sys
import os
path = os.path.abspath(r"C:\\Users\\Asus\Desktop\\smartBotFlask\\Project - Chitti")
sys.path.append(path)
# adding Folder_2/subfolder to the system path

import main

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/chatbot', methods=["GET", "POST"])
def chatbotResponse():
    if request.method == 'POST':
        the_question = request.form['question']
        print(the_question)
    response = 'Hi there, Please try again.'
    try:
        response = main.generate_response(the_question)
    except:
        pass
    return jsonify({"response": response })

if __name__ == '__main__':
    app.run(debug=True)

