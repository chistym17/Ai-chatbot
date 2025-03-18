from huggingface_hub import notebook_login, HfApi

# Authenticate
notebook_login()

# Define repository name
repo_name = "mynuddin/chatbot"

# Upload model
api = HfApi()
api.upload_folder(
    folder_path="./opt-finetuned-adapters",  # Your model directory
    repo_id=repo_name,
    repo_type="model"
)
