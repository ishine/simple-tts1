import functools

from torch.distributed.fsdp.wrap import (size_based_auto_wrap_policy,
                                         transformer_auto_wrap_policy)
from transformers.models.llama.modeling_llama import (LlamaDecoderLayer,
                                                      Qwen2MoeDecoderLayer)
from transformers.models.mllama.modeling_mllama import (
    MllamaCrossAttentionDecoderLayer, MllamaSelfAttentionDecoderLayer,
    MllamaVisionEncoderLayer)


def get_size_policy(min_params=1e8):
    num_wrap_policy = functools.partial(size_based_auto_wrap_policy,
                                        min_num_params=min_params)
    return num_wrap_policy


def get_llama_wrapper():
    """we register our main layer class and use the fsdp transformer wrapping policy
    ensures embedding layers are in the root fsdp unit for shared access and that fsdp units map to transformer layers
    """
    # ====   use new transformer wrapper

    llama_auto_wrap_policy = functools.partial(
        transformer_auto_wrap_policy,
        transformer_layer_cls=set([
            LlamaDecoderLayer,
            MllamaSelfAttentionDecoderLayer,
            MllamaVisionEncoderLayer,
            MllamaCrossAttentionDecoderLayer,
            Qwen2MoeDecoderLayer,
        ]))

    return llama_auto_wrap_policy
