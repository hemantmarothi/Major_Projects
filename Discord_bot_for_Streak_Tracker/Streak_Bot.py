import discord
from discord.ext import commands
import csv
import shutil
import requests
import os
from datetime import datetime

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='!', intents=intents)

csv_directory = 'user_csv_data/'

os.makedirs(csv_directory, exist_ok=True)

def is_valid_url(url):
    try:
        response = requests.head(url)
        return response.status_code == 200
    except Exception as e:
        return False

# Create a dictionary to store the challenge start date for each user
challenge_start_date = {}
debarred_list = {}

@bot.command()
async def startchallenge(ctx):
    user_id = ctx.author.id
    if user_id in debarred_list:
        await ctx.send("You have missed some submission, So you are out of the contest")
        return
    if user_id not in challenge_start_date:
        challenge_start_date[user_id] = datetime.now()
        await ctx.send("Challenge has started for you!")
    else:
        await ctx.send("You have already started the challenge and cannot start it again.")

@bot.command()
async def submit(ctx, link: str):
    user_id = ctx.author.id
    if user_id not in challenge_start_date:
        await ctx.send("You need to start the challenge first using !startchallenge.")
        return

    current_time = datetime.now()
    start_date = challenge_start_date[user_id]
    day_number = (current_time - start_date).days + 1  # Calculate the day number

    user_csv_filename = f'{csv_directory}{user_id}.csv'

    # Check if the user's CSV file exists; if not, create it with headers
    if not os.path.exists(user_csv_filename):
        with open(user_csv_filename, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(['User ID', 'Day Number', 'Link', 'Timestamp'])

    timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

    # Check the validity of the link
    if not is_valid_url(link):
        await ctx.send("Invalid link. Please provide a valid URL.")
        return

    # Read the existing CSV data
    with open(user_csv_filename, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        rows = list(csv_reader)

    # Skip the header row
    header = rows[0]
    rows = rows[1:]

    # Check if there's already an entry for the same day
    for row in rows:
        if row[1] == str(day_number):
            row[2] = link
            row[3] = timestamp
            break
    else:
        # If no existing entry is found, create a new one
        rows.append([user_id, day_number, link, timestamp])

    # Write the modified data back to the CSV file, including the header
    with open(user_csv_filename, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(header)
        csv_writer.writerows(rows)

    await ctx.send(f"Submission for Day {day_number} received at {timestamp}, and the link is updated.")

    # Check if the user has missed a submission for any day
    if len(set(int(row[1]) for row in rows)) != day_number:
        # If there are missed days, remove the user from the challenge
        del challenge_start_date[user_id]
        debarred_list[user_id] = True
        user_csv_filename = f'{csv_directory}{user_id}.csv'

        if os.path.exists(user_csv_filename):
            os.remove(user_csv_filename)
        await ctx.send("You've missed a submission and have been removed from the challenge.")


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    if os.path.exists(csv_directory):
        shutil.rmtree(csv_directory)
    os.makedirs(csv_directory, exist_ok=True)

# Replace 'YOUR_TOKEN' with your actual bot token
bot.run('YOUR_TOKEN_HERE')