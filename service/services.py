from aiogram.types import BotCommand


class Lexicon:
    """Storage location for all bot string constants."""

    menu_commands = (
        BotCommand(command="/change", description="Displays a list of available courses."),
        BotCommand(command="/progress", description="Show your progress on the course.")
    )
