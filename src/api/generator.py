import openai
from typing import List

class TaxGenerator:
    def __init__(self):
        self.client = openai.OpenAI()
        self.system_prompt = (
            "You are an expert Certified Public Accountant (CPA) answering US Tax questions. "
            "You will be provided with a user's question and relevant sections of the US Tax Code. "
            "Answer the question using ONLY the provided code sections. If the answer is not in the "
            "provided text, reply strictly with 'I cannot answer this based on the provided tax code'."
        )

    def generate_answer(self, query: str, contexts: List[str]) -> str:
        joined_contexts = "\n\n".join(contexts)
        user_message = (
            f"Query: {query}\n\n"
            f"Contexts:\n{joined_contexts}"
        )
        
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_message}
            ]
        )
        return response.choices[0].message.content
