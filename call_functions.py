from google.genai import types
from functions.get_files_info import schema_get_files_info,get_files_info
from functions.write_file import schema_write_file,write_file
from functions.run_python_file import schema_run_python_file ,run_python_file
from functions.get_files_content import schema_get_file_content,get_files_content

available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_write_file, schema_run_python_file, schema_get_file_content],
)

def call_function(function_call, verbose=False):
    if verbose :
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")
    func_map = {
        "get_file_content": get_files_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
        "get_files_info": get_files_info
    }

    func_name = function_call.name or ""

    if func_name not in func_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                name=func_name,
                response={"error": f"Unknown function: {func_name}"},
            )
        ],
    )
    args = dict(function_call.args) if function_call.args else {}

    args["working_directory"] = "./calculator"
    

    final_result = func_map[func_name](**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=func_name,
                response={"result": final_result},
            )
        ],
    )