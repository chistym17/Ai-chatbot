import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

# Load fine-tuned model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("./opt-finetuned-adapters")
base_model = AutoModelForCausalLM.from_pretrained(
    "facebook/opt-2.7b",
    torch_dtype=torch.float16
)
model = PeftModel.from_pretrained(base_model, "./opt-finetuned-adapters")
model.eval()

# Test prompt
prompt = "Patients with Diabetes diagnosed after 2023"
inputs = tokenizer(f"### Prompt: {prompt}\n### Completion:", return_tensors="pt")
with torch.no_grad():
    outputs = model.generate(**inputs, max_length=100)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))