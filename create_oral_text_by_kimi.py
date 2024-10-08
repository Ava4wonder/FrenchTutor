import math 
import os
from openai import OpenAI
import subprocess
import argparse

# MY_API_KEY = os.getenv('API_KEY')


def generate(my_api_key, my_base_url, my_model, filepath, levelname):
# def generate():
    # Here, you can run any Python code you want to generate the response
    client = OpenAI(
    api_key=my_api_key,  # 替换为你的API Key
    base_url=my_base_url,
    )

    completion = client.chat.completions.create(
        model=my_model,  # 你可以选择不同的模型，如moonshot-v1-32k或moonshot-v1-128k
        messages=[
            {"role": "system", "content": "Please search some French DELF" + levelname +  "past papers."},
            # {"role": "user", "content": "please generate a conversation about changing appointment"}
            # {"role": "user", "content": "Could you please generate three exercises of DELF A1 level Listening Comprehension about time. Please generate both the audio script and corresponding exercises"}
            {"role": "user", "content": "Then according to these exercises, please generate a standard" + levelname + "level oral script which could get high score."}
        ],
        temperature=0.7,
        # stream=True,
    )

    response = completion.choices[0].message.content
    print(filepath)
    # Save the response to a file
    with open(filepath + '.txt', 'w') as file:
        file.write(response)

    #####################################
    ### Generate audio file with edge-tts
    #####################################
    run_edge_tts_command(response, filepath)



def run_edge_tts_command(text, filepath):
    # Define the command as a list of arguments
    command = [
        "edge-tts", 
        "--voice", "fr-FR-DeniseNeural", 
        "--text", text,
        "--write-media", filepath + ".mp3",
        "--write-subtitles", filepath + ".vtt"
    ]

    # Run the command
    result = subprocess.run(command, capture_output=True, text=True)

    # Print the output and any errors
    if result.returncode == 0:
        print("Command executed successfully.")
        print("Output:", result.stdout)
    else:
        print("Command failed with error:")
        print(result.stderr)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the script with category and iteration arguments.")
    
    # Add arguments
    parser.add_argument("--category", type=str, required=True, help="The category name for the output file.")
    parser.add_argument("--iteration", type=int, required=True, help="The iteration number for generating the file name.")
    parser.add_argument("--level", type=str, default='B1', required=False, help="Please specify the level.")
    
    # Parse the arguments
    args = parser.parse_args()


    api_key="sk-LAbGx20bvcYb8SYYgOtIn2nprsuKlHhU76XULqOtMhfRk7P0"
    # api_key = MY_API_KEY
    base_url = "https://api.moonshot.cn/v1"
    model = "moonshot-v1-8k"
    category = args.category
    iteration = args.iteration
    levelname = args.level
    id = str(math.floor(iteration)).zfill(3)
    filepath = levelname + '_' + category + '_' + id
    generate(api_key, base_url, model, filepath, levelname)
