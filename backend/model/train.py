import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
from datasets import load_dataset
from peft import LoraConfig, get_peft_model

# Authenticate (replace with your token)

# Model and tokenizer
model_name = "facebook/opt-2.7b"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,  # Reduce to FP16
    device_map="cpu"
)

# Add padding token
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# Apply LoRA immediately
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)
model = get_peft_model(model, lora_config)

# Load dataset
dataset = load_dataset("json", data_files="working_data.jsonl", split="train")

# Preprocess with smaller max_length
def preprocess_function(examples):
    inputs = [f"### Prompt: {p}\n### Completion: {c}" for p, c in zip(examples["prompt"], examples["query"])]
    tokenized = tokenizer(inputs, padding="max_length", truncation=True, max_length=256, return_tensors="pt")
    tokenized["labels"] = tokenized["input_ids"].clone()
    return tokenized

tokenized_dataset = dataset.map(preprocess_function, batched=True, remove_columns=["prompt", "query"])

# Split dataset
train_size = int(0.9 * len(tokenized_dataset))
train_dataset = tokenized_dataset.select(range(train_size))
eval_dataset = tokenized_dataset.select(range(train_size, len(tokenized_dataset)))

# Training arguments
training_args = TrainingArguments(
    output_dir="./op-finetuned",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    num_train_epochs=3,
    learning_rate=2e-4,
    logging_steps=10,
    save_steps=50,
    evaluation_strategy="steps",
    eval_steps=50,
    max_grad_norm=0.3,
    report_to="none"
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
)

# Start training
print("Starting fine-tuning on CPU...")
trainer.train()

# Save model
model.save_pretrained("./opt-finetuned-adapters")
tokenizer.save_pretrained("./opt-finetuned-adapters")
print("Fine-tuning complete")


