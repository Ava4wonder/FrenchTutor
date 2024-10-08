import subprocess
import argparse
import time

def run_script_read(total_iter, levelnum):
    for i in range(total_iter):
        command = [
                "python", 
                "create_read_text_by_kimi.py", 
                "--category", "read", 
                "--iteration", str(i),
                "--level", levelnum
            ]
        
        # Run the command
        result = subprocess.run(command, capture_output=True, text=True)
        
        # Print the output and any errors
        if result.returncode == 0:
            print("=== SUCCESS ===")
            print("Output:", result.stdout)
        else:
            print("[!!!] FAIL: ")
            print(result.stderr)
        time.sleep(30)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the script with specified <iteration>.")
    
    # Add arguments
    parser.add_argument("--iternum", type=int, required=True, help="total iterations to run.")
    parser.add_argument("--level", type=str, required=False, default='B1', help="The expected DELF level.")

    # Parse the arguments
    args = parser.parse_args()
    
    total_iter = args.iternum
    levelnum = args.level

    run_script_read(total_iter, levelnum)