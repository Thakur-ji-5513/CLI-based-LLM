import os
import sys
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    #creating abs paths
    abs_dir = os.path.abspath(working_directory)
    abs_file = os.path.abspath(os.path.join(abs_dir,file_path))

    #validating the paths
    if os.path.commonpath([abs_dir,abs_file]) != abs_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(abs_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    
    if not abs_file.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'
    
    try:
        command = ["python3", abs_file]
        if args :
            command.extend(args)
        returned_obj = subprocess.run(command,cwd= abs_dir, text=True, timeout=30, capture_output=True)
        code = returned_obj.returncode
        ans=""
        if code !=0:
            ans = f'Process exited with code {code}\n'
        if not returned_obj.stderr  and not returned_obj.stdout:
            ans = ans + "No output produced"
            return ans
        else:
            ans = ans + f'STDOUT: {returned_obj.stdout}' + "\n" + f'STDERR: {returned_obj.stderr}'
            return ans


    except Exception as Error:
        return f"Error: executing Python file: {Error}"

#schema for calling this function by our ai

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="runs the python file whose path is provided",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to file that is to be executed",
            ),
            "args":types.Schema(
                type=types.Type.STRING,
                description="arguments that are to be provided while making the run call to the specified python file,(default is none/empty)",
            )
        },
    ),
)