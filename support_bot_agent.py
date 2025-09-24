# support_bot_agent.py

import logging
import random
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
import torch

SIMILARITY_THRESHOLD = 0.3

logging.basicConfig(
    filename='support_bot_log.txt',
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class SupportBotAgent:
    def __init__(self, document_path: str):
        logging.info("Initializing SupportBotAgent...")
        self.qa_model = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        
        self.document_text = self._load_document(document_path)
        self.sections = [s.strip() for s in self.document_text.split('\n\n') if s.strip()]
        self.section_embeddings = self.embedder.encode(self.sections, convert_to_tensor=True)
        
        logging.info(f"Successfully loaded and processed document: {document_path}")
        print("Bot initialized successfully.")

    def _load_document(self, path: str) -> str:
        try:
            with open(path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            logging.error(f"Document not found at path: {path}")
            raise
    
    def _find_relevant_section(self, query: str) -> tuple[str, float]:
        query_embedding = self.embedder.encode(query, convert_to_tensor=True)
        similarities = util.cos_sim(query_embedding, self.section_embeddings)[0]
        best_score, best_section_index = torch.max(similarities, dim=0)
        logging.info(f"Query: '{query}'. Best section index: {best_section_index}, Score: {best_score:.4f}")
        return self.sections[best_section_index], best_score.item()

    def answer_query(self, query: str) -> str:
        context, score = self._find_relevant_section(query)
        if score < SIMILARITY_THRESHOLD:
            logging.warning(f"Relevance score {score:.4f} is below threshold. Responding with fallback.")
            return "I don't have enough information to answer that."
        
        logging.info(f"Answering query '{query}' using retrieved context with score {score:.4f}.")
        result = self.qa_model(question=query, context=context)
        answer = result.get("answer", "I could not find a specific answer in the document.")
        confidence = result.get("score", 0)
        
        if confidence < 0.1:
            logging.warning(f"Low QA model confidence score ({confidence:.2f}).")
            return "I was able to find some information, but I'm not confident in the answer."
        
        logging.info(f"Generated answer: '{answer}' with confidence {confidence:.2f}")
        return answer

    def get_feedback(self) -> str:
        feedback = random.choice(["not helpful", "too vague", "good"])
        logging.info(f"Simulated feedback received: '{feedback}'")
        return feedback

    def adjust_response(self, query: str, feedback: str) -> str:
        logging.info(f"Adjusting response based on feedback: '{feedback}'")
        if feedback == "too vague" or feedback == "not helpful":
            context, _ = self._find_relevant_section(query)
            return f"Let me provide more context: '{context}'"
        return ""

    def run(self, queries: list[str]):
        for query in queries:
            print(f"\n─────────────────────────────────\nQuery: '{query}'")
            logging.info(f"--- Processing new query: {query} ---")
            
            response = self.answer_query(query)
            print(f"Initial Response: {response}")
            
            if "I don't have enough information" in response or "not confident" in response:
                logging.info("Initial response was a fallback. Skipping feedback loop.")
                continue
            
            for i in range(2):
                feedback = self.get_feedback()
                print(f"Simulated Feedback: '{feedback}'")
                
                if feedback == "good":
                    logging.info("Feedback was 'good'. Ending loop.")
                    break
                
                response = self.adjust_response(query, feedback)
                print(f"Adjusted Response (Attempt {i+1}): {response}")
                
                # --- FINAL LOGIC FIX ---
                # After making one adjustment, the bot's job is done for this query.
                logging.info("One adjustment attempt made. Ending loop.")
                break
            
            logging.info(f"--- Finished processing query: {query} ---")

if __name__ == "__main__":
    bot = SupportBotAgent(document_path="data/faq.txt")
    sample_queries = [
        "How do I reset my password?",
        "What's the refund policy?",
        "How do I fly to the moon?"
    ]
    bot.run(sample_queries)
    print("\n─────────────────────────────────")
    print("\nRun complete. Check 'support_bot_log.txt' for details.")