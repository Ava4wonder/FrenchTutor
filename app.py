from flask import Flask, render_template, jsonify, abort, send_file, request
from openai import OpenAI
from urllib.parse import quote
import math, random
import json
import subprocess



import os
# print(os.getcwd())
# print(os.getcwd() + '/template/index.html')

app = Flask(__name__, static_folder='static', template_folder='templates')

from flask_cors import CORS
CORS(app)

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

## 每个类目下的文件数
BASE_FILE_NUM = 10
# MY_API_KEY = os.getenv('API_KEY')
MY_API_KEY = "sk-LAbGx20bvcYb8SYYgOtIn2nprsuKlHhU76XULqOtMhfRk7P0"

# # Proxy route that forwards audio data to service2 (speech-to-text)
# @app.route('/proxy/recognize', methods=['POST'])
# def proxy_recognize():
#     try:
#         # Assuming you're sending an audio blob in the request
#         files = {'audio_data': request.files['audio_data']}  # Assuming the audio is sent as 'audio_data'

#         # Make an internal HTTP request to service2, available at 'http://service2:5002' in the Docker network
#         response = requests.post('http://service2:5002/recognize', files=files)

#         # Return the response from service2 to the frontend
#         return jsonify(response.json()), response.status_code
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
    

@app.route('/read_file/<filename>')
def read_file(filename):
    # 构建文件的完整路径
    file_path = os.path.join(PROJECT_PATH, filename)
    
    # 检查文件是否存在以及是否是文件
    if os.path.isfile(file_path):
        return send_file(file_path, mimetype='text/plain')
    else:
        # 如果文件不存在，返回404
        abort(404)


@app.route('/read_audio_file/<filename>')
def read_audio_file(filename):
    # 构建音频文件的完整路径
    file_path = os.path.join(PROJECT_PATH, filename)
    
    # 检查文件是否存在以及是否是文件
    if os.path.isfile(file_path):
        # 确定音频文件的MIME类型，这里以.mp3为例，根据实际情况可能需要调整
        mimetype = 'audio/wav'
        return send_file(file_path, mimetype=mimetype)
    else:
        # 如果文件不存在，返回404
        abort(404)


# Route for the homepage
@app.route('/')
def homepage():
    # return render_template('index.html')
    return render_template('homepage.html')

@app.route('/speech')
def speech():
    # return render_template('index.html')
    return render_template('speech.html')

@app.route('/oral')
def oral():
    # return render_template('index.html')
    return render_template('new_index.html')

# Route for the reading page
@app.route('/reading')
def reading():
    # return render_template('index.html')
    return render_template('reading.html')

# Route for the listening page
@app.route('/listening')
def listening():
    # return render_template('index.html')
    return render_template('listening.html')

# Route for the notebook page
@app.route('/notebook')
def notebook():
    # return render_template('index.html')
    return render_template('notebook.html')

# Route for the vocabreplay page
@app.route('/vocabreplay')
def vocabreplay():
    # return render_template('index.html')
    return render_template('vocabreplay.html')


# from openai import OpenAI
@app.route('/generate', methods=['GET'])
def generate():
    # Here, you can run any Python code you want to generate the response
    client = OpenAI(
    # api_key="sk-LAbGx20bvcYb8SYYgOtIn2nprsuKlHhU76XULqOtMhfRk7P0",  # 替换为你的API Key
    api_key=MY_API_KEY,  # 替换为你的API Key
    base_url="https://api.moonshot.cn/v1",
    )

    completion = client.chat.completions.create(
        model="moonshot-v1-8k",  # 你可以选择不同的模型，如moonshot-v1-32k或moonshot-v1-128k
        messages=[
            {"role": "system", "content": "Please create french exam DELF A1 corresponding level of daily conversation or annonce or broadcast of some other specified topics. Those words used here should be simple. Or if prompt with random, then generate a conversation from one of the following topics: (1) self introduction, (2) exchange information, (3) role play or say simulated dialog. Please use english to present the non-conversation-body part. Please show the conversation body only and show the corresponding role name in French in the conversation body."},
            # {"role": "user", "content": "please generate a conversation about changing appointment"}
            # {"role": "user", "content": "Could you please generate three exercises of DELF A1 level Listening Comprehension about time. Please generate both the audio script and corresponding exercises"}
            {"role": "user", "content": "random"}
        ],
        temperature=0.5,
        # stream=True,
    )

    response = completion.choices[0].message.content
    # response = "Hello yabiyobi"
    return response

##########################
### [Func] kimi_oral_agent 
##########################
@app.route('/oralagent', methods=['POST'])
def oralAgent():
    # Here, you can run any Python code you want to generate the response
    client = OpenAI(
    # api_key="sk-LAbGx20bvcYb8SYYgOtIn2nprsuKlHhU76XULqOtMhfRk7P0",  # 替换为你的API Key
    api_key=MY_API_KEY,  # 替换为你的API Key
    base_url="https://api.moonshot.cn/v1",
    )

    system_prompt = """现在是DELF B1等级的口语模拟考试中的其中一轮. 
                    提示词用<prompt>和</prompt>进行标识，已进行的上下文用<context>和</context>进行标识。
                    作为一位经验丰富的 DELF-B1 口语考试专家，您将首先分析样本试卷：您将阅读并分析 DELF-B1 口语考试的样本试卷，
                    以便熟悉考试的具体范围、主题和关键评估点。您将扮演考官的角色，给出与当前上下文相匹配的一次回答，
                    按照考试流程完成评估。"""

    data = request.get_json()
    user_prompt = data.get('temp_user_prompt')


    completion = client.chat.completions.create(
        model="moonshot-v1-8k",  # 你可以选择不同的模型，如moonshot-v1-32k或moonshot-v1-128k
        messages=[
            {"role": "system", "content": system_prompt},
            # {"role": "user", "content": "please generate a conversation about changing appointment"}
            # {"role": "user", "content": "Could you please generate three exercises of DELF A1 level Listening Comprehension about time. Please generate both the audio script and corresponding exercises"}
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.5,
        # stream=True,
    )

    response = completion.choices[0].message.content
    # response = "Hello yabiyobi"
    return response

###############
### [PAGE] oral
###############
@app.route('/generatenew', methods=['GET'])
def generatenew():
    category = 'oral'
    # 生成随机数并填充
    id = str(math.floor(random.random() * BASE_FILE_NUM)).zfill(3)
    # id = '000'
    # relative_path = 'assets'
    
    # # 打开BerkeleyDB
    # with dbm.open(DB_PATH, 'r') as db:
    #     # 根据ID获取文件路径
    #     file_path = db.get(random_number)

    level = request.args.get('level', '')  # Get the level parameter from the query string

    text_path = level + '_' + category + '_' + id + '.txt'

    # text_path = os.path.join(relative_path, id, file_path)

    # # 读取文本文件内容
    # with open(file_path, 'r', encoding='utf-8') as file:
    #     text_content = file.read()
    
    # 假设你的语音文件和文本文件在同一目录下，并且文件名相同，只是扩展名为.wav
    audio_path = level + '_' + category + '_' + id + '.mp3'
    
    # 返回文本内容和语音文件路径
    return jsonify({
        'text': text_path,
        'audioPath': audio_path
    })

##################
### [PAGE] reading
##################
@app.route('/generatereadingexer', methods=['GET'])
def generatereadingexer():
    category = 'read'
    # 生成随机数并填充
    id = str(math.floor(random.random() * BASE_FILE_NUM)).zfill(3)
    # id = '000'
    # relative_path = 'assets'
    
    # # 打开BerkeleyDB
    # with dbm.open(DB_PATH, 'r') as db:
    #     # 根据ID获取文件路径
    #     file_path = db.get(random_number)

    level = request.args.get('level', '')  # Get the level parameter from the query string

    text_path = level + '_' + category + '_' + id + '_text' + '.txt'
    qa_path = level + '_' + category + '_' + id + '_questions' + '.json'

    # text_path = os.path.join(relative_path, id, file_path)

    # # 读取文本文件内容
    with open(text_path, 'r', encoding='utf-8') as file:
        text_content = file.read()

    # with open(qa_path, 'r', encoding='utf-8') as file:
    with open(qa_path, 'r', encoding='utf-8') as file:
        qa_content = json.load(file)
        # qa_content = file.read()
    
    # 假设你的语音文件和文本文件在同一目录下，并且文件名相同，只是扩展名为.wav
    # audio_path = category + '_' + id + '.wav'
    
    # 返回文本内容和语音文件路径
    return jsonify({
        'text_content': text_content,
        'qa_content': qa_content
    })
    # return text_content, qa_content
    # return jsonify({'text_content': text_content})

#################
### [PAGE] listen
#################
@app.route('/generatelisten', methods=['GET'])
def generatelisten():
    category = 'listen'
    # 生成随机数并填充
    id = str(math.floor(random.random() * BASE_FILE_NUM)).zfill(3)
    # id = '000'
    level = request.args.get('level', '')  # Get the level parameter from the query string
    
    text_path = level + '_' + category + '_' + id + '_text' + '.txt'
    qa_path = level + '_' + category + '_' + id + '_questions' + '.json'
    audio_path = level + '_' + category + '_' + id + '.mp3'

    # 读取文本文件内容
    with open(text_path, 'r', encoding='utf-8') as file:
        text_content = file.read()

    # 读取问答内容
    with open(qa_path, 'r', encoding='utf-8') as file:
        qa_content = json.load(file)

    
    # 返回文本内容和语音文件路径
    return jsonify({
        'text_content': text_content,
        'audio_path': audio_path,
        'qa_content': qa_content
    })


#######################################
### [PAGE] check different level files
#######################################
@app.route('/checklevelfiles', methods=['GET'])
def checklevelfiles():
    # Define the command and arguments
    level = request.args.get('level', '')  # Get the level parameter from the query string

    command = 'python'
    # arguments = ['run_script_read.py', '--iternum', '10']

    # Get the current working directory
    current_directory = os.getcwd()

    # Check whether corresponding level exercises exist
    i = BASE_FILE_NUM - 1
    id = str(i).zfill(3)
    file_name_oral = level + '_oral_' + id + '.txt'
    file_name_listen = level + '_listen_' + id + '_text.txt'
    file_name_read = level + '_read_' + id + '_text.txt'

    file_path_oral = os.path.join(current_directory, file_name_oral)
    file_path_listen = os.path.join(current_directory, file_name_listen)
    file_path_read = os.path.join(current_directory, file_name_read)

    generated = False
    
    # Check if the file exists
    if os.path.isfile(file_path_oral):
        print('>>>>>> DELF' + level + 'level <ORAL> exercises have been generated successfully!! <<<<<<')
        pass
    else:
        print(f" ===== Start to generate DELF {level} oral exercises =====")
        arguments = ['run_script_oral.py', '--iternum', '10', '--level', level]
        result = subprocess.run([command] + arguments, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Check if the command was successful
        if result.returncode == 0:
            print('>>>>>> DELF' + level + 'level <ORAL> exercises have been generated successfully!! <<<<<<')
            generated = True
            

    if os.path.isfile(file_path_listen):
        print('>>>>>> DELF' + level + 'level <LISTENING> exercises have been generated successfully!! <<<<<<')
        pass
    else:
        print(f" ===== Start to generate DELF {level} listening exercises =====")
        arguments = ['run_script_listen.py', '--iternum', '10']
        result = subprocess.run([command] + arguments, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Check if the command was successful
        if result.returncode == 0:
            print('>>>>>> DELF' + level + 'level <LISTENING> exercises have been generated successfully!! <<<<<<')
            generated = True

    if os.path.isfile(file_path_read):
        print('>>>>>> DELF' + level + 'level <READING> exercises have been generated successfully!! <<<<<<')
        pass
    else:
        print(f" ===== Start to generate DELF {level} reading exercises =====")
        arguments = ['run_script_read.py', '--iternum', '10']
        result = subprocess.run([command] + arguments, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Check if the command was successful
        if result.returncode == 0:
            print('>>>>>> DELF' + level + 'level <READING> exercises have been generated successfully!! <<<<<<')
            generated = True

    return jsonify({'result': 1 if generated else 0})

        
if __name__ == '__main__':
    # Get the port from environment variables or default to 5000
    # port = int(os.environ.get('PORT', 5000))
    
    # Bind to 0.0.0.0 to allow access from outside the container
    # app.run(host="0.0.0.0", port=port)
    app.run(debug=True, host='127.0.0.1', port=5001)
    # app.run(debug=True)
