# The Price is Right – Autonomous Deal Hunter

## Overview

**The Price is Right** is an AI-powered autonomous agent framework that hunts for high-value online deals, estimates their true prices using advanced machine learning and LLMs, and notifies users about the best opportunities. The system features a modular agent architecture, real-time Gradio dashboard, and push notifications for actionable deals.

---

## Features

- **Automated Deal Discovery:** Scrapes and summarizes deals from multiple RSS feeds.
- **LLM-based Filtering:** Uses a fine-tuned LLM (Meta Llama via Together API & Modal) to select and summarize the most promising deals.
- **Ensemble Price Prediction:** Combines predictions from a fine-tuned LLM, Random Forest model, and retrieval-augmented generation (RAG) for robust price estimation.
- **Vector Similarity Search:** Integrates ChromaDB and SentenceTransformers for finding similar products and context-aware pricing.
- **Real-Time Dashboard:** Interactive Gradio UI for monitoring deals, logs, and 3D deal clustering visualization.
- **Push Notifications:** Sends alerts for high-value deals using the Pushover API.
- **Memory & Deduplication:** Avoids duplicate notifications by tracking processed deals.

---

## Technologies Used

- **Python 3.10+**
- **Gradio** – UI and dashboard
- **PyTorch, Transformers** – LLMs and embeddings
- **Modal** – Remote LLM inference (fine-tuned Meta Llama)
- **ChromaDB** – Vector database for similarity search
- **Scikit-learn** – Random Forest, Linear Regression, t-SNE
- **SentenceTransformers** – Embedding generation
- **Pushover** – Push notifications
- **Feedparser, BeautifulSoup** – Web scraping and RSS parsing
- **Plotly, Matplotlib** – Data visualization
- **dotenv** – Environment variable management

---

## Project Structure

```
agents/
    agent.py
    deals.py
    ensemble_agent.py
    frontier_agent.py
    messaging_agent.py
    planning_agent.py
    random_forest_agent.py
    scanner_agent.py
    specialist_agent.py
deal_agent_framework.py
price_is_right_final.py
items.py
log_utils.py
memory.json
requirements.txt
.env
```

---

## Quick Start

1. **Clone the repository:**
    ```bash
    git clone https://github.com/UtkarshShaarma/price-is-right.git
    cd price-is-right
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up environment variables:**
    - Copy `.env.example` to `.env` and fill in your API keys for HuggingFace, Together API, and Pushover.

4. **Run the application:**
    ```bash
    python price_is_right_final.py
    ```
    - The Gradio dashboard will launch in your browser.

---

## How It Works

1. **Deal Fetching:**  
   The system scrapes deals from RSS feeds and filters out previously seen deals.

2. **LLM Summarization:**  
   A fine-tuned LLM selects and summarizes the top 5 most detailed deals with clear prices.

3. **Price Estimation:**  
   - **SpecialistAgent:** Calls a remote fine-tuned LLM for price prediction.
   - **FrontierAgent:** Uses vector similarity (ChromaDB) and LLM for context-aware pricing.
   - **RandomForestAgent:** Predicts price using a classical ML model.
   - **EnsembleAgent:** Combines all predictions using linear regression for a robust estimate.

4. **Opportunity Selection:**  
   The PlanningAgent identifies the best deal (highest discount) and, if it exceeds a threshold, triggers a notification.

5. **Notification & Visualization:**  
   - Sends push notifications for high-value deals.
   - Updates the Gradio dashboard with new deals, logs, and a 3D plot of deal embeddings.

---

## Example Notification

```
Deal Alert! Price=$505.00, Estimate=$902.21, Discount=$397.21 : The Refurb... https://www.dealnews.com/products/Samsung/Unlocked-Samsung-Galaxy-S23-Ultra-512-GB-Smartphone/405671.html?iref=rss-c142
```

---

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## License

This project is licensed under the MIT License.

---

## Acknowledgements

- [Meta Llama](https://ai.meta.com/llama/)
- [Together API](https://www.together.ai/)
- [Modal](https://modal.com/)
- [ChromaDB](https://www.trychroma.com/)
- [Gradio](https://gradio.app/)
- [Pushover](https://pushover.net/)
