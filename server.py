from flask import Flask, jsonify, request
from github import Github, UnknownObjectException, RateLimitExceededException
import re
from flask_cors import CORS
import sys

print(sys.path)

app = Flask(__name__)
CORS(app)
git_object = Github() # When sensitive data then .env should be used
git_user = "Kodex-AI"

@app.route('/',methods=['GET'])
def hello():
    return jsonify({"response":"This is Kodex AI Analysis"})
# Repos API Route
@app.route("/repos")
def members():
    try:
        print(sys.path)
        user = git_object.get_user(git_user)
        repository = user.get_repo('coding-challenges-input')
        source_file_content = repository.get_contents("python-challenge")
        repos_send = str(source_file_content)
        regexed_response_send = re.findall( r'/(.*?)\"',repos_send)
        return {"repos": regexed_response_send}
    except UnknownObjectException as e:
        print(e.status)
        print("Unknown object exception")
        return {"repos": ["Exception","Unknown Object"]}
    except RateLimitExceededException as e:
        print(e.status)
        print("Rate Limit Exceeded")
        return {"repos": ["Exception","Rate Limit Exceeded"]}

# Fetch-Analysis API Route
@app.route('/fetch-analysis', methods=['POST'])
def fetching():
    file_name = request.get_json()
    data_requested_file_name = str(file_name)
    user = git_object.get_user(git_user)
    repository = user.get_repo('coding-challenges-input')
    source_file_content = repository.get_contents("python-challenge/"+file_name).decoded_content
    source_code = str(source_file_content)
    source_code = source_code.replace(" ","").replace("\\n","").replace("\\","")
    # Classifying_Model
    found_hidden_layer = source_code.count("model.add(Dense(")
    relu_count = source_code.count("activation='relu'")
    sigmoid_count = source_code.count("activation='sigmoid'")
    output_message = ""
    if found_hidden_layer > 0:
        if found_hidden_layer >0 and found_hidden_layer <= 9: classifying_severity = "posing a low transparency risk"
        elif found_hidden_layer >= 10 and found_hidden_layer < 20: classifying_severity = "posing a medium transparency risk"
        elif found_hidden_layer >= 20: classifying_severity = "posing a high transparency risk"
        output_message = "Found deep neural network with "+ str(found_hidden_layer) +" hidden layers in " + data_requested_file_name \
        + " (" + str(sigmoid_count) + " sigmoid activation functions, " + str(relu_count) + " relu activation functions), " + classifying_severity
    else: 
        output_message = "No hidden layers found in "+ data_requested_file_name
    return {"message":output_message}

if __name__ == "__main__":
    app.run(host="0.0.0.0",threaded=True,port=5000) # As we are in Dev envrionment