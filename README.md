# TicketTracker

It is a bot designed to automate ticket availability tracking. It reads links from a Google Sheet, checks each link to see if tickets are available, and sends a notification to a designated Telegram channel when they are. The bot also includes an adjustable cooldown timer to prevent duplicate notifications within a specified period.

## Features:

- Reads ticket URLs from a Google Sheet
- Checks each link for ticket availability
- Sends Telegram notifications when tickets become available
- Customizable notification cooldown period

Easily keep track of ticket availability with real-time alerts!

## Prerequisites

- **Generate Google service keys**

  - Navigate to `https://console.cloud.google.com/` and create a new project
  - Select the newly created project from the project selection dropdown menu
  - On the `Enabled API and services` page, click on the `+ Enable APIS AND SERVICES` button

  - Now, search and enable the following services
    - Google Sheets API
    - Google Drive API
  - From the `Credentials` drawer, click on the `+ CREATE CREDENTIALS` button and select the `Service account` option.
  - Now fill the required fields and hit `Create and Continue` button. After that select a role. For simplicity, you can select the role of `owner`
  - Now, you will see a new account added under the `Service account` tab and then click on that new account.

  - Now, go to the `KEYS` tab and click on the `ADD KEY` button and select `Create new key` option.
  - Finally, you will see a pop up of How you want to download the key.
    Select the JSON format

- **Generate Telegram Credentials**

  - search for `BotFather` in Telegram
  - write command `/start`
  - write command `/newbot`
  - give it a name
  - give it an unique username (ends with \_bot)

  - copy the API token: For example 5401329997:AAF2ZHcsn93lj_qkqKGYyZRNNYC_isV_Vh8

  - Now create a channel/group in Telegram
  - Make the bot an admin of the channel
  - Send a hello message in the channel
  - Go to the url`https://api.telegram.org/bot{API_KEY}/getUpdates`to get the chat_id, for example -1002119021579

## Setup

1. Clone the repository using the following command

   ```bash
   git clone https://github.com/md-Salah/ticket-checking
   ```

2. Go to the `ticket-checking` directory

## Installation

1. Create and activate a virtual environment by running the following command

   ```bash
    python -m venv venv

    .\venv\Scripts\activate
   ```

2. Run the following command to install the dependencies

   ```bash
   pip install -r requirements.txt
   ```

## Run

1. Create a `.env` file in the source directory and place the below contents

   ```
   TELEGRAM_BOT_API_KEY=
   TELEGRAM_CHAT_ID=
   ```

2. Now, run the `main.py` file to start the bot

   ```bash
   py main.py
   ```
