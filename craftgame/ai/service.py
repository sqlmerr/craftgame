import json
import logging
from dataclasses import dataclass

from openai import AsyncClient

from craftgame.ai.dto import GenerateItemDTO, GeneratedItemDTO
from craftgame.ai.exceptions import AiGenerationError
from craftgame.ai.interfaces.item_generator import ItemGenerator


@dataclass(frozen=True)
class AiService(ItemGenerator):
    client: AsyncClient

    async def generate_item(self, data: GenerateItemDTO) -> GeneratedItemDTO:
        prompt = f"""
        You are a creative assistant for a crafting game. Based on two input items, generate a new item that combines their concepts. The result should include a name and an emoji that represent the new item. Return the response in JSON format with the fields "name" and "emoji".

        Input items:
        - Item 1: {data.ingredient1_name}
        - Item 2: {data.ingredient2_name}

        Example output:
        ```json
        {{
            "name": "resulting_item_name",
            "emoji": "🔥"
        }}
        ```

        Ensure the name is:
        - Preferably a single word, but two words are allowed if necessary to reflect the combination.
        - In snake_case format (lowercase letters, words separated by underscores, e.g., "fire_ball").
        - Concise (max 50 characters).
        - Creative and reflective of the combination of the two items.
        The emoji should be a single Unicode emoji that visually represents the item.
        """

        try:
            response = await self.client.chat.completions.create(
                model="deepseek/deepseek-r1-0528:free",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that generates creative item combinations for a crafting game in JSON format.",
                    },
                    {"role": "user", "content": prompt},
                ],
                response_format={"type": "json_object"},
            )

            result = json.loads(response.choices[0].message.content)

            if "name" in result and "emoji" in result:
                return GeneratedItemDTO(name=result["name"], emoji=result["emoji"])
            raise AiGenerationError

        except Exception as e:
            logging.error(f"Error generating item: {e}")
            raise AiGenerationError
