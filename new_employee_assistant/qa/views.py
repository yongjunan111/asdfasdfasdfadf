from django.shortcuts import render
import os
from django.http import JsonResponse
from openai import OpenAI
from .models import Post, Category, Tag, AIResponse

def get_response(request):
    client = OpenAI()

    if request.method == 'POST':
        user_input = request.POST.get('text')

        try:
            response = client.chat.completions.create(
                model = 'gpt-4o-mini',
                messages = [
                    {
                        'role': 'system',
                        'content': '너는 유저의 질문에 친절하게 답변하는 봇이다.'
                    },
                    {
                        'role': 'user',
                        'content': user_input
                    },
                ]
            )

            answer = response.choices[0].message.content.strip()

            return JsonResponse({"response": answer})
        except Exception as error:
            return JsonResponse({"error": str(error)})
        
    return render(
        request,
        'blog/llm.html',
        {
            'get_response': get_response,
        }
    )


def ai_response_view(request):
    if request.method == "POST":
        user_prompt = request.POST.get("prompt", "")
        if not user_prompt:
            return JsonResponse({"error": "No prompt provided."}, status=400)

        response = get_response(user_prompt)
        AIResponse.objects.create(prompt=user_prompt, response=response)
        return JsonResponse({"response": response})

    return JsonResponse({"error": "Invalid request method."}, status=405)