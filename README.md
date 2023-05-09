# About

Telegram bot for a convenient way to keep track of which people were at a meeting

# API

- `say /meet [date]` add quated meeting with `date` as `start_date`
- `say /unmeet` remove quated meeting
- `say /was (id )*` add user as participant for quated meeting
- `say /unwas (id )*` remove uses from participants of quated meeting

# Install

```
python3 -m pip install -t requirements.txt
```

Add bot token in env as `API_KEY`.

# Run

```
./main.py
```
