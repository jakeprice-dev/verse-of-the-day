# Verse of The Day

## Summary

A simple Python script that sends a "verse of the day" notification to a Telegram Bot. It uses the [ESV API](https://api.esv.org/) to retrieve the verse/reading/passage.

## Setup

You need to create a `config.yml` file with the following key/values:

```yaml
esv_api_token: <api-token>
readings_file: year_1.txt
telegram_base_url: https://api.telegram.org
telegram_bot_chat_id: 
telegram_bot_token: 
```

You can get an ESV API application and retrieve a token from [here](https://api.esv.org/account/create-application/). You'll also need to create a Telegram Bot.

## Verses/Readings/Passages

Just picking a verse from the bible won't necessarily give you a good verse for the day! [Joshua 10:43](https://www.esv.org/Joshua+10:43/) for example is not gonna be a particuarly thought provoking one!

> Then Joshua returned, and all Israel with him, to the camp at Gilgal.

I couldn't find any decent collections of verses or passages that I could extract the data from (I even asked ChatGPT) but I did find an interesting source in OpenBible's [Topical Bible](https://www.openbible.info/topics/). The references should hopefully lead to verses/passages that are more helpful then the one above. The references are provided in a text file [here](https://a.openbible.info/data/topic-scores.zip) and the format of the references was in a format that the ESV API can work with by default.

I've massaged the data a bit to remove all but the verse/passage references, and then removed any duplicates. Rather hilariously to me at least this gives me a list of readings enough for 12,686 days! That'll take me through till when I'm 66!!

Anyway, I've included this file in the repository, it's named `openbible_topical_bible_readings.txt`. It's been shuffled into a random order, and I've then taken the first 365 lines from that file and added a dates column to get my verses for "year 1".

## Usage

I run the script at 9am every morning via a simple cron job on my home server.

```sh
0 9 * * * /usr/bin/docker run --rm --env TZ=Europe/London --volume /srv/data-01/my/files/code/verse-of-the-day:/app jakepricedev/docker-pyrunner:latest python3 main.py
```

That sends a notification to Telegram, and I'll get a notification that I can view. 

