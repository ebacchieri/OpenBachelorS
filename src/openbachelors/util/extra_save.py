import os
import json

from psycopg.types.json import Json

from ..const.json_const import true, false, null
from .db_manager import IS_DB_READY, get_db_conn_or_pool, create_user_if_necessary
from .const_json_loader import SavableThing


class BasicExtraSave:
    @classmethod
    def get_default_save_obj(cls):
        return {
            "received_mail_lst": [],
            "removed_mail_lst": [],
            "received_message_lst": [],
        }

    def reset(self):
        self.save_obj = ExtraSave.get_default_save_obj()


class ExtraSave(BasicExtraSave, SavableThing):
    @classmethod
    async def create(cls, filepath: str):
        extra_save = cls()
        extra_save.filepath = filepath

        if os.path.isfile(extra_save.filepath):
            with open(extra_save.filepath, encoding="utf-8") as f:
                extra_save.save_obj = json.load(f)
        else:
            extra_save.save_obj = ExtraSave.get_default_save_obj()

        return extra_save

    async def save(self):
        dirpath = os.path.dirname(self.filepath)
        os.makedirs(dirpath, exist_ok=True)

        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.save_obj, f, ensure_ascii=False, indent=4)


class DBExtraSave(BasicExtraSave, SavableThing):
    @classmethod
    async def create(cls, username: str):
        extra_save = cls()
        extra_save.username = username

        await create_user_if_necessary(extra_save.username)

        save_obj = await extra_save.load_save_obj_from_db()
        if not save_obj:
            save_obj = ExtraSave.get_default_save_obj()

        extra_save.save_obj = save_obj

        return extra_save

    async def load_save_obj_from_db(self):
        async with get_db_conn_or_pool() as pool:
            async with pool.connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(
                        "SELECT extra FROM player_data WHERE username = %s",
                        (self.username,),
                    )
                    return (await cur.fetchone())[0]

    async def save(self):
        async with get_db_conn_or_pool() as pool:
            async with pool.connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(
                        "UPDATE player_data SET extra = %s WHERE username = %s",
                        (
                            Json(self.save_obj),
                            self.username,
                        ),
                    )
                    await conn.commit()
