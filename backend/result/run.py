import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import requests
from transformers.utils import hub
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Check device
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Customize requests session with retries and timeout
session = requests.Session()
retry_strategy = Retry(
    total=5,  # Max number of retries
    backoff_factor=1,  # Wait 1s, 2s, 4s, etc. between retries
    status_forcelist=[500, 502, 503, 504, 443],  # Retry on these HTTP errors
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)
session.timeout = 60  # Increase timeout to 60 seconds per request

# Patch transformers to use our custom session
original_get = hub.http_get
def custom_get(*args, **kwargs):
    kwargs["session"] = session
    return original_get(*args, **kwargs)
hub.http_get = custom_get

# Load fine-tuned model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("./opt_finetuned/opt-finetuned-adapters")
base_model = AutoModelForCausalLM.from_pretrained(
    "facebook/opt-2.7b",
    torch_dtype=torch.float16  # FP16 for lower memory
).to(device)
model = PeftModel.from_pretrained(base_model, "./opt_finetuned/opt-finetuned-adapters")
model.eval()

# Test prompts
prompts = [
    "Get all diseases with symptoms including cough",
    "List the top 1 doctors with the most medical records",
]

# Generate predictions
for prompt in prompts:
    input_text = f"### Prompt: {prompt}\n### Completion:"
    inputs = tokenizer(input_text, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=100,  # Your working setting
            do_sample=False,  # Your working setting
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.pad_token_id,
        )
    # Decode and extract just the query
    raw_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
    if "### Completion:" in raw_output:
        query_output = raw_output.split("### Completion:")[1].strip()
    else:
        query_output = raw_output.replace(input_text, "").strip()  # Fallback

    print(f"Prompt: {prompt}")
    print(query_output)  # Print only the query, no "Output:" label
    print("-" * 50)