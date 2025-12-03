import asyncio
from database.models import WeiboNote, WeiboNoteComment
from sqlalchemy import select
from database.db_session import get_session
from tools.utils import utils

async def update_reddit_note_as_weibo(note_item: WeiboNote):
    """
    Save Reddit note mapped as WeiboNote
    """
    try:
        async with get_session() as session:
            # Check if exists by note_id
            stmt = select(WeiboNote).where(WeiboNote.note_id == note_item.note_id)
            res = await session.execute(stmt)
            db_note = res.scalar_one_or_none()
            
            if db_note:
                # Update existing note
                db_note.last_modify_ts = utils.get_current_timestamp()
                # Update fields if necessary, for now we assume note_item has latest content
                db_note.content = note_item.content
                db_note.liked_count = note_item.liked_count
                db_note.comment_count = note_item.comment_count
                db_note.shared_count = note_item.shared_count
                db_note.nickname = note_item.nickname
                db_note.user_id = note_item.user_id
                db_note.avatar = note_item.avatar
                db_note.note_url = note_item.note_url
                db_note.ip_location = note_item.ip_location
                db_note.source_keyword = note_item.source_keyword
                
                utils.logger.info(f"[Store] Note {note_item.note_id} already exists, updated.")
            else:
                # Insert new note
                note_item.add_ts = utils.get_current_timestamp()
                note_item.last_modify_ts = utils.get_current_timestamp()
                session.add(note_item)
                utils.logger.info(f"[Store] Note {note_item.note_id} saved.")
            
            await session.commit()
                
    except Exception as e:
        utils.logger.error(f"[Store] Failed to save note: {e}")
