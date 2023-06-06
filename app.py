from flask import Flask, render_template, request
import openai
import pyttsx3
# import speech_recognition as sr


app = Flask(__name__)

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.save_to_file(text, 'static/output.mp3')
    engine.runAndWait()
    return 'output.mp3'


health_conditions = [
    "Common Illness",
    "Chronic Conditions",
    "Mental Health",
    "General Symptoms",
    "Physical Wounds"
]


openai.api_key = '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'

@app.route('/')
def index():
    return render_template('index.html', health_conditions=health_conditions)

@app.route("/api002", methods=["POST"])
def api002():
    health_condition = request.form.get("health_conditions")
    illness = request.form.get("illness")
    severity = request.form.get("severity")
    message = f"{health_condition}, I have {severity} {illness}, how can i relieve myself"
    print(message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": message}
        ]
    )
    text = ""
    if response.choices[0].message != None:
        result = response.choices[0].message["content"]
        text = result+". You can also tell me more about your symptoms"
        
        if "However," in result:
            result003 = str(result.split("However, ")[1])
            result = result003.capitalize()+" \nHowever, "+ str(result.split("However, ")[0])
        speech = text_to_speech(text)
        return render_template('index.html', health_conditions=health_conditions, result=result, speech="TEMPBOT/output.mp3")



@app.route("/api", methods=["POST"])
def api():
    data = request.get_json() 

    message = data.get("message")

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": message}
        ]
    )

    if completion.choices[0].message != None:
        content = completion.choices[0].message["content"]
        isCodeBlock = "```" in content 
        return {"content": content, "isCodeBlock": isCodeBlock}

    else:
        return {"content": 'Failed to generate response!', "isCodeBlock": False}

if __name__=='__main__':
    app.run(debug=False, host='0.0.0.0')

