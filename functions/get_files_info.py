import os
from google.genai import types

def get_files_info(working_directory, directory="."):

    abs_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_directory,directory))
    # ... build target_dir ...
    if os.path.commonpath([abs_working_dir, target_dir]) != abs_working_dir:
        return f'   Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_dir):
        return f'   Error: "{directory}" is not a directory'
    
    try:
        sub_list = os.listdir(target_dir)
        final_info = ""
        for item in sub_list:
                curr_name = item
                curr_size = os.path.getsize(os.path.join(target_dir,item))
                is_dir = os.path.isdir(os.path.join(target_dir,item))
                final_info = final_info + f'- {curr_name}: file_size={curr_size} bytes, is_dir={is_dir}\n' 
        return final_info[:-1]
    except Exception as E:
        return f'{E}'
    

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)