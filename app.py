from typing import Optional
from ninja import NinjaAPI, Schema, Router
from django.http import HttpRequest
import torch
import os
import re
from model import get_model, initialize_model
import asyncio
from functools import partial
from concurrent.futures import ThreadPoolExecutor
import threading

# NCCL 환경 변수 설정
os.environ['NCCL_DEBUG'] = 'INFO'
os.environ['NCCL_IB_GID_INDEX'] = '1'
os.environ['NCCL_ASYNC_ERROR_HANDLING'] = '1'
os.environ['NCCL_DEBUG_SUBSYS'] = 'GRAPH'
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

model_router = Router()

executor = ThreadPoolExecutor(max_workers=1)

model_lock = threading.Lock()

class ChatRequest(Schema):
    system_prompt: Optional[str] = None
    user_prompt: str

class ChatResponse(Schema):
    Q: str
    A: str

model, params = initialize_model()

async def run_model_inference(prompt: str):
    try:
        def sync_inference():
            outputs = model.generate(prompt, params)
            return outputs[0].outputs[0].text
            
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, sync_inference)
        
    except Exception as e:
        print(f"Inference error: {e}")
        raise

@model_router.get("/")
def get_something(request):
    return {"message": "Hiiiiiiiiiiiiiiiii"}

@model_router.get("/request", response=ChatResponse)
async def chat_get(request: HttpRequest, system_prompt: str, user_prompt: str) -> ChatResponse:
    if not user_prompt:
        return ChatResponse(Q="", A="질문이 없습니다.")
    
    prompt = f"""
        <|begin_of_text|><|start_header_id|>system<|end_header_id|>
        {system_prompt}
        <|eot_id|><|start_header_id|>user<|end_header_id|>
        {user_prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
    """
    
    response = await run_model_inference(prompt)
    
    return ChatResponse(Q=user_prompt, A=response)

@model_router.post("/request", response=ChatResponse)
async def chat_post(request: HttpRequest, chat_request: ChatRequest) -> ChatResponse:
    if not chat_request.user_prompt:
        return ChatResponse(Q="", A="질문이 없습니다.")
    
    prompt = f"""
        <|begin_of_text|><|start_header_id|>system<|end_header_id|>
        {chat_request.system_prompt or ''}
        <|eot_id|><|start_header_id|>user<|end_header_id|>
        {chat_request.user_prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
    """
    
    response = await run_model_inference(prompt)
    
    return ChatResponse(Q=chat_request.user_prompt, A=response)