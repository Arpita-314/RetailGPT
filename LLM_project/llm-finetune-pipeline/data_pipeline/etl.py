"""
train.py
Simple fine-tuning script using Hugging Face Trainer for a classification objective.
Includes basic logging hooks for W&B or MLflow (optional).

Usage:
python training/train.py --data_dir data/processed --model_name microsoft/deberta-v3-small \
    --output_dir runs/deberta_demo --epochs 3 --batch_size 16
"""

import argparse
import os
import json
from datasets import load_from_disk, Dataset
import glob
import pandas as pd
from transformers import (
    AutoTokenizer, AutoModelForSequenceClassification,
    Trainer, TrainingArguments,
)
import torch
from sklearn.model_selection import train_test_split
from transformers import DataCollatorWithPadding

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", type=str, required=True)
    p.add_argument("--model_name", type=str, default="microsoft/deberta-v3-small")
    p.add_argument("--output_dir", type=str, default="runs/deberta_demo")
    p.add_argument("--epochs", type=int, default=3)
    p.add_argument("--batch_size", type=int, default=16)
    p.add_argument("--learning_rate", type=float, default=2e-5)
    p.add_argument("--max_seq_length", type=int, default=256)
    p.add_argument("--label_col", type=str, default="toxicity")
    p.add_argument("--num_labels", type=int, default=2)  # 2 for binary (adjust as needed)
    return p.parse_args()

def load_shards_to_df(data_dir):
    files = sorted(glob.glob(os.path.join(data_dir, "*.parquet")))
    dfs = []
    for f in files:
        dfs.append(pd.read_parquet(f))
    df = pd.concat(dfs, ignore_index=True)
    return df

def prepare_datasets(df, tokenizer, args):
    # map label to int if necessary
    if args.label_col in df.columns:
        df = df.dropna(subset=[args.label_col])
        if df[args.label_col].dtype == object:
            df[args.label_col] = df[args.label_col].astype(int)
    else:
        # create dummy label 0 if not present (e.g. for unsupervised)
        df[args.label_col] = 0

    train_df, val_df = train_test_split(df, test_size=0.1, random_state=42, stratify=df[args.label_col])
    def to_dataset(df_in):
        # rebuild a Dataset from pandas and map tokenizer on the concatenated tokens
        ds = Dataset.from_pandas(df_in.reset_index(drop=True))
        def preprocess(ex):
            return tokenizer(ex["input_ids"] if "input_ids" in ex else ex.get("text", ""), truncation=True)
        # We assume ETL saved input_ids & attention_mask; if not, tokenization needed
        return ds

    train_ds = Dataset.from_pandas(train_df.reset_index(drop=True))
    val_ds = Dataset.from_pandas(val_df.reset_index(drop=True))
    return train_ds, val_ds

def collate_fn(features):
    # If ETL saved input_ids and attention_mask, we can use them directly.
    # Here we use DataCollatorWithPadding to handle variable-length tokens.
    return DataCollatorWithPadding(tokenizer=tokenizer, return_tensors="pt")(features)

if __name__ == "__main__":
    args = parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    tokenizer = AutoTokenizer.from_pretrained(args.model_name, use_fast=True)

    print("Loading parquet shards...")
    df = load_shards_to_df(args.data_dir)
    print(f"Loaded {len(df)} samples")

    # If ETL produced input_ids vectors, you might skip tokenization here. For simplicity we assume df contains raw text.
    # If ETL preserved raw text column named 'text', otherwise change appropriately:
    if "text" not in df.columns and "input_ids" in df.columns:
        # convert input_ids back to tokens? Here we add a fallback but better to maintain raw text or re-tokenize.
        df["text"] = df["input_ids"].astype(str)

    # Simple dataset split
    train_df, val_df = train_test_split(df, test_size=0.1, random_state=42, stratify=df.get(args.label_col))
    train_ds = Dataset.from_pandas(train_df.reset_index(drop=True))
    val_ds = Dataset.from_pandas(val_df.reset_index(drop=True))

    # model init
    model = AutoModelForSequenceClassification.from_pretrained(args.model_name, num_labels=args.num_labels)

    # training args
    training_args = TrainingArguments(
        output_dir=args.output_dir,
        evaluation_strategy="steps",
        eval_steps=200,
        save_strategy="steps",
        save_steps=200,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size//2 if args.batch_size>1 else 1,
        num_train_epochs=args.epochs,
        learning_rate=args.learning_rate,
        fp16=torch.cuda.is_available(),
        logging_dir=os.path.join(args.output_dir, "logs"),
        logging_steps=50,
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        save_total_limit=3,
    )

    # data collator (tokenize on the fly if needed)
    def preprocess_function(examples):
        # If ETL preserved token ids, you can map them directly
        if "input_ids" in examples:
            return examples
        texts = examples.get("text")
        return tokenizer(texts, truncation=True, padding=False, max_length=args.max_seq_length)

    train_ds = train_ds.map(preprocess_function, batched=True)
    val_ds = val_ds.map(preprocess_function, batched=True)

    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    # metrics
    import numpy as np
    from sklearn.metrics import accuracy_score, f1_score

    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        preds = np.argmax(logits, axis=-1)
        return {
            "accuracy": accuracy_score(labels, preds),
            "f1": f1_score(labels, preds, average="binary")
        }

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        tokenizer=tokenizer,
        data_collator=data_collator,
        compute_metrics=compute_metrics
    )

    trainer.train()
    trainer.save_model(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)
    print("Training complete. Model and tokenizer saved at", args.output_dir)
