import pytest

from main import process_start_command


class TestStartHandler:
    @pytest.mark.asyncio
    async def test_start_handler(self, message):
        await process_start_command(None)
