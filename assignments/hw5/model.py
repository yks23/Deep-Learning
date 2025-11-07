import torch
import torch.nn as nn
import random


class SortRNN(nn.Module):
    """Encoder-Decoder RNN that maps an input integer sequence to its sorted version.

    Decoder is autoregressive (GRUCell). A special start token index == vocab_size is used.
    """

    def __init__(self, vocab_size, embed_dim=32, hidden_dim=128):
        super().__init__()
        self.vocab_size = vocab_size
        self.embed = nn.Embedding(vocab_size + 1, embed_dim)  # +1 for <START>
        self.encoder = nn.GRU(embed_dim, hidden_dim, batch_first=True)
        self.decoder_cell = nn.GRUCell(embed_dim, hidden_dim)
        self.output = nn.Linear(hidden_dim, vocab_size)
        self.start_index = vocab_size

    def forward(self, src, trg=None, teacher_forcing_ratio=0.5):
        """Forward pass.

        Args:
            src: LongTensor (B, K)
            trg: LongTensor (B, K) or None
            teacher_forcing_ratio: float

        Returns:
            logits: FloatTensor (B, K, vocab_size)
        """
        B, K = src.size()
        device = src.device
        src_emb = self.embed(src)  # (B,K,E)
        _, h = self.encoder(src_emb)  # h: (1,B,H)
        h = h.squeeze(0)  # (B,H)

        outputs = []
        input_tok = torch.full((B,), self.start_index, dtype=torch.long, device=device)

        for t in range(K):
            input_emb = self.embed(input_tok)  # (B,E)
            h = self.decoder_cell(input_emb, h)  # (B,H)
            logits = self.output(h)  # (B,vocab_size)
            outputs.append(logits.unsqueeze(1))

            # decide next input token
            if trg is not None and random.random() < teacher_forcing_ratio:
                input_tok = trg[:, t]
            else:
                input_tok = logits.argmax(dim=1)

        return torch.cat(outputs, dim=1)
