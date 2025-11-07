import argparse
import os
import random
from pathlib import Path

import torch
import torch.nn as nn
import torch.optim as optim

from model import SortRNN


def generate_batch(batch_size, seq_len, vocab_size, device):
    # values in [0, vocab_size-1]
    src = torch.randint(0, vocab_size, (batch_size, seq_len), device=device)
    trg, _ = torch.sort(src, dim=1)
    return src, trg


def train(args):
    device = torch.device(args.device if torch.cuda.is_available() else "cpu")
    model = SortRNN(args.vocab_size, embed_dim=args.embed_dim, hidden_dim=args.hidden_dim).to(device)
    optimizer = optim.Adam(model.parameters(), lr=args.lr)
    criterion = nn.CrossEntropyLoss()

    Path("checkpoints").mkdir(parents=True, exist_ok=True)

    for epoch in range(1, args.epochs + 1):
        model.train()
        total_loss = 0.0
        iters = args.iters_per_epoch

        for it in range(iters):
            src, trg = generate_batch(args.batch_size, args.seq_len, args.vocab_size, device)
            logits = model(src, trg=trg, teacher_forcing_ratio=args.teacher_forcing)
            # logits: (B,K,V)
            B, K, V = logits.shape
            loss = criterion(logits.view(-1, V), trg.view(-1))

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        avg_loss = total_loss / iters
        print(f"Epoch {epoch}/{args.epochs} — loss: {avg_loss:.4f}")

        # quick sample at epoch end
        if epoch % args.sample_every == 0 or epoch == args.epochs:
            model.eval()
            with torch.no_grad():
                src, trg = generate_batch(4, args.seq_len, args.vocab_size, device)
                logits = model(src, trg=None, teacher_forcing_ratio=0.0)
                pred = logits.argmax(dim=2)
                for i in range(src.size(0)):
                    print("in:", src[i].tolist())
                    print("trg:", trg[i].tolist())
                    print("pred:", pred[i].tolist())
                    print("---")

        # save checkpoint
        ckpt_path = Path("checkpoints") / args.checkpoint
        torch.save({"model_state": model.state_dict(), "args": vars(args)}, ckpt_path)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seq-len", type=int, default=6)
    parser.add_argument("--vocab-size", type=int, default=10)
    parser.add_argument("--embed-dim", type=int, default=32)
    parser.add_argument("--hidden-dim", type=int, default=128)
    parser.add_argument("--batch-size", type=int, default=256)
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--iters-per-epoch", type=int, default=200)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--teacher-forcing", type=float, default=0.5)
    parser.add_argument("--sample-every", type=int, default=1)
    parser.add_argument("--checkpoint", type=str, default="sort_rnn.pth")
    parser.add_argument("--device", type=str, default="cuda")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    train(args)
