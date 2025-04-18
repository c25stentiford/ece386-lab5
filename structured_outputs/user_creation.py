'''Passes a personal intro statement to an LLM.
The LLM produces valid JSON that could be ingested into a database to create a new user.

Modified from https://ollama.com/blog/structured-outputs
'''
from ollama import chat
from pydantic import BaseModel
import sys

class User(BaseModel):
  name: str
  occupation: str
  age: int
  taken: bool
  hometown: str

response = chat(
  messages=[
    {
      'role': 'system',
      'content': "Your purpose to interpret the user's statement or \
        statements about himself or herself and output JSON in the specified format with information about the user.\
            Be concise. If the user omits a piece of information, fill in the field with \"Unknown\" (for age, use 0\
                for unknown and for `taken`, assume false).",
    }, {
        'role': 'user',
        'content': sys.argv[1]
    }
  ],
  model='deepseek-r1:14b',
  format=User.model_json_schema(),
)

user = User.model_validate_json(response.message.content)
print(user)