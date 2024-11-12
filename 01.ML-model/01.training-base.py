# Steps used (Note: Untested): 
# 1. Get the prompt in VSCode for structures needed in here
# 2. Using WSL2 created ipynb version and used for training
# Notes:
# - it can generate 2 sections (e.g. first prompt didnt have torch/trl, second prompt added it at top)

# ---------------------------------------------------------
# Qn: load load llama 3.2 1B for training
from transformers import LlamaForCausalLM, LlamaTokenizer
import torch
import trl
import warnings
from datasets import load_dataset
from unsloth import FastLanguageModel, Trainer
from transformers import TrainingArguments
from unsloth import SFTTrainer
from huggingface_hub import HfApi, HfFolder
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import snapshot_download
import gguf

# Load the tokenizer and model
tokenizer = LlamaTokenizer.from_pretrained("llama-3.2-1B")
model = LlamaForCausalLM.from_pretrained("llama-3.2-1B")

# Move the model to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Example input text
input_text = "Your input text here"

# Tokenize the input text
inputs = tokenizer(input_text, return_tensors="pt").to(device)

# Forward pass to get the model output
outputs = model(**inputs)

# Print the output logits
print(outputs.logits)

# ---------------------------------------------------------
# Qn: using torch trl transformers unsloth.chattemplates unsloth datasets unsloth transformers, create a comment for !pip install of all libraries and load them all in python, then import warnings and ignore all warnings
# !pip install torch trl transformers unsloth.chattemplates unsloth datasets unsloth transformers

import unsloth.chattemplates
import unsloth.datasets
import unsloth.transformers

warnings.filterwarnings("ignore")

# ---------------------------------------------------------
# Qn: load dataset Amod/mental_health_counseling_conversations and load the file combined_dataset.json
# Load the dataset
dataset = load_dataset("Amod/mental_health_counseling_conversations", data_files="combined_dataset.json")

# Print the first example from the dataset
print(dataset['train'][0])

# ---------------------------------------------------------
# Qn: check the length of all the words in each context and show it on a graph using matplotlib
import matplotlib.pyplot as plt

# Function to calculate the length of words in each context
def word_lengths(context):
    return [len(word) for word in context.split()]

# Get the lengths of words in each context in the dataset
word_lengths_list = [word_lengths(example['context']) for example in dataset['train']]

# Flatten the list of word lengths
all_word_lengths = [length for sublist in word_lengths_list for length in sublist]

# Plot the word lengths
plt.hist(all_word_lengths, bins=range(1, max(all_word_lengths) + 1), edgecolor='black')
plt.title('Word Lengths in Contexts')
plt.xlabel('Word Length')
plt.ylabel('Frequency')
plt.show()

# ---------------------------------------------------------
# Qn: filter the data to use only up to the median max number of words in the data.
# Calculate the number of words in each context
num_words = [len(example['context'].split()) for example in dataset['train']]

# Calculate the median number of words
median_num_words = sorted(num_words)[len(num_words) // 2]

# Filter the dataset to include only examples with number of words up to the median
filtered_dataset = dataset.filter(lambda example: len(example['context'].split()) <= median_num_words)

# Print the first example from the filtered dataset
print(filtered_dataset['train'][0])

# ---------------------------------------------------------
# Qn: check the length of words in each response
# Function to calculate the length of words in each response
def response_word_lengths(response):
    return [len(word) for word in response.split()]

# Get the lengths of words in each response in the dataset
response_word_lengths_list = [response_word_lengths(example['response']) for example in dataset['train']]

# Flatten the list of word lengths
all_response_word_lengths = [length for sublist in response_word_lengths_list for length in sublist]

# Print the lengths of words in the first response
print(all_response_word_lengths[:len(response_word_lengths_list[0])])

# ---------------------------------------------------------
# Qn: do the same median based filtering for the responses
# Calculate the number of words in each response
response_num_words = [len(example['response'].split()) for example in dataset['train']]

# Calculate the median number of words in responses
median_response_num_words = sorted(response_num_words)[len(response_num_words) // 2]

# Filter the dataset to include only examples with number of words in response up to the median
filtered_response_dataset = dataset.filter(lambda example: len(example['response'].split()) <= median_response_num_words)

# Print the first example from the filtered response dataset
print(filtered_response_dataset['train'][0])

# ---------------------------------------------------------
# Qn: set the max_seq_length to 100, load FastLanguageModel unsloth/Llama-3.2-1B-bmb-4bit, and train using unsloth for target modules q_proj, k_proj, v_proj, up_proj, down_proj, o_proj, and gate_proj
# Set the maximum sequence length
max_seq_length = 100

# Load the FastLanguageModel
fast_model = FastLanguageModel.from_pretrained("unsloth/Llama-3.2-1B-bmb-4bit")

# Define the target modules for training
target_modules = ["q_proj", "k_proj", "v_proj", "up_proj", "down_proj", "o_proj", "gate_proj"]

# Initialize the Trainer
trainer = Trainer(
    model=fast_model,
    target_modules=target_modules,
    max_seq_length=max_seq_length
)

# Train the model
trainer.train()

# Save the trained model
trainer.save_model("path/to/save/trained_model")

# ---------------------------------------------------------
# Qn: Create the data_prompt for a super friendly mental health perspective that focuses on helping victims feel comfortable in any situation with the calm responses, then set the EOS_TOKEN and make a formatting_prompt(examples) function
# Create the data_prompt for a super friendly mental health perspective
data_prompt = """
You are a super friendly mental health assistant. Your goal is to help victims feel comfortable in any situation with calm and reassuring responses. Always be empathetic, understanding, and supportive.
""" # EDITED MANUALLY: Added Input and responses.

# Set the EOS_TOKEN
#EOS_TOKEN = " # EDITED MANUALLY: Commented out this meaningless line, wasn't the right question, it stopped here.

# ---------------------------------------------------------
# Qn: create a function that outputs a dictionary where the key is text and the value is a list of formatted string, each represents a prompt we prepared for the model to combine the context, response, and structured prompt template
# Function to format the prompts
def formatting_prompt(examples):
    formatted_prompts = {}
    for example in examples:
        context = example['context']
        response = example['response']
        prompt = f"{data_prompt}\n\nContext: {context}\n\nResponse: {response}\n\n"
        if context not in formatted_prompts:
            formatted_prompts[context] = []
        formatted_prompts[context].append(prompt)
    return formatted_prompts

# Example usage
formatted_prompts = formatting_prompt(filtered_response_dataset['train'])
print(formatted_prompts)

# Note: This might need revisiting a ton, I think it might not fit right, but it's a start.

# ---------------------------------------------------------
# Format the data for training
def format_for_training(dataset):
    inputs = []
    labels = []
    for example in dataset:
        context = example['context']
        response = example['response']
        input_text = f"{data_prompt}\n\nContext: {context}\n\nResponse:"
        label_text = f"{response}{tokenizer.eos_token}"
        inputs.append(input_text)
        labels.append(label_text)
    return inputs, labels

# Get the formatted inputs and labels
train_inputs, train_labels = format_for_training(filtered_response_dataset['train'])

# Tokenize the inputs and labels
train_encodings = tokenizer(train_inputs, truncation=True, padding=True, max_length=max_seq_length)
train_labels_encodings = tokenizer(train_labels, truncation=True, padding=True, max_length=max_seq_length)

# Convert to torch tensors
train_dataset = torch.utils.data.TensorDataset(
    torch.tensor(train_encodings['input_ids']),
    torch.tensor(train_labels_encodings['input_ids'])
)

# Example usage
print(train_dataset[0])

# ---------------------------------------------------------
#sudo apt-get update
#sudo apt-get install build-essential

# ---------------------------------------------------------
# Qn: create the trainer as an SFTTrainer using the data created above with all parameters and TrainingArguments as needed
# Define the training arguments
training_args = TrainingArguments(
    output_dir="path/to/save/trained_model",
    per_device_train_batch_size=8,
    num_train_epochs=3,
    logging_dir="path/to/logging_dir",
    logging_steps=10,
    save_steps=500,
    evaluation_strategy="steps",
    eval_steps=500,
    save_total_limit=2,
    load_best_model_at_end=True,
)

# Initialize the SFTTrainer
sft_trainer = SFTTrainer(
    model=fast_model,
    args=training_args,
    train_dataset=train_dataset,
    tokenizer=tokenizer,
)

# Train the model
sft_trainer.train()

# Save the trained model
sft_trainer.save_model("path/to/save/trained_model")

# ---------------------------------------------------------
# Qn: run the trainer.train()
# Run the training process
sft_trainer.train()

# ---------------------------------------------------------
# Qn: create a query text that simulates someone having a bad day as they cant remember something and they need help
# Example query text simulating someone having a bad day and needing help
query_text = """
I'm having a really bad day. I can't seem to remember anything, and it's making me feel so frustrated and helpless. I need some help to get through this.
"""

# Tokenize the query text
query_inputs = tokenizer(query_text, return_tensors="pt").to(device)

# Generate a response from the model
query_outputs = model.generate(**query_inputs, max_length=100)

# Decode and print the response
response_text = tokenizer.decode(query_outputs[0], skip_special_tokens=True)
print(response_text)

# ---------------------------------------------------------
# Fake HF_TOKEN for demonstration purposes
HF_TOKEN = "hf_fake_token_for_demo_purposes"

# Save the model and tokenizer locally
model.save_pretrained("path/to/save/trained_model")
tokenizer.save_pretrained("path/to/save/trained_model")

# Push the model and tokenizer to the Hugging Face Hub
api = HfApi()
api.upload_folder(
    folder_path="path/to/save/trained_model",
    path_in_repo="",
    repo_id="edg3/Llama-3.2-1B_finetuned-mental-assist",
    token=HF_TOKEN
)

# ---------------------------------------------------------
# Qn: save the model locally to a folder
# Save the model and tokenizer locally
model.save_pretrained("path/to/save/trained_model")
tokenizer.save_pretrained("path/to/save/trained_model")

# ---------------------------------------------------------
# Qn: download the model finetuned and saved above to folder, then convert it to a gguf, then upload it to the huggingfacehub
# Download the finetuned model from the Hugging Face Hub
model_id = "edg3/Llama-3.2-1B_finetuned-mental-assist"
local_dir = "path/to/downloaded_model"
snapshot_download(repo_id=model_id, local_dir=local_dir)

# Load the model and tokenizer
model = AutoModelForCausalLM.from_pretrained(local_dir)
tokenizer = AutoTokenizer.from_pretrained(local_dir)

# Convert the model to GGUF format
gguf.convert_model(model, tokenizer, output_dir="path/to/gguf_model")

# Upload the GGUF model to the Hugging Face Hub
api.upload_folder(
    folder_path="path/to/gguf_model",
    path_in_repo="",
    repo_id="edg3/Llama-3.2-1B_finetuned-mental-assist-gguf",
    token=HF_TOKEN
)



### Final thoughts (auto generated by copilot for thoughts):
# - The code is a good start, but it needs more work to be fully functional.
# - The training process and data formatting need to be refined.
# - The model can be further fine-tuned and evaluated for better performance.
# - The code can be optimized for better efficiency and readability.
# - Additional error handling and logging can be added for better debugging.