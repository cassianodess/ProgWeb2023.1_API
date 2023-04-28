import openai


class OpenAI:
    def __init__(self, organization, api_key, model):
        self.organization = organization
        self.api_key = api_key
        self.model = model
        self.chat_history = []

    def create_response(self, question):
        prompt = "Conversation history:\n" + "\n".join(self.chat_history)
        prompt += f"\nUser: {question}"
        
        prompt_tokens = len(prompt.split())
        if prompt_tokens > 4096:
            prompt = " ".join(prompt.split()[-4096:])

        openai.api_key = self.api_key
        openai.organization = self.organization
        response = openai.Completion.create(
            engine=self.model,
            prompt=prompt,
            temperature=0.7,
            max_tokens=2048,
            n=1,
            stop=None,
            frequency_penalty=0,
            presence_penalty=0
        )
        answer = response.choices[0].text.strip()
        self.chat_history.append(f"User: {question}\nAI: {answer}")
        return answer
