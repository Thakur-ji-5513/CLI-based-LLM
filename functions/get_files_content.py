import os
from config import MAX_CHARS
from google.genai import types

def get_files_content(working_directory, file_pth):
    #xraeting abs path for both file and dir
    abs_working_directory = os.path.abspath(working_directory)
    abs_file = os.path.abspath(os.path.join(abs_working_directory,file_pth))


    #checking if the file exists in the dir or not
    if os.path.commonpath([abs_working_directory,abs_file]) != abs_working_directory:
        return f'Error: Cannot read "{file_pth}" as it is outside the permitted working directory'
    
    #checking if the file even exists or not
    if not os.path.isfile(abs_file):
        return f'Error: File not found or is not a regular file: "{file_pth}"'
    
    #reading the file

    try:
        with open(abs_file,"r") as f:
            file_content = f.read(MAX_CHARS)
            check = f.read(1)
            if check == "" or check == None:
                return file_content
            else:
                return  file_content + f'[...File "{file_pth}" truncated at {MAX_CHARS} characters]'
    
    except Exception as e:
        return f'   Error:{e}'
    
    #again, the schema for making a call to this fnc by our AI

schema_get_file_content = types.FunctionDeclaration(
    name= "get_file_content",
    description="it retrives the contents that are inside the file whose path is provided",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_pth": types.Schema(
                type=types.Type.STRING,
                description="Directory path to the file whose content is supposed to be retreived",
            ),
        },
    )
)
