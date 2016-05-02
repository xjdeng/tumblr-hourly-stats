# tumblr-hourly-stats

Are you wondering when your Tumblr followers are online?  Want to schedule your posts during the hours of your day when they're most active and likely to engage with your posts?  Then you'll want this Python script!

## Requirements

- Python 2.7
- UNIX Environment with Cron (i.e. Mac OSX, Linux, etc.)

## Installation

You'll need to install Pytumblr first using the following command:

`pip install pytumblr`

Then clone this repisotory:

```
git clone https://github.com/xjdeng/tumblr-hourly-stats.git
cd tumblr-hourly-stats
```

## Setting Up Tumblr

Make a copy of the example-credentials.csv file and open it

Then log in to your Tumblr account and head over to the [Tumblr API Console](https://github.com/xjdeng/tumblr-hourly-stats)

Click **Register a new application**

Give your application any name you want (I just use something like "testing".

Put your Tumblr blog's URL into "Application Website"

Put anything you want into "Application Description" (i.e. just testing)

Put http://www.tumblr.com/dashboard into "Default callback URL"

Then register your app!

Now, click on **Explore API** for your newly registered app.

Click Python

Now go into the CSV file and copy the values for **consumer key**, **consumer secret**, **token**, and **token secret** into the respective fields.  Make sure there are no extra spaces or any non-alphanumeric characters in any of those fields!!!

## Running It

From the command line, run: `python runme.py <mytumblr.csv>` where you replace <mytumblr.csv> with the CSV file you created in the previous section.

It may take several minutes depending on your # of followers (generally, give it 1-2 minutes for every 1000 followers you have.)

Once it's successfully completed, you'll see a .db file created with your blog's name.

## Scheduling It to Run Every Hour

You'll need to create a cron job for this script to run every hour in order to be effective.  I highly recommend you run it on a UNIX server where you have an account (i.e. a webhosting account) rather than your personal computer.

You'll want the following parameters for a cron job:

`0 * * * * python /path/to/tumblr-hourly-stats/runme.py /path/to/tumblr-hourly-stats/mytumblr.csv`

where you replace `/path/to` with the appropriate path to where you installed this repository.


## Querying Your Results

Run the following in your **tumblr-hourly-stats** directory:

`cat stats_query.txt | sqlite3 <my blog>.db`

where you replace <my blog>.db with the name of your blog or the .db file that's been generated.

The left column of the query is the hour (in GMT time) and the right column is the fraction of your followers that are idle 3600 (1 hour) or less at the beginning of that particular hour.

Let's take a look at an example result:

```
0|0.0791098348887294
1|0.0757225433526012
2|0.0762564991334489
3|0.0818915801614764
4|0.0772111783347738
5|0.0731145653425446
6|0.0612597066436583
7|0.0617993676343777
8|0.0542635658914729
9|0.046758462421113
10|0.0456110154905336
11|0.0441767068273092
12|0.0521788990825688
13|0.0527220630372493
14|0.0603892386949056
15|0.0692219679633867
16|0.0877644368210406
17|0.0874785591766724
18|0.0845955987424979
19|0.0896886603827478
20|0.0821448944666286
21|0.0832383124287343
22|0.0877742946708464
23|0.08520946138501
```

See the entry `13|0.0527220630372493`?  This means at 13:00 (or 1:00pm) GMT, 0.0527 or about 5% of your followers were idle for 1 hour or less.

If you got a result like this, you'd probably want to schedule more posts around 0:00 - 4:00 and 16:00 - 23:00 GMT.

If converting from GMT to your local time is confusing, consider changing your Timezone to **GMT Azores** in your Tumblr blog's settings!


