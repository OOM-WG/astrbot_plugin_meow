import asyncio
import random
from typing import Dict
from astrbot.api.event.filter import command
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register

@register("astrbot_plugin_meow", "慕容奈依", "喵喵喵", "1.0.0", "https://github.com/OOM-WG/astrbot_plugin_meow")
class MeowPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.groups: set[int] = set()
        self.tasks: Dict[int, asyncio.Task] = {}
        self.meow = [
            "喵",
            "喵喵",
            "喵喵喵",
            "喵呜"
        ]
        self.sym = [
            "···",
            "······",
            "❤️",
            "♡",
            "～",
            "~",
            "?"
        ]
    async def _meow_loop(self, group_id: int, event: AstrMessageEvent):
        try:
            while group_id in self.groups:
                await event.bot.api.send_group_msg(**{
                    "group_id": group_id,
                    "message": [
                        {
                            "type": "text",
                            "data": {
                                "text": f"{random.choice(self.meow)}{random.choice(self.sym)}"
                            }
                        }
                    ]
                })
                await asyncio.sleep(random.randint(45 * 60, 90 * 60))
        except asyncio.CancelledError:
            return
    @filter.permission_type(filter.PermissionType.ADMIN)
    @command("meow")
    async def meow_cmd(self, event: AstrMessageEvent, operation: str = ""):
        if event.get_platform_name() != "aiocqhttp":
            yield event.plain_result("此命令仅在QQ中可用")
            return
        if not event.message_obj.group_id:
            yield event.plain_result("此命令仅在群聊中可用")
            return
        id = event.get_group_id()
        if operation == "off":
            self.groups.discard(id)
            task = self.tasks.pop(id, None)
            if task:
                task.cancel()
            yield event.plain_result("已在本群关闭喵喵喵")
        elif operation == "on":
            if id in self.groups:
                yield event.plain_result("本群已经开启喵喵喵")
                return
            self.groups.add(id)
            self.tasks[id] = asyncio.create_task(self._meow_loop(id, event))
            yield event.plain_result("已在本群开启喵喵喵")
        else:
            yield event.plain_result("用法: /meow [on|off]")