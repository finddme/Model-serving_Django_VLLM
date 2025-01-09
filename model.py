from typing import Optional
import torch
from vllm import LLM, SamplingParams
import os
from huggingface_hub import login

login("")

# NCCL 환경 변수 설정
os.environ['NCCL_DEBUG'] = 'INFO'
os.environ['NCCL_IB_GID_INDEX'] = '1'
os.environ['NCCL_ASYNC_ERROR_HANDLING'] = '1'
os.environ['NCCL_DEBUG_SUBSYS'] = 'GRAPH'
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

llm = None
sampling_params = None

def initialize_model():
    global llm, sampling_params
    
    try:
        torch.cuda.empty_cache()
        model_name = "meta-llama/Meta-Llama-3.1-8B-Instruct"
        
        llm = LLM(
            model=model_name,
            tensor_parallel_size=2,
            gpu_memory_utilization=0.95,
            dtype="half",
            max_model_len=4096,
            trust_remote_code=True,
            enable_prefix_caching=False,
            max_num_seqs=16,
            rope_scaling={"type": "extended", "factor": 8.0},
        )
        
        sampling_params = SamplingParams(
            max_tokens=1024,
            temperature=0.1,
            skip_special_tokens=True
        )
        
        return llm, sampling_params
        
    except Exception as e:
        print(f"Model loading error: {e}")
        raise

def get_model():
    global llm, sampling_params
    if llm is None or sampling_params is None:
        raise RuntimeError("Model not initialized. Call initialize_model() first.")
    return llm, sampling_params