<div align="center">
    <img src="./media/logo.png" width="250px" />
    <h1 style="underline">keepalive</h1>
    <h3>helping to keep my server alive</h3>
    <img src="https://img.shields.io/github/license/Tch1b0/keepalive" />
    <img src="https://img.shields.io/github/actions/workflow/status/Tch1b0/keepalive/ci.yml?branch=main&label=ci" />
    <img src="https://img.shields.io/github/issues/Tch1b0/keepalive" />
</div>

## demo

<img src="./media/demo.gif" width="400px" />

## why?

There are frequent tasks that I need to do on my server and different processes I need to keep track of.

keepalive does certain tasks for me, asks me for permission for more complex tasks and notifies me if something is wrong with server or my docker containers.

## how does it operate?

keepalive has some jobs that run in a specified interval (sounds like cronjob, but it's different). If it needs my permission for something or I need to decide something, keepalive reaches out to me on telegram to ask me for my permission or my choice. And if something happens, e.g. one of my containers stops working or my storage goes really low, it tells me via telegram and depending on the problem offers solutions.

## when can I get my own keepalive?

The software is currently made to fit my needs, so it isn't generic enough to do the job for the majority of users.

But we can make it generic. Feel free to contribute to help achieving this goal.

However, **if** your needs fit mine and you want to use keepalive in the state it currently is, read [the setting up guide](#setting-up).

## setting up

```sh
$ cd /usr/lib

$ git clone https://github.com/Tch1b0/keepalive

$ cd ./keepalive
```

Now create a `.env` file in the directory you're currently in.
In the file, you need to set the variables `ADMIN_ID` and `BOT_TOKEN`.

The `BOT_TOKEN` needs to be the token of your telegram bot and the `ADMIN_ID` needs to be your telegram id. To get your telegram id you can use a bot like [@userinfobot](https://t.me/userinfobot).

```sh
$ ./cli.sh deploy
```

## requirements

- python >= 3.10

_README generated by [readcli](https://github.com/Tch1b0/readcli)_
