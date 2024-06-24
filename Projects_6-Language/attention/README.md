# README

## Problem Description
The full problem description is available at the following link: [CS50 AI Project 6: Attention](https://cs50.harvard.edu/ai/2024/projects/6/attention/)

## Introduction
This project consists of two main components:

1. **Masked Language Model (BERT)**: 
   - We use the Masked Language Model BERT to predict a masked token within a given sentence. The model will provide three possible predictions for the masked token.
   
2. **Attention Diagrams**: 
   - We generate and analyze attention diagrams to understand what each attention head in each layer focuses on while interpreting the input text.

## Utilization
1. **Setup**:
   - Navigate to the project directory: `cd attention`
   - Install the required dependencies: `pip3 install -r requirements.txt` (only needs to be done once)

2. **Running the Program**:
   - Execute the script: `python mask.py`
   - Input a phrase with a single `[MASK]` token when prompted. For example: "We made a very long trip around the country [MASK]." 
   - The program will output three possible predictions for the `[MASK]` token.
   - Additionally, it will display the tokens identified from the input phrase (included for debugging and learning purposes).

3. **Viewing Attention Diagrams**:
   - The program generates 144 PNG files, each representing the attention values for one of the 12 heads from each of the 12 layers. These files are overwritten each time a phrase is processed.

## Background
Language models like BERT are trained to predict masked words within a sequence of text using the surrounding context. BERT employs a transformer architecture with an attention mechanism, consisting of 12 layers, each with 12 self-attention heads (144 heads in total).

In this project, we use the `transformers` Python library from Hugging Face to:
1. Predict masked words using BERT.
2. Generate diagrams visualizing attention scores for each of the 144 self-attention heads.
3. Analyze these diagrams to infer what the attention heads are focusing on while processing the input text.

## Detailed Steps
### Masked Language Model
1. **Tokenization**:
   - The input text containing a `[MASK]` token is tokenized using `AutoTokenizer`.
   
2. **Prediction**:
   - The masked token is predicted using an instance of `TFBertForMaskedLM`.
   - The top K output tokens are identified and the original sequence is displayed with each predicted token replacing the `[MASK]`.

3. **Attention Visualization**:
   - The `visualize_attentions` function generates diagrams showing the attention values for each of BERT’s attention heads, providing insight into what the model focuses on during interpretation.

### Custom Implementations
- **get_mask_token_index**: Identifies the index of the `[MASK]` token within the input sequence.
- **get_color_for_attention_score**: Converts attention scores to RGB color values for visualization.
- **visualize_attentions**: Generates attention diagrams for each attention head.

## Analysis
The second part of this project involves analyzing the generated attention diagrams. Details of the analysis are documented in `analysis.md`.

### Analysis Documentation (analysis.md)
- **Attention Head Analysis**: Describes three attention heads, identifying relationships between words that the heads seem to focus on.
- **Example Sentences**: Provides two to three example sentences for each identified relationship to illustrate the attention patterns.

### Important Notes
- Attention heads may not always align with human expectations and can sometimes exhibit noise. The goal is to make inferences based on human intuition, not to precisely define each attention head’s role.
```

Feel free to make any additional changes or let me know if there's anything else you'd like to include!