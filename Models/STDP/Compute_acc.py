import torch
import numpy as np


def CompAcc(accuracy_var, label_tensor, all_activity_pred, proportion_pred):
    accuracy_var["all"].append(
        100
        * torch.sum(label_tensor.long() == all_activity_pred).item()
        / len(label_tensor)
    )
    accuracy_var["proportion"].append(
        100
        * torch.sum(label_tensor.long() == proportion_pred).item()
        / len(label_tensor)
    )
    print(
        "\nAll activity Acc: %.2f (last), %.2f (average), %.2f (best)"
        % (
            accuracy_var["all"][-1],
            np.mean(accuracy_var["all"]),
            np.max(accuracy_var["all"]),
        )
    )
    print(
        "Proportion weighting Acc: %.2f (last), %.2f (average), %.2f (best)\n"
        % (
            accuracy_var["proportion"][-1],
            np.mean(accuracy_var["proportion"]),
            np.max(accuracy_var["proportion"]),
        )
    )
