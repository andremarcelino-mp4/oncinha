import os
import torch

# 1. Desativa a trava de segurança de pesos do PyTorch para permitir modelos customizados
os.environ["TORCH_FORCE_WEIGHTS_ONLY_LOAD"] = "0"

# 2. Se a versão do PyTorch for muito nova, usamos este ajuste também
try:
    torch.serialization.add_safe_globals(['ultralytics.nn.tasks.DetectionModel'])
except:
    pass

from app import create_app
from dotenv import load_dotenv
from app.core.database import init_db

import torch
# Autoriza o PyTorch a carregar modelos da Ultralytics
torch.serialization.add_safe_globals(['ultralytics.nn.tasks.DetectionModel', 'ultralytics.nn.modules.block.C2f', 'ultralytics.nn.modules.conv.Conv', 'ultralytics.nn.modules.head.Detect', 'ultralytics.nn.modules.block.DFL', 'ultralytics.nn.modules.block.SPPF', 'ultralytics.nn.modules.conv.Concat', 'torch.nn.modules.container.Sequential', 'torch.nn.modules.container.ModuleList', 'torch.nn.modules.upsampling.Upsample', 'torch.nn.modules.pooling.MaxPool2d', 'torch.nn.modules.activation.SiLU'])
# Carrega o .env antes de tudo
load_dotenv()

app = create_app()

init_db()

if __name__ == '__main__':
    # Roda o servidor na porta 8000, com debug ativado (atualiza sozinho)
    app.run(host='0.0.0.0', port=8000, debug=True)