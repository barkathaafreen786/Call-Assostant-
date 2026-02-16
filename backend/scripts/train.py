
# train.py - Logic for Fine-Tuning SLM (e.g., TinyLlama or Phi-2) on the Dataset
# Note: This script requires a GPU and installed libraries (peft, transformers, bitsandbytes, trl).

import json
from datasets import Dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from peft import LoraConfig, get_peft_model
from trl import SFTTrainer
import torch

def train_slm():
    # 1. Load Dataset
    data_path = "../data/dataset.json"
    with open(data_path, 'r') as f:
        data = json.load(f)
    
    # Convert to HuggingFace Dataset
    hf_dataset = Dataset.from_list(data)

    # 2. Model & Tokenizer
    model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    tokenizer.pad_token = tokenizer.eos_token

    # Load Model in 4-bit (Quantized)
    model = AutoModelForCausalLM.from_pretrained(
        model_id, 
        device_map="auto",
        load_in_4bit=True
    )

    # 3. LoRA Configuration
    peft_config = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )

    # 4. Training Arguments
    training_args = TrainingArguments(
        output_dir="../models/finetuned_slm",
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        logging_steps=10,
        num_train_epochs=3,
        max_steps=100, # For demo purposes
        fp16=True,
    )

    # 5. Trainer
    trainer = SFTTrainer(
        model=model,
        train_dataset=hf_dataset,
        peft_config=peft_config,
        dataset_text_field="text", # Need to format dataset to text field
        max_seq_length=1024,
        tokenizer=tokenizer,
        args=training_args,
        formatting_func=format_prompt
    )

    trainer.train()
    trainer.save_model("../models/finetuned_slm_final")
    print("Training Complete. Model saved.")

def format_prompt(example):
    return f"<|system|>\nYou are a helpful BFSI assistant.</s>\n<|user|>\n{example['instruction']}</s>\n<|assistant|>\n{example['output']}</s>"

if __name__ == "__main__":
    print("Starting training (Simulation - requires GPU)...")
    # train_slm() 
