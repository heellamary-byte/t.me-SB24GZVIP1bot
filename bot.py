"""
DailyThinking_bot — Telegram Bot
Sends decision-making and reasoning tips on request, or one per day by subscription.

Run locally:
    export BOT_TOKEN="your-token-from-botfather"
    python bot.py

On Railway, set BOT_TOKEN in the Variables tab. Never hard-code it here.
"""

import json
import logging
import os
import random
from datetime import time as dtime

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

SUBSCRIBERS_FILE = "subscribers.json"

# ---------------------------------------------------------------------------
# CONTENT LIBRARY — add new entries any time, nothing else needs to change
# ---------------------------------------------------------------------------

TIPS = [
    {
        "title": "Separate the decision from the outcome",
        "body": (
            "A good decision can still turn out badly, and a poor one can get lucky.\n\n"
            "Judge a choice by the information and reasoning you had at the time, not "
            "only by how it ended."
        ),
    },
    {
        "title": "Write down your reasoning first",
        "body": (
            "Before an important decision, write why you are choosing it and what you "
            "expect to happen.\n\n"
            "Later you can check your thinking honestly instead of rewriting memory."
        ),
    },
    {
        "title": "Ask what would change your mind",
        "body": (
            "Decide in advance what evidence would make you change your view.\n\n"
            "If nothing could, you are defending a belief rather than reasoning."
        ),
    },
    {
        "title": "Consider the opposite",
        "body": (
            "Spend a few minutes arguing the other side as well as its supporters "
            "would.\n\n"
            "It exposes weak spots in your own position before someone else does."
        ),
    },
    {
        "title": "Look for the base rate",
        "body": (
            "Before judging a specific case, ask how often similar cases turn out a "
            "certain way.\n\n"
            "Starting from the general pattern guards against being swayed by one "
            "vivid story."
        ),
    },
    {
        "title": "Don't decide when you're tired or upset",
        "body": (
            "Fatigue and strong emotion narrow your thinking.\n\n"
            "If a decision can wait a day, let it. Important choices deserve a clear "
            "head."
        ),
    },
    {
        "title": "Limit your options",
        "body": (
            "Too many choices make decisions slower and less satisfying.\n\n"
            "Narrow the list to two or three that meet your must-haves, then choose."
        ),
    },
    {
        "title": "Reversible or irreversible?",
        "body": (
            "Easy-to-undo decisions deserve speed. Hard-to-undo ones deserve care.\n\n"
            "Matching your effort to how reversible a choice is saves time and "
            "prevents costly mistakes."
        ),
    },
    {
        "title": "Test the question, not just the answer",
        "body": (
            "A poorly framed question leads to a poor answer however well you reason.\n\n"
            "Ask whether you are solving the real problem or only the one in front "
            "of you."
        ),
    },
    {
        "title": "Beware the first number you hear",
        "body": (
            "Early figures anchor later judgments, even when they are arbitrary.\n\n"
            "Make your own estimate before looking at someone else's."
        ),
    },
    {
        "title": "Seek disagreement on purpose",
        "body": (
            "Ask someone you trust to find the flaws in your plan.\n\n"
            "Agreement feels good, but useful criticism is what improves decisions."
        ),
    },
    {
        "title": "Use a pre-mortem",
        "body": (
            "Imagine the plan has already failed, then list the reasons why.\n\n"
            "It surfaces risks that optimism hides while you can still address them."
        ),
    },
    {
        "title": "Know what you don't know",
        "body": (
            "Mark which parts of a decision rest on facts and which on guesses.\n\n"
            "Being clear about uncertainty makes your conclusions more honest and "
            "easier to revise."
        ),
    },
    {
        "title": "Beware of sunk costs",
        "body": (
            "Effort or money already spent can't be recovered whatever you do next.\n\n"
            "Decide based on future costs and benefits, not on what you've already "
            "invested."
        ),
    },
    {
        "title": "Slow down for the big ones",
        "body": (
            "Quick intuition works for familiar, low-stakes choices.\n\n"
            "For unfamiliar, high-stakes ones, slow deliberate reasoning is worth the "
            "extra time."
        ),
    },
    {
        "title": "Look for what's missing",
        "body": (
            "We tend to reason from the information in front of us.\n\n"
            "Ask what data you don't have and who might see this differently."
        ),
    },
    {
        "title": "Correlation is not causation",
        "body": (
            "Two things moving together doesn't mean one causes the other.\n\n"
            "Look for a third factor, or ask whether the direction could be "
            "reversed."
        ),
    },
    {
        "title": "Define terms before arguing",
        "body": (
            "Many disagreements come from people using the same word differently.\n\n"
            "Agree on what the key terms mean before debating the conclusion."
        ),
    },
    {
        "title": "Review past decisions",
        "body": (
            "Every few months, look back at a few decisions and how they played out.\n\n"
            "Patterns in your own mistakes are some of the most useful lessons you "
            "have."
        ),
    },
    {
        "title": "Aim for 'good enough' sometimes",
        "body": (
            "Chasing the perfect option can cost more than it returns.\n\n"
            "For minor decisions, pick the first option that meets your needs and "
            "move on."
        ),
    },
]

WELCOME_MESSAGE = (
    "Welcome to Daily Thinking.\n\n"
    "This bot sends short, practical tips on decision-making and clear reasoning.\n\n"
    "Commands:\n"
    "/tip - get a random tip\n"
    "/subscribe - get one tip every day\n"
    "/unsubscribe - stop the daily message\n"
    "/help - show this message again"
)

# ---------------------------------------------------------------------------
# SUBSCRIBER STORAGE
# ---------------------------------------------------------------------------


def load_subscribers() -> set:
    if os.path.exists(SUBSCRIBERS_FILE):
        with open(SUBSCRIBERS_FILE, "r") as f:
            return set(json.load(f))
    return set()


def save_subscribers(subs: set) -> None:
    with open(SUBSCRIBERS_FILE, "w") as f:
        json.dump(list(subs), f)


subscribers = load_subscribers()


def format_tip(pick: dict) -> str:
    return f"💭 {pick['title']}\n\n{pick['body']}"


# ---------------------------------------------------------------------------
# COMMAND HANDLERS
# ---------------------------------------------------------------------------


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(WELCOME_MESSAGE)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(WELCOME_MESSAGE)


async def tip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(format_tip(random.choice(TIPS)))


async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    if chat_id in subscribers:
        await update.message.reply_text("You're already subscribed.")
        return
    subscribers.add(chat_id)
    save_subscribers(subscribers)
    await update.message.reply_text(
        "Subscribed. You'll get one tip a day. Send /unsubscribe to stop."
    )


async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    if chat_id not in subscribers:
        await update.message.reply_text("You're not subscribed.")
        return
    subscribers.discard(chat_id)
    save_subscribers(subscribers)
    await update.message.reply_text("You've been unsubscribed.")


async def send_daily_tip(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Runs once a day and sends one random tip to every subscriber."""
    if not subscribers:
        return
    text = format_tip(random.choice(TIPS))
    for chat_id in list(subscribers):
        try:
            await context.bot.send_message(chat_id=chat_id, text=text)
        except Exception as exc:
            logger.warning("Failed to send to %s: %s", chat_id, exc)


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------


def main() -> None:
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise RuntimeError(
            "BOT_TOKEN is not set. Use `export BOT_TOKEN=...` locally or the "
            "Variables tab on Railway."
        )

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("tip", tip))
    application.add_handler(CommandHandler("subscribe", subscribe))
    application.add_handler(CommandHandler("unsubscribe", unsubscribe))

    # Daily message at 09:00 UTC. Change the hour to suit your audience.
    application.job_queue.run_daily(send_daily_tip, time=dtime(hour=9, minute=0))

    logger.info("Bot starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
