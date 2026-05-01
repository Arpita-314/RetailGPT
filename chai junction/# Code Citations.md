# Code Citations

## License: MIT
https://github.com/colinch4/colinch4.github.io/tree/e311fb0e9d2c623501b943aa5210b9918664873c/_posts/2023/09/7/2023-09-07-11-45-46-233115.md

```
from torch.utils.data import Dataset

class CustomDataset(Dataset):
    def __init__(self, data):
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        sample = self.data[idx
```

