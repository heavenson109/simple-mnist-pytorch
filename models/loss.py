import torch.nn.functional as f


def nll_loss(y_input, y_target):
    return f.nll_loss(y_input, y_target)
