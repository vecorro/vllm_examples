import requests

prompt = "What colour is the sky?"
sample_input = {"prompt": prompt, "stream": True}
output = requests.post("http://localhost:8000/", json=sample_input)
for line in output.iter_lines():
    print(line.decode("utf-8"))