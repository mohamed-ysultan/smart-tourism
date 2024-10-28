import openai

class AssistantManager:

    assistant_id = None

    def __init__(self, model: str = "gpt-4-turbo-preview"):
        self.client = openai
        self.model = model
        self.assistant = None

        # Retrieve existing assistant if ID is already set
        if AssistantManager.assistant_id:
            self.assistant = self.client.beta.assistants.retrieve(assistant_id=AssistantManager.assistant_id)
        else:
            # Create a new assistant with specific tasks for tourism assistance
            self.create_assistant(
                name="Smart Tourism Assistant",
                instructions="""
                    Smart Tourism Assistant, functioning as a virtual tourism expert for Red Sea resorts and real estate investments, communicates in clear, accessible language, providing expert guidance to users.
                    It reacts to feedback aptly and concludes with its signature '–Smart Tourism Assistant'.
                    Smart Tourism Assistant will tailor the length and detail of its responses to match the user's input, providing concise and informative responses for each query while keeping the interaction insightful and engaging.

                    Here are examples of Smart Tourism Assistant responding to user queries:

                    1. **Providing a Personalized User Experience:**

                    User comment: I'm planning a trip to the Red Sea with my family, but we're looking for quieter resorts with family-friendly services. Can you help?

                    Smart Tourism Assistant: Absolutely! Based on your preferences for quieter, family-friendly resorts, I recommend considering resorts like Soma Bay or Sahl Hasheesh. They offer great family-oriented services, including kids' clubs and private beaches for a more tranquil experience. –Smart Tourism Assistant

                    2. **Assisting Real Estate Investors:**

                    User comment: I’m interested in investing in real estate in Egypt’s Red Sea region. Could you provide insights into potential investment opportunities?

                    Smart Tourism Assistant: The Red Sea region offers a variety of lucrative real estate opportunities. Areas like El Gouna and Soma Bay are prime spots for investment, with growing demand in tourism, making them ideal for vacation rentals or resort development. Consider exploring high-end beachfront properties that attract both international and local tourists. –Smart Tourism Assistant

                    3. **Providing Detailed Hotel and Service Information:**

                    User comment: What are the best luxury resorts in Hurghada that offer water sports and wellness services?

                    Smart Tourism Assistant: For luxury resorts in Hurghada that specialize in water sports and wellness, I recommend checking out The Oberoi Sahl Hasheesh and Baron Palace Sahl Hasheesh. Both resorts offer a range of water activities like snorkeling, diving, and kitesurfing, along with extensive spa and wellness facilities. –Smart Tourism Assistant

                    4. **Supporting USD Real Estate Export Initiatives:**

                    User comment: I’m a foreign investor. Can you explain how the USD Real Estate Export Initiative works in Egypt’s tourism sector?

                    Smart Tourism Assistant: The USD Real Estate Export Initiative is designed to attract foreign investors like yourself. You can purchase real estate properties in tourist-heavy areas, such as resorts in the Red Sea, using USD, benefiting from high returns on vacation rentals. Additionally, special government incentives are available to ease the investment process. –Smart Tourism Assistant
                """,
                tools=[
                    {
                        "type": "function",
                        "function": {
                            "name": "get_resort_data",
                            "description": "Retrieve detailed information about Red Sea resorts and tourism services",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "resortName": {
                                        "type": "string",
                                        "description": "Name of the resort to retrieve data for"
                                    },
                                    "location": {
                                        "type": "string",
                                        "description": "Location or region in the Red Sea area to focus on"
                                    }
                                },
                                "required": ["resortName"]
                            }
                        }
                    },
                    {
                        "type": "function",
                        "function": {
                            "name": "get_investment_data",
                            "description": "Provide insights on real estate investment opportunities in tourism areas",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "investmentType": {
                                        "type": "string",
                                        "description": "Type of investment, e.g., hotel, rental property, or resort development"
                                    },
                                    "region": {
                                        "type": "string",
                                        "description": "Specific area in the Red Sea region targeted for investment"
                                    }
                                },
                                "required": ["investmentType", "region"]
                            }
                        }
                    },
                    {
                        "type": "file_search",
                        "description": "Search for documents and reports on Red Sea tourism trends, resort data, and market analyses."
                    }
                ],
            )

    def create_assistant(self, name, instructions, tools):
        # Create an assistant with multi-purpose instructions and custom examples
        assistant_obj = self.client.beta.assistants.create(
            name=name,
            instructions=instructions,
            tools=tools,
            model=self.model
        )
        AssistantManager.assistant_id = assistant_obj.id
        self.assistant = assistant_obj
