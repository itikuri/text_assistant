import gradio as gr
import openai
import json
import re
import os

# Set up OpenAI client
openai.api_key = os.environ.get("OPENAI_API_KEY")
client = openai.OpenAI()

def clean_json_string(json_string):
    json_string = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', json_string)
    try:
        json_obj = json.loads(json_string)
        return json.dumps(json_obj)
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error during cleaning: {e}")
        return json_string

def edit_text(text_to_edit, instructions):
    system_prompt = """You are an AI-driven text editor assistant. Your task is to help users edit and improve their text based on their instructions. The user will provide you with the text to be edited and their instructions for editing. Your response should include the edited text, along with any explanations or comments about the changes made. Preserve all newline characters in the text."""

    # Replace newline characters with a special token
    text_to_edit_tokenized = text_to_edit.replace('\n', '[NEWLINE]')

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Text to edit:\n{text_to_edit_tokenized}\n\nInstructions:\n{instructions}"}
            ],
            functions=[
                {
                    "name": "update_edited_text",
                    "description": "Update the edited text",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "edited_text": {
                                "type": "string",
                                "description": "The edited version of the text"
                            }
                        },
                        "required": ["edited_text"]
                    }
                }
            ],
            function_call={"name": "update_edited_text"}
        )
        
        assistant_message = response.choices[0].message
        function_call = assistant_message.function_call

        if function_call and function_call.name == "update_edited_text":
            try:
                cleaned_arguments = clean_json_string(function_call.arguments)
                edited_text = json.loads(cleaned_arguments)["edited_text"]
                # Replace the special token back with newline characters
                edited_text = edited_text.replace('[NEWLINE]', '\n')
            except json.JSONDecodeError as json_error:
                print(f"JSON Decode Error: {json_error}")
                print(f"Problematic JSON string: {cleaned_arguments}")
                edited_text = text_to_edit  # Keep original text if parsing fails
            
            comments = assistant_message.content if assistant_message.content else ""
            return edited_text, comments
        else:
            comments = assistant_message.content if assistant_message.content else ""
            return text_to_edit, comments
    except Exception as e:
        return text_to_edit, f"An error occurred: {str(e)}"

def clear_text():
    return "", ""

# Create Gradio interface
with gr.Blocks() as iface:
    text_editor = gr.Textbox(lines=15, label="Text Editor", placeholder="Enter your text here...")
    editing_instructions = gr.Textbox(lines=5, label="Editing Instructions", placeholder="Enter your editing instructions here...")
    output_text = gr.Textbox(lines=15, label="Edited Text")
    comments_box = gr.Textbox(lines=5, label="Assistant's Comments")

    # Create Gradio interface
    gr.Interface(
        fn=edit_text,
        inputs=[text_editor, editing_instructions],
        outputs=[output_text, comments_box],
        title="AI Text Editor Assistant",
        description="Enter the text you want to edit and provide instructions. The AI will edit the text and provide comments on the changes made.",
        flagging_mode="never"
    )

    # Add clear button
    clear_button = gr.Button("Clear Text")
    clear_button.click(fn=clear_text, inputs=None, outputs=[output_text, comments_box])

# Launch the app
if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
