from narration import parse

response_path = 'shorts/1720846468/response.txt'
with open(response_path, 'r') as f:
    response_text = f.read()
    print(response_text)

data, narrations = parse(response_text)

print(data)