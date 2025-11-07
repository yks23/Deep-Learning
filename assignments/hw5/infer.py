import argparse
from pathlib import Path

import torch

from model import SortRNN


def infer(args):
    device = torch.device(args.device if torch.cuda.is_available() else "cpu")
    ckpt = torch.load(args.checkpoint, map_location=device)
    saved_args = ckpt.get("args", {})
    model = SortRNN(saved_args.get("vocab_size", args.vocab_size), embed_dim=saved_args.get("embed_dim", 32), hidden_dim=saved_args.get("hidden_dim", 128)).to(device)
    model.load_state_dict(ckpt["model_state"])
    model.eval()

    with torch.no_grad():
        for _ in range(args.n_samples):
            src = torch.randint(0, args.vocab_size, (1, args.seq_len), device=device)
            trg, _ = torch.sort(src, dim=1)
            logits = model(src, trg=None, teacher_forcing_ratio=0.0)
            pred = logits.argmax(dim=2)
            print("in :", src[0].tolist())
            print("trg:", trg[0].tolist())
            print("pred:", pred[0].tolist())
            print("---")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=str, required=True)
    parser.add_argument("--n-samples", type=int, default=8)
    parser.add_argument("--seq-len", type=int, default=6)
    parser.add_argument("--vocab-size", type=int, default=10)
    parser.add_argument("--device", type=str, default="cuda")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    infer(args)
