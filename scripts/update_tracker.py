import os

path = "/Users/shanyu/.gemini/antigravity/brain/f28f1f0b-8c16-49a8-84a1-329681970c72/task.md"
with open(path, "r") as f:
    text = f.read()

text = text.replace("- [ ] Execute Task 1: Generate Sparse Vectors (BM25)", "- [x] Execute Task 1: Generate Sparse Vectors (BM25)")

with open(path, "w") as f:
    f.write(text)
print("Updated tracker")
