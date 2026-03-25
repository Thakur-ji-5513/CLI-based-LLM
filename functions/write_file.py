import os
from google.genai import types

def write_file(working_directory, file_path, content):

    # making absolute path for the file
    abs_working = os.path.abspath(working_directory)
    abs_file = os.path.abspath(os.path.join(abs_working,file_path))

    #validating the files path

    if os.path.commonpath([abs_working,abs_file]) != abs_working:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    if os.path.isdir(abs_file):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    
    #making sure all the dirs exist in the path
    os.makedirs(file_path,exist_ok=True)

    # opening the file
    try:
        with open(abs_file,"w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as Error:
        return f'Error: {Error}'
    
    #schema for ai to call this


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="writes the content provided to a file who's path is provided",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to file that is to be written in, relative to the working directory",
            ),
            "content":types.Schema(
                type=types.Type.STRING,
                description="actual content that is supposed to be written in the file specified ",
            )
        },
    ),
)