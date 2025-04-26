Here’s your corrected and polished version for the GitHub README:

---

# Tableau Log Analysis with Personalized Fine-tuned GPT Model

This project is a log analyzer built with Flask, powered by a fine-tuned OpenAI GPT model.

You can configure your API key, upload your logs to the server, and the server will use OpenAI to analyze the logs and provide suggestions about the root cause of any identified issues.

## How It Works

![Log Analysis Overview]()

### Prerequisites

- Python 3.6 or higher
- OpenAI API key

### Installation

1. Clone the repository to your local machine:

    ```bash
    git clone git@github.com:slingalaSalesforce/tableau_log_analysis_gpt.git
    cd tableau_log_analysis_gpt
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

    > **Note:** If you have both Python 2 and Python 3 installed, you may need to use `pip3` instead of `pip`.

    The `requirements.txt` file includes:

    - `flask`
    - `openai`

    > **Important:** This project is compatible with OpenAI SDK version `1.72.0`. If requests to OpenAI fail, it may be due to an outdated SDK version. Use `pip show openai` to check your installed version.

3. Fine-tune your model:
   
    Follow the instructions in `fine_tune.py` to train the GPT model with your custom training data.

4. Run the application:

    After your model has been successfully trained, OpenAI will provide you with a model ID. Update `start.py` with your model ID, and then run:

    ```bash
    python start.py
    ```

    > **Note:** You may need to use `python3` depending on your system setup.

5. Open your browser and navigate to [http://localhost:5000/](http://localhost:5000/).

    Upload your log file, select one of the predefined options, or input your own question. Click the **Send** button. Your question and GPT's response will be displayed in the message form.

    ![Tool UI](https://github.com/slingalaSalesforce/tableau_log_analysis_gpt/blob/main/static/img/Tool%20GUI.png)

### Further Development

This is a basic setup for a Tableau log analysis tool. Future improvements can include building more sophisticated systems by fine-tuning OpenAI model parameters further or handling more complex log analysis tasks.

## License

`log_analysis_openai` is available under the MIT License. See [LICENSE](LICENSE) for more details.

---

Would you also like me to help you polish the **fine_tune.py** or **start.py** documentation too if you're planning to include that later? 🚀  
(Helps make it a perfect repo!)
