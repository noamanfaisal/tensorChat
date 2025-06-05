from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

class Factory:
    templates = {
        "default": ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant."),
            MessagesPlaceholder("history"),
            ("user", "{input}")
        ]),
        "qa": ChatPromptTemplate.from_messages([
            ("system", "Answer the question based on the context."),
            ("user", "Context:\n{context}\n\nQuestion: {question}")
        ])
    }

    @staticmethod
    def create(template_name: str = "default") -> ChatPromptTemplate:
        return Factory.templates.get(template_name, Factory.templates["default"])

   
