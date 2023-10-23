"# Openquest_Hackathon" 
"# Openquest_Hackathon" 
# GitHub README for Submission Checker Discord Bot

## Introduction

This Discord bot is designed to help users keep track of and manage their daily submissions for a challenge, contest, or any other activity. It allows users to submit links for different days and ensures that they don't miss any submissions. This README provides instructions on how to set up and use the bot.

## Features

- Start the challenge: Users can start the challenge to track their daily submissions.
- Submit links: Users can submit links related to the challenge.
- Check validity of links: The bot verifies the validity of the links provided.
- Handle missed submissions: If a user misses a submission for any day, the bot removes them from the challenge.
- Provide feedback: The bot gives feedback to users about their submissions.

## Prerequisites

- Python 3.x
- Discord Developer Account: You need to create a Discord bot on the [Discord Developer Portal](https://discord.com/developers/applications).
- Discord Bot Token: You'll get a bot token for your Discord bot on the Developer Portal.
- Required Libraries: You need to install the required Python libraries using `pip install`.

## Installation

1. Clone the repository to your local machine.

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

2. Install the required libraries using pip.

```bash
pip install discord.py
pip install requests
pip install beautifulsoup4
```

3. Replace `'YOUR_TOKEN'` with your actual bot token in the Python script (`bot.run('YOUR_TOKEN')`).

## Usage

1. Invite the bot to your Discord server using the OAuth2 URL generated in the Discord Developer Portal.
2. Run the Python script to start the bot.

```bash
python your-bot-script.py
```

3. Set up the challenge:

- Use `!startchallenge` to start the challenge. This command is required to track the day of the challenge.
- Use `!submit <link>` to submit a link for the challenge. The bot checks the validity of the link and records it.
- The bot will also check if you have missed a submission, and if so, it will remove you from the challenge.

## Commands

- `!startchallenge`: Start the challenge.
- `!submit <link>`: Submit a link for the challenge.
- Additional custom commands can be added to enhance functionality.

## Repository Structure

- `your-bot-script.py`: The main Python script for the Discord bot.
- `user_csv_data/`: Directory to store user submission data in CSV files.

## Feedback and Support

If you encounter any issues or need assistance, please feel free to open an issue in the repository. We welcome your feedback and contributions!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.