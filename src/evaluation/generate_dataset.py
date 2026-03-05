import os
import random
import pandas as pd
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from openai import OpenAI

load_dotenv()

def main():
    qdrant = QdrantClient(url=os.getenv("QDRANT_URL", "http://localhost:6333"), api_key=os.getenv("QDRANT_API_KEY"))
    collection_name = "tax_code_chunks"
    
    print("Fetching chunks from Qdrant...")
    records, _ = qdrant.scroll(
        collection_name=collection_name,
        limit=1000,
        with_payload=True,
        with_vectors=False
    )
    
    if len(records) < 50:
        print(f"Warning: Only found {len(records)} chunks in Qdrant. Using all available chunks.")
        sample_records = records
    else:
        sample_records = random.sample(records, 50)
        
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    dataset = []
    
    print(f"Generating synthetic questions for {len(sample_records)} chunks using gpt-4o-mini...")
    for i, record in enumerate(sample_records):
        payload = record.payload or {}
        chunk_text = payload.get("text", "")
        section_number = payload.get("section_number", "")
        chunk_id = str(record.id)
        
        prompt = f"You are a taxpayer. Read this section of the US Tax Code: {chunk_text}. Write exactly 1 realistic, complex question that this law answers. Return only the question."
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=150
            )
            question = response.choices[0].message.content.strip()
            
            # Remove enclosing quotes if the model added them
            if question.startswith('"') and question.endswith('"'):
                question = question[1:-1]
            
            dataset.append({
                "question": question,
                "ground_truth_context": chunk_text,
                "section_number": section_number
            })
            
            if (i+1) % 10 == 0:
                print(f"Processed {i+1}/{len(sample_records)} chunks.")
                
        except Exception as e:
            print(f"Error generating question for chunk {chunk_id}: {e}")
            
    output_dir = "data/evaluation"
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, "synthetic_dataset.csv")
    df = pd.DataFrame(dataset)
    df.to_csv(output_path, index=False)
    
    print(f"Successfully saved {len(dataset)} items to {output_path}")

if __name__ == "__main__":
    main()
