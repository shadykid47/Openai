from flask import Flask, request, render_template
import transformers

app = Flask(__name__)
model = transformers.AutoModelWithLMHead.from_pretrained("facebook/opt-350m")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.form["user_input"]
    response = generate_response(model, user_input)
    return response

def generate_response(model, user_input):
    model = transformers.AutoModelForCausalLM.from_pretrained("facebook/opt-350m")
    tokenizer = transformers.AutoTokenizer.from_pretrained("facebook/opt-350m")
    input_ids = tokenizer.encode(user_input, return_tensors="pt", add_special_tokens=True)
    response = model.generate(input_ids)
    response_text = tokenizer.decode(response[0], skip_special_tokens=True)
    return response_text


if __name__ == "__main__":
    app.run(debug=True)
