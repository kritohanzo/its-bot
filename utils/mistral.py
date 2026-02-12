from typing import Final

import aiohttp

from utils.config import config


class MistralClient:
    BASE_URL: Final[str] = 'https://api.mistral.ai'
    CHAT_URI: Final[str] = '/v1/chat/completions'
    API_KEY: Final[str] = config.MISTRAL_TOKEN

    DEFAULT_FIRST_MESSAGE: Final[
        str
    ] = '''
        Привет, представь, что ты самый крутой генератор комплиментов к 14 февраля.
        Тебе будет предоставлен промпт, который будет являться примером и пожеланием к комплименту.
        Твоя задача придумать комплимент на основе полученного промта, который будет максимально приближён к нему.
        В ответе избегай эмодзи и лишней информации, отдавай только комплимент без лишней воды и шума, спасибо!
    '''

    @property
    def _headers(self) -> dict[str, str]:
        return {
            'Authorization': f'Bearer {self.API_KEY}',
            'Content-Type': 'application/json',
        }

    async def get_compliment(self, prompt: str) -> str:
        body = await self._build_body(prompt=prompt)

        async with aiohttp.ClientSession(base_url=self.BASE_URL, connector_owner=False) as session:
            response = await session.post(
                url=self.CHAT_URI,
                headers=self._headers,
                json=body,
            )

        try:
            response.raise_for_status()
        except Exception as exc:
            return f'Интеграция с Mistral API сломалась: {exc}'

        data = await response.json()

        return data['choices'][0]['message']['content']

    async def _build_body(self, prompt: str) -> dict[str, str | int | list[dict[str, str]]]:
        return {
            'model': 'mistral-large-latest',
            'n': 1,
            'messages': [
                {
                    'content': self.DEFAULT_FIRST_MESSAGE,
                    'role': 'user',
                },
                {
                    'content': prompt,
                    'role': 'user',
                },
            ],
        }
