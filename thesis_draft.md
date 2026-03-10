# Chapter 3: System Architecture

## 3.1 Overview of the Hybrid AI Educational Platform
The Hybrid AI Educational Platform is designed as a polyglot, multi-model system that seamlessly integrates traditional rule-based Natural Language Processing (NLP) techniques with both local and cloud-based Large Language Models (LLMs). This hybrid architecture allows the system to balance computational efficiency, data privacy, and advanced reasoning capabilities. 

The architecture is divided into two primary tiers:
1. **The Dynamic Frontend Presentation Layer:** A lightweight, browser-based UI built with HTML, Tailwind CSS, and Vanilla JavaScript, optimized for seamless user experience without the overhead of heavy JavaScript frameworks.
2. **The FastAPI Backend Service Layer:** A high-performance Python backend responsible for orchestrating the various AI models and NLP pipelines.

## 3.2 The Polyglot Multi-Model Approach
The core novelty of this platform lies in its "Polyglot" model architecture, strategically routing tasks to the most appropriate processing engine based on the task's complexity and latency requirements.

### 3.2.1 Abstractive Summarization (Local LLM)
For document summarization, the system utilizes a locally hosted `facebook/bart-large-cnn` sequence-to-sequence model globally renowned for high-quality abstractive English summarization. By running this model locally via the HuggingFace `transformers` and `PyTorch` libraries, the platform ensures that large, sensitive user uploaded documents (PDFs and raw text) are processed without incurring cloud API costs or transmitting large payloads over the network.

### 3.2.2 Structured Quiz Generation (Rule-Based NLP)
Generating structured, deterministic educational content (e.g., Multiple Choice Questions, True/False, Fill-in-the-Blanks, and Flashcards) requires a high degree of precision that generative LLMs often struggle with (e.g., hallucinating answers or failing to follow strict JSON schemas). To solve this, the architecture employs `spaCy` (using the `xx_ent_wiki_sm` model) combined with deterministic, rule-based heuristics. This approach guarantees grammatically correct distractors and accurate Named Entity Recognition (NER) for knowledge extraction.

### 3.2.3 Voice-Interactive Agent (Cloud LLM)
For open-ended, real-time conversational tutoring, the system integrates the **Gemini 2.5 Flash API** via the `google-genai` SDK. As the fastest state-of-the-art model on the Google Cloud tier, Gemini 2.5 Flash provides the low-latency reasoning required for a fluid voice interface. To synchronize the agent's knowledge with the user's current study session, the FastAPI backend injects the locally generated `BART` summary directly into the Gemini model's strict `system_instruction` configuration.

## 3.3 Component Interaction Flow
1. **Document Ingestion:** The user drags and drops a PDF into the Tailwind UI. The file is sent via `multipart/form-data` to the FastAPI backend.
2. **Parsing & Summarization:** The backend parses the PDF using `PyPDF2` and passes the extracted text to the local `BART-Large-CNN` model. A rich, heavily-detailed executive summary is returned to the UI.
3. **Knowledge Extraction:** The same extracted text is routed to the `QuizGenerator` class, where `spaCy` performs NER to generate structured quizzes.
4. **Contextual Auditory Tutoring:** When the user interacts with the floating Voice Tutor widget, the browser's native **Web Speech API** captures the microphone audio and transcribes it to text. This text, alongside the previously generated document summary, is sent to the `/api/voice-chat` endpoint. The Gemini 2.5 Flash model processes the prompt and returns a response, which the Web Speech API then synthesizes back into audio for the user.


---

# Chapter 4: Implementation Details

## 4.1 Backend Implementation (FastAPI)
The backend is built using FastAPI due to its asynchronous capabilities and automatic OpenAPI documentation generation. 

- **Hardware Acceleration Consideration:** The system dynamically checks for CUDA availability using `torch.cuda.is_available()`. Due to local hardware constraints, the `BART-Large-CNN` model is presently configured to run on CPU cores using native `torch.float32` precisions, maximizing compatibility and stability.
- **Endpoint Design:** The API exposes three primary endpoints:
  - `/summarize`: Accepts raw text or PDF files and returns a JSON payload containing the original length, compressed length, and the summary string.
  - `/generate-quizzes`: Processes the text using `spaCy` and returns a complex JSON unmarshalled into four distinct arrays (MCQs, True/False, Blank fills, and Flashcards).
  - `/api/voice-chat`: Acts as a secure proxy to the Gemini API, combining user queries with session context to prevent the frontend from exposing API keys.

## 4.2 Frontend Implementation (Tailwind CSS & Vanilla JS)
To achieve the "Light and Dynamic" aesthetic, the frontend eschews heavy frameworks in favor of rapid prototyping with Tailwind CSS via CDN.

- **UI/UX Paradigms:** The interface utilizes soft shadows (`shadow-soft`, `shadow-float`), gradient backgrounds, and glassmorphism elements to create a modern learning environment. 
- **State Management & Perceived Performance:** During API calls, the UI employs CSS-animated skeleton loaders (`animate-pulse` variations) rather than standard spinners. This skeleton loading mechanism reduces the user's perceived waiting time while the local `BART` model processes large documents.
- **Web Speech API Integration:** The floating **Voice Tutor** widget is implemented using JavaScript's native `webkitSpeechRecognition` and `SpeechSynthesisUtterance` interfaces. This allows the platform to achieve voice-in/voice-out capabilities entirely within the browser, eliminating the need for complex internal audio streaming or expensive third-party Text-to-Speech (TTS) services. Visual feedback is provided via synchronized CSS `animate-ping` keyframes that react to the microphone's active state.

## 4.3 Multi-Model Comparative Benchmarking
To formally validate the architectural choices made for the Hybrid Platform, an offline pipeline `evaluate_models.py` was developed to parse unseen test documents against three separate methodological approaches:
1. **BART-Large-CNN:** The preferred, high-quality Abstractive baseline.
2. **mT5-Small:** The old, sequence-to-sequence Abstractive baseline.
3. **TextRank (spaCy/PyTextRank):** A purely Extractive NLP algorithm baseline.

For each sample document, the inference script tracks Processing Latency (Seconds), Compression Ratio (Original Tokens vs Output Tokens), and absolute ROUGE (1, 2, and L) scores. These multidimensional metrics are strictly grouped, quantified, and plotted via `seaborn` and `matplotlib` generated charts, permanently serialized into the `output/` artifacts directory to validate the thesis thesis.
