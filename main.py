from fastapi import FastAPI, HTTPException, Query,Form
import openai
import replicate

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


llama2 = "meta/llama-2-13b-chat:f4e2de70d66816a838a89eeeb621910adffb0dd0baba3976c96980970978018d"

def LLamaChatCompletion(replicate_key,prompt, system_prompt=None):
    api = replicate.Client(api_token=replicate_key)
    output = api.run(
    llama2,
    input={"system_prompt": system_prompt,
            "prompt": prompt,
            "temperature": 0.1,
            "max_new_tokens":12000}
    )
    return "".join(output)


def get_answer(replicate_key,system_prompt, prompt):
    return LLamaChatCompletion( replicate_key=replicate_key,prompt=prompt, system_prompt=system_prompt)


@app.post("/explain_cobol_code")
def explain_code(
                                replicate_key: str = Form(...),
                                system_prompt: str = Form(...),
                                filename: str = Form(...),
                                prompt: str = Form(...),
                            ):

    system_prompt = """
            You are an expert in COBOL. Write a summary for the code in about 100 words. 
            Do not exceed 150 words.

            Just describe in english what is happenning in this code.

            Start your answer with '
                Here is the description of the selected code:'
        """
    try:
        replicate_key = replicate_key
        response = get_answer(replicate_key, system_prompt, prompt)
        print(response)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))