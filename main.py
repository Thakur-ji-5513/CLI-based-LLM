import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from promts import system_prompt
from call_functions import available_functions,call_function
import sys

def main():
    # loading api
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        print("loaded!")
    else:
        raise RuntimeError
        return
    
    # after api loaded
    client = genai.Client(api_key = api_key)
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    for _ in range(20):
        response = client.models.generate_content(
            model='gemini-2.5-flash', contents=messages,
            config=types.GenerateContentConfig(system_instruction=system_prompt, temperature=0, tools= [available_functions]),
        )

        candidate = response.candidates
        if candidate != None:
            for cand in candidate:
                messages.append(cand.content)


        if args.verbose:
            print(f'User prompt: {args.user_prompt}')
            print(f'Prompt tokens:{response.usage_metadata.prompt_token_count}  \nResponse tokens: {response.usage_metadata.candidates_token_count}')
        func_called = response.function_calls

        if func_called != None:
            func_res = []
            for function in func_called:
                returned_res = call_function(function, verbose= args.verbose)
                if len(returned_res.parts) == 0:
                    raise Exception
                if returned_res.parts[0].function_response == None:
                    raise Exception
                if returned_res.parts[0].function_response.response == None:
                    raise Exception
                func_res.append(returned_res.parts[0])
                if args.verbose:
                    print(f"-> {returned_res.parts[0].function_response.response}")
            messages.append(types.Content(role="user", parts=func_res))
        else:
            print("Final response:")
            print(response.text)
            return
    print("Maximum iterations reached without a final response")
    sys.exit(1)

if __name__ == "__main__":
    main()