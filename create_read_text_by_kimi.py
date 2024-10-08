import math 
import os
from openai import OpenAI
import subprocess
import argparse
import time

# MY_API_KEY = os.getenv('API_KEY')


def generate(my_api_key, my_base_url, my_model, filepath, levelname):
    print("Inside func::generate")

    correct_format_flag = False 
    # def generate():
    # Here, you can run any Python code you want to generate the response
    while (not correct_format_flag):
        client = OpenAI(
        api_key=my_api_key,  # 替换为你的API Key
        base_url=my_base_url,
        )

        user_prompt = """generate one French DELF """ + levelname + """level `COMPREHENSION DES ECRITS` exercise (which should include a context script and one to three sub-questions) and give the questions and answers in this json format 
                `[
                    {
                        "question": "...",
                        "options": [
                            "...",
                            "...",
                            "...",
                            "..."
                        ],
                        "correctAnswer": "..."
                    },
                    {
                        "question": "...",
                        "options": [
                            "...",
                            "...",
                            "...",
                            "..."
                        ],
                        "correctAnswer": "..."
                    },
                    {
                        "question": "...",
                        "options": [
                            "...",
                            "...",
                            "...",
                            "..."
                        ],
                        "correctAnswer": "..."
                    },
                    {
                        "question": "...",
                        "options": [
                            "...",
                            "...",
                            "...",
                            "..."
                        ],
                        "correctAnswer": "..."
                    }
                ]`. In the output, for the context script part, start with overhead `<script>` and end with `</script>`, for the exercise json part, start with overhead `<exercise>` and end with `</exercise>`

                """
        
        completion = client.chat.completions.create(
            model=my_model,  # 你可以选择不同的模型，如moonshot-v1-32k或moonshot-v1-128k
            messages=[
                {"role": "system", "content": "Please read delf-" + levelname.lower() + "-sample-papers. "},
                # {"role": "user", "content": "please generate a conversation about changing appointment"}
                # {"role": "user", "content": "Could you please generate three exercises of DELF A1 level Listening Comprehension about time. Please generate both the audio script and corresponding exercises"}
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            # stream=True,
        )

        response = completion.choices[0].message.content
        print(response)
        # print(filepath)

        #######################################################################
        ###   [Split the response into <audio script> part and <exercise> part]
        ###   > To extract the content between <script> and </script> tags 
        ###     and write it to a text.txt file, and to extract the content 
        ###     between <exercise> and </exercise> tags and write it to 
        ###     a qa.txt 
        #######################################################################
        import re

        # Define the regular expressions for the content you want to extract
        script_content_pattern = re.compile(r'<script>(.*?)</script>', re.DOTALL)
        exercise_content_pattern = re.compile(r'<exercise>(.*?)</exercise>', re.DOTALL)

        try:
            # Search for the content using the regular expressions
            script_content = script_content_pattern.search(response).group(1)
            exercise_content = exercise_content_pattern.search(response).group(1)
            correct_format_flag = True
        except:
            print("NOT A EXPECTED FORMAT")
            time.sleep(10)
            continue

    # print(script_content)
    # print('======')
    # print(exercise_content)
    # print('=========')

    # Write the extracted content to the respective files
    with open(filepath + '_text.txt', 'w', encoding='utf-8') as file:
        if script_content:
            file.write(script_content)
            print("Content has been written to text.txt")

    with open(filepath + '_questions.json', 'w', encoding='utf-8') as file:
        if exercise_content:
            file.write(exercise_content)
            print("Content has been written to qa.txt")


    # #####################################
    # ### Generate audio file with edge-tts
    # #####################################
    # run_edge_tts_command(script_content, filepath)



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
        print(".mp3 audio file has been generate successfully.")
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
    print(id)
    filepath = levelname + '_' + category + '_' + id
    print('filepath: ', filepath)
    generate(api_key, base_url, model, filepath, levelname)
