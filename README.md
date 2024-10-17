# AI Text Editor Assistant

This is an AI-powered text editor assistant built using Gradio and OpenAI's GPT-4 model. It allows users to input text and editing instructions, and then receives AI-generated edits and comments.

## Deployment to Render.com

Follow these steps to deploy the application to Render.com:

1. Fork or clone this repository to your GitHub account.

2. Sign up for a Render account at https://render.com if you haven't already.

3. In your Render dashboard, click on "New +" and select "Web Service".

4. Connect your GitHub account and select the repository containing this project.

5. Configure the deployment:
   - Name: Choose a name for your service
   - Environment: Select "Python"
   - Region: Choose the region closest to you or your target audience
   - Branch: Select the branch you want to deploy (usually "main" or "master")
   - Build Command: Leave as `pip install -r requirements.txt`
   - Start Command: `python texteditor_assistant_gradio.py`

6. Add the following environment variable:
   - Key: `OPENAI_API_KEY`
   - Value: Your OpenAI API key

7. Click "Create Web Service" to deploy your application.

Render will now build and deploy your application. Once the deployment is complete, you'll receive a URL where your application is hosted.

## Local Development

To run this application locally:

1. Clone the repository to your local machine.

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set your OpenAI API key as an environment variable:
   ```
   export OPENAI_API_KEY='your-api-key-here'
   ```

4. Run the application:
   ```
   python texteditor_assistant_gradio.py
   ```

5. Open your web browser and navigate to `http://localhost:7860` to use the application.

## Note

Make sure to keep your OpenAI API key confidential and never commit it to version control systems.
