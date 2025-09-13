

# **An In-Depth Analysis of AI Text Attribution: Technologies, Evaluation, and Visualization with Python**

## **I. The Attribution Problem in the Age of Generative AI**

### **Introduction: The New Frontier of Authorship**

The advent of sophisticated Large Language Models (LLMs) such as GPT-4, LLaMA, and PaLM represents a fundamental paradigm shift in content creation. These models, refined through reinforcement learning from human feedback, can generate text that is not only coherent and contextually relevant but also increasingly indistinguishable from human writing.1 This technological leap has blurred the traditional lines of authorship, introducing significant ambiguity and creating profound challenges for content verification, academic integrity, and the detection of misleading information across digital ecosystems.1

The core of the issue lies in the escalating capabilities of these models. What began as a tool for automated content creation has evolved into a system capable of mimicking diverse human writing styles, making it difficult to discern the origin of a given text. This is not a static problem but a dynamic and escalating "arms race" between the advancement of generative models and the development of detection technologies.3 As LLMs become more powerful, the statistical and linguistic artifacts that once served as reliable markers of machine generation are progressively smoothed away, forcing detection methods to become correspondingly more sophisticated. The decommissioning of OpenAI's own AI Classifier due to its ineffectiveness serves as a stark testament to the difficulty of this task.3

This dynamic has pushed the field beyond a simple binary classification of "human" versus "AI." The rise of human-AI collaborative writing workflows, where AI is used as a tool for drafting, editing, and refining content, has given rise to hybrid texts that defy simple categorization.4 Early detection tools were predicated on the assumption of a clear distinction between the two sources.3 However, research quickly demonstrated their vulnerability to adversarial attacks such as paraphrasing and the use of "AI humanizer" tools, which are specifically designed to alter AI-generated text to mimic human writing patterns.4 The challenge posed by hybrid or "manually edited AI-generated text" is particularly acute, with some studies showing that detection rates for such content can plummet to as low as 30%.9 Consequently, the central question is evolving from "Is this AI-written?" to a more nuanced inquiry: "What percentage of this document is AI-generated, which specific passages are likely machine-authored, and how has the content been modified by a human editor?" This shift from binary detection to granular attribution necessitates not only more advanced analytical techniques but also more sophisticated methods of visualization to appraise and communicate these complex findings.

### **Societal and Ethical Imperatives for Detection**

The need for reliable text attribution is not merely an academic exercise; it is a critical imperative across several societal domains where the authenticity of written communication is paramount.

* **Academic and Scientific Integrity:** The proliferation of LLMs among students has made it increasingly important to distinguish between original student work and content produced or heavily assisted by AI.10 The potential for uncritical use of these tools threatens to undermine the development of critical thinking and writing skills. In the realm of scientific research, the ability of AI to generate plausible-sounding but potentially fabricated text risks watering down the quality of academic publications and eroding the integrity of the scientific record.6  
* **Journalism and Media:** The capacity of LLMs to automate the production of propaganda, fake news, and misinformation at an unprecedented scale poses a direct threat to public discourse and the stability of information ecosystems.1 During critical periods such as election years, the ability to rapidly generate and disseminate convincing but false narratives can undermine public confidence and manipulate opinion, making robust detection a crucial component of digital literacy and platform governance.3  
* **Cybersecurity and Malicious Use:** Beyond misinformation, LLMs can be weaponized for a range of malicious activities. These include generating malicious code for cyberattacks, orchestrating sophisticated phishing and scam campaigns, and automating the spread of hate speech.6 In this context, AI text detection serves as a potential first line of defense, helping to identify and mitigate threats that leverage machine-generated content.  
* **Legal and Copyright Implications:** The ambiguity of AI-assisted authorship creates complex legal challenges related to copyright, intellectual property, and accountability.6 When an LLM generates content trained on vast datasets of human-authored work, questions of ownership and originality become fraught. Reliable attribution technologies could provide a technical foundation for navigating these legal gray areas by offering evidence of a text's provenance.

## **II. Foundational Analysis: Statistical and Linguistic Fingerprints**

At the heart of AI text detection lies the hypothesis that machine-generated and human-written texts possess fundamental, measurable differences in their statistical properties and linguistic structures.7 While advanced LLMs are adept at mimicking human style, they are still products of a probabilistic process, which can leave subtle, "unnatural" fingerprints in the text they produce. This section deconstructs these core differentiators, from foundational metrics to a broader toolkit of stylometric features.

### **The Core Duo: Perplexity and Burstiness**

Among the most widely cited metrics for distinguishing AI from human text are perplexity and burstiness. These two measures form the cornerstone of many early and contemporary detection systems, including popular tools like GPTZero.1

* **Perplexity:** In the context of natural language processing, perplexity is a measurement of how well a probability model predicts a sample. It can be intuitively understood as a measure of a language model's "surprise" when encountering a sequence of words.4 A low perplexity score indicates that the model finds the text predictable and is not surprised by the word choices, while a high perplexity score suggests the text is unpredictable and contains unexpected linguistic constructions.3 Formally, for a tokenized sequence  
  X=(x0​,x1​,…,xt​), the perplexity is defined as the exponentiated average negative log-likelihood of the sequence:

  PPL(X)=exp{−t1​i∑t​logpθ​(xi​∣x\<i​)}

  where pθ​(xi​∣x\<i​) is the probability of the i-th token given the preceding tokens, according to the model θ.13 Autoregressive (AR) language models, which generate text token-by-token, tend to favor high-probability, statistically common word choices. This results in text that is highly predictable to another language model, and therefore, AI-generated text is generally expected to exhibit  
  **lower perplexity** than human-written text, which is often more creative and less predictable.10  
* **Burstiness:** Burstiness measures the variation in sentence length and structure within a document.3 Human writing is characterized by a natural rhythm and flow, often featuring a dynamic mix of short, declarative sentences and longer, more complex ones. This variability is referred to as high burstiness.4 In contrast, text generated by LLMs can often be more uniform and monotonous in its sentence construction, lacking the natural cadence of human prose. This uniformity results in  
  **lower burstiness**.10 Burstiness can be quantified by calculating the standard deviation of sentence lengths (measured in tokens) within a text.10 A related metric, the Fano Factor, provides another measure of this variability by calculating the ratio of the variance to the mean of sentence lengths.10

While early detection systems operated on the assumption that the absolute values of perplexity and burstiness would be significantly different between AI and human texts, research has shown that this distinction is becoming increasingly blurred.3 There is a moderately strong positive linear relationship between the two metrics for both types of text.3 As LLMs become more sophisticated—particularly with the advent of non-autoregressive architectures like diffusion models or the use of "AI humanizer" tools—they are better able to generate text that mimics the perplexity and burstiness patterns of human writing, thereby undermining the reliability of these two metrics in isolation.8

### **A Deeper Stylometric Toolkit: Beyond the Basics**

The diminishing efficacy of perplexity and burstiness alone has necessitated a shift towards a more comprehensive analytical approach. This involves leveraging a broader suite of classic stylometric and linguistic features to build a more robust and multi-faceted "fingerprint" of a text's origin. This trend represents a "back to fundamentals" movement, where the field is rediscovering the power of deep linguistic analysis that has been a staple of computational linguistics for decades. While initial detection methods focused on computationally simple statistics directly tied to the probabilistic nature of LLMs, defeating modern models requires examining the deeper, structural choices of language that are more difficult for an algorithm to perfectly replicate.

#### **Lexical Features**

These features analyze the vocabulary and word choices within a text.

* **Vocabulary Richness and Diversity:** This can be measured using metrics like the Type-Token Ratio (TTR), which is the ratio of unique words (types) to the total number of words (tokens). AI models, particularly older or less complex ones, can sometimes exhibit reduced lexical fidelity or a more repetitive vocabulary compared to humans.8  
* **Word and Syllable Counts:** Simple but effective features include the average word length and the average number of syllables per word. These can be indicative of stylistic complexity.1  
* **Functional Word Usage:** The frequency of common functional words (e.g., articles, prepositions, conjunctions) can vary systematically between human and AI-generated text and can serve as a subtle stylistic marker.2

#### **Syntactic and Structural Features**

These features examine the grammatical construction and organization of sentences.

* **Sentence Complexity:** This is often measured by the average sentence length in words and the variance of sentence lengths across the document.2  
* **Part-of-Speech (POS) Tagging:** By tagging each word with its grammatical role (e.g., noun, verb, adjective, adverb), one can analyze the distribution of these roles. Research has shown that MGT detection classifiers can be highly sensitive to the distribution of specific POS tags, such as the frequency of adverbs, which can differ between human and machine prose.1  
* **Punctuation Distribution:** The frequency and spread of various punctuation marks (commas, periods, semicolons) can also serve as a statistical indicator of authorship style.2  
* **Active vs. Passive Voice Usage:** The ratio of sentences written in the active voice versus the passive voice is a significant stylistic feature that can be quantified and used for classification.

#### **Readability Scores**

Readability metrics, which algorithmically assess the complexity of a text, can also provide valuable features for classification.

* **Flesch Reading Ease & Flesch-Kincaid Grade Level:** These widely used scores combine metrics like average sentence length and average syllables per word to estimate how difficult a text is to read.  
* **Gunning Fog Index:** This index provides an estimate of the years of formal education a person needs to understand the text on a first reading, with a focus on identifying "complex" words (those with three or more syllables).

The following table synthesizes these key differentiators, providing a reference for the features that form the basis of modern detection systems.

| Feature | Description | How It's Measured | Typical AI Signature | Typical Human Signature |
| :---- | :---- | :---- | :---- | :---- |
| **Perplexity** | A measure of how "surprising" a text is to a language model. | Exponentiated average negative log-likelihood of a token sequence. 13 | Lower (more predictable, common word choices). 12 | Higher (more creative, unexpected word choices). 3 |
| **Burstiness** | The variation in sentence length and structure. | Standard deviation of sentence lengths (in tokens). 10 | Lower (more uniform sentence structure). 12 | Higher (dynamic mix of short and long sentences). 4 |
| **Fano Factor** | A measure of dispersion related to burstiness. | Ratio of variance to the mean of sentence lengths. 10 | Lower (less variation). 12 | Higher (more variation). 12 |
| **Lexical Diversity (TTR)** | The richness of the vocabulary used in a text. | Ratio of unique words (types) to total words (tokens). | Potentially Lower. 8 | Typically Higher. 15 |
| **Flesch-Kincaid Score** | A readability metric assessing text complexity. | Formula based on average sentence length and syllables per word. | Varies by model and prompt. | Varies by author and style. |
| **Gunning Fog Index** | A readability metric estimating the education level required to understand the text. | Formula based on average sentence length and percentage of complex words. | Varies by model and prompt. | Varies by author and style. |
| **Sentence Length Variance** | The statistical variance in the length of sentences. | Statistical variance of sentence lengths (in words or tokens). 2 | Lower. 10 | Higher. 12 |
| **POS Tag Ratios** | The frequency distribution of grammatical parts of speech (e.g., nouns, verbs, adverbs). | Count occurrences of each POS tag and normalize by total words. 1 | Can exhibit unnatural distributions. 17 | Follows natural linguistic patterns. 17 |
| **Passive Voice Usage** | The proportion of sentences constructed in the passive voice. | Ratio of passive voice sentences to total sentences. | Varies by model and prompt. | Varies by author and style. |

## **III. Machine Learning Paradigms for Text Classification**

While individual statistical and linguistic features provide valuable signals, their true power is realized when they are integrated into machine learning (ML) models trained to perform automated classification. These models learn to weigh the various features and identify the complex, non-linear patterns that differentiate AI-generated text from human writing. The development of an effective ML-based detector involves a standard pipeline of feature engineering, model selection, and evaluation.

### **Feature Engineering and Data Representation**

Before text data can be fed into an ML algorithm, it must be transformed into a structured, numerical format. This process involves several critical steps.

* **Preprocessing:** The initial stage involves cleaning the raw text data. A crucial first step is **duplicate removal** from the training set to prevent the model from overfitting to redundant examples.18 The text is then broken down into smaller units through  
  **tokenization**. Modern tokenizers, such as the Byte-Pair Encoding (BPE) implementation found in the Hugging Face tokenizers library, are often used to handle words and sub-word units effectively.18  
* **Vectorization:** This is the process of converting the processed tokens into numerical vectors. Several techniques are commonly employed:  
  * **TF-IDF (Term Frequency-Inverse Document Frequency):** This classic vectorization method creates a matrix where each entry represents the importance of a word in a document relative to the entire corpus. It effectively highlights words that are frequent in a specific text but rare overall, making it a powerful feature for text classification.2  
  * **N-gram Analysis:** To capture local context and phraseology, vectorizers are often configured to consider n-grams (sequences of 2, 3, or more words). This allows the model to learn from common phrases and syntactic patterns. AI-generated text may exhibit an over-reliance on clichéd or statistically common n-grams, which can be a strong detection signal.16  
  * **Embeddings:** More advanced techniques represent words as dense vectors in a high-dimensional space. Models like Word2Vec or GloVe learn these representations by analyzing word co-occurrence patterns in large corpora, allowing them to capture semantic relationships (e.g., the vectors for "king" and "queen" are related in a meaningful way).16 These embeddings can be used as input features for downstream classifiers.

### **A Spectrum of Classification Models**

Once the text is represented as a numerical feature matrix, a variety of classification algorithms can be trained to distinguish between the "human" and "AI" classes.

* **Traditional Classifiers:** These models are often computationally efficient, more interpretable, and can achieve high performance, especially when paired with a rich set of engineered features.  
  * **Logistic Regression:** A simple and fast linear model that serves as a strong baseline. When optimized with techniques like stochastic gradient descent (SGD), it can learn complex decision boundaries.18  
  * **Multinomial Naive Bayes:** A probabilistic classifier well-suited for text data represented as word counts or TF-IDF vectors. It is known for its simplicity and resistance to overfitting.18  
  * **Support Vector Machines (SVM):** A powerful algorithm that finds an optimal hyperplane to separate the data points of different classes, often effective in high-dimensional feature spaces.19  
  * **Tree-Based Models:** Gradient-boosted decision tree models like **XGBoost**, **LightGBM**, and **CatBoost** are consistently top performers on structured (tabular) data. When a rich set of linguistic features is extracted from text, the problem effectively becomes a tabular classification task where these models excel. Studies have shown XGBoost models achieving accuracy as high as 98% when combined with a comprehensive feature set.1  
* **Deep Learning and Transformer-Based Models:** These models can learn features directly from the text, often bypassing the need for extensive manual feature engineering.  
  * **Recurrent Neural Networks (RNNs) and LSTMs:** These architectures are designed to process sequential data, making them naturally suited for text. They were a cornerstone of NLP before the advent of transformers.  
  * **BERT (Bidirectional Encoder Representations from Transformers):** This model revolutionized NLP by learning deep bidirectional representations from unlabeled text. By fine-tuning a pre-trained BERT model on a labeled dataset of human and AI text, researchers have achieved excellent performance, with reported accuracies of 93% and higher.9  
    **RoBERTa**, a robustly optimized version of BERT, has demonstrated even greater success, reaching an accuracy of 99.73% on the HC3-English dataset when combined with linguistic features.

### **Ensemble Methods for Enhanced Robustness**

Rather than relying on a single model, a more robust approach is to use an **ensemble**, which combines the predictions of multiple, complementary classifiers. This strategy can lead to significant improvements in accuracy and generalization by mitigating the weaknesses of any individual model.18 A common technique is

**soft-voting**, where the final classification is determined by averaging the probabilistic predictions from each model in the ensemble. A practical example of this is a system that combines Multinomial Naive Bayes, Logistic Regression, LightGBM, and CatBoost, leveraging the diverse strengths of each algorithm.18

The choice between these modeling paradigms reveals a critical performance trade-off. While complex transformer models like BERT demonstrate state-of-the-art accuracy by learning features implicitly from raw text 20, simpler and more traditional models like XGBoost can achieve nearly equivalent performance when provided with a comprehensive, well-engineered set of linguistic features. This suggests two viable paths to high-accuracy detection: a "heavy model" approach that relies on the power of large transformers and a "heavy feature engineering" approach that pairs classical ML models with deep linguistic analysis. The optimal strategy is not universal but depends on the specific context, including available computational resources and domain expertise. An organization with deep NLP and linguistics expertise but limited GPU capacity might favor the feature engineering route, while one with massive compute resources might opt to fine-tune a large transformer. This duality explains why even in the age of transformers, traditional classifiers remain highly relevant and are often key components of powerful ensemble systems.18

The following table provides a comparative overview of the machine learning classifiers commonly used for AI text detection.

| Model/Algorithm | Model Family | Key Strengths | Key Weaknesses/Limitations | Typical Accuracy Range (from sources) |
| :---- | :---- | :---- | :---- | :---- |
| **Logistic Regression** | Linear | Fast, interpretable, good baseline, effective with strong features. 18 | May underfit complex, non-linear relationships. | 70-85% |
| **Multinomial Naive Bayes** | Probabilistic | Simple, fast to train, avoids overfitting, works well with TF-IDF features. 18 | Relies on a strong feature independence assumption that is often violated in text. | 70-85% |
| **Support Vector Machines (SVM)** | Linear / Kernel-based | Effective in high-dimensional spaces, robust. 19 | Can be computationally intensive and less interpretable. | 81-90% 20 |
| **XGBoost / LightGBM** | Tree-based Ensemble | High performance on tabular/feature data, robust to noise, handles feature interactions well. 18 | Can be prone to overfitting if not carefully tuned; less interpretable than linear models. | 84-98% 1 |
| **BERT / RoBERTa** | Transformer | State-of-the-art performance, learns context and features implicitly, requires less feature engineering. 20 | Computationally expensive to train/fine-tune, requires large datasets, can be a "black box". | 93-99%+ 1 |

## **IV. The Frontier of Detection: Zero-Shot Methods and Cryptographic Watermarking**

As the race between generative models and detection systems intensifies, researchers are exploring more advanced and proactive paradigms that move beyond traditional supervised classification. Two of the most promising frontiers are zero-shot detection methods, which require no training on labeled data, and cryptographic watermarking, which embeds an undetectable signal into text at the moment of its creation.

### **Zero-Shot Detection: No Training Required**

The concept of zero-shot detection aims to identify AI-generated text without the need to train a dedicated classifier on large, labeled datasets of human and AI examples. The most prominent method in this category is **DetectGPT**.

* **The DetectGPT Mechanism:** Developed by researchers at Stanford University, DetectGPT is founded on the "negative curvature" hypothesis.2 This principle posits that text generated by an LLM tends to occupy a very sharp peak in that model's probability distribution. In other words, the model assigns a significantly higher probability to the exact text it generated compared to very similar, slightly altered versions of that text.8 Human-written text, by contrast, does not typically form such a sharp peak; its log-probability as judged by the model is more stable under minor paraphrasing or word substitutions.8  
* **Implementation:** To test a given passage, DetectGPT uses a perturbation technique. It generates multiple minor variations of the passage (e.g., by masking and refilling some words using another model like T5). It then compares the log-probability of the original passage to the average log-probability of the perturbed versions, as calculated by the source LLM. If there is a large, statistically significant drop in probability for the perturbed versions, the text is flagged as likely machine-generated.21  
* **Advantages and Limitations:** The primary advantage of DetectGPT is that it is a "zero-shot" method, eliminating the costly and time-consuming process of data collection and classifier training.8 However, its critical limitation is the requirement of access to the source language model's output probabilities (logits). This makes it impractical for use with many commercial, API-gated models like ChatGPT or Bard, which do not expose these internal calculations to the public.21

### **Proactive Attribution via Cryptographic Watermarking**

Watermarking represents a paradigm shift from reactive, post-hoc detection to proactive, embedded attribution. Instead of trying to find statistical artifacts left behind by a model, watermarking intentionally embeds a secret, algorithmically verifiable signal into the generated text that is invisible to human readers but easily detectable by a corresponding algorithm.21

* **The Kirchenbauer et al. Framework:** The most widely cited and influential watermarking scheme was proposed by Kirchenbauer et al. and provides a robust and practical framework for implementation.24  
  1. **Vocabulary Partitioning:** Before each token is generated, the system uses a cryptographic hash function on the preceding token (or a sequence of preceding tokens) to seed a pseudorandom number generator. This generator then partitions the model's entire vocabulary into a "green list" of tokens and a "red list" of tokens.21  
  2. **Soft Logit Modification:** During the text generation process, the system applies a "soft" rule. Instead of strictly forbidding tokens from the red list, it adds a small positive constant, delta (δ), to the logits (the raw, pre-probability scores) of all tokens on the green list. This subtly biases the model's sampling process, making it more likely to choose a green-listed token without a noticeable degradation in text quality.24  
  3. **Public and Efficient Detection:** A third party can detect the watermark without access to the LLM's API or parameters. The detection algorithm, which can be open-sourced, simply needs to know the hash function. It can then re-compute the green/red lists for each token in a given text and count the number of generated tokens that fall on the green list. A one-proportion z-test is then used to determine if the observed count of green tokens is statistically significantly higher than what would be expected by random chance. This provides a rigorous p-value indicating the confidence of the detection.24  
* **Robustness and Cryptographic Guarantees:** This watermarking scheme is designed to be robust against common attacks. While paraphrasing can dilute the watermark's signal, studies show that it often preserves enough of the original n-grams and high-entropy token sequences (like names or numbers) for the watermark to remain detectable in passages of sufficient length (e.g., 800 tokens).25 The entire process can be formalized using cryptographic principles, aiming for  
  **undetectability** (the watermarked model's output is statistically indistinguishable from the original) and **soundness** (the probability of human-written text being falsely flagged as watermarked is negligible).26

The emergence of these advanced techniques, particularly watermarking, signals a potential shift in the power dynamics of content moderation. Reactive detection methods place the burden of analysis on the content consumer or platform (e.g., a university, a social media site), leading to a decentralized and often inconsistent landscape of detection quality.9 Watermarking, in contrast, is a proactive and centralized approach where the LLM provider embeds the signal at the source. This could empower platforms to enforce authenticity policies with much higher confidence. Instead of building a probabilistic case based on a detector with known error rates, the presence of a watermark could serve as near-definitive cryptographic proof of a text's origin. This shifts the burden of proof in an academic integrity case, for example, from the institution proving AI use to the student explaining the presence of a cryptographic signature from an LLM. However, this centralization also raises new concerns about control, user privacy, and the potential for a "chilling effect" on the legitimate use of AI as a writing assistant if all such usage becomes permanently trackable.

## **V. A Python-Based Toolkit for Contribution Analysis**

This section provides a practical guide to implementing the analytical techniques discussed previously, complete with annotated Python code. It serves as a starting point for building a custom toolkit for evaluating AI and human contributions to written documentation.

### **Environment Setup and Core Libraries**

A robust Python environment is essential for this work. It is recommended to use a virtual environment to manage dependencies. The core libraries that form the foundation of this toolkit are:

* **transformers and torch:** The Hugging Face transformers library provides access to thousands of pre-trained models, including those needed for calculating perplexity. PyTorch is the underlying deep learning framework.10  
* **nltk and spacy:** These are foundational libraries for natural language processing. They provide essential tools for text preprocessing, such as sentence splitting (sentencization) and tokenization.27  
* **scikit-learn:** The primary library for traditional machine learning in Python, offering tools for vectorization, model training, and evaluation.18  
* **pandas:** A crucial library for data manipulation and analysis, used for handling datasets and feature matrices.30

The following table summarizes the key libraries and their roles in this analysis.

| Library Name | Primary Use Case in AI Text Analysis | Key Functions/Classes |
| :---- | :---- | :---- |
| **Hugging Face transformers** | Accessing pre-trained LLMs, tokenizers, and calculating perplexity. | AutoTokenizer, AutoModelForCausalLM |
| **torch** | Deep learning framework for model operations and tensor math. | torch.no\_grad(), torch.exp(), outputs.loss |
| **spacy** | Industrial-strength NLP for tokenization and sentence splitting. | spacy.load(), doc.sents |
| **nltk** | Foundational NLP library for text processing tasks. | sent\_tokenize, word\_tokenize |
| **scikit-learn** | Machine learning pipeline: vectorization, classification, evaluation. | TfidfVectorizer, LogisticRegression, classification\_report |
| **pandas** | Data manipulation, handling datasets and results. | DataFrame, Series, read\_csv() |
| **matplotlib** | Foundational library for static and annotated visualizations. | pyplot.figure(), pyplot.bar(), pyplot.annotate() |
| **seaborn** | High-level statistical data visualization based on Matplotlib. | heatmap(), barplot(), histplot() |
| **plotly** | Library for creating interactive, web-based visualizations. | express.pie(), graph\_objects.Scatterpolar |
| **highlight\_text** | Matplotlib extension for advanced text highlighting and annotation. | ax\_text(), fig\_text() |
| **TypeTruth** | Open-source Python library specifically for AI text detection. | AITextDetector (hypothetical class name) |

### **Calculating Core Statistical Metrics**

The following Python functions demonstrate how to compute perplexity and burstiness for a given text.

#### **Perplexity Calculation**

This function calculates perplexity using a pre-trained GPT-2 model from Hugging Face. It employs a sliding window approach to handle texts longer than the model's maximum context length, ensuring a more accurate approximation of the fully-factorized perplexity.10

Python

import torch  
from transformers import AutoModelForCausalLM, AutoTokenizer  
import numpy as np

\# Load pre-trained GPT-2 model and tokenizer  
model\_name \= 'gpt2'  
model \= AutoModelForCausalLM.from\_pretrained(model\_name)  
tokenizer \= AutoTokenizer.from\_pretrained(model\_name)  
model.eval() \# Set model to evaluation mode

def calculate\_perplexity(text, stride=512):  
    """  
    Calculates the perplexity of a given text using a sliding window approach.  
    Based on the methodology from Hugging Face and research snippet.\[10\]  
    """  
    encodings \= tokenizer(text, return\_tensors='pt', truncation=True)  
    input\_ids \= encodings.input\_ids  
    seq\_len \= input\_ids.size(1)  
      
    \# Use model's max length if available, otherwise default to 1024  
    max\_length \= model.config.max\_position\_embeddings if hasattr(model.config, 'max\_position\_embeddings') else 1024  
      
    nlls \= \# Negative log-likelihoods  
    prev\_end\_loc \= 0  
      
    if seq\_len \== 0:  
        return 0.0

    for begin\_loc in range(0, seq\_len, stride):  
        end\_loc \= min(begin\_loc \+ max\_length, seq\_len)  
        trg\_len \= end\_loc \- prev\_end\_loc  
        input\_ids\_chunk \= input\_ids\[:, begin\_loc:end\_loc\]  
        target\_ids \= input\_ids\_chunk.clone()  
        target\_ids\[:, :-trg\_len\] \= \-100 \# Mask tokens that are not part of the target

        with torch.no\_grad():  
            outputs \= model(input\_ids\_chunk, labels=target\_ids)  
            neg\_log\_likelihood \= outputs.loss \* trg\_len  
          
        nlls.append(neg\_log\_likelihood)  
        prev\_end\_loc \= end\_loc  
        if end\_loc \== seq\_len:  
            break  
              
    \# Calculate perplexity  
    ppl \= torch.exp(torch.stack(nlls).sum() / seq\_len)  
    return ppl.item()

\# Example Usage  
human\_text \= "This is a sentence written by a human, with all its quirks and nuances. It might be a bit unpredictable."  
ai\_text \= "The primary function of this sentence is to convey information in a clear and concise manner."

perplexity\_human \= calculate\_perplexity(human\_text)  
perplexity\_ai \= calculate\_perplexity(ai\_text)

print(f"Perplexity of Human Text: {perplexity\_human:.2f}")  
print(f"Perplexity of AI Text: {perplexity\_ai:.2f}")

#### **Burstiness and Stylometric Features**

These functions use spacy for robust sentence segmentation and numpy for statistical calculations to determine burstiness and related metrics.10

Python

import spacy  
import numpy as np

\# Load a spaCy model for sentence tokenization  
try:  
    nlp \= spacy.load("en\_core\_web\_sm")  
except OSError:  
    print("Downloading 'en\_core\_web\_sm' model...")  
    from spacy.cli import download  
    download("en\_core\_web\_sm")  
    nlp \= spacy.load("en\_core\_web\_sm")

def calculate\_burstiness(text):  
    """Calculates the burstiness of a text (std dev of sentence lengths)."""  
    doc \= nlp(text)  
    sentence\_lengths \= \[len(tokenizer.encode(sent.text)) for sent in doc.sents if sent.text.strip()\]  
    if not sentence\_lengths:  
        return 0.0  
    return np.std(sentence\_lengths)

def calculate\_fano\_factor(text):  
    """Calculates the Fano Factor of a text (variance/mean of sentence lengths)."""  
    doc \= nlp(text)  
    sentence\_lengths \= \[len(tokenizer.encode(sent.text)) for sent in doc.sents if sent.text.strip()\]  
    if not sentence\_lengths or np.mean(sentence\_lengths) \== 0:  
        return 0.0  
    mean\_length \= np.mean(sentence\_lengths)  
    variance \= np.var(sentence\_lengths)  
    return variance / mean\_length if mean\_length \> 0 else 0.0

\# Example Usage  
burstiness\_human \= calculate\_burstiness(human\_text)  
burstiness\_ai \= calculate\_burstiness(ai\_text)  
fano\_human \= calculate\_fano\_factor(human\_text)  
fano\_ai \= calculate\_fano\_factor(ai\_text)

print(f"Burstiness of Human Text: {burstiness\_human:.2f}")  
print(f"Burstiness of AI Text: {burstiness\_ai:.2f}")  
print(f"Fano Factor of Human Text: {fano\_human:.2f}")  
print(f"Fano Factor of AI Text: {fano\_ai:.2f}")

### **Implementing a Machine Learning Detector**

This example demonstrates a simplified pipeline for training a Logistic Regression classifier using scikit-learn and TF-IDF features. It uses a publicly available dataset for demonstration purposes.10

Python

import pandas as pd  
from sklearn.model\_selection import train\_test\_split  
from sklearn.feature\_extraction.text import TfidfVectorizer  
from sklearn.linear\_model import LogisticRegression  
from sklearn.metrics import classification\_report  
from datasets import load\_dataset

\# Load a dataset for AI text detection  
\# Using a subset for faster demonstration  
try:  
    dataset \= load\_dataset("arincon/llm-detect-dataset", split='train\[:2000\]')  
    df \= pd.DataFrame(dataset)  
except Exception as e:  
    print(f"Could not load dataset. Using dummy data. Error: {e}")  
    \# Create a dummy dataframe if dataset loading fails  
    data \= {'text': \[human\_text, ai\_text\] \* 100, 'label':  \* 100}  
    df \= pd.DataFrame(data)

\# 1\. Data Preparation  
X \= df\['text'\]  
y \= df\['label'\]  
X\_train, X\_test, y\_train, y\_test \= train\_test\_split(X, y, test\_size=0.2, random\_state=42, stratify=y)

\# 2\. Feature Extraction (Vectorization)  
vectorizer \= TfidfVectorizer(ngram\_range=(1, 3), sublinear\_tf=True, max\_features=10000)  
X\_train\_tfidf \= vectorizer.fit\_transform(X\_train)  
X\_test\_tfidf \= vectorizer.transform(X\_test)

\# 3\. Model Training  
model \= LogisticRegression(solver='liblinear', random\_state=42)  
model.fit(X\_train\_tfidf, y\_train)

\# 4\. Prediction and Evaluation  
y\_pred \= model.predict(X\_test\_tfidf)

print("Classification Report:")  
print(classification\_report(y\_test, y\_pred, target\_names=\['Human', 'AI'\]))

\# Example prediction on new text  
new\_texts \= \[human\_text, ai\_text\]  
new\_texts\_tfidf \= vectorizer.transform(new\_texts)  
predictions \= model.predict(new\_texts\_tfidf)  
proba\_predictions \= model.predict\_proba(new\_texts\_tfidf)

for text, pred, proba in zip(new\_texts, predictions, proba\_predictions):  
    label \= 'AI' if pred \== 1 else 'Human'  
    print(f"\\nText: '{text\[:50\]}...'")  
    print(f"Predicted: {label}")  
    print(f"Probabilities (Human, AI): ({proba:.2f}, {proba:.2f})")

### **Leveraging Open-Source Libraries and APIs**

While building a custom model provides maximum control, several open-source libraries and commercial APIs offer ready-to-use solutions.

* **Open-Source Libraries:** The Python ecosystem contains several projects aimed at AI text detection. A notable example is **TypeTruth**, an open-source library designed for this purpose. Its key features include the ability to perform detection at both the sentence and paragraph level, and it provides built-in visualization tools like bar plots and heatmaps to help interpret the results.31 Other relevant projects can be found on platforms like GitHub, often leveraging transformers or traditional ML models to perform classification.33  
* **Commercial APIs:** For applications requiring high accuracy without the overhead of model development and maintenance, commercial APIs are a viable option. Leading providers include **GPTZero**, **Originality.AI**, and **Copyleaks**. These services are continuously updated to handle the latest LLMs and often incorporate additional features like plagiarism detection. They are typically accessed via a simple API call, returning a probability score indicating the likelihood of AI generation.31

## **VI. Visualizing Provenance: A Guide to Effective Appraisal in Python**

Effective visualization is critical for transforming raw detection scores into actionable insights. A simple probability score may be insufficient for complex decision-making; a well-designed chart can reveal patterns, highlight suspicious passages, and provide a more nuanced understanding of a document's composition. This section provides Python code examples for creating three types of visualizations: aggregate contribution charts, comparative feature dashboards, and granular, sentence-level analyses.

### **Aggregate Contribution Charts (The Big Picture)**

These visualizations provide a high-level summary of a document's overall composition, answering the question: "What is the total proportion of AI vs. human contribution?" After classifying each sentence or paragraph, the results can be aggregated and displayed in a pie or bar chart.

The following code uses Plotly Express to create an interactive pie chart, which is excellent for clear, at-a-glance summaries.37

Python

import plotly.express as px  
import pandas as pd

\# Assume we have classified each sentence and stored the results  
\# 0 \= Human, 1 \= AI  
sentence\_labels \=  

\# Aggregate the results  
human\_count \= sentence\_labels.count(0)  
ai\_count \= sentence\_labels.count(1)  
total\_count \= len(sentence\_labels)

human\_percent \= (human\_count / total\_count) \* 100  
ai\_percent \= (ai\_count / total\_count) \* 100

\# Create a DataFrame for Plotly  
data \= {  
    'Author': \['Human', 'AI'\],  
    'Contribution (%)': \[human\_percent, ai\_percent\],  
    'Sentence Count': \[human\_count, ai\_count\]  
}  
df\_agg \= pd.DataFrame(data)

\# Create the pie chart  
fig \= px.pie(df\_agg,   
             values='Contribution (%)',   
             names='Author',   
             title='Aggregate Contribution Analysis of Document',  
             color='Author',  
             color\_discrete\_map={'Human':'\#1f77b4', 'AI':'\#d62728'},  
             hover\_data=,  
             labels={'Contribution (%)':'Contribution Percentage'})

fig.update\_traces(textposition='inside', textinfo='percent+label')  
fig.show()

### **Comparative Linguistic Feature Dashboards**

These visualizations are designed to compare the linguistic "fingerprints" of two or more texts. This is particularly useful for tasks like comparing a student's submission to their past work or evaluating a suspicious text against a known human-written baseline.

#### **Radar Chart for Multivariate Comparison**

A radar chart (or spider plot) is exceptionally effective for visualizing the multivariate profiles of different texts across several linguistic features simultaneously. The following code uses Plotly's graph\_objects to create a comparative radar chart.39

Python

import plotly.graph\_objects as go  
import pandas as pd  
import numpy as np

\# Assume we have calculated and normalized linguistic features for two texts  
\# Normalization (e.g., min-max scaling) is crucial for a meaningful radar chart  
features \=

\# Hypothetical normalized scores (0-1 scale)  
text1\_scores \= \[0.3, 0.4, 0.8, 0.7, 0.6\] \# Profile of Text 1 (e.g., Human)  
text2\_scores \= \[0.8, 0.7, 0.3, 0.4, 0.4\] \# Profile of Text 2 (e.g., AI)

fig \= go.Figure()

\# Add trace for Text 1  
fig.add\_trace(go.Scatterpolar(  
      r=text1\_scores,  
      theta=features,  
      fill='toself',  
      name='Text 1 (Suspected Human)'  
))

\# Add trace for Text 2  
fig.add\_trace(go.Scatterpolar(  
      r=text2\_scores,  
      theta=features,  
      fill='toself',  
      name='Text 2 (Suspected AI)'  
))

fig.update\_layout(  
  title='Comparative Linguistic Feature Analysis',  
  polar=dict(  
    radialaxis=dict(  
      visible=True,  
      range\=  
    )),  
  showlegend=True  
)

fig.show()

### **Granular Analysis: Sentence-Level Heatmaps and Text Highlighting**

The most powerful visualizations move beyond aggregate scores to pinpoint exactly *which parts* of a document are likely AI-generated. This provides specific, actionable evidence.

#### **Heatmap of Sentence Probabilities**

A heatmap can provide an intuitive, high-level overview of AI probability distribution across a document. The y-axis represents each sentence, and the color of the cell indicates its probability of being AI-generated. The following code uses Seaborn to create such a heatmap.40

Python

import seaborn as sns  
import matplotlib.pyplot as plt  
import numpy as np

\# Assume we have an array of AI probabilities for each sentence  
sentence\_ai\_probs \= np.random.rand(20, 1) \# 20 sentences, each with an AI probability

\# Create the heatmap  
plt.figure(figsize=(4, 8))  
sns.heatmap(sentence\_ai\_probs,   
            cmap='vlag', \# A diverging colormap (e.g., blue-white-red)  
            annot=True,   
            fmt=".2f",  
            linewidths=.5,  
            cbar\_kws={'label': 'AI-Generated Probability'},  
            vmin=0,   
            vmax=1)

plt.title('Sentence-Level AI Contribution Heatmap')  
plt.xlabel('Probability Score')  
plt.ylabel('Sentence Number')  
plt.yticks(np.arange(20) \+ 0.5, np.arange(1, 21), rotation=0)  
plt.show()

#### **Interactive Text Highlighting**

The most direct and interpretable visualization is to display the text itself, with the background of each word or sentence colored according to its AI probability score. This can be achieved in Matplotlib using the highlight\_text library. The key is to programmatically construct the input string with \<highlight\> tags and a corresponding list of properties for each highlighted segment, where the background color is determined by the AI score.42

Python

import matplotlib.pyplot as plt  
from highlight\_text import fig\_text  
import numpy as np  
import matplotlib.colors as mcolors

\# Sample text and corresponding AI probability scores per sentence  
full\_text \= "This is the first sentence, written by a human. The second sentence, however, was generated by an advanced AI model. It exhibits a very low perplexity and uniform structure. The final sentence returns to a human author, providing a concluding thought."  
sentences \= \[s.strip() for s in full\_text.split('.')\]  
sentences \= \[s for s in sentences if s\]  
scores \= \[0.15, 0.92, 0.85, 0.20\] \# AI probability for each sentence

\# Function to map a score (0-1) to a color from a colormap  
def score\_to\_color(score, cmap=plt.get\_cmap('vlag'), vmin=0, vmax=1):  
    norm \= mcolors.Normalize(vmin=vmin, vmax=vmax)  
    return mcolors.to\_hex(cmap(norm(score)))

\# Programmatically build the string for highlight\_text  
highlight\_string \= ""  
highlight\_props \=

for sentence, score in zip(sentences, scores):  
    color \= score\_to\_color(score)  
    highlight\_string \+= f"\<{sentence}.\> "  
      
    \# Define the bounding box properties for the background color  
    prop\_dict \= {  
        "bbox": {  
            "edgecolor": "black",  
            "facecolor": color,  
            "linewidth": 0.5,  
            "pad": 2,  
            "alpha": 0.6  
        }  
    }  
    highlight\_props.append(prop\_dict)

\# Create the visualization  
fig, ax \= plt.subplots(figsize=(10, 4))  
ax.axis('off') \# Hide the axes

fig\_text(x=0.05, y=0.85,  
         s=highlight\_string,  
         highlight\_textprops=highlight\_props,  
         fontsize=14,  
         ha='left',  
         va='top',  
         wrap=True,  
         fig=fig)

\# Add a title  
plt.title('Document Analysis with Sentence-Level Highlighting', fontsize=16, pad=20)

\# Manually add a colorbar legend  
cax \= fig.add\_axes(\[0.1, 0.1, 0.8, 0.05\])  
cmap \= plt.get\_cmap('vlag')  
norm \= mcolors.Normalize(vmin=0, vmax=1)  
cb \= plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), cax=cax, orientation='horizontal')  
cb.set\_label('Probability of AI Contribution (0 \= Human, 1 \= AI)')

plt.show()

## **VII. Critical Appraisal: Efficacy, Limitations, and the Path Forward**

While the technologies for AI text attribution are advancing rapidly, it is crucial to approach their application with a sober understanding of their current capabilities and significant limitations. The landscape is fraught with challenges related to accuracy, bias, and the relentless pace of AI development. Responsible implementation requires a nuanced, human-centric approach that treats these tools as aids for investigation rather than infallible arbiters of truth.

### **The Reliability Crisis: A Landscape of Inaccuracy**

Despite claims of high accuracy from some commercial vendors, independent research reveals a significant reliability crisis across the spectrum of AI detection tools.15

* **False Positives and Negatives:** The most pressing issue is the prevalence of incorrect classifications. **False positives**, where human-written content is mistakenly flagged as AI-generated, can lead to unfair accusations and severe consequences for individuals, particularly in academic settings.4 Conversely,  
  **false negatives**, where AI-generated text goes undetected, undermine the very purpose of the tools.4 The accuracy of many free detectors is alarmingly low, with some studies reporting an average accuracy of only 26%.6 Even OpenAI's own classifier was found to mislabel human text frequently.9  
* **Bias and Fairness Concerns:** AI detection models are not immune to the biases present in their training data. A significant concern is that these algorithms may unfairly penalize non-native English speakers or individuals from diverse linguistic backgrounds.6 Writing styles that deviate from the "norm" of the training data—perhaps by exhibiting simpler sentence structures or a less varied vocabulary—may have statistical properties (like lower perplexity) that algorithms misinterpret as hallmarks of AI generation.4 This creates a serious equity issue, where the tools may systematically discriminate against certain groups of writers.  
* **The Evolving Adversary:** The field is in a constant state of flux, with detection technologies perpetually trying to keep pace with the rapid evolution of LLMs. A detector that is effective against text from an older model like GPT-3.5 may be entirely inadequate against the more sophisticated and human-like output of GPT-4 or newer architectures like diffusion models.4 Furthermore, the ecosystem of adversarial tools is growing. "AI humanizers" or paraphrasing tools are now widely available and are designed specifically to rewrite AI text to evade detection, often by restoring human-like levels of perplexity and burstiness.8

### **Recommendations for Responsible Implementation**

Given these profound limitations, it is imperative that organizations and individuals adopt a set of best practices for the responsible use of AI detection tools.

* **Indicators, Not Proof:** There is a strong consensus among researchers, ethicists, and even the creators of these tools (such as Turnitin) that a detection score is a probabilistic assessment, not definitive proof of misconduct.4 An algorithm's output is merely an estimation of the likelihood that another algorithm was used. It should never be the sole basis for academic penalties, content removal, or any other adverse action against an individual.46  
* **A Human-in-the-Loop Approach:** Detection tools are most effective when used as one component of a broader, human-led investigation. A high AI-probability score should be treated as an indicator that warrants further inquiry, not a final verdict. This inquiry should involve other forms of evidence, such as reviewing a document's version history, comparing the text in question with a portfolio of the individual's known writing samples, or conducting an oral examination to assess their understanding of the material.5  
* **Focus on Pedagogy and Assignment Design:** In academic and educational contexts, the most robust and ethical response to the rise of generative AI is not to invest in a technological arms race of detection, but to rethink pedagogy and assignment design. Assignments that require personal reflection, the integration of specific course concepts, original research, or process-oriented tasks (like submitting outlines and drafts) are inherently more resistant to being fully outsourced to AI and do more to foster genuine learning.5

### **Future Outlook**

The future of AI text attribution is likely to be characterized by this ongoing co-evolution of generative and detective technologies. It remains an open question whether robust, unremovable watermarking will become an industry standard, though this would require widespread adoption and consensus among major LLM developers. Some researchers have even argued that perfect, foolproof detection of AI text may be mathematically impossible, as the ultimate goal of generative models is to perfectly replicate the statistical distribution of human language.6

Ultimately, the most productive path forward may involve a conceptual shift away from a punitive framework of "AI detection" and toward a more constructive framework of "AI-human collaboration transparency." In this future, the focus would be less on policing the use of AI and more on developing the tools, standards, and ethical norms for clearly and honestly disclosing the role that AI assistants play in the writing process. The technologies and visualizations detailed in this report, when used responsibly, can be a crucial part of that transparent future, providing a means to understand and appraise the new frontier of authorship in the age of generative AI.

#### **Works cited**

1. Detecting AI-Generated Text with Pre-Trained ... \- ACL Anthology, accessed August 29, 2025, [https://aclanthology.org/2024.icon-1.21.pdf](https://aclanthology.org/2024.icon-1.21.pdf)  
2. Detecting and Unmasking AI-Generated Texts through Explainable Artificial Intelligence using Stylistic Features \- Semantic Scholar, accessed August 29, 2025, [https://pdfs.semanticscholar.org/7852/53903e072b1915387e83a0a1351bcee2ddaa.pdf](https://pdfs.semanticscholar.org/7852/53903e072b1915387e83a0a1351bcee2ddaa.pdf)  
3. What's the Relationship Between Perplexity and Burstiness? \- Generative AI, accessed August 29, 2025, [https://generativeai.pub/whats-the-relationship-between-perplexity-and-burstiness-4cfd9907df29](https://generativeai.pub/whats-the-relationship-between-perplexity-and-burstiness-4cfd9907df29)  
4. How Do AI Detectors Work? Key Methods, Accuracy, and Limitations \- Grammarly, accessed August 29, 2025, [https://www.grammarly.com/blog/ai/how-do-ai-detectors-work/](https://www.grammarly.com/blog/ai/how-do-ai-detectors-work/)  
5. Why AI Detection Tools are Ineffective | Center for Academic Innovation, accessed August 29, 2025, [https://facultyhub.chemeketa.edu/technology/generative-ai/why-ai-detection-tools-are-ineffective/](https://facultyhub.chemeketa.edu/technology/generative-ai/why-ai-detection-tools-are-ineffective/)  
6. Problems and Challenges of AI-Generated Text Detectors \- Antispoofing Wiki, accessed August 29, 2025, [https://antispoofing.org/problems-and-challenges-of-ai-generated-text-detectors/](https://antispoofing.org/problems-and-challenges-of-ai-generated-text-detectors/)  
7. Statistically-augmented Neural Detection of AI-generated text \- Stanford University, accessed August 29, 2025, [https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1234/final-reports/final-report-169358982.pdf](https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1234/final-reports/final-report-169358982.pdf)  
8. Can You Detect the Difference? \- arXiv, accessed August 29, 2025, [https://arxiv.org/pdf/2507.10475?](https://arxiv.org/pdf/2507.10475)  
9. Understanding the Challenges in AI Text Detection \- AI Checker Free 100%, accessed August 29, 2025, [https://aichecker.app/understanding-the-challenges-in-ai-text-detection/](https://aichecker.app/understanding-the-challenges-in-ai-text-detection/)  
10. Analysing Perplexity and Burstiness in AI vs. Human Text | by ..., accessed August 29, 2025, [https://medium.com/@jhanwarsid/human-contentanalysing-perplexity-and-burstiness-in-ai-vs-human-text-df70fdcc5525](https://medium.com/@jhanwarsid/human-contentanalysing-perplexity-and-burstiness-in-ai-vs-human-text-df70fdcc5525)  
11. Observability in Generative AI with Azure AI Foundry, accessed August 29, 2025, [https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/observability](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/observability)  
12. medium.com, accessed August 29, 2025, [https://medium.com/@jhanwarsid/human-contentanalysing-perplexity-and-burstiness-in-ai-vs-human-text-df70fdcc5525\#:\~:text=Lower%20perplexity%20for%20AI%20text,less%20variation%20in%20sentence%20length.](https://medium.com/@jhanwarsid/human-contentanalysing-perplexity-and-burstiness-in-ai-vs-human-text-df70fdcc5525#:~:text=Lower%20perplexity%20for%20AI%20text,less%20variation%20in%20sentence%20length.)  
13. Perplexity of fixed-length models \- Hugging Face, accessed August 29, 2025, [https://huggingface.co/docs/transformers/perplexity](https://huggingface.co/docs/transformers/perplexity)  
14. Perplexity for LLM Evaluation \- GeeksforGeeks, accessed August 29, 2025, [https://www.geeksforgeeks.org/nlp/perplexity-for-llm-evaluation/](https://www.geeksforgeeks.org/nlp/perplexity-for-llm-evaluation/)  
15. AI detectors: operation, limitations and comparison \- Innovatiana, accessed August 29, 2025, [https://www.innovatiana.com/en/post/ai-content-detector](https://www.innovatiana.com/en/post/ai-content-detector)  
16. Identifying artificial intelligence-generated content using the DistilBERT transformer and NLP techniques \- PMC, accessed August 29, 2025, [https://pmc.ncbi.nlm.nih.gov/articles/PMC12217667/](https://pmc.ncbi.nlm.nih.gov/articles/PMC12217667/)  
17. Exploring the Limitations of Detecting Machine-Generated Text \- ACL Anthology, accessed August 29, 2025, [https://aclanthology.org/2025.coling-main.288.pdf](https://aclanthology.org/2025.coling-main.288.pdf)  
18. iamjr15/Ensemble-AI-Text-Detection: This project detects AI ... \- GitHub, accessed August 29, 2025, [https://github.com/iamjr15/Ensemble-AI-Text-Detection](https://github.com/iamjr15/Ensemble-AI-Text-Detection)  
19. 4 Ways AI Content Detectors Work To Spot AI \- Surfer SEO, accessed August 29, 2025, [https://surferseo.com/blog/how-do-ai-content-detectors-work/](https://surferseo.com/blog/how-do-ai-content-detectors-work/)  
20. Detecting AI Generated Text Based on NLP and Machine Learning Approaches \- arXiv, accessed August 29, 2025, [https://arxiv.org/abs/2404.10032](https://arxiv.org/abs/2404.10032)  
21. Techniques to Tell When You're Reading AI-Generated Text \- DeepLearning.AI, accessed August 29, 2025, [https://www.deeplearning.ai/the-batch/techniques-to-tell-when-youre-reading-ai-generated-text/](https://www.deeplearning.ai/the-batch/techniques-to-tell-when-youre-reading-ai-generated-text/)  
22. Watermarking for Large Language Models: A Survey \- MDPI, accessed August 29, 2025, [https://www.mdpi.com/2227-7390/13/9/1420](https://www.mdpi.com/2227-7390/13/9/1420)  
23. No Free Lunch in LLM Watermarking: Trade-offs in Watermarking Design Choices, accessed August 29, 2025, [https://blog.ml.cmu.edu/2024/09/27/no-free-lunch-in-llm-watermarking-trade-offs-in-watermarking-design-choices/](https://blog.ml.cmu.edu/2024/09/27/no-free-lunch-in-llm-watermarking-trade-offs-in-watermarking-design-choices/)  
24. A Watermark for Large Language Models \- arXiv, accessed August 29, 2025, [https://arxiv.org/abs/2301.10226](https://arxiv.org/abs/2301.10226)  
25. On the Reliability of Watermarks for Large Language Models \- OpenReview, accessed August 29, 2025, [https://openreview.net/forum?id=DEJIDCmWOz](https://openreview.net/forum?id=DEJIDCmWOz)  
26. Watermarks for Language Models: a Cryptographic Perspective \- IACR, accessed August 29, 2025, [https://iacr.org/cryptodb/data/paper.php?pubkey=35385](https://iacr.org/cryptodb/data/paper.php?pubkey=35385)  
27. 9 Best Python Natural Language Processing (NLP) Libraries \- Sunscrapers, accessed August 29, 2025, [https://sunscrapers.com/blog/9-best-python-natural-language-processing-nlp/](https://sunscrapers.com/blog/9-best-python-natural-language-processing-nlp/)  
28. spaCy · Industrial-strength Natural Language Processing in Python, accessed August 29, 2025, [https://spacy.io/](https://spacy.io/)  
29. Detecting AI-Generated Text with Python \- YouTube, accessed August 29, 2025, [https://www.youtube.com/watch?v=tf6o\_2A2eok](https://www.youtube.com/watch?v=tf6o_2A2eok)  
30. Feature Selection and Data Visualization \- Kaggle, accessed August 29, 2025, [https://www.kaggle.com/code/kanncaa1/feature-selection-and-data-visualization](https://www.kaggle.com/code/kanncaa1/feature-selection-and-data-visualization)  
31. Top Free AI Content Detection APIs and Open Source models \- Eden AI, accessed August 29, 2025, [https://www.edenai.co/post/top-free-ai-content-detection-apis-and-open-source-models](https://www.edenai.co/post/top-free-ai-content-detection-apis-and-open-source-models)  
32. TypeTruth is a Python library that detects whether a text is written by a human or AI. Ideal for fact-checking and content validation in the age of AI content generators. \- GitHub, accessed August 29, 2025, [https://github.com/bhaskatripathi/TypeTruth](https://github.com/bhaskatripathi/TypeTruth)  
33. Kishanjaisoorya/AI-Text-Detector-python \- GitHub, accessed August 29, 2025, [https://github.com/Kishanjaisoorya/AI-Text-Detector-python](https://github.com/Kishanjaisoorya/AI-Text-Detector-python)  
34. saro0307/AI-detector: Python program designed to distinguish between AI-generated and human-authored text, helping identify the source of written content based on unique characteristics. \- GitHub, accessed August 29, 2025, [https://github.com/saro0307/AI-detector](https://github.com/saro0307/AI-detector)  
35. ai-text-detector · GitHub Topics, accessed August 29, 2025, [https://github.com/topics/ai-text-detector](https://github.com/topics/ai-text-detector)  
36. Best AI Content Detection APIs in 2025 \- Eden AI, accessed August 29, 2025, [https://www.edenai.co/post/best-ai-content-detection-apis](https://www.edenai.co/post/best-ai-content-detection-apis)  
37. Aggregations in Python \- Plotly, accessed August 29, 2025, [https://plotly.com/python/aggregations/](https://plotly.com/python/aggregations/)  
38. Pie charts in Python \- Plotly, accessed August 29, 2025, [https://plotly.com/python/pie-charts/](https://plotly.com/python/pie-charts/)  
39. Radar charts in Python \- Plotly, accessed August 29, 2025, [https://plotly.com/python/radar-chart/](https://plotly.com/python/radar-chart/)  
40. Seaborn Heatmaps: A Guide to Data Visualization \- DataCamp, accessed August 29, 2025, [https://www.datacamp.com/tutorial/seaborn-heatmaps](https://www.datacamp.com/tutorial/seaborn-heatmaps)  
41. Heatmap | Python Graph Gallery, accessed August 29, 2025, [https://python-graph-gallery.com/heatmap/](https://python-graph-gallery.com/heatmap/)  
42. How to create advanced annotations in Matplotlib \- Python Graph Gallery, accessed August 29, 2025, [https://python-graph-gallery.com/advanced-custom-annotations-matplotlib/](https://python-graph-gallery.com/advanced-custom-annotations-matplotlib/)  
43. znstrider/highlight\_text: functions to plot text with  
44. I found 5 AI content detectors that can correctly identify AI text 100% of the time | ZDNET, accessed August 29, 2025, [https://www.zdnet.com/article/i-found-5-ai-content-detectors-that-can-correctly-identify-ai-text-100-of-the-time/](https://www.zdnet.com/article/i-found-5-ai-content-detectors-that-can-correctly-identify-ai-text-100-of-the-time/)  
45. Best AI Detector | Free & Premium Tools Compared \- Scribbr, accessed August 29, 2025, [https://www.scribbr.com/ai-tools/best-ai-detector/](https://www.scribbr.com/ai-tools/best-ai-detector/)  
46. Limitations of AI Detection Algorithms \- A-State Knowledge Base, accessed August 29, 2025, [https://kb.astate.edu/books/authentication-and-proctoring/page/limitations-of-ai-detection-algorithms](https://kb.astate.edu/books/authentication-and-proctoring/page/limitations-of-ai-detection-algorithms)  
47. Bias in Text Embedding Models \- arXiv, accessed August 29, 2025, [https://arxiv.org/html/2406.12138v1](https://arxiv.org/html/2406.12138v1)