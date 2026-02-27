import os
import requests
import pandas as pd
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import context_precision, faithfulness
from dotenv import load_dotenv

load_dotenv()

def main():
    dataset_path = "data/evaluation/synthetic_dataset.csv"
    if not os.path.exists(dataset_path):
        print(f"Dataset not found at {dataset_path}")
        return

    print(f"Loading dataset from {dataset_path}...")
    df = pd.read_csv(dataset_path)
    
    questions = []
    contexts_list = []
    ground_truths_single = []
    ground_truths_list = []
    answers = []
    
    print(f"Processing {len(df)} questions...")
    for idx, row in df.iterrows():
        question = row["question"]
        ground_truth = str(row["ground_truth_context"])
        
        try:
            response = requests.post(
                "http://localhost:8000/search",
                json={"query": question, "top_k": 5}
            )
            response.raise_for_status()
            results = response.json().get("results", [])
            contexts = [res["text"] for res in results]
        except Exception as e:
            print(f"Error querying API for question {idx}: {e}")
            contexts = []
            
        questions.append(question)
        contexts_list.append(contexts)
        ground_truths_single.append(ground_truth)
        ground_truths_list.append([ground_truth])
        
        if contexts:
            answers.append(contexts[0])
        else:
            answers.append("No answer found due to empty contexts.")

    data_dict = {
        "question": questions,
        "contexts": contexts_list,
        "ground_truth": ground_truths_single,
        "ground_truths": ground_truths_list,
        "answer": answers
    }
    
    dataset = Dataset.from_dict(data_dict)
    
    print("Running evaluation with ragas (context_precision, faithfulness)...")
    try:
        result = evaluate(
            dataset=dataset,
            metrics=[context_precision, faithfulness]
        )
    except Exception as e:
        print(f"Error during Ragas evaluate: {e}")
        return
        
    print("\n--- Evaluation Results ---")
    print(result)
    
    os.makedirs("data/evaluation", exist_ok=True)
    out_path = "data/evaluation/eval_results_latest.csv"
    result_df = result.to_pandas()
    result_df.to_csv(out_path, index=False)
    print(f"\nDetailed results saved to {out_path}")

if __name__ == "__main__":
    main()
