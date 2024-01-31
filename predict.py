import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel, PeftConfig
from transformers import TextStreamer, TextIteratorStreamer, GenerationConfig
from threading import Thread

model='./model'
peft_model_name = './peft_model'
tokenizer_path = './tokenizer'
config = PeftConfig.from_pretrained(peft_model_name)
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)
config.base_model_name_or_path =model
model = AutoModelForCausalLM.from_pretrained(config.base_model_name_or_path, quantization_config=bnb_config, device_map="auto")
model = PeftModel.from_pretrained(model, peft_model_name)
tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
streamer = TextIteratorStreamer(tokenizer)


from typing import Generator

# async def gen(x) -> Generator[str, None, None]:
#     generation_config = GenerationConfig(
#         temperature=0.8,
#         top_p=0.8,
#         top_k=100,
#         max_new_tokens=512,
#         early_stopping=True,
#         do_sample=True,
#     )
#     q = f"### instruction: {x}\n\n### Response: "
#     gened = model.generate(
#         **tokenizer(
#             q,
#             return_tensors='pt',
#             return_token_type_ids=False
#         ).to('cuda'),
#         generation_config=generation_config,
#         pad_token_id=tokenizer.eos_token_id,
#         eos_token_id=tokenizer.eos_token_id,
#         streamer=streamer,
#     )

#     for partial_output in gened:
#         result_str = tokenizer.decode(partial_output)
#         start_tag = f"\n\n### Response: "
#         start_index = result_str.find(start_tag)

#         if start_index != -1:
#             result_str = result_str[start_index + len(start_tag):].strip()
#             yield result_str

async def gen(x) -> Generator[str, None, None]:
    generation_config = GenerationConfig(
        temperature=0.8,
        top_p=0.8,
        top_k=100,
        max_new_tokens=512,
        early_stopping=True,
        do_sample=True,
    )
    q = f"### instruction: {x}\n\n### Response: "
    
    # Tokenizer를 통해 입력을 변환
    inputs = tokenizer(
        q,
        return_tensors='pt',
        return_token_type_ids=False
    ).to('cuda')

    # TextIteratorStreamer 설정
    streamer = TextIteratorStreamer(tokenizer)

    # 스레드를 사용하여 모델의 generate 메소드 실행
    thread = Thread(target=model.generate, kwargs=dict(
        **inputs,
        generation_config=generation_config,
        pad_token_id=tokenizer.eos_token_id,
        eos_token_id=tokenizer.eos_token_id,
        streamer=streamer,
    ))
    thread.start()
    # # 24.01.24., 14:35 success
    # for partial_output in streamer:
    #     yield partial_output
    # 24.01.24., 14:36 TEST
    result_str = ""
    for partial_output in streamer:
        # partial_output에서 "### Response:" 이후의 텍스트만 추출
        result_str += partial_output
        start_tag = "\n\n### Response: "
        start_index = result_str.find(start_tag)
        if start_index != -1:
            # 태그 이후의 텍스트만 추출하고 '</s>' 태그 제거
            response = result_str[start_index + len(start_tag):]
            response = response.replace('</s>', '').strip()  # '</s>' 태그 제거 및 공백 제거
            yield response

    # for partial_output in streamer:
    #     result_str += partial_output  # partial_output을 직접 사용
    #     print(result_str)
    #     start_tag = f"\n\n### Response: "
    #     start_index = partial_output.find(start_tag)

    #     if start_index != -1:
    #         result_str = result_str[start_index + len(start_tag):].strip()
    #         yield result_str

        # # result_str = tokenizer.decode(partial_output) # 이 줄을 삭제
        # result_str = partial_output  # partial_output을 직접 사용
        # print(result_str)
        # start_tag = f"\n\n### Response: "
        # start_index = result_str.find(start_tag)

        # if start_index != -1:
        #     result_str = result_str[start_index + len(start_tag):].strip()
        #     yield result_str
